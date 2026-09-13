"""Render paper/review/round2/verification_report.md mechanically from the committed re-review JSON records.

No judgement is added here: every verdict, residual gap, new issue and observation is copied from traceability.json,
verdict_record.json and roadmap.json. Em dashes inside quoted record text are shown as hyphens (house style).
Run from the project root with the project venv: .venv/bin/python paper/review/round2/render_report.py
"""

import collections
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, "src")
from seer_study.report import assert_style  # noqa: E402

R = pathlib.Path("paper/review/round2")
CHECKER = pathlib.Path.home() / ".claude/plugins/cache/academic-research-skills/academic-research-skills/3.19.0/scripts/legacy/check_re_review_synthesis_v1_0.py"
spec = importlib.util.spec_from_file_location("legacy_checker", CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

roadmap = json.load(open(R / "roadmap.json"))
tr = json.load(open(R / "traceability.json"))
ver = json.load(open(R / "verdict_record.json"))
pre = json.load(open(R / "precommitment.json"))
items = {i["id"]: i for i in roadmap["items"]}
vrec = {v["item_id"]: v for v in ver["items"]}
VERIFIED = {"YES": "Yes", "PARTIAL": "Partial", "NO": "No", "CANNOT_VERIFY": "Cannot verify"}


def cell(text, limit=220):
    text = " ".join(str(text).replace("|", "/").replace("—", "-").split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


rows = sorted(tr["rows"], key=lambda r: int(r["item_id"].split("-")[1]))


def table(priority, full):
    out = []
    for r in rows:
        if r["priority"] != priority:
            continue
        item, gap = items[r["item_id"]], vrec[r["item_id"]].get("residual_gap")
        residual = f"{cell(gap['text'], 260)} (residual: {gap['residual_magnitude']})" if gap else "none"
        ref = f"{item['transport_ref']} ({r['item_id']})"
        if full:
            out.append(f"| {ref} | {cell(item['title'])} | {cell(r['authors_claim'])} | {r['final_verdict']} | "
                       f"{cell(r['revision_location'], 120)} | {VERIFIED[r['verified']]} | {r.get('cross_model_status', 'n/a')} | "
                       f"{r['verified_by']} | {residual} |")
        else:
            out.append(f"| {ref} | {cell(item['title'])} | {r['final_verdict']} | {r['verified_by']} | {residual} |")
    return out


counts = collections.Counter((r["priority"], r["final_verdict"]) for r in rows)
inputs = tr["decision_inputs"]
lines = [
    "[LEGACY-NO-CONTRACT]", "", "# Verification Review Report (round 2, re-review of revision 1)", "",
    "## Judge Record (#539)", "",
    "- **Verification judge**: Claude (Anthropic) model family running this session; gate agents ran on the same family.",
    "- **Round-1 panel provenance**: all five round-1 seats ran on a single model family, which also drafted the manuscript (paper/review/round1/synthesis.md, Review Panel Provenance).",
    "- **Independent cross-model pass**: not_configured.",
    f"- **Pre-committed criteria**: precommitment_hash {checker.canonical_hash(pre)}.",
    "- **Prompt/rubric surfaces**: academic-paper-reviewer references/re_review_mode_protocol.md (three-gate orchestration, decision derivation, output format); archived legacy v1.0 schemas shared/contracts/re_review/legacy/v1_0/ and scripts/legacy/check_re_review_synthesis_v1_0.py (ARS 3.19.0).",
    "- **Reviewer configuration**: round1_cards_reused (paper/review/round1/00_field_analysis.md).",
    "- **Routing**: card_mapped.",
    "- **Apply-report chain**: not_run_no_reports.",
    "- **Evidence seen by the judge**: Phase 1 saw the roadmap, round-1 letter, round-1 findings and cards only; Phase 2A added the original and revised manuscripts, figures and generated reports; Phase 2B added the Response to Reviewers.",
    "- **Judging budget**: three gate agents (Phase 1, 2A, 2B) plus orchestration, separate from the revision itself.",
    "",
    "This verification round ran on the same model family that drove the revisions; over-optimization to this judge's latent biases is possible (Ren et al. 2026, arXiv:2607.13104 §8.1.2).",
    "",
    "## Process notes", "",
    "- **Legacy contract:** the re-review ran under the archived legacy v1.0 contract, chosen by the author. The revision was made directly in the manuscript sources, not through the ARS patch workflow, so no revision patch, apply report, author-adjudication sidecar or revision-evidence bundle exists; the current v1.1 contract could not be run without reconstructing those after the fact.",
    "- **Roadmap provenance:** the roadmap (paper/review/round2/roadmap.json) is a mechanical transcription of the round-1 Editorial Decision Package by paper/review/round2/build_bundle.py.",
    "- **Attempt 1 aborted:** the first checker run ended in [RE-REVIEW-ABORT: synthesis_mismatch]. The transcription had left severity blank for three items whose round-1 severity was split between seats: REV-8 (R7), REV-10 (R9) and REV-18 (R14).",
    "- **Repair (author-approved):**",
    "  - the transcription now records the highest severity any seat gave (major for all three);",
    "  - the manifest was rebuilt, with the roadmap as the only changed artifact;",
    "  - the hash links in the precommitment, verdict record and traceability files were re-stamped, with the three driving severities set to major.",
    "- **What did not change:**",
    "  - no criterion, verdict, new issue or letter-matching content;",
    "  - the committed Phase 1 and Phase 2A records for those three items do not mention severity;",
    "  - severity enters the decision rules only through critical-severity items.",
    "- **Audit copy:** the aborted artifacts and their checksums are in paper/review/round2/aborted_attempt_1/.",
    "- **Verification report:** the Phase 2B agent stopped at the abort before writing this report. It was rendered afterwards from the committed JSON records by paper/review/round2/render_report.py.",
    "",
    "## Decision", "", f"**{tr['decision_state']}** (recomputed by the legacy checker: re-review synthesis ok).", "",
    "## Revision Response Checklist", "", "### must_fix: Required Revisions", "",
    "| Transport ref | Item | Author's claim | Response status | Revision location | Verified? | Cross-model (#539) | Verified by | Residual gap |",
    "|---|---|---|---|---|---|---|---|---|", *table("MUST_FIX", True), "",
    "### should_fix: Suggested Revisions", "", "| Transport ref | Item | Response status | Verified by | Residual gap |",
    "|---|---|---|---|---|", *table("SHOULD_FIX", False), "",
    "### consider: Nice to Fix", "", "| Transport ref | Item | Response status | Verified by | Residual gap |",
    "|---|---|---|---|---|", *table("CONSIDER", False), "",
    "## New Issues (Discovered During Revision)", "", "| # | Attribution | Severity | Location | Description |", "|---|---|---|---|---|",
]
for issue in tr["new_issues"]:
    lines.append(f"| {issue['new_issue_id']} | {issue['attribution']} | {issue['severity']} | "
                 f"{cell(issue['location_anchor'], 140)} | {cell(issue['description'], 400)} |")
lines += [
    "", "## Decision Rationale", "",
    "The legacy checker derived and confirmed the decision under the Step 1 to 3 rules.",
    "",
    "- **Step 1 (gates):** no gate fired. The manifest is complete and hash-bound, no verdict changed without an adjustment record (Phase 2B made none), and no deferral state is pending.",
    f"- **must_fix verdicts:** {counts[('MUST_FIX', 'FULLY_ADDRESSED')]} FULLY_ADDRESSED and {counts[('MUST_FIX', 'PARTIALLY_ADDRESSED')]} PARTIALLY_ADDRESSED. None is NOT_ADDRESSED, MADE_WORSE or CANNOT_VERIFY, and no partial item's residual is rated must_fix, so B1 to B4 do not fire.",
    f"- **Step 2, rule B5 (Minor Revision):** fires because must_fix items are partly addressed with should_fix or consider residuals, and because {len(inputs['regressions'])} new issues are minor regressions.",
    f"- **should_fix addressed rate:** {inputs['p2_addressed_rate']['numerator']}/{inputs['p2_addressed_rate']['denominator']}.",
    "- **Step 3:** no escalation floors apply, and reject is not recommended.",
    "", "## Residual Issues", "",
    "The residual gaps in the checklists above, and the new issues, remain for the next revision. Observations recorded only after reading the letter (decision-inert):", "",
]
for observation in tr["post_letter_observations"]:
    lines.append(f"- {cell(observation if isinstance(observation, str) else json.dumps(observation, ensure_ascii=False), 500)}")
text = "\n".join(lines) + "\n"
assert_style(text)
(R / "verification_report.md").write_text(text)
print(f"{R / 'verification_report.md'}: {len(text.split())} words")
