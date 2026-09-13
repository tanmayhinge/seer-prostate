import dataclasses

import pytest
import yaml

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import CohortOptions, UnmappedLabelError, build_cohort
from seer_study.config import ConfigError
from synthetic import PROJECT_ROOT, analysis_config, make_frame

INTERVAL = "Time from diagnosis to treatment in days recode"


@pytest.fixture
def acfg():
    return analysis_config()


def test_analysis_config_loads(acfg):
    assert acfg.interval.primary_threshold_days == 90
    assert "A500" in acfg.treatment.prostatectomy_codes
    assert acfg.risk.psa_top_codes["98.0 ng/ml or greater"] == 98.0


def test_analysis_config_rejects_overlapping_codes(tmp_path):
    raw = yaml.safe_load((PROJECT_ROOT / "config" / "analysis.yaml").read_text())
    raw["treatment"]["surgery_other_codes"].append("50")
    path = tmp_path / "analysis.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="50"):
        load_analysis_config(path)


def test_flow_counts_follow_protocol_order(acfg):
    result = build_cohort(make_frame(), acfg)
    assert result.flow["step"].tolist() == [
        "all records",
        "first primary",
        "localised or regional stage",
        "not death certificate or autopsy only",
        "age 40 or over",
        "diagnosed 2010 to 2022",
        "first course includes prostatectomy or radiotherapy",
        "interval recorded or top-coded",
        "interval above 0 days",
    ]
    assert result.flow["remaining"].tolist() == [15, 14, 13, 12, 11, 10, 7, 6, 5]
    assert result.flow["excluded"].tolist() == [0, 1, 1, 1, 1, 1, 3, 1, 1]
    assert sorted(result.frame.index.tolist()) == [0, 9, 10, 11, 12]


def test_derived_treatment_and_interval_columns(acfg):
    frame = build_cohort(make_frame(), acfg).frame
    assert frame.loc[0, "modality"] == "surgery_only"
    assert frame.loc[9, "modality"] == "radiotherapy_only"
    assert frame.loc[10, "modality"] == "both"
    assert frame.loc[9, "interval_days"] == 731
    assert bool(frame.loc[9, "interval_top_coded"]) is True
    assert bool(frame.loc[0, "delayed"]) is False  # 60 days
    assert bool(frame.loc[9, "delayed"]) is True  # 731+ counts as delayed
    assert bool(frame.loc[10, "delayed"]) is True  # 120 days
    assert frame.loc[0, "risk_group"] == "intermediate"


def test_treated_frame_keeps_missing_intervals_for_selection_analysis(acfg):
    result = build_cohort(make_frame(), acfg)
    assert len(result.treated) == 7
    assert result.treated.loc[7, "interval_class"] == "missing"
    assert result.treated.loc[8, "interval_class"] == "recorded"


def test_option_include_2023(acfg):
    result = build_cohort(make_frame(), acfg, CohortOptions(include_2023=True))
    assert 5 in result.frame.index
    assert result.flow.loc[result.flow["step"] == "diagnosed 2010 to 2023", "excluded"].item() == 0


def test_option_include_zero_days(acfg):
    frame = build_cohort(make_frame(), acfg, CohortOptions(include_zero_days=True)).frame
    assert 8 in frame.index
    assert bool(frame.loc[8, "delayed"]) is False


def test_option_strict_first_primary(acfg):
    frame = build_cohort(make_frame(), acfg, CohortOptions(strict_first_primary=True)).frame
    assert 12 not in frame.index


def test_option_exclude_prostatectomy_nos(acfg):
    frame = build_cohort(make_frame(), acfg, CohortOptions(exclude_prostatectomy_nos=True)).frame
    assert 11 not in frame.index


def test_option_threshold_is_strictly_greater(acfg):
    frame = build_cohort(make_frame(), acfg, CohortOptions(threshold_days=60)).frame
    assert bool(frame.loc[0, "delayed"]) is False  # exactly 60 days is within
    assert bool(frame.loc[10, "delayed"]) is True


def test_option_surgery_only(acfg):
    frame = build_cohort(make_frame(), acfg, CohortOptions(surgery_only=True)).frame
    assert set(frame["modality"]) == {"surgery_only"}


def test_unmapped_interval_label_raises(acfg):
    frame = make_frame()
    frame.loc[0, INTERVAL] = "Unknown"
    with pytest.raises(UnmappedLabelError, match="Unknown"):
        build_cohort(frame, acfg)


def test_unmapped_surgery_code_raises(acfg):
    frame = make_frame()
    frame.loc[0, "RX Summ--Surg Prim Site (1998-2022)"] = "55"
    with pytest.raises(UnmappedLabelError, match="55"):
        build_cohort(frame, acfg)


def test_unmapped_radiation_label_raises(acfg):
    frame = make_frame()
    frame.loc[0, "Radiation recode"] = "Proton therapy"
    with pytest.raises(UnmappedLabelError, match="Proton"):
        build_cohort(frame, acfg)


def test_cohort_does_not_mutate_input(acfg):
    frame = make_frame()
    before = frame.copy()
    build_cohort(frame, acfg)
    assert frame.equals(before)
