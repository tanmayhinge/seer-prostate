import numpy as np
import pytest

from seer_study.increments import bootstrap_increments, cluster_bootstrap_interval, resample_clusters, step_metrics

CLIP = 1e-6


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def _synthetic(social_effect, seed=3, n=30_000, n_clusters=40):
    rng = np.random.default_rng(seed)
    clinical = rng.normal(size=n)
    social = rng.normal(size=n)
    clusters = rng.integers(0, n_clusters, size=n).astype(str)
    y = rng.binomial(1, _sigmoid(clinical + social_effect * social))
    predictions = {
        0: np.full(n, y.mean()),
        1: _sigmoid(clinical),
        2: _sigmoid(clinical + social_effect * social),
    }
    return y, predictions, clusters


def test_step_metrics_skill_is_relative_to_step_zero():
    y, predictions, _ = _synthetic(social_effect=1.5)
    table = step_metrics(y, predictions, CLIP).set_index("step")
    assert table.loc[0, "log_loss_skill"] == 0.0
    assert table.loc[1, "log_loss_skill"] > 0
    assert table.loc[2, "log_loss_skill"] > table.loc[1, "log_loss_skill"]
    for column in ("log_loss", "brier", "auc", "calibration_intercept", "calibration_slope", "brier_skill"):
        assert column in table.columns


def test_resample_keeps_clusters_whole():
    clusters = np.array(["a", "a", "b", "b", "b", "c"])
    rng = np.random.default_rng(0)
    for _ in range(20):
        index = resample_clusters(clusters, rng)
        counts = np.bincount(index, minlength=len(clusters))
        for label in ("a", "b", "c"):
            member_counts = counts[clusters == label]
            assert len(set(member_counts)) == 1  # every member of a cluster appears equally often


def test_social_increment_is_positive_when_outcome_depends_on_social_position():
    y, predictions, clusters = _synthetic(social_effect=1.5)
    summary = bootstrap_increments(y, predictions, clusters, n_resamples=200, seed=1, clip=CLIP, level=0.95)
    row = summary.set_index("comparison").loc["social position (step 1 to 2)"]
    assert row["estimate"] > 0
    assert row["lower"] > 0


def test_social_increment_is_zero_when_outcome_ignores_social_position():
    y, predictions, clusters = _synthetic(social_effect=0.0)
    summary = bootstrap_increments(y, predictions, clusters, n_resamples=200, seed=1, clip=CLIP, level=0.95)
    row = summary.set_index("comparison").loc["social position (step 1 to 2)"]
    assert row["estimate"] == pytest.approx(0.0, abs=1e-12)
    assert row["lower"] <= 0 <= row["upper"]


def test_cluster_bootstrap_interval_for_a_mean():
    rng = np.random.default_rng(5)
    y = rng.binomial(1, 0.3, size=20_000)
    clusters = rng.integers(0, 50, size=20_000).astype(str)
    estimate, lower, upper = cluster_bootstrap_interval(lambda index: y[index].mean(), clusters, n_resamples=200, seed=2, level=0.95)
    assert estimate == pytest.approx(y.mean())
    assert lower < estimate < upper
    assert upper - lower < 0.05
    again = cluster_bootstrap_interval(lambda index: y[index].mean(), clusters, n_resamples=200, seed=2, level=0.95)
    assert again == (estimate, lower, upper)


def test_bootstrap_is_reproducible_and_reports_all_consecutive_steps():
    y, predictions, clusters = _synthetic(social_effect=0.5)
    first = bootstrap_increments(y, predictions, clusters, n_resamples=50, seed=9, clip=CLIP, level=0.95)
    second = bootstrap_increments(y, predictions, clusters, n_resamples=50, seed=9, clip=CLIP, level=0.95)
    assert first.equals(second)
    assert first["comparison"].tolist() == ["clinical need (step 0 to 1)", "social position (step 1 to 2)"]
