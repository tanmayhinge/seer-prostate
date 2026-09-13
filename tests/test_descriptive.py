import math

import pandas as pd

from seer_study.descriptive import delay_summary


def _frame():
    return pd.DataFrame(
        {
            "risk": ["low", "low", "high", "high", "high"],
            "area": ["x", "y", "x", "x", "y"],
            "days": [30.0, 120.0, 10.0, 200.0, 95.0],
            "delayed": pd.array([False, True, False, True, True], dtype="boolean"),
        }
    )


def test_delay_summary_single_grouping():
    out = delay_summary(_frame(), ["risk"], "delayed", "days").set_index("risk")
    low, high = out.loc["low"], out.loc["high"]
    assert low["n"] == 2 and low["n_delayed"] == 1
    assert math.isclose(low["pct_delayed"], 50.0)
    assert low["median_days"] == 75.0
    assert math.isclose(low["p90_days"], 111.0)
    assert high["n"] == 3 and high["n_delayed"] == 2
    assert math.isclose(high["pct_delayed"], 200 / 3)
    assert high["median_days"] == 95.0


def test_delay_summary_two_groupings():
    out = delay_summary(_frame(), ["risk", "area"], "delayed", "days").set_index(["risk", "area"])
    assert out.loc[("high", "x"), "n"] == 2
    assert math.isclose(out.loc[("high", "x"), "pct_delayed"], 50.0)
    assert out["n"].sum() == 5


def test_delay_summary_overall_row_when_no_grouping():
    out = delay_summary(_frame(), [], "delayed", "days")
    assert len(out) == 1
    assert out.iloc[0]["n"] == 5
    assert math.isclose(out.iloc[0]["pct_delayed"], 60.0)
