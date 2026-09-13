"""Model feature blocks kept strictly separate: base, clinical need, social position, pathway (PROTOCOL.md section 5)."""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
import pandas as pd

from seer_study.analysis_config import AnalysisConfig
from seer_study.cohort import MODALITIES
from seer_study.labels import require_known
from seer_study.risk import STAGE_CLASSES

BLOCKS = ("base", "clinical", "social", "pathway")
STEPS = (("base",), ("base", "clinical"), ("base", "clinical", "social"), ("base", "clinical", "social", "pathway"))


@dataclass(frozen=True)
class FeatureBlocks:
    frame: pd.DataFrame
    columns_by_block: dict[str, list[str]]


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def one_hot_column(prefix: str, label: str) -> str:
    """Name of the indicator column for ``label`` in a one-hot encoded variable."""
    return f"{prefix}_{_slug(label)}"


def _one_hot(series: pd.Series, labels: tuple[str, ...], prefix: str) -> pd.DataFrame:
    return pd.DataFrame(
        {one_hot_column(prefix, label): series.eq(label).astype("int64") for label in labels}, index=series.index
    )


def build_feature_blocks(cohort: pd.DataFrame, config: AnalysisConfig, include_pathway: bool = True) -> FeatureBlocks:
    """Feature blocks for the ordered steps. ``include_pathway=False`` leaves the pathway block empty, for men
    without a recorded curative treatment (A9), where modality is part of the outcome."""
    c, spec, risk = config.columns, config.features, config.risk
    index = cohort.index

    base = pd.DataFrame(
        {
            "year": cohort["year_int"].astype("int64"),
            "covid_2020": cohort["year_int"].eq(spec.covid_year).astype("int64"),
        },
        index=index,
    )

    require_known(cohort[c.age], spec.age_midpoints, c.age)
    psa_floor = min(risk.psa_top_codes.values())
    clinical = pd.concat(
        [
            _one_hot(cohort["stage_class"], STAGE_CLASSES, "stage"),
            pd.DataFrame(
                {
                    "gleason_score": cohort["gleason_score"].astype(float),
                    "gleason_missing": cohort["gleason_score"].isna().astype("int64"),
                    "log_psa": np.log(cohort["psa_value"].clip(lower=psa_floor)).astype(float),
                    "psa_top_coded": cohort[c.psa].isin(list(risk.psa_top_codes)).astype("int64"),
                    "psa_missing": cohort["psa_value"].isna().astype("int64"),
                    "age_midpoint": cohort[c.age].map(spec.age_midpoints).astype(float),
                },
                index=index,
            ),
        ],
        axis=1,
    )

    require_known(cohort[c.marital], spec.marital_labels, c.marital)
    require_known(cohort[c.rurality], {*spec.rurality_labels, *spec.rurality_unknown_labels}, c.rurality)
    require_known(cohort[c.income], {*spec.income_order, *spec.income_unknown_labels}, c.income)
    income_rank = {label: rank for rank, label in enumerate(spec.income_order, start=1)}
    social = pd.concat(
        [
            _one_hot(cohort[c.marital], spec.marital_labels, "marital"),
            _one_hot(cohort[c.rurality], spec.rurality_labels, "rurality"),
            pd.DataFrame(
                {
                    "rurality_unknown": cohort[c.rurality].isin(spec.rurality_unknown_labels).astype("int64"),
                    "income_rank": cohort[c.income].map(income_rank).astype(float),
                    "income_unknown": cohort[c.income].isin(spec.income_unknown_labels).astype("int64"),
                },
                index=index,
            ),
        ],
        axis=1,
    )

    if include_pathway:
        require_known(cohort["modality"], MODALITIES, "modality")
        pathway = _one_hot(cohort["modality"], MODALITIES, "modality")
    else:
        pathway = pd.DataFrame(index=index)

    blocks = {"base": base, "clinical": clinical, "social": social, "pathway": pathway}
    return FeatureBlocks(
        frame=pd.concat([blocks[name] for name in BLOCKS], axis=1),
        columns_by_block={name: list(blocks[name].columns) for name in BLOCKS},
    )


def design_matrix(blocks: FeatureBlocks, step: int) -> pd.DataFrame:
    empty = [name for name in STEPS[step] if not blocks.columns_by_block[name]]
    if empty:
        raise ValueError(f"step {step} needs the {', '.join(empty)} block, which was not built")
    columns =[column for name in STEPS[step] for column in blocks.columns_by_block[name]]
    return blocks.frame[columns]
