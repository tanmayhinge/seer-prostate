"""Typed configuration for the timeliness analysis (config/analysis.yaml)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from seer_study.config import ConfigError, load_typed_yaml


@dataclass(frozen=True)
class AnalysisColumns:
    year: str
    sequence: str
    stage: str
    survival_flag: str
    age: str
    surgery_old: str
    surgery_new: str
    radiation: str
    interval: str
    gleason_clinical: str
    psa: str
    marital: str
    rurality: str
    income: str


@dataclass(frozen=True)
class CohortSpec:
    first_primary_labels: tuple[str, ...]
    first_primary_strict_labels: tuple[str, ...]
    localised_labels: tuple[str, ...]
    regional_extension_labels: tuple[str, ...]
    regional_node_labels: tuple[str, ...]
    dco_labels: tuple[str, ...]
    excluded_age_labels: tuple[str, ...]
    year_min: int
    year_max: int
    sensitivity_year_max: int


@dataclass(frozen=True)
class TreatmentSpec:
    blank_label: str
    prostatectomy_codes: tuple[str, ...]
    prostatectomy_nos_codes: tuple[str, ...]
    surgery_other_codes: tuple[str, ...]
    radiation_labels: tuple[str, ...]
    radiation_other_labels: tuple[str, ...]


@dataclass(frozen=True)
class IntervalSpec:
    missing_labels: tuple[str, ...]
    top_code_label: str
    top_code_days: int
    primary_threshold_days: int
    sensitivity_thresholds_days: tuple[int, ...]


@dataclass(frozen=True)
class RiskSpec:
    gleason_pattern: str
    gleason_missing_labels: tuple[str, ...]
    psa_missing_labels: tuple[str, ...]
    psa_top_codes: dict[str, float]
    low_max_gleason: int
    intermediate_gleason: int
    high_min_gleason: int
    low_psa_below: float
    high_psa_above: float


@dataclass(frozen=True)
class FeatureSpec:
    covid_year: int
    age_midpoints: dict[str, float]
    marital_labels: tuple[str, ...]
    rurality_labels: tuple[str, ...]
    rurality_unknown_labels: tuple[str, ...]
    income_order: tuple[str, ...]
    income_unknown_labels: tuple[str, ...]


@dataclass(frozen=True)
class ModellingSpec:
    cv_folds: int
    bootstrap_resamples: int
    tuning_rows: int
    min_meaningful_percentage_points: float
    min_meaningful_days: float


@dataclass(frozen=True)
class AnalysisConfig:
    seed: int
    columns: AnalysisColumns
    cohort: CohortSpec
    treatment: TreatmentSpec
    interval: IntervalSpec
    risk: RiskSpec
    features: FeatureSpec
    modelling: ModellingSpec


def load_analysis_config(path: str | Path) -> AnalysisConfig:
    config = load_typed_yaml(path, AnalysisConfig)
    overlap = set(config.treatment.prostatectomy_codes) & set(config.treatment.surgery_other_codes)
    if overlap:
        raise ConfigError(f"treatment: codes listed as both prostatectomy and other: {sorted(overlap)}")
    if not set(config.treatment.prostatectomy_nos_codes) <= set(config.treatment.prostatectomy_codes):
        raise ConfigError("treatment: prostatectomy_nos_codes must be a subset of prostatectomy_codes")
    if set(config.treatment.radiation_labels) & set(config.treatment.radiation_other_labels):
        raise ConfigError("treatment: a radiation label is listed as both definitive and other")
    if config.cohort.year_max > config.cohort.sensitivity_year_max:
        raise ConfigError("cohort: year_max cannot exceed sensitivity_year_max")
    return config
