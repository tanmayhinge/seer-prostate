import dataclasses
import math

import pandas as pd
import pytest

from seer_study import inventory as inv

TTT = "Time from diagnosis to treatment in days recode"
GLEASON_C = "Gleason Score Clinical Recode (2010+)"
GLEASON_P = "Gleason Score Pathological Recode (2010+)"
EOD_T = "Derived EOD 2018 T Recode (2018+)"
PSA = "PSA Lab Value Recode (2010+)"
REASON = "Reason no cancer-directed surgery"
STAGE = "Combined Summary Stage with Expanded Regional Codes (2004+)"
YEAR = "Year of diagnosis"


def test_row_summary(mini_frame, mini_config):
    summary = inv.row_summary(mini_frame, mini_config.data)
    assert summary.rows == 6
    assert summary.columns == 12
    assert summary.unique_ids == 6
    assert summary.rows_sharing_an_id == 0


def test_row_summary_counts_duplicate_ids(mini_frame, mini_config):
    frame = mini_frame.copy()
    frame.loc[5, "Patient ID"] = "00000225"
    summary = inv.row_summary(frame, mini_config.data)
    assert summary.unique_ids == 5
    assert summary.rows_sharing_an_id == 2


def test_frequency_sums_to_n_for_every_column(mini_frame):
    for column in mini_frame.columns:
        table = inv.frequency(mini_frame[column])
        assert table["n"].sum() == len(mini_frame)
        assert math.isclose(table["pct"].sum(), 100.0)


def test_frequency_sorted_by_count_descending(mini_frame):
    table = inv.frequency(mini_frame[STAGE])
    assert table.iloc[0]["value"] == "Localized only"
    assert table.iloc[0]["n"] == 4
    assert table["n"].is_monotonic_decreasing


def test_missingness_pathological_grade(mini_frame, mini_config):
    table = inv.missingness(mini_frame, mini_config).set_index("column")
    row = table.loc[GLEASON_P]
    assert row["blank_in_era"] == 0
    assert row["blank_structural"] == 0
    assert row["unknown"] == 1
    assert row["not_applicable"] == 4
    assert row["known"] == 1


def test_missingness_separates_structural_blanks_by_era(mini_frame, mini_config):
    row = inv.missingness(mini_frame, mini_config).set_index("column").loc[EOD_T]
    assert row["blank_structural"] == 2  # 2011 rows, before the 2018+ era
    assert row["blank_in_era"] == 1  # 2023 row with Blank(s)
    assert row["not_applicable"] == 1  # code 88
    assert row["known"] == 2
    assert row["n_in_era"] == 4
    assert math.isclose(row["pct_missing_in_era"], 25.0)


def test_missingness_numeric_string_top_codes_count_as_known(mini_frame, mini_config):
    row = inv.missingness(mini_frame, mini_config).set_index("column").loc[PSA]
    assert row["blank_in_era"] == 1
    assert row["unknown"] == 1
    assert row["top_coded"] == 1
    assert row["known"] == 4  # 6.6, 7.7, 4.5 and the 98.0+ top code


def test_missingness_only_counts_configured_labels(mini_frame, mini_config):
    row = inv.missingness(mini_frame, mini_config).set_index("column").loc[REASON]
    assert row["unknown"] == 0
    assert row["not_applicable"] == 0
    assert row["known"] == 6


def test_missingness_components_reconcile(mini_frame, mini_config):
    table = inv.missingness(mini_frame, mini_config)
    parts = table[["blank_in_era", "blank_structural", "unknown", "not_applicable", "known"]].sum(axis=1)
    assert (parts == table["n"]).all()


def test_classify_numeric_string_time_to_treatment(mini_frame, mini_config):
    spec = mini_config.columns[TTT]
    classes = inv.classify_numeric_string(mini_frame[TTT], spec, mini_config.data.blank_label)
    counts = classes.value_counts()
    assert counts["numeric"] == 4
    assert counts["Unable to calculate"] == 1
    assert counts["731+ days"] == 1


def test_classify_numeric_string_unexpected_label_raises(mini_config):
    spec = mini_config.columns[TTT]
    series = pd.Series(["12", "Unknown"], dtype=str)
    with pytest.raises(inv.UnexpectedLabelError, match="Unknown"):
        inv.classify_numeric_string(series, spec, mini_config.data.blank_label)


def test_time_to_treatment_profile(mini_frame, mini_config):
    profile = inv.time_to_treatment_profile(mini_frame, mini_config)
    categories = profile.categories.set_index("value")["n"]
    assert categories["numeric"] == 4
    assert categories["Unable to calculate"] == 1
    assert categories["731+ days"] == 1
    quantiles = profile.quantiles.set_index("quantile")["days"]
    assert quantiles[0.5] == 28.5  # median of 0, 12, 45, 127
    assert profile.bins["n"].sum() == 4
    assert profile.by_year.loc["2023", "731+ days"] == 1


def test_completeness_by_year(mini_frame, mini_config):
    table = inv.completeness_by_year(mini_frame, [GLEASON_C], mini_config)
    by_year = table.set_index("year")
    assert by_year.loc["2011", "n"] == 2
    assert by_year.loc["2011", "known"] == 2
    assert by_year.loc["2021", "known"] == 0
    assert by_year.loc["2021", "unknown"] == 1
    assert math.isclose(by_year.loc["2011", "pct_known"], 100.0)


def test_completeness_by_year_lists_every_configured_year(mini_frame, mini_config):
    table = inv.completeness_by_year(mini_frame, [GLEASON_C], mini_config)
    assert table["year"].tolist() == [str(y) for y in range(2010, 2024)]
    empty = table.set_index("year").loc["2010"]
    assert empty["n"] == 0
    assert math.isnan(empty["pct_known"])


def test_surgery_code_group(mini_frame, mini_config):
    groups = inv.surgery_code_group(mini_frame, mini_config)
    assert groups.tolist() == ["none", "performed", "none", "performed", "none", "none"]


def test_surgery_code_group_unknown_and_both_blank(mini_frame, mini_config):
    frame = mini_frame.copy()
    frame.loc[0, "RX Summ--Surg Prim Site (1998-2022)"] = "99"
    frame.loc[1, "RX Summ--Surg Prim Site (1998-2022)"] = "Blank(s)"
    groups = inv.surgery_code_group(frame, mini_config)
    assert groups.iloc[0] == "unknown"
    assert groups.iloc[1] == "both_blank"


def test_completeness_by_group(mini_frame, mini_config):
    groups = inv.surgery_code_group(mini_frame, mini_config)
    table = inv.completeness_by_group(mini_frame, GLEASON_P, groups, mini_config).set_index("group")
    assert table.loc["performed", "n"] == 2
    assert table.loc["performed", "known"] == 1
    assert table.loc["none", "known"] == 0
    assert table.loc["none", "not_applicable"] == 4


def test_sequence_profile(mini_frame, mini_config):
    profile = inv.sequence_profile(mini_frame, mini_config)
    assert profile.first_primary_strict == 4
    assert profile.first_primary_inclusive == 5
    assert profile.frequency["n"].sum() == 6


def test_sequence_profile_requires_exact_labels(mini_frame, mini_config):
    frame = mini_frame.copy()
    frame["Sequence number"] = " One primary only"
    profile = inv.sequence_profile(frame, mini_config)
    assert profile.first_primary_strict == 0


def test_crosstab_counts_and_margins(mini_frame):
    table = inv.crosstab_counts(mini_frame, STAGE, YEAR)
    assert table.loc["Localized only", "2011"] == 2
    assert table.loc["Total", "Total"] == 6


def test_column_percentages_sum_to_100(mini_frame):
    pct = inv.column_percentages(mini_frame, STAGE, YEAR)
    for year in ["2011", "2019", "2021", "2023"]:
        assert math.isclose(pct[year].sum(), 100.0)


def test_single_valued_columns(mini_frame):
    frame = mini_frame.copy()
    frame["Race and origin (recommended by SEER)"] = "All races/ethnicities"
    assert inv.single_valued_columns(frame) == ["Race and origin (recommended by SEER)"]


def test_nonblank_by_year(mini_frame, mini_config):
    old, new = mini_config.inventory.surgery_columns
    table = inv.nonblank_by_year(mini_frame, [old, new], mini_config)
    assert table.loc["2011", old] == 2
    assert table.loc["2023", old] == 0
    assert table.loc["2023", new] == 2
    assert table.loc["2010"].sum() == 0


def test_suspect_unconfigured_labels(mini_frame, mini_config):
    frame = mini_frame.copy()
    frame.loc[0, STAGE] = "Unknown stage"
    table = inv.suspect_unconfigured_labels(frame, mini_config)
    found = set(zip(table["column"], table["value"]))
    assert (STAGE, "Unknown stage") in found
    assert (GLEASON_C, "Not documented; Not assessed or unknown if assessed") not in found


def test_age_check_counts_labels(mini_frame, mini_config):
    age = "Age recode with <1 year olds and 90+"
    frame = mini_frame.copy()
    frame[age] = ["00 years", "15-19 years", "65-69 years", "65-69 years", "10-14 years", "70-74 years"]
    inventory = dataclasses.replace(
        mini_config.inventory,
        age_column=age,
        age_labels_below_18=("00 years", "10-14 years"),
        age_labels_straddling_18=("15-19 years",),
    )
    check = inv.age_check(frame, dataclasses.replace(mini_config, inventory=inventory))
    assert check.below_18 == 2
    assert check.straddling_18 == 1


def test_age_check_is_none_without_age_column(mini_frame, mini_config):
    assert inv.age_check(mini_frame, mini_config) is None


def test_selection_criteria_flags_extra_criterion():
    note = (
        "Site recode ICD-O-3/WHO 2008 = Prostate\n"
        "Year of diagnosis = 2010 to 2023\n"
        "Age at diagnosis = 18 and over\n\n\n"
        "Surveillance, Epidemiology, and End Results (SEER) Program SEER*Stat Database\n"
    )
    criteria = inv.selection_criteria(note)
    assert len(criteria) == 3
    unexpected = inv.unexpected_selection_criteria(criteria, ("Site recode", "Year of diagnosis"))
    assert unexpected == ["Age at diagnosis = 18 and over"]


def test_absent_variable_check(mini_config):
    names = ["Patient ID", "Insurance Recode (2007+)"]
    result = inv.check_absent_variables(names, mini_config.inventory.absent_variable_keywords)
    assert result["insurance"] == ["Insurance Recode (2007+)"]
    assert result["registry"] == []
    assert result["month_of_diagnosis"] == []
