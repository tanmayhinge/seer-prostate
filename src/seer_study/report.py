"""Markdown formatting helpers with the study's writing rules enforced."""

from __future__ import annotations

import math
import re

import numpy as np
import pandas as pd

EM_DASH = "—"
BANNED_WORDS = ("promising", "striking", "significant", "significantly")


class StyleError(ValueError):
    """Raised when rendered text breaks the writing rules."""


def assert_style(text: str) -> None:
    """No em dashes; no 'promising', 'striking' or 'significant' (reports without statistical tests)."""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if EM_DASH in line:
            raise StyleError(f"em dash on line {line_number}")
    for word in BANNED_WORDS:
        match = re.search(rf"\b{word}\b", text, flags=re.IGNORECASE)
        if match:
            raise StyleError(f"banned word {word!r} at character {match.start()}")


def fmt_int(value: float) -> str:
    return f"{int(value):,}"


def fmt_float(value: float, digits: int = 1) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    return f"{value:,.{digits}f}"


def fmt_pct(numerator: float, denominator: float, digits: int = 1) -> str:
    if not denominator:
        return "n/a"
    return f"{100.0 * numerator / denominator:.{digits}f}%"


def _cell(value: object, digits: int) -> str:
    if isinstance(value, (bool, np.bool_)):
        return str(bool(value))
    if isinstance(value, (int, np.integer)):
        return fmt_int(value)
    if isinstance(value, (float, np.floating)):
        return fmt_float(float(value), digits)
    return str(value).replace("|", "\\|")


def md_table(frame: pd.DataFrame, index: bool = False, digits: int = 1) -> str:
    table = frame.reset_index() if index else frame
    header = "| " + " | ".join(str(c).replace("|", "\\|") for c in table.columns) + " |"
    rule = "|" + "|".join("---" for _ in table.columns) + "|"
    rows = [
        "| " + " | ".join(_cell(value, digits) for value in row) + " |"
        for row in table.itertuples(index=False, name=None)
    ]
    return "\n".join([header, rule, *rows])
