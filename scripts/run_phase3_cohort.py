"""Phase 3: build the primary cohort and write the inclusion flow and Table 1 to reports/phase3.md."""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import CohortOptions, build_cohort
from seer_study.config import load_config
from seer_study.disclosure import suppress_small_cells
from seer_study.describe import (
    TableRow,
    gleason_band,
    gleason_band_levels,
    income_group,
    income_group_levels,
    load_reporting_config,
    period_band,
    period_levels,
    psa_band,
    psa_band_levels,
    rurality_group,
    rurality_levels,
    table_one,
)
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.report import assert_style, fmt_int, md_table
from seer_study.risk import RISK_GROUPS, STAGE_CLASSES

INCLUDED, ZERO, MISSING = "Interval included", "0 days", "Missing interval"


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _describe(frame, acfg, rcfg, threshold, year_max):
    c = acfg.columns
    rank = frame[c.income].map({label: i for i, label in enumerate(acfg.features.income_order, start=1)})
    delayed = frame["delayed"].astype("object").map({True: f"over {threshold} days", False: f"{threshold} days or less"})
    return pd.DataFrame(
        {
            "rurality": rurality_group(frame[c.rurality], acfg.features, rcfg),
            "age": frame[c.age],
            "period": period_band(frame["year_int"], acfg.cohort, rcfg, year_max=year_max),
            "marital": frame[c.marital],
            "income": income_group(rank, acfg.features, rcfg),
            "risk": frame["risk_group"],
            "stage": frame["stage_class"].map(rcfg.stage_display),
            "gleason": gleason_band(frame["gleason_score"], acfg.risk, rcfg),
            "psa": psa_band(frame["psa_value"], acfg.risk),
            "modality": frame["modality"].map(rcfg.modality_display),
            "days": frame["interval_days"],
            "delayed": delayed.fillna("no interval"),
        },
        index=frame.index,
    )


def _rows(acfg, rcfg, threshold, year_max, delayed_levels):
    return [
        TableRow("Age at diagnosis", "age", tuple(acfg.features.age_midpoints)),
        TableRow("Year of diagnosis", "period", period_levels(acfg.cohort, rcfg, year_max=year_max)),
        TableRow("Marital status", "marital", acfg.features.marital_labels),
        TableRow("County median household income (quartile of 16 bands)", "income", income_group_levels(rcfg)),
        TableRow("Risk group", "risk", RISK_GROUPS),
        TableRow("Summary stage", "stage", tuple(rcfg.stage_display[s] for s in STAGE_CLASSES)),
        TableRow("Clinical Gleason score", "gleason", gleason_band_levels(acfg.risk, rcfg)),
        TableRow("PSA (ng/ml)", "psa", psa_band_levels(acfg.risk)),
        TableRow("First-course treatment", "modality", tuple(rcfg.modality_display.values())),
        TableRow("Days to first recorded treatment", "days", None),
        TableRow(f"Waited more than {threshold} days", "delayed", delayed_levels),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)

    primary = build_cohort(frame, acfg)
    sensitivity = build_cohort(frame, acfg, CohortOptions(include_2023=True, include_zero_days=True))
    threshold = primary.threshold_days
    year_max = acfg.cohort.year_max

    cohort = primary.frame
    described = _describe(cohort, acfg, rcfg, threshold, year_max)
    rurality_order = rurality_levels(rcfg)
    table1 = table_one(
        described,
        group="rurality",
        group_levels=rurality_order,
        rows=_rows(acfg, rcfg, threshold, year_max, (f"{threshold} days or less", f"over {threshold} days")),
    )

    treated = primary.treated
    treated_described = _describe(treated, acfg, rcfg, threshold, year_max)
    treated_described["interval_status"] = np.select(
        [treated["interval_class"].eq("missing").to_numpy(), treated["interval_days"].eq(0).to_numpy()],
        [MISSING, ZERO],
        default=INCLUDED,
    )
    selection_rows = [row for row in _rows(acfg, rcfg, threshold, year_max, ()) if row.column not in ("days", "delayed")]
    selection_rows.insert(0, TableRow("Rurality", "rurality", rurality_order))
    table1b = table_one(
        treated_described, group="interval_status", group_levels=(INCLUDED, ZERO, MISSING), rows=selection_rows
    )

    table1_public = suppress_small_cells(
        table1, ["Overall", *rurality_order], rcfg.small_count_threshold, rcfg.suppression_mask
    )
    table1b_public = suppress_small_cells(
        table1b, ["Overall", INCLUDED, ZERO, MISSING], rcfg.small_count_threshold, rcfg.suppression_mask
    )
    suppression_note = (
        f"Counts of 1 to {rcfg.small_count_threshold - 1} are shown as {rcfg.suppression_mask}, and a second cell is "
        "hidden wherever a row or column total would reveal them (SEER Research Data Use Agreement)."
    )

    def flow_table(result):
        flow = result.flow.copy()
        previous = flow["remaining"].shift(1)
        flow["% of previous step excluded"] = 100.0 * flow["excluded"] / previous
        return flow

    tables_dir = study.paths.reports_dir / "phase3_tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    primary.flow.to_csv(tables_dir / "flow_primary.csv", index=False)
    sensitivity.flow.to_csv(tables_dir / "flow_with_2023_and_zero_days.csv", index=False)
    table1.to_csv(tables_dir / "table1_by_rurality.csv", index=False)
    table1b.to_csv(tables_dir / "table1b_by_interval_status.csv", index=False)

    n = len(cohort)
    delayed_n = int(cohort["delayed"].sum())
    lines = [
        "# Phase 3. Cohort construction",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase3_cohort.py` at git revision "
        f"`{_git_revision()}` (protocol v1.0). Definitions: `PROTOCOL.md` sections 3 to 5 and `config/analysis.yaml`. "
        "Every label in the export is mapped explicitly; an unmapped label stops the run.",
        "## Summary",
        f"- Primary cohort: **{fmt_int(n)}** men diagnosed {acfg.cohort.year_min} to {year_max} whose first course "
        "included radical prostatectomy or radiotherapy, with a recorded interval above 0 days.",
        f"- {fmt_int(delayed_n)} ({100 * delayed_n / n:.1f}% of the cohort) waited more than {threshold} days, the "
        "Australian optimal care pathway benchmark (a lower percentage is better).",
        f"- Among {fmt_int(len(treated))} treated men before the interval steps, {fmt_int(int((treated_described['interval_status'] == MISSING).sum()))} "
        f"have no recorded interval and {fmt_int(int((treated_described['interval_status'] == ZERO).sum()))} have an interval of 0 days. "
        "Table 1b compares these groups with the included men (selection, PROTOCOL.md A7).",
        "## Inclusion flow (primary cohort)",
        "Percentages are of the men remaining at the previous step.",
        md_table(flow_table(primary)),
        "## Inclusion flow with 2023 diagnoses and 0-day intervals retained (sensitivity cohort)",
        "This flow uses the Phase 0 preview definitions and reproduces its counts exactly at every shared step.",
        md_table(flow_table(sensitivity)),
        "## Table 1. Characteristics of the primary cohort by county rurality",
        "Cells are n (% of the column's men), except days, which are median (interquartile range). "
        "Rurality is the county Rural-Urban Continuum Code at diagnosis. " + suppression_note,
        md_table(table1_public),
        "## Table 1b. Treated men by interval status",
        f"Men meeting cohort steps 1 to 6 (n = {fmt_int(len(treated))}). Cells are n (% of the column's men). A "
        "difference in social composition between the included and missing-interval columns would indicate that the "
        "timeliness analysis is selected on social position; PROTOCOL.md A7 bounds this. " + suppression_note,
        md_table(table1b_public),
        "## Not yet done",
        "No outcome model has been fitted. Phase 4 (descriptive timeliness results and the ordered-step models) follows "
        "the protocol without deviation unless an amendment is logged.",
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    report = study.paths.reports_dir / "phase3.md"
    report.write_text(text)
    print(report)


if __name__ == "__main__":
    main()
