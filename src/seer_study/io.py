"""Reading the raw SEER*Stat case listing without letting pandas reinterpret it."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from pathlib import Path

import pandas as pd

from seer_study.config import DataSpec

VARIABLE_LINE = re.compile(r"^Var(\d+)Name=(.*)$")
OPTION_LINE = re.compile(r"^([^=\[\]]+)=(.*)$")
CHUNK_BYTES = 1 << 20


class FrameIntegrityError(ValueError):
    """Raised when the export does not match its dictionary or the configured expectations."""


def read_dictionary(path: str | Path) -> list[str]:
    """Column names from a SEER*Stat .dic file, in VarN order."""
    found: dict[int, str] = {}
    for line in Path(path).read_text().splitlines():
        match = VARIABLE_LINE.match(line.strip())
        if not match:
            continue
        index = int(match.group(1))
        if index in found:
            raise FrameIntegrityError(f"{path}: Var{index}Name appears more than once")
        found[index] = match.group(2)
    if not found:
        raise FrameIntegrityError(f"{path}: no VarNName entries")
    gaps = [f"Var{i}" for i in range(1, max(found) + 1) if i not in found]
    if gaps:
        raise FrameIntegrityError(f"{path}: dictionary has no entry for {', '.join(gaps)}")
    return [found[i] for i in range(1, max(found) + 1)]


def read_dictionary_options(path: str | Path) -> dict[str, str]:
    """The key=value export options recorded in a .dic file, excluding the variable list."""
    options: dict[str, str] = {}
    section = ""
    for line in Path(path).read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1]
            continue
        if section == "Variables":
            continue
        match = OPTION_LINE.match(stripped)
        if match:
            options[match.group(1).strip()] = match.group(2).strip()
    return options


def check_field_counts(path: str | Path, expected: int, report_limit: int = 5) -> None:
    """Raise if any line does not split into exactly ``expected`` tab-separated fields."""
    bad = []
    with open(path, "rb") as handle:
        for line_number, line in enumerate(handle, start=1):
            fields_found = line.count(b"\t") + 1
            if fields_found != expected:
                bad.append(f"line {line_number} has {fields_found}")
                if len(bad) >= report_limit:
                    break
    if bad:
        raise FrameIntegrityError(f"{path}: expected {expected} fields per line; {'; '.join(bad)}")


def read_export(path: str | Path, names: list[str]) -> pd.DataFrame:
    """Read the tab-delimited export with every value kept as the exported text."""
    path = Path(path)
    check_field_counts(path, len(names))
    try:
        frame = pd.read_csv(
            path,
            sep="\t",
            header=None,
            names=names,
            dtype=str,
            keep_default_na=False,
            na_filter=False,
            quoting=csv.QUOTE_NONE,
            encoding="utf-8",
            engine="c",
        )
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise FrameIntegrityError(f"{path}: could not be parsed: {exc}") from exc
    if frame.shape[1] != len(names):
        raise FrameIntegrityError(f"{path}: parsed {frame.shape[1]} columns, dictionary has {len(names)}")
    if frame.isna().to_numpy().any():
        raise FrameIntegrityError(f"{path}: parser produced missing cells, so some rows are short")
    return frame


def validate_frame(frame: pd.DataFrame, data: DataSpec) -> None:
    """Check row count, column count and the year range against the configuration."""
    if len(frame) != data.expected_rows:
        raise FrameIntegrityError(f"expected {data.expected_rows:,} rows, found {len(frame):,}")
    if frame.shape[1] != data.expected_columns:
        raise FrameIntegrityError(f"expected {data.expected_columns} columns, found {frame.shape[1]}")
    observed = set(frame[data.year_column].unique())
    outside = sorted(observed - set(data.years))
    if outside:
        raise FrameIntegrityError(f"year values outside {data.year_min}-{data.year_max}: {outside}")


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zip_member_sha256(archive: str | Path, member: str) -> str:
    digest = hashlib.sha256()
    with zipfile.ZipFile(archive) as zf, zf.open(member) as handle:
        for chunk in iter(lambda: handle.read(CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()
