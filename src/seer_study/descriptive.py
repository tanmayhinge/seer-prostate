"""Descriptive timeliness summaries (PROTOCOL.md A1)."""

from __future__ import annotations

import pandas as pd


def delay_summary(frame: pd.DataFrame, by: list[str], delayed_column: str, days_column: str) -> pd.DataFrame:
    """Per group: men, men delayed, % delayed (of men with a known delay status), median and 90th percentile days.

    Top-coded intervals enter the day summaries at their top-coded value, so upper percentiles are lower bounds.
    """
    keys = list(by) if by else ["_all"]
    data = frame.assign(_all="all") if not by else frame
    delayed = data[delayed_column]
    data = data.assign(_delayed=delayed.fillna(False).astype(bool), _known=delayed.notna())
    grouped = data.groupby(keys, sort=True, observed=True)
    out = grouped.agg(
        n=("_known", "size"),
        n_known=("_known", "sum"),
        n_delayed=("_delayed", "sum"),
        median_days=(days_column, "median"),
        p90_days=(days_column, lambda s: s.quantile(0.9)),
    )
    out["pct_delayed"] = 100.0 * out["n_delayed"] / out["n_known"]
    out = out.reset_index()
    if not by:
        out = out.drop(columns="_all")
    return out[[*by, "n", "n_delayed", "pct_delayed", "median_days", "p90_days"]]
