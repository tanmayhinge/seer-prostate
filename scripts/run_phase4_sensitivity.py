"""Phase 4 sensitivity analyses (PROTOCOL.md A8, amendment 1.8).

For each configured scenario the cohort is rebuilt with one change, and the ordered steps 0 to 2 are refitted for
both model types with the hyperparameters tuned in the primary analysis (reports/phase4_tables/model_tuning.csv).
Reported per scenario: delay by risk group, the social position increment with cluster bootstrap intervals, and the
standardised area and marital status contrasts. A post hoc check re-tunes penalised logistic regression on a wider
C grid in the primary cohort.

Aggregate tables go to reports/phase4_tables/; the delay summary holds exact counts and is git-ignored.
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort, scenario_options
from seer_study.config import load_config
from seer_study.descriptive import delay_summary
from seer_study.features import build_feature_blocks, design_matrix
from seer_study.increments import bootstrap_increments, step_metrics
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.models import MODEL_KINDS, cross_fit_predictions, fit_full_model, tune_hyperparameters
from seer_study.risk import RISK_GROUPS
from seer_study.standardise import area_income_ranks, standardised_percentages

STRATA = ("all", *RISK_GROUPS)
PRIMARY = "primary"
WIDE_C = "logistic_wide_c_grid"


def log(message: str, handle) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    print(line, flush=True)
    handle.write(line + "\n")
    handle.flush()


def primary_params(tuning: pd.DataFrame, stratum: str, kind: str) -> dict:
    row = tuning[(tuning["stratum"] == stratum) & (tuning["model"] == kind)].iloc[0]
    if kind == "logistic":
        return {"C": float(row["C"]), "max_iter": int(row["max_iter"])}
    return {
        "learning_rate": float(row["learning_rate"]),
        "n_estimators": int(row["n_estimators"]),
        "num_leaves": int(row["num_leaves"]),
        "min_child_samples": int(row["min_child_samples"]),
    }


def stratum_mask(cohort: pd.DataFrame, stratum: str) -> np.ndarray:
    return np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()


def delay_by_risk(label: str, cohort: pd.DataFrame) -> pd.DataFrame:
    overall = delay_summary(cohort, [], "delayed", "interval_days").assign(risk_group="all")
    by_risk = delay_summary(cohort, ["risk_group"], "delayed", "interval_days")
    table = pd.concat([overall, by_risk], ignore_index=True)
    table.insert(0, "scenario", label)
    return table[["scenario", "risk_group", "n", "n_delayed", "pct_delayed", "median_days", "p90_days"]]


def analyse_cohort(label, cohort, acfg, params_for, kinds, resamples, handle, standardise=True):
    """Steps 0 to 2 per stratum and model: step metrics, bootstrap increments and standardised contrasts."""
    c, features, modelling = acfg.columns, acfg.features, acfg.modelling
    seed, clip, level = acfg.seed, modelling.probability_clip, modelling.interval_level
    blocks = build_feature_blocks(cohort, acfg)
    clinical = blocks.columns_by_block["clinical"]
    y_all = cohort["delayed"].astype(bool).to_numpy().astype(int)
    clusters_all = (cohort[c.rurality] + " | " + cohort[c.income]).to_numpy()
    matrices_all = {step: design_matrix(blocks, step) for step in (0, 1, 2)}

    reference = {
        "marital": modelling.reference_marital,
        "rurality": modelling.reference_rurality,
        "income_rank": float(np.nanquantile(matrices_all[2]["income_rank"], modelling.reference_income_quantile)),
    }
    area_rank = area_income_ranks(matrices_all[2]["income_rank"], cohort[c.rurality], features.rurality_labels)
    remote, metro = features.rurality_labels[-1], modelling.reference_rurality
    single = next(name for name in features.marital_labels if name.startswith("Single"))
    profiles = {
        "area remote": {"rurality": remote, "income_rank": area_rank[remote]},
        "area metro": {"rurality": metro, "income_rank": area_rank[metro]},
        "marital single": {"marital": single},
    }

    metrics_rows, increment_rows, contrast_rows = [], [], []
    for stratum in STRATA:
        mask = stratum_mask(cohort, stratum)
        y = y_all[mask]
        if min(int(y.sum()), int(len(y) - y.sum())) < modelling.cv_folds:
            log(f"{label} {stratum}: skipped ({len(y)} men, too few in one outcome class)", handle)
            continue
        matrices = {step: matrix.loc[mask] for step, matrix in matrices_all.items()}
        for kind in kinds:
            params = params_for(stratum, kind)

            def interactions(columns):
                return [col for col in clinical if col in columns] if kind == "logistic" else []

            predictions = {
                step: cross_fit_predictions(matrix, y, kind, params, modelling.cv_folds, seed, interactions(matrix.columns))
                for step, matrix in matrices.items()
            }
            metrics = step_metrics(y, predictions, clip)
            increments = bootstrap_increments(y, predictions, clusters_all[mask], resamples, seed, clip, level)
            for table, rows in ((metrics, metrics_rows), (increments, increment_rows)):
                table.insert(0, "model", kind)
                table.insert(0, "stratum", stratum)
                table.insert(0, "scenario", label)
                rows.append(table)
            if standardise:
                model = fit_full_model(matrices[2], y, kind, params, seed, interactions(matrices[2].columns))
                pct = standardised_percentages(model, matrices[2], features, reference, profiles)
                for contrast, estimate in (
                    ("social", pct["as observed"] - pct["reference profile"]),
                    ("area", pct["area remote"] - pct["area metro"]),
                    ("marital", pct["marital single"] - pct["reference profile"]),
                ):
                    contrast_rows.append(
                        {"scenario": label, "stratum": stratum, "model": kind, "contrast": contrast, "estimate": estimate}
                    )
            social = increments.loc[increments["comparison"].str.startswith("social"), "estimate"].item()
            log(f"{label} {stratum} {kind}: {len(y):,} men, social increment {100 * social:.2f} points", handle)
    return metrics_rows, increment_rows, contrast_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--scenarios", nargs="+", default=None, help="development only: subset of scenario names")
    parser.add_argument("--skip-wide-c", action="store_true", help="development only")
    parser.add_argument("--sample", type=int, default=None, help="development only: random subsample per cohort")
    parser.add_argument("--bootstrap-resamples", type=int, default=None, help="development only: override")
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    modelling = acfg.modelling
    resamples = args.bootstrap_resamples or modelling.bootstrap_resamples
    suffix = f"_sample{args.sample}" if args.sample else ""
    tuning = pd.read_csv(args.tables_dir / "model_tuning.csv")
    scenarios = [s for s in acfg.sensitivity.scenarios if args.scenarios is None or s.name in args.scenarios]
    handle = open(args.tables_dir / f"sensitivity_log{suffix}.txt", "w")

    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)

    def prepare(cohort):
        if args.sample:
            return cohort.sample(n=min(args.sample, len(cohort)), random_state=acfg.seed).sort_index()
        return cohort

    def params_from_primary(stratum, kind):
        return primary_params(tuning, stratum, kind)

    primary = prepare(build_cohort(frame, acfg).frame)
    summaries = [delay_by_risk(PRIMARY, primary)]
    metrics_rows, increment_rows, contrast_rows = [], [], []

    def write():
        pd.concat(summaries).to_csv(args.tables_dir / f"sensitivity_delay_summary{suffix}.csv", index=False)
        if metrics_rows:
            pd.concat(metrics_rows).to_csv(args.tables_dir / f"sensitivity_step_metrics{suffix}.csv", index=False)
            pd.concat(increment_rows).to_csv(args.tables_dir / f"sensitivity_increments{suffix}.csv", index=False)
        if contrast_rows:
            pd.DataFrame(contrast_rows).to_csv(args.tables_dir / f"sensitivity_contrasts{suffix}.csv", index=False)

    for spec in scenarios:
        started = time.time()
        cohort = prepare(build_cohort(frame, acfg, scenario_options(spec)).frame)
        log(f"{spec.name}: {len(cohort):,} men, {cohort['delayed'].astype(bool).mean():.4f} delayed", handle)
        summaries.append(delay_by_risk(spec.name, cohort))
        m, i, k = analyse_cohort(spec.name, cohort, acfg, params_from_primary, MODEL_KINDS, resamples, handle)
        metrics_rows += m
        increment_rows += i
        contrast_rows += k
        write()
        log(f"{spec.name}: done in {time.time() - started:.0f}s", handle)

    if not args.skip_wide_c:
        started = time.time()
        grid = acfg.sensitivity.logistic_wide_c_grid
        blocks = build_feature_blocks(primary, acfg)
        clinical = blocks.columns_by_block["clinical"]
        y_all = primary["delayed"].astype(bool).to_numpy().astype(int)
        chosen, tuning_rows = {}, []
        for stratum in STRATA:
            mask = stratum_mask(primary, stratum)
            matrix = design_matrix(blocks, 3).loc[mask]
            params = tune_hyperparameters(
                matrix, y_all[mask], "logistic", {"C": grid}, {"max_iter": modelling.logistic_max_iter},
                modelling.tuning_folds, acfg.seed, modelling.tuning_rows,
                [col for col in clinical if col in matrix.columns], modelling.probability_clip,
            )
            chosen[stratum] = params
            tuning_rows.append(
                {"stratum": stratum, "C": params["C"], "grid": " ".join(f"{v:g}" for v in grid),
                 "at lowest C": params["C"] == min(grid), "at highest C": params["C"] == max(grid)}
            )
            log(f"{WIDE_C} {stratum}: chose C = {params['C']:g}", handle)
        pd.DataFrame(tuning_rows).to_csv(args.tables_dir / f"sensitivity_wide_c_tuning{suffix}.csv", index=False)
        m, i, _ = analyse_cohort(
            WIDE_C, primary, acfg, lambda stratum, kind: chosen[stratum], ("logistic",), resamples, handle, standardise=False
        )
        metrics_rows += m
        increment_rows += i
        write()
        log(f"{WIDE_C}: done in {time.time() - started:.0f}s", handle)

    log("finished", handle)
    handle.close()


if __name__ == "__main__":
    main()
