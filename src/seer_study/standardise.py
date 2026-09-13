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


RESERVED_PROFILES = ("as observed", "reference profile")


def standardised_percentages(
    model, X: pd.DataFrame, features: FeatureSpec, reference: dict, profiles: dict[str, dict]
) -> dict[str, float]:
    """Standardised percentages: as observed, at the reference profile, and at each profile.

    Each profile lists only the social settings that differ from ``reference`` (keys ``marital``, ``rurality``,
    ``income_rank``).
    """
    reserved = sorted(set(profiles) & set(RESERVED_PROFILES))
    if reserved:
        raise ValueError(f"profile names {reserved} are reserved")
    out = {
        "as observed": 100.0 * standardised_mean(model, X),
        "reference profile": 100.0 * standardised_mean(model, set_social_profile(X, features, **reference)),
    }
    for name, overrides in profiles.items():
        out[name] = 100.0 * standardised_mean(model, set_social_profile(X, features, **{**reference, **overrides}))
    return out


def area_income_ranks(income_rank: pd.Series, rurality: pd.Series, labels) -> dict[str, float]:
    """Median county income rank of men living in each type of area (NaN when no man has a known rank there)."""
    ranks = income_rank.to_numpy(dtype=float)
    areas = rurality.to_numpy()
    out = {}
    for label in labels:
        values = ranks[(areas == label) & ~np.isnan(ranks)]
        out[label] = float(np.median(values)) if values.size else float("nan")
    return out


def agreement_label(logistic: float, lightgbm: float, minimum: float) -> str:
    """Agreement rule for standardised contrasts (PROTOCOL.md amendment 1.7)."""
    if abs(logistic) >= minimum and abs(lightgbm) >= minimum and np.sign(logistic) == np.sign(lightgbm):
        return f"both models {minimum:g} points or more, same direction"
    if abs(logistic) < minimum and abs(lightgbm) < minimum:
        return f"both models under {minimum:g} points"
    return "models disagree"


def excess_days_per_1000(days: np.ndarray, threshold: float) -> float:
    """Waiting days beyond the threshold, summed and expressed per 1,000 men (top-coded days count at their cap)."""
    excess = np.clip(np.asarray(days, dtype=float) - threshold, 0.0, None)
    return float(excess.mean() * 1000.0)
