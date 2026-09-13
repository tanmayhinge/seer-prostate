# Phase 4, part 1. Descriptive timeliness results

Generated 2026-09-13 11:49 UTC by `scripts/run_phase4_descriptive.py` at git revision `66a99f1`. Definitions: `PROTOCOL.md` (A1). These are crude descriptive figures: nothing is adjusted, and no difference here is a tested result.

## Summary

- Primary cohort: 330,827 men. 131,326 (39.7%) waited more than 90 days from diagnosis to first recorded treatment, the Australian optimal care pathway benchmark (a lower percentage is better).

- Median 77 days; 90th percentile 174 days.

## How to read the tables

- "Waited over 90 days" counts men whose first recorded treatment came more than 90 days after diagnosis, including the top-coded group (731 days or more).

- Percentages use the men in that row as the denominator.

- Median and 90th percentile days treat top-coded intervals as 731, so the 90th percentile can be a lower bound.

- Table D1 shows exact numbers of men. Tables D2 to D5 round the number of men to the nearest 10 and do not show delayed counts, so that small groups cannot be recovered by subtraction.

- Statistics based on 1 to 4 men are shown as <5. A percentage is also hidden when 1 to 4 men in that row did, or did not, wait more than 90 days (SEER Research Data Use Agreement).

## Tables

### D1. By risk group

| risk group | men | % waited over 90 days | median days | 90th percentile days |
|---|---|---|---|---|
| low | 57,495 | 47.9 | 88.0 | 210.0 |
| intermediate | 127,622 | 42.8 | 82.0 | 176.0 |
| high | 130,893 | 32.8 | 70.0 | 150.0 |
| unknown | 14,817 | 42.1 | 79.0 | 212.0 |

### D2. By risk group and county rurality

| risk group | rurality | men | % waited over 90 days | median days | 90th percentile days |
|---|---|---|---|---|---|
| low | Metro, 1 million or more | 34,260 | 50.7 | 91.0 | 217.0 |
| low | Metro, 250,000 to 1 million | 11,930 | 47.0 | 86.0 | 211.0 |
| low | Metro, under 250,000 | 4,780 | 42.3 | 82.0 | 198.2 |
| low | Nonmetro, adjacent to metro | 3,990 | 39.0 | 77.0 | 187.0 |
| low | Nonmetro, not adjacent to metro | 2,510 | 39.0 | 76.0 | 177.0 |
| low | Unknown | 20 | 34.8 | 81.0 | 122.8 |
| intermediate | Metro, 1 million or more | 75,190 | 45.5 | 84.0 | 182.0 |
| intermediate | Metro, 250,000 to 1 million | 28,140 | 41.1 | 79.0 | 172.0 |
| intermediate | Metro, under 250,000 | 10,070 | 36.7 | 75.0 | 165.0 |
| intermediate | Nonmetro, adjacent to metro | 8,830 | 36.1 | 74.0 | 161.0 |
| intermediate | Nonmetro, not adjacent to metro | 5,360 | 36.1 | 71.0 | 160.0 |
| intermediate | Unknown | 40 | 42.5 | 71.0 | 200.5 |
| high | Metro, 1 million or more | 75,760 | 35.7 | 73.0 | 157.0 |
| high | Metro, 250,000 to 1 million | 29,320 | 30.0 | 67.0 | 142.0 |
| high | Metro, under 250,000 | 10,130 | 27.9 | 65.0 | 140.0 |
| high | Nonmetro, adjacent to metro | 9,590 | 27.7 | 63.0 | 134.5 |
| high | Nonmetro, not adjacent to metro | 6,010 | 26.0 | 62.0 | 133.0 |
| high | Unknown | 90 | 28.4 | 61.5 | 141.5 |
| unknown | Metro, 1 million or more | 9,460 | 44.2 | 82.0 | 224.0 |
| unknown | Metro, 250,000 to 1 million | 2,770 | 42.2 | 80.0 | 203.0 |
| unknown | Metro, under 250,000 | 1,120 | 35.0 | 70.0 | 179.0 |
| unknown | Nonmetro, adjacent to metro | 950 | 36.5 | 72.0 | 174.2 |
| unknown | Nonmetro, not adjacent to metro | 510 | 29.6 | 63.5 | 162.0 |
| unknown | Unknown | 10 | <5 | 77.0 | 212.7 |

### D3. By risk group and county income quartile

| risk group | county income quartile | men | % waited over 90 days | median days | 90th percentile days |
|---|---|---|---|---|---|
| low | Q1 (lowest) | 5,420 | 37.6 | 76.0 | 182.0 |
| low | Q2 | 15,540 | 44.1 | 83.0 | 196.0 |
| low | Q3 | 19,460 | 50.4 | 91.0 | 216.0 |
| low | Q4 (highest) | 17,070 | 51.9 | 93.0 | 225.0 |
| low | Unknown | <5 | <5 | <5 | <5 |
| intermediate | Q1 (lowest) | 9,930 | 33.5 | 70.0 | 155.0 |
| intermediate | Q2 | 30,100 | 39.3 | 77.0 | 168.0 |
| intermediate | Q3 | 44,260 | 44.9 | 84.0 | 184.0 |
| intermediate | Q4 (highest) | 43,330 | 45.2 | 84.0 | 179.0 |
| intermediate | Unknown | 10 | <5 | 71.0 | 372.2 |
| high | Q1 (lowest) | 9,920 | 26.7 | 63.0 | 134.8 |
| high | Q2 | 30,420 | 30.5 | 67.0 | 145.0 |
| high | Q3 | 46,890 | 35.0 | 71.0 | 156.0 |
| high | Q4 (highest) | 43,650 | 33.4 | 70.0 | 151.0 |
| high | Unknown | 10 | 38.5 | 82.0 | 146.2 |
| unknown | Q1 (lowest) | 1,160 | 31.4 | 65.0 | 175.7 |
| unknown | Q2 | 3,740 | 39.3 | 76.0 | 207.0 |
| unknown | Q3 | 5,610 | 44.6 | 83.0 | 222.5 |
| unknown | Q4 (highest) | 4,300 | 44.4 | 83.0 | 210.0 |
| unknown | Unknown | <5 | <5 | <5 | <5 |

### D4. By risk group and marital status

| risk group | marital status | men | % waited over 90 days | median days | 90th percentile days |
|---|---|---|---|---|---|
| low | Married (including common law) | 41,490 | 47.0 | 87.0 | 204.0 |
| low | Single (never married) | 5,690 | 51.9 | 93.0 | 226.0 |
| low | Divorced | 3,300 | 50.0 | 90.0 | 220.2 |
| low | Separated | 410 | 52.1 | 92.0 | 231.6 |
| low | Widowed | 1,200 | 42.5 | 83.0 | 196.0 |
| low | Unmarried or Domestic Partner | 160 | 59.9 | 106.5 | 245.0 |
| low | Unknown | 5,250 | 49.8 | 90.0 | 243.0 |
| intermediate | Married (including common law) | 89,430 | 41.3 | 80.0 | 169.2 |
| intermediate | Single (never married) | 14,160 | 49.4 | 90.0 | 197.0 |
| intermediate | Divorced | 8,840 | 47.4 | 87.0 | 190.0 |
| intermediate | Separated | 1,040 | 49.3 | 90.0 | 196.0 |
| intermediate | Widowed | 4,030 | 40.4 | 78.0 | 176.0 |
| intermediate | Unmarried or Domestic Partner | 570 | 49.6 | 90.0 | 194.5 |
| intermediate | Unknown | 9,560 | 42.6 | 81.0 | 189.0 |
| high | Married (including common law) | 92,380 | 30.9 | 68.0 | 143.0 |
| high | Single (never married) | 15,390 | 40.0 | 77.0 | 172.0 |
| high | Divorced | 9,110 | 36.6 | 74.0 | 161.0 |
| high | Separated | 1,110 | 41.4 | 80.0 | 177.0 |
| high | Widowed | 4,320 | 30.9 | 63.0 | 148.0 |
| high | Unmarried or Domestic Partner | 600 | 40.3 | 77.0 | 166.6 |
| high | Unknown | 7,980 | 36.6 | 73.0 | 168.0 |
| unknown | Married (including common law) | 9,230 | 40.2 | 77.0 | 197.4 |
| unknown | Single (never married) | 1,460 | 47.3 | 87.0 | 222.2 |
| unknown | Divorced | 770 | 46.4 | 83.0 | 223.0 |
| unknown | Separated | 80 | 48.1 | 87.0 | 311.0 |
| unknown | Widowed | 360 | 40.0 | 77.0 | 208.6 |
| unknown | Unmarried or Domestic Partner | 40 | 50.0 | 90.0 | 255.0 |
| unknown | Unknown | 2,890 | 44.6 | 82.0 | 253.0 |

### D5. By year of diagnosis (all risk groups)

| year of diagnosis | men | % waited over 90 days | median days | 90th percentile days |
|---|---|---|---|---|
| 2010 | 29,740 | 36.0 | 73.0 | 166.0 |
| 2011 | 29,350 | 35.8 | 73.0 | 161.0 |
| 2012 | 23,830 | 34.0 | 71.0 | 160.0 |
| 2013 | 22,530 | 33.5 | 71.0 | 159.0 |
| 2014 | 21,060 | 34.4 | 72.0 | 160.0 |
| 2015 | 22,530 | 36.2 | 74.0 | 162.0 |
| 2016 | 23,300 | 38.1 | 76.0 | 168.0 |
| 2017 | 24,120 | 39.3 | 77.0 | 164.0 |
| 2018 | 25,730 | 41.4 | 79.0 | 181.0 |
| 2019 | 27,270 | 43.5 | 82.0 | 187.0 |
| 2020 | 23,870 | 41.3 | 79.0 | 178.0 |
| 2021 | 28,750 | 46.3 | 85.0 | 188.0 |
| 2022 | 28,780 | 52.3 | 93.0 | 199.0 |
