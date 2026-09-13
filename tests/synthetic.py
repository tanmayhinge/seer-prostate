"""Synthetic SEER-shaped rows for analysis tests. Labels match the real export exactly."""

from pathlib import Path

import pandas as pd

from seer_study.analysis_config import load_analysis_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_ROW = {
    "Year of diagnosis": "2015",
    "Sequence number": "One primary only",
    "Combined Summary Stage with Expanded Regional Codes (2004+)": "Localized only",
    "Survival months flag": "Complete dates are available and there are more than 0 days of survival",
    "Age recode with <1 year olds and 90+": "65-69 years",
    "RX Summ--Surg Prim Site (1998-2022)": "50",
    "RX Summ--Surg Prim Site 2023 (2023+)": "Blank(s)",
    "Radiation recode": "None/Unknown",
    "Time from diagnosis to treatment in days recode": "60",
    "Gleason Score Clinical Recode (2010+)": "Gleason score 7",
    "PSA Lab Value Recode (2010+)": "6.6",
    "Marital status at diagnosis": "Married (including common law)",
    "Rural-Urban Continuum Code": "Counties in metropolitan areas ge 1 million pop",
    "Median household income inflation adj to 2024": "$100,000 - $109,999",
}

# Each entry: (overrides, expected fate in the primary cohort)
COHORT_ROWS = [
    ({}, "included"),                                                                      # 0
    ({"Sequence number": "2nd of 2 or more primaries"}, "first primary"),                  # 1
    ({"Combined Summary Stage with Expanded Regional Codes (2004+)": "Distant site(s)/node(s) involved"}, "stage"),  # 2
    ({"Survival months flag": "Not calculated because a Death Certificate Only or Autopsy Only case"}, "dco"),  # 3
    ({"Age recode with <1 year olds and 90+": "35-39 years"}, "age"),                      # 4
    ({"Year of diagnosis": "2023", "RX Summ--Surg Prim Site (1998-2022)": "Blank(s)",
      "RX Summ--Surg Prim Site 2023 (2023+)": "A500"}, "year"),                            # 5
    ({"RX Summ--Surg Prim Site (1998-2022)": "00"}, "no curative treatment"),              # 6
    ({"Time from diagnosis to treatment in days recode": "Unable to calculate"}, "interval missing"),  # 7
    ({"Time from diagnosis to treatment in days recode": "0"}, "zero days"),               # 8
    ({"Time from diagnosis to treatment in days recode": "731+ days",
      "RX Summ--Surg Prim Site (1998-2022)": "00", "Radiation recode": "Beam radiation"}, "included"),  # 9
    ({"Time from diagnosis to treatment in days recode": "120", "Radiation recode": "Beam radiation"}, "included"),  # 10
    ({"RX Summ--Surg Prim Site (1998-2022)": "80"}, "included"),                           # 11
    ({"Sequence number": "1st of 2 or more primaries"}, "included"),                       # 12
    ({"RX Summ--Surg Prim Site (1998-2022)": "30"}, "no curative treatment"),              # 13
    ({"RX Summ--Surg Prim Site (1998-2022)": "00", "Radiation recode": "Refused (1988+)"}, "no curative treatment"),  # 14
]


def analysis_config():
    return load_analysis_config(PROJECT_ROOT / "config" / "analysis.yaml")


def make_frame(rows=COHORT_ROWS) -> pd.DataFrame:
    records = [{**DEFAULT_ROW, **overrides} for overrides, _ in rows]
    return pd.DataFrame(records, dtype=str)
