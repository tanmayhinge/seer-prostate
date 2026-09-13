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
