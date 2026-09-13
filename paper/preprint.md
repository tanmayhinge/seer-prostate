# Waiting for prostate cancer treatment: how much is clinical need? A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022

**Author:** Tanmay Hinge [AUTHOR TO CONFIRM: affiliation, ORCID]

**Correspondence:** hingetanmay@gmail.com

**Status:** draft for medRxiv, not peer reviewed.

## Abstract

**Background.** The Australian optimal care pathway for prostate cancer recommends that surgery or radiotherapy begin within 3 months of diagnosis. Studies of waiting times report associations with single social factors, but not how much social position adds to predicting delay once clinical need is known.

**Methods.** Retrospective cohort study of the US Surveillance, Epidemiology, and End Results (SEER) 17 registries.
- **Men:** aged 40 or over, diagnosed 2010 to 2022 with localised or regional prostate cancer, whose first course of treatment included radical prostatectomy or radiotherapy, with a recorded interval above 0 days.
- **Outcome:** first recorded treatment more than 90 days after diagnosis.
- **Models:** cross-fitted penalised logistic regression and gradient boosting (LightGBM), built in ordered steps (year; clinical need; social position, meaning marital status, county rurality and county income; treatment type), within clinical risk groups.
- **Primary estimand:** out-of-fold log-loss skill added by social position, with cluster bootstrap intervals.
- **Further analyses:** standardised percentages, an income concentration index, selection bounds, 10 sensitivity analyses, and recorded curative treatment as a secondary outcome.

**Results.**
- **Delay:** of 330,827 men, 39.7% waited more than 90 days (lower is better). The share rose from 36.0% in 2010 to 52.3% in 2022.
- **Predictability:** it was low, with AUC 0.592 to 0.663 across risk groups and models (0.5 is chance).
- **Social position increment:**
  - 0.62 percentage points of skill (95% interval 0.39 to 0.87) under penalised logistic regression and 0.99 (0.73 to 1.30) under LightGBM;
  - intervals above 0 in every risk group;
  - in low-risk men it added more than clinical need did.
- **Model comparison:** LightGBM had higher out-of-fold skill than penalised logistic regression in every risk group.
- **Standardised differences** (clinical features kept as observed):
  - men in non-metropolitan counties not adjacent to a metropolitan area were 9.2 (logistic regression) and 8.8 (LightGBM) percentage points less likely to wait more than 90 days than men in large metropolitan counties;
  - never-married men were 6.7 and 5.9 points more likely to wait than married men.
- **Income:** delay was concentrated among men in higher-income counties (Erreygers index 0.062, 0.039 to 0.083; 0 means no income gradient).
- **Sensitivity analyses:** the social position increment stayed above 0 in 98 of 100 results.

**Conclusions.** In US registry data, social position adds a small but consistent amount to predicting waits beyond the Australian 3-month benchmark, over and above recorded clinical need. Waits beyond the benchmark were more common, not less, in large metropolitan and higher-income counties. Registries that record referral dates, treating sector and comorbidity could test what this signal represents.

## Introduction

Timely treatment is a standard measure of cancer care quality.
- **The benchmark:** the Australian optimal care pathway for men with prostate cancer states that surgery or radiation therapy should begin within 3 months of diagnosis, or within 4 weeks when local symptoms are pronounced [1].
- **Tasmanian findings:** analyses of the Prostate Cancer Outcomes Registry in Tasmania report unequal waits.
  - Men from outer regional and remote areas took a median of 82 days to start active treatment, against 75 days for men from inner regional areas. The age-adjusted mean difference was 9.25 days (95% CI 1.72 to 16.79) [2].
  - Among men not treated with external beam radiotherapy, men treated in public facilities started treatment later than men treated privately. Adjusted mean differences were 43.46 days in low-risk, 59.22 days in intermediate-risk and 42.25 days in high-risk disease [3].
- **Lung cancer in Tasmania:** benchmarking against optimal care pathway standards found that on average 7% of patients (range 0 to 16%) met the treatment-time standards [4]. General practitioners described fragmented referral and limited rural specialist access as barriers [5].

Large US registry studies describe who waits.
- **SEER:** mean time to treatment for prostate cancer was 82.75 days in 2021 [6]. Across four cancers from 2015 to 2020, time to treatment was shorter for lower-income and non-metropolitan patients [7].
- **Tennessee registry:** residence in rural Appalachian counties was associated with lower odds of waiting more than 90 days (odds ratio 0.83, 95% CI 0.78 to 0.89) [8].
- **National Cancer Database:** the median time to treatment for prostate cancer was 79 days (interquartile range 55 to 117) [9].

These studies report adjusted associations for one factor at a time, usually pooled across risk groups. Waiting, however, is partly triage. Men with aggressive disease are treated sooner, which is why unadjusted comparisons of waiting time and survival can run in the wrong direction [10].

A different question is how much of the variation in waiting can be predicted from clinical need, and how much more social position adds beyond it.
- **Why this framing:** out-of-sample prediction measures the size of the social signal without assuming its direction. That matters because rural and income effects on timeliness point in different directions across studies [2, 7, 8].
- **A small gain can still be informative:** in one US health system, adding neighbourhood variables to a clinical model predicting advanced prostate cancer changed the AUC from 0.671 to 0.673 [11].
- **Why two model types:** flexible models such as gradient boosting [12] can adjust for clinical need without assuming linear effects. Comparing them with penalised regression shows whether any social increment is an artefact of an under-fitted clinical model.

**Aim.** Within clinical risk groups, among men treated with radical prostatectomy or radiotherapy, the study measures how much marital status, county rurality and county income add to predicting a wait beyond the Australian 3-month benchmark. It also expresses that contribution as standardised percentages and an income concentration index, and tests how sensitive the result is to the cohort and outcome definitions.

## Methods

### Design, data and protocol
**Design and data**
- Retrospective cohort study using the SEER Research Data, 17 registries, November 2025 submission, linked to county attributes [13].
- A SEER\*Stat case listing was exported with a selection by site (prostate) and year of diagnosis (2010 to 2023) only, giving 793,214 tumour records. No age restriction was applied at export.

**Protocol**
- The protocol (`PROTOCOL.md`) fixed the cohort, definitions, estimand, models and analyses before any outcome model was fitted. It was committed to version control before the first cohort was built; it was not registered externally.
- Twelve amendments are logged with dates and reasons (Supplementary Table S32). Two were made after seeing results and are labelled that way:
  - replacing one-at-a-time rurality and income profiles with joint area profiles, after a development run on 5 bootstrap resamples;
  - a wider penalty grid for logistic regression.

**Reporting and ethics**
- Reporting follows STROBE [14], RECORD [15] and, for the prediction models, TRIPOD+AI [16].
- **Ethics:** [AUTHOR TO CONFIRM: ethics statement. The data are de-identified and released under the SEER Research Data Use Agreement.]

### Cohort
Exclusions were applied in this order (Figure 1):
1. First primary cancer (one primary only, or the first of two or more).
2. Localised or regional combined summary stage.
3. Not a death certificate or autopsy case, identified from the survival months flag because the type of reporting source was not in the export.
4. Aged 40 or over.
5. Diagnosed 2010 to 2022. 2023 was excluded because of truncated follow-up and new surgery codes.
6. First course of treatment includes radical prostatectomy or radiotherapy.
7. Interval recorded or top-coded.
8. Interval above 0 days, because a 0-day interval usually marks a cancer found at a procedure.

**Treatment definitions**
- **Radical prostatectomy:** surgery codes 50, 70 or 80 (A500, A700 or A800 from 2023), checked against the SEER coding manual [17].
- **Radiotherapy:** beam radiation, implants or brachytherapy, combinations, radioisotopes, or radiation not otherwise specified.

**Active surveillance.** SEER records the first course of treatment only. Men whose first course was active surveillance have surgery and radiation coded as none, so they are not in this cohort.

### Outcome
- **Source:** SEER's time from diagnosis to treatment in days. It ends at the first treatment of any kind, which can include hormone therapy, not recorded in this export.
- **Primary outcome:** a wait of more than 90 days, following the optimal care pathway benchmark [1]. Intervals top-coded at 731 days or more count as delayed.
- **Sensitivity thresholds:** 60, 120 and 180 days.

### Clinical risk groups
Risk groups used clinical information only, because pathological grade is observed only after surgery.
- **High:** regional stage, clinical Gleason score 8 to 10, or PSA above 20 ng/ml.
- **Unknown:** otherwise, if Gleason score or PSA was missing.
- **Intermediate:** otherwise, Gleason score 7 or PSA 10 to 20 ng/ml.
- **Low:** Gleason score 6 or lower and PSA below 10 ng/ml.

### Ordered feature steps
The blocks shared no columns.
- **Step 0 (base):** year of diagnosis and a 2020 indicator.
- **Step 1 (clinical need):** added stage category, clinical Gleason score with a missing indicator, log PSA with top-code and missing indicators, and age band midpoint.
- **Step 2 (social position):** added the following.
  - Marital status: 7 categories including unknown.
  - County Rural-Urban Continuum Code: 5 levels plus unknown.
  - County median household income: 16 inflation-adjusted bands, entered as an ordinal rank plus an unknown indicator.
- **Step 3 (treatment type):** added treatment type (prostatectomy, radiotherapy, or both).

Treatment type entered after social position because social factors can influence the choice of treatment, and adjusting for it first would remove part of the social contribution.

### Models and validation
**Models**
- **Penalised logistic regression:** L2 penalty, median imputation, standardisation and pairwise interactions among clinical features [18].
- **LightGBM:** learning rate 0.05 [12].

**Tuning**
- Hyperparameters were tuned once per model and stratum, by 3-fold cross-validated log-loss on a random subsample of 50,000 men at step 3, and then reused at every step.
- Grids: C from 0.01 to 10; 200 or 500 trees; 15 or 63 leaves; a minimum of 50 or 200 men per leaf.
- Tuning was not nested inside the evaluation folds.

**Validation**
- All predictions were out-of-fold, from 5-fold stratified cross-fitting within each risk group and in all men pooled.
- **Log-loss skill** is 1 minus a step's log-loss divided by the log-loss of the step 0 model; 0 means no improvement and higher is better.
- Brier skill, AUC, and calibration intercept and slope were also computed.
- **Primary estimand:** the skill added from step 1 to step 2.

**Uncertainty**
- Rurality and income are county-level measures, and the export has no county or registry identifier.
- Intervals therefore come from a cluster bootstrap over the 79 cells formed by rurality and income band: 500 resamples of out-of-fold predictions, percentile intervals, no refitting.
- The social block is interpreted as geographic and social position, including any unmeasured registry differences.

**Leave-one-variable-out refits** removed marital status, rurality or income from step 2 in turn.

### Standardised percentages
**Method**
- Standardised percentages came from g-computation using a step 2 model fitted to all men in each stratum.
- Each man kept his own clinical features and year, while his social features were set to a profile. The mean predicted probability gave the standardised percentage.

**Profiles**
- **Reference:** married, a county in a metropolitan area of 1 million or more, and county income rank at the 83.33% quantile of the cohort (the middle of the top income tertile).
- **Area profiles:** rurality and county income were set together, at the median income band of men living in each type of area. Rurality and income are strongly correlated in this cohort (Table 1), so changing one while holding the other fixed creates combinations that are rarely observed.

**Judging differences.** Bootstrap intervals that hold the fitted model fixed ignore model-fitting uncertainty, so a contrast was described as meaningful only when both model types agreed on 3 percentage points or more in the same direction. Crude excess waiting days beyond 90 days per 1,000 men were reported by rurality and income.

### Income inequality
- **Index:** the Erreygers-corrected concentration index [19] of waiting more than 90 days, ranking men by county median household income (poorest first).
- **Interpretation:** it ranges from -1 to 1. Positive values mean delay is concentrated in higher-income counties, and 0 means no gradient.
- **Uncertainty:** intervals used the same cluster bootstrap.

### Men without a recorded interval
Among treated men, three checks examined men without a recorded interval:
- **Bounds:** the percentage delayed was bounded by assuming every man without an interval waited 90 days or less, and then that every such man waited longer.
- **Membership model:** a model for having no recorded interval measured whether this was predicted by social position beyond clinical need.
- **Weighting:** percentages were reweighted by the inverse of the predicted probability of having a recorded interval.

### Sensitivity analyses
**Scenarios.** Ten scenarios each changed one setting:
- thresholds of 60, 120 and 180 days;
- risk groups from Gleason score and PSA only;
- prostatectomy without radiotherapy only;
- excluding 2020;
- including 2023;
- including 0-day intervals;
- one primary cancer only;
- excluding prostatectomy not otherwise specified.

**Refitting.** Steps 0 to 2 were refitted for both models with the primary hyperparameters. A post hoc check re-tuned logistic regression on a wider grid (C from 0.0001 to 10).

### Secondary outcome: recorded curative treatment
**Cohort and outcome**
- **Men:** intermediate- and high-risk men meeting cohort steps 1 to 5.
- **Outcome:** a record of radical prostatectomy or radiotherapy in the first course.
- **What no record can mean:** active surveillance, watchful waiting, hormone therapy only, refusal, or treatment the registry did not capture [20]. It is therefore not described as untreated.

**Analysis.** The same ordered steps (0 to 2), models, bootstrap and standardisation were used, with hyperparameters tuned on step 2.

### Disclosure control and software
**Disclosure control**
- As the SEER Research Data Use Agreement requires, statistics based on 1 to 4 men are suppressed.
- Counts in cross-tabulations are rounded to the nearest 10, and delayed counts are not shown, so hidden cells cannot be recovered by subtraction.

**Software and reproducibility**
- Python 3.13, pandas 3.0.5, NumPy 2.5.3, scikit-learn 1.9.1, LightGBM 4.7.0, statsmodels 0.15.0 and matplotlib 3.11.2, with seed 20260913.
- All settings are in configuration files, and every table and figure is regenerated by scripts with unit tests.

## Results

### Cohort
**Inclusion flow (Figure 1)**
- Of 793,214 records, 557,683 met the first five steps.
- 355,581 had radical prostatectomy or radiotherapy in the first course.
- 330,827 had a recorded interval above 0 days.

**Characteristics (Table 1)**
- **Treatment:** 48.2% had radical prostatectomy, 47.9% radiotherapy and 3.9% both.
- **Risk groups:** 17.4% low risk, 38.6% intermediate, 39.6% high and 4.5% unknown.
- **Rurality and income:** they overlapped heavily. 45.6% of men in non-metropolitan counties not adjacent to a metropolitan area lived in the lowest county income quartile, against 1.1% of men in metropolitan counties of 1 million or more.

### Waiting beyond 90 days
**Overall.** The median wait was 77 days (interquartile range 52 to 116), and 39.7% of men waited more than 90 days (lower is better).

**By group (Figure 2)**
- **Risk group:** delay was more common in low-risk men (47.9%) than in high-risk men (32.8%). Intermediate-risk men were at 42.8%.
- **Year:** the share rose from 36.0% in 2010 to 52.3% in 2022.
- **Rurality:** within every risk group, delay was more common in large metropolitan counties than in non-metropolitan counties not adjacent to a metropolitan area. The gap was 50.7% against 39.0% in low-risk and 35.7% against 26.0% in high-risk men.
- **Income:** within every risk group, men in the lowest county income quartile were delayed less often than men in the highest (high risk: 26.7% against 33.4%).
- **Marital status:** never-married men were delayed more often than married men (high risk: 40.0% against 30.9%).

### How much social position adds
**Overall predictability.** It was low (Table 2).
- At step 2, AUC ranged from 0.592 to 0.663 across strata and models (0.5 is chance).
- Log-loss skill over year alone ranged from 0.76% to 4.90%.

**Clinical need**
- In all men, clinical need added 3.01 percentage points of skill (95% interval 2.69 to 3.38) under penalised logistic regression.
- In high-risk men it added 3.53 points.
- In low-risk men it added 0.14 points (0.08 to 0.20), and 0.02 (-0.09 to 0.13) under LightGBM.

**Social position (Figure 3)**
- **All men:** it added 0.62 points (0.39 to 0.87) under penalised logistic regression and 0.99 (0.73 to 1.30) under LightGBM.
- **High-risk men:** 0.86 (0.60 to 1.15) and 1.18 (0.90 to 1.56).
- **Low-risk men:** 0.62 (0.32 to 0.94) and 0.96 (0.67 to 1.28), making up 82% and 98% of step 2 skill.
- **Across strata:** every interval lay above 0.
- **Treatment type,** added afterwards, contributed 0.04 to 0.71 points.

**Model comparison and calibration**
- LightGBM had higher step 2 skill than penalised logistic regression in every stratum, by 0.23 to 0.90 points.
- Calibration slopes at step 2 were 0.98 to 1.00 for logistic regression and 0.88 to 1.03 for LightGBM, where 1 is ideal (Supplementary Figure S1).
- Logistic regression chose C = 0.01, the edge of the pre-specified grid, in every stratum. Re-tuning on a wider grid chose the same value, with identical results.

**Which social variable.** Removing marital status or rurality each lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata. The two models disagreed on how much income carried on its own: 0.00 to 0.02 points under logistic regression, and 0.26 to 0.29 under LightGBM.

### Standardised percentages and excess days
**Area profiles (Figure 4a, Table 3)**
- **Direction:** standardised delay was lower in non-metropolitan counties not adjacent to a metropolitan area than in large metropolitan counties, each at its typical county income ($55,000 to $59,999 against $90,000 to $94,999).
- **All men:** 9.2 points lower under logistic regression and 8.8 under LightGBM.
- **By risk group:** both models agreed on 3 points or more in the same direction in every risk group (-7.2 to -14.2 points).

**Marital status**
- Never-married men had standardised delay 6.7 and 5.9 points higher than married men.
- The models agreed in every stratum except low risk (3.6 and 2.4).

**All social features.** Setting every man's social features to the reference profile raised the pooled percentage by 1.1 and 1.6 points, under the 3-point rule.

**Excess days.** Crude excess waiting days beyond 90 days were 30,597 per 1,000 men in large metropolitan counties and 20,014 in non-metropolitan counties not adjacent to a metropolitan area (fewer is better).

### Income inequality
- **Direction:** delay was concentrated among men in higher-income counties (Figure 4b).
- **Index values:**
  - all men 0.062 (0.039 to 0.083);
  - low risk 0.103 (0.068 to 0.134);
  - intermediate risk 0.075 (0.051 to 0.096);
  - high risk 0.041 (0.017 to 0.065).

### Men without a recorded interval
- **How many:** 2.7% to 5.5% of treated men had no recorded interval, depending on rurality.
- **Worst-case bounds:** the rurality gap held under the extreme assumptions, at 40.2% to 45.7% for large metropolitan counties against 31.3% to 34.0% for non-metropolitan counties not adjacent to a metropolitan area.
- **Social patterning:** having no recorded interval was patterned by social position beyond clinical need (0.53 points of skill, 0.07 to 1.02).
- **Weighting:** inverse probability weighting changed group percentages by 0.2 points or less.

### Sensitivity analyses
**Social position increment (Supplementary Figure S2)**
- **Intervals:** the 95% interval lay above 0 in 98 of 100 scenario, stratum and model combinations. Both exceptions were in the unknown-risk stratum.
- **All men:** the increment ranged from 0.54 to 0.68 points under logistic regression and 0.94 to 1.06 under LightGBM.
- **Model comparison:** LightGBM had higher step 2 skill in 47 of 50 combinations; the three exceptions differed by 0.17 points or less.

**Standardised contrasts**
- **Area:** in all men, both models agreed on a lower delay of 3 points or more in remote counties in 9 of 10 scenarios. The exception was the 180-day threshold (-2.96 and -3.20).
- **Marital status:** the models agreed in all 10 scenarios.

### Secondary outcome: recorded curative treatment
**Crude.** Of 352,644 intermediate- and high-risk men, 75.4% of intermediate-risk and 81.1% of high-risk men had a recorded radical prostatectomy or radiotherapy.

**Models**
- **Predictability:** it was higher than for delay, with AUC at step 2 from 0.692 to 0.865.
- **Social position:** it added 1.96 points of skill (1.72 to 2.31) under logistic regression and 2.16 (1.92 to 2.54) under LightGBM, with every interval above 0.

**Standardised contrasts**
- **Marital status:** never-married men were 6.5 and 5.9 points less likely than married men to have a recorded curative treatment.
- **Area:** the difference between non-metropolitan counties not adjacent to a metropolitan area and large metropolitan counties was under 3 points (-2.9 and -1.4).

## Discussion

### Principal findings
**Clinical need and social position**
- In 330,827 US men treated with radical prostatectomy or radiotherapy, waiting more than 90 days was only weakly predictable from recorded clinical and social information.
- Clinical need predicted delay mainly in high-risk men, consistent with triage.
- Social position added a small amount of skill, 0.42 to 1.37 points of log-loss across strata and models, but the gain was consistent across risk groups, both model types and ten sensitivity analyses.
- In low-risk men, social position predicted more of the delay than clinical need did.

**Direction of the differences.** Men in large metropolitan and higher-income counties, and never-married men, were more often delayed, after clinical features were held as observed.

### Interpretation
**What the data cannot tell apart**
- A wait beyond 90 days can reflect considered deferral, patient choice, time for decisions between surgery and radiotherapy, or access problems.
- Registry data cannot separate these. The low predictability says that most of what determines the wait is not in the registry.

**The rural direction**
- It agrees with other US studies that found shorter intervals for non-metropolitan or rural patients [7, 8].
- It is not evidence that rural men receive better care. In the secondary analysis, crude recorded curative treatment was lower in remote than large metropolitan counties among high-risk men (75.3% against 81.9%), consistent with a national SEER study of guideline-concordant management [21], although the standardised difference was under 3 points.
- The data cannot test explanations such as longer surgical queues in large centres, second opinions, or wider choice of treatment settings.

**Marital status**
- Never-married men were both more often delayed and less often recorded as having curative treatment.
- This is consistent with higher use of surveillance or watchful waiting among unmarried men in an earlier SEER study [22].
- Without data on social support or comorbidity, the reason cannot be identified.

**The machine learning comparison**
- Gradient boosting improved on penalised regression by less than 1 point of skill in every stratum.
- The social increment was larger under gradient boosting. A more flexible clinical adjustment therefore did not absorb the social signal.
- Re-tuning over a wider penalty grid gave identical results, so the edge of the original grid does not explain the difference between model types.

### Relevance to Australian pathway research
**What no Australian data allow.** No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings. The area measures, health systems and interval definitions differ.

**What does transfer is the measurement approach**
- a benchmark-based outcome;
- risk-stratified ordered steps with out-of-sample skill;
- joint area profiles when remoteness and disadvantage are collinear;
- explicit handling of men without a recorded interval.

**What an Australian registry could add**
- Published PCOR-TAS analyses used remoteness areas and area socioeconomic indices assigned by postcode. They reported an adjusted difference of 9.25 days by remoteness, and of 42 to 59 days between public and private facilities [2, 3].
- A registry that records treating sector could add sector as its own block.
- Referral and multidisciplinary meeting dates would allow the interval to be divided into the parts a health service can act on.
- Comparing survival between treated and untreated men would need a design that avoids immortal time bias [23]. That comparison was not attempted here (Supplementary Box 1).

### Strengths and limitations
**Strengths**
- A large population-based cohort.
- A protocol fixed before modelling, with logged amendments.
- Out-of-sample estimation with two model types.
- Uncertainty that respects county-level exposures.
- Bounds for missing intervals and ten sensitivity analyses.
- Code that regenerates every table and figure.

**Limitations**
- **Missing variables:** the export had no race or ethnicity, insurance, registry identifier or comorbidity. Part of the social increment may therefore reflect unmeasured health or registry practice. A decomposition of treatment receipt that included comorbidity still left most of a racial gap unexplained [24], but that does not show the same here.
- **The interval** ends at the first treatment of any kind, including hormone therapy.
- **Treatment capture:** SEER under-captures treatment given outside reporting facilities. Against Medicare claims, SEER identified radiation therapy with 80% sensitivity [20].
- **Stage:** summary stage cannot separate T1 from T2 disease and partly uses pathology for surgical patients.
- **Ecological exposures:** rurality and income are county measures, not individual ones.
- **Tuning** was not nested, and standardised contrasts have no intervals.
- **Post hoc amendments:** two, labelled as such.
- **Associations only:** all results are associations, not causal effects.
- **Review:** the analysis was done by one person with AI coding assistance and has not been reviewed by a clinician or biostatistician.

### Conclusions
- **What the wait reflects:** in US registry data, whether a man waits beyond the Australian 3-month benchmark is mostly not predictable from recorded information.
- **Social position:** what is predictable is partly clinical triage and partly social position.
- **Direction:** the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties.
- **Next step:** measuring the same increment in a registry with referral dates, treating sector and comorbidity would show what the signal represents.

## Declarations

- **Funding:** [AUTHOR TO CONFIRM: none].
- **Competing interests:** [AUTHOR TO CONFIRM: none].
- **Data availability:** SEER data are available from the National Cancer Institute under a Research Data Use Agreement and cannot be shared by the author. Aggregate results tables are in the code repository.
- **Code availability:** [AUTHOR TO ADD: repository URL].
- **Use of AI tools:** [TO BE COMPLETED: disclosure statement]. Code, analyses and this draft were developed with assistance from Claude (Anthropic). The author is responsible for the design, checks and interpretation.

## Tables

### Table 1. Characteristics of the primary cohort by county rurality
Cells are n (% of the column's men), except days, which are median (interquartile range). Counts of 1 to 4 are shown as <5, and a second cell is hidden wherever a row or column total would reveal them.

| characteristic | level | Overall | Metro, 1 million or more | Metro, 250,000 to 1 million | Metro, under 250,000 | Nonmetro, adjacent to metro | Nonmetro, not adjacent to metro | Unknown |
|---|---|---|---|---|---|---|---|---|
| Men, n |  | 330,827 | 194,681 | 72,150 | 26,092 | 23,360 | 14,385 | 159 |
| Age at diagnosis | 40-44 years | 1,480 (0.4%) | 928 (0.5%) | 319 (0.4%) | 111 (0.4%) | 71 (0.3%) | 51 (0.4%) | 0 (0.0%) |
| Age at diagnosis | 45-49 years | 6,921 (2.1%) | 4,386 (2.3%) | 1,439 (2.0%) | 501 (1.9%) | 387 (1.7%) | 203 (1.4%) | 5 (3.1%) |
| Age at diagnosis | 50-54 years | 24,293 (7.3%) | 14,862 (7.6%) | 5,198 (7.2%) | 1,820 (7.0%) | 1,503 (6.4%) | 899 (6.2%) | 11 (6.9%) |
| Age at diagnosis | 55-59 years | 49,078 (14.8%) | 29,373 (15.1%) | 10,741 (14.9%) | 3,658 (14.0%) | 3,232 (13.8%) | 2,044 (14.2%) | 30 (18.9%) |
| Age at diagnosis | 60-64 years | 70,459 (21.3%) | 41,419 (21.3%) | 15,405 (21.4%) | 5,585 (21.4%) | 4,942 (21.2%) | 3,070 (21.3%) | 38 (23.9%) |
| Age at diagnosis | 65-69 years | 83,831 (25.3%) | 48,697 (25.0%) | 18,343 (25.4%) | 6,726 (25.8%) | 6,248 (26.7%) | 3,785 (26.3%) | 32 (20.1%) |
| Age at diagnosis | 70-74 years | 56,371 (17.0%) | 32,308 (16.6%) | 12,399 (17.2%) | 4,645 (17.8%) | 4,410 (18.9%) | 2,577 (17.9%) | 32 (20.1%) |
| Age at diagnosis | 75-79 years | 28,114 (8.5%) | 16,536 (8.5%) | 6,059 (8.4%) | 2,249 (8.6%) | 1,950 (8.3%) | 1,311 (9.1%) | 9 (5.7%) |
| Age at diagnosis | 80-84 years | 8,636 (2.6%) | 5,148 (2.6%) | 1,885 (2.6%) | 681 (2.6%) | 530 (2.3%) | <5 | <5 |
| Age at diagnosis | 85-89 years | 1,516 (0.5%) | 940 (0.5%) | 337 (0.5%) | 109 (0.4%) | 80 (0.3%) | <5 | <5 |
| Age at diagnosis | 90+ years | 128 (0.0%) | 84 (0.0%) | 25 (0.0%) | 7 (0.0%) | 7 (0.0%) | 5 (0.0%) | 0 (0.0%) |
| Year of diagnosis | 2010 to 2014 | 126,503 (38.2%) | 74,127 (38.1%) | 27,219 (37.7%) | 10,445 (40.0%) | 8,850 (37.9%) | 5,793 (40.3%) | 69 (43.4%) |
| Year of diagnosis | 2015 to 2019 | 122,936 (37.2%) | 72,147 (37.1%) | 26,945 (37.3%) | 9,621 (36.9%) | 8,749 (37.5%) | 5,431 (37.8%) | 43 (27.0%) |
| Year of diagnosis | 2020 to 2022 | 81,388 (24.6%) | 48,407 (24.9%) | 17,986 (24.9%) | 6,026 (23.1%) | 5,761 (24.7%) | 3,161 (22.0%) | 47 (29.6%) |
| Marital status | Married (including common law) | 232,525 (70.3%) | 135,592 (69.6%) | 51,698 (71.7%) | 18,144 (69.5%) | 16,696 (71.5%) | 10,308 (71.7%) | 87 (54.7%) |
| Marital status | Single (never married) | 36,703 (11.1%) | 22,527 (11.6%) | 7,799 (10.8%) | 2,727 (10.5%) | 2,361 (10.1%) | <5 | <5 |
| Marital status | Divorced | 22,023 (6.7%) | 12,267 (6.3%) | 4,912 (6.8%) | 1,931 (7.4%) | 1,772 (7.6%) | 1,129 (7.8%) | 12 (7.5%) |
| Marital status | Separated | 2,630 (0.8%) | 1,656 (0.9%) | 530 (0.7%) | 200 (0.8%) | <5 | <5 | <5 |
| Marital status | Widowed | 9,905 (3.0%) | 5,319 (2.7%) | 2,244 (3.1%) | 926 (3.5%) | 866 (3.7%) | 543 (3.8%) | 7 (4.4%) |
| Marital status | Unmarried or Domestic Partner | 1,369 (0.4%) | 820 (0.4%) | 329 (0.5%) | 91 (0.3%) | <5 | <5 | 0 (0.0%) |
| Marital status | Unknown | 25,672 (7.8%) | 16,500 (8.5%) | 4,638 (6.4%) | 2,073 (7.9%) | 1,437 (6.2%) | 978 (6.8%) | 46 (28.9%) |
| County median household income (quartile of 16 bands) | Q1 (lowest) | 26,436 (8.0%) | 2,200 (1.1%) | 3,596 (5.0%) | 5,276 (20.2%) | 8,804 (37.7%) | 6,560 (45.6%) | 0 (0.0%) |
| County median household income (quartile of 16 bands) | Q2 | 79,804 (24.1%) | 24,179 (12.4%) | 23,461 (32.5%) | 15,247 (58.4%) | 10,533 (45.1%) | 6,384 (44.4%) | 0 (0.0%) |
| County median household income (quartile of 16 bands) | Q3 | 116,211 (35.1%) | 83,131 (42.7%) | 24,466 (33.9%) | 4,703 (18.0%) | 2,571 (11.0%) | 1,276 (8.9%) | 64 (40.3%) |
| County median household income (quartile of 16 bands) | Q4 (highest) | 108,348 (32.8%) | 85,171 (43.7%) | 20,627 (28.6%) | 866 (3.3%) | 1,452 (6.2%) | 165 (1.1%) | 67 (42.1%) |
| County median household income (quartile of 16 bands) | Unknown | 28 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 28 (17.6%) |
| Risk group | low | 57,495 (17.4%) | 34,262 (17.6%) | 11,928 (16.5%) | 4,779 (18.3%) | 3,991 (17.1%) | 2,512 (17.5%) | 23 (14.5%) |
| Risk group | intermediate | 127,622 (38.6%) | 75,192 (38.6%) | 28,135 (39.0%) | 10,065 (38.6%) | 8,834 (37.8%) | 5,356 (37.2%) | 40 (25.2%) |
| Risk group | high | 130,893 (39.6%) | 75,764 (38.9%) | 29,317 (40.6%) | 10,127 (38.8%) | 9,586 (41.0%) | 6,011 (41.8%) | 88 (55.3%) |
| Risk group | unknown | 14,817 (4.5%) | 9,463 (4.9%) | 2,770 (3.8%) | 1,121 (4.3%) | 949 (4.1%) | 506 (3.5%) | 8 (5.0%) |
| Summary stage | Localised | 256,475 (77.5%) | 151,179 (77.7%) | 55,346 (76.7%) | 20,532 (78.7%) | 18,088 (77.4%) | 11,209 (77.9%) | 121 (76.1%) |
| Summary stage | Regional, direct extension | 61,984 (18.7%) | 35,854 (18.4%) | 14,124 (19.6%) | 4,757 (18.2%) | 4,513 (19.3%) | 2,707 (18.8%) | 29 (18.2%) |
| Summary stage | Regional, lymph nodes | 12,368 (3.7%) | 7,648 (3.9%) | 2,680 (3.7%) | 803 (3.1%) | 759 (3.2%) | 469 (3.3%) | 9 (5.7%) |
| Clinical Gleason score | 6 or less | 81,630 (24.7%) | 48,408 (24.9%) | 16,883 (23.4%) | 6,819 (26.1%) | 5,789 (24.8%) | 3,684 (25.6%) | 47 (29.6%) |
| Clinical Gleason score | 7 | 171,345 (51.8%) | 101,245 (52.0%) | 37,799 (52.4%) | 13,217 (50.7%) | 11,897 (50.9%) | 7,121 (49.5%) | 66 (41.5%) |
| Clinical Gleason score | 8 to 10 | 73,447 (22.2%) | 42,202 (21.7%) | 16,666 (23.1%) | 5,755 (22.1%) | 5,368 (23.0%) | <5 | <5 |
| Clinical Gleason score | Unknown | 4,405 (1.3%) | 2,826 (1.5%) | 802 (1.1%) | 301 (1.2%) | 306 (1.3%) | <5 | <5 |
| PSA (ng/ml) | below 10 | 223,700 (67.6%) | 132,150 (67.9%) | 49,185 (68.2%) | 17,686 (67.8%) | 15,427 (66.0%) | 9,198 (63.9%) | 54 (34.0%) |
| PSA (ng/ml) | 10 to 20 | 58,930 (17.8%) | 33,727 (17.3%) | 13,098 (18.2%) | 4,619 (17.7%) | 4,437 (19.0%) | 3,005 (20.9%) | 44 (27.7%) |
| PSA (ng/ml) | above 20 | 28,789 (8.7%) | 16,581 (8.5%) | 6,163 (8.5%) | 2,290 (8.8%) | 2,162 (9.3%) | 1,545 (10.7%) | 48 (30.2%) |
| PSA (ng/ml) | Unknown | 19,408 (5.9%) | 12,223 (6.3%) | 3,704 (5.1%) | 1,497 (5.7%) | 1,334 (5.7%) | 637 (4.4%) | 13 (8.2%) |
| First-course treatment | Radical prostatectomy | 159,580 (48.2%) | 94,117 (48.3%) | 35,254 (48.9%) | 12,782 (49.0%) | 10,677 (45.7%) | 6,675 (46.4%) | 75 (47.2%) |
| First-course treatment | Radiotherapy | 158,473 (47.9%) | 93,163 (47.9%) | 33,841 (46.9%) | 12,308 (47.2%) | 11,873 (50.8%) | 7,210 (50.1%) | 78 (49.1%) |
| First-course treatment | Both | 12,774 (3.9%) | 7,401 (3.8%) | 3,055 (4.2%) | 1,002 (3.8%) | 810 (3.5%) | 500 (3.5%) | 6 (3.8%) |
| Days to first recorded treatment | median (IQR) | 77.0 (52.0 to 116.0) | 81.0 (55.0 to 121.0) | 76.0 (50.0 to 112.0) | 71.0 (48.0 to 106.0) | 70.0 (46.0 to 105.0) | 68.0 (43.0 to 103.0) | 64.0 (40.0 to 103.5) |
| Waited more than 90 days | 90 days or less | 199,501 (60.3%) | 111,852 (57.5%) | 45,016 (62.4%) | 17,160 (65.8%) | 15,610 (66.8%) | 9,757 (67.8%) | 106 (66.7%) |
| Waited more than 90 days | over 90 days | 131,326 (39.7%) | 82,829 (42.5%) | 27,134 (37.6%) | 8,932 (34.2%) | 7,750 (33.2%) | 4,628 (32.2%) | 53 (33.3%) |

### Table 2. Out-of-fold skill added at each step, by risk group and model
Skill is the percentage reduction in out-of-fold log-loss against the step 0 model (higher is better). Added values are percentage points with 95% cluster bootstrap intervals.

| stratum | model | men | skill at step 2 | clinical need added | social position added | social position as % of step 2 skill | treatment type added |
|---|---|---|---|---|---|---|---|
| all men (pooled) | penalised logistic regression | 330,827 | 3.63 | 3.01 (2.69 to 3.38) | 0.62 (0.39 to 0.87) | 17 | 0.04 (0.03 to 0.06) |
| all men (pooled) | LightGBM | 330,827 | 4.17 | 3.18 (2.85 to 3.54) | 0.99 (0.73 to 1.30) | 24 | 0.29 (0.25 to 0.32) |
| low risk | penalised logistic regression | 57,495 | 0.76 | 0.14 (0.08 to 0.20) | 0.62 (0.32 to 0.94) | 82 | 0.21 (0.11 to 0.32) |
| low risk | LightGBM | 57,495 | 0.99 | 0.02 (-0.09 to 0.13) | 0.96 (0.67 to 1.28) | 98 | 0.36 (0.27 to 0.47) |
| intermediate risk | penalised logistic regression | 127,622 | 1.06 | 0.49 (0.41 to 0.56) | 0.56 (0.35 to 0.83) | 53 | 0.04 (0.01 to 0.07) |
| intermediate risk | LightGBM | 127,622 | 1.48 | 0.55 (0.44 to 0.65) | 0.93 (0.65 to 1.27) | 63 | 0.18 (0.14 to 0.23) |
| high risk | penalised logistic regression | 130,893 | 4.39 | 3.53 (3.16 to 3.86) | 0.86 (0.60 to 1.15) | 20 | 0.24 (0.15 to 0.34) |
| high risk | LightGBM | 130,893 | 4.90 | 3.72 (3.34 to 4.06) | 1.18 (0.90 to 1.56) | 24 | 0.38 (0.30 to 0.47) |
| unknown risk | penalised logistic regression | 14,817 | 1.07 | 0.65 (0.41 to 0.89) | 0.42 (0.08 to 0.80) | 39 | 0.34 (0.06 to 0.61) |
| unknown risk | LightGBM | 14,817 | 1.96 | 0.59 (0.27 to 0.95) | 1.37 (0.80 to 2.19) | 70 | 0.71 (0.45 to 0.97) |

### Table 3. Standardised differences in the percentage waiting more than 90 days
Percentage points. A contrast is described as meaningful only when both model types agree on 3 points or more in the same direction.

| stratum | contrast | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|---|
| all men (pooled) | all social features as observed minus reference profile | -1.1 | -1.6 | both models under 3 points |
| all men (pooled) | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -9.2 | -8.8 | both models 3 points or more, same direction |
| all men (pooled) | marital status: Single (never married) minus Married (including common law) | 6.7 | 5.9 | both models 3 points or more, same direction |
| low risk | all social features as observed minus reference profile | -3.4 | -4.7 | both models 3 points or more, same direction |
| low risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -11.3 | -13.5 | both models 3 points or more, same direction |
| low risk | marital status: Single (never married) minus Married (including common law) | 3.6 | 2.4 | models disagree |
| intermediate risk | all social features as observed minus reference profile | -1.4 | -1.6 | both models under 3 points |
| intermediate risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -8.7 | -9.5 | both models 3 points or more, same direction |
| intermediate risk | marital status: Single (never married) minus Married (including common law) | 6.4 | 5.5 | both models 3 points or more, same direction |
| high risk | all social features as observed minus reference profile | 0.1 | -0.1 | both models under 3 points |
| high risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -8.4 | -7.2 | both models 3 points or more, same direction |
| high risk | marital status: Single (never married) minus Married (including common law) | 8.3 | 7.6 | both models 3 points or more, same direction |
| unknown risk | all social features as observed minus reference profile | -0.1 | 0.0 | both models under 3 points |
| unknown risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -12.1 | -14.2 | both models 3 points or more, same direction |
| unknown risk | marital status: Single (never married) minus Married (including common law) | 6.0 | 6.2 | both models 3 points or more, same direction |

## Figures

![Figure 1](figures/figure1_flow.png)

**Figure 1. Inclusion flow for the primary cohort.** Boxes give the number of records remaining after each step, in protocol order; side boxes give the number excluded at that step.

![Figure 2](figures/figure2_delay_by_risk_and_rurality.png)

**Figure 2. Crude percentage of men waiting more than 90 days** from diagnosis to first recorded treatment, by risk group and county rurality. Lower is better. Men with unknown rurality, and percentages resting on 1 to 4 men, are not shown.

![Figure 3](figures/figure3_skill_added.png)

**Figure 3. Out-of-fold log-loss skill added by each block of features,** in percentage points, by risk group and model type, with 95% cluster bootstrap intervals (500 resamples). The dashed line marks no added skill.

![Figure 4](figures/figure4_area_and_income.png)

**Figure 4. (a)** Standardised percentage of all men waiting more than 90 days, with rurality and county income set together to each type of area at the median income band of men living there. Each man keeps his own clinical features and year, and marital status is set to married. **(b)** Concentration curves of waiting more than 90 days by county income rank, by risk group. A curve below the line of equality means delay is concentrated among men in higher-income counties.

## References

1. Cancer Australia, Cancer Council. Optimal care pathway for men with prostate cancer, second edition: quick reference guide. June 2021. https://www.cancer.org.au/assets/pdf/ocp/prostate-cancer-quick-reference-guide
2. Foley GR, Blizzard CL, Stokes B, et al. Urban-rural prostate cancer disparities in a regional state of Australia. Sci Rep. 2022;12(1):3022. doi:10.1038/s41598-022-06958-2
3. Foley GR, Blizzard CL, Skala M, et al. Prostate cancer disparities between public and private healthcare patients in Tasmania, a regional state of Australia. Cancers (Basel). 2025;18(1):79. doi:10.3390/cancers18010079
4. Leong CL, Cox I, Grundy R, et al. Optimal lung cancer care pathways: a Tasmanian perspective. Aust Health Rev. 2025;49:AH24249. doi:10.1071/AH24249
5. Usman SK, van Dam P, de Graaff B, et al. Bridging the divide: GP narratives on lung cancer care in Tasmania. Aust J Prim Health. 2026;32(4):PY26059. doi:10.1071/PY26059
6. Abdel-Rahman O, Ghosh S. Disparities in time to treatment initiation among patients with major types of cancer in the United States. J Racial Ethn Health Disparities. 2026. doi:10.1007/s40615-026-02847-w
7. Di Vanna M, Shambhavi S, Khikmatov M, et al. Time to treatment initiation of lung, breast, colorectal, and prostate cancers and contributing factors from 2015 to 2020 utilizing Surveillance, Epidemiology, and End Results Program database. World J Oncol. 2025;16(2):152-160. doi:10.14740/wjon2519
8. Montiel Ishino FA, Odame EA, Villalobos K, et al. Sociodemographic and geographic disparities of prostate cancer treatment delay in Tennessee: a population-based study. Am J Mens Health. 2021;15(6):15579883211057990. doi:10.1177/15579883211057990
9. Cone EB, Marchese M, Paciotti M, et al. Assessment of time-to-treatment initiation and survival in a cohort of patients with common cancers. JAMA Netw Open. 2020;3(12):e2030072. doi:10.1001/jamanetworkopen.2020.30072
10. Ang SP, Lee E, Chia JE, et al. Time-to-treatment initiation and its effect on all-cause mortality: insights from the Surveillance, Epidemiology, and End Results database. World J Oncol. 2025;16(3):286-294. doi:10.14740/wjon2584
11. Tagai EK, Handorf EA, Sorice KA, et al. Does inclusion of neighborhood variables improve clinical risk prediction for advanced prostate cancer in Black and White men? Urol Oncol. 2025;43(5):334.e17-334.e24. doi:10.1016/j.urolonc.2025.02.021
12. Ke G, Meng Q, Finley T, Wang T, et al. LightGBM: a highly efficient gradient boosting decision tree. Advances in Neural Information Processing Systems 30 (NIPS 2017). 2017.
13. Surveillance, Epidemiology, and End Results (SEER) Program. SEER\*Stat Database: Incidence - SEER Research Data, 17 Registries, Nov 2025 Sub (2000-2023) - Linked To County Attributes - Time Dependent (1990-2024) Income/Rurality, 1969-2024 Counties. National Cancer Institute, DCCPS, Surveillance Research Program, released April 2026, based on the November 2025 submission.
14. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet. 2007;370:1453-1457. doi:10.1016/S0140-6736(07)61602-X
15. Benchimol EI, Smeeth L, Guttmann A, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement. PLoS Med. 2015;12(10):e1001885. doi:10.1371/journal.pmed.1001885
16. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. doi:10.1136/bmj-2023-078378
17. National Cancer Institute. SEER Program Coding and Staging Manual 2021 and 2023, Appendix C: Surgery Codes, Prostate. https://seer.cancer.gov/manuals/2023/AppendixC/Surgery_Codes_Prostate_2023.pdf
18. Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: machine learning in Python. J Mach Learn Res. 2011;12:2825-2830.
19. Erreygers G. Correcting the concentration index. J Health Econ. 2009;28(2):504-515. doi:10.1016/j.jhealeco.2008.02.003
20. Noone AM, Lund JL, Mariotto A, et al. Comparison of SEER treatment data with Medicare claims. Med Care. 2016;54(9):e55-e64. doi:10.1097/MLR.0000000000000073
21. Dirican CD, Jumean S, Al Mardini A, et al. Rural-urban variation in guideline-concordant management of early-stage kidney, prostate, and testicular cancer in the United States (2010-2022). Urol Oncol. 2026;44(6):189-196. doi:10.1016/j.urolonc.2026.111088
22. Huang D, Ruan X, Huang J, et al. Socioeconomic determinants are associated with the utilization and outcomes of active surveillance or watchful waiting in favorable-risk prostate cancer. Cancer Med. 2023;12(8):9868-9878. doi:10.1002/cam4.5650
23. Zheng Q, Otahal P, Cox IA, et al. The influence of immortal time bias in observational studies examining associations of antifibrotic therapy with survival in idiopathic pulmonary fibrosis: a simulation study. Front Med (Lausanne). 2023;10:1157706. doi:10.3389/fmed.2023.1157706
24. Hammarlund N, Holt SK, Basu A, et al. Isolating the drivers of racial inequities in prostate cancer treatment. Cancer Epidemiol Biomarkers Prev. 2024;33(3):435-441. doi:10.1158/1055-9965.EPI-23-0892
