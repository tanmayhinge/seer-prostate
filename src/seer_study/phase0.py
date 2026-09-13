"""Phase 0: inventory of the raw SEER export.

run_phase0 computes every table, render_phase0 turns them into markdown, and
write_phase0 writes reports/phase0.md plus full frequency tables as CSV.
Nothing in this phase excludes, recodes or models anything.
"""

from __future__ import annotations

import os
import platform
import random
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from seer_study import inventory as inv
from seer_study.config import ColumnSpec, StudyConfig, validate_config
from seer_study.io import (
    file_sha256,
    read_dictionary,
    read_dictionary_options,
    read_export,
    validate_frame,
    zip_member_sha256,
)
from seer_study.report import assert_style, fmt_float, fmt_int, fmt_pct, md_table

RECORDED_DAYS = "days recorded"


@dataclass(frozen=True)
class Provenance:
    dictionary_options: dict[str, str]
    selection_note: str | None
    selection_criteria: list[str]
    unexpected_selection: list[str]
    session_file_present: bool
    session_like_files: tuple[str, ...]
    export_sha256: str
    archive_sha256: str | None
    archive_matches: bool | None


@dataclass(frozen=True)
class Phase0Results:
    config: StudyConfig
    names: list[str]
    generated_at: str
    versions: dict[str, str]
    provenance: Provenance
    example_id: str
    row_summary: inv.RowSummary
    year_counts: pd.DataFrame
    missingness: pd.DataFrame
    suspect_labels: pd.DataFrame
    frequencies: dict[str, pd.DataFrame]
    numeric_profiles: dict[str, inv.NumericProfile]
    single_valued: list[str]
    absent_variables: dict[str, list[str]]
    surgery_by_year: pd.DataFrame
    age: inv.AgeCheck | None
    completeness_clinical: pd.DataFrame
    completeness_pathological: pd.DataFrame
    completeness_psa: pd.DataFrame
    surgery_groups: pd.DataFrame
    pathological_by_surgery: pd.DataFrame
    time_to_treatment: inv.NumericProfile
    ttt_by_surgery: pd.DataFrame
    ttt_by_radiation: pd.DataFrame | None
    reason_frequency: pd.DataFrame
    reason_by_year: pd.DataFrame
    sequence: inv.SequenceProfile
    first_primary_ids: inv.RowSummary
    stage_counts: pd.DataFrame
    stage_pct: pd.DataFrame


# ---------------------------------------------------------------- computation


def run_phase0(config: StudyConfig) -> Phase0Results:
    random.seed(config.seed)
    np.random.seed(config.seed)
    names = read_dictionary(config.paths.dictionary)
    validate_config(config, names)
    frame = read_export(config.paths.export, names)
    validate_frame(frame, config.data)

    data = config.data
    spec = config.inventory
    years = list(data.years)

    year_rows = frame[data.year_column].value_counts().reindex(years, fill_value=0)
    year_counts = pd.DataFrame({"year": years, "rows": year_rows.to_numpy(dtype="int64")})
    year_counts["pct"] = 100.0 * year_counts["rows"] / len(frame)

    ttt = inv.time_to_treatment_profile(frame, config)
    numeric_profiles = {}
    for column in names:
        column_spec = config.columns[column]
        if column_spec.kind != "numeric_string":
            continue
        if column == spec.time_to_treatment_column:
            numeric_profiles[column] = ttt
        else:
            numeric_profiles[column] = inv.numeric_profile(frame, column, config, unit=column_spec.unit or "value")

    groups = inv.surgery_code_group(frame, config)
    pathological_parts = []
    for column in spec.pathological_grade_columns:
        table = inv.completeness_by_group(frame, column, groups, config)
        table.insert(0, "column", column)
        table["pct_not_applicable"] = 100.0 * table["not_applicable"] / table["n"].where(table["n"] > 0)
        pathological_parts.append(table)

    ttt_classes = ttt.classes.replace({"numeric": RECORDED_DAYS}).rename("time to treatment")
    ttt_by_surgery = inv.crosstab_counts(
        pd.DataFrame({"time to treatment": ttt_classes, "surgery code group": groups}),
        "time to treatment",
        "surgery code group",
    )
    ttt_by_radiation = None
    if spec.radiation_column is not None:
        ttt_by_radiation = inv.crosstab_counts(
            pd.DataFrame({"time to treatment": ttt_classes, spec.radiation_column: frame[spec.radiation_column]}),
            "time to treatment",
            spec.radiation_column,
        )

    sequence = inv.sequence_profile(frame, config)

    return Phase0Results(
        config=config,
        names=names,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        versions={"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__},
        provenance=_provenance(config),
        example_id=str(frame[data.id_column].iloc[0]),
        row_summary=inv.row_summary(frame, data),
        year_counts=year_counts,
        missingness=inv.missingness(frame, config),
        suspect_labels=inv.suspect_unconfigured_labels(frame, config),
        frequencies={c: inv.frequency(frame[c]) for c in names if config.columns[c].kind != "identifier"},
        numeric_profiles=numeric_profiles,
        single_valued=inv.single_valued_columns(frame),
        absent_variables=inv.check_absent_variables(names, spec.absent_variable_keywords),
        surgery_by_year=inv.nonblank_by_year(frame, list(spec.surgery_columns), config),
        age=inv.age_check(frame, config),
        completeness_clinical=inv.completeness_by_year(frame, list(spec.clinical_grade_columns), config),
        completeness_pathological=inv.completeness_by_year(frame, list(spec.pathological_grade_columns), config),
        completeness_psa=inv.completeness_by_year(frame, list(spec.psa_columns), config),
        surgery_groups=inv.frequency(groups),
        pathological_by_surgery=pd.concat(pathological_parts, ignore_index=True),
        time_to_treatment=ttt,
        ttt_by_surgery=ttt_by_surgery,
        ttt_by_radiation=ttt_by_radiation,
        reason_frequency=inv.frequency(frame[spec.reason_no_surgery_column]),
        reason_by_year=inv.column_percentages(frame, spec.reason_no_surgery_column, data.year_column),
        sequence=sequence,
        first_primary_ids=inv.row_summary(frame[sequence.inclusive_mask], data),
        stage_counts=inv.crosstab_counts(frame, spec.stage_column, data.year_column),
        stage_pct=inv.column_percentages(frame, spec.stage_column, data.year_column),
    )


def _provenance(config: StudyConfig) -> Provenance:
    paths = config.paths
    spec = config.inventory
    folder = paths.export.parent
    session_like = tuple(sorted({p.name for ext in spec.session_file_extensions for p in folder.glob(f"*{ext}")}))
    note = paths.selection_note.read_text() if paths.selection_note.exists() else None
    criteria = inv.selection_criteria(note) if note else []
    export_sha = file_sha256(paths.export)
    archive_sha = zip_member_sha256(paths.archive, paths.archive_member) if paths.archive.exists() else None
    return Provenance(
        dictionary_options=read_dictionary_options(paths.dictionary),
        selection_note=note,
        selection_criteria=criteria,
        unexpected_selection=inv.unexpected_selection_criteria(criteria, spec.expected_selection_variables),
        session_file_present=paths.session_file.exists(),
        session_like_files=session_like,
        export_sha256=export_sha,
        archive_sha256=archive_sha,
        archive_matches=None if archive_sha is None else archive_sha == export_sha,
    )


def write_phase0(config: StudyConfig) -> Path:
    results = run_phase0(config)
    text = render_phase0(results)
    assert_style(text)
    config.paths.reports_dir.mkdir(parents=True, exist_ok=True)
    config.paths.tables_dir.mkdir(parents=True, exist_ok=True)
    for column, table in results.frequencies.items():
        table.to_csv(config.paths.tables_dir / f"frequency_{_slug(column)}.csv", index=False)
    report = config.paths.reports_dir / "phase0.md"
    report.write_text(text)
    return report


# ---------------------------------------------------------------- rendering


def _slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()


def _short(column: str) -> str:
    return re.sub(r"\s*\((?:\d{4}\+?|\d{4}-\d{4}|thru \d{4})\)$", "", column)


def _roles_of(config: StudyConfig, column: str) -> list[str]:
    roles = config.roles
    return [name for name in roles.__dataclass_fields__ if column in getattr(roles, name)]


def _era_label(spec: ColumnSpec) -> str:
    return spec.era.label() if spec.era else "all years"


def _label_class(value: str, spec: ColumnSpec, blank_label: str) -> str:
    if value in ("numeric", RECORDED_DAYS):
        return "recorded value"
    if value == blank_label:
        return "blank"
    if value in spec.missing:
        return "missing (sentinel)"
    if value in spec.not_applicable:
        return "not applicable"
    if value in spec.top_codes:
        return "top-coded (real value beyond recorded range)"
    return "recorded value"


def _inside_era(years: pd.Index, spec: ColumnSpec) -> np.ndarray:
    values = np.array([int(y) for y in years])
    if spec.era is None:
        return np.ones(len(values), dtype=bool)
    mask = values >= spec.era.first_year
    if spec.era.last_year is not None:
        mask &= values <= spec.era.last_year
    return mask


def _completeness_wide(long: pd.DataFrame, config: StudyConfig) -> pd.DataFrame:
    """Percentages per year; years outside a column's collection era are n/a rather than 100% blank."""
    out: pd.DataFrame | None = None
    for column, part in long.groupby("column", sort=False):
        part = part.set_index("year")
        inside = _inside_era(part.index, config.columns[column])
        denominator = part["n"].where((part["n"] > 0) & inside)
        if out is None:
            out = pd.DataFrame({"year": part.index.to_numpy(), "rows": part["n"].to_numpy()})
        short = _short(column)
        out[f"{short}: % known"] = (100.0 * part["known"] / denominator).to_numpy()
        out[f"{short}: % not applicable"] = (100.0 * part["not_applicable"] / denominator).to_numpy()
        out[f"{short}: % unknown or blank"] = (100.0 * (part["unknown"] + part["blank"]) / denominator).to_numpy()
    return out if out is not None else pd.DataFrame()


def _range_summary(pct: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    for name, values in pct.iterrows():
        rows.append(
            {
                label: name,
                "lowest %": float(values.min()),
                "year of lowest": str(values.idxmin()),
                "highest %": float(values.max()),
                "year of highest": str(values.idxmax()),
                "range (percentage points)": float(values.max() - values.min()),
            }
        )
    return pd.DataFrame(rows)


def _known_range(long: pd.DataFrame, column: str, config: StudyConfig) -> str:
    part = long[(long["column"] == column) & (long["n"] > 0)]
    part = part[_inside_era(pd.Index(part["year"]), config.columns[column])]
    if part.empty:
        return f"{_short(column)}: no rows"
    low = part.loc[part["pct_known"].idxmin()]
    high = part.loc[part["pct_known"].idxmax()]
    return (
        f"{_short(column)} known in {fmt_float(low['pct_known'])}% ({low['year']}) to "
        f"{fmt_float(high['pct_known'])}% ({high['year']}) of each year's rows"
    )


def _findings(r: Phase0Results) -> list[str]:
    c = r.config
    n = r.row_summary.rows
    p = r.provenance
    out = []

    for column in r.single_valued:
        value = r.frequencies[column]["value"].iloc[0] if column in r.frequencies else "(identifier)"
        roles = _roles_of(c, column)
        text = (
            f"`{column}` has a single value, `{value}`, in all {n:,} rows, so it carries no information "
            f"in this export. Role in the brief: {', '.join(roles) or 'unassigned'}."
        )
        if set(roles) & {"clinical", "nonclinical"}:
            text += (
                " Questions 1 to 3 cannot use this variable from this export. A re-export from SEER*Stat "
                "with this variable at its native categories is needed before Phase 3."
            )
        out.append(text)

    if p.unexpected_selection:
        listed = ", ".join(f"`{x}`" for x in p.unexpected_selection)
        out.append(
            f"`{c.paths.selection_note.name}` records selection criteria beyond site and year: {listed}. "
            "The brief states that no other selection was applied."
        )

    if r.age is not None and (r.age.below_18 or r.age.straddling_18):
        detail = ", ".join(f"`{v}` {fmt_int(k)}" for v, k in zip(r.age.table["value"], r.age.table["n"]))
        text = (
            f"{r.age.below_18:,} rows carry an age band entirely below 18 years and {r.age.straddling_18:,} "
            f"rows fall in a band that straddles 18 ({detail})."
        )
        if any("age" in x.lower() for x in p.unexpected_selection):
            text += (
                " An age 18 and over selection would have removed the first group, so the selection note "
                "does not appear to describe this export exactly."
            )
        out.append(text)

    if not p.session_file_present:
        present = ", ".join(f"`{x}`" for x in p.session_like_files) or "none"
        out.append(
            f"`{c.paths.session_file.name}`, named in the brief as the reproducibility record, is not in the "
            f"project folder. SEER*Stat files present: {present}. The selection cannot be checked against a "
            "saved session until the session file is supplied."
        )

    for concept, text in c.inventory.available_not_exported.items():
        out.append(
            f"Available in case listings from this SEER database but not in this export "
            f"({concept.replace('_', ' ')}): {text}"
        )

    if p.archive_matches is False:
        out.append(f"`{c.paths.archive.name}` does not contain a byte-identical copy of `{c.paths.export.name}`.")

    rs = r.row_summary
    if rs.rows_sharing_an_id:
        fp = r.first_primary_ids
        out.append(
            f"{rs.rows_sharing_an_id:,} rows share a Patient ID with at least one other row "
            f"({rs.ids_with_multiple_rows:,} IDs), so rows are tumour records, not men. Among first primaries "
            f"(inclusive definition, item 6) {fp.rows_sharing_an_id:,} rows still share an ID."
        )

    ttt = r.time_to_treatment
    ttt_spec = c.columns[ttt.column]
    top = ", ".join(f"`{x}`" for x in ttt_spec.top_codes)
    out.append(
        f"Time to treatment: {ttt.summary['unknown']:,} rows ({fmt_pct(ttt.summary['unknown'], n)} of all rows) "
        f"carry a missing sentinel and {ttt.summary['top_coded']:,} rows carry the top code {top}. "
        "The top code is a real interval longer than the recorded range and must be analysed as censored at "
        "that bound, not as missing. Item 4 cross-tabulates the sentinel against surgery and radiation codes."
    )

    era_blanks = r.missingness[(r.missingness["era"] != "all years") & (r.missingness["blank_in_era"] > 0)]
    if not era_blanks.empty:
        listed = "; ".join(
            f"`{row.column}` {row.blank_in_era:,} of {row.n_in_era:,} rows in its era"
            for row in era_blanks.itertuples()
        )
        out.append(f"Blanks inside a variable's own collection era (true missingness, not structural): {listed}.")

    if not r.suspect_labels.empty:
        out.append(
            f"{len(r.suspect_labels):,} labels look like missing or partial codes but are not classified as "
            "missing in the configuration. They are listed at the end of item 2 for a decision in Phase 2."
        )
    return out


def _facts_table(r: Phase0Results) -> pd.DataFrame:
    c = r.config
    data = c.data
    spec = c.inventory
    p = r.provenance
    rs = r.row_summary
    rows = []

    def status(ok: bool, fail: str = "Contradicted") -> str:
        return "Confirmed" if ok else fail

    rows.append(
        (
            "Column count",
            f"{data.expected_columns} columns",
            f"{rs.columns} columns parsed; {len(r.names)} names in the dictionary; every line has "
            f"{rs.columns} fields",
            status(rs.columns == data.expected_columns == len(r.names)),
        )
    )
    present = r.year_counts[r.year_counts["rows"] > 0]["year"]
    rows.append(
        (
            "Years of diagnosis",
            f"{data.year_min} to {data.year_max}",
            f"{present.min()} to {present.max()}; {len(present)} of {len(r.year_counts)} years have rows",
            status(len(present) == len(r.year_counts)),
        )
    )
    rows.append(
        (
            "Selection applied before export",
            "Site recode = Prostate; year 2010 to 2023; nothing else",
            "; ".join(p.selection_criteria) or "no selection note found",
            "Contradicted" if p.unexpected_selection else ("Confirmed" if p.selection_criteria else "Not verifiable"),
        )
    )
    for concept, matches in r.absent_variables.items():
        rows.append(
            (
                f"No {concept.replace('_', ' ')} variable",
                "Not available in this product",
                "no column name matches" if not matches else "matching columns: " + ", ".join(matches),
                status(not matches),
            )
        )
    for concept, text in spec.available_not_exported.items():
        rows.append(
            (
                f"{concept.replace('_', ' ').capitalize()} variable",
                "not stated",
                text,
                "Available in database, not exported",
            )
        )
    surgery_notes = []
    surgery_ok = True
    for column in spec.surgery_columns:
        counts = r.surgery_by_year[column]
        populated = counts[counts > 0].index
        era = c.columns[column].era
        if era is not None:
            outside = [y for y in populated if int(y) < era.first_year or (era.last_year and int(y) > era.last_year)]
            surgery_ok &= not outside
        span = f"{populated.min()} to {populated.max()}" if len(populated) else "no year"
        surgery_notes.append(f"`{column}` non-blank in {span}")
    rows.append(("Surgery coding splits at 2023", "Two surgery variables to harmonise", "; ".join(surgery_notes), status(surgery_ok)))
    rows.append(
        (
            "Values read as text",
            "dtype=str, sentinels not mangled",
            f"all columns read as text with NA inference off; first Patient ID reads `{r.example_id}`",
            "Confirmed",
        )
    )
    rows.append(
        (
            "Session definition file",
            f"`{c.paths.session_file.name}` is the reproducibility record",
            "present" if p.session_file_present else "not found; SEER*Stat files present: "
            + (", ".join(p.session_like_files) or "none"),
            status(p.session_file_present, fail="Not found"),
        )
    )
    if p.archive_matches is not None:
        rows.append(
            (
                "Archive copy",
                "not stated",
                f"`{c.paths.archive.name}` member sha256 {'matches' if p.archive_matches else 'differs from'} the export",
                "Confirmed" if p.archive_matches else "Differs",
            )
        )
    stage_missing = [label for label in c.columns[spec.stage_column].missing if label in r.stage_pct.index]
    consistency = []
    for label in stage_missing:
        values = r.stage_pct.loc[label]
        consistency.append(
            f"stage `{label}` is {fmt_float(values.min())}% ({values.idxmin()}) to {fmt_float(values.max())}% "
            f"({values.idxmax()}) of each year's rows"
        )
    consistency += [_known_range(r.completeness_clinical, col, c) for col in spec.clinical_grade_columns[:1]]
    consistency += [_known_range(r.completeness_psa, col, c) for col in spec.psa_columns]
    rows.append(
        (
            "Stage, Gleason and PSA consistent 2010 to 2023",
            "Consistent via Combined Summary Stage, Gleason recodes and PSA recode",
            "; ".join(consistency),
            "See items 3 and 7",
        )
    )
    return pd.DataFrame(rows, columns=["fact", "brief", "export", "status"])


def _numeric_block(r: Phase0Results, profile: inv.NumericProfile, spec: ColumnSpec) -> list[str]:
    s = profile.summary
    n = s["n"]
    blank = r.config.data.blank_label
    blocks = [
        f"Recorded numeric values: {s['numeric']:,} of {n:,} rows ({fmt_pct(s['numeric'], n)}). "
        f"Mean {fmt_float(s['mean'])}, minimum {fmt_float(s['min'])}, maximum {fmt_float(s['max'])} {profile.unit} "
        "(denominator for the mean: recorded numeric values only)."
    ]
    labels = profile.categories[profile.categories["value"] != "numeric"].copy()
    if not labels.empty:
        labels["classification"] = [_label_class(v, spec, blank) for v in labels["value"]]
        labels["SEER meaning"] = [spec.label_notes.get(v, "") for v in labels["value"]]
        labels = labels.rename(columns={"pct": "% of all rows"})
        blocks.append(md_table(labels[["value", "classification", "n", "% of all rows", "SEER meaning"]]))
    quantiles = profile.quantiles.copy()
    quantiles["quantile"] = [f"{round(q * 100)}th percentile" for q in quantiles["quantile"]]
    blocks.append(md_table(quantiles, digits=1))
    return blocks


def render_phase0(r: Phase0Results) -> str:
    c = r.config
    data = c.data
    spec = c.inventory
    rs = r.row_summary
    p = r.provenance
    n = rs.rows
    blank = data.blank_label
    tables_rel = os.path.relpath(c.paths.tables_dir, c.paths.reports_dir)
    blocks: list[str] = []
    add = blocks.append

    add("# Phase 0. Data inventory")
    add(
        f"Generated {r.generated_at} from `{c.paths.export.name}` (sha256 `{p.export_sha256}`) by "
        f"`scripts/run_phase0.py` with seed {c.seed}. Python {r.versions['python']}, pandas "
        f"{r.versions['pandas']}, numpy {r.versions['numpy']}."
    )
    add(
        "How to read this report. Every column was read as text with missing-value inference switched off, so "
        "leading zeros and SEER labels appear exactly as exported. Nothing was excluded or recoded. Each "
        "percentage names its denominator. For completeness, a higher known percentage is better; for "
        "missingness, lower is better. No statistical tests are reported in this phase."
    )

    add("## Findings that need a decision before Phase 2")
    findings = _findings(r)
    add("\n".join(f"- {item}" for item in findings) if findings else "- None.")

    add("## Provenance and verification of known data facts")
    add(md_table(_facts_table(r)))
    add("Export options recorded in the SEER*Stat dictionary file:")
    add(md_table(pd.DataFrame(list(p.dictionary_options.items()), columns=["option", "value"])))
    if p.selection_criteria:
        add(
            f"Selection criteria recorded in `{c.paths.selection_note.name}`:\n\n"
            + "\n".join(f"- `{line}`" for line in p.selection_criteria)
        )
    add("Rows with a non-blank code in each surgery variable, by year of diagnosis:")
    surgery = r.surgery_by_year.copy()
    surgery.insert(0, "rows", r.year_counts.set_index("year")["rows"])
    add(md_table(surgery, index=True))

    # 1
    add("## 1. Row count and columns")
    add(
        md_table(
            pd.DataFrame(
                [
                    ("Rows (tumour records)", n),
                    ("Columns expected", data.expected_columns),
                    ("Columns found", rs.columns),
                    ("Distinct Patient IDs", rs.unique_ids),
                    ("Rows sharing a Patient ID with another row", rs.rows_sharing_an_id),
                    ("Patient IDs with more than one row", rs.ids_with_multiple_rows),
                ],
                columns=["measure", "value"],
            )
        )
    )
    add(f"Rows by year of diagnosis (denominator for %: all {n:,} rows):")
    add(md_table(r.year_counts.rename(columns={"pct": "% of all rows"})))

    # 2
    add("## 2. Missingness for every column")
    add(
        "Classification rules. `Blank(s)` outside a variable's collection era is structural (the item did not "
        "exist for that year) and is not counted as missing. `Blank(s)` inside the era and labels that SEER "
        "documents as unknown are missing. Labels meaning the item does not apply (for example no "
        "prostatectomy) are counted separately as not applicable, because that absence carries information. "
        "Top-coded values are real values and count as known. The label sets and their sources are in "
        "`config/study.yaml`. Denominators: % missing uses rows inside the era; the other percentages use all "
        f"{n:,} rows."
    )
    miss = r.missingness.copy()
    miss.insert(1, "role", [", ".join(_roles_of(c, col)) or "unassigned" for col in miss["column"]])
    miss = miss[
        [
            "column", "role", "kind", "era", "n_in_era", "blank_structural", "blank_in_era", "unknown",
            "not_applicable", "top_coded", "known", "pct_missing_in_era", "pct_not_applicable", "pct_known",
        ]
    ].rename(
        columns={
            "n_in_era": "rows in era",
            "blank_structural": "blank outside era",
            "blank_in_era": "blank inside era",
            "unknown": "unknown label",
            "not_applicable": "not applicable label",
            "top_coded": "top-coded",
            "known": "known (incl. top-coded)",
            "pct_missing_in_era": "% missing (of rows in era)",
            "pct_not_applicable": "% not applicable (of all rows)",
            "pct_known": "% known (of all rows)",
        }
    )
    add(md_table(miss))
    add(
        "Full frequency distributions for every categorical column are in Appendix A; complete tables for all "
        f"non-identifier columns are also written as CSV to `{tables_rel}/`."
    )
    add("Labels that look like missing or partial codes but are treated as recorded values (review in Phase 2):")
    add(md_table(r.suspect_labels) if not r.suspect_labels.empty else "None.")

    # 3
    add("## 3. Gleason and PSA completeness by year")
    add(
        "Known means a recorded score, pattern or value (top-coded PSA counts as known). Not applicable means "
        "the registry records that no biopsy (clinical) or no prostatectomy (pathological) was done. Denominator "
        "for every percentage: all rows diagnosed in that year. Higher % known is better. n/a marks years "
        "outside a variable's collection era."
    )
    add("### 3a. Clinical grade")
    add(md_table(_completeness_wide(r.completeness_clinical, c)))
    add("### 3b. Pathological grade")
    add(
        "Pathological grade exists only when the prostate was removed, so its absence in untreated men is "
        "informative, not random. Table 3d shows this directly."
    )
    add(md_table(_completeness_wide(r.completeness_pathological, c)))
    add("### 3c. PSA")
    add(md_table(_completeness_wide(r.completeness_psa, c)))
    add("### 3d. Pathological grade by raw surgery code (descriptive only)")
    add(
        "Surgery code group is a descriptive grouping of the two raw surgery variables for this inventory "
        f"(none: codes {', '.join(spec.surgery_none_codes)}; unknown: codes {', '.join(spec.surgery_unknown_codes)}; "
        "performed: any other code). It is not the Phase 2 treatment definition. 'Performed' includes local "
        "tumour destruction, local excision and TURP codes, which do not produce a prostatectomy specimen, so "
        "part of that group is correctly recorded as no prostatectomy. Denominator for %: all rows."
    )
    add(md_table(r.surgery_groups.rename(columns={"value": "surgery code group", "pct": "% of all rows"})))
    add("Denominator for % known and % not applicable: rows in that surgery code group.")
    add(
        md_table(
            r.pathological_by_surgery.rename(
                columns={"pct_known": "% known", "pct_not_applicable": "% not applicable"}
            )
        )
    )

    # 4
    ttt = r.time_to_treatment
    ttt_spec = c.columns[ttt.column]
    s = ttt.summary
    add(f"## 4. {ttt.column}")
    if ttt_spec.note:
        add(f"SEER definition: {ttt_spec.note}")
    categories = ttt.categories.copy()
    categories["value"] = categories["value"].replace({"numeric": RECORDED_DAYS})
    categories["classification"] = [_label_class(v, ttt_spec, blank) for v in categories["value"]]
    categories["SEER meaning"] = [ttt_spec.label_notes.get(v, "") for v in categories["value"]]
    add(f"Every row by value type (denominator for %: all {n:,} rows):")
    add(
        md_table(
            categories.rename(columns={"pct": "% of all rows"})[
                ["value", "classification", "n", "% of all rows", "SEER meaning"]
            ]
        )
    )
    missing_total = s["unknown"] + s["blank_in_era"]
    add(
        f"Missing rate: {missing_total:,} of {n:,} rows ({fmt_pct(missing_total, n)}) carry a missing sentinel or "
        f"blank. Top-coded: {s['top_coded']:,} rows ({fmt_pct(s['top_coded'], n)}). Recorded day counts: "
        f"{s['numeric']:,} rows ({fmt_pct(s['numeric'], n)})."
    )
    add(
        f"Distribution of recorded days (denominator: the {s['numeric']:,} rows with a recorded day count; "
        f"top-coded rows are excluded because their exact value is unknown). Mean {fmt_float(s['mean'])} days, "
        f"minimum {fmt_float(s['min'], 0)}, maximum {fmt_float(s['max'], 0)}."
    )
    quantiles = ttt.quantiles.copy()
    quantiles["quantile"] = [f"{round(q * 100)}th percentile" for q in quantiles["quantile"]]
    add(md_table(quantiles))
    add(md_table(ttt.bins.rename(columns={"bin": "days", "pct": "% of recorded"})))
    add("By year of diagnosis (denominator for %: rows diagnosed that year):")
    by_year = ttt.by_year.copy()
    rows_per_year = by_year.sum(axis=1)
    by_year = by_year.rename(columns={"numeric": RECORDED_DAYS})
    by_year.insert(0, "rows", rows_per_year)
    for label in list(ttt_spec.missing) + list(ttt_spec.top_codes):
        if label in by_year.columns:
            by_year[f"% {label}"] = 100.0 * by_year[label] / rows_per_year.where(rows_per_year > 0)
    add(md_table(by_year, index=True))
    add(
        "What the sentinel tracks, descriptively: value type against the raw surgery code group and against the "
        "radiation recode (counts; no treatment definition is applied here)."
    )
    add(md_table(r.ttt_by_surgery, index=True))
    if r.ttt_by_radiation is not None:
        add(md_table(r.ttt_by_radiation, index=True))

    # 5
    add(f"## 5. {spec.reason_no_surgery_column}")
    add(f"Full distribution (denominator for %: all {n:,} rows):")
    reason = r.reason_frequency.copy()
    reason["classification"] = [_label_class(v, c.columns[spec.reason_no_surgery_column], blank) for v in reason["value"]]
    add(md_table(reason.rename(columns={"pct": "% of all rows"})))
    add("By year of diagnosis (each cell is a % of that year's rows):")
    add(md_table(r.reason_by_year, index=True))

    # 6
    seq = r.sequence
    add(f"## 6. {spec.sequence_column}")
    add(f"Full distribution (denominator for %: all {n:,} rows):")
    add(md_table(seq.frequency.rename(columns={"pct": "% of all rows"})))
    add(
        md_table(
            pd.DataFrame(
                [
                    ("Strict: only one primary ever reported", "; ".join(spec.first_primary_strict), seq.first_primary_strict, 100.0 * seq.first_primary_strict / n),
                    ("Inclusive: first of one or more primaries", "; ".join(spec.first_primary_inclusive), seq.first_primary_inclusive, 100.0 * seq.first_primary_inclusive / n),
                ],
                columns=["first primary definition", "labels", "rows", "% of all rows"],
            )
        )
    )
    fp = r.first_primary_ids
    add(
        f"Among the {fp.rows:,} inclusive first-primary rows there are {fp.unique_ids:,} distinct Patient IDs; "
        f"{fp.rows_sharing_an_id:,} rows share an ID. The choice between definitions is a Phase 2 protocol decision."
    )

    # 7
    add(f"## 7. {spec.stage_column} by year")
    add("Counts:")
    add(md_table(r.stage_counts, index=True))
    add("Column percentages (each cell is a % of that year's rows):")
    add(md_table(r.stage_pct, index=True))
    add(
        "Spread of each stage category across years (percentage points between the lowest and highest year; "
        "a narrow range is consistent with stable coding, though it cannot separate coding change from real change):"
    )
    add(md_table(_range_summary(r.stage_pct, "stage")))

    # Appendix A
    add("## Appendix A. Full frequency distributions")
    for position, column in enumerate(r.names, start=1):
        column_spec = c.columns[column]
        add(f"### A{position}. {column}")
        add(
            f"Kind: {column_spec.kind}. Role: {', '.join(_roles_of(c, column)) or 'unassigned'}. "
            f"Era: {_era_label(column_spec)}. Source for label classes: {column_spec.source}."
            + (f" Note: {column_spec.note}" if column_spec.note else "")
        )
        if column_spec.kind == "identifier":
            add(f"{rs.unique_ids:,} distinct values across {n:,} rows. Distribution not printed.")
            continue
        if column_spec.kind == "numeric_string":
            blocks.extend(_numeric_block(r, r.numeric_profiles[column], column_spec))
            add(f"Full value distribution: `{tables_rel}/frequency_{_slug(column)}.csv`.")
            continue
        table = r.frequencies[column].copy()
        table["classification"] = [_label_class(v, column_spec, blank) for v in table["value"]]
        add(f"Denominator for %: all {n:,} rows.")
        add(md_table(table.rename(columns={"pct": "% of all rows"}), digits=2))

    # Appendix B
    add("## Appendix B. Column roles")
    add(
        "Roles are copied from the brief, matched to the exact exported column names "
        "(for example the brief's `Chemotherapy recode` is exported as `Chemotherapy recode (yes, no/unk)`)."
    )
    role_rows = [(name, "; ".join(getattr(c.roles, name))) for name in c.roles.__dataclass_fields__]
    assigned = {col for _, cols in role_rows for col in cols.split("; ") if col}
    role_rows.append(("unassigned", "; ".join(col for col in r.names if col not in assigned)))
    add(md_table(pd.DataFrame(role_rows, columns=["role", "columns"])))

    return "\n\n".join(blocks) + "\n"
