import pytest

from seer_study.cohort import build_cohort
from seer_study.features import build_feature_blocks, design_matrix
from seer_study.labels import UnmappedLabelError
from synthetic import analysis_config, make_frame


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def eligible(acfg):
    return build_cohort(make_frame(), acfg).eligible


def test_blocks_without_pathway_accept_men_without_curative_treatment(eligible, acfg):
    blocks = build_feature_blocks(eligible, acfg, include_pathway=False)
    assert blocks.columns_by_block["pathway"] == []
    assert design_matrix(blocks, 2).shape[0] == len(eligible)
    assert not any(column.startswith("modality_") for column in blocks.frame.columns)


def test_step_3_needs_the_pathway_block(eligible, acfg):
    blocks = build_feature_blocks(eligible, acfg, include_pathway=False)
    with pytest.raises(ValueError, match="pathway"):
        design_matrix(blocks, 3)


def test_pathway_block_still_rejects_men_without_curative_treatment(eligible, acfg):
    with pytest.raises(UnmappedLabelError):
        build_feature_blocks(eligible, acfg)
