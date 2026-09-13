# Phase 4, part 4. Sensitivity analyses

Generated 2026-09-13 15:40 UTC by `scripts/run_phase4_sensitivity_report.py` at git revision `62d951c`. Definitions: `PROTOCOL.md` A8 with amendment 1.8. All results are associations, not causal effects.

## How the checks were run

- **One change at a time:** each scenario rebuilds the cohort with exactly one setting changed from the primary analysis.

- **Models:** steps 0 to 2 are refitted for both model types, with the hyperparameters tuned in the primary analysis for the same model and stratum. Step 3 and the leave-one-variable-out refits are not repeated.

- **Intervals:** 95% cluster bootstrap intervals (500 resamples over rurality by county income cells).

- **Standardised contrasts:** judged by the agreement rule of amendment 1.7 (both models 3 percentage points or more in the same direction).

- **Thresholds:** fewer men wait beyond longer thresholds, so skill and percentage point differences are not directly comparable across the threshold scenarios.

## Summary

- **Social position increment:** the 95% interval lay above 0 in 98 of 100 scenario, stratum and model combinations. The exceptions were:
  - radical prostatectomy without radiotherapy only, unknown risk, LightGBM: 0.74 (-0.13 to 1.42)
  - one primary cancer only (strict first primary), unknown risk, penalised logistic regression: 0.40 (-0.04 to 0.79)

- **Pooled social position increment across scenarios** (percentage points of log-loss skill): penalised logistic regression from 0.54 (threshold of 60 days) to 0.68 (threshold of 120 days); LightGBM from 0.94 (including men diagnosed in 2023) to 1.06 (threshold of 120 days). In the primary analysis it was 0.62 and 0.99.

- **LightGBM against penalised logistic regression:** LightGBM had higher step 2 skill in 47 of 50 scenario and stratum combinations. Combinations where it did not:
  - radical prostatectomy without radiotherapy only, low risk: LightGBM 0.73, logistic regression 0.76
  - radical prostatectomy without radiotherapy only, unknown risk: LightGBM 1.36, logistic regression 1.53
  - threshold of 180 days, low risk: LightGBM 0.61, logistic regression 0.63

- **Area:** in the pooled cohort, both models agreed on a difference of 3 points or more in the primary direction (lower) in 9 of 10 scenarios, and in 47 of 50 scenario and stratum combinations.

- **Marital status:** in the pooled cohort, both models agreed on a difference of 3 points or more in the primary direction (higher) in 10 of 10 scenarios, and in 38 of 50 scenario and stratum combinations.

- **Wider C grid (0.0001, 0.001, 0.01, 0.1, 1, 10, post hoc):** the same C was chosen as in the primary analysis in every stratum, so the logistic regression results are unchanged; the edge of the original grid did not limit the model. LightGBM had higher step 2 skill than the re-tuned logistic regression in 5 of 5 strata. No chosen C was at an edge of the wider grid.

- **Scenarios that change only part of the analysis:** risk groups from Gleason score and PSA only change which men fall in each risk stratum but not the pooled cohort or its features, so pooled results equal the primary analysis.

## Percentage waiting beyond the threshold

Crude percentages. Numbers of men are rounded to the nearest 10; statistics resting on 1 to 4 men are hidden. A lower percentage is better.

| scenario | threshold (days) | men | % over threshold, all men | % over threshold, low risk | % over threshold, intermediate risk | % over threshold, high risk | % over threshold, unknown risk |
|---|---|---|---|---|---|---|---|
| primary analysis | 90 | 330,830 | 39.7 | 47.9 | 42.8 | 32.8 | 42.1 |
| threshold of 60 days | 60 | 330,830 | 66.6 | 75.0 | 70.0 | 59.5 | 66.7 |
| threshold of 120 days | 120 | 330,830 | 23.0 | 30.3 | 24.8 | 17.5 | 26.8 |
| threshold of 180 days | 180 | 330,830 | 9.1 | 13.9 | 9.5 | 6.1 | 13.3 |
| risk groups from Gleason score and PSA only | 90 | 330,830 | 39.7 | 47.7 | 42.6 | 28.2 | 41.7 |
| radical prostatectomy without radiotherapy only | 90 | 159,580 | 41.1 | 45.8 | 42.3 | 38.4 | 38.2 |
| excluding men diagnosed in 2020 | 90 | 306,960 | 39.6 | 47.4 | 42.5 | 32.9 | 41.7 |
| including men diagnosed in 2023 | 90 | 358,540 | 40.8 | 48.4 | 44.2 | 34.0 | 43.5 |
| including intervals of 0 days | 90 | 338,580 | 38.8 | 47.2 | 42.2 | 32.0 | 37.8 |
| one primary cancer only (strict first primary) | 90 | 296,120 | 40.1 | 48.3 | 43.2 | 33.2 | 42.7 |
| excluding prostatectomy not otherwise specified | 90 | 330,180 | 39.7 | 47.9 | 42.8 | 32.8 | 42.2 |

## Social position increment by scenario

Percentage points of out-of-fold log-loss skill added by social position (step 1 to 2), with 95% intervals. Higher means social position predicts more of the delay.

| scenario | model | all men (pooled) | low risk | intermediate risk | high risk | unknown risk |
|---|---|---|---|---|---|---|
| primary analysis | penalised logistic regression | 0.62 (0.39 to 0.87) | 0.62 (0.32 to 0.94) | 0.56 (0.35 to 0.83) | 0.86 (0.60 to 1.15) | 0.42 (0.08 to 0.80) |
| primary analysis | LightGBM | 0.99 (0.73 to 1.30) | 0.96 (0.67 to 1.28) | 0.93 (0.65 to 1.27) | 1.18 (0.90 to 1.56) | 1.37 (0.80 to 2.19) |
| threshold of 60 days | penalised logistic regression | 0.54 (0.31 to 0.79) | 0.82 (0.38 to 1.27) | 0.53 (0.28 to 0.82) | 0.61 (0.39 to 0.86) | 0.41 (0.06 to 0.86) |
| threshold of 60 days | LightGBM | 0.94 (0.73 to 1.18) | 1.22 (0.86 to 1.67) | 0.88 (0.66 to 1.16) | 0.96 (0.75 to 1.21) | 1.56 (0.90 to 2.36) |
| threshold of 120 days | penalised logistic regression | 0.68 (0.45 to 0.93) | 0.60 (0.31 to 0.90) | 0.58 (0.37 to 0.82) | 1.02 (0.75 to 1.33) | 0.52 (0.10 to 1.00) |
| threshold of 120 days | LightGBM | 1.06 (0.79 to 1.38) | 0.97 (0.69 to 1.23) | 0.90 (0.58 to 1.25) | 1.39 (1.10 to 1.77) | 1.47 (0.71 to 2.40) |
| threshold of 180 days | penalised logistic regression | 0.66 (0.41 to 0.92) | 0.56 (0.32 to 0.82) | 0.58 (0.33 to 0.83) | 0.96 (0.64 to 1.31) | 0.58 (0.00 to 1.19) |
| threshold of 180 days | LightGBM | 1.00 (0.69 to 1.35) | 0.84 (0.56 to 1.10) | 0.93 (0.60 to 1.33) | 1.40 (1.05 to 1.81) | 1.33 (0.14 to 2.85) |
| risk groups from Gleason score and PSA only | penalised logistic regression | 0.62 (0.39 to 0.87) | 0.67 (0.34 to 1.01) | 0.58 (0.38 to 0.82) | 0.94 (0.65 to 1.28) | 0.51 (0.16 to 0.87) |
| risk groups from Gleason score and PSA only | LightGBM | 0.99 (0.73 to 1.30) | 1.02 (0.71 to 1.32) | 0.92 (0.67 to 1.23) | 1.34 (1.00 to 1.78) | 1.21 (0.59 to 1.92) |
| radical prostatectomy without radiotherapy only | penalised logistic regression | 0.66 (0.48 to 0.88) | 0.71 (0.47 to 1.07) | 0.59 (0.37 to 0.83) | 0.77 (0.56 to 0.99) | 0.62 (0.19 to 1.01) |
| radical prostatectomy without radiotherapy only | LightGBM | 1.00 (0.79 to 1.26) | 0.88 (0.60 to 1.19) | 0.90 (0.65 to 1.20) | 1.07 (0.85 to 1.36) | 0.74 (-0.13 to 1.42) |
| excluding men diagnosed in 2020 | penalised logistic regression | 0.64 (0.40 to 0.91) | 0.59 (0.28 to 0.97) | 0.58 (0.33 to 0.86) | 0.89 (0.62 to 1.20) | 0.43 (0.03 to 0.83) |
| excluding men diagnosed in 2020 | LightGBM | 1.03 (0.75 to 1.35) | 0.95 (0.67 to 1.27) | 0.98 (0.66 to 1.35) | 1.20 (0.91 to 1.58) | 1.33 (0.61 to 2.21) |
| including men diagnosed in 2023 | penalised logistic regression | 0.56 (0.35 to 0.80) | 0.57 (0.27 to 0.89) | 0.51 (0.31 to 0.75) | 0.76 (0.51 to 1.04) | 0.39 (0.08 to 0.75) |
| including men diagnosed in 2023 | LightGBM | 0.94 (0.69 to 1.22) | 0.98 (0.72 to 1.28) | 0.87 (0.61 to 1.19) | 1.10 (0.86 to 1.46) | 1.17 (0.54 to 1.95) |
| including intervals of 0 days | penalised logistic regression | 0.61 (0.38 to 0.86) | 0.63 (0.32 to 0.95) | 0.55 (0.33 to 0.81) | 0.83 (0.57 to 1.12) | 0.52 (0.16 to 0.91) |
| including intervals of 0 days | LightGBM | 0.97 (0.70 to 1.27) | 1.04 (0.77 to 1.35) | 0.92 (0.63 to 1.26) | 1.14 (0.87 to 1.50) | 1.31 (0.65 to 2.16) |
| one primary cancer only (strict first primary) | penalised logistic regression | 0.61 (0.38 to 0.85) | 0.63 (0.33 to 0.95) | 0.54 (0.32 to 0.79) | 0.85 (0.59 to 1.12) | 0.40 (-0.04 to 0.79) |
| one primary cancer only (strict first primary) | LightGBM | 0.98 (0.73 to 1.27) | 0.98 (0.71 to 1.27) | 0.90 (0.62 to 1.24) | 1.22 (0.93 to 1.58) | 1.39 (0.70 to 2.26) |
| excluding prostatectomy not otherwise specified | penalised logistic regression | 0.62 (0.39 to 0.87) | 0.61 (0.30 to 0.94) | 0.54 (0.32 to 0.80) | 0.86 (0.59 to 1.15) | 0.52 (0.15 to 0.93) |
| excluding prostatectomy not otherwise specified | LightGBM | 0.98 (0.72 to 1.28) | 1.03 (0.76 to 1.32) | 0.93 (0.65 to 1.28) | 1.19 (0.92 to 1.55) | 1.37 (0.74 to 2.13) |

## Standardised contrasts, all men (pooled)

Percentage points. Contrasts for each risk group are in `reports/phase4_tables/sensitivity_contrasts.csv`.

### Area: Nonmetro, not adjacent to metro minus Metro, 1 million or more, each at its typical county income

| scenario | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|
| primary analysis | -9.2 | -8.8 | both models 3 points or more, same direction |
| threshold of 60 days | -10.6 | -10.3 | both models 3 points or more, same direction |
| threshold of 120 days | -6.9 | -7.1 | both models 3 points or more, same direction |
| threshold of 180 days | -3.0 | -3.2 | same direction, only one model 3 points or more |
| risk groups from Gleason score and PSA only | -9.2 | -8.8 | both models 3 points or more, same direction |
| radical prostatectomy without radiotherapy only | -8.9 | -7.8 | both models 3 points or more, same direction |
| excluding men diagnosed in 2020 | -9.4 | -8.9 | both models 3 points or more, same direction |
| including men diagnosed in 2023 | -8.6 | -8.3 | both models 3 points or more, same direction |
| including intervals of 0 days | -9.2 | -9.2 | both models 3 points or more, same direction |
| one primary cancer only (strict first primary) | -9.1 | -9.3 | both models 3 points or more, same direction |
| excluding prostatectomy not otherwise specified | -9.2 | -9.1 | both models 3 points or more, same direction |

### Marital status: never married minus the reference profile (married)

| scenario | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|
| primary analysis | 6.7 | 5.9 | both models 3 points or more, same direction |
| threshold of 60 days | 3.7 | 3.2 | both models 3 points or more, same direction |
| threshold of 120 days | 6.0 | 5.0 | both models 3 points or more, same direction |
| threshold of 180 days | 3.4 | 3.1 | both models 3 points or more, same direction |
| risk groups from Gleason score and PSA only | 6.7 | 5.9 | both models 3 points or more, same direction |
| radical prostatectomy without radiotherapy only | 7.1 | 6.9 | both models 3 points or more, same direction |
| excluding men diagnosed in 2020 | 6.8 | 5.9 | both models 3 points or more, same direction |
| including men diagnosed in 2023 | 6.4 | 5.8 | both models 3 points or more, same direction |
| including intervals of 0 days | 6.5 | 5.8 | both models 3 points or more, same direction |
| one primary cancer only (strict first primary) | 6.6 | 5.6 | both models 3 points or more, same direction |
| excluding prostatectomy not otherwise specified | 6.7 | 5.9 | both models 3 points or more, same direction |

### All social features as observed minus the reference profile

| scenario | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|
| primary analysis | -1.1 | -1.6 | both models under 3 points |
| threshold of 60 days | -1.7 | -2.8 | both models under 3 points |
| threshold of 120 days | -0.6 | -0.6 | both models under 3 points |
| threshold of 180 days | 0.1 | 0.3 | both models under 3 points |
| risk groups from Gleason score and PSA only | -1.1 | -1.6 | both models under 3 points |
| radical prostatectomy without radiotherapy only | -1.5 | -1.1 | both models under 3 points |
| excluding men diagnosed in 2020 | -1.1 | -1.6 | both models under 3 points |
| including men diagnosed in 2023 | -1.0 | -1.6 | both models under 3 points |
| including intervals of 0 days | -1.1 | -1.6 | both models under 3 points |
| one primary cancer only (strict first primary) | -1.1 | -1.6 | both models under 3 points |
| excluding prostatectomy not otherwise specified | -1.1 | -1.6 | both models under 3 points |

## Penalised logistic regression with a wider C grid (post hoc)

In the primary analysis penalised logistic regression chose C = 0.01 (all men (pooled)), 0.01 (low risk), 0.01 (intermediate risk), 0.01 (high risk), 0.01 (unknown risk) from the grid 0.01, 0.1, 1, 10. Here C was re-tuned on the grid 0.0001, 0.001, 0.01, 0.1, 1, 10 in the primary cohort, using the same tuning procedure, and steps 0 to 2 were refitted. Skill is in percentage points of log-loss reduction against step 0; higher is better.

| stratum | C chosen (wider grid) | at an edge of the wider grid | logistic step 2 skill, original grid | logistic step 2 skill, wider grid | LightGBM step 2 skill | social position added, original grid | social position added, wider grid |
|---|---|---|---|---|---|---|---|
| all men (pooled) | 0.01 | no | 3.63 | 3.63 | 4.17 | 0.62 (0.39 to 0.87) | 0.62 (0.39 to 0.87) |
| low risk | 0.01 | no | 0.76 | 0.76 | 0.99 | 0.62 (0.32 to 0.94) | 0.62 (0.32 to 0.94) |
| intermediate risk | 0.01 | no | 1.06 | 1.06 | 1.48 | 0.56 (0.35 to 0.83) | 0.56 (0.35 to 0.83) |
| high risk | 0.01 | no | 4.39 | 4.39 | 4.90 | 0.86 (0.60 to 1.15) | 0.86 (0.60 to 1.15) |
| unknown risk | 0.01 | no | 1.07 | 1.07 | 1.96 | 0.42 (0.08 to 0.80) | 0.42 (0.08 to 0.80) |
