"""Figures and captions for the preprint, from aggregate Phase 3 and Phase 4 tables and saved out-of-fold predictions.

Writes paper/figures/<name>.<format> and paper/figures/captions.md. Calibration bins are written to
reports/phase4_tables/calibration_bins.csv.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.describe import load_reporting_config, rurality_levels
from seer_study.figures import (
    area_and_concentration_figure,
    calibration_bins,
    calibration_figure,
    flow_figure,
    increments_figure,
    load_figure_config,
    plottable_rates,
    rates_figure,
    save_figure,
    sensitivity_figure,
)
from seer_study.report import assert_style
from seer_study.risk import RISK_GROUPS

COMPARISONS = {
    "clinical need (step 0 to 1)": "Clinical need added",
    "social position (step 1 to 2)": "Social position added",
    "pathway (step 2 to 3)": "Treatment type added",
}
SOCIAL = "social position (step 1 to 2)"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--figure-config", type=Path, default=Path("config/figures.yaml"))
    parser.add_argument("--phase3-tables", type=Path, default=Path("reports/phase3_tables"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--predictions-dir", type=Path, default=Path("data/derived/phase4"))
    parser.add_argument("--out-dir", type=Path, default=Path("paper/figures"))
    args = parser.parse_args()

    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    spec = load_figure_config(args.figure_config)
    modelling = acfg.modelling
    threshold = acfg.interval.primary_threshold_days
    t = args.tables_dir
    strata = {key: spec.stratum_labels[key] for key in ["all", *RISK_GROUPS]}
    written, captions = [], []

    def small(values):
        return ((values >= 1) & (values < rcfg.small_count_threshold)).any()

    # Figure 1: inclusion flow
    flow = pd.read_csv(args.phase3_tables / "flow_primary.csv")
    if small(flow["remaining"]) or small(flow["excluded"]):
        raise ValueError("flow has a count of 1 to 4, which cannot be published")
    written += save_figure(flow_figure(flow, spec), "figure1_flow", args.out_dir, spec)
    captions.append(
        "**Figure 1. Inclusion flow for the primary cohort.** Boxes give the number of records remaining after each step, "
        "in protocol order; side boxes give the number excluded at that step. Source: SEER Research Data, 17 registries, "
        "November 2025 submission."
    )

    # Figure 2: crude percentage delayed by risk group and rurality
    d2 = pd.read_csv(t / "descriptive_D2.csv")
    rates = plottable_rates(d2, ["risk group", "rurality"], rcfg.small_count_threshold, rcfg.suppression_mask,
                            rcfg.cross_tab_count_rounding, rcfg.rurality_unknown_display)
    series = [level for level in rurality_levels(rcfg) if level != rcfg.rurality_unknown_display]
    fig = rates_figure(rates, "risk group", "rurality", list(RISK_GROUPS), series, spec,
                       f"% waiting more than {threshold} days")
    written += save_figure(fig, "figure2_delay_by_risk_and_rurality", args.out_dir, spec)
    captions.append(
        f"**Figure 2. Crude percentage of men waiting more than {threshold} days** from diagnosis to first recorded treatment, "
        "by risk group and county rurality. Men with unknown rurality, and percentages resting on 1 to "
        f"{rcfg.small_count_threshold - 1} men, are not shown. Nothing is adjusted."
    )

    # Figure 3: skill added by each block
    increments = pd.read_csv(t / "model_increments.csv")
    written += save_figure(increments_figure(increments, COMPARISONS, strata, spec), "figure3_skill_added", args.out_dir, spec)
    captions.append(
        "**Figure 3. Out-of-fold log-loss skill added by each block of features,** in percentage points, by risk group and "
        f"model type. Blocks are added in order: clinical need, then social position, then treatment type. Bars are "
        f"{modelling.interval_level:.0%} cluster bootstrap intervals ({modelling.bootstrap_resamples} resamples over rurality "
        "by county income cells). The dashed line marks no added skill. The x-axis scale differs between panels. "
        "Associations, not causal effects."
    )

    # Figure 4: standardised area profiles and concentration curves
    profiles = pd.read_csv(t / "standardised_profiles.csv")
    area_names = [p for p in profiles.loc[profiles["stratum"] == "all", "profile"].unique() if p.startswith("area: ")]
    area_profiles = {p: p[len("area: "):].replace(", typical county income ", "\n") for p in area_names}
    curves = pd.read_csv(t / "equity_concentration_curves.csv")
    fig = area_and_concentration_figure(
        profiles, area_profiles, curves, strata, spec,
        titles=("a. Area profiles, all men", "b. Concentration curves"),
        value_label=f"Standardised % waiting more than {threshold} days",
        curve_labels=("Cumulative share of men,\npoorest county income first", f"Cumulative share of men\nwaiting more than {threshold} days"),
    )
    written += save_figure(fig, "figure4_area_and_income", args.out_dir, spec)
    captions.append(
        f"**Figure 4. (a)** Standardised percentage of all men waiting more than {threshold} days when each man's rurality "
        "and county income are set together to each type of area, at the median county income band of men living there, "
        "with his own clinical features and year of diagnosis, and marital status set to married. Points show both model "
        "types; the x-axis does not start at 0. **(b)** Concentration curves of waiting more than "
        f"{threshold} days by county median household income rank, by risk group. A curve below the line of equality means "
        "delay is concentrated among men in higher-income counties. Associations, not causal effects."
    )

    # Supplementary Figure S1: calibration at step 2
    rows = []
    for stratum in strata:
        for model in spec.model_labels:
            saved = np.load(args.predictions_dir / f"{stratum}_{model}.npz")
            table = calibration_bins(saved["y"], saved["step2"], spec.calibration_bins).drop(columns="n")
            rows.append(table.assign(stratum=stratum, model=model))
    bins = pd.concat(rows, ignore_index=True)[["stratum", "model", "bin", "mean_predicted", "observed"]]
    bins.to_csv(t / "calibration_bins.csv", index=False)
    written += save_figure(calibration_figure(bins, strata, spec), "figureS1_calibration", args.out_dir, spec)
    captions.append(
        f"**Supplementary Figure S1. Calibration of out-of-fold predicted probabilities at step 2** (clinical need and social "
        f"position), in {spec.calibration_bins} equal-count bins, by risk group and model type. The dashed line marks perfect "
        "calibration."
    )

    # Supplementary Figure S2: social position increment across sensitivity scenarios, all men
    sens = pd.concat(
        [increments.assign(scenario="primary"), pd.read_csv(t / "sensitivity_increments.csv")], ignore_index=True
    )
    sens = sens[(sens["stratum"] == "all") & (sens["scenario"] != "logistic_wide_c_grid")]
    scenarios = {"primary": "Primary analysis", **{s.name: s.description[0].upper() + s.description[1:] for s in acfg.sensitivity.scenarios}}
    written += save_figure(sensitivity_figure(sens, SOCIAL, scenarios, spec), "figureS2_sensitivity", args.out_dir, spec)
    captions.append(
        "**Supplementary Figure S2. Log-loss skill added by social position under each sensitivity scenario,** all men, with "
        f"{modelling.interval_level:.0%} cluster bootstrap intervals. Each scenario changes one setting from the primary "
        "analysis (`PROTOCOL.md` A8). The threshold scenarios use a different outcome, so their values are not directly "
        "comparable with the others."
    )

    text = "# Figure captions\n\nGenerated by `scripts/make_figures.py`.\n\n" + "\n\n".join(captions) + "\n"
    assert_style(text)
    (args.out_dir / "captions.md").write_text(text)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
