# Round 1 reviewer card: eic

contract_role: eic
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: warn
trigger: "claimed reporting guideline items that are missing or hard to find"

### D6: venue_fit_and_contribution
score: warn
trigger: "The contribution is real but under-articulated or overstated in places"

## Review Body

Reviewer identity (Card #1): senior editor for cancer health services research, field-general. Criteria binding is unavailable, so no venue-alignment claim is made. Contribution and structure are judged against general norms for registry-based health services research.

### Summary Assessment

The manuscript uses SEER 17 data on 330,827 men treated with radical prostatectomy or radiotherapy. It measures how much out-of-fold log-loss skill social position (marital status, county rurality, county income) adds to predicting a wait of more than 90 days, beyond year and recorded clinical need, within clinical risk groups and with two model types. It adds standardised contrasts, an income concentration index, selection bounds and 10 sensitivity scenarios. I checked many reported numbers against the generated analysis reports (reports/phase3.md, phase4_descriptive.md, phase4_models.md, phase4_equity_selection.md, phase4_sensitivity.md, phase4_receipt.md). Almost all match and are used in the right context. The exceptions are listed as W7 and W8.

The contribution is real but modest. It is careful about what registry data cannot show and states clearly that no Australian data were analysed. Editorially, four things weaken it:
- The central quantity (percentage points of log-loss skill) is not made interpretable, and its significance is asserted rather than argued (W1).
- One headline direction statement attributes a separate signal to lower-income counties that the analysis does not isolate (W2).
- Using an Australian benchmark for US data, and a title built around clinical need, are not justified for a general reader (W3).
- Readers cannot verify the protocol timing or the code (W4).

Declarations and reporting checklists are still placeholders (W5, W6). Preliminary overall quality signal for synthesis: major revision. The core analysis looks sound within my competence, but the framing, interpretation and transparency items need substantial rewriting before the contribution can be judged at full value.

### S1: Explicit boundary against cross-country comparison
The Discussion states directly that the US direction cannot be compared with Tasmanian findings. It limits what transfers to the measurement approach, which avoids an implied comparison the data cannot support.
**Evidence Anchor**: text: Discussion, Relevance to Australian pathway research "No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings."

### S2: Candid disclosure of post hoc decisions
The two amendments made after seeing results are named in Methods and listed again as a limitation. The full amendment log is in the supplement.
**Evidence Anchor**: text: Methods, Protocol "Two were made after seeing results and are labelled that way"

### S3: Two-model design tests a real alternative explanation
The comparison of penalised regression and LightGBM tests whether an under-fitted clinical model could create the social increment. The answer is reported plainly.
**Evidence Anchor**: text: Discussion, The machine learning comparison "A more flexible clinical adjustment therefore did not absorb the social signal."

### S4: Tables faithful to the analysis outputs
Table 2 reproduces the generated model report exactly, including intervals and the share of step 2 skill. The supplement carries the full step-by-step performance table.
**Evidence Anchor**: table: Table 2 — all men, social position added 0.62 (0.39 to 0.87) and 0.99 (0.73 to 1.30), identical to reports/phase4_models.md

### S5: Selection handled transparently
Worst-case bounds are reported for men without a recorded interval. The rurality ordering survives the extreme assumptions, which guards the descriptive direction against one obvious selection explanation.
**Evidence Anchor**: table: Supplementary Table S14 — bounds 40.2 to 45.7% (large metro) against 31.3 to 34.0% (nonmetro, not adjacent)

### S6: Honest statement of review status
The manuscript discloses that the analysis was done by one person with AI coding assistance and has not been reviewed by a clinician or biostatistician.
**Evidence Anchor**: text: Discussion, Limitations "the analysis was done by one person with AI coding assistance and has not been reviewed by a clinician or biostatistician"

### W1: Significance of the log-loss skill increment is asserted, not argued
**Problem**: The headline result is an increment of 0.42 to 1.37 percentage points of log-loss skill, but the manuscript gives a health services reader no basis for judging whether that is large or small.
- The protocol set a meaningful-difference threshold for standardised contrasts (3 points), but none for skill increments.
- The only argument that "a small gain can still be informative" is a cited study where AUC moved from 0.671 to 0.673. That example shows a small gain, not that one is informative.
- The abstract and Results say that in low-risk men social position "added more than clinical need did", making up 82% and 98% of step 2 skill. Total step 2 skill in that stratum is only 0.76 and 0.99 points (Table 2), so a share of a near-zero total can mislead.
**Evidence Anchor**: text: Introduction "in one US health system, adding neighbourhood variables to a clinical model predicting advanced prostate cancer changed the AUC from 0.671 to 0.673"
**Why it matters**: The claimed contribution rests on the increment being "small but consistent" and still worth reporting. Without an interpretive anchor, readers cannot judge significance, and the low-risk share statement overstates relative importance.
**Suggestion**: Explain what a skill increment of this size means in patient terms. The standardised percentages already reported could be tied to it explicitly, or the increment compared with a benchmark such as the year or treatment-type increments. Replace the AUC example with a real argument, and give the low-risk share alongside the absolute step 2 skill wherever it appears.
**Severity**: Major
**Confidence**: 4 — core editorial competence in interpreting health services metrics; statistical detail of skill metrics is adjacent

### W2: Conclusion attributes a separate direction to lower-income counties
**Problem**: The Conclusions say the social signal "points to less delay, not more, in rural and lower-income counties". The Discussion says men in higher-income counties were more often delayed "after clinical features were held as observed". The analysis does not separate income:
- The standardised contrast is a joint area profile, with rurality and income set together.
- The Erreygers index is computed on the crude outcome within risk groups, and the source report notes it "does not separate income from rurality".
- Under logistic regression, removing income lost 0.00 to 0.02 points.
- One-at-a-time income contrasts were not interpreted because the models conflicted.
- Setting all social features to the reference profile changed the pooled percentage by only 1.1 and 1.6 points, under the paper's own 3-point rule.
**Evidence Anchor**: text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties"
**Why it matters**: This is a headline direction claim in the Conclusions and principal findings. It goes beyond what the joint area contrast and a crude concentration index can show.
**Suggestion**: Describe the direction as an area contrast (large metropolitan, higher-income counties against remote, lower-income counties), as the Results already do. State that the income index is not standardised for clinical features and does not separate income from rurality. Remove "after clinical features were held as observed" from any statement that relies on the concentration index.
**Severity**: Major
**Confidence**: 4 — checked against reports/phase4.md, phase4_equity_selection.md and phase4_models.md

### W3: Using an Australian benchmark for US data, and a clinical-need title, are not justified for readers
**Problem**:
- The title asks "how much is clinical need?", but the primary estimand is the increment added by social position.
- The Introduction opens with Australian and Tasmanian findings, including two lung cancer studies, before the US evidence.
- The 90-day outcome is justified only as the Australian pathway benchmark, although a cited US study [8] used the same threshold.
- The manuscript never explains to a general reader why a US registry study is judged against an Australian pathway. It also cites Tasmanian and US studies together as pointing "in different directions", which sits uneasily with the later statement that the two cannot be compared.
**Evidence Anchor**: text: Title "how much is clinical need?"
**Why it matters**: Readers need to see a coherent reason for the benchmark and a title that names the actual question. As written, the positioning of the contribution is harder to follow, and the Australian material takes space without data behind it.
**Suggestion**: Give a short, explicit rationale for the 90-day threshold that stands on its own for US data, noting that the same cut-off appears in US work. Move the Australian material to a clearly labelled context or transferability paragraph. Retitle so the title names the social-position increment, and shorten it.
**Severity**: Major
**Confidence**: 4 — core editorial competence in framing and title–estimand alignment

### W4: Pre-specification and reproducibility claims cannot yet be verified by readers
**Problem**:
- The Strengths list "A protocol fixed before modelling" and "Code that regenerates every table and figure".
- The protocol was not registered externally and is cited only as a file name.
- The code repository URL is a placeholder.
- Every amendment in Supplementary Table S32 carries the same date, so the order of amendments relative to model fitting cannot be seen from the manuscript.
**Evidence Anchor**: text: Methods, Protocol "It was committed to version control before the first cohort was built; it was not registered externally"
**Why it matters**: Pre-specification is the main defence against analytic flexibility, especially with two post hoc amendments. As presented, it is a claim readers must take on trust.
**Suggestion**: Before posting, give a public, timestamped link to the protocol and code, for example a tagged repository release or archived DOI. Add commit identifiers or times to the amendment log so the sequence against model fitting can be checked.
**Severity**: Major
**Confidence**: 4 — core editorial competence in transparency and reporting standards

### W5: Claimed reporting guideline adherence has no checklists
**Problem**: Methods state that reporting follows STROBE, RECORD and TRIPOD+AI, but the checklist section is a placeholder. Readers cannot find where each item is addressed.
**Evidence Anchor**: absence: Supplement, Reporting checklists — expected completed STROBE, RECORD and TRIPOD+AI checklists with section references; checked Methods (Reporting and ethics), Declarations, the final supplement section
**Why it matters**: A claim of guideline adherence cannot be checked without the checklists. Completing them may reveal items that are not reported.
**Suggestion**: Complete all three checklists with section references and address any items found missing.
**Severity**: Minor
**Confidence**: 5 — directly observable

### W6: Declarations are incomplete
**Problem**: The affiliation, ethics statement, funding, competing interests, code URL and AI-use disclosure are all placeholders.
**Evidence Anchor**: text: Declarations, Use of AI tools "[TO BE COMPLETED: disclosure statement]"
**Why it matters**: A health research manuscript is not complete for public posting without these statements.
**Suggestion**: Complete every declaration. Keep the existing description of AI assistance in the finished disclosure.
**Severity**: Minor
**Confidence**: 5 — directly observable

### W7: Leave-one-variable-out range misreported
**Problem**: Results say removing marital status or rurality "each lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata". Supplementary Table S8 shows 0.18 and 0.19 for intermediate risk under logistic regression. The same range appears in the phase 4 overview, but not in the generated model table.
**Evidence Anchor**: table: Supplementary Table S8 — intermediate risk, penalised logistic regression, marital status 0.18 and rurality 0.19
**Why it matters**: The text disagrees with the table. The conclusions do not change.
**Suggestion**: Correct the range to 0.18 to 0.45.
**Severity**: Minor
**Confidence**: 5 — checked against reports/phase4_models.md

### W8: Secondary-outcome area contrast misdescribed for high-risk men
**Problem**: The Discussion quotes crude high-risk percentages (75.3% against 81.9%) and says the standardised difference "was under 3 points". In high-risk men the contrast was -3.3 and -2.5, labelled "models disagree". Only the pooled contrast (-2.9 and -1.4) was under 3 points for both models.
**Evidence Anchor**: text: Discussion, The rural direction "although the standardised difference was under 3 points"
**Why it matters**: The number is used outside the stratum it belongs to.
**Suggestion**: Either say the pooled contrast was under 3 points, or say the models disagreed in high-risk men.
**Severity**: Minor
**Confidence**: 5 — checked against Supplementary Table S30 and reports/phase4_receipt.md

### W9: "Models disagree" label is misleading
**Problem**: Contrasts where both models point the same way but one falls below 3 points are labelled "models disagree". Readers are likely to take this as opposite directions.
**Evidence Anchor**: table: Table 3 — low risk, marital status 3.6 and 2.4 labelled "models disagree"
**Why it matters**: The label misstates the actual pattern in Table 3 and in Supplementary Tables S21 and S30.
**Suggestion**: Use a label such as "same direction, below 3 points in one model".
**Severity**: Minor
**Confidence**: 5 — directly observable

### W10: A tuning limitation for the secondary outcome is not reported
**Problem**: The source report states that, for the secondary outcome, logistic regression chose C at an edge of the grid in intermediate risk (0.01) and high risk (10). It calls this a limitation that was not re-tuned. The manuscript reports the grid edge for the primary analysis only.
**Evidence Anchor**: absence: Results (Secondary outcome) and Limitations — expected a statement that logistic regression chose C at a grid edge in intermediate and high risk for the secondary outcome, as in reports/phase4_receipt.md; checked Methods (Secondary outcome), Results (Secondary outcome), Limitations, Supplementary Tables S25 to S31
**Why it matters**: A limitation known from the source analysis is left out of the manuscript.
**Suggestion**: Report the chosen C values for the secondary outcome and state the grid-edge limitation.
**Severity**: Minor
**Confidence**: 5 — checked against reports/phase4_receipt.md

### W11: Bullet-list exposition and a long abstract
**Problem**: The Introduction, Methods, Results and Discussion are written mainly as nested bullet lists, and the gap argument is never developed in prose. The structured abstract runs to about 430 words with nested bullets and repeats most of the Results.
**Evidence Anchor**: text: Abstract, Results (nested bullets) "Social position increment"
**Why it matters**: Research articles in this field are normally read as connected argument. The bullet form breaks the line of reasoning from gap to conclusion.
**Suggestion**: Rewrite the Introduction and Discussion as prose. Shorten the abstract to the primary estimand, the key contrasts and the main limitation.
**Severity**: Minor
**Confidence**: 4 — editorial convention, field-general

### W12: Strengths list overstates the uncertainty design
**Problem**: The Strengths claim uncertainty that "respects county-level exposures". The export has no county identifier, and resampling is over 79 rurality by income cells, not counties.
**Evidence Anchor**: text: Discussion, Strengths "Uncertainty that respects county-level exposures"
**Why it matters**: A strength should not claim more than the Methods describe.
**Suggestion**: Reword to describe a cluster bootstrap over rurality by income cells, used as a proxy because no county identifier exists.
**Severity**: Minor
**Confidence**: 4 — wording checked against Methods; adequacy of the bootstrap design is outside my focus

### W13: Figure scales can mislead visual comparison
**Problem**:
- The three panels of Figure 3 use different x-axis ranges, so treatment type and social position look similar in size to clinical need.
- In Figure 4b the five concentration curves overlap almost completely and are hard to tell apart.
- The x-axis of Figure 4a starts near 31%, not 0.
**Evidence Anchor**: figure: Figure 3 — panel x-axis ranges 0 to 4, 0 to 2 and 0 to 1
**Why it matters**: Readers compare dot positions across panels, so different scales can give a wrong impression of relative size.
**Suggestion**: Use a common x-axis in Figure 3, or say clearly in the caption that scales differ. Consider showing Figure 4b as the difference from the line of equality, or dropping it in favour of Supplementary Table S12. Note the truncated axis in the Figure 4a caption.
**Severity**: Minor
**Confidence**: 4 — direct inspection of the figure files

### W14: Income band labelling in Table 1 is confusing
**Problem**: The "quartile of 16 bands" income groups are quartiles of bands, not of men. Q1 holds 8.0% of men and Q4 32.8%, which readers will not expect from the word quartile.
**Evidence Anchor**: table: Table 1 — County median household income (quartile of 16 bands), Q1 8.0% and Q4 32.8% of men
**Why it matters**: Income contrasts and the text rely on these groups.
**Suggestion**: Rename the groups (for example, band groups 1 to 4) and give the dollar range of each in a table note.
**Severity**: Minor
**Confidence**: 5 — directly observable

### W15: Research gap described through a narrow set of studies
**Problem**: The novelty claim rests on describing earlier work as reporting "adjusted associations for one factor at a time", based on four cited US studies. The manuscript does not say how the literature was reviewed. The closest methodological precedent [11], which adds neighbourhood variables to a clinical prediction model, is cited as support rather than positioned as prior incremental-value work.
**Evidence Anchor**: text: Introduction "These studies report adjusted associations for one factor at a time, usually pooled across risk groups."
**Why it matters**: The contribution is a new use of an incremental-value approach, not a new method. Positioning it candidly would make the gap claim easier to defend.
**Suggestion**: Briefly describe how prior work was identified. Present incremental-value analyses in adjacent prostate cancer questions as precedent, and state the novelty as applying that approach to timeliness within risk groups with selection bounds.
**Severity**: Minor
**Confidence**: 3 — completeness of the domain literature is better judged by a domain specialist

### Questions for Authors
1. What size of social-position skill increment would you consider meaningful for health services decisions, and how does 0.62 to 0.99 points relate to the standardised percentages?
2. Can a timestamped public record (commit identifiers or an archived release) show that the protocol version used for the primary estimand came before the first outcome model was fitted?
3. Apart from the Australian benchmark, what is the rationale for the 90-day threshold in US data, and would the title and Introduction change if it were presented on that basis?


# Round 1 reviewer card: methodology

## Methodology Review Report (Peer Reviewer 1)

Reviewer identity: biostatistician specialising in clinical prediction model evaluation and reporting (TRIPOD+AI), cross-fitting, calibration assessment, clustered resampling and g-computation (Reviewer Configuration Card #2). Criteria binding unavailable: no venue-alignment claim is made.

contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: block
trigger: "uncertainty intervals that do not reflect the stated resampling"
block_class: repairable

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: warn
trigger: "a secondary claim with thin supporting analysis"

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

**Overall recommendation:** Major Revision. **Reviewer confidence:** 4 of 5.

**Summary assessment.** The design is sensible and unusually transparent for a single-analyst registry study. There is a dated protocol with an amendment log, fold assignments are shared across steps, calibration is reported, missing intervals are bounded, and the ten one-change sensitivity analyses are shown in full. I checked the main-text numbers against Tables 1 to 3, Supplementary Tables S1 to S32 and the Phase 3/4 source reports. Almost all match. D1 is blocked (repairable) for three analysis-level reasons.
- **Headline intervals:** the intervals for the primary estimand resample fixed out-of-fold losses over 79 rurality by income cells. They leave out the model-fitting, tuning and cross-fitting variability of the stated validation design. The authors themselves reject this kind of interval for the standardised contrasts.
- **Tuning reused across steps:** hyperparameters tuned on the step 3 feature set are reused at step 1. In the low-risk and unknown-risk strata this goes with a miscalibrated, weaker LightGBM clinical model. That inflates the LightGBM social increment there and weakens the argument that a flexible clinical adjustment did not absorb the social signal.
- **Post hoc switch to area profiles:** the switch was prompted by the two model types disagreeing on how much of the gap is rurality and how much is income. The main text does not report that disagreement, and the supplementary table the amendment log promises is missing.

The income concentration index is crude and pooled over 2010 to 2022, while county income is linked by year. D3 is warn: the model-comparison inference and some carried-over wording go beyond the supporting analyses, but the main thesis survives. All three fixes are repairable with existing data and code.

### S1: Protocol, amendment log and post hoc labelling
The protocol, a 12-entry dated amendment log (S32) and explicit post hoc labels make the analytic history auditable. That is a real strength, despite the labelling gap in W3.
**Evidence Anchor**: text: Methods, Design, data and protocol "Two were made after seeing results and are labelled that way"

### S2: Out-of-fold calibration reported by stratum and model
Calibration intercepts and slopes are reported at every step (S7), and binned calibration plots are shown at step 2. Folds are drawn with a fixed seed, so every step is evaluated on the same partition (`models.fold_ids`) and the increments are paired comparisons.
**Evidence Anchor**: figure: Supplementary Figure S1, calibration of out-of-fold step 2 predictions in 10 equal-count bins by stratum and model

### S3: Bounds and membership model for men without an interval
The worst-case bounds, the social-position increment for having no interval, and the reweighting are all reported. The rurality ordering holds at the extremes. The code (`selection.delay_bounds`) matches the description.
**Evidence Anchor**: table: Supplementary Table S14, lower and upper bounds by rurality (large metro 40.2 to 45.7, remote 31.3 to 34.0)

### S4: Sensitivity analyses reported in full
Every scenario, stratum and model cell is shown with its interval, not just a summary. The two cells whose intervals include 0 are named in the source report, and the counts in the text (98 of 100, 47 of 50) match it.
**Evidence Anchor**: table: Supplementary Table S20, social position increment with intervals for 10 scenarios, 5 strata and 2 models

### S5: Grid-edge check carried out and shown
The re-tune on the wider grid addresses the grid-edge concern directly. It is labelled post hoc and its results are shown side by side.
**Evidence Anchor**: table: Supplementary Table S24, wider C grid again chose C = 0.01 in every stratum with identical increments

### W1: Primary-estimand intervals leave out model-fitting and cross-fitting uncertainty, and cluster on cells rather than counties or registries
**What the code does:** `increments.bootstrap_increments` resamples rurality by income cells and recomputes skill from fixed out-of-fold pointwise losses. It does not refit, re-tune or redraw folds.

**Why this is a problem**
- **Missing variability:** the intervals capture only test-set sampling of the losses. The stated design has 5-fold cross-fitting and data-driven tuning, and neither source of variability is propagated.
- **The authors' own standard:** the manuscript declines this construction for the standardised contrasts because it "ignore[s] model-fitting uncertainty". The source report (`reports/phase4_equity_selection.md`, A5) adds that such intervals are "far narrower than the disagreement between model types". The same construction still underpins the headline claims "intervals above 0 in every risk group" and "98 of 100".
- **Cells are not the dependence unit:** the 79 cells are defined by the exposures themselves, not by county or registry. Registry practice, which the authors say may load onto the social block, cuts across cells. County income and rurality are linked by year (reference 13), so one county may fall in more than one cell over time.
- **Cluster sizes unreported:** the manuscript gives neither the number of cells per stratum nor their sizes. Large metropolitan counties alone hold 194,681 men (Table 1), so a few cells probably dominate every resample.
- **Overstated strength:** the Strengths list claims "Uncertainty that respects county-level exposures".

**Minimum remedy**
- Repeat the cross-fitting with several fold seeds and report the spread of the increment.
- Report the cell count and size distribution for each stratum.
- Qualify the Strengths wording.

**Stronger option:** a cluster bootstrap that refits steps 1 and 2 in each resample, perhaps on fewer resamples or a subsample. Add a sensitivity analysis with an alternative clustering, for example cells crossed with diagnosis period.

**Severity**: Major
**Evidence Anchor**: text: Methods, Models and validation, Uncertainty "500 resamples of out-of-fold predictions, percentile intervals, no refitting"
**Confidence**: 4 — resampling design read directly from `increments.py` and `run_phase4_models.py`

### W2: Tuning on the step 3 feature set, reused at step 1, inflates the LightGBM increment in low-risk and unknown-risk men
Hyperparameters were tuned once, on step 3, and reused at every step. The tuning sample is 50,000 of 57,495 low-risk men, and all 14,817 unknown-risk men, because the code only subsamples when a stratum exceeds 50,000.

**What the step 1 results show (S7)**
| Stratum | LightGBM step 1 skill | Logistic regression step 1 skill | LightGBM step 1 calibration slope |
|---|---|---|---|
| Low risk | 0.02 | 0.14 | 0.883 |
| Unknown risk | 0.59 | 0.65 | 0.850 |

In these two strata the flexible clinical model is both worse and more over-dispersed than the penalised model, and LightGBM's clinical-need interval includes 0 in low risk (-0.09 to 0.13). This pattern fits a step 3 configuration that is too flexible for the smaller step 1 feature set. A weak step 1 reference raises the step 1 to step 2 increment: 0.96 and 1.37, and "98%" of step 2 skill in low risk.

**Claims affected**
- The Discussion inference "A more flexible clinical adjustment therefore did not absorb the social signal" rests on LightGBM's larger increment. It is supported only where LightGBM's step 1 beats logistic regression's: the pooled, intermediate-risk and high-risk strata.
- The wider-C re-tune (S24) addresses the logistic grid only, not this issue.

**Minimum remedy:** tune separately at each step, or at least at step 1 and step 2. Report the resulting increments, and limit the model-comparison inference to strata where the flexible clinical model is at least as good.

**Severity**: Major
**Evidence Anchor**: table: Supplementary Table S7, low risk, LightGBM, step 1 log-loss skill 0.02 and calibration slope 0.883 against penalised logistic regression 0.14 and 0.998
**Confidence**: 4 — values read from S7; the mechanism is inferred, not tested

### W3: The post hoc switch to joint area profiles hides a model conflict, and the promised supplementary table is missing
**What the amendment log says:** amendment 1.7 (S32) was "Prompted by the model disagreement seen in the development run". It promises that the one-at-a-time results are "kept in a supplementary table", but no such table appears in S1 to S32.

**What the source report shows** (`reports/phase4_equity_selection.md`, all men)
| Change to the profile | Logistic regression | LightGBM |
|---|---|---|
| Rurality only, large metro to remote | -8.7 points | +1.7 points |
| County income only, Q4 to Q1 | -0.9 points | -8.7 points |

Under one model the gap is carried by rurality; under the other it is carried by income. The joint area contrast (-9.2 and -8.8) agrees only because it cannot separate the two. The leave-one-variable-out results (S8, income 0.00 to 0.02 against 0.26 to 0.29) point the same way.

**What the main text does**
- It labels only the profile change as post hoc.
- It presents the "3 points or more, same direction" rule and the dropping of intervals without a post hoc label, although both came from the same amendment. Protocol section 6 had pre-specified "estimates with 95% intervals".
- The abstract gives the area and marital differences with no statement that they lack uncertainty measures.
- The Discussion paragraph "The rural direction" reads a joint area contrast as a rurality finding.

**Minimum remedy**
- Publish the one-at-a-time table, including these values.
- Label the agreement rule and the dropped intervals as post hoc in Methods and the abstract.
- Describe the area contrast as rurality and income combined throughout.

**Stronger option:** refit-based bootstrap intervals for the joint contrasts, as in W1.

**Severity**: Major
**Evidence Anchor**: text: Supplementary Table S32, amendment version 1.7 "with the one-at-a-time results kept in a supplementary table"
**Confidence**: 5 — amendment text, supplement contents and source report compared directly

### W4: The income concentration index is crude, pooled over years, and ranked on a time-linked income variable
**What the code does:** the Erreygers index uses only the delay indicator and the county income band rank within each risk stratum. There is no adjustment for or stratification by year (`run_phase4_equity_selection.py`, A6).

**Why this matters**
- County income is inflation-adjusted and linked by year (reference 13), and the delay rate rose from 36.0% in 2010 to 52.3% in 2022 (S6). If income bands drift with diagnosis year, the secular trend loads onto the index.
- The manuscript does not report whether bands drift with year, so the size of any such effect cannot be judged.
- The source overview (`reports/phase4.md`, section 4) states that "this index does not separate income from rurality". That caveat is absent from the manuscript's Income inequality results and from the abstract, which present the index next to the standardised results.

The formula itself is correct: E = 8 cov(y, R) for a 0/1 outcome, with average ranks for ties.

**Minimum remedy**
- Report the income rank distribution by diagnosis year.
- Add a year-stratified (or year-standardised) index.
- Restore the rurality caveat.

**Severity**: Major
**Evidence Anchor**: absence: Methods and Results, Income inequality — expected an index stratified or standardised by year of diagnosis, or a report of how county income band varies with diagnosis year; checked Methods Income inequality, Results Income inequality, Figure 4b legend, Supplementary Table S12, Limitations
**Confidence**: 3 — the pooling is confirmed in code; the size of any year and income drift is not shown in any available surface

### W5: A reported range for the leave-one-variable-out results does not match S8
The text gives 0.22 to 0.45 for removing marital status or rurality in the pooled, intermediate-risk and high-risk strata. S8 shows 0.18 and 0.19 (logistic regression) and 0.21 (LightGBM) for intermediate risk, so the range is 0.18 to 0.45. The error is also in `reports/phase4.md`, section 2, so it came from the overview report. The claim that weighting changed percentages by "0.2 points or less" cannot be confirmed at the displayed precision: county income Unknown (n = 30) is shown as 39.3 unweighted and 39.6 weighted.
**Severity**: Minor
**Evidence Anchor**: text: Results, Which social variable "Removing marital status or rurality each lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata"
**Confidence**: 5 — direct table comparison

### W6: A grid-edge choice in the secondary-outcome tuning is not disclosed
The source report (`reports/phase4_receipt.md`) records that logistic regression chose C = 0.01 in intermediate risk and C = 10 in high risk. Both are grid edges, and neither was re-tuned. The manuscript discloses and checks the grid edge for the primary outcome only.
**Severity**: Minor
**Evidence Anchor**: absence: Secondary outcome Methods and Results — expected disclosure that penalised logistic regression chose C at an edge of the grid in the intermediate-risk and high-risk strata; checked Methods Secondary outcome, Results Secondary outcome, Supplementary Tables S29 to S31, Limitations
**Confidence**: 4 — source report compared with manuscript

### W7: Reporting-guideline adherence is claimed but not yet shown
The manuscript claims STROBE, RECORD and TRIPOD+AI adherence, but the checklist section is a placeholder and the code repository URL is missing. That makes "every table and figure is regenerated by scripts with unit tests" unverifiable for readers. Prediction-model items not yet covered:
- how LightGBM handles missing Gleason and PSA values (only median imputation for logistic regression is described);
- the exact interaction terms, and whether the fitted models are available;
- performance by social subgroup;
- the number and size of bootstrap clusters.
**Severity**: Minor
**Evidence Anchor**: text: Reporting checklists "IN PREPARATION: STROBE, RECORD and TRIPOD+AI checklists with page references."
**Confidence**: 4 — manuscript surfaces and code checked

### W8: The model comparison is stated without uncertainty, and the source caveat was dropped
The source overview says of the difference between LightGBM and logistic regression that "No interval was computed for this difference". The abstract and Results state the comparison without that caveat. Several differences are small (0.23 points in low risk), and three sensitivity combinations reverse (source report).
**Severity**: Minor
**Evidence Anchor**: text: Abstract, Results "LightGBM had higher out-of-fold skill than penalised logistic regression in every risk group."
**Confidence**: 4 — compared with `reports/phase4.md`

### W9: The logistic base model is linear in year while delay is not
In the code, step 0 enters year as one numeric term plus a 2020 indicator. Interactions for logistic regression are among clinical columns only. Crude delay is non-monotone: 36.0% in 2010, 33.5% in 2013, 52.3% in 2022 (S6). Under logistic regression, leftover year signal could be absorbed by the time-linked county attributes at step 2. LightGBM models year flexibly, so this does not explain its increment.

**Remedy:** enter year as categories or a spline, and report the logistic increment.
**Severity**: Minor
**Evidence Anchor**: text: Methods, Ordered feature steps "year of diagnosis and a 2020 indicator"
**Confidence**: 3 — specification read from `features.py` and `run_phase4_models.py`; effect size unknown

### W10: The directional conclusions leave out that the cohort is conditioned on recorded curative treatment
Recorded curative treatment is itself patterned by social position. The secondary increment is 1.96 and 2.16 points, larger than the primary increment. Crude receipt is 75.3% in remote and 81.9% in large metro counties for high-risk men. The bounds cover men without an interval, not men without a recorded treatment. The Conclusions state the direction without this conditioning.
**Severity**: Minor
**Evidence Anchor**: text: Conclusions "points to less delay, not more, in rural and lower-income counties"
**Confidence**: 3 — the selection mechanism overlaps with the devil's advocate and domain seats

### Detailed Comments
- **Research question and estimand:** the step 1 to step 2 log-loss skill increment is a coherent measure of added predictive signal. It is scaled by the step 0 log-loss of each stratum, so readers should not compare increments across strata as absolute amounts. AUC changes (S7) help interpretation and could be cited next to the headline.
- **Cohort and data:** the flow counts match `reports/phase3.md` at every step. Treatment code lists match `config/analysis.yaml`, and the risk-group logic matches the protocol.
- **Leakage:** imputation and scaling are fitted inside each training fold, so there is no predictor-processing leakage. Tuning is not nested (disclosed). Its main consequence is the per-step issue in W2, not generic optimism.
- **g-computation:** the standardisation code matches the description: a step 2 model fitted to all men, social columns overwritten, predictions averaged. The marital contrast is evaluated at the reference area and income, which is correct as labelled.
- **Arithmetic cross-checks (reporting-only, no bounded procedure):** these matched their source tables within rounding.
  - Abstract, Results, Tables 2 and 3 against S7 to S24.
  - Bound identities in S13 and S14, e.g. unknown risk 42.1 × (1 - 0.144) = 36.0 and 36.1 + 14.4 = 50.5.
  - Standardised contrasts against the S10 profile values.
  - Secondary-outcome totals.

### Questions for Authors
1. How many bootstrap cells does each stratum have, and what is the largest cell's share of men?
2. How much does the social increment vary across different fold seeds, and across a refitting bootstrap?
3. What are the LightGBM step 1 and step 2 increments when hyperparameters are tuned separately at each step?
4. Does the county income band rank drift with diagnosis year, and what is the income index within periods?
5. Where is the one-at-a-time table that amendment 1.7 promises?

### Minor Issues
- The abstract says the increment "stayed above 0 in 98 of 100 results". The 98 refers to intervals; point estimates are above 0 in every cell. S20 shows one lower bound as 0.00 (threshold of 180 days, unknown risk, logistic regression), and it is counted as above 0.
- Supplementary Figure S1 shows step 2 only. The step 1 miscalibration in W2 is visible only in S7.

## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: table: Supplementary Table S3, low risk by Unknown rurality, % waited over 90 days 34.8, with n = 23 from Table 1 (low risk, Unknown rurality)
reported_inputs: reported percentage 34.8 at one decimal place, analytic N 23 (Table 1), outcome binary (waited more than 90 days, yes or no)
assumptions: every cohort member has a recorded interval above 0 days (inclusion step 8) so the percentage is 100 times a mean of 23 binary values, rounding rule not stated but the attainable value is not near an interval boundary
derivation: 100 times k/23 for integer k, k = 8 gives 34.7826 which lies inside [34.75, 34.85)
derived_value_or_range: 8/23 = 34.7826%
comparison_rule: reachable when some integer k makes 100 times k/N fall inside the rounding interval of the reported value
rounding_interval: [34.75, 34.85)
nearest_achievable: 7/23 = 30.4348%, 8/23 = 34.7826%, 9/23 = 39.1304%
status: consistent

### AR2
procedure_id: grim
evidence_anchor: table: Supplementary Table S3, intermediate risk by Unknown rurality, % waited over 90 days 42.5, with n = 40 from Table 1 (intermediate risk, Unknown rurality)
reported_inputs: reported percentage 42.5 at one decimal place, analytic N 40 (Table 1), outcome binary
assumptions: every cohort member has a recorded interval above 0 days so the percentage is 100 times a mean of 40 binary values, rounding rule not stated but the attainable value is exact
derivation: 100 times k/40 for integer k, k = 17 gives exactly 42.5
derived_value_or_range: 17/40 = 42.5000%
comparison_rule: reachable when some integer k makes 100 times k/N fall inside the rounding interval of the reported value
rounding_interval: [42.45, 42.55)
nearest_achievable: 16/40 = 40.0000%, 17/40 = 42.5000%, 18/40 = 45.0000%
status: consistent

### AR3
procedure_id: grim
evidence_anchor: table: Supplementary Table S3, high risk by Unknown rurality, % waited over 90 days 28.4, with n = 88 from Table 1 (high risk, Unknown rurality)
reported_inputs: reported percentage 28.4 at one decimal place, analytic N 88 (Table 1), outcome binary
assumptions: every cohort member has a recorded interval above 0 days so the percentage is 100 times a mean of 88 binary values, rounding rule not stated but the attainable value is not near an interval boundary
derivation: 100 times k/88 for integer k, k = 25 gives 28.4091 which lies inside [28.35, 28.45)
derived_value_or_range: 25/88 = 28.4091%
comparison_rule: reachable when some integer k makes 100 times k/N fall inside the rounding interval of the reported value
rounding_interval: [28.35, 28.45)
nearest_achievable: 24/88 = 27.2727%, 25/88 = 28.4091%, 26/88 = 29.5455%
status: consistent

### AR4
procedure_id: grim
evidence_anchor: table: Supplementary Table S5, unknown risk by Unmarried or Domestic Partner, men 40 (rounded to nearest 10), % waited over 90 days 50.0
reported_inputs: reported percentage 50.0 at one decimal place, men shown as 40 after rounding to the nearest 10, outcome binary
assumptions: the exact analytic N is not reported for this cell and Table 1 does not cross marital status with risk group, so N is only known to lie between 35 and 44
derivation: for N from 35 to 44, 50.0 is attainable for every even N (18/36, 19/38, 20/40, 21/42, 22/44) and not attainable for odd N, so reachability depends on the unreported N
derived_value_or_range: feasible N set 35 to 44, attainable only for even N
comparison_rule: a verdict requires a single known analytic N
status: not_computable
not_computable_reason: analytic_n_ambiguous


# Round 1 reviewer card: domain

contract_role: domain

## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: block
trigger: "One or more factual errors or misrepresentations of prior work or of an external benchmark that materially alter a headline claim or its interpretation"
block_class: repairable

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Reviewer identity: Peer Reviewer 2 (domain), an urologic oncology outcomes researcher working with SEER and NCDB data on prostate cancer risk stratification, treatment coding and time to treatment. Criteria binding is unavailable, so this review makes no claim about fit with any venue.

Summary. The preprint uses SEER 17 data (2010 to 2022) to measure how much marital status, county rurality and county income add to predicting a wait of more than 90 days before first recorded treatment, beyond clinical need, in men whose first course included radical prostatectomy or radiotherapy. The domain groundwork is careful in several places. Treatment codes are checked against the coding manual, the secondary outcome is worded as recorded treatment, and the paper declines to compare with Tasmanian data. The social increment and the direction of the area contrast also survive the prostatectomy-only sensitivity analysis. However, two domain problems change how a headline conclusion should be read ("what is predictable is partly clinical triage"):
- the recorded interval ends at hormone therapy, which radiotherapy patients with higher-risk disease often start first;
- the Methods wrongly state that risk groups use clinical information only.

Separately, the Introduction's account of prior work leaves out the closest analogues that the project's own literature check found. These problems can be fixed by rewriting and by analyses the authors have largely already run, so the D2 block is repairable, not fatal.

### S1: The secondary outcome is named for what SEER can show
The paper calls the secondary outcome recorded curative treatment and lists what a missing record can mean. This matches the validation evidence it cites. Noone et al. (Med Care 2016, PMID 24638121) found moderate sensitivity for SEER treatment fields and advised against using SEER to estimate the proportion treated.
**Evidence Anchor**: text: Methods, Secondary outcome "It is therefore not described as untreated."

### S2: Surgery and radiation codes are explicit and checked against the manual
Radical prostatectomy codes are listed for both coding eras and checked against Appendix C. Radiation labels are named. Prostatectomy not otherwise specified is removed in a sensitivity analysis. RECORD asks for this kind of code-level transparency.
**Evidence Anchor**: text: Methods, Treatment definitions "checked against the SEER coding manual [17]"

### S3: The Australian material is kept as background
The Tasmanian estimates match the values stated in the protocol from full-text reading (Foley 2022, Foley 2025), and the Discussion refuses a cross-country comparison.
**Evidence Anchor**: text: Discussion, Relevance to Australian pathway research "No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings."

### S4: The rural direction is not read as better rural care
Shorter recorded waits in remote counties are set against lower crude recorded curative treatment among high-risk men. The paper cites a national SEER study (Dirican 2026) that points the same way.
**Evidence Anchor**: text: Discussion, The rural direction "It is not evidence that rural men receive better care."

### W1: The triage interpretation ignores hormone therapy started before radiotherapy
The Methods state correctly that the SEER interval ends at the first treatment of any kind, including hormone therapy. The Discussion and Conclusions then read the shorter waits of high-risk men as clinical triage ("consistent with triage", "partly clinical triage"). In higher-risk localised disease, androgen deprivation is commonly given with radiotherapy and started before it. In TROG 96.01, deprivation was given for 3 or 6 months before and during radiation (Denham et al., Lancet Oncol 2008, PMID 18929505). D'Amico et al. (JAMA 2004, PMID 15315996) showed a survival benefit of 6 months of androgen suppression with radiotherapy.

Other evidence points the same way:
- **Queensland:** treatment intervals were shorter when men received deprivation combined with radiotherapy (Baade et al., Cancer Causes Control 2012, PMID 22382868).
- **SEER-Medicare:** when the endpoint was definitive treatment, not any treatment, the wait was longer in high-risk than low-risk disease (Stokes et al., Cancer 2013, PMID 23716470). This is the opposite of the gradient reported here.
- **This paper's own data:** in men treated with prostatectomy only, where deprivation before treatment is less usual, the crude low-risk versus high-risk gap in delay shrinks from 15.1 to 7.4 percentage points.

So part of the "clinical need" signal in high-risk men is probably hormone therapy recorded as the end of the interval, not faster curative treatment.

**Why it matters:** the Principal findings and the second Conclusions bullet rest on this reading. The social increment and the area contrast stay similar in the prostatectomy-only scenario, so the core estimand survives.

**Suggestion:** state in the Outcome and Interpretation sections that radiotherapy patients with higher-risk disease often start deprivation first. Bring the prostatectomy-only risk gradient into the main text. Report the clinical-need increment for that scenario, if it is available from the refitted steps. Rephrase "triage" as one possible explanation among several.
**Severity**: Major
**Evidence Anchor**: table: Supplementary Table S19, primary analysis row against the radical prostatectomy without radiotherapy only row — low risk 47.9 against 45.8, high risk 32.8 against 38.4
**Confidence**: 4 — core expertise in prostate cancer treatment pathways and SEER interval coding, with facts checked in PubMed records

### W2: Risk groups are described as clinical-only, but stage partly uses surgical pathology
The Methods say risk groups use clinical information only. Yet the first criterion for high risk is regional summary stage. The paper's own Limitations, and protocol section 4, say summary stage partly uses pathology for surgical patients. Pathological upstaging at prostatectomy therefore moves surgical men into the high-risk group. Stage category also sits in the step 1 clinical-need block, so treatment-dependent information enters before treatment type is added at step 3. This works against the ordering the estimand relies on.

The effect is visible in the data. When risk groups are built from Gleason score and PSA only, the crude share of high-risk men waiting more than 90 days falls from 32.8% to 28.2% (Supplementary Table S19).

**Why it matters:** "beyond clinical need" is the reference point of the primary estimand. A clinical-need block that partly encodes surgery and its pathology changes both the size of the clinical-need increment and its meaning as triage.

**Suggestion:** correct the Methods sentence. State that regional stage for surgical patients is often pathological. Consider a sensitivity analysis that leaves stage out of step 1 (or uses it only for non-surgical men), and say whether the Gleason-and-PSA-only scenario kept stage in step 1.
**Severity**: Major
**Evidence Anchor**: text: Methods, Clinical risk groups "Risk groups used clinical information only, because pathological grade is observed only after surgery."
**Confidence**: 4 — core expertise in SEER prostate staging and risk-group construction

### W3: The account of prior work omits the closest analogues and misdescribes the literature
The Introduction says prior studies report adjusted associations one factor at a time, usually pooled across risk groups. The project's own literature check (reports/phase1.md) identified studies this description does not fit, none of which is cited:
- **Stokes et al. 2013** (Cancer, PMID 23716470): SEER-Medicare time to definitive treatment, reported by risk group, with a multivariable model.
- **Ajjawi et al. 2026** (Curr Urol, PMID 41969320): the closest design analogue. It compares a clinical-only machine learning model with one that adds sociodemographic variables, in SEER high-risk men, although for cancer-specific survival.
- **Semprini et al. 2026** (Health Serv Res, PMID 40476571): county income and timeliness in SEER.
- **Baade et al. 2012** (Cancer Causes Control, PMID 22382868): an Australian study of prostate cancer treatment intervals, relevant to private health insurance and radiotherapy. The Australian framing currently rests on two lung cancer studies [4, 5] instead.

The studies that are cited (Di Vanna 2025, Montiel Ishino 2021) fit multivariable models with several social factors together, not one factor at a time.

**Why it matters:** the novelty claim in the Abstract and Introduction depends on how prior work is described. The literature check was PubMed-only, screened by title and abstract, with one reviewer. It supports "we found no study that…", not a flat statement.

**Suggestion:** cite and set the paper apart from Stokes, Ajjawi, Semprini and Baade. Describe prior models accurately as multivariable. Hedge the novelty statement to match the search that was done.
**Severity**: Major
**Evidence Anchor**: text: Introduction "These studies report adjusted associations for one factor at a time, usually pooled across risk groups."
**Confidence**: 4 — core expertise in the prostate time-to-treatment literature, with every cited record checked in PubMed

### W4: "Lower is better" is applied to low-risk men
The Abstract, Results and the axis of Figure 2 label the percentage waiting more than 90 days as "lower is better" in every risk group. For low-risk disease, a systematic review found that delays of several months or even years do not appear to affect outcomes (van den Bergh et al., Eur Urol 2013, PMID 23453419). The Discussion itself allows for considered deferral. The quality label goes further than the evidence for the low-risk stratum, which is where the paper's most prominent contrast sits.

**Suggestion:** limit the quality label to intermediate- and high-risk men, or describe the low-risk result neutrally as meeting or exceeding the benchmark.
**Severity**: Minor
**Evidence Anchor**: text: Abstract, Results "39.7% waited more than 90 days (lower is better)"
**Confidence**: 4 — core expertise, grounded in a systematic review found in PubMed

### W5: "Added more than clinical need" in low-risk men partly reflects the narrow group definition
Low-risk men are defined by Gleason score 6 or lower, PSA below 10 and localised stage. Recorded clinical need can therefore barely vary within this stratum. The factors that drive timing decisions in low-risk disease (T stage, PSA density, imaging, core volume, patient preference) are not recorded. The finding is true as measured, but the Abstract and Discussion invite the reading that clinical factors matter less for timing in low-risk men.

**Suggestion:** say "recorded clinical variables, which vary little within this group by definition".
**Severity**: Minor
**Evidence Anchor**: text: Abstract, Results "in low-risk men it added more than clinical need did."
**Confidence**: 4 — core expertise in prostate risk stratification

### W6: The exclusion of active surveillance is stated as certain
The Methods state that men whose first course was active surveillance are not in the cohort. This depends on how registrars code treatment given after early reclassification. SEER's own definition of the interval includes "a decision to start active surveillance" (as quoted in reports/phase0.md). Intervals of 731 days or more are counted as delayed, and they are hard to square with a planned first course. The Discussion's marital-status interpretation also appeals to surveillance, which sits awkwardly with the stated exclusion.

I have not checked the SEER first-course coding rule directly.

**Suggestion:** present the exclusion as an assumption. Cite the coding rule. Report the share of intervals over 365 days, and those top-coded, by risk group.
**Severity**: Minor
**Evidence Anchor**: text: Methods, Active surveillance "Men whose first course was active surveillance have surgery and radiation coded as none, so they are not in this cohort."
**Confidence**: 3 — core expertise, but the SEER coding rule was not checked in this review

### W7: Huang et al. [22] is applied beyond its population
Huang et al. studied favourable-risk men only: low risk and favourable intermediate risk, clinical T1 to T2c (PMID 36727535). The paper uses it to support never-married findings pooled across intermediate and high risk, including longer waits among men who were treated. Huang also found that rural low-risk men were more likely to be on surveillance or watchful waiting (urban odds ratio 0.77). This bears directly on who is selected into the treated low-risk rural group, but it is not cited for that point.

**Suggestion:** restrict the claim to favourable-risk disease, and use the rural finding when discussing selection into treatment.
**Severity**: Minor
**Evidence Anchor**: text: Discussion, Marital status "This is consistent with higher use of surveillance or watchful waiting among unmarried men in an earlier SEER study [22]."
**Confidence**: 4 — abstract checked in PubMed

### W8: The Noone 80% figure is quoted without its context
The 80% sensitivity for radiation is pooled over seven cancer sites, in men aged 65 or older diagnosed 2000 to 2006. The study reports that sensitivity varied by site, stage and patient characteristics. It also advises against using SEER to compare treated with untreated individuals (PMID 24638121). The secondary analysis does exactly that by social group, and the Discussion leans on crude receipt by rurality.

**Suggestion:** give the scope of the 80% figure, and bring Noone's caution into the interpretation of the secondary outcome.
**Severity**: Minor
**Evidence Anchor**: text: Limitations "Against Medicare claims, SEER identified radiation therapy with 80% sensitivity [20]."
**Confidence**: 4 — abstract checked in PubMed

### W9: US and Australian area measures are presented as equivalent
Supplementary Box 2 says the Rural-Urban Continuum Code "corresponds to" ASGS remoteness areas, and that county median household income corresponds to SEIFA IRSAD. They are different constructs:
- the continuum code is based on county metropolitan population and adjacency, while the ASGS measure is accessibility-based;
- IRSAD is a composite area index, not income.

Two related points:
- **Insurance:** Box 2 says the closest Australian contrast is a public or private treating facility, but Australian prostate studies have used private health insurance directly (Baade 2012).
- **Terminology:** the Results call non-metropolitan counties not adjacent to a metropolitan area "remote counties", which borrows an ASGS term.

**Suggestion:** use "candidate proxy for" instead of "corresponds to", and avoid "remote" for US counties.
**Severity**: Minor
**Evidence Anchor**: text: Supplementary Box 2 "the Rural-Urban Continuum Code corresponds to Australian Statistical Geography Standard remoteness areas, assigned by residential postcode."
**Confidence**: 3 — adjacent expertise in Australian area classifications

### W10: The leave-one-variable-out range misstates the table
The Results say removing marital status or rurality lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata. In Supplementary Table S8, intermediate-risk logistic regression lost 0.18 (marital status) and 0.19 (rurality), and LightGBM lost 0.21 (marital status). The same range appears in the source report reports/phase4.md.
**Severity**: Minor
**Evidence Anchor**: table: Supplementary Table S8, intermediate risk rows — marital status 0.18 and rurality 0.19 under penalised logistic regression, against the stated range of 0.22 to 0.45
**Confidence**: 5 — direct check against the table

### W11: Ang et al. [10] is cited for a mechanism it does not report
Ang et al. report the unadjusted paradox of lower mortality with longer intervals, pooled across breast, lung, prostate and colorectal cancer (PMID 40556964). The explanation that men with aggressive disease are treated sooner is the author's own inference (reports/phase1.md), not a finding of that study.

**Suggestion:** attribute the paradox to [10] and the triage explanation to the authors, or to a prostate-specific source.
**Severity**: Minor
**Evidence Anchor**: text: Introduction "Men with aggressive disease are treated sooner, which is why unadjusted comparisons of waiting time and survival can run in the wrong direction [10]."
**Confidence**: 4 — abstract checked in PubMed

### W12: The Discussion does not engage with evidence on large centres or the rising trend
The Discussion lists explanations the data cannot test, but cites no work that has tested them. In the NCDB, care at an academic centre was a determinant of longer time to treatment, and median time to treatment rose over 2004 to 2013 (Khorana et al., PLoS One 2019, PMID 30822350). The rise from 36.0% to 52.3% between 2010 and 2022 is a headline result in the Abstract, but the Discussion does not interpret it.

**Suggestion:** set the metropolitan direction and the time trend against this literature.
**Severity**: Minor
**Evidence Anchor**: text: Discussion, The rural direction "The data cannot test explanations such as longer surgical queues in large centres, second opinions, or wider choice of treatment settings."
**Confidence**: 4 — record checked in PubMed

### W13: STROBE and RECORD compliance is claimed but not yet shown
The paper says it follows STROBE and RECORD, but the checklists and the ethics statement are placeholders. RECORD [15] asks for the codes and algorithms used to classify variables, and for access to code. Two gaps stand out:
- the SEER variable names behind clinical Gleason score and PSA are not given in the manuscript (they appear only in config/analysis.yaml);
- the repository URL is missing.

**Suggestion:** complete the checklists, add the ethics statement, name the Gleason and PSA recode variables, and supply the code link.
**Severity**: Minor
**Evidence Anchor**: absence: Methods and Declarations — expected completed STROBE and RECORD checklists, an ethics statement, SEER variable names for clinical Gleason score and PSA, and a code repository link; checked Methods, Declarations, Reporting checklists section, Supplementary material
**Confidence**: 4 — reporting guideline cited by the manuscript itself

### Questions for Authors
1. In the prostatectomy-only and Gleason-and-PSA-only scenarios, was summary stage still included in step 1? What was the clinical-need increment in high-risk men in each?
2. What share of men in each risk group had intervals over 365 days, or top-coded at 731 days or more?
3. Does the November 2025 export include SEER's reviewed and corrected PSA values? The SEER PSA Working Group reported meaningful PSA errors in 5.7% of 2012 cases (Cancer 2017, PMID 27783399).

### Missing key references (each checked in PubMed)
- Stokes WA, et al. Racial differences in time from prostate cancer diagnosis to treatment initiation: a population-based study. Cancer. 2013;119(13):2486-93. PMID 23716470.
- Ajjawi I, et al. Machine learning approaches to optimize the integration of sociodemographic factors for predicting cancer-specific survival among patients with high-risk prostate cancer. Curr Urol. 2026;20(3):141-147. PMID 41969320.
- Baade PD, et al. Factors associated with diagnostic and treatment intervals for prostate cancer in Queensland, Australia: a large cohort study. Cancer Causes Control. 2012;23(4):625-34. PMID 22382868.
- Semprini JT, et al. Hospital accreditation and geographic disparities in timely cancer care. Health Serv Res. 2026;61(2):e14655. PMID 40476571.
- van den Bergh RC, et al. Timing of curative treatment for prostate cancer: a systematic review. Eur Urol. 2013;64(2):204-15. PMID 23453419.
- Khorana AA, et al. Time to initial cancer treatment in the United States and association with survival over time: an observational study. PLoS One. 2019;14(3):e0213209. PMID 30822350.
- Denham JW, et al. Time to biochemical failure and prostate-specific antigen doubling time as surrogates for prostate cancer-specific mortality: evidence from the TROG 96.01 randomised controlled trial. Lancet Oncol. 2008;9(11):1058-68. PMID 18929505.


# Round 1 reviewer card: perspective

contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "some cross-disciplinary implications are stated more strongly than the cited support warrants"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Reviewer: Peer Reviewer 3 (cross-disciplinary). I review as a health economist who works on equity measurement (concentration indices) and rural access, and who compares health systems. My blind spots are prediction-model calibration detail and clinical coding. Criteria binding is unavailable, so I make no claim about fit with any venue.

Summary. The preprint uses US SEER data to measure how much marital status, county rurality and county income add to predicting a wait of more than 90 days, beyond recorded clinical need. It adds standardised percentages, an Erreygers concentration index and selection bounds. For readers in health services research, equity and policy, the framing is mostly careful. The manuscript says plainly that no Australian data were analysed. The joint area profiles are a sound choice for collinear area measures. I checked the headline numbers in the abstract, Results and Discussion against reports/phase3.md, reports/phase4*.md and PROTOCOL.md, and they match. D4 scores warn, not block. Every central construct has an operational definition that can be reproduced, and no principal takeaway lacks data. But several equity and policy statements say more than the analysis supports. The main ones are the income gradient, the direction statement in the Conclusions and the label "social position". The source report states one caveat that the manuscript leaves out. I found no wording that implies Australian data were analysed. The title, abstract, Discussion and Supplementary Box 2 all identify the data as US SEER, and the Discussion rules out a comparison with Tasmania.

### S1: Joint area profiles avoid off-support counterfactuals
The rurality and income contrast is standardised jointly, each area at its typical county income. It is not a one-at-a-time contrast. This is how equity analysts should handle collinear area measures, and the manuscript gives the reason in terms adjacent-field readers can follow.
**Evidence Anchor**: text: Methods, Standardised percentages "changing one while holding the other fixed creates combinations that are rarely observed"

### S2: Explicit boundary on cross-country interpretation
The Discussion states that no Australian data were analysed and that US and Tasmanian findings cannot be set against each other. It gives the reasons (area measures, health systems, interval definitions). This prevents the misreading that a comparison was made.
**Evidence Anchor**: text: Discussion, Relevance to Australian pathway research "No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings"

### S3: Careful labelling of the secondary outcome
Recorded curative treatment is not presented as treatment receipt or under-treatment. Policy readers could otherwise misread lower percentages as unmet need.
**Evidence Anchor**: text: Methods, Secondary outcome "It is therefore not described as untreated."

### S4: Selection bounds make the missing-interval problem transparent
The worst-case bounds by rurality and income let a reader check that the crude orderings survive extreme assumptions about men without a recorded interval.
**Evidence Anchor**: table: Supplementary Table S14 — lower and upper bounds by rurality for men without a recorded interval

### W1: The concentration index is presented as an income gradient although it cannot separate income from rurality
**Problem**: The abstract lists "Income" as a separate result, and the Conclusions refer to "lower-income counties". Both rest on an Erreygers index that ranks men by county median household income band. The source report (reports/phase4.md, section 4) says this index does not separate income from rurality. The manuscript leaves that caveat out of Methods, Results and Discussion. The manuscript's own evidence also shows that an income-specific signal depends on the model. In the leave-one-variable-out refits, income carried 0.00 to 0.02 points under logistic regression and 0.26 to 0.29 under LightGBM (Results, Which social variable). And 45.6% of men in remote counties were in the lowest income quartile, against 1.1% in large metropolitan counties (Table 1).
**Evidence Anchor**: text: Abstract, Results "delay was concentrated among men in higher-income counties (Erreygers index 0.062, 0.039 to 0.083; 0 means no income gradient)"
**Why it matters**: Equity and policy readers treat a concentration index as a socioeconomic gradient. Read alongside the separate rurality result, it looks like independent evidence that lower-income areas are advantaged. It is the same area contrast measured a second way.
**Suggestion**: Restore the source report's caveat in Results and Discussion. Present the index as an area-income and rurality gradient, not an income gradient. Drop the stand-alone income reading from the abstract and Conclusions, or state that it is not separable from rurality.
**Severity**: Major
**Confidence**: 4 — core expertise: concentration-index interpretation

### W2: The direction statement in the Conclusions omits that it holds only among men with recorded curative treatment
**Problem**: The Conclusions say the signal "points to less delay, not more, in rural and lower-income counties". The cohort is restricted to men with a recorded prostatectomy or radiotherapy. That restriction is itself socially patterned. Social position added 1.96 to 2.16 points of skill in predicting recorded curative treatment. Among high-risk men, crude recorded curative treatment was 75.3% in remote against 81.9% in large metropolitan counties, and 73.7% in the lowest against 83.0% in the highest income quartile (Supplementary Tables S26, S27). The Discussion's rural-direction paragraph says the rural direction "is not evidence that rural men receive better care". That qualifier does not reach the Conclusions or the abstract. The selection bounds cover men without a recorded interval, not selection into the treated cohort.
**Evidence Anchor**: text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties"
**Why it matters**: Policy readers usually read only the abstract and Conclusions. "Less delay in rural and lower-income counties" can be taken as better access. It may instead reflect who reaches recorded curative treatment and who is captured by reporting facilities.
**Suggestion**: State the conditioning population in the abstract Conclusions and the Conclusions section, for example "among men with recorded curative treatment". Carry the Discussion's "not evidence of better care" sentence into the Conclusions. Mention the lower recorded-treatment percentages in remote and low-income counties next to the delay direction.
**Severity**: Major
**Confidence**: 4 — core expertise: rural access and selection in equity measurement

### W3: "Social position" names a block that is mostly area attributes and registry practice
**Problem**: The primary estimand is called "social position". The block holds one individual variable (marital status) and two county-level area attributes. The Methods say it also absorbs unmeasured registry differences. The leave-one-variable-out results show that marital status and rurality carry most of the increment. In sociology and social epidemiology, "social position" usually means individual socioeconomic position. The title, abstract and Conclusions use the label without qualification.
**Evidence Anchor**: text: Methods, Uncertainty "The social block is interpreted as geographic and social position, including any unmeasured registry differences"
**Why it matters**: Readers from adjacent fields will take "social position adds 0.62 to 0.99 points" to mean individual socioeconomic disadvantage. That is not what was measured, and part of the signal may be registry or area practice.
**Suggestion**: Rename the block, for example "area and marital attributes", or qualify "social position" wherever it appears in the title, abstract and Conclusions. State once, prominently, that two of the three variables are ecological and that registry differences load onto the block.
**Severity**: Major
**Confidence**: 4 — core expertise: equity measurement constructs

### W4: The practical size of the primary estimand is not bridged to the percentage-point contrasts
**Problem**: The headline quantity is percentage points of log-loss skill, described as "small". The standardised area and marital contrasts are 6 to 9 percentage points, which a policy reader will read as large. The population-level "all social features as observed" contrast is only 1.1 to 1.6 points. The manuscript does not explain how the three relate. In low-risk men, social position is reported as 82% and 98% of step 2 skill. Step 2 skill there is below 1%, so the share framing can suggest that social position matters more than clinical need, when both contributions are tiny.
**Evidence Anchor**: table: Table 2, low risk rows — social position as 82 and 98 percent of step 2 skill, where step 2 skill is 0.76 and 0.99
**Why it matters**: Health services and policy readers cannot judge whether the increment matters, or reconcile "small" with a 9-point area difference. They are therefore likely to misjudge the policy weight of the findings.
**Suggestion**: Add a short interpretive paragraph, and a sentence in the abstract, relating skill points, the between-group standardised contrasts and the population-level contrast. Report the low-risk share next to the absolute skill values wherever it appears.
**Severity**: Major
**Confidence**: 3 — adjacent field: prediction-metric interpretation

### W5: Why an Australian benchmark is applied to US men is not stated
**Problem**: The outcome is justified only by reference to the Australian optimal care pathway. The manuscript does not say why this benchmark suits US men. It also does not link the benchmark to the 90-day threshold already used in the US literature it cites [8]. The Discussion says interval definitions differ, but the Methods do not say how the benchmark's clock compares with SEER's interval, which ends at the first treatment of any kind.
**Evidence Anchor**: text: Methods, Outcome "a wait of more than 90 days, following the optimal care pathway benchmark"
**Why it matters**: US readers will find the choice arbitrary. Australian readers may read the percentage as a measure of compliance with their pathway, which it is not.
**Suggestion**: In Methods, give one or two sentences on why the threshold was chosen, noting that 90 days is also used in US studies. Say that the SEER interval is not the pathway's own measure, and that the results are robust across 60, 120 and 180 days.
**Severity**: Minor
**Confidence**: 4 — core expertise: cross-system benchmarking

### W6: Labels saying lower waits are better conflict with the Discussion
**Problem**: The abstract, Results and figure legends label fewer delayed men, and fewer excess days, as better. The Discussion says a wait beyond 90 days can reflect considered deferral or patient choice. That is especially plausible in low-risk men, where delay was most common.
**Evidence Anchor**: text: Abstract, Results "39.7% waited more than 90 days (lower is better)"
**Why it matters**: These labels decide whether equity readers see the positive concentration index and the metropolitan excess as disadvantage. The normative direction is not established.
**Suggestion**: Remove the labels or qualify them, for example "a lower percentage means more men were treated within the benchmark". Say once that a longer wait is not necessarily worse care.
**Severity**: Minor
**Confidence**: 4 — core expertise: normative interpretation of equity indices

### W7: Excess waiting days are hard to interpret as a policy metric
**Problem**: Excess days are crude and unadjusted for risk group. They count top-coded intervals at 731 days and are expressed per 1,000 men without a per-man equivalent. The protocol's pre-specified 7-day meaningful difference in standardised mean waiting time is not mentioned in the manuscript.
**Evidence Anchor**: table: Supplementary Table S11, all men — 30,597 and 20,014 crude excess days per 1,000 men
**Why it matters**: Service planners will read these as the size of an access gap. Top-coded tails and case mix may drive them, and they carry no uncertainty.
**Suggestion**: Report days per man. Show how much of the excess comes from top-coded intervals. State that the 7-day threshold could not be applied and why.
**Severity**: Minor
**Confidence**: 3 — adjacent field: health services metrics

### W8: Supplementary Box 2 claims correspondence where only candidate equivalence is supported
**Problem**: The box title says "candidate" equivalents, but the text says the Rural-Urban Continuum Code "corresponds to" remoteness areas and that county median income corresponds to SEIFA IRSAD. By its name, IRSAD is an index of relative advantage and disadvantage, not a median income. The Australian measures are assigned by postcode, not county. The box gives no source for either equivalence.
**Evidence Anchor**: text: Supplementary Box 2 "the Rural-Urban Continuum Code corresponds to Australian Statistical Geography Standard remoteness areas, assigned by residential postcode"
**Why it matters**: A different construct and geographic scale would change the collinearity, the rank ties and the concentration index. That limits the claim that the measurement approach transfers as is.
**Suggestion**: Replace "corresponds to" with "is the closest available analogue of". Note the differences in construct and scale, and how they would affect joint area profiles and the concentration index.
**Severity**: Minor
**Confidence**: 3 — core expertise: cross-system area measures; details of the Australian classifications not verified here

### W9: Tasmanian public-private finding restated without its population restriction
**Problem**: The Introduction correctly restricts the Foley et al. 2025 differences to men not treated with external beam radiotherapy. The Discussion restates "42 to 59 days" without that restriction. PROTOCOL.md confirms the restriction.
**Evidence Anchor**: text: Discussion, What an Australian registry could add "They reported an adjusted difference of 9.25 days by remoteness, and of 42 to 59 days between public and private facilities"
**Why it matters**: Australian readers could over-generalise the size of the public-private gap.
**Suggestion**: Add "among men not treated with external beam radiotherapy". Note that the 9.25 days is an age-adjusted comparison of outer regional and remote with inner regional men.
**Severity**: Minor
**Confidence**: 4 — verified against PROTOCOL.md background section

### W10: The amendment log promises a supplementary table of one-at-a-time profiles that the supplement does not contain
**Problem**: Amendment 1.7 says the one-at-a-time rurality and income results are "kept in a supplementary table". The supplement has no such table. The source report shows they exist as a repository CSV, and that the models disagreed sharply on them (income Q4 to Q1: -0.9 against -8.7 points).
**Evidence Anchor**: absence: Supplement — expected the one-at-a-time rurality and county income profile table cited in amendment 1.7 of Supplementary Table S32; checked Methods Standardised percentages, Supplementary Tables S10, S21 to S24, S30, S31
**Why it matters**: Those results are the most direct evidence that an income-only gradient is not robust. Readers interested in equity cannot see them.
**Suggestion**: Add the table, with the statement that it is not interpreted, or correct the amendment text.
**Severity**: Minor
**Confidence**: 4 — direct document check

### W11: Rank ties and need standardisation for the concentration index are not described
**Problem**: Men are ranked by 16 county income bands, so ties are very large, yet the fractional-rank rule is not stated. The pooled index uses crude delay, not a need-standardised outcome. A need-standardised outcome is the usual way to measure horizontal inequity in health economics.
**Evidence Anchor**: absence: Methods, Income inequality — expected the fractional-rank rule for men tied within county income bands and whether delay was need-standardised; checked Methods Income inequality, Supplementary Table S12, Figure 4 legend
**Why it matters**: The value of the index depends on how ties are handled. The pooled 0.062 mixes risk-group composition with the income gradient, although the stratified indices partly address this.
**Suggestion**: State the tie rule. Report a pooled index of need-standardised delay, or say that the stratified indices are the intended need-adjusted estimates.
**Severity**: Minor
**Confidence**: 4 — core expertise: concentration index computation

### Questions for Authors
1. The concentration-index interval comes from a cluster bootstrap over cells defined partly by the ranking variable itself. Resamples therefore drop or duplicate whole income bands and change the rank distribution. How does this affect coverage for an index of income rank?
2. Could lower SEER capture of treatment given outside reporting facilities differ by rurality, so that the recorded cohort in remote counties is systematically different?
3. The Discussion says the measurement approach transfers. Which parts assume collinearity between remoteness and area disadvantage, and would that assumption hold at postcode scale?

### Cross-Disciplinary Reading Recommendations
- Search lead [UNVERIFIED]: the health economics literature on need-standardised (indirectly standardised) concentration indices and horizontal inequity indices, including World Bank guidance on analysing health equity with household survey data. This is relevant to W11 and to separating need from area income.


# Round 1 reviewer card: da

contract_role: da

## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: block
trigger: "A principal conclusion depends on an inferential leap the presented evidence cannot carry"
block_class: repairable

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

**Scope and binding.** Devil's Advocate seat, owner of D3. No target venue is confirmed (criteria_binding_unavailable), so nothing below is a venue-fit claim. I checked the claims against the manuscript and supplement and against PROTOCOL.md, reports/phase1.md, reports/phase3.md and reports/phase4*.md. Numbers quoted here come from those surfaces.

**What the paper does well (brief).** The protocol was committed before modelling, post hoc amendments are labelled, the paper says repeatedly that results are associations, two model families are compared, the recorded-curative-treatment outcome is carefully not called under-treatment, and the Discussion says outright that shorter rural waits are not evidence of better care. None of this is in dispute below.

**Core thesis as I read it.** Among US men treated with prostatectomy or radiotherapy, three variables called "social position" (marital status, county rurality, county income) add a small, consistent, non-zero amount of out-of-fold log-loss skill for predicting a wait over 90 days, beyond recorded clinical need. The signal is also said to point to less delay in rural and lower-income counties. The first half is literally supported by Table 2. The problem is the second half, and the labels that carry the first half into interpretation.

**Strongest counter-argument.** A sceptic would say the paper has measured a registry-and-geography signal and named it social position. The block has no individual socioeconomic measure. It has two county-level area measures, which in a SEER 17 export with no registry identifier also stand in for registry, health-system supply and recording practice, plus marital status, which includes an "Unknown" category that behaves like a data-completeness marker. Under penalised logistic regression, removing county income costs 0.00 to 0.02 points (Supplementary Table S8). So in the better-calibrated model almost nothing of the increment is income, and what remains is marital status and rurality. The paper's own model disagreement shows the directional reading is fragile. When rurality alone was changed, one model gave -8.7 points and the other +1.7 (reports/phase4_equity_selection.md). That analysis was dropped post hoc, and the results were not put in the supplement. The low-risk finding that social position predicts more than clinical need is what you would expect after stratifying on clinical need, which leaves little clinical variation within the stratum. The high-risk triage pattern may partly be a timing artefact, because the interval ends at hormone therapy. Finally, the cohort is conditioned on a recorded curative first course. The paper's own secondary analysis shows that condition is more socially patterned than delay itself (increment 1.96 to 2.16 against 0.62 to 0.99). On this reading, the consistent finding is that SEER fields carrying geography and record completeness predict a SEER-derived interval slightly better than clinical fields do. What that tells us about social position is unknown. The authors partly concede this in their Limitations, but not in the Abstract conclusion, the Principal findings or the Conclusions.

**Why D3 is block (repairable), not fatal.** The central quantity is well defined and reported honestly, and no result contradicts it. But two principal conclusions go beyond the evidence: the Conclusions' separate rural and lower-income direction, and the low-risk claim that social position predicts more than clinical need. Readers are also invited to read the >90-day outcome as a quality failure ("lower is better", "income inequality", "excess days") while the Interpretation says long waits can be considered deferral. Fixing this means substantial reframing and some added reporting, not abandoning the claim, so it is repairable. No finding alone reaches rejection level, so the CRITICAL table is empty.

**Ignored alternative explanations.** (1) Registry-level differences in recording practice or care pathways, entangled with metropolitan counties because no registry identifier is available. (2) Differential coding of surveillance as first course: excluded deferrers push treated-cohort delay down, and surveillance conversions recorded as first course push it up. The paper uses this mechanism for marital status only. (3) Neoadjuvant or first-line hormone therapy ending the interval early for radiotherapy patients. (4) Considered deferral and choice among providers in higher-income metropolitan areas, where a longer wait is not a harm.

**Unexamined premise.** The interval's start, SEER's date of diagnosis, is taken as a fixed clinical event, comparable across 17 registries, 13 years and metropolitan and rural settings. The manuscript never discusses whether that start point is recorded consistently. Delay rose from 36.0% to 52.3%, which the Abstract reports, but the paper never interprets the trend. Year is only absorbed into step 0. If the start point shifted with diagnostic pathways, differently by setting, the area contrast and the trend could partly be measurement. I raise this as a question for the authors, not as an established defect.

**Minor issues (below MAJOR; listed for completeness).**
- Numeric misstatement, anchor table: Supplementary Table S8. The Results say removing marital status or rurality "each lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata". In S8, intermediate-risk logistic regression loses 0.18 (marital status) and 0.19 (rurality). The same error is in reports/phase4.md, so it was carried over from the source report.
- Mixing analyses, anchor text: Discussion, The rural direction, "although the standardised difference was under 3 points". This follows a high-risk crude contrast (75.3% against 81.9%), but "under 3 points" is true only of the pooled standardised contrast. In high-risk men the models gave -3.3 and -2.5, labelled "models disagree" (Supplementary Table S30).
- A caveat dropped from the source, anchor text: Results, Model comparison, "LightGBM had higher step 2 skill than penalised logistic regression in every stratum". reports/phase4.md adds that no interval was computed for this difference. The manuscript omits that.
- Abstract wording, anchor text: Abstract, "stayed above 0 in 98 of 100 results". It is the 95% interval that stayed above 0 in 98 of 100. The point estimates were above 0 in all 100.
- Consistency oversold: the ten sensitivity scenarios mostly reuse the same men, and the threshold scenarios reuse exactly the same men with nested outcomes. Agreement across them is expected and is not independent replication. The Discussion's "consistent across ... ten sensitivity analyses" should say so.
- Citation used for more than it shows, anchor text: Introduction, "A small gain can still be informative". The cited example is an AUC change from 0.671 to 0.673. That shows small gains get reported, not that they inform.
- Figures: Figure 3 uses a different x-axis range in each panel (about 0 to 4, 0 to 2 and 0 to 1), so the social position increment looks as large as the clinical need increment. Figure 4a starts its axis near 31% and shows no uncertainty.
- Crude excess days (Supplementary Table S11) sit under a Results heading that also covers standardised percentages. Top-coded intervals count as 731 days, so a few extreme records can dominate. Both points need saying next to the figures.
- Low-risk shares of 82% and 98% of step 2 skill are ratios over denominators of 0.76 and 0.99 points, and a clinical increment of 0.02 (-0.09 to 0.13). They should not be read as stable proportions.

**Missing stakeholder perspectives (named only).** Men who choose deferral, treating urologists and radiation oncologists (on why waits differ), and registry staff (on how the start date and treatment are recorded).

**Observations (non-defects).** The joint area profile is a defensible response to collinearity (Table 1: 45.6% against 1.1% in the lowest income quartile). Both models agree on the area contrast in every risk group. The worst-case bounds for missing intervals do preserve the crude orderings. These points make the pooled area contrast credible as a description; they do not settle what it means.

#### CRITICAL
| # | Dimension | Issue Description | Evidence Anchor | Confidence | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|-----------|-------------------|-----------------|------------|---------------------|-----------------------------|

#### MAJOR
| # | Dimension | Issue Description | Evidence Anchor | Confidence | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|-----------|-------------------|-----------------|------------|---------------------|-----------------------------|
| M1 | Core thesis / logic chain | The headline names the increment "social position", but the block has no individual socioeconomic measure. It is two county measures that, with no registry identifier, also carry registry and health-system differences, plus marital status with an Unknown category (7.8% of men, standardised delay 45.6% and 45.7% against 40.8% and 41.3% married, S10) that behaves like a record-completeness marker. Income alone adds 0.00 to 0.02 points under logistic regression (S8). Methods state the registry caveat, but the Abstract conclusion, Principal findings and Conclusions drop it. Remedy: rename the block (for example area and marital characteristics), carry the registry caveat into the Abstract and Conclusions, and report the increment without the Unknown marital category. | text: Abstract Conclusions "social position adds a small but consistent amount to predicting waits beyond the Australian 3-month benchmark, over and above recorded clinical need" against Methods "The social block is interpreted as geographic and social position, including any unmeasured registry differences." | 4 (logic of prediction increments; registry data structure as reported) | n/a, severity does not rest on a field norm | n/a |
| M2 | Logic chain / overgeneralisation | The claim that social position predicted more delay than clinical need in low-risk men compares like with unlike. Risk groups are built from the same Gleason, PSA and stage variables that form the clinical block, so little clinical variation is left inside the low-risk stratum (Gleason 6 or lower, PSA below 10, localised). The clinical increment is almost bound to be small there (0.14; 0.02, -0.09 to 0.13), while the social block keeps its full variation. The 82% and 98% shares divide by 0.76 and 0.99 points. The result shows how the strata were built, not that social position matters more than need in low-risk disease. It appears in the Abstract and the Principal findings. Remedy: remove the comparison, or give the pooled-cohort increments with risk group inside the clinical block. | text: Discussion Principal findings "In low-risk men, social position predicted more of the delay than clinical need did." | 4 (design logic; checked against risk-group definitions and Table 2) | n/a, severity does not rest on a field norm | n/a |
| M3 | Unsupported directional conclusion | The Conclusions and Discussion give separate adjusted directions for rurality and for lower income. Only the joint area profile, which moves rurality and income together, was interpretable. Amendment 1.7 dropped one-at-a-time profiles because the models conflicted: rurality alone -8.7 against +1.7, income alone -0.9 against -8.7 (reports/phase4_equity_selection.md). The Erreygers index is crude within risk group, not standardised for clinical features. Income adds 0.00 to 0.02 skill under logistic regression. reports/phase4.md warns that the area result "is an area contrast, not a rurality effect separate from income"; that caution is missing from the manuscript. Remedy: state direction only for the joint area contrast and label the income index as crude. | text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties." | 5 (checked source reports and S8, S12, Table 3) | n/a, severity does not rest on a field norm | n/a |
| M4 | Selective reporting after a post hoc change | The switch to joint area profiles was made after a development run in which the two models disagreed, and it is labelled post hoc. The amendment log says the conflicting one-at-a-time results are kept in a supplementary table, but no such table is in the supplement. They exist only in a repository CSV. The Abstract's standardised area contrast (-9.2 and -8.8) comes from the analysis that replaced them. Readers cannot see the disagreement that prompted the change. Remedy: add the one-at-a-time profiles to the supplement, with the disagreement stated. | absence: Supplementary material — expected the one-at-a-time rurality and county income standardised profiles that amendment 1.7 in Supplementary Table S32 says are kept in a supplementary table; checked Methods (Standardised percentages), Results, Tables 1 to 3, Supplementary Tables S1 to S32, supplementary figures | 5 (direct inspection of all supplementary tables) | n/a, severity does not rest on a field norm | n/a |
| M5 | Internal inconsistency in the uncertainty argument | The paper refuses to report fixed-model bootstrap intervals for standardised contrasts because they ignore model-fitting uncertainty, and because in the source report such intervals were narrower than the disagreement between models. The primary estimand's intervals, which carry the claim "every interval above 0", are also fixed-model, no-refit intervals. By the paper's own test they may be too narrow: in the unknown-risk stratum the two models' increments do not overlap (0.42, 0.08 to 0.80; 1.37, 0.80 to 2.19). Low-risk logistic regression has a lower bound of 0.32. Remedy: either give a reason why no-refit intervals are adequate for the increment but not for the contrasts, or add refitting uncertainty and soften "consistent". | text: Methods Uncertainty "500 resamples of out-of-fold predictions, percentile intervals, no refitting" against Judging differences "Bootstrap intervals that hold the fitted model fixed ignore model-fitting uncertainty" | 3 (argument consistency; size of any widening not computed) | n/a, severity does not rest on a field norm | n/a |
| M6 | Normative framing contradicts own interpretation | Throughout, a wait over 90 days is presented as a harm: "lower is better", "fewer is better", an "Income inequality" section, excess waiting days. The Interpretation says such waits can reflect considered deferral or patient choice, and the registry cannot tell these apart. The social share is largest in low-risk men (82% and 98%), and the concentration index is highest there too (0.103), which is exactly where deferral is most plausible. Calling delay concentrated among higher-income men an inequality is an equity judgement this outcome cannot support. Remedy: drop the better or worse labels and the inequality framing for this outcome, or restrict the normative reading to high-risk men. | text: Results "39.7% of men waited more than 90 days (lower is better)" against Interpretation "A wait beyond 90 days can reflect considered deferral, patient choice, time for decisions between surgery and radiotherapy, or access problems." | 4 (internal consistency; checked Abstract, Results, Discussion) | n/a, severity does not rest on a field norm | n/a |
| M7 | Rival explanation for the triage pattern | The paper reads the strong clinical-need signal in high-risk men as triage. But the interval ends at the first treatment of any kind, including hormone therapy, which is not in the export and commonly accompanies radiotherapy in high-risk disease. In the paper's own prostatectomy-only scenario, high-risk delay rises from 32.8% to 38.4% while low-risk delay changes little (47.9% to 45.8%), so the low-to-high gap halves from 15.1 to 7.4 points. Case mix also differs in that scenario, so this does not prove an artefact, but the triage reading was never tested against it. The clinical-need increment in the surgery-only cohort is not reported. Remedy: report the clinical increment by treatment type and qualify the triage reading. | table: Supplementary Table S19, rows primary analysis and radical prostatectomy without radiotherapy only — high risk 32.8 against 38.4; low risk 47.9 against 45.8 | 3 (clinical practice point general; data pattern checked, not decomposed) | n/a, severity does not rest on a field norm | n/a |
| M8 | Selection handled in one direction only | The cohort requires a recorded curative first course. Step 6 excluded 202,102 men: surveillance, hormone therapy only, refusal and uncaptured treatment. The secondary analysis shows this condition is more socially patterned (increment 1.96 to 2.16) than delay itself. The Abstract's "selection bounds" cover only the 17,001 treated men with no recorded interval. The Discussion invokes differential surveillance to explain the marital result but not the rural or income results, although the authors' own literature report records less surveillance among urban than rural low-risk men (reports/phase1.md, Huang 2023). Depending on whether deferrers are excluded or converted, the rural and income contrasts could move in either direction, and the paper never says which. Remedy: say the bounds do not cover step-6 selection, and discuss the direction of this bias for area as well as marital status. | text: Discussion Marital status "This is consistent with higher use of surveillance or watchful waiting among unmarried men in an earlier SEER study [22]." | 3 (mechanism plausible; direction not identifiable from reported data) | n/a, severity does not rest on a field norm | n/a |
