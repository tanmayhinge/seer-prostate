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
