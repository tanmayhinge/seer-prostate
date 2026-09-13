"""Cross-fitted prediction models: penalised logistic regression and LightGBM (PROTOCOL.md section 7).

Every prediction for a man comes from a model fitted without him (out-of-fold), so performance measures are
out-of-sample.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from seer_study.metrics import log_loss

MODEL_KINDS = ("logistic", "lightgbm")


def fold_ids(y: np.ndarray, folds: int, seed: int) -> np.ndarray:
    """Stratified fold number (0 to folds - 1) for every observation."""
    ids = np.empty(len(y), dtype=int)
    splitter = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    for fold, (_, test) in enumerate(splitter.split(np.zeros(len(y)), y)):
        ids[test] = fold
    return ids


def add_interactions(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Append pairwise products of the listed columns, named "a*b"."""
    out = frame.copy()
    for left, right in combinations(columns, 2):
        out[f"{left}*{right}"] = frame[left] * frame[right]
    return out


def make_model(kind: str, params: dict, seed: int):
    if kind == "logistic":
        return make_pipeline(
            SimpleImputer(strategy="median", keep_empty_features=True),
            StandardScaler(),
            LogisticRegression(C=params["C"], max_iter=params["max_iter"]),
        )
    if kind == "lightgbm":
        return LGBMClassifier(
            n_estimators=params["n_estimators"],
            num_leaves=params["num_leaves"],
            min_child_samples=params["min_child_samples"],
            learning_rate=params["learning_rate"],
            random_state=seed,
            deterministic=True,
            force_row_wise=True,
            verbose=-1,
        )
    raise ValueError(f"unknown model kind {kind!r}; expected one of {MODEL_KINDS}")


def cross_fit_predictions(
    X: pd.DataFrame,
    y: np.ndarray,
    kind: str,
    params: dict,
    folds: int,
    seed: int,
    interaction_columns: list[str] | tuple[str, ...] = (),
) -> np.ndarray:
    """Out-of-fold predicted probabilities of the positive class."""
    make_model(kind, params, seed)  # validate the kind before any fitting
    y = np.asarray(y)
    data = add_interactions(X, list(interaction_columns)) if interaction_columns else X
    ids = fold_ids(y, folds, seed)
    predictions = np.empty(len(y), dtype=float)
    for fold in range(folds):
        train = ids != fold
        model = make_model(kind, params, seed)
        model.fit(data[train], y[train])
        predictions[~train] = model.predict_proba(data[~train])[:, 1]
    return predictions


def tune_hyperparameters(
    X: pd.DataFrame,
    y: np.ndarray,
    kind: str,
    grid: dict[str, tuple],
    fixed: dict,
    folds: int,
    seed: int,
    max_rows: int,
    interaction_columns: list[str] | tuple[str, ...] = (),
    clip: float = 1e-6,
) -> dict:
    """Grid search by cross-validated log-loss on a random subsample of at most ``max_rows`` rows."""
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    if len(y) > max_rows:
        keep = np.sort(rng.choice(len(y), size=max_rows, replace=False))
        X, y = X.iloc[keep], y[keep]
    best_params, best_loss = None, float("inf")
    for values in product(*grid.values()):
        params = {**fixed, **dict(zip(grid, values))}
        predictions = cross_fit_predictions(X, y, kind, params, folds, seed, interaction_columns)
        loss = log_loss(y, predictions, clip)
        if loss < best_loss:
            best_params, best_loss = params, loss
    return best_params


@dataclass
class FittedModel:
    """A model fitted on all rows; adds the same interaction terms at prediction time."""

    model: object
    interaction_columns: tuple[str, ...]

    def predict_proba(self, frame: pd.DataFrame) -> np.ndarray:
        data = add_interactions(frame, list(self.interaction_columns)) if self.interaction_columns else frame
        return self.model.predict_proba(data)


def fit_full_model(
    X: pd.DataFrame,
    y: np.ndarray,
    kind: str,
    params: dict,
    seed: int,
    interaction_columns: list[str] | tuple[str, ...] = (),
) -> FittedModel:
    """Fit one model on every row, for standardisation (g-computation) rather than for measuring performance."""
    data = add_interactions(X, list(interaction_columns)) if interaction_columns else X
    model = make_model(kind, params, seed)
    model.fit(data, np.asarray(y))
    return FittedModel(model=model, interaction_columns=tuple(interaction_columns))
