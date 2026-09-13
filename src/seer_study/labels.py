"""Strict label mapping shared by the analysis modules: a label the configuration does not know is an error."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


class UnmappedLabelError(ValueError):
    """Raised when a SEER label appears that the analysis configuration does not map."""


def require_known(series: pd.Series, known: Iterable[str], what: str) -> None:
    unmapped = sorted(set(series.unique()) - set(known))
    if unmapped:
        raise UnmappedLabelError(f"{what}: unmapped label(s) {unmapped[:10]}")
