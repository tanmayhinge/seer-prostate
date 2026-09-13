# Progress so far

**Study title:** Waiting for prostate cancer treatment: how much is clinical need? A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022

**Last updated:** 13 September 2026

## The project in one paragraph

After a man is diagnosed with prostate cancer and decides on surgery or radiotherapy, there is a wait before treatment starts. Some of that wait is medically sensible: a man with low-risk cancer can safely take longer to decide, while a man with high-risk cancer should be treated sooner. The question is whether the wait also depends on things that should not matter medically, such as whether a man is married, whether he lives in a city or in the country, and how well off his county is. This project measures how much of the waiting can be predicted from a man's medical situation, and how much more can be predicted once his social situation is added. That extra amount is a measure of unequal access to timely care.

## Why it matters

- **The Australian benchmark:** Australia's optimal care pathway for prostate cancer says surgery or radiotherapy should begin within 3 months of diagnosis.
- **What has been reported in Tasmania:**
  - Men from outer regional and remote areas took a median of 82 days to start active treatment, against 75 days for men from inner regional areas. The difference was about 9 days once age was taken into account (Foley et al., Sci Rep 2022).
  - Among men not treated with external radiotherapy, men treated in public hospitals started active treatment about 42 to 59 days later on average than men treated privately, in low-, intermediate- and high-risk disease (Foley et al., Cancers 2025).
  - These findings come from the published papers, not from this project's data.
- **What this project adds:** it asks a related question in a large US population registry, using machine learning as a measuring tool. It analyses no Australian data. The Australian link is the benchmark (the 3-month pathway target), and the Tasmanian findings are cited as background only. All definitions live in configuration files, so the method could later be adapted to an Australian registry if that registry's data allow it.

## The questions in plain terms

Among men whose prostate cancer had not spread to distant sites, and who had surgery or radiotherapy as their first treatment:

1. **Main question.** How much of the chance of waiting more than 90 days is explained by medical need, and how much more by marital status, rural or city living, and county income?
2. **Second question.** The same comparison for whether men receive surgery or radiotherapy at all.
3. **Survival** is not analysed here. The protocol explains how it would need to be done to avoid a common error called immortal time bias.

## The data

- **Source:** the US SEER cancer registry (17 regions): 793,214 prostate cancer records diagnosed from 2010 to 2023.
- **Access:** the data are licensed and cannot be shared. Under SEER's rules, any table count between 1 and 4 is hidden before anything is published.
- **Not in this dataset:** race (the exported column was faulty), insurance, other illnesses, and which regional registry a man came from. These are listed as limitations.

## How the analysis works

The same question is answered step by step, each time adding one group of information to a prediction model:

1. **Base:** year of diagnosis only.
2. **Medical need:** cancer stage, Gleason grade, PSA level and age.
3. **Social position:** marital status, rurality and county income. **The improvement at this step is the main result.**
4. **Treatment type:** surgery or radiotherapy, reported separately, because social factors can influence which treatment a man gets.

**Models and checks**
- Two kinds of model are compared: penalised logistic regression (a standard statistical model) and gradient boosting (a machine learning model).
- Every model is tested on data it did not see during fitting.
- Calibration (whether predicted risks match what really happened) counts as much as ranking accuracy.

**Results in human terms**
- Extra waiting days per 1,000 men.
- How waiting differs across county income levels.

## What is done

| part | what it means | status |
|---|---|---|
| Phase 0: data check | Checked every column and every label in the raw export, and found and documented its problems | Done |
| Phase 1: literature check | Searched PubMed to see whether this study already exists | Done |
| Protocol | Wrote down the full study plan and every definition before looking at any results | Done, saved in git on 13 September 2026 |
| Phase 3: study group | Built the group of men to analyse, with a record of every exclusion | Done |
| Phase 4: results | Descriptive results, the step-by-step models, results in patient terms, income inequality, and checks on men with no recorded waiting time | Done, including the checks and the second question |
| Write-up | A short research paper (preprint) and a web article | Planned |

### Phase 0: data check
- **Structure:** 793,214 records with 41 columns, and every line has the correct structure.
- **Race column:** it contains a single value for everyone, so race cannot be used from this export.
- **Selection:** the saved SEER session shows what was actually selected: prostate cancer, diagnosed 2010 to 2023, with no age filter. That corrects an earlier note, which said an age filter had been applied.
- **Missing labels:** missing-value labels were checked against SEER's documentation for every column.

### Phase 1: literature check
- **Search:** 7 PubMed searches found 493 unique papers; the 10 most relevant are summarised in `reports/phase1.md`.
- **Gap found:** earlier studies show social factors are linked to longer waits, but none measured how much they add beyond medical need.
- **Second question:** it has been partly studied before, so it is treated as an extension, not as new.
- **Rural direction:** one SEER study found shorter waits for patients in non-metropolitan areas (Di Vanna et al., World J Oncol 2025), and a Tennessee study found lower odds of delay in Appalachian counties (Montiel Ishino et al., Am J Mens Health 2021). The Tasmanian study found longer waits in outer regional and remote areas. These studies define areas and waiting times differently, so they cannot be compared directly.

### Protocol
- **Written before results:** the cohort, treatment codes, risk groups, outcome, models and checks were all fixed in `PROTOCOL.md` before any results.
- **Why 90 days:** the threshold comes from the Australian optimal care pathway.
- **Changes are logged:** any change must be recorded in the protocol's amendment log. Twelve changes are logged so far (the protocol is at version 1.8), each with its reason. Earlier ones renamed the study to name the machine learning approach, made clear that no Australian data are analysed, and added and checked citations. The four most recent were made during Phase 4:
  - the model tuning details were written down before the full models were run;
  - extra waiting days are reported as plain counts rather than adjusted figures;
  - rurality and income are compared together, because the two are too closely linked to change one at a time;
  - how the checks and the second question would be run was written down before running them. This change also added one check that was not in the original plan, and it is labelled that way.

### Phase 3: study group

| step | men remaining |
|---|---|
| All records | 793,214 |
| First cancer only | 710,343 |
| Cancer not spread to distant sites | 608,441 |
| Diagnosed 2010 to 2022, aged 40 or over, not a death-certificate-only record | 557,683 |
| Had surgery or radiotherapy first | 355,581 |
| Waiting time recorded and above 0 days | **330,827** |

- **Headline:** 39.7% of these men waited more than 90 days.
- **An early look (description only, not a tested result):**
  - Men in counties in large metropolitan areas (1 million people or more) more often waited more than 90 days (42.5%) than men in non-metropolitan counties not adjacent to a metropolitan area (32.2%). This is a crude count, not adjusted for risk group or anything else. It cannot be set directly against the Tasmanian findings, which used different area categories and measures.
  - Men with low-risk cancer waited longest (47.9% over 90 days) and men with high-risk cancer the least (32.8%), which fits doctors treating urgent cases first.
- **Two cautions for the next phase:**
  - Rural counties in this data are also much poorer, so rurality and income are hard to separate.
  - Men without a recorded waiting time are more often from big cities and from earlier years; the analysis will test how much this could change the results.

### Phase 4: results
The full summary is in `reports/phase4.md`. All of these are associations, not proof of cause.

- **Waiting has got longer:** the share of men waiting more than 90 days rose from 36.0% in 2010 to 52.3% in 2022 (lower is better).
- **Waiting is hard to predict:** even the best models were only modestly better than chance at telling who would wait more than 90 days (AUC 0.59 to 0.66, where 0.5 is chance and 1 is perfect).
- **Social position adds a little, but reliably:**
  - Adding marital status, rurality and county income improved prediction in every risk group, under both models. The uncertainty range stayed above zero every time.
  - For all men, the gain was 0.62 points under logistic regression and 0.99 points under gradient boosting.
  - For low-risk men, social position added more than medical need did.
- **Which model did better:** gradient boosting (LightGBM) predicted better than penalised logistic regression in every risk group. The logistic model first chose the strongest penalty on offer. A later check with a wider range of settings picked the same penalty and gave identical results, so that did not hold it back.
- **In patient terms, after accounting for medical need:**
  - Men in the most remote type of county were about 9 percentage points less likely to wait more than 90 days than men in large cities, when each area is taken at its typical income. Both models agreed.
  - Never-married men were about 6 to 7 points more likely to wait than married men.
- **Income:** longer waits were concentrated among men in richer counties (concentration index 0.062, range 0.039 to 0.083). Richer counties are mostly big-city counties, so this cannot be separated from rurality.
- **Men with no recorded waiting time (2.7% to 5.5% by area):**
  - The unadjusted differences by area, income and marital status held even under the most extreme assumptions about these men.
  - Reweighting for them changed percentages by 0.2 points or less.
- **Checks with 10 alternative definitions** (other waiting-time cut-offs, surgery only, leaving out 2020, adding 2023, and others):
  - The small but reliable gain from social position held in 98 of 100 check results. Both exceptions were in the smallest group (men whose risk group could not be worked out).
  - The finding that remote-county men waited less often held in 9 of 10 checks for all men. The exception was the 180-day cut-off, where one model gave 2.96 points, just under the 3-point rule.
  - The finding that never-married men waited more often held in all 10.
  - Gradient boosting predicted better in 47 of 50 check results.
- **Second question: who has a recorded surgery or radiotherapy at all** (352,644 intermediate- and high-risk men):
  - 75.4% of intermediate-risk and 81.1% of high-risk men had one on record.
  - Having no record does not prove a man went untreated. It can mean active surveillance, hormone therapy only, refusal, or treatment the registry missed.
  - After accounting for medical need, never-married men were about 6 points less likely than married men to have a record. Both models agreed.
  - The difference between remote and big-city counties was under 3 points for men with the same medical features, with each area at its typical county income.
- **How this sits next to Tasmania:** in these US data, city men waited more often. In Tasmania, men from outer regional and remote areas started treatment later (Foley et al. 2022). The two studies measure areas and waiting times differently, so this is not a direct comparison.

## What comes next

1. **Figures.**
2. **Write-up:** a short preprint (medRxiv) and a two-page summary.
3. **Web article,** built last from the preprint.

## Known limits

- **No race or insurance information** in this export.
- **No information on other illnesses,** so part of what looks like a social effect could be unmeasured health.
- **The waiting time ends at the first treatment of any kind,** which can include hormone therapy.
- **US healthcare is organised differently from Australia's.**
- **All results are associations, not proof of cause.**

## How the project is kept tidy

- **Settings in one place:** every setting lives in `config/`, not in the code.
- **Tests first:** tests were written before each piece of code, and 284 tests currently pass.
- **Private data stays local:** raw data and outputs with individual-level detail are kept out of git.
- **A report per phase:** each phase writes a report to `reports/`. `README.md` has the folder map and the commands to run everything.

## A note on tools

This project was developed with AI coding assistance (Anthropic's Claude). The author is responsible for the design choices, checks and interpretation.
