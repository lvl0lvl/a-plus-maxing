# Gate 6 — Critique / Red-Team
**Draft:** `vault/library/peptides/kisspeptin-10/research-report.md`
**Critique agent ID:** `critique-kp10-deep`
**Date:** 2026-06-21
**Iterations:** 1

---

## Verdict

verdict: PASS

```json
{
  "phase": "6",
  "verdict": "PASS",
  "iterations": 1,
  "critique_agent_id": "critique-kp10-deep",
  "draft_path": "vault/library/peptides/kisspeptin-10/research-report.md",
  "findings": [
    {
      "category": "citation-incomplete",
      "severity": "minor",
      "description": "Two regulatory sources (WADA 2026 PDF and FDA PCAC briefing PDF) were unavailable at fetch time (403/404). The report discloses both fetch failures, which is correct practice, but a reader relying on these for enforcement decisions cannot verify the exact statutory language. No missing-substance problem — the disclosed fetch-failure plus secondary cross-referencing is acceptable — but the disclosure language in the bibliography is more prominent in the source sections than in the final report bibliography entries, where it is visible only on close reading. This is minor: the disclosures are present and honest."
    },
    {
      "category": "balance-issue",
      "severity": "minor",
      "description": "The report documents that the 2022 and 2023 JAMA Network Open HSDD trials found pharmacodynamic fMRI and tumescence effects, but neither study reported any psychometric long-term sexual-function improvement on validated scales (e.g., FSFI, IIEF) with sustained follow-up. The report correctly notes that neither trial was powered for long-term clinical efficacy, but does not explicitly state that validated composite sexual function scales (beyond a single 'happiness about sex' p=.02 item) were not primary endpoints in either HSDD trial. A consumer reading this entry could reasonably infer more comprehensive psychometric support than exists. This is minor given the caveat language present, but a one-line clarification would sharpen the endpoint distinction."
    },
    {
      "category": "missing-perspective",
      "severity": "minor",
      "description": "The report notes the 2022 JAMA women's HSDD trial enrolled 32 premenopausal women but does not note the 40 randomized / 32 completing the crossover discrepancy (8 dropouts, ~20%). This is consistent with the published paper, but the 20% dropout rate in a crossover design is information a critical reader would want — in IV crossover studies, dropouts often reflect IV administration burden. This is minor: the report is accurate; the dropout detail would add context for evaluating whether the effect is maintained in a 'real-world' convenience sample."
    },
    {
      "category": "alternative-explanation",
      "severity": "minor",
      "description": "The report attributes the women's HSDD fMRI deactivation pattern (left inferior and middle frontal gyri) to reduced sexual inhibition consistent with the dual-control model of sexual response. This is the authors' interpretation but it is contested in the fMRI-HSDD literature: deactivation of frontal regions during erotic stimuli is observed in healthy volunteers too, and the claim that HSDD-specific frontal hyperactivation was 'reduced' by kisspeptin rests on between-group assumptions that are not stated in the report. The report does not need to resolve this debate, but noting that the fMRI deactivation pattern interpretation is model-dependent (not observer-independent) would strengthen objectivity. Minor — the report already caps the interpretation at mechanistic rather than clinical."
    }
  ],
  "additional_retrievals": [],
  "halt_reasons": []
}
```

---

## Detailed Prose

### Probe 1 — KP-10 vs. KP-54 confound (load-bearing)

**Finding: PASS — clean attribution throughout.**

This was the highest-stakes concern and the report handles it with exceptional discipline. The KP-10 / KP-54 distinction is:

- Stated in the metadata block at the very top of the entry ("KP-10's own direct human evidence is limited to approximately three small trials").
- Made the organizing principle of Section 2.1 ("Framing: KP-10 vs. KP-54") and carried through every subsection with an explicit isoform column in the HPG evidence summary table.
- Restated in Section 3.1 ("the fMRI and HSDD trials used KP-54... not KP-10") and Section 4.1.
- Applied in Section 2.6 with a dedicated "Critical note before reading this subsection" header for IVF.

At no point does the report silently credit KP-54's clinical outcomes to KP-10. The Jayasena 2015 head-to-head is used correctly as pharmacological bridge evidence (per-receptor-occupancy equivalence) while the plasma-exposure and half-life gap is stated repeatedly as the reason dosing numbers do not translate. This probe finds no problem.

### Probe 2 — Single-center sexual evidence ceiling

**Finding: PASS — stated with full force, not buried.**

The Caveat 2 in the Summary block and the entire Section 3.5 explicitly name Imperial College London (Comninos/Dhillo group) as the sole source of all five human fMRI/HSDD RCTs. The report:

- Names the specific research group and institutional address.
- States "No independent group has run a confirmatory kisspeptin fMRI or HSDD efficacy study" in plain language.
- Uses the phrase "promising-but-single-center-unreplicated" in the metadata and section header.
- Distinguishes surrogate endpoints (fMRI activation, tumescence, questionnaire items) from long-term clinical outcomes.
- The Concentration Note in the Summary preserves the two-tier distinction: ~45-55% broad field; ~100% sexual sub-literature.

**Minor finding:** The report correctly states penile tumescence (objective) and "happiness about sex" (psychometric) as the key HSDD outcomes in men. However, for the women's HSDD trial, the primary fMRI endpoints were deactivation patterns plus self-reported "sexiness" (p=.04). The report does not explicitly note that no validated composite desire instrument (e.g., FSFI, Decreased Sexual Desire Screener) constituted the primary endpoint in either HSDD trial. This is not an error — those instruments were secondary or not used — but the balance-issue minor finding reflects that the endpoint characterization in the prose slightly undersells how surrogate the evidence remains. Filed as minor `balance-issue`.

### Probe 3 — Desensitization risk for naive grey-market dosing

**Finding: PASS — stated as a genuine risk, not buried.**

Section 1.6 is titled "The Bolus-Stimulates / Continuous-Desensitizes Pharmacodynamic Dichotomy" and opens with the sentence: "The most clinically critical pharmacodynamic property of KP-10 — and the one most systematically ignored in grey-market promotion." This is not a caveat buried in a footnote. The Caveat 3 in the Summary block states the Day-14 tachyphylaxis datum (LH 24.0 → 2.5 IU/L) with full numbers. Section 5.2 translates the desensitization risk directly into grey-market language: "Continuous or frequent high-dose KISS1R stimulation causes β-arrestin-mediated receptor internalization and HPG suppression rather than stimulation. Daily or frequent KP-10 use without clinical titration risks near-complete tachyphylaxis within approximately 14 days."

The bolus-dose signal (3 µg/kg blunting relative to 1 µg/kg) and the continuous-infusion desensitization (5-hour LH decline in HA women) are both documented in separate subsections. The risk is triple-sourced across George 2011, Jayasena 2009, and Jayasena 2014. No problem here.

### Probe 4 — Alternative-explanation / over-claim for libido/testosterone therapy

**Finding: PASS with minor alternative-explanation finding.**

The report does not at any point state or imply that KP-10 is an "established libido/testosterone therapy." The Caveat 4 explicitly states no FDA approval exists and 503A compounding is closed. The regulatory status section is detailed and accurate. The grey-market section in 5.2 is appropriately cautionary.

**Minor finding (alternative-explanation):** The report describes the women's HSDD trial fMRI deactivation pattern (left inferior/middle frontal gyri) using the framing that this represents "reduced neural correlates of sexual aversion" — which is the authors' model-dependent interpretation from the dual-control model of sexual response (Bancroft & Janssen). An alternative explanation is that frontal deactivation during erotic stimuli is common in healthy volunteers, and the clinical significance of the observed difference depends on between-subject baseline comparisons that are not presented in the report. The report already limits interpretation to "pharmacodynamic effects" without claiming clinical utility, so this is minor.

### Probe 5 — Concentration honesty: field-broad vs. sexual sub-literature

**Finding: PASS — two-tier distinction preserved correctly.**

The Concentration Note in the Summary block is the key test. The report states: "Estimated Imperial share of the full human-translational literature is approximately 45–55%... However, the human sexual-brain and HSDD sub-literature — which is the primary basis for consumer 'libido' claims — is effectively 100% Imperial-concentrated with no independent replication." This is exactly the right two-tier formulation. The number (45-55%) is sourced from Section 5.1 where four independent human-dosing groups are verified with named institutions and publication examples. The ~100% HSDD sub-literature figure is accurate — all five RCTs originate from Imperial. No collapse to a single misleading figure. This probe finds no problem.

### Probe 6 — Unexamined counter-evidence: null/negative studies

**Finding: PASS — no significant omitted negative evidence identified.**

The kisspeptin literature does not have prominent null or retracted RCTs. The key negative finding within the literature is the tachyphylaxis result itself (Jayasena 2009: twice-daily dosing collapses LH by Day 14), and the blunted response at 3 µg/kg IV bolus (George 2011). Both are documented. The report does not suppress these; they are the organizing evidence for the desensitization risk section.

No major independent null study was omitted. The lack of Phase 3 trial data is stated. The report notes the MVT-602 pipeline status (no Phase 3 registered as of mid-2026) and that Myovant's program continuation is unconfirmed post-acquisition — which is the closest thing to "negative pipeline evidence" in this field.

### Probe 7 — PT-141 / bremelanotide attribution

**Finding: PASS — correct throughout.**

The report correctly attributes bremelanotide/Vyleesi as the FDA-approved HSDD peptide with distinct mechanism (MC4R/MC3R agonist, dopaminergic/oxytocinergic pathway, not GnRH/limbic). The approval date (June 2019), trial scale (two 24-week Phase 3 RCTs, n=1,247 women), and mechanism are all accurate. The report explicitly states: "KP-10's approval status, trial scale, and administration route are all substantially less mature than bremelanotide's." The compound-class context section (3.4) maintains clear mechanistic separation between kisspeptin (HPG/limbic command), bremelanotide (mid-level arousal), and MT-II (non-selective melanocortin, unapproved). No merger of evidence bases.

### Probe 8 — Bias from Imperial COI

**Finding: PASS — COI disclosed and characterized accurately.**

Section 4.5 notes Dhillo and Abbara's consulting fee relationships with Myovant Sciences and correctly characterizes them as "circumscribed" — relevant to IVF/analog development work (where Myovant funded trials) but not to the foundational HPG stimulation or HSDD mechanistic studies. The report does not suppress the COI; it names it and distinguishes where it applies. The HSDD studies do not carry Myovant funding (the 2017 JCI study declared no conflicts; the two 2022-2023 JAMA Network Open HSDD trials disclose Myovant consulting but for non-Myovant-funded work). The COI characterization is accurate and balanced.

### Additional retrievals dispatched

None. The report's handling of all key probe areas was sufficiently clear from reading the draft and source sections that targeted counter-claim retrievals were not necessary to verify or refute specific assertions.

---

## Summary judgment

The research report is thorough, mechanistically accurate, and handles the load-bearing KP-10/KP-54 confound better than most clinical research literature does — it is the organizing logic of the entire entry rather than a footnote. The desensitization risk is stated with full force and grounded in human data. The single-center ceiling for sexual evidence is named plainly. The concentration distinction between the broad field (~45-55% Imperial) and the sexual sub-literature (~100% Imperial) is preserved in both the Summary and the body. Four minor findings were identified — none critical, none justifying a HALT. The verdict is PASS.
