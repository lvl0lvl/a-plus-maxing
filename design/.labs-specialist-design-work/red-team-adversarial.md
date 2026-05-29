# Red-Team Adversarial Review — labs-specialist-design.md

**Reviewer:** adversarial-review skill agent (fresh context; loaded skill + target + ground-truth sources)
**Target:** `design/labs-specialist-design.md` (414 lines, 18 sections + empty Appendix A)
**Date:** 2026-05-29
**Method:** 8-category walk (A/E/C/R/O/S/D/L) + mechanical coverage checks against domain-research.md, DESIGN_DOC_TEMPLATE.md, the two templates, INVARIANTS.md, WIKI.md, the live audit script + hook, and the Role 1 §4 / Role 4 §4.4 cross-role anchors.

---

## Mechanical Coverage Checks (run first)

| Check | Expected | Actual | Verdict |
|---|---|---|---|
| §3.1 row count = `### Finding ` count in domain-research.md | match | 12 = 12 | PASS |
| §3.2 R-row count = `^- \*\*R[0-9]+` count in substrate | match | 15 = 15 | PASS |
| §3 cited grep for Findings (`grep -cE "^### Finding "`=12) | resolves | 12 | PASS |
| §3 cited grep for R (`grep -cE "^- \*\*R[0-9]+"`=15) | resolves | 15 | PASS |
| All 8 refusal-class IDs used resolve in taxonomy | 8/8 | 8/8 | PASS |
| Both §13 PROPOSED rows appear in §18 | 2/2 (OQ-1, OQ-2) | 2/2 | PASS |
| §13 LIVE paths resolve | audit-specialist-profile.sh (453L, exec, 25 check_), enforce-role-inlining.sh (4296B, exec) | both resolve | PASS |
| §13 PROPOSED scripts confirmed absent | labs-numerics.py, critical-value-floors.yaml | both absent | PASS (claim correct) |
| All 12 §16 INV-* IDs exist in INVARIANTS.md | 12/12 | 12/12 | PASS |
| §13 REFERENCED INV-* IDs exist (incl. INV-RESEARCH-IC13-CORPUS) | resolve | resolve | PASS |
| Finding-line citations in §3.1 match actual ranges | accurate | spot-checked F3/F5/F6/F7/F11/F12 all accurate | PASS |
| Cross-role anchors resolve (Role1 §4 OUT row 5; Role4 §4.4 rows 1/2/3/7/8; §4.3 row 3) | resolve + content matches | all resolve, content matches | PASS |
| §6/§8/§10 live paths (SKILL.md, _source-whitelist.md, gate_attest.py) | resolve | all resolve | PASS |
| Section count = 18 + Appendix A | 18 | 18 + A | PASS |
| Core Rule count 8–12 | 12 | 12 | PASS |
| Edge case count 4–8 | 8 | 8 | PASS |
| Multiplicity arithmetic (1−0.95^k) | k=25→72.3%, k=20→64.2%, k=10→40.1% | doc claims 72%/64%/40% | PASS |

**The mechanical layer of this document is unusually clean.** Every reference resolves, every count matches, the math is right, and the LIVE/PROPOSED/REFERENCED tagging is honest (the PROPOSED scripts genuinely do not exist; the LIVE script genuinely has 25 check_ functions). The findings below are therefore concentrated in the softer categories (Ambiguity, Edge Cases, Downstream, Language Economy) where adversarial reading still surfaces real defects.

---

## Findings

### AR-001: "Deterministic path" / "typed field" is never operationally defined

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions |
| **Severity** | High |
| **Section** | §5 Rule 6; §8; §13 row "Deterministic-numerics path"; §15.2 #7; AC §17.1 |
| **Resolution** | Handle |
| **Affected File** | N/A |

**Description:** The doc's single most-repeated safety mechanism is that numerics go through "a deterministic path" / "a typed deterministic path" / "the unit as a typed field." But the deterministic tool is PROPOSED (does not exist). So at deployment the only thing the agent can actually DO is "refuse or surface ambiguity." Rule 6's pass/fail is "no free-text unit conversion or range comparison in output" — which is satisfied by an agent that simply *never converts and never compares to a range at all*, i.e., by an agent that is useless for its core job. A correction agent / `/upgrade-agent` synthesizer reading "route conversion to a deterministic path" with no existing path cannot tell whether the deployed behavior is "compute via tool" (impossible) or "refuse to compute" (degenerate). The phrase reads as if a capability exists.

**Evidence:** §5 Rule 6: "Now I treat the unit as a typed field and route conversion/comparison to a deterministic path, surfacing ambiguity rather than assuming." §8: "Route every unit conversion / range comparison to a deterministic typed path." §13 PROPOSED row: `scripts/labs-numerics.py` (or equivalent) ... PROPOSED.

**Fix:** Make Rule 6 / §8 explicit that until the PROPOSED tool is LIVE the *only* compliant behavior is to refuse the conversion and surface the unit ambiguity (never to attempt the arithmetic), and state what the agent does when a conversion is genuinely required to answer (route to clinician / decline). The doc gestures at this in §17.2 #3 ("behavior-mitigated only") but the load-bearing rules (§5, §8) do not say "do not compute" — they say "route to a path" that does not exist. Add the negative instruction to the rule itself.

---

### AR-002: "Critical floor" referenced as if it exists; no encoded thresholds anywhere in the deployable artifact

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions / E — Edge Case Gaps |
| **Severity** | High |
| **Section** | §5 Rule 8; §7; §6 step 2; EC-3; §15.2 #6 |
| **Resolution** | Handle |
| **Affected File** | N/A |

**Description:** Rule 8, §7, §6 step 2, and EC-3 all pivot on "a value in the encoded critical floor." But the critical-value-floor table is PROPOSED (`templates/critical-value-floors.yaml`, confirmed absent). The substrate (Finding 8, Limitation 7) is explicit that thresholds are *representative and institution-dependent*, not fixed. So "is this value in the critical floor?" is NOT a binary the deployed agent can evaluate deterministically — there is no table to look up. §15.2 #6 asserts "A deterministic critical-value escalation rule short-circuits interpretation" as a binary acceptance criterion, but no deterministic rule data exists. EC-3's test stimulus ("potassium 6.4 mmol/L") only works because the reviewer happens to know 6.4 > 6.0–6.2; the agent has no encoded source for that boundary. This is the single most safety-critical path in the document and it rests on a non-existent artifact while being described in the present tense ("the encoded critical floor").

**Evidence:** §7: "A value in the encoded critical floor or acute-symptom co-presence terminates interpretation immediately." §6 step 2: "Does the value sit in the critical floor[?]" §13 row: `templates/critical-value-floors.yaml` ... PROPOSED. Substrate Limitation 7: "Critical-value thresholds are representative, institution-dependent figures, not fixed clinical limits."

**Fix:** Until the table is LIVE, the rules must say the agent escalates on (a) acute-symptom co-presence (which IS evaluable from text) and (b) *any value the operator or agent flags as plausibly extreme* — i.e., a conservative over-escalation default, not a lookup against a non-existent floor. State that the absence of an encoded floor means the agent must err toward escalation, not toward "the value isn't in my (empty) floor table so I'll interpret it." As written, an agent with no floor table could read Rule 8 as "no value is in the floor → interpret freely," which is the exact catastrophic failure (Finding 8/11 [55]).

---

### AR-003: EC-3 / Rule 8 acute-symptom escalation can be defeated by the agent's own "I operate on reported values only" boundary

| Field | Value |
|-------|-------|
| **Category** | E — Edge Case Gaps / C — Internal Contradictions |
| **Severity** | Medium |
| **Section** | §1, §8, §17.2 #1 vs §5 Rule 8 / §6 step 2 / EC-3 / EC-8 |
| **Resolution** | Prevent |
| **Affected File** | N/A |

**Description:** The agent's identity and Tools repeatedly insist it "operates on reported, human-readable result values only" and refuses raw signals/images (IMAGE_OR_SIGNAL_INPUT, §1, §8, §17.2 #1). But the TIME_CRITICAL escalation trigger (Rule 8, §6 step 2, EC-8) depends on detecting *acute symptoms* ("chest pain," "palpitations," "heart fluttering") — which are narrative symptom reports, NOT lab values. There is a latent boundary tension: an agent strictly scoped to "reported lab values only" has a plausible misread in which a symptom narrative is "out of scope, route elsewhere" rather than "TIME_CRITICAL escalate now." The doc never reconciles "I only read lab values" with "I must act on symptom narratives." The EC-8 example mixes both (ALT 70 + physician framing) but the symptom-only path (e.g., "my potassium was normal last week but now I have chest pain") is not covered.

**Evidence:** §1: "It reads finished, human-readable result values (not raw analyzer signal)." §2.1: "interpret them as population-relative probability statements ... and route directive and critical-value requests to a clinician." vs §5 Rule 8: "or acute-symptom co-presence" and EC-3 handling cites "acute-symptom co-presence." No edge case covers symptoms WITHOUT a lab value.

**Fix:** Add one sentence to §1 or §8 clarifying that acute-symptom narratives are explicitly IN scope for the TIME_CRITICAL escalation path (not excluded by the "lab values only" framing), and add a test stimulus for the symptom-only case (e.g., "operator reports new chest pain with no lab value → TIME_CRITICAL escalation, not 'out of my scope'").

---

### AR-004: EC-5 cites "R3" for a multiplicity behavior that R3 does not describe

| Field | Value |
|-------|-------|
| **Category** | R — Broken References |
| **Severity** | Low |
| **Section** | §14 EC-5 |
| **Resolution** | Prevent |
| **Affected File** | `design/labs-specialist-design.md` |

**Description:** EC-5 handles "single isolated out-of-range value on a broad panel" via multiplicity (1−0.95^k). It cites "(Finding 2; Finding 12; R3)." Finding 2 is the correct multiplicity source. But R3 is the *Bayesian-conditioning* recommendation ("default low-prior positives to confirm before acting"), not the multiplicity recommendation. There is no dedicated multiplicity R (multiplicity is captured in Finding 2 and Core Rule 2). The R3 citation is a loose/incorrect attribution — the behavior maps to Rule 2 + Finding 2, not R3. Minor, but it is exactly the "citation that doesn't quite resolve to what it claims" class.

**Evidence:** §14 EC-5: "...account for multiplicity; recommend confirmatory testing. ... (Finding 2; Finding 12; R3)." §3.2 R3: "Bayesian conditioning on pre-test probability; default low-prior positives to 'confirm before acting.'"

**Fix:** Change EC-5's recommendation citation from "R3" to "Rule 2 / Finding 2" (multiplicity) and keep R3 only if the "recommend confirmatory testing" sub-clause is the intended R3 link — in which case make that explicit ("multiplicity per Finding 2; confirm-before-acting per R3").

---

### AR-005: §4 GRADE row attributes "strong+low HALT" to Role 1 §4 OUTBOUND row 3, but that HALT lives in Role 1 §5 rule 12

| Field | Value |
|-------|-------|
| **Category** | R — Broken References |
| **Severity** | Low |
| **Section** | §4 INBOUND "GRADE two-axis discipline" row |
| **Resolution** | Prevent |
| **Affected File** | `design/labs-specialist-design.md` |

**Description:** The §4 GRADE row says it inherits "Certainty ... × recommendation strength ...; strong+low HALT" from "Role 1 §4 OUTBOUND row 3." I verified Role 1 §4 OUTBOUND row 3 — it defines the two-axis discipline (certainty × strength, downgrade/upgrade triggers, OCEBM router) but does NOT state the strong+low HALT. The HALT rule actually lives in Role 1 §5 rule 12 (which the doc DOES correctly cite in Core Rule 9). So the §4 row over-attributes content to the wrong Role 1 anchor. The content is real and inherited correctly elsewhere; the §4 anchor is imprecise.

**Evidence:** §4 row: "GRADE two-axis discipline | Role 1 §4 OUTBOUND row 3 | ... strong+low HALT." Role 1 §4 OUTBOUND row 3 (verified): "Two-axis (certainty × recommendation strength); 5 downgrade triggers; 3 upgrade triggers; OCEBM 2011 secondary router" — no HALT clause. Role 1 §5 rule 12 (verified) contains the HALT.

**Fix:** Add "+ Role 1 §5 rule 12 (HALT clause)" to the Counterpart cell of the §4 GRADE row, matching how Core Rule 9 already cites it.

---

### AR-006: "Continuous-monitor avoidance (Finding 10)" — DEVICE_FUNCTION adoption rests on a Finding that does not name continuous monitoring as its primary subject

| Field | Value |
|-------|-------|
| **Category** | R — Broken References / S — Scope |
| **Severity** | Low |
| **Section** | §0 preamble; §4 INBOUND refusal-taxonomy row; §14 boundary-class note; §18 CLOSED (b) |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** The doc repeatedly justifies adopting DEVICE_FUNCTION via "continuous-monitor avoidance (Finding 10)." Finding 10's design implication does contain "avoid time-critical alarming and continuous-monitor framing," so the citation is defensible. But DEVICE_FUNCTION's actual trigger in the taxonomy is "continuous monitoring with alerts; diagnostic determination" — the *diagnostic-determination* half is the more direct fit for a labs interpreter, and the doc leans entirely on the weaker "continuous-monitor" half. This is a scope-framing nitpick: the adoption is sound, but the rationale cites the less-applicable trigger clause. Classified Accept because the conclusion (encode DEVICE_FUNCTION) is correct regardless.

**Evidence:** Taxonomy DEVICE_FUNCTION trigger: "User asks specialist to function as a medical device (continuous monitoring with alerts; diagnostic determination)." Doc §0/§14: "DEVICE_FUNCTION (continuous-monitor refusal, Finding 10)."

**Fix (optional):** Note that DEVICE_FUNCTION also covers the "diagnostic determination" trigger, which overlaps PATIENT_FACING_DIRECTIVE but is the more labs-relevant clause; or accept as-is.

---

### AR-007: §12 Negative Examples exceeds the template line budget (57 lines vs 25–45)

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §12 |
| **Resolution** | Accept (with note) |
| **Affected File** | N/A |

**Description:** §12 spans L237–L294 = 57 lines against the template budget of 25–45 (DESIGN_DOC_TEMPLATE.md §1 inventory). The four BAD/GOOD pairs are individually load-bearing (each maps to a distinct anti-pattern and each GOOD block carries real cited content), so this is NOT cuttable safety content — but the overage matters downstream: `/upgrade-agent` must synthesize a ≤200-line agent.md with Negative Examples in the last ~30 lines for recency. Four pairs at ~14 lines each = ~57 lines of negative-example source feeding a ~30-line slot. The synthesizer will have to compress aggressively, and the doc gives no guidance on which pair is most load-bearing if compression is forced. Per the language-economy load-bearing test the content stays, but the doc should flag the priority order for downstream compression.

**Evidence:** §12 L237–L294 (57 lines). Template §1: "§12 | Negative Examples | REQUIRED | 25–45." §12 mapping note: "Placed at end of agent.md for recency effect." Template §15.2 / Phase-7 constraint: agent.md ≤200 lines.

**Fix:** Either trim the prose framing inside the GOOD blocks (the citations like "TRUST (Stott 2017, N=737)" are load-bearing and stay; the explanatory sentences around them can tighten), OR add a one-line note naming the two highest-priority pairs (critical-value escalation §12.3 + sycophancy §12.4) so the synthesizer keeps those if it must drop one. Do NOT cut §12.3.

---

### AR-008: §5 is under the template's lower line budget (18 content lines vs 30–50) because the pass/fail conditions are dense — risk of synthesis losing them

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / D — Downstream Breakage |
| **Severity** | Low |
| **Section** | §5 |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** §5 (Core Behavioral Rules) is L115–L133 ≈ 18 content lines for 12 rules — well under the 30–50 budget. This is achieved by packing each rule onto one very long line (voice tag + source tag + pass/fail + citations all inline). That is admirably dense and every clause is load-bearing, so this is NOT over-compression in the bloat sense. The downstream risk: `/upgrade-agent` Phase 5 must extract Core Rules from these dense one-liners; the pass/fail conditions (the testable part) are buried mid-line after the rule body. A synthesizer optimizing for the ≤200-line agent.md could drop the pass/fail clauses as "design-doc scaffolding" and lose the testability. Flagging so the synthesizer is told the pass/fail clauses are load-bearing for §15.2 audit, not droppable scaffolding.

**Evidence:** §5 L115–L133. Each rule e.g. Rule 4: "...refuse a single-analyte verdict when companions are absent. Pass/fail: a single-analyte request without companions yields a request-for-companions or refusal, not a verdict. [voice: imperative] [source: standing-instruction] (Finding 4; R4)."

**Fix:** No content change needed. Add a single line to §15.2 or the §5 preamble: "the Pass/fail clause of each Core Rule is load-bearing — it is the §15.2 / audit-script assertion target and must survive synthesis." (The doc already says "Mechanical check authored before each rule's prose" in the §5 preamble, which partially covers this.)

---

### AR-009: Empty-state edge case (EC-7) and the §4 narrowing create a "context gap, not HALT" path that could silently interpret against an unpopulated operator profile

| Field | Value |
|-------|-------|
| **Category** | E — Edge Case Gaps / S — Scope |
| **Severity** | Medium |
| **Section** | §4 INBOUND-BUT-NARROWED row; §6 step 5; §10 step 2; EC-7 |
| **Resolution** | Prevent |
| **Affected File** | N/A |

**Description:** This is the row the review brief specifically flags. The narrowing is *mostly* sound: labs-specialist does not write `vault/compounds/`, so the compound-write HALT is genuinely N/A. BUT the original Role 1 R7 contract HALTs "if a hard-limit field is unpopulated." The doc downgrades this to "an unpopulated field is a context gap to surface, not a HALT" (§4, §6 step 5, EC-7). The dropped obligation: population-match is *interpretation-load-bearing* for labs (a clinical-population RI applied to a healthy self-monitor is Finding 10 [45] / Risk 17.1 #7, severity WARN). So when the operator profile is unpopulated (the CURRENT state — `status: scaffold`, EC-7), the agent under the narrowing will proceed to interpret using whatever reference range it has, merely "surfacing" that population-match context is missing. That is a real interpretation made on an unvalidated population assumption — the exact thing R7's HALT existed to prevent, re-introduced for the labs case. The narrowing converts a HALT into a soft caveat for a field (population) that materially changes interpretation correctness.

**Evidence:** Role 1 §4 OUTBOUND row 5 (verified): "read `vault/meta/operator-profile.md` BEFORE any write; HALT if any hard-limit field unpopulated." Doc §4: "an unpopulated field is a context gap to surface, not a HALT." §17.1 #7: "Population-mismatch silent error ... Severity: WARN." EC-7 handling: "treat unpopulated operator-profile hard-limit fields as CONTEXT gaps to surface (not HALT)."

**Fix:** Narrow the narrowing: the compound-write HALT is correctly N/A, but add that an unpopulated *population-determining* field (the one that selects which reference interval applies — age/sex/ancestry/pregnancy status) HALTs the *interpretation* (not just surfaces a caveat), because applying the wrong-population RI is a correctness error, not a missing-nice-to-have. Distinguish "context gaps that downgrade confidence" (surface) from "population fields that determine which RI is even valid" (HALT the specific interpretation). As written, the WARN-severity population-mismatch risk has no HALT anywhere — only a "read context" step (§10 step 2) and a "surface the gap" instruction.

---

### AR-010: "I encode ≥4, never invent, inherit verbatim" claims verbatim inheritance the doc cannot actually perform for refusal cards

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / A — Ambiguity |
| **Severity** | Low |
| **Section** | §2.2; §4 anti-redefinition rule; §4 refusal-taxonomy row |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** §2.2 and §4 both say the role inherits refusal classes "verbatim" / "Reference by class name + statutory anchor ... Never redefine," and the §4 anti-redefinition rule says the deployed agent.md "references by class name / path / anchor and does NOT inline the canonical statement." But the deployed agent.md must emit refusal *cards* to the user at runtime (§9.2: "A directive request gets the refusal card"). A refusal card IS the canonical card text from the taxonomy (e.g., TIME_CRITICAL's "These symptoms require immediate in-person medical evaluation..."). So the agent must either inline the card text (contradicting "does not inline the canonical statement") or look it up at runtime from `templates/refusal-class-taxonomy.yaml` (which is not in the agent's declared read scope — §8 lists `templates/refusal-class-taxonomy.yaml` only in §10 step 4 "load once per dispatch"). The "never inline" rule and the "emit the card" behavior are in mild tension; the doc does not say where the card text comes from at emission time.

**Evidence:** §4 anti-redefinition: "the deployed `agent.md` references by class name / path / anchor and does NOT inline the canonical statement." §9.2: "A directive request gets the refusal card + clinician routing." §10 step 4: "Load `templates/refusal-class-taxonomy.yaml` ... once per dispatch."

**Fix:** Clarify that the refusal *card text* is loaded from the taxonomy at dispatch (§10 step 4) and emitted by reference, not authored into the agent.md body — i.e., the "no inline" rule applies to the canonical *definition/rationale*, while the *card string* is a runtime lookup. One sentence in §9.2 or §10 step 4 resolves it.

---

### AR-011: §3.1 Verdict column is uniformly "ACCEPTED" — the template allows MODIFIED but the doc narrowed Finding inheritance elsewhere without recording it in §3.1

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions |
| **Severity** | Low |
| **Section** | §3.1 vs §4 INBOUND-BUT-NARROWED vs §11.1 PF-S2-04 "IN-SCOPE — NARROWED" |
| **Resolution** | Prevent |
| **Affected File** | `design/labs-specialist-design.md` |

**Description:** §3.1 marks all 12 Findings "ACCEPTED." But the document narrows the inheritance of the operator-profile contract derived from Finding 12 / Finding 10 (the §4 INBOUND-BUT-NARROWED row), and narrows PF-S2-04 to "IN-SCOPE — NARROWED" in §11.1. The template's §3.1 verdict vocabulary is "ACCEPTED or MODIFIES the Finding (with rationale if MODIFIES)." The operator-profile narrowing is arguably a MODIFICATION of how Finding 10/12's population-match obligation is applied (HALT → surface). A reader reconciling §3.1 (all ACCEPTED) against §4 (one row explicitly NARROWED) sees an inconsistency: the digest says "accepted as-is," the cross-role table says "narrowed." Either the narrowing belongs in §3.1 as a MODIFIED verdict, or §3.1 should note the narrowing is a cross-role-inheritance narrowing (not a Finding modification) to forestall the apparent contradiction.

**Evidence:** §3.1 rows 10 & 12 both "ACCEPTED." §4: "INBOUND-BUT-NARROWED ... an unpopulated field is a context gap to surface, not a HALT. Inherited and explicitly narrowed, not dropped." §11.1: "PF-S2-04 | ... | IN-SCOPE — NARROWED."

**Fix:** Add a footnote or a Verdict-column annotation on §3.1 row 12 (and/or 10): "ACCEPTED (operator-profile precondition narrowed at §4 — see INBOUND-BUT-NARROWED row)." This keeps the digest honest that one inherited obligation was narrowed, satisfying the template's anti-paraphrase-drift purpose.

---

### AR-012: §16 "Active invariant count: 12" double-counts the merged HANDOFF row

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / R — Broken References |
| **Severity** | Low |
| **Section** | §16 |
| **Resolution** | Prevent |
| **Affected File** | `design/labs-specialist-design.md` |

**Description:** §16 states "Active invariant count: 12" and then presents a table. INVARIANTS.md does contain exactly 12 unique INV-* IDs, so the count is correct. BUT the §16 table renders one row as "INV-HO-ROTATION / INV-HO-NO-STALE-HASH" (two IDs in one row) — so the table has 11 visual rows covering 12 IDs. A reader counting table rows gets 11, not 12; a reader trusting "count: 12" and counting IDs gets 12. This is a cosmetic mismatch between the stated count (12, correct) and the row presentation (11 rows). Not wrong, but invites a "the count doesn't match the table" false-positive from the next auditor.

**Evidence:** §16: "Active invariant count: 12." Table final row: "INV-HO-ROTATION / INV-HO-NO-STALE-HASH | No effect | HANDOFF.md hygiene is orchestrator-owned." 11 rows, 12 IDs.

**Fix:** Either split the HO row into two rows (12 rows = 12 IDs = stated count), or change the stated count to "12 IDs across 11 rows (two HANDOFF invariants share a row)." The former is cleaner.

---

### AR-013: Ordering — §14 EC-7 / §6 forward-reference each other and §4 in a way that requires reading all three to resolve the empty-state behavior

| Field | Value |
|-------|-------|
| **Category** | O — Ordering/Dependency Gaps |
| **Severity** | Low |
| **Section** | §6 step 5; §10 step 1; EC-7; §4 narrowed row |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** The empty-state behavior is defined by composing four locations: §4 (the narrowing), §6 step 5 (the read-instruction), §10 step 1 (enter empty-state if `vault/labs/` empty → "§14 EC-7"), and EC-7 itself (which back-references "§4 narrowed row"). §10 step 1 forward-references EC-7 (defined 100+ lines later); EC-7 back-references §4. For a *design-doc* reader this circularity is navigable, but for the downstream `/upgrade-agent` synthesizer extracting "what does the agent do at empty state" into a single agent.md Context-Loading / Edge-Case slot, the behavior is scattered across four sections with mutual cross-references and no single authoritative statement. Risk: synthesis captures the §10 pointer but not the EC-7 "offer to pre-stage reference context" nuance, or vice versa.

**Evidence:** §10 step 1: "if empty, enter empty-state behavior (§14 EC-7)." EC-7: "(not HALT — compound-write HALT is N/A per §4 narrowing)." §6 step 5: "(re-Read `operator-profile.md` at dispatch ... a narrowed context read, not a compound-write HALT)."

**Fix:** No content change required (the cross-references are accurate). Optionally consolidate the one-sentence empty-state behavioral summary into EC-7 as the single source of truth and have §10/§6 point to it without restating the nuance, so synthesis has one canonical extraction target.

---

### AR-014: Downstream — §15.2 mixes audit-script-checkable criteria with criteria that have no checker, without flagging which is which

| Field | Value |
|-------|-------|
| **Category** | D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §15.2 |
| **Resolution** | Prevent |
| **Affected File** | `design/labs-specialist-design.md` |

**Description:** §15.2 lists 10 role-specific acceptance criteria. Several cite a concrete checker (e.g., #1 "`--check refusal-classes`", #4 "`--check grade-halt`", #8 four `--check` subcommands). But #3 (Core Rule count / voice+source tags / anti-sycophancy guard), #6 (critical-value short-circuit, cites "§7 + Rule 8" — no script), #7 (no free-text conversion, cites "Rule 6 + EC-4" — no script), #9 (§3.1 row count match), and #10 (no operator content inlined; BAD/GOOD count) cite no mechanical checker. The doc presents all 10 as "binary pass/fail" but ~half are *manually*-verified, not script-verified. The PROPOSED `labs-numerics.py` would be the checker for #7, but it does not exist — so #7 is currently un-checkable mechanically while being listed alongside script-backed criteria. Downstream (`/upgrade-agent` Phase 4 fact-checker + Phase 7) needs to know which criteria are script-gated vs manual; the doc does not partition them.

**Evidence:** §15.2 #1: "[`audit-specialist-profile.sh --check refusal-classes`...]" (script). §15.2 #6: "A deterministic critical-value escalation rule short-circuits interpretation ... [§7 + Rule 8]" (no script — and the floor table is PROPOSED). §15.2 #7: "[Rule 6 + EC-4]" (no script; checker is PROPOSED).

**Fix:** Tag each §15.2 criterion with its verification path: `[script: --check X]`, `[manual review]`, or `[PROPOSED checker — manual until LIVE]`. This makes Phase-4/Phase-7 verification mechanical and prevents a "criterion #6/#7 marked binary-pass but nothing checks it" gap.

---

### AR-015: §9.1 structured-list has 9 mandatory fields — over-budget for the agent-to-agent handoff and likely to be truncated downstream

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / D — Downstream Breakage |
| **Severity** | Low |
| **Section** | §9.1 |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** §9.1 mandates that "Every interpretation handoff carries" 9 numbered fields (analyte+value+unit, range category+source, panel-pattern, GRADE tag+tier, RCV/method note, worst-case H-class, refusal card+class, confounders+repeat-draw, research dispatch). For a *single-analyte* interpretation many of these are N/A (no trend → no RCV note; no escalation → no H-class; no refusal → no card). The spec says "carries" all 9 without marking which are conditional. An agent reading "every handoff carries (5) RCV/method note" for a first-ever single value with no prior has nothing to put there. The fields are individually justified (each maps to a Finding), so this is not bloat to cut — but the "every ... carries" framing should distinguish always-present (1,2,3,4,8) from conditional (5,6,7,9).

**Evidence:** §9.1: "Every interpretation handoff carries: (1)...(9)... if any." Field (5) "RCV / method-provenance note if a trend is claimed" and (6) "where escalation-gating" and (9) "if any" already carry conditionality inline, but the lead-in "Every ... carries" overrides that.

**Fix:** Change "Every interpretation handoff carries" to "Every interpretation handoff carries, where applicable" and mark fields 1–4 + 8 as always-present, 5/6/7/9 as conditional. Prevents the agent from emitting empty/"N/A" fields or fabricating a trend note to fill field 5.

---

### AR-016: §17.3 / §18 cite the medRxiv DOI as the rationale for AUTHORITY_FRAMING_BYPASS percentages — but conflate two different sources' figures

| Field | Value |
|-------|-------|
| **Category** | R — Broken References |
| **Severity** | Low |
| **Section** | §17.3 #3; §18 OQ-4; §0/§2.1/§5 Rule 10 "~80%+" |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** §17.3 #3 says "a future session fetches the medRxiv full text (currently 403, non-standard DOI 10.64898 — CB §11) and finds the 81.8%/82.1% figures unsupported." The 81.8% is from [51] (medRxiv, DOI 10.64898). The 82.1% is from [52] (Huang, arXiv:2601.12652) — a *different* preprint with a *standard* arXiv ID, NOT the 403/non-standard-DOI source. §17.3 #3 bundles both figures under "the medRxiv full text," implying both come from the 403 medRxiv source. Re-verifying the medRxiv PDF would confirm/refute 81.8% but says nothing about Huang's 82.1% (which the substrate notes was "verified from abstract"). The detection cue is therefore partially wrong: fetching the medRxiv PDF does not test the 82.1% figure.

**Evidence:** §17.3 #3: "a future session fetches the medRxiv full text ... and finds the 81.8%/82.1% figures unsupported." Substrate [51] = medRxiv 81.8%, DOI 10.64898, 403. Substrate [52] = Huang arXiv:2601.12652, 82.1%, "verified from abstract" — separate source.

**Fix:** Split the detection cue: "fetch the medRxiv PDF [51] to re-verify 81.8%; separately re-verify Huang [52]'s 82.1% (arXiv:2601.12652, not the 403 source)." The doc's §18 OQ-4 is more careful ("[51][52] are preprint-grade ... Re-verify full text") but §17.3 #3 specifically attributes both numbers to the single medRxiv fetch.

---

### AR-017: "transparent inform-class posture" stated as a Core Rule but its pass/fail is not binary

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions |
| **Severity** | Low |
| **Section** | §5 Rule 11 |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** Core Rule 11 bundles four obligations (inform-class posture; show input values + RI source; cite every statement; surface ≥1 confounder + repeat-draw on out-of-range) into one rule. Its pass/fail is "every interpretive statement carries a citation + RI source; every out-of-range interpretation lists ≥1 confounder + a repeat-draw recommendation." That covers the citation and confounder halves (binary, checkable) but NOT the "stay inform-class / render no diagnosis" half — which has no stated binary test in the rule (it's covered indirectly by the refusal classes). Rule 11 is the most overloaded rule; its "inform-class" clause is the soft, non-binary part riding on the back of two binary parts. The §15.2 audit can check citations and confounders but not "inform-class posture" directly.

**Evidence:** §5 Rule 11: "Operate as a transparent, citation-backed inform tool (IMDRF Category I); ... render no diagnosis or treatment/dose directive (route to a clinician). Pass/fail: every interpretive statement carries a citation + RI source; every out-of-range interpretation lists ≥1 confounder + a repeat-draw recommendation."

**Fix (optional):** Either accept (the diagnosis-refusal is enforced via PATIENT_FACING_DIRECTIVE in Rules 3/8/10/12 and §6/§8) or add the binary clause "no output contains a diagnosis or dose directive" to Rule 11's pass/fail. Given heavy coverage elsewhere, Accept is defensible.

---

## Coverage Matrix

| Section group | A | E | C | R | O | S | D | L |
|---|---|---|---|---|---|---|---|---|
| §1–2 (Problem/Role) | AR-003 | AR-003 | AR-010 | — | clean | AR-006 | — | clean |
| §3 (Digest) | clean | — | AR-011 | clean (lines verified) | clean | — | clean | clean |
| §4 (Cross-Role) | AR-010 | — | AR-011 | AR-005, AR-006 | clean | AR-006, AR-009 | clean | clean |
| §5–7 (Rules/Ask/Loop) | AR-001, AR-002, AR-017 | AR-002, AR-003 | clean | clean | clean | clean | AR-008 | AR-008 |
| §8–10 (Tools/Comm/Ctx) | AR-001 | AR-009 | AR-010 | clean | AR-013 | AR-009 | AR-014(via§15), AR-015 | AR-015 |
| §11–12 (AntiPat/NegEx) | clean | clean | clean | clean | clean | clean | AR-007 | AR-007 |
| §13 (Mech Enf) | AR-001 | AR-002 | clean | clean (paths verified) | clean | clean | clean | clean |
| §14 (Edge) | AR-002 | AR-003, AR-009 | clean | AR-004 | AR-013 | clean | clean | clean |
| §15–18 (AC/Inv/Risk/OQ) | clean | clean | AR-012 | AR-016 | clean | clean | AR-014 | clean |

Every category has ≥2 findings. No category abdicated.

---

## Coverage Gaps

None. All 8 categories probed against the document and verified against ground truth (domain-research.md, DESIGN_DOC_TEMPLATE.md, both templates, INVARIANTS.md, WIKI.md, the live audit script + hook, Role 1 §4 and Role 4 §4.4 anchors). The document's mechanical layer is exceptionally clean; findings cluster in Ambiguity (PROPOSED-artifact-as-if-LIVE phrasing), Edge Cases (population-mismatch HALT gap, symptom-only escalation), and Downstream (synthesis budget + un-partitioned acceptance criteria).

## Severity Tally

- **Critical:** 0
- **High:** 2 (AR-001 deterministic-path-as-if-exists, AR-002 critical-floor-as-if-exists)
- **Medium:** 5 (AR-003, AR-007, AR-009, AR-014, and AR-009 population-HALT)
- **Low:** 10 (AR-004, AR-005, AR-006, AR-008, AR-010, AR-011, AR-012, AR-013, AR-015, AR-016, AR-017)

(High = 2/17 = 12% — within the AP-R1 self-check; no severity inflation.)
