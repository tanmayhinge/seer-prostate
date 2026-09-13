"""Figures for the preprint, drawn only from aggregate tables (settings in config/figures.yaml).

Figures are built with matplotlib's object interface (no pyplot state), so building one never affects another.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from seer_study.config import load_typed_yaml
from seer_study.disclosure import publishable_summary
from seer_study.report import fmt_int


@dataclass(frozen=True)
class FigureSpec:
    dpi: int
    formats: tuple[str, ...]
    width_inches: float
    font_size: float
    calibration_bins: int
    model_colors: dict[str, str]
    model_labels: dict[str, str]
    stratum_labels: dict[str, str]


def load_figure_config(path: str | Path) -> FigureSpec:
    return load_typed_yaml(path, FigureSpec)


def _style(spec: FigureSpec):
    return matplotlib.rc_context(
        {"font.size": spec.font_size, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False}
    )


def _models(spec: FigureSpec, present) -> list[str]:
    return [model for model in spec.model_labels if model in set(present)]


def _offsets(keys: list[str], spread: float) -> dict[str, float]:
    if len(keys) == 1:
        return {keys[0]: 0.0}
    return dict(zip(keys, np.linspace(spread, -spread, len(keys))))  # first key highest, matching legend order


def _literal(text: str) -> str:
    """Escape dollar signs so matplotlib shows them instead of starting mathtext."""
    return str(text).replace("$", r"\$")


def calibration_bins(y: np.ndarray, p: np.ndarray, n_bins: int) -> pd.DataFrame:
    """Equal-count bins of predicted probability: mean prediction and observed proportion per bin."""
    y, p = np.asarray(y, dtype=float), np.asarray(p, dtype=float)
    if n_bins > len(p):
        raise ValueError(f"{n_bins} bins requested for {len(p)} predictions")
    order = np.argsort(p, kind="stable")
    rows = [
        {"bin": number, "n": len(members), "mean_predicted": float(p[members].mean()), "observed": float(y[members].mean())}
        for number, members in enumerate(np.array_split(order, n_bins), start=1)
    ]
    return pd.DataFrame(rows)


def plottable_rates(
    table: pd.DataFrame, group_columns: list[str], threshold: int, mask: str, rounding: int, unknown_label: str
) -> pd.DataFrame:
    """Rows of a delay summary whose percentage may be published, excluding groups labelled unknown."""
    published = publishable_summary(table, threshold, mask, rounding)
    keep = published["pct_delayed"].ne(mask).to_numpy() & published["n"].ne(mask).to_numpy()
    for column in group_columns:
        keep &= table[column].ne(unknown_label).to_numpy()
    return table.loc[keep].reset_index(drop=True)


def flow_figure(flow: pd.DataFrame, spec: FigureSpec) -> Figure:
    """Inclusion flow: records remaining after each step, with the number excluded at that step alongside."""
    with _style(spec):
        n = len(flow)
        fig = Figure(figsize=(spec.width_inches, 0.75 * n + 0.3))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(0, 1)
        ax.set_ylim(-n + 0.5, 0.5)
        ax.axis("off")
        main_x, side_x = 0.33, 0.76
        for i, row in enumerate(flow.itertuples(index=False)):
            y = -i
            label = "All records" if i == 0 else f"{row.step[0].upper()}{row.step[1:]}"
            ax.text(main_x, y, f"{label}\nn = {fmt_int(row.remaining)}", ha="center", va="center",
                    bbox={"boxstyle": "round,pad=0.4", "fc": "white", "ec": "0.3"})
            if i > 0:
                ax.annotate("", xy=(main_x, y + 0.3), xytext=(main_x, y + 0.7),
                            arrowprops={"arrowstyle": "->", "color": "0.3", "lw": 0.8})
                ax.plot([main_x, side_x - 0.12], [y + 0.5, y + 0.5], color="0.5", lw=0.8)
                ax.text(side_x, y + 0.5, f"Excluded: {fmt_int(row.excluded)}", ha="center", va="center",
                        bbox={"boxstyle": "round,pad=0.3", "fc": "0.95", "ec": "0.6"})
        return fig


def rates_figure(
    table: pd.DataFrame,
    row_column: str,
    series_column: str,
    row_order: list[str],
    series_order: list[str],
    spec: FigureSpec,
    xlabel: str,
    value_column: str = "pct_delayed",
) -> Figure:
    """Dot plot of a percentage by two groupings: rows on the y axis, one colour per series."""
    with _style(spec):
        fig = Figure(figsize=(spec.width_inches, 0.8 * len(row_order) + 1.0), layout="constrained")
        ax = fig.add_subplot()
        colors = matplotlib.colormaps["viridis"](np.linspace(0.0, 0.85, len(series_order)))
        offsets = _offsets(list(series_order), 0.3)
        for k, series in enumerate(series_order):
            part = table[table[series_column] == series].set_index(row_column)
            points = [(-i + offsets[series], part.loc[row, value_column]) for i, row in enumerate(row_order) if row in part.index]
            if points:
                ys, xs = zip(*points)
                ax.scatter(xs, ys, color=colors[k], label=_literal(series), s=22, zorder=3)
        ax.set_yticks([-i for i in range(len(row_order))], [_literal(spec.stratum_labels.get(row, row)) for row in row_order])
        for i in range(len(row_order) - 1):
            ax.axhline(-i - 0.5, color="0.9", lw=0.8)
        ax.set_xlabel(xlabel)
        ax.grid(axis="x", color="0.92", lw=0.6)
        ax.legend(title=series_column[0].upper() + series_column[1:], loc="upper left", bbox_to_anchor=(1.01, 1.0))
        return fig


def _interval_points(ax, rows: pd.DataFrame, order: list[str], offset: float, color: str, label: str, scale: float) -> None:
    ys, est, lo, hi = [], [], [], []
    for i, key in enumerate(order):
        if key in rows.index:
            ys.append(-i + offset)
            est.append(scale * rows.loc[key, "estimate"])
            lo.append(scale * rows.loc[key, "lower"])
            hi.append(scale * rows.loc[key, "upper"])
    est, lo, hi = np.array(est), np.array(lo), np.array(hi)
    xerr = [np.clip(est - lo, 0, None), np.clip(hi - est, 0, None)]
    ax.errorbar(est, ys, xerr=xerr, fmt="o", color=color, label=label, ms=3.5, capsize=2, lw=1)


def increments_figure(increments: pd.DataFrame, comparisons: dict[str, str], strata: dict[str, str], spec: FigureSpec) -> Figure:
    """Skill added by each block (percentage points, with intervals), one panel per comparison."""
    with _style(spec):
        fig = Figure(figsize=(spec.width_inches, 0.45 * len(strata) + 1.6), layout="constrained")
        axes = fig.subplots(1, len(comparisons), sharey=True, squeeze=False)[0]
        models = _models(spec, increments["model"])
        offsets = _offsets(models, 0.15)
        order = list(strata)
        for ax, (comparison, title) in zip(axes, comparisons.items()):
            part = increments[increments["comparison"] == comparison]
            for model in models:
                rows = part[part["model"] == model].set_index("stratum")
                _interval_points(ax, rows, order, offsets[model], spec.model_colors[model], spec.model_labels[model], 100.0)
            ax.axvline(0, color="0.6", lw=0.8, ls="--")
            ax.set_title(title)
            ax.grid(axis="x", color="0.92", lw=0.6)
        axes[0].set_yticks([-i for i in range(len(order))], [_literal(v) for v in strata.values()])
        fig.supxlabel("Log-loss skill added (percentage points)")
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="outside upper center", ncols=len(models))
        return fig


def area_and_concentration_figure(
    profiles: pd.DataFrame,
    area_profiles: dict[str, str],
    curves: pd.DataFrame,
    strata: dict[str, str],
    spec: FigureSpec,
    titles: tuple[str, str] = ("a", "b"),
    value_label: str = "Standardised %",
    curve_labels: tuple[str, str] = ("Cumulative share of men", "Cumulative share of the outcome"),
    stratum: str = "all",
) -> Figure:
    """(a) Standardised percentages for joint area profiles by model; (b) concentration curves by stratum."""
    with _style(spec):
        fig = Figure(figsize=(spec.width_inches, 4.2), layout="constrained")
        ax_a, ax_b = fig.subplots(1, 2, width_ratios=(1.1, 1.0))
        models = _models(spec, profiles["model"])
        offsets = _offsets(models, 0.12)
        order = list(area_profiles)
        pooled = profiles[profiles["stratum"] == stratum]
        for model in models:
            rows = pooled[pooled["model"] == model].set_index("profile")
            points = [(-i + offsets[model], rows.loc[p, "standardised %"]) for i, p in enumerate(order) if p in rows.index]
            ys, xs = zip(*points)
            ax_a.scatter(xs, ys, color=spec.model_colors[model], label=spec.model_labels[model], s=20, zorder=3)
        ax_a.set_yticks([-i for i in range(len(order))], [_literal(v) for v in area_profiles.values()])
        ax_a.set_xlabel(value_label)
        ax_a.set_title(titles[0], loc="left")
        ax_a.grid(axis="x", color="0.92", lw=0.6)
        fig.legend(*ax_a.get_legend_handles_labels(), loc="outside upper center", ncols=len(models))

        colors = matplotlib.colormaps["Dark2"](np.arange(len(strata)))
        for k, (key, label) in enumerate(strata.items()):
            curve = curves[curves["stratum"] == key].sort_values("population_share")
            if len(curve):
                ax_b.plot(curve["population_share"], curve["outcome_share"], color=colors[k], lw=1.1, label=label)
        ax_b.plot([0, 1], [0, 1], color="0.5", lw=0.8, ls="--", label="Line of equality")
        ax_b.set_xlim(0, 1)
        ax_b.set_ylim(0, 1)
        ax_b.set_xlabel(curve_labels[0])
        ax_b.set_ylabel(curve_labels[1])
        ax_b.set_title(titles[1], loc="left")
        ax_b.legend(loc="upper left")
        return fig


def calibration_figure(bins: pd.DataFrame, strata: dict[str, str], spec: FigureSpec) -> Figure:
    """Observed proportion against mean predicted probability per bin, one panel per stratum."""
    with _style(spec):
        n = len(strata)
        columns = min(3, n)
        rows = int(np.ceil(n / columns))
        fig = Figure(figsize=(spec.width_inches, 2.3 * rows + 0.7), layout="constrained")
        axes = fig.subplots(rows, columns, squeeze=False).ravel()
        models = _models(spec, bins["model"])
        for ax, (key, label) in zip(axes, strata.items()):
            part = bins[bins["stratum"] == key]
            for model in models:
                sub = part[part["model"] == model].sort_values("bin")
                ax.plot(sub["mean_predicted"], sub["observed"], marker="o", ms=3, lw=1,
                        color=spec.model_colors[model], label=spec.model_labels[model])
            low = float(min(part["mean_predicted"].min(), part["observed"].min()))
            high = float(max(part["mean_predicted"].max(), part["observed"].max()))
            pad = 0.05 * (high - low or 1.0)
            ax.plot([low - pad, high + pad], [low - pad, high + pad], color="0.6", lw=0.8, ls="--")
            ax.set_xlim(low - pad, high + pad)
            ax.set_ylim(low - pad, high + pad)
            ax.set_title(label)
            ax.grid(color="0.92", lw=0.6)
        for ax in axes[n:]:
            ax.set_visible(False)
        fig.supxlabel("Mean predicted probability")
        fig.supylabel("Observed proportion")
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="outside upper center", ncols=len(models))
        return fig


def sensitivity_figure(increments: pd.DataFrame, comparison: str, scenarios: dict[str, str], spec: FigureSpec) -> Figure:
    """One comparison's increment (with intervals) under each scenario, for one stratum."""
    with _style(spec):
        fig = Figure(figsize=(spec.width_inches, 0.38 * len(scenarios) + 1.3), layout="constrained")
        ax = fig.add_subplot()
        part = increments[increments["comparison"] == comparison]
        models = _models(spec, part["model"])
        offsets = _offsets(models, 0.15)
        order = list(scenarios)
        for model in models:
            rows = part[part["model"] == model].set_index("scenario")
            _interval_points(ax, rows, order, offsets[model], spec.model_colors[model], spec.model_labels[model], 100.0)
        ax.axvline(0, color="0.6", lw=0.8, ls="--")
        ax.set_yticks([-i for i in range(len(order))], [_literal(v) for v in scenarios.values()])
        ax.set_xlabel("Log-loss skill added (percentage points)")
        ax.grid(axis="x", color="0.92", lw=0.6)
        fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncols=len(models))
        return fig


def save_figure(fig: Figure, stem: str, out_dir: str | Path, spec: FigureSpec) -> list[Path]:
    """Write the figure in every configured format; PDF creation dates are omitted so reruns give identical files."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in spec.formats:
        path = out_dir / f"{stem}.{fmt}"
        metadata = {"CreationDate": None} if fmt == "pdf" else None
        fig.savefig(path, dpi=spec.dpi, format=fmt, metadata=metadata)
        paths.append(path)
    return paths
