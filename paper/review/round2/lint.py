"""Lint the round-2 legacy re-review gate outputs: schema validation plus the legacy checker's binding rules.

Usage (from the project root, with the ARS scratch venv python):
    python paper/review/round2/lint.py phase1     # precommitment.json
    python paper/review/round2/lint.py phase2a    # verdict_record.json
    python paper/review/round2/lint.py phase2b    # full legacy checker over all artifacts
Exit 0 on pass, 1 on any failure.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
R1 = ROOT / "paper/review/round1"
R2 = ROOT / "paper/review/round2"
CHECKER = Path.home() / ".claude/plugins/cache/academic-research-skills/academic-research-skills/3.19.0/scripts/legacy/check_re_review_synthesis_v1_0.py"

spec = importlib.util.spec_from_file_location("legacy_checker", CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def load(path: Path):
    return json.loads(path.read_text())


def schema(validate, artifact, failures):
    try:
        validate(artifact)
    except Exception as exc:  # the checker raises its own error classes on schema failure
        failures.append(f"schema: {exc}")


def phase1() -> list[str]:
    failures = []
    manifest, roadmap = load(R2 / "manifest.json"), load(R2 / "roadmap.json")
    pre = load(R2 / "precommitment.json")
    schema(checker.validate_precommitment, pre, failures)
    items = checker.load_roadmap(roadmap)
    by_id = {item["id"]: item for item in items}
    must_fix = [item["id"] for item in items if item["priority"] == "must_fix"]
    blocks = dict(checker.parse_letter_blocks((R1 / "synthesis.md").read_text()))
    if pre.get("round_id") != manifest["round_id"]:
        failures.append("round_id differs from manifest")
    if pre.get("input_manifest_hash") != checker.canonical_hash(manifest):
        failures.append("input_manifest_hash does not equal the canonical manifest hash")
    records = {rec["item_id"]: rec for rec in pre.get("items", [])}
    expected = {item["id"] for item in items if item["priority"] in ("must_fix", "should_fix")}
    if set(records) != expected:
        failures.append(f"coverage: missing {sorted(expected - set(records))}, extra {sorted(set(records) - expected)}")
    for item_id, rec in records.items():
        item = by_id.get(item_id)
        if item is None:
            continue
        crit = rec.get("inherited_criterion", {})
        if rec.get("priority") != item["priority"]:
            failures.append(f"{item_id}: priority mismatch")
        if crit.get("roadmap_text") != item["verification_criteria"]:
            failures.append(f"{item_id}: roadmap_text is not a verbatim copy of verification_criteria")
        if rec.get("source_reviewer") != item["reviewer"]:
            failures.append(f"{item_id}: source_reviewer is not a verbatim copy of reviewer")
        labels, _ = checker.normalize_reviewer_labels(item["reviewer"])
        if rec.get("source_reviewer_labels") != labels:
            failures.append(f"{item_id}: source_reviewer_labels should be {labels}")
        if item["priority"] == "must_fix":
            ref = f"R{must_fix.index(item_id) + 1}"
            if crit.get("letter_item_ref") != ref:
                failures.append(f"{item_id}: letter_item_ref should be {ref}")
            if crit.get("letter_text") != blocks.get(ref):
                failures.append(f"{item_id}: letter_text is not a verbatim copy of the letter's {ref} Acceptance criteria")
            op = rec.get("operationalization", {})
            for key in ("partially_addressed", "made_worse_discriminator"):
                if not op.get(key):
                    failures.append(f"{item_id}: must_fix operationalization needs {key}")
        elif "letter_text" in crit or "letter_item_ref" in crit:
            failures.append(f"{item_id}: letter fields are only for must_fix items")
    return failures


def phase2a() -> list[str]:
    failures = []
    manifest, roadmap = load(R2 / "manifest.json"), load(R2 / "roadmap.json")
    pre, verdict = load(R2 / "precommitment.json"), load(R2 / "verdict_record.json")
    schema(checker.validate_verdict_record, verdict, failures)
    items = checker.load_roadmap(roadmap)
    by_id = {item["id"]: item for item in items}
    if verdict.get("round_id") != manifest["round_id"]:
        failures.append("round_id differs from manifest")
    if verdict.get("precommitment_hash") != checker.canonical_hash(pre):
        failures.append("precommitment_hash does not equal the canonical precommitment hash")
    records = {rec["item_id"]: rec for rec in verdict.get("items", [])}
    if set(records) != set(by_id):
        failures.append(f"coverage: missing {sorted(set(by_id) - set(records))}, extra {sorted(set(records) - set(by_id))}")
    for item_id, rec in records.items():
        item = by_id.get(item_id)
        if item is None:
            continue
        applied = rec.get("applied_criterion")
        if item["priority"] == "consider" and applied != "not_precommitted":
            failures.append(f"{item_id}: consider items carry applied_criterion not_precommitted")
        if item["priority"] != "consider" and applied == "not_precommitted":
            failures.append(f"{item_id}: not_precommitted is only for consider items")
        if rec.get("verdict") == "PARTIALLY_ADDRESSED" and "residual_gap" not in rec:
            failures.append(f"{item_id}: PARTIALLY_ADDRESSED needs residual_gap")
    return failures


def phase2b() -> list[str]:
    python = sys.executable
    command = [
        python, str(CHECKER),
        "--manifest", str(R2 / "manifest.json"),
        "--precommitment", str(R2 / "precommitment.json"),
        "--verdict-record", str(R2 / "verdict_record.json"),
        "--traceability", str(R2 / "traceability.json"),
        "--roadmap", str(R2 / "roadmap.json"),
        "--letter", str(R1 / "synthesis.md"),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    return [] if result.returncode == 0 else [f"legacy checker exit {result.returncode}"]


if __name__ == "__main__":
    gate = sys.argv[1] if len(sys.argv) > 1 else ""
    functions = {"phase1": phase1, "phase2a": phase2a, "phase2b": phase2b}
    if gate not in functions:
        sys.exit(__doc__)
    problems = functions[gate]()
    for problem in problems:
        print(f"FAIL {problem}")
    print("PASS" if not problems else f"{len(problems)} failure(s)")
    sys.exit(0 if not problems else 1)
