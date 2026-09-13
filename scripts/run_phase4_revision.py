"""Phase 4 revision analyses after internal review (PROTOCOL.md amendment 1.9), all labelled post-review.

(a) per-step tuning; (b) cross-fitting variability over fold-assignment seeds; (c) bootstrap cluster sizes and a
coarser clustering; (d) stage-free clinical block; (e) year as categories in logistic regression; (f) concentration
index by diagnosis period; (g) long and top-coded intervals. Aggregate tables go to reports/phase4_tables/; tables
with exact group counts are git-ignored.
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study.analysis_config import load_analysis_config
from seer_study.cohort import build_cohort
from seer_study.config import load_config
from seer_study.describe import income_group, load_reporting_config, period_band, rurality_group
from seer_study.equity import erreygers_index
from seer_study.features import build_feature_blocks, design_matrix, year_as_categories
from seer_study.increments import bootstrap_increments, cluster_bootstrap_interval, cluster_size_summary
from seer_study.io import read_dictionary, read_export, validate_frame
from seer_study.metrics import log_loss, skill
from seer_study.models import MODEL_KINDS, cross_fit_predictions, tune_hyperparameters
from seer_study.risk import RISK_GROUPS

STRATA = ("all", *RISK_GROUPS)
STEPS = (0, 1, 2)
CELLS = "rurality by income cells"
INCOME_ONLY = "county income band only"


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
    parser.add_argument("--seed-repeats", type=int, default=None, help="development only: override")
    parser.add_argument("--strata", nargs="+", default=list(STRATA), help="development only")
    args = parser.parse_args()

    study = load_config(args.study_config)
    acfg = load_analysis_config(args.analysis_config)
    rcfg = load_reporting_config(args.reporting_config)
    modelling, revision, c = acfg.modelling, acfg.revision, acfg.columns
    seed, clip, level = acfg.seed, modelling.probability_clip, modelling.interval_level
    resamples = args.bootstrap_resamples or modelling.bootstrap_resamples
    repeats = args.seed_repeats or revision.fold_seed_repeats
    suffix = f"_sample{args.sample}" if args.sample else ""
    t = args.tables_dir
    handle = open(t / f"revision_log{suffix}.txt", "w")

    frame = read_export(study.paths.export, read_dictionary(study.paths.dictionary))
    validate_frame(frame, study.data)
    cohort = build_cohort(frame, acfg).frame
    if args.sample:
        cohort = cohort.sample(n=min(args.sample, len(cohort)), random_state=seed).sort_index()
    log(f"cohort {len(cohort):,} men", handle)

    # (g) long and top-coded intervals (exact counts; the report publishes suppressed percentages)
    long_rows = []
    groups = {"risk group": cohort["risk_group"], "rurality": rurality_group(cohort[c.rurality], acfg.features, rcfg)}
    days = cohort["interval_days"].to_numpy()
    for variable, labels in groups.items():
        for label in pd.unique(labels):
            gmask = (labels == label).to_numpy()
            long_rows.append({
                "variable": variable, "group": label, "n": int(gmask.sum()),
                "n_long": int((days[gmask] > revision.long_interval_days).sum()),
                "n_top_coded": int(cohort["interval_top_coded"].to_numpy()[gmask].sum()),
            })
    pd.DataFrame(long_rows).to_csv(t / f"revision_long_intervals{suffix}.csv", index=False)

    # (f) concentration index by diagnosis period, and income quartile distribution by period
    blocks = build_feature_blocks(cohort, acfg)
    income_rank = design_matrix(blocks, 2)["income_rank"].to_numpy()
    periods = period_band(cohort["year_int"], acfg.cohort, rcfg)
    cells_all = (cohort[c.rurality] + " | " + cohort[c.income]).to_numpy()
    y_all = cohort["delayed"].astype(bool).to_numpy().astype(int)
    period_rows = []
    for stratum in STRATA:
        smask = np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()
        for period in pd.unique(periods):
            m = smask & (periods == period).to_numpy() & ~np.isnan(income_rank)
            ys, ranks = y_all[m], income_rank[m]
            estimate, lower, upper = cluster_bootstrap_interval(
                lambda index, ys=ys, ranks=ranks: erreygers_index(ys[index], ranks[index]), cells_all[m], resamples, seed, level
            )
            period_rows.append({"stratum": stratum, "period": period, "n": int(m.sum()), "estimate": estimate, "lower": lower, "upper": upper})
    pd.DataFrame(period_rows).drop(columns="n").to_csv(t / f"revision_erreygers_by_period{suffix}.csv", index=False)
    quartiles = income_group(cohort[c.income].map({l: i for i, l in enumerate(acfg.features.income_order, start=1)}), acfg.features, rcfg)
    pd.crosstab(periods, quartiles).reset_index().rename(columns={"index": "period"}).to_csv(
        t / f"revision_income_by_period{suffix}.csv", index=False
    )
    log("(f) and (g) done", handle)

    # (a) to (e) models
    clinical = blocks.columns_by_block["clinical"]
    alt_all = cohort[getattr(c, revision.alternative_cluster_column)].to_numpy()
    years = sorted(int(y) for y in cohort["year_int"].unique())
    stage_free = (revision.stage_free_prefix,)
    tuning_rows, seed_rows, interval_rows, cluster_rows = [], [], [], []

    def write():
        pd.DataFrame(tuning_rows).to_csv(t / f"revision_tuning{suffix}.csv", index=False)
        pd.DataFrame(seed_rows).to_csv(t / f"revision_seed_increments{suffix}.csv", index=False)
        pd.DataFrame(interval_rows).to_csv(t / f"revision_intervals{suffix}.csv", index=False)
        pd.DataFrame(cluster_rows).to_csv(t / f"revision_cluster_sizes{suffix}.csv", index=False)

    def add_intervals(analysis, stratum, kind, clustering, y, predictions, clusters):
        table = bootstrap_increments(y, predictions, clusters, resamples, seed, clip, level)
        for row in table.itertuples():
            interval_rows.append({"analysis": analysis, "stratum": stratum, "model": kind, "clustering": clustering,
                                  "comparison": row.comparison, "estimate": row.estimate, "lower": row.lower, "upper": row.upper})

    for stratum in args.strata:
        mask = np.ones(len(cohort), dtype=bool) if stratum == "all" else (cohort["risk_group"] == stratum).to_numpy()
        y, cells, alt = y_all[mask], cells_all[mask], alt_all[mask]
        for clustering, clusters in ((CELLS, cells), (INCOME_ONLY, alt)):
            cluster_rows.append({"stratum": stratum, "clustering": clustering,
                                 **cluster_size_summary(clusters, rcfg.small_count_threshold, rcfg.suppression_mask)})
        matrices = {step: design_matrix(blocks, step).loc[mask] for step in STEPS}
        for kind in MODEL_KINDS:
            def interactions(columns):
                return [col for col in clinical if col in columns] if kind == "logistic" else []

            started = time.time()
            grid, fixed = model_settings(kind, modelling)
            params = {}
            for step in STEPS:
                params[step] = tune_hyperparameters(
                    matrices[step], y, kind, grid, fixed, modelling.tuning_folds, seed, modelling.tuning_rows,
                    interactions(matrices[step].columns), clip,
                )
                tuning_rows.append({"stratum": stratum, "model": kind, "step": step, **params[step]})
            log(f"{stratum} {kind}: per-step tuning {params} ({time.time() - started:.0f}s)", handle)

            for k in range(repeats):
                predictions = {
                    step: cross_fit_predictions(matrices[step], y, kind, params[step], modelling.cv_folds, seed + k,
                                                interactions(matrices[step].columns))
                    for step in STEPS
                }
                losses = {step: log_loss(y, predictions[step], clip) for step in STEPS}
                skills = {step: skill(losses[step], losses[0]) for step in STEPS}
                seed_rows.append({"stratum": stratum, "model": kind, "fold_seed": seed + k,
                                  "clinical need (step 0 to 1)": skills[1] - skills[0],
                                  "social position (step 1 to 2)": skills[2] - skills[1], "step 2 skill": skills[2]})
                if k == 0:
                    add_intervals("per-step tuning", stratum, kind, CELLS, y, predictions, cells)
                    add_intervals("per-step tuning", stratum, kind, INCOME_ONLY, y, predictions, alt)
            log(f"{stratum} {kind}: {repeats} fold seeds done ({time.time() - started:.0f}s)", handle)

            sf = {step: design_matrix(blocks, step, exclude_prefixes=stage_free).loc[mask] for step in STEPS}
            predictions = {step: cross_fit_predictions(sf[step], y, kind, params[step], modelling.cv_folds, seed,
                                                       interactions(sf[step].columns)) for step in STEPS}
            add_intervals("stage-free clinical block", stratum, kind, CELLS, y, predictions, cells)

            if kind == "logistic":
                yc = {step: year_as_categories(matrices[step], years) for step in STEPS}
                predictions = {step: cross_fit_predictions(yc[step], y, kind, params[step], modelling.cv_folds, seed,
                                                           interactions(yc[step].columns)) for step in STEPS}
                add_intervals("year as categories", stratum, kind, CELLS, y, predictions, cells)
            write()
            log(f"{stratum} {kind}: done ({time.time() - started:.0f}s)", handle)

    write()
    log("finished", handle)
    handle.close()


if __name__ == "__main__":
    main()
