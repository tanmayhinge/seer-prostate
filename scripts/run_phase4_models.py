"""Phase 4 models (PROTOCOL.md A2 to A4): ordered-step cross-fitted models, cluster-bootstrap increments and
leave-one-variable-out refits, within each risk group and pooled.

Outputs aggregate tables to reports/phase4_tables/ and out-of-fold predictions to data/derived/phase4/
(excluded from git, because predictions are row level).
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import load_config
from seer_study.features import STEPS, build_feature_blocks, design_matrix
from seer_study.increments import bootstrap_increments, step_metrics
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.metrics import log_loss, skill
from seer_study.models import MODEL_KINDS, cross_fit_predictions, tune_hyperparameters
from seer_study.risk import RISK_GROUPS

SOCIAL_VARIABLE_PREFIXES = {"marital status": ("marital_",), "rurality": ("rurality_",), "county income": ("income_",)}


def log(message: str, handle) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    print(line, flush=True)
    handle.write(line + "\n")
    handle.flush()


def social_variable_groups(social_columns: list[str]) -> dict[str, list[str]]:
    groups = {
        name: [c for c in social_columns if c.startswith(prefixes)] for name, prefixes in SOCIAL_VARIABLE_PREFIXES.items()
    }
    assigned = [c for columns in groups.values() for c in columns]
    if sorted(assigned) != sorted(social_columns):
        raise ValueError("every social column must belong to exactly one social variable")
    return groups


def model_settings(kind: str, modelling) -> tuple[dict, dict]:
    if kind == "logistic":
        return {"C": modelling.logistic_c_grid}, {"max_iter": modelling.logistic_max_iter}
    return dict(modelling.lightgbm_grid), {"learning_rate": modelling.lightgbm_learning_rate}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--strata", nargs="+", default=["all", *RISK_GROUPS])
    parser.add_argument("--models", nargs="+", default=list(MODEL_KINDS))
    parser.add_argument("--sample", type=int, default=None, help="development only: run on a random subsample")
    parser.add_argument("--bootstrap-resamples", type=int, default=None, help="development only: override")
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--predictions-dir", type=Path, default=Path("data/derived/phase4"))
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    modelling = acfg.modelling
    resamples = args.bootstrap_resamples or modelling.bootstrap_resamples
    suffix = f"_sample{args.sample}" if args.sample else ""
    args.tables_dir.mkdir(parents=True, exist_ok=True)
    args.predictions_dir.mkdir(parents=True, exist_ok=True)
    handle = open(args.tables_dir / f"models_log{suffix}.txt", "w")

    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)
    cohort = build_cohort(frame, acfg).frame
    if args.sample:
        cohort = cohort.sample(n=min(args.sample, len(cohort)), random_state=acfg.seed).sort_index()
    blocks = build_feature_blocks(cohort, acfg)
    y_all = cohort["delayed"].astype(bool).to_numpy().astype(int)
    c = acfg.columns
    clusters_all = (cohort[c.rurality] + " | " + cohort[c.income]).to_numpy()
    clinical_columns = blocks.columns_by_block["clinical"]
    social_groups = social_variable_groups(blocks.columns_by_block["social"])
    log(f"cohort {len(cohort):,} men, {y_all.mean():.4f} delayed; {len(np.unique(clusters_all))} bootstrap clusters", handle)

    metrics_rows, increment_rows, lovo_rows, tuning_rows = [], [], [], []
    for stratum in args.strata:
        mask = np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()
        y = y_all[mask]
        clusters = clusters_all[mask]
        matrices = {step: design_matrix(blocks, step).loc[mask] for step in range(len(STEPS))}
        log(f"stratum {stratum}: {mask.sum():,} men, {y.mean():.4f} delayed", handle)
        for kind in args.models:
            def interactions(columns):
                return [col for col in clinical_columns if col in columns] if kind == "logistic" else []

            grid, fixed = model_settings(kind, modelling)
            started = time.time()
            params = tune_hyperparameters(
                matrices[3], y, kind, grid, fixed, modelling.tuning_folds, acfg.seed, modelling.tuning_rows,
                interactions(matrices[3].columns), modelling.probability_clip,
            )
            tuning_rows.append({"stratum": stratum, "model": kind, **params, "seconds": round(time.time() - started, 1)})
            log(f"  {kind}: tuned {params}", handle)

            predictions = {}
            for step, matrix in matrices.items():
                predictions[step] = cross_fit_predictions(
                    matrix, y, kind, params, modelling.cv_folds, acfg.seed, interactions(matrix.columns)
                )
                log(f"  {kind}: step {step} cross-fitted ({matrix.shape[1]} features)", handle)
            np.savez_compressed(
                args.predictions_dir / f"{stratum}_{kind}{suffix}.npz",
                index=cohort.index.to_numpy()[mask],
                y=y,
                **{f"step{step}": p for step, p in predictions.items()},
            )

            metrics = step_metrics(y, predictions, modelling.probability_clip)
            metrics.insert(0, "model", kind)
            metrics.insert(0, "stratum", stratum)
            metrics.insert(2, "n", len(y))
            metrics_rows.append(metrics)

            increments = bootstrap_increments(
                y, predictions, clusters, resamples, acfg.seed, modelling.probability_clip, modelling.interval_level
            )
            increments.insert(0, "model", kind)
            increments.insert(0, "stratum", stratum)
            increment_rows.append(increments)
            log(f"  {kind}: bootstrap done ({resamples} resamples)", handle)

            reference = log_loss(y, predictions[0], modelling.probability_clip)
            step2_skill = skill(log_loss(y, predictions[2], modelling.probability_clip), reference)
            for variable, columns in social_groups.items():
                reduced = matrices[2].drop(columns=columns)
                p = cross_fit_predictions(reduced, y, kind, params, modelling.cv_folds, acfg.seed, interactions(reduced.columns))
                without = skill(log_loss(y, p, modelling.probability_clip), reference)
                lovo_rows.append(
                    {"stratum": stratum, "model": kind, "variable removed": variable, "step 2 skill": step2_skill,
                     "skill without variable": without, "skill lost": step2_skill - without}
                )
            log(f"  {kind}: leave-one-variable-out done ({time.time() - started:.0f}s for this model)", handle)

    pd.concat(metrics_rows).to_csv(args.tables_dir / f"model_step_metrics{suffix}.csv", index=False)
    pd.concat(increment_rows).to_csv(args.tables_dir / f"model_increments{suffix}.csv", index=False)
    pd.DataFrame(lovo_rows).to_csv(args.tables_dir / f"model_leave_one_variable_out{suffix}.csv", index=False)
    pd.DataFrame(tuning_rows).to_csv(args.tables_dir / f"model_tuning{suffix}.csv", index=False)
    log("finished", handle)
    handle.close()


if __name__ == "__main__":
    main()
