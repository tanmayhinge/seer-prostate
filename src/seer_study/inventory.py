"""Pure inventory functions for the Phase 0 profile of the raw SEER export.

Every function takes the all-text frame and the typed configuration and
returns plain pandas objects. Nothing here recodes values or drops rows.

Value status vocabulary used throughout:
    blank           the export's blank label (structural if outside the column's era)
    unknown         a label SEER documents as unknown or not recorded
    not_applicable  a label meaning the item does not apply (for example no prostatectomy)
    top_coded       a real value beyond the recorded range (for example 731+ days)
    known           anything else
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
import pandas as pd

from seer_study.config import ColumnSpec, DataSpec, StudyConfig

NUMERIC_PATTERN = r"\d+(?:\.\d+)?"
STATUSES = ("blank", "unknown", "not_applicable", "top_coded", "known")
SURGERY_GROUPS = ("performed", "none", "unknown", "both_blank", "multiple_coded")


class UnexpectedLabelError(ValueError):
    """A label the configuration does not document, found where one is not allowed."""


@dataclass(frozen=True)
class RowSummary:
    rows: int
    columns: int
    unique_ids: int
    rows_sharing_an_id: int
    ids_with_multiple_rows: int


@dataclass(frozen=True)
class NumericProfile:
    column: str
    unit: str
    summary: dict[str, float]
    categories: pd.DataFrame
    quantiles: pd.DataFrame
    bins: pd.DataFrame
    by_year: pd.DataFrame
    classes: pd.Series


@dataclass(frozen=True)
class SequenceProfile:
    frequency: pd.DataFrame
    first_primary_strict: int
    first_primary_inclusive: int
    strict_mask: pd.Series
    inclusive_mask: pd.Series


@dataclass(frozen=True)
class AgeCheck:
    column: str
    below_18: int
    straddling_18: int
    table: pd.DataFrame


def _pct(numerator: float, denominator: float) -> float:
    return 100.0 * numerator / denominator if denominator else float("nan")


def row_summary(frame: pd.DataFrame, data: DataSpec) -> RowSummary:
    counts = frame[data.id_column].value_counts()
    shared = counts[counts > 1]
    return RowSummary(
        rows=len(frame),
        columns=frame.shape[1],
        unique_ids=int(counts.size),
        rows_sharing_an_id=int(shared.sum()),
        ids_with_multiple_rows=int(shared.size),
    )


def frequency(series: pd.Series) -> pd.DataFrame:
    """Full frequency distribution, most common first, ties broken by label."""
    counts = series.value_counts(sort=False)
    table = pd.DataFrame({"value": counts.index.astype(str), "n": counts.to_numpy(dtype="int64")})
    table["pct"] = 100.0 * table["n"] / len(series) if len(series) else np.nan
    return table.sort_values(["n", "value"], ascending=[False, True], kind="stable").reset_index(drop=True)


def in_era(frame: pd.DataFrame, spec: ColumnSpec, data: DataSpec) -> pd.Series:
    """True for rows whose year of diagnosis falls inside the column's collection era."""
    if spec.era is None:
        return pd.Series(True, index=frame.index)
    years = frame[data.year_column].astype("int64")
    mask = years >= spec.era.first_year
    if spec.era.last_year is not None:
        mask &= years <= spec.era.last_year
    return mask


def classify_numeric_string(series: pd.Series, spec: ColumnSpec, blank_label: str) -> pd.Series:
    """'numeric' for digit strings, the label itself otherwise. Undocumented labels raise."""
    is_numeric = series.str.fullmatch(NUMERIC_PATTERN).astype(bool)
    documented = {blank_label, *spec.missing, *spec.not_applicable, *spec.top_codes}
    undocumented = sorted(set(series[~is_numeric].unique()) - documented)
    if undocumented:
        raise UnexpectedLabelError(f"column {series.name!r} has undocumented labels: {undocumented[:10]}")
    return series.where(~is_numeric, "numeric").rename(series.name)


def value_status(series: pd.Series, spec: ColumnSpec, blank_label: str) -> pd.Series:
    if spec.kind == "numeric_string":
        classify_numeric_string(series, spec, blank_label)
    status = np.full(len(series), "known", dtype=object)
    status[series.isin(spec.top_codes).to_numpy()] = "top_coded"
    status[series.isin(spec.not_applicable).to_numpy()] = "not_applicable"
    status[series.isin(spec.missing).to_numpy()] = "unknown"
    status[(series == blank_label).to_numpy()] = "blank"
    return pd.Series(status, index=series.index, name=series.name)


def missingness(frame: pd.DataFrame, config: StudyConfig) -> pd.DataFrame:
    """Per column: structural blanks, blanks inside the era, unknown, not applicable, known."""
    data = config.data
    rows = []
    for column in frame.columns:
        spec = config.columns[column]
        status = value_status(frame[column], spec, data.blank_label)
        era = in_era(frame, spec, data)
        is_blank = status.eq("blank")
        n = len(frame)
        n_in_era = int(era.sum())
        blank_in_era = int((is_blank & era).sum())
        blank_structural = int((is_blank & ~era).sum())
        unknown = int(status.eq("unknown").sum())
        not_applicable = int(status.eq("not_applicable").sum())
        top_coded = int(status.eq("top_coded").sum())
        known = int(status.isin(["known", "top_coded"]).sum())
        rows.append(
            {
                "column": column,
                "kind": spec.kind,
                "era": spec.era.label() if spec.era else "all years",
                "n": n,
                "n_in_era": n_in_era,
                "blank_structural": blank_structural,
                "blank_in_era": blank_in_era,
                "unknown": unknown,
                "not_applicable": not_applicable,
                "top_coded": top_coded,
                "known": known,
                "pct_blank_structural": _pct(blank_structural, n),
                "pct_missing_in_era": _pct(blank_in_era + unknown, n_in_era),
                "pct_not_applicable": _pct(not_applicable, n),
                "pct_known": _pct(known, n),
            }
        )
    return pd.DataFrame(rows)


def _status_table(status: pd.Series, groups: pd.Series, order: list[str]) -> pd.DataFrame:
    table = pd.crosstab(groups, status).reindex(index=order, fill_value=0)
    for name in STATUSES:
        if name not in table.columns:
            table[name] = 0
    n = table[list(STATUSES)].sum(axis=1)
    out = pd.DataFrame(
        {
            "n": n,
            "known": table["known"] + table["top_coded"],
            "unknown": table["unknown"],
            "not_applicable": table["not_applicable"],
            "blank": table["blank"],
        }
    )
    out["pct_known"] = 100.0 * out["known"] / out["n"].where(out["n"] > 0)
    return out


def completeness_by_year(frame: pd.DataFrame, columns: list[str], config: StudyConfig) -> pd.DataFrame:
    """Long table of status counts per column per configured year, including empty years."""
    data = config.data
    parts = []
    for column in columns:
        status = value_status(frame[column], config.columns[column], data.blank_label)
        table = _status_table(status, frame[data.year_column], list(data.years))
        table = table.rename_axis("year").reset_index()
        table.insert(0, "column", column)
        parts.append(table)
    return pd.concat(parts, ignore_index=True)


def surgery_code_group(frame: pd.DataFrame, config: StudyConfig) -> pd.Series:
    """Descriptive grouping of the raw surgery codes across both coding eras. Not an analysis variable."""
    spec = config.inventory
    blank = config.data.blank_label
    columns = list(spec.surgery_columns)
    coded = frame[columns].ne(blank)
    n_coded = coded.sum(axis=1)
    code = pd.Series("", index=frame.index, dtype=object)
    for column in columns:
        code = code.mask(coded[column], frame[column])
    group = np.select(
        [
            n_coded.eq(0).to_numpy(),
            n_coded.gt(1).to_numpy(),
            code.isin(spec.surgery_none_codes).to_numpy(),
            code.isin(spec.surgery_unknown_codes).to_numpy(),
        ],
        ["both_blank", "multiple_coded", "none", "unknown"],
        default="performed",
    )
    return pd.Series(group, index=frame.index, name="surgery_code_group", dtype=object)


def completeness_by_group(
    frame: pd.DataFrame, column: str, groups: pd.Series, config: StudyConfig
) -> pd.DataFrame:
    status = value_status(frame[column], config.columns[column], config.data.blank_label)
    return _status_table(status, groups, list(SURGERY_GROUPS)).rename_axis("group").reset_index()


def _bin_counts(values: pd.Series, edges: tuple[int, ...], column: str) -> pd.DataFrame:
    if not edges:
        return pd.DataFrame({"bin": [], "n": [], "pct": []})
    edges_list = list(edges)
    outside = values[(values < edges_list[0]) | (values >= edges_list[-1])]
    if len(outside):
        raise UnexpectedLabelError(
            f"column {column!r}: {len(outside)} values outside bin edges {edges_list[0]} to {edges_list[-1]}"
        )
    counts = pd.cut(values, bins=edges_list, right=False).value_counts(sort=False).to_numpy(dtype="int64")
    labels = [f"{low} to {high - 1}" for low, high in zip(edges_list[:-1], edges_list[1:])]
    total = counts.sum()
    return pd.DataFrame({"bin": labels, "n": counts, "pct": 100.0 * counts / total if total else np.nan})


def numeric_profile(
    frame: pd.DataFrame,
    column: str,
    config: StudyConfig,
    unit: str,
    bin_edges: tuple[int, ...] = (),
) -> NumericProfile:
    data = config.data
    spec = config.columns[column]
    series = frame[column]
    classes = classify_numeric_string(series, spec, data.blank_label)
    numeric_mask = classes.eq("numeric")
    values = pd.to_numeric(series[numeric_mask]).astype(float)
    q = list(config.inventory.quantiles)
    quantile_values = values.quantile(q).to_numpy() if len(values) else np.full(len(q), np.nan)
    era = in_era(frame, spec, data)
    is_blank = classes.eq(data.blank_label)
    by_year = pd.crosstab(frame[data.year_column], classes).reindex(index=list(data.years), fill_value=0)
    by_year.index.name = "year"
    by_year.columns.name = None
    summary = {
        "n": len(series),
        "numeric": int(numeric_mask.sum()),
        "top_coded": int(classes.isin(spec.top_codes).sum()),
        "unknown": int(classes.isin(spec.missing).sum()),
        "blank_in_era": int((is_blank & era).sum()),
        "blank_structural": int((is_blank & ~era).sum()),
        "not_applicable": int(classes.isin(spec.not_applicable).sum()),
        "mean": float(values.mean()) if len(values) else float("nan"),
        "min": float(values.min()) if len(values) else float("nan"),
        "max": float(values.max()) if len(values) else float("nan"),
    }
    return NumericProfile(
        column=column,
        unit=unit,
        summary=summary,
        categories=frequency(classes),
        quantiles=pd.DataFrame({"quantile": q, unit: quantile_values}),
        bins=_bin_counts(values, bin_edges, column),
        by_year=by_year,
        classes=classes,
    )


def time_to_treatment_profile(frame: pd.DataFrame, config: StudyConfig) -> NumericProfile:
    spec = config.inventory
    return numeric_profile(
        frame, spec.time_to_treatment_column, config, unit="days", bin_edges=spec.time_to_treatment_bin_edges
    )


def sequence_profile(frame: pd.DataFrame, config: StudyConfig) -> SequenceProfile:
    spec = config.inventory
    series = frame[spec.sequence_column]
    strict = series.isin(spec.first_primary_strict)
    inclusive = series.isin(spec.first_primary_inclusive)
    return SequenceProfile(
        frequency=frequency(series),
        first_primary_strict=int(strict.sum()),
        first_primary_inclusive=int(inclusive.sum()),
        strict_mask=strict,
        inclusive_mask=inclusive,
    )


def crosstab_counts(frame: pd.DataFrame, row: str, column: str) -> pd.DataFrame:
    """Counts with Total margins; rows ordered by overall frequency."""
    table = pd.crosstab(frame[row], frame[column], margins=True, margins_name="Total")
    order = table["Total"].drop("Total").sort_values(ascending=False, kind="stable").index.tolist()
    table = table.loc[order + ["Total"]]
    table.index.name = row
    table.columns.name = None
    return table


def column_percentages(frame: pd.DataFrame, row: str, column: str) -> pd.DataFrame:
    """Each cell as a percentage of its column total."""
    counts = pd.crosstab(frame[row], frame[column])
    pct = counts.div(counts.sum(axis=0), axis=1) * 100.0
    order = counts.sum(axis=1).sort_values(ascending=False, kind="stable").index
    pct = pct.loc[order]
    pct.columns.name = None
    return pct


def nonblank_by_year(frame: pd.DataFrame, columns: list[str], config: StudyConfig) -> pd.DataFrame:
    data = config.data
    counts = frame[list(columns)].ne(data.blank_label).groupby(frame[data.year_column]).sum()
    counts = counts.reindex(list(data.years), fill_value=0).astype("int64")
    counts.index.name = "year"
    return counts


def single_valued_columns(frame: pd.DataFrame) -> list[str]:
    return [column for column in frame.columns if frame[column].nunique(dropna=False) == 1]


def check_absent_variables(names: list[str], keywords: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    """For each concept, the column names matching any of its keywords (empty means absent)."""
    return {
        concept: [name for name in names if any(word.lower() in name.lower() for word in words)]
        for concept, words in keywords.items()
    }


def suspect_unconfigured_labels(frame: pd.DataFrame, config: StudyConfig) -> pd.DataFrame:
    """Labels that look like missing-value codes but are not configured as missing, not applicable or top-coded."""
    patterns = [re.compile(p, re.IGNORECASE) for p in config.inventory.suspect_label_patterns]
    numeric = re.compile(NUMERIC_PATTERN)
    rows = []
    for column in frame.columns:
        spec = config.columns[column]
        if spec.kind == "identifier":
            continue
        configured = {config.data.blank_label, *spec.missing, *spec.not_applicable, *spec.top_codes}
        for value, n in frame[column].value_counts().items():
            if value in configured or numeric.fullmatch(value):
                continue
            if any(p.search(value) for p in patterns):
                rows.append({"column": column, "value": value, "n": int(n)})
    return pd.DataFrame(rows, columns=["column", "value", "n"])


def age_check(frame: pd.DataFrame, config: StudyConfig) -> AgeCheck | None:
    spec = config.inventory
    if spec.age_column is None:
        return None
    series = frame[spec.age_column]
    below = series.isin(spec.age_labels_below_18)
    straddling = series.isin(spec.age_labels_straddling_18)
    table = frequency(series[below | straddling]).drop(columns="pct")
    return AgeCheck(
        column=spec.age_column,
        below_18=int(below.sum()),
        straddling_18=int(straddling.sum()),
        table=table,
    )


def selection_criteria(note: str) -> list[str]:
    """Selection lines from a SEER*Stat selection note (lines of the form 'Variable = value')."""
    return [line.strip() for line in note.splitlines() if " = " in line]


def unexpected_selection_criteria(criteria: list[str], expected_variables: tuple[str, ...]) -> list[str]:
    return [line for line in criteria if not line.startswith(tuple(expected_variables))]
