"""Performance measures for binary predictions (PROTOCOL.md section 7)."""

from __future__ import annotations

import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score


def clip_probabilities(p: np.ndarray, clip: float) -> np.ndarray:
    return np.clip(np.asarray(p, dtype=float), clip, 1.0 - clip)


def pointwise_log_loss(y: np.ndarray, p: np.ndarray, clip: float) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    p = clip_probabilities(p, clip)
    return -(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))


def log_loss(y: np.ndarray, p: np.ndarray, clip: float) -> float:
    """Mean negative log-likelihood. Lower is better."""
    return float(np.mean(pointwise_log_loss(y, p, clip)))


def brier_score(y: np.ndarray, p: np.ndarray) -> float:
    """Mean squared error of predicted probabilities. Lower is better."""
    return float(np.mean((np.asarray(p, dtype=float) - np.asarray(y, dtype=float)) ** 2))


def skill(model_loss: float, reference_loss: float) -> float:
    """1 minus model loss over reference loss: 0 means no better than the reference, higher is better."""
    return 1.0 - model_loss / reference_loss


def auc(y: np.ndarray, p: np.ndarray) -> float:
    """Area under the ROC curve: 0.5 is chance, higher is better."""
    return float(roc_auc_score(np.asarray(y), np.asarray(p, dtype=float)))


def calibration_intercept_slope(y: np.ndarray, p: np.ndarray, clip: float) -> tuple[float, float]:
    """Calibration intercept (ideal 0) and slope (ideal 1) from logistic recalibration on the log-odds scale.

    The intercept is estimated with the log-odds as an offset (calibration in the large); the slope from a
    logistic regression of the outcome on the log-odds. The slope is undefined for constant predictions.
    """
    y = np.asarray(y, dtype=float)
    p = clip_probabilities(p, clip)
    log_odds = np.log(p / (1.0 - p))
    intercept_fit = sm.GLM(y, np.ones_like(log_odds), family=sm.families.Binomial(), offset=log_odds).fit()
    intercept = float(intercept_fit.params[0])
    if np.ptp(log_odds) < 1e-12:
        return intercept, float("nan")
    slope_fit = sm.GLM(y, sm.add_constant(log_odds), family=sm.families.Binomial()).fit()
    return intercept, float(slope_fit.params[1])
