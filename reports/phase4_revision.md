# Phase 4, part 6. Revision analyses after internal review (post-review)

Generated 2026-09-13 17:59 UTC by `scripts/run_phase4_revision_report.py` at git revision `a22bbfc`. Definitions: `PROTOCOL.md` amendment 1.9. These analyses were specified after an internal review of the draft preprint and before they were run. All results are associations, not causal effects.

## Summary

- **Social position increment under per-step tuning:** the 95% cell-bootstrap interval lay above 0 in 10 of 10 stratum and model combinations, and in 10 of 10 with county income band clusters.

- **Fold-seed variability:** across 10 fold-assignment seeds, the smallest increment was above 0 in 10 of 10 stratum and model combinations.

- **Logistic regression tuning:** C was chosen at an edge of the grid (0.01 or 10) in 8 of 15 stratum and step combinations.

- **Inverse probability weighting:** among published group percentages, weighting changed the percentage by at most 0.36 points, and by at most 0.21 points in groups of 1,000 men or more.

## (a) and (b) Social position increment with per-step tuning and repeated fold assignment

Percentage points of out-of-fold log-loss skill added by social position (step 1 to 2). Intervals are 95% cluster bootstrap intervals over out-of-fold predictions from the first fold seed (500 resamples, no refitting). The seed range shows how much the estimate moves when men are assigned to different folds; tuning was not repeated per seed.

| stratum | model | social position added, primary (step 3 tuning) | social position added, per-step tuning, first fold seed | mean (minimum to maximum) over 10 fold seeds | interval with county income band clusters |
|---|---|---|---|---|---|
| all men (pooled) | penalised logistic regression | 0.62 (0.39 to 0.87) | 0.62 (0.39 to 0.87) | 0.62 (0.61 to 0.62) | 0.62 (0.38 to 0.90) |
| all men (pooled) | LightGBM | 0.99 (0.73 to 1.30) | 0.99 (0.73 to 1.30) | 0.99 (0.98 to 0.99) | 0.99 (0.72 to 1.35) |
| low risk | penalised logistic regression | 0.62 (0.32 to 0.94) | 0.62 (0.32 to 0.94) | 0.62 (0.59 to 0.63) | 0.62 (0.28 to 1.07) |
| low risk | LightGBM | 0.96 (0.67 to 1.28) | 0.96 (0.67 to 1.28) | 0.98 (0.95 to 1.01) | 0.96 (0.64 to 1.36) |
| intermediate risk | penalised logistic regression | 0.56 (0.35 to 0.83) | 0.56 (0.34 to 0.83) | 0.56 (0.54 to 0.56) | 0.56 (0.33 to 0.89) |
| intermediate risk | LightGBM | 0.93 (0.65 to 1.27) | 0.93 (0.65 to 1.27) | 0.93 (0.91 to 0.97) | 0.93 (0.63 to 1.31) |
| high risk | penalised logistic regression | 0.86 (0.60 to 1.15) | 0.86 (0.60 to 1.15) | 0.85 (0.85 to 0.86) | 0.86 (0.58 to 1.15) |
| high risk | LightGBM | 1.18 (0.90 to 1.56) | 1.18 (0.90 to 1.54) | 1.18 (1.16 to 1.20) | 1.18 (0.87 to 1.55) |
| unknown risk | penalised logistic regression | 0.42 (0.08 to 0.80) | 0.40 (0.07 to 0.80) | 0.41 (0.32 to 0.48) | 0.40 (0.07 to 0.78) |
| unknown risk | LightGBM | 1.37 (0.80 to 2.19) | 1.37 (0.80 to 2.19) | 1.29 (1.22 to 1.43) | 1.37 (0.78 to 2.09) |

### Clinical model comparison under per-step tuning

Where the LightGBM clinical model (step 1) is weaker than the logistic one, a larger LightGBM social increment can partly reflect that weaker reference. Values are means over fold seeds.

| stratum | clinical need added, logistic (seed mean) | clinical need added, LightGBM (seed mean) | LightGBM clinical model at least as good | step 2 skill, logistic (seed mean) | step 2 skill, LightGBM (seed mean) |
|---|---|---|---|---|---|
| all men (pooled) | 3.01 | 3.18 | yes | 3.63 | 4.17 |
| low risk | 0.14 | 0.05 | no | 0.76 | 1.03 |
| intermediate risk | 0.49 | 0.53 | yes | 1.05 | 1.47 |
| high risk | 3.53 | 3.72 | yes | 4.38 | 4.90 |
| unknown risk | 0.64 | 0.55 | no | 1.05 | 1.84 |

### Hyperparameters chosen at each step

| stratum | model | step | max_iter | C | learning_rate | n_estimators | num_leaves | min_child_samples |
|---|---|---|---|---|---|---|---|---|
| all men (pooled) | penalised logistic regression | 0 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| all men (pooled) | penalised logistic regression | 1 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| all men (pooled) | penalised logistic regression | 2 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| all men (pooled) | LightGBM | 0 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| all men (pooled) | LightGBM | 1 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| all men (pooled) | LightGBM | 2 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| low risk | penalised logistic regression | 0 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| low risk | penalised logistic regression | 1 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| low risk | penalised logistic regression | 2 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| low risk | LightGBM | 0 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| low risk | LightGBM | 1 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| low risk | LightGBM | 2 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| intermediate risk | penalised logistic regression | 0 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| intermediate risk | penalised logistic regression | 1 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| intermediate risk | penalised logistic regression | 2 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| intermediate risk | LightGBM | 0 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| intermediate risk | LightGBM | 1 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| intermediate risk | LightGBM | 2 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| high risk | penalised logistic regression | 0 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| high risk | penalised logistic regression | 1 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| high risk | penalised logistic regression | 2 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| high risk | LightGBM | 0 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| high risk | LightGBM | 1 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| high risk | LightGBM | 2 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| unknown risk | penalised logistic regression | 0 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| unknown risk | penalised logistic regression | 1 | 2000 | 0.1 | n/a | n/a | n/a | n/a |
| unknown risk | penalised logistic regression | 2 | 2000 | 0.01 | n/a | n/a | n/a | n/a |
| unknown risk | LightGBM | 0 | n/a | n/a | 0.05 | 200 | 15 | 50 |
| unknown risk | LightGBM | 1 | n/a | n/a | 0.05 | 200 | 15 | 200 |
| unknown risk | LightGBM | 2 | n/a | n/a | 0.05 | 200 | 15 | 200 |

## (c) Bootstrap clusters

Clusters are rurality by county income band cells (primary) or county income band alone (coarser alternative). The export has no county or registry identifier. Cluster sizes of 1 to 4 men are shown as <5.

| stratum | clustering | clusters | smallest cluster (men) | median cluster (men) | largest cluster (men) | largest cluster, % of men |
|---|---|---|---|---|---|---|
| all men (pooled) | rurality by income cells | 79 | 23 | 1,870 | 28,195 | 8.5 |
| all men (pooled) | county income band only | 17 | 28 | 22,703 | 36,147 | 10.9 |
| low risk | rurality by income cells | 78 | <5 | 310 | 5,288 | 9.2 |
| low risk | county income band only | 17 | <5 | 3,342 | 6,807 | 11.8 |
| intermediate risk | rurality by income cells | 79 | 7 | 659 | 11,724 | 9.2 |
| intermediate risk | county income band only | 17 | 7 | 8,879 | 14,291 | 11.2 |
| high risk | rurality by income cells | 79 | 12 | 717 | 11,366 | 8.7 |
| high risk | county income band only | 17 | 13 | 9,352 | 14,824 | 11.3 |
| unknown risk | rurality by income cells | 77 | <5 | 70 | 1,226 | 8.3 |
| unknown risk | county income band only | 17 | <5 | 967 | 1,644 | 11.1 |

## (d) Stage-free clinical block and (e) year as categories

Stage-free: summary stage removed from the clinical block, with risk strata unchanged. Year as categories: logistic regression only, with one indicator per year of diagnosis replacing the linear year and the 2020 indicator. Both reuse the per-step tuned hyperparameters and the first fold seed.

| analysis | stratum | model | comparison | estimate (95% interval) | primary |
|---|---|---|---|---|---|
| stage-free clinical block | all men (pooled) | penalised logistic regression | clinical need (step 0 to 1) | 2.97 (2.64 to 3.34) | 3.01 (2.69 to 3.38) |
| stage-free clinical block | all men (pooled) | penalised logistic regression | social position (step 1 to 2) | 0.62 (0.39 to 0.87) | 0.62 (0.39 to 0.87) |
| stage-free clinical block | all men (pooled) | LightGBM | clinical need (step 0 to 1) | 3.13 (2.80 to 3.48) | 3.18 (2.85 to 3.54) |
| stage-free clinical block | all men (pooled) | LightGBM | social position (step 1 to 2) | 1.02 (0.75 to 1.33) | 0.99 (0.73 to 1.30) |
| stage-free clinical block | low risk | penalised logistic regression | clinical need (step 0 to 1) | 0.14 (0.08 to 0.20) | 0.14 (0.08 to 0.20) |
| stage-free clinical block | low risk | penalised logistic regression | social position (step 1 to 2) | 0.62 (0.32 to 0.94) | 0.62 (0.32 to 0.94) |
| stage-free clinical block | low risk | LightGBM | clinical need (step 0 to 1) | 0.02 (-0.09 to 0.13) | 0.02 (-0.09 to 0.13) |
| stage-free clinical block | low risk | LightGBM | social position (step 1 to 2) | 0.96 (0.67 to 1.28) | 0.96 (0.67 to 1.28) |
| stage-free clinical block | intermediate risk | penalised logistic regression | clinical need (step 0 to 1) | 0.49 (0.41 to 0.57) | 0.49 (0.41 to 0.56) |
| stage-free clinical block | intermediate risk | penalised logistic regression | social position (step 1 to 2) | 0.56 (0.34 to 0.83) | 0.56 (0.35 to 0.83) |
| stage-free clinical block | intermediate risk | LightGBM | clinical need (step 0 to 1) | 0.55 (0.44 to 0.65) | 0.55 (0.44 to 0.65) |
| stage-free clinical block | intermediate risk | LightGBM | social position (step 1 to 2) | 0.93 (0.65 to 1.27) | 0.93 (0.65 to 1.27) |
| stage-free clinical block | high risk | penalised logistic regression | clinical need (step 0 to 1) | 3.42 (3.07 to 3.76) | 3.53 (3.16 to 3.86) |
| stage-free clinical block | high risk | penalised logistic regression | social position (step 1 to 2) | 0.85 (0.59 to 1.14) | 0.86 (0.60 to 1.15) |
| stage-free clinical block | high risk | LightGBM | clinical need (step 0 to 1) | 3.64 (3.27 to 3.99) | 3.72 (3.34 to 4.06) |
| stage-free clinical block | high risk | LightGBM | social position (step 1 to 2) | 1.19 (0.91 to 1.57) | 1.18 (0.90 to 1.56) |
| stage-free clinical block | unknown risk | penalised logistic regression | clinical need (step 0 to 1) | 0.66 (0.41 to 0.92) | 0.65 (0.41 to 0.89) |
| stage-free clinical block | unknown risk | penalised logistic regression | social position (step 1 to 2) | 0.40 (0.06 to 0.80) | 0.42 (0.08 to 0.80) |
| stage-free clinical block | unknown risk | LightGBM | clinical need (step 0 to 1) | 0.59 (0.27 to 0.95) | 0.59 (0.27 to 0.95) |
| stage-free clinical block | unknown risk | LightGBM | social position (step 1 to 2) | 1.37 (0.80 to 2.19) | 1.37 (0.80 to 2.19) |
| year as categories | all men (pooled) | penalised logistic regression | clinical need (step 0 to 1) | 2.98 (2.66 to 3.34) | 3.01 (2.69 to 3.38) |
| year as categories | all men (pooled) | penalised logistic regression | social position (step 1 to 2) | 0.62 (0.39 to 0.86) | 0.62 (0.39 to 0.87) |
| year as categories | low risk | penalised logistic regression | clinical need (step 0 to 1) | 0.15 (0.09 to 0.21) | 0.14 (0.08 to 0.20) |
| year as categories | low risk | penalised logistic regression | social position (step 1 to 2) | 0.60 (0.31 to 0.92) | 0.62 (0.32 to 0.94) |
| year as categories | intermediate risk | penalised logistic regression | clinical need (step 0 to 1) | 0.50 (0.42 to 0.58) | 0.49 (0.41 to 0.56) |
| year as categories | intermediate risk | penalised logistic regression | social position (step 1 to 2) | 0.56 (0.34 to 0.83) | 0.56 (0.35 to 0.83) |
| year as categories | high risk | penalised logistic regression | clinical need (step 0 to 1) | 3.48 (3.12 to 3.82) | 3.53 (3.16 to 3.86) |
| year as categories | high risk | penalised logistic regression | social position (step 1 to 2) | 0.87 (0.61 to 1.16) | 0.86 (0.60 to 1.15) |
| year as categories | unknown risk | penalised logistic regression | clinical need (step 0 to 1) | 0.65 (0.41 to 0.90) | 0.65 (0.41 to 0.89) |
| year as categories | unknown risk | penalised logistic regression | social position (step 1 to 2) | 0.47 (0.11 to 0.89) | 0.42 (0.08 to 0.80) |

## (f) Income concentration index by diagnosis period

Erreygers index of waiting more than 90 days by county income rank within each period; positive values mean delay is concentrated in higher-income counties. It does not separate income from rurality and is not standardised for clinical features.

| stratum | period | Erreygers index (95% interval) |
|---|---|---|
| all men (pooled) | 2010 to 2014 | 0.059 (0.025 to 0.092) |
| all men (pooled) | 2015 to 2019 | 0.037 (0.011 to 0.065) |
| all men (pooled) | 2020 to 2022 | 0.027 (0.003 to 0.061) |
| high risk | 2010 to 2014 | 0.028 (-0.011 to 0.062) |
| high risk | 2015 to 2019 | 0.020 (-0.004 to 0.049) |
| high risk | 2020 to 2022 | 0.015 (-0.013 to 0.056) |
| intermediate risk | 2010 to 2014 | 0.058 (0.023 to 0.099) |
| intermediate risk | 2015 to 2019 | 0.048 (0.019 to 0.080) |
| intermediate risk | 2020 to 2022 | 0.039 (0.015 to 0.067) |
| low risk | 2010 to 2014 | 0.092 (0.053 to 0.136) |
| low risk | 2015 to 2019 | 0.084 (0.052 to 0.121) |
| low risk | 2020 to 2022 | 0.052 (0.017 to 0.092) |
| unknown risk | 2010 to 2014 | 0.060 (0.001 to 0.130) |
| unknown risk | 2015 to 2019 | 0.023 (-0.041 to 0.100) |
| unknown risk | 2020 to 2022 | 0.049 (-0.005 to 0.101) |

### County income quartile distribution by period (% of men in the period)

| period | Q1 (lowest) | Q2 | Q3 | Q4 (highest) | Unknown |
|---|---|---|---|---|---|
| 2010 to 2014 | 9.7 | 30.4 | 33.7 | 26.2 | 0.0 |
| 2015 to 2019 | 7.9 | 20.9 | 37.1 | 34.1 | 0.0 |
| 2020 to 2022 | 5.4 | 19.3 | 34.3 | 41.0 | <5 |

## (g) Long and top-coded intervals

| variable | group | % of men waiting more than 365 days | % of men top-coded (731 days or more) |
|---|---|---|---|
| risk group | intermediate | 1.3 | 0.25 |
| risk group | high | 0.8 | 0.17 |
| risk group | low | 3.0 | 0.80 |
| risk group | unknown | 4.2 | 1.57 |
| rurality | Metro, 1 million or more | 1.7 | 0.40 |
| rurality | Metro, 250,000 to 1 million | 1.4 | 0.35 |
| rurality | Nonmetro, adjacent to metro | 1.1 | 0.23 |
| rurality | Nonmetro, not adjacent to metro | 0.9 | 0.22 |
| rurality | Metro, under 250,000 | 1.5 | 0.41 |
| rurality | Unknown | <5 | <5 |

## (h) One-at-a-time rurality and income profiles (amendment 1.7)

These profiles change rurality or county income alone, holding the other at the reference profile. They create combinations rarely observed in the data, and the two model types conflict; they are not interpreted and are published as amendment 1.7 stated.

### Contrasts (percentage points)

| stratum | contrast | penalised logistic regression | LightGBM | agreement |
|---|---|---|---|---|
| all men (pooled) | rurality only: Nonmetro, not adjacent to metro minus Metro, 1 million or more | -8.7 | 1.7 | opposite directions, at least one model 3 points or more |
| all men (pooled) | county income only: Q1 (lowest) minus Q4 (highest) | -0.9 | -8.7 | same direction, only one model 3 points or more |
| low risk | rurality only: Nonmetro, not adjacent to metro minus Metro, 1 million or more | -7.3 | -4.9 | both models 3 points or more, same direction |
| low risk | county income only: Q1 (lowest) minus Q4 (highest) | -7.0 | -14.8 | both models 3 points or more, same direction |
| intermediate risk | rurality only: Nonmetro, not adjacent to metro minus Metro, 1 million or more | -7.7 | -2.5 | same direction, only one model 3 points or more |
| intermediate risk | county income only: Q1 (lowest) minus Q4 (highest) | -2.0 | -10.9 | same direction, only one model 3 points or more |
| high risk | rurality only: Nonmetro, not adjacent to metro minus Metro, 1 million or more | -9.9 | -3.3 | both models 3 points or more, same direction |
| high risk | county income only: Q1 (lowest) minus Q4 (highest) | 3.4 | -4.8 | opposite directions, at least one model 3 points or more |
| unknown risk | rurality only: Nonmetro, not adjacent to metro minus Metro, 1 million or more | -11.4 | -6.2 | both models 3 points or more, same direction |
| unknown risk | county income only: Q1 (lowest) minus Q4 (highest) | -1.5 | -9.6 | same direction, only one model 3 points or more |

### Standardised percentages

| stratum | model | profile | standardised % |
|---|---|---|---|
| all men (pooled) | penalised logistic regression | rurality only: Metro, 1 million or more (county income held at reference) | 40.8 |
| all men (pooled) | penalised logistic regression | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 36.6 |
| all men (pooled) | penalised logistic regression | rurality only: Metro, under 250,000 (county income held at reference) | 33.3 |
| all men (pooled) | penalised logistic regression | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 32.4 |
| all men (pooled) | penalised logistic regression | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 32.1 |
| all men (pooled) | penalised logistic regression | county income only: Q1 (lowest) (rurality held at reference) | 39.9 |
| all men (pooled) | penalised logistic regression | county income only: Q2 (rurality held at reference) | 40.2 |
| all men (pooled) | penalised logistic regression | county income only: Q3 (rurality held at reference) | 40.5 |
| all men (pooled) | penalised logistic regression | county income only: Q4 (highest) (rurality held at reference) | 40.8 |
| all men (pooled) | LightGBM | rurality only: Metro, 1 million or more (county income held at reference) | 41.3 |
| all men (pooled) | LightGBM | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 37.4 |
| all men (pooled) | LightGBM | rurality only: Metro, under 250,000 (county income held at reference) | 37.4 |
| all men (pooled) | LightGBM | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 38.0 |
| all men (pooled) | LightGBM | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 43.0 |
| all men (pooled) | LightGBM | county income only: Q1 (lowest) (rurality held at reference) | 32.6 |
| all men (pooled) | LightGBM | county income only: Q2 (rurality held at reference) | 34.6 |
| all men (pooled) | LightGBM | county income only: Q3 (rurality held at reference) | 40.4 |
| all men (pooled) | LightGBM | county income only: Q4 (highest) (rurality held at reference) | 41.3 |
| low risk | penalised logistic regression | rurality only: Metro, 1 million or more (county income held at reference) | 51.3 |
| low risk | penalised logistic regression | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 48.9 |
| low risk | penalised logistic regression | rurality only: Metro, under 250,000 (county income held at reference) | 46.1 |
| low risk | penalised logistic regression | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 42.8 |
| low risk | penalised logistic regression | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 44.0 |
| low risk | penalised logistic regression | county income only: Q1 (lowest) (rurality held at reference) | 44.6 |
| low risk | penalised logistic regression | county income only: Q2 (rurality held at reference) | 46.9 |
| low risk | penalised logistic regression | county income only: Q3 (rurality held at reference) | 49.3 |
| low risk | penalised logistic regression | county income only: Q4 (highest) (rurality held at reference) | 51.6 |
| low risk | LightGBM | rurality only: Metro, 1 million or more (county income held at reference) | 52.6 |
| low risk | LightGBM | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 50.0 |
| low risk | LightGBM | rurality only: Metro, under 250,000 (county income held at reference) | 50.0 |
| low risk | LightGBM | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 48.7 |
| low risk | LightGBM | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 47.7 |
| low risk | LightGBM | county income only: Q1 (lowest) (rurality held at reference) | 37.8 |
| low risk | LightGBM | county income only: Q2 (rurality held at reference) | 41.5 |
| low risk | LightGBM | county income only: Q3 (rurality held at reference) | 47.7 |
| low risk | LightGBM | county income only: Q4 (highest) (rurality held at reference) | 52.6 |
| intermediate risk | penalised logistic regression | rurality only: Metro, 1 million or more (county income held at reference) | 44.2 |
| intermediate risk | penalised logistic regression | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 40.2 |
| intermediate risk | penalised logistic regression | rurality only: Metro, under 250,000 (county income held at reference) | 36.7 |
| intermediate risk | penalised logistic regression | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 36.0 |
| intermediate risk | penalised logistic regression | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 36.6 |
| intermediate risk | penalised logistic regression | county income only: Q1 (lowest) (rurality held at reference) | 42.3 |
| intermediate risk | penalised logistic regression | county income only: Q2 (rurality held at reference) | 43.0 |
| intermediate risk | penalised logistic regression | county income only: Q3 (rurality held at reference) | 43.6 |
| intermediate risk | penalised logistic regression | county income only: Q4 (highest) (rurality held at reference) | 44.3 |
| intermediate risk | LightGBM | rurality only: Metro, 1 million or more (county income held at reference) | 44.4 |
| intermediate risk | LightGBM | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 40.9 |
| intermediate risk | LightGBM | rurality only: Metro, under 250,000 (county income held at reference) | 43.0 |
| intermediate risk | LightGBM | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 40.9 |
| intermediate risk | LightGBM | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 41.9 |
| intermediate risk | LightGBM | county income only: Q1 (lowest) (rurality held at reference) | 33.5 |
| intermediate risk | LightGBM | county income only: Q2 (rurality held at reference) | 37.0 |
| intermediate risk | LightGBM | county income only: Q3 (rurality held at reference) | 43.5 |
| intermediate risk | LightGBM | county income only: Q4 (highest) (rurality held at reference) | 44.4 |
| high risk | penalised logistic regression | rurality only: Metro, 1 million or more (county income held at reference) | 32.7 |
| high risk | penalised logistic regression | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 27.2 |
| high risk | penalised logistic regression | rurality only: Metro, under 250,000 (county income held at reference) | 24.5 |
| high risk | penalised logistic regression | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 24.2 |
| high risk | penalised logistic regression | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 22.9 |
| high risk | penalised logistic regression | county income only: Q1 (lowest) (rurality held at reference) | 35.9 |
| high risk | penalised logistic regression | county income only: Q2 (rurality held at reference) | 34.8 |
| high risk | penalised logistic regression | county income only: Q3 (rurality held at reference) | 33.7 |
| high risk | penalised logistic regression | county income only: Q4 (highest) (rurality held at reference) | 32.6 |
| high risk | LightGBM | rurality only: Metro, 1 million or more (county income held at reference) | 32.9 |
| high risk | LightGBM | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 27.8 |
| high risk | LightGBM | rurality only: Metro, under 250,000 (county income held at reference) | 28.0 |
| high risk | LightGBM | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 29.0 |
| high risk | LightGBM | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 29.6 |
| high risk | LightGBM | county income only: Q1 (lowest) (rurality held at reference) | 28.1 |
| high risk | LightGBM | county income only: Q2 (rurality held at reference) | 29.2 |
| high risk | LightGBM | county income only: Q3 (rurality held at reference) | 33.7 |
| high risk | LightGBM | county income only: Q4 (highest) (rurality held at reference) | 32.9 |
| unknown risk | penalised logistic regression | rurality only: Metro, 1 million or more (county income held at reference) | 42.3 |
| unknown risk | penalised logistic regression | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 41.2 |
| unknown risk | penalised logistic regression | rurality only: Metro, under 250,000 (county income held at reference) | 34.4 |
| unknown risk | penalised logistic regression | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 36.2 |
| unknown risk | penalised logistic regression | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 30.8 |
| unknown risk | penalised logistic regression | county income only: Q1 (lowest) (rurality held at reference) | 40.9 |
| unknown risk | penalised logistic regression | county income only: Q2 (rurality held at reference) | 41.4 |
| unknown risk | penalised logistic regression | county income only: Q3 (rurality held at reference) | 41.9 |
| unknown risk | penalised logistic regression | county income only: Q4 (highest) (rurality held at reference) | 42.3 |
| unknown risk | LightGBM | rurality only: Metro, 1 million or more (county income held at reference) | 42.1 |
| unknown risk | LightGBM | rurality only: Metro, 250,000 to 1 million (county income held at reference) | 42.0 |
| unknown risk | LightGBM | rurality only: Metro, under 250,000 (county income held at reference) | 35.0 |
| unknown risk | LightGBM | rurality only: Nonmetro, adjacent to metro (county income held at reference) | 41.5 |
| unknown risk | LightGBM | rurality only: Nonmetro, not adjacent to metro (county income held at reference) | 36.0 |
| unknown risk | LightGBM | county income only: Q1 (lowest) (rurality held at reference) | 32.5 |
| unknown risk | LightGBM | county income only: Q2 (rurality held at reference) | 32.7 |
| unknown risk | LightGBM | county income only: Q3 (rurality held at reference) | 42.5 |
| unknown risk | LightGBM | county income only: Q4 (highest) (rurality held at reference) | 42.1 |

## Clinical need increment when radiotherapy patients are excluded

The interval ends at the first treatment of any kind, which for men having radiotherapy can be hormone therapy. This compares the clinical need increment in the primary cohort with the prostatectomy-without-radiotherapy scenario (A8).

| stratum | model | clinical need added, primary cohort | clinical need added, prostatectomy without radiotherapy only |
|---|---|---|---|
| all men (pooled) | penalised logistic regression | 3.01 (2.69 to 3.38) | 1.66 (1.49 to 1.81) |
| all men (pooled) | LightGBM | 3.18 (2.85 to 3.54) | 1.66 (1.49 to 1.81) |
| low risk | penalised logistic regression | 0.14 (0.08 to 0.20) | 0.05 (-0.01 to 0.12) |
| low risk | LightGBM | 0.02 (-0.09 to 0.13) | -0.15 (-0.28 to -0.02) |
| intermediate risk | penalised logistic regression | 0.49 (0.41 to 0.56) | 0.33 (0.21 to 0.44) |
| intermediate risk | LightGBM | 0.55 (0.44 to 0.65) | 0.06 (-0.06 to 0.17) |
| high risk | penalised logistic regression | 3.53 (3.16 to 3.86) | 2.20 (1.96 to 2.42) |
| high risk | LightGBM | 3.72 (3.34 to 4.06) | 2.13 (1.88 to 2.32) |
| unknown risk | penalised logistic regression | 0.65 (0.41 to 0.89) | 0.91 (0.57 to 1.25) |
| unknown risk | LightGBM | 0.59 (0.27 to 0.95) | 0.62 (0.12 to 1.16) |

## (i) Share of crude excess waiting days from top-coded intervals

Tabulated after the second internal review from existing tables (not part of amendment 1.9). Each top-coded interval counts as 731 days, contributing 641 days beyond the 90-day threshold; the share is of all crude excess waiting days in the group. All men.

| rurality | % of crude excess waiting days from top-coded intervals |
|---|---|
| Metro, 1 million or more | 8.4 |
| Metro, 250,000 to 1 million | 8.6 |
| Metro, under 250,000 | 10.9 |
| Nonmetro, adjacent to metro | 6.8 |
| Nonmetro, not adjacent to metro | 7.1 |
| Unknown | <5 |
