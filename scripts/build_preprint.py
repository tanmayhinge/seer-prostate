"""Assemble paper/preprint.md and paper/supplement.md from paper/src/, with tables copied from the generated reports.

Checks the writing style (no em dashes or banned words) and audits numbers: every number in the text that appears in
none of the source documents (reports, protocol, configuration, requirements, figure captions) is written to
paper/number_audit.txt for a person to check by hand.
"""

import argparse
from pathlib import Path

from seer_study.manuscript import render_includes, unsupported_numbers
from seer_study.report import assert_style

DOCUMENTS = ("preprint.md", "supplement.md")
SOURCE_GLOBS = ("reports/*.md", "PROTOCOL.md", "config/*.yaml", "requirements.txt", "paper/figures/captions.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--src-dir", type=Path, default=Path("paper/src"))
    parser.add_argument("--out-dir", type=Path, default=Path("paper"))
    args = parser.parse_args()

    sources = sorted({path for pattern in SOURCE_GLOBS for path in args.root.glob(pattern)})
    source_texts = [path.read_text() for path in sources]
    audit = [f"Sources: {', '.join(str(p) for p in sources)}", ""]
    for name in DOCUMENTS:
        src = args.src_dir / name
        if not src.exists():
            continue
        text = render_includes(src.read_text(), args.root)
        assert_style(text)
        (args.out_dir / name).write_text(text)
        body = text.split("\n## References\n")[0]  # reference details are checked against PubMed records, not reports
        missing = unsupported_numbers(body, source_texts)
        audit.append(f"{name}: {len(missing)} number(s) not found in any source")
        audit += [f"  {token}" for token in missing]
        print(f"{args.out_dir / name}: {len(text.split()):,} words, {len(missing)} unsupported number(s)")
    (args.out_dir / "number_audit.txt").write_text("\n".join(audit) + "\n")


if __name__ == "__main__":
    main()
