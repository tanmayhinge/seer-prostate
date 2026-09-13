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
