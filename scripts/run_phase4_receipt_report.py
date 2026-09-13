"""Phase 4 secondary question report (PROTOCOL.md A9, amendment 1.8), rendered from run_phase4_receipt.py tables."""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.describe import income_group_levels, load_reporting_config, rurality_levels
from seer_study.disclosure import publishable_summary
from seer_study.report import assert_style, md_table
from seer_study.standardise import agreement_label

MODEL_LABEL = {"logistic": "penalised logistic regression", "lightgbm": "LightGBM"}
OUTCOME = "% with a recorded curative treatment"


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _interval(row) -> str:
    return f"{100 * row['estimate']:.2f} ({100 * row['lower']:.2f} to {100 * row['upper']:.2f})"


def _ordered(table: pd.DataFrame, column: str, levels) -> pd.DataFrame:
    order = {level: i for i, level in enumerate(levels)}
    return table.assign(_order=table[column].map(order)).sort_values("_order", kind="stable").drop(columns="_order")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase4_receipt.md"))
    args = parser.parse_args()

    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling, features = acfg.modelling, acfg.features
    minimum = modelling.min_meaningful_percentage_points
    groups = list(acfg.receipt.risk_groups)
    strata = ["all", *groups]
    stratum_label = {"all": f"{' and '.join(groups)} risk (pooled)", **{g: f"{g} risk" for g in groups}}
    t = args.tables_dir

    def publish(table: pd.DataFrame, by: list[str], levels: dict) -> pd.DataFrame:
        renamed = table.rename(columns={"n_recorded": "n_delayed", "pct_recorded": "pct_delayed"}).assign(median_days=np.nan, p90_days=np.nan)
        out = publishable_summary(renamed, rcfg.small_count_threshold, rcfg.suppression_mask, rcfg.cross_tab_count_rounding)
        out = out.drop(columns=["median_days", "p90_days"])
        for column in reversed(by):
            out = _ordered(out, column, levels[column])
        return out.rename(
            columns={"n": "men", "pct_delayed": OUTCOME, "risk_group": "risk group",
                     "county_income_quartile": "county income quartile", "marital_status": "marital status"}
        )

    levels = {
        "risk_group": groups,
        "rurality": rurality_levels(rcfg),
        "county_income_quartile": income_group_levels(rcfg),
        "marital_status": features.marital_labels,
    }
    crude = {
        by: publish(pd.read_csv(t / f"receipt_crude_{by}.csv"), by.replace("risk_group_", "risk_group|").split("|"), levels)
        for by in ("risk_group", "risk_group_rurality", "risk_group_county_income_quartile", "risk_group_marital_status")
    }
    by_risk = pd.read_csv(t / "receipt_crude_risk_group.csv")

    metrics = pd.read_csv(t / "receipt_step_metrics.csv")
    increments = pd.read_csv(t / "receipt_increments.csv")
    tuning = pd.read_csv(t / "receipt_tuning.csv")
    profiles = pd.read_csv(t / "receipt_profiles.csv")
    area_income = pd.read_csv(t / "receipt_area_income.csv").set_index("rurality")

    step2 = metrics[metrics["step"] == 2].set_index(["stratum", "model"])
    inc = increments.set_index(["stratum", "model", "comparison"])
    headline = []
    for stratum in strata:
        for model in ("logistic", "lightgbm"):
            skill2 = step2.loc[(stratum, model), "log_loss_skill"]
            social = inc.loc[(stratum, model, "social position (step 1 to 2)")]
            headline.append(
                {
                    "stratum": stratum_label[stratum],
                    "model": MODEL_LABEL[model],
                    "skill at step 2": f"{100 * skill2:.2f}",
                    "clinical need added": _interval(inc.loc[(stratum, model, "clinical need (step 0 to 1)")]),
                    "social position added": _interval(social),
                    "social position as % of step 2 skill": f"{100 * social['estimate'] / skill2:.0f}" if skill2 > 0 else "n/a",
                    "AUC at step 2": f"{step2.loc[(stratum, model), 'auc']:.3f}",
                    "calibration slope at step 2": f"{step2.loc[(stratum, model), 'calibration_slope']:.2f}",
                }
            )
    social_rows = increments[increments["comparison"] == "social position (step 1 to 2)"]
    above = int((social_rows["lower"] > 0).sum())
    skill_by_model = step2["log_loss_skill"].unstack("model")
    lightgbm_better = int((skill_by_model["lightgbm"] > skill_by_model["logistic"]).sum())
    c_grid = modelling.logistic_c_grid
    logistic_c = tuning[tuning["model"] == "logistic"].set_index("stratum")["C"]
    edge_strata = [stratum_label[s] for s in strata if logistic_c[s] in (min(c_grid), max(c_grid))]

    pv = profiles.pivot_table(index=["stratum", "profile"], columns="model", values="standardised %")
    remote, metro = features.rurality_labels[-1], modelling.reference_rurality
    single = next(label for label in features.marital_labels if label.startswith("Single"))
    contrast_rows = []
    for stratum in strata:
        for title, value in (
            ("all social features as observed minus reference profile", pv.loc[(stratum, "as observed")] - pv.loc[(stratum, "reference profile")]),
            (f"area: {rcfg.rurality_display[remote]} minus {rcfg.rurality_display[metro]}, each at its typical county income",
             pv.loc[(stratum, f"area: {remote}")] - pv.loc[(stratum, f"area: {metro}")]),
            (f"marital status: {single} minus {modelling.reference_marital}",
             pv.loc[(stratum, f"marital status: {single}")] - pv.loc[(stratum, "reference profile")]),
        ):
            contrast_rows.append(
                {"stratum": stratum_label[stratum], "contrast": title,
                 MODEL_LABEL["logistic"]: f"{value['logistic']:.1f}", MODEL_LABEL["lightgbm"]: f"{value['lightgbm']:.1f}",
                 "agreement": agreement_label(value["logistic"], value["lightgbm"], minimum)}
            )

    def profile_name(profile: str) -> str:
        if profile.startswith("area: "):
            label = profile[len("area: "):]
            return f"area: {rcfg.rurality_display[label]}, typical county income ({area_income.loc[label, 'income band']})"
        return profile

    pooled = pv.loc["all"].reindex(columns=["logistic", "lightgbm"])
    profile_order = ["as observed", "reference profile", *[f"area: {l}" for l in features.rurality_labels],
                     *[f"marital status: {l}" for l in features.marital_labels]]
    pooled = pooled.reindex(profile_order).reset_index()
    pooled["profile"] = pooled["profile"].map(profile_name)
    pooled = pooled.rename(columns=MODEL_LABEL)

    risk_lines = [
        f"{r.risk_group} risk {r.pct_recorded:.1f}%" for r in _ordered(by_risk, "risk_group", groups).itertuples()
    ]
    area_lines = "\n".join(f"- {rcfg.rurality_display[label]}: {area_income.loc[label, 'income band']}" for label in features.rurality_labels)

    lines = [
        "# Phase 4, part 5. Secondary question: recorded curative treatment",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_receipt_report.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` A9 with amendment 1.8. All results are associations, not causal effects.",
        "## What is measured",
        f"- **Men:** {' and '.join(groups)}-risk men meeting every cohort step before treatment (first primary, localised or "
        f"regional stage, not a death certificate or autopsy case, aged 40 or over, diagnosed {acfg.cohort.year_min} to "
        f"{acfg.cohort.year_max}).",
        "- **Outcome:** a record of radical prostatectomy or radiotherapy in the first course of treatment.",
        "- **What no record can mean:** active surveillance or watchful waiting, hormone therapy only, refusal, or treatment that "
        "was not captured. SEER under-captures treatment given outside reporting facilities, especially radiotherapy "
        "(`PROTOCOL.md` section 9). The data do not record why a man had no recorded curative treatment, so a lower percentage "
        "cannot be read as under-treatment, and a higher percentage is not necessarily better.",
        "- **Risk groups:** summary stage partly uses surgical pathology, so risk groups are better informed for men who had "
        "surgery than for men who did not.",
        "- **Models:** ordered steps 0 to 2 (year; clinical need; social position) for both model types, tuned once per model and "
        f"stratum on step 2. Intervals are {modelling.interval_level:.0%} cluster bootstrap intervals ({modelling.bootstrap_resamples} "
        "resamples over rurality by county income cells).",
        "## Summary",
        f"- **Crude:** a recorded curative treatment for {', '.join(risk_lines)}.",
        f"- **Predictability:** AUC at step 2 ranged from {step2['auc'].min():.3f} to {step2['auc'].max():.3f} (0.5 is chance), "
        f"and log-loss skill from {100 * step2['log_loss_skill'].min():.2f}% to {100 * step2['log_loss_skill'].max():.2f}%.",
        f"- **Social position increment:** the interval lay above 0 in {above} of {len(social_rows)} stratum and model combinations.",
        f"- **LightGBM against penalised logistic regression:** LightGBM had higher step 2 skill in {lightgbm_better} of "
        f"{len(skill_by_model)} strata.",
        "- **Tuning:** penalised logistic regression chose C = "
        + ", ".join(f"{logistic_c[s]:g} ({stratum_label[s]})" for s in strata)
        + (f"; at an edge of the grid in: {', '.join(edge_strata)}." if edge_strata else "; none at an edge of the grid."),
        "## Crude percentages",
        f"Numbers of men are rounded to the nearest {rcfg.cross_tab_count_rounding}. Statistics resting on 1 to "
        f"{rcfg.small_count_threshold - 1} men are hidden, and a percentage is hidden when 1 to {rcfg.small_count_threshold - 1} "
        "men in the row did, or did not, have a recorded curative treatment.",
        "### By risk group",
        md_table(crude["risk_group"]),
        "### By risk group and county rurality",
        md_table(crude["risk_group_rurality"]),
        "### By risk group and county income quartile",
        md_table(crude["risk_group_county_income_quartile"]),
        "### By risk group and marital status",
        md_table(crude["risk_group_marital_status"]),
        "## Value added at each step",
        "Skill is the percentage reduction in out-of-fold log-loss against step 0 (higher is better). Added values are in "
        "percentage points with intervals. AUC: 0.5 is chance. Calibration slope: 1 is ideal.",
        md_table(pd.DataFrame(headline)),
        "## Standardised percentage with a recorded curative treatment",
        "Each man keeps his own clinical features and year of diagnosis while his social features are set to a profile, using a "
        "model fitted on all men in the stratum at step 2. The reference profile is married, living in a county in a metropolitan "
        f"area of 1 million or more, with county income rank at the {modelling.reference_income_quantile:.2%} quantile of these men. "
        f"Area profiles set rurality and county income together, at the median county income band of men living there:\n{area_lines}",
        f"A difference is described as meaningful only when both model types agree on {minimum:g} percentage points or more in the "
        "same direction (amendment 1.7).",
        "### Contrasts (percentage points)",
        md_table(pd.DataFrame(contrast_rows)),
        f"### Standardised percentages by profile, {stratum_label['all']}",
        md_table(pooled),
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    args.output.write_text(text)
    print(args.output)


if __name__ == "__main__":
    main()
