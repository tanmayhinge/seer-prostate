"""Clinical risk grouping from summary stage, clinical Gleason score and PSA (PROTOCOL.md section 4)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from seer_study.analysis_config import CohortSpec, RiskSpec
from seer_study.inventory import NUMERIC_PATTERN
from seer_study.labels import require_known

STAGE_CLASSES = ("localised", "regional_extension", "regional_nodes")
RISK_GROUPS = ("low", "intermediate", "high", "unknown")


def stage_class(series: pd.Series, cohort: CohortSpec) -> pd.Series:
    classes = np.full(len(series), "other", dtype=object)
    classes[series.isin(cohort.localised_labels).to_numpy()] = "localised"
    classes[series.isin(cohort.regional_extension_labels).to_numpy()] = "regional_extension"
    classes[series.isin(cohort.regional_node_labels).to_numpy()] = "regional_nodes"
    return pd.Series(classes, index=series.index, name="stage_class")


def parse_gleason(series: pd.Series, risk: RiskSpec) -> pd.Series:
    scores = series.str.extract(risk.gleason_pattern)[0]
    require_known(series[scores.isna()], risk.gleason_missing_labels, "clinical Gleason score")
    return pd.to_numeric(scores, errors="coerce").astype(float).rename("gleason_score")


def parse_psa(series: pd.Series, risk: RiskSpec) -> pd.Series:
    numeric = series.str.fullmatch(NUMERIC_PATTERN).astype(bool)
    top_coded = series.isin(list(risk.psa_top_codes))
    require_known(series[~numeric & ~top_coded], risk.psa_missing_labels, "PSA")
    values = pd.to_numeric(series.where(numeric), errors="coerce").astype(float)
    return values.mask(top_coded, series.map(risk.psa_top_codes)).astype(float).rename("psa_value")


def assign_risk(
    stage: pd.Series, gleason: pd.Series, psa: pd.Series, risk: RiskSpec, use_stage: bool = True
) -> pd.Series:
    """High if regional, Gleason >= 8 or PSA above the high cut; unknown if undeterminable; then intermediate; then low."""
    if use_stage:
        invalid = sorted(set(stage) - set(STAGE_CLASSES))
        if invalid:
            raise ValueError(f"risk grouping needs localised or regional stage, got {invalid}")
        regional = stage.isin(["regional_extension", "regional_nodes"]).to_numpy()
    else:
        regional = np.zeros(len(stage), dtype=bool)
    g = gleason.to_numpy(dtype=float)
    p = psa.to_numpy(dtype=float)
    high = regional | (g >= risk.high_min_gleason) | (p > risk.high_psa_above)
    unknown = ~high & (np.isnan(g) | np.isnan(p))
    intermediate = ~high & ~unknown & ((g == risk.intermediate_gleason) | (p >= risk.low_psa_below))
    low = ~high & ~unknown & ~intermediate & (g <= risk.low_max_gleason) & (p < risk.low_psa_below)
    groups = np.select([high, unknown, intermediate, low], ["high", "unknown", "intermediate", "low"], default="")
    if (groups == "").any():
        raise ValueError("some rows could not be assigned a risk group; check the risk thresholds")
    return pd.Series(groups.astype(object), index=stage.index, name="risk_group")
