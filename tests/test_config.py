from pathlib import Path

import pytest
import yaml

from seer_study.config import (
    ColumnSpec,
    ConfigError,
    StudyConfig,
    load_config,
    validate_config,
)
from seer_study.io import read_dictionary


@pytest.fixture
def raw(fixtures_dir):
    return yaml.safe_load((fixtures_dir / "mini_study.yaml").read_text())


def _load(tmp_path, raw, root):
    path = tmp_path / "study.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False))
    return load_config(path, root=root)


def test_valid_config_loads_into_typed_objects(mini_config):
    assert isinstance(mini_config, StudyConfig)
    assert type(mini_config.seed) is int
    spec = mini_config.columns["Time from diagnosis to treatment in days recode"]
    assert isinstance(spec, ColumnSpec)
    assert spec.kind == "numeric_string"
    assert spec.top_codes == ("731+ days",)
    assert isinstance(mini_config.roles.clinical, tuple)
    assert mini_config.roles.nonclinical == ()
    assert mini_config.inventory.quantiles == (0.05, 0.25, 0.5, 0.75, 0.95)


def test_paths_resolve_against_root(mini_config, fixtures_dir):
    assert isinstance(mini_config.paths.export, Path)
    assert mini_config.paths.export == fixtures_dir / "mini_export.txt"


def test_era_parsed_with_open_end(mini_config):
    era = mini_config.columns["Derived EOD 2018 T Recode (2018+)"].era
    assert era.first_year == 2018
    assert era.last_year is None
    assert mini_config.columns["Year of diagnosis"].era is None


def test_mini_config_validates_against_dictionary(mini_config):
    validate_config(mini_config, read_dictionary(mini_config.paths.dictionary))


def test_unknown_top_level_key_raises(tmp_path, raw, fixtures_dir):
    raw["surprise"] = 1
    with pytest.raises(ConfigError, match="surprise"):
        _load(tmp_path, raw, fixtures_dir)


def test_unknown_nested_key_raises(tmp_path, raw, fixtures_dir):
    raw["data"]["expected_colums"] = 41
    with pytest.raises(ConfigError, match="expected_colums"):
        _load(tmp_path, raw, fixtures_dir)


def test_missing_key_raises(tmp_path, raw, fixtures_dir):
    del raw["data"]["year_min"]
    with pytest.raises(ConfigError, match="year_min"):
        _load(tmp_path, raw, fixtures_dir)


def test_wrong_type_raises(tmp_path, raw, fixtures_dir):
    raw["data"]["expected_columns"] = "41"
    with pytest.raises(ConfigError, match="expected_columns"):
        _load(tmp_path, raw, fixtures_dir)


def test_bool_is_not_accepted_as_int(tmp_path, raw, fixtures_dir):
    raw["seed"] = True
    with pytest.raises(ConfigError, match="seed"):
        _load(tmp_path, raw, fixtures_dir)


def test_string_is_not_accepted_as_list(tmp_path, raw, fixtures_dir):
    raw["inventory"]["first_primary_strict"] = "One primary only"
    with pytest.raises(ConfigError, match="first_primary_strict"):
        _load(tmp_path, raw, fixtures_dir)


def test_invalid_column_kind_raises(tmp_path, raw, fixtures_dir):
    raw["columns"]["Patient ID"]["kind"] = "free_text"
    with pytest.raises(ConfigError, match="free_text"):
        _load(tmp_path, raw, fixtures_dir)


def test_role_naming_unknown_column_raises(tmp_path, raw, fixtures_dir):
    raw["roles"]["nonclinical"] = ["Insurance Recode (2007+)"]
    cfg = _load(tmp_path, raw, fixtures_dir)
    with pytest.raises(ConfigError, match="Insurance Recode"):
        validate_config(cfg, read_dictionary(cfg.paths.dictionary))


def test_inventory_naming_unknown_column_raises(tmp_path, raw, fixtures_dir):
    raw["inventory"]["stage_column"] = "SEER Summary Stage 2000"
    cfg = _load(tmp_path, raw, fixtures_dir)
    with pytest.raises(ConfigError, match="SEER Summary Stage 2000"):
        validate_config(cfg, read_dictionary(cfg.paths.dictionary))


def test_dictionary_column_without_spec_raises(tmp_path, raw, fixtures_dir):
    del raw["columns"]["Sequence number"]
    cfg = _load(tmp_path, raw, fixtures_dir)
    with pytest.raises(ConfigError, match="Sequence number"):
        validate_config(cfg, read_dictionary(cfg.paths.dictionary))


def test_label_listed_as_both_missing_and_not_applicable_raises(tmp_path, raw, fixtures_dir):
    spec = raw["columns"]["Gleason Score Clinical Recode (2010+)"]
    spec["not_applicable"].append(spec["missing"][0])
    with pytest.raises(ConfigError, match="Gleason Score Clinical"):
        _load(tmp_path, raw, fixtures_dir)
