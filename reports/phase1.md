# Phase 1. Literature check

Study: Timeliness and Allocation of Treatment in Localised Prostate Cancer: A Machine Learning Decomposition of Clinical Need and Social Position. (This was the working title when Phase 1 ran; the current title is in PROTOCOL.md.)

Search run 2026-09-13. Question order follows the reframe: Q1 (primary) timeliness among men receiving definitive treatment; Q2 (secondary) receipt of definitive treatment; Q3 survival with competing risks.

## Answer in brief

- **Q1 has not been done.** No study found decomposes diagnosis-to-treatment time in prostate cancer into what clinical need predicts and what non-clinical factors add. SEER studies of this interval report adjusted odds ratios for single factors (race, marital status, income, metropolitan residence) across several cancers, without risk stratification and without separating active surveillance from delay.
- **Q2 is partly done.** Receipt of definitive treatment by marital status, race, rurality and income is well described in SEER. One study decomposes the Black-White gap in definitive treatment (Oaxaca, SEER-Medicare, men 66 and older). One machine learning study models treatment choice with socioeconomic and geographic inputs. Q2 should be framed as an extension that uses the same metric as Q1, not as a first description.
- **The closest design analogue is Ajjawi 2026.** It compares a clinical-only model with a clinical plus sociodemographic model, but its outcome is cancer-specific survival, and it uses time to treatment as a clinical input.
- **The direction of the rural effect on timeliness is contested.** In SEER, non-metropolitan and lower-income patients had shorter intervals across four cancers (Di Vanna 2025), while rural men are less likely to receive definitive treatment at all (Dirican 2026). Rural disadvantage may operate on whether men are treated more than on when. That is a testable hypothesis for this design, not a finding.

## Search methods

PubMed was searched through NCBI E-utilities with `scripts/run_phase1_search.py`. The queries, date limits (2000/01/01 to 2026/09/13) and pacing are in `config/literature.yaml`. Each query's exact term, PubMed's translation, hit count and run time are logged in `reports/phase1_search/search_log.json`, and all retrieved records are in `articles.json`. Four queries cover the requested topics, restricted to SEER. Three novelty checks are not restricted to SEER.

| query key | topic | hits (all retrieved) |
|---|---|---|
| timeliness_seer | Time to treatment and treatment delay in prostate cancer, SEER | 21 |
| marital_seer | Marital status and prostate cancer treatment, SEER | 131 |
| rural_seer | Rural and urban disparities in prostate cancer treatment, SEER | 32 |
| income_seer | County-level income and cancer treatment access, SEER, any cancer | 210 |
| timeliness_disparities_any_source | Novelty check: prostate timeliness and social factors, any data source | 71 |
| incremental_value_social_factors | Novelty check: added predictive value of social factors for prostate treatment or timing | 15 |
| ml_decomposition | Novelty check: machine learning or decomposition of prostate treatment disparities | 48 |

The seven queries returned 493 unique records. As a citation-chasing check, PubMed "similar articles" lists were pulled for the three closest matches (Ajjawi 2026, Hammarlund 2024, Semprini 2026), 25 records each (`similar_articles.json`). They surfaced no closer study. Title and abstract screening decisions for the 38 shortlisted records are in `screening.tsv`.

Limits of this check: PubMed only (no Embase, Scopus or grey literature). Screening was by title and abstract with one reviewer (Claude), without dual review. Full texts were not read, so every number below is quoted from the abstract. Conference abstracts are poorly indexed. This is a scoping check for novelty, not a systematic review.

## The ten most recent and relevant studies

Ordered by publication year, then relevance to Q1. For each number, the comparison group and the direction that favours patients are stated.

**1. Abdel-Rahman O et al. Disparities in time to treatment initiation among patients with major types of cancer in the United States. J Racial Ethn Health Disparities, 2026. PMID 41591736; doi 10.1007/s40615-026-02847-w.**
- SEER; lung, colorectal, breast and prostate cancer with a known diagnosis-to-treatment time.
- Mean time for prostate cancer was 82.75 days in 2021, the longest of the years studied (lower is better).
- Compared with White men, the odds of a longer time to treatment were 1.239 for Black men (95% CI 1.196 to 1.285) and 1.219 for Asian or Pacific Islander men (1.157 to 1.284); above 1 means more delay.
- Relevance to Q1: the same outcome in the same registry, but association only, pooled across risk groups, with active surveillance not separated.

**2. Semprini JT et al. Hospital accreditation and geographic disparities in timely cancer care. Health Serv Res, 2026. PMID 40476571; doi 10.1111/1475-6773.14655.**
- SEER 2018 to 2021; 2,107,188 treated patients, all cancers; quantile regression.
- Median time to treatment 27 days (IQR 1 to 52).
- Care at an accredited hospital added 2.6 days to the median in low-income counties (median household income under $80,000), with no association in high-income counties (fewer days is better).
- Relevance to Q1: the closest health services framing of county income and timeliness, and a distributional method worth borrowing. It is not prostate-specific, excludes untreated patients, and does not ask how much of the interval clinical need explains.

**3. Dirican CD et al. Rural-urban variation in guideline-concordant management of early-stage kidney, prostate, and testicular cancer in the United States (2010-2022). Urol Oncol, 2026. PMID 41925394; doi 10.1016/j.urolonc.2026.111088.** A companion conference abstract from the same group covers rural definitive therapy (JNCCN 2026, PMID 41990793).
- SEER 2010 to 2022; 439,435 men with non-metastatic prostate adenocarcinoma, classified as eligible or ineligible for active surveillance.
- Compared with urban men, the adjusted odds of guideline-concordant management were 0.82 in rural-adjacent counties (0.80 to 0.84) and 0.74 in rural-remote counties (0.71 to 0.76); below 1 means less concordant care.
- Among men ineligible for surveillance, definitive local therapy was 81.6% urban, 78.5% rural-adjacent and 76.8% rural-remote (higher is better).
- Relevance to Q2: substantial overlap in data, years and exposure. It handles surveillance through eligibility, which Q1 must also do. It does not measure the added contribution of rurality over clinical need, and does not examine timing.

**4. Pustake M et al. Clinical and sociodemographic determinants of treatment selection in prostate cancer: a population-based study in the United States (2004-2022). Cancers, 2026. PMID 42352495; doi 10.3390/cancers18121962.**
- SEER; 917,194 men with localised or regional disease; 33.5% had radical prostatectomy.
- Odds of prostatectomy were 1.601 for married versus unmarried men (1.554 to 1.649) and 0.547 for Black versus White men (0.539 to 0.555).
- Prostatectomy use alone is not a quality measure, since radiotherapy is an equivalent definitive option.
- Relevance to Q2: the same variables and near-identical years. Definitive treatment is defined as surgery only, and results are odds ratios rather than an explained share.

**5. Ajjawi I et al. Machine learning approaches to optimize the integration of sociodemographic factors for predicting cancer-specific survival among patients with high-risk prostate cancer. Curr Urol, 2026. PMID 41969320; doi 10.1097/CU9.0000000000000335.**
- SEER 2010 to 2020; 80,858 men with high-risk disease.
- A random forest on clinical variables had an AUC of 0.54, rising to 0.72 when race, income, marital status, region and urbanicity were added (0.5 is chance; higher is better). XGBoost gave similar results.
- A clinical-only AUC of 0.54 for cancer-specific survival is close to chance even though Gleason grade was reported as the strongest predictor. The abstract cannot resolve this, and it warrants caution before citing the size of the gain.
- Relevance: the closest design analogue (model A versus model B). Its outcome is survival, and it treats time to treatment as a clinical predictor, the opposite role from Q1.

**6. Di Vanna M et al. Time to treatment initiation of lung, breast, colorectal, and prostate cancers and contributing factors from 2015 to 2020 utilizing SEER. World J Oncol, 2025. PMID 40162107; doi 10.14740/wjon2519.**
- SEER 2015 to 2020; 991,772 patients across four cancers; late treatment defined as more than 1 month; propensity-matched competing-risks regression.
- Time to treatment was shorter for White and married patients, and also shorter for lower-income and non-metropolitan patients.
- Metropolitan residence and income above $35,000 carried a greater risk of delay beyond 1 month (fewer delayed patients is better).
- Relevance to Q1: the only SEER study found that tests marital status, income and geography against the interval. The rural and income results run against the rural-delay hypothesis. It is pooled across cancers, so the prostate-specific direction is not given in the abstract.

**7. Ang SP et al. Time-to-treatment initiation and its effect on all-cause mortality: insights from the SEER database. World J Oncol, 2025. PMID 40556964; doi 10.14740/wjon2584.**
- The same SEER 2015 to 2020 four-cancer cohort (991,771 patients); 63.9% started treatment within 1 month.
- Unadjusted mortality was lower with longer intervals: 26.1% at 0 to 1 month versus 11.4% at 10 months or more.
- After adjustment, intervals of 10 months or more carried a hazard ratio for all-cause mortality of 1.23 compared with 0 to 1 month (above 1 means higher mortality).
- Relevance to Q1 and Q3: the unadjusted reversal is confounding by indication, since aggressive disease is treated fast and indolent disease is watched. This is why Q1 must be stratified by risk group and must separate surveillance from delay.

**8. Hammarlund N et al. Isolating the drivers of racial inequities in prostate cancer treatment. Cancer Epidemiol Biomarkers Prev, 2024. PMID 38214587; doi 10.1158/1055-9965.EPI-23-0892.**
- SEER-Medicare; 40,137 men aged 66 and older, cT1-4N0M0, grade group 2 to 5, diagnosed 2010 to 2015; Kitagawa-Oaxaca-Blinder decomposition.
- Definitive treatment was 72.1% for Black men and 78.6% for White men, a gap of 6.5 percentage points (higher is better).
- Patient health, including comorbidity, explained 15% of the gap (95% CI 6 to 24); 85% (74 to 94) remained unexplained.
- Relevance to Q2: the closest decomposition of treatment receipt. It covers one non-clinical factor (race), older Medicare men only, and receipt rather than timing. Its comorbidity data are exactly what this SEER product lacks.

**9. Huang D et al. Socioeconomic determinants are associated with the utilization and outcomes of active surveillance or watchful waiting in favorable-risk prostate cancer. Cancer Med, 2023. PMID 36727535; doi 10.1002/cam4.5650.**
- SEER Prostate with Watchful Waiting database 2010 to 2016; 229,428 men with localised disease.
- Compared with married men, unmarried men had higher odds of surveillance or watchful waiting: 1.20 in low-risk disease (1.12 to 1.28) and 1.41 in favourable intermediate-risk disease (1.26 to 1.59).
- Urban men had lower odds than rural men in low-risk disease (0.77, 0.68 to 0.87).
- Relevance to Q1: marital status and rurality shift the surveillance share. The unable-to-calculate group and the long-interval tail in low-risk men will therefore differ by these same factors, which is why the excluded group needs its own description.

**10. Han JH et al. Explainable ML models for a deeper insight on treatment decision for localized prostate cancer. Sci Rep, 2023. PMID 37460568; doi 10.1038/s41598-023-38162-1.**
- SEER Prostate with Watchful Waiting database 2010 to 2015; 255,837 men; gradient-boosted models explained with SHAP.
- Multiclass AUC for surveillance, prostatectomy or radiotherapy was 0.77, and 0.74 for surveillance in low-risk men (0.5 is chance; higher is better).
- Prostatectomy decisions were driven mainly by oncological variables; radiotherapy decisions were strongly associated with geographic variables.
- Relevance to Q2: machine learning applied to allocation with social inputs. It does not compare a clinical-only model with an added model, so it cannot say how much the non-clinical inputs add, and it does not address timing.

## Other studies that shape the design

| study | data | key result (comparison, direction) | use in this study |
|---|---|---|---|
| Stokes 2013, Cancer, PMID 23716470 | SEER-Medicare 2004 to 2007 | Time to definitive treatment 7.6 days longer for African American men after adjustment; the gap was largest in high-risk disease (96 versus 105 days) | Precedent for stratifying the interval by risk group |
| Cone 2020, JAMA Netw Open, PMID 33315115 | NCDB 2004 to 2015 | Prostate median time to treatment 79 days (IQR 55 to 117); high-risk 5-year predicted mortality 12.8% at 61 to 120 days versus 14.1% at 181 to 365 days (lower is better) | External benchmark for our median of 66 days and for delay categories |
| Janopaul-Naylor 2023, Cancer Med, PMID 37537835 | NCDB 2010 to 2016, intermediate and high risk | 4.4% delayed beyond 180 days; Black versus White odds 1.79 (1.72 to 1.87) | Candidate delay threshold (180 days) |
| Montiel Ishino 2021, Am J Mens Health, PMID 34836465 | Tennessee registry 2005 to 2015 | Delay beyond 90 days: divorced or separated odds 1.15 (1.01 to 1.31); rural Appalachian residence odds 0.83 (0.78 to 0.89), meaning less delay | Candidate threshold (90 days); second finding of shorter rural intervals |
| Baade 2012, Cancer Causes Control, PMID 22382868 | Queensland cohort | Median treatment interval 65 days (IQR 36 to 107); men without private insurance more likely to wait beyond 70 days | Australian context (published figures, not compared statistically with this study) |
| Cary 2016, Prostate Cancer Prostatic Dis, PMID 26782713 | SEER 2005 to 2008 | 6% (4.3 to 9.0) of treatment variation at county level and 3% (1.2 to 6.2) at SEER region | Precedent for an explained-share metric; shows what registry clustering would add, which this product cannot examine |
| Tagai 2025, Urol Oncol, PMID 40121103 | Single US health system | Adding neighbourhood variables moved AUC from 0.671 to 0.673 | A small or null gain is a plausible, publishable result |
| Oake 2021, J Urol, PMID 34181467 | Manitoba, universal system | Highest versus lowest income quintile odds of prostatectomy rather than radiotherapy 2.30 (1.70 to 3.12) | Income gradients persist without insurance barriers; context for a universal health system |

## What the decomposition framing adds

Existing SEER work on prostate cancer timeliness asks whether a given social factor is associated with a longer interval, and answers with adjusted odds ratios pooled across cancers or across risk groups (Abdel-Rahman 2026, Di Vanna 2025). Work on allocation asks the same question of treatment receipt (Pustake 2026, Dirican 2026), and the one decomposition of receipt covers race only, in Medicare men aged 66 and older (Hammarlund 2024). None of these studies measures how much of the variation in time to definitive treatment is predictable from clinical need alone, or how much marital status, rurality, county income and race add beyond it. That is the quantity a health economist needs to judge whether delay is mainly clinical triage or mainly an access problem. It is also robust to the conflicting directions in the literature: if rural men wait less while urban or higher-income men wait more, the added-performance measure still captures the size of the non-clinical signal without presupposing its sign. Restricting to recorded surgery or radiotherapy and stratifying by risk group separates appropriate deferral in low-risk disease from access failure in high-risk disease. The existing SEER timeliness studies do not make this separation, and the confounding-by-indication reversal in Ang 2025 shows why it matters. Reporting the unable-to-calculate group as its own descriptive result then shows whether the men who drop out of the timeliness analysis differ on the same social factors, which Huang 2023 suggests they will.

## Does the study already exist

No. No study was found that decomposes prostate cancer diagnosis-to-treatment time into clinical and non-clinical contributions, in SEER or elsewhere. Q2 is closer to existing work and should not be presented as new. The narrowest framing that is still novel is:

> Within NCCN-style risk groups of men with localised prostate cancer who received surgery or radiotherapy (SEER, 2010 to 2023), the out-of-sample gain in predicting diagnosis-to-treatment time from adding marital status, rurality, county income and race to clinical need, with the unable-to-calculate group characterised separately.

This is the reframed Q1 as specified. Q2 then becomes an extension of Hammarlund 2024 and Dirican 2026: the same added-performance metric applied to receipt, covering all four non-clinical factors and all ages. Q3 stays secondary and descriptive of consequences. If the added gain in Q1 is small, that is the finding, and it would still be new, because no prior study has put a number on it.

## Carried into Phase 2

**Selection actually applied.** The saved SEER*Stat file `kkkkk.slm` contains the selection statement used for the export:

```
{Site and Morphology.Site recode ICD-O-3/WHO 2008} = '    Prostate'
AND {Race, Sex, Year Dx.Year of diagnosis} = '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023'
```

There is no age clause anywhere in the file, so the `Age at diagnosis = 18 and over` line in `shared.txt` was not applied to this export. That is consistent with the 24 rows aged under 15 found in Phase 0. The methods should state that selection was by site and year only, and that any age restriction is applied in code. This should be checked again against the new session file when it arrives.

**Why race collapsed.** The same file shows that the exported race column was a user-defined SEER*Stat variable. Its first group, `All races/ethnicities`, was defined as `Race and origin recode (NHW, NHB, NHAIAN, NHAPI, Hispanic) = 1-5,9`, which matches every case, so every case landed in that group. Exporting the base variable, as planned, avoids this.

**SEER registry.** The `.slm` lists `{main.SEER registry} = 1,2,21,22,23,25,26,27,29,31,35,37,41,42,43,44,47` as part of the database definition. The November 2025 data items list marks `SEER registry` and `SEER registry (with CA and GA as whole states)` as unavailable in case listings from the Research database; the second is marked available only in Research Plus. Unless the re-export uses a Research Plus database, registry will probably not be exportable, and its absence stays a stated limitation.

**Design inputs from the literature for the protocol:**
- **Delay thresholds used before:** more than 1 month (Di Vanna 2025), more than 90 days (Montiel Ishino 2021), more than 180 days or 6 months (Janopaul-Naylor 2023, Jain 2022, Luu 2024). The protocol should pre-specify one threshold, justified from guidance, and report the others as sensitivity analyses.
- **Direction of rural effects:** shorter intervals for non-metropolitan and rural residents in two studies, but lower receipt of definitive treatment for rural men. The protocol should not pre-specify a direction for rurality in Q1.
- **Confounding by indication:** Ang 2025 shows the unadjusted reversal between interval and mortality. Q1 is stratified by risk group, and Q3 must not read longer intervals as protective.
- **Comorbidity:** Hammarlund 2024 had comorbidity data and still left 85% of the race gap unexplained. Our clinical-need model lacks comorbidity, so part of what the non-clinical variables add may be unmeasured health. The protocol must state what result would point to confounding rather than an access effect.
