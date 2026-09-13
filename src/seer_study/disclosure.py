"""Small-count suppression for published tables.

The SEER Research Data Use Agreement requires statistics about geography or
demographics based on counts of 1 to 4 to be suppressed in all publications.
Masking one cell is not enough when a row or column total would reveal it, so a
second (complementary) cell is masked until no row or block has exactly one
masked count. The first column in ``columns`` is the row total (for example
"Overall"); rows with the characteristic "Men, n" hold the column totals.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

HEADER_LABEL = "Men, n"
COUNT_CELL = re.compile(r"^(\d[\d,]*)(?: \(|$)")


def _count(cell: object) -> float:
    match = COUNT_CELL.match(str(cell))
    return float(match.group(1).replace(",", "")) if match else float("nan")


def _mask_smallest(masked: pd.DataFrame, counts: pd.DataFrame, cells: list[tuple[object, str]]) -> bool:
    candidates = [(counts.at[i, c], i, c) for i, c in cells if not masked.at[i, c] and counts.at[i, c] > 0]
    if not candidates:
        return False
    _, i, c = min(candidates, key=lambda item: item[0])
    masked.at[i, c] = True
    return True


def rounded_count(n: float, threshold: int, mask: str, rounding: int) -> int | str:
    """One published count: 1 to ``threshold - 1`` is masked, anything else is rounded half up to ``rounding``."""
    if 1 <= n < threshold:
        return mask
    return int(np.floor(n / rounding + 0.5) * rounding)


PUBLISHED_STATISTICS = ("n", "pct_delayed", "median_days", "p90_days")


def publishable_summary(table: pd.DataFrame, threshold: int, mask: str, rounding: int) -> pd.DataFrame:
    """Prepare a grouped delay summary (columns as in ``delay_summary``) for publication.

    - The delayed count column is dropped, and the number of men is rounded half up to the nearest ``rounding``
      (use 1 for exact counts), so small groups cannot be recovered by subtracting published rows from totals.
    - A row describing 1 to ``threshold - 1`` men has every statistic masked.
    - The percentage delayed is also masked when 1 to ``threshold - 1`` men in the row were delayed, or were not.
    """
    n = table["n"].to_numpy(dtype=float)
    delayed = table["n_delayed"].to_numpy(dtype=float)

    def small(values):
        return (values >= 1) & (values < threshold)

    tiny = small(n)
    hide_percentage = tiny | small(delayed) | small(n - delayed)
    rounded = (np.floor(n / rounding + 0.5) * rounding).astype(int)

    out = table.drop(columns="n_delayed").copy()
    for column in PUBLISHED_STATISTICS:
        out[column] = out[column].astype(object)
    positions = {column: out.columns.get_loc(column) for column in PUBLISHED_STATISTICS}
    for row in range(len(out)):
        if tiny[row]:
            for column in PUBLISHED_STATISTICS:
                out.iat[row, positions[column]] = mask
            continue
        out.iat[row, positions["n"]] = int(rounded[row])
        if hide_percentage[row]:
            out.iat[row, positions["pct_delayed"]] = mask
    return out


BOUND_STATISTICS = ("n", "pct_delayed_observed", "pct_delayed_lower", "pct_delayed_upper", "pct_missing")


def publishable_bounds(table: pd.DataFrame, threshold: int, mask: str, rounding: int) -> pd.DataFrame:
    """Prepare selection bounds (columns as in ``delay_bounds``) for publication.

    - Observed and missing counts are dropped; the number of men is rounded half up to the nearest ``rounding``.
    - A row describing 1 to ``threshold - 1`` men has every statistic masked.
    - When 1 to ``threshold - 1`` men are missing, the missing share and both bounds are masked.
    - When 1 to ``threshold - 1`` observed men were delayed, or were not, the observed percentage and both bounds
      are masked.
    """
    n = table["n"].to_numpy(dtype=float)
    missing = table["n_missing"].to_numpy(dtype=float)
    observed = table["n_observed"].to_numpy(dtype=float)
    delayed_observed = np.rint(table["pct_delayed_observed"].to_numpy(dtype=float) / 100.0 * observed)

    def small(values):
        return (values >= 1) & (values < threshold)

    tiny = small(n)
    hide_missing = small(missing)
    hide_delay = small(delayed_observed) | small(observed - delayed_observed)
    rounded = (np.floor(n / rounding + 0.5) * rounding).astype(int)

    out = table.drop(columns=["n_observed", "n_missing"]).copy()
    for column in BOUND_STATISTICS:
        out[column] = out[column].astype(object)
    positions = {column: out.columns.get_loc(column) for column in BOUND_STATISTICS}
    for row in range(len(out)):
        if tiny[row]:
            for column in BOUND_STATISTICS:
                out.iat[row, positions[column]] = mask
            continue
        out.iat[row, positions["n"]] = int(rounded[row])
        if hide_missing[row]:
            for column in ("pct_missing", "pct_delayed_lower", "pct_delayed_upper"):
                out.iat[row, positions[column]] = mask
        if hide_delay[row]:
            for column in ("pct_delayed_observed", "pct_delayed_lower", "pct_delayed_upper"):
                out.iat[row, positions[column]] = mask
    return out


def suppress_small_cells(table: pd.DataFrame, columns: list[str], threshold: int, mask: str) -> pd.DataFrame:
    columns = list(columns)
    total_column, group_columns = columns[0], columns[1:]
    counts = pd.DataFrame({c: table[c].map(_count) for c in columns}, index=table.index)
    masked = (counts >= 1) & (counts < threshold)

    header = table["characteristic"].eq(HEADER_LABEL)
    for column in columns:
        column_totals = counts.loc[header, column]
        if ((column_totals >= 1) & (column_totals < threshold)).any():
            masked[column] = True  # every statistic in a column describing fewer than `threshold` men

    body_rows = table.index[~header]
    blocks = table.loc[body_rows].groupby("characteristic", sort=False).groups

    changed = True
    while changed:
        changed = False
        for i in body_rows:
            count_columns = [c for c in columns if pd.notna(counts.at[i, c])]
            if sum(bool(masked.at[i, c]) for c in count_columns) == 1:
                groups = [(i, c) for c in count_columns if c in group_columns]
                changed |= _mask_smallest(masked, counts, groups) or _mask_smallest(
                    masked, counts, [(i, total_column)] if total_column in count_columns else []
                )
        for rows in blocks.values():
            for column in columns:
                cells = [(i, column) for i in rows if pd.notna(counts.at[i, column])]
                if sum(bool(masked.at[i, c]) for i, c in cells) == 1:
                    changed |= _mask_smallest(masked, counts, cells)

    out = table.copy()
    for column in columns:
        out.loc[masked[column], column] = mask
    return out
