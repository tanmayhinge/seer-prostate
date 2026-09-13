"""Build the short paper (paper/paper.pdf) and its supplement (paper/supplement.pdf) from paper/tex/.

Tables are generated from the analysis reports into paper/tex/tables/, so they cannot drift from the analysis outputs;
the reports already apply SEER disclosure control. Before compiling, the script checks the writing style (no em dashes
or banned words), that citations are numbered in order of first use with every reference cited, and word counts. Every
number in the running text that appears in none of the source documents is written to paper/number_audit.txt for a
person to check by hand. PDFs are compiled with tectonic. Run from the project root.
"""

import argparse
import re
import shutil
import subprocess
from pathlib import Path

from seer_study.manuscript import (
    bibitem_order,
    cite_order,
    extract_table,
    latex_tabular,
    markdown_rows,
    tex_prose,
    unsupported_numbers,
)
from seer_study.report import assert_style

SOURCE_GLOBS = ("reports/*.md", "PROTOCOL.md", "config/*.yaml", "requirements.txt", "paper/figures/captions.md")
DOCUMENTS = {"main": "paper.pdf", "supplement": "supplement.pdf"}
STRATA = {
    "all men (pooled)": "All men", "low risk": "Low risk", "intermediate risk": "Intermediate risk",
    "high risk": "High risk", "unknown risk": "Unknown risk",
    "intermediate and high risk (pooled)": "Intermediate and high risk",
}
MODELS = {"penalised logistic regression": "Logistic", "LightGBM": "LightGBM"}
RURALITY_HEADERS = [
    "Overall", r"\makecell[r]{Metro,\\1 million\\or more}", r"\makecell[r]{Metro,\\250,000 to\\1 million}",
    r"\makecell[r]{Metro,\\under\\250,000}", r"\makecell[r]{Nonmetro,\\adjacent\\to metro}",
    r"\makecell[r]{Nonmetro,\\not adjacent\\to metro}",
]
AGREEMENT = {
    "both models 3 points or more, same direction": "yes",
    "both models under 3 points": "no, both under 3",
    "same direction, only one model 3 points or more": "no, one model only",
    "opposite directions, at least one model 3 points or more": "no, opposite directions",
}


def rows_under(root: Path, report: str, heading: str) -> list[list[str]]:
    return markdown_rows(extract_table((root / report).read_text(), heading))[1]


def cell(value: str) -> str:
    """A report value written for LaTeX: minus signs, and <5 for suppressed statistics."""
    value = re.sub(r"(?<![\w.])-(?=\d)", "$-$", value)
    return value.replace("<5", r"$<$5")


def whole(value: str) -> str:
    """Drop a trailing .0 from day counts (77.0 becomes 77)."""
    return re.sub(r"\.0(?!\d)", "", value)


def tab(labels: tuple[str, ...], body: list[list[str]], spec: str, escape: bool = False) -> str:
    """A booktabs tabular with each header label aligned like its column; cells are already LaTeX."""
    columns = re.findall(r"[lrc]", re.sub(r"@\{\}|>\{[^}]*\}|p\{[^}]*\}",
                                          lambda m: "l" if m.group().startswith("p") else "", spec))
    if len(columns) != len(labels):
        raise SystemExit(f"{len(labels)} header labels for column spec {spec!r}")
    header = [label if label.startswith("\\") else rf"\makecell[{align}]{{{label}}}"
              for label, align in zip(labels, columns)]
    return latex_tabular(header, body, spec, escape=escape)


def grouped(rows: list[list[str]], columns: int = 1) -> list[list[str]]:
    """Blank the leading cells that repeat the row above."""
    out, previous = [], [None] * columns
    for row in rows:
        shown = [("" if row[i] == previous[i] and all(row[j] == previous[j] for j in range(i)) else row[i])
                 for i in range(columns)]
        previous = row[:columns]
        out.append(shown + row[columns:])
    return out


FLOW_LABELS = {
    "all records": ("All prostate cancer records", None),
    "first primary": ("First primary cancer", "Not the first primary cancer"),
    "localised or regional stage": ("Localised or regional stage", "Not localised or regional stage"),
    "not death certificate or autopsy only": ("Not death certificate or autopsy only",
                                              "Death certificate or autopsy only"),
    "age 40 or over": ("Aged 40 or over", "Not aged 40 or over"),
    "diagnosed 2010 to 2022": ("Diagnosed 2010 to 2022", "Not diagnosed 2010 to 2022"),
    "first course includes prostatectomy or radiotherapy": (
        "Radical prostatectomy or radiotherapy recorded", "No radical prostatectomy or radiotherapy"),
    "interval recorded or top-coded": ("Interval recorded or top-coded", "No recorded interval"),
    "interval above 0 days": (r"\textbf{Primary cohort: interval above 0 days}", "Interval of 0 days"),
}


def flow_figure(root: Path) -> str:
    """TikZ inclusion flow drawn from the primary cohort flow table in reports/phase3.md."""
    lines = [
        r"\begin{tikzpicture}[>=latex, font=\sffamily\scriptsize,",
        r"  cohortbox/.style={draw=accent, align=center, text width=3.9cm, inner sep=2.5pt, execute at begin node={\hyphenpenalty=10000}},",
        r"  exclusionbox/.style={draw=accent, align=left, text width=3.3cm, inner sep=2.5pt, fill=accentlight, execute at begin node={\hyphenpenalty=10000}}]",
    ]
    for i, (step, remaining, excluded, _share) in enumerate(
            rows_under(root, "reports/phase3.md", "## Inclusion flow (primary cohort)")):
        if step not in FLOW_LABELS:
            raise SystemExit(f"no flow label for step {step!r}")
        label, reason = FLOW_LABELS[step]
        position = "" if i == 0 else f", below=6mm of s{i - 1}"
        lines.append(rf"\node[cohortbox{position}] (s{i}) {{{label}\\n = {remaining}}};")
        if i:
            middle = rf"$(s{i - 1}.south)!0.5!(s{i}.north)$"
            lines += [
                rf"\draw[->, accent] (s{i - 1}) -- (s{i});",
                rf"\node[exclusionbox, anchor=west] (e{i}) at ($(s{i - 1}.south)!0.5!(s{i}.north) + (2.35cm,0)$) "
                rf"{{{reason}\\n = {excluded}}};",
                rf"\draw[->, accent] ({middle}) -- (e{i}.west);",
            ]
    return "\n".join(lines + [r"\end{tikzpicture}"]) + "\n"


def float_table(label: str, caption: str, tabular: str, note: str, size: str = r"\footnotesize",
                colsep: str = "3pt", wide: bool = False) -> str:
    """A captioned table with a shaded header row; ``wide`` spans both columns of the two-column paper."""
    environment = "table*" if wide else "table"
    tabular = tabular.replace("\\toprule\n", "\\toprule\n\\rowcolor{tablehead}", 1)
    return (
        f"\\begin{{{environment}}}[tbp]\n\\centering\\sffamily\n{size}\n\\setlength{{\\tabcolsep}}{{{colsep}}}\n"
        f"\\caption{{{caption}}}\n\\label{{{label}}}\n{tabular}\n\\par\\smallskip\n"
        f"\\begin{{minipage}}{{\\linewidth}}\\scriptsize {note}\\end{{minipage}}\n\\end{{{environment}}}\n"
    )


def percent_of(value: str) -> str:
    match = re.search(r"\(([\d.]+)%\)", value)
    return match.group(1) if match else cell(value)


def table1(root: Path) -> str:
    header, rows = markdown_rows(extract_table((root / "reports/phase3.md").read_text(), "## Table 1."))
    if header[2:8] != ["Overall", "Metro, 1 million or more", "Metro, 250,000 to 1 million", "Metro, under 250,000",
                       "Nonmetro, adjacent to metro", "Nonmetro, not adjacent to metro"]:
        raise SystemExit(f"unexpected Table 1 columns: {header}")
    columns = range(2, 8)
    find = {(row[0], row[1]): row for row in rows}
    sections = [
        ("Risk group", "Risk group", [("low", "Low"), ("intermediate", "Intermediate"), ("high", "High"),
                                      ("unknown", "Unknown")]),
        ("Summary stage", "Summary stage", [("Localised", "Localised"),
                                            ("Regional, direct extension", "Regional, direct extension"),
                                            ("Regional, lymph nodes", "Regional, lymph nodes")]),
        ("Marital status", "Marital status", [("Married (including common law)", "Married"),
                                              ("Single (never married)", "Never married"),
                                              ("Divorced", "Divorced"), ("Widowed", "Widowed"),
                                              ("Unknown", "Unknown")]),
        ("County median household income (quartile of 16 bands)", "County income quartile",
         [("Q1 (lowest)", "Q1 (lowest)"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4 (highest)", "Q4 (highest)")]),
        ("First-course treatment", "First-course treatment",
         [("Radical prostatectomy", "Radical prostatectomy"), ("Radiotherapy", "Radiotherapy"),
          ("Both", "Both")]),
    ]
    body = [["Men, n"] + [find[("Men, n", "")][i] for i in columns]]
    for characteristic, title, levels in sections:
        body.append([rf"\textit{{{title}}}"] + [""] * 6)
        body += [[rf"\quad {label}"] + [percent_of(find[(characteristic, level)][i]) for i in columns]
                 for level, label in levels]
    days = find[("Days to first recorded treatment", "median (IQR)")]
    medians = [re.match(r"([\d.]+) \(([\d.]+) to ([\d.]+)\)", days[i]).groups() for i in columns]
    body.append([r"\textit{Days to first recorded treatment}"] + [""] * 6)
    body.append([r"\quad Median"] + [whole(m[0]) for m in medians])
    body.append([r"\quad Interquartile range"] + [f"{whole(m[1])} to {whole(m[2])}" for m in medians])
    body.append([r"Waited more than 90 days"] + [percent_of(find[("Waited more than 90 days", "over 90 days")][i])
                                                 for i in columns])
    tabular = latex_tabular(["Characteristic"] + RURALITY_HEADERS, body, "@{}l*{6}{r}@{}", escape=False)
    note = (r"Values are the percentage of men in the column unless stated. Rurality is the county Rural-Urban "
            r"Continuum Code at diagnosis; 159 men with unknown rurality are included in Overall only. Separated "
            r"(0.8\%) and unmarried or domestic partner (0.4\%) men are not shown. $<$5: suppressed under the SEER "
            r"Research Data Use Agreement, either because it rests on 1 to 4 men or because a total would reveal "
            r"such a cell. County income quartiles are formed from 16 bands of county median household income.")
    return float_table("tab:cohort", "Characteristics of the 330,827 men in the cohort, by county rurality",
                       tabular, note, colsep="6pt", wide=True)


def table2(root: Path) -> str:
    headline = rows_under(root, "reports/phase4_models.md", "## Headline")
    auc = {(r[0], r[1]): r[5] for r in rows_under(root, "reports/phase4_models.md", "## Performance at every step")
           if r[2] == "2"}
    seeds = {(r[0], r[1]): re.search(r"\((.+)\)", r[4]).group(1)
             for r in rows_under(root, "reports/phase4_revision.md", "## (a) and (b)")}
    body = grouped([[STRATA[r[0]].removesuffix(" risk"), MODELS[r[1]], r[2], r[3], auc[(r[0], r[1])], cell(r[4]),
                     cell(r[5]), seeds[(r[0], r[1])]] for r in headline])
    tabular = tab(("Risk group", "Model", "Men", r"Skill at\\step 2 (\%)", r"AUC at\\step 2",
             r"Clinical need\\added (95\% interval)", r"Area and marital\\added (95\% interval)",
             r"Fold-seed\\range\textsuperscript{a}"),
        body, "@{}llrrrrrr@{}", escape=False)
    note = (r"Skill is the percentage reduction in out-of-fold log-loss against the step 0 model (year of diagnosis "
            r"only); added values are in percentage points. Intervals are 95\% cluster bootstrap intervals over "
            r"79 rurality by county income cells (500 resamples of out-of-fold predictions, no refitting), so they "
            r"exclude model-fitting variability. \textsuperscript{a}Range of the area and marital increment over 10 "
            r"fold assignments, from the post-review analysis with per-step tuning (protocol amendment 1.9). AUC: "
            r"0.5 is chance.")
    return float_table("tab:models", "Predictive performance and skill added by clinical need and by area and "
                       "marital characteristics, by risk group and model", tabular, note, colsep="5pt", wide=True)


def s1(root: Path) -> str:
    rows = rows_under(root, "reports/phase4_descriptive.md", "### D2.")
    body = grouped([[r[0].capitalize(), r[1], r[2], cell(r[3]), whole(r[4]), whole(r[5])] for r in rows])
    tabular = tab(("Risk group", "County rurality", "Men", r"Waited more\\than 90 days (\%)",
                                 r"Median\\days", r"90th percentile\\days"), body, "@{}llrrrr@{}", escape=False)
    note = (r"Crude values; nothing is adjusted. Numbers of men are rounded to the nearest 10. Medians and 90th "
            r"percentiles count top-coded intervals as 731 days. $<$5: statistic suppressed because 1 to 4 men "
            r"in the row did, or did not, wait more than 90 days.")
    return float_table("tab:s1", "Crude waiting beyond 90 days by risk group and county rurality", tabular, note)


def s2(root: Path) -> str:
    rows = [r for r in rows_under(root, "reports/phase4_models.md", "## Performance at every step") if r[2] == "2"]
    body = grouped([[STRATA[r[0]], MODELS[r[1]], r[3], r[4], r[5], cell(r[6]), r[7]] for r in rows])
    tabular = tab(("Stratum", "Model", r"Log-loss\\skill (\%)", r"Brier\\skill (\%)", "AUC",
                                 r"Calibration\\intercept", r"Calibration\\slope"), body, "@{}llrrrrr@{}",
                            escape=False)
    note = (r"Out-of-fold predictions at step 2 (clinical need plus area and marital characteristics). Skill is "
            r"against the step 0 model. Calibration intercept: 0 is ideal; slope: 1 is ideal, below 1 means "
            r"predictions are too extreme. Values for every step are in \texttt{reports/phase4\_models.md}.")
    return float_table("tab:s2", "Performance at step 2 by risk group and model", tabular, note)


def s3(root: Path) -> str:
    rows = rows_under(root, "reports/phase4_revision.md", "## (a) and (b)")
    body = grouped([[STRATA[r[0]], MODELS[r[1]]] + [cell(v) for v in r[2:6]] for r in rows])
    tabular = tab(("Stratum", "Model", r"Primary analysis\\(tuned at step 3)", r"Tuned at\\each step",
                                 r"Mean (range) over\\10 fold seeds", r"Clustered by county\\income band only"),
                            body, "@{}llrrrr@{}", escape=False)
    note = (r"Percentage points of out-of-fold log-loss skill added by area and marital characteristics (step 1 "
            r"to 2), with 95\% cluster bootstrap intervals (first fold seed, 500 resamples, no refitting). Tuning "
            r"was not repeated per seed. Specified after an internal review (protocol amendment 1.9).")
    return float_table("tab:s3", "Robustness of the area and marital increment to tuning, fold assignment and "
                       "clustering", tabular, note, colsep="2pt")


def s4(root: Path) -> str:
    rows = rows_under(root, "reports/phase4_revision.md", "## (d) Stage-free")
    pivot: dict[tuple[str, str, str], dict[str, str]] = {}
    for analysis, stratum, model, comparison, estimate, _primary in rows:
        pivot.setdefault((analysis, stratum, model), {})[comparison.split(" (")[0]] = estimate
    body = grouped([[a.capitalize(), STRATA[s], MODELS[m], cell(v["clinical need"]), cell(v["social position"])]
                    for (a, s, m), v in pivot.items()], columns=2)
    tabular = tab(("Analysis", "Stratum", "Model", r"Clinical need added\\(95\% interval)",
                                 r"Area and marital added\\(95\% interval)"), body, "@{}lllrr@{}", escape=False)
    note = (r"Stage-free: summary stage removed from the clinical block, risk strata unchanged. Year as "
            r"categories: logistic regression only, one indicator per year replacing linear year and the 2020 "
            r"indicator. Both use per-step tuning and the first fold seed. Primary estimates are in Table 2 of the "
            r"main text. Specified after an internal review (protocol amendment 1.9).")
    return float_table("tab:s4", "Stage-free clinical block and year of diagnosis as categories", tabular, note)


def s5(root: Path) -> str:
    report = "reports/phase4_sensitivity.md"
    delayed = {r[0]: (r[1], r[2], r[3]) for r in rows_under(root, report, "## Percentage waiting beyond the threshold")}
    increment = {(r[0], r[1]): r[2] for r in rows_under(root, report, "## Social position increment by scenario")}

    def contrast(heading: str) -> dict[str, str]:
        return {r[0]: f"{cell(r[1])} / {cell(r[2])}" + ("" if AGREEMENT[r[3]] == "yes" else r"\textsuperscript{a}")
                for r in rows_under(root, report, heading)}

    area, marital = contrast("### Area:"), contrast("### Marital status:")
    body = [[scenario[0].upper() + scenario[1:], threshold, men, pct,
             cell(increment[(scenario, "penalised logistic regression")]), cell(increment[(scenario, "LightGBM")]),
             area[scenario], marital[scenario]]
            for scenario, (threshold, men, pct) in delayed.items()]
    tabular = tab(("Scenario", r"Threshold\\(days)", "Men", r"Delayed\\(\%)", r"Added, logistic\\(95\% interval)",
             r"Added, LightGBM\\(95\% interval)", r"Area\\contrast", r"Never married\\contrast"),
        body, r"@{}>{\raggedright\arraybackslash}p{3.2cm}rrrrrrr@{}", escape=False)
    note = (r"All men. Each scenario changes one setting from the primary analysis. Added: percentage points of "
            r"log-loss skill added by area and marital characteristics. Contrasts are standardised differences in "
            r"percentage points (logistic / LightGBM): nonmetro counties not adjacent to a metro area minus metro "
            r"areas of 1 million or more, each at its typical county income; and never married minus married. "
            r"\textsuperscript{a}Two-model rule (both 3 points or more, same direction) not met. Threshold "
            r"scenarios use a different outcome, so their values are not directly comparable. Numbers of men are "
            r"rounded to the nearest 10.")
    return float_table("tab:s5", "Sensitivity analyses", tabular, note, size=r"\scriptsize")


def contrast_label(text: str) -> str:
    if text.startswith("all social"):
        return "Observed minus reference profile"
    if text.startswith("area:"):
        return "Nonmetro not adjacent minus metro 1 million or more"
    if text.startswith("marital"):
        return "Never married minus married"
    raise SystemExit(f"unknown contrast {text!r}")


def s6(root: Path) -> str:
    rows = rows_under(root, "reports/phase4_equity_selection.md", "### Contrasts (percentage points)")
    body = grouped([[STRATA[r[0]], contrast_label(r[1]), cell(r[2]), cell(r[3]), AGREEMENT[r[4]]] for r in rows])
    tabular = tab(("Stratum", "Contrast", "Logistic", "LightGBM", r"Two-model\\rule met"), body,
                            "@{}llrrl@{}", escape=False)
    note = (r"Standardised percentage points waiting more than 90 days (g-computation with the step 2 model; each "
            r"man keeps his own clinical features and year). Reference profile: married, metro area of 1 million "
            r"or more, county income rank at the 83.33\% quantile. Area profiles set rurality and county income "
            r"together at the median income band of men living in that type of area. Rule (post hoc, amendment "
            r"1.7): both models 3 points or more in the same direction. No intervals are reported.")
    return float_table("tab:s6", "Standardised contrasts in waiting more than 90 days, by risk group", tabular, note)


def s7(root: Path) -> str:
    overall = dict(rows_under(root, "reports/phase4_equity_selection.md", "## A6."))
    period: dict[str, dict[str, str]] = {}
    for stratum, years, value in rows_under(root, "reports/phase4_revision.md", "## (f) Income"):
        period.setdefault(stratum, {})[years] = value
    periods = ["2010 to 2014", "2015 to 2019", "2020 to 2022"]
    body = [[STRATA[s], cell(overall[s])] + [cell(period[s][p]) for p in periods] for s in overall]
    tabular = tab(("Stratum", "2010 to 2022", *periods), body, "@{}lrrrr@{}", escape=False)
    note = (r"Erreygers-corrected concentration index (95\% cluster bootstrap interval) of waiting more than 90 "
            r"days, ranking men by county median household income, poorest first. Positive values mean delay is "
            r"concentrated in higher-income counties. Crude: not standardised for clinical features, and it does "
            r"not separate income from rurality. Indices by period were specified after an internal review "
            r"(amendment 1.9).")
    return float_table("tab:s7", "Income concentration of delay, overall and by period of diagnosis", tabular, note)


def s8(root: Path) -> str:
    report = "reports/phase4_equity_selection.md"
    weighted = {r[1]: r[4] for r in rows_under(root, report, "### Inverse probability weighted percentages")
                if r[0] == "rurality"}
    body = [[r[0], r[1], r[2], r[3], r[4], r[5], weighted[r[0]]] for r in rows_under(root, report, "### Bounds by rurality")]
    tabular = tab(("County rurality", r"Treated\\men", r"Recorded\\men (\%)", r"Lower\\bound (\%)",
                                 r"Upper\\bound (\%)", r"No recorded\\interval (\%)", r"Weighted\\(\%)"),
                            body, "@{}lrrrrrr@{}", escape=False)
    note = (r"Percentage waiting more than 90 days among treated men meeting cohort steps 1 to 6 (intervals of 0 "
            r"days excluded). Lower bound: every man without a recorded interval waited 90 days or less; upper "
            r"bound: every such man waited longer. Weighted: men with a recorded interval, weighted by the inverse "
            r"of their predicted probability of having one. Numbers of men rounded to the nearest 10. Neither "
            r"approach addresses selection into recorded treatment.")
    return float_table("tab:s8", "Men without a recorded interval: bounds and inverse probability weighting",
                       tabular, note)


def s9(root: Path) -> str:
    report = "reports/phase4_receipt.md"
    contrasts: dict[tuple[str, str], dict[str, str]] = {}
    for stratum, contrast, logistic, lightgbm, _ in rows_under(root, report, "### Contrasts (percentage points)"):
        label = contrast_label(contrast)
        contrasts.setdefault((stratum, "penalised logistic regression"), {})[label] = logistic
        contrasts.setdefault((stratum, "LightGBM"), {})[label] = lightgbm
    body = []
    for r in rows_under(root, report, "## Value added at each step"):
        c = contrasts[(r[0], r[1])]
        body.append([STRATA[r[0]], MODELS[r[1]], r[2], cell(r[3]), cell(r[4]), r[6],
                     cell(c["Nonmetro not adjacent minus metro 1 million or more"]),
                     cell(c["Never married minus married"])])
    tabular = tab(("Stratum", "Model", r"Skill at\\step 2 (\%)", r"Clinical need\\added (95\% interval)",
             r"Area and marital\\added (95\% interval)", r"AUC at\\step 2", r"Area\\contrast", r"Never married\\contrast"),
        grouped(body), "@{}llrrrrrr@{}", escape=False)
    note = (r"Outcome: a record of radical prostatectomy or radiotherapy in the first course, among intermediate- "
            r"and high-risk men meeting every cohort step before treatment. No record can mean active surveillance, "
            r"watchful waiting, hormone therapy only, refusal or uncaptured treatment, so a lower percentage "
            r"cannot be read as under-treatment. Contrasts are standardised percentage points, defined as in "
            r"Table S6.")
    return float_table("tab:s9", "Secondary outcome: recorded radical prostatectomy or radiotherapy", tabular, note,
                       size=r"\scriptsize")


TABLES = {"figure1_flow": flow_figure, "table1": table1, "table2": table2, "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7,
          "s8": s8, "s9": s9}


def between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def check(name: str, tex: str, sources: list[str]) -> list[str]:
    if "---" in tex:
        raise SystemExit(f"{name}.tex: '---' renders as an em dash")
    body = tex.split("\\begin{document}", 1)[1]
    prose = tex_prose(body)
    assert_style(prose)
    cited, listed = cite_order(body), bibitem_order(body)
    if cited != listed:
        raise SystemExit(f"{name}.tex: citations in order of first use {cited} differ from bibliography {listed}")
    words = {"words (prose)": len(prose.split())}
    if name == "main":
        words["abstract words"] = len(tex_prose(between(body, "%% abstract-start", "%% abstract-end")).split())
        words["main text words"] = len(tex_prose(between(body, "%% main-text-start", "%% main-text-end")).split())
    missing = unsupported_numbers(prose, sources)
    print(f"{name}.tex: " + ", ".join(f"{k} {v:,}" for k, v in words.items()) + f"; {len(cited)} references; "
          f"{len(missing)} unsupported number(s)")
    return [f"{name}.tex: {len(missing)} number(s) not found in any source"] + [f"  {token}" for token in missing]


def compile_tex(tex_dir: Path, name: str, target: Path) -> None:
    build = tex_dir / "build"
    build.mkdir(exist_ok=True)
    result = subprocess.run(["tectonic", "--keep-logs", "--outdir", "build", f"{name}.tex"], cwd=tex_dir,
                            capture_output=True, text=True)
    if result.returncode:
        print(result.stdout[-4000:], result.stderr[-4000:])
        raise SystemExit(f"tectonic failed on {name}.tex")
    log = (build / f"{name}.log").read_text(errors="replace")
    for line in log.splitlines():
        if re.search(r"undefined|Overfull \\hbox \((?:[3-9]\.|\d{2,})", line):
            print(f"  {name}.log: {line.strip()}")
    shutil.copy(build / f"{name}.pdf", target)
    print(f"wrote {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--no-compile", action="store_true")
    args = parser.parse_args()
    tex_dir = args.root / "paper/tex"
    (tex_dir / "tables").mkdir(parents=True, exist_ok=True)
    for stem, build in TABLES.items():
        text = build(args.root)
        if stem.startswith("s"):  # supplement tables stay under their section heading
            text = text.replace(r"\begin{table}[tbp]", r"\begin{table}[H]")
        (tex_dir / "tables" / f"{stem}.tex").write_text(text)

    sources = sorted({path for pattern in SOURCE_GLOBS for path in args.root.glob(pattern)})
    source_texts = [path.read_text() for path in sources]
    audit = [f"Sources: {', '.join(str(p) for p in sources)}", ""]
    for name in DOCUMENTS:
        audit += check(name, (tex_dir / f"{name}.tex").read_text(), source_texts)
    (args.root / "paper/number_audit.txt").write_text("\n".join(audit) + "\n")
    if not args.no_compile:
        for name, pdf in DOCUMENTS.items():
            compile_tex(tex_dir, name, args.root / "paper" / pdf)


if __name__ == "__main__":
    main()
