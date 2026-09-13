import pandas as pd
import pytest

from seer_study.report import StyleError, assert_style, fmt_float, fmt_pct, md_table


def test_md_table_escapes_pipes_and_formats_numbers():
    frame = pd.DataFrame({"value": ["a|b"], "n": [1200], "pct": [12.345]})
    lines = md_table(frame).splitlines()
    assert lines[0] == "| value | n | pct |"
    assert lines[1] == "|---|---|---|"
    assert lines[2] == "| a\\|b | 1,200 | 12.3 |"


def test_md_table_renders_nan_as_not_available():
    frame = pd.DataFrame({"pct": [float("nan")]})
    assert md_table(frame).splitlines()[2] == "| n/a |"


def test_fmt_pct():
    assert fmt_pct(1, 3) == "33.3%"
    assert fmt_pct(0, 0) == "n/a"


def test_fmt_float_nan():
    assert fmt_float(float("nan")) == "n/a"


def test_style_rejects_em_dash():
    with pytest.raises(StyleError, match="line 2"):
        assert_style("fine\nnot — fine")


@pytest.mark.parametrize("word", ["promising", "Striking", "significant", "significantly"])
def test_style_rejects_banned_words(word):
    with pytest.raises(StyleError):
        assert_style(f"This is {word}.")


def test_style_accepts_plain_text():
    assert_style("Completeness rose from 80.0% to 95.0% (higher is better).")
