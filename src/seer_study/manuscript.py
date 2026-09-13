"""Manuscript assembly: LaTeX tables built from generated reports, and checks on the manuscript text.

Tables enter the paper only by being generated from the reports, so they cannot drift from them. The number audit
lists every number in the running text that appears in none of the source documents, for a person to check by hand.
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


LATEX_SPECIAL = {
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}", "\\": r"\textbackslash{}",
}


def latex_escape(text: str) -> str:
    """Escape the characters LaTeX treats as special."""
    return "".join(LATEX_SPECIAL.get(char, char) for char in text)


def markdown_rows(table_md: str) -> tuple[list[str], list[list[str]]]:
    """Header and body rows of a markdown table; the separator row is dropped and ``\\|`` becomes ``|``."""
    parsed = []
    for line in table_md.strip().splitlines():
        cells = [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        parsed.append(cells)
    return parsed[0], parsed[1:]


def latex_tabular(header: list[str], rows: list[list[str]], column_spec: str, escape: bool = True) -> str:
    """A booktabs tabular; cells are escaped unless ``escape`` is False (cells already written in LaTeX)."""
    fix = latex_escape if escape else (lambda cell: cell)
    line = lambda cells: " & ".join(fix(cell) for cell in cells) + " \\\\"  # noqa: E731
    return "\n".join(
        [f"\\begin{{tabular}}{{{column_spec}}}", "\\toprule", line(header), "\\midrule"]
        + [line(row) for row in rows]
        + ["\\bottomrule", "\\end{tabular}"]
    )


def tex_prose(tex: str) -> str:
    """Running text of a LaTeX document, for word counts and number audits.

    Comments, floats (tables and figures, whose content comes from the reports), the bibliography, citations,
    cross-references and URLs are removed; formatting commands are dropped but their text is kept.
    """
    text = re.sub(r"(?<!\\)%.*", "", tex)
    text = re.sub(r"\\begin\{(thebibliography|figure|table)(\*?)\}.*?\\end\{\1\2\}", " ", text, flags=re.S)
    text = re.sub(r"\\(?:cite[pt]?|label|ref|input|includegraphics|url|href)(?:\[[^\]]*\])*\{[^}]*\}", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\([%&$#_{}])", r"\1", text)
    text = text.replace("~", " ").replace("{", "").replace("}", "").replace("\\\\", " ")
    return re.sub(r"[ \t]+", " ", text)


def cite_order(tex: str) -> list[str]:
    """Citation keys in order of first use."""
    keys: list[str] = []
    for group in re.findall(r"\\cite[pt]?\{([^}]*)\}", tex):
        keys += [key.strip() for key in group.split(",") if key.strip() not in keys]
    return keys


def bibitem_order(tex: str) -> list[str]:
    """Bibliography keys in the order they are listed."""
    return re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", tex)


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
