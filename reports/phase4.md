# Phase 4. Results overview

Written 2026-09-13 from three generated reports. Every number below is copied from them, and each section names its source:

- `reports/phase4_descriptive.md` (A1)
- `reports/phase4_models.md` (A2 to A4)
- `reports/phase4_equity_selection.md` (A5 to A7)

Definitions are in `PROTOCOL.md` version 1.7. All results are associations in observational registry data. None is a causal effect.

## Cohort and outcome

- **Cohort:** 330,827 men diagnosed 2010 to 2022 with localised or regional prostate cancer, whose first course of treatment included radical prostatectomy or radiotherapy, with a recorded interval above 0 days.
- **Outcome:** first recorded treatment more than 90 days after diagnosis, the Australian optimal care pathway benchmark (a lower percentage is better).

## 1. Descriptive results (A1, crude)

- **Overall:** 39.7% of men waited more than 90 days. The median wait was 77 days and the 90th percentile 174 days.
- **By risk group:** delay was more common in low-risk men (47.9%) than in high-risk men (32.8%). Intermediate-risk men were at 42.8% and unknown-risk men at 42.1%.
- **By year:** the percentage over 90 days rose from 36.0% in 2010 to 52.3% in 2022. It dipped to 33.5% in 2013, and 2020 (41.3%) was lower than 2019 (43.5%).
- **By rurality:** within every risk group, men in large metropolitan counties (1 million or more) waited more than 90 days more often than men in non-metropolitan counties not adjacent to a metro area. The gap was 50.7% against 39.0% in low risk and 35.7% against 26.0% in high risk.
- **By county income:** within every risk group, men in the lowest county income quartile waited more than 90 days less often than men in the highest quartile. In high risk it was 26.7% against 33.4%.
- **By marital status:** within every risk group, never-married men waited more than 90 days more often than married men. In high risk it was 40.0% against 30.9%.

## 2. Primary estimand: what social position adds to predicting delay (A2 to A4)

### Predictability is low
- **AUC at step 2** (clinical need plus social position) ranged from 0.592 to 0.663 across strata and models, where 0.5 is chance.
- **Log-loss skill** over year of diagnosis alone ranged from 0.76% to 4.90%.
- **What this means:** most of the variation in who waits more than 90 days is not explained by the recorded variables.

### Social position adds a small, non-zero amount in every stratum
The table shows skill added in percentage points of log-loss reduction, with 95% cluster bootstrap intervals (500 resamples over 79 rurality by county income cells). Higher means social position predicts more of the delay.

| stratum | penalised logistic regression | LightGBM |
|---|---|---|
| all men (pooled) | 0.62 (0.39 to 0.87) | 0.99 (0.73 to 1.30) |
| low risk | 0.62 (0.32 to 0.94) | 0.96 (0.67 to 1.28) |
| intermediate risk | 0.56 (0.35 to 0.83) | 0.93 (0.65 to 1.27) |
| high risk | 0.86 (0.60 to 1.15) | 1.18 (0.90 to 1.56) |
| unknown risk | 0.42 (0.08 to 0.80) | 1.37 (0.80 to 2.19) |

- **Every interval lies above 0.**
- **Low-risk men:** clinical need added little. It added 0.14 points under logistic regression and 0.02 (-0.09 to 0.13) under LightGBM, so social position made up 82% and 98% of step 2 skill.
- **High-risk men:** clinical need added more (3.53 and 3.72 points), and social position made up 20% and 24% of step 2 skill.
- **Treatment type** (step 3), added after social position, contributed a further 0.04 to 0.71 points.

### Gradient boosting against penalised regression
- **Skill:** LightGBM had higher out-of-fold log-loss skill than penalised logistic regression at step 2 in every stratum. The difference ranged from 0.23 points (low risk) to 0.90 points (unknown risk).
- **Caveats:**
  - No interval was computed for this difference.
  - Logistic regression chose the smallest C in the pre-specified grid (0.01, the strongest penalty) in all 5 strata, so a better logistic model may lie outside the grid. This is a limitation and was not changed after seeing results.
- **Calibration slopes at step 2** (1 is ideal):
  - logistic regression: 0.98 to 1.00;
  - LightGBM: 0.88 to 1.03, where values below 1 mean predictions are more extreme than observed.

### Which social variable (A4)
- **Marital status and rurality:** removing either one lost 0.22 to 0.45 points of skill in the pooled, intermediate and high-risk strata under both models.
- **County income:**
  - under logistic regression, removing it lost 0.00 to 0.02 points in those strata;
  - under LightGBM, it lost 0.26 to 0.29.
- **Why these disagree:** rurality and county income are strongly correlated, so removing one lets the other partly stand in for it. The two models disagree on how much income carries on its own.

## 3. Size in patient terms (A5)

### Standardised percentage delayed
- **Method:** g-computation. Each man keeps his own clinical features while his social features are set to a profile.
- **Rule for a meaningful difference:** both model types must agree on 3 percentage points or more in the same direction (amendment 1.7).

**Area**
- Across all men, non-metropolitan counties not adjacent to a metro area had a standardised delay 9.2 points lower than large metropolitan counties under logistic regression, and 8.8 points lower under LightGBM. Each area was evaluated at its own typical county income, so this is an area contrast, not a rurality effect separate from income.
- Both models agreed on a difference of 3 points or more in the same direction in every risk group, from -7.2 to -14.2 points.

**Marital status**
- Never-married men had a standardised delay 6.7 and 5.9 points higher than married men.
- The models agreed in every stratum except low risk (3.6 and 2.4 points).

**All social features as observed against the reference profile** (married, large metro, top income tertile)
- Pooled, the difference was -1.1 and -1.6 points, which is under 3 points.
- Only low-risk men passed the 3-point rule, at -3.4 and -4.7 points.

### Excess waiting days (crude, amendment 1.6)
- Days beyond 90, per 1,000 men, were 30,597 in large metropolitan counties against 20,014 in non-metropolitan counties not adjacent to a metro area. Fewer days is better.
- These figures are not adjusted for risk group or anything else.

## 4. Income inequality in delay (A6)

The Erreygers concentration index ranks men by county median household income. A positive value means delay is concentrated in higher-income counties.

| stratum | index (95% interval) |
|---|---|
| all men (pooled) | 0.062 (0.039 to 0.083) |
| low risk | 0.103 (0.068 to 0.134) |
| intermediate risk | 0.075 (0.051 to 0.096) |
| high risk | 0.041 (0.017 to 0.065) |
| unknown risk | 0.077 (0.037 to 0.128) |

- **Direction:** all intervals lie above 0, so in this cohort delay over 90 days was concentrated among men in higher-income counties.
- **Rurality:** higher-income counties are mostly metropolitan, and this index does not separate income from rurality.

## 5. Men without a recorded interval (A7)

- **How many:** 2.7% to 5.5% of treated men had no recorded interval, depending on rurality, and 14.4% in the unknown-risk group.
- **Worst-case bounds:** counting every missing man as delayed, and then as not delayed, did not remove the gaps below. The rurality, county income and marital status orderings seen in recorded men hold even under these extreme assumptions.
  - Large metro 40.2% to 45.7%, against non-metro not adjacent 31.3% to 34.0%.
  - Lowest income quartile 31.0% to 33.1%, against highest 39.6% to 44.1%.
  - Married 36.3% to 41.0%, against never married 43.5% to 48.4%.
- **Missingness is socially patterned:** social position added 0.53 points (0.07 to 1.02) of skill in predicting a missing interval, beyond clinical need (4.99 points).
- **Weighting:** inverse probability weighting changed every group percentage by 0.2 points or less.

## What these results do and do not show

- **They show:**
  - in US SEER men treated with surgery or radiotherapy, marital status and area characteristics predict waiting more than 90 days beyond clinical need and year;
  - the added predictive value is small in absolute terms, and prediction overall is weak;
  - delay was more common in large metropolitan, higher-income counties and among unmarried men.
- **They do not show why.** This dataset has no referral, biopsy or multidisciplinary meeting dates, no insurance, no comorbidity and no race.
- **Unmeasured factors:** part of the social increment may reflect them, including differences between registries, which the cluster bootstrap describes only as unmeasured area effects.
- **Comparison with Tasmania:** the SEER direction for rurality is opposite to the longer waits reported for outer regional and remote Tasmanian men (Foley et al. 2022). The area definitions, health systems and interval definitions differ, so the two cannot be compared directly.

## Not yet done

- **A8 sensitivity analyses:**
  - thresholds of 60, 120 and 180 days;
  - Gleason and PSA-only risk groups;
  - surgery only;
  - excluding 2020;
  - including 2023;
  - including 0-day intervals;
  - strict first primary;
  - excluding prostatectomy not otherwise specified.
- **A9:** treatment receipt (Q2).
- **Figures.**
- **Optional:** a logistic regression refit with a wider C grid, reported as a sensitivity analysis because the choice was at the grid edge.
