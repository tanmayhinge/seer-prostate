import numpy as np
import pandas as pd
import pytest
import yaml

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import ConfigError
from seer_study.features import build_feature_blocks, design_matrix, year_as_categories
from seer_study.increments import cluster_size_summary
from synthetic import PROJECT_ROOT, analysis_config, make_frame


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def blocks(acfg):
    return build_feature_blocks(build_cohort(make_frame(), acfg).frame, acfg)


def test_revision_settings_load(acfg):
    assert acfg.revision.fold_seed_repeats == 10
    assert acfg.revision.alternative_cluster_column == "income"
    assert acfg.revision.long_interval_days == 365


def test_fold_seed_repeats_below_two_rejected(tmp_path):
    raw = yaml.safe_load((PROJECT_ROOT / "config" / "analysis.yaml").read_text())
    raw["revision"]["fold_seed_repeats"] = 1
    path = tmp_path / "analysis.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="fold_seed_repeats"):
        load_analysis_config(path)


def test_alternative_cluster_column_must_be_a_configured_column(tmp_path):
    raw = yaml.safe_load((PROJECT_ROOT / "config" / "analysis.yaml").read_text())
    raw["revision"]["alternative_cluster_column"] = "registry"
    path = tmp_path / "analysis.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="alternative_cluster_column"):
        load_analysis_config(path)


def test_design_matrix_excludes_prefixed_columns(blocks):
    full = design_matrix(blocks, 2)
    reduced = design_matrix(blocks, 2, exclude_prefixes=("stage_",))
    assert any(c.startswith("stage_") for c in full.columns)
    assert not any(c.startswith("stage_") for c in reduced.columns)
    assert list(reduced.columns) == [c for c in full.columns if not c.startswith("stage_")]


def test_year_as_categories_replaces_linear_year_and_covid_indicator():
    X = pd.DataFrame({"year": [2010, 2011, 2020], "covid_2020": [0, 0, 1], "age": [60.0, 70.0, 65.0]})
    out = year_as_categories(X, years=[2010, 2011, 2020])
    assert "year" not in out.columns and "covid_2020" not in out.columns
    assert list(out.columns) == ["age", "year_2011", "year_2020"]  # first year is the reference
    assert out["year_2011"].tolist() == [0, 1, 0]
    assert out["year_2020"].tolist() == [0, 0, 1]
    assert "year" in X.columns  # input unchanged


def test_year_as_categories_rejects_unlisted_year():
    X = pd.DataFrame({"year": [2010, 2012], "covid_2020": [0, 0]})
    with pytest.raises(ValueError, match="2012"):
        year_as_categories(X, years=[2010, 2011])


def test_cluster_size_summary_masks_small_smallest_cell():
    clusters = np.array(["a"] * 3 + ["b"] * 10 + ["c"] * 20 + ["d"] * 67)
    out = cluster_size_summary(clusters, threshold=5, mask="<5")
    assert out["clusters"] == 4
    assert out["smallest"] == "<5"
    assert out["median"] == 15.0
    assert out["largest"] == 67
    assert out["largest_share_pct"] == pytest.approx(67.0)


def test_cluster_size_summary_shows_smallest_when_not_small():
    out = cluster_size_summary(np.array(["a"] * 6 + ["b"] * 6), threshold=5, mask="<5")
    assert out["smallest"] == 6
