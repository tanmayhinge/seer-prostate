# Phase 4, part 2. How much social position adds to predicting delay

Generated 2026-09-13 11:57 UTC by `scripts/run_phase4_models_report.py` at git revision `66a99f1`. Definitions: `PROTOCOL.md` sections 5 to 7 (A2 to A4).

## What is measured

- Outcome: first recorded treatment more than 90 days after diagnosis.

- Each model is built in ordered steps: step 0 year of diagnosis only; step 1 adds clinical need; step 2 adds social position (marital status, rurality, county income); step 3 adds treatment type.

- **Skill** is the percentage reduction in out-of-fold log-loss compared with the step 0 model (0 means no better than year alone; higher is better). The value added by a block is the skill it adds, in percentage points.

- Intervals are 95% cluster-bootstrap intervals (500 resamples over rurality by county income cells).

- These are associations measured as predictive gains. They are not causal effects.

## How well delay can be predicted at all

Across strata and models, AUC at step 2 ranged from 0.592 to 0.663 (0.5 is chance, 1 is perfect) and log-loss skill from 0.76% to 4.90% (0 means no better than year of diagnosis alone). Most of the variation in which men wait more than 90 days is not explained by the recorded clinical and social variables. The value added by social position should be read against this low ceiling.

## Headline: value added at each step

Skill and the value added by each block are in percentage points of log-loss reduction, with 95% intervals. "Social position as % of step 2 skill" is the share of the step 2 model's total skill contributed by the social block.

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

## Did gradient boosting beat penalised regression?

LightGBM had higher out-of-fold skill than penalised logistic regression at step 2 in every stratum.

| stratum | logistic regression skill at step 2 | LightGBM skill at step 2 | difference (LightGBM minus logistic) |
|---|---|---|---|
| all men (pooled) | 3.63 | 4.17 | 0.54 |
| low risk | 0.76 | 0.99 | 0.23 |
| intermediate risk | 1.06 | 1.48 | 0.42 |
| high risk | 4.39 | 4.90 | 0.51 |
| unknown risk | 1.07 | 1.96 | 0.90 |

## Performance at every step

AUC: 0.5 is chance, higher is better. Calibration intercept: 0 is ideal. Calibration slope: 1 is ideal; below 1 means predictions are too extreme.

LightGBM: calibration slopes at step 2 from 0.88 to 1.03. penalised logistic regression: calibration slopes at step 2 from 0.98 to 1.00. A slope below 1 means predicted risks are more extreme than observed risks.

| stratum | model | step | log-loss skill % | Brier skill % | AUC | calibration intercept | calibration slope |
|---|---|---|---|---|---|---|---|
| all men (pooled) | penalised logistic regression | 0 | 0.00 | 0.00 | 0.558 | -0.000 | 1.001 |
| all men (pooled) | penalised logistic regression | 1 | 3.01 | 3.89 | 0.628 | -0.000 | 1.002 |
| all men (pooled) | penalised logistic regression | 2 | 3.63 | 4.66 | 0.638 | -0.000 | 1.000 |
| all men (pooled) | penalised logistic regression | 3 | 3.67 | 4.71 | 0.638 | -0.000 | 1.000 |
| all men (pooled) | LightGBM | 0 | 0.00 | 0.00 | 0.561 | -0.000 | 0.997 |
| all men (pooled) | LightGBM | 1 | 3.18 | 4.09 | 0.633 | -0.000 | 1.004 |
| all men (pooled) | LightGBM | 2 | 4.17 | 5.34 | 0.648 | -0.000 | 1.030 |
| all men (pooled) | LightGBM | 3 | 4.46 | 5.70 | 0.653 | -0.000 | 1.041 |
| low risk | penalised logistic regression | 0 | 0.00 | 0.00 | 0.566 | 0.000 | 1.005 |
| low risk | penalised logistic regression | 1 | 0.14 | 0.19 | 0.573 | -0.000 | 0.998 |
| low risk | penalised logistic regression | 2 | 0.76 | 1.03 | 0.592 | 0.000 | 0.988 |
| low risk | penalised logistic regression | 3 | 0.97 | 1.31 | 0.597 | 0.000 | 0.989 |
| low risk | LightGBM | 0 | 0.00 | 0.00 | 0.570 | -0.000 | 0.989 |
| low risk | LightGBM | 1 | 0.02 | 0.04 | 0.577 | -0.000 | 0.883 |
| low risk | LightGBM | 2 | 0.99 | 1.35 | 0.604 | -0.000 | 0.937 |
| low risk | LightGBM | 3 | 1.35 | 1.84 | 0.611 | -0.000 | 0.957 |
| intermediate risk | penalised logistic regression | 0 | 0.00 | 0.00 | 0.581 | 0.000 | 1.003 |
| intermediate risk | penalised logistic regression | 1 | 0.49 | 0.66 | 0.594 | -0.000 | 1.006 |
| intermediate risk | penalised logistic regression | 2 | 1.06 | 1.40 | 0.605 | -0.000 | 1.001 |
| intermediate risk | penalised logistic regression | 3 | 1.09 | 1.45 | 0.606 | -0.000 | 1.001 |
| intermediate risk | LightGBM | 0 | 0.00 | 0.00 | 0.582 | 0.000 | 0.993 |
| intermediate risk | LightGBM | 1 | 0.55 | 0.74 | 0.596 | 0.000 | 0.966 |
| intermediate risk | LightGBM | 2 | 1.48 | 1.96 | 0.615 | -0.000 | 1.008 |
| intermediate risk | LightGBM | 3 | 1.66 | 2.20 | 0.619 | -0.000 | 1.022 |
| high risk | penalised logistic regression | 0 | 0.00 | 0.00 | 0.564 | -0.000 | 1.004 |
| high risk | penalised logistic regression | 1 | 3.53 | 4.41 | 0.641 | -0.000 | 1.002 |
| high risk | penalised logistic regression | 2 | 4.39 | 5.42 | 0.654 | 0.000 | 1.001 |
| high risk | penalised logistic regression | 3 | 4.63 | 5.71 | 0.657 | 0.000 | 1.001 |
| high risk | LightGBM | 0 | 0.00 | 0.00 | 0.565 | -0.000 | 0.993 |
| high risk | LightGBM | 1 | 3.72 | 4.63 | 0.645 | -0.000 | 0.992 |
| high risk | LightGBM | 2 | 4.90 | 6.04 | 0.663 | -0.000 | 1.023 |
| high risk | LightGBM | 3 | 5.28 | 6.49 | 0.668 | -0.000 | 1.033 |
| unknown risk | penalised logistic regression | 0 | 0.00 | 0.00 | 0.584 | -0.000 | 1.019 |
| unknown risk | penalised logistic regression | 1 | 0.65 | 0.89 | 0.601 | -0.000 | 1.022 |
| unknown risk | penalised logistic regression | 2 | 1.07 | 1.43 | 0.610 | 0.000 | 0.982 |
| unknown risk | penalised logistic regression | 3 | 1.41 | 1.86 | 0.616 | 0.000 | 0.980 |
| unknown risk | LightGBM | 0 | 0.00 | 0.00 | 0.585 | -0.000 | 0.946 |
| unknown risk | LightGBM | 1 | 0.59 | 0.83 | 0.601 | -0.001 | 0.850 |
| unknown risk | LightGBM | 2 | 1.96 | 2.64 | 0.629 | -0.000 | 0.882 |
| unknown risk | LightGBM | 3 | 2.67 | 3.54 | 0.640 | -0.000 | 0.901 |

## Which social variable carries the gain

Skill lost when one social variable is removed from the step 2 model and the model is refitted. Rurality and county income are strongly correlated in this cohort, so removing one lets the other partly stand in for it; a small loss does not mean a variable is unrelated to delay.

| stratum | model | variable removed | skill lost when removed (points) |
|---|---|---|---|
| all men (pooled) | penalised logistic regression | marital status | 0.22 |
| all men (pooled) | penalised logistic regression | rurality | 0.23 |
| all men (pooled) | penalised logistic regression | county income | 0.00 |
| all men (pooled) | LightGBM | marital status | 0.27 |
| all men (pooled) | LightGBM | rurality | 0.23 |
| all men (pooled) | LightGBM | county income | 0.26 |
| low risk | penalised logistic regression | marital status | 0.05 |
| low risk | penalised logistic regression | rurality | 0.13 |
| low risk | penalised logistic regression | county income | 0.09 |
| low risk | LightGBM | marital status | 0.05 |
| low risk | LightGBM | rurality | 0.10 |
| low risk | LightGBM | county income | 0.38 |
| intermediate risk | penalised logistic regression | marital status | 0.18 |
| intermediate risk | penalised logistic regression | rurality | 0.19 |
| intermediate risk | penalised logistic regression | county income | 0.01 |
| intermediate risk | LightGBM | marital status | 0.21 |
| intermediate risk | LightGBM | rurality | 0.22 |
| intermediate risk | LightGBM | county income | 0.29 |
| high risk | penalised logistic regression | marital status | 0.42 |
| high risk | penalised logistic regression | rurality | 0.37 |
| high risk | penalised logistic regression | county income | 0.02 |
| high risk | LightGBM | marital status | 0.45 |
| high risk | LightGBM | rurality | 0.36 |
| high risk | LightGBM | county income | 0.26 |
| unknown risk | penalised logistic regression | marital status | 0.16 |
| unknown risk | penalised logistic regression | rurality | 0.12 |
| unknown risk | penalised logistic regression | county income | -0.03 |
| unknown risk | LightGBM | marital status | 0.41 |
| unknown risk | LightGBM | rurality | 0.16 |
| unknown risk | LightGBM | county income | 0.59 |

## Tuning

Penalised logistic regression chose C = 0.01, an edge of the pre-specified grid [0.01, 0.1, 1.0, 10.0], in 5 of 5 strata; the best penalty may lie outside the grid. This is reported as a limitation rather than changed after the fact.

| stratum | model | max_iter | C | seconds | learning_rate | n_estimators | num_leaves | min_child_samples |
|---|---|---|---|---|---|---|---|---|
| all men (pooled) | penalised logistic regression | 2000 | 0.01 | 1.9 | n/a | n/a | n/a | n/a |
| all men (pooled) | LightGBM | n/a | n/a | 41.6 | 0.05 | 200 | 15 | 200 |
| low risk | penalised logistic regression | 2000 | 0.01 | 1.3 | n/a | n/a | n/a | n/a |
| low risk | LightGBM | n/a | n/a | 40.7 | 0.05 | 200 | 15 | 200 |
| intermediate risk | penalised logistic regression | 2000 | 0.01 | 1.4 | n/a | n/a | n/a | n/a |
| intermediate risk | LightGBM | n/a | n/a | 40.5 | 0.05 | 200 | 15 | 200 |
| high risk | penalised logistic regression | 2000 | 0.01 | 1.9 | n/a | n/a | n/a | n/a |
| high risk | LightGBM | n/a | n/a | 42.4 | 0.05 | 200 | 15 | 200 |
| unknown risk | penalised logistic regression | 2000 | 0.01 | 0.4 | n/a | n/a | n/a | n/a |
| unknown risk | LightGBM | n/a | n/a | 30.7 | 0.05 | 200 | 15 | 200 |
