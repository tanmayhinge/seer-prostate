# Editorial Decision Package

## Manuscript Information
- **Title**: Waiting for prostate cancer treatment: how much is clinical need? A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022
- **Manuscript ID**: not assigned (internal ARS review, round 1)
- **Intended outlet**: medRxiv preprint server (screens, does not peer review). No author-confirmed target venue.
- **Decision Date**: 2026-09-13
- **Review Round**: Round 1
- **Contract**: reviewer/reviewer_full/v2 (panel_size 5)

## Review Panel Provenance (#540)

All five reviewer personas ran on a single model family (the Claude model family that runs this session). Persona diversity is not model diversity, so blind spots may be correlated across reviewers (Ren et al. 2026, arXiv:2607.13104 §5.2). Cross-model verification was not active (ARS_CROSS_MODEL unset). The same model family also drafted the manuscript, so the panel may share errors and blind spots with the drafting process as well as with each other.

- **Criteria binding**: unavailable (`criteria_binding_unavailable`). No author-confirmed target venue. All five cards disclose this, and this package makes no venue-alignment claim.
- **Seat conformance**: all five Phase 2 seats ran their own conformance checker before sending and fixed only structural grammar. All five passed `check_phase_conformance.py` and `check_panel_synthesis.py --layer1-only`. No seat was dropped.
- **Cross-model decision check (Step 4b)**: not run, because ARS_CROSS_MODEL is unset.

---

# Part 1: Editorial Decision Letter

Dear Author,

Thank you for preparing the manuscript named above for posting on medRxiv. It was reviewed by five independent reviewer personas under a pre-registered sprint contract. The panel was a Journal-Fit Reviewer (EIC), Reviewer 1 (R1, methodology), Reviewer 2 (R2, domain), Reviewer 3 (R3, cross-disciplinary perspective) and a Devil's Advocate (DA). No journal is configured, so the decision below is a readiness decision against field-general standards for registry-based health services research. It is not a journal decision.

Naming note: in this package, R1, R2 and R3 in prose and in the Source columns name reviewer seats. In the first column of the roadmap tables, `R<n>` and `S<n>` are transport references for roadmap rows. They are not seats and not ranks.

## Decision

### Major Revision

This decision is mechanical under the sprint contract (editorial_decision_standards.md §0). Condition F2 ("any mandatory dimension scores 'block'", severity 90) fired on D1, D2 and D3, and it takes precedence over the other fired conditions, F3 and F5. No seat declared a fatal block, so F1 (reject) did not fire. The DA's CRITICAL table is empty.

### Mechanical audit (sprint contract Steps 1 to 3)

**Step 1: role-scoped scoring matrix.** Only eligible seats count. Ineligible `not_assessed` values are excluded.

| Dimension | Priority | Eligible seats | Assessed scores | Worst (verdict) |
|---|---|---|---|---|
| D1 methodology_rigor | mandatory | methodology | R1: block (repairable) | block |
| D2 domain_accuracy | mandatory | domain | R2: block (repairable) | block |
| D3 argumentative_coherence | mandatory | da, methodology | DA: block (repairable); R1: warn | block |
| D4 cross_disciplinary_relevance | high | perspective | R3: warn | warn |
| D5 writing_and_structure | normal | eic | EIC: warn | warn |
| D6 venue_fit_and_contribution | mandatory | eic | EIC: warn | warn |

**Step 2: failure conditions.**

| Condition | Quantifier | Expression | Evaluation | Fired |
|---|---|---|---|---|
| F1 (95) | any | any mandatory dimension has a fatal block | No assessed seat declared `block_class: fatal` | false |
| F2 (90) | any | any mandatory dimension scores 'block' | D1 (1 of 1 seats), D2 (1 of 1), D3 (1 of 2 blocks; "any" needs at least 1) | true |
| F3 (70) | majority | two or more mandatory dimensions score 'warn' or worse | D1 (n=1, owner warn or worse), D2 (n=1, owner), D3 (n=2, both seats warn or worse), D6 (n=1, owner): 4 dimensions | true |
| F4 (60) | any | any high-priority dimension scores 'block' | D4 is warn | false |
| F5 (40) | any | any dimension scores 'warn' or worse | All six dimensions | true |
| F0 (10) | all | every dimension scores 'pass' | No dimension passes | false |

**Step 3: precedence.** The fired conditions are F2, F3 and F5. The highest severity is F2 (90), and its action is major revision.

```
dimension_verdicts: [D1=block, D2=block, D3=block, D4=warn, D5=warn, D6=warn]
fired_conditions: [F2, F3, F5]
da_critical_adjudications: []
editorial_decision=major_revision
```

The DA's CRITICAL table has no rows, so there are no DA-CRITICAL IDs to adjudicate and no accept-consistency marker applies. The DA's eight MAJOR findings (M1 to M8) are not adjudication IDs. Each is mapped to a roadmap item below, with any corroboration noted.

---

## Blocking Issues (0 to 3, immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---------------|----------------|--------------------|-----------------|------------------------|
| R3 | Conclusions give separate directions for rurality and lower income, which the joint area contrast cannot support (drives the D3 block) | EIC, R1, R3, DA | text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties" | REV-4 |
| R17 | Primary-estimand intervals leave out model-fitting and cross-fitting variability (drives the D1 block) | R1, DA | text: Methods, Models and validation, Uncertainty "500 resamples of out-of-fold predictions, percentile intervals, no refitting" | REV-23 |
| R24 | The "triage" reading ignores hormone therapy recorded as the end of the interval (one of the D2 block findings; R25 and R15 also bear on D2) | R2, DA | table: Supplementary Table S19, primary analysis row against the radical prostatectomy without radiotherapy only row — low risk 47.9 against 45.8, high risk 32.8 against 38.4 | REV-35 |

---

## Reviewer Summary

| Reviewer | Role | Recommendation (as stated on card) | Confidence | Dimension scores |
|----------|------|-----------------------------------|------------|------------------|
| Journal-Fit Reviewer (EIC) | Senior editor, cancer health services research (field-general) | "Preliminary overall quality signal for synthesis: major revision" | Not stated at report level; per-finding 3 to 5 | D5 warn, D6 warn |
| Reviewer 1 (R1) | Biostatistician, prediction-model evaluation (TRIPOD+AI), resampling, g-computation | Major Revision | 4 of 5 | D1 block (repairable), D3 warn |
| Reviewer 2 (R2) | Urologic oncology outcomes researcher, SEER/NCDB | Not stated; card says the D2 block "is repairable, not fatal" | Not stated at report level; per-finding 3 to 5 | D2 block (repairable) |
| Reviewer 3 (R3) | Health economist, equity measurement and rural access | Not stated; D4 "scores warn, not block" | Not stated at report level; per-finding 3 to 4 | D4 warn |
| Devil's Advocate (DA) | Adversarial, owner of D3 | Not stated; D3 block (repairable), "No finding alone reaches rejection level" | Per-finding 3 to 5 | D3 block (repairable); CRITICAL 0, MAJOR 8 |

---

## Weakness Sub-Claim Inventory (Step 1b)

Each weakness bundle is split into atomic sub-claims. Position is `raised` for the first seat in panel order and `corroborated` for later seats. `disputed` marks a materially different severity for the same sub-claim. Seats not listed are `not-mentioned`, which is silence, not opposition. Severity and Confidence are copied from each seat's own finding. DA positions are listed for traceability but are not counted in consensus.

| sub_claim_id | parent_weakness | reviewer_id | position | evidence_pointer | severity | confidence |
|---|---|---|---|---|---|---|
| SC-1 | EIC W1; R3 W4 | EIC | raised | EIC W1 (text: Introduction, AUC 0.671 to 0.673) | major | 4 |
| SC-1 | | R3 | corroborated | R3 W4 (table: Table 2, low risk rows) | major | 3 |
| SC-2 | EIC W1 | EIC | raised | EIC W1 | major | 4 |
| SC-2 | | DA | corroborated (DA minor list) | DA minor issues, Introduction "A small gain can still be informative" | minor | — |
| SC-3 | EIC W1; R3 W4 | EIC | raised | EIC W1 | major | 4 |
| SC-3 | | R3 | corroborated | R3 W4 | major | 3 |
| SC-3 | | DA | corroborated | DA M2, DA minor list | major | 4 |
| SC-4 | EIC W2; R1 W3; R3 W1 | EIC | raised | EIC W2 (text: Conclusions) | major | 4 |
| SC-4 | | R1 | corroborated | R1 W3 ("Describe the area contrast as rurality and income combined throughout") | major | 5 |
| SC-4 | | R3 | corroborated | R3 W1 (text: Abstract, Results, Erreygers index) | major | 4 |
| SC-4 | | DA | corroborated | DA M3 | major | 5 |
| SC-5 | EIC W2; R1 W4; R3 W1 | EIC | raised | EIC W2 | major | 4 |
| SC-5 | | R1 | corroborated | R1 W4 (rurality caveat absent) | major | 3 |
| SC-5 | | R3 | corroborated | R3 W1 | major | 4 |
| SC-5 | | DA | corroborated | DA M3 | major | 5 |
| SC-6 | EIC W3 | EIC | raised | EIC W3 (text: Title) | major | 4 |
| SC-7 | EIC W3; R2 W3 | EIC | raised | EIC W3 | major | 4 |
| SC-7 | | R2 | corroborated | R2 W3 (Australian framing "rests on two lung cancer studies [4, 5]") | major | 4 |
| SC-8 | EIC W3; R3 W5 | EIC | raised | EIC W3 | major | 4 |
| SC-8 | | R3 | disputed (severity) | R3 W5 (text: Methods, Outcome) | minor | 4 |
| SC-9 | EIC W4 | EIC | raised | EIC W4 (text: Methods, Protocol) | major | 4 |
| SC-10 | EIC W4; R1 W7; R2 W13 | EIC | raised | EIC W4 (code URL placeholder) | major | 4 |
| SC-10 | | R1 | disputed (severity) | R1 W7 ("the code repository URL is missing") | minor | 4 |
| SC-10 | | R2 | disputed (severity) | R2 W13 ("the repository URL is missing") | minor | 4 |
| SC-11 | EIC W5; R1 W7; R2 W13 | EIC | raised | EIC W5 (absence: Supplement, Reporting checklists) | minor | 5 |
| SC-11 | | R1 | corroborated | R1 W7 | minor | 4 |
| SC-11 | | R2 | corroborated | R2 W13 | minor | 4 |
| SC-12 | EIC W6; R2 W13 | EIC | raised | EIC W6 (text: Declarations, Use of AI tools) | minor | 5 |
| SC-12 | | R2 | corroborated | R2 W13 (ethics statement placeholder) | minor | 4 |
| SC-13 | EIC W7; R1 W5; R2 W10 | EIC | raised | EIC W7 (table: Supplementary Table S8) | minor | 5 |
| SC-13 | | R1 | corroborated | R1 W5 | minor | 5 |
| SC-13 | | R2 | corroborated | R2 W10 | minor | 5 |
| SC-13 | | DA | corroborated | DA minor list | minor | — |
| SC-14 | EIC W8 | EIC | raised | EIC W8 (text: Discussion, The rural direction) | minor | 5 |
| SC-14 | | DA | corroborated | DA minor list | minor | — |
| SC-15 | EIC W9 | EIC | raised | EIC W9 (table: Table 3) | minor | 5 |
| SC-16 | EIC W10; R1 W6 | EIC | raised | EIC W10 (absence: secondary outcome grid edge) | minor | 5 |
| SC-16 | | R1 | corroborated | R1 W6 | minor | 4 |
| SC-17 | EIC W11 | EIC | raised | EIC W11 (text: Abstract) | minor | 4 |
| SC-18 | EIC W12; R1 W1 | EIC | raised | EIC W12 (text: Discussion, Strengths) | minor | 4 |
| SC-18 | | R1 | disputed (severity) | R1 W1 ("Qualify the Strengths wording") | major | 4 |
| SC-19 | EIC W13 | EIC | raised | EIC W13 (figure: Figure 3) | minor | 4 |
| SC-19 | | DA | corroborated | DA minor list | minor | — |
| SC-20 | EIC W14 | EIC | raised | EIC W14 (table: Table 1) | minor | 5 |
| SC-21 | EIC W15; R2 W3 | EIC | raised | EIC W15 (text: Introduction, "one factor at a time") | minor | 3 |
| SC-21 | | R2 | disputed (severity) | R2 W3 (same anchor) | major | 4 |
| SC-22 | EIC W15; R2 W3 | EIC | raised | EIC W15 (precedent [11] cited as support, not positioned) | minor | 3 |
| SC-22 | | R2 | disputed (severity) | R2 W3 (Stokes, Ajjawi, Semprini, Baade omitted) | major | 4 |
| SC-23 | R1 W1 | R1 | raised | R1 W1 (text: Methods, Uncertainty) | major | 4 |
| SC-23 | | DA | corroborated | DA M5 | major | 3 |
| SC-24 | R1 W1 | R1 | raised | R1 W1 (cells not counties or registries; cell sizes unreported) | major | 4 |
| SC-25 | R1 W2 | R1 | raised | R1 W2 (table: Supplementary Table S7) | major | 4 |
| SC-26 | R1 W3; R3 W10 | R1 | raised | R1 W3 (text: Supplementary Table S32, amendment 1.7) | major | 5 |
| SC-26 | | R3 | disputed (severity) | R3 W10 (absence: Supplement) | minor | 4 |
| SC-26 | | DA | corroborated | DA M4 | major | 5 |
| SC-27 | R1 W3 | R1 | raised | R1 W3 (agreement rule and dropped intervals not labelled post hoc) | major | 5 |
| SC-28 | R1 W4 | R1 | raised | R1 W4 (absence: index by diagnosis year) | major | 3 |
| SC-29 | R1 W5 | R1 | raised | R1 W5 (weighting "0.2 points or less" not confirmable) | minor | 5 |
| SC-30 | R1 W7 | R1 | raised | R1 W7 (TRIPOD+AI prediction-model items) | minor | 4 |
| SC-31 | R1 W8 | R1 | raised | R1 W8 (text: Abstract, Results) | minor | 4 |
| SC-31 | | DA | corroborated | DA minor list | minor | — |
| SC-32 | R1 W9 | R1 | raised | R1 W9 (text: Methods, Ordered feature steps) | minor | 3 |
| SC-33 | R1 W10; R3 W2 | R1 | raised | R1 W10 (text: Conclusions) | minor | 3 |
| SC-33 | | R3 | disputed (severity) | R3 W2 (same anchor) | major | 4 |
| SC-33 | | DA | corroborated | DA M8 | major | 3 |
| SC-34 | R1 Minor Issues | R1 | raised | R1 Minor Issues ("98 of 100") [SEVERITY-SOURCE: letter-fallback] [CONFIDENCE-SOURCE: report-level] | minor | 4 |
| SC-34 | | DA | corroborated | DA minor list | minor | — |
| SC-35 | R2 W1 | R2 | raised | R2 W1 (table: Supplementary Table S19) | major | 4 |
| SC-35 | | DA | corroborated | DA M7 | major | 3 |
| SC-36 | R2 W2 | R2 | raised | R2 W2 (text: Methods, Clinical risk groups) | major | 4 |
| SC-37 | R2 W4; R3 W6 | R2 | raised | R2 W4 (text: Abstract, Results "lower is better") | minor | 4 |
| SC-37 | | R3 | corroborated | R3 W6 | minor | 4 |
| SC-37 | | DA | corroborated | DA M6 | major | 4 |
| SC-38 | R2 W5 | R2 | raised | R2 W5 (text: Abstract, Results) | minor | 4 |
| SC-38 | | DA | corroborated | DA M2 | major | 4 |
| SC-39 | R2 W6 | R2 | raised | R2 W6 (text: Methods, Active surveillance) | minor | 3 |
| SC-40 | R2 W7 | R2 | raised | R2 W7 (text: Discussion, Marital status) | minor | 4 |
| SC-40 | | DA | corroborated (rural surveillance point) | DA M8 | major | 3 |
| SC-41 | R2 W8 | R2 | raised | R2 W8 (text: Limitations) | minor | 4 |
| SC-42 | R2 W9; R3 W8 | R2 | raised | R2 W9 (text: Supplementary Box 2) | minor | 3 |
| SC-42 | | R3 | corroborated | R3 W8 | minor | 3 |
| SC-43 | R2 W11 | R2 | raised | R2 W11 (text: Introduction, [10]) | minor | 4 |
| SC-44 | R2 W12 | R2 | raised | R2 W12 (text: Discussion, The rural direction) | minor | 4 |
| SC-44 | | DA | corroborated (trend not interpreted) | DA Unexamined premise | — | — |
| SC-45 | R2 W13 | R2 | raised | R2 W13 (SEER variable names for Gleason and PSA) | minor | 4 |
| SC-46 | R3 W3 | R3 | raised | R3 W3 (text: Methods, Uncertainty) | major | 4 |
| SC-46 | | DA | corroborated | DA M1 | major | 4 |
| SC-47 | R3 W7 | R3 | raised | R3 W7 (table: Supplementary Table S11) | minor | 3 |
| SC-47 | | DA | corroborated | DA minor list | minor | — |
| SC-48 | R3 W9 | R3 | raised | R3 W9 (text: Discussion, What an Australian registry could add) | minor | 4 |
| SC-49 | R3 W11 | R3 | raised | R3 W11 (absence: Methods, Income inequality) | minor | 4 |

Two DA-only points have no non-DA sub-claim, so their roadmap rows use `—`. The first (REV-50) is that sensitivity-scenario agreement is not independent replication, from the DA minor list. The second (REV-51) is the unexamined premise that the SEER diagnosis date is a comparable start point, which the DA raised "as a question for the authors, not as an established defect".

Surface-form parity check (Step 1c): no sub-claim was down-weighted for its wording. Weighting uses per-finding confidence and the stated expertise boundaries only. In SC-21/22, the EIC defers to "a domain specialist". In SC-33, R1 notes that the mechanism "overlaps with the devil's advocate and domain seats".

---

## Consensus Analysis

Counts use the four non-DA seats (EIC, R1, R2, R3) as the denominator. DA positions are reported separately.

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (all four agree): none. No sub-claim was raised by all four non-DA seats.

**[CONSENSUS-3]** (three agree, the fourth silent):
1. **SC-4, joint area contrast read as separate rural and lower-income directions.** EIC W2, R1 W3 and R3 W1 agree. R2 is silent. The DA corroborates in M3 (confidence 5). All three seats agree that only the joint area profile is interpretable and that the Conclusions go beyond it.
2. **SC-5, income concentration index cannot separate income from rurality, and the source-report caveat is missing.** EIC W2, R1 W4 and R3 W1 agree. R2 is silent. The DA corroborates in M3.
3. **SC-11, STROBE, RECORD and TRIPOD+AI adherence claimed with placeholder checklists.** EIC W5, R1 W7 and R2 W13 agree. R3 is silent.
4. **SC-13, leave-one-variable-out range (0.22 to 0.45) contradicts Supplementary Table S8 (0.18 to 0.45).** EIC W7, R1 W5 and R2 W10 agree. R3 is silent. The DA also lists it.

**Corroborated findings (two seats, no conflict):** SC-1 and SC-3 (EIC, R3), SC-7 (EIC, R2), SC-12 (EIC, R2), SC-16 (EIC, R1), SC-37 (R2, R3; the DA rates the same concern Major in M6), and SC-42 (R2, R3).

**Single-reviewer findings:** all other sub-claims. They are weighted by per-finding confidence. None carries confidence 1 or 2, so none is excluded or reduced. Several single-seat Major findings are corroborated by the DA: SC-23 by M5, SC-35 by M7, and SC-46 by M1.

**Noted tension, not a dispute.** EIC S2 credits the "Candid disclosure of post hoc decisions" for the two labelled amendments. R1 W3 (SC-27) finds that the agreement rule and the dropped intervals from the same amendment are not labelled post hoc. The EIC strength does not argue those two elements were labelled, so SC-27 remains a single-reviewer finding.

### Points of Disagreement

**Disagreement 1: Rationale for applying the 90-day Australian benchmark to US data (SC-8)**
- **EIC view (W3, Major, confidence 4)**: the benchmark and title are "not justified for readers". The 90-day outcome is justified only as the Australian pathway benchmark, although cited US study [8] used the same threshold.
- **R3 view (W5, Minor, confidence 4)**: the same gap. The remedy is "one or two sentences" in Methods noting that 90 days is also used in US studies and that the SEER interval is not the pathway's own measure.
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: unresolved on severity; remedy agreed. The author must add a threshold rationale that stands on its own for US data, citing [8] and noting the interval difference. Obligation: must_fix. Both severities are transported unchanged.
- **Resolution Rationale**: both seats are within competence at equal confidence and cite the same Methods passage. EIC's Major rating comes from a bundle that also covers the title (SC-6) and Introduction structure (SC-7). The panel does not resolve whether the threshold rationale alone is Major. No seat opposes the change, so the author must address it.

**Disagreement 2: Placeholder code repository link (SC-10)**
- **EIC view (W4, Major, confidence 4)**: reproducibility and pre-specification claims "cannot yet be verified by readers". The code URL is a placeholder.
- **R1 view (W7, Minor, confidence 4)** and **R2 view (W13, Minor, confidence 4)**: the missing repository link is a reporting-completeness gap under the claimed guidelines.
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: remedy agreed by three seats (supply a public, timestamped code link). Obligation: must_fix. Severity is recorded as disputed (Major for EIC, Minor for R1 and R2).
- **Resolution Rationale**: the placeholder is directly observable, and all three seats require the same fix. The Major weight in EIC W4 rests mainly on unverifiable protocol timing (SC-9, single-reviewer Major), which stays its own item. For the link alone, R1 (reproducibility within its expertise) and R2 rate it Minor. The remedy is identical under both severities, so the severity dispute does not change the required action.

**Disagreement 3: Strengths wording on county-level uncertainty (SC-18)**
- **EIC view (W12, Minor, confidence 4)**: "Uncertainty that respects county-level exposures" overstates the design. The card says "adequacy of the bootstrap design is outside my focus".
- **R1 view (W1, Major, confidence 4)**: the same wording is an "Overstated strength" inside a Major finding about the interval construction.
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: remedy agreed (reword to a cluster bootstrap over rurality by income cells, used as a proxy). Obligation: must_fix. R1's Major severity for the interval design itself is carried by SC-23 and SC-24.
- **Resolution Rationale**: expertise first. Resampling design belongs to R1, and the EIC explicitly places it outside their focus. Both seats agree the wording must change. The severity difference reflects R1 bundling the wording with the design problem.

**Disagreement 4: How prior work is described, and omitted precedents (SC-21, SC-22)**
- **EIC view (W15, Minor, confidence 3)**: the gap rests on "a narrow set of studies". Precedent [11] should be positioned as prior incremental-value work. The card says completeness "is better judged by a domain specialist".
- **R2 view (W3, Major, confidence 4)**: the account "omits the closest analogues and misdescribes the literature". The cited studies are multivariable, not one factor at a time. Stokes 2013, Ajjawi 2026, Semprini 2026 and Baade 2012 are uncited. The PubMed-only literature check supports only "we found no study that…".
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: R2's Major severity is adopted for the arbitration record, and both sub-claims are must_fix. Transported severities are shown unchanged in the roadmap.
- **Resolution Rationale**: expertise first (domain literature defers to R2) and evidence first (R2 checked each record in PubMed). The EIC seat itself defers to a domain specialist, so this is resolved rather than left as unresolved dissent.

**Disagreement 5: Promised one-at-a-time profile table is missing (SC-26)**
- **R1 view (W3, Major, confidence 5)**: the post hoc switch "hides a model conflict". Rurality alone gave -8.7 against +1.7 points, and income alone -0.9 against -8.7. Amendment 1.7 promises a supplementary table that is absent.
- **R3 view (W10, Minor, confidence 4)**: the same missing table. R3 notes these results "are the most direct evidence that an income-only gradient is not robust".
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: Major, must_fix. Publish the one-at-a-time table with the disagreement stated, or correct the amendment text. R1's remedy (publish the table) is the requirement.
- **Resolution Rationale**: expertise first (post hoc analytic reporting is R1's domain, at confidence 5) and evidence first. R1 compared the amendment text, the supplement contents and the source report directly. R3's own rationale describes the omitted results as decision-relevant evidence. The DA independently rates the same omission Major (M4, confidence 5).

**Disagreement 6: Directional conclusions omit that the cohort is conditioned on recorded curative treatment (SC-33)**
- **R1 view (W10, Minor, confidence 3)**: the Conclusions state the direction without the conditioning. R1 notes the mechanism "overlaps with the devil's advocate and domain seats".
- **R3 view (W2, Major, confidence 4)**: policy readers of the abstract and Conclusions may take "less delay" as better access. Recorded curative treatment is itself socially patterned (increment 1.96 to 2.16; 75.3% against 81.9% in high-risk men). The selection bounds do not cover it.
- **Disagreement type**: severity disagreement.
- **Editor's Resolution**: Major, must_fix. State the conditioning population in the abstract and Conclusions, carry the "not evidence of better care" qualifier forward, and say that the bounds do not cover selection into the treated cohort.
- **Resolution Rationale**: expertise first. Selection into treatment and rural access are R3's core expertise (confidence 4), and R1 flags the point as outside its lead area (confidence 3). The DA's M8 corroborates at Major and adds that the direction of this bias for area measures is not discussed.

### Devil's Advocate findings

- **CRITICAL**: none. The DA states: "No finding alone reaches rejection level, so the CRITICAL table is empty."
- **MAJOR, mapped to roadmap items**: M1 to REV-46 (corroborates R3 W3); M2 to REV-3 and REV-38 (corroborates EIC W1, R3 W4 and R2 W5); M3 to REV-4 and REV-5 (corroborates the CONSENSUS-3 findings); M4 to REV-26 (corroborates R1 W3 and R3 W10); M5 to REV-23 (corroborates R1 W1); M6 to REV-37 (corroborates R2 W4 and R3 W6 at a higher severity); M7 to REV-35 (corroborates R2 W1); M8 to REV-33 and REV-40 (corroborates R3 W2, R1 W10 and R2 W7).
- The DA's severity on M6 (Major) is higher than the two non-DA seats on the same sub-claim (both Minor). DA findings do not enter consensus counting, so SC-37 remains a corroborated Minor finding. The DA's argument is recorded here, and the author must respond to it in the response letter.

---

## Decision Rationale

The decision follows from the contract. Three mandatory dimensions carry a repairable block, each from its owning or eligible seat.
- **D1 (R1)**: the headline intervals do not reflect the stated resampling design.
- **D2 (R2)**: the high-risk "triage" reading ignores hormone therapy recorded as the end of the interval, and risk groups are misdescribed as clinical-only.
- **D3 (DA)**: principal conclusions go beyond the joint area contrast and the constructed low-risk stratum.

Condition F2 therefore sets major revision. F3 fired independently on four mandatory dimensions at warn or worse, so the outcome does not depend on a single block.

A stricter outcome is not supported. F1 did not fire because no seat declared a fatal block. Every blocking seat classed its block as repairable, and the DA found nothing at rejection level. The panel agrees that the core estimand is well defined and honestly reported. EIC S3 notes that a more flexible clinical adjustment "did not absorb the social signal". R2 notes that the social increment survives the prostatectomy-only scenario, and the DA writes that "no result contradicts" the central quantity.

A lighter outcome is not available either. Under the contract, a mandatory block cannot resolve to minor revision, and the cards themselves describe decision-bearing rewriting and re-analysis. R1 asks for fold-seed repeats, per-step tuning and a year-stratified index. R2 asks for a stage-free step 1 sensitivity analysis. Several seats ask for reframing of the Conclusions and of the "social position" label.

The six recorded disagreements are all about severity. None disputes whether the problem exists. Four were resolved by expertise and evidence (SC-18, SC-21/22, SC-26, SC-33). For the other two (SC-8, SC-10) the remedy is agreed and the severity is left open. None of them changes the mechanical decision.

This package was produced by a single-family panel that shares its model family with the drafting process. The provenance caveat above therefore limits how much independent confirmation the consensus labels provide.

---

## Closing

We encourage you to consider the reviewers' comments carefully and to prepare a substantially revised manuscript before posting. The revised manuscript should go through another round of review (re-review mode), because the D1, D2 and D3 blocks rest on analyses and framing that a re-review needs to verify.

---

# Part 2: Revision Roadmap

Schema: `revision-roadmap/1.0` core (reviewer-owned). Rows are in immutable source-traceability order: the first raising seat in panel order (EIC, R1, R2, R3, DA), then finding number. Here REV-n equals SC-n, and REV-50 and REV-51 are DA-only. Severity, obligation, cost and author choice never determine order. No author triage, work order or display order appears here; those belong in the separate author sidecar.

Proposed targets: no block manifest was bound for this round, so no block ids are proposed. Locators are manuscript section names only and carry no write authority. The allowed operations when a manifest is bound are `replace_block`, `insert_after` and `delete_block`.

Seat labels in the Source column: EIC = Journal-Fit Reviewer; R1 = methodology; R2 = domain; R3 = perspective; DA = Devil's Advocate. The first column holds transport references (`R<n>`, `S<n>`), not seats.

## Required Revisions (Must Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Give the skill increment an interpretive anchor and bridge it to the standardised and population-level percentage contrasts | SC-1 | major (EIC W1; R3 W4) | text: Introduction "in one US health system, adding neighbourhood variables to a clinical model predicting advanced prostate cancer changed the AUC from 0.671 to 0.673" | 4 — EIC editorial competence; R3 3 — adjacent field | EIC, R3 (corroborated) | must_fix | section: Discussion (interpretive paragraph) + Abstract sentence | interpretive_ambiguity_remains; target claim: significance of the social-position increment |
| R2 | Report the low-risk share (82%, 98%) alongside the absolute step 2 skill wherever it appears | SC-3 | major (EIC W1; R3 W4; DA M2) | table: Table 2, low risk rows — social position as 82 and 98 percent of step 2 skill, where step 2 skill is 0.76 and 0.99 | 4 — EIC; R3 3; DA 4 | EIC, R3 (corroborated); DA | must_fix | sentence: Abstract Results; Results; Discussion Principal findings | claim_scope_unsupported; target claim: low-risk "added more than clinical need" |
| R3 | State direction only for the joint area contrast; remove separate rural and lower-income directions from the Conclusions and Discussion | SC-4 | major (EIC W2; R1 W3; R3 W1; DA M3) | text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties" | 4 — EIC checked against source reports; R1 5; R3 4; DA 5 | EIC, R1, R3 (CONSENSUS-3; R2 silent); DA | must_fix | section: Conclusions; Discussion (Principal findings, The rural direction) | claim_scope_unsupported; target claim: Conclusions direction statement |
| R4 | Restore the caveat that the income concentration index does not separate income from rurality and is not standardised for clinical features | SC-5 | major (EIC W2; R1 W4; R3 W1; DA M3) | text: Abstract, Results "delay was concentrated among men in higher-income counties (Erreygers index 0.062, 0.039 to 0.083; 0 means no income gradient)" | 4 — R3 core expertise; EIC 4; R1 3 | EIC, R1, R3 (CONSENSUS-3; R2 silent); DA | must_fix | section: Results Income inequality; Discussion; Abstract | interpretive_ambiguity_remains; target claim: income gradient |
| R5 | Retitle so the title names the social-position increment, and shorten it | SC-6 | major (EIC W3) | text: Title "how much is clinical need?" | 4 — core editorial competence in title–estimand alignment | EIC (single) | must_fix | sentence: Title | editorial_conformance_unmet; target section: Title |
| R6 | Move Australian and Tasmanian material (including the two lung cancer studies) into a labelled context or transferability paragraph; resolve the "different directions" tension | SC-7 | major (EIC W3; R2 W3) | text: Title "how much is clinical need?" [EIC W3 anchor; R2 W3 anchor: text: Introduction "These studies report adjusted associations for one factor at a time, usually pooled across risk groups."] | 4 — EIC; R2 4 | EIC, R2 (corroborated) | must_fix | section: Introduction | reader_traceability_reduced; target section: Introduction |
| R7 | Give a 90-day threshold rationale that stands on its own for US data (cite [8]) and state that the SEER interval is not the pathway's measure | SC-8 | major (EIC W3) / minor (R3 W5) — SPLIT, severity unresolved | text: Methods, Outcome "a wait of more than 90 days, following the optimal care pathway benchmark" | 4 — EIC; 4 — R3 core expertise | EIC, R3 (SPLIT, Disagreement 1) | must_fix | sentence: Methods, Outcome | interpretive_ambiguity_remains; target section: Methods Outcome |
| R8 | Make protocol timing verifiable: public timestamped protocol and commit identifiers or times in the amendment log (S32) | SC-9 | major (EIC W4) | text: Methods, Protocol "It was committed to version control before the first cohort was built; it was not registered externally" | 4 — core editorial competence in transparency | EIC (single) | must_fix | section: Methods Protocol + Supplementary Table S32 | method_reproducibility_unresolved; target table: Supplementary Table S32 |
| R9 | Supply a public, timestamped code repository link | SC-10 | major (EIC W4) / minor (R1 W7; R2 W13) — SPLIT, severity disputed | text: Reporting checklists "IN PREPARATION: STROBE, RECORD and TRIPOD+AI checklists with page references." | 4 — EIC; 4 — R1; 4 — R2 | EIC, R1, R2 (SPLIT, Disagreement 2) | must_fix | sentence: Declarations (code availability) | method_reproducibility_unresolved; target dataset: analysis code |
| R10 | Complete STROBE, RECORD and TRIPOD+AI checklists with section references and address missing items | SC-11 | minor (EIC W5; R1 W7; R2 W13) | absence: Supplement, Reporting checklists — expected completed STROBE, RECORD and TRIPOD+AI checklists with section references; checked Methods (Reporting and ethics), Declarations, the final supplement section | 5 — directly observable (EIC); R1 4; R2 4 | EIC, R1, R2 (CONSENSUS-3; R3 silent) | must_fix | section: Supplement, Reporting checklists | reporting_requirement_unmet; target section: Reporting checklists |
| R11 | Complete all declarations (affiliation, ethics, funding, competing interests, AI-use disclosure) | SC-12 | minor (EIC W6; R2 W13) | text: Declarations, Use of AI tools "[TO BE COMPLETED: disclosure statement]" | 5 — directly observable (EIC); R2 4 | EIC, R2 (corroborated) | must_fix | section: Declarations | reporting_requirement_unmet; target section: Declarations |
| R12 | Correct the leave-one-variable-out range to 0.18 to 0.45 | SC-13 | minor (EIC W7; R1 W5; R2 W10) | table: Supplementary Table S8 — intermediate risk, penalised logistic regression, marital status 0.18 and rurality 0.19 | 5 — direct table comparison (EIC, R1, R2) | EIC, R1, R2 (CONSENSUS-3; R3 silent); DA | must_fix | sentence: Results, Which social variable | acceptance_criterion_unmet; target table: Supplementary Table S8 |
| R13 | Correct the high-risk "under 3 points" statement (pooled contrast under 3 points; high-risk models disagreed) | SC-14 | minor (EIC W8) | text: Discussion, The rural direction "although the standardised difference was under 3 points" | 5 — checked against S30 and phase4_receipt | EIC (single); DA | must_fix | sentence: Discussion, The rural direction | claim_scope_unsupported; target claim: high-risk standardised difference |
| R14 | Reword the Strengths claim about county-level uncertainty to describe the cell-level cluster bootstrap proxy | SC-18 | minor (EIC W12) / major (R1 W1) — SPLIT | text: Discussion, Strengths "Uncertainty that respects county-level exposures" | 4 — EIC wording check; 4 — R1 code read | EIC, R1 (SPLIT, Disagreement 3) | must_fix | sentence: Discussion, Strengths | claim_scope_unsupported; target section: Strengths |
| R15 | Describe prior models accurately (multivariable, not one factor at a time), describe how prior work was identified, and hedge the novelty claim to the search done | SC-21 | minor (EIC W15) / major (R2 W3) — SPLIT, resolved to R2 | text: Introduction "These studies report adjusted associations for one factor at a time, usually pooled across risk groups." | 3 — EIC defers to domain; 4 — R2 PubMed-checked | EIC, R2 (SPLIT, Disagreement 4) | must_fix | section: Introduction (gap paragraph) + Abstract | claim_scope_unsupported; target claim: novelty statement |
| R16 | Cite and position the closest precedents (Stokes 2013, Ajjawi 2026, Semprini 2026, Baade 2012; [11] as incremental-value precedent) | SC-22 | minor (EIC W15) / major (R2 W3) — SPLIT, resolved to R2 | absence: Introduction references — expected Stokes 2013, Ajjawi 2026, Semprini 2026 and Baade 2012 cited and set apart; checked Introduction, Discussion, reference list [R2 W3 missing references] | 3 — EIC; 4 — R2 | EIC, R2 (SPLIT, Disagreement 4) | must_fix | section: Introduction; Discussion | evidence_gap_remains; target section: Introduction |
| R17 | Propagate model-fitting and cross-fitting uncertainty into the primary-estimand intervals (minimum: repeat cross-fitting over several fold seeds and report the spread) | SC-23 | major (R1 W1; DA M5) | text: Methods, Models and validation, Uncertainty "500 resamples of out-of-fold predictions, percentile intervals, no refitting" | 4 — resampling design read from increments.py and run_phase4_models.py | R1 (single); DA | must_fix | re_analysis: primary increment intervals (Table 2, S20) | method_reproducibility_unresolved; target table: Table 2 |
| R18 | Report bootstrap cell count and size distribution per stratum; justify cells as the dependence unit or add an alternative-clustering sensitivity analysis | SC-24 | major (R1 W1) | table: Table 1 — large metropolitan counties 194,681 men [R1 W1 locator; finding anchor shared with R17: Methods, Uncertainty] | 4 — R1 code read | R1 (single) | must_fix | re_analysis: bootstrap clustering (Methods Uncertainty; supplement) | evidence_gap_remains; target section: Methods Uncertainty |
| R19 | Tune hyperparameters separately at each step (at least steps 1 and 2); report resulting LightGBM increments and limit the model-comparison inference to strata where the flexible clinical model is at least as good | SC-25 | major (R1 W2) | table: Supplementary Table S7, low risk, LightGBM, step 1 log-loss skill 0.02 and calibration slope 0.883 against penalised logistic regression 0.14 and 0.998 | 4 — values read from S7; mechanism inferred, not tested | R1 (single) | must_fix | re_analysis: per-step tuning (Table 2, S7) | claim_scope_unsupported; target claim: "A more flexible clinical adjustment therefore did not absorb the social signal." |
| R20 | Publish the one-at-a-time rurality and income profile table promised by amendment 1.7, with the model disagreement stated | SC-26 | major (R1 W3; DA M4) / minor (R3 W10) — SPLIT, resolved Major | text: Supplementary Table S32, amendment version 1.7 "with the one-at-a-time results kept in a supplementary table" | 5 — R1 direct comparison; 4 — R3 | R1, R3 (SPLIT, Disagreement 5); DA | must_fix | section: Supplement (new table) | reporting_requirement_unmet; target table: Supplementary Table S32 |
| R21 | Label the 3-point agreement rule and the dropped intervals as post hoc in Methods and the abstract; state that area and marital differences lack uncertainty measures | SC-27 | major (R1 W3) | text: Supplementary Table S32, amendment 1.7 "Prompted by the model disagreement seen in the development run" | 5 — R1 amendment text and protocol compared | R1 (single) | must_fix | sentence: Methods Judging differences; Abstract | reporting_requirement_unmet; target section: Methods |
| R22 | Report county income rank distribution by diagnosis year and add a year-stratified or year-standardised concentration index | SC-28 | major (R1 W4) | absence: Methods and Results, Income inequality — expected an index stratified or standardised by year of diagnosis, or a report of how county income band varies with diagnosis year; checked Methods Income inequality, Results Income inequality, Figure 4b legend, Supplementary Table S12, Limitations | 3 — pooling confirmed in code; drift size not shown | R1 (single) | must_fix | re_analysis: concentration index (S12, Figure 4b) | evidence_gap_remains; target table: Supplementary Table S12 |
| R23 | State the conditioning on recorded curative treatment in the abstract and Conclusions; carry "not evidence of better care" forward; say the bounds do not cover selection into the treated cohort and discuss bias direction for area measures | SC-33 | minor (R1 W10) / major (R3 W2; DA M8) — SPLIT, resolved Major | text: Conclusions "points to less delay, not more, in rural and lower-income counties" [R3 W2 anchor, full Conclusions sentence] | 3 — R1; 4 — R3 core expertise | R1, R3 (SPLIT, Disagreement 6); DA | must_fix | section: Abstract Conclusions; Conclusions; Discussion | claim_scope_unsupported; target claim: Conclusions direction statement |
| R24 | Qualify the "triage" reading: state that higher-risk radiotherapy patients often start hormone therapy first; bring the prostatectomy-only gradient into the main text; report the clinical-need increment for that scenario | SC-35 | major (R2 W1; DA M7) | table: Supplementary Table S19, primary analysis row against the radical prostatectomy without radiotherapy only row — low risk 47.9 against 45.8, high risk 32.8 against 38.4 | 4 — core expertise, facts checked in PubMed | R2 (single); DA | must_fix | re_analysis: clinical-need increment, prostatectomy-only scenario + section: Discussion Interpretation, Conclusions | claim_scope_unsupported; target claim: "partly clinical triage" |
| R25 | Correct the "clinical information only" risk-group sentence; state that regional stage is often pathological for surgical men; consider a step 1 sensitivity analysis without stage | SC-36 | major (R2 W2) | text: Methods, Clinical risk groups "Risk groups used clinical information only, because pathological grade is observed only after surgery." | 4 — core expertise in SEER staging | R2 (single) | must_fix | sentence: Methods Clinical risk groups + re_analysis: step 1 without stage | interpretive_ambiguity_remains; target claim: "beyond clinical need" reference point |
| R26 | Rename or qualify "social position" in the title, abstract and Conclusions; state prominently that two of three variables are ecological and that registry differences load onto the block | SC-46 | major (R3 W3; DA M1) | text: Methods, Uncertainty "The social block is interpreted as geographic and social position, including any unmeasured registry differences" | 4 — core expertise in equity measurement constructs | R3 (single); DA | must_fix | section: Title; Abstract; Conclusions | interpretive_ambiguity_remains; target claim: "social position" label |

### Required Item Details

> Ordinal contract (#576/#670): `R<n>` is a transport reference, never a work rank. Numbering follows the immutable roadmap source order filtered to `obligation_class == must_fix`. Required blocks are exactly R1 to R26.

**R1: Interpretive anchor for the skill increment**
- **Problem**: A headline increment of 0.42 to 1.37 points of log-loss skill is given no basis for judging its size, and it is not related to the 6 to 9 point area contrasts or the 1.1 to 1.6 point population contrast.
- **Source**: EIC W1 ("Significance of the log-loss skill increment is asserted, not argued"); R3 W4 ("The practical size of the primary estimand is not bridged to the percentage-point contrasts").
- **Requirement**: Add an interpretive paragraph, plus an abstract sentence, relating skill points to the standardised and population-level contrasts or to a benchmark increment.
- **Acceptance criteria**: The Discussion and Abstract explicitly relate the skill increment to at least one patient-scale or benchmark quantity reported in the paper.

**R2: Low-risk share with its denominator**
- **Problem**: The 82% and 98% shares of step 2 skill in low-risk men are ratios over 0.76 and 0.99 points.
- **Source**: EIC W1; R3 W4; DA M2.
- **Requirement**: Give the absolute step 2 skill wherever the share appears.
- **Acceptance criteria**: Every occurrence of the low-risk share in Abstract, Results and Discussion is accompanied by the absolute step 2 skill values.

**R3: Direction stated for the joint area contrast only**
- **Problem**: The Conclusions attribute separate directions to rural and lower-income counties. Only the joint area profile was interpretable.
- **Source**: EIC W2; R1 W3; R3 W1; DA M3.
- **Requirement**: Describe the direction as a contrast between large metropolitan, higher-income counties and remote, lower-income counties. Remove "after clinical features were held as observed" from statements that rely on the concentration index.
- **Acceptance criteria**: No sentence in Abstract, Discussion or Conclusions assigns a separate adjusted direction to rurality or to income.

**R4: Concentration-index caveat restored**
- **Problem**: The Erreygers index is presented as an income gradient, although the source report says it "does not separate income from rurality" and it is crude within risk groups.
- **Source**: EIC W2; R1 W4; R3 W1; DA M3.
- **Requirement**: Restore the caveat in Results and Discussion, and present the index as an area-income and rurality gradient or state that the two are not separable.
- **Acceptance criteria**: Results, Discussion and Abstract state that the index is not standardised for clinical features and does not separate income from rurality.

**R5: Title names the estimand**
- **Problem**: The title asks "how much is clinical need?", while the primary estimand is the social-position increment.
- **Source**: EIC W3.
- **Requirement**: Retitle to name the social-position (or renamed, see R26) increment, and shorten.
- **Acceptance criteria**: The title names the primary estimand and no longer frames the question as clinical need.

**R6: Australian material placed as context**
- **Problem**: The Introduction opens with Australian and Tasmanian findings, including two lung cancer studies, and cites Tasmanian and US studies as pointing "in different directions" while the Discussion rules out comparison.
- **Source**: EIC W3; R2 W3.
- **Requirement**: Move the Australian material into a labelled context or transferability paragraph and remove the directional juxtaposition.
- **Acceptance criteria**: The Introduction presents US evidence first, and no sentence sets US and Tasmanian findings against each other.

**R7: 90-day threshold rationale for US data**
- **Problem**: The outcome is justified only by the Australian pathway, although cited US study [8] uses the same threshold, and the SEER interval differs from the pathway's measure.
- **Source**: EIC W3 (Major); R3 W5 (Minor). This is a SPLIT with the remedy agreed (Disagreement 1).
- **Requirement**: Add a rationale that stands on its own for US data, citing [8], and state that the SEER interval is not the pathway's own measure.
- **Acceptance criteria**: Methods, Outcome contains a US-grounded threshold rationale citing [8] and a sentence on the interval definition difference.

**R8: Verifiable protocol timing**
- **Problem**: "A protocol fixed before modelling" cannot be verified. The protocol is unregistered and cited as a file name, and every S32 amendment carries the same date.
- **Source**: EIC W4.
- **Requirement**: Provide a public, timestamped protocol record, and add commit identifiers or times to the amendment log.
- **Acceptance criteria**: A public timestamped link resolves to the protocol, and each S32 amendment shows a commit identifier or time that can be ordered against model fitting.

**R9: Code repository link**
- **Problem**: The code repository URL is a placeholder, so "Code that regenerates every table and figure" is unverifiable.
- **Source**: EIC W4 (Major); R1 W7 (Minor); R2 W13 (Minor). This is a SPLIT with the remedy agreed (Disagreement 2).
- **Requirement**: Supply a public, timestamped code link, such as a tagged release or archived DOI.
- **Acceptance criteria**: The Declarations contain a resolvable, versioned code repository link.

**R10: Reporting checklists**
- **Problem**: STROBE, RECORD and TRIPOD+AI adherence is claimed, but the checklist section is a placeholder.
- **Source**: EIC W5; R1 W7; R2 W13.
- **Requirement**: Complete all three checklists with section references and address any items found missing.
- **Acceptance criteria**: All three completed checklists are present with a section reference for every applicable item.

**R11: Declarations**
- **Problem**: Affiliation, ethics statement, funding, competing interests, code URL and AI-use disclosure are placeholders.
- **Source**: EIC W6; R2 W13.
- **Requirement**: Complete every declaration, keeping the existing description of AI assistance.
- **Acceptance criteria**: No "[TO BE COMPLETED" placeholder remains in the Declarations.

**R12: Leave-one-variable-out range**
- **Problem**: The Results give 0.22 to 0.45, but S8 shows 0.18 and 0.19 for intermediate-risk logistic regression.
- **Source**: EIC W7; R1 W5; R2 W10; DA minor list.
- **Requirement**: Correct the range to 0.18 to 0.45.
- **Acceptance criteria**: The Results range matches the minimum and maximum of the corresponding S8 cells.

**R13: High-risk standardised difference**
- **Problem**: "Under 3 points" follows a high-risk crude contrast, but the high-risk contrasts were -3.3 and -2.5 ("models disagree"). Only the pooled contrast was under 3 points.
- **Source**: EIC W8; DA minor list.
- **Requirement**: Either say the pooled contrast was under 3 points, or say the models disagreed in high-risk men.
- **Acceptance criteria**: The sentence refers to a stratum whose S30 values match the stated description.

**R14: Strengths wording on uncertainty**
- **Problem**: "Uncertainty that respects county-level exposures" overstates a bootstrap over 79 rurality by income cells, and the export has no county identifier.
- **Source**: EIC W12 (Minor); R1 W1 (Major). This is a SPLIT with the remedy agreed (Disagreement 3).
- **Requirement**: Reword to describe a cluster bootstrap over rurality by income cells, used as a proxy.
- **Acceptance criteria**: The Strengths list no longer claims county-level uncertainty and names the cell-level proxy.

**R15: Accurate description of prior work and hedged novelty**
- **Problem**: Prior studies are described as "one factor at a time", although the cited models are multivariable, and the novelty claim is stated flatly on a PubMed-only, single-screener search.
- **Source**: EIC W15 (Minor); R2 W3 (Major). This is a SPLIT resolved to R2 by expertise (Disagreement 4).
- **Requirement**: Describe prior models accurately, describe how prior work was identified, and hedge the novelty statement to match the search.
- **Acceptance criteria**: The gap sentence describes cited prior models as multivariable, and the novelty statement is scoped to the search that was performed.

**R16: Closest precedents cited and positioned**
- **Problem**: Stokes 2013, Ajjawi 2026, Semprini 2026 and Baade 2012 are not cited, and [11] is cited as support rather than positioned as incremental-value precedent.
- **Source**: R2 W3 (Major); EIC W15 (Minor). This is a SPLIT resolved to R2 (Disagreement 4).
- **Requirement**: Cite these studies and set the paper apart from them. Present [11] and similar work as precedent, with novelty stated as applying the approach to timeliness within risk groups.
- **Acceptance criteria**: The four named studies are cited in Introduction or Discussion with a stated point of difference, and [11] is described as prior incremental-value work.

**R17: Model-fitting and cross-fitting uncertainty in headline intervals**
- **Problem**: Intervals resample fixed out-of-fold losses without refitting, re-tuning or redrawing folds, which is the same construction the paper rejects for standardised contrasts.
- **Source**: R1 W1; DA M5.
- **Requirement**: At minimum, repeat cross-fitting over several fold seeds and report the spread of the increment. The stronger option is a refitting cluster bootstrap. Soften "consistent" claims if the intervals widen.
- **Acceptance criteria**: The manuscript reports increment variability across fold seeds (or refit resamples) for every stratum and model, and the headline interval claims are consistent with it.

**R18: Bootstrap clustering unit and cell sizes**
- **Problem**: The 79 cells are defined by the exposures, not by county or registry, and cell counts and sizes are unreported.
- **Source**: R1 W1.
- **Requirement**: Report cell count and size distribution per stratum, and add an alternative-clustering sensitivity analysis or justify cells as the dependence unit.
- **Acceptance criteria**: The cell count and largest-cell share per stratum are reported, and either an alternative clustering result or an explicit justification is given.

**R19: Per-step tuning**
- **Problem**: Hyperparameters tuned on step 3 are reused at step 1. In low-risk and unknown-risk strata, LightGBM step 1 is weaker and miscalibrated, which inflates its increment.
- **Source**: R1 W2.
- **Requirement**: Tune separately at each step (at least steps 1 and 2), report the resulting increments, and limit the model-comparison inference to strata where the flexible clinical model is at least as good.
- **Acceptance criteria**: Per-step-tuned increments are reported, and the "did not absorb the social signal" inference is restricted to the strata that meet the stated condition.

**R20: One-at-a-time profile table**
- **Problem**: Amendment 1.7 promises a supplementary table of one-at-a-time profiles that is absent, and those results show the models conflicting (-8.7 against +1.7; -0.9 against -8.7).
- **Source**: R1 W3 (Major); R3 W10 (Minor); DA M4. This is a SPLIT resolved Major (Disagreement 5).
- **Requirement**: Add the table with the model disagreement stated, or correct the amendment text.
- **Acceptance criteria**: The supplement contains the one-at-a-time rurality and income profiles for both models, and the amendment 1.7 text matches the supplement.

**R21: Post hoc labels for agreement rule and dropped intervals**
- **Problem**: The "3 points or more, same direction" rule and the dropping of intervals came from the same post hoc amendment but are not labelled post hoc, while protocol section 6 pre-specified intervals.
- **Source**: R1 W3.
- **Requirement**: Label both as post hoc in Methods and the abstract, and state that the abstract's area and marital differences lack uncertainty measures.
- **Acceptance criteria**: Methods and Abstract label the agreement rule and dropped intervals as post hoc.

**R22: Year-aware concentration index**
- **Problem**: The index is pooled over 2010 to 2022 on a year-linked income variable while delay rose from 36.0% to 52.3%.
- **Source**: R1 W4.
- **Requirement**: Report the income rank distribution by diagnosis year and add a year-stratified or year-standardised index.
- **Acceptance criteria**: A year-stratified or year-standardised index and the income-band-by-year distribution are reported.

**R23: Conditioning on recorded curative treatment**
- **Problem**: The Conclusions state the direction without noting that the cohort requires recorded curative treatment, which is itself socially patterned. The bounds do not cover this selection.
- **Source**: R3 W2 (Major); R1 W10 (Minor); DA M8. This is a SPLIT resolved Major (Disagreement 6).
- **Requirement**: State the conditioning population in the abstract and Conclusions, carry "not evidence that rural men receive better care" into the Conclusions, and state that the bounds cover only men without a recorded interval. Discuss the direction of the bias for area measures as well as marital status.
- **Acceptance criteria**: The Abstract Conclusions and Conclusions name the recorded-curative-treatment population, and the Discussion states the scope of the bounds.

**R24: Hormone therapy and the triage reading**
- **Problem**: The interval ends at the first treatment of any kind. Androgen deprivation often precedes radiotherapy in higher-risk disease, and in the prostatectomy-only scenario the low-to-high gap shrinks from 15.1 to 7.4 points.
- **Source**: R2 W1; DA M7.
- **Requirement**: State this in the Outcome and Interpretation sections, bring the prostatectomy-only risk gradient into the main text, report the clinical-need increment for that scenario, and present triage as one explanation among several.
- **Acceptance criteria**: The main text reports the prostatectomy-only gradient and clinical-need increment, and "triage" is presented as one possible explanation.

**R25: Risk-group construction described accurately**
- **Problem**: Methods say risk groups use clinical information only, but regional summary stage partly uses surgical pathology and sits in the step 1 clinical-need block.
- **Source**: R2 W2.
- **Requirement**: Correct the Methods sentence and state that stage for surgical patients is often pathological. Consider a sensitivity analysis leaving stage out of step 1, and say whether the Gleason-and-PSA-only scenario kept stage in step 1.
- **Acceptance criteria**: The Methods no longer describe risk groups as clinical-only, and the treatment of stage in step 1 is stated for the primary and Gleason-and-PSA-only analyses.

**R26: The "social position" label**
- **Problem**: The block holds one individual variable and two county-level area attributes that also absorb registry differences. It carries no individual socioeconomic measure.
- **Source**: R3 W3; DA M1.
- **Requirement**: Rename the block (for example, area and marital attributes) or qualify the label in title, abstract and Conclusions. State prominently that two variables are ecological and that registry differences load onto the block.
- **Acceptance criteria**: Title, Abstract and Conclusions either use the renamed label or qualify "social position" with its ecological and registry content.

## Suggested Revisions (Should Fix / Consider)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Replace the AUC 0.671 to 0.673 example with an argument that small gains are informative | SC-2 | major (EIC W1) | text: Introduction "in one US health system, adding neighbourhood variables to a clinical model predicting advanced prostate cancer changed the AUC from 0.671 to 0.673" | 4 — EIC | EIC (single); DA | should_fix | sentence: Introduction | claim_scope_unsupported; target claim: "A small gain can still be informative" |
| S2 | Replace the "models disagree" label with one that describes same-direction, below-threshold cases | SC-15 | minor (EIC W9) | table: Table 3 — low risk, marital status 3.6 and 2.4 labelled "models disagree" | 5 — directly observable | EIC (single) | should_fix | sentence: Table 3, S21, S30 labels | reader_traceability_reduced; target table: Table 3 |
| S3 | Report secondary-outcome C values and the grid-edge limitation | SC-16 | minor (EIC W10; R1 W6) | absence: Results (Secondary outcome) and Limitations — expected a statement that logistic regression chose C at a grid edge in intermediate and high risk for the secondary outcome, as in reports/phase4_receipt.md; checked Methods (Secondary outcome), Results (Secondary outcome), Limitations, Supplementary Tables S25 to S31 | 5 — EIC; 4 — R1 | EIC, R1 (corroborated) | should_fix | sentence: Results Secondary outcome; Limitations | reporting_requirement_unmet; target section: Limitations |
| S4 | Rewrite Introduction and Discussion as prose; shorten the abstract | SC-17 | minor (EIC W11) | text: Abstract, Results (nested bullets) "Social position increment" | 4 — editorial convention | EIC (single) | should_fix | section: Introduction; Discussion; Abstract | editorial_conformance_unmet; target manuscript |
| S5 | Common or captioned x-axis scales in Figure 3; revise Figure 4b; note the truncated axis in Figure 4a | SC-19 | minor (EIC W13) | figure: Figure 3 — panel x-axis ranges 0 to 4, 0 to 2 and 0 to 1 | 4 — direct inspection | EIC (single); DA | should_fix | section: Figures 3 and 4 | reader_traceability_reduced; target figure: Figure 3 |
| S6 | Rename income "quartile of 16 bands" groups and give dollar ranges | SC-20 | minor (EIC W14) | table: Table 1 — County median household income (quartile of 16 bands), Q1 8.0% and Q4 32.8% of men | 5 — directly observable | EIC (single) | should_fix | sentence: Table 1 note | reader_traceability_reduced; target table: Table 1 |
| S7 | Report weighted and unweighted percentages at a precision that supports "0.2 points or less", or restate the claim | SC-29 | minor (R1 W5) | text: Results, Which social variable "Removing marital status or rurality each lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata" [R1 W5 anchor; weighting sub-claim in same finding] | 5 — direct table comparison | R1 (single) | should_fix | sentence: Results (weighting) | acceptance_criterion_unmet; target claim: "0.2 points or less" |
| S8 | Add TRIPOD+AI prediction-model items: LightGBM missing-value handling, interaction terms, model availability, subgroup performance, cluster count | SC-30 | minor (R1 W7) | text: Reporting checklists "IN PREPARATION: STROBE, RECORD and TRIPOD+AI checklists with page references." | 4 — manuscript and code checked | R1 (single) | should_fix | section: Methods Models and validation; Supplement | reporting_requirement_unmet; target section: Methods |
| S9 | Add the caveat that no interval was computed for the LightGBM versus logistic difference | SC-31 | minor (R1 W8) | text: Abstract, Results "LightGBM had higher out-of-fold skill than penalised logistic regression in every risk group." | 4 — compared with reports/phase4.md | R1 (single); DA | should_fix | sentence: Abstract; Results Model comparison | claim_scope_unsupported; target claim: model comparison |
| S10 | Enter year as categories or a spline in the logistic base model and report the logistic increment | SC-32 | minor (R1 W9) | text: Methods, Ordered feature steps "year of diagnosis and a 2020 indicator" | 3 — specification read from code; effect size unknown | R1 (single) | should_fix | re_analysis: logistic step 0 year specification | evidence_gap_remains; target table: Table 2 |
| S11 | State that 98 of 100 refers to intervals, and note the 0.00 lower bound | SC-34 | minor [SEVERITY-SOURCE: letter-fallback] | text: Abstract "stayed above 0 in 98 of 100 results" [R1 Minor Issues; DA minor list] | 4 [CONFIDENCE-SOURCE: report-level] | R1 (single); DA | should_fix | sentence: Abstract | interpretive_ambiguity_remains; target claim: "98 of 100" |
| S12 | Remove or qualify "lower is better" labels, especially for low-risk men; state once that a longer wait is not necessarily worse care | SC-37 | minor (R2 W4; R3 W6); DA M6 major | text: Abstract, Results "39.7% waited more than 90 days (lower is better)" | 4 — R2; 4 — R3; DA 4 | R2, R3 (corroborated); DA | should_fix | sentence: Abstract; Results; figure legends | interpretive_ambiguity_remains; target claim: normative direction of delay |
| S13 | Say "recorded clinical variables, which vary little within this group by definition" for the low-risk comparison | SC-38 | minor (R2 W5); DA M2 major | text: Abstract, Results "in low-risk men it added more than clinical need did." | 4 — R2; DA 4 | R2 (single); DA | should_fix | sentence: Abstract; Discussion Principal findings | claim_scope_unsupported; target claim: low-risk comparison |
| S14 | Present the active-surveillance exclusion as an assumption; cite the coding rule; report the share of intervals over 365 days and top-coded, by risk group | SC-39 | minor (R2 W6) | text: Methods, Active surveillance "Men whose first course was active surveillance have surgery and radiation coded as none, so they are not in this cohort." | 3 — coding rule not checked | R2 (single) | should_fix | sentence: Methods Active surveillance + section: supplement table | interpretive_ambiguity_remains; target section: Methods |
| S15 | Restrict the Huang et al. [22] claim to favourable-risk disease; use its rural surveillance finding in the selection discussion | SC-40 | minor (R2 W7) | text: Discussion, Marital status "This is consistent with higher use of surveillance or watchful waiting among unmarried men in an earlier SEER study [22]." | 4 — abstract checked in PubMed | R2 (single); DA | should_fix | sentence: Discussion Marital status | claim_scope_unsupported; target claim: citation [22] |
| S16 | Give the scope of Noone's 80% figure and carry its caution into the secondary-outcome interpretation | SC-41 | minor (R2 W8) | text: Limitations "Against Medicare claims, SEER identified radiation therapy with 80% sensitivity [20]." | 4 — abstract checked in PubMed | R2 (single) | should_fix | sentence: Limitations; Discussion | claim_scope_unsupported; target claim: citation [20] |
| S17 | Replace "corresponds to" with candidate-analogue wording in Supplementary Box 2; avoid "remote" for US counties | SC-42 | minor (R2 W9; R3 W8) | text: Supplementary Box 2 "the Rural-Urban Continuum Code corresponds to Australian Statistical Geography Standard remoteness areas, assigned by residential postcode." | 3 — R2 adjacent; 3 — R3 | R2, R3 (corroborated) | should_fix | sentence: Supplementary Box 2; Results terminology | claim_scope_unsupported; target section: Supplementary Box 2 |
| S18 | Attribute the waiting-time paradox to [10] and the triage explanation to the authors or a prostate-specific source | SC-43 | minor (R2 W11) | text: Introduction "Men with aggressive disease are treated sooner, which is why unadjusted comparisons of waiting time and survival can run in the wrong direction [10]." | 4 — abstract checked in PubMed | R2 (single) | should_fix | sentence: Introduction | claim_scope_unsupported; target claim: citation [10] |
| S19 | Set the metropolitan direction and the 2010 to 2022 rise against evidence on large centres and time trends (e.g. Khorana 2019) | SC-44 | minor (R2 W12) | text: Discussion, The rural direction "The data cannot test explanations such as longer surgical queues in large centres, second opinions, or wider choice of treatment settings." | 4 — record checked in PubMed | R2 (single); DA | should_fix | section: Discussion | evidence_gap_remains; target section: Discussion |
| S20 | Name the SEER variables for clinical Gleason score and PSA in the manuscript | SC-45 | minor (R2 W13) | absence: Methods and Declarations — expected completed STROBE and RECORD checklists, an ethics statement, SEER variable names for clinical Gleason score and PSA, and a code repository link; checked Methods, Declarations, Reporting checklists section, Supplementary material | 4 — reporting guideline cited by the manuscript | R2 (single) | should_fix | sentence: Methods Clinical risk groups | reporting_requirement_unmet; target section: Methods |
| S21 | Report excess waiting days per man, the top-coded share, and why the 7-day threshold could not be applied | SC-47 | minor (R3 W7) | table: Supplementary Table S11, all men — 30,597 and 20,014 crude excess days per 1,000 men | 3 — adjacent field | R3 (single); DA | should_fix | sentence: Results; Supplementary Table S11 | interpretive_ambiguity_remains; target table: Supplementary Table S11 |
| S22 | Restore the Foley 2025 restriction (men not treated with external beam radiotherapy) in the Discussion | SC-48 | minor (R3 W9) | text: Discussion, What an Australian registry could add "They reported an adjusted difference of 9.25 days by remoteness, and of 42 to 59 days between public and private facilities" | 4 — verified against PROTOCOL.md | R3 (single) | should_fix | sentence: Discussion | claim_scope_unsupported; target claim: Foley 2025 estimate |
| S23 | State the fractional-rank tie rule and whether delay was need-standardised for the concentration index | SC-49 | minor (R3 W11) | absence: Methods, Income inequality — expected the fractional-rank rule for men tied within county income bands and whether delay was need-standardised; checked Methods Income inequality, Supplementary Table S12, Figure 4 legend | 4 — core expertise | R3 (single) | should_fix | sentence: Methods Income inequality | method_reproducibility_unresolved; target section: Methods |
| S24 | State that sensitivity scenarios reuse largely the same men, so agreement is not independent replication | — | minor (DA minor list) | text: Discussion "consistent across ... ten sensitivity analyses" [DA minor list locator] | — (DA minor list; no per-finding confidence) [CONFIDENCE-SOURCE: report-level] | DA | consider | sentence: Discussion | interpretive_ambiguity_remains; target claim: consistency across sensitivity analyses |
| S25 | Address whether the SEER diagnosis date is a comparable start point across registries, years and settings (raised as a question, not an established defect) | — | [SEVERITY-SOURCE: letter-fallback] minor | absence: Discussion — expected discussion of start-date recording consistency; checked per DA Unexamined premise | — [CONFIDENCE-SOURCE: report-level] | DA | consider | sentence: Discussion Limitations | evidence_gap_remains; target section: Limitations |

## Source-Traceability Checklist

> Immutable source order. This is not a work order. Author triage (`will_address`, `wont_address`, `not_on_point`) is collected later in a separate sidecar.

- [ ] R1 — obligation `must_fix`: Interpretive anchor for the skill increment (REV-1)
- [ ] S1 — obligation `should_fix`: Replace the AUC example (REV-2)
- [ ] R2 — obligation `must_fix`: Low-risk share with its denominator (REV-3)
- [ ] R3 — obligation `must_fix`: Direction stated for the joint area contrast only (REV-4)
- [ ] R4 — obligation `must_fix`: Concentration-index caveat restored (REV-5)
- [ ] R5 — obligation `must_fix`: Title names the estimand (REV-6)
- [ ] R6 — obligation `must_fix`: Australian material placed as context (REV-7)
- [ ] R7 — obligation `must_fix`: 90-day threshold rationale for US data (REV-8)
- [ ] R8 — obligation `must_fix`: Verifiable protocol timing (REV-9)
- [ ] R9 — obligation `must_fix`: Code repository link (REV-10)
- [ ] R10 — obligation `must_fix`: Reporting checklists (REV-11)
- [ ] R11 — obligation `must_fix`: Declarations (REV-12)
- [ ] R12 — obligation `must_fix`: Leave-one-variable-out range (REV-13)
- [ ] R13 — obligation `must_fix`: High-risk standardised difference (REV-14)
- [ ] S2 — obligation `should_fix`: "Models disagree" label (REV-15)
- [ ] S3 — obligation `should_fix`: Secondary-outcome grid-edge disclosure (REV-16)
- [ ] S4 — obligation `should_fix`: Prose exposition and shorter abstract (REV-17)
- [ ] R14 — obligation `must_fix`: Strengths wording on uncertainty (REV-18)
- [ ] S5 — obligation `should_fix`: Figure scales (REV-19)
- [ ] S6 — obligation `should_fix`: Income band labelling (REV-20)
- [ ] R15 — obligation `must_fix`: Accurate description of prior work and hedged novelty (REV-21)
- [ ] R16 — obligation `must_fix`: Closest precedents cited and positioned (REV-22)
- [ ] R17 — obligation `must_fix`: Model-fitting and cross-fitting uncertainty in headline intervals (REV-23)
- [ ] R18 — obligation `must_fix`: Bootstrap clustering unit and cell sizes (REV-24)
- [ ] R19 — obligation `must_fix`: Per-step tuning (REV-25)
- [ ] R20 — obligation `must_fix`: One-at-a-time profile table (REV-26)
- [ ] R21 — obligation `must_fix`: Post hoc labels for agreement rule and dropped intervals (REV-27)
- [ ] R22 — obligation `must_fix`: Year-aware concentration index (REV-28)
- [ ] S7 — obligation `should_fix`: Weighting precision claim (REV-29)
- [ ] S8 — obligation `should_fix`: TRIPOD+AI prediction-model items (REV-30)
- [ ] S9 — obligation `should_fix`: Model-comparison uncertainty caveat (REV-31)
- [ ] S10 — obligation `should_fix`: Year specification in logistic base model (REV-32)
- [ ] R23 — obligation `must_fix`: Conditioning on recorded curative treatment (REV-33)
- [ ] S11 — obligation `should_fix`: "98 of 100" wording (REV-34)
- [ ] R24 — obligation `must_fix`: Hormone therapy and the triage reading (REV-35)
- [ ] R25 — obligation `must_fix`: Risk-group construction described accurately (REV-36)
- [ ] S12 — obligation `should_fix`: "Lower is better" labels (REV-37)
- [ ] S13 — obligation `should_fix`: Low-risk narrow-stratum wording (REV-38)
- [ ] S14 — obligation `should_fix`: Active-surveillance exclusion as assumption (REV-39)
- [ ] S15 — obligation `should_fix`: Huang et al. [22] scope (REV-40)
- [ ] S16 — obligation `should_fix`: Noone 80% context (REV-41)
- [ ] S17 — obligation `should_fix`: Area-measure equivalence wording (REV-42)
- [ ] S18 — obligation `should_fix`: Ang et al. [10] attribution (REV-43)
- [ ] S19 — obligation `should_fix`: Large centres and time-trend literature (REV-44)
- [ ] S20 — obligation `should_fix`: SEER Gleason and PSA variable names (REV-45)
- [ ] R26 — obligation `must_fix`: The "social position" label (REV-46)
- [ ] S21 — obligation `should_fix`: Excess waiting days metric (REV-47)
- [ ] S22 — obligation `should_fix`: Foley 2025 population restriction (REV-48)
- [ ] S23 — obligation `should_fix`: Concentration-index tie rule and need standardisation (REV-49)
- [ ] S24 — obligation `consider`: Sensitivity agreement is not independent replication (REV-50)
- [ ] S25 — obligation `consider`: Comparability of the SEER diagnosis date as start point (REV-51)

## Journal-Supplied Deadline (Optional Transport)

- **Exact deadline from source letter**: NOT PROVIDED
- No deadline, duration or work estimate is inferred.

## Response Letter Instructions

Use `templates/revision_response_template.md` to respond item by item. The response must include:
1. A response and revision description for each Required Revision (R1 to R26).
2. A response for each Suggested Revision (S1 to S25), whether adopted or not, with the reason if not.
3. A response to each DA MAJOR finding (M1 to M8) through its mapped roadmap item, including DA M6, whose severity exceeds the non-DA seats.
4. Tracked changes in the revised manuscript.
5. A cross-reference table to the revised sections.

---

# Part 3: Reviewer Report Summary (Appendix)

### Journal-Fit Review Report Summary (EIC)
- Recommendation: major revision (preliminary quality signal) | Confidence: not stated at report level (per-finding 3 to 5)
- Key point: the contribution is "real but modest". The skill increment's significance is asserted rather than argued, the Conclusions over-attribute an income direction, the benchmark and title are unjustified, and pre-specification and code cannot yet be verified.

### Reviewer 1 (Methodology) Summary
- Recommendation: Major Revision | Confidence: 4
- Key point: the design is transparent and most numbers match, but the headline intervals omit fitting and cross-fitting variability, tuning reuse inflates the LightGBM increment in two strata, and the post hoc profile switch hides a model conflict (D1 block, repairable).

### Reviewer 2 (Domain) Summary
- Recommendation: not stated (D2 block, repairable) | Confidence: not stated at report level (per-finding 3 to 5)
- Key point: the triage interpretation ignores hormone therapy ending the interval, risk groups are misdescribed as clinical-only, and the account of prior work omits the closest analogues.

### Reviewer 3 (Perspective) Summary
- Recommendation: not stated (D4 warn) | Confidence: not stated at report level (per-finding 3 to 4)
- Key point: the framing is mostly careful and makes no implied Australian comparison, but the income-gradient reading, the unconditioned direction statement, the "social position" label and the unbridged estimand size overstate what equity and policy readers can take away.

### Devil's Advocate Summary
- Recommendation: not stated (D3 block, repairable; CRITICAL 0, MAJOR 8) | Confidence: per-finding 3 to 5
- Key point: the paper may have measured a registry-and-geography signal and named it social position. The separate rural and income directions, the low-risk comparison and the normative framing exceed the evidence.
