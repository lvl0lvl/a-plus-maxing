# Gate 7.5 — Risk-Floor Verifier (reference-landscape adaptation)

**Phase:** 7.5 RISK-FLOOR
**Target:** `design/.supplement-specialist-design-work/domain-research.md`
**target_type:** reference (goal-agnostic LANDSCAPE substrate — NO single compound entry was written this dispatch)
**Rule:** `.claude/skills/aplus-research/references/health-gates.md` §2
**Verified:** 2026-05-29

## Adaptation note

This dispatch's target is a goal-agnostic LANDSCAPE reference substrate, not a single
`risk_tier: experimental` compound entry with template fields to parse. The per-entry §2
procedure ("read the draft compound entry at the planned output path; parse the four named
fields") does not apply verbatim — there is no one entry. The adapted job: verify the
substrate demonstrates that the four risk-floor fields are FILLABLE from the retrieved
evidence, at the class level with citations, for the experimental/high-risk-tier
supplements/nootropics the landscape covers — so a future per-compound entry could pass
the per-entry gate. The experimental/high-risk set assessed: green-tea-extract/EGCG, kava,
ashwagandha, sustained-release niacin, phenibut, tianeptine, kratom, yohimbine, high-dose
B6/fat-soluble-vitamin/mineral toxicity tier, SJW (interaction hazard), and the
banned/gray-market class (ephedra, DMAA/DMHA, SARMs, MK-677-class research nootropics
named at F15 item 8 as the experimental floor the deep-mode dispatch covers).

## Per-field assessment

### Field 1 — adverse effects (literature) → FILLABLE

Non-empty and densely cited at class level for the entire experimental/high-risk set.

- F7 / R7 (lines 111-121, 255) — botanical + high-dose-vitamin DILI: green-tea-extract/EGCG
  hepatocellular injury, ~9% fatal, EGCG 140-1,000 mg/day [25, mechanism_review]; kava
  hepatitis/cirrhosis/liver failure, ≥9 cases + 1 death + 3 transplants [26]; ashwagandha
  cholestatic/mixed injury 2-12 wk onset, rare fatal/transplant [27]; sustained-release
  niacin acute hepatic necrosis [28].
- F10 / R11 (lines 155-165, 263) — gray-zone dependence/overdose AEs: phenibut tolerance/
  dependence/severe withdrawal (agitation, delirium) [36]; tianeptine opioid toxicity,
  poison-center 11→151 in 2020 [37]; kratom dependence/respiratory depression/overdose
  death [38]; yohimbine GI 46% / tachycardia 43% / anxiety 33% / hypertension 25% [39].
- F6 (lines 97-107) — toxicity-ceiling AEs: B6 sensory neuropathy at 1-6 g/day [22];
  vitamin A teratogenicity [17]; vitamin D hypercalcemia [18,24]; selenosis [19];
  zinc-copper antagonism [20].

Verdict: populated.

### Field 2 — contraindications → FILLABLE

Non-empty and cited at class level.

- F7 (line 119-121) — pre-existing liver disease (ashwagandha, esp. prior liver disease);
  HLA-B*35:01 carriers (GTE pharmacogenomic risk) [25,27].
- F8 / R8 (lines 125-135, 257) — SJW contraindicated against cyclosporine, tacrolimus,
  HIV protease/NNRTI agents, warfarin, digoxin, oral contraceptives (CYP3A4/P-gp induction);
  serotonergic stacking SJW + SSRI/SNRI [29,30]; additive bleeding (ginkgo/garlic/vitamin E/
  ginger/fish oil + warfarin/surgery) [31].
- F10 (line 161-165) — opioid/dependence context for phenibut/tianeptine/kratom.
- F6 (line 105) — pregnancy (vitamin A teratogenicity-driven ceiling); life-stage-conditional ULs.

Verdict: populated.

### Field 3 — monitoring → FILLABLE, third-party biomarker PRESENT

Non-empty AND at least one item references a third-party lab assay / biomarker (not purely
subjective). Named objective assays in the substrate:

- **Serum/urine calcium** — hypercalcemia + hypercalciuria dose-response, Billington 2020
  Calgary RCT (0/3/9% and 17/22/31% at 400/4,000/10,000 IU/day) [24, rct] (F6, line 101).
- **Serum 25(OH)D** — named monitored biomarker, regulatory vs functional-medicine target
  ranges [51,52] (F15, line 229).
- **HLA-B\*35:01 genotyping** — named pharmacogenomic lab assay gating GTE hepatotoxicity
  risk (72% of confirmed cases vs 5-15% population) [25, mechanism_review] (F7, line 115).
- **Liver-function monitoring** — implied/required by the hepatocellular/cholestatic DILI
  framing and "acute hepatic necrosis" for GTE/kava/ashwagandha/SR-niacin [25-28] (F7).
- **Whole-blood NAD+** — measured biomarker for NAD+ precursors, p ≤ 0.001 [61, rct];
  serum cortisol for ashwagandha [57, rct] (F15, line 229).

At least one third-party biomarker (serum/urine calcium, serum 25(OH)D, HLA-B*35:01 assay,
whole-blood NAD+, serum cortisol) is explicitly named and cited. Third-party marker present: YES.

Verdict: populated; third-party monitoring marker requirement satisfied.

### Field 4 — stopping criteria → FILLABLE as concept (requirement visible)

Per §2 Override, library/landscape entries may render stopping criteria as
`*(operator-specific — populated per trial)*`, but the section header and the requirement
must be visible. The substrate makes the requirement visible and supplies the class-level
inputs a per-trial stopping rule would draw on:

- F15 item (5) (line 231) — the inherited contract pack mandates the operator-profile R7
  read-before-`vault/compounds/*`-write precondition with a HALT on an unpopulated
  hard-limit field, i.e. the per-compound entry machinery into which stopping criteria are
  populated per trial. F15 item (3) GRADE strong-on-low-certainty HALT is the companion gate.
- F7 (line 119) — discontinuation triggers are implicit in the DILI onset windows
  (ashwagandha 2-12 wk; "stop on rising LFTs / jaundice") — class-level stopping inputs.
- F10 (line 159) — phenibut withdrawal is managed by a baclofen taper with recovery up to
  ~6 months: a concrete stopping/tapering protocol concept for the dependence class [36].

The requirement is visibly present and the field is fillable per-trial; for this
operator-agnostic landscape substrate it correctly resolves to the operator-specific
placeholder rather than a single hard-coded rule.

Verdict: present as concept; requirement visible; fillable per-trial.

## Verdict

```
verdict: PASS
target_type: reference (landscape substrate — no single compound entry written this dispatch)
risk_tier_set_assessed: experimental + high (GTE/EGCG, kava, ashwagandha, SR-niacin,
  phenibut, tianeptine, kratom, yohimbine, high-dose B6/vitamin/mineral, SJW, banned/
  gray-market incl. MK-677-class research nootropics)
required_fields:
  adverse_effects_literature: fillable
  contraindications:          fillable
  monitoring:                 fillable
  stopping_criteria:          fillable (concept present; operator-specific per-trial)
fields_fillable: 4/4
third_party_monitoring_marker_present: true
third_party_markers: [serum/urine calcium, serum 25(OH)D, HLA-B*35:01 genotyping,
  whole-blood NAD+, serum cortisol]
halt_reasons: []
```

All four risk-floor fields are demonstrably fillable from the retrieved evidence for the
experimental-tier set, and at least one third-party monitoring biomarker (objective lab
assay) is present. A future per-compound entry derived from this substrate has the cited
class-level material needed to populate each of the four §2 fields and pass the per-entry
risk-floor gate. This is the reference-landscape adaptation — no single `risk_tier:
experimental` compound entry was written this dispatch.
