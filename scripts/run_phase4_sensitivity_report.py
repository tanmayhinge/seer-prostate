"""Phase 4 sensitivity analyses report (PROTOCOL.md A8, amendment 1.8).

Rendered from the tables written by run_phase4_sensitivity.py, alongside the primary results written by
run_phase4_models.py and run_phase4_equity_selection.py.
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
PRIMARY, WIDE_C = "primary", "logistic_wide_c_grid"
SOCIAL = "social position (step 1 to 2)"


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _interval(row) -> str:
    return f"{100 * row['estimate']:.2f} ({100 * row['lower']:.2f} to {100 * row['upper']:.2f})"


def _pct(value) -> str:
    return value if isinstance(value, str) else f"{float(value):.1f}"


def _primary_contrast_key(name: str):
    if name.startswith("all social"):
        return "social"
    if name.startswith("area:"):
        return "area"
    if name.startswith("marital status:"):
        return "marital"
    return None  # one-at-a-time rows are not interpreted (amendment 1.7)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase4_sensitivity.md"))
    args = parser.parse_args()

    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling, features = acfg.modelling, acfg.features
    minimum = modelling.min_meaningful_percentage_points
    primary_threshold = acfg.interval.primary_threshold_days
    scenarios = acfg.sensitivity.scenarios
    order = [PRIMARY, *[s.name for s in scenarios]]
    name = {PRIMARY: "primary analysis", **{s.name: s.description for s in scenarios}}
    threshold = {PRIMARY: primary_threshold, **{s.name: s.threshold_days or primary_threshold for s in scenarios}}
    t = args.tables_dir

    increments = pd.concat(
        [pd.read_csv(t / "model_increments.csv").assign(scenario=PRIMARY), pd.read_csv(t / "sensitivity_increments.csv")],
        ignore_index=True,
    )
    missing = sorted(set(order) - set(increments["scenario"]))
    if missing:
        raise ValueError(f"no sensitivity results for scenario(s) {missing}; run run_phase4_sensitivity.py first")
    social = increments[increments["comparison"] == SOCIAL]
    metrics = pd.concat(
        [pd.read_csv(t / "model_step_metrics.csv").drop(columns="n").assign(scenario=PRIMARY),
         pd.read_csv(t / "sensitivity_step_metrics.csv")],
        ignore_index=True,
    )
    step2 = metrics[metrics["step"] == 2]
    primary_contrasts = pd.read_csv(t / "standardised_contrasts.csv")
    primary_contrasts["contrast"] = primary_contrasts["contrast"].map(_primary_contrast_key)
    contrasts = pd.concat(
        [primary_contrasts.dropna(subset=["contrast"]).assign(scenario=PRIMARY), pd.read_csv(t / "sensitivity_contrasts.csv")],
        ignore_index=True,
    )
    summary = pd.read_csv(t / "sensitivity_delay_summary.csv")
    wide_tuning = pd.read_csv(t / "sensitivity_wide_c_tuning.csv").set_index("stratum")
    primary_tuning = pd.read_csv(t / "model_tuning.csv")
    primary_c = primary_tuning[primary_tuning["model"] == "logistic"].set_index("stratum")["C"]

    # ---- social increment: does the interval stay above 0?
    checks = social[~social["scenario"].isin([PRIMARY, WIDE_C])]
    below = checks[checks["lower"] <= 0]
    exception_lines = [
        f"  - {name[r.scenario]}, {STRATUM_LABEL[r.stratum]}, {MODEL_LABEL[r.model]}: {_interval(r._asdict())}"
        for r in below.itertuples()
    ]
    pooled_ranges = []
    for model in ("logistic", "lightgbm"):
        part = checks[(checks["stratum"] == "all") & (checks["model"] == model)]
        low, high = part.loc[part["estimate"].idxmin()], part.loc[part["estimate"].idxmax()]
        pooled_ranges.append(
            f"{MODEL_LABEL[model]} from {100 * low['estimate']:.2f} ({name[low['scenario']]}) to "
            f"{100 * high['estimate']:.2f} ({name[high['scenario']]})"
        )

    # ---- LightGBM against penalised logistic regression at step 2
    skill = step2[step2["scenario"] != WIDE_C].pivot_table(index=["scenario", "stratum"], columns="model", values="log_loss_skill")
    sens_skill = skill.drop(index=PRIMARY, level="scenario")
    lightgbm_better = sens_skill[sens_skill["lightgbm"] > sens_skill["logistic"]]
    not_better = sens_skill[sens_skill["lightgbm"] <= sens_skill["logistic"]].reset_index()
    not_better_lines = [
        f"  - {name[r.scenario]}, {STRATUM_LABEL[r.stratum]}: LightGBM {100 * r.lightgbm:.2f}, logistic regression {100 * r.logistic:.2f}"
        for r in not_better.itertuples()
    ]

    # ---- standardised contrasts
    contrast_table = contrasts.pivot_table(index=["scenario", "stratum", "contrast"], columns="model", values="estimate").reset_index()
    contrast_table["agreement"] = [agreement_label(r.logistic, r.lightgbm, minimum) for r in contrast_table.itertuples()]
    same = f"both models {minimum:g} points or more, same direction"
    remote, metro = features.rurality_labels[-1], modelling.reference_rurality
    contrast_titles = {
        "area": f"Area: {rcfg.rurality_display[remote]} minus {rcfg.rurality_display[metro]}, each at its typical county income",
        "marital": "Marital status: never married minus the reference profile (married)",
        "social": "All social features as observed minus the reference profile",
    }
    contrast_sections, contrast_counts = [], []
    for key, title in contrast_titles.items():
        part = contrast_table[contrast_table["contrast"] == key]
        pooled = part[part["stratum"] == "all"].set_index("scenario").reindex(order).reset_index()
        display = pd.DataFrame(
            {
                "scenario": pooled["scenario"].map(name),
                MODEL_LABEL["logistic"]: pooled["logistic"].map(lambda v: f"{v:.1f}"),
                MODEL_LABEL["lightgbm"]: pooled["lightgbm"].map(lambda v: f"{v:.1f}"),
                "agreement": pooled["agreement"],
            }
        )
        contrast_sections.append(f"### {title}\n\n{md_table(display)}")
        if key in ("area", "marital"):
            primary_sign = np.sign(pooled.loc[pooled["scenario"] == PRIMARY, "logistic"].item())
            others = part[part["scenario"] != PRIMARY]
            agree = others[(others["agreement"] == same) & (np.sign(others["logistic"]) == primary_sign)]
            pooled_others = others[others["stratum"] == "all"]
            pooled_agree = agree[agree["stratum"] == "all"]
            direction = "lower" if primary_sign < 0 else "higher"
            contrast_counts.append(
                f"- **{title.split(':')[0]}:** in the pooled cohort, both models agreed on a difference of {minimum:g} points or "
                f"more in the primary direction ({direction}) in {len(pooled_agree)} of {len(pooled_others)} scenarios, and in "
                f"{len(agree)} of {len(others)} scenario and stratum combinations."
            )

    # ---- Table: delay by scenario
    published = publishable_summary(summary, rcfg.small_count_threshold, rcfg.suppression_mask, rcfg.cross_tab_count_rounding)
    delay_rows = []
    for scenario in order:
        part = published[published["scenario"] == scenario].set_index("risk_group")
        row = {
            "scenario": name[scenario],
            "threshold (days)": threshold[scenario],
            "men": part.loc["all", "n"],
            "% over threshold, all men": _pct(part.loc["all", "pct_delayed"]),
        }
        for group in RISK_GROUPS:
            row[f"% over threshold, {group} risk"] = _pct(part.loc[group, "pct_delayed"]) if group in part.index else "n/a"
        delay_rows.append(row)

    # ---- Table: social increments
    increment_rows = []
    for scenario in order:
        for model in ("logistic", "lightgbm"):
            part = social[(social["scenario"] == scenario) & (social["model"] == model)].set_index("stratum")
            row = {"scenario": name[scenario], "model": MODEL_LABEL[model]}
            for stratum in STRATA:
                row[STRATUM_LABEL[stratum]] = _interval(part.loc[stratum]) if stratum in part.index else "not estimated"
            increment_rows.append(row)

    # ---- Wide C grid (post hoc)
    grid_text = ", ".join(f"{v:g}" for v in acfg.sensitivity.logistic_wide_c_grid)
    primary_log = step2[(step2["scenario"] == PRIMARY) & (step2["model"] == "logistic")].set_index("stratum")["log_loss_skill"]
    primary_lgb = step2[(step2["scenario"] == PRIMARY) & (step2["model"] == "lightgbm")].set_index("stratum")["log_loss_skill"]
    wide_log = step2[step2["scenario"] == WIDE_C].set_index("stratum")["log_loss_skill"]
    primary_social_log = social[(social["scenario"] == PRIMARY) & (social["model"] == "logistic")].set_index("stratum")
    wide_social = social[social["scenario"] == WIDE_C].set_index("stratum")
    wide_rows = []
    for stratum in STRATA:
        edge = bool(wide_tuning.loc[stratum, "at lowest C"]) or bool(wide_tuning.loc[stratum, "at highest C"])
        wide_rows.append(
            {
                "stratum": STRATUM_LABEL[stratum],
                "C chosen (wider grid)": f"{wide_tuning.loc[stratum, 'C']:g}",
                "at an edge of the wider grid": "yes" if edge else "no",
                "logistic step 2 skill, original grid": f"{100 * primary_log[stratum]:.2f}",
                "logistic step 2 skill, wider grid": f"{100 * wide_log[stratum]:.2f}",
                "LightGBM step 2 skill": f"{100 * primary_lgb[stratum]:.2f}",
                "social position added, original grid": _interval(primary_social_log.loc[stratum]),
                "social position added, wider grid": _interval(wide_social.loc[stratum]),
            }
        )
    wide_better = sum(primary_lgb[s] > wide_log[s] for s in STRATA)
    wide_edges = [STRATUM_LABEL[s] for s in STRATA if bool(wide_tuning.loc[s, "at lowest C"]) or bool(wide_tuning.loc[s, "at highest C"])]
    skill_change = [100 * (wide_log[s] - primary_log[s]) for s in STRATA]

    total_checks = len(checks)
    lines = [
        "# Phase 4, part 4. Sensitivity analyses",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_sensitivity_report.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` A8 with amendment 1.8. All results are associations, not causal effects.",
        "## How the checks were run",
        "- **One change at a time:** each scenario rebuilds the cohort with exactly one setting changed from the primary analysis.",
        "- **Models:** steps 0 to 2 are refitted for both model types, with the hyperparameters tuned in the primary analysis for "
        "the same model and stratum. Step 3 and the leave-one-variable-out refits are not repeated.",
        f"- **Intervals:** {modelling.interval_level:.0%} cluster bootstrap intervals ({modelling.bootstrap_resamples} resamples over "
        "rurality by county income cells).",
        f"- **Standardised contrasts:** judged by the agreement rule of amendment 1.7 (both models {minimum:g} percentage points or "
        "more in the same direction).",
        "- **Thresholds:** fewer men wait beyond longer thresholds, so skill and percentage point differences are not directly "
        "comparable across the threshold scenarios.",
        "## Summary",
        f"- **Social position increment:** the {modelling.interval_level:.0%} interval lay above 0 in {total_checks - len(below)} of "
        f"{total_checks} scenario, stratum and model combinations."
        + (" The exceptions were:\n" + "\n".join(exception_lines) if exception_lines else ""),
        f"- **Pooled social position increment across scenarios** (percentage points of log-loss skill): {'; '.join(pooled_ranges)}. "
        f"In the primary analysis it was {100 * social[(social.scenario == PRIMARY) & (social.model == 'logistic') & (social.stratum == 'all')]['estimate'].item():.2f} "
        f"and {100 * social[(social.scenario == PRIMARY) & (social.model == 'lightgbm') & (social.stratum == 'all')]['estimate'].item():.2f}.",
        f"- **LightGBM against penalised logistic regression:** LightGBM had higher step 2 skill in {len(lightgbm_better)} of "
        f"{len(sens_skill)} scenario and stratum combinations."
        + (" Combinations where it did not:\n" + "\n".join(not_better_lines) if not_better_lines else ""),
        *contrast_counts,
        f"- **Wider C grid ({grid_text}, post hoc):** "
        + (
            "the same C was chosen as in the primary analysis in every stratum, so the logistic regression results are "
            "unchanged; the edge of the original grid did not limit the model. "
            if all(wide_tuning.loc[s, "C"] == primary_c[s] for s in STRATA)
            else f"the step 2 skill of penalised logistic regression changed by {min(skill_change):.2f} to {max(skill_change):.2f} points. "
        )
        + f"LightGBM had higher step 2 skill than the re-tuned logistic regression in {wide_better} of {len(STRATA)} strata. "
        + (f"The chosen C was at an edge of the wider grid in: {', '.join(wide_edges)}." if wide_edges else "No chosen C was at an edge of the wider grid."),
        "- **Scenarios that change only part of the analysis:** risk groups from Gleason score and PSA only change which men "
        "fall in each risk stratum but not the pooled cohort or its features, so pooled results equal the primary analysis.",
        "## Percentage waiting beyond the threshold",
        f"Crude percentages. Numbers of men are rounded to the nearest {rcfg.cross_tab_count_rounding}; statistics resting on 1 to "
        f"{rcfg.small_count_threshold - 1} men are hidden. A lower percentage is better.",
        md_table(pd.DataFrame(delay_rows)),
        "## Social position increment by scenario",
        f"Percentage points of out-of-fold log-loss skill added by social position (step 1 to 2), with {modelling.interval_level:.0%} "
        "intervals. Higher means social position predicts more of the delay.",
        md_table(pd.DataFrame(increment_rows)),
        "## Standardised contrasts, all men (pooled)",
        "Percentage points. Contrasts for each risk group are in `reports/phase4_tables/sensitivity_contrasts.csv`.",
        *contrast_sections,
        "## Penalised logistic regression with a wider C grid (post hoc)",
        f"In the primary analysis penalised logistic regression chose C = "
        + ", ".join(f"{primary_c[s]:g} ({STRATUM_LABEL[s]})" for s in STRATA)
        + f" from the grid {', '.join(f'{v:g}' for v in modelling.logistic_c_grid)}. "
        f"Here C was re-tuned on the grid {grid_text} in the primary cohort, using the same tuning procedure, and steps 0 to 2 were "
        "refitted. Skill is in percentage points of log-loss reduction against step 0; higher is better.",
        md_table(pd.DataFrame(wide_rows)),
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    args.output.write_text(text)
    print(args.output)


if __name__ == "__main__":
    main()
