# Progress so far

**Study title:** Waiting for prostate cancer treatment: how much is clinical need? A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022

**Last updated:** 13 September 2026

## The project in one paragraph

After a man is diagnosed with prostate cancer and decides on surgery or radiotherapy, there is a wait before treatment starts. Some of that wait is medically sensible: a man with low-risk cancer can safely take longer to decide, while a man with high-risk cancer should be treated sooner. The question is whether the wait also depends on things that should not matter medically, such as whether a man is married, whether he lives in a city or in the country, and how well off his county is. This project measures how much of the waiting can be predicted from a man's medical situation, and how much more can be predicted once his social situation is added. That extra amount is a measure of unequal access to timely care.

## Why it matters

- **The Australian benchmark:** Australia's optimal care pathway for prostate cancer says surgery or radiotherapy should begin within 3 months of diagnosis.
- **What has been reported in Tasmania:** published studies found that men from outer regional and remote areas took longer to start active treatment than men from inner regional areas (Foley et al., Sci Rep 2022), and that public-hospital patients started treatment 40 to 59 days later than private patients in most risk groups (Foley et al., Cancers 2025). These findings come from the published papers, not from this project's data.
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
| Phase 4: results | Descriptive results, then the step-by-step models | Next |
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
- **Changes are logged:** any change must be recorded in the protocol's amendment log. Seven changes are logged so far, each with its reason. Recent ones renamed the study to name the machine learning approach, made clear that no Australian data are analysed, and added published Tasmanian and methods work as citations.

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

## What comes next

1. **Descriptive results:** waiting times by risk group, rurality and income.
2. **Models:** the step-by-step models, with uncertainty ranges.
3. **Human terms:** results turned into extra waiting days and an income inequality measure.
4. **Checks:** different thresholds (60, 120 and 180 days), surgery only, excluding 2020, and bounds for men without a recorded waiting time.
5. **Write-up:** a short preprint and a web article.

## Known limits

- **No race or insurance information** in this export.
- **No information on other illnesses,** so part of what looks like a social effect could be unmeasured health.
- **The waiting time ends at the first treatment of any kind,** which can include hormone therapy.
- **US healthcare is organised differently from Australia's.**
- **All results are associations, not proof of cause.**

## How the project is kept tidy

- **Settings in one place:** every setting lives in `config/`, not in the code.
- **Tests first:** tests were written before each piece of code, and 173 tests currently pass.
- **Private data stays local:** raw data and outputs with individual-level detail are kept out of git.
- **A report per phase:** each phase writes a report to `reports/`. `README.md` has the folder map and the commands to run everything.

## A note on tools

This project was developed with AI coding assistance (Anthropic's Claude). The author is responsible for the design choices, checks and interpretation.
