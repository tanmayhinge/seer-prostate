"""Phase 4 revision report (PROTOCOL.md amendment 1.9), rendered from run_phase4_revision.py tables and earlier
Phase 4 tables. Every analysis here was specified after an internal review of the draft preprint (post-review).
"""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.describe import load_reporting_config
from seer_study.disclosure import publishable_summary
from seer_study.report import assert_style, md_table
from seer_study.risk import RISK_GROUPS
from seer_study.standardise import agreement_label

STRATA = ["all", *RISK_GROUPS]
STRATUM_LABEL = {"all": "all men (pooled)", **{group: f"{group} risk" for group in RISK_GROUPS}}
MODEL_LABEL = {"logistic": "penalised logistic regression", "lightgbm": "LightGBM"}
CLINICAL, SOCIAL = "clinical need (step 0 to 1)", "social position (step 1 to 2)"
CELLS, INCOME_ONLY = "rurality by income cells", "county income band only"


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _points(value: float) -> str:
    return f"{100 * value:.2f}"


def _interval(row) -> str:
    return f"{_points(row['estimate'])} ({_points(row['lower'])} to {_points(row['upper'])})"


def _small(value: float, threshold: int) -> bool:
    return 1 <= value < threshold


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase4_revision.md"))
    args = parser.parse_args()

    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling, revision, features = acfg.modelling, acfg.revision, acfg.features
    minimum, threshold, mask = modelling.min_meaningful_percentage_points, rcfg.small_count_threshold, rcfg.suppression_mask
    t = args.tables_dir

    primary = pd.read_csv(t / "model_increments.csv")
    seeds = pd.read_csv(t / "revision_seed_increments.csv")
    intervals = pd.read_csv(t / "revision_intervals.csv")
    tuning = pd.read_csv(t / "revision_tuning.csv")
    clusters = pd.read_csv(t / "revision_cluster_sizes.csv")
    periods = pd.read_csv(t / "revision_erreygers_by_period.csv")
    income_by_period = pd.read_csv(t / "revision_income_by_period.csv")
    long_intervals = pd.read_csv(t / "revision_long_intervals.csv")
    one_at_a_time = pd.read_csv(t / "standardised_profiles_one_at_a_time.csv")
    sensitivity = pd.read_csv(t / "sensitivity_increments.csv")
    ipw = pd.read_csv(t / "selection_ipw.csv")

    def lookup(frame, **keys):
        part = frame
        for key, value in keys.items():
            part = part[part[key] == value]
        return part.iloc[0]

    # ---- (a) and (b): per-step tuning and fold-seed variability
    main_rows, comparison_rows = [], []
    for stratum in STRATA:
        seed_means = {}
        for model in ("logistic", "lightgbm"):
            s = seeds[(seeds["stratum"] == stratum) & (seeds["model"] == model)]
            seed_means[model] = s.mean(numeric_only=True)
            main_rows.append({
                "stratum": STRATUM_LABEL[stratum],
                "model": MODEL_LABEL[model],
                "social position added, primary (step 3 tuning)": _interval(lookup(primary, stratum=stratum, model=model, comparison=SOCIAL)),
                "social position added, per-step tuning, first fold seed": _interval(lookup(intervals, analysis="per-step tuning", stratum=stratum, model=model, clustering=CELLS, comparison=SOCIAL)),
                f"mean (minimum to maximum) over {len(s)} fold seeds": f"{_points(s[SOCIAL].mean())} ({_points(s[SOCIAL].min())} to {_points(s[SOCIAL].max())})",
                "interval with county income band clusters": _interval(lookup(intervals, analysis="per-step tuning", stratum=stratum, model=model, clustering=INCOME_ONLY, comparison=SOCIAL)),
            })
        comparison_rows.append({
            "stratum": STRATUM_LABEL[stratum],
            "clinical need added, logistic (seed mean)": _points(seed_means["logistic"][CLINICAL]),
            "clinical need added, LightGBM (seed mean)": _points(seed_means["lightgbm"][CLINICAL]),
            "LightGBM clinical model at least as good": "yes" if seed_means["lightgbm"][CLINICAL] >= seed_means["logistic"][CLINICAL] else "no",
            "step 2 skill, logistic (seed mean)": _points(seed_means["logistic"]["step 2 skill"]),
            "step 2 skill, LightGBM (seed mean)": _points(seed_means["lightgbm"]["step 2 skill"]),
        })
    per_step = intervals[(intervals["analysis"] == "per-step tuning") & (intervals["comparison"] == SOCIAL)]
    above_cells = int((per_step[per_step["clustering"] == CELLS]["lower"] > 0).sum())
    above_income = int((per_step[per_step["clustering"] == INCOME_ONLY]["lower"] > 0).sum())
    seed_min_positive = int((seeds.groupby(["stratum", "model"])[SOCIAL].min() > 0).sum())
    n_combinations = len(seeds.groupby(["stratum", "model"]))

    tuning_display = tuning.copy()
    tuning_display["stratum"] = tuning_display["stratum"].map(STRATUM_LABEL)
    tuning_display["model"] = tuning_display["model"].map(MODEL_LABEL)
    tuning_display = tuning_display.fillna("n/a")
    for column in ("max_iter", "n_estimators", "num_leaves", "min_child_samples"):
        tuning_display[column] = [v if v == "n/a" else f"{int(v)}" for v in tuning_display[column]]
    for column in ("C", "learning_rate"):
        tuning_display[column] = [v if v == "n/a" else f"{float(v):g}" for v in tuning_display[column]]
    c_grid = modelling.logistic_c_grid
    logistic_tuning = tuning[tuning["model"] == "logistic"]
    edge = logistic_tuning[logistic_tuning["C"].isin([min(c_grid), max(c_grid)])]

    # ---- (c) clusters
    cluster_display = clusters.assign(
        stratum=clusters["stratum"].map(STRATUM_LABEL),
        median=clusters["median"].map(lambda v: f"{v:,.0f}"),
        largest_share_pct=clusters["largest_share_pct"].map(lambda v: f"{v:.1f}"),
    ).rename(columns={"clusters": "clusters", "smallest": "smallest cluster (men)", "median": "median cluster (men)",
                      "largest": "largest cluster (men)", "largest_share_pct": "largest cluster, % of men"})

    # ---- (d) and (e)
    alt_rows = []
    for analysis in ("stage-free clinical block", "year as categories"):
        part = intervals[intervals["analysis"] == analysis]
        for row in part[part["comparison"].isin([CLINICAL, SOCIAL])].itertuples():
            alt_rows.append({"analysis": analysis, "stratum": STRATUM_LABEL[row.stratum], "model": MODEL_LABEL[row.model],
                             "comparison": row.comparison, "estimate (95% interval)": _interval(row._asdict()),
                             "primary": _interval(lookup(primary, stratum=row.stratum, model=row.model, comparison=row.comparison))})

    # ---- (f) concentration index by period, income quartile distribution by period
    period_display = periods.assign(stratum=periods["stratum"].map(STRATUM_LABEL))
    period_display["Erreygers index (95% interval)"] = [f"{r.estimate:.3f} ({r.lower:.3f} to {r.upper:.3f})" for r in periods.itertuples()]
    period_display = period_display.sort_values(["stratum", "period"])[["stratum", "period", "Erreygers index (95% interval)"]]
    income_by_period = income_by_period.rename(columns={income_by_period.columns[0]: "period"}).set_index("period")
    shares = income_by_period.div(income_by_period.sum(axis=1), axis=0) * 100
    share_display = shares.copy().astype(object)
    for period in income_by_period.index:
        for column in income_by_period.columns:
            count = income_by_period.loc[period, column]
            share_display.loc[period, column] = mask if _small(count, threshold) else f"{shares.loc[period, column]:.1f}"
    share_display = share_display.reset_index()

    # ---- (g) long intervals
    long_display = []
    for row in long_intervals.itertuples():
        long_pct = mask if _small(row.n_long, threshold) or _small(row.n - row.n_long, threshold) else f"{100 * row.n_long / row.n:.1f}"
        top_pct = mask if _small(row.n_top_coded, threshold) or _small(row.n - row.n_top_coded, threshold) else f"{100 * row.n_top_coded / row.n:.2f}"
        if _small(row.n, threshold):
            long_pct = top_pct = mask
        long_display.append({"variable": row.variable, "group": row.group,
                             f"% of men waiting more than {revision.long_interval_days} days": long_pct,
                             "% of men top-coded (731 days or more)": top_pct})

    # ---- (h) one-at-a-time profiles (amendment 1.7) with contrasts
    pivot = one_at_a_time.pivot_table(index=["stratum", "profile"], columns="model", values="standardised %")
    remote, metro = features.rurality_labels[-1], modelling.reference_rurality
    rurality_display = rcfg.rurality_display
    oat_rows = []
    for stratum in STRATA:
        rural = pivot.loc[(stratum, f"rurality only: {rurality_display[remote]} (county income held at reference)")] - \
            pivot.loc[(stratum, f"rurality only: {rurality_display[metro]} (county income held at reference)")]
        income = pivot.loc[(stratum, "county income only: Q1 (lowest) (rurality held at reference)")] - \
            pivot.loc[(stratum, "county income only: Q4 (highest) (rurality held at reference)")]
        for name, value in ((f"rurality only: {rurality_display[remote]} minus {rurality_display[metro]}", rural),
                            ("county income only: Q1 (lowest) minus Q4 (highest)", income)):
            oat_rows.append({"stratum": STRATUM_LABEL[stratum], "contrast": name,
                             MODEL_LABEL["logistic"]: f"{value['logistic']:.1f}", MODEL_LABEL["lightgbm"]: f"{value['lightgbm']:.1f}",
                             "agreement": agreement_label(value["logistic"], value["lightgbm"], minimum)})
    oat_profiles = one_at_a_time.assign(stratum=one_at_a_time["stratum"].map(STRATUM_LABEL), model=one_at_a_time["model"].map(MODEL_LABEL))
    oat_profiles["standardised %"] = oat_profiles["standardised %"].map(lambda v: f"{v:.1f}")

    # ---- surgery-only clinical-need increment (from sensitivity tables)
    surgery_rows = []
    for stratum in STRATA:
        for model in ("logistic", "lightgbm"):
            surgery_rows.append({
                "stratum": STRATUM_LABEL[stratum], "model": MODEL_LABEL[model],
                "clinical need added, primary cohort": _interval(lookup(primary, stratum=stratum, model=model, comparison=CLINICAL)),
                "clinical need added, prostatectomy without radiotherapy only": _interval(lookup(sensitivity, scenario="surgery_only", stratum=stratum, model=model, comparison=CLINICAL)),
            })

    # ---- inverse probability weighting precision, over published rows only
    published = publishable_summary(
        ipw.rename(columns={"weighted_pct_delayed": "median_days"}).assign(p90_days=np.nan), threshold, mask, rcfg.cross_tab_count_rounding
    )
    shown = published["pct_delayed"].ne(mask).to_numpy()
    difference = (ipw["weighted_pct_delayed"] - ipw["pct_delayed"]).abs().to_numpy()[shown]
    large = shown & (ipw["n"].to_numpy() >= 1000)
    difference_large = (ipw["weighted_pct_delayed"] - ipw["pct_delayed"]).abs().to_numpy()[large]

    lines = [
        "# Phase 4, part 6. Revision analyses after internal review (post-review)",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_revision_report.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` amendment 1.9. These analyses were specified after an internal "
        "review of the draft preprint and before they were run. All results are associations, not causal effects.",
        "## Summary",
        f"- **Social position increment under per-step tuning:** the 95% cell-bootstrap interval lay above 0 in {above_cells} of "
        f"{len(per_step[per_step['clustering'] == CELLS])} stratum and model combinations, and in {above_income} of "
        f"{len(per_step[per_step['clustering'] == INCOME_ONLY])} with county income band clusters.",
        f"- **Fold-seed variability:** across {revision.fold_seed_repeats} fold-assignment seeds, the smallest increment was above 0 in "
        f"{seed_min_positive} of {n_combinations} stratum and model combinations.",
        f"- **Logistic regression tuning:** C was chosen at an edge of the grid ({min(c_grid):g} or {max(c_grid):g}) in {len(edge)} of "
        f"{len(logistic_tuning)} stratum and step combinations.",
        f"- **Inverse probability weighting:** among published group percentages, weighting changed the percentage by at most "
        f"{difference.max():.2f} points, and by at most {difference_large.max():.2f} points in groups of 1,000 men or more.",
        "## (a) and (b) Social position increment with per-step tuning and repeated fold assignment",
        "Percentage points of out-of-fold log-loss skill added by social position (step 1 to 2). Intervals are 95% cluster "
        f"bootstrap intervals over out-of-fold predictions from the first fold seed ({modelling.bootstrap_resamples} resamples, no "
        "refitting). The seed range shows how much the estimate moves when men are assigned to different folds; tuning was not "
        "repeated per seed.",
        md_table(pd.DataFrame(main_rows)),
        "### Clinical model comparison under per-step tuning",
        "Where the LightGBM clinical model (step 1) is weaker than the logistic one, a larger LightGBM social increment can partly "
        "reflect that weaker reference. Values are means over fold seeds.",
        md_table(pd.DataFrame(comparison_rows)),
        "### Hyperparameters chosen at each step",
        md_table(tuning_display),
        "## (c) Bootstrap clusters",
        "Clusters are rurality by county income band cells (primary) or county income band alone (coarser alternative). The export "
        "has no county or registry identifier. Cluster sizes of 1 to 4 men are shown as <5.",
        md_table(cluster_display),
        "## (d) Stage-free clinical block and (e) year as categories",
        "Stage-free: summary stage removed from the clinical block, with risk strata unchanged. Year as categories: logistic "
        "regression only, with one indicator per year of diagnosis replacing the linear year and the 2020 indicator. Both reuse the "
        "per-step tuned hyperparameters and the first fold seed.",
        md_table(pd.DataFrame(alt_rows)),
        "## (f) Income concentration index by diagnosis period",
        "Erreygers index of waiting more than 90 days by county income rank within each period; positive values mean delay is "
        "concentrated in higher-income counties. It does not separate income from rurality and is not standardised for clinical "
        "features.",
        md_table(period_display),
        "### County income quartile distribution by period (% of men in the period)",
        md_table(share_display),
        "## (g) Long and top-coded intervals",
        md_table(pd.DataFrame(long_display)),
        "## (h) One-at-a-time rurality and income profiles (amendment 1.7)",
        "These profiles change rurality or county income alone, holding the other at the reference profile. They create "
        "combinations rarely observed in the data, and the two model types conflict; they are not interpreted and are published "
        "as amendment 1.7 stated.",
        "### Contrasts (percentage points)",
        md_table(pd.DataFrame(oat_rows)),
        "### Standardised percentages",
        md_table(oat_profiles),
        "## Clinical need increment when radiotherapy patients are excluded",
        "The interval ends at the first treatment of any kind, which for men having radiotherapy can be hormone therapy. This "
        "compares the clinical need increment in the primary cohort with the prostatectomy-without-radiotherapy scenario (A8).",
        md_table(pd.DataFrame(surgery_rows)),
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    args.output.write_text(text)
    print(args.output)


if __name__ == "__main__":
    main()
