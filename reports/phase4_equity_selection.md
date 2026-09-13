# Phase 4, part 3. Standardised differences, income inequality and selection

Generated 2026-09-13 15:52 UTC by `scripts/run_phase4_equity_selection.py` at git revision `62d951c`. Definitions: `PROTOCOL.md` A5 to A7 with amendments 1.6 and 1.7. All results are associations, not causal effects.

## A5. Standardised percentage waiting more than 90 days

Each man keeps his own clinical features and year of diagnosis while his social features are set to a profile, using a model fitted on all men in the stratum at step 2. The mean predicted probability is the standardised percentage.

- **Reference profile:** married, living in a county in a metropolitan area of 1 million or more, with county income rank 14 of 16 (the cohort's 83.33% quantile, the midpoint of the top income tertile).

- **Area profiles** set rurality and county income together, at the median county income band of men living in each type of area:
- Metro, 1 million or more: $90,000 - $94,999
- Metro, 250,000 to 1 million: $80,000 - $84,999
- Metro, under 250,000: $65,000 - $69,999
- Nonmetro, adjacent to metro: $55,000 - $59,999
- Nonmetro, not adjacent to metro: $55,000 - $59,999

- **Why rurality and income are not changed one at a time:** the two are strongly correlated in this cohort, so holding one fixed while changing the other creates combinations that are rare in the data. The two model types gave conflicting estimates for such changes. For all men, changing only rurality from Metro, 1 million or more to Nonmetro, not adjacent to metro changed the standardised percentage by -8.7 points under penalised logistic regression and 1.7 under LightGBM; changing only county income from Q4 (highest) to Q1 (lowest) changed it by -0.9 and -8.7 points. These one-at-a-time results are not interpreted and are kept in `reports/phase4_tables/standardised_profiles_one_at_a_time.csv`.

- **How differences are judged:** bootstrap intervals that hold the fitted model fixed are far narrower than the disagreement between model types, so they are not reported. A difference is described as meaningful only when both model types agree on 3 percentage points or more in the same direction.

### Contrasts (percentage points)

| stratum | contrast | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|---|
| all men (pooled) | all social features as observed minus reference profile | -1.1 | -1.6 | both models under 3 points |
| all men (pooled) | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -9.2 | -8.8 | both models 3 points or more, same direction |
| all men (pooled) | marital status: Single (never married) minus Married (including common law) | 6.7 | 5.9 | both models 3 points or more, same direction |
| low risk | all social features as observed minus reference profile | -3.4 | -4.7 | both models 3 points or more, same direction |
| low risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -11.3 | -13.5 | both models 3 points or more, same direction |
| low risk | marital status: Single (never married) minus Married (including common law) | 3.6 | 2.4 | same direction, only one model 3 points or more |
| intermediate risk | all social features as observed minus reference profile | -1.4 | -1.6 | both models under 3 points |
| intermediate risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -8.7 | -9.5 | both models 3 points or more, same direction |
| intermediate risk | marital status: Single (never married) minus Married (including common law) | 6.4 | 5.5 | both models 3 points or more, same direction |
| high risk | all social features as observed minus reference profile | 0.1 | -0.1 | both models under 3 points |
| high risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -8.4 | -7.2 | both models 3 points or more, same direction |
| high risk | marital status: Single (never married) minus Married (including common law) | 8.3 | 7.6 | both models 3 points or more, same direction |
| unknown risk | all social features as observed minus reference profile | -0.1 | 0.0 | both models under 3 points |
| unknown risk | area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income | -12.1 | -14.2 | both models 3 points or more, same direction |
| unknown risk | marital status: Single (never married) minus Married (including common law) | 6.0 | 6.2 | both models 3 points or more, same direction |

### Standardised percentages by profile, all men (pooled)

| profile | penalised logistic regression | LightGBM |
|---|---|---|
| as observed | 39.7 | 39.7 |
| reference profile | 40.8 | 41.3 |
| area: Metro, 1 million or more, typical county income ($90,000 - $94,999) | 40.6 | 41.1 |
| area: Metro, 250,000 to 1 million, typical county income ($80,000 - $84,999) | 36.3 | 36.9 |
| area: Metro, under 250,000, typical county income ($65,000 - $69,999) | 32.8 | 32.4 |
| area: Nonmetro, adjacent to metro, typical county income ($55,000 - $59,999) | 31.8 | 31.9 |
| area: Nonmetro, not adjacent to metro, typical county income ($55,000 - $59,999) | 31.4 | 32.4 |
| marital status: Married (including common law) | 40.8 | 41.3 |
| marital status: Single (never married) | 47.5 | 47.2 |
| marital status: Divorced | 46.9 | 46.7 |
| marital status: Separated | 49.4 | 46.9 |
| marital status: Widowed | 42.7 | 44.0 |
| marital status: Unmarried or Domestic Partner | 46.7 | 45.9 |
| marital status: Unknown | 45.6 | 45.7 |

### Crude excess waiting days beyond 90 days per 1,000 men

These are crude observed values, not standardised: standardised excess days would need a separate model for the number of days, which was not built (amendment 1.6). Top-coded intervals count at 731 days. Numbers of men are rounded to the nearest 10.

| stratum | variable | group | men | excess days per 1,000 men (crude) |
|---|---|---|---|---|
| all men (pooled) | rurality | Metro, 1 million or more | 194,680 | 30,597 |
| all men (pooled) | rurality | Metro, 250,000 to 1 million | 72,150 | 26,040 |
| all men (pooled) | rurality | Metro, under 250,000 | 26,090 | 24,387 |
| all men (pooled) | rurality | Nonmetro, adjacent to metro | 23,360 | 21,678 |
| all men (pooled) | rurality | Nonmetro, not adjacent to metro | 14,390 | 20,014 |
| all men (pooled) | rurality | Unknown | 160 | 24,258 |
| all men (pooled) | county income quartile | Q1 (lowest) | 26,440 | 22,045 |
| all men (pooled) | county income quartile | Q2 | 79,800 | 25,568 |
| all men (pooled) | county income quartile | Q3 | 116,210 | 30,250 |
| all men (pooled) | county income quartile | Q4 (highest) | 108,350 | 28,889 |
| all men (pooled) | county income quartile | Unknown | 30 | 45,571 |
| high risk | rurality | Metro, 1 million or more | 75,760 | 21,912 |
| high risk | rurality | Metro, 250,000 to 1 million | 29,320 | 17,331 |
| high risk | rurality | Metro, under 250,000 | 10,130 | 16,770 |
| high risk | rurality | Nonmetro, adjacent to metro | 9,590 | 15,316 |
| high risk | rurality | Nonmetro, not adjacent to metro | 6,010 | 13,553 |
| high risk | rurality | Unknown | 90 | 11,216 |
| high risk | county income quartile | Q1 (lowest) | 9,920 | 15,461 |
| high risk | county income quartile | Q2 | 30,420 | 17,899 |
| high risk | county income quartile | Q3 | 46,890 | 21,596 |
| high risk | county income quartile | Q4 (highest) | 43,650 | 19,625 |
| high risk | county income quartile | Unknown | 10 | 18,462 |

## A6. Income inequality in delay

Erreygers-corrected concentration index of waiting more than 90 days, ranking men by county median household income (poorest first). It ranges from -1 to 1: a negative value means delay is concentrated in lower-income counties, a positive value means it is concentrated in higher-income counties, and 0 means no income gradient. Men with unknown county income are excluded. Intervals are 95% cluster bootstrap intervals (500 resamples over rurality by county income cells).

| stratum | Erreygers index (95% interval) |
|---|---|
| all men (pooled) | 0.062 (0.039 to 0.083) |
| low risk | 0.103 (0.068 to 0.134) |
| intermediate risk | 0.075 (0.051 to 0.096) |
| high risk | 0.041 (0.017 to 0.065) |
| unknown risk | 0.077 (0.037 to 0.128) |

## A7. Selection: men without a recorded interval

Treated men meeting cohort steps 1 to 6, excluding intervals of 0 days. The lower bound assumes every man without a recorded interval waited 90 days or less; the upper bound assumes every such man waited longer. Numbers of men are rounded to the nearest 10, and statistics resting on 1 to 4 men are hidden.

### Bounds by risk group

| risk group | men | % over 90 days (recorded men) | lower bound % | upper bound % | % with no recorded interval |
|---|---|---|---|---|---|
| low | 59,930 | 47.9 | 46.0 | 50.0 | 4.1 |
| intermediate | 132,650 | 42.8 | 41.2 | 44.9 | 3.8 |
| high | 137,950 | 32.8 | 31.1 | 36.2 | 5.1 |
| unknown | 17,300 | 42.1 | 36.1 | 50.5 | 14.4 |

### Bounds by rurality

| rurality | men | % over 90 days (recorded men) | lower bound % | upper bound % | % with no recorded interval |
|---|---|---|---|---|---|
| Metro, 1 million or more | 205,980 | 42.5 | 40.2 | 45.7 | 5.5 |
| Metro, 250,000 to 1 million | 75,790 | 37.6 | 35.8 | 40.6 | 4.8 |
| Metro, under 250,000 | 27,050 | 34.2 | 33.0 | 36.6 | 3.6 |
| Nonmetro, adjacent to metro | 24,050 | 33.2 | 32.2 | 35.1 | 2.9 |
| Nonmetro, not adjacent to metro | 14,780 | 32.2 | 31.3 | 34.0 | 2.7 |
| Unknown | 170 | 33.3 | 31.9 | 36.1 | 4.2 |

### Bounds by county income quartile

| county income quartile | men | % over 90 days (recorded men) | lower bound % | upper bound % | % with no recorded interval |
|---|---|---|---|---|---|
| Q1 (lowest) | 27,000 | 31.7 | 31.0 | 33.1 | 2.1 |
| Q2 | 84,200 | 36.9 | 35.0 | 40.2 | 5.2 |
| Q3 | 123,100 | 41.8 | 39.5 | 45.1 | 5.6 |
| Q4 (highest) | 113,500 | 41.4 | 39.6 | 44.1 | 4.5 |
| Unknown | 30 | 39.3 | 32.4 | 50.0 | 17.6 |

### Bounds by marital status

| marital status | men | % over 90 days (recorded men) | lower bound % | upper bound % | % with no recorded interval |
|---|---|---|---|---|---|
| Married (including common law) | 244,030 | 38.1 | 36.3 | 41.0 | 4.7 |
| Single (never married) | 38,630 | 45.7 | 43.5 | 48.4 | 5.0 |
| Divorced | 23,070 | 43.3 | 41.3 | 45.8 | 4.5 |
| Separated | 2,790 | 46.3 | 43.8 | 49.4 | 5.6 |
| Widowed | 10,540 | 36.5 | 34.3 | 40.3 | 6.1 |
| Unmarried or Domestic Partner | 1,420 | 46.7 | 45.0 | 48.8 | 3.8 |
| Unknown | 27,350 | 42.4 | 39.8 | 46.0 | 6.1 |

### Is having a recorded interval predictable from social position?

Out-of-fold penalised logistic regression for having no recorded interval, with the same ordered steps. Skill added by social position above 0 means missingness is socially patterned beyond clinical need. Intervals are 95% cluster bootstrap intervals (500 resamples).

| comparison | skill added, percentage points (95% interval) |
|---|---|
| clinical need (step 0 to 1) | 4.99 (4.51 to 5.42) |
| social position (step 1 to 2) | 0.53 (0.07 to 1.02) |

### Inverse probability weighted percentages

Percentage of men with a recorded interval who waited more than 90 days, unweighted and weighted by the inverse of each man's predicted probability of having a recorded interval (step 2 membership model).

| variable | group | men | % over 90 days (unweighted) | % over 90 days (weighted) |
|---|---|---|---|---|
| rurality | Metro, 1 million or more | 194,680 | 42.5 | 42.3 |
| rurality | Metro, 250,000 to 1 million | 72,150 | 37.6 | 37.4 |
| rurality | Metro, under 250,000 | 26,090 | 34.2 | 34.1 |
| rurality | Nonmetro, adjacent to metro | 23,360 | 33.2 | 33.1 |
| rurality | Nonmetro, not adjacent to metro | 14,390 | 32.2 | 32.0 |
| rurality | Unknown | 160 | 33.3 | 33.5 |
| county income quartile | Q1 (lowest) | 26,440 | 31.7 | 31.5 |
| county income quartile | Q2 | 79,800 | 36.9 | 36.8 |
| county income quartile | Q3 | 116,210 | 41.8 | 41.6 |
| county income quartile | Q4 (highest) | 108,350 | 41.4 | 41.3 |
| county income quartile | Unknown | 30 | 39.3 | 39.6 |
| marital status | Married (including common law) | 232,530 | 38.1 | 38.0 |
| marital status | Single (never married) | 36,700 | 45.7 | 45.5 |
| marital status | Divorced | 22,020 | 43.3 | 43.1 |
| marital status | Separated | 2,630 | 46.3 | 46.2 |
| marital status | Widowed | 9,910 | 36.5 | 36.3 |
| marital status | Unmarried or Domestic Partner | 1,370 | 46.7 | 46.6 |
| marital status | Unknown | 25,670 | 42.4 | 42.4 |
