"""Typed study configuration loaded from YAML.

Every constant the analysis depends on lives in config/study.yaml. The loader
builds frozen dataclasses and rejects unknown keys, missing keys and wrong
types, so a typo in the YAML fails loudly instead of silently using a default.
"""

from __future__ import annotations

import dataclasses
import types
import typing
from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from pathlib import Path

import yaml

COLUMN_KINDS = ("categorical", "numeric_string", "identifier")


class ConfigError(ValueError):
    """Raised when the study configuration is malformed or inconsistent."""


@dataclass(frozen=True)
class Era:
    first_year: int
    last_year: int | None

    def __post_init__(self) -> None:
        if self.last_year is not None and self.last_year < self.first_year:
            raise ConfigError(f"era last_year {self.last_year} precedes first_year {self.first_year}")

    def label(self) -> str:
        return f"{self.first_year}+" if self.last_year is None else f"{self.first_year}-{self.last_year}"


@dataclass(frozen=True)
class ColumnSpec:
    kind: str
    source: str
    missing: tuple[str, ...] = ()
    not_applicable: tuple[str, ...] = ()
    top_codes: tuple[str, ...] = ()
    era: Era | None = None
    unit: str = ""
    note: str = ""
    label_notes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in COLUMN_KINDS:
            raise ConfigError(f"column kind {self.kind!r} is not one of {COLUMN_KINDS}")


@dataclass(frozen=True)
class Paths:
    export: Path
    dictionary: Path
    archive: Path
    archive_member: str
    selection_note: Path
    session_file: Path
    reports_dir: Path
    tables_dir: Path


@dataclass(frozen=True)
class DataSpec:
    expected_columns: int
    expected_rows: int
    id_column: str
    year_column: str
    year_min: int
    year_max: int
    blank_label: str

    @property
    def years(self) -> tuple[str, ...]:
        return tuple(str(year) for year in range(self.year_min, self.year_max + 1))


@dataclass(frozen=True)
class Roles:
    clinical: tuple[str, ...]
    nonclinical: tuple[str, ...]
    treatment: tuple[str, ...]
    outcome: tuple[str, ...]
    cohort: tuple[str, ...]
    secondary: tuple[str, ...]


@dataclass(frozen=True)
class InventorySpec:
    quantiles: tuple[float, ...]
    time_to_treatment_bin_edges: tuple[int, ...]
    time_to_treatment_column: str
    sequence_column: str
    first_primary_strict: tuple[str, ...]
    first_primary_inclusive: tuple[str, ...]
    reason_no_surgery_column: str
    stage_column: str
    clinical_grade_columns: tuple[str, ...]
    pathological_grade_columns: tuple[str, ...]
    psa_columns: tuple[str, ...]
    surgery_columns: tuple[str, ...]
    surgery_none_codes: tuple[str, ...]
    surgery_unknown_codes: tuple[str, ...]
    absent_variable_keywords: dict[str, tuple[str, ...]]
    available_not_exported: dict[str, str]
    age_column: str | None
    age_labels_below_18: tuple[str, ...]
    age_labels_straddling_18: tuple[str, ...]
    radiation_column: str | None
    expected_selection_variables: tuple[str, ...]
    session_file_extensions: tuple[str, ...]
    suspect_label_patterns: tuple[str, ...]


@dataclass(frozen=True)
class StudyConfig:
    seed: int
    paths: Paths
    data: DataSpec
    roles: Roles
    columns: dict[str, ColumnSpec]
    inventory: InventorySpec


def load_config(path: str | Path, root: str | Path | None = None) -> StudyConfig:
    """Load and type-check the YAML configuration.

    Relative paths inside the file resolve against ``root``, which defaults to
    the parent of the directory holding the config file (the project root).
    """
    path = Path(path)
    root = Path(root) if root is not None else path.resolve().parent.parent
    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ConfigError(f"{path}: invalid YAML: {exc}") from exc
    config = _build(StudyConfig, raw, "")
    _check_label_sets(config)
    return dataclasses.replace(config, paths=_resolve_paths(config.paths, root))


def referenced_columns(config: StudyConfig) -> list[tuple[str, str]]:
    """Every (config location, column name) pair the configuration refers to."""
    refs = [("data.id_column", config.data.id_column), ("data.year_column", config.data.year_column)]
    for role in fields(config.roles):
        refs += [(f"roles.{role.name}", c) for c in getattr(config.roles, role.name)]
    for item in fields(config.inventory):
        value = getattr(config.inventory, item.name)
        if item.name.endswith("_column") and value is not None:
            refs.append((f"inventory.{item.name}", value))
        elif item.name.endswith("_columns"):
            refs += [(f"inventory.{item.name}", c) for c in value]
    return refs


def load_typed_yaml(path: str | Path, cls: type):
    """Load a YAML file into any frozen config dataclass with the same strict checks as load_config."""
    path = Path(path)
    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ConfigError(f"{path}: invalid YAML: {exc}") from exc
    return _build(cls, raw, "")


def validate_config(config: StudyConfig, names: list[str]) -> None:
    """Check the configuration against the column names in the SEER dictionary."""
    known = set(names)
    problems = []
    if len(names) != config.data.expected_columns:
        problems.append(f"dictionary has {len(names)} columns, config expects {config.data.expected_columns}")
    for where, column in referenced_columns(config):
        if column not in known:
            problems.append(f"{where} names {column!r}, which is not in the dictionary")
    for column in config.columns:
        if column not in known:
            problems.append(f"columns has a spec for {column!r}, which is not in the dictionary")
    for column in names:
        if column not in config.columns:
            problems.append(f"dictionary column {column!r} has no column spec")
    if problems:
        raise ConfigError("; ".join(problems))


def _check_label_sets(config: StudyConfig) -> None:
    for name, spec in config.columns.items():
        seen: dict[str, str] = {}
        for group in ("missing", "not_applicable", "top_codes"):
            for label in getattr(spec, group):
                if label == config.data.blank_label:
                    raise ConfigError(f"column {name!r}: blank label is handled globally, remove it from {group}")
                if label in seen:
                    raise ConfigError(f"column {name!r}: label {label!r} listed under both {seen[label]} and {group}")
                seen[label] = group


def _resolve_paths(paths: Paths, root: Path) -> Paths:
    updates = {}
    for item in fields(paths):
        value = getattr(paths, item.name)
        if isinstance(value, Path) and not value.is_absolute():
            updates[item.name] = root / value
    return dataclasses.replace(paths, **updates)


def _build(cls: type, raw: object, where: str):
    if not isinstance(raw, dict):
        raise ConfigError(f"{where or 'config'}: expected a mapping, got {type(raw).__name__}")
    hints = typing.get_type_hints(cls)
    allowed = {item.name for item in fields(cls)}
    unknown = sorted(str(key) for key in raw if key not in allowed)
    if unknown:
        raise ConfigError(f"{where or 'config'}: unknown key(s) {unknown}")
    kwargs = {}
    for item in fields(cls):
        location = f"{where}.{item.name}" if where else item.name
        if item.name not in raw:
            if item.default is not MISSING or item.default_factory is not MISSING:
                continue
            raise ConfigError(f"{location}: required key missing")
        kwargs[item.name] = _coerce(raw[item.name], hints[item.name], location)
    return cls(**kwargs)


def _coerce(value: object, annotation: object, where: str):
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    if origin in (types.UnionType, typing.Union):
        if value is None and type(None) in args:
            return None
        (inner,) = [arg for arg in args if arg is not type(None)]
        return _coerce(value, inner, where)
    if value is None:
        raise ConfigError(f"{where}: value is required, got null")
    if is_dataclass(annotation):
        return _build(annotation, value, where)
    if origin is tuple:
        if not isinstance(value, list):
            raise ConfigError(f"{where}: expected a list, got {type(value).__name__}")
        return tuple(_coerce(item, args[0], f"{where}[{i}]") for i, item in enumerate(value))
    if origin is dict:
        if not isinstance(value, dict):
            raise ConfigError(f"{where}: expected a mapping, got {type(value).__name__}")
        return {
            _coerce(key, args[0], f"{where} key"): _coerce(item, args[1], f"{where}.{key}")
            for key, item in value.items()
        }
    if annotation is bool:
        if type(value) is not bool:
            raise ConfigError(f"{where}: expected bool, got {type(value).__name__}")
        return value
    if annotation is int:
        if type(value) is not int:
            raise ConfigError(f"{where}: expected int, got {type(value).__name__}")
        return value
    if annotation is float:
        if type(value) not in (int, float):
            raise ConfigError(f"{where}: expected float, got {type(value).__name__}")
        return float(value)
    if annotation is str:
        if type(value) is not str:
            raise ConfigError(f"{where}: expected str, got {type(value).__name__}")
        return value
    if annotation is Path:
        if type(value) is not str:
            raise ConfigError(f"{where}: expected a path string, got {type(value).__name__}")
        return Path(value)
    raise ConfigError(f"{where}: unsupported annotation {annotation!r}")
