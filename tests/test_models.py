import numpy as np
import pandas as pd
import pytest

from seer_study.metrics import auc
from seer_study.models import add_interactions, cross_fit_predictions, fold_ids, tune_hyperparameters
from synthetic import analysis_config


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


@pytest.fixture
def signal_data():
    rng = np.random.default_rng(7)
    n = 4000
    x = pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.normal(size=n)})
    y = rng.binomial(1, _sigmoid(2.0 * x["x1"].to_numpy()))
    return x, y


def test_modelling_config_has_grids():
    modelling = analysis_config().modelling
    assert modelling.logistic_c_grid == (0.01, 0.1, 1.0, 10.0)
    assert modelling.lightgbm_grid["num_leaves"] == (15, 63)
    assert modelling.reference_rurality == "Counties in metropolitan areas ge 1 million pop"


def test_fold_ids_partition_and_stratify():
    y = np.array([0] * 50 + [1] * 50)
    folds = fold_ids(y, 5, seed=1)
    assert sorted(set(folds)) == [0, 1, 2, 3, 4]
    for k in range(5):
        assert (folds == k).sum() == 20
        assert y[folds == k].sum() == 10


def test_add_interactions_adds_pairwise_products_only_for_listed_columns():
    frame = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0], "c": [5.0, 6.0]})
    out = add_interactions(frame, ["a", "b"])
    assert list(out.columns) == ["a", "b", "c", "a*b"]
    assert out["a*b"].tolist() == [3.0, 8.0]


def test_cross_fit_logistic_learns_signal(signal_data):
    x, y = signal_data
    p = cross_fit_predictions(x, y, "logistic", {"C": 1.0, "max_iter": 1000}, folds=5, seed=1)
    assert p.shape == (len(y),)
    assert ((p > 0) & (p < 1)).all()
    assert auc(y, p) > 0.75


def test_cross_fit_lightgbm_handles_missing_values(signal_data):
    x, y = signal_data
    x = x.copy()
    x.loc[::10, "x1"] = np.nan
    params = {"n_estimators": 50, "num_leaves": 15, "min_child_samples": 20, "learning_rate": 0.1}
    p = cross_fit_predictions(x, y, "lightgbm", params, folds=3, seed=1)
    assert np.isfinite(p).all()
    assert auc(y, p) > 0.7


def test_noise_features_give_chance_level_auc():
    rng = np.random.default_rng(11)
    n = 6000
    x = pd.DataFrame({"noise": rng.normal(size=n)})
    y = rng.binomial(1, 0.4, size=n)
    p = cross_fit_predictions(x, y, "logistic", {"C": 1.0, "max_iter": 1000}, folds=5, seed=1)
    assert 0.45 < auc(y, p) < 0.55


def test_predictions_are_reproducible_with_seed(signal_data):
    x, y = signal_data
    params = {"n_estimators": 30, "num_leaves": 7, "min_child_samples": 20, "learning_rate": 0.1}
    first = cross_fit_predictions(x, y, "lightgbm", params, folds=3, seed=5)
    second = cross_fit_predictions(x, y, "lightgbm", params, folds=3, seed=5)
    assert np.allclose(first, second)


def test_unknown_model_kind_raises(signal_data):
    x, y = signal_data
    with pytest.raises(ValueError, match="forest"):
        cross_fit_predictions(x, y, "forest", {}, folds=3, seed=1)


def test_tuning_returns_a_grid_member(signal_data):
    x, y = signal_data
    best = tune_hyperparameters(
        x, y, "logistic", grid={"C": (0.01, 1.0)}, fixed={"max_iter": 1000}, folds=3, seed=1, max_rows=2000
    )
    assert best["C"] in (0.01, 1.0)
    assert best["max_iter"] == 1000
