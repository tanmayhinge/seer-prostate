# Waiting for prostate cancer treatment: how much is clinical need?

A machine learning analysis of social position and time to treatment against the Australian optimal care pathway benchmark, US SEER 2010 to 2022.

This project measures how much of the wait between a prostate cancer diagnosis and the start of surgery or radiotherapy is explained by clinical need, and how much more is explained by social position (marital status, rurality, county income). It uses the US SEER cancer registry only; no Australian data are analysed. The 90-day threshold comes from the Australian optimal care pathway for prostate cancer, and published Tasmanian findings are cited as background.

- **Plain-language summary and status:** [PROGRESS.md](PROGRESS.md)
- **Pre-specified study protocol:** [PROTOCOL.md](PROTOCOL.md)

## Project layout

```
config/           All analysis settings (no constants in code)
  study.yaml        Raw-export inventory: paths, column roles, SEER label classes
  analysis.yaml     Cohort, treatment codes, risk groups, outcome, feature blocks
  reporting.yaml    Display names, bands and small-count suppression
  literature.yaml   PubMed search terms
data/raw/         SEER export and session files (not in git; see Data below)
reports/          Phase reports (phase1.md, phase3.md, phase4*.md), aggregate result tables and PubMed search record
scripts/          One entry point per phase
src/seer_study/   Library code, one module per concern
tests/            Unit tests, written before each module, with synthetic fixtures
PROTOCOL.md       Study protocol and amendment log
PROGRESS.md       What the project is and what is done so far
```

## Setup

Python 3.13.

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export PYTHONPATH=src
.venv/bin/pytest
```

## Running

Each phase has one script, run from the project root:

```
.venv/bin/python scripts/run_phase0.py           # inventory of the raw export (internal report)
.venv/bin/python scripts/run_phase1_search.py    # PubMed literature search
.venv/bin/python scripts/run_phase3_cohort.py    # cohort, inclusion flow and Table 1
.venv/bin/python scripts/run_phase4_descriptive.py        # A1 crude timeliness tables
.venv/bin/python scripts/run_phase4_models.py             # A2 to A4 cross-fitted models and bootstrap (long run)
.venv/bin/python scripts/run_phase4_models_report.py      # A2 to A4 report from the saved model tables
.venv/bin/python scripts/run_phase4_equity_selection.py   # A5 to A7 standardisation, equity index, selection
.venv/bin/python scripts/run_phase4_receipt.py            # A9 recorded curative treatment (secondary question)
.venv/bin/python scripts/run_phase4_receipt_report.py     # A9 report
.venv/bin/python scripts/run_phase4_sensitivity.py        # A8 sensitivity scenarios (long run; needs model_tuning.csv)
.venv/bin/python scripts/run_phase4_sensitivity_report.py # A8 report
```

`reports/phase4.md` summarises the Phase 4 reports.

## Data

The data are the SEER Research Data (17 registries, November 2025 submission). They are not included and cannot be shared. Access requires a SEER Research Data Use Agreement. Place the SEER*Stat case listing export (`export.txt`, `export.dic`) and session files in `data/raw/`.

Under that agreement, published tables suppress counts of 1 to 4 (`src/seer_study/disclosure.py`). Outputs that list individual label frequencies from the case listing (`reports/phase0.md`, `reports/phase0_tables/`, `reports/phase3_tables/`), and Phase 4 tables holding exact group counts, stay local and are excluded from git (see `.gitignore`). Row-level model predictions are written to `data/derived/`, which is also excluded.

Citation: Surveillance, Epidemiology, and End Results (SEER) Program, SEER*Stat Database: Incidence - SEER Research Data, 17 Registries, Nov 2025 Sub (2000-2023) - Linked To County Attributes - Time Dependent (1990-2024) Income/Rurality, 1969-2024 Counties, National Cancer Institute, DCCPS, Surveillance Research Program, released April 2026, based on the November 2025 submission.
