"""Selection checks for men with a missing waiting time (PROTOCOL.md A7)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def weighted_percentage(flags: np.ndarray, weights: np.ndarray) -> float:
    """Weighted percentage of rows where ``flags`` is 1 (used for inverse probability weighting)."""
    w = np.asarray(weights, dtype=float)
    if (w < 0).any():
        raise ValueError("weights must not be negative")
    return float(100.0 * np.sum(w * np.asarray(flags, dtype=float)) / np.sum(w))


def delay_bounds(frame: pd.DataFrame, group: str, delayed_column: str) -> pd.DataFrame:
    """Percentage delayed among men with a recorded interval, and bounds assuming every missing man was
    not delayed (lower) or was delayed (upper)."""
    delayed = frame[delayed_column]
    missing = delayed.isna()
    keys = frame[group]
    n = keys.value_counts(sort=False)
    n_missing = missing.groupby(keys, sort=False).sum().reindex(n.index)
    n_delayed = delayed.fillna(False).astype(bool).groupby(keys, sort=False).sum().reindex(n.index)
    n_observed = n - n_missing
    out = pd.DataFrame(
        {
            "n": n.astype("int64"),
            "n_observed": n_observed.astype("int64"),
            "n_missing": n_missing.astype("int64"),
            "pct_delayed_observed": 100.0 * n_delayed / n_observed.where(n_observed > 0, np.nan),
            "pct_delayed_lower": 100.0 * n_delayed / n,
            "pct_delayed_upper": 100.0 * (n_delayed + n_missing) / n,
            "pct_missing": 100.0 * n_missing / n,
        }
    )
    out.index.name = group
    return out.reset_index()
