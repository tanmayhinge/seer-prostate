# Phase 3. Cohort construction

Generated 2026-09-13 10:59 UTC by `scripts/run_phase3_cohort.py` at git revision `5954e76` (protocol v1.0). Definitions: `PROTOCOL.md` sections 3 to 5 and `config/analysis.yaml`. Every label in the export is mapped explicitly; an unmapped label stops the run.

## Summary

- Primary cohort: **330,827** men diagnosed 2010 to 2022 whose first course included radical prostatectomy or radiotherapy, with a recorded interval above 0 days.

- 131,326 (39.7% of the cohort) waited more than 90 days, the Australian optimal care pathway benchmark (a lower percentage is better).

- Among 355,581 treated men before the interval steps, 17,001 have no recorded interval and 7,753 have an interval of 0 days. Table 1b compares these groups with the included men (selection, PROTOCOL.md A7).

## Inclusion flow (primary cohort)

Percentages are of the men remaining at the previous step.

| step | remaining | excluded | % of previous step excluded |
|---|---|---|---|
| all records | 793,214 | 0 | n/a |
| first primary | 710,343 | 82,871 | 10.4 |
| localised or regional stage | 608,441 | 101,902 | 14.3 |
| not death certificate or autopsy only | 608,375 | 66 | 0.0 |
| age 40 or over | 608,133 | 242 | 0.0 |
| diagnosed 2010 to 2022 | 557,683 | 50,450 | 8.3 |
| first course includes prostatectomy or radiotherapy | 355,581 | 202,102 | 36.2 |
| interval recorded or top-coded | 338,580 | 17,001 | 4.8 |
| interval above 0 days | 330,827 | 7,753 | 2.3 |

## Inclusion flow with 2023 diagnoses and 0-day intervals retained (sensitivity cohort)

This flow uses the Phase 0 preview definitions and reproduces its counts exactly at every shared step.

| step | remaining | excluded | % of previous step excluded |
|---|---|---|---|
| all records | 793,214 | 0 | n/a |
| first primary | 710,343 | 82,871 | 10.4 |
| localised or regional stage | 608,441 | 101,902 | 14.3 |
| not death certificate or autopsy only | 608,375 | 66 | 0.0 |
| age 40 or over | 608,133 | 242 | 0.0 |
| diagnosed 2010 to 2023 | 608,133 | 0 | 0.0 |
| first course includes prostatectomy or radiotherapy | 384,394 | 223,739 | 36.8 |
| interval recorded or top-coded | 366,838 | 17,556 | 4.6 |
| interval above 0 days (not applied) | 366,838 | 0 | 0.0 |

## Table 1. Characteristics of the primary cohort by county rurality

Cells are n (% of the column's men), except days, which are median (interquartile range). Rurality is the county Rural-Urban Continuum Code at diagnosis. Counts of 1 to 4 are shown as <5, and a second cell is hidden wherever a row or column total would reveal them (SEER Research Data Use Agreement).

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

## Table 1b. Treated men by interval status

Men meeting cohort steps 1 to 6 (n = 355,581). Cells are n (% of the column's men). A difference in social composition between the included and missing-interval columns would indicate that the timeliness analysis is selected on social position; PROTOCOL.md A7 bounds this. Counts of 1 to 4 are shown as <5, and a second cell is hidden wherever a row or column total would reveal them (SEER Research Data Use Agreement).

| characteristic | level | Overall | Interval included | 0 days | Missing interval |
|---|---|---|---|---|---|
| Men, n |  | 355,581 | 330,827 | 7,753 | 17,001 |
| Rurality | Metro, 1 million or more | 210,372 (59.2%) | 194,681 (58.8%) | 4,388 (56.6%) | 11,303 (66.5%) |
| Rurality | Metro, 250,000 to 1 million | 77,524 (21.8%) | 72,150 (21.8%) | 1,737 (22.4%) | 3,637 (21.4%) |
| Rurality | Metro, under 250,000 | 27,705 (7.8%) | 26,092 (7.9%) | 652 (8.4%) | 961 (5.7%) |
| Rurality | Nonmetro, adjacent to metro | 24,621 (6.9%) | 23,360 (7.1%) | 567 (7.3%) | 694 (4.1%) |
| Rurality | Nonmetro, not adjacent to metro | 15,188 (4.3%) | 14,385 (4.3%) | 404 (5.2%) | 399 (2.3%) |
| Rurality | Unknown | 171 (0.0%) | 159 (0.0%) | 5 (0.1%) | 7 (0.0%) |
| Age at diagnosis | 40-44 years | 1,547 (0.4%) | 1,480 (0.4%) | 32 (0.4%) | 35 (0.2%) |
| Age at diagnosis | 45-49 years | 7,297 (2.1%) | 6,921 (2.1%) | 128 (1.7%) | 248 (1.5%) |
| Age at diagnosis | 50-54 years | 25,787 (7.3%) | 24,293 (7.3%) | 477 (6.2%) | 1,017 (6.0%) |
| Age at diagnosis | 55-59 years | 52,043 (14.6%) | 49,078 (14.8%) | 894 (11.5%) | 2,071 (12.2%) |
| Age at diagnosis | 60-64 years | 75,120 (21.1%) | 70,459 (21.3%) | 1,368 (17.6%) | 3,293 (19.4%) |
| Age at diagnosis | 65-69 years | 89,835 (25.3%) | 83,831 (25.3%) | 1,769 (22.8%) | 4,235 (24.9%) |
| Age at diagnosis | 70-74 years | 61,150 (17.2%) | 56,371 (17.0%) | 1,473 (19.0%) | 3,306 (19.4%) |
| Age at diagnosis | 75-79 years | 31,004 (8.7%) | 28,114 (8.5%) | 947 (12.2%) | 1,943 (11.4%) |
| Age at diagnosis | 80-84 years | 9,834 (2.8%) | 8,636 (2.6%) | 491 (6.3%) | 707 (4.2%) |
| Age at diagnosis | 85-89 years | 1,792 (0.5%) | 1,516 (0.5%) | 147 (1.9%) | 129 (0.8%) |
| Age at diagnosis | 90+ years | 172 (0.0%) | 128 (0.0%) | 27 (0.3%) | 17 (0.1%) |
| Year of diagnosis | 2010 to 2014 | 138,812 (39.0%) | 126,503 (38.2%) | 2,967 (38.3%) | 9,342 (54.9%) |
| Year of diagnosis | 2015 to 2019 | 131,356 (36.9%) | 122,936 (37.2%) | 3,056 (39.4%) | 5,364 (31.6%) |
| Year of diagnosis | 2020 to 2022 | 85,413 (24.0%) | 81,388 (24.6%) | 1,730 (22.3%) | 2,295 (13.5%) |
| Marital status | Married (including common law) | 249,351 (70.1%) | 232,525 (70.3%) | 5,321 (68.6%) | 11,505 (67.7%) |
| Marital status | Single (never married) | 39,507 (11.1%) | 36,703 (11.1%) | 881 (11.4%) | 1,923 (11.3%) |
| Marital status | Divorced | 23,631 (6.6%) | 22,023 (6.7%) | 565 (7.3%) | 1,043 (6.1%) |
| Marital status | Separated | 2,853 (0.8%) | 2,630 (0.8%) | 67 (0.9%) | 156 (0.9%) |
| Marital status | Widowed | 10,885 (3.1%) | 9,905 (3.0%) | 341 (4.4%) | 639 (3.8%) |
| Marital status | Unmarried or Domestic Partner | 1,447 (0.4%) | 1,369 (0.4%) | 24 (0.3%) | 54 (0.3%) |
| Marital status | Unknown | 27,907 (7.8%) | 25,672 (7.8%) | 554 (7.1%) | 1,681 (9.9%) |
| County median household income (quartile of 16 bands) | Q1 (lowest) | 27,790 (7.8%) | 26,436 (8.0%) | <5 | <5 |
| County median household income (quartile of 16 bands) | Q2 | 86,090 (24.2%) | 79,804 (24.1%) | 1,886 (24.3%) | 4,400 (25.9%) |
| County median household income (quartile of 16 bands) | Q3 | 125,843 (35.4%) | 116,211 (35.1%) | 2,747 (35.4%) | 6,885 (40.5%) |
| County median household income (quartile of 16 bands) | Q4 (highest) | 115,822 (32.6%) | 108,348 (32.8%) | 2,323 (30.0%) | 5,151 (30.3%) |
| County median household income (quartile of 16 bands) | Unknown | 36 (0.0%) | 28 (0.0%) | <5 | <5 |
| Risk group | low | 60,793 (17.1%) | 57,495 (17.4%) | 863 (11.1%) | 2,435 (14.3%) |
| Risk group | intermediate | 134,413 (37.8%) | 127,622 (38.6%) | 1,766 (22.8%) | 5,025 (29.6%) |
| Risk group | high | 141,384 (39.8%) | 130,893 (39.6%) | 3,434 (44.3%) | 7,057 (41.5%) |
| Risk group | unknown | 18,991 (5.3%) | 14,817 (4.5%) | 1,690 (21.8%) | 2,484 (14.6%) |
| Summary stage | Localised | 276,161 (77.7%) | 256,475 (77.5%) | 6,025 (77.7%) | 13,661 (80.4%) |
| Summary stage | Regional, direct extension | 66,083 (18.6%) | 61,984 (18.7%) | 1,301 (16.8%) | 2,798 (16.5%) |
| Summary stage | Regional, lymph nodes | 13,337 (3.8%) | 12,368 (3.7%) | 427 (5.5%) | 542 (3.2%) |
| Clinical Gleason score | 6 or less | 87,024 (24.5%) | 81,630 (24.7%) | 1,406 (18.1%) | 3,988 (23.5%) |
| Clinical Gleason score | 7 | 181,097 (50.9%) | 171,345 (51.8%) | 2,688 (34.7%) | 7,064 (41.6%) |
| Clinical Gleason score | 8 to 10 | 79,786 (22.4%) | 73,447 (22.2%) | 2,164 (27.9%) | 4,175 (24.6%) |
| Clinical Gleason score | Unknown | 7,674 (2.2%) | 4,405 (1.3%) | 1,495 (19.3%) | 1,774 (10.4%) |
| PSA (ng/ml) | below 10 | 236,726 (66.6%) | 223,700 (67.6%) | 3,954 (51.0%) | 9,072 (53.4%) |
| PSA (ng/ml) | 10 to 20 | 62,849 (17.7%) | 58,930 (17.8%) | 984 (12.7%) | 2,935 (17.3%) |
| PSA (ng/ml) | above 20 | 31,563 (8.9%) | 28,789 (8.7%) | 944 (12.2%) | 1,830 (10.8%) |
| PSA (ng/ml) | Unknown | 24,443 (6.9%) | 19,408 (5.9%) | 1,871 (24.1%) | 3,164 (18.6%) |
| First-course treatment | Radical prostatectomy | 170,715 (48.0%) | 159,580 (48.2%) | 3,746 (48.3%) | 7,389 (43.5%) |
| First-course treatment | Radiotherapy | 171,287 (48.2%) | 158,473 (47.9%) | 3,672 (47.4%) | 9,142 (53.8%) |
| First-course treatment | Both | 13,579 (3.8%) | 12,774 (3.9%) | 335 (4.3%) | 470 (2.8%) |

## Not yet done

No outcome model has been fitted. Phase 4 (descriptive timeliness results and the ordered-step models) follows the protocol without deviation unless an amendment is logged.
