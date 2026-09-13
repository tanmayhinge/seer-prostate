## Contract Paraphrase

D1 (methodology_rigor, mandatory, owned by methodology). From a methodology standpoint this asks whether the design fits the stated research question, whether cohort construction, exclusions, missing-data handling and variable coding are transparent and defensible, whether model development and validation follow accepted practice for registry-based prediction work, whether statistics are reported with effect sizes and uncertainty that match the resampling scheme actually used, whether post hoc analytic choices are disclosed, and whether another analyst could reproduce the analysis from what is reported.

D2 (domain_accuracy, mandatory, owned by domain). This asks whether substantive claims agree with the current evidence base in the field, whether prior studies are represented faithfully, and whether domain terminology and results are stated correctly. Methodology does not score this dimension, but a methods reader relies on it being sound because a correct analysis of a mis-specified clinical construct still yields misleading conclusions.

D3 (argumentative_coherence, mandatory, owned by the devil's advocate, methodology eligible). This asks whether the central thesis holds together and whether the evidence actually produced supports each claim made from it. From the methodology perspective the key question is whether conclusions stay within what the design can identify, for example whether associational or predictive results are presented as causal, and whether every reported number is interpreted in the context of the analysis that generated it.

D4 (cross_disciplinary_relevance, high, owned by perspective). This asks whether framing, definitions and implications are understandable to readers from neighbouring fields and whether interdisciplinary claims are backed up. For methods, this matters mainly insofar as key measurement concepts are defined clearly enough for readers outside the core specialty to interpret the results correctly.

D5 (writing_and_structure, normal, owned by the editor). This asks whether the manuscript is well organised, clearly written, uses informative figures and tables, and follows the conventions expected of its format. From a methods view, clear placement of design details, reporting-checklist items and supplementary material affects how auditable the analysis is.

D6 (venue_fit_and_contribution, mandatory, owned by the editor). This asks whether the work suits the configured outlet and offers an original and significant contribution for its readers. No target outlet has been confirmed for this call, so the methodology seat makes no judgement on fit and does not score this dimension.

## Scoring Plan

### D1: methodology_rigor
dimension_id: D1
what_to_look_for: Explicit cohort flow with counts at each exclusion; definition and ascertainment of the time-to-treatment outcome and any censoring; handling and reporting of missing data; justification of predictor set and model choice; internal validation design (resampling scheme, repeats, tuning nested within resampling) with discrimination and calibration reported; uncertainty intervals whose construction matches the resampling actually used; disclosure of any post hoc analytic decisions; adherence to the reporting guidelines the authors claim (STROBE, RECORD, TRIPOD+AI) with checklist evidence; availability of code, software versions and data-access route sufficient for reproduction.
what_triggers_block: A core design or analysis flaw that could change the main estimates but is fixable in revision, such as data leakage between model fitting and evaluation, uncertainty intervals that do not reflect the stated resampling, undisclosed post hoc analytic choices affecting headline results, missing calibration assessment for a model used as a measuring tool, or cohort exclusions that are unexplained and plausibly selective.
what_triggers_warn: Reporting gaps that limit auditability without undermining the main results, such as incomplete checklist items for claimed guidelines, missing software versions or seeds, sensitivity analyses mentioned but not shown, partial description of missing-data handling, or effect sizes given without accompanying intervals for secondary results.
what_triggers_fatal: The analysis cannot support its primary question at all, such as an outcome definition that is structurally incompatible with the data source, reported numbers that cannot be reconciled with the described analysis, or a design in which the central quantity is not identifiable from the data used, so that no revision short of a new study would repair it.

### D3: argumentative_coherence
dimension_id: D3
what_to_look_for: Whether each conclusion maps to a specific reported analysis; whether predictive or associational findings are described without causal overreach; whether numbers cited in the abstract, discussion and conclusions match their source tables and are interpreted within the analysis that produced them; whether stated limitations are consistent with the strength of claims; whether any external benchmark comparison is framed with its assumptions made explicit.
what_triggers_block: One or more principal conclusions go beyond what the design can identify, such as causal language drawn from observational prediction results, or a headline number is reused in a context different from its source analysis in a way that changes its meaning, but the underlying analysis could support a correctly scoped claim after revision.
what_triggers_warn: Localised overstatement or inconsistency that does not alter the main thesis, such as hedging that varies between sections, a secondary claim with thin supporting analysis, or limitations acknowledged in one section but not reflected in the wording of conclusions elsewhere.
what_triggers_fatal: The central thesis is contradicted by the paper's own reported results or depends on an inference the design cannot support in any form, so that the main argument collapses rather than needing rescoping.

criteria_binding_unavailable

[CONTRACT-ACKNOWLEDGED]
