"""Phase 4 model results report (PROTOCOL.md A2 to A4), rendered from the tables written by run_phase4_models.py."""

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.report import assert_style, md_table
from seer_study.risk import RISK_GROUPS

STRATUM_ORDER = ["all", *RISK_GROUPS]
STRATUM_LABEL = {"all": "all men (pooled)", **{group: f"{group} risk" for group in RISK_GROUPS}}
MODEL_LABEL = {"logistic": "penalised logistic regression", "lightgbm": "LightGBM"}


def _git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "unknown"


def _pct(value: float, digits: int = 2) -> str:
    return f"{100.0 * value:.{digits}f}"


def _interval(row) -> str:
    return f"{_pct(row['estimate'])} ({_pct(row['lower'])} to {_pct(row['upper'])})"


def _order(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["_s"] = frame["stratum"].map({s: i for i, s in enumerate(STRATUM_ORDER)})
    frame["_m"] = frame["model"].map({"logistic": 0, "lightgbm": 1})
    return frame.sort_values(["_s", "_m"] + (["step"] if "step" in frame else [])).drop(columns=["_s", "_m"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase4_models.md"))
    args = parser.parse_args()
    acfg = load_analysis_config(args.analysis_config)
    modelling = acfg.modelling

    metrics = _order(pd.read_csv(args.tables_dir / "model_step_metrics.csv"))
    increments = _order(pd.read_csv(args.tables_dir / "model_increments.csv"))
    lovo = _order(pd.read_csv(args.tables_dir / "model_leave_one_variable_out.csv"))
    tuning = _order(pd.read_csv(args.tables_dir / "model_tuning.csv"))

    social = increments[increments["comparison"] == "social position (step 1 to 2)"].set_index(["stratum", "model"])
    clinical = increments[increments["comparison"] == "clinical need (step 0 to 1)"].set_index(["stratum", "model"])
    pathway = increments[increments["comparison"] == "pathway (step 2 to 3)"].set_index(["stratum", "model"])

    headline_rows = []
    for stratum in STRATUM_ORDER:
        for model in ("logistic", "lightgbm"):
            if (stratum, model) not in social.index:
                continue
            n = int(metrics[(metrics["stratum"] == stratum) & (metrics["model"] == model)]["n"].iloc[0])
            s, c, p = social.loc[(stratum, model)], clinical.loc[(stratum, model)], pathway.loc[(stratum, model)]
            step2_skill = float(
                metrics[(metrics["stratum"] == stratum) & (metrics["model"] == model) & (metrics["step"] == 2)]["log_loss_skill"].iloc[0]
            )
            headline_rows.append(
                {
                    "stratum": STRATUM_LABEL[stratum],
                    "model": MODEL_LABEL[model],
                    "men": n,
                    "skill at step 2": _pct(step2_skill),
                    "clinical need added": _interval(c),
                    "social position added": _interval(s),
                    "social position as % of step 2 skill": f"{100.0 * s['estimate'] / step2_skill:.0f}" if step2_skill > 0 else "n/a",
                    "treatment type added": _interval(p),
                }
            )
    headline = pd.DataFrame(headline_rows)

    step2 = metrics[metrics["step"] == 2].set_index(["stratum", "model"])["log_loss_skill"]
    comparison_rows = []
    boosting_better = []
    for stratum in STRATUM_ORDER:
        if (stratum, "logistic") in step2.index and (stratum, "lightgbm") in step2.index:
            lr, gb = step2.loc[(stratum, "logistic")], step2.loc[(stratum, "lightgbm")]
            boosting_better.append(gb > lr)
            comparison_rows.append(
                {"stratum": STRATUM_LABEL[stratum], "logistic regression skill at step 2": _pct(lr),
                 "LightGBM skill at step 2": _pct(gb), "difference (LightGBM minus logistic)": _pct(gb - lr)}
            )
    comparison = pd.DataFrame(comparison_rows)
    if all(boosting_better):
        verdict = "LightGBM had higher out-of-fold skill than penalised logistic regression at step 2 in every stratum."
    elif not any(boosting_better):
        verdict = "Gradient boosting (LightGBM) did not beat penalised logistic regression: its out-of-fold skill at step 2 was lower in every stratum."
    else:
        wins = sum(boosting_better)
        verdict = f"LightGBM had higher out-of-fold skill than penalised logistic regression at step 2 in {wins} of {len(boosting_better)} strata."

    metric_table = metrics.assign(
        stratum=metrics["stratum"].map(STRATUM_LABEL),
        model=metrics["model"].map(MODEL_LABEL),
        **{
            "log-loss skill %": metrics["log_loss_skill"].map(_pct),
            "Brier skill %": metrics["brier_skill"].map(_pct),
            "AUC": metrics["auc"].map(lambda v: f"{v:.3f}"),
            "calibration intercept": metrics["calibration_intercept"].map(lambda v: f"{v:.3f}"),
            "calibration slope": metrics["calibration_slope"].map(lambda v: f"{v:.3f}"),
        },
    )[["stratum", "model", "step", "log-loss skill %", "Brier skill %", "AUC", "calibration intercept", "calibration slope"]]

    lovo_table = lovo.assign(
        stratum=lovo["stratum"].map(STRATUM_LABEL),
        model=lovo["model"].map(MODEL_LABEL),
        **{"skill lost when removed (points)": lovo["skill lost"].map(_pct)},
    )[["stratum", "model", "variable removed", "skill lost when removed (points)"]]

    at_step2 = metrics[metrics["step"] == 2]
    predictability = (
        f"Across strata and models, AUC at step 2 ranged from {at_step2['auc'].min():.3f} to {at_step2['auc'].max():.3f} "
        f"(0.5 is chance, 1 is perfect) and log-loss skill from {_pct(at_step2['log_loss_skill'].min())}% to "
        f"{_pct(at_step2['log_loss_skill'].max())}% (0 means no better than year of diagnosis alone). Most of the variation "
        "in which men wait more than 90 days is not explained by the recorded clinical and social variables. The value "
        "added by social position should be read against this low ceiling."
    )
    slopes = at_step2.groupby("model")["calibration_slope"].agg(["min", "max"])
    calibration = " ".join(
        f"{MODEL_LABEL[model]}: calibration slopes at step 2 from {row['min']:.2f} to {row['max']:.2f}."
        for model, row in slopes.iterrows()
    ) + " A slope below 1 means predicted risks are more extreme than observed risks."

    def _format_parameter(column, value):
        if pd.isna(value):
            return "n/a"
        if column in ("C", "learning_rate"):
            return f"{value:g}"
        if column == "seconds":
            return f"{value:.1f}"
        return str(int(value))

    tuning_display = tuning.copy()
    for column in [col for col in tuning_display.columns if col not in ("stratum", "model")]:
        tuning_display[column] = [_format_parameter(column, v) for v in tuning_display[column]]
    tuning_display["stratum"] = tuning_display["stratum"].map(STRATUM_LABEL)
    tuning_display["model"] = tuning_display["model"].map(MODEL_LABEL)

    c_grid = modelling.logistic_c_grid
    edge = tuning[(tuning["model"] == "logistic") & (tuning["C"].isin([min(c_grid), max(c_grid)]))]
    tuning_note = (
        f"Penalised logistic regression chose C = {edge['C'].iloc[0]:g}, an edge of the pre-specified grid "
        f"{list(c_grid)}, in {len(edge)} of {int((tuning['model'] == 'logistic').sum())} strata; the best penalty may lie "
        "outside the grid. This is reported as a limitation rather than changed after the fact."
        if len(edge)
        else "No logistic regression tuning result fell on an edge of its grid."
    )

    lines = [
        "# Phase 4, part 2. How much social position adds to predicting delay",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `scripts/run_phase4_models_report.py` at git revision "
        f"`{_git_revision()}`. Definitions: `PROTOCOL.md` sections 5 to 7 (A2 to A4).",
        "## What is measured",
        "- Outcome: first recorded treatment more than 90 days after diagnosis.",
        "- Each model is built in ordered steps: step 0 year of diagnosis only; step 1 adds clinical need; step 2 adds "
        "social position (marital status, rurality, county income); step 3 adds treatment type.",
        "- **Skill** is the percentage reduction in out-of-fold log-loss compared with the step 0 model (0 means no better "
        "than year alone; higher is better). The value added by a block is the skill it adds, in percentage points.",
        f"- Intervals are {modelling.interval_level:.0%} cluster-bootstrap intervals ({modelling.bootstrap_resamples} "
        "resamples over rurality by county income cells).",
        "- These are associations measured as predictive gains. They are not causal effects.",
        "## How well delay can be predicted at all",
        predictability,
        "## Headline: value added at each step",
        "Skill and the value added by each block are in percentage points of log-loss reduction, with 95% intervals. "
        "\"Social position as % of step 2 skill\" is the share of the step 2 model's total skill contributed by the "
        "social block.",
        md_table(headline),
        "## Did gradient boosting beat penalised regression?",
        verdict,
        md_table(comparison),
        "## Performance at every step",
        "AUC: 0.5 is chance, higher is better. Calibration intercept: 0 is ideal. Calibration slope: 1 is ideal; below 1 "
        "means predictions are too extreme.",
        calibration,
        md_table(metric_table),
        "## Which social variable carries the gain",
        "Skill lost when one social variable is removed from the step 2 model and the model is refitted. Rurality and "
        "county income are strongly correlated in this cohort, so removing one lets the other partly stand in for it; "
        "a small loss does not mean a variable is unrelated to delay.",
        md_table(lovo_table),
        "## Tuning",
        tuning_note,
        md_table(tuning_display),
    ]
    text = "\n\n".join(lines) + "\n"
    assert_style(text)
    args.output.write_text(text)
    print(args.output)


if __name__ == "__main__":
    main()
