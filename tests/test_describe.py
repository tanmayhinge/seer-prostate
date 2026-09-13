import math

import numpy as np
import pandas as pd
import pytest
import yaml

from seer_study.config import ConfigError
from seer_study.describe import (
    TableRow,
    categorical_summary,
    continuous_summary,
    gleason_band,
    gleason_band_levels,
    income_group,
    income_group_levels,
    load_reporting_config,
    period_band,
    period_levels,
    psa_band,
    psa_band_levels,
    rurality_group,
    rurality_levels,
    table_one,
)
from seer_study.labels import UnmappedLabelError
from synthetic import PROJECT_ROOT, analysis_config

NAN = float("nan")


@pytest.fixture
def acfg():
    return analysis_config()


@pytest.fixture
def rcfg():
    return load_reporting_config(PROJECT_ROOT / "config" / "reporting.yaml")


def test_reporting_config_rejects_unknown_key(tmp_path):
    raw = yaml.safe_load((PROJECT_ROOT / "config" / "reporting.yaml").read_text())
    raw["colour"] = "blue"
    path = tmp_path / "reporting.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="colour"):
        load_reporting_config(path)


def test_psa_band_uses_risk_thresholds(acfg):
    bands = psa_band(pd.Series([5.0, 10.0, 20.0, 20.1, NAN]), acfg.risk)
    assert bands.tolist() == ["below 10", "10 to 20", "10 to 20", "above 20", "Unknown"]


def test_gleason_band_uses_risk_thresholds(acfg, rcfg):
    bands = gleason_band(pd.Series([6.0, 5.0, 7.0, 8.0, 10.0, NAN]), acfg.risk, rcfg)
    assert bands.tolist() == ["6 or less", "6 or less", "7", "8 to 10", "8 to 10", "Unknown"]


def test_income_group_quartiles_of_ordered_bands(acfg, rcfg):
    groups = income_group(pd.Series([1.0, 4.0, 5.0, 16.0, NAN]), acfg.features, rcfg)
    assert groups.tolist() == ["Q1 (lowest)", "Q1 (lowest)", "Q2", "Q4 (highest)", "Unknown"]


def test_period_band(acfg, rcfg):
    periods = period_band(pd.Series([2010, 2014, 2015, 2020, 2022]), acfg.cohort, rcfg)
    assert periods.tolist() == ["2010 to 2014", "2010 to 2014", "2015 to 2019", "2020 to 2022", "2020 to 2022"]


def test_rurality_group_maps_display_names_and_unknowns(acfg, rcfg):
    values = pd.Series(
        [
            "Counties in metropolitan areas ge 1 million pop",
            "Unknown/missing/no match/Not 1990-2024",
            "Nonmetropolitan counties not adjacent to a metropolitan area",
        ]
    )
    assert rurality_group(values, acfg.features, rcfg).tolist() == [
        "Metro, 1 million or more",
        "Unknown",
        "Nonmetro, not adjacent to metro",
    ]


def test_band_levels_follow_config_order(acfg, rcfg):
    assert gleason_band_levels(acfg.risk, rcfg) == ("6 or less", "7", "8 to 10", "Unknown")
    assert psa_band_levels(acfg.risk) == ("below 10", "10 to 20", "above 20", "Unknown")
    assert income_group_levels(rcfg) == ("Q1 (lowest)", "Q2", "Q3", "Q4 (highest)", "Unknown")
    assert period_levels(acfg.cohort, rcfg) == ("2010 to 2014", "2015 to 2019", "2020 to 2022")
    assert period_levels(acfg.cohort, rcfg, year_max=2023) == ("2010 to 2014", "2015 to 2019", "2020 to 2023")
    assert rurality_levels(rcfg) == (
        "Metro, 1 million or more",
        "Metro, 250,000 to 1 million",
        "Metro, under 250,000",
        "Nonmetro, adjacent to metro",
        "Nonmetro, not adjacent to metro",
        "Unknown",
    )


def test_gleason_band_label_uses_display_maximum(acfg, rcfg):
    assert gleason_band(pd.Series([9.0]), acfg.risk, rcfg).tolist() == ["8 to 10"]


def test_rurality_group_unmapped_raises(acfg, rcfg):
    with pytest.raises(UnmappedLabelError, match="Frontier"):
        rurality_group(pd.Series(["Frontier county"]), acfg.features, rcfg)


@pytest.fixture
def small():
    return pd.DataFrame({"g": ["a", "a", "b", "b", "b"], "x": ["u", "v", "u", "u", "w"], "days": [10.0, 30.0, 5.0, 7.0, 9.0]})


def test_categorical_summary_counts_percentages_and_zero_levels(small):
    out = categorical_summary(small, "x", "g", levels=("u", "v", "w"))
    lookup = out.set_index(["group", "level"])
    assert lookup.loc[("a", "u"), "n"] == 1
    assert math.isclose(lookup.loc[("a", "u"), "pct"], 50.0)
    assert lookup.loc[("a", "w"), "n"] == 0
    assert math.isclose(lookup.loc[("b", "u"), "pct"], 200 / 3)
    for group in ("a", "b"):
        assert math.isclose(out[out["group"] == group]["pct"].sum(), 100.0)


def test_categorical_summary_unlisted_level_raises(small):
    with pytest.raises(UnmappedLabelError, match="w"):
        categorical_summary(small, "x", "g", levels=("u", "v"))


def test_continuous_summary(small):
    out = continuous_summary(small, "days", "g").set_index("group")
    assert out.loc["a", "median"] == 20.0
    assert out.loc["b", "median"] == 7.0
    assert out.loc["b", "q1"] == 6.0
    assert out.loc["b", "q3"] == 8.0


def test_table_one_layout_and_formatting(small):
    table = table_one(
        small,
        group="g",
        group_levels=("a", "b"),
        rows=[TableRow("X category", "x", ("u", "v", "w")), TableRow("Days", "days", None)],
    )
    assert table.columns.tolist() == ["characteristic", "level", "Overall", "a", "b"]
    header = table.iloc[0]
    assert header["characteristic"] == "Men, n"
    assert header["Overall"] == "5" and header["a"] == "2" and header["b"] == "3"
    u_row = table[(table["characteristic"] == "X category") & (table["level"] == "u")].iloc[0]
    assert u_row["a"] == "1 (50.0%)"
    assert u_row["Overall"] == "3 (60.0%)"
    days_row = table[table["characteristic"] == "Days"].iloc[0]
    assert days_row["b"] == "7.0 (6.0 to 8.0)"
    assert days_row["level"] == "median (IQR)"
