---
title: medical-liaison (Role 7) Design Doc — Adversarial Review (Red Team)
target: design/medical-liaison-design.md
reviewer: adversarial-review (8-category walk), fresh-context
date: 2026-05-29
substrate-spot-checked: design/.medical-liaison-design-work/domain-research.md; design/medical-safety-reviewer-design.md §4.4 + §5 + §13 + §14 EC-4 + §17 BC-1; design/health-specialist-architect-design.md §4 + §13 row 6 + §14 EC-10; design/DESIGN_DOC_TEMPLATE.md; templates/specialist-risk-class.yaml; templates/refusal-class-taxonomy.yaml; scripts/audit-specialist-profile.sh; vault/WIKI.md
---

# Adversarial Review — medical-liaison (Role 7) Design Doc

## Severity Summary

| Severity | Count |
|----------|-------|
| BLOCK    | 0 |
| MAJOR    | 4 |
| MINOR    | 7 |
| NIT      | 4 |
| **Total** | **15** |

**Zero BLOCK findings — justified.** A BLOCK here would mean the design doc, fed to `/upgrade-agent`, would produce a wrong or unbuildable agent.md, or that a cross-role contract it asserts is empirically false. I spot-checked the load-bearing claims against source and they hold:

- **R13-12 defect is real, not invented.** `scripts/audit-specialist-profile.sh:359` `check_aplus_mode_floor()` greps `$BODY` for a `--mode` floor and is unconditional (BLOCK); it never reads `$RISK_TABLE`. Only `check_mode_floor_correctness()` (row 12.5, WARN, line 366) reads `templates/specialist-risk-class.yaml`. The doc's OQ-1/§8/§13 treatment is accurate and honestly surfaced (it appears in §3.2 R16, §8 Forbidden, §13 PROPOSED-DEFECT, §16, §18 OQ-1, §17.3 BC-2) — NOT quietly worked around.
- **The CRITICAL/H1–H2 non-overridable boundary is internally consistent** across §1(#1), §2.2 (Hard adjudicator boundary), §5 rule 2, §6 branch 2, §7 (Do-not-self-finalize HALT), §9.1 field 4, §9.3 preamble, §11.2 AP 5, §14 EC-2, §15.2 #3, §16 INV-CRITICAL-NON-OVERRIDABLE, §17 A-4. All agree: liaison sets `severity_final` ONLY for HIGH/MEDIUM; CRITICAL or `harm_class ∈ {H1,H2}` is `mechanical-auto-block-per-R3` with null/absent `override_path`.
- **Cross-role anchors spot-checked resolve.** Role 4 §4.4 row 4 (adjudicator slot + `operator-with-warning` fallback + canonical literal) — confirmed at medical-safety-reviewer-design.md:149. Role 4 §13 row 7 (override-literal grep target) — confirmed at :537 (it IS the literal anchor, despite the row also being titled "adjudicator-name + fallback prose audit"). Role 1 §13 row 6 + §14 EC-10 (risk-floor escalation → medical-liaison queue) — confirmed at health-specialist-architect-design.md:480 + :585. Role 4 §17 BC-1 (the flip) — confirmed at :741. specialist-risk-class.yaml medical-liaison row (`collation-only`, `mode_floor: not_applicable`, `target_class: none`) — confirmed at :93.
- **No scope creep into another role's ownership.** §2.2 + §4.2 row 3 + §14 EC-7 are scrupulous about "APPROVE entries, NOT author them" (catalog authoring stays Role 4; schema stays Role 1) and "do NOT own the band→verdict mapping" (Role 4 §4.4 row 1). This is exactly the boundary the WIKI row + Role 4 reserve.

The findings below are all correctable in-place by the synthesis/correction phase without re-architecting.

---

## Findings

### AR-01: RISK-5 "(OQ-3)" cross-reference points to the wrong Open Question

| Field | Value |
|-------|-------|
| Category | R — References |
| Severity | MAJOR |
| Location | §17.1 RISK-5: `\| RISK-5 \| Importing ≥65/inpatient base rates as the athlete-operator's risk. \| Population mismatch (OQ-3). \|` |

**Claim.** RISK-5 cites "(OQ-3)" for the population-base-rate mismatch. But in the design doc's OWN §18 numbering, OQ-3 is "Should the override-record schema become a new INV candidate?" (line 540) — not population mismatch. The population-base-rate concern was *substrate* OQ-3, which the design doc dropped from its §18 OQ list entirely (design OQ-4 is the narrower fish-oil/creatine base rate). So RISK-5's pointer resolves to an unrelated OQ, and the population-mismatch concern it names is orphaned — no §18 OQ owns it. A reader following the pointer to justify RISK-5's WARN mitigation lands on the wrong topic. The doc renumbered substrate OQs into design OQs but left this one pointer keyed to the substrate numbering.

**Suggested fix.** Drop the "(OQ-3)" pointer from RISK-5 (population mismatch has no design-§18 OQ), or add a design-§18 OQ for population-base-rate transfer and point RISK-5 at it.

---

### AR-02: §11.2 (the deployed Anti-Patterns section) carries only 2 distinct PF ids inline; R13-11 demands ≥3

| Field | Value |
|-------|-------|
| Category | C — Contradictions / D — Downstream |
| Severity | MAJOR |
| Location | §11.2 anti-patterns 1–6 vs §13 R13-11 (`≥3 distinct PF-S#-## ids in Anti-Patterns`) + §15.2 #9 |

**Claim.** §13 R13-11 (LIVE, BLOCK) requires "≥3 distinct PF-S#-## ids in Anti-Patterns, each resolvable in `memory/process-failures.md`," and §15.2 #9 restates it. But the role-specific anti-patterns in §11.2 (the content that maps 1:1 to the deployed `## Anti-Patterns` section) inline only `PF-S2-04` (AP 6) and `PF-S3-01` (AP 3) — 2 distinct ids. The other six PF ids live in the §11.1 "Project PF coverage" table, a meta sub-section whose status as part of the deployed Anti-Patterns body is ambiguous (AGENT_TEMPLATE.md has no "PF coverage table" slot; the §11.1 table reads like design-doc scaffolding, not deployed prose). If `/upgrade-agent` inlines only §11.2's cues into the agent.md Anti-Patterns section, the deployed profile carries 2 PF ids and trips R13-11 (BLOCK) at deploy time. The design doc does not state which of §11.1 / §11.2 becomes the deployed section.

**Suggested fix.** Add a third PF id inline to a §11.2 anti-pattern (e.g., PF-S6-01 on the deployment-flip cue in AP-style prose, or PF-S2-05 on the re-read cue), OR add an explicit note that the §11.1 PF table is inlined into the deployed Anti-Patterns section so R13-11's grep target is satisfied.

---

### AR-03: §13 R13-7 ("every section carries a Mechanical-Check/Binary line") is asserted as LIVE/BLOCK but §6, §7, §10, §11, §12, §14 carry no `**Binary:**` line

| Field | Value |
|-------|-------|
| Category | C — Contradictions / D — Downstream |
| Severity | MAJOR |
| Location | §13 `\| R13-7 Mechanical-Check/Binary line \| every section carries a Mechanical Check / Binary line \| ... \| LIVE \| BLOCK \|` |

**Claim.** §13 asserts R13-7 is LIVE and BLOCK: every deployed section must carry a Mechanical-Check/Binary line. In the design doc, only §5 (Core Rules, each rule) and §6 (Fabrication guard) and §10 (each entry) carry `**Binary:**` lines. §7 Loop-Breaking, §11 Anti-Patterns, §12 Negative Examples, §14 Edge Cases carry none. The deployed sections derived from these (Loop-Breaking, Anti-Patterns, Negative Examples, Modes) would need Binary lines to pass an "every section" check. The design doc neither shows those Binary lines nor flags that the deployed sections must add them — a downstream `/upgrade-agent` synthesis working only from this doc has no Binary-line source for those sections and will trip R13-7. (Contrast Role 4's design doc, which the doc inherits its discipline from — verify whether R13-7 actually means "every section" or "every behavioral rule"; if the former, this is a gap; if the latter, the §13 wording over-claims.)

**Suggested fix.** Either add a Binary line to §7/§11/§12/§14 (or specify they emerge at synthesis), or narrow §13 R13-7's "every section" wording to the sections the check actually inspects, so the design doc and the deployed-section requirement agree.

---

### AR-04: §3.2 R16 verdict is internally self-contradictory — "ACCEPTED" with a rationale that says the profile "cannot satisfy R13-12"

| Field | Value |
|-------|-------|
| Category | C — Contradictions |
| Severity | MAJOR |
| Location | §3.2 row R16: `ACCEPTED — see §13 PROPOSED-DEFECT + §18 OQ-1` / Rationale: "the deployed profile cannot satisfy R13-12 without integrator adjudication." |

**Claim.** The §3.2 table's own legend says the Rationale column is populated for "non-ACCEPTED only," yet R16 is marked `ACCEPTED` AND carries a rationale. More substantively, the recommendation R16 ("collation-only, no runtime research dispatch") is accepted, but the rationale describes a BLOCKING audit defect that prevents a clean deploy — conflating "the recommendation is sound" with "the recommendation is mechanically satisfiable." A reader scanning verdicts sees ACCEPTED and may miss that R16 cannot pass R13-12 today. The verdict should distinguish "recommendation accepted" from "satisfaction blocked by external defect."

**Suggested fix.** Change R16 verdict to `ACCEPTED (satisfaction blocked — R13-12 defect, §18 OQ-1)` and keep the rationale; or split into the accepted recommendation + a separate flagged blocker so the table legend ("rationale for non-ACCEPTED only") stays honest.

---

### AR-05: §13 rows 381–382 cite "deferred — §18 OQ-3" for the override-validation script, but OQ-3 is the INV-candidate question, not a deferral of those scripts

| Field | Value |
|-------|-------|
| Category | R — References |
| Severity | MINOR |
| Location | §13 PROPOSED rows: `scripts/audit-medical-liaison-override.sh (does not exist) ... (deferred — §18 OQ-3)` and `Override literal presence ... (deferred — §18 OQ-3)` |

**Claim.** Both PROPOSED override-audit rows are tagged "deferred — §18 OQ-3." Design §18 OQ-3 asks "Should the override-record schema become a new INV candidate?" — it is a should-we-promote question, not a deferral note for two named-but-nonexistent scripts. The scripts' nonexistence is a deferral fact; OQ-3 is a policy question that *would* create those scripts if answered yes. The pointer is approximately on-topic but imprecise: a reader expecting a deferral rationale at OQ-3 finds an open policy question. (Distinct from AR-01, which is a wrong-topic pointer; this one is right-topic-but-mislabeled.)

**Suggested fix.** Re-tag as "(PROPOSED; promotion gated on §18 OQ-3)" so the row reads as "this script exists only if OQ-3 resolves yes," not "deferred to OQ-3."

---

### AR-06: §13 R13-3 body-length BLOCK (≤200 lines / ≤2500 tokens) is at risk — the design doc's §5+§11+§14 redundancy will overflow the agent.md

| Field | Value |
|-------|-------|
| Category | L — Language Economy / D — Downstream |
| Severity | MAJOR |
| Location | §5 rules 2/4, §6 branches 2/4, §7 bullets 2/3/4, §11.2 AP 2/3/4/5, §12.1/12.2/12.3, §14 EC-2/EC-4/EC-6 — the same four propositions restated. |

**Claim.** The deployed agent.md has a hard ≤200-line / ≤2500-token BLOCK (R13-3). Four propositions are each stated 4–6 times across the design doc and would carry that redundancy into synthesis:
(1) "CRITICAL/H1–H2 → no override path, mechanical-auto-block" — §1#1, §2.2, §5 r2, §6 b2, §7, §9.1 f4, §11.2 AP5, §14 EC-2, §15.2 #3, §16, §17 A-4 (≈11 restatements).
(2) "maintain position under pushback; ~98% reversal; in-context agreement is not authorization" — §5 r3, §6 b3, §11.2 AP2, §12 (implied), §15.2 #6/#8, §17 RISK-1.
(3) "no bare 'no interaction found' on a watchlist pairing" — §5 r4, §6 b4, §11.2 AP4, §12.3, §14 EC-6, §17 RISK-3.
(4) "Appelbaum–Grisso severity-scaled rung; reject under-evidenced override" — §5 r6/r7, §7, §11.2 AP3, §12.2, §14 EC-4, §15.2, §17 RISK-2.
A design doc legitimately restates across §5/§11/§12/§14 (different consumption surfaces), but the synthesis agent must be told which surface is canonical for the deployed body, or the agent.md inlines all four and overflows R13-3. The doc gives no de-duplication guidance to Phase 5.

**Suggested fix.** Add a one-line synthesis note (analogous to the AGENT_TEMPLATE mapping note at the top) stating that §5 is the canonical home for these four rules and §11/§12/§14 are design-doc elaboration not to be inlined verbatim; OR pre-compress the restatements in the design doc.

---

### AR-07: "Eight §9.3 fields" is asserted in §15.2 #4 and §9.3 but the list has nine bullets / the count is ambiguous

| Field | Value |
|-------|-------|
| Category | C — Contradictions |
| Severity | MINOR |
| Location | §15.2 #4 "names all eight §9.3 fields (caution_verbatim, composite_band, risks_communicated, operator_reason, evidence_tier_required/evidence_provided, override_literal, voluntariness_note, timestamp+contradictions_log_ref)" vs §9.3 bullet list. |

**Claim.** §9.3 renders the schema as 8 bullets, but two bullets each pack two fields: `evidence_tier_required / evidence_provided` (two fields) and `timestamp + contradictions_log_ref` (two fields). So the field *count* is 10 if counted by field name, 8 if counted by bullet. §15.2 #4's acceptance criterion says "names all eight fields" and then parenthetically lists 8 comma-groups — meaning a validator counting distinct field names finds 10, not 8. AC #4 is the binary check `/upgrade-agent` will run; "eight" is the wrong number for a name-counting grep and will either pass-by-accident or fail-by-strictness depending on how the checker tokenizes.

**Suggested fix.** State the count unambiguously: "names all 8 schema bullets / 10 field names" or list them as a flat enumerated set so the AC's binary is checkable without interpretation.

---

### AR-08: §9.1 field 4 example uses `set_by: mechanical-auto-block-per-R3` but elsewhere `set_by` is a role-id and the disposition string is the *value*, not the setter

| Field | Value |
|-------|-------|
| Category | A — Ambiguity |
| Severity | MINOR |
| Location | §9.1 field 4: `{set_by: mechanical-auto-block-per-R3, verdict: BLOCK, override_path: null}` vs §5 rule 2 "the field reads `mechanical-auto-block-per-R3`" and §14 EC-2 `severity_final.set_by: mechanical-auto-block-per-R3`. |

**Claim.** `severity_final.set_by` is described in Role 4 §5 rule 6 as the *setter identity* (enum: a role-id, or `mechanical-auto-block-per-R3` as a sentinel). The liaison doc consistently writes `set_by: mechanical-auto-block-per-R3`, which is fine as a sentinel — but the field semantics ("who set it") vs the auto-block sentinel ("nobody set it; it is mechanical") are blurred, and a synthesis or validation agent could read `mechanical-auto-block-per-R3` as a fabricated role-id that the §6 Fabrication guard forbids ("Never fabricate ... the adjudicator id `medical-liaison`"). The doc never states that `mechanical-auto-block-per-R3` is a sanctioned non-role sentinel value for `set_by`, so a strict reader of the Fabrication guard sees a conflict.

**Suggested fix.** Add one clause to §5 rule 2 or §9.1: "`mechanical-auto-block-per-R3` is the sanctioned sentinel `set_by` value for the non-overridable band; it is not a role-id and is exempt from the §6 adjudicator-id fabrication guard."

---

### AR-09: §15.1 cites a hard line range "lines 291–301 of `upgrade-agent.md`" — brittle and unverifiable from this doc

| Field | Value |
|-------|-------|
| Category | R — References |
| Severity | MINOR |
| Location | §15.1 "enforced by `/upgrade-agent` Phase 7 (lines 291–301 of `upgrade-agent.md`)" |

**Claim.** A hard line-range citation into an external skill file is brittle (the same anti-pattern the project's own HANDOFF rotation rule warns against for sha256 prefixes). If `upgrade-agent.md` is edited, lines 291–301 drift and the citation silently mis-points. The design doc cannot itself verify the range, and a reviewer with only this doc cannot confirm Phase 7 lives there. (The §0 mapping note similarly cites "lines 236" of upgrade-agent for the Modes slot — same brittleness.)

**Suggested fix.** Cite by phase name + section heading ("`/upgrade-agent` Phase 7 — Acceptance Gate") rather than line numbers.

---

### AR-10: §10 entry 2 "any specialist writing a `risk_tier: medium+` compound triggers the liaison to queue it" describes a push-trigger the liaison cannot implement

| Field | Value |
|-------|-------|
| Category | E — Edge Cases / A — Ambiguity |
| Severity | MINOR |
| Location | §10 entry 2: "the queue-eligible set (any specialist writing a `risk_tier: medium+` compound triggers the liaison to queue it)" |

**Claim.** This phrasing implies an event-driven push: a specialist's write *triggers* the liaison. But the liaison is a dispatched agent with no daemon/listener; it auto-LOADS the `risk_tier: medium+` set at dispatch time (the surrounding sentence). The "triggers the liaison to queue it" clause describes orchestration the liaison does not own and cannot detect at rest. A fresh agent reading this could believe it must subscribe to writes or poll. The actual contract (Role 1 §13 row 6 / EC-10) is that the *specialist's* risk-floor HALT routes into the queue — a pull at the liaison's next dispatch, not a push at the specialist's write.

**Suggested fix.** Reword: "the queue-eligible set the liaison drains at dispatch; the trigger is the specialist's risk-floor HALT routing per §4.1 (Role 1 §13 row 6), consumed when the liaison next runs — not a real-time push."

---

### AR-11: §8 "Restrictions" duplicates the full R13-12 OQ-1 paragraph already in §13 and §18

| Field | Value |
|-------|-------|
| Category | L — Language Economy |
| Severity | MINOR |
| Location | §8 "No `aplus-research` runtime dispatch. ... Known audit gap (→ §18 OQ-1): `scripts/audit-specialist-profile.sh check_aplus_mode_floor` (R13-12, BLOCK) is unconditional and does not read the risk table — only the WARN row 12.5 does ..." (≈full restatement of §13's R13-12 PROPOSED-DEFECT detail and §18 OQ-1). |

**Claim.** The R13-12 defect mechanics ("unconditional ... only the WARN row 12.5 reads the risk table ... fix belongs to Role 2 ... surface as Open Question") are stated in full three times: §8 Restrictions, §13 R13-12 PROPOSED-DEFECT detail, §18 OQ-1. Per the Cross-Document Ownership Matrix discipline this doc operates under, the defect mechanics should live once (§18 OQ-1, the owner) and be pointed at. The triple statement is ~15 lines of repeated prose. §8 only needs the one-line forbidden + pointer.

**Suggested fix.** In §8, reduce to: "No `aplus-research` runtime dispatch (`target_class: none`). The R13-12 audit mis-fires for collation-only profiles — see §18 OQ-1." Keep the full mechanics only at §18 OQ-1 (or §13).

---

### AR-12: §4 anti-redefinition footer + §0 mapping note both say the Phase-3 review "checks cross-sibling duplication" — but no sibling design doc is named or pathed

| Field | Value |
|-------|-------|
| Category | R — References |
| Severity | NIT |
| Location | §4 "The Phase-3 adversarial-review checks cross-sibling duplication." |

**Claim.** "Cross-sibling duplication" implies a set of sibling Pass-3 specialist design docs to diff against, but none is enumerated or pathed. As a fresh reviewer I cannot perform the check the doc claims will happen, because the sibling set is undefined here. (Role 4's equivalent footer at least names the consuming docs.) Low impact — it's a forward-looking process note, not a build input.

**Suggested fix.** Either name the sibling corpus ("other Pass-3 `design/*-design.md` specialists") or drop the clause as out-of-scope for this doc.

---

### AR-13: §2.1 word-count parenthetical ("39 words") is unverifiable and will drift

| Field | Value |
|-------|-------|
| Category | L — Language Economy / C — Contradictions |
| Severity | NIT |
| Location | §2.1 "*(39 words. No must/never/always/refuse modal lexicon ...)*" |

**Claim.** The Identity is annotated "39 words." R13-1 (LIVE, BLOCK) enforces ≤40 words. Counting the §2.1 Identity sentence ("You are the medical-liaison. You collate ... you never prescribe.") the figure is plausible but the parenthetical is a frozen self-report that will silently go stale if the Identity is edited at synthesis, and it sits 1 word under the hard cap with no margin. A synthesis tweak (e.g., expanding "MD handout" to "first-MD-visit handout" to match §1) pushes it over 40 and trips R13-1.

**Suggested fix.** Drop the hard "39 words" claim (the script counts it) or rephrase the Identity to leave margin under 40; do not hard-code a count one word from the cap.

---

### AR-14: §17.2 A-1 leans on the "Factory-to-Component Wiring rule" but never names where the orchestrator dispatch call-site lives

| Field | Value |
|-------|-------|
| Category | E — Edge Cases / D — Downstream |
| Severity | MINOR |
| Location | §17.2 A-1 breaks-if: "the deployment lands but orchestrator dispatch logic still routes HIGH/MEDIUM findings to `operator-with-warning` ... the call-site update is a separate change ... an un-updated dispatch call-site is a bug, not a deferral." |

**Claim.** The assumption correctly invokes the Factory-to-Component Wiring rule (the deploy flip requires updating the orchestrator's dispatch call-site, not just shipping the agent.md). But it names neither the file nor the artifact that holds that call-site, so the deferred work it implies has no target — exactly the "deferred work must reference the specific file and function" failure the project's own invariants warn about. The detection ("a HIGH-band finding post-deployment whose `override_path.adjudicator` is still `operator-with-warning`") is good, but the *fix locus* is unnamed.

**Suggested fix.** Name the call-site owner: cite Role 4 §17 BC-1 (which already says "replace `operator-with-warning` fallback with `medical-liaison` default") as the contract, and add "the dispatch call-site is orchestrator-owned; flip tracked at <bead>." Make the deferred wiring a pathed dependency.

---

### AR-15: §9.2 user-facing example hard-codes a vault path ("artifacts/_doctor-visit-queue") into operator prose

| Field | Value |
|-------|-------|
| Category | S — Scope / A — Ambiguity |
| Severity | NIT |
| Location | §9.2 "Your visit handout is at artifacts/_doctor-visit-queue." |

**Claim.** §9.2 mandates "plain language; no preamble ... no internal jargon," yet the sample user message hands the operator a raw repo path (`artifacts/_doctor-visit-queue`). For the July-2026-visit reader (the operator at a doctor's office), a repo-relative artifact path is internal jargon — the operator wants the handout content or a rendered document, not a filesystem path. Mild tension between the §9.2 rule and its own example.

**Suggested fix.** Either soften the example ("Your visit handout is ready — I've put it in your doctor-visit queue") or note that the path is acceptable because the operator is also the repo owner (single-operator A2 assumption). Pick one and make the example consistent with the stated rule.

---

## Coverage Matrix

| Category | Findings | Probed-clean notes |
|----------|----------|--------------------|
| A — Ambiguity | AR-08, AR-10, AR-15 | §6 decision tree branch order is sound; §5 Binary lines are unusually crisp. |
| E — Edge Cases | AR-10, AR-14 | §14 covers mandated (a)–(g) + cross-phase EC-8; the pre/post-flip (EC-1), inherited-HALT (EC-8), and upstream-malformed (§17 A-4/A-5) edges are all handled. |
| C — Contradictions | AR-02, AR-03, AR-04, AR-07, AR-13 | The CRITICAL/H1–H2 boundary is consistent across all 11 sections that touch it (verified) — the doc's hardest internal-consistency target passes. |
| R — References | AR-01, AR-05, AR-09, AR-12 | Spot-checked 5+ cross-role anchors against source (Role 4 §4.4 r4, §13 r7, §5 r5/r6, §17 BC-1; Role 1 §13 r6, §14 EC-10; risk-class.yaml; WIKI) — all resolve. The R13-12 script claim verified against scripts/audit-specialist-profile.sh:359. |
| O — Ordering | (clean) | §6 branch order (authoritative-source-first → adjudication → authority-framing → false-reassurance → default) is correctly load-bearing and stated as such; §7 thresholds compose without dead-ends. No ordering finding. |
| S — Scope | AR-15 | Strong: §2.2 + §4.2 r3 + EC-7 hold the approve-not-author and not-own-band→verdict lines exactly as Role 4/WIKI reserve them. No scope-creep finding into another role's ownership. |
| D — Downstream | AR-02, AR-03, AR-06, AR-14 | §9.1 7-field return + §9.3 schema are well-formed for the orchestrator/deploy-gate consumer; the live downstream risks are R13-3 length (AR-06) and R13-7/R13-11 section-content gaps (AR-02/AR-03). |
| L — Language Economy | AR-06, AR-11, AR-13 | The doc is dense and mostly earns its tokens; the bloat is concentrated in the four restated propositions (AR-06) and the triple-stated R13-12 mechanics (AR-11). |

## Coverage Gaps
None. Every category received ≥1 finding except O (Ordering), which was probed (§6 branch order, §7 threshold composition, §10 load order) and is clean — documented above per AP-R6.
