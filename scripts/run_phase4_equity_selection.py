"""Phase 4 standardisation, income inequality and selection checks (PROTOCOL.md A5 to A7, amendments 1.6 and 1.7).

Reads the tuned hyperparameters from reports/phase4_tables/model_tuning.csv (written by run_phase4_models.py),
writes aggregate tables to reports/phase4_tables/ and the report to reports/phase4_equity_selection.md.
"""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import load_config
from seer_study.describe import income_group, income_group_levels, load_reporting_config, rurality_group, rurality_levels
from seer_study.disclosure import publishable_bounds, publishable_summary
from seer_study.equity import concentration_curve, erreygers_index
from seer_study.features import build_feature_blocks, design_matrix
from seer_study.increments import bootstrap_increments, cluster_bootstrap_interval
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.models import cross_fit_predictions, fit_full_model
from seer_study.report import assert_style, md_table
from seer_study.risk import RISK_GROUPS
from seer_study.selection import delay_bounds, weighted_percentage
from seer_study.standardise import excess_days_per_1000, set_social_profile

STRATA = ["all", *RISK_GROUPS]
STRATUM_LABEL = {"all": "all men (pooled)", **{group: f"{group} risk" for group in RISK_GROUPS}}
MODEL_LABEL = {"logistic": "penalised logistic regression", "lightgbm": "LightGBM"}


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _params(tuning: pd.DataFrame, stratum: str, kind: str) -> dict:
    row = tuning[(tuning["stratum"] == stratum) & (tuning["model"] == kind)].iloc[0]
    if kind == "logistic":
        return {"C": float(row["C"]), "max_iter": int(row["max_iter"])}
    return {
        "learning_rate": float(row["learning_rate"]),
        "n_estimators": int(row["n_estimators"]),
        "num_leaves": int(row["num_leaves"]),
        "min_child_samples": int(row["min_child_samples"]),
    }


def _agreement(logistic: float, lightgbm: float, minimum: float) -> str:
    if abs(logistic) >= minimum and abs(lightgbm) >= minimum and np.sign(logistic) == np.sign(lightgbm):
        return f"both models {minimum:g} points or more, same direction"
    if abs(logistic) < minimum and abs(lightgbm) < minimum:
        return f"both models under {minimum:g} points"
    return "models disagree"


def _ordered(table: pd.DataFrame, column: str, levels) -> pd.DataFrame:
    order = {level: i for i, level in enumerate(levels)}
    return table.assign(_order=table[column].map(order)).sort_values("_order", kind="stable").drop(columns="_order")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase4_equity_selection.md"))
    parser.add_argument("--bootstrap-resamples", type=int, default=None, help="development only: override")
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling = acfg.modelling
    resamples = args.bootstrap_resamples or modelling.bootstrap_resamples
    seed, clip, level = acfg.seed, modelling.probability_clip, modelling.interval_level
    minimum = modelling.min_meaningful_percentage_points
    c, features = acfg.columns, acfg.features
    tuning = pd.read_csv(args.tables_dir / "model_tuning.csv")

    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)
    result = build_cohort(frame, acfg)
    cohort, threshold = result.frame, result.threshold_days
    blocks = build_feature_blocks(cohort, acfg)
    X2 = design_matrix(blocks, 2)
    y = cohort["delayed"].astype(bool).to_numpy().astype(int)
    clusters = (cohort[c.rurality] + " | " + cohort[c.income]).to_numpy()
    clinical_columns = blocks.columns_by_block["clinical"]
    n_bands = len(features.income_order)

    reference_rank = float(np.nanquantile(X2["income_rank"], modelling.reference_income_quantile))
    reference = {"marital": modelling.reference_marital, "rurality": modelling.reference_rurality, "income_rank": reference_rank}
    area_rank = {
        label: float(np.nanmedian(X2.loc[(cohort[c.rurality] == label).to_numpy(), "income_rank"]))
        for label in features.rurality_labels
    }
    area_band = {label: features.income_order[int(round(rank)) - 1] for label, rank in area_rank.items()}
    band_size = n_bands // rcfg.income_groups
    quartile_ranks = {
        name: (k * band_size) + (band_size + 1) / 2.0 for k, name in enumerate(income_group_levels(rcfg)[: rcfg.income_groups])
    }
    remote, metro = features.rurality_labels[-1], modelling.reference_rurality
    single = next(label for label in features.marital_labels if label.startswith("Single"))
    q_low, q_high = list(quartile_ranks)[0], list(quartile_ranks)[-1]

    def area_name(label):
        return f"area: {rcfg.rurality_display[label]}, typical county income ({area_band[label]})"

    contrast_names = {
        "social": "all social features as observed minus reference profile",
        "area": f"area: {rcfg.rurality_display[remote]} minus {rcfg.rurality_display[metro]}, each at its typical county income",
        "marital": f"marital status: {single} minus {modelling.reference_marital}",
    }

    # ---------------- A5: standardisation
    profile_rows, one_at_a_time_rows, contrast_rows = [], [], []
    for stratum in STRATA:
        mask = np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()
        Xs, ys = X2.loc[mask], y[mask]
        for kind in ("logistic", "lightgbm"):
            interactions = [col for col in clinical_columns if col in Xs.columns] if kind == "logistic" else []
            model = fit_full_model(Xs, ys, kind, _params(tuning, stratum, kind), seed, interactions)

            def predict(**overrides):
                return model.predict_proba(set_social_profile(Xs, features, **{**reference, **overrides}))[:, 1]

            observed = model.predict_proba(Xs)[:, 1]
            at_reference = predict()
            profiles = {"as observed": observed, "reference profile": at_reference}
            for label in features.rurality_labels:
                profiles[area_name(label)] = predict(rurality=label, income_rank=area_rank[label])
            for label in features.marital_labels:
                profiles[f"marital status: {label}"] = predict(marital=label)
            for name, p in profiles.items():
                profile_rows.append({"stratum": stratum, "model": kind, "profile": name, "standardised %": 100.0 * p.mean()})

            one_at_a_time = {}
            for label in features.rurality_labels:
                one_at_a_time[f"rurality only: {rcfg.rurality_display[label]} (county income held at reference)"] = predict(rurality=label)
            for name, rank in quartile_ranks.items():
                one_at_a_time[f"county income only: {name} (rurality held at reference)"] = predict(income_rank=rank)
            for name, p in one_at_a_time.items():
                one_at_a_time_rows.append({"stratum": stratum, "model": kind, "profile": name, "standardised %": 100.0 * p.mean()})

            contrast_rows += [
                {"stratum": stratum, "model": kind, "contrast": contrast_names["social"], "estimate": 100.0 * (observed - at_reference).mean()},
                {"stratum": stratum, "model": kind, "contrast": contrast_names["area"],
                 "estimate": 100.0 * (profiles[area_name(remote)] - profiles[area_name(metro)]).mean()},
                {"stratum": stratum, "model": kind, "contrast": contrast_names["marital"],
                 "estimate": 100.0 * (profiles[f"marital status: {single}"] - at_reference).mean()},
                {"stratum": stratum, "model": kind, "contrast": "_rurality only",
                 "estimate": 100.0 * (one_at_a_time[f"rurality only: {rcfg.rurality_display[remote]} (county income held at reference)"]
                                      - one_at_a_time[f"rurality only: {rcfg.rurality_display[metro]} (county income held at reference)"]).mean()},
                {"stratum": stratum, "model": kind, "contrast": "_income only",
                 "estimate": 100.0 * (one_at_a_time[f"county income only: {q_low} (rurality held at reference)"]
                                      - one_at_a_time[f"county income only: {q_high} (rurality held at reference)"]).mean()},
            ]
            print(f"A5 {stratum} {kind} done", flush=True)

    profiles_table = pd.DataFrame(profile_rows)
    one_at_a_time_table = pd.DataFrame(one_at_a_time_rows)
    contrasts_long = pd.DataFrame(contrast_rows)
    profiles_table.to_csv(args.tables_dir / "standardised_profiles.csv", index=False)
    one_at_a_time_table.to_csv(args.tables_dir / "standardised_profiles_one_at_a_time.csv", index=False)
    contrasts_long.to_csv(args.tables_dir / "standardised_contrasts.csv", index=False)

    contrasts = contrasts_long.pivot_table(index=["stratum", "contrast"], columns="model", values="estimate").reset_index()
    contrasts["agreement"] = [_agreement(r.logistic, r.lightgbm, minimum) for r in contrasts.itertuples()]
    unstable = contrasts[(contrasts["stratum"] == "all") & contrasts["contrast"].str.startswith("_")].set_index("contrast")
    reported = contrasts[~contrasts["contrast"].str.startswith("_")].copy()
    reported = _ordered(_ordered(reported, "contrast", list(contrast_names.values())), "stratum", STRATA)

    # Crude excess days beyond the threshold per 1,000 men
    rank_all = cohort[c.income].map({label: i for i, label in enumerate(features.income_order, start=1)})
    groups = pd.DataFrame(
        {"rurality": rurality_group(cohort[c.rurality], features, rcfg), "county income quartile": income_group(rank_all, features, rcfg)},
        index=cohort.index,
    )
    days = cohort["interval_days"].to_numpy()
    excess_rows = []
    for stratum in STRATA:
        smask = np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()
        for variable, levels in (("rurality", rurality_levels(rcfg)), ("county income quartile", income_group_levels(rcfg))):
            for level_name in levels:
                gmask = smask & (groups[variable] == level_name).to_numpy()
                n = int(gmask.sum())
                excess_rows.append(
                    {"stratum": stratum, "variable": variable, "group": level_name, "n": n,
                     "excess days per 1,000 men (crude)": excess_days_per_1000(days[gmask], threshold) if n >= rcfg.small_count_threshold else np.nan}
                )
    excess_table = pd.DataFrame(excess_rows)
    excess_table.to_csv(args.tables_dir / "excess_days_crude.csv", index=False)

    # ---------------- A6: income inequality in delay
    equity_rows, curves = [], []
    known_income = X2["income_rank"].notna().to_numpy()
    for stratum in STRATA:
        mask = known_income & (np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy())
        ys, ranks, cls = y[mask], X2["income_rank"].to_numpy()[mask], clusters[mask]
        estimate, lower, upper = cluster_bootstrap_interval(
            lambda index, ys=ys, ranks=ranks: erreygers_index(ys[index], ranks[index]), cls, resamples, seed, level
        )
        equity_rows.append({"stratum": stratum, "estimate": estimate, "lower": lower, "upper": upper})
        curve = concentration_curve(ys, ranks)
        curve.insert(0, "stratum", stratum)
        curves.append(curve)
    equity_table = pd.DataFrame(equity_rows)
    equity_table.to_csv(args.tables_dir / "equity_erreygers.csv", index=False)
    pd.concat(curves).to_csv(args.tables_dir / "equity_concentration_curves.csv", index=False)
    print("A6 done", flush=True)

    # ---------------- A7: selection among treated men
    treated = result.treated
    selected = treated[~treated["interval_days"].eq(0)].copy()
    group_levels = {
        "risk group": RISK_GROUPS,
        "rurality": rurality_levels(rcfg),
        "county income quartile": income_group_levels(rcfg),
        "marital status": features.marital_labels,
    }
    selected_groups = pd.DataFrame(
        {
            "rurality": rurality_group(selected[c.rurality], features, rcfg),
            "county income quartile": income_group(
                selected[c.income].map({label: i for i, label in enumerate(features.income_order, start=1)}), features, rcfg
            ),
            "marital status": selected[c.marital],
            "risk group": selected["risk_group"],
            "delayed": selected["delayed"],
        },
        index=selected.index,
    )
    bounds_tables = {}
    for variable, levels in group_levels.items():
        bounds = _ordered(delay_bounds(selected_groups, variable, "delayed"), variable, levels)
        bounds.to_csv(args.tables_dir / f"selection_bounds_{variable.replace(' ', '_')}.csv", index=False)
        bounds_tables[variable] = publishable_bounds(bounds, rcfg.small_count_threshold, rcfg.suppression_mask, rcfg.cross_tab_count_rounding)

    missing = selected["interval_class"].eq("missing").to_numpy().astype(int)
    selected_blocks = build_feature_blocks(selected, acfg)
    membership_params = _params(tuning, "all", "logistic")
    membership_predictions = {}
    for step in (0, 1, 2):
        matrix = design_matrix(selected_blocks, step)
        interactions = [col for col in selected_blocks.columns_by_block["clinical"] if col in matrix.columns]
        membership_predictions[step] = cross_fit_predictions(matrix, missing, "logistic", membership_params, modelling.cv_folds, seed, interactions)
    selected_clusters = (selected[c.rurality] + " | " + selected[c.income]).to_numpy()
    membership = bootstrap_increments(missing, membership_predictions, selected_clusters, resamples, seed, clip, level)
    membership.to_csv(args.tables_dir / "selection_membership_increments.csv", index=False)

    matrix2 = design_matrix(selected_blocks, 2)
    interactions2 = [col for col in selected_blocks.columns_by_block["clinical"] if col in matrix2.columns]
    membership_model = fit_full_model(matrix2, missing, "logistic", membership_params, seed, interactions2)
    p_recorded = 1.0 - membership_model.predict_proba(matrix2)[:, 1]
    recorded = missing == 0
    weights = 1.0 / np.clip(p_recorded[recorded], clip, None)
    delayed_recorded = selected["delayed"].to_numpy()[recorded].astype(bool).astype(int)
    ipw_rows = []
    for variable, levels in group_levels.items():
        if variable == "risk group":
            continue
        labels = selected_groups[variable].to_numpy()[recorded]
        for level_name in levels:
            gmask = labels == level_name
            n = int(gmask.sum())
            if n == 0:
                continue
            n_delayed = int(delayed_recorded[gmask].sum())
            ipw_rows.append(
                {"variable": variable, "group": level_name, "n": n, "n_delayed": n_delayed, "pct_delayed": 100.0 * n_delayed / n,
                 "median_days": weighted_percentage(delayed_recorded[gmask], weights[gmask]), "p90_days": np.nan}
            )
    ipw_raw = pd.DataFrame(ipw_rows)
    ipw_raw.rename(columns={"median_days": "weighted_pct_delayed"}).drop(columns="p90_days").to_csv(args.tables_dir / "selection_ipw.csv", index=False)
    ipw_public = publishable_summary(ipw_raw, rcfg.small_count_threshold, rcfg.suppression_mask, rcfg.cross_tab_count_rounding)
    # The weighted percentage rests on the same small delayed counts as the unweighted one, so it is hidden with it.
    ipw_public.loc[ipw_public["pct_delayed"].eq(rcfg.suppression_mask), "median_days"] = rcfg.suppression_mask
    ipw_public = ipw_public.rename(
        columns={"pct_delayed": f"% over {threshold} days (unweighted)", "median_days": f"% over {threshold} days (weighted)", "n": "men"}
    ).drop(columns="p90_days")
    print("A7 done", flush=True)

    # ---------------- report
    contrast_display = reported.assign(
        stratum=reported["stratum"].map(STRATUM_LABEL),
        **{MODEL_LABEL["logistic"]: reported["logistic"].map(lambda v: f"{v:.1f}"), MODEL_LABEL["lightgbm"]: reported["lightgbm"].map(lambda v: f"{v:.1f}")},
    )[["stratum", "contrast", MODEL_LABEL["logistic"], MODEL_LABEL["lightgbm"], "agreement"]]

    profile_order = ["as observed", "reference profile", *[area_name(label) for label in features.rurality_labels],
                     *[f"marital status: {label}" for label in features.marital_labels]]
    pooled = profiles_table[profiles_table["stratum"] == "all"].pivot(index="profile", columns="model", values="standardised %")
    pooled = pooled.reindex(index=profile_order, columns=["logistic", "lightgbm"]).rename(columns=MODEL_LABEL).reset_index()

    equity_display = _ordered(equity_table, "stratum", STRATA)
    equity_display = equity_display.assign(
        stratum=equity_display["stratum"].map(STRATUM_LABEL),
        **{"Erreygers index (95% interval)": [f"{r.estimate:.3f} ({r.lower:.3f} to {r.upper:.3f})" for r in equity_display.itertuples()]},
    )[["stratum", "Erreygers index (95% interval)"]]

    excess_public = excess_table[excess_table["stratum"].isin(["all", "high"])].copy()
    excess_public["stratum"] = excess_public["stratum"].map(STRATUM_LABEL)
    excess_public["men"] = [
        int(np.floor(v / rcfg.cross_tab_count_rounding + 0.5) * rcfg.cross_tab_count_rounding) if v >= rcfg.small_count_threshold else rcfg.suppression_mask
        for v in excess_public["n"]
    ]
    excess_public["excess days per 1,000 men (crude)"] = [
        f"{v:,.0f}" if pd.notna(v) else rcfg.suppression_mask for v in excess_public["excess days per 1,000 men (crude)"]
    ]
    excess_public = excess_public[["stratum", "variable", "group", "men", "excess days per 1,000 men (crude)"]]

    membership_display = membership.assign(
        **{"skill added, percentage points (95% interval)": [f"{100 * r.estimate:.2f} ({100 * r.lower:.2f} to {100 * r.upper:.2f})" for r in membership.itertuples()]}
    )[["comparison", "skill added, percentage points (95% interval)"]]
    bounds_rename = {
        "n": "men", "pct_delayed_observed": f"% over {threshold} days (recorded men)", "pct_delayed_lower": "lower bound %",
        "pct_delayed_upper": "upper bound %", "pct_missing": "% with no recorded interval",
    }
    rural_only, income_only = unstable.loc["_rurality only"], unstable.loc["_income only"]
    area_lines = "\n".join(f"- {rcfg.rurality_display[label]}: {area_band[label]}" for label in features.rurality_labels)

    lines = [
        f"# Phase 4, part 3. Standardised differences, income inequality and selection",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_equity_selection.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` A5 to A7 with amendments 1.6 and 1.7. All results are "
        "associations, not causal effects.",
        f"## A5. Standardised percentage waiting more than {threshold} days",
        "Each man keeps his own clinical features and year of diagnosis while his social features are set to a profile, "
        "using a model fitted on all men in the stratum at step 2. The mean predicted probability is the standardised "
        "percentage.",
        f"- **Reference profile:** married, living in a county in a metropolitan area of 1 million or more, with county "
        f"income rank {reference_rank:g} of {n_bands} (the cohort's {modelling.reference_income_quantile:.2%} quantile, "
        "the midpoint of the top income tertile).",
        "- **Area profiles** set rurality and county income together, at the median county income band of men living in "
        f"each type of area:\n{area_lines}",
        "- **Why rurality and income are not changed one at a time:** the two are strongly correlated in this cohort, so "
        "holding one fixed while changing the other creates combinations that are rare in the data. The two model types "
        "gave conflicting estimates for such changes. For all men, changing only rurality from "
        f"{rcfg.rurality_display[metro]} to {rcfg.rurality_display[remote]} changed the standardised percentage by "
        f"{rural_only['logistic']:.1f} points under penalised logistic regression and {rural_only['lightgbm']:.1f} under "
        f"LightGBM; changing only county income from {q_high} to {q_low} changed it by {income_only['logistic']:.1f} and "
        f"{income_only['lightgbm']:.1f} points. These one-at-a-time results are not interpreted and are kept in "
        "`reports/phase4_tables/standardised_profiles_one_at_a_time.csv`.",
        f"- **How differences are judged:** bootstrap intervals that hold the fitted model fixed are far narrower than the "
        f"disagreement between model types, so they are not reported. A difference is described as meaningful only when "
        f"both model types agree on {minimum:g} percentage points or more in the same direction.",
        "### Contrasts (percentage points)",
        md_table(contrast_display),
        "### Standardised percentages by profile, all men (pooled)",
        md_table(pooled),
        f"### Crude excess waiting days beyond {threshold} days per 1,000 men",
        "These are crude observed values, not standardised: standardised excess days would need a separate model for the "
        "number of days, which was not built (amendment 1.6). Top-coded intervals count at 731 days. Numbers of men are "
        f"rounded to the nearest {rcfg.cross_tab_count_rounding}.",
        md_table(excess_public),
        "## A6. Income inequality in delay",
        f"Erreygers-corrected concentration index of waiting more than {threshold} days, ranking men by county median "
        "household income (poorest first). It ranges from -1 to 1: a negative value means delay is concentrated in "
        "lower-income counties, a positive value means it is concentrated in higher-income counties, and 0 means no income "
        f"gradient. Men with unknown county income are excluded. Intervals are {level:.0%} cluster bootstrap intervals "
        f"({resamples} resamples over rurality by county income cells).",
        md_table(equity_display),
        "## A7. Selection: men without a recorded interval",
        f"Treated men meeting cohort steps 1 to 6, excluding intervals of 0 days. The lower bound assumes every man without a "
        f"recorded interval waited {threshold} days or less; the upper bound assumes every such man waited longer. Numbers "
        f"of men are rounded to the nearest {rcfg.cross_tab_count_rounding}, and statistics resting on 1 to "
        f"{rcfg.small_count_threshold - 1} men are hidden.",
        *[f"### Bounds by {variable}\n\n{md_table(table.rename(columns=bounds_rename))}" for variable, table in bounds_tables.items()],
        "### Is having a recorded interval predictable from social position?",
        "Out-of-fold penalised logistic regression for having no recorded interval, with the same ordered steps. Skill "
        f"added by social position above 0 means missingness is socially patterned beyond clinical need. Intervals are "
        f"{level:.0%} cluster bootstrap intervals ({resamples} resamples).",
        md_table(membership_display),
        "### Inverse probability weighted percentages",
        f"Percentage of men with a recorded interval who waited more than {threshold} days, unweighted and weighted by the "
        "inverse of each man's predicted probability of having a recorded interval (step 2 membership model).",
        md_table(ipw_public),
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    args.output.write_text(text)
    print(args.output)


if __name__ == "__main__":
    main()
