"""Cohort construction: exclusions in protocol order with counts, and derived treatment, interval and risk columns."""

from __future__ import annotations

from dataclasses import dataclass, fields

import numpy as np
import pandas as pd

from seer_study.analysis_config import AnalysisConfig, ScenarioSpec
from seer_study.labels import UnmappedLabelError, require_known
from seer_study.risk import assign_risk, parse_gleason, parse_psa, stage_class

__all__ = ["MODALITIES", "CohortOptions", "CohortResult", "UnmappedLabelError", "build_cohort", "scenario_options"]

MODALITIES = ("surgery_only", "radiotherapy_only", "both")


@dataclass(frozen=True)
class CohortOptions:
    """Switches for the pre-specified sensitivity analyses (PROTOCOL.md A8). Defaults give the primary cohort."""

    include_2023: bool = False
    exclude_covid_year: bool = False
    include_zero_days: bool = False
    strict_first_primary: bool = False
    exclude_prostatectomy_nos: bool = False
    surgery_only: bool = False
    risk_from_grade_and_psa_only: bool = False
    threshold_days: int | None = None


@dataclass(frozen=True)
class CohortResult:
    """``eligible``: men meeting every step before treatment, with risk group and a ``curative`` flag (A9).
    ``treated``: the curative part of ``eligible``, before interval exclusions (A7). ``frame``: the analysis cohort.
    """

    frame: pd.DataFrame
    treated: pd.DataFrame
    flow: pd.DataFrame
    options: CohortOptions
    threshold_days: int
    eligible: pd.DataFrame


def scenario_options(spec: ScenarioSpec) -> CohortOptions:
    """Cohort options for a configured sensitivity scenario."""
    return CohortOptions(**{f.name: getattr(spec, f.name) for f in fields(CohortOptions)})


def _validate_labels(frame: pd.DataFrame, config: AnalysisConfig) -> None:
    c, treatment, interval = config.columns, config.treatment, config.interval
    surgery_codes = {treatment.blank_label, *treatment.prostatectomy_codes, *treatment.surgery_other_codes}
    require_known(frame[c.surgery_old], surgery_codes, c.surgery_old)
    require_known(frame[c.surgery_new], surgery_codes, c.surgery_new)
    require_known(frame[c.radiation], {*treatment.radiation_labels, *treatment.radiation_other_labels}, c.radiation)
    values = frame[c.interval]
    recorded = values.str.fullmatch(r"\d+").astype(bool)
    require_known(values[~recorded], {*interval.missing_labels, interval.top_code_label}, c.interval)


def _derive(frame: pd.DataFrame, config: AnalysisConfig, options: CohortOptions, threshold: int) -> pd.DataFrame:
    c, interval, treatment = config.columns, config.interval, config.treatment
    out = frame.copy()
    out["year_int"] = pd.to_numeric(frame[c.year]).astype("int64")
    codes = set(treatment.prostatectomy_codes)
    if options.exclude_prostatectomy_nos:
        codes -= set(treatment.prostatectomy_nos_codes)
    prostatectomy = frame[c.surgery_old].isin(codes) | frame[c.surgery_new].isin(codes)
    radiotherapy = frame[c.radiation].isin(treatment.radiation_labels)
    out["prostatectomy"] = prostatectomy
    out["radiotherapy"] = radiotherapy
    out["modality"] = np.select(
        [(prostatectomy & radiotherapy).to_numpy(), prostatectomy.to_numpy(), radiotherapy.to_numpy()],
        ["both", "surgery_only", "radiotherapy_only"],
        default="none",
    )
    values = frame[c.interval]
    recorded = values.str.fullmatch(r"\d+").astype(bool)
    top_coded = values.eq(interval.top_code_label)
    out["interval_class"] = np.select([recorded.to_numpy(), top_coded.to_numpy()], ["recorded", "top_coded"], default="missing")
    days = pd.to_numeric(values.where(recorded), errors="coerce").astype(float)
    out["interval_days"] = days.mask(top_coded, float(interval.top_code_days))
    out["interval_top_coded"] = top_coded
    delayed = pd.array(out["interval_days"] > threshold, dtype="boolean")
    delayed[out["interval_days"].isna().to_numpy()] = pd.NA
    out["delayed"] = delayed
    out["stage_class"] = stage_class(frame[c.stage], config.cohort)
    return out


def build_cohort(frame: pd.DataFrame, config: AnalysisConfig, options: CohortOptions = CohortOptions()) -> CohortResult:
    _validate_labels(frame, config)
    c, cohort = config.columns, config.cohort
    threshold = options.threshold_days if options.threshold_days is not None else config.interval.primary_threshold_days
    data = _derive(frame, config, options, threshold)

    first_labels = cohort.first_primary_strict_labels if options.strict_first_primary else cohort.first_primary_labels
    year_max = cohort.sensitivity_year_max if options.include_2023 else cohort.year_max
    if options.surgery_only:
        curative = data["prostatectomy"] & ~data["radiotherapy"]
        curative_step = "first course is prostatectomy without radiotherapy"
    else:
        curative = data["prostatectomy"] | data["radiotherapy"]
        curative_step = "first course includes prostatectomy or radiotherapy"
    positive = data["interval_days"].gt(0) | pd.Series(options.include_zero_days, index=data.index)

    treated_steps = [
        ("first primary", frame[c.sequence].isin(first_labels)),
        ("localised or regional stage", data["stage_class"].ne("other")),
        ("not death certificate or autopsy only", ~frame[c.survival_flag].isin(cohort.dco_labels)),
        ("age 40 or over", ~frame[c.age].isin(cohort.excluded_age_labels)),
        (f"diagnosed {cohort.year_min} to {year_max}", data["year_int"].between(cohort.year_min, year_max)),
    ]
    if options.exclude_covid_year:
        covid_year = config.features.covid_year
        treated_steps.append((f"not diagnosed in {covid_year}", data["year_int"].ne(covid_year)))
    treated_steps.append((curative_step, curative))
    interval_steps = [
        ("interval recorded or top-coded", data["interval_class"].ne("missing")),
        ("interval above 0 days" if not options.include_zero_days else "interval above 0 days (not applied)", positive),
    ]

    keep = pd.Series(True, index=data.index)
    flow = [("all records", len(data), 0)]
    eligible_keep = None
    for position, (step, condition) in enumerate(treated_steps + interval_steps):
        before = int(keep.sum())
        keep &= condition.fillna(False).astype(bool)
        flow.append((step, int(keep.sum()), before - int(keep.sum())))
        if position == len(treated_steps) - 2:
            eligible_keep = keep.copy()

    eligible = data[eligible_keep].copy()
    eligible["curative"] = curative[eligible_keep].fillna(False).astype(bool)
    gleason = parse_gleason(eligible[c.gleason_clinical], config.risk)
    psa = parse_psa(eligible[c.psa], config.risk)
    eligible["gleason_score"] = gleason
    eligible["psa_value"] = psa
    eligible["risk_group"] = assign_risk(
        eligible["stage_class"], gleason, psa, config.risk, use_stage=not options.risk_from_grade_and_psa_only
    )
    treated = eligible[eligible["curative"].to_numpy()].copy()
    final = treated[keep.loc[treated.index].to_numpy()].copy()
    return CohortResult(
        frame=final,
        treated=treated,
        flow=pd.DataFrame(flow, columns=["step", "remaining", "excluded"]),
        options=options,
        threshold_days=threshold,
        eligible=eligible,
    )
