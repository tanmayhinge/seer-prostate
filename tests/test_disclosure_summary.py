import random

import pandas as pd
import pytest

from seer_study.disclosure import publishable_bounds, publishable_summary

MASK = "<5"
STATS = ["n", "pct_delayed", "median_days", "p90_days"]


def _row(n, n_delayed):
    return {
        "group": "g",
        "n": n,
        "n_delayed": n_delayed,
        "pct_delayed": 100.0 * n_delayed / n if n else 0.0,
        "median_days": 80.0,
        "p90_days": 150.0,
    }


def _publish(rows, rounding=10):
    return publishable_summary(pd.DataFrame(rows), threshold=5, mask=MASK, rounding=rounding)


def test_delayed_count_column_is_dropped():
    assert "n_delayed" not in _publish([_row(50, 20)]).columns


def test_counts_are_rounded_half_up_and_never_to_zero():
    out = _publish([_row(1234, 600), _row(1235, 600), _row(7, 3), _row(5, 0)])
    assert out["n"].tolist()[:2] == [1230, 1240]
    assert out.loc[2, "n"] == 10
    assert out.loc[3, "n"] == 10


def test_rounding_of_one_keeps_exact_counts():
    assert _publish([_row(1234, 600)], rounding=1).loc[0, "n"] == 1234


def test_tiny_row_masks_every_statistic():
    out = _publish([_row(3, 1)])
    assert all(out.loc[0, column] == MASK for column in STATS)


def test_small_delayed_or_not_delayed_count_masks_percentage_only():
    out = _publish([_row(50, 2), _row(10, 8)])
    assert out.loc[0, "pct_delayed"] == MASK
    assert out.loc[0, "n"] == 50 and out.loc[0, "median_days"] == 80.0
    assert out.loc[1, "pct_delayed"] == MASK


def test_zero_delayed_percentage_is_shown():
    assert _publish([_row(50, 0)]).loc[0, "pct_delayed"] == 0.0


def test_large_rows_keep_their_statistics():
    out = _publish([_row(400, 150)])
    assert out.loc[0, "pct_delayed"] == pytest.approx(37.5)
    assert out.loc[0, "median_days"] == 80.0 and out.loc[0, "p90_days"] == 150.0


def test_input_is_not_modified():
    table = pd.DataFrame([_row(3, 1), _row(40, 20)])
    before = table.copy()
    publishable_summary(table, threshold=5, mask=MASK, rounding=10)
    assert table.equals(before)


BOUND_STATS = ["n", "pct_delayed_observed", "pct_delayed_lower", "pct_delayed_upper", "pct_missing"]


def _bounds_row(n, n_missing, delayed_observed):
    observed = n - n_missing
    return {
        "group": "g",
        "n": n,
        "n_observed": observed,
        "n_missing": n_missing,
        "pct_delayed_observed": 100.0 * delayed_observed / observed if observed else float("nan"),
        "pct_delayed_lower": 100.0 * delayed_observed / n if n else float("nan"),
        "pct_delayed_upper": 100.0 * (delayed_observed + n_missing) / n if n else float("nan"),
        "pct_missing": 100.0 * n_missing / n if n else float("nan"),
    }


def _publish_bounds(rows):
    return publishable_bounds(pd.DataFrame(rows), threshold=5, mask=MASK, rounding=10)


def test_bounds_drop_counts_and_round_men():
    out = _publish_bounds([_bounds_row(1234, 50, 400)])
    assert "n_observed" not in out.columns and "n_missing" not in out.columns
    assert out.loc[0, "n"] == 1230
    assert out.loc[0, "pct_missing"] == pytest.approx(100.0 * 50 / 1234)
    assert out.loc[0, "pct_delayed_lower"] == pytest.approx(100.0 * 400 / 1234)


def test_bounds_tiny_row_masks_everything():
    out = _publish_bounds([_bounds_row(3, 1, 1)])
    assert all(out.loc[0, column] == MASK for column in BOUND_STATS)


def test_small_missing_count_hides_missing_share_and_bounds():
    out = _publish_bounds([_bounds_row(500, 3, 200)])
    assert out.loc[0, "pct_missing"] == MASK
    assert out.loc[0, "pct_delayed_lower"] == MASK and out.loc[0, "pct_delayed_upper"] == MASK
    assert out.loc[0, "pct_delayed_observed"] == pytest.approx(100.0 * 200 / 497)


def test_small_observed_delayed_or_not_delayed_hides_delay_percentages():
    out = _publish_bounds([_bounds_row(500, 50, 2), _bounds_row(500, 50, 448)])
    for row in (0, 1):
        assert out.loc[row, "pct_delayed_observed"] == MASK
        assert out.loc[row, "pct_delayed_lower"] == MASK
        assert out.loc[row, "pct_delayed_upper"] == MASK
        assert out.loc[row, "pct_missing"] == pytest.approx(10.0)


def test_large_bounds_row_keeps_its_statistics():
    out = _publish_bounds([_bounds_row(800, 40, 300)])
    assert out.loc[0, "pct_delayed_observed"] == pytest.approx(100.0 * 300 / 760)
    assert out.loc[0, "pct_delayed_upper"] == pytest.approx(100.0 * 340 / 800)


@pytest.mark.parametrize("seed", range(30))
def test_invariants_on_random_rows(seed):
    rng = random.Random(seed)
    rows = []
    for _ in range(12):
        n = rng.choice([0, rng.randint(1, 4), rng.randint(5, 12), rng.randint(20, 500)])
        rows.append(_row(n, rng.randint(0, n)))
    out = _publish(rows)
    for original, published in zip(rows, out.to_dict("records")):
        n, delayed = original["n"], original["n_delayed"]
        if 1 <= n <= 4:
            assert all(published[column] == MASK for column in STATS)
            continue
        assert published["n"] % 10 == 0
        if published["pct_delayed"] != MASK:
            assert not 1 <= delayed <= 4
            assert not 1 <= n - delayed <= 4
