"""Manuscript assembly: tables copied from generated reports, and an audit of numbers in the text.

Tables enter the preprint only through include directives, so they cannot drift from the reports. The number audit
lists every number in the text that appears in none of the source documents, for a person to check by hand.
"""

from __future__ import annotations

import re
from pathlib import Path

INCLUDE = re.compile(r"<!-- table: (.+?) \| (.+?) -->")
REFERENCE_PATTERNS = (r"PMID:?\s*\d+", r"PMC\d+", r"doi:?\s*\S+", r"https?://\S+")
NUMBER = re.compile(r"(?<![\w.,])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(?!\w)")


def extract_table(markdown: str, heading: str) -> str:
    """The first markdown table after the line starting with ``heading``, before the next heading."""
    lines = markdown.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(heading)]
    if not starts:
        raise ValueError(f"heading {heading!r} not found")
    table: list[str] = []
    for line in lines[starts[0] + 1:]:
        if line.startswith("|"):
            table.append(line)
        elif table:
            break
        elif line.startswith("#"):
            break
    if not table:
        raise ValueError(f"no table under heading {heading!r}")
    return "\n".join(table)


def render_includes(text: str, root: str | Path) -> str:
    """Replace each ``<!-- table: path | heading -->`` directive with that table from the file under ``root``."""
    root = Path(root)
    return INCLUDE.sub(lambda m: extract_table((root / m.group(1).strip()).read_text(), m.group(2).strip()), text)


def numbers_in(text: str) -> set[str]:
    """Numbers written in running text, without sign; identifiers such as PMIDs, DOIs and URLs are ignored."""
    for pattern in REFERENCE_PATTERNS:
        text = re.sub(pattern, " ", text)
    return {whole + (decimals or "") for whole, decimals in NUMBER.findall(text)}


VERSION_LINE = re.compile(r"^Version (\d+(?:\.\d+)*),", re.M)


def protocol_version(text: str) -> str | None:
    """The protocol version from its 'Version X.Y, dated ...' line, or None if the line is absent."""
    match = VERSION_LINE.search(text)
    return match.group(1) if match else None


def _value(token: str) -> float:
    return float(token.replace(",", ""))


def unsupported_numbers(text: str, sources: list[str], min_integer: int = 100) -> list[str]:
    """Numbers in ``text`` found in no source; integers below ``min_integer`` (step numbers, counts) are skipped."""
    known = {_value(token) for source in sources for token in numbers_in(source)}
    missing = [
        token for token in numbers_in(text)
        if _value(token) not in known and not ("." not in token and _value(token) < min_integer)
    ]
    return sorted(missing, key=lambda token: (_value(token), token))
