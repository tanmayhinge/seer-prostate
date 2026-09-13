import numpy as np
import pandas as pd
import pytest

from seer_study.cohort import build_cohort
from seer_study.features import build_feature_blocks, design_matrix, one_hot_column
from seer_study.standardise import agreement_label, area_income_ranks, standardised_percentages
from synthetic import analysis_config, make_frame

MARRIED = "Married (including common law)"
SINGLE = "Single (never married)"
METRO = "Counties in metropolitan areas ge 1 million pop"
REMOTE = "Nonmetropolitan counties not adjacent to a metropolitan area"


class Linear:
    """Probability 0.2 + 0.1 remote + 0.05 single + 0.01 income rank."""

    def predict_proba(self, frame):
        p = (
            0.2
            + 0.1 * frame[one_hot_column("rurality", REMOTE)].to_numpy()
            + 0.05 * frame[one_hot_column("marital", SINGLE)].to_numpy()
            + 0.01 * frame["income_rank"].to_numpy()
        )
        return np.column_stack([1 - p, p])


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def step2(acfg):
    cohort = build_cohort(make_frame(), acfg).frame
    return design_matrix(build_feature_blocks(cohort, acfg), 2)


def test_standardised_percentages_known_answer(step2, acfg):
    reference = {"marital": MARRIED, "rurality": METRO, "income_rank": 10.0}
    profiles = {"remote": {"rurality": REMOTE, "income_rank": 5.0}, "single": {"marital": SINGLE}}
    out = standardised_percentages(Linear(), step2, acfg.features, reference, profiles)
    assert out["reference profile"] == pytest.approx(30.0)
    assert out["remote"] == pytest.approx(35.0)
    assert out["single"] == pytest.approx(35.0)
    # every synthetic man is married, large metro, income band $100,000 - $109,999 (rank 14)
    assert out["as observed"] == pytest.approx(34.0)


def test_standardised_percentages_rejects_reserved_profile_names(step2, acfg):
    reference = {"marital": MARRIED, "rurality": METRO, "income_rank": 10.0}
    with pytest.raises(ValueError, match="reserved"):
        standardised_percentages(Linear(), step2, acfg.features, reference, {"as observed": {}})


def test_area_income_ranks_uses_median_rank_of_men_in_each_area():
    ranks = pd.Series([1.0, 3.0, 5.0, np.nan, 10.0])
    rurality = pd.Series(["A", "A", "A", "A", "B"])
    out = area_income_ranks(ranks, rurality, ("A", "B", "C"))
    assert out["A"] == 3.0 and out["B"] == 10.0
    assert np.isnan(out["C"])


@pytest.mark.parametrize(
    ("logistic", "lightgbm", "expected"),
    [
        (-9.2, -8.8, "both models 3 points or more, same direction"),
        (3.0, 4.5, "both models 3 points or more, same direction"),
        (-1.1, -1.6, "both models under 3 points"),
        (3.6, 2.4, "same direction, only one model 3 points or more"),
        (-2.96, -3.20, "same direction, only one model 3 points or more"),
        (4.0, -4.0, "opposite directions, at least one model 3 points or more"),
        (2.0, -3.5, "opposite directions, at least one model 3 points or more"),
    ],
)
def test_agreement_label(logistic, lightgbm, expected):
    assert agreement_label(logistic, lightgbm, minimum=3.0) == expected
