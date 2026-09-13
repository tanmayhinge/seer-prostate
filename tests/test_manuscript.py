import pytest

from seer_study.manuscript import extract_table, numbers_in, protocol_version, render_includes, unsupported_numbers


def test_protocol_version_reads_the_version_line():
    assert protocol_version("# Protocol\n\nVersion 1.9, dated 2026-09-13 (see the amendment log).") == "1.9"


def test_protocol_version_missing_returns_none():
    assert protocol_version("# Protocol\n\nNo version here.") is None

REPORT = """# Report

Intro 1.5

## Table 1. Characteristics

Cells are n (%).

| a | b |
|---|---|
| 1 | 2 |

After the table.

## Table 2. Other

| c |
|---|
| 3 |
"""


def test_extract_table_returns_first_table_after_heading():
    assert extract_table(REPORT, "## Table 1.") == "| a | b |\n|---|---|\n| 1 | 2 |"
    assert extract_table(REPORT, "## Table 2.") == "| c |\n|---|\n| 3 |"


def test_extract_table_missing_heading_raises():
    with pytest.raises(ValueError, match="Table 9"):
        extract_table(REPORT, "## Table 9.")


def test_extract_table_heading_without_table_raises():
    with pytest.raises(ValueError, match="no table"):
        extract_table("## Empty\n\ntext only\n\n## Next\n\n| x |\n|---|\n", "## Empty")


def test_render_includes_replaces_table_directives(tmp_path):
    (tmp_path / "rep.md").write_text(REPORT)
    text = "Before\n\n<!-- table: rep.md | ## Table 2. -->\n\nAfter\n"
    assert render_includes(text, tmp_path) == "Before\n\n| c |\n|---|\n| 3 |\n\nAfter\n"


def test_numbers_in_finds_decimals_thousands_and_negatives():
    text = "39.7% of 330,827 men; 0.62 (0.39 to 0.87); -9.2 points; 2010 to 2022; step 2"
    assert numbers_in(text) == {"39.7", "330,827", "0.62", "0.39", "0.87", "9.2", "2010", "2022", "2"}


def test_numbers_in_ignores_numbers_inside_words_and_references():
    assert numbers_in("TRIPOD+AI, A500, PMID 35194109, doi 10.1038/s41598-022-06958-2") == set()


def test_unsupported_numbers_lists_numbers_absent_from_sources():
    assert unsupported_numbers("rose to 39.7 then 41.2 in 7 of 2022", ["was 39.7 in 2022"]) == ["41.2"]


def test_unsupported_numbers_compares_values_not_spelling():
    assert unsupported_numbers("median 116 days (330827 men)", ["116.0 (330,827)"]) == []


def test_unsupported_numbers_checks_small_integers_when_asked():
    assert unsupported_numbers("in 7 strata", ["none"], min_integer=0) == ["7"]
