# Phase 4, part 5. Secondary question: recorded curative treatment

Generated 2026-09-13 12:54 UTC by `scripts/run_phase4_receipt_report.py` at git revision `52982e0`. Definitions: `PROTOCOL.md` A9 with amendment 1.8. All results are associations, not causal effects.

## What is measured

- **Men:** intermediate and high-risk men meeting every cohort step before treatment (first primary, localised or regional stage, not a death certificate or autopsy case, aged 40 or over, diagnosed 2010 to 2022).

- **Outcome:** a record of radical prostatectomy or radiotherapy in the first course of treatment.

- **What no record can mean:** active surveillance or watchful waiting, hormone therapy only, refusal, or treatment that was not captured. SEER under-captures treatment given outside reporting facilities, especially radiotherapy (`PROTOCOL.md` section 9). The data do not record why a man had no recorded curative treatment, so a lower percentage cannot be read as under-treatment, and a higher percentage is not necessarily better.

- **Risk groups:** summary stage partly uses surgical pathology, so risk groups are better informed for men who had surgery than for men who did not.

- **Models:** ordered steps 0 to 2 (year; clinical need; social position) for both model types, tuned once per model and stratum on step 2. Intervals are 95% cluster bootstrap intervals (500 resamples over rurality by county income cells).

## Summary

- **Crude:** a recorded curative treatment for intermediate risk 75.4%, high risk 81.1%.

- **Predictability:** AUC at step 2 ranged from 0.692 to 0.865 (0.5 is chance), and log-loss skill from 8.79% to 31.76%.

- **Social position increment:** the interval lay above 0 in 6 of 6 stratum and model combinations.

- **LightGBM against penalised logistic regression:** LightGBM had higher step 2 skill in 3 of 3 strata.

- **Tuning:** penalised logistic regression chose C = 1 (intermediate and high risk (pooled)), 0.01 (intermediate risk), 10 (high risk); at an edge of the grid in: intermediate risk, high risk.

## Crude percentages

Numbers of men are rounded to the nearest 10. Statistics resting on 1 to 4 men are hidden, and a percentage is hidden when 1 to 4 men in the row did, or did not, have a recorded curative treatment.

### By risk group

| risk group | men | % with a recorded curative treatment |
|---|---|---|
| intermediate | 178,250 | 75.4 |
| high | 174,390 | 81.1 |

### By risk group and county rurality

| risk group | rurality | men | % with a recorded curative treatment |
|---|---|---|---|
| intermediate | Metro, 1 million or more | 104,530 | 76.0 |
| intermediate | Metro, 250,000 to 1 million | 39,410 | 75.3 |
| intermediate | Metro, under 250,000 | 14,100 | 74.5 |
| intermediate | Nonmetro, adjacent to metro | 12,430 | 73.9 |
| intermediate | Nonmetro, not adjacent to metro | 7,700 | 72.3 |
| intermediate | Unknown | 80 | 53.2 |
| high | Metro, 1 million or more | 100,450 | 81.9 |
| high | Metro, 250,000 to 1 million | 38,520 | 82.1 |
| high | Metro, under 250,000 | 13,730 | 78.9 |
| high | Nonmetro, adjacent to metro | 13,060 | 77.7 |
| high | Nonmetro, not adjacent to metro | 8,490 | 75.3 |
| high | Unknown | 150 | 63.9 |

### By risk group and county income quartile

| risk group | county income quartile | men | % with a recorded curative treatment |
|---|---|---|---|
| intermediate | Q1 (lowest) | 14,140 | 72.7 |
| intermediate | Q2 | 42,320 | 75.1 |
| intermediate | Q3 | 61,910 | 75.7 |
| intermediate | Q4 (highest) | 59,870 | 76.0 |
| intermediate | Unknown | 20 | 36.4 |
| high | Q1 (lowest) | 14,280 | 73.7 |
| high | Q2 | 41,500 | 79.6 |
| high | Q3 | 62,280 | 82.0 |
| high | Q4 (highest) | 56,310 | 83.0 |
| high | Unknown | 30 | 51.6 |

### By risk group and marital status

| risk group | marital status | men | % with a recorded curative treatment |
|---|---|---|---|
| intermediate | Married (including common law) | 118,930 | 79.0 |
| intermediate | Single (never married) | 20,560 | 72.8 |
| intermediate | Divorced | 12,520 | 74.5 |
| intermediate | Separated | 1,550 | 71.4 |
| intermediate | Widowed | 6,020 | 71.0 |
| intermediate | Unmarried or Domestic Partner | 790 | 74.6 |
| intermediate | Unknown | 17,890 | 56.8 |
| high | Married (including common law) | 115,360 | 86.2 |
| high | Single (never married) | 20,970 | 79.2 |
| high | Divorced | 12,170 | 80.7 |
| high | Separated | 1,560 | 78.2 |
| high | Widowed | 7,450 | 64.7 |
| high | Unmarried or Domestic Partner | 730 | 86.5 |
| high | Unknown | 16,140 | 54.7 |

## Value added at each step

Skill is the percentage reduction in out-of-fold log-loss against step 0 (higher is better). Added values are in percentage points with intervals. AUC: 0.5 is chance. Calibration slope: 1 is ideal.

| stratum | model | skill at step 2 | clinical need added | social position added | social position as % of step 2 skill | AUC at step 2 | calibration slope at step 2 |
|---|---|---|---|---|---|---|---|
| intermediate and high risk (pooled) | penalised logistic regression | 17.18 | 15.22 (14.85 to 15.65) | 1.96 (1.72 to 2.31) | 11 | 0.771 | 1.00 |
| intermediate and high risk (pooled) | LightGBM | 20.49 | 18.32 (17.92 to 18.77) | 2.16 (1.92 to 2.54) | 11 | 0.791 | 1.02 |
| intermediate risk | penalised logistic regression | 8.79 | 6.81 (6.38 to 7.21) | 1.97 (1.65 to 2.42) | 22 | 0.692 | 1.00 |
| intermediate risk | LightGBM | 10.14 | 7.83 (7.42 to 8.20) | 2.31 (1.99 to 2.82) | 23 | 0.703 | 1.02 |
| high risk | penalised logistic regression | 29.29 | 27.25 (26.63 to 27.96) | 2.04 (1.84 to 2.33) | 7 | 0.854 | 1.00 |
| high risk | LightGBM | 31.76 | 29.54 (28.94 to 30.17) | 2.22 (2.00 to 2.53) | 7 | 0.865 | 1.01 |

## Standardised percentage with a recorded curative treatment

Each man keeps his own clinical features and year of diagnosis while his social features are set to a profile, using a model fitted on all men in the stratum at step 2. The reference profile is married, living in a county in a metropolitan area of 1 million or more, with county income rank at the 83.33% quantile of these men. Area profiles set rurality and county income together, at the median county income band of men living there:
- Metro, 1 million or more: $90,000 - $94,999
- Metro, 250,000 to 1 million: $80,000 - $84,999
- Metro, under 250,000: $65,000 - $69,999
- Nonmetro, adjacent to metro: $55,000 - $59,999
- Nonmetro, not adjacent to metro: $55,000 - $59,999

A difference is described as meaningful only when both model types agree on 3 percentage points or more in the same direction (amendment 1.7).

### Contrasts (percentage points)

| stratum | contrast | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|---|
| intermediate and high risk (pooled) | all social features as observed minus reference profile | -4.3 | -3.5 | both models 3 points or more, same direction |
| intermediate and high risk (pooled) | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -2.9 | -1.4 | both models under 3 points |
| intermediate and high risk (pooled) | marital status: Single (never married) minus Married (including common law) | -6.5 | -5.9 | both models 3 points or more, same direction |
| intermediate risk | all social features as observed minus reference profile | -4.2 | -3.2 | both models 3 points or more, same direction |
| intermediate risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -2.2 | -0.3 | both models under 3 points |
| intermediate risk | marital status: Single (never married) minus Married (including common law) | -7.2 | -6.4 | both models 3 points or more, same direction |
| high risk | all social features as observed minus reference profile | -4.3 | -3.8 | both models 3 points or more, same direction |
| high risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -3.3 | -2.5 | models disagree |
| high risk | marital status: Single (never married) minus Married (including common law) | -5.8 | -5.1 | both models 3 points or more, same direction |

### Standardised percentages by profile, intermediate and high risk (pooled)

| profile | penalised logistic regression | LightGBM |
|---|---|---|
| as observed | 78.2 | 78.2 |
| reference profile | 82.5 | 81.7 |
| area: Metro, 1 million or more, typical county income ($90,000 - $94,999) | 82.1 | 81.5 |
| area: Metro, 250,000 to 1 million, typical county income ($80,000 - $84,999) | 81.5 | 81.6 |
| area: Metro, under 250,000, typical county income ($65,000 - $69,999) | 80.7 | 81.1 |
| area: Nonmetro, adjacent to metro, typical county income ($55,000 - $59,999) | 79.7 | 80.1 |
| area: Nonmetro, not adjacent to metro, typical county income ($55,000 - $59,999) | 79.2 | 80.1 |
| marital status: Married (including common law) | 82.5 | 81.7 |
| marital status: Single (never married) | 76.0 | 75.9 |
| marital status: Divorced | 78.1 | 77.1 |
| marital status: Separated | 75.5 | 75.9 |
| marital status: Widowed | 78.4 | 78.3 |
| marital status: Unmarried or Domestic Partner | 79.8 | 77.4 |
| marital status: Unknown | 65.0 | 66.9 |
