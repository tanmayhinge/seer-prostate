contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "some cross-disciplinary implications are stated more strongly than the cited support warrants"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Reviewer: Peer Reviewer 3 (cross-disciplinary). I review as a health economist who works on equity measurement (concentration indices) and rural access, and who compares health systems. My blind spots are prediction-model calibration detail and clinical coding. Criteria binding is unavailable, so I make no claim about fit with any venue.

Summary. The preprint uses US SEER data to measure how much marital status, county rurality and county income add to predicting a wait of more than 90 days, beyond recorded clinical need. It adds standardised percentages, an Erreygers concentration index and selection bounds. For readers in health services research, equity and policy, the framing is mostly careful. The manuscript says plainly that no Australian data were analysed. The joint area profiles are a sound choice for collinear area measures. I checked the headline numbers in the abstract, Results and Discussion against reports/phase3.md, reports/phase4*.md and PROTOCOL.md, and they match. D4 scores warn, not block. Every central construct has an operational definition that can be reproduced, and no principal takeaway lacks data. But several equity and policy statements say more than the analysis supports. The main ones are the income gradient, the direction statement in the Conclusions and the label "social position". The source report states one caveat that the manuscript leaves out. I found no wording that implies Australian data were analysed. The title, abstract, Discussion and Supplementary Box 2 all identify the data as US SEER, and the Discussion rules out a comparison with Tasmania.

### S1: Joint area profiles avoid off-support counterfactuals
The rurality and income contrast is standardised jointly, each area at its typical county income. It is not a one-at-a-time contrast. This is how equity analysts should handle collinear area measures, and the manuscript gives the reason in terms adjacent-field readers can follow.
**Evidence Anchor**: text: Methods, Standardised percentages "changing one while holding the other fixed creates combinations that are rarely observed"

### S2: Explicit boundary on cross-country interpretation
The Discussion states that no Australian data were analysed and that US and Tasmanian findings cannot be set against each other. It gives the reasons (area measures, health systems, interval definitions). This prevents the misreading that a comparison was made.
**Evidence Anchor**: text: Discussion, Relevance to Australian pathway research "No Australian data were analysed, and the US rural direction cannot be set against Tasmanian findings"

### S3: Careful labelling of the secondary outcome
Recorded curative treatment is not presented as treatment receipt or under-treatment. Policy readers could otherwise misread lower percentages as unmet need.
**Evidence Anchor**: text: Methods, Secondary outcome "It is therefore not described as untreated."

### S4: Selection bounds make the missing-interval problem transparent
The worst-case bounds by rurality and income let a reader check that the crude orderings survive extreme assumptions about men without a recorded interval.
**Evidence Anchor**: table: Supplementary Table S14 — lower and upper bounds by rurality for men without a recorded interval

### W1: The concentration index is presented as an income gradient although it cannot separate income from rurality
**Problem**: The abstract lists "Income" as a separate result, and the Conclusions refer to "lower-income counties". Both rest on an Erreygers index that ranks men by county median household income band. The source report (reports/phase4.md, section 4) says this index does not separate income from rurality. The manuscript leaves that caveat out of Methods, Results and Discussion. The manuscript's own evidence also shows that an income-specific signal depends on the model. In the leave-one-variable-out refits, income carried 0.00 to 0.02 points under logistic regression and 0.26 to 0.29 under LightGBM (Results, Which social variable). And 45.6% of men in remote counties were in the lowest income quartile, against 1.1% in large metropolitan counties (Table 1).
**Evidence Anchor**: text: Abstract, Results "delay was concentrated among men in higher-income counties (Erreygers index 0.062, 0.039 to 0.083; 0 means no income gradient)"
**Why it matters**: Equity and policy readers treat a concentration index as a socioeconomic gradient. Read alongside the separate rurality result, it looks like independent evidence that lower-income areas are advantaged. It is the same area contrast measured a second way.
**Suggestion**: Restore the source report's caveat in Results and Discussion. Present the index as an area-income and rurality gradient, not an income gradient. Drop the stand-alone income reading from the abstract and Conclusions, or state that it is not separable from rurality.
**Severity**: Major
**Confidence**: 4 — core expertise: concentration-index interpretation

### W2: The direction statement in the Conclusions omits that it holds only among men with recorded curative treatment
**Problem**: The Conclusions say the signal "points to less delay, not more, in rural and lower-income counties". The cohort is restricted to men with a recorded prostatectomy or radiotherapy. That restriction is itself socially patterned. Social position added 1.96 to 2.16 points of skill in predicting recorded curative treatment. Among high-risk men, crude recorded curative treatment was 75.3% in remote against 81.9% in large metropolitan counties, and 73.7% in the lowest against 83.0% in the highest income quartile (Supplementary Tables S26, S27). The Discussion's rural-direction paragraph says the rural direction "is not evidence that rural men receive better care". That qualifier does not reach the Conclusions or the abstract. The selection bounds cover men without a recorded interval, not selection into the treated cohort.
**Evidence Anchor**: text: Conclusions "the social signal is small and consistent, and points to less delay, not more, in rural and lower-income counties"
**Why it matters**: Policy readers usually read only the abstract and Conclusions. "Less delay in rural and lower-income counties" can be taken as better access. It may instead reflect who reaches recorded curative treatment and who is captured by reporting facilities.
**Suggestion**: State the conditioning population in the abstract Conclusions and the Conclusions section, for example "among men with recorded curative treatment". Carry the Discussion's "not evidence of better care" sentence into the Conclusions. Mention the lower recorded-treatment percentages in remote and low-income counties next to the delay direction.
**Severity**: Major
**Confidence**: 4 — core expertise: rural access and selection in equity measurement

### W3: "Social position" names a block that is mostly area attributes and registry practice
**Problem**: The primary estimand is called "social position". The block holds one individual variable (marital status) and two county-level area attributes. The Methods say it also absorbs unmeasured registry differences. The leave-one-variable-out results show that marital status and rurality carry most of the increment. In sociology and social epidemiology, "social position" usually means individual socioeconomic position. The title, abstract and Conclusions use the label without qualification.
**Evidence Anchor**: text: Methods, Uncertainty "The social block is interpreted as geographic and social position, including any unmeasured registry differences"
**Why it matters**: Readers from adjacent fields will take "social position adds 0.62 to 0.99 points" to mean individual socioeconomic disadvantage. That is not what was measured, and part of the signal may be registry or area practice.
**Suggestion**: Rename the block, for example "area and marital attributes", or qualify "social position" wherever it appears in the title, abstract and Conclusions. State once, prominently, that two of the three variables are ecological and that registry differences load onto the block.
**Severity**: Major
**Confidence**: 4 — core expertise: equity measurement constructs

### W4: The practical size of the primary estimand is not bridged to the percentage-point contrasts
**Problem**: The headline quantity is percentage points of log-loss skill, described as "small". The standardised area and marital contrasts are 6 to 9 percentage points, which a policy reader will read as large. The population-level "all social features as observed" contrast is only 1.1 to 1.6 points. The manuscript does not explain how the three relate. In low-risk men, social position is reported as 82% and 98% of step 2 skill. Step 2 skill there is below 1%, so the share framing can suggest that social position matters more than clinical need, when both contributions are tiny.
**Evidence Anchor**: table: Table 2, low risk rows — social position as 82 and 98 percent of step 2 skill, where step 2 skill is 0.76 and 0.99
**Why it matters**: Health services and policy readers cannot judge whether the increment matters, or reconcile "small" with a 9-point area difference. They are therefore likely to misjudge the policy weight of the findings.
**Suggestion**: Add a short interpretive paragraph, and a sentence in the abstract, relating skill points, the between-group standardised contrasts and the population-level contrast. Report the low-risk share next to the absolute skill values wherever it appears.
**Severity**: Major
**Confidence**: 3 — adjacent field: prediction-metric interpretation

### W5: Why an Australian benchmark is applied to US men is not stated
**Problem**: The outcome is justified only by reference to the Australian optimal care pathway. The manuscript does not say why this benchmark suits US men. It also does not link the benchmark to the 90-day threshold already used in the US literature it cites [8]. The Discussion says interval definitions differ, but the Methods do not say how the benchmark's clock compares with SEER's interval, which ends at the first treatment of any kind.
**Evidence Anchor**: text: Methods, Outcome "a wait of more than 90 days, following the optimal care pathway benchmark"
**Why it matters**: US readers will find the choice arbitrary. Australian readers may read the percentage as a measure of compliance with their pathway, which it is not.
**Suggestion**: In Methods, give one or two sentences on why the threshold was chosen, noting that 90 days is also used in US studies. Say that the SEER interval is not the pathway's own measure, and that the results are robust across 60, 120 and 180 days.
**Severity**: Minor
**Confidence**: 4 — core expertise: cross-system benchmarking

### W6: Labels saying lower waits are better conflict with the Discussion
**Problem**: The abstract, Results and figure legends label fewer delayed men, and fewer excess days, as better. The Discussion says a wait beyond 90 days can reflect considered deferral or patient choice. That is especially plausible in low-risk men, where delay was most common.
**Evidence Anchor**: text: Abstract, Results "39.7% waited more than 90 days (lower is better)"
**Why it matters**: These labels decide whether equity readers see the positive concentration index and the metropolitan excess as disadvantage. The normative direction is not established.
**Suggestion**: Remove the labels or qualify them, for example "a lower percentage means more men were treated within the benchmark". Say once that a longer wait is not necessarily worse care.
**Severity**: Minor
**Confidence**: 4 — core expertise: normative interpretation of equity indices

### W7: Excess waiting days are hard to interpret as a policy metric
**Problem**: Excess days are crude and unadjusted for risk group. They count top-coded intervals at 731 days and are expressed per 1,000 men without a per-man equivalent. The protocol's pre-specified 7-day meaningful difference in standardised mean waiting time is not mentioned in the manuscript.
**Evidence Anchor**: table: Supplementary Table S11, all men — 30,597 and 20,014 crude excess days per 1,000 men
**Why it matters**: Service planners will read these as the size of an access gap. Top-coded tails and case mix may drive them, and they carry no uncertainty.
**Suggestion**: Report days per man. Show how much of the excess comes from top-coded intervals. State that the 7-day threshold could not be applied and why.
**Severity**: Minor
**Confidence**: 3 — adjacent field: health services metrics

### W8: Supplementary Box 2 claims correspondence where only candidate equivalence is supported
**Problem**: The box title says "candidate" equivalents, but the text says the Rural-Urban Continuum Code "corresponds to" remoteness areas and that county median income corresponds to SEIFA IRSAD. By its name, IRSAD is an index of relative advantage and disadvantage, not a median income. The Australian measures are assigned by postcode, not county. The box gives no source for either equivalence.
**Evidence Anchor**: text: Supplementary Box 2 "the Rural-Urban Continuum Code corresponds to Australian Statistical Geography Standard remoteness areas, assigned by residential postcode"
**Why it matters**: A different construct and geographic scale would change the collinearity, the rank ties and the concentration index. That limits the claim that the measurement approach transfers as is.
**Suggestion**: Replace "corresponds to" with "is the closest available analogue of". Note the differences in construct and scale, and how they would affect joint area profiles and the concentration index.
**Severity**: Minor
**Confidence**: 3 — core expertise: cross-system area measures; details of the Australian classifications not verified here

### W9: Tasmanian public-private finding restated without its population restriction
**Problem**: The Introduction correctly restricts the Foley et al. 2025 differences to men not treated with external beam radiotherapy. The Discussion restates "42 to 59 days" without that restriction. PROTOCOL.md confirms the restriction.
**Evidence Anchor**: text: Discussion, What an Australian registry could add "They reported an adjusted difference of 9.25 days by remoteness, and of 42 to 59 days between public and private facilities"
**Why it matters**: Australian readers could over-generalise the size of the public-private gap.
**Suggestion**: Add "among men not treated with external beam radiotherapy". Note that the 9.25 days is an age-adjusted comparison of outer regional and remote with inner regional men.
**Severity**: Minor
**Confidence**: 4 — verified against PROTOCOL.md background section

### W10: The amendment log promises a supplementary table of one-at-a-time profiles that the supplement does not contain
**Problem**: Amendment 1.7 says the one-at-a-time rurality and income results are "kept in a supplementary table". The supplement has no such table. The source report shows they exist as a repository CSV, and that the models disagreed sharply on them (income Q4 to Q1: -0.9 against -8.7 points).
**Evidence Anchor**: absence: Supplement — expected the one-at-a-time rurality and county income profile table cited in amendment 1.7 of Supplementary Table S32; checked Methods Standardised percentages, Supplementary Tables S10, S21 to S24, S30, S31
**Why it matters**: Those results are the most direct evidence that an income-only gradient is not robust. Readers interested in equity cannot see them.
**Suggestion**: Add the table, with the statement that it is not interpreted, or correct the amendment text.
**Severity**: Minor
**Confidence**: 4 — direct document check

### W11: Rank ties and need standardisation for the concentration index are not described
**Problem**: Men are ranked by 16 county income bands, so ties are very large, yet the fractional-rank rule is not stated. The pooled index uses crude delay, not a need-standardised outcome. A need-standardised outcome is the usual way to measure horizontal inequity in health economics.
**Evidence Anchor**: absence: Methods, Income inequality — expected the fractional-rank rule for men tied within county income bands and whether delay was need-standardised; checked Methods Income inequality, Supplementary Table S12, Figure 4 legend
**Why it matters**: The value of the index depends on how ties are handled. The pooled 0.062 mixes risk-group composition with the income gradient, although the stratified indices partly address this.
**Suggestion**: State the tie rule. Report a pooled index of need-standardised delay, or say that the stratified indices are the intended need-adjusted estimates.
**Severity**: Minor
**Confidence**: 4 — core expertise: concentration index computation

### Questions for Authors
1. The concentration-index interval comes from a cluster bootstrap over cells defined partly by the ranking variable itself. Resamples therefore drop or duplicate whole income bands and change the rank distribution. How does this affect coverage for an index of income rank?
2. Could lower SEER capture of treatment given outside reporting facilities differ by rurality, so that the recorded cohort in remote counties is systematically different?
3. The Discussion says the measurement approach transfers. Which parts assume collinearity between remoteness and area disadvantage, and would that assumption hold at postcode scale?

### Cross-Disciplinary Reading Recommendations
- Search lead [UNVERIFIED]: the health economics literature on need-standardised (indirectly standardised) concentration indices and horizontal inequity indices, including World Bank guidance on analysing health equity with household survey data. This is relevant to W11 and to separating need from area income.
