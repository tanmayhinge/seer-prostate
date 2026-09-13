"""Socioeconomic inequality in a bounded outcome: Erreygers concentration index and concentration curve."""

from __future__ import annotations

import numpy as np
import pandas as pd


def fractional_rank(values: np.ndarray) -> np.ndarray:
    """Fractional rank in (0, 1), lowest value first; tied values share the average rank."""
    series = pd.Series(np.asarray(values, dtype=float))
    return ((series.rank(method="average") - 0.5) / len(series)).to_numpy()


def erreygers_index(outcome: np.ndarray, rank_values: np.ndarray, lower: float = 0.0, upper: float = 1.0) -> float:
    """Erreygers-corrected concentration index for an outcome bounded by [lower, upper].

    E = 8 cov(y, R) / (upper - lower), where R is the fractional rank of ``rank_values`` (for example county
    income, poorest first). It ranges from -1 to 1; a negative value means the outcome is concentrated among
    lower-ranked (poorer) groups, and 0 means no socioeconomic gradient.
    """
    y = np.asarray(outcome, dtype=float)
    if np.ptp(y) == 0:
        return 0.0
    ranks = fractional_rank(rank_values)
    covariance = np.mean(y * ranks) - y.mean() * ranks.mean()
    return float(8.0 * covariance / (upper - lower))


def concentration_curve(outcome: np.ndarray, rank_values: np.ndarray) -> pd.DataFrame:
    """Cumulative share of the population (poorest first) against cumulative share of the outcome."""
    frame = pd.DataFrame({"rank": np.asarray(rank_values, dtype=float), "y": np.asarray(outcome, dtype=float)})
    grouped = frame.groupby("rank", sort=True)["y"].agg(["size", "sum"])
    population = grouped["size"].cumsum() / grouped["size"].sum()
    total = grouped["sum"].sum()
    outcome_share = grouped["sum"].cumsum() / total if total else grouped["sum"].cumsum() * 0.0
    curve = pd.DataFrame({"population_share": population.to_numpy(), "outcome_share": outcome_share.to_numpy()})
    return pd.concat([pd.DataFrame({"population_share": [0.0], "outcome_share": [0.0]}), curve], ignore_index=True)
