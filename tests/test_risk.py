import math

import numpy as np
import pandas as pd
import pytest

from seer_study.cohort import UnmappedLabelError
from seer_study.risk import assign_risk, parse_gleason, parse_psa, stage_class
from synthetic import analysis_config


@pytest.fixture
def acfg():
    return analysis_config()


def test_parse_gleason(acfg):
    values = pd.Series(["Gleason score 6", "Gleason score 10", "No needle core biopsy/TURP performed", "Blank(s)"])
    parsed = parse_gleason(values, acfg.risk)
    assert parsed.iloc[0] == 6
    assert parsed.iloc[1] == 10
    assert math.isnan(parsed.iloc[2]) and math.isnan(parsed.iloc[3])


def test_parse_gleason_unmapped_raises(acfg):
    with pytest.raises(UnmappedLabelError, match="Grade Group 2"):
        parse_gleason(pd.Series(["Grade Group 2"]), acfg.risk)


def test_parse_psa(acfg):
    values = pd.Series(["6.6", "98.0 ng/ml or greater", "0.1 or less nanograms/milliliter (ng/ml)", "Test ordered, results not in chart"])
    parsed = parse_psa(values, acfg.risk)
    assert parsed.iloc[0] == 6.6
    assert parsed.iloc[1] == 98.0
    assert parsed.iloc[2] == 0.1
    assert math.isnan(parsed.iloc[3])


def test_parse_psa_unmapped_raises(acfg):
    with pytest.raises(UnmappedLabelError, match="elevated"):
        parse_psa(pd.Series(["elevated"]), acfg.risk)


def test_stage_class(acfg):
    values = pd.Series(
        [
            "Localized only",
            "Regional by direct extension only",
            "Regional lymph nodes involved only",
            "Regional by both direct extension and lymph node involvement",
            "Distant site(s)/node(s) involved",
        ]
    )
    assert stage_class(values, acfg.cohort).tolist() == [
        "localised",
        "regional_extension",
        "regional_nodes",
        "regional_nodes",
        "other",
    ]


NAN = float("nan")
TRUTH_TABLE = [
    # stage, gleason, psa, expected
    ("localised", 6, 5.0, "low"),
    ("localised", 5, 9.9, "low"),
    ("localised", 6, 10.0, "intermediate"),
    ("localised", 6, 20.0, "intermediate"),
    ("localised", 7, 4.0, "intermediate"),
    ("localised", 6, 20.1, "high"),
    ("localised", 8, 4.0, "high"),
    ("localised", 10, 4.0, "high"),
    ("regional_extension", 6, 4.0, "high"),
    ("regional_nodes", 6, 4.0, "high"),
    ("regional_extension", NAN, NAN, "high"),
    ("localised", 8, NAN, "high"),
    ("localised", NAN, 25.0, "high"),
    ("localised", 7, NAN, "unknown"),
    ("localised", 6, NAN, "unknown"),
    ("localised", NAN, 5.0, "unknown"),
]


@pytest.mark.parametrize("stage,gleason,psa,expected", TRUTH_TABLE)
def test_assign_risk_truth_table(acfg, stage, gleason, psa, expected):
    result = assign_risk(pd.Series([stage]), pd.Series([gleason], dtype=float), pd.Series([psa], dtype=float), acfg.risk)
    assert result.iloc[0] == expected


def test_assign_risk_without_stage_treats_regional_like_localised(acfg):
    result = assign_risk(
        pd.Series(["regional_extension"]), pd.Series([6.0]), pd.Series([4.0]), acfg.risk, use_stage=False
    )
    assert result.iloc[0] == "low"


def test_assign_risk_rejects_other_stage(acfg):
    with pytest.raises(ValueError, match="other"):
        assign_risk(pd.Series(["other"]), pd.Series([6.0]), pd.Series([4.0]), acfg.risk)
