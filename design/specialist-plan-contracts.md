# Specialist Plan Contracts

*The specialist-layer design substrate for the comprehensive plan (Slice 1 of `plan-platform-architecture.md`). For every deployed specialist + the care assistant, acting from its FULL profile via sequential-thinking, the four contract questions:*

1. **Inputs** — what information do I need to build a plan around my specialization?
2. **Monitoring** — what do I monitor, and how (with validity tiers where the profile demands them)?
3. **Tracking / update** — what tracked streams + writes + adjustment rules keep my domain current?
4. **Analysis → plan** — what my hand-off looks like and how it feeds the one coherent plan (incl. cross-domain seams + escalation).

This is what the Context Assembler must feed each specialist, what the specialist output schema must carry, and what compiles into the monitoring config. It supersedes the thin 4-domain wiring in `plan_driver.py` (`workout/nutrition/supplements/peptides`), which is exactly why today's plan is minimal.

**Roster (18):** 15 domain specialists · 2 safety/escalation (medical-liaison, medical-safety-reviewer) · the care assistant (orchestrator). Excluded: `health-implementer` / `health-specialist-architect` / `health-edge-case-reviewer` — these *build and review* specialists, they don't contribute to a health plan.

**This is a generic specialist-methodology document.** It describes HOW each specialist reasons — the input CATEGORIES it needs, its monitoring approach, its tracked streams, and its analysis→plan hand-off — never WHO the operator is. The operator's real record reaches the model through the identity-stripped user-message record (`assemble_context`), NOT through this document; the worked examples below are generic illustrations of the method, not any real person's data.

---

## 1. personal-trainer — Training

**Acts as:** evidence-ranked, basis-reviewable training programming under an inform-class posture; routes diagnosis / clearance / rehab-Rx / exertional red flags to clinical care. Reasons from the dose-response lever order; treats every population number as a hypothesis to revise against measured response.

### 1 — Inputs I need
- **Population-determining fields** (the operator profile): training status (advanced vs novice changes the prescription), age/sex (masters norms + protein coordination), and the **injury/pain map** (an injury/pain site, if present).
- **Clearance gate — hard, upstream of everything** (the operator profile's contraindication/PAR-Q+/CMRD fields): an active contraindication/clearance flag, if present. An unpopulated or active contraindication field is **UNKNOWN, never "cleared."** If a post-event / CMRD trigger is present → *refer-then-defer*: I build only the criteria-gated re-entry once a clinician's clearance is on file. I cannot skip this.
- **Current-program + benchmarks** (the operator's current-program record): the actual current program (strength / zone-2 / interval work / weekly frequency), current lifts & 1RMs, VO₂max / work capacity, and wearable presence (**absent wearable → empty-state, no fabricated metrics**).
- **Goals** (the operator's goals): the operator's bodyweight and goal-weight, a session-time-reduction target, strength preserved. The reduced-session-time target is a **density/sequencing** problem (superset antagonists, trim junk volume, autoregulate accessories) — I need the current session breakdown to find the time to cut.
- **Vetted library**: the exercise protocol + training parameter library — the established science I cite (every claim source/population-tagged).

### 2 — What I monitor & how (strict validity-tiering, Core Rule 10)
- **sRPE / session-RPE — VALIDATED** → primary daily internal-load signal.
- **Raw resting HR + raw HRV trend — evidence-supported** (raw trend ONLY; proprietary "readiness/recovery" composites are non-validated black boxes, never a verdict).
- **Daily check-in (energy, soreness, injury-site pain, sleep) — trend signal only.**
- **Measured benchmarks — the ground truth** for revise-against-response (strength progressing? zone-2 pace-at-140 bpm improving? interval output rising?).
- **Load progression** watched for abrupt post-layoff spikes (the narrow *ramp-gradually* heuristic — I report ACWR as hypothesis + Impellizzeri/Lolli repudiation, never as validated prevention).
- **Fail-safe floor (outranks all coaching):** exertional red flags (cardiac signs / rhabdomyolysis cluster / cauda equina) → STOP-and-escalate to the LIVE medical-liaison. **Recognize-and-route:** OTS picture (never *labeled* — diagnosis of exclusion) and any LEA/RED-S signal → nutritionist + clinician, never a deficit programmed into it.

### 3 — What I track to update
- **Tracked streams I consume on a loop:** session logs (sets×reps×load×RIR + session sRPE = adherence + real load progression); the daily readiness check-in (drives today's autoregulation); **periodic benchmark re-tests** on a cadence (key lifts 4–6 wk; zone-2 pace-at-HR + interval output monthly) — this is what turns a population mean into the operator's response; injury/pain-map updates (injury-site loading pain-free?); raw RHR/HRV once a wearable lands.
- **My writes (owned):** the exercise protocol + training parameter library (the program, versioned across the block); the contradictions ledger for a cross-domain conflict.
- **Adjustment rules the tracking triggers:** autoregulate today by RIR when self-report/HRV flags low; ramp gradually after any missed week; deliberate taper/peak but **no routine every-4th-week deload** (not evidence-based); reduce load + route on OTS-picture signs; **HOLD all programming** on a contraindication/red-flag. Cap: after 2 revisions of one parameter without new evidence, ship as-is with residual uncertainty surfaced. Ungroundable claim → dispatch `aplus-research --mode=standard --target-class=protocol`, never fabricate.

### 4 — My analysis → the overall plan
- **Hand-off shape** (Communication field-list): (1) recommendation + its lever-order place; (2) parameter values + population-derived-from + revise-against-response caveat; (3) established-vs-provisional + GRADE certainty×strength; (4) return-to-training note *if a re-entry* (time-is-a-floor, criteria-gated, clinician-shared — live when a clearance flag is present); (5) monitoring validation tier per signal; (6) escalation band + refusal card if fired; (7) out-of-domain routes; (8) aplus-research provenance.
- **The DOMAIN PROGRAM I emit:** a periodized 12-wk block — 2 strength days (compound progression + ATG/tibialis/hip-flexor knee-health work), 1 hypertrophy day, zone-2 45 min ≤140 bpm ×1, high-intensity interval work ×1 — **sequenced so the VO₂max/interference load doesn't blunt lower-body strength**, density-restructured to the session-time target, each block GRADE-tagged, benchmarks + re-test cadence baked in. **I emit the monitoring signals + adjustment rules WITH the prescription** so the plan carries its own autoregulation (daily loop runs deterministically off sRPE/self-report; re-plan only on a material trend).
- **Cross-domain seams the orchestrator must reconcile:** (a) **nutrition→workout energy bounce** — the operator's deficit blunts recovery/adaptation, so training load and deficit depth are a JOINT constraint, not independent; aggressive deficit → I cut volume/intensity or it bounces back; (b) **RED-S/LEA short-circuit** — deficit + load trips a low-energy-availability signal → my programming HALTS and routes; (c) **masters-protein** — I flag the need, the g/kg dose is the nutritionist's owned write; (d) **medical-liaison clearance** for an active flag sits upstream of the whole program; (e) recovery-specialist + sleep-coach own the recovery capacity my load assumes.

---

## 2. nutritionist — Nutrition

**Acts as:** evidence-ranked nutrition guidance under an inform-class posture, reasoning from the lever hierarchy energy > macro > timing > supplements; gates quantitative directives behind population screening; routes disordered-eating / refeeding / RED-S to clinical care.

### 1 — Inputs I need
- **Body-comp**: weight + FFM (protein in a deficit is dosed on FFM), age/sex.
- **Population screen — hard gate before high-protein**: renal/hepatic/special-population status (unpopulated = **UNKNOWN, not "no contraindication"** → withhold + caveat).
- **Medications as first-class inputs**: **GLP-1 agonists** (GLP-1/GIP/glucagon axis → strong appetite suppression) + **testosterone therapy** — both are drug-nutrient/population gates that route a `risk_tier: medium+` note to the live medical-liaison, coordinated with endocrine; I never emit the autonomous move around them.
- **The genetics input layer** — nutrition-relevant variants from the operator's genetics library.
- **Training load (from the trainer)** — deficit depth + concurrent strength/VO₂max work are a JOINT constraint (energy availability).
- **Goal**: the operator's goal-weight on their stated timeline, lean mass preserved. Vetted meal-template + parameter library.

### 2 — What I monitor & how (critical floor = fail-safe ceiling)
- **Body-weight trajectory** — target ~0.5–1 %BW/wk; faster → raise calories (lean-mass risk).
- **Protein adherence** (g/day actually hit) — I watch **protein-at-low-appetite** specifically, because a GLP-1 agonist can silently drop intake.
- **Energy availability (kcal/kg FFM/day)** — my hard guardrail; deficit + training load below **~30 kcal/kg FFM = RED-S trigger** → HALTS directive engagement, routes to care.
- **Calorie adherence as a WEEKLY average, not a daily verdict** — this is the answer to "what if I go over one day": the week absorbs it, no same-day panic.
- **Micronutrient sufficiency** — at reduced volume + suppressed appetite, gaps are likely → watch via labs (labs-specialist read-only), food-first, UL-bounded.
- HOW: reported intake/food log + weight stream + daily appetite/energy check-in + micronutrient labs + the training-load feed for the EA calc. Fail-safe floor above all optimization: sub-floor calories (<~1200), ED/refeeding/RED-S → route to care, zero plan sentences first.

### 3 — What I track to update
- **Streams consumed:** weight stream, intake/food log (calories, protein, fiber), daily appetite/energy check-in, micronutrient/metabolic labs.
- **My writes (owned):** the meal-template protocol — **this is where the RECIPES live** (the operator's explicit ask; the template is the versioned parameter I own), the nutrition parameter library (protein g/kg, fiber ~14 g/1000 kcal, deficit target, fasting window), the contradictions ledger.
- **Adjustment rules:** **weekly-calorie absorb** (one-day overage → adjust the week's average, not a same-day cut); **recompute macros** if weight off-trajectory (too fast → raise calories; stalled → small further cut); **raise protein** strategy if appetite-suppressed intake drops it below floor; **HALT + route** if EA trips RED-S; **withhold high-protein** if renal status UNKNOWN. Caps: revision cap 2; ungroundable value → `aplus-research --mode=standard --target-class=protocol` (escalate `--mode=deep` for an outlier), never fabricate a value/UL.

### 4 — My analysis → the overall plan
- **Hand-off shape:** (1) recommendation + hierarchy place (energy balance is the lever for the cut — no isocaloric-split magic); (2) parameter values + population tag (protein g/kg-FFM for aggressive-deficit lean-mass preservation; deficit size); (3) GRADE certainty×strength + causal/associational; (4) UL + toxicity syndrome per supplement; (5) drug-nutrient conflict + medical-liaison route (GLP-1 agonist + testosterone therapy); (6) refusal card if the floor fired; (7) operator fields read + unpopulated caveats; (8) research provenance.
- **The DOMAIN PROGRAM I emit:** a moderate-deficit protocol (energy target for ~0.5–1 %BW/wk to goal-weight) + elevated protein on FFM + carbs periodized around the 2 lift days + fiber target + **a meal-template with real recipes** + micronutrient food-first UL-bounded — all GRADE-tagged, WITH its monitoring signals (weight trajectory, protein adherence, the EA/RED-S guardrail, weekly-calorie absorb) + adjustment rules + required labs.
- **Cross-domain seams:** (a) the deficit↔training-load **energy bounce** + the shared **RED-S short-circuit** with the trainer; (b) **GLP-1 agonist** appetite/intake coordination with endocrine + medical-liaison; (c) the **supplement boundary** (I own food-first micronutrients; supplement-specialist owns compound supplements — de-dupe so a nutrient isn't double-counted); (d) **labs-specialist** for micronutrient/metabolic biomarkers (read-only linkage); (e) I own the **masters-protein g/kg** the trainer flags but never doses.

---

## 3. peptide-specialist — Peptides

**Acts as:** an evidence-maturity discriminator + extrapolation circuit-breaker for the peptide class. NOT a prescriber — dosing is a PRESCRIPTIVE_DIRECTIVE that routes to the human-gate. Mechanism is never efficacy; class never substitutes for compound-level human evidence.

### 1 — Inputs I need
- The compound entries (the peptide compound + peptide library entries) carrying `maturity_rung` / `mechanism_target` / `human_outcome_evidence` (kept **separate**) / `source_tier` / `concentration_of_evidence` / `worst_case_h_class`.
- The operator profile's **hard-limit fields read at dispatch — HALT on an unpopulated hard-limit** before any compound reasoning.
- The injury context (routed from the trainer) + the operator's other agents (testosterone therapy, GLP-1 agonist) for the interaction surface.
- **Combination reasoning:** the **regenerative-peptide combination inherits the weakest evidence rung** — `combination_evidence: none`, and component tolerability does NOT compose to combination safety (two co-administered soft-tissue/angiogenic peptides are graded at the weaker component). Where a compound's evidence is ~80 %+ single-group (one research team's body of work) → dominance caveat + downgraded certainty + `[non-English-literature]` when the literature is non-English; a preclinical/pilot human_outcome → certainty very-low regardless of how well the angiogenic mechanism is mapped.

### 2 — What I monitor & how (experimental-tier: I emit contraindications + monitoring + STOPPING criteria, not a prescription)
- **`worst_case_h_class` = H2** for angiogenic peptides (malignancy + thrombotic) → surface the risk-floor, a thrombotic-sign watch, a hard stopping criterion, a malignancy-history contraindication. **H1/H2 auto-block** means the go/no-go is not mine — it routes.
- **Injection-site tolerance / AE**; a **claimed indication benefit watched as anecdote-tier**, never counted as proof.
- **Regulatory status** time-stamped (WADA S0 strict-liability; "removed from FDA Category 2" ≠ approved ≠ safe).

### 3 — What I track to update
- **Re-verify time-sensitive regulatory status** at each answer.
- **Re-dispatch `aplus-research --mode=deep --target-class=compound`** when new human evidence could move the `maturity_rung` (a preclinical→trial-stage transition is the update event; dominance/population-mismatch/concentration checks re-run on returns).
- **AE / injection-site / thrombotic-sign reports.**
- **Writes:** the peptide compound + peptide library — author NEW entries from dispatch, **never re-author an existing consumed entry**; contradictions append.
- **Adjustment rules:** new human RCT → update rung + certainty; any AE / hard-limit change → route to medical-liaison + apply stopping criteria; 2 empty dispatches → `status: excluded`, never a fabricated number. Revision cap 2.

### 4 — My analysis → the overall plan
- **Hand-off:** `compound_slug` + `maturity_rung`; `mechanism_target` vs `human_outcome_evidence` DISTINCT; GRADE certainty×strength + strong-with-low HALT (no strong "use this peptide" on a preclinical rung); `worst_case_h_class` + H1/H2 auto-block flag; `refusal_class` + `escalation_target`; aplus-research provenance.
- **What I contribute = an evidence-graded protocol CANDIDATE the human-gate decides on:** a regenerative-peptide candidate for a soft-tissue/injury indication — preclinical/anecdote rung, certainty very-low, worst-case H2, `combination_evidence: none`, WADA S0 flag, dominance + `[non-English-literature]` caveats, WITH experimental-tier monitoring + stopping criteria — and **the actual dose/go-no-go routes to the LIVE medical-liaison** (the human-gate tier). This is exactly why the mockup grades an experimental peptide "B" with a physician flag, not an "A" one-liner — honest maturity discrimination IS the feature.
- **Cross-domain seams:** (a) the **supplement↔peptide additive-AE screen** (orchestrate.py compound band — an angiogenic/bleeding-risk peptide composing with a bleeding-risk supplement HOLDS the supplement); (b) **endocrine** for the testosterone-therapy/GLP-1-agonist interaction; (c) the **trainer** (peptides don't clear the operator to load — the trainer's return criteria still gate that); (d) **medical-liaison** owns the prescriptive / human-gate adjudication + physician-oversight.

---

## 4. supplement-specialist — Supplements

**Acts as:** an evidence-maturity + adulteration/interaction circuit-breaker for OTC / herbal / nootropic. Marketing class is not evidence; "natural" is not safe; DSHEA status is not approval.

### 1 — Inputs I need
- The compound entries with `maturity_rung` **per outcome** + UL + interaction + adulteration + DSHEA status.
- The operator profile's **hard-limit fields — HALT on unpopulated** before any write.
- The operator's **medications** for the mandatory **bidirectional** herb/supplement-drug interaction screen (testosterone therapy, GLP-1 agonist, any Rx — a supplement is not inert against an Rx regimen).
- The operator's **labs** (25-OH-D especially — food-first; supplement only for a documented deficiency; coordinate with nutritionist + labs-specialist).
- The **nutritionist boundary** (I own compound supplements; she owns food-first micronutrients — de-dupe). OTC-hormonal (DHEA/pregnenolone/melatonin) I do NOT own → route to endocrine.

### 2 — What I monitor & how (the operator's stack — typically established-tier compounds such as creatine / vitamin D / omega-3 / magnesium — is mostly established, so UL/interaction/labs-response, not experimental-tier)
- **UL adherence** with the named toxicity syndrome as the ceiling (vitamin D → hypercalcemia; "more is not better").
- **Interaction surface** — any new Rx → re-screen both directions.
- **Adulteration mitigation** — third-party-tested only (NSF / USP / Informed-Sport; WADA strict-liability if the operator competes).
- **Labs-response** — is vitamin D moving the level INTO range, not past it. Any AE.

### 3 — What I track to update
- **Labs** (25-OH-D, Mg if measured) to titrate dose toward range, never past UL.
- **Re-verify DSHEA / banned-ingredient status** against the LIVE FDA directory, time-stamped, for anything gray-zone (banned class → BASIS_NOT_REVIEWABLE + H1/H2 auto-block).
- **Re-run the interaction screen on ANY medication change**; AE reports.
- **Writes:** the supplement compound library + the supplement-stack protocol (the stack carries `combination_evidence: none` + weakest-rung).
- **Adjustment rules:** titrate within UL toward the lab target; DROP/route on a new interaction; STOP + route on AE; acute-AE (hepatotoxicity / serotonin syndrome / stimulant toxicity) → TIME_CRITICAL + emergency-services, stop the turn. Revision cap 2.

### 4 — My analysis → the overall plan
- **Hand-off:** `compound_slug` + `maturity_rung`; mechanism vs human_outcome distinct; GRADE certainty×strength + strong-with-low HALT; `worst_case_h_class` + H1/H2 flag; `ul_status` + `interaction_screen` + `adulteration_flag` + `dshea_status` (time-stamped); `refusal_class` + `escalation_target` (LIVE medical-liaison); aplus-research provenance.
- **What I contribute:** the stack as an evidence-graded, UL-bounded, interaction-screened program — creatine (established, high certainty), vitamin D (titrated to the operator's 25-OH-D, UL-bounded), omega-3 EPA/DHA, magnesium glycinate PM — each with rung + UL ceiling + the bidirectional interaction result + a third-party-testing note, GRADE-tagged, WITH monitoring + adjustment rules. This is why the mockup grades an established, well-screened stack "A" vs the experimental "B" peptides.
- **Cross-domain seams:** (a) the **supplement↔peptide additive-AE screen** (my bleeding-risk/additive-AE classes compose with the peptide's — a match HOLDS the supplement); (b) the **supplement↔Rx BPMH screen** (my compound's AE class vs the operator's med list → medical-liaison); (c) the **nutritionist de-dupe** (a nutrient counted once); (d) **labs-specialist** for the D/Mg linkage; (e) **endocrine** for any OTC-hormonal I route.

---

## 5. endocrine-specialist — Hormonal

**Acts as:** the HPA/HPG/HPT coupled-axis interpreter + owner of the hormone/testosterone compound + hormone-biomarker classes. Inform-class: **no dose, no titration, ever**; the AAS boundary is a categorical hard limit, not an evidence question.

### 1 — Inputs I need
- Hormone panels read as **coupled axes** (T / free-T / E2-sensitive-assay / LH / FSH / SHBG / prolactin / TSH-T4-T3-rT3 / cortisol / insulin-HOMA-IR / IGF-1) — **never a single-analyte verdict**.
- **Provenance-gate** every value (draw-time / assay+lab / age-sex range / units, else BASIS_NOT_REVIEWABLE) + **assay-artifact screen** (biotin, direct-analog free-T, non-sensitive E2 in men, macroprolactin).
- The operator profile's hard-limits at dispatch (HALT if unpopulated for a medium+ hormone compound) + the goals' **"No anabolic steroids" CATEGORICAL** limit — testosterone-therapy↔AAS is dose/intent, supraphysiologic/above-range "optimization" AUTO-BLOCKS.
- The operator's **testosterone therapy** (I own the testosterone compound class); a **GLP-1 agonist**'s metabolic axis read coupled (glucose/insulin/weight — HbA1c interpretation is labs-specialist's).

### 2 — What I monitor & how
- **Testosterone-therapy safety axis:** hematocrit/erythrocytosis (the H2 signal), E2 (sensitive assay), PSA (IGF-1/cancer is prostate-concentrated), lipids, LH/FSH (suppressed on exogenous T). T targeted **mid-range age-appropriate** (U-shaped mortality), never maximal — optimization-without-indication refused.
- **GLP-1 agonist:** glucose / HbA1c / weight / GI tolerance.
- **Acute clusters** (thyroid storm / adrenal crisis / severe hypoglycemia / DKA-HHS) = TIME_CRITICAL, override any lab read. No DEVICE_FUNCTION "be my glucose monitor and tell me when to dose."

### 3 — What I track to update
- **Periodic hormone panels** on a cadence — testosterone therapy: T/free-T/E2/hematocrit/PSA/lipids/LH-FSH; GLP-1 agonist: glucose/HbA1c/weight (labs-specialist interprets reported values; I author the hormone-class biomarker + compound entries + the contradictions ledger).
- **Adjustment rules:** rising hematocrit → flag erythrocytosis + route (dose is the clinician's, never mine); T drifting above range / "optimize higher" → AUTO-BLOCK (AAS line); a multi-hormone stack or cross-axis sequence → **hard-block as an ASSEMBLY** inheriting the worst component's H-class (clearing it component-by-component is the failure); acute cluster → TIME_CRITICAL. Revision cap 2; new evidence via `aplus-research --mode=deep --target-class=compound`.

### 4 — My analysis → the overall plan
- **Hand-off:** `analyte_or_compound` + coupled-axis read; mechanism vs human_outcome distinct; GRADE certainty×strength + strong-with-low HALT; `worst_case_h_class` + H1/H2 flag; `provenance`; `refusal_class` + `escalation_target`; aplus provenance.
- **What I contribute** = the hormonal program's **interpretation + monitoring + safety gates** — testosterone-therapy maintenance read at the axis level (**NOT dosed** — physician-oversight flagged, the dose is the clinician's), GLP-1-agonist metabolic monitoring, the IGF-1 ceiling, with the required lab panel + the erythrocytosis / AAS-line / acute-cluster gates. **This IS the mockup's "Hormonal" card graded B + physician-flag + "Labs pending" amber** — the labs literally aren't drawn yet, so it runs provisional.
- **Cross-domain seams:** (a) **nutritionist** for GLP-1-agonist appetite/deficit; (b) **labs-specialist** for HbA1c + the biomarker linkage; (c) **cardiovascular-specialist** for testosterone-therapy erythrocytosis/lipids → CV risk; (d) **medical-liaison** owns the prescriptive / human-gate + the AAS categorical block.

---

## 6. cardiovascular-specialist — CV / Metabolic

**Acts as:** a recognize-and-route cardiac safety instrument + a causal-vs-associational over-claim circuit-breaker. The cardiac emergency floor is the dominant, non-overridable behavior. Owns CV biomarkers/protocols/HR-zones; every CV Rx is name-and-route, never a compound write.

### 1 — Inputs I need
- CV biomarkers in the **causal hierarchy**: **ApoB** (better estimate on LDL-C/ApoB discordance) / LDL-C / **Lp(a)** (once — causal, lifestyle-unmodifiable amplifier) / remnant-TG are the modifiable levers; **HDL / RHR / HRV are ASSOCIATIONAL only** (no "raise HDL / lower RHR to cut risk"); **hs-CRP** is a risk/responsiveness marker, not a per-person causal lever.
- **BP with measurement context** (office/ABPM/HBPM validated device — out-of-office is the operative exposure, masked HTN not benign). Risk scores rank populations, never a precise personal probability; no user-facing score computed.
- **CRF as a first-class but observational lever** — the operator's zone-2 + high-intensity interval build **IS a CV intervention** (no observed upper limit; low-end-steep dose-response; no "too much cardio" warning here).
- The operator profile's cardiac/clotting/renal hard-limits at dispatch (HALT if unpopulated on a medium+ surface); the operator's **testosterone therapy** as a CV input (erythrocytosis + lipids).

### 2 — What I monitor & how
- **ApoB / Lp(a) / remnant-TG + BP-in-context + hs-CRP + CRF trend** (zone-2 pace-at-HR + VO₂max, from the trainer's benchmarks). RHR/HRV associational-only.
- **Consumer-device figures = SCREENING signals, never diagnoses**; no ECG/echo interpretation (IMAGE_OR_SIGNAL_INPUT); no continuous-monitoring/alerting (DEVICE_FUNCTION).
- **The cardiac emergency floor** (chest-pain-with-features / exertional syncope / FAST) — evaluated FIRST, non-overridable, persists across turns, never cleared by a normal watch reading.

### 3 — What I track to update
- **Periodic lipid panel** (ApoB / LDL-C / Lp(a)-once / remnant-TG), **hs-CRP**, a **BP log** in measurement context, **CRF re-test** (fed from the trainer's benchmarks).
- **Writes:** CV biomarker + protocol (Z2/cardio) + parameter (HR-zones) libraries + the contradictions ledger. **Owns NO compound library entries** (CV Rx are name-and-route).
- **Adjustment rules:** ApoB above target → name the lever (lifestyle first; a statin/PCSK9i is a clinician's Rx I name-and-route, **never dose/titrate**); rising hematocrit on testosterone therapy → CV-risk flag with endocrine; BP trend → measurement-context read + medical-liaison route if medium+; cardiac floor → TIME_CRITICAL → emergency services; no exercise clearance (routes to clinician — overlaps the trainer's clearance gate).

### 4 — My analysis → the overall plan
- **Hand-off:** CV finding + evidence-maturity (causal vs associational; surrogate vs hard endpoint; molecule×population); GRADE + causal/associational tag; operator fields + unpopulated caveat; biomarker/measurement-validity line; `risk_tier` + contra/monitoring/stopping if a medium+ compound surface fired; `refusal_class` + `escalation_target`; `worst_case_h_class`; aplus provenance.
- **What I contribute** = the **CV/metabolic risk layer** — the causal marker targets (ApoB primary, Lp(a) once, remnant-TG), BP-in-context, hs-CRP, and **CRF as the first-class modifiable lever that ties the operator's cardio training to hard CV outcomes** — with the required lab panel + the cardiac emergency floor as the non-overridable safety gate + the testosterone-therapy erythrocytosis watch. Feeds the Longevity / CV-metabolic surface (the mockup's Longevity card watches ApoB).
- **Cross-domain seams:** (a) **endocrine** (testosterone-therapy erythrocytosis/lipids → contradictions ledger); (b) **labs-specialist** (shared lipid/inflammatory panels); (c) **recovery-specialist** (HR/HRV shared); (d) **personal-trainer** (owns the zone-2 programming; I own the CV-risk framing + the exercise-clearance overlap); (e) **medical-liaison** for CV Rx + the emergency floor.

---

## 7. recovery-specialist — Recovery

**Acts as:** interprets training-recovery + autonomic-balance trends (HRV/RHR/readiness) **against the operator's own baseline**, flags overtraining WITHOUT diagnosing it, grades modalities honestly, routes red-flags. **This owns the "respond when I'm overtrained/primed" mechanism.**

### 1 — Inputs I need
- **HRV/RHR/readiness as a ROLLING TREND vs the operator's OWN baseline** (needs ≥1–2 wks baseline; an absent wearable → empty-wearable-state, **no fabricated metrics**).
- **Subjective wellness / mood / soreness / perceived-recovery = the PRIMARY layer** (devices are adjunct); confound fields (alcohol, illness, short sleep, posture/time-of-day) checked FIRST.
- The operator's modalities (sauna, cold exposure, yoga); the operator profile's **CV flags for sauna/cold contraindication screening**; strength/hypertrophy goals in play → the CWI interference trade-off.

### 2 — What I monitor & how
- **Maladaptation = a FALLING rolling HRV with COLLAPSING CV + subjective decline** — never a single day. Nocturnal RHR trend; a sustained resting-HR +5–10 bpm over weeks = ROUTINE-MONITOR.
- I **FLAG the load/recovery-imbalance pattern, NEVER diagnose OTS** (diagnosis of exclusion → medical-liaison). Red-flag tiers: cardiac cluster / fever-and-train myocarditis → EMERGENCY/URGENT.
- HOW: self-report primary + wearable trend (tiered when a wearable lands).

### 3 — What I track to update
- Daily subjective check-in + wearable HRV/RHR trend + modality logs → **writes to the recovery protocol + recovery parameter (sauna/cold dose) libraries** + the contradictions ledger.
- **Adjustment rules:** falling-trend + subjective-decline + confounds-excluded → flag imbalance → **reduce load (with the trainer)** + route if persists; **NO unscreened heat/cold dose-escalation** (bromism-class — "hotter/longer/colder = faster" is a syncope/arrhythmia path); **CWI-after-lifting → surface the hypertrophy/strength-blunting trade-off** (goal-conditional → time cold away from the operator's lifts); sauna graded honestly (Laukkanen CV-mortality is observational/CV, NOT a muscle-recovery claim). Revision cap 2.

### 4 — My analysis → the overall plan
- **Hand-off:** recovery dimension + value; wearable validation tier; GRADE + modality grade (established/provisional/equivocal); trend/baseline note; confound-pass; CWI/heat trade-off; escalation band + refusal card; out-of-domain route.
- **What I contribute** = the recovery program (sauna / cold / yoga each evidence-graded) + the **HRV/RHR own-baseline trend monitoring + subjective-primary daily check-in + the overtraining-pattern flag**. **This feeds the dashboard READINESS BANNER** ("HRV low 2 days → today trimmed to 3 top sets") that autoregulates the trainer's session — the exact adaptive behavior the design targets.
- **Cross-domain seams:** (a) **personal-trainer** (readiness→load autoregulation); (b) **sleep-coach** + **nutritionist** (foundations-first — I defer sleep + fueling to them); (c) **cardiovascular-specialist** (HR/HRV shared + sauna/cold CV screen); (d) **medical-liaison** (OTS-suspected + contraindication routing).

---

## 8. sleep-coach — Sleep

**Acts as:** interprets self-reported sleep + validation-tiered wearable trends as circadian/behavioral pattern under an inform-class posture, privileges CBT-I, routes diagnosis / Rx / red-flags. Orthosomnia-aware (behavior over numbers).

### 1 — Inputs I need
- Self-reported sleep + validation-tiered wearable trends (an absent wearable → empty-state, **no fabricated stage/readiness numbers**).
- **Circadian timing relative to the operator's clock** (morning light advances, evening delays); age/sex architecture norms (SWS declines with age — age-typical is never "broken"); the **≥7 h POPULATION floor** (not a personal "8 hours"; a target within the floor fits).
- The operator profile for age/sex + red-flag context (SI, OSA screen).

### 2 — What I monitor & how
- **Rolling sleep trend vs own baseline** (single night = noise; orthosomnia guard — never surface one night's number as a verdict). Epoch sleep/wake + RHR usable when a wearable lands (auto-staging low-confidence; readiness composites NOT clinical).
- **CUMULATIVE sleep debt** (felt-adequacy "fine on 6 h" is unreliable, not evidence).
- **Red-flag floor:** SI incl. passive/masked ("better off not waking up"), OSA-screen-positive, injurious-RBD, drowsy-driving → urgency band → LIVE medical-liaison.

### 3 — What I track to update
- Daily sleep check-in (duration/timing/quality) + wearable trend → **writes to the sleep protocol + sleep parameter libraries**.
- **Adjustment rules:** **PRIVILEGE CBT-I** (the sanctioned strong-on-low — strength governs action, certainty gap surfaced); circadian interventions by PHASE (morning light, evening dim, consistent wake); track cumulative debt; **NO dose/sedation-equivalence for ANY sedating agent** (diphenhydramine/alcohol/gabapentinoid — bromism-class → route to prescriber); hygiene is adjunct, not treatment. Revision cap 2.

### 4 — My analysis → the overall plan
- **Hand-off:** sleep dimension + value; wearable validation tier; established-vs-provisional + GRADE + CBT-I HALT-exception; trend/baseline note; circadian-timing note; escalation band + refusal card; out-of-domain route.
- **What I contribute** = the sleep program — a ≥7 h-floor target, wind-down + circadian timing, CBT-I-privileged behavioral levers, the sleep-debt + rolling-trend monitoring + the SI/OSA/drowsy-driving floor. Feeds the daily check-in (sleep quality) + the readiness banner (**sleep debt → recovery → trainer autoregulation**).
- **Cross-domain seams:** (a) **recovery-specialist** (foundations-first — sleep is the foundation it defers to me for; HRV/RHR overlap); (b) **nutritionist** (caffeine / evening-meal timing); (c) **mental-performance-coach** (sleep↔mood/stress); (d) **medical-liaison** (SI/OSA escalation); (e) **compound specialists** (melatonin — I never dose).

---

## 9. longevity-strategist — Longevity (cross-cutting synthesis)

**Acts as:** over-claim control for the longevity domain — foregrounds established high-GRADE levers at their true precedence, gates experimental geroprotectors, interprets aging-clocks without diagnostic over-claim. **A synthesis/sequencing layer, not a new data owner** — it cross-reads the other specialists' surfaces read-only.

### 1 — Inputs I need
- The **established high-GRADE levers** (sleep, VO₂max, strength, muscle mass, ApoB, BP, glucose) — **which are ALREADY the other specialists' outputs, cross-read READ-ONLY** (ApoB from cardio, glucose/HbA1c from labs/endocrine, VO₂max/strength from the trainer, sleep from sleep-coach).
- The operator's goal hard-limits (**No anabolic steroids** — enforced even framed as a longevity lever).
- Any **aging-clock output** with the 5 over-claim controls (clock ≠ diagnosis; not an FDA surrogate; clocks disagree; intervention→clock→outcome unproven; per-marker validity varies).

### 2 — What I monitor & how
- **Trajectory of the PROVEN levers over time** (VO₂max, ApoB, BP, glucose, muscle mass, sleep) — the healthspan backbone.
- **Experimental geroprotectors GATED** (rapamycin / metformin-for-longevity / NAD+ / senolytics → HALT + MD-gate + per-compound STOP triggers + route to medical-liaison + MD-handout queue; acute red-flag → TIME_CRITICAL). The **no-lifespan-RCT backbone** under every geroprotector.
- HOW: cross-read the other specialists' monitored markers; I synthesize, I don't re-measure.

### 3 — What I track to update
- The established-lever markers on a cadence; **goal-agnostic reference-library longevity writes** + the contradictions ledger; MD-handout queue for any experimental survivor (routed, never written).
- **Adjustment rules:** sequence/re-sequence the levers by GRADE; gate any experimental geroprotector; anabolic-as-longevity → HALT-refuse (goals); `aplus-research --mode=deep --target-class=protocol` (deep floor).

### 4 — My analysis → the overall plan
- **Hand-off:** the sequenced strategy (established levers foregrounded, experimental walled off gated); GRADE per claim; operator+goals fields; the 5 clock controls if a clock; the MD-handout entry if an experimental compound survived; refusal_class; `worst_case_h_class`; aplus provenance.
- **What I contribute** = the **LONGEVITY LAYER that sequences the established levers at their true precedence** into a healthspan strategy + gates the experimental + interprets clocks. Feeds the mockup's Longevity card (VO₂max + metabolic markers + lab cadence + ApoB trend). **This is the natural synthesis partner to the care-agent** — the plan's healthspan coherence gets sequenced here.
- **Cross-domain seams:** (a) **labs + cardiovascular** (ApoB/glucose/lipids — cross-read, not owned); (b) **personal-trainer** (VO₂max/strength are the trainer's outputs); (c) **sleep-coach**; (d) **supplement/peptide/endocrine** (cross-read for contradictions + geroprotector routing); (e) **medical-liaison** (experimental gate + MD-handout queue).

---

## 10. mental-performance-coach — Mind

**Acts as:** a PERFORMANCE coach for cognition/focus/stress-resilience — **NOT a mental-health provider**. Leads with the established levers (exercise, sleep, nutrition), is a nootropic over-claim circuit-breaker, and detect-and-escalates suicidality + clinical signal. **The SI floor outranks every coaching rule.**

### 1 — Inputs I need
- Cognition/focus/stress state — but the **established levers (exercise, sleep, nutrition) are the LEADING suspects** for a focus complaint (read lever-first).
- The operator profile / current program; cognitive-compounds class READ-only for routing (nootropics route OUT to supplement-specialist); any mood/stress context (**the SI screen is the overriding gate**); wearable stress/readiness scores as directional black-box, never a verdict.

### 2 — What I monitor & how
- Stress-resilience + focus + cognition — **lever-first**.
- **The SI FLOOR** (explicit OR passive/masked, operator OR third-party) → EMERGENCY/URGENT → LIVE medical-liaison; **persists across turns**, minimization / authority-clearance never downgrades.
- The **performance-vs-clinical boundary** (recognize a PHQ-9/GAD-7/C-SSRS pattern WITHOUT scoring/diagnosing); the stimulant/nootropic over-claim + the psychosis screen on a push-stimulant ask.

### 3 — What I track to update
- The daily stress/mood check-in + focus self-report → **writes to the cognitive protocol + mental parameter libraries** + NEW cognitive library research + the contradictions ledger.
- **Adjustment rules:** lead with established levers for a focus/stress complaint; route nootropic authoring to supplement-specialist; SI → escalate (non-overridable); burnout in-lane for workload/recovery BUT depression-pattern / functional-collapse / SI → escalate; no sedation/stimulant substitution. Revision cap 2.

### 4 — My analysis → the overall plan
- **Hand-off:** cognition finding + dissociable construct + lever-vs-compound placement; GRADE + causal/associational; lever-ordering note; mechanism/population caveat; wearable validation note; escalation band + refusal class; out-of-domain route.
- **What I contribute** = the **MIND program** — stress-resilience + focus coached lever-first (exercise/sleep/nutrition are other specialists' domains → I sequence/reference, don't author), stress-management protocols, wearable-stress interpreted directional — **WITH the SI/mental-health escalation floor as the non-overridable safety gate**. Feeds the Mind domain + the daily check-in (stress).
- **Cross-domain seams:** (a) **personal-trainer / sleep-coach / nutritionist** (the levers ARE their domains — I lead with them); (b) **supplement-specialist** (nootropics); (c) **recovery-specialist** (stress↔HRV overlap); (d) **medical-liaison** (SI/psychiatric escalation).

---

> **Progressive-activation design note (applies to §11–§13):** dermatology, GI, and lymphatic are largely **empty-state for an operator with no skin/gut/lymphatic goal or data on file**. The honest specialist output is "nothing operator-specific to ground a personalized plan" + goal-agnostic reference, and **the domain card renders only when the operator surfaces a goal or data.** The comprehensive plan is progressive: domains activate as needed, they don't all emit a rich card for everyone. (Skincare / Gut are in the UI-map "hardening" slice for exactly this reason.)

---

## 11. dermatologist — Skin / Hair

**Acts as:** a route-and-marketing circuit-breaker for skin/hair — holds topical evidence apart from oral and RCTs from vendor pages, refuses to remotely diagnose skin cancer or read a clinical image.

### 1 — Inputs I need
- Topical-active + AGA compound entries; the operator profile's hard-limits (cardiac/handling for medium+ oral finasteride/minoxidil — pregnancy N/A for a male operator); skin-cancer red-flag context; any DTC skin test (non-evidentiary).
- **For an operator with no stated skin/hair goal: largely empty-state** — honest "nothing operator-specific" + goal-agnostic reference until one is surfaced.

### 2 — What I monitor & how
- **The skin-cancer refer-not-reassure floor** (persists across turns — "probably benign" never ships); **NO clinical-image interpretation** (IMAGE_OR_SIGNAL_INPUT — melanoma sensitivity collapses on darker skin); per-active evidence-tiering (anchor tretinoin/sunscreen vs cosmeceutical conditional); cross-route/cross-sex non-transfer (`[route-extrapolation]`); regimen tolerance (barrier irritation).

### 3 — What I track to update
- Writes to topical-active/AGA compound + dermatology library entries + the contradictions ledger.
- **Adjustment rules:** skin-cancer flag → refer; medium+ oral finasteride/minoxidil → medical-liaison + unpopulated-field HALT; sustained-use-dangerous (chronic high-strength tretinoin/AHA → barrier destruction) → refuse; cosmeceuticals conditional GRADE.

### 4 — My analysis → the overall plan
- **Hand-off:** derm finding + maturity; GRADE; operator fields; `[route-extrapolation]` tag; risk_tier + medical-liaison route if medium+; refusal_class; skin-cancer-floor flag; aplus provenance.
- **What I contribute** (when active) = a **Skincare domain** — topical regimen evidence-graded (anchor actives vs cosmeceuticals; AGA/hair if relevant) + the skin-cancer floor + tolerance monitoring.
- **Cross-domain seams:** (a) **endocrine** (systemic 5ARI DHT/T axis, gynecomastia); (b) **peptide-specialist** (GHK-Cu experimental topicals); (c) **labs-specialist** (systemic absorption); (d) **medical-liaison** (Rx + skin-cancer).

---

## 12. gi-specialist — Gut

**Acts as:** an over-claim circuit-breaker for microbiome/GI — holds correlation apart from causation and a validated assay apart from a name-borrowing commercial test, routes GI alarm features to care.

### 1 — Inputs I need
- GI/inflammation biomarkers (calprotectin, FIT, hs-CRP, fecal sIgA); gut protocols; probiotic/prebiotic compound entries; the operator profile's immune/critical-illness hard-limits (medium+ probiotic writes); GI alarm-feature context; any invalid consumer test (IgG / microbiome kit / SIBO / zonulin).
- **For an operator with no stated GI complaint: largely empty-state** — honest "nothing operator-specific" + goal-agnostic reference until a gut goal/symptom appears.

### 2 — What I monitor & how
- **The GI ALARM-FEATURE floor** (hematemesis / melena / dysphagia / weight-loss / nocturnal symptoms → TIME_CRITICAL or urgent-referral, persists across turns); **biomarker validity** (a single non-specific marker never rules in a diagnosis); the food-sensitivity taxonomy (**NO IgG/IgG4 panels** — advised against by 4 allergy societies); probiotic strain×indication (class-membership ≠ efficacy); the PROPATRIA contraindication in compromised hosts.

### 3 — What I track to update
- Writes to GI biomarker + gut protocol + probiotic compound + GI library entries.
- **Adjustment rules:** alarm feature → route; medium+ probiotic → medical-liaison + unpopulated immune-field HALT; invalid test → refuse; **NO unsupervised elimination diet** (ED-signal → nutritionist's owned floor).

### 4 — My analysis → the overall plan
- **Hand-off:** GI finding + maturity; GRADE + causal/associational; operator fields; biomarker validity line; risk_tier + medical-liaison route if medium+; refusal_class; `worst_case_h_class`; aplus provenance.
- **What I contribute** (when active) = a **Gut domain** — evidence-graded probiotic/prebiotic/fiber/digestive protocol (strain×indication; the validated food-reaction taxonomy) + the GI alarm-feature floor + biomarker validity.
- **Cross-domain seams:** (a) **nutritionist** (meal-template/fiber overlap; the ED floor DEFERS to nutritionist); (b) **labs-specialist** (GI biomarkers overlap); (c) **medical-liaison** (Rx + alarm).

---

## 13. lymphatic-specialist — Lymphatic / fluid status

**Acts as:** interprets self-reported fluid status + validation-tiered inflammation trends under an inform-class posture, grades drainage modalities by GRADE, refutes lymphatic pseudoscience without nihilism, routes red-flags. **Progressive-activation (empty-state when no fluid data is on file).**

### 1 — Inputs I need
- Self-reported fluid/swelling status; lymphatic/inflammation biomarkers when present (**hs-CRP/IL-6 are systemic-inflammation, NOT lymphatic-function readouts**); the operator profile's contraindication-comorbidities. **For an operator with no fluid data: empty-state** — educate from physiology + self-report, fabricate no value; card renders only if a fluid/swelling issue is surfaced.

### 2 — What I monitor & how
- **The red-flag / contraindication floor:** cellulitis/lymphangitis → URGENT + **MLD contraindicated**; new acute unilateral painful swollen limb = **DVT-until-excluded** → route BEFORE any drainage (massage risks PE); bilateral edema + dyspnea → cardiac/renal work-up; hard/fixed/supraclavicular node → malignancy work-up; the lipedema-vs-lymphedema / filariasis-endemic / BCRL-recurrence long-tail.
- **Trend-vs-own-baseline** (single value = noise); the **drainage-modality contraindication GATE** before any MLD/compression/exercise education; glymphatic-clearance is provisional/contested at ANY strength.

### 3 — What I track to update
- Writes to the lymphatic protocol + lymphatic/inflammation biomarker libraries.
- **Adjustment rules:** CDT/compression is the sanctioned strong-on-low (MLD **not** over-sold); no compound dose (benzopyrone/diuretic → route; **diuretics ineffective/harmful for chronic lymphedema = a safety fact, not a dose**); red-flag → escalation. `aplus-research --mode=standard --target-class=protocol`.

### 4 — My analysis → the overall plan
- **Hand-off:** fluid/inflammation dimension + value; validation tier; established-vs-provisional + GRADE (CDT HALT-exception); trend note; **contraindication-gate note (mandatory when a drainage modality is in scope)**; escalation band + refusal card; out-of-domain route.
- **What I contribute** (when active) = a fluid/lymphatic domain — CDT/compression evidence-graded for **diagnosed** lymphedema, the contraindication gate, pseudoscience refutation (no "detox/cleanse" for a healthy person, but CDT genuinely helps diagnosed lymphedema) + the red-flag floor.
- **Cross-domain seams:** (a) **recovery-specialist** (recovery-overlap read-only); (b) **supplement-specialist** (lymphatic compounds route there); (c) **labs-specialist** (inflammation markers); (d) **medical-liaison** (Rx + red-flag).

---

## 14. genetics-specialist — Genetics / PGx (cross-cutting input, DE-ID by construction)

**Acts as:** the DTC-raw≠diagnostic floor + genetics-library provenance owner + PGx/nutrigenomic literacy layer — holds a variant apart from a diagnosis and a probability apart from certainty. **A cross-cutting input layer (like labs), not a domain card.** This is the DNA-aware planning engine.

### 1 — Inputs I need
- The genetics raw dropzone (read BEFORE writing any page); the genetics variant pages with the **R8 metadata contract** (assay_provenance, confirmation_status, ancestry_denominator, classification_tier/source/last_requeried, actionability_routing); the operator profile (medication list for PGx, ancestry for frequency/PRS denominators, jurisdiction for GINA); the live knowledgebases (ClinVar/ClinGen review-status, PharmGKB/CPIC, gnomAD, ACMG-SF).
- **When genetics is unpopulated:** the library may be stood up but **EMPTY** — the live variant research is the operator-gated remaining step; genetics is STAGED, not populated.

### 2 — What I monitor & how
- **The DTC-raw floor** (a raw call is a HYPOTHESIS needing clinical-grade confirmation — `confirmation_status` stays `unconfirmed-raw`; ~4.2% PPV for pathogenic BRCA-region chip calls); **the EMERGENCY gene-CLASS floor** (inherited-cardiac/channelopathy/aortopathy → TIME_CRITICAL).
- **PGx flags surfaced as prescriber-facing decision support, NEVER a dose** (+ phenoconversion caveat); **nutrigenomic effect-size honesty** (FTO ~0.36 kg/m²/allele, <1 % BMI variance; MTHFR is NOT a thrombophilia/dosing marker); ancestry-matched denominators; VUS re-query never cache.
- **THE LOAD-BEARING DESIGN POINT — DE-ID BY CONSTRUCTION:** the crown-jewel non-egress — care assistant → de-associated allele-agnostic gene+rsID research → vetted findings cache in the genetics library → **LOCAL** genotype↔library match → the planner sees ONLY a coarse de-id **genetic-trait-classes token**; raw genotypes NEVER reach the planner.

### 3 — What I track to update
- Writes the genetics variant pages (R8 metadata) + PGx annotations on the compound library (gene/diplotype→phenotype/CPIC, **never a dose**); re-query stale VUS; `aplus-research --mode=deep --target-class=reference`.
- **Adjustment rules:** clinical-grade confirmation → stamp `confirmed-clinical-grade` (never on an operator assertion); EMERGENCY class → TIME_CRITICAL; a PGx flag on a live drug → prescriber.

### 4 — My analysis → the overall plan
- **Hand-off:** the 6-field PGx flag spec (Gene / Diplotype→phenotype / CPIC level / Drug / recommended Conversation / GRADE) — explicitly **NOT a dose**.
- **What I contribute** = the **GENETICS INPUT LAYER** (cross-cutting, like labs): PGx flags (e.g. CYP1A2 for caffeine metabolism; metabolizer status for any med), nutrigenomic effect-sizes fed to nutrition/supplements WITH honest small-effect framing, disease-risk routing to counselor+MD — **all reaching the plan as the coarse de-id trait-classes token**.
- **Cross-domain seams:** (a) the **6 genetics-READING specialists** (nutrition/supplement/endocrine/CV/peptide/gi read the genetics layer; genetics WRITES it); (b) **labs** (genetics read→own handoff); (c) **medical-liaison** (disease-risk/EMERGENCY); (d) **the de-id boundary is the load-bearing seam** — the planner never sees raw genotypes.

---

## 15. labs-specialist — Labs (cross-cutting backbone)

**Acts as:** basis-reviewable biomarker interpretation — reads reported bloodwork as population-relative probability + physiological pattern against cited ranges, surfaces confounders, escalates critical values. **A cross-cutting interpretation layer (like genetics), not a domain card.**

### 1 — Inputs I need
- Reported lab values **UNTRANSFORMED** (with unit + method/lab + prior value); the **RI source TAGGED** (descriptive 95 % RI / decision limit / functional-optimal — never promote optimal to decision-limit authority); the operator profile (age/sex/ancestry/pregnancy for the VALID RI; medication/contraindication fields); **COMPANION analytes** (iron studies, thyroid axis, lipid fractions — panels read as PATTERNS, not lone analytes); the labs + biomarker libraries + the genetics layer (PGx).
- **When labs are unpopulated: first labs PENDING** — the empty-state today.

### 2 — What I monitor & how
- **RCV-gated trends** (the PRIOR result is the comparator; the delta must exceed the Reference Change Value; within ONE method/lab — a method/RI change is a first-order alternative explanation).
- **Multiplicity** (P[≥1 flag] ≈ 1−0.95^k on a broad panel — one flag is noise).
- **The CRITICAL-VALUE floor** (K/Na/glucose/Ca/Hgb/platelets/INR/pH thresholds → TIME_CRITICAL, escalate-not-interpret).
- **Confounder surfacing** (≥1 pre-analytical confounder + a standardized repeat before interpreting an out-of-range value). Reported values only (no image/signal); no prose unit-conversion.

### 3 — What I track to update
- Lab panels over time (RCV-gated within method/lab) → **writes the biomarker + labs libraries** + the contradictions ledger; `aplus-research --mode=standard --target-class=biomarker`.
- **Adjustment rules:** critical value → escalate; out-of-range → confounder + repeat draw; a trend called only past RCV; no diagnosis/dose/substitution.

### 4 — My analysis → the overall plan
- **Hand-off:** analyte + value + typed unit; range category + source/population; panel-pattern read; GRADE certainty + intervention tier; RCV/method note; worst-case H-class; refusal card; confounders + repeat-draw; research dispatch.
- **What I contribute** = the **LABS BACKBONE** that interprets EVERY domain's biomarkers — ApoB/lipids for CV, glucose/HbA1c for endocrine, hormone VALUES for endocrine (**I read reported hormone values; endocrine AUTHORS the hormone-class entries**), micronutrients for nutrition, inflammation for GI/lymphatic — as population-relative probability + RCV-gated trends + the critical-value floor. **I drive the LABS CADENCE** (quarterly/biannual/annual + compound-triggered + genetics-informed) that is the plan's tracking backbone. Feeds the mockup's "lab cadence" + "Labs pending."
- **Cross-domain seams:** (a) **EVERY domain** (I interpret their biomarkers); (b) the **endocrine handoff** (I read hormone values, endocrine authors them); (c) **genetics** (prior reader → genetics now owns); (d) **medical-liaison** (critical values + directives).

---

## 16. medical-liaison — Safety / human-gate (the plan's safety spine)

**Acts as:** the NON-PRESCRIBING care-coordination + adjudication slot — collates `risk_tier: medium+` compounds + contraindications into a doctor-visit queue, assembles the MD handout, adjudicates HIGH/MEDIUM safety blocks. **Never prescribes.** This IS the platform's human-gate adjustment tier.

### 1 — Inputs I need
- The `safety_finding` blocks from specialists (medium+ compounds, contraindications, HIGH/MEDIUM blocks) + their `composite_band` + `harm_class`; the operator profile read at RUNTIME (**contraindication filtering TIGHTENS, never LOWERS a band**); the compounds risk set (all `risk_tier: medium+`, drained at dispatch); the contradictions ledger; the interaction **WATCHLIST** (SJW/CYP3A4, vitamin-K/warfarin, antithrombotic+ginkgo, calcium/levothyroxine).
- **For a compound-carrying operator:** their medium+ compounds (e.g. testosterone therapy, a GLP-1 agonist, regenerative peptides) are what flow here.

### 2 — What I monitor & how
- **The doctor-visit queue** (collated medium+ compounds + contraindications); the **interaction-triage surface** (severity-ranked, source-attributed — **FALSE REASSURANCE is a blockable harm equal to commission**).
- **HIGH/MEDIUM blocks** → adjudicate via `severity_final` + a **CONTENT-VALIDATED override record at the band rung** (Appelbaum-Grisso: MEDIUM→clear-choice; HIGH→understanding+appreciation+reasoning).
- **CRITICAL / H1-H2** → `mechanical-auto-block`, NULL override path (releasing it is the cardinal sin).

### 3 — What I track to update
- Writes `artifacts/_doctor-visit-queue` + the **SBAR handout** + contraindication entries + the override record + the contradictions ledger.
- **Adjustment rules:** a specialist risk-floor HALT → enqueue severity-ranked; HIGH/MEDIUM → build override record **fail-closed** (a block releases ONLY via a content-valid operator override — pushback ≠ authorization; ~98 % in-context concession is the trap; after the cap, if the rung is unmet, **the BLOCK STANDS**); CRITICAL/H1-H2 → auto-block; false-reassurance on a watchlist → BLOCK_WITH_OVERRIDE_PATH + route to database + doctor; re-adjudicate stale routes.

### 4 — My analysis → the overall plan
- **Hand-off:** the 7-field return (status / queue / finding / severity_final / override_record / escalations / self_audit); to the user: what was queued, **that a block needs the operator's decision and cannot be cleared FOR them**, the handout is ready.
- **What I contribute** = the **HUMAN-GATE TIER** — collate every specialist's medium+ compounds/contraindications into the doctor-visit queue + the **SBAR MD handout the operator brings to a doctor visit**, adjudicate HIGH/MEDIUM blocks fail-closed, auto-block CRITICAL/H1-H2. This IS the platform architecture's "human/clinician gate" (HOLD + surface, never auto-advance risk). **Feeds the dashboard "Decisions-for-you" cards + every physician-oversight flag on the plan** (the mockup's peptides/hormonal flags route HERE).
- **Cross-domain seams:** (a) **EVERY compound specialist** (peptide/supplement/endocrine/derm route medium+ here); (b) **the care-agent** (the tier it escalates to — nothing risky auto-advances); (c) **the real doctor** (the SBAR handout = the doctor-visit handoff). **The load-bearing safety spine of the whole adaptive system.**

---

## 17. medical-safety-reviewer — Safety review (deploy-gate, not a runtime contributor)

**Acts as:** the third pre-deployment gate — receives a candidate specialist profile + Role-3 coverage findings, runs FRESH adversarial probes against the refusal taxonomy + harm classes, emits safety findings + a binary DEPLOY/BLOCK verdict. **Default BLOCK.** NOT a runtime plan contributor — it's the meta-safety gate that makes the other specialists trustworthy.

### 1 — Inputs I need
- The candidate profile + Role-3 findings + the **threat-model catalog** (A1–A5 × S1–S7 × P1–P10 × H1–H8) + the refusal taxonomy (**re-read at each probe boundary, never from memory**); the operator profile as adversarial-probe-AUDIT context (**NOT personalization** — probes are goal-agnostic).

### 2 — What I monitor & how
- Jailbreak / authority-impersonation / bromism-class ASR against each specialist; the **H1/H2 auto-block** (mechanically → CRITICAL + BLOCK); silent-agreement among judge instances (it IS the Council-Mode dissent slot, cosine-audit >0.95 → HALT).

### 3 — What I track to update
- Writes its findings report + the append-only threat-model catalog + the divergence log; re-tunes on the count (N=5) / rate (≥30 % override) trigger.
- **Adjustment rules:** default BLOCK; H1/H2 → auto-block; emits `severity_proposed` only (medical-liaison finalizes HIGH/MEDIUM); coverage-pass is an INPUT to probes, never a substitute for the adversarial pass.

### 4 — My analysis → the overall plan
- **What I contribute** = INDIRECT but load-bearing — it is **why you can trust that the peptide/endocrine/etc. specialists won't emit an unsafe dose under adversarial framing.** The runtime analog (adversarially probing the ASSEMBLED plan's safety-relevant outputs before they surface) is the natural extension of this gate into the live loop.
- **Cross-domain seams:** (a) **Role-2 health-implementer** (builds the profile it gates); (b) **Role-3 health-edge-case-reviewer** (coverage findings are its INPUT); (c) **medical-liaison** (finalizes the HIGH/MEDIUM bands it proposes). It sits at deploy-time; the care-agent + medical-liaison are its runtime counterparts.

---

## 18. care-assistant — The orchestrator (Step 2 / 4 — the heart)

**Acts as:** the conductor. The operator's Steps 2 & 4: analyzes the operator's data, **farms specific briefs to each specialist**, then **reconciles their material and tailors ONE coherent plan** + dated milestones. *(No `.claude/agents/` profile — it's `scripts/serve/care_chat.py`.)*

> **Grounded reality vs intent (the gap).** TODAY `care_chat.py` reasons over the operator's FULL record (identity-safe demographics/goals/genetics + raw `health_detail` — NOT coarse bands) and makes ONE `converse` call that replies + captures facts through the de-id gate. But its system prompt is literally `{task: "care-conversation", profile: …}` — **there is no orchestration instruction.** It converses + captures; it does **not** decompose goals into specialist briefs, collect, reconcile, or synthesize a plan. **That is the Slice-1 fix.**

### 1 — Inputs I need
- The operator's **FULL record** (the care conversation + full profile + goals + raw `health_detail` + genetics).
- **Every specialist's structured domain program** (their §4 hand-offs: prescription + rationale + `monitoring_signals` + `adjustment_rules` + `required_labs` + cross-domain seams).
- The **cross-domain constraints** (the energy bounce, RED-S, additive-AE, the safety gates).

### 2 — What I monitor & how
- The operator's stated goals / priorities / feedback; **CROSS-DOMAIN CONFLICTS** (the reconciliation surface — deficit vs training load, supplement↔peptide AE, testosterone-therapy↔CV); plan coherence; the specialists' rolled-up monitoring signals; adherence + satisfaction; the **material/scheduled events** that trigger a re-plan.

### 3 — What I track to update
- The conversation persisted to the vault (the care conversation); the extracted facts through the de-id gate; the **PLAN VERSIONS + decisions + the "what changed & why" log**.
- **Adjustment rules:** on a material change or a request ("swap Tuesday's bike") → **RE-BRIEF the affected specialist → that slice re-plans → a "→ updated your plan" confirmation** + a change-log entry. (This is the loop between talking and the plan actually moving.)

### 4 — My analysis → the overall plan
- **My analysis IS the orchestration + reconciliation + synthesis:** decompose the operator's goals + state into RICH cross-constrained specialist **briefs** (each carrying the real detail + the cross-domain constraints) → collect the domain programs → **RECONCILE** the conflicts → **SYNTHESIZE ONE coherent plan + dated milestones** → drive the loop between talking and the plan moving.
- **THE SYSTEM-PROMPT FIX (Slice-1):** replace `task: "care-conversation"` with an **ORCHESTRATOR prompt** that (1) reasons over the full record, (2) decomposes goals + state into per-specialist briefs, (3) collects + reconciles + synthesizes ONE plan + milestones, (4) drives the re-plan loop on talk/events. This is the single change that makes the care agent the conductor.
- **What I feed:** the WHOLE plan (My Plan + Today's Plan) + the chat control surface + the "→ updated your plan" confirmations; **every risky change routes to the medical-liaison human-gate — nothing risky auto-advances.**
- **Cross-domain seams:** (a) **EVERY specialist** (I brief + collect from all 15 + labs/genetics/liaison); (b) **the de-id boundary** — I reason over the full record, but the specialist/plan hand-off is de-identified via `summarize`→`dispatch` (the parked-de-id note: only identity stripped, all health substance stays); (c) **the medical-liaison** (the human-gate I escalate risk to); (d) **the surfaces** (I author My Plan + Today's Plan).

---

## Synthesis — what this specifies for the Slice-1 build

All 18 contracts converge on a small, concrete set of build requirements:

1. **A shared specialist output schema.** Every domain specialist emits the SAME shape: `{prescription (periodized/dated), rationale (GRADE-tagged, causal-vs-associational), monitoring_signals (validity-tiered), adjustment_rules, required_labs, refusal/escalation, cross_domain_seams}`. This is the "DOMAIN PROGRAM" — it's uniform across §1–§14, which is what lets the orchestrator collect and reconcile mechanically.
2. **The Context Assembler feeds the FULL record** (identity stripped only) — every specialist's §1 "inputs I need" is the operator's real detail (the actual program, the actual stack, an active clearance question), NOT coarse tokens. The `router.summarize` token-collapse is replaced on the plan path.
3. **Monitoring compiles from the plan.** Every §2 "what I monitor" + §3 "adjustment rules" are authored INTO the plan by the specialist, then compiled into the monitoring config the daily loop runs deterministically (sRPE, weight trajectory, HRV own-baseline, EA/RED-S guardrail, UL adherence, lab cadence).
4. **Two cross-cutting input layers** (labs §15, genetics §14) feed every domain — not domain cards themselves, but the biomarker + PGx/nutrigenomic substrate. Genetics reaches the planner DE-ID by construction (the crown-jewel).
5. **The tiered adjustment executor is already specified by the seams:** auto-apply (deterministic rules, §3s) → specialist re-plan (material in-domain) → **care-agent reconcile** (the cross-domain seams — §18) → **medical-liaison human-gate** (§16 — every physician-oversight flag, nothing risky auto-advances).
6. **Progressive activation** (§11–§13 note): domains render only when the operator has a goal/data there; the plan is not a fixed 8-card template.
7. **The care-agent system-prompt rewrite (§18) is the keystone** — it turns the existing full-record converse call into the orchestrator that briefs → reconciles → synthesizes. Smallest change, largest leverage.

This document is the specialist-layer spec for `plan-platform-architecture.md` Slice 1.
