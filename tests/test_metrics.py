import math

import numpy as np

from seer_study.metrics import auc, brier_score, calibration_intercept_slope, log_loss, skill

CLIP = 1e-6


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def test_log_loss_known_value():
    assert math.isclose(log_loss(np.array([1, 0]), np.array([0.8, 0.2]), CLIP), -math.log(0.8))


def test_log_loss_clips_extreme_predictions():
    assert np.isfinite(log_loss(np.array([1, 0]), np.array([0.0, 1.0]), CLIP))


def test_brier_score_known_value():
    assert math.isclose(brier_score(np.array([1, 0]), np.array([0.8, 0.2])), 0.04)


def test_skill_relative_to_reference():
    assert skill(0.5, 0.5) == 0.0
    assert math.isclose(skill(0.25, 0.5), 0.5)


def test_auc_perfect_ranking():
    assert auc(np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9])) == 1.0


def test_calibration_of_well_calibrated_predictions():
    rng = np.random.default_rng(1)
    p = rng.uniform(0.05, 0.95, 200_000)
    y = rng.binomial(1, p)
    intercept, slope = calibration_intercept_slope(y, p, CLIP)
    assert abs(intercept) < 0.03
    assert abs(slope - 1.0) < 0.03


def test_calibration_slope_detects_overconfidence():
    rng = np.random.default_rng(2)
    true = rng.uniform(0.05, 0.95, 200_000)
    y = rng.binomial(1, true)
    overconfident = _sigmoid(2.0 * np.log(true / (1 - true)))
    _, slope = calibration_intercept_slope(y, overconfident, CLIP)
    assert abs(slope - 0.5) < 0.05


def test_calibration_intercept_detects_underprediction():
    rng = np.random.default_rng(3)
    true = rng.uniform(0.2, 0.8, 200_000)
    y = rng.binomial(1, true)
    intercept, _ = calibration_intercept_slope(y, true * 0.5, CLIP)
    assert intercept > 0.5
