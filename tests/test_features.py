import math

import numpy as np
import pytest

from seer_study.cohort import UnmappedLabelError, build_cohort
from seer_study.features import STEPS, build_feature_blocks, design_matrix
from synthetic import analysis_config, make_frame


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def cohort(acfg):
    return build_cohort(make_frame(), acfg).frame


def test_blocks_are_disjoint_and_aligned(cohort, acfg):
    blocks = build_feature_blocks(cohort, acfg)
    names = ["base", "clinical", "social", "pathway"]
    column_sets = [set(blocks.columns_by_block[name]) for name in names]
    for i in range(len(column_sets)):
        for j in range(i + 1, len(column_sets)):
            assert not column_sets[i] & column_sets[j], (names[i], names[j])
    for name in names:
        assert blocks.frame[blocks.columns_by_block[name]].index.equals(cohort.index)


def test_steps_are_cumulative_in_protocol_order(cohort, acfg):
    blocks = build_feature_blocks(cohort, acfg)
    assert STEPS == (("base",), ("base", "clinical"), ("base", "clinical", "social"), ("base", "clinical", "social", "pathway"))
    step2 = design_matrix(blocks, 2)
    assert set(step2.columns) == set(blocks.columns_by_block["base"]) | set(blocks.columns_by_block["clinical"]) | set(
        blocks.columns_by_block["social"]
    )
    assert not set(step2.columns) & set(blocks.columns_by_block["pathway"])


def test_social_block_never_contains_clinical_or_pathway_information(cohort, acfg):
    social = build_feature_blocks(cohort, acfg).columns_by_block["social"]
    for column in social:
        assert not any(word in column for word in ("gleason", "psa", "stage", "age", "modality", "year"))


def test_feature_values(cohort, acfg):
    frame = build_feature_blocks(cohort, acfg).frame
    assert frame.loc[0, "year"] == 2015
    assert frame.loc[0, "covid_2020"] == 0
    assert frame.loc[0, "gleason_score"] == 7
    assert math.isclose(frame.loc[0, "log_psa"], math.log(6.6))
    assert frame.loc[0, "age_midpoint"] == 67.0
    assert frame.loc[0, "income_rank"] == 14  # "$100,000 - $109,999" is the 14th of 16 bands
    assert frame.loc[0, "marital_married_including_common_law"] == 1
    assert frame.loc[0, "rurality_counties_in_metropolitan_areas_ge_1_million_pop"] == 1
    assert frame.loc[9, "modality_radiotherapy_only"] == 1


def test_numeric_matrix_has_no_strings(cohort, acfg):
    matrix = design_matrix(build_feature_blocks(cohort, acfg), 3)
    assert all(np.issubdtype(dtype, np.number) for dtype in matrix.dtypes)


def test_unknown_income_sets_indicator(acfg):
    frame = make_frame()
    frame["Median household income inflation adj to 2024"] = "Unknown/missing/no match/Not 1990-2024"
    cohort = build_cohort(frame, acfg).frame
    features = build_feature_blocks(cohort, acfg).frame
    assert (features["income_unknown"] == 1).all()
    assert features["income_rank"].isna().all()


def test_unmapped_marital_label_raises(acfg):
    frame = make_frame()
    frame["Marital status at diagnosis"] = "Engaged"
    cohort = build_cohort(frame, acfg).frame
    with pytest.raises(UnmappedLabelError, match="Engaged"):
        build_feature_blocks(cohort, acfg)
