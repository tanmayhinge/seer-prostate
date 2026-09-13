"""Phase 4 secondary question (PROTOCOL.md A9, amendment 1.8): a recorded radical prostatectomy or radiotherapy.

Among intermediate- and high-risk men meeting every cohort step before treatment, the outcome is a record of
radical prostatectomy or radiotherapy in the first course. Men without such a record include men on active
surveillance or watchful waiting, hormone therapy only, men who refused, and men whose treatment was not captured.

Ordered steps 0 to 2 for both model types (tuned once per model and stratum on step 2), cluster bootstrap increments,
standardised percentages for joint area profiles and marital status, and crude percentages. Aggregate tables go to
reports/phase4_tables/; crude tables hold exact counts and are git-ignored.
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import load_config
from seer_study.describe import income_group, load_reporting_config, rurality_group
from seer_study.descriptive import delay_summary
from seer_study.features import build_feature_blocks, design_matrix
from seer_study.increments import bootstrap_increments, step_metrics
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.models import MODEL_KINDS, cross_fit_predictions, fit_full_model, tune_hyperparameters
from seer_study.risk import RISK_GROUPS
from seer_study.standardise import area_income_ranks, standardised_percentages


def log(message: str, handle) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    print(line, flush=True)
    handle.write(line + "\n")
    handle.flush()


def model_settings(kind: str, modelling) -> tuple[dict, dict]:
    if kind == "logistic":
        return {"C": modelling.logistic_c_grid}, {"max_iter": modelling.logistic_max_iter}
    return dict(modelling.lightgbm_grid), {"learning_rate": modelling.lightgbm_learning_rate}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-config", type=Path, default=Path("config/study.yaml"))
    parser.add_argument("--analysis-config", type=Path, default=Path("config/analysis.yaml"))
    parser.add_argument("--reporting-config", type=Path, default=Path("config/reporting.yaml"))
    parser.add_argument("--tables-dir", type=Path, default=Path("reports/phase4_tables"))
    parser.add_argument("--sample", type=int, default=None, help="development only: random subsample")
    parser.add_argument("--bootstrap-resamples", type=int, default=None, help="development only: override")
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling, features, c = acfg.modelling, acfg.features, acfg.columns
    seed, clip, level = acfg.seed, modelling.probability_clip, modelling.interval_level
    resamples = args.bootstrap_resamples or modelling.bootstrap_resamples
    suffix = f"_sample{args.sample}" if args.sample else ""
    groups = list(acfg.receipt.risk_groups)
    unknown = sorted(set(groups) - set(RISK_GROUPS))
    if unknown:
        raise ValueError(f"receipt.risk_groups has unknown risk group(s) {unknown}")
    handle = open(args.tables_dir / f"receipt_log{suffix}.txt", "w")

    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)
    eligible = build_cohort(frame, acfg).eligible
    men = eligible[eligible["risk_group"].isin(groups)].copy()
    if args.sample:
        men = men.sample(n=min(args.sample, len(men)), random_state=seed).sort_index()
    y_all = men["curative"].to_numpy().astype(int)
    log(f"eligible {'/'.join(groups)} risk men: {len(men):,}, {y_all.mean():.4f} with a recorded curative treatment", handle)

    # Crude percentages (exact counts; published in rounded, suppressed form by the report script)
    income_rank = men[c.income].map({label: i for i, label in enumerate(features.income_order, start=1)})
    crude = men.assign(
        rurality=rurality_group(men[c.rurality], features, rcfg),
        county_income_quartile=income_group(income_rank, features, rcfg),
        marital_status=men[c.marital],
        recorded=men["curative"],
    )
    for by in (["risk_group"], ["risk_group", "rurality"], ["risk_group", "county_income_quartile"], ["risk_group", "marital_status"]):
        table = delay_summary(crude, by, "recorded", "interval_days").drop(columns=["median_days", "p90_days"])
        table = table.rename(columns={"n_delayed": "n_recorded", "pct_delayed": "pct_recorded"})
        table.to_csv(args.tables_dir / f"receipt_crude_{'_'.join(by)}{suffix}.csv", index=False)

    blocks = build_feature_blocks(men, acfg, include_pathway=False)
    clinical = blocks.columns_by_block["clinical"]
    clusters_all = (men[c.rurality] + " | " + men[c.income]).to_numpy()
    matrices_all = {step: design_matrix(blocks, step) for step in (0, 1, 2)}
    reference = {
        "marital": modelling.reference_marital,
        "rurality": modelling.reference_rurality,
        "income_rank": float(np.nanquantile(matrices_all[2]["income_rank"], modelling.reference_income_quantile)),
    }
    area_rank = area_income_ranks(matrices_all[2]["income_rank"], men[c.rurality], features.rurality_labels)
    profiles = {f"area: {label}": {"rurality": label, "income_rank": area_rank[label]} for label in features.rurality_labels}
    profiles.update({f"marital status: {label}": {"marital": label} for label in features.marital_labels})
    pd.DataFrame(
        [{"rurality": label, "median income rank": rank, "income band": features.income_order[int(round(rank)) - 1]}
         for label, rank in area_rank.items()]
    ).to_csv(args.tables_dir / f"receipt_area_income{suffix}.csv", index=False)

    tuning_rows, metrics_rows, increment_rows, profile_rows = [], [], [], []
    for stratum in ["all", *groups]:
        mask = np.ones(len(men), dtype=bool) if stratum == "all" else (men["risk_group"] == stratum).to_numpy()
        y = y_all[mask]
        matrices = {step: matrix.loc[mask] for step, matrix in matrices_all.items()}
        for kind in MODEL_KINDS:
            def interactions(columns):
                return [col for col in clinical if col in columns] if kind == "logistic" else []

            started = time.time()
            grid, fixed = model_settings(kind, modelling)
            params = tune_hyperparameters(
                matrices[2], y, kind, grid, fixed, modelling.tuning_folds, seed, modelling.tuning_rows,
                interactions(matrices[2].columns), clip,
            )
            tuning_rows.append({"stratum": stratum, "model": kind, **params, "seconds": round(time.time() - started, 1)})
            predictions = {
                step: cross_fit_predictions(matrix, y, kind, params, modelling.cv_folds, seed, interactions(matrix.columns))
                for step, matrix in matrices.items()
            }
            metrics = step_metrics(y, predictions, clip)
            increments = bootstrap_increments(y, predictions, clusters_all[mask], resamples, seed, clip, level)
            for table, rows in ((metrics, metrics_rows), (increments, increment_rows)):
                table.insert(0, "model", kind)
                table.insert(0, "stratum", stratum)
                rows.append(table)
            model = fit_full_model(matrices[2], y, kind, params, seed, interactions(matrices[2].columns))
            for name, value in standardised_percentages(model, matrices[2], features, reference, profiles).items():
                profile_rows.append({"stratum": stratum, "model": kind, "profile": name, "standardised %": value})
            social = increments.loc[increments["comparison"].str.startswith("social"), "estimate"].item()
            log(f"{stratum} {kind}: tuned {params}; social increment {100 * social:.2f} points ({time.time() - started:.0f}s)", handle)

    pd.DataFrame(tuning_rows).to_csv(args.tables_dir / f"receipt_tuning{suffix}.csv", index=False)
    pd.concat(metrics_rows).to_csv(args.tables_dir / f"receipt_step_metrics{suffix}.csv", index=False)
    pd.concat(increment_rows).to_csv(args.tables_dir / f"receipt_increments{suffix}.csv", index=False)
    pd.DataFrame(profile_rows).to_csv(args.tables_dir / f"receipt_profiles{suffix}.csv", index=False)
    log("finished", handle)
    handle.close()


if __name__ == "__main__":
    main()
