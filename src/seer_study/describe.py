"""Descriptive tables: display bands derived from the analysis thresholds, and Table 1 cells."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import CohortSpec, FeatureSpec, RiskSpec
from seer_study.config import ConfigError, load_typed_yaml
from seer_study.labels import require_known
from seer_study.report import fmt_int

UNKNOWN = "Unknown"


@dataclass(frozen=True)
class ReportingSpec:
    small_count_threshold: int
    suppression_mask: str
    income_groups: int
    year_period_width: int
    gleason_max_display: int
    rurality_display: dict[str, str]
    rurality_unknown_display: str
    modality_display: dict[str, str]
    stage_display: dict[str, str]


@dataclass(frozen=True)
class TableRow:
    label: str
    column: str
    levels: tuple[str, ...] | None  # None means a continuous row, shown as median (IQR)


def load_reporting_config(path: str | Path) -> ReportingSpec:
    spec = load_typed_yaml(path, ReportingSpec)
    if spec.income_groups <= 0 or spec.year_period_width <= 0:
        raise ConfigError("income_groups and year_period_width must be positive")
    return spec


def _fmt_number(value: float) -> str:
    return f"{value:g}"


def gleason_band_levels(risk: RiskSpec, reporting: ReportingSpec) -> tuple[str, ...]:
    return (
        f"{risk.low_max_gleason} or less",
        f"{risk.intermediate_gleason}",
        f"{risk.high_min_gleason} to {reporting.gleason_max_display}",
        UNKNOWN,
    )


def gleason_band(values: pd.Series, risk: RiskSpec, reporting: ReportingSpec) -> pd.Series:
    low, mid, high, unknown = gleason_band_levels(risk, reporting)
    v = values.astype(float)
    bands = np.select(
        [v.isna().to_numpy(), (v <= risk.low_max_gleason).to_numpy(), (v == risk.intermediate_gleason).to_numpy(), (v >= risk.high_min_gleason).to_numpy()],
        [unknown, low, mid, high],
        default="",
    )
    if (bands == "").any():
        raise ValueError("a Gleason score falls outside the configured bands")
    return pd.Series(bands.astype(object), index=values.index)


def psa_band_levels(risk: RiskSpec) -> tuple[str, ...]:
    low, high = _fmt_number(risk.low_psa_below), _fmt_number(risk.high_psa_above)
    return (f"below {low}", f"{low} to {high}", f"above {high}", UNKNOWN)


def psa_band(values: pd.Series, risk: RiskSpec) -> pd.Series:
    below, middle, above, unknown = psa_band_levels(risk)
    v = values.astype(float)
    bands = np.select(
        [v.isna().to_numpy(), (v < risk.low_psa_below).to_numpy(), (v <= risk.high_psa_above).to_numpy()],
        [unknown, below, middle],
        default=above,
    )
    return pd.Series(bands.astype(object), index=values.index)


def income_group_levels(reporting: ReportingSpec) -> tuple[str, ...]:
    k = reporting.income_groups
    names = [f"Q{i}" for i in range(1, k + 1)]
    names[0] += " (lowest)"
    names[-1] += " (highest)"
    return (*names, UNKNOWN)


def income_group(rank: pd.Series, features: FeatureSpec, reporting: ReportingSpec) -> pd.Series:
    n_bands = len(features.income_order)
    if n_bands % reporting.income_groups:
        raise ConfigError(f"{n_bands} income bands cannot be split into {reporting.income_groups} equal groups")
    size = n_bands // reporting.income_groups
    levels = income_group_levels(reporting)
    r = rank.astype(float)
    outside = r.notna() & ((r < 1) | (r > n_bands))
    if outside.any():
        raise ValueError(f"income rank outside 1 to {n_bands}")
    groups = [UNKNOWN if math.isnan(value) else levels[math.ceil(value / size) - 1] for value in r]
    return pd.Series(groups, index=rank.index, dtype=object)


def period_levels(cohort: CohortSpec, reporting: ReportingSpec, year_max: int | None = None) -> tuple[str, ...]:
    end = cohort.year_max if year_max is None else year_max
    width = reporting.year_period_width
    return tuple(f"{start} to {min(start + width - 1, end)}" for start in range(cohort.year_min, end + 1, width))


def period_band(years: pd.Series, cohort: CohortSpec, reporting: ReportingSpec, year_max: int | None = None) -> pd.Series:
    end = cohort.year_max if year_max is None else year_max
    width = reporting.year_period_width
    y = years.astype("int64")
    if ((y < cohort.year_min) | (y > end)).any():
        raise ValueError(f"year outside {cohort.year_min} to {end}")
    starts = cohort.year_min + ((y - cohort.year_min) // width) * width
    return pd.Series([f"{s} to {min(s + width - 1, end)}" for s in starts], index=years.index, dtype=object)


def rurality_levels(reporting: ReportingSpec) -> tuple[str, ...]:
    return (*reporting.rurality_display.values(), reporting.rurality_unknown_display)


def rurality_group(values: pd.Series, features: FeatureSpec, reporting: ReportingSpec) -> pd.Series:
    if set(reporting.rurality_display) != set(features.rurality_labels):
        raise ConfigError("rurality_display must name exactly the analysis rurality labels")
    require_known(values, {*features.rurality_labels, *features.rurality_unknown_labels}, "rurality")
    mapping = {**reporting.rurality_display, **{label: reporting.rurality_unknown_display for label in features.rurality_unknown_labels}}
    return values.map(mapping).astype(object)


def categorical_summary(frame: pd.DataFrame, variable: str, group: str, levels: tuple[str, ...]) -> pd.DataFrame:
    require_known(frame[variable], levels, variable)
    counts = pd.crosstab(frame[group], frame[variable])
    groups = list(dict.fromkeys(frame[group]))
    counts = counts.reindex(index=groups, columns=list(levels), fill_value=0)
    sizes = frame[group].value_counts()
    rows = [
        {"variable": variable, "group": g, "level": level, "n": int(counts.loc[g, level]), "pct": 100.0 * counts.loc[g, level] / sizes[g]}
        for g in groups
        for level in levels
    ]
    return pd.DataFrame(rows, columns=["variable", "group", "level", "n", "pct"])


def continuous_summary(frame: pd.DataFrame, variable: str, group: str) -> pd.DataFrame:
    grouped = frame.groupby(group, sort=False)[variable]
    out = pd.DataFrame(
        {"n": grouped.count(), "median": grouped.median(), "q1": grouped.quantile(0.25), "q3": grouped.quantile(0.75)}
    )
    out.index.name = "group"
    return out.reset_index()


def _median_cell(row: pd.Series) -> str:
    if row["n"] == 0:
        return "n/a"
    return f"{row['median']:.1f} ({row['q1']:.1f} to {row['q3']:.1f})"


def table_one(frame: pd.DataFrame, group: str, group_levels: tuple[str, ...], rows: list[TableRow]) -> pd.DataFrame:
    overall = frame.assign(_overall="Overall")
    sizes = frame[group].value_counts()
    records = [
        {"characteristic": "Men, n", "level": "", "Overall": fmt_int(len(frame)), **{g: fmt_int(sizes.get(g, 0)) for g in group_levels}}
    ]
    for row in rows:
        if row.levels is None:
            per_group = continuous_summary(frame, row.column, group).set_index("group")
            everyone = continuous_summary(overall, row.column, "_overall").set_index("group")
            record = {"characteristic": row.label, "level": "median (IQR)", "Overall": _median_cell(everyone.loc["Overall"])}
            for g in group_levels:
                record[g] = _median_cell(per_group.loc[g]) if g in per_group.index else "n/a"
            records.append(record)
            continue
        per_group = categorical_summary(frame, row.column, group, row.levels).set_index(["group", "level"])
        everyone = categorical_summary(overall, row.column, "_overall", row.levels).set_index(["group", "level"])
        for level in row.levels:
            total = everyone.loc[("Overall", level)]
            record = {"characteristic": row.label, "level": level, "Overall": f"{fmt_int(total['n'])} ({total['pct']:.1f}%)"}
            for g in group_levels:
                if (g, level) in per_group.index:
                    cell = per_group.loc[(g, level)]
                    record[g] = f"{fmt_int(cell['n'])} ({cell['pct']:.1f}%)"
                else:
                    record[g] = "n/a"
            records.append(record)
    return pd.DataFrame(records, columns=["characteristic", "level", "Overall", *group_levels])
