# Protocol

**Waiting for prostate cancer treatment: how much is clinical need? A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022**

Version 1.3, dated 2026-09-13 (see the amendment log). Written before any outcome modelling. Every constant below lives in `config/analysis.yaml`; this document states the rationale. Nothing later deviates from it without an entry in the amendment log at the end.

## 1. Background and aim

Timely treatment is a core measure of cancer care quality. The Australian optimal care pathway (OCP) for prostate cancer sets the benchmark that surgery or radiation therapy should begin within 3 months of diagnosis, or within 4 weeks when local symptoms are pronounced (Cancer Australia and Cancer Council, second edition, June 2021). In Tasmania, men from outer regional and remote areas took longer to start active treatment (Foley et al., Sci Rep 2022), and public-hospital patients started 40 to 59 days later than private patients in most risk groups (Foley et al., Cancers 2025).

In Tasmanian lung cancer care, a hospital-based study benchmarked referral, diagnosis and treatment intervals against national quality indicators and the OCP, and on average 7% of patients (range 0 to 16%) met the treatment-time standards (Leong et al., Aust Health Rev 2025). Interviews with Tasmanian general practitioners described fragmented referral systems and limited rural specialist access as barriers to timely lung cancer care (Usman et al., Aust J Prim Health 2026). These studies concern lung cancer. They are cited as context for assessing timeliness against OCP benchmarks, not for comparison with this study's results.

In the US, SEER studies report adjusted associations between single social factors and time to treatment, but none measures how much of the variation in waiting is predictable from clinical need, and how much is added by social position (reports/phase1.md).

The aim is to measure that added contribution within clinical risk groups, express it in patient terms, and set out what an Australian registry such as PCOR-TAS could add.

## 2. Data

Surveillance, Epidemiology, and End Results (SEER) Program, SEER*Stat Database: Incidence - SEER Research Data, 17 Registries, Nov 2025 Sub (2000-2023) - Linked To County Attributes - Time Dependent (1990-2024) Income/Rurality, 1969-2024 Counties, National Cancer Institute, DCCPS, Surveillance Research Program, released April 2026, based on the November 2025 submission.

Selection actually applied in SEER*Stat, taken from the saved session file `kkkkk.slm`: Site recode ICD-O-3/WHO 2008 = Prostate AND Year of diagnosis = 2010 to 2023. No age restriction was applied at export; the "Age at diagnosis = 18 and over" line in `shared.txt` does not describe this export. The file is a case listing of 793,214 tumour records and 41 variables (reports/phase0.md).

Not available in this export: race and ethnicity (the exported grouping collapsed to one value), Type of Reporting Source, histology, insurance, registry, comorbidity and month of diagnosis.

## 3. Cohort

Exclusions are applied in this order, and every step is counted in the flow diagram.

| step | rule | rationale |
|---|---|---|
| 1 | First primary: `One primary only` or `1st of 2 or more primaries` | A prior cancer changes care pathways and competing risks |
| 2 | Combined Summary Stage localised or regional | Timeliness benchmarks for curative treatment apply to non-metastatic disease; unknown stage cannot be risk-grouped |
| 3 | Exclude death-certificate-only and autopsy-only cases (Survival months flag) | No treatment pathway exists; Type of Reporting Source is unavailable, so this flag is the proxy |
| 4 | Age 40 or over | Younger age bands hold 331 records and include implausible childhood ages |
| 5 | Diagnosed 2010 to 2022 | Follow-up is truncated for 2023 diagnoses (six top-coded intervals versus 149 in 2018), and 2023 uses new surgery codes |
| 6 | First course of treatment includes radical prostatectomy or radiotherapy | The question concerns time to curative treatment |
| 7 | Interval recorded, or top-coded `731+ days` | `Unable to calculate` has no interval; this group is described separately (section 8) |
| 8 | Interval above 0 days | A 0-day interval usually marks a cancer found at a procedure rather than a planned treatment start |

## 4. Definitions

**Radical prostatectomy.** Surgery of primary site codes 50, 70 or 80 (1998 to 2022) or A500, A700 or A800 (2023), verified against the SEER Program Coding and Staging Manual Appendix C, 2021 and 2023 editions. Code 80/A800 is prostatectomy not otherwise specified and is removed in a sensitivity analysis. Codes 10 to 30 and A100 to A300 (local destruction, TURP, simple prostatectomy) and 90/A900 (surgery not otherwise specified) are not counted.

**Radiotherapy.** Radiation recode `Beam radiation`, `Radioactive implants (includes brachytherapy) (1988+)`, `Combination of beam with implants or isotopes`, `Radioisotopes (1988+)` or `Radiation, NOS  method or source not specified`. Not counted: `None/Unknown`, `Recommended, unknown if administered`, `Refused (1988+)`.

**Modality.** Surgery only, radiotherapy only, or both.

**First course.** SEER treatment fields record the first course only. If the first course was active surveillance, the surgery and radiation fields are coded none, so men in this cohort chose, or were offered, curative treatment as their first course. Long waits among treated low-risk men are therefore not active surveillance; they may reflect deliberate deferral, patient choice or access.

**Outcome.** Time to first recorded treatment: SEER's "Time from diagnosis to treatment in days recode". It measures days from diagnosis to the first treatment of any kind, which can include hormone therapy (not in this export). It is therefore a lower bound on time to surgery or radiotherapy for men who started hormone therapy first.
- Primary outcome: delayed, defined as more than 90 days, following the OCP three-month benchmark. `731+ days` counts as delayed.
- Sensitivity thresholds: 60, 120 and 180 days.
- The median and 90th percentile are reported descriptively only.

**Risk group.** NCCN-style groups built from clinical information only. Pathological grade is observed only after prostatectomy, and using it would condition on the treatment being studied.
- High: regional stage (direct extension or nodes), or clinical Gleason score 8 to 10, or PSA above 20 ng/ml.
- Otherwise unknown: clinical Gleason score or PSA missing.
- Otherwise intermediate: Gleason score 7, or PSA 10 to 20 ng/ml.
- Otherwise low: Gleason score 6 or lower, and PSA below 10 ng/ml.

Summary stage cannot separate T1 from T2 disease, and for surgical patients it partly uses pathology. A sensitivity analysis therefore assigns risk groups from Gleason score and PSA alone.

## 5. Feature blocks and ordered steps

The blocks share no columns; this is enforced by tests.

| step | block added | contents |
|---|---|---|
| 0 | Base | Year of diagnosis; 2020 indicator |
| 1 | Clinical need | Stage category; clinical Gleason score with missing indicator; log PSA with top-code and missing indicators; age band midpoint |
| 2 | Social position | Marital status (7 categories including unknown); Rural-Urban Continuum Code (5 levels plus unknown); county median household income band (ordinal rank plus unknown indicator) |
| 3 | Pathway | Modality |

Year sits in the base model because secular change (guidelines, surveillance uptake, the 2020 pandemic) is neither clinical need nor social position. Modality enters after social position because social factors can influence the choice of surgery or radiotherapy. Adjusting for it first would remove part of the social contribution.

## 6. Primary estimand

Within each risk group, among men diagnosed 2010 to 2022 whose first course included radical prostatectomy or radiotherapy: the out-of-sample improvement in log-loss skill from step 1 to step 2 for predicting delay beyond 90 days. It is reported alongside the standardised difference in the percentage delayed between social profiles.

Log-loss skill is 1 minus the model's cross-fitted log-loss divided by the log-loss of the step 0 model (0 means no improvement over the base; higher is better).

A difference is pre-specified as meaningful when it reaches 3 percentage points in standardised percentage delayed or 7 days in standardised mean waiting time. Results are reported as estimates with 95% intervals; no p-values are used for decisions.

## 7. Models and validation

- Penalised logistic regression (L2, with clinical interaction terms) and LightGBM gradient boosting at each step.
- Five-fold cross-fitting within each risk group; hyperparameters tuned by inner cross-validation on a subsample.
- Metrics, all computed on out-of-fold predictions:
  - log-loss skill and Brier skill (higher is better; 0 is the base model);
  - AUC (0.5 is chance; higher is better);
  - calibration intercept (0 is ideal) and calibration slope (1 is ideal).
- Calibration is weighted more heavily than discrimination.
- If gradient boosting does not improve on penalised regression, this is stated in the abstract.

**Uncertainty.** Rurality and income are measured at county level, and the export has no county or registry identifier. Intervals therefore come from a cluster bootstrap over rurality by income cells (500 resamples of out-of-fold predictions, no refitting), not from resampling individual men. The social block is interpreted as geographic and social position, including any unmeasured registry differences.

## 8. Analyses

- **A1. Descriptive.**
  - Percentage within the 90-day benchmark, median and 90th percentile, by risk group and rurality, by income band and by year.
  - Table 1 by rurality.
- **A2 and A3. Primary analysis.** Ordered-step model performance with cluster-bootstrap intervals, for both model types.
- **A4. Which social variables.** Leave-one-variable-out refits within the social block (marital status, rurality, income).
- **A5. Size in patient terms.** Associational g-computation from the step 2 model.
  - Standardised percentage delayed under each observed social profile compared with a reference profile (county in a metropolitan area of 1 million or more, top income tertile, married).
  - Excess waiting person-days beyond 90 days per 1,000 men, by rurality and income.
  - A rurality by income grid of standardised percentage delayed.
- **A6. Equity.** Erreygers-corrected concentration index of delay by county income rank, with the concentration curve, per risk group. A negative index means delay concentrates among men in lower-income counties.
- **A7. Selection.** Among treated men, a model for having a recorded interval (step 1 against step 2).
  - Bounds on percentage delayed by social group, assigning every man with a missing interval as delayed and then as not delayed.
  - Inverse probability weighting as a sensitivity analysis.
  - All results are conditional on receiving curative treatment.
- **A8. Sensitivity analyses:**
  - thresholds of 60, 120 and 180 days;
  - risk groups from Gleason score and PSA only;
  - surgery only;
  - excluding 2020;
  - including 2023;
  - including 0-day intervals;
  - strict first primary;
  - excluding prostatectomy not otherwise specified.
- **A9. Secondary question.** Among intermediate- and high-risk men meeting cohort steps 1 to 5: receipt of radical prostatectomy or radiotherapy, using ordered steps 0 to 2 with penalised logistic regression and standardised percentage treated by rurality and income.
- **A10. Survival (methods box only, not run).** Comparing survival between treated and untreated men is exposed to immortal time bias, because treated men must survive until treatment starts. A simulation study of observational research (Zheng et al., Front Med 2023) found that time-fixed and exclusion methods overestimated a treatment's benefit, that a 1-year landmark method reduced but did not remove the bias, and recommended the time-dependent method.
  - **Preferred design:** treatment as a time-dependent exposure, with competing risks of prostate cancer death and other-cause death.
  - **Sensitivity analysis only:** a 12-month landmark analysis.
  - This design is described, not estimated, in this study.
- **A11. Australian context (no Australian data are analysed).** List candidate Australian equivalents of the SEER variables, to be confirmed against an Australian registry's data dictionary before any use:
  - Rural-Urban Continuum Code to Australian Statistical Geography Standard remoteness areas;
  - county income to an area-level socioeconomic index such as IRSD;
  - no insurance variable to public or private treating sector.

  Describe which additional data (for example referral, biopsy and multidisciplinary meeting dates, comorbidity and patient-reported outcomes) would strengthen the analysis, without assuming which of these any particular registry holds.

## 9. Limitations stated in advance

- **No race or ethnicity in this export,** so a known determinant of delay is omitted from the social block.
- **No insurance variable,** the closest US analogue of the public and private sector difference reported in Tasmania (Foley et al., Cancers 2025).
- **No registry or county identifier,** so regional clustering cannot be modelled directly, and practice differences between registries may load onto the social block.
- **No comorbidity data:** clinical need means recorded stage, grade, PSA and age, and part of what the social block adds may be unmeasured health.
- **No data on referral or care coordination:** qualitative work in Tasmanian lung cancer care describes these as barriers to timely care (Usman et al., Aust J Prim Health 2026), but a registry cannot observe them.
- **The interval ends at the first treatment of any kind,** including hormone therapy.
- **SEER under-captures treatment** given outside reporting facilities, especially radiotherapy.
- **Summary stage cannot separate T1 from T2** and partly uses pathology for surgical patients.
- **Surgery coding changes in 2023.**
- **US payment and access structures differ from Australia's.**
- **All findings are associations, not causal effects.**

## References

The data source is cited in full in section 2. Details for the journal articles below were taken from their PubMed records. Only the abstracts have been read so far; the full texts must be read before any detail is quoted in the paper.

1. Cancer Australia, Cancer Council. Optimal care pathway for men with prostate cancer, second edition: quick reference guide. June 2021. https://www.cancer.org.au/assets/pdf/ocp/prostate-cancer-quick-reference-guide
2. National Cancer Institute. SEER Program Coding and Staging Manual 2021 and 2023, Appendix C: Surgery Codes, Prostate. https://seer.cancer.gov/manuals/2023/AppendixC/Surgery_Codes_Prostate_2023.pdf
3. Foley GR, Blizzard CL, Stokes B, Skala M, Redwig F, Dickinson JL, et al. Urban-rural prostate cancer disparities in a regional state of Australia. Sci Rep. 2022;12(1):3022. doi:10.1038/s41598-022-06958-2. PMID 35194109.
4. Foley GR, Blizzard CL, Skala M, Redwig F, Roydhouse J, Dickinson JL, et al. Prostate cancer disparities between public and private healthcare patients in Tasmania, a regional state of Australia. Cancers (Basel). 2025;18(1):79. doi:10.3390/cancers18010079. PMID 41514591.
5. Leong CL, Cox I, Grundy R, Harkness N, Palmer AJ, de Graaff B, et al. Optimal lung cancer care pathways: a Tasmanian perspective. Aust Health Rev. 2025;49:AH24249. doi:10.1071/AH24249. PMID 39928915.
6. Usman SK, van Dam P, de Graaff B, Palmer AJ, Otahal P, Harkness N, et al. Bridging the divide: GP narratives on lung cancer care in Tasmania. Aust J Prim Health. 2026;32(4):PY26059. doi:10.1071/PY26059. PMID 42373555.
7. Zheng Q, Otahal P, Cox IA, de Graaff B, Campbell JA, Ahmad H, et al. The influence of immortal time bias in observational studies examining associations of antifibrotic therapy with survival in idiopathic pulmonary fibrosis: a simulation study. Front Med (Lausanne). 2023;10:1157706. doi:10.3389/fmed.2023.1157706. PMID 37113607.

The literature reviewed for novelty is listed with PubMed identifiers in reports/phase1.md.

## Amendment log

| date | amendment | reason |
|---|---|---|
| 2026-09-13 | Timeliness made the primary question; treatment receipt secondary; survival reduced to a methods box | Strongest data, closest match to the intended audience, and time available |
| 2026-09-13 | Analysis built on the current export without race, Type of Reporting Source or histology | Re-export not available before the application deadline; death-certificate proxy and stated limitations used instead |
| 2026-09-13 | Modality moved after social position; ordered steps replace order-invariant decomposition; binary outcome only; cohort limited to 2010 to 2022; 0-day intervals excluded; cluster bootstrap over rurality by income cells | Independent design review: modality partly carries social effects; every treated man has the event, so survival framing does not apply; follow-up truncation; county-level exposures |
| 2026-09-13 | Selection statement corrected: no age filter was applied at export | Session file inspection (reports/phase1.md) |
| 2026-09-13 | Title changed to name the machine learning approach (version 1.1) | Clarity about methods; no change to the cohort, definitions, estimand or analyses |
| 2026-09-13 | Wording clarified: no Australian data are analysed; Tasmanian findings are cited as background only; Australian registry variables are candidate equivalents to be confirmed (version 1.2) | Avoid implying a cross-country comparison or unverified registry contents; no change to the cohort, definitions, estimand or analyses |
| 2026-09-13 | Survival methods box (A10) now prefers a time-dependent treatment exposure, with the 12-month landmark as a sensitivity analysis only; citations added for Leong 2025, Usman 2026 and Zheng 2023; references section added (version 1.3) | Simulation evidence that landmark methods only partly remove immortal time bias (Zheng et al. 2023). A10 is not estimated, so no result changes |
