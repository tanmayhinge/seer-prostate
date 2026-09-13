"""Render paper/preprint.md and paper/supplement.md to PDF via styled HTML and headless Chrome.

Requires the `markdown` package (not an analysis dependency) and Google Chrome. Run from the project root after
scripts/build_preprint.py. Writes paper/preprint.html, paper/preprint.pdf, paper/supplement.html and paper/supplement.pdf.
"""

import argparse
import subprocess
from pathlib import Path

import markdown

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BREAK_BEFORE = ("Tables", "Figures", "References", "Supplementary figures", "Supplementary Table S45. STROBE and RECORD checklist")

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: "Charter", "Georgia", "Times New Roman", serif; font-size: 10pt; line-height: 1.45; color: #111; }
h1 { font-size: 16pt; line-height: 1.25; margin: 0 0 10pt 0; }
h2 { font-size: 12.5pt; margin: 16pt 0 6pt 0; border-bottom: 0.6pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 10.5pt; margin: 12pt 0 4pt 0; }
p { margin: 0 0 6pt 0; text-align: left; overflow-wrap: anywhere; }
ul, ol { margin: 0 0 6pt 16pt; padding: 0; }
li { margin: 0 0 2pt 0; }
table { border-collapse: collapse; width: 100%; font-size: 6.6pt; line-height: 1.25; margin: 4pt 0 10pt 0; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: 0.4pt solid #aaa; padding: 1.5pt 3pt; vertical-align: top; text-align: left; word-break: break-word; }
th { background: #eee; }
img { max-width: 100%; display: block; margin: 8pt auto 4pt auto; page-break-inside: avoid; }
code { font-size: 8.5pt; }
.break { page-break-before: always; }
"""


def render(md_path: Path) -> Path:
    html_body = markdown.markdown(md_path.read_text(), extensions=["tables", "sane_lists"])
    for heading in BREAK_BEFORE:
        html_body = html_body.replace(f"<h2>{heading}</h2>", f'<h2 class="break">{heading}</h2>')
    title = md_path.stem.capitalize()
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{html_body}</body></html>"
    html_path = md_path.with_suffix(".html")
    html_path.write_text(html)
    pdf_path = md_path.with_suffix(".pdf")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf-no-header",
         f"--print-to-pdf={pdf_path.resolve()}", html_path.resolve().as_uri()],
        check=True, capture_output=True, timeout=240,
    )
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="*", type=Path, default=[Path("paper/preprint.md"), Path("paper/supplement.md")])
    args = parser.parse_args()
    for document in args.documents:
        print(render(document))


if __name__ == "__main__":
    main()
