"""Ordered-step performance and its uncertainty (PROTOCOL.md sections 6 and 7).

Skill at each step is 1 minus the step's out-of-fold log-loss over the log-loss at step 0. The increment for a
block is the skill gained when that block is added. Intervals come from resampling whole clusters (rurality by
income cells) of out-of-fold predictions, without refitting, because the social exposures are county-level.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from seer_study.metrics import auc, brier_score, calibration_intercept_slope, log_loss, pointwise_log_loss, skill

COMPARISONS = {1: "clinical need (step 0 to 1)", 2: "social position (step 1 to 2)", 3: "pathway (step 2 to 3)"}


def cluster_size_summary(clusters: np.ndarray, threshold: int, mask: str) -> dict:
    """Number of bootstrap clusters and their sizes; a smallest size of 1 to ``threshold - 1`` men is masked."""
    _, sizes = np.unique(np.asarray(clusters), return_counts=True)
    smallest = int(sizes.min())
    return {
        "clusters": int(len(sizes)),
        "smallest": mask if 1 <= smallest < threshold else smallest,
        "median": float(np.median(sizes)),
        "largest": int(sizes.max()),
        "largest_share_pct": 100.0 * float(sizes.max()) / float(sizes.sum()),
    }


def step_metrics(y: np.ndarray, predictions: dict[int, np.ndarray], clip: float) -> pd.DataFrame:
    steps = sorted(predictions)
    reference_log_loss = log_loss(y, predictions[steps[0]], clip)
    reference_brier = brier_score(y, predictions[steps[0]])
    rows = []
    for step in steps:
        p = predictions[step]
        step_log_loss = log_loss(y, p, clip)
        step_brier = brier_score(y, p)
        intercept, slope = calibration_intercept_slope(y, p, clip)
        rows.append(
            {
                "step": step,
                "log_loss": step_log_loss,
                "brier": step_brier,
                "auc": auc(y, p),
                "calibration_intercept": intercept,
                "calibration_slope": slope,
                "log_loss_skill": skill(step_log_loss, reference_log_loss),
                "brier_skill": skill(step_brier, reference_brier),
            }
        )
    return pd.DataFrame(rows)


def _cluster_members(clusters: np.ndarray) -> list[np.ndarray]:
    _, inverse = np.unique(np.asarray(clusters), return_inverse=True)
    order = np.argsort(inverse, kind="stable")
    boundaries = np.flatnonzero(np.diff(inverse[order])) + 1
    return np.split(order, boundaries)


def _draw(members: list[np.ndarray], rng: np.random.Generator) -> np.ndarray:
    chosen = rng.integers(0, len(members), size=len(members))
    return np.concatenate([members[i] for i in chosen])


def resample_clusters(clusters: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Row indices for one cluster bootstrap resample: clusters drawn with replacement, members kept together."""
    return _draw(_cluster_members(clusters), rng)


def cluster_bootstrap_interval(
    statistic, clusters: np.ndarray, n_resamples: int, seed: int, level: float
) -> tuple[float, float, float]:
    """Estimate and cluster-bootstrap interval for any statistic computed from an array of row indices."""
    estimate = float(statistic(np.arange(len(clusters))))
    members = _cluster_members(clusters)
    rng = np.random.default_rng(seed)
    draws = np.array([statistic(_draw(members, rng)) for _ in range(n_resamples)], dtype=float)
    tail = (1.0 - level) / 2.0
    lower, upper = np.quantile(draws, [tail, 1.0 - tail])
    return estimate, float(lower), float(upper)


def bootstrap_increments(
    y: np.ndarray,
    predictions: dict[int, np.ndarray],
    clusters: np.ndarray,
    n_resamples: int,
    seed: int,
    clip: float,
    level: float,
) -> pd.DataFrame:
    steps = sorted(predictions)
    if steps != list(range(len(steps))):
        raise ValueError(f"steps must be consecutive from 0, got {steps}")
    losses = {step: pointwise_log_loss(y, predictions[step], clip) for step in steps}

    def increments(index: np.ndarray | None) -> np.ndarray:
        means = {step: (losses[step] if index is None else losses[step][index]).mean() for step in steps}
        skills = [skill(means[step], means[0]) for step in steps]
        return np.array([skills[k] - skills[k - 1] for k in steps[1:]])

    estimate = increments(None)
    members = _cluster_members(clusters)
    rng = np.random.default_rng(seed)
    draws = np.array([increments(_draw(members, rng)) for _ in range(n_resamples)])
    tail = (1.0 - level) / 2.0
    lower, upper = np.quantile(draws, [tail, 1.0 - tail], axis=0)
    return pd.DataFrame(
        {
            "comparison": [COMPARISONS[k] for k in steps[1:]],
            "estimate": estimate,
            "lower": lower,
            "upper": upper,
            "n_resamples": n_resamples,
            "level": level,
            "metric": "log-loss skill",
        }
    )
