# Section D — Prescribing-practice layer

Scope: how the OTC-supplement & nootropic prescribing-and-use CONVENTION ecosystem
diverges from trial evidence. This is the MANDATORY practitioner-convention layer
(Hard Rule 3). Every dose stated below by a functional/integrative practitioner body
renders as **practitioner convention, not trial-validated**. Where a Tier-1/2 source
contradicts the convention on a primary dose statement, the academic evidence wins for
the report's primary dose and both are reported (per whitelist Tier-2.7 admissibility rule).

DISCIPLINE NOTE: the supplement ecosystem has weaker Tier-2.7 institutional scaffolding
than peptides — there is no supplement equivalent of the Seeds Peptide Protocols with
named per-dose prescribing tables. Functional-medicine bodies (IFM, A4M) publish
*target-level* and *category* conventions more than fixed milligram prescribing tables,
and much "stack dose" convention originates from manufacturer trials or community lore
rather than a citable prescriber. This is itself a finding (D1).

---

### Finding D1 — Functional/integrative-medicine convention sets vitamin D TARGET LEVELS (and therefore doses) well above the trial/regulatory range; this is a practitioner convention, not a trial-validated target

Conventional/regulatory convention treats serum 25(OH)D ≥ 20–30 ng/mL as sufficient
(IOM "adequate" ~20 ng/mL; Endocrine Society 2011 "sufficient" ≥30 ng/mL, with a tolerable
upper intake the IOM place at 4,000 IU/day and the Endocrine Society at 10,000 IU/day)
[1, regulatory (IOM 2011 DRI + Endocrine Society 2011 guideline)]. Functional-medicine
practitioner convention instead targets 50–80 ng/mL (IFM-stated optimal ~60–80 ng/mL),
i.e. 2–3× the conventional 30 ng/mL threshold, which in turn drives higher maintenance and
repletion doses [2, practitioner_protocol]. A repletion ("loading") convention of 50,000 IU
D3 weekly × 8 weeks for 25(OH)D < 20 ng/mL traces to the Endocrine Society guideline and
is widely used clinically [3, regulatory-derived / open_label-supported].

- **Convention-vs-trial gap:** The 50–80 ng/mL target is a *practitioner convention*, NOT a
  trial-validated optimum — RCTs powered on hard outcomes (VITAL, etc.) did not establish that
  driving 25(OH)D to 60–80 ng/mL improves the outcomes the convention invokes (immune, cardiac,
  oncologic). Indeed Tier-1 work argues the *dose-response itself* is mis-estimated:
  Veugelers & Ekwaru (2014) re-analyzed the IOM's own data and contend the IOM UNDER-estimated the
  intake needed to reach a given 25(OH)D — calculating that ~8,895 IU/day (vs the IOM's 600 IU
  RDA) would be needed for 97.5% of individuals to reach 50 nmol/L, a figure the authors flag as
  beyond the studied dose range — a methodological dispute orthogonal to whether 60–80 ng/mL is
  the right target [4, mechanism_review]. (Note the opposite-direction Tier-1 critique exists too:
  McKenna & Murray 2013, PMC3680954, argue the dose-response rate constant should be DOUBLED —
  i.e. LESS intake per unit — so the Tier-1 literature itself is split on direction; D1 cites the
  "more intake needed" side.) So convention and trial literature disagree on TWO axes:
  the target level (no RCT hard-outcome validation) and the dose needed to hit any target.
- **Caveats:** [1]/[3] dose statements are guideline-derived (admissible for dose convention and
  regulated upper limits). [2] is a practitioner-convention target — it may NOT ground an efficacy
  claim that 60–80 ng/mL is *beneficial*; that requires Tier-1/2, which is currently mixed/negative
  on hard outcomes. The IFM page that states the 50–80 ng/mL target ("Vitamin D Evaluation: A
  Clinical Tool in Personalized Medicine", ifm.org) was HTTP-403 to direct fetch; the 50–80 / 60–80
  figure is corroborated across multiple practitioner restatements but the IFM page itself should be
  re-fetched (authenticated) before the exact figure + author + date are locked for wiki ingest.
  Per Tier-2.7 rule, a `practitioner_protocol` cite REQUIRES practitioner/venue + date — currently
  satisfied at the venue level (IFM article title) but the author + publication date are not yet captured.

---

### Finding D2 — The creatine "loading phase" (20 g/day × ~6 days) is a speed-of-saturation convention, not a necessity; the trial that established it explicitly offers low-dose (3 g/day × 28 days) as equally effective

Hultman et al. (1996, *J Appl Physiol*) established both protocols head-to-head: 20 g/day × 6 days
raised muscle total creatine ~20%, maintainable thereafter on 2 g/day; 3 g/day × 28 days produced
the *same ~20%* increase, more gradually [5, rct]. The authors frame rapid loading as "a rapid way
to creatine load" — a practical OPTION, not a requirement [5, rct]. The community/practitioner
convention that loading is a mandatory first step is therefore not supported by the originating trial.

- **Convention-vs-trial gap:** "Load with 20 g/day for a week" is presented across community and
  trainer convention as a near-mandatory protocol; the Tier-1 source it derives from says the
  loading phase is NOT necessary and that low-dose reaches identical saturation given ~3 more weeks.
  This is the cleanest case in the section where convention OVER-states necessity relative to its own
  source trial.
- **Tolerability note (keep separated from efficacy):** the loading convention's main documented
  downside is GI discomfort / acute water-weight gain during the high-dose window — an adverse-effect
  EXISTENCE claim admissible from Tier-1/2 trial reports, not an AE-rate claim [5, rct; AE-rate would
  need a powered tolerability RCT — one such 28-day loading-vs-no-load GI/fluid trial is registered,
  ClinicalTrials.gov NCT07176325, but is a registration, not yet a result] [6, regulatory-registry].
- **Caveats:** [5] is a small mechanistic human trial (muscle-biopsy creatine), strong for the
  saturation claim, not a body-composition/performance outcome trial. Do not let the saturation
  endpoint stand in for a strength/performance efficacy claim.

---

### Finding D3 — Multi-ingredient "stacks" inherit `combination_evidence: none` and the WEAKEST component rung; component tolerability does NOT compose to combination safety. Branded-extract "stack doses" often trace to manufacturer-funded trials, and some marketed precursors lack hard-outcome validation entirely

Three converging strands:

1. **Stacks carry no combination evidence unless a combination study exists.** Caffeine + L-theanine
   is the rare nootropic pair with an actual combination RCT — and it shows the combination behaves
   DIFFERENTLY from the sum of parts: adding L-theanine ATTENUATED/eliminated caffeine's
   vasoconstrictive and some cognitive/mood effects on cerebral blood flow while improving
   task-switching accuracy and alertness [7, rct; 8, rct]. This is direct evidence that you cannot
   infer a stack's effect (or safety) from single-ingredient data — the canonical justification for
   `combination_evidence: none` as the default and "inherits the weakest component rung." Broader
   multi-ingredient nootropic stacks (e.g. racetam + cholinergic + caffeine + theanine "blends") have
   NO located combination trial; their "stack dose" is community/vendor convention, not trial-derived
   [retrieval gap — no admissible combination study located for ≥3-ingredient nootropic stacks].

2. **Branded-extract "stack dose" originates from the manufacturer's own trials.** The widely
   repeated ashwagandha "600 mg KSM-66" dose traces to Chandrasekhar et al. 2012 (*Indian J Psychol
   Med*), a randomized, double-blind, placebo-controlled trial of a high-concentration full-spectrum
   root extract at 600 mg/day showing reduced stress scores and a ~28% (exact 27.9%) serum cortisol
   reduction from baseline vs 7.9% on placebo (between-group P=0.002) — a figure that appears in the
   trial's FULL-TEXT RESULTS TABLE, not the abstract (which states only "substantially reduced,
   P=0.0006") [9, rct; figure from full-text results table]. The dose CONVENTION is real and
   trial-anchored — but the anchoring trials use the
   proprietary branded extract and are manufacturer-associated, so the "600 mg" number is extract-
   specific (KSM-66 root, ~5% withanolides) and does NOT transfer to generic ashwagandha or to
   leaf-inclusive extracts (Sensoril dosing convention is lower, ~125–250 mg, reflecting higher
   withanolide concentration) [9, rct for KSM-66; Sensoril dose is a branded-extract convention not
   yet pinned to an admissible primary in this retrieval].

3. **Some clinic/IV-marketed precursors lack hard-outcome validation AND have shifting regulated
   status.** NAD+ precursors: NR reliably RAISES blood NAD+ in healthy adults (~60% PBMC NAD+ rise)
   [10, rct (NR, Martens et al.)], and a separate Tier-1 NMN RCT shows NMN significantly raises
   blood NAD+ in healthy middle-aged adults (300/600/900 mg/day × 60 d, n=80, p ≤ 0.001 vs placebo
   at days 30 and 60) [14, rct (NMN, Yi & Maier)]; NMN at 1250 mg/day × 4 wk was separately well-
   tolerated with no SAEs (n=31), though that safety trial did NOT measure NAD+ [11, rct (NMN safety;
   NAD+ not measured)]. Reviews state the clinical
   evidence that raising NAD+ improves physiological function is unclear / "in its infancy"
   [12, mechanism_review]. Regulated-status convention has diverged from marketing AND has itself
   shifted: in NOV 2022 the FDA took the position that NMN is excluded from the dietary-supplement
   definition because it was authorized for investigation as a new drug; FDA then REVERSED that
   position on SEP 29, 2025 and issued confirmation letters DEC 2, 2025, so that as of 2026 NMN is
   a LAWFUL dietary ingredient (retaining NDI status, premarket notification still required). The
   clinic/IV "NAD+ precursor supplement" framing conflicted with the 2022–2025 exclusion but is
   no longer in conflict with NMN's current (2026) regulated status; the regulated-status question
   is best read as the divergence-then-convergence above rather than a settled exclusion
   [13, regulatory — primary FDA NDIN correspondence; time-stamped, re-verify against posted FDA
   letters before ingest].

- **Convention-vs-trial gap:** (a) stack doses presented as validated are, for ≥3-ingredient blends,
  convention with `combination_evidence: none`; (b) branded-extract doses are trial-anchored but
  manufacturer-funded and extract-specific, not a generic "the dose"; (c) NAD+ precursor IV/clinic
  marketing implies functional BENEFIT that the Tier-1 efficacy literature (mixed/early) does not
  support; the NMN supplement-legitimacy question is now resolved in marketing's favor (FDA
  reversed the 2022 exclusion in 2025, NMN lawful as of 2026) but the benefit gap remains.
- **Caveats:** [9] is manufacturer-associated — strong for the dose CONVENTION and for an
  effect-exists signal, but its effect-size should be read with sponsor-bias flagged and cross-checked
  against independent ashwagandha RCTs before any efficacy claim is locked. [10] (NR) and [14] (NMN)
  support NAD+ ELEVATION (a biomarker), NOT clinical benefit; [11] is an NMN safety/tolerability trial
  that did NOT measure NAD+ and therefore supports tolerability ONLY, not the elevation half. [13] is a regulated-status claim anchored to
  primary FDA NDIN correspondence (Tier-2 / FDA position) and is time-stamped through the Nov-2022
  exclusion → Sep-2025 reversal → Dec-2025 confirmation arc; current (2026) status is NMN lawful
  as an NDI. Re-verify against the posted FDA NDIN response letters before ingest, as the posture
  has changed twice and could move again.

---

## Bibliography

1. IOM (Institute of Medicine) 2011, *Dietary Reference Intakes for Calcium and Vitamin D* —
   sets the vitamin D tolerable upper intake level (UL) at 4,000 IU/day for adults and the
   "adequacy" serum 25(OH)D target at ~20 ng/mL (50 nmol/L). National Academies Press,
   nap.nationalacademies.org/catalog/13050 — `regulatory` (regulatory DRI / UL figure;
   admissible for regulated upper limit). PAIRED with the Endocrine Society 2011 guideline
   (Holick MF et al., "Evaluation, Treatment, and Prevention of Vitamin D Deficiency: an
   Endocrine Society Clinical Practice Guideline," *J Clin Endocrinol Metab.* 2011;96(7):1911-30,
   PMID 21646368) for the ≥30 ng/mL "sufficiency" threshold and the 10,000 IU/day upper limit —
   `regulatory` (guideline-derived dose & upper-limit figures).
2. Functional-medicine vitamin D target convention (IFM-stated 50–80 ng/mL optimal, ~60–80 ng/mL):
   IFM, "Vitamin D Evaluation: A Clinical Tool in Personalized Medicine," ifm.org/articles/
   vitamin-d-evaluation-personalized-medicine (HTTP-403 on direct fetch; title/venue captured,
   author+date NOT yet captured) — `practitioner_protocol` (venue = IFM; target/dose convention ONLY,
   NOT efficacy). REQUIRES author + date before wiki lock per Tier-2.7 rule.
3. Endocrine Society repletion convention (50,000 IU D3 weekly × 8 wk for 25(OH)D < 20 ng/mL) +
   loading-dose evidence: "Safety and Efficacy of Loading Doses of Vitamin D: Recommendations for
   Effective Repletion," PubMed 39770462, pubmed.ncbi.nlm.nih.gov/39770462/ — guideline-derived /
   `open_label`-supported (dose convention).
4. Veugelers PJ, Ekwaru JP. "A Statistical Error in the Estimation of the Recommended Dietary
   Allowance for Vitamin D." *Nutrients.* 2014 Oct 20;6(10):4472-5. PMID 25333201 / PMC4210929,
   pmc.ncbi.nlm.nih.gov/articles/PMC4210929/ — `mechanism_review` (re-analysis of the IOM's own
   data; argues the IOM RDA of 600 IU/day is underestimated and that ~8,895 IU/day would be
   needed for 97.5% of individuals to reach 50 nmol/L — i.e. MORE intake needed per the dose-
   response than the IOM concluded; figure noted by the authors as beyond the studied dose
   range). NOTE: distinct from PMC3680954 (McKenna MJ, Murray BF, "Vitamin D dose response is
   underestimated by Endocrine Society's Clinical Practice Guideline," *Endocr Connect.* 2013;
   2(2):87-95), which argues the dose-response rate constant should be DOUBLED (2.5→5.0 nmol/L
   per 100 IU) — the OPPOSITE direction — and is therefore NOT the support for D1's "more intake
   needed" claim.
5. Hultman E, Söderlund K, Timmons JA, Cederblad G, Greenhaff PL. "Muscle creatine loading in men."
   *J Appl Physiol (1985)*. 1996 Jul;81(1):232-7. PMID 8828669,
   pubmed.ncbi.nlm.nih.gov/8828669/ — `rct` (20 g×6d and 3 g×28d both → ~20% muscle Cr;
   maintenance 2 g/d; loading framed as optional).
6. ClinicalTrials.gov NCT07176325, "Gastrointestinal and Fluid Retention Symptoms Associated With
   Creatine Monohydrate With and Without Loading Dose Over 28 Days," clinicaltrials.gov/study/
   NCT07176325 — `regulatory` (trial registry; registration only, no results — AE-existence context,
   NOT an AE-rate source).
7. Dodd FL et al. "A double-blind, placebo-controlled study evaluating the effects of caffeine and
   L-theanine both alone and in combination on cerebral blood flow, cognition and mood." PMID
   25761837 / PMC4480845, ncbi.nlm.nih.gov/pmc/articles/PMC4480845/ — `rct` (combination ≠ sum of
   parts; theanine attenuated caffeine CBF/mood effects).
8. Owen GN et al. "The combination of L-theanine and caffeine improves cognitive performance and
   increases subjective alertness." PMID 21040626, pubmed.ncbi.nlm.nih.gov/21040626/ — `rct`
   (combination-specific effects).
9. Chandrasekhar K, Kapoor J, Anishetty S. "A prospective, randomized double-blind, placebo-controlled
   study of safety and efficacy of a high-concentration full-spectrum extract of ashwagandha root in
   reducing stress and anxiety in adults." *Indian J Psychol Med.* 2012 Jul;34(3):255-62. PMID
   23439798, pubmed.ncbi.nlm.nih.gov/23439798/ (PMC3573577) — `rct` (KSM-66 600 mg/day; cortisol
   reduction. NOTE on figure provenance: the ABSTRACT states only that serum cortisol was
   "substantially reduced (P=0.0006)" with NO percentage; the ~28% figure (exact 27.9% reduction
   from baseline in the ashwagandha group vs 7.9% placebo, between-group P=0.002) is from the
   FULL-TEXT RESULTS TABLE, not the abstract. Manufacturer-associated — sponsor bias flag).
10. Martens CR et al. "Chronic nicotinamide riboside supplementation is well-tolerated and elevates
    NAD+ in healthy middle-aged and older adults." PMID 29599478 / PMC5876407,
    ncbi.nlm.nih.gov/pmc/articles/PMC5876407/ — `rct` (NAD+ ELEVATION + tolerability, NOT clinical
    benefit).
11. "Safety evaluation of β-nicotinamide mononucleotide oral administration in healthy adult men and
    women," PMC9400576, ncbi.nlm.nih.gov/pmc/articles/PMC9400576/ — `rct` (NMN safety / tolerability;
    1250 mg/day × 4 wk, n=31, no SAEs. NAD+ NOT measured — authors explicitly state "metabolomic
    analysis of NMN and its metabolites, such as NAD+ ... in the blood and urine samples was not
    performed during the study period"; cannot support an NMN→NAD+ elevation claim).
12. "Dietary Supplementation With NAD+-Boosting Compounds in Humans: Current Knowledge and Future
    Directions," PMC10692436, pmc.ncbi.nlm.nih.gov/articles/PMC10692436/ — `mechanism_review`
    (clinical functional benefit unclear / early).
13. FDA new-dietary-ingredient correspondence on β-nicotinamide mononucleotide (NMN), primary
    regulatory record: FDA NDIN responses to SyncoZymes (NDIN 1247) and Inner Mongolia Kingdomway
    Pharmaceutical Ltd (NDIN 1259). Timeline anchored to the primary FDA letters: (a) NOV 2022 —
    FDA informed both notifiers that NMN is excluded from the dietary-supplement definition under
    the drug-preclusion clause (NMN authorized for investigation as a new drug by MetroBiotech
    before lawful marketing as a supplement); (b) SEP 29, 2025 — FDA responded to the industry
    citizen petition reversing that interpretation, concluding NMN is NOT excluded because it was
    marketed as a supplement (evidence as early as 2017) before the drug authorization; (c) DEC 2,
    2025 — FDA confirmation letters to SyncoZymes and Inner Mongolia Kingdomway setting aside the
    prior exclusion determinations. CURRENT 2026 STATUS: NMN is a LAWFUL dietary ingredient
    retaining NDI status (premarket NDI notification still required) — `regulatory` (regulated-
    status claim). NOTE: the 2022 action canNOT be sourced to the 2021 review PMC9039735, which
    predates it and states the opposite ("no authorising agency to regulate NMN"; NR — not NMN —
    has GRAS); that review is removed as the anchor for this regulatory claim. FDALawBlog /
    NutraIngredients / Natural Products Association coverage corroborate the letter recipients and
    dates; the underlying FDA NDIN letters are the primary record. FLAG: re-verify against the
    posted FDA NDIN response letters before wiki lock.
14. Yi L, Maier AB, et al. "The efficacy and safety of β-nicotinamide mononucleotide (NMN)
    supplementation in healthy middle-aged adults: a randomized, multicenter, double-blind,
    placebo-controlled, parallel-group, dose-dependent clinical trial." PMC9735188,
    pmc.ncbi.nlm.nih.gov/articles/PMC9735188/ — `rct` (NMN 300/600/900 mg/day × 60 d, n=80 healthy
    middle-aged adults; whole-blood NAD concentrations statistically significantly increased in ALL
    NMN groups vs placebo at days 30 and 60, p ≤ 0.001 — the admissible Tier-1 human NMN trial that
    DID measure blood NAD+, supporting the NMN→NAD+ ELEVATION claim; biomarker only, NOT clinical
    benefit).

---

## Self-check

- **Source count:** 14 cited sources across the four sub-topics. ≥6 satisfied. Tier breakdown:
  Tier-1 primary (`rct`/`mechanism_review`) = [4,5,7,8,9,10,11,12,14] ([11] = NMN safety-only,
  NAD+ not measured; [14] = Yi & Maier NMN RCT, the NMN→NAD+ elevation support; note [4] = Veugelers & Ekwaru
  2014 re-analysis, swapped in iter-2 from the mis-attributed McKenna & Murray PMC3680954);
  Tier-2 regulatory/registry (`regulatory`) = [1 (IOM 2011 DRI + Endocrine Society 2011), 3 partial,
  6, 13 (primary FDA NDIN correspondence)]; Tier-2.7 practitioner (`practitioner_protocol`) = [2];
  guideline-derived dose/upper-limit convention = [1,3].
- **Convention-not-trial-validated discipline:** CONFIRMED. Every practitioner/community dose is
  rendered as convention: D1 vitamin D 50–80 ng/mL = "practitioner convention, NOT trial-validated";
  D2 creatine loading = "speed convention, not a necessity," with the originating Tier-1 trial
  explicitly contradicting the necessity framing; D3 stack doses = `combination_evidence: none` /
  inherits weakest rung, branded doses flagged manufacturer-funded + extract-specific. No
  practitioner dose is phrased as "the recommended/safe dose." Where Tier-1 contradicts convention
  (D1 dose-response, D2 necessity), the academic source is given primacy and both reported.
- **≥1 compounding/practitioner source:** SATISFIED at venue level — [2] IFM (`practitioner_protocol`).
  PARTIAL on the Tier-2.7 citation rule: practitioner NAME + DATE are NOT yet captured for [2] (IFM
  page was HTTP-403; examine.com discovery page also HTTP-403). No admissible Tier-3
  `compounding_data_sheet` was located for these OTC supplements (compounding-pharmacy data sheets in
  the whitelist are peptide-oriented; OTC supplements are not compounded). Searched-but-blocked list:
  ifm.org vitamin-D article (403), examine.com ashwagandha page (403). FLAG: re-fetch IFM page with
  an authenticated tool to capture author+date before D1's practitioner cite is wiki-locked.
- **Goal-agnosticism (PF-S2-04):** CONFIRMED. No personalization to the operator; findings describe
  the convention-vs-trial ecosystem generically. Doses reported as conventions/trial figures, not as
  recommendations for any individual.
- **Anti-hallucination:** every claim carries inline `[N, type_tag]`; no fabricated citations; two
  explicit retrieval gaps flagged (≥3-ingredient nootropic stack combination study; Sensoril dose
  primary) rather than filled with invented sources.

---

## Post-fix grep audit

iter-2 remediation OLD→NEW changes and lingering-hit disposition (run against the WHOLE file):

| # | OLD value/attribution | NEW value/attribution | grep regex | hits | disposition |
|---|---|---|---|---|---|
| 1 | "Heaney et al." as D1 dose-response author | Veugelers & Ekwaru 2014 (D1); McKenna & Murray noted as the distinct opposite-direction source | `heaney` | 0 | CLEAN — removed |
| 2 | (new correct attribution) Veugelers & Ekwaru | bib [4], D1 body, self-check | `veugelers` | 3 | OK — all correct attributions (D1 body L35, bib [4] L161, self-check L228) |
| 3 | PMC3680954 mis-attributed to "Heaney/Veugelers" as D1 support | PMC3680954 = McKenna & Murray, cited only as the distinct DOUBLED-rate-constant source explicitly flagged NOT-the-support for D1 | `PMC3680954\|3680954` | 3 | OK — all 3 are corrective/disambiguating (L40 body note, L167 bib note, L229 self-check note) |
| 4 | "Endocrine Society guideline UNDER-estimates the intake needed" (inverted vs cited paper) | "the IOM UNDER-estimated the intake needed" attributed to Veugelers & Ekwaru (their actual claim); McKenna & Murray's opposite direction noted | `under-?estimates? the intake` / `Endocrine Society guideline UNDER` | 0 / 0 | CLEAN — inversion removed |
| 5 | [1] anchoring 4,000/10,000 IU ULs to PMC3680954 (which has no UL discussion) | [1] = IOM 2011 DRI (4,000 IU UL) + Endocrine Society 2011 (10,000 IU, ≥30 ng/mL), tagged `regulatory` | (covered by #3; [1] no longer cites PMC3680954) | n/a | RESOLVED — UL figures re-anchored to regulatory primaries |
| 6 | [13] = PMC9039735 (Aug-2021 review) as source for a "late 2022" FDA action it predates | [13] = primary FDA NDIN correspondence (SyncoZymes NDIN 1247, Kingdomway NDIN 1259), Nov-2022→Sep-2025→Dec-2025 timeline | `PMC9039735\|9039735` | 1 | OK — sole hit (L216) is a corrective NOTE stating it CANNOT anchor the claim and is removed as anchor |
| 7 | "late 2022" sole timestamp on a now-reversed FDA posture | full Nov-2022 exclusion → Sep-29-2025 reversal → Dec-2-2025 confirmation; 2026 status = NMN lawful NDI | `late 2022` | 0 | CLEAN — replaced with precise dated arc |
| 8 | "NMN excluded" as a settled present-tense framing | divergence-then-convergence framing; current status lawful | `NMN excluded` | 0 | CLEAN — stale settled framing removed |
| 9 | bare "~28%" cortisol with no section anchor | "~28% (exact 27.9%) ... from the FULL-TEXT RESULTS TABLE, not the abstract" + [9] note | `~?28%\|27\.9` | 2 | OK — both hits (L98 body, L192 bib) now carry the full-text-results-table anchor |

All lingering hits are intentional corrective/disambiguating mentions; no OLD attribution survives as live support for any claim.

### iter-3

Issue: the conjoined claim "NR and NMN reliably RAISE blood NAD+ ... and are well-tolerated
[10, rct (NR); 11, rct (NMN)]" over-attributed — [11] (PMC9400576) is an NMN safety/tolerability
trial that explicitly did NOT measure NAD+ (verified by fetch: authors state "metabolomic analysis
of NMN and its metabolites, such as NAD+ ... in the blood and urine samples was not performed during
the study period"), so it cannot support the NAD+-elevation half. Fix: disaggregated the claim —
attributed NAD+ elevation for NR to [10], ADDED an admissible Tier-1 human NMN RCT ([14], Yi & Maier
2023 / PMC9735188; verified by fetch: NMN 300/600/900 mg/day × 60 d, n=80, whole-blood NAD+
significantly increased in all NMN groups vs placebo at days 30 & 60, p ≤ 0.001) as the NMN→NAD+
elevation support, and re-rendered [11] as NMN tolerability ONLY (NAD+ not measured).

OLD→NEW changes:

| # | OLD value/attribution | NEW value/attribution | grep regex | hits | disposition |
|---|---|---|---|---|---|
| 1 | "NR and NMN reliably RAISE blood NAD+ ... [10, rct (NR); 11, rct (NMN)]" (conjoined; [11] over-attributed) | NR NAD+ rise → [10]; NMN NAD+ rise → [14, Yi & Maier]; [11] = NMN tolerability only, NAD+ not measured | `\[11` | 4 | OK — L114 body, L137-138 caveat, L205 bib, L243 self-check all render [11] as safety/tolerability ONLY ("NAD+ not measured"); none attribute NMN→NAD+ elevation to [11] |
| 2 | bib [11] descriptor "NMN safety / NAD+ elevation" | "NMN safety / tolerability (1250 mg/day × 4 wk, n=31, no SAEs; NAD+ NOT measured ... cannot support an NMN→NAD+ elevation claim)" | `PMC9400576` | 2 | OK — both hits (L205 bib, L208 within bib note) carry corrected descriptor |
| 3 | (no NMN NAD+-elevation primary existed) | [14] Yi & Maier 2023 PMC9735188 added as the admissible NMN→NAD+ elevation source | `\[14\|PMC9735188\|Yi & Maier` | 4 | OK — L112 body, L137 caveat, L233-235 bib, L244 self-check; all correct attributions of NMN→NAD+ elevation |

No surviving claim attributes NMN→NAD+ elevation to [11]; the [11] bib descriptor is corrected to
tolerability-only; an admissible Tier-1 NMN-NAD+ source ([14]) was added rather than dropping the claim.
