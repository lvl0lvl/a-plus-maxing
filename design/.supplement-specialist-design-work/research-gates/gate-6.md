# Gate 6 — CRITIQUE (deep-mode red-team)

Agent: Phase-6 critique, separate from synthesis. Target draft: `design/.supplement-specialist-design-work/domain-research.md` (397 lines, F1-F15 + R1-R18 + 68-entry bibliography + 4 design surfaces). Type-tag enum: `vault/library/_source-whitelist.md`. Epistemic walk: 8-category probe applied.

## Coverage gaps

The hazard taxonomy is broad and well-stratified. Adulteration (F9), toxicity ceilings (F6), hepatotoxicity (F7), pharmacokinetic + pharmacodynamic interactions (F8), the dependence gray-zone (F10), anti-doping strict-liability (F11), and the four regulatory-status findings (F12-F14) cover the canonical supplement-domain hazard surface. The four-rung maturity model (F1/F5) is coherent and applied consistently per-compound AND per-outcome (creatine strength Rung 1 vs cognition Rung 2-3 is the cleanest demonstration). No critical class of hazard is missing. Advisories:

- **A1 (advisory) — Pediatric / pregnancy population conditioning is thin.** F6 cites vitamin A teratogenicity as the critical effect but the draft never states the obvious downstream rule: a UL/teratogenicity gate behaves differently for a pregnancy-context query. The EFSA B6 opinion (confirmed by retrieval R-ret-1) sets the 12 mg/day UL explicitly *including* pregnant/lactating women and derives child ULs by allometric scaling. F6 is goal-agnostic-correct to omit operator personalization, but a *class-level* "ULs are life-stage-conditional (pregnancy, pediatric)" caveat is a missing edge-case anchor. Fix: add one sentence to F6 caveats — "ULs are life-stage-conditional; teratogenic ceilings (vitamin A) and the EFSA B6 UL apply with different margins in pregnancy/pediatric populations" — so the design doc can author a life-stage Edge Case. Non-blocking (the agent's R7 operator-profile precondition + medical-liaison escalation backstop this).

- **A2 (advisory) — Iron acute-toxicity / pediatric-ingestion hazard understated.** F6 lists iron UL 45 mg/day as a chronic ceiling but omits that iron is the single most common cause of fatal pediatric supplement poisoning (acute overdose, distinct from the chronic UL). This is a high-prevalence supplement-domain hazard pattern that the draft's own "more is worse" frame would benefit from. Fix: one clause in F6 distinguishing iron's *acute* overdose hazard from its chronic UL. Non-blocking.

- **A3 (advisory) — No explicit "excipient / botanical-allergen / contaminant-metal" sub-class.** Heavy-metal contamination (lead/arsenic/cadmium in botanicals and protein powders) is a documented supplement-domain hazard distinct from both the pharmaceutical-adulteration mode (F9) and species-substitution (F9). F9 covers undeclared *drugs* and species mismatch but not the heavy-metal contamination mode. Fix: add a clause to F9 caveats noting heavy-metal contamination as a third contamination mode requiring its own detection (ICP-MS), parallel to the existing "DNA vs LC-MS" two-mode note. Non-blocking — the third-party-testing mitigation (USP Verified audits for contaminants) already partly covers it.

None of A1-A3 is a critical gap; each is a one-clause addition to an existing finding's caveats, not a missing finding.

## Balance & counter-evidence

Balance is genuinely good and survives the over-skew-to-hazard probe. Strong-evidence compounds are given fair due and are NOT laundered into universal endorsement:
- Creatine Rung 1 for strength with named effect sizes + CIs (F1), AND its weaker cognition rung (F5/F16-cite) — both directions reported.
- Vitamin D / omega-3: the VITAL null (F5) is reported as a finding, not filtered. The draft uses VITAL precisely to make the "high rung ≠ positive result" point — this is the correct anti-cherry-pick move.
- Melatonin and caffeine are named in the Executive Summary thesis as established-rung but (advisory A4) **caffeine and melatonin have no dedicated finding or citation**. They appear only in prose. For a supplement-specialist substrate this is a thinness: caffeine (dependence/tolerance/anxiety/CV dose-response) and melatonin (dose-timing, next-day grogginess, the well-documented OTC-melatonin overdosing/label-inaccuracy literature) are two of the highest-prevalence OTC compounds Walter is likely to query. Fix: either add a short finding or explicitly scope them out in §0. Currently they are asserted as Rung-1 anchors in the Exec Summary without a finding to anchor a behavioral rule — a confidence-calibration gap (EH probe). **Advisory, not blocking**, because the maturity-ladder *method* (F1/F5) tells the agent how to place them even absent a dedicated finding.

Hazard-overstatement probe (the converse): the draft is disciplined. Each hazard carries a down-calibrating caveat:
- F9 explicitly guards against over-generalizing the 47-89% adulteration figures to single-ingredient USP-verified vitamins ("base rates far lower").
- F8 downgrades additive-bleeding to `cohort`/case-level and flags 5-HTP serotonin-syndrome as *theoretical* (no confirmed monotherapy case) vs SJW+SSRI documented — exactly the right asymmetry.
- F10 reports synephrine CV evidence as *genuinely conflicting* (case-series signal vs ~30 RCTs null) and downgrades certainty rather than picking the scary side.
- F3 marks the industry-funding RR 1.31 as CI-crossing-1.0 ("documented risk, unestablished magnitude," not "proven inflation").
No hazard is overstated beyond its evidence. This is the strongest dimension of the draft.

## Logical consistency

Mechanism-vs-outcome separation is held uniformly and is the spine of the document:
- F2 is the explicit two-column rule (NMN raises NAD+ but null on glucose/lipid endpoints; resveratrol activates SIRT1 in vitro but the human SIRT1 meta-analysis failed to move) — no mechanism→efficacy laundering.
- The `in_vitro` resveratrol 8-fold SIRT1 figure [6] is explicitly fenced off from any human-outcome claim, with [7] (human meta-analysis) named as the admissible human anchor. Animal→human is fenced (NMN mouse-vs-human translational gap named as the cause of the human null).
- Vendor→numerical: [8] (vendor_label, Transparent Labs) is restricted to brand-ownership/standardization-% and never efficacy/dose/AE — checked, correct.
- Convention→trial-validated: F15/R16 render every practitioner dose (IFM 50-80 ng/mL D target, creatine loading) as "practitioner convention, not trial-validated," with the Tier-1-wins-on-contradiction rule. The creatine-loading example (Hultman 1996: 3 g×28d reaches the same saturation as 20 g×6d) is the correct disconfirming anchor.
- class-never-substitutes-for-compound-evidence (F1) is applied uniformly: marketing class ("adaptogen"/"nootropic") is explicitly barred as a credibility proxy.

One internal-consistency nit (advisory A5): the Self-check claims "68 numbered literature entries" and explains the [15] gap as intentional, but the prose Exec Summary says "15 Findings... and 18 Recommendations." The finding/rec counts are internally consistent (F1-F15, R1-R18 both verified by count). No logical inconsistency in the finding set itself. The [15]-gap rationale is plausible but slightly strained ("kept its source-section number") — cosmetic, not load-bearing.

No finding launders mechanism→efficacy, animal→human, vendor→numerical, or convention→trial-validated. Logical consistency: PASS.

## Citation spot-checks

Five load-bearing claims spot-checked against bibliography + type-tag enum:

1. **F6 / R6 — EFSA B6 UL 12 mg/day (the 8-fold IOM-vs-EFSA divergence).** Cite [23] EFSA 2023, PMC10189633, tagged `regulatory`. **Retrieval R-ret-1 (WebSearch) confirms**: EFSA 2023 set the adult UL at 12 mg/day (PMC10189633 resolves; the EFSA Journal DOI 10.2903/j.efsa.2023.8006 is live). The IOM-100-vs-EFSA-12 framing is correct (IOM 2000 UL = 100 mg/day; the prior *EU* SCF figure was 25 mg/day, which the draft does NOT confuse with the IOM 100). Claim VERIFIED, type-tag correct.
2. **F12 — DSHEA post-market-only / FDA-does-not-pre-approve.** Cite [42] FDA Q&A, [43] 21 CFR 111.70/.75/.80, both `regulatory`, both fda.gov / accessdata.fda.gov (Tier 2 whitelist). Type-tag correct; the quoted FDA language is a verbatim-style quote and maps to BASIS_NOT_REVIEWABLE — admissible-as-cited.
3. **F3 — industry-sponsorship RR 1.31 (95% CI 0.99-1.72).** Cite [10] Chartres 2016 JAMA Intern Med, PMID 27802480, `meta_analysis`. The draft correctly reports the CI crosses 1.0 and labels it "documented risk, unestablished magnitude" — no overclaim. Type-tag correct.
4. **F4 — curcumin 57×/30× and 185× (114×/277×) bioavailability factors.** Split across two papers [12] Flory 2021 (57×/30×) and [13] Schiborr 2014 (185×), both `rct`, both with PMIDs (34665507 / 24402825). The draft explicitly states no number is shared across the two papers and that all are RELATIVE (formulation vs native), not absolute — the exact discipline that prevents vendor-chart laundering. Type-tag correct.
5. **Contract-pack / F15 — AUTHORITY_FRAMING_BYPASS mandatory + 81.8% + A3.** Verified directly against `templates/refusal-class-taxonomy.yaml`: `mandatory_for_every_specialist: true` (line 69), statutory_anchor medRxiv 2026.02.26.26347212 "81.8% of successful jailbreaks" (line 62), Walter A3 rationale (line 70). The draft correctly marks 81.8% as **CONTRACT-INHERITED, not corpus-verified here** — proper no-self-attest discipline. VERIFIED.

**Goal-agnosticism (PF-S2-04):** confirmed. Spot-read of all 15 findings + 18 recs: every claim is stated at class/population level. No "best for Walter," no ranking, no operator pre-filtering. Null results carried as findings. PASS.

**Surfaced CONTRADICTION (the load-bearing check):** The template-vs-commit contradiction is **correctly flagged, not buried**. Verified mechanically: commit 0514f2d ("dispatch-flip: medical-liaison live adjudicator; deprecate pre-Role-7 fallback (BC-1)") deprecates the fallback, while `templates/refusal-class-taxonomy.yaml:22` STILL carries verbatim `escalation: medical-liaison (Role 7) when deployed; otherwise operator-acknowledged-override + vault/meta/contradictions.md log` (and line 41 carries a second `or operator-acknowledged-override`). The draft surfaces this in THREE places — F15 Claim, F15 Caveats/CONTRADICTION block (with the explicit "must NOT be inherited until the template is reconciled" directive), and the Methodology Residual-WARNs. R18 also encodes the LIVE-Role-7 escalation "NOT the deprecated pre-Role-7 fallback." This is exactly the prominence the contradiction warrants. PASS — and the design doc has a clean instruction to encode the live escalation.

## Design-readiness

The finding set + R1-R18 is sufficient to author every required `agent.md` section. Mapping verified — every finding carries an explicit `→ consumes:` line routing it to Identity / Core Rules / Refusal taxonomy / Tools / Anti-Patterns / Edge Cases:

- **Identity:** F1/F5 (maturity discriminator + monograph backbone), F2 (two-column) — anchored.
- **Core Rules:** UL gate (F6), hepatotox class hazard (F7), interaction-screen (F8), adulteration signature (F9), DSHEA frame (F12), status-disambiguation card (F13), per-compound maturity_rung (F1) — all anchored with named numbers.
- **Refusal classes:** AUTHORITY_FRAMING_BYPASS (mandatory, contract-verified), BASIS_NOT_REVIEWABLE (F12/F13/F14), gray-zone/non-lawful-ingredient block (F10/F14), H1/H2 auto-block coupling (F14) — ≥4 distinct classes available.
- **Tools (deep-mode dispatch):** R18 + F15 item-8 give the exact dispatch contract: `aplus-research --mode=deep --target-class=compound`, never bare `deep-research`; concentration-audit/population-mismatch/type-tag enforcement on returns; NO gate self-attestation. Write surface (`vault/compounds/` + `vault/protocols/supplement-stack`, no `vault/library/` tree) verified against existing repo dirs. Mechanically clean.
- **Anti-Patterns:** class-as-credibility-proxy, mechanism-as-efficacy, "more is better," "natural = safe," practitioner-convention-as-validated, stack-from-single-ingredient-data, inheriting the stale template fallback — a rich set, each traceable to a finding.
- **Edge Cases:** same-compound-different-rung, high-potency B-complex, pre-existing liver disease + HLA-B*35:01, tested-athlete conditionality, GRAS self-affirmation gradient, NMN status-shift, 50-80 ng/mL target, creatine loading, LIVE-Role-7 escalation — abundant.

Thin-finding probe (which findings are too thin to anchor a rule?):
- **F11 (anti-doping strict-liability)** is population-conditional and largely a consequence-multiplier on F9's contamination base rate. It anchors a *conditional* Edge Case (tested-athlete pool) — adequate, not thin, but the design doc should treat it as a sub-case of F9 rather than a standalone Core Rule.
- **Caffeine/melatonin (A4):** as noted, these are Exec-Summary assertions without a finding — the ONLY place the substrate names a Rung-1 anchor it does not separately evidence. The maturity-ladder method covers the gap, so this is advisory not blocking, but it is the single weakest spot for design-readiness.

The `basis-not-fully-reviewable` flags (H1-H8 exact composition, GRADE/anti-sycophancy canonical wording live in Role-1/Role-2 design docs not read this dispatch) are correctly disclosed and correctly NOT self-attested — the design doc author must read those source docs for exact wording, which the draft tells them to do. This is honest scoping, not a gap.

## Verdict

The substrate is wiki-defensible and complete enough to anchor the specialist design doc. Hazard coverage is broad, the four-rung maturity model is coherent and uniformly applied, mechanism/outcome separation holds throughout, balance is genuinely two-sided (strong-evidence compounds given fair due; no hazard overstated), citation + type-tag discipline survives spot-checking, and the load-bearing template-vs-commit contradiction is surfaced prominently and verified mechanically against the actual commit and template line. The advisories (A1-A5) are each a one-clause caveat addition or an explicit scope-out (caffeine/melatonin), not a missing finding — none blocks design-doc authoring because the maturity-ladder method and the R7/medical-liaison backstops cover the residual.

verdict: PASS

PASS-with-advisory. Recommended (non-blocking) improvements for the design-doc author to fold in:
- A1: add a life-stage-conditionality caveat to F6 (pregnancy/pediatric UL margins).
- A2: distinguish iron's acute pediatric-overdose hazard from its chronic UL in F6.
- A3: add heavy-metal contamination as a third contamination mode in F9 caveats (ICP-MS detection).
- A4: add a short caffeine + melatonin finding OR explicitly scope them out in §0 — currently asserted as Rung-1 anchors in the Exec Summary with no finding to anchor a behavioral rule. Highest-value advisory.
- A5 (cosmetic): the [15]-gap rationale in Self-check is strained; trivial.

Retrievals run (1 of 3 budget): R-ret-1 WebSearch — "EFSA 2023 vitamin B6 tolerable upper intake level 12 mg" — confirmed F6/R6 load-bearing B6 UL claim (EFSA 2023 adult UL = 12 mg/day, PMC10189633 / DOI 10.2903/j.efsa.2023.8006 live; IOM-100-vs-EFSA-12 framing correct).
