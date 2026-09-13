"""Standardisation (g-computation) of delay under a chosen social profile (PROTOCOL.md A5).

Every man keeps his own clinical and pathway features while his social features are set to one profile. The
mean predicted probability is the standardised percentage delayed. This is an associational contrast, not a
causal effect.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from seer_study.analysis_config import FeatureSpec
from seer_study.features import one_hot_column
from seer_study.labels import require_known


def set_social_profile(
    X: pd.DataFrame, features: FeatureSpec, marital: str, rurality: str, income_rank: float
) -> pd.DataFrame:
    require_known(pd.Series([marital]), features.marital_labels, "marital status")
    require_known(pd.Series([rurality]), features.rurality_labels, "rurality")
    out = X.copy()
    for label in features.marital_labels:
        out[one_hot_column("marital", label)] = int(label == marital)
    for label in features.rurality_labels:
        out[one_hot_column("rurality", label)] = int(label == rurality)
    out["rurality_unknown"] = 0
    out["income_rank"] = float(income_rank)
    out["income_unknown"] = 0
    return out[X.columns]


def standardised_mean(model, X: pd.DataFrame) -> float:
    """Mean predicted probability of delay over the rows of ``X``."""
    return float(np.mean(model.predict_proba(X)[:, 1]))


def excess_days_per_1000(days: np.ndarray, threshold: float) -> float:
    """Waiting days beyond the threshold, summed and expressed per 1,000 men (top-coded days count at their cap)."""
    excess = np.clip(np.asarray(days, dtype=float) - threshold, 0.0, None)
    return float(excess.mean() * 1000.0)
