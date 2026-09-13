import math

import numpy as np

from seer_study.equity import concentration_curve, erreygers_index, fractional_rank


def test_fractional_rank_averages_ties():
    ranks = fractional_rank(np.array([1, 1, 2, 3]))
    assert np.allclose(ranks, [0.25, 0.25, 0.625, 0.875])


def test_fractional_rank_is_order_invariant():
    values = np.array([3, 1, 2, 1])
    assert np.allclose(fractional_rank(values), [0.875, 0.25, 0.625, 0.25])


def test_erreygers_extremes():
    income = np.array([1, 2, 3, 4])
    assert math.isclose(erreygers_index(np.array([0, 0, 1, 1]), income), 1.0)
    assert math.isclose(erreygers_index(np.array([1, 1, 0, 0]), income), -1.0)


def test_erreygers_zero_without_gradient():
    assert math.isclose(erreygers_index(np.array([1, 0, 0, 1]), np.array([1, 2, 3, 4])), 0.0, abs_tol=1e-12)


def test_erreygers_zero_when_outcome_constant():
    assert erreygers_index(np.array([1, 1, 1, 1]), np.array([1, 2, 3, 4])) == 0.0


def test_concentration_curve_endpoints_and_monotone():
    curve = concentration_curve(np.array([0, 1, 1, 0, 1]), np.array([5, 4, 3, 2, 1]))
    assert curve.iloc[0]["population_share"] == 0.0 and curve.iloc[0]["outcome_share"] == 0.0
    assert math.isclose(curve.iloc[-1]["population_share"], 1.0)
    assert math.isclose(curve.iloc[-1]["outcome_share"], 1.0)
    assert curve["population_share"].is_monotonic_increasing
    assert curve["outcome_share"].is_monotonic_increasing
