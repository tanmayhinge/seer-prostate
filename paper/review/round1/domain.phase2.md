contract_role: domain

## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: block
trigger: "One or more factual errors or misrepresentations of prior work or of an external benchmark that materially alter a headline claim or its interpretation"
block_class: repairable

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Reviewer identity: Peer Reviewer 2 (domain), an urologic oncology outcomes researcher working with SEER and NCDB data on prostate cancer risk stratification, treatment coding and time to treatment. Criteria binding is unavailable, so this review makes no claim about fit with any venue.

Summary. The preprint uses SEER 17 data (2010 to 2022) to measure how much marital status, county rurality and county income add to predicting a wait of more than 90 days before first recorded treatment, beyond clinical need, in men whose first course included radical prostatectomy or radiotherapy. The domain groundwork is careful in several places. Treatment codes are checked against the coding manual, the secondary outcome is worded as recorded treatment, and the paper declines to compare with Tasmanian data. The social increment and the direction of the area contrast also survive the prostatectomy-only sensitivity analysis. However, two domain problems change how a headline conclusion should be read ("what is predictable is partly clinical triage"):
- the recorded interval ends at hormone therapy, which radiotherapy patients with higher-risk disease often start first;
- the Methods wrongly state that risk groups use clinical information only.

Separately, the Introduction's account of prior work leaves out the closest analogues that the project's own literature check found. These problems can be fixed by rewriting and by analyses the authors have largely already run, so the D2 block is repairable, not fatal.

### S1: The secondary outcome is named for what SEER can show
The paper calls the secondary outcome recorded curative treatment and lists what a missing record can mean. This matches the validation evidence it cites. Noone et al. (Med Care 2016, PMID 24638121) found moderate sensitivity for SEER treatment fields and advised against using SEER to estimate the proportion treated.
**Evidence Anchor**: text: Methods, Secondary outcome "It is therefore not described as untreated."

### S2: Surgery and radiation codes are explicit and checked against the manual
Radical prostatectomy codes are listed for both coding eras and checked against Appendix C. Radiation labels are named. Prostatectomy not otherwise specified is removed in a sensitivity analysis. RECORD asks for this kind of code-level transparency.
**Evidence Anchor**: text: Methods, Treatment definitions "checked against the SEER coding manual [17]"

### S3: The Australian material is kept as background
The Tasmanian estimates match the values stated in the protocol from full-text reading (Foley 2022, Foley 2025), and the Discussion refuses a cross-country comparison.
**Evidence Anchor**: text: Discussion, Relevance to Australian pathway research "No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings."

### S4: The rural direction is not read as better rural care
Shorter recorded waits in remote counties are set against lower crude recorded curative treatment among high-risk men. The paper cites a national SEER study (Dirican 2026) that points the same way.
**Evidence Anchor**: text: Discussion, The rural direction "It is not evidence that rural men receive better care."

### W1: The triage interpretation ignores hormone therapy started before radiotherapy
The Methods state correctly that the SEER interval ends at the first treatment of any kind, including hormone therapy. The Discussion and Conclusions then read the shorter waits of high-risk men as clinical triage ("consistent with triage", "partly clinical triage"). In higher-risk localised disease, androgen deprivation is commonly given with radiotherapy and started before it. In TROG 96.01, deprivation was given for 3 or 6 months before and during radiation (Denham et al., Lancet Oncol 2008, PMID 18929505). D'Amico et al. (JAMA 2004, PMID 15315996) showed a survival benefit of 6 months of androgen suppression with radiotherapy.

Other evidence points the same way:
- **Queensland:** treatment intervals were shorter when men received deprivation combined with radiotherapy (Baade et al., Cancer Causes Control 2012, PMID 22382868).
- **SEER-Medicare:** when the endpoint was definitive treatment, not any treatment, the wait was longer in high-risk than low-risk disease (Stokes et al., Cancer 2013, PMID 23716470). This is the opposite of the gradient reported here.
- **This paper's own data:** in men treated with prostatectomy only, where deprivation before treatment is less usual, the crude low-risk versus high-risk gap in delay shrinks from 15.1 to 7.4 percentage points.

So part of the "clinical need" signal in high-risk men is probably hormone therapy recorded as the end of the interval, not faster curative treatment.

**Why it matters:** the Principal findings and the second Conclusions bullet rest on this reading. The social increment and the area contrast stay similar in the prostatectomy-only scenario, so the core estimand survives.

**Suggestion:** state in the Outcome and Interpretation sections that radiotherapy patients with higher-risk disease often start deprivation first. Bring the prostatectomy-only risk gradient into the main text. Report the clinical-need increment for that scenario, if it is available from the refitted steps. Rephrase "triage" as one possible explanation among several.
**Severity**: Major
**Evidence Anchor**: table: Supplementary Table S19, primary analysis row against the radical prostatectomy without radiotherapy only row — low risk 47.9 against 45.8, high risk 32.8 against 38.4
**Confidence**: 4 — core expertise in prostate cancer treatment pathways and SEER interval coding, with facts checked in PubMed records

### W2: Risk groups are described as clinical-only, but stage partly uses surgical pathology
The Methods say risk groups use clinical information only. Yet the first criterion for high risk is regional summary stage. The paper's own Limitations, and protocol section 4, say summary stage partly uses pathology for surgical patients. Pathological upstaging at prostatectomy therefore moves surgical men into the high-risk group. Stage category also sits in the step 1 clinical-need block, so treatment-dependent information enters before treatment type is added at step 3. This works against the ordering the estimand relies on.

The effect is visible in the data. When risk groups are built from Gleason score and PSA only, the crude share of high-risk men waiting more than 90 days falls from 32.8% to 28.2% (Supplementary Table S19).

**Why it matters:** "beyond clinical need" is the reference point of the primary estimand. A clinical-need block that partly encodes surgery and its pathology changes both the size of the clinical-need increment and its meaning as triage.

**Suggestion:** correct the Methods sentence. State that regional stage for surgical patients is often pathological. Consider a sensitivity analysis that leaves stage out of step 1 (or uses it only for non-surgical men), and say whether the Gleason-and-PSA-only scenario kept stage in step 1.
**Severity**: Major
**Evidence Anchor**: text: Methods, Clinical risk groups "Risk groups used clinical information only, because pathological grade is observed only after surgery."
**Confidence**: 4 — core expertise in SEER prostate staging and risk-group construction

### W3: The account of prior work omits the closest analogues and misdescribes the literature
The Introduction says prior studies report adjusted associations one factor at a time, usually pooled across risk groups. The project's own literature check (reports/phase1.md) identified studies this description does not fit, none of which is cited:
- **Stokes et al. 2013** (Cancer, PMID 23716470): SEER-Medicare time to definitive treatment, reported by risk group, with a multivariable model.
- **Ajjawi et al. 2026** (Curr Urol, PMID 41969320): the closest design analogue. It compares a clinical-only machine learning model with one that adds sociodemographic variables, in SEER high-risk men, although for cancer-specific survival.
- **Semprini et al. 2026** (Health Serv Res, PMID 40476571): county income and timeliness in SEER.
- **Baade et al. 2012** (Cancer Causes Control, PMID 22382868): an Australian study of prostate cancer treatment intervals, relevant to private health insurance and radiotherapy. The Australian framing currently rests on two lung cancer studies [4, 5] instead.

The studies that are cited (Di Vanna 2025, Montiel Ishino 2021) fit multivariable models with several social factors together, not one factor at a time.

**Why it matters:** the novelty claim in the Abstract and Introduction depends on how prior work is described. The literature check was PubMed-only, screened by title and abstract, with one reviewer. It supports "we found no study that…", not a flat statement.

**Suggestion:** cite and set the paper apart from Stokes, Ajjawi, Semprini and Baade. Describe prior models accurately as multivariable. Hedge the novelty statement to match the search that was done.
**Severity**: Major
**Evidence Anchor**: text: Introduction "These studies report adjusted associations for one factor at a time, usually pooled across risk groups."
**Confidence**: 4 — core expertise in the prostate time-to-treatment literature, with every cited record checked in PubMed

### W4: "Lower is better" is applied to low-risk men
The Abstract, Results and the axis of Figure 2 label the percentage waiting more than 90 days as "lower is better" in every risk group. For low-risk disease, a systematic review found that delays of several months or even years do not appear to affect outcomes (van den Bergh et al., Eur Urol 2013, PMID 23453419). The Discussion itself allows for considered deferral. The quality label goes further than the evidence for the low-risk stratum, which is where the paper's most prominent contrast sits.

**Suggestion:** limit the quality label to intermediate- and high-risk men, or describe the low-risk result neutrally as meeting or exceeding the benchmark.
**Severity**: Minor
**Evidence Anchor**: text: Abstract, Results "39.7% waited more than 90 days (lower is better)"
**Confidence**: 4 — core expertise, grounded in a systematic review found in PubMed

### W5: "Added more than clinical need" in low-risk men partly reflects the narrow group definition
Low-risk men are defined by Gleason score 6 or lower, PSA below 10 and localised stage. Recorded clinical need can therefore barely vary within this stratum. The factors that drive timing decisions in low-risk disease (T stage, PSA density, imaging, core volume, patient preference) are not recorded. The finding is true as measured, but the Abstract and Discussion invite the reading that clinical factors matter less for timing in low-risk men.

**Suggestion:** say "recorded clinical variables, which vary little within this group by definition".
**Severity**: Minor
**Evidence Anchor**: text: Abstract, Results "in low-risk men it added more than clinical need did."
**Confidence**: 4 — core expertise in prostate risk stratification

### W6: The exclusion of active surveillance is stated as certain
The Methods state that men whose first course was active surveillance are not in the cohort. This depends on how registrars code treatment given after early reclassification. SEER's own definition of the interval includes "a decision to start active surveillance" (as quoted in reports/phase0.md). Intervals of 731 days or more are counted as delayed, and they are hard to square with a planned first course. The Discussion's marital-status interpretation also appeals to surveillance, which sits awkwardly with the stated exclusion.

I have not checked the SEER first-course coding rule directly.

**Suggestion:** present the exclusion as an assumption. Cite the coding rule. Report the share of intervals over 365 days, and those top-coded, by risk group.
**Severity**: Minor
**Evidence Anchor**: text: Methods, Active surveillance "Men whose first course was active surveillance have surgery and radiation coded as none, so they are not in this cohort."
**Confidence**: 3 — core expertise, but the SEER coding rule was not checked in this review

### W7: Huang et al. [22] is applied beyond its population
Huang et al. studied favourable-risk men only: low risk and favourable intermediate risk, clinical T1 to T2c (PMID 36727535). The paper uses it to support never-married findings pooled across intermediate and high risk, including longer waits among men who were treated. Huang also found that rural low-risk men were more likely to be on surveillance or watchful waiting (urban odds ratio 0.77). This bears directly on who is selected into the treated low-risk rural group, but it is not cited for that point.

**Suggestion:** restrict the claim to favourable-risk disease, and use the rural finding when discussing selection into treatment.
**Severity**: Minor
**Evidence Anchor**: text: Discussion, Marital status "This is consistent with higher use of surveillance or watchful waiting among unmarried men in an earlier SEER study [22]."
**Confidence**: 4 — abstract checked in PubMed

### W8: The Noone 80% figure is quoted without its context
The 80% sensitivity for radiation is pooled over seven cancer sites, in men aged 65 or older diagnosed 2000 to 2006. The study reports that sensitivity varied by site, stage and patient characteristics. It also advises against using SEER to compare treated with untreated individuals (PMID 24638121). The secondary analysis does exactly that by social group, and the Discussion leans on crude receipt by rurality.

**Suggestion:** give the scope of the 80% figure, and bring Noone's caution into the interpretation of the secondary outcome.
**Severity**: Minor
**Evidence Anchor**: text: Limitations "Against Medicare claims, SEER identified radiation therapy with 80% sensitivity [20]."
**Confidence**: 4 — abstract checked in PubMed

### W9: US and Australian area measures are presented as equivalent
Supplementary Box 2 says the Rural-Urban Continuum Code "corresponds to" ASGS remoteness areas, and that county median household income corresponds to SEIFA IRSAD. They are different constructs:
- the continuum code is based on county metropolitan population and adjacency, while the ASGS measure is accessibility-based;
- IRSAD is a composite area index, not income.

Two related points:
- **Insurance:** Box 2 says the closest Australian contrast is a public or private treating facility, but Australian prostate studies have used private health insurance directly (Baade 2012).
- **Terminology:** the Results call non-metropolitan counties not adjacent to a metropolitan area "remote counties", which borrows an ASGS term.

**Suggestion:** use "candidate proxy for" instead of "corresponds to", and avoid "remote" for US counties.
**Severity**: Minor
**Evidence Anchor**: text: Supplementary Box 2 "the Rural-Urban Continuum Code corresponds to Australian Statistical Geography Standard remoteness areas, assigned by residential postcode."
**Confidence**: 3 — adjacent expertise in Australian area classifications

### W10: The leave-one-variable-out range misstates the table
The Results say removing marital status or rurality lost 0.22 to 0.45 points in the pooled, intermediate- and high-risk strata. In Supplementary Table S8, intermediate-risk logistic regression lost 0.18 (marital status) and 0.19 (rurality), and LightGBM lost 0.21 (marital status). The same range appears in the source report reports/phase4.md.
**Severity**: Minor
**Evidence Anchor**: table: Supplementary Table S8, intermediate risk rows — marital status 0.18 and rurality 0.19 under penalised logistic regression, against the stated range of 0.22 to 0.45
**Confidence**: 5 — direct check against the table

### W11: Ang et al. [10] is cited for a mechanism it does not report
Ang et al. report the unadjusted paradox of lower mortality with longer intervals, pooled across breast, lung, prostate and colorectal cancer (PMID 40556964). The explanation that men with aggressive disease are treated sooner is the author's own inference (reports/phase1.md), not a finding of that study.

**Suggestion:** attribute the paradox to [10] and the triage explanation to the authors, or to a prostate-specific source.
**Severity**: Minor
**Evidence Anchor**: text: Introduction "Men with aggressive disease are treated sooner, which is why unadjusted comparisons of waiting time and survival can run in the wrong direction [10]."
**Confidence**: 4 — abstract checked in PubMed

### W12: The Discussion does not engage with evidence on large centres or the rising trend
The Discussion lists explanations the data cannot test, but cites no work that has tested them. In the NCDB, care at an academic centre was a determinant of longer time to treatment, and median time to treatment rose over 2004 to 2013 (Khorana et al., PLoS One 2019, PMID 30822350). The rise from 36.0% to 52.3% between 2010 and 2022 is a headline result in the Abstract, but the Discussion does not interpret it.

**Suggestion:** set the metropolitan direction and the time trend against this literature.
**Severity**: Minor
**Evidence Anchor**: text: Discussion, The rural direction "The data cannot test explanations such as longer surgical queues in large centres, second opinions, or wider choice of treatment settings."
**Confidence**: 4 — record checked in PubMed

### W13: STROBE and RECORD compliance is claimed but not yet shown
The paper says it follows STROBE and RECORD, but the checklists and the ethics statement are placeholders. RECORD [15] asks for the codes and algorithms used to classify variables, and for access to code. Two gaps stand out:
- the SEER variable names behind clinical Gleason score and PSA are not given in the manuscript (they appear only in config/analysis.yaml);
- the repository URL is missing.

**Suggestion:** complete the checklists, add the ethics statement, name the Gleason and PSA recode variables, and supply the code link.
**Severity**: Minor
**Evidence Anchor**: absence: Methods and Declarations — expected completed STROBE and RECORD checklists, an ethics statement, SEER variable names for clinical Gleason score and PSA, and a code repository link; checked Methods, Declarations, Reporting checklists section, Supplementary material
**Confidence**: 4 — reporting guideline cited by the manuscript itself

### Questions for Authors
1. In the prostatectomy-only and Gleason-and-PSA-only scenarios, was summary stage still included in step 1? What was the clinical-need increment in high-risk men in each?
2. What share of men in each risk group had intervals over 365 days, or top-coded at 731 days or more?
3. Does the November 2025 export include SEER's reviewed and corrected PSA values? The SEER PSA Working Group reported meaningful PSA errors in 5.7% of 2012 cases (Cancer 2017, PMID 27783399).

### Missing key references (each checked in PubMed)
- Stokes WA, et al. Racial differences in time from prostate cancer diagnosis to treatment initiation: a population-based study. Cancer. 2013;119(13):2486-93. PMID 23716470.
- Ajjawi I, et al. Machine learning approaches to optimize the integration of sociodemographic factors for predicting cancer-specific survival among patients with high-risk prostate cancer. Curr Urol. 2026;20(3):141-147. PMID 41969320.
- Baade PD, et al. Factors associated with diagnostic and treatment intervals for prostate cancer in Queensland, Australia: a large cohort study. Cancer Causes Control. 2012;23(4):625-34. PMID 22382868.
- Semprini JT, et al. Hospital accreditation and geographic disparities in timely cancer care. Health Serv Res. 2026;61(2):e14655. PMID 40476571.
- van den Bergh RC, et al. Timing of curative treatment for prostate cancer: a systematic review. Eur Urol. 2013;64(2):204-15. PMID 23453419.
- Khorana AA, et al. Time to initial cancer treatment in the United States and association with survival over time: an observational study. PLoS One. 2019;14(3):e0213209. PMID 30822350.
- Denham JW, et al. Time to biochemical failure and prostate-specific antigen doubling time as surrogates for prostate cancer-specific mortality: evidence from the TROG 96.01 randomised controlled trial. Lancet Oncol. 2008;9(11):1058-68. PMID 18929505.
