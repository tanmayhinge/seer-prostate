import numpy as np
import pandas as pd
import pytest

from seer_study.figures import (
    area_and_concentration_figure,
    calibration_bins,
    calibration_figure,
    flow_figure,
    increments_figure,
    load_figure_config,
    plottable_rates,
    rates_figure,
    save_figure,
    sensitivity_figure,
)
from synthetic import PROJECT_ROOT

STRATA = {"all": "All men", "low": "Low risk"}
MODELS = ("logistic", "lightgbm")


@pytest.fixture
def spec():
    return load_figure_config(PROJECT_ROOT / "config" / "figures.yaml")


def visible_axes(fig):
    return [ax for ax in fig.axes if ax.get_visible()]


def test_figure_config_loads(spec):
    assert set(spec.model_colors) == set(MODELS) == set(spec.model_labels)
    assert spec.calibration_bins > 1 and spec.formats


def test_calibration_bins_known_answer():
    p = np.array([0.1] * 5 + [0.9] * 5)
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 0])
    out = calibration_bins(y, p, n_bins=2)
    assert out["bin"].tolist() == [1, 2]
    assert out["n"].tolist() == [5, 5]
    assert out["mean_predicted"].tolist() == pytest.approx([0.1, 0.9])
    assert out["observed"].tolist() == pytest.approx([0.2, 0.8])


def test_calibration_bins_rejects_more_bins_than_rows():
    with pytest.raises(ValueError, match="bins"):
        calibration_bins(np.array([0, 1]), np.array([0.2, 0.8]), n_bins=3)


def test_plottable_rates_drops_masked_and_unknown_rows():
    table = pd.DataFrame(
        {
            "group": ["A", "B", "C", "Unknown"],
            "n": [100, 3, 100, 100],
            "n_delayed": [50, 1, 2, 50],
            "pct_delayed": [50.0, 33.3, 2.0, 50.0],
            "median_days": [80.0] * 4,
            "p90_days": [150.0] * 4,
        }
    )
    out = plottable_rates(table, ["group"], threshold=5, mask="<5", rounding=10, unknown_label="Unknown")
    assert out["group"].tolist() == ["A"]
    assert out["pct_delayed"].tolist() == [50.0]


def test_flow_figure(spec):
    flow = pd.DataFrame({"step": ["all records", "first primary", "age 40 or over"], "remaining": [100, 80, 70], "excluded": [0, 20, 10]})
    before = flow.copy()
    fig = flow_figure(flow, spec)
    assert len(visible_axes(fig)) == 1
    assert flow.equals(before)


def test_rates_figure(spec):
    table = pd.DataFrame({"risk group": ["low", "low", "high"], "rurality": ["Metro", "Rural", "Metro"], "pct_delayed": [50.0, 40.0, 30.0]})
    fig = rates_figure(table, "risk group", "rurality", ["low", "high"], ["Metro", "Rural"], spec, "% waiting more than 90 days")
    assert len(visible_axes(fig)) == 1


def _increments(extra_columns=None):
    rows = []
    for stratum in STRATA:
        for model in MODELS:
            for comparison in ("clinical", "social"):
                rows.append({"stratum": stratum, "model": model, "comparison": comparison, "estimate": 0.01, "lower": 0.0, "upper": 0.02, **(extra_columns or {})})
    return pd.DataFrame(rows)


def test_increments_figure_has_one_panel_per_comparison(spec):
    fig = increments_figure(_increments(), {"clinical": "Clinical need", "social": "Social position"}, STRATA, spec)
    assert len(visible_axes(fig)) == 2


def test_area_and_concentration_figure(spec):
    profiles = pd.DataFrame(
        [{"stratum": "all", "model": m, "profile": p, "standardised %": v} for m in MODELS for p, v in (("area a", 40.0), ("area b", 30.0))]
    )
    curves = pd.DataFrame({"stratum": ["all"] * 3 + ["low"] * 3, "population_share": [0, 0.5, 1] * 2, "outcome_share": [0, 0.4, 1] * 2})
    fig = area_and_concentration_figure(profiles, {"area a": "A", "area b": "B"}, curves, STRATA, spec)
    assert len(visible_axes(fig)) == 2


def test_dollar_signs_in_labels_are_literal_not_mathtext(spec):
    profile = "area: Metro ($90,000 - $94,999)"
    profiles = pd.DataFrame([{"stratum": "all", "model": m, "profile": profile, "standardised %": 40.0} for m in MODELS])
    curves = pd.DataFrame({"stratum": ["all"] * 2, "population_share": [0, 1], "outcome_share": [0, 1]})
    fig = area_and_concentration_figure(profiles, {profile: "Metro ($90,000 - $94,999)"}, curves, STRATA, spec)
    labels = [label.get_text() for label in visible_axes(fig)[0].get_yticklabels()]
    assert labels == [r"Metro (\$90,000 - \$94,999)"]


def test_concentration_panel_can_show_difference_from_equality(spec):
    profiles = pd.DataFrame([{"stratum": "all", "model": m, "profile": "area a", "standardised %": 40.0} for m in MODELS])
    curves = pd.DataFrame({"stratum": ["all"] * 3, "population_share": [0.0, 0.5, 1.0], "outcome_share": [0.0, 0.4, 1.0]})
    fig = area_and_concentration_figure(profiles, {"area a": "A"}, curves, {"all": "All men"}, spec, curve_difference=True)
    ydata = visible_axes(fig)[1].get_lines()[0].get_ydata()
    assert list(np.round(ydata, 6)) == [0.0, -0.1, 0.0]


def test_first_model_in_legend_is_plotted_highest(spec):
    fig = increments_figure(_increments(), {"social": "Social position"}, {"all": "All men"}, spec)
    ax = visible_axes(fig)[0]
    heights = {container.get_label(): container.lines[0].get_ydata()[0] for container in ax.containers}
    assert heights[spec.model_labels["logistic"]] > heights[spec.model_labels["lightgbm"]]


def test_calibration_figure_has_one_panel_per_stratum(spec):
    bins = pd.DataFrame(
        [{"stratum": s, "model": m, "bin": b, "mean_predicted": b / 10, "observed": b / 10} for s in STRATA for m in MODELS for b in (1, 2, 3)]
    )
    fig = calibration_figure(bins, STRATA, spec)
    assert len(visible_axes(fig)) == len(STRATA)


def test_sensitivity_figure(spec):
    increments = pd.concat([_increments({"scenario": "primary"}), _increments({"scenario": "threshold_60"})])
    fig = sensitivity_figure(increments[increments["stratum"] == "all"], "social", {"primary": "Primary", "threshold_60": "60 days"}, spec)
    assert len(visible_axes(fig)) == 1


def test_save_figure_writes_every_format(spec, tmp_path):
    flow = pd.DataFrame({"step": ["all records", "first primary"], "remaining": [100, 80], "excluded": [0, 20]})
    paths = save_figure(flow_figure(flow, spec), "figure1", tmp_path, spec)
    assert sorted(p.suffix for p in paths) == sorted(f".{fmt}" for fmt in spec.formats)
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
