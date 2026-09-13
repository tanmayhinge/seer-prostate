import pytest

from seer_study.cohort import CohortOptions, build_cohort
from synthetic import analysis_config, make_frame


@pytest.fixture
def acfg():
    return analysis_config()


def test_eligible_frame_keeps_men_without_curative_treatment(acfg):
    result = build_cohort(make_frame(), acfg)
    assert sorted(result.eligible.index.tolist()) == [0, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert int(result.eligible["curative"].sum()) == 7
    assert bool(result.eligible.loc[6, "curative"]) is False
    assert bool(result.eligible.loc[14, "curative"]) is False  # radiation refused, no surgery


def test_eligible_men_have_risk_groups(acfg):
    eligible = build_cohort(make_frame(), acfg).eligible
    assert eligible.loc[6, "risk_group"] == "intermediate"
    assert eligible["risk_group"].notna().all()


def test_treated_frame_is_the_curative_part_of_eligible(acfg):
    result = build_cohort(make_frame(), acfg)
    assert result.treated.index.equals(result.eligible.index[result.eligible["curative"].to_numpy()])
    assert result.treated["risk_group"].equals(result.eligible.loc[result.treated.index, "risk_group"])


def test_option_exclude_covid_year(acfg):
    rows = [({}, "included"), ({"Year of diagnosis": "2020"}, "covid year")]
    result = build_cohort(make_frame(rows), acfg, CohortOptions(exclude_covid_year=True))
    assert result.frame.index.tolist() == [0]
    step = f"not diagnosed in {acfg.features.covid_year}"
    assert result.flow.loc[result.flow["step"] == step, "excluded"].item() == 1
    assert 1 not in result.eligible.index


def test_covid_year_kept_by_default(acfg):
    rows = [({}, "included"), ({"Year of diagnosis": "2020"}, "covid year")]
    result = build_cohort(make_frame(rows), acfg)
    assert result.frame.index.tolist() == [0, 1]
    assert not result.flow["step"].str.startswith("not diagnosed in").any()
