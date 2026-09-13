"""Phase 4 descriptive timeliness results (PROTOCOL.md A1) with SEER small-count suppression.

Writes unsuppressed tables to reports/phase4_tables/ (local only, excluded from git) and suppressed tables to
reports/phase4_descriptive.md.
"""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import load_config
from seer_study.describe import income_group, income_group_levels, load_reporting_config, rurality_group, rurality_levels
from seer_study.descriptive import delay_summary
from seer_study.disclosure import publishable_summary
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.report import assert_style, fmt_int, md_table
from seer_study.risk import RISK_GROUPS


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)
    result = build_cohort(frame, acfg)
    cohort = result.frame
    threshold = result.threshold_days
    c = acfg.columns

    rank = cohort[c.income].map({label: i for i, label in enumerate(acfg.features.income_order, start=1)})
    data = pd.DataFrame(
        {
            "risk group": pd.Categorical(cohort["risk_group"], categories=RISK_GROUPS, ordered=True),
            "rurality": pd.Categorical(rurality_group(cohort[c.rurality], acfg.features, rcfg), categories=rurality_levels(rcfg), ordered=True),
            "county income quartile": pd.Categorical(income_group(rank, acfg.features, rcfg), categories=income_group_levels(rcfg), ordered=True),
            "marital status": pd.Categorical(cohort[c.marital], categories=acfg.features.marital_labels, ordered=True),
            "year of diagnosis": cohort["year_int"].astype(str),
            "delayed": cohort["delayed"],
            "days": cohort["interval_days"],
        },
        index=cohort.index,
    )

    specs = [
        ("D1", "By risk group", ["risk group"]),
        ("D2", "By risk group and county rurality", ["risk group", "rurality"]),
        ("D3", "By risk group and county income quartile", ["risk group", "county income quartile"]),
        ("D4", "By risk group and marital status", ["risk group", "marital status"]),
        ("D5", "By year of diagnosis (all risk groups)", ["year of diagnosis"]),
    ]
    rename = {
        "n": "men",
        "n_delayed": f"waited over {threshold} days",
        "pct_delayed": f"% waited over {threshold} days",
        "median_days": "median days",
        "p90_days": "90th percentile days",
    }

    args.tables_dir.mkdir(parents=True, exist_ok=True)
    overall = delay_summary(data, [], "delayed", "days")
    sections = []
    for code, title, by in specs:
        table = delay_summary(data, by, "delayed", "days")
        table.to_csv(args.tables_dir / f"descriptive_{code}.csv", index=False)
        rounding = 1 if code == "D1" else rcfg.cross_tab_count_rounding
        public = publishable_summary(table, rcfg.small_count_threshold, rcfg.suppression_mask, rounding)
        sections.append(f"### {code}. {title}\n\n{md_table(public.rename(columns=rename))}")

    o = overall.iloc[0]
    lines = [
        "# Phase 4, part 1. Descriptive timeliness results",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_descriptive.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` (A1). These are crude descriptive figures: nothing is adjusted, "
        "and no difference here is a tested result.",
        "## Summary",
        f"- Primary cohort: {fmt_int(o['n'])} men. {fmt_int(o['n_delayed'])} ({o['pct_delayed']:.1f}%) waited more than "
        f"{threshold} days from diagnosis to first recorded treatment, the Australian optimal care pathway benchmark "
        "(a lower percentage is better).",
        f"- Median {o['median_days']:.0f} days; 90th percentile {o['p90_days']:.0f} days.",
        "## How to read the tables",
        f"- \"Waited over {threshold} days\" counts men whose first recorded treatment came more than {threshold} days after diagnosis, "
        "including the top-coded group (731 days or more).",
        "- Percentages use the men in that row as the denominator.",
        "- Median and 90th percentile days treat top-coded intervals as 731, so the 90th percentile can be a lower bound.",
        f"- Table D1 shows exact numbers of men. Tables D2 to D5 round the number of men to the nearest "
        f"{rcfg.cross_tab_count_rounding} and do not show delayed counts, so that small groups cannot be recovered by subtraction.",
        f"- Statistics based on 1 to {rcfg.small_count_threshold - 1} men are shown as {rcfg.suppression_mask}. A percentage is also "
        f"hidden when 1 to {rcfg.small_count_threshold - 1} men in that row did, or did not, wait more than {threshold} days "
        "(SEER Research Data Use Agreement).",
        "## Tables",
        *sections,
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    report = study.paths.reports_dir / "phase4_descriptive.md"
    report.write_text(text)
    print(report)


if __name__ == "__main__":
    main()
