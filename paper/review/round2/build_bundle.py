"""Build the round-2 input bundle for an ARS re-review under the archived legacy v1.0 contract.

The revision was made directly in the manuscript sources, so there are no revision patches or apply reports.
The roadmap is a mechanical transcription of the round-1 Editorial Decision Package (paper/review/round1/synthesis.md):
each item keeps its REV id, obligation class, revision item text (as verification criteria), source reviewers and
severity. Run from the project root after building paper/preprint.md and paper/supplement.md.
"""

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
R1 = ROOT / "paper/review/round1"
R2 = ROOT / "paper/review/round2"
CHECKER = Path.home() / ".claude/plugins/cache/academic-research-skills/academic-research-skills/3.19.0/scripts/legacy/check_re_review_synthesis_v1_0.py"
ROUND_ID = "seer-preprint-rereview-round2"
DATE = "2026-09-13"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(path: Path, version_label: str) -> dict:
    return {"present": True, "path_or_passport_ref": f"path:{path.relative_to(ROOT)}", "sha256": sha256_file(path),
            "version_label": version_label, "origin_date": DATE}


def severity(cell: str):
    text = re.sub(r"\[[^\]]*\]\s*", "", cell).strip().lower()
    if "split" in text:
        if "resolved major" in text or "resolved to r2" in text:
            return "major"
        # Severity left unresolved by the round-1 synthesis: record the highest severity any seat gave.
        # (Attempt 1 left these blank, which the legacy checker rejects; see aborted_attempt_1/.)
        found = re.findall(r"\b(critical|major|minor)\b", text)
        return min(found, key=("critical", "major", "minor").index) if found else None
    match = re.match(r"(critical|major|minor)\b", text)
    return match.group(1) if match else None


def main() -> None:
    R2.mkdir(parents=True, exist_ok=True)
    revised = R2 / "manuscript.md"
    revised.write_text((ROOT / "paper/preprint.md").read_text() + "\n\n" + (ROOT / "paper/supplement.md").read_text())
    findings = R2 / "round1_findings.md"
    findings.write_text("\n\n".join(
        f"# Round 1 reviewer card: {role}\n\n" + (R1 / f"{role}.phase2.md").read_text()
        for role in ("eic", "methodology", "domain", "perspective", "da")
    ))

    synthesis = (R1 / "synthesis.md").read_text()
    checklist = re.findall(r"^- \[ \] ([RS]\d+) — obligation `(\w+)`: (.+) \((REV-\d+)\)$", synthesis, re.M)
    section = synthesis.split("## Required Revisions (Must Fix)")[1].split("## Source-Traceability Checklist")[0]
    rows = {}
    for line in section.splitlines():
        match = re.match(r"^\| ([RS]\d+) \| ", line)
        if not match:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) != 10:
            sys.exit(f"{match.group(1)}: expected 10 table cells, found {len(cells)}")
        rows[match.group(1)] = cells

    items = []
    for ref, obligation, title, rev in checklist:
        cells = rows[ref]
        if cells[7] != obligation:
            sys.exit(f"{ref}: obligation {cells[7]!r} in table differs from checklist {obligation!r}")
        item = {"id": rev, "transport_ref": ref, "title": title.strip(), "priority": obligation,
                "verification_criteria": cells[1], "reviewer": cells[6], "evidence_anchor": cells[4]}
        sev = severity(cells[3])
        if sev is not None:
            item["severity"] = sev
        items.append(item)
    items.sort(key=lambda item: int(item["id"].split("-")[1]))
    must_fix_refs = [item["transport_ref"] for item in items if item["priority"] == "must_fix"]
    if must_fix_refs != [f"R{i}" for i in range(1, len(must_fix_refs) + 1)]:
        sys.exit(f"must_fix order is not R1..Rn: {must_fix_refs}")
    roadmap = {"schema": "revision-roadmap machine transcription (legacy v1.0 re-review input)",
               "source": "paper/review/round1/synthesis.md", "round_id": ROUND_ID, "items": items}
    roadmap_path = R2 / "roadmap.json"
    roadmap_path.write_text(json.dumps(roadmap, indent=2, ensure_ascii=False) + "\n")

    manifest = {"round_id": ROUND_ID, "cross_model_active": False, "artifacts": {
        "original_manuscript": entry(R1 / "manuscript.md", "round1-draft"),
        "revised_manuscript": entry(revised, "revision-1"),
        "revision_roadmap": entry(roadmap_path, "round1-roadmap"),
        "editorial_decision_letter": entry(R1 / "synthesis.md", "round1-decision"),
        "response_to_reviewers": entry(R2 / "response_to_reviewers.md", "revision-1-response"),
        "revision_patches": {"present": False},
        "apply_reports": {"present": False},
        "round1_findings": entry(findings, "round1-cards"),
        "round1_config_cards": entry(R1 / "00_field_analysis.md", "round1-field-analysis"),
    }}
    (R2 / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    spec = importlib.util.spec_from_file_location("legacy_checker", CHECKER)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker.validate_manifest(manifest)
    loaded = checker.load_roadmap(roadmap)
    blocks = checker.parse_letter_blocks(synthesis)
    counts = {p: sum(1 for i in loaded if i["priority"] == p) for p in ("must_fix", "should_fix", "consider")}
    print(f"items {len(loaded)} {counts}; letter blocks {len(blocks)}, ordinals sound: "
          f"{checker.letter_ordinals_sound(blocks, counts['must_fix'])}; blocks with acceptance text: "
          f"{sum(1 for _, t in blocks if t)}")
    print(f"input_manifest_hash {checker.canonical_hash(manifest)}")
    labels = {item["id"]: checker.normalize_reviewer_labels(item["reviewer"]) for item in loaded}
    failures = [rid for rid, (lab, failed) in labels.items() if failed]
    print(f"reviewer label parse failures: {failures}")


if __name__ == "__main__":
    main()
