import math

import numpy as np
import pandas as pd
import pytest

from seer_study.selection import delay_bounds, weighted_percentage


def test_delay_bounds_by_group():
    frame = pd.DataFrame(
        {
            "group": ["a", "a", "a", "a", "b", "b"],
            "delayed": pd.array([True, False, pd.NA, pd.NA, True, False], dtype="boolean"),
        }
    )
    out = delay_bounds(frame, "group", "delayed").set_index("group")
    a = out.loc["a"]
    assert a["n"] == 4 and a["n_observed"] == 2 and a["n_missing"] == 2
    assert math.isclose(a["pct_delayed_observed"], 50.0)
    assert math.isclose(a["pct_delayed_lower"], 25.0)  # every missing man assumed not delayed
    assert math.isclose(a["pct_delayed_upper"], 75.0)  # every missing man assumed delayed
    assert math.isclose(a["pct_missing"], 50.0)
    b = out.loc["b"]
    assert b["pct_delayed_lower"] == b["pct_delayed_observed"] == b["pct_delayed_upper"] == 50.0


def test_weighted_percentage():
    assert weighted_percentage(np.array([1, 0, 1]), np.array([1.0, 1.0, 2.0])) == pytest.approx(75.0)


def test_weighted_percentage_with_equal_weights_is_plain_percentage():
    flags = np.array([1, 0, 0, 1, 1])
    assert weighted_percentage(flags, np.ones(5)) == pytest.approx(60.0)


def test_weighted_percentage_rejects_negative_weights():
    with pytest.raises(ValueError, match="negative"):
        weighted_percentage(np.array([1, 0]), np.array([1.0, -1.0]))
