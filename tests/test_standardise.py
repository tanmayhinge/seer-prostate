import numpy as np
import pandas as pd
import pytest

from seer_study.cohort import build_cohort
from seer_study.features import build_feature_blocks, design_matrix
from seer_study.labels import UnmappedLabelError
from seer_study.models import fit_full_model
from seer_study.standardise import excess_days_per_1000, set_social_profile, standardised_mean
from synthetic import analysis_config, make_frame

SINGLE = "Single (never married)"
REMOTE = "Nonmetropolitan counties not adjacent to a metropolitan area"


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def step2(acfg):
    cohort = build_cohort(make_frame(), acfg).frame
    return design_matrix(build_feature_blocks(cohort, acfg), 2)


def test_set_social_profile_sets_every_social_feature(step2, acfg):
    out = set_social_profile(step2, acfg.features, marital=SINGLE, rurality=REMOTE, income_rank=3.0)
    marital = [c for c in out.columns if c.startswith("marital_")]
    rurality = [c for c in out.columns if c.startswith("rurality_")]
    assert (out["marital_single_never_married"] == 1).all()
    assert out[[c for c in marital if c != "marital_single_never_married"]].eq(0).all().all()
    assert (out["rurality_nonmetropolitan_counties_not_adjacent_to_a_metropolitan_area"] == 1).all()
    assert out[[c for c in rurality if c != "rurality_nonmetropolitan_counties_not_adjacent_to_a_metropolitan_area"]].eq(0).all().all()
    assert (out["income_rank"] == 3.0).all() and (out["income_unknown"] == 0).all()


def test_set_social_profile_leaves_other_features_and_input_unchanged(step2, acfg):
    before = step2.copy()
    out = set_social_profile(step2, acfg.features, marital=SINGLE, rurality=REMOTE, income_rank=3.0)
    other = [c for c in step2.columns if not c.startswith(("marital_", "rurality_", "income_"))]
    assert out[other].equals(step2[other])
    assert step2.equals(before)


def test_set_social_profile_unknown_label_raises(step2, acfg):
    with pytest.raises(UnmappedLabelError, match="Engaged"):
        set_social_profile(step2, acfg.features, marital="Engaged", rurality=REMOTE, income_rank=3.0)


def test_standardised_mean_averages_model_predictions():
    class Constant:
        def predict_proba(self, frame):
            p = frame["x"].to_numpy() / 10.0
            return np.column_stack([1 - p, p])

    frame = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    assert standardised_mean(Constant(), frame) == pytest.approx(0.2)


def test_fit_full_model_predicts_probabilities():
    rng = np.random.default_rng(4)
    frame = pd.DataFrame({"a": rng.normal(size=500), "b": rng.normal(size=500)})
    y = rng.binomial(1, 1 / (1 + np.exp(-frame["a"].to_numpy())))
    model = fit_full_model(frame, y, "logistic", {"C": 1.0, "max_iter": 1000}, seed=1, interaction_columns=["a", "b"])
    p = model.predict_proba(frame)[:, 1]
    assert p.shape == (500,) and ((p > 0) & (p < 1)).all()


def test_excess_days_per_1000():
    days = np.array([60.0, 100.0, 731.0])
    assert excess_days_per_1000(days, threshold=90) == pytest.approx(217_000.0)
