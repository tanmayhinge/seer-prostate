# Response to reviewers (revision 1)

Manuscript: What area and marital characteristics add to clinical need in predicting waits beyond 90 days for prostate cancer surgery or radiotherapy: a machine learning analysis of US SEER data, 2010 to 2022 (round 1 title: Waiting for prostate cancer treatment: how much is clinical need?).

We thank the reviewers. The revision was made directly in the manuscript sources, not through a patch workflow, so no revision patch or apply report exists. Post-review analyses were specified in protocol amendment 1.9 before they were run. Section names below refer to the revised main text; S numbers refer to the renumbered supplement. Where a request was only partly met, we say so.

## Required revisions

**R1 (REV-1). Interpretive anchor for the skill increment.** Added Discussion, "Interpreting the size of the increment", relating an increment below 1.4 points of log-loss skill to standardised differences of 6 to 9 percentage points between profiles and 1.1 to 1.6 points for the cohort as a whole. The Abstract reports the increment and the standardised contrasts in adjacent sentences but does not state the relation explicitly.

**R2 (REV-3). Low-risk share with its denominator.** Results now give 82% and 98% together with the step 2 skill of 0.76 and 0.99 points; the Discussion says that skill was under 1 point. The low-risk share no longer appears in the Abstract.

**R3 (REV-4). Direction for the joint area contrast only.** The Abstract, Discussion and Conclusions describe the direction as large metropolitan, higher-income counties against non-metropolitan, lower-income counties. Discussion, "What the direction can and cannot show", states that rurality and income cannot be separated and cites the conflicting one-at-a-time results. Crude descriptive comparisons by rurality and by income remain in Results, labelled as crude.

**R4 (REV-5). Concentration-index caveat.** Methods, Results and the Figure 4 legend state that the index is crude, not standardised for clinical features, and does not separate income from rurality. The index is no longer in the Abstract.

**R5 (REV-6). Title names the estimand.** Retitled to name what area and marital characteristics add to clinical need in predicting waits beyond 90 days.

**R6 (REV-7). Australian material as context.** The Introduction now presents US evidence only. Australian and Tasmanian material, including the two lung cancer studies, is in a labelled Discussion section, "Australian context", which states that the results cannot be compared directly.

**R7 (REV-8). Threshold rationale for US data.** Methods, Outcome now cites the use of 90 days in US registry research [6], notes that it matches the Australian pathway, and states that the SEER interval is not the pathway's own measure.

**R8 (REV-9). Verifiable protocol timing.** The protocol and code are public at https://github.com/tanmayhinge/seer-prostate. Supplementary Table S44, generated from git, lists the commit, commit time and protocol version for every protocol change. Methods state that commit times are recorded by the author's computer, that the repository became public after the analyses, and that versions 1.1 to 1.3 and 1.5 to 1.7 were committed together with other work. The timing is therefore inspectable but not independently timestamped, and the study was not registered.

**R9 (REV-10). Code repository link.** Given in Methods and Declarations.

**R10 (REV-11). Reporting checklists.** Supplementary Tables S45 (STROBE and RECORD) and S46 (TRIPOD+AI) give a location for every item, using item wording from the published checklists. Items not met are marked, including TRIPOD+AI 22 (no released model) and 23b (heterogeneity across clusters not examined).

**R11 (REV-12). Declarations.** Funding, competing interests, ethics, patient and public involvement, data and code availability and AI use are completed. The author chose not to give an affiliation.

**R12 (REV-13). Leave-one-variable-out range.** Corrected to 0.18 to 0.45.

**R13 (REV-14). High-risk standardised difference.** Results, Secondary outcome now give the pooled contrast (-2.9 and -1.4) and the high-risk contrast (-3.3 and -2.5, only one model reaching 3 points). The incorrect Discussion clause was removed.

**R14 (REV-18). Strengths wording on uncertainty.** Now "a cluster bootstrap over rurality by income cells as a proxy for county-level dependence".

**R15 (REV-21). Prior work and hedged novelty.** The Introduction describes prior studies as multivariable and scopes the novelty statement to a PubMed search screened by title and abstract by one reviewer.

**R16 (REV-22). Closest precedents.** Stokes 2013 [4], Semprini 2026 [7], Tagai 2025 [9] and Ajjawi 2026 [10] are cited and positioned in the Introduction; Baade 2012 [26] is in the Australian context section.

**R17 (REV-23). Model-fitting uncertainty.** Under per-step tuning, cross-fitting was repeated with 10 fold assignments per stratum and model (Supplementary Table S11). A refitting bootstrap was not run, for computing time. Methods, Table 2 and the Figure 3 legend state that the intervals do not include model-fitting variability, and this is listed as a limitation.

**R18 (REV-24). Bootstrap clustering unit.** Supplementary Table S14 reports the number of clusters and the smallest, median and largest cluster per stratum. Intervals were repeated with county income band alone as a coarser cluster (Supplementary Table S11). Counties and registries remain unavailable in the export.

**R19 (REV-25). Per-step tuning.** Hyperparameters were tuned separately at steps 0, 1 and 2 (Supplementary Tables S11 to S13). The inference that flexible clinical adjustment did not absorb the signal is now restricted to all men and intermediate- and high-risk men, where the LightGBM clinical model was at least as good as the logistic one.

**R20 (REV-26). One-at-a-time profile table.** Published as Supplementary Tables S17 and S18, with the model disagreement stated.

**R21 (REV-27). Post hoc labels.** Methods, Standardised percentages, the Abstract and the Table 3 note label the agreement rule as post hoc and state that standardised contrasts have no intervals.

**R22 (REV-28). Year-aware concentration index.** The index by diagnosis period and the county income quartile distribution by period are in Supplementary Tables S21 and S22 and in Results.

**R23 (REV-33). Conditioning on recorded curative treatment.** The Abstract Conclusions and the Conclusions name the population with recorded surgery or radiotherapy and state that the pattern is not evidence of better care. Methods and Discussion state that the bounds cover only treated men without a recorded interval, and the Discussion considers the direction of selection bias for area measures.

**R24 (REV-35). Hormone therapy and triage.** Methods, Outcome explain that hormone therapy can end the interval. Results report the prostatectomy-only risk gradient and the clinical need increment for that scenario (Supplementary Table S35). The Discussion presents triage as one explanation alongside hormone therapy.

**R25 (REV-36). Risk-group construction.** Methods, Risk groups no longer say "clinical information only". They state that summary stage can incorporate pathology for surgical patients and that the Gleason-and-PSA-only scenario kept stage in the clinical block. A stage-free sensitivity analysis is in Supplementary Table S15.

**R26 (REV-46). The "social position" label.** The block is renamed "area and marital characteristics" in the title, Abstract and Conclusions. Methods state that two of the three variables describe the county and that registry practice can load onto the block.

## Suggested revisions

**S1 (REV-2).** The AUC 0.671 to 0.673 example is no longer offered as support that small gains are informative. It is now cited as precedent for incremental-value analysis.
**S2 (REV-15).** "Models disagree" is replaced by labels distinguishing same-direction, below-threshold results from opposite directions.
**S3 (REV-16).** Grid-edge C values for the secondary outcome are reported in Results.
**S4 (REV-17).** The Introduction and Discussion are prose, and the Abstract is shortened, although still above 300 words.
**S5 (REV-19).** The Figure 3 legend notes the differing panel scales, and the Figure 4 legend notes that the Figure 4a axis does not start at 0. Figure 4b itself was not revised.
**S6 (REV-20).** The Table 1 note gives dollar ranges for the income quartiles.
**S7 (REV-29).** Results now state that weighting changed published percentages by at most 0.36 points, and 0.21 in groups of 1,000 men or more.
**S8 (REV-30).** Methods describe LightGBM missing-value handling, the logistic interaction terms and that no model is released; performance is reported by risk group, and the number of clusters is in Supplementary Table S14.
**S9 (REV-31).** Results state that no interval was computed for the LightGBM against logistic regression differences.
**S10 (REV-32).** Logistic regression with year as categories is reported (Supplementary Table S15).
**S11 (REV-34).** Results state that 98 of 100 refers to intervals and note the 0.00 lower bound.
**S12 (REV-37).** "Lower is better" labels are removed; Results state once that a longer wait is not necessarily worse care for low-risk men.
**S13 (REV-38).** Results say low-risk clinical variables vary little by definition.
**S14 (REV-39).** The active-surveillance exclusion is stated as an assumption that was not verified against the coding manual. Long and top-coded intervals by risk group and rurality are in Supplementary Table S7. The coding rule itself is not cited.
**S15 (REV-40).** The Huang et al. finding is restricted to favourable-risk disease, and its rural surveillance finding is used in the selection discussion.
**S16 (REV-41).** Noone et al. is described with its population, years and the authors' caution about treated-untreated comparisons.
**S17 (REV-42).** Supplementary Box 2 uses candidate-analogue wording.
**S18 (REV-43).** The waiting-time and mortality pattern is attributed to Ang et al.; the triage reading is presented as ours.
**S19 (REV-44).** Khorana et al. [1] is cited for the time trend and academic-centre intervals.
**S20 (REV-45).** SEER variable names for clinical Gleason score and PSA are given.
**S21 (REV-47).** Excess days per man are given alongside the per-1,000 figure; top-coded shares are in Supplementary Table S7; Results explain that the 7-day threshold applied to standardised days, which were not modelled.
**S22 (REV-48).** The Foley 2025 restriction to men not treated with external beam radiotherapy is restored.
**S23 (REV-49).** Methods give the average-rank tie rule and state that the index is not need-standardised.

## Items marked consider

**S24 (REV-50).** Methods, Sensitivity analyses state that the scenarios reuse largely the same men, so agreement is not independent replication.
**S25 (REV-51).** The limitations note that the SEER diagnosis date may not be recorded consistently across registries and years.
