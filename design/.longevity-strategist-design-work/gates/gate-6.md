# Gate-6 — Phase-6 CRITIQUE (longevity-strategist agent-design substrate)

Independent adversarial read of `domain-research.md` (492-line synthesis spine)
cross-referenced against `sections/section-A.md` (13 findings, established levers),
`section-B.md` (12 findings, biomarkers/clocks), and `section-C.md` (7 compound
classes). The full 491-line spine was read including its consolidated [1]–[71]
bibliography (lines 339–481) and Methodology Appendix (lines 483–491). The merged
spine renumbers findings (A→1–13, B-clocks folded into Findings 14–16, C-compounds
into Findings 17–23) and carries Synthesis, a whole-corpus concentration audit,
and a unified renumbered bibliography not present in the section files. All
findings, type-tags, GRADEs, per-compound safety blocks, and citations are present
and resolvable. One factual spot-check (PEARL/Moel 2025 "SAEs fewer in rapamycin
arms") was confirmed accurate against the source via web search. This is a
high-quality substrate; findings below are improvements, not substrate-invalidating
gaps.

## 1. Over-claim / evidence-grade integrity

**Lead-with-established structurally honored — minor (location: spine Findings 1–13 vs 14–23; Main-Analysis preamble line 21).** The ordering is correct: Section-A established levers (Findings 1–13) precede clocks (14–16) precede geroprotectors (17–23), and the preamble explicitly states findings are "ordered by certainty tier." Established levers carry moderate/high GRADE; geroprotectors floor at very-low. The structural mandate is met. No fix required; recorded as a PASS-confirming observation.

**Animal/mouse numbers are population-mismatch-tagged — minor (location: Findings 10, 16, 17, 18, 20, 23).** Every rodent/primate/dog lifespan figure carries an inline `[population-mismatch:<species>]` tag in the same sentence (rapamycin mouse [41/42], metformin-combo mouse [47], senolytic mouse [60], taurine mouse [67]/monkey [68], CR rodent + rhesus [12/13], dog TRIAD [46], iAge mouse+cell [24]). Tag discipline is intact. No fix required.

**Fahy reversal "~2.5 years" stated without an inline derived/CI guard — minor (location: Finding 16, line 177).** The number "~2.5 years mean epigenetic-age reduction across four clocks" is reported as a point estimate from an uncontrolled n≈9 open-label study. The surrounding prose correctly demolishes it (no control, regression-to-mean, confounded GH regimen), so this is not an over-claim in context. Required fix (minor): when this number is ported to agent.md it must never appear without its design-limit clause attached in the same sentence, or a reader lifts "2.5 years" as a citable effect. Recommend the implementer store it as a NEGATIVE example only, never as a standalone figure.

**PhenoAge "~9%/yr (clinical) vs ~4.5%/yr (DNAm)" dual-number — minor (location: Finding 14, line 157; Section-B Finding 2, lines 35–37).** The two numbers are correctly separated with an explicit "must not be conflated" instruction, and the integrity gate (4.75) already remediated this exact number. Internally consistent across spine and section. No fix; flagged so the implementer preserves BOTH numbers and the non-conflation instruction when encoding the per-marker table.

**Resveratrol GRADE phrasing — minor (location: Finding 21, line 237).** "moderate certainty of NO meaningful benefit" is the rare correctly-stated null-with-confidence. It is the one compound graded above very-low, and the grade is for *absence* of benefit, not presence — correctly framed. No fix.

## 2. Missing perspectives / counter-evidence

**Rapamycin immunosuppression/stomatitis — PRESENT (Finding 17, line 191).** Covered: "dose-dependent immunosuppression, stomatitis/mouth ulcers… interstitial pneumonitis." No gap.

**Metformin B12 + exercise-blunting — PRESENT (Finding 18, lines 199, 203).** Both covered: Konopka exercise-blunting in the body, B12 depletion in the AE block. No gap.

**Senolytic D+Q chemo-agent risk — PRESENT (Finding 20, line 227).** Covered: "dasatinib is a chemotherapeutic TKI — bleeding risk, QT prolongation… pleural effusion." No gap.

**Clocks-not-FDA-surrogate + clock disagreement — PRESENT (Finding 15, lines 167–171).** Both covered and made the "regulatory/scientific spine." No gap.

**That NO geroprotector has a human lifespan RCT — PRESENT (Exec Summary line 5; Section-C line 94).** Stated as "the single load-bearing fact." No gap.

**Hormesis for CR/exercise — MISSING — major (location: Findings 4, 9, 11; no hormesis treatment anywhere in spine or sections).** The substrate never names hormesis/mitohormesis as the mechanistic frame for why CR, exercise, and fasting can BENEFIT at moderate dose yet HARM at extremes — the exact concept that governs the "diminishing-but-not-harmful returns" (Finding 4) and the metformin-blunts-exercise antioxidant story (Finding 18). Without it, the agent has no principled way to answer "if some fasting/CR is good, is more better?" — a common high-stakes operator question (eating-disorder adjacency, over-restriction in a lean training operator). Required fix: add a hormesis finding or a hormesis clause to Findings 4/9/11 grounding a "dose-makes-the-poison / more-is-not-better" Ask-vs-Proceed trigger, so the agent escalates rather than extrapolates the dose-response curve.

**Sex differences — PARTIAL / under-generalized — major (location: Findings 17 PEARL women-only signal line 187; Finding 5 grip; otherwise absent).** Sex appears only incidentally: rapamycin ITP female>male extension (~23%, Finding 17) and the PEARL exploratory lean/pain signal "in women at 10 mg." There is no finding establishing sex as a first-class moderator the agent must carry — yet the operator is a specific male (per project memory) and several levers (grip-strength cut-points, protein dose, the women-only PEARL signal) are sex-dependent. Required fix: add an explicit sex-differences note to the Synthesis or a short finding, so the agent encodes "sex moderates effect sizes and cut-points" as a standing caveat rather than leaving it implicit in two scattered numbers. As written, an implementer could miss that the lone positive PEARL signal is sex-restricted and not generalize-able to a male operator.

**Drug–drug interaction surface for the operator's existing regimen — minor (location: Finding 20 line 227 CYP note; otherwise absent).** Only quercetin/fisetin CYP interactions are named. Rapamycin (CYP3A4/P-gp substrate, grapefruit, statin interaction) and metformin (contrast/iodinated-dye hold) interaction surfaces are not stated. For a HALT-pending-MD class this is acceptable (the MD owns interaction-checking), but recommend one Synthesis line stating interaction-checking is explicitly out-of-agent-scope and an MD/pharmacist responsibility, so the agent does not attempt partial interaction reasoning.

## 3. Citation completeness & balance

**Body↔bibliography symmetry in section files — PASS (sections A/B/C).** Section-A cites [1]–[15], bib has [1]–[15]. Section-B cites [1]–[25] (incl. [16],[17],[24],[25] used in concentration/functional findings), bib has [1]–[25]. Section-C cites [1]–[32], bib has [1]–[32]. No orphan in-text [N] and no uncited bib entry detected in the section files.

**Spine consolidated [1]–[71] bibliography RESOLVES — PASS (verified, location: domain-research.md lines 339–481).** The spine carries a complete merged [1]–[71] bibliography with a clean renumber map relative to the section files (section-local numbers are remapped, e.g., Kodama is section-B [24] → spine [27]; Mandsager is section-A/B [3]/[25] → spine [3]; Wu/grip-meta section-B [20] → spine [22]). I spot-checked the highest-risk spine in-text cites against the consolidated bib: [33]/[34] resolve to the Nature-News and Borrus-2024 clock-trust sources; [40]–[71] all resolve to the geroprotector entries; every finding's bracketed [N] has a matching bib line. No orphan in-text [N] and no uncited bib entry found in the spine. (Initial draft flagged this as a major unresolved-citation risk because the bibliography fell below the first read window; reading lines 339–481 cleared it.) The id-reconcile gate (4.25) and integrity gate (4.75) attestations in the Methodology Appendix (lines 489) are consistent with what I observe. No fix required.

**Single-paper-as-three-citations correctly disclosed — minor (location: Finding 23 / Section-C [28][29][30]).** Singh 2023 is cited as [28]/[29]/[30] (mouse/monkey/human arms of ONE Science paper) and the concentration note explicitly states "[67]/[68]/[69] are the SAME paper … 100% concentration." This is the right way to handle it. No fix; flagged so the implementer does NOT count it as three independent sources.

**Over-reliance on single groups — SURFACED, not buried (location: Evidence Landscape lines 271–281).** Horvath/Levine/Belsky clock cluster (~0.78 dev-subset), NIA ITP rapamycin (1.00 for the mouse-lifespan claim), Sinclair/Brenner/Imai NAD+ (~0.40), Mayo/Kirkland senolytics (~0.50), Singh taurine (1.00). All disclosed with numbers. Balance handling is a strength. No fix.

## 4. Logical consistency

**GRADE matches prose throughout — PASS (spot-checked Findings 3, 9/10, 14, 17, 21, 23).** Fitness moderate-associational, CR moderate-biomarker/very-low-lifespan, clocks high-for-association/very-low-for-reversibility, rapamycin very-low-human, resveratrol moderate-for-null, taurine very-low-actively-contradicted. Prose and GRADE are aligned.

**Protein vs mTOR-restriction tension is held, not resolved — PASS (Finding 8 line 101; Section-A line 125).** Correctly flagged as an unresolved trade-off the agent must surface rather than adjudicate. Good.

**TRE lean-mass-loss vs muscle-preservation cross-link — PASS (Finding 11 line 131 → Findings 5, 8).** Internally cross-referenced. Good.

**CALERIE/DunedinPACE: spine drops the clock name the section keeps — minor (location: Finding 9 line 107 "the DunedinPACE DNA-methylation clock" vs Section-A line 77 "a DNA-methylation clock (DunedinPACE)").** Consistent; both name DunedinPACE for Waziry 2023. No contradiction. No fix.

**"SAEs were fewer in rapamycin arms" is a within-HALT reassurance with no guard — major (location: Finding 17 line 187; Section-C line 13; claim verified accurate against PEARL/Moel 2025).** I confirmed via web check that the PEARL trial (Moel/Zalzala 2025, n=114, 48 wk, NCT04488601) does report adverse and serious AEs "similar across all groups" with the rapamycin arms not worse — so the substrate's datum is factually accurate. The problem is rhetorical/safety-adjacent, not factual: the substrate's posture is HARD HALT on rapamycin, yet the body volunteers this exculpatory safety datum from a single small short trial. An adversarial operator will quote exactly this sentence ("even your own research says PEARL found rapamycin safe — fewer SAEs") to argue the HALT is unwarranted. The finding's recommendation does not arm the agent against its own cited reassurance. Required fix: pair the PEARL safety datum with an explicit "underpowered for safety; absence of signal at n=114/48wk ≠ established safety for chronic off-label use; does not relax the HALT" clause, AND add an Anti-Pattern: "do not let a small-trial null-AE finding be used to downgrade an experimental compound's risk floor." Without this the agent's strongest HALT has a self-inflicted soft spot.

## 5. Agent-design fitness

**Findings are encodable — largely PASS.** Each finding names its AGENT_TEMPLATE section(s) and the discipline it grounds (Identity, Core Rules, Anti-Patterns, Modes/HALT, Refusal Classes, Per-Marker Validity Table, Ask-vs-Proceed, Loop-Breaking, Context-Loading). The refusal-class vocabulary (`HIGH_RISK_SAMD`, `PRESCRIPTIVE_DIRECTIVE`, `PATIENT_FACING_DIRECTIVE`, `BASIS_NOT_REVIEWABLE`, `AUTHORITY_FRAMING_BYPASS`) is defined and mapped per compound (Section-C lines 103–108). The per-marker validity table is specified as a two-field structure (Section-B lines 243–255) — directly encodable.

**`AUTHORITY_FRAMING_BYPASS` defined but not exemplified for the implementer — minor (location: Exec Summary line 5; Section-C line 107).** The class is named with the canonical trigger ("my longevity clinic prescribes rapamycin / sells NAD+ IVs", "a longevity doctor/podcast recommends X"). Good. Required fix (minor): the implementer would benefit from ONE worked negative-example dialogue per high-risk class (rapamycin, D+Q, NMN) showing the refusal text, because the substrate gives the trigger and the class but not a sample refusal utterance. This is a Negative-Examples section need, not a substrate defect.

**experimental-HALT is well-specified; cite-or-refuse is well-specified — PASS (Section-C lines 94, 103–108; Exec line 5).** The risk-floor rule ("a compound cannot be elevated above experimental by mechanism, mouse data, or surrogate biomarkers alone") is a clean, mechanical, encodable rule.

**MD-gating specified per compound but the GATING MECHANISM is abstract — minor (location: Findings 17–20 "routes to MD").** Every experimental compound says "routes to MD" / "MD-gated," but the substrate does not specify HOW (does the agent emit a structured referral to the sibling `medical-liaison`/`medical-safety-reviewer` specialists named in Assumption 4, line 15? a free-text "see your doctor"?). For an implementer this is the difference between a real gate and a disclaimer. Required fix: add one Synthesis line specifying the MD-gate is a HANDOFF to the named sibling medical specialist(s), not a terminal disclaimer, so the gate is a routing contract rather than a refusal string.

## 6. Safety completeness

**Per-compound MD-gating + risk-floor — PASS for the four high-risk compounds (Findings 17–20).** Rapamycin, metformin-for-aging, NMN/NR, senolytics each carry: GRADE, Read:experimental, Key AEs/contraindications/monitoring, refusal class, MD-route. Resveratrol/spermidine/taurine (Findings 21–23) carry AEs framed as "the over-claim is the hazard," which is correct for low-toxicity-but-ineffective compounds.

**Monitoring/stopping rules are THIN — major (location: Findings 17–20 AE blocks).** The AE blocks list contraindications and adverse events well, but "monitoring" is named only for metformin (B12) and stopping rules are absent across all compounds. For an experimental compound an operator MIGHT already be taking (the substrate cannot assume they are not — and Section-C line 17 explicitly notes "off-label longevity use is unmonitored self-experimentation"), the agent needs an encodable "if you are already on this, here are the red-flag symptoms that mean stop and seek care today" surface — e.g., rapamycin: fever/infection signs (immunosuppression), non-healing wound, new dyspnea (pneumonitis); D+Q: bleeding, syncope/palpitation (QT). Required fix: add per-compound STOPPING/red-flag triggers to the high-risk AE blocks (17, 20 especially) so the agent serves an already-using operator safely, not only the not-yet-using one. This is the most operationally important safety gap.

**Operator-profile + goals.md hard-limit respect — NOT ADDRESSED, by design, but the boundary needs an explicit line — major (location: Introduction lines 11, 17; SCOPE NOTE Section-C line 3).** The substrate is deliberately goal-agnostic and states personalization is the runtime agent's job (correct per PF-S2-04). BUT the critique brief asks specifically about "no anabolic steroids; MD-gated experimental" hard limits from goals.md. The substrate contains NO anabolic-steroid content at all (correct — out of longevity-compound scope) and never references goals.md hard-limits. Because the agent will operate against a goals.md with hard limits, the substrate should carry ONE explicit pointer that the agent must load and respect operator goals.md hard-limits at runtime even though the substrate itself encodes none. Required fix: add a single Context-Loading line ("agent MUST load operator goals.md hard-limits; substrate is population-level and overridden by any operator hard-limit") so the goal-agnostic substrate does not get encoded into a goal-blind agent. Without it, an implementer reading "goal-agnostic" could omit the hard-limit load entirely.

**Place the agent could be talked into a directive on an experimental compound — IDENTIFIED, see Axis-4 PEARL finding.** The "SAEs fewer in rapamycin arms" sentence (Finding 17) is the one place the substrate's own text could be weaponized to argue down the HALT. Cross-listed here; fix is the Axis-4 required fix. Additionally, the GH-containing Fahy regimen (Finding 16) and the "compounded rapamycin 5/10 mg weekly" specific doses (Finding 17 line 187) appear verbatim in the substrate — the implementer must ensure these doses are stored as DESCRIPTION of what trials used, never echoed as a usable schedule; recommend an Anti-Pattern that the agent never repeats a trial's dose/schedule back as an actionable number even when "just describing the study."

## Verdict
verdict: PASS
halt_reasons: []
