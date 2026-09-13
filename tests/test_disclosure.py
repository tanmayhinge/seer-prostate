import itertools
import random
import re

import pandas as pd
import pytest

from seer_study.disclosure import suppress_small_cells

MASK = "<5"
COLUMNS = ["Overall", "a", "b", "c"]
COUNT = re.compile(r"^(\d[\d,]*)( \(|$)")


def _table(rows):
    return pd.DataFrame(rows, columns=["characteristic", "level", *COLUMNS])


def _count(cell):
    match = COUNT.match(cell)
    return int(match.group(1).replace(",", "")) if match else None


def test_primary_cell_is_masked_and_zero_is_kept():
    table = _table(
        [
            ["Men, n", "", "200", "100", "60", "40"],
            ["X", "u", "150 (75.0%)", "97 (97.0%)", "30 (50.0%)", "23 (57.5%)"],
            ["X", "v", "50 (25.0%)", "3 (3.0%)", "30 (50.0%)", "17 (42.5%)"],
            ["Y", "p", "200 (100.0%)", "100 (100.0%)", "60 (100.0%)", "40 (100.0%)"],
            ["Y", "q", "0 (0.0%)", "0 (0.0%)", "0 (0.0%)", "0 (0.0%)"],
        ]
    )
    out = suppress_small_cells(table, COLUMNS, threshold=5, mask=MASK)
    assert out.loc[2, "a"] == MASK
    assert out.loc[4, "a"] == "0 (0.0%)"


def test_row_complement_is_masked():
    table = _table(
        [
            ["Men, n", "", "200", "100", "60", "40"],
            ["X", "u", "150 (75.0%)", "97 (97.0%)", "30 (50.0%)", "23 (57.5%)"],
            ["X", "v", "50 (25.0%)", "3 (3.0%)", "30 (50.0%)", "17 (42.5%)"],
        ]
    )
    out = suppress_small_cells(table, COLUMNS, threshold=5, mask=MASK)
    row = out.loc[2, COLUMNS].tolist()
    assert row.count(MASK) >= 2  # 3 in column a, plus a complement so Overall minus the rest cannot reveal it


def test_block_complement_is_masked_within_a_column():
    table = _table(
        [
            ["Men, n", "", "200", "100", "60", "40"],
            ["X", "u", "150 (75.0%)", "90 (90.0%)", "35 (58.3%)", "25 (62.5%)"],
            ["X", "v", "10 (5.0%)", "2 (2.0%)", "5 (8.3%)", "3 (7.5%)"],
            ["X", "w", "40 (20.0%)", "8 (8.0%)", "20 (33.3%)", "12 (30.0%)"],
        ]
    )
    out = suppress_small_cells(table, COLUMNS, threshold=5, mask=MASK)
    column_a = out.loc[1:3, "a"].tolist()
    assert column_a.count(MASK) >= 2


def test_median_rows_are_masked_for_tiny_columns():
    table = _table(
        [
            ["Men, n", "", "103", "96", "4", "3"],
            ["Days", "median (IQR)", "70.0 (50.0 to 90.0)", "71.0 (50.0 to 90.0)", "60.0 (40.0 to 80.0)", "55.0 (45.0 to 65.0)"],
        ]
    )
    out = suppress_small_cells(table, COLUMNS, threshold=5, mask=MASK)
    assert out.loc[0, "b"] == MASK and out.loc[0, "c"] == MASK
    assert out.loc[1, "b"] == MASK and out.loc[1, "c"] == MASK
    assert out.loc[1, "a"] == "71.0 (50.0 to 90.0)"


def test_input_is_not_modified():
    table = _table([["Men, n", "", "10", "3", "3", "4"]])
    before = table.copy()
    suppress_small_cells(table, COLUMNS, threshold=5, mask=MASK)
    assert table.equals(before)


def _random_table(rng):
    rows = [["Men, n", "", "", "", "", ""]]
    totals = [rng.randint(5, 60) for _ in range(3)]
    for characteristic in ("X", "Y"):
        splits = []
        for total in totals:
            cuts = sorted(rng.randint(0, total) for _ in range(2))
            splits.append([cuts[0], cuts[1] - cuts[0], total - cuts[1]])
        for level in range(3):
            counts = [splits[g][level] for g in range(3)]
            rows.append([characteristic, str(level), f"{sum(counts)} (x%)", *(f"{n} (x%)" for n in counts)])
    rows[0][2:] = [str(sum(totals)), *map(str, totals)]
    return _table(rows)


@pytest.mark.parametrize("seed", range(25))
def test_no_visible_small_cell_and_no_single_mask_in_any_row_or_block(seed):
    out = suppress_small_cells(_random_table(random.Random(seed)), COLUMNS, threshold=5, mask=MASK)
    body = out.iloc[1:]
    for _, row in body.iterrows():
        cells = row[COLUMNS].tolist()
        assert not any(1 <= (_count(c) or 0) <= 4 for c in cells)
        assert cells.count(MASK) != 1
    for column in COLUMNS:
        for _, block in body.groupby("characteristic"):
            assert block[column].tolist().count(MASK) != 1
