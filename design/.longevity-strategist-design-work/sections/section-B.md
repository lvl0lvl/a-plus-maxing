# Section B — Biological-Age Biomarkers & Aging Clocks

Substrate for the `longevity-strategist` agent's **biological-age over-claim control**. The
load-bearing distinction throughout: a clock reading is a *population-calibrated estimate*, not a
diagnosis; its validated property is *association with chronological age and/or mortality risk*, not
proof that an intervention moving the clock improves a person's health. The single most important
fact for the agent is that **intervention-induced clock change has not been shown to predict real
health outcomes** — this gap is what every "reverse your age N years" marketing claim leaps over.

## Findings

### 1. First-generation clocks are predictors of *chronological* age, not measures of health damage

Horvath's multi-tissue clock was trained to predict **chronological age** from 353 CpG sites,
assembled from ~8,000 non-cancer samples across 82 Illumina array datasets spanning 51 tissues/cell
types, achieving median absolute error ~3.6 years and correlation r≈0.96 with age [1, mechanism_review][16, mechanism_review].
Hannum's clock (71 CpGs) was likewise trained to predict chronological age, but in **whole blood
only**, from 656 individuals aged 19–101 [2, cohort]. Study-design classification: both are
**predictive-modeling (regression) studies on human methylation data** — Horvath multi-tissue,
Hannum single-tissue (blood). Neither was trained on, nor validated against, a health outcome at
inception; "age acceleration" (residual of predicted minus chronological age) is a *derived*
quantity whose disease associations were established in *later* cohort work, not the original papers.
- **GRADE:** high certainty these clocks predict chronological age; **associational only** for any
  health meaning.
- **AGENT_TEMPLATE section:** Capabilities / Per-Marker Validity Table. **Discipline:** the agent
  must label first-gen clocks as "chronological-age estimators" and refuse to present age
  acceleration as a measured health deficit.

### 2. Second-generation clocks (PhenoAge, GrimAge) predict mortality — but the relationship is associational, not causal or proven-reversible

PhenoAge (Levine 2018, Aging) is a two-stage construct: a "phenotypic age" was first built from
chronological age + **9 clinical-chemistry biomarkers** (albumin, creatinine, glucose, CRP,
lymphocyte %, mean cell volume, red-cell distribution width, alkaline phosphatase, white-cell count)
calibrated to mortality in NHANES III; **DNAm PhenoAge** (513 CpGs) was then trained to predict that
phenotype [3, cohort]. A one-year increase in DNAm PhenoAge was associated with ~4.5% higher all-cause
mortality risk in validation [3, cohort]. (The underlying clinical phenotypic-age composite carries a
larger ~9%/yr association [HR≈1.09]; the DNAm clock that predicts it lands at ~4.5%/yr — the two must
not be conflated.) GrimAge (Lu 2019, Aging; senior author Horvath) is a
composite of DNAm surrogates for 7 plasma proteins plus DNAm-estimated smoking pack-years, trained
directly on **time-to-death**; it outperformed prior clocks for time-to-coronary-heart-disease and
mortality [4, cohort]. Design classification: **cohort/methods (regression on observational
cohorts)**. These are genuinely better *risk predictors* — but prediction of mortality in a
population is categorically different from demonstrating that lowering the score lowers an
individual's risk.
- **GRADE:** moderate–high (association with mortality, well-replicated); **causality and
  reversibility: very-low / unestablished.**
- **AGENT_TEMPLATE section:** Per-Marker Validity Table + Over-Claim Guards. **Discipline:** a HALT
  on any phrasing that treats a GrimAge/PhenoAge change as a proven health improvement.

### 3. DunedinPACE measures *rate* of aging, not a static age — and is a refinement of DunedinPoAm

DunedinPoAm (Belsky 2020, eLife) distilled the **Pace of Aging** — within-person rate of change
across 18 organ-system biomarkers measured at four timepoints over ~12 years (ages 26–38) in the
Dunedin 1972–73 birth cohort (N≈954) — into a single-blood-draw DNAm algorithm; its bootstrap
out-of-sample correlation with the longitudinal Pace of Aging was only r≈0.33 [5, cohort].
DunedinPACE (Belsky 2022, eLife) extended the observation window to 20 years (ages 26–45),
restricted input to high-reliability probes, and reports a value centered on 1.0 = one biological
year per chronological year [6, cohort]. It associates with morbidity, disability, and mortality and
has been replicated across many cohorts. Critically, what it validly measures is *pace* (a
speedometer), not a diagnosable state; and its outcome associations remain **observational**.
- **GRADE:** moderate (association with outcomes, broad replication); reversibility unproven.
- **AGENT_TEMPLATE section:** Per-Marker Validity Table. **Discipline:** the agent must distinguish
  "pace" clocks (rate) from "age" clocks (level) and never sum a DunedinPACE change into "years
  reversed."

### 4. Technical measurement noise is large enough to manufacture false intervention effects

Higgins-Chen 2022 (Nature Aging; senior author Levine) showed that for six prominent clocks,
**technical replicates from the same blood sample can differ by several years** of estimated
epigenetic age — maximum deviations ranged across clocks up to ~8.6 years (e.g., PhenoAge ~8.6 yr;
Horvath1 ~4.8 yr), exceeding one SD of age acceleration for several first-gen clocks [7, mechanism_review].
The principal-component ("PC") reformulation brought >90% of replicates into agreement within ~1–1.5
years (median deviation ~0.3–0.8 yr) and improved detection of true intervention effects [7, mechanism_review].
This is decisive for the agent: a within-person before/after clock change of a few years can be pure
measurement error, not biology. Most commercial single-run reports do not use PC-clocks and report no
confidence interval.
- **GRADE:** high (directly measured technical reliability).
- **AGENT_TEMPLATE section:** Over-Claim Guards / Measurement-Noise Caveat. **Discipline:** the agent
  must attach a measurement-noise caveat to any single clock reading and refuse to interpret a small
  longitudinal delta as a real change without replicate/CI information.

### 5. Whether clock changes are *causal* to aging — or just byproducts — is unresolved, and regulators have not accepted clocks as surrogate endpoints

A 2022 Nature news feature and a 2024 methods analysis document the central epistemic gap: it is
unknown whether the methylation changes clocks read are *causal* to age-related disease or are
*byproducts* of aging, and the **FDA does not recognize epigenetic-clock scores as surrogate
endpoints for clinical trials** — it wants the mechanistic basis defined and an answer to whether a
short-term clock decrease lowers age-related disease risk [8, mechanism_review][9, mechanism_review].
The 2024 analysis adds that chronological-age-trained (first-generation) clocks frequently show
**non-replicable, sporadic intervention changes** ("some significant epigenetic clock changes are
not replicable using any other clock model because they are false positives due to noise"), while
mortality/rate-trained clocks behave more reliably; and that different clocks can *disagree* on
whether the same intervention helped ("one significant clock is not enough to indicate a reliable
decrease in biological age") [9, mechanism_review]. This is the regulatory and scientific spine of the
over-claim control.

The surrogate-endpoint distinction is the most precise tool the agent has. A surrogate endpoint is a
biomarker *validated* to substitute for a clinical outcome — meaning a treatment-induced change in
the surrogate has been shown to predict a corresponding change in the outcome (the canonical positive
example is LDL cholesterol for cardiovascular events; the canonical failures are cancer-biomarker
surrogates that moved without survival benefit). No aging clock has cleared this bar. Therefore "your
GrimAge dropped two years" carries no validated implication for the person's mortality, even though
GrimAge *cross-sectionally* predicts mortality at the population level. The agent must hold both facts
at once and never collapse the second into the first.
- **GRADE:** the *uncertainty* itself is high-certainty (well-documented consensus that causality is
  unestablished and clocks are not validated surrogates).
- **AGENT_TEMPLATE section:** Refusal Classes / Scope Boundaries. **Discipline:** a refusal class for
  "reverse your biological age" directives, grounded in the absence of surrogate-endpoint validation;
  the agent must distinguish "predicts outcome cross-sectionally" from "validated surrogate."

### 6. The one widely-cited human "age reversal" result is an uncontrolled open-label pilot (n≈9)

The Fahy TRIIM study (Fahy 2019, Aging Cell; co-author Horvath), routinely invoked to support "you
can reverse your age," was an **open-label trial with no control group**, 9 men who completed,
using recombinant growth hormone + DHEA + metformin; it reported ~2.5 years of mean epigenetic-age
reduction across four clocks (Horvath, Hannum, PhenoAge, GrimAge) over 12 months [10, open_label].
With no control arm, small n, regression-to-the-mean, and a confounded multi-drug regimen (including
growth hormone, which carries its own risks), this cannot establish that the intervention reversed
aging or improved any clinical outcome; the authors themselves called for an "appropriately powered
follow-up study." It is the canonical example of evidence being stretched past its design.
- **GRADE:** very-low (uncontrolled, tiny n, surrogate-only endpoint).
- **AGENT_TEMPLATE section:** Over-Claim Guards / Negative Examples. **Discipline:** the agent must
  name the design limits when this study is cited and refuse to generalize it to a recommendation.

### 7. Organ-specific proteomic clocks add resolution but remain associational

Oh 2023 (Nature; senior author Wyss-Coray) estimated the biological age of **11 organs** from plasma
proteomics (~5,000 proteins) in ~5,676 individuals with replication across additional cohorts,
finding accelerated organ aging predicted future onset of organ-relevant disease (heart failure,
COPD, type 2 diabetes, Alzheimer's) over up to ~15 years and that **brain and immune aging were most
strongly linked to mortality** [11, cohort]. These are mortality/disease *associations* in
observational cohorts; the clocks are not validated as causal or as intervention endpoints, and
proteomic platform/assay drift introduces its own measurement variability.
- **GRADE:** moderate (association); causal/interventional: very-low.
- **AGENT_TEMPLATE section:** Per-Marker Validity Table. **Discipline:** same over-claim guard as
  methylation clocks; the agent must not present "your heart is X years old" as actionable diagnosis.

### 8. The inflammatory clock (iAge) is a single-lab deep-learning construct — promising but unreplicated

iAge (Sayed 2021, Nature Aging; senior author Furman) was built by deep learning on the blood
immunome (~50 cytokines/chemokines) of ~1,001 people aged 8–96; it tracked multimorbidity,
immunosenescence, frailty, and cardiovascular aging, with CXCL9 the dominant contributor
[12, cohort]. The mechanistic CXCL9 reversal experiments were performed in human endothelial cells
and mice, not in humans [12, animal] [population-mismatch: mouse and human cell lines]. iAge is
largely a single-group product with limited independent replication and a proprietary panel — a
concentration-risk flag.
- **GRADE:** low–moderate (single-cohort association); mechanism causal only in cells/mice, not
  humans.
- **AGENT_TEMPLATE section:** Per-Marker Validity Table + Concentration-Risk note. **Discipline:**
  the agent must flag single-lab/proprietary clocks as provisional and not treat mouse/cell mechanism
  as human-actionable.

### 9. Clinical-chemistry composites (Klemera–Doubal, PhenoAge-clinical) are interpretable and mortality-associated — and arguably more defensible than DTC methylation tests

The Klemera–Doubal method (Klemera & Doubal 2006, Mech Ageing Dev) computes biological age from
multiple routine biomarkers by treating chronological age as one more biomarker, minimizing error
propagation [13, mechanism_review]. Parker 2019 (J Gerontol A) compared KDM Biological Age,
homeostatic dysregulation, and the Levine clinical method in the Duke-EPESE cohort (N≈1,374, mean age
78) and showed KDM-BA associated with both **disability** (per-quintile ADL incidence rate ratio
~1.25) and **mortality** (HR ~1.09 per quintile) [14, cohort]. These use transparent, cheap,
re-orderable labs — but remain **associational** measures of risk, not diagnoses or proven
intervention targets.
- **GRADE:** moderate (association with mortality/disability); causal/interventional: low.
- **AGENT_TEMPLATE section:** Per-Marker Validity Table. **Discipline:** the agent may present these
  as risk *summaries* of standard labs while still refusing diagnostic or "reverse N years" framing.

### 10. Telomere length is a *weak* individual predictor — the cautionary baseline for all single biomarkers

Pooled across ~122,000 individuals (~21,800 deaths), one SD shorter leukocyte telomere length carried
a hazard ratio of ~1.09 (95% CI 1.06–1.13) for all-cause mortality — statistically real but small
[15, meta_analysis]. In a multinational cohort (Glei 2016, PLOS ONE; N≈4,571 across Costa Rica,
Taiwan, U.S.), after adjustment for age and sex, leukocyte telomere length ranked roughly
**15th–17th of 20 predictors**, below ten self-reported variables and three other biomarkers (CRP,
creatinine, HbA1c) [17, cohort]. Telomere length is the historical example of a biomarker with
population-level signal but poor individual discrimination — the same trap newer clocks risk when
marketed individually.
- **GRADE:** high (well-pooled); the *weakness* of individual prediction is the high-certainty
  finding.
- **AGENT_TEMPLATE section:** Per-Marker Validity Table / Negative Examples. **Discipline:** the agent
  must state telomere length is a weak individual predictor and refuse to act on a single LTL reading.

### 11. Functional markers (VO2max, grip strength, gait speed) have the strongest, most replicated, and most modifiable mortality links

Gait speed predicts survival across older adults: a pooled analysis of 34,485 individuals (Studenski
2011, JAMA) found a hazard ratio of 0.88 per 0.1 m/s faster gait (95% CI 0.87–0.90) — ~12% lower
mortality per increment [18, meta_analysis]. Grip strength (Leong 2015, Lancet, PURE study, 139,691
adults across 17 countries) was inversely associated with mortality at HR 1.16 per 5 kg lower grip
(95% CI 1.13–1.20), outpredicting systolic blood pressure [19, cohort]; a meta-analysis of 42 cohort
studies (~3,000,000 participants, Wu 2017, JAMDA) found the same HR ~1.16 per 5 kg [20, meta_analysis].
VO2max/cardiorespiratory fitness is a strong, independent predictor of all-cause and cause-specific
mortality: a JAMA meta-analysis of healthy men and women (Kodama 2009) found each 1-MET higher
maximal aerobic capacity associated with ~13% lower all-cause and ~15% lower CHD/CVD risk
[24, meta_analysis], and a 122,007-patient cohort undergoing exercise treadmill testing (Mandsager
2018, JAMA Netw Open) found graded, dose-dependent mortality reduction with higher fitness and no
observed upper limit of benefit [25, cohort]; a narrative review reaches the same conclusion
[21, mechanism_review]. These are functional aging markers, not "clocks" — and unlike
methylation clocks the underlying capacities are demonstrably trainable and their improvement
plausibly tracks real function. Even so, they are markers, not guarantees.
- **GRADE:** high (robust, replicated association); modifiability of the underlying capacity is
  well-established, though "improving the marker improves mortality" remains largely associational.
- **AGENT_TEMPLATE section:** Capabilities / Preferred-Evidence hierarchy. **Discipline:** the agent
  should privilege validated functional markers over provisional clocks when framing what is worth
  measuring, while still avoiding causal over-claim.

### 12. The DTC biological-age market systematically outruns the evidence

Commentary across an AMA Journal of Ethics piece and a 2026 ELSI review converges: DTC epigenetic-age
tests are marketed as actionable "your true biological age" and paired with supplements promising to
"reverse" aging, but the clocks are research/population tools — not medical tests to measure
individual health, best used by researchers studying populations rather than individuals; the lone
human reversal study cannot support the marketing claim, and the lack of regulation lets companies
exploit consumer fear [22, mechanism_review][23, mechanism_review]. Documented risks include
psychological harm and normalizing age-based discrimination [22, mechanism_review].
- **GRADE:** high (consensus critique); the over-claim is well-documented.
- **AGENT_TEMPLATE section:** Refusal Classes / Marketing-Claim Guard. **Discipline:** the agent must
  refuse to endorse "reverse your biological age by N years," disclose conflicts when a test is sold
  with supplements, and frame any clock result as a probabilistic population estimate with wide
  uncertainty.

## Evidence-landscape / concentration note

**Concentration risk — surface it, don't bury it.** The epigenetic-clock literature is unusually
concentrated. Steve Horvath is first or senior author on the Horvath clock [1], GrimAge [4], the
foundational Nature Reviews Genetics review [16], and is a co-author on the Fahy reversal trial [10].
Morgan Levine is first author on PhenoAge [3] and senior author on the reliability fix [7]. Daniel
Belsky is first author on **both** DunedinPoAm [5] **and** DunedinPACE [6]. Effectively three labs
(Horvath/UCLA-then-Altos, Levine/Yale-then-Altos, Belsky/Columbia with the Moffitt–Caspi/Duke group
and the Dunedin Study cohort/Otago) author the
majority of the primary clock-development papers cited here — well above the ~70% single-group
threshold for a flagged concentration. Independent replication exists for *outcome associations*, but
the *construction* and *reliability methodology* of the clocks largely originate from these groups,
several now affiliated with longevity-industry entities (Altos Labs, commercial test providers). The
agent must treat clock provenance as a conflict-of-interest surface.

**Methodological pattern.** Findings 1–9 and 11–12 rest on Tier-1 human studies (regression on
methylation/proteomic data, observational cohorts, meta-analyses). Animal/in-vitro evidence appears
only in Finding 8 (iAge CXCL9 mechanism), correctly tagged `[population-mismatch: mouse and human
cell lines]`. No numerical claim in this section is grounded in a `vendor_label` or
`anecdote_aggregate`; the DTC over-claim findings (12) cite critique/mechanism_review sources, not
vendor pages. No route-extrapolation issues arise because this section concerns measurement, not
dosing.

**The per-marker validity table the agent must carry.** Every marker needs two stored fields, kept
separate so neither silently borrows the other's authority: (i) *what it validly measures* and (ii)
*what it does not establish*. Horvath/Hannum: validly estimate chronological age; do not establish
health status. PhenoAge/GrimAge/DunedinPACE: validly stratify mortality risk in populations; do not
establish that moving the score changes an individual's outcome, and a single reading carries
multi-year measurement noise. Organ proteomic clocks: validly associate with future disease onset in
cohorts; do not diagnose an organ. iAge: validly tracks inflammatory burden in one cohort; lacks
independent multi-lab replication. KDM/clinical composites: validly summarize mortality risk from
standard labs; do not diagnose. Telomere length: validly associates with mortality at population
scale; does not discriminate well at the individual level. Functional markers (VO2max, grip, gait):
validly predict mortality and reflect trainable capacities; still do not guarantee outcomes for one
person. This two-field structure is the mechanical substrate for the over-claim control — when asked
"what does my clock say?" the agent must answer from field (i) and immediately surface field (ii).

**Lowest-certainty / highest-risk items the agent must carry:** (a) causality and reversibility of
*any* clock — very-low/unestablished (Findings 2, 5, 6); (b) iAge — single-lab, limited replication,
mouse/cell mechanism (8); (c) the Fahy reversal — uncontrolled n≈9 (6). The strongest evidence is for
functional markers (11) and the *weakness* of telomere length (10).

**Net design conclusion for the agent.** Across all twelve markers the pattern is identical: robust
*association* with age or mortality at the population level, paired with absent or very-low-certainty
evidence that intervention-driven movement of the marker changes an individual's outcome. The
longevity-strategist must therefore treat every biological-age result as a probabilistic,
noise-bearing population estimate; must refuse any directive framed as "reverse your biological age by
N years" or "lower your GrimAge to live longer"; must distinguish cross-sectional prediction from
validated surrogacy; must flag single-lab/proprietary clocks and clock provenance tied to
test-selling commercial entities; and should steer toward the better-evidenced, modifiable functional
markers (cardiorespiratory fitness, strength, gait) when a user asks what is actually worth tracking
— while still declining to promise that improving a marker guarantees a longer life. This is the
substrate for the agent's biological-age over-claim control.

## Bibliography

[1] Horvath S. 2013. DNA methylation age of human tissues and cell types. Genome Biology 14(10):R115. PMID 24138928. DOI 10.1186/gb-2013-14-10-r115. [mechanism_review]
[2] Hannum G, et al. 2013. Genome-wide methylation profiles reveal quantitative views of human aging rates. Molecular Cell 49(2):359–367. PMID 23177740. DOI 10.1016/j.molcel.2012.10.016. [cohort]
[3] Levine ME, et al. 2018. An epigenetic biomarker of aging for lifespan and healthspan (PhenoAge). Aging (Albany NY) 10(4):573–591. PMID 29676998. DOI 10.18632/aging.101414. [cohort]
[4] Lu AT, et al. (Horvath S senior). 2019. DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging (Albany NY) 11(2):303–327. PMID 30669119. DOI 10.18632/aging.101684. [cohort]
[5] Belsky DW, et al. 2020. Quantification of the pace of biological aging in humans through a blood test, the DunedinPoAm DNA methylation algorithm. eLife 9:e54870. DOI 10.7554/eLife.54870. URL https://elifesciences.org/articles/54870. [cohort]
[6] Belsky DW, et al. 2022. DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife 11:e73420. PMID 35029144. DOI 10.7554/eLife.73420. [cohort]
[7] Higgins-Chen AT, et al. (Levine ME senior). 2022. A computational solution for bolstering reliability of epigenetic clocks: implications for clinical trials and longitudinal tracking. Nature Aging 2(7):644–661. PMID 36277076. DOI 10.1038/s43587-022-00248-2. [mechanism_review]
[8] Goldman B / Nature News. 2022. Turning back time with epigenetic clocks. Nature 601:548–551. DOI 10.1038/d41586-022-00077-8. URL https://www.nature.com/articles/d41586-022-00077-8. [mechanism_review]
[9] Borrus T, et al. 2024. When to Trust Epigenetic Clocks: Avoiding False Positives in Aging Interventions. bioRxiv preprint. URL https://pmc.ncbi.nlm.nih.gov/articles/PMC11526921/. [mechanism_review; preprint — flagged]
[10] Fahy GM, et al. (Horvath S co-author). 2019. Reversal of epigenetic aging and immunosenescent trends in humans (TRIIM; open-label, no control). Aging Cell 18(6):e13028. PMID 31496122. DOI 10.1111/acel.13028. [open_label]
[11] Oh HS, et al. (Wyss-Coray T senior). 2023. Organ aging signatures in the plasma proteome track health and disease. Nature 624(7990):164–172. PMID 38057571. DOI 10.1038/s41586-023-06802-1. [cohort]
[12] Sayed N, et al. (Furman D senior). 2021. An inflammatory aging clock (iAge) based on deep learning tracks multimorbidity, immunosenescence, frailty and cardiovascular aging. Nature Aging 1(7):598–615. PMID 34888528. DOI 10.1038/s43587-021-00082-y. Human iAge is a 1000-Immunomes cohort-derived deep-learning construct; the embedded CXCL9 reversal mechanism was tested in human endothelial cells and mice (see Finding 8 `[population-mismatch: mouse and human cell lines]`), not in humans. [cohort]
[13] Klemera P, Doubal S. 2006. A new approach to the concept and computation of biological age. Mechanisms of Ageing and Development 127(3):240–248. PMID 16318865. DOI 10.1016/j.mad.2005.10.004. [mechanism_review]
[14] Parker DC, et al. 2019. Association of blood chemistry quantifications of biological aging with disability and mortality in older adults. J Gerontol A Biol Sci Med Sci 75(9):1671–1679. PMID 31693736. DOI 10.1093/gerona/glz219. [cohort]
[15] Wang Q, et al. 2018. Telomere length and all-cause mortality: a meta-analysis. Ageing Research Reviews 48:11–20. PMID 30254001. DOI 10.1016/j.arr.2018.09.002. [meta_analysis]
[16] Horvath S, Raj K. 2018. DNA methylation-based biomarkers and the epigenetic clock theory of ageing. Nature Reviews Genetics 19(6):371–384. PMID 29643443. DOI 10.1038/s41576-018-0004-3. [mechanism_review]
[17] Glei DA, et al. 2016. Predicting survival from telomere length versus conventional predictors: a multinational population-based cohort study. PLoS One 11(4):e0152486. DOI 10.1371/journal.pone.0152486. URL https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0152486. [cohort]
[18] Studenski S, et al. 2011. Gait speed and survival in older adults (pooled analysis of 9 cohorts). JAMA 305(1):50–58. PMID 21205966. DOI 10.1001/jama.2010.1923. [meta_analysis]
[19] Leong DP, et al. 2015. Prognostic value of grip strength: findings from the Prospective Urban Rural Epidemiology (PURE) study. Lancet 386(9990):266–273. PMID 25982160. DOI 10.1016/S0140-6736(14)62000-6. [cohort]
[20] Wu Y, et al. (Hu FB senior). 2017. Association of grip strength with risk of all-cause mortality, cardiovascular diseases, and cancer in community-dwelling populations: a meta-analysis of prospective cohort studies. J Am Med Dir Assoc 18(6):551.e17–551.e35. PMID 28549705. DOI 10.1016/j.jamda.2017.03.011. [meta_analysis]
[21] Strasser B, Burtscher M. 2018. Survival of the fittest: VO2max, a key predictor of longevity? Frontiers in Bioscience (Landmark) 23(8):1505–1516. URL https://article.imrpress.com/journal/FBL/23/8/10.2741/4657/Landmark4657.pdf. [mechanism_review; lower-trust publisher — flagged]
[22] (Author) 2025. What are the most ethically salient implications of epigenetic age testing? AMA Journal of Ethics 27(12). URL https://journalofethics.ama-assn.org/article/what-are-most-ethically-salient-implications-epigenetic-age-testing/2025-12. [mechanism_review]
[23] (Author) 2026. Consumer epigenomics and biological age editing: ethical, legal, and social implications. Epigenetics Communications. DOI 10.1186/s43682-026-00044-8. URL https://link.springer.com/article/10.1186/s43682-026-00044-8. [mechanism_review]
[24] Kodama S, et al. 2009. Cardiorespiratory fitness as a quantitative predictor of all-cause mortality and cardiovascular events in healthy men and women: a meta-analysis. JAMA 301(19):2024–2035. PMID 19454641. DOI 10.1001/jama.2009.681. [meta_analysis]
[25] Mandsager K, et al. (Jaber W senior). 2018. Association of cardiorespiratory fitness with long-term mortality among adults undergoing exercise treadmill testing. JAMA Network Open 1(6):e183605. PMID 30646252. DOI 10.1001/jamanetworkopen.2018.3605. [cohort]
