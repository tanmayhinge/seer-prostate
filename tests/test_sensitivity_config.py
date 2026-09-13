import dataclasses

import pytest
import yaml

from seer_study.analysis_config import ScenarioSpec, load_analysis_config
from seer_study.cohort import CohortOptions, scenario_options
from seer_study.config import ConfigError
from synthetic import PROJECT_ROOT, analysis_config


def _write(tmp_path, raw):
    path = tmp_path / "analysis.yaml"
    path.write_text(yaml.safe_dump(raw))
    return path


def _raw():
    return yaml.safe_load((PROJECT_ROOT / "config" / "analysis.yaml").read_text())


def test_protocol_scenarios_load():
    acfg = analysis_config()
    names = [s.name for s in acfg.sensitivity.scenarios]
    assert len(names) == len(set(names)) == 10
    thresholds = sorted(s.threshold_days for s in acfg.sensitivity.scenarios if s.threshold_days is not None)
    assert thresholds == sorted(acfg.interval.sensitivity_thresholds_days)
    assert acfg.receipt.risk_groups == ("intermediate", "high")


def test_every_cohort_option_is_available_to_scenarios():
    scenario_fields = {f.name for f in dataclasses.fields(ScenarioSpec)}
    assert {f.name for f in dataclasses.fields(CohortOptions)} <= scenario_fields


def test_scenario_options_copies_settings():
    spec = ScenarioSpec(name="x", description="x", exclude_covid_year=True)
    assert scenario_options(spec) == CohortOptions(exclude_covid_year=True)
    assert scenario_options(ScenarioSpec(name="t", description="t", threshold_days=60)).threshold_days == 60


def test_scenario_changing_two_settings_is_rejected(tmp_path):
    raw = _raw()
    raw["sensitivity"]["scenarios"][3]["surgery_only"] = True
    with pytest.raises(ConfigError, match="exactly one"):
        load_analysis_config(_write(tmp_path, raw))


def test_scenario_changing_nothing_is_rejected(tmp_path):
    raw = _raw()
    raw["sensitivity"]["scenarios"].append({"name": "same", "description": "primary again"})
    with pytest.raises(ConfigError, match="exactly one"):
        load_analysis_config(_write(tmp_path, raw))


def test_duplicate_scenario_names_are_rejected(tmp_path):
    raw = _raw()
    raw["sensitivity"]["scenarios"][1]["name"] = raw["sensitivity"]["scenarios"][0]["name"]
    with pytest.raises(ConfigError, match="duplicate"):
        load_analysis_config(_write(tmp_path, raw))


def test_threshold_scenarios_must_match_interval_thresholds(tmp_path):
    raw = _raw()
    raw["sensitivity"]["scenarios"][0]["threshold_days"] = 45
    with pytest.raises(ConfigError, match="threshold"):
        load_analysis_config(_write(tmp_path, raw))
