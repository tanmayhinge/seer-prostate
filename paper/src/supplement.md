# Supplementary material

**What area and marital characteristics add to clinical need in predicting waits beyond 90 days for prostate cancer surgery or radiotherapy: a machine learning analysis of US SEER data, 2010 to 2022**

How to read this supplement:
- **Source of tables:** every table is copied by script from the generated analysis reports in the public repository (https://github.com/tanmayhinge/seer-prostate), so the tables match the analysis outputs exactly.
- **Labels:** tables generated before revision 1 call the area and marital block "social position".
- **Post-review analyses:** Supplementary Tables S7, S11 to S15, S17, S18, S21, S22 and S35 come from analyses specified after an internal review (protocol amendment 1.9); S17 and S18 publish results computed under amendment 1.7.
- **Numbers of men:** in cross-tabulations they are rounded to the nearest 10, and statistics resting on 1 to 4 men are shown as <5.
- **References:** numbered as in the main text.

## Supplementary Box 1. Survival comparisons and immortal time bias (not estimated)

Comparing survival between treated and untreated men is exposed to immortal time bias, because treated men must survive until treatment starts. A simulation study of observational research found that time-fixed and exclusion methods overestimated a treatment's benefit, that a 1-year landmark method reduced the bias but did not remove it, and recommended the time-dependent method [29]. A suitable design would treat treatment as a time-dependent exposure, with competing risks of prostate cancer death and death from other causes, and use a 12-month landmark analysis only as a sensitivity analysis. This design is described, not estimated, in this study.

## Supplementary Box 2. Candidate Australian analogues of the SEER variables (no Australian data analysed)

Published analyses of the Prostate Cancer Outcomes Registry in Tasmania used the measures below [24, 25]. They are candidate analogues, not equivalents: the geographic units, the construction of the measures and the health systems differ, and availability for any new study must be confirmed against the registry's data dictionary.
- **Rurality:** the county Rural-Urban Continuum Code has a candidate analogue in Australian Statistical Geography Standard remoteness areas, assigned by residential postcode.
- **Area income:** county median household income has a candidate analogue in the SEIFA Index of Relative Socio-Economic Advantage and Disadvantage, assigned by postcode.
- **Insurance and sector:** SEER has no insurance variable. The closest Australian contrast studied is a public or private treating facility.

Data gaps reported in those analyses were no comorbidity data [24], patient-reported outcomes collected consistently only from 2018 [25], and no way to tell whether external beam radiotherapy was given in a public or private facility [25]. Referral, biopsy and multidisciplinary meeting dates are not assumed to be available.

## Supplementary Table S1. Treated men by interval status
Men meeting cohort steps 1 to 6.

<!-- table: reports/phase3.md | ## Table 1b. -->

## Supplementary Tables S2 to S6. Crude waiting beyond 90 days
Medians and 90th percentiles treat top-coded intervals as 731 days.

### Supplementary Table S2. By risk group
<!-- table: reports/phase4_descriptive.md | ### D1. -->

### Supplementary Table S3. By risk group and county rurality
<!-- table: reports/phase4_descriptive.md | ### D2. -->

### Supplementary Table S4. By risk group and county income quartile
<!-- table: reports/phase4_descriptive.md | ### D3. -->

### Supplementary Table S5. By risk group and marital status
<!-- table: reports/phase4_descriptive.md | ### D4. -->

### Supplementary Table S6. By year of diagnosis
<!-- table: reports/phase4_descriptive.md | ### D5. -->

## Supplementary Table S7. Long and top-coded intervals (post-review)
<!-- table: reports/phase4_revision.md | ## (g) Long and top-coded intervals -->

## Supplementary Table S8. Model performance at every step
AUC: 0.5 is chance. Calibration intercept: 0 is ideal. Calibration slope: 1 is ideal.

<!-- table: reports/phase4_models.md | ## Performance at every step -->

## Supplementary Table S9. Skill lost when one variable is removed from step 2
Rurality and county income are strongly correlated, so removing one lets the other partly stand in for it.

<!-- table: reports/phase4_models.md | ## Which social variable carries the gain -->

## Supplementary Table S10. Tuned hyperparameters (primary analysis, tuned at step 3)

<!-- table: reports/phase4_models.md | ## Tuning -->

## Supplementary Tables S11 to S15. Post-review robustness analyses of the primary estimand

### Supplementary Table S11. Area and marital increment with per-step tuning and repeated fold assignment
Intervals come from the first fold seed and do not include model-fitting variability; the seed range shows how much the estimate moves across 10 fold assignments.

<!-- table: reports/phase4_revision.md | ## (a) and (b) -->

### Supplementary Table S12. Clinical model comparison under per-step tuning
<!-- table: reports/phase4_revision.md | ### Clinical model comparison under per-step tuning -->

### Supplementary Table S13. Hyperparameters chosen at each step
<!-- table: reports/phase4_revision.md | ### Hyperparameters chosen at each step -->

### Supplementary Table S14. Bootstrap clusters by stratum
<!-- table: reports/phase4_revision.md | ## (c) Bootstrap clusters -->

### Supplementary Table S15. Stage-free clinical block and year as categories
<!-- table: reports/phase4_revision.md | ## (d) Stage-free -->

## Supplementary Table S16. Standardised percentage waiting more than 90 days by profile, all men

<!-- table: reports/phase4_equity_selection.md | ### Standardised percentages by profile, all men (pooled) -->

## Supplementary Tables S17 and S18. One-at-a-time rurality and income profiles (not interpreted)
These profiles change rurality or county income alone, holding the other at the reference profile, which creates combinations rarely observed in the data. The two model types conflict, which is why joint area profiles are reported instead (amendment 1.7).

### Supplementary Table S17. Contrasts (percentage points)
<!-- table: reports/phase4_revision.md | ### Contrasts (percentage points) -->

### Supplementary Table S18. Standardised percentages
<!-- table: reports/phase4_revision.md | ### Standardised percentages -->

## Supplementary Table S19. Crude excess waiting days beyond 90 days per 1,000 men

<!-- table: reports/phase4_equity_selection.md | ### Crude excess waiting days -->

## Supplementary Table S20. Erreygers concentration index by risk group
Crude within each stratum; it does not separate income from rurality.

<!-- table: reports/phase4_equity_selection.md | ## A6. Income inequality in delay -->

## Supplementary Tables S21 and S22. Concentration index by diagnosis period (post-review)

### Supplementary Table S21. Erreygers index by period
<!-- table: reports/phase4_revision.md | ## (f) Income concentration index by diagnosis period -->

### Supplementary Table S22. County income quartile distribution by period
<!-- table: reports/phase4_revision.md | ### County income quartile distribution by period -->

## Supplementary Tables S23 to S26. Bounds for men without a recorded interval
The lower bound assumes every man without a recorded interval waited 90 days or less; the upper bound assumes every such man waited longer. These bounds do not address selection into recorded treatment.

### Supplementary Table S23. By risk group
<!-- table: reports/phase4_equity_selection.md | ### Bounds by risk group -->

### Supplementary Table S24. By rurality
<!-- table: reports/phase4_equity_selection.md | ### Bounds by rurality -->

### Supplementary Table S25. By county income quartile
<!-- table: reports/phase4_equity_selection.md | ### Bounds by county income quartile -->

### Supplementary Table S26. By marital status
<!-- table: reports/phase4_equity_selection.md | ### Bounds by marital status -->

## Supplementary Table S27. Skill added in predicting a missing interval

<!-- table: reports/phase4_equity_selection.md | ### Is having a recorded interval predictable -->

## Supplementary Table S28. Inverse probability weighted percentages

<!-- table: reports/phase4_equity_selection.md | ### Inverse probability weighted percentages -->

## Supplementary Tables S29 to S35. Sensitivity analyses

### Supplementary Table S29. Percentage waiting beyond the threshold, by scenario
<!-- table: reports/phase4_sensitivity.md | ## Percentage waiting beyond the threshold -->

### Supplementary Table S30. Area and marital increment by scenario
<!-- table: reports/phase4_sensitivity.md | ## Social position increment by scenario -->

### Supplementary Table S31. Standardised area contrast by scenario, all men
<!-- table: reports/phase4_sensitivity.md | ### Area: -->

### Supplementary Table S32. Standardised marital status contrast by scenario, all men
<!-- table: reports/phase4_sensitivity.md | ### Marital status: -->

### Supplementary Table S33. All area and marital features as observed minus the reference profile, by scenario, all men
<!-- table: reports/phase4_sensitivity.md | ### All social features -->

### Supplementary Table S34. Penalised logistic regression with a wider C grid (post hoc)
<!-- table: reports/phase4_sensitivity.md | ## Penalised logistic regression with a wider C grid -->

### Supplementary Table S35. Clinical need increment with and without radiotherapy patients
<!-- table: reports/phase4_revision.md | ## Clinical need increment when radiotherapy patients are excluded -->

## Supplementary Tables S36 to S42. Secondary outcome: recorded curative treatment
No record can mean active surveillance, watchful waiting, hormone therapy only, refusal, or treatment the registry did not capture [20]. A lower percentage cannot be read as under-treatment.

### Supplementary Table S36. By risk group
<!-- table: reports/phase4_receipt.md | ### By risk group -->

### Supplementary Table S37. By risk group and county rurality
<!-- table: reports/phase4_receipt.md | ### By risk group and county rurality -->

### Supplementary Table S38. By risk group and county income quartile
<!-- table: reports/phase4_receipt.md | ### By risk group and county income quartile -->

### Supplementary Table S39. By risk group and marital status
<!-- table: reports/phase4_receipt.md | ### By risk group and marital status -->

### Supplementary Table S40. Value added at each step
<!-- table: reports/phase4_receipt.md | ## Value added at each step -->

### Supplementary Table S41. Standardised contrasts
<!-- table: reports/phase4_receipt.md | ### Contrasts (percentage points) -->

### Supplementary Table S42. Standardised percentages by profile, intermediate and high risk pooled
<!-- table: reports/phase4_receipt.md | ### Standardised percentages by profile -->

## Supplementary Table S43. Protocol amendment log

<!-- table: PROTOCOL.md | ## Amendment log -->

## Supplementary Table S44. Protocol versions by commit
Commit times are recorded by the author's computer; the repository was first made public on 13 September 2026, after the analyses.

<!-- table: reports/protocol_history.md | ## Protocol versions by commit -->

## Supplementary figures

![Supplementary Figure S1](figures/figureS1_calibration.png)

**Supplementary Figure S1. Calibration of out-of-fold predicted probabilities at step 2** (clinical need plus area and marital characteristics), in 10 equal-count bins, by risk group and model type. The dashed line marks perfect calibration.

![Supplementary Figure S2](figures/figureS2_sensitivity.png)

**Supplementary Figure S2. Log-loss skill added by the area and marital block under each sensitivity scenario,** all men, with 95% cluster bootstrap intervals. Each scenario changes one setting from the primary analysis. The threshold scenarios use a different outcome, so their values are not directly comparable with the others.

## Supplementary Table S45. STROBE and RECORD checklist

Item wording is abbreviated from the RECORD statement checklist, which includes the STROBE items [13, 14]. Locations refer to sections of the main text unless marked S (supplement).

| Item | Topic | Where reported |
|---|---|---|
| 1a, 1b | Design in title or abstract; informative abstract | Abstract (Methods names a retrospective cohort study) |
| RECORD 1.1 | Type of data and database named | Title and Abstract (SEER registry data) |
| RECORD 1.2 | Region and time frame | Title and Abstract (US, 2010 to 2022) |
| RECORD 1.3 | Linkage stated | Methods, Design: county attributes linked by SEER; no person-level linkage |
| 2 | Background and rationale | Introduction |
| 3 | Objectives | Introduction, final paragraph |
| 4 | Study design | Methods, Design |
| 5 | Setting, locations and dates | Methods, Design and Cohort |
| 6a | Eligibility and selection | Methods, Cohort; Figure 1 |
| 6b | Matching | Not applicable |
| RECORD 6.1 | Codes and algorithms for population selection | Methods, Cohort; config/analysis.yaml in the repository |
| RECORD 6.2 | Validation of codes | Methods, Secondary outcome [20]; no validation study of the cohort algorithm |
| RECORD 6.3 | Linkage flow diagram | Not applicable (no person-level linkage) |
| 7 | Outcomes, exposures, predictors defined | Methods, Outcome, Risk groups and Ordered feature steps |
| RECORD 7.1 | Complete list of codes | config/analysis.yaml in the repository |
| 8 | Data sources and measurement | Methods, Design, Outcome and Risk groups |
| 9 | Efforts to address bias | Methods, Men without a recorded interval and Sensitivity analyses; Discussion, Strengths and limitations |
| 10 | Study size | Methods, Cohort (all eligible men, no sample size calculation); Figure 1 |
| 11 | Quantitative variables | Methods, Ordered feature steps |
| 12a | Statistical methods | Methods, Models and validation, Standardised percentages and Income concentration index |
| 12b | Subgroups and interactions | Methods, Models and validation (risk-group strata; clinical interaction terms) |
| 12c | Missing data | Methods, Ordered feature steps, Models and validation, and Men without a recorded interval |
| 12d | Loss to follow-up | Not applicable (outcome is the recorded interval; top-coding described in Methods, Outcome) |
| 12e | Sensitivity analyses | Methods, Sensitivity analyses and post-review robustness analyses |
| RECORD 12.1 | Access to the database population | Methods, Design (full case listing of the selected site and years) |
| RECORD 12.2 | Data cleaning | Methods, Cohort (explicit label mapping) |
| RECORD 12.3 | Linkage methods | Not applicable (no person-level linkage) |
| 13a to 13c | Numbers at each stage, reasons, flow diagram | Results, Cohort; Figure 1 |
| RECORD 13.1 | Selection of included persons | Methods, Cohort; Figure 1 |
| 14a, 14b | Characteristics and missing data | Table 1 (unknown categories shown) |
| 14c | Follow-up time | Not applicable |
| 15 | Outcome data | Results, Waiting beyond 90 days; Tables S2 to S6 |
| 16a | Estimates and precision | Table 2 (intervals); Table 3 (no intervals, stated) |
| 16b | Category boundaries | Methods, Risk groups; Table 1 note (income quartiles) |
| 16c | Absolute measures | Results, Standardised percentages and excess days |
| 17 | Other analyses | Results, Sensitivity analyses and post-review robustness analyses; Tables S11 to S15, S29 to S35 |
| 18 | Key results | Discussion, Principal findings |
| 19 | Limitations | Discussion, Strengths and limitations |
| RECORD 19.1 | Implications of routinely collected data | Discussion, Strengths and limitations; What the direction can and cannot show |
| 20 | Interpretation | Discussion |
| 21 | Generalisability | Discussion, Australian context and Strengths and limitations |
| 22 | Funding | Declarations |
| RECORD 22.1 | Access to protocol, data and code | Methods, Design; Declarations |

## Supplementary Table S46. TRIPOD+AI checklist

Item wording is abbreviated from the TRIPOD+AI checklist [15]. Development and internal evaluation use the same data through cross-fitting; the models are measurement tools and are not proposed for clinical use.

| Item | Topic | Where reported |
|---|---|---|
| 1 | Title | Title (prediction, population and outcome named) |
| 2 | Abstract | Abstract |
| 3a | Healthcare context and rationale | Introduction |
| 3b | Target population and intended purpose | Introduction, final paragraph; Methods, Models and validation (not intended for clinical use) |
| 3c | Known health inequalities | Introduction, second paragraph |
| 4 | Objectives | Introduction, final paragraph |
| 5a | Data sources | Methods, Design |
| 5b | Dates of data | Methods, Design and Cohort |
| 6a | Setting | Methods, Design (population-based registries) |
| 6b | Eligibility | Methods, Cohort |
| 6c | Treatments | Methods, Cohort and Ordered feature steps (treatment type at step 3) |
| 7 | Data preparation | Methods, Cohort (label mapping) |
| 8a | Outcome definition | Methods, Outcome |
| 8b, 8c | Outcome assessors and blinding | Not applicable (registry-abstracted outcome) |
| 9a | Choice of predictors | Methods, Ordered feature steps (pre-specified in the protocol) |
| 9b | Predictor definitions | Methods, Risk groups and Ordered feature steps; config/analysis.yaml |
| 9c | Predictor assessors | Not applicable (registry-coded predictors) |
| 10 | Sample size | Methods, Cohort (all eligible men) |
| 11 | Missing data | Methods, Ordered feature steps, Models and validation, and Men without a recorded interval |
| 12a | Data use and partitioning | Methods, Models and validation (5-fold cross-fitting) |
| 12b | Predictor handling | Methods, Ordered feature steps and Models and validation |
| 12c | Model type, building steps, tuning, internal validation | Methods, Models and validation |
| 12d | Heterogeneity across clusters | Methods, Models and validation (cluster bootstrap only; heterogeneity across clusters not quantified) |
| 12e | Performance measures | Methods, Models and validation; Supplementary Figure S1 |
| 12f | Model updating | Not applicable |
| 12g | How predictions were calculated | Code in the repository |
| 13 | Class imbalance | Methods, Models and validation (none used) |
| 14 | Fairness | Not addressed as a model property; differences by area and marital status are the study's measured quantity |
| 15 | Model output | Predicted probabilities; no classification threshold |
| 16 | Training versus evaluation differences | Not applicable (cross-fitting within the same data) |
| 17 | Ethical approval | Methods, Design; Declarations |
| 18a to 18f | Funding, conflicts, protocol, registration, data and code sharing | Methods, Design; Declarations |
| 19 | Patient and public involvement | Methods, Design; Declarations (none) |
| 20a | Participant flow and outcome counts | Results, Cohort and Waiting beyond 90 days; Figure 1 |
| 20b | Participant characteristics | Table 1 |
| 20c | Comparison with development data | Not applicable |
| 21 | Participants and events per analysis | Table 2; Tables S2, S8 and S10 |
| 22 | Full model specification | Not released as a clinical model; code that refits every model is in the repository |
| 23a | Performance with confidence intervals, including subgroups | Table 2 and Table S8 by risk group (skill increments with intervals; AUC and calibration without intervals) |
| 23b | Heterogeneity across clusters | Not examined |
| 24 | Model updating results | Not applicable |
| 25 | Interpretation | Discussion |
| 26 | Limitations | Discussion, Strengths and limitations |
| 27a, 27b | Input data handling and user interaction in implementation | Not applicable (no implementation proposed) |
| 27c | Next steps | Discussion, Australian context; Conclusions |
