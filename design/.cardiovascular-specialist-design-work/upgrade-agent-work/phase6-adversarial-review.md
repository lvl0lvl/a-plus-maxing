# Phase-6 Adversarial Review — cardiovascular-specialist (agent.md + library-index.md)

**Reviewer:** /upgrade-agent Phase-6 Adversarial Reviewer (adversarial-review document skill, 8-category walk + 4 agent-specific criteria)
**Artifacts:** `.claude/agents/cardiovascular-specialist/agent.md` (176 lines, ~4,228 words), `.claude/agents/cardiovascular-specialist/library-index.md` (11 lines)
**Safety weight:** HIGHEST in roster (cardiac symptoms can be emergencies). Reviewed accordingly.
**Date:** 2026-05-31

## Overall Verdict: APPROVE-WITH-NITS

The profile is safety-sound on every high-weight surface I stress-tested. The cardiac `TIME_CRITICAL` floor is non-bypassable across all four attack paths (device-normal, multi-turn "just give me the plan," authority/educational framing, content-trigger independence); the bromism-class clause is concrete enough to fire (names the specific mechanism, the specific operator-state check, and a HALT on an unpopulated field); the no-compounds-write decision is internally consistent across Role Boundaries / Tools / Modes / library-index; and the `PRESCRIPTIVE_DIRECTIVE` gate is explicitly content-triggered. No CRITICAL or HIGH findings. The blocking-quality issues are all already-disclosed deferrals (the two PROPOSED audits) that the design doc correctly routes to beads, not defects in the profile. The findings below are one MEDIUM broken-reference (a library-index path that doesn't resolve on disk and isn't a design-established read surface) plus LOW/NITPICK polish.

## Findings by Severity

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 1 (AR-001)
- LOW: 4 (AR-002, AR-003, AR-005, AR-007)
- NITPICK: 2 (AR-004, AR-006)
- Total: 7

---

### AR-001: library-index points to `vault/library/cardiovascular/`, which does not exist and is not a design-established read surface

| Field | Value |
|-------|-------|
| **Category** | R — Broken References |
| **Severity** | Medium |
| **Section** | library-index.md, bullet 1 |
| **Resolution** | Prevent |
| **Affected File** | `.claude/agents/cardiovascular-specialist/library-index.md` |

**Description:** The first conditional reference names `vault/library/cardiovascular/` as a "CV research-artifact subtree" to "Consume READ-ONLY when grounding a biomarker/protocol/parameter claim." The directory does not exist on disk (`vault/library/` contains only `_source-whitelist.md`, `methodology/`, `peptides/`, `README.md`). More importantly, the design doc only mentions this path **once** — in §18 OQ-4 — as a *conditional future* layer that would be added *only if* the role is later granted a `vault/compounds/` (CV) write class ("if it should... a `vault/library/cardiovascular/` research layer... need adding"). The design's actual owned/read surfaces are biomarkers(CV)/protocols(Z2-cardio)/parameters(HR-zones). So the library-index introduces a read surface the design does not establish, pointing at a path that does not resolve. The `check_library_index` audit only greps for the literal string `vault/library/` (it does not stat the path), so this passes the deploy gate silently — a fresh agent told to "consume READ-ONLY when grounding a claim" would Glob/Read a missing directory and get nothing, or worse, treat the empty result as "no grounding available" rather than "wrong path." Note this is the same surface flagged in the user's contradiction prompt: the bullet's own text says "this role owns NO `vault/library/cardiovascular/` write class" — i.e., the bullet simultaneously names a read surface and disclaims the write surface for a directory that isn't created yet.

**Evidence:** library-index.md line 5: "`vault/library/cardiovascular/` — CV research-artifact subtree (lipid hierarchy, BP measurement-validity, risk-score, inflammation-axis, CV-compound, HR-zone/CRF entries). Consume READ-ONLY when grounding a biomarker/protocol/parameter claim". Disk: `ls vault/library/cardiovascular/` → "No such file or directory." Design §18 OQ-4: the path is named only as a *contingent* addition tied to an unresolved compounds-write question.

**Fix:** Resolve one of two ways. (a) If the design intends CV library artifacts to live under a CV subtree once research lands, gate the bullet on existence: reword to "`vault/library/cardiovascular/` (created when CV research artifacts land; until then, ground against `vault/library/_source-whitelist.md` + dispatched-agent output) — consume READ-ONLY...". (b) If no CV library subtree is planned under the no-compounds-write decision, drop the standalone path and fold the read-grounding guidance into the `_source-whitelist.md` bullet (which DOES resolve). Either way the standalone unresolvable path should not ship as an unconditional "consume when grounding" instruction. (Optional but recommended for the maintainer, out of this artifact's scope: `check_library_index` should stat referenced paths, not just grep the string — it currently cannot catch this class.)

---

### AR-002: "All 8 canonical classes are encoded" is true for enumeration but the IMAGE/DEVICE/HIGH_RISK_SAMD classes have no recognition-cue exercise outside the enumeration — same thinness the design's own CV-COV-003 fix targeted for BASIS_NOT_REVIEWABLE

| Field | Value |
|-------|-------|
| **Category** | S — Scope Violations (completeness of encoded behavior) |
| **Severity** | Low |
| **Section** | Role Boundaries; Anti-Patterns |
| **Resolution** | Accept (documented) |
| **Affected File** | N/A |

**Description:** The enumeration claim "All 8 canonical classes are encoded" is accurate (verified: all 8 IDs present in Role Boundaries; counts ≥3 each across the body). IMAGE_OR_SIGNAL_INPUT, DEVICE_FUNCTION, and HIGH_RISK_SAMD are each exercised in Core Rule 10/11 + Ask-vs-Proceed §3 + Modes — so they are not enumeration-only (unlike the pre-fix BASIS_NOT_REVIEWABLE that CV-COV-003 addressed). This is a watch-item, not a defect: the device/SaMD classes have rule-and-gate coverage but no dedicated BAD/GOOD pair (Negative Examples cover device-normal-reassurance, association-upgrade, surrogate, and authority-dosing — DEVICE_FUNCTION monitoring-request and a pasted-ECG IMAGE refusal are not shown as pairs). Given the 6-marker minimum is met (4 pairs present) and the behaviors ARE rule-encoded, this is acceptable as-is.

**Evidence:** agent.md line 34: "All 8 canonical classes are encoded." Negative Examples (lines 127-176): 4 pairs, none demonstrating a DEVICE_FUNCTION or IMAGE_OR_SIGNAL_INPUT refusal in isolation.

**Fix:** Accept. If a future revision adds a 5th pair, a "pasted ECG → IMAGE_OR_SIGNAL_INPUT, non-interpretation must not read as looks-normal" pair is the highest-value addition (it doubles as the device-clearing-the-floor reinforcement). No change required to pass.

---

### AR-003: The IDENTICAL-BLOCK is labeled "IDENTICAL" but is not byte-identical to the gi-specialist sibling block; design §4 calls it "verbatim"

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions (label vs content) |
| **Severity** | Low |
| **Section** | IDENTICAL-BLOCK (lines 5-7) |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** The block is wrapped in `<!-- IDENTICAL-BLOCK-START/END -->` sentinels and design §4 INBOUND row 7 says the role "Inherits the block verbatim from the sibling-shared source." The cardio block and the gi-specialist block are NOT byte-identical — they differ in sentence structure and the closing line (cardio: "Respond to substance directly."; gi: "These map onto GI marketing social proof..."). The `check_identical_block` audit only enforces sentinel *presence* (hash-match is skipped unless a `--compare-to` corpus is passed), so this does not block deployment, and per-sibling adaptation of the anti-sycophancy framing is a defensible Role-2 partition choice. The "IDENTICAL" label and the §4 "verbatim" wording overstate the constraint: what is actually shared is the three-mechanism *structure* and the four banned openers, not the text. This is a naming/fidelity nuance, not a behavioral risk — the three mechanisms (A/B/C), the argument-strength-over-speaker principle, and the banned-opener list are all present and correct.

**Evidence:** agent.md line 6 vs gi-specialist/agent.md line 6 (full blocks compared — differ in wording). Design §4 row 7: "Inherits the block verbatim from the sibling-shared source." Audit: `check_identical_block` warns only if sentinel absent; "hash match skipped" when no corpus.

**Fix:** Accept (no behavioral impact). If the maintainer wants the label to be truthful, either (a) make the block byte-identical to the canonical sibling-shared source and run the audit with `--compare-to`, or (b) rename the sentinel to reflect a per-sibling-adapted shared-structure block. Not a Phase-6 blocker.

---

### AR-004: "no device-override" / "device-override" used as a compressed noun without first defining the term

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy (over-compression) |
| **Severity** | Nitpick |
| **Section** | Core Rules 1 |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** Core Rule 1 ends "...zero self-management before it, no device-override." The compound "device-override" is used before the concept is spelled out (it becomes clear by Core Rule 10 and Loop-Breaking that it means "a normal device reading overriding/clearing the floor"). A fresh agent reading Rule 1 top-down resolves it correctly from the adjacent "a normal device reading... does not clear it" clause two sentences earlier, so the isolation test marginally passes. Borderline over-compression; flagged for completeness, not blocking.

**Evidence:** agent.md line 19: "zero self-management before it, no device-override."

**Fix:** Accept, or expand to "no device reading overrides it" to remove the noun-compression. Trivial.

---

### AR-005: Tools `Read/Grep/Glob` lists `vault/parameters/` and `vault/library/*` as read scopes; `vault/parameters/` does not exist on disk yet (empty-state launch)

| Field | Value |
|-------|-------|
| **Category** | E — Edge Case Gaps (empty-state vault) |
| **Severity** | Low |
| **Section** | Tools (line 67); Context Loading step 3 |
| **Resolution** | Handle |
| **Affected File** | N/A |

**Description:** Tools and Context Loading both name `vault/parameters/` (HR-zones) as a read/write surface, and `vault/biomarkers/` currently holds only `_template.md`. `vault/parameters/` does not exist on disk. This is the *expected* empty-state launch condition — and the profile DOES handle it: Modes "Empty state" explicitly says "When `vault/biomarkers|protocols|parameters/` CV entries are absent... do not fabricate... report there is nothing operator-specific." So the empty-state path is covered. The residual gap: the Context Loading step 1 "HALT `context-load-missing` if absent" list is scoped to the *contract* files (operator-profile, current-state, goals, whitelist, taxonomies) — all of which exist — and does NOT include the data-layer dirs, so a missing `vault/parameters/` correctly routes to empty-state rather than HALT. This is correct behavior; the only nit is that a fresh agent might read the Tools line "Write/Edit scoped to ... `vault/parameters/`" and try to write to a non-existent dir on first authoring. Standard Write creates parent dirs, so low impact.

**Evidence:** agent.md line 67: "Write/Edit scoped to `vault/biomarkers/` (CV class), `vault/protocols/` (Z2/cardio), `vault/parameters/` (HR-zones)". Disk: `ls vault/parameters/` → "No such file or directory." Modes line 118 covers the empty read state.

**Fix:** Handle — already mitigated by Modes empty-state. No change strictly required. Optional: a one-clause note in Tools that owned write dirs are created on first authored entry would remove the ambiguity.

---

### AR-006: Communication "To the user" sentence pattern packs five `{...}` slots into one template sentence — dense but load-bearing

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy (compression vs clarity) |
| **Severity** | Nitpick |
| **Section** | Communication, "To the user" |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** The user-facing template "The evidence supports {GRADE certainty + causal/associational maturity}; what it does NOT establish is {non-causal / surrogate-only / screening-not-diagnostic / calibration caveat}; {worst-case risk / unknown}; {routing line if a floor or refusal fired}." is a dense four-clause fill-in. Passes the isolation test (each slot is named with concrete examples) and matches the gi sibling idiom exactly, so this is consistent and load-bearing, not bloat. Noted only because the density is at the edge of one-shot parseability for a fresh agent under a long-context dispatch.

**Evidence:** agent.md line 80.

**Fix:** Accept. Consistent with sibling; every slot is load-bearing.

---

### AR-007: "Mechanical Check" footer lines duplicate the gate logic that lives in the audit script — borderline document-to-reference duplication, but intentional per design

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy (B3 document-to-reference) |
| **Severity** | Low |
| **Section** | Every section's "**Mechanical Check:**" footer |
| **Resolution** | Accept |
| **Affected File** | N/A |

**Description:** Each section ends with a "**Mechanical Check:**" line that restates, in prose, the grep/field assertion the `audit-specialist-profile.sh --check` function performs (e.g., Role Boundaries: "≥4 taxonomy class IDs incl AUTHORITY_FRAMING_BYPASS (`grep -w`)"). This is B3-adjacent (the authoritative check lives in the script; the profile restates it). However, this is the established design idiom (design §5 "the mechanical check is authored before the prose"; the gi sibling does the same; §15.2 treats these as assertion targets), and the footer serves the fresh-agent self-verification purpose, not just the audit. Net: the duplication is intentional and load-bearing as an in-profile contract, within the 176-line / ≤200 budget and ≤2,500-token target. Not bloat to cut.

**Evidence:** agent.md lines 13, 40, 53, 63, 74, 82, 94, 109, 121 (nine Mechanical Check footers). Each mirrors a `--check` function verified present in `scripts/audit-specialist-profile.sh`.

**Fix:** Accept. The duplication is the design's deliberate self-check idiom and stays within budget.

---

## Stress-Test Results (the four highest-safety surfaces the brief named)

1. **Can the cardiac TIME_CRITICAL floor be read as bypassable?** No. Verified non-bypassable across all four paths:
   - Device-normal override: Core Rule 1 ("a normal device reading... does not clear it"), Core Rule 10 ("a normal device reading is explicitly stated NOT to clear a red-flag"), Loop-Breaking, Ask-vs-Proceed §3, Negative Example 12.1, Anti-Pattern 1 — five-way redundant.
   - Multi-turn "just give me the plan": Core Rule 1 + Loop-Breaking ("the floor persists across turns... a subsequent 'just give me the plan'... does NOT clear it; the floor re-fires") — explicit.
   - Authority/educational framing: GRADE override is "available ONLY for a lower-band non-safety claim, NOT on the cardiac emergency floor / H1–H2 / `risk_tier: medium+` surface (operator is A3)"; AUTHORITY_FRAMING_BYPASS holds framing separately.
   - "Atypical" loophole: explicitly retired ("'Atypical' is retired").

2. **Is the bromism-class clause concrete enough to fire?** Yes. Core Rule 11 names the specific molecule (potassium/KCl salt-substitute), the specific context (ACEi/ARB or CKD), the specific mechanism (hyperkalemia → fatal arrhythmia), the specific operator-state check, and a R7 HALT on an unpopulated ACEi-ARB/renal field. It is mapped to a refusal class + routing and reinforced in Ask-vs-Proceed §3, Anti-Pattern 3 cue, and Negative Example 12.4. It cannot be read as permitting a "chemically equivalent" answer — the Negative Example explicitly refuses the daily-amount request and the rule wording is "Render no chemically-correct-but-contextually-unsafe substitution."

3. **Is the no-compounds-write decision internally consistent everywhere?** Yes, in the agent.md: Role Boundaries ("a `vault/compounds/` write class — CV compounds... never owned compound writes"), Tools ("this role owns NO `vault/compounds/` write class"; Mechanical Check "no `vault/compounds/` write"), Modes (empty-state names only biomarkers|protocols|parameters), and library-index ("owns NO `vault/library/cardiovascular/` write class"). The one snag is AR-001: the library-index introduces a *read* surface (`vault/library/cardiovascular/`) that the design only contemplates as a conditional future addition tied to the compounds question — the write-disclaimer is consistent, but the read-path itself is unresolved. That is the single MEDIUM.

4. **Does the PRESCRIPTIVE_DIRECTIVE gate fire on a dosing request independent of framing?** Yes. Core Rule 8: "The gate is content-triggered — the request fires it, framing neither triggers nor relaxes it (framing-bypass held separately by `AUTHORITY_FRAMING_BYPASS`)." Ask-vs-Proceed §3 repeats "The gate is content-triggered; authority/educational framing relaxes none of these." This is the CV-SF-06 fix, correctly carried.

## Cross-File Pass (agent.md + library-index.md as one unit)

- **Contradictions between files:** None on the write surfaces. The no-compounds-write and no-`vault/library/cardiovascular/`-write disclaimers are consistent across both. The only cross-file issue is AR-001 (library-index read-path doesn't resolve).
- **Content duplicated across files:** The library-index `_source-whitelist.md` bullet and the agent.md Context Loading step 1 both reference the whitelist — appropriate (index routes, profile loads), not duplication.
- **References that don't match the referenced file:** AR-001 (`vault/library/cardiovascular/`). All other referenced paths/IDs resolve: all 6 PF-S#-## ids resolve in `memory/process-failures.md`; all 8 refusal-class IDs resolve in `templates/refusal-class-taxonomy.yaml`; `templates/specialist-risk-class.yaml` confirms cardiovascular-specialist = compound-medium/standard/compound; all 11 `--check` function names resolve in `scripts/audit-specialist-profile.sh`; `enforce-role-inlining.sh` exists; section count = 11 (matches the gate's expected 11).

## Agent-Specific Criteria

- **Operational completeness:** Every verb has a tool/workflow. "Dispatch" → `aplus-research --mode=standard --target-class=compound`; "ground" → Read against whitelist; "escalate a new class" → Agent (Architecture Question); "log a conflict" → Write to contradictions.md; "route" → medical-liaison / emergency services. No orphaned verb found. (The one orphaned *target* is the AR-001 read path.)
- **Scope creep:** None. The "I do NOT own" block correctly fences labs (shared lipid/inflammatory panels), endocrine (hormone axes), recovery (HR/HRV recovery framing, explicitly batch-4-not-deployed → contradictions.md), personal-trainer (training volume), and medical-liaison (patient-facing adjudication). HRV is correctly handled as a shared surface with runtime reconciliation, not claimed.
- **Token economics:** 176 lines / ~4,228 words, within the ≤200-line gate and the AGENT_TEMPLATE budget. The Mechanical Check footers (AR-007) are the densest duplication but are the design's intentional self-check idiom. No budget waste warranting a cut.
- **Personality traps:** None. The Identity section is observable-behavior framed ("recognize-and-route... hold causal apart from associational"); the banned-adjective set is absent (Identity Mechanical Check confirms, 29 words ≤40). Anti-sycophancy is encoded as observable rules (banned openers, maintain-position-without-new-evidence), not as an adjective.

## Coverage Matrix

| Section | A | E | C | R | O | S | D | L |
|---|---|---|---|---|---|---|---|---|
| Identity / IDENTICAL-BLOCK | clean | clean | AR-003 | clean | clean | clean | clean | clean |
| Core Rules (1-12) | clean | clean | clean | clean | clean | clean | clean | AR-004 |
| Role Boundaries | clean | clean | clean | clean | clean | AR-002 | clean | clean |
| Ask vs Proceed | clean | clean | clean | clean | clean (floor-first) | clean | clean | clean |
| Loop-Breaking | clean | clean | clean | clean | clean | clean | clean | clean |
| Tools | clean | AR-005 | clean | clean | clean | clean | clean | clean |
| Communication | clean | clean | clean | clean | clean | clean | clean (consumer fields match orchestrator intake) | AR-006 |
| Context Loading | clean | AR-005 | clean | clean | clean (order=dependency) | clean | clean | clean |
| Anti-Patterns | clean | clean | clean | clean (PF ids resolve) | clean | clean | clean | clean |
| Modes | clean | clean (empty-state covered) | clean | clean | clean | clean | clean | clean |
| Negative Examples | clean | clean | clean | clean | clean | clean | clean | AR-007 |
| library-index.md | clean | clean | clean | **AR-001** | clean | clean | AR-001 | clean |

All coverage-check boxes pass. Categories with zero findings (O Ordering, after probing): the Ask-vs-Proceed floor-first ordering and Context-Loading step-order-is-dependency-order were both probed against the floor-evaluated-first and contracts-before-data-layer requirements and are correct — the floor is step 2 (after only the authoritative-source read), evaluated before any optimization branch, with the GRADE override explicitly non-overridable on the floor. D (Downstream) probed: the Communication always-present(1-3)/conditional(4-8) field list matches the orchestrator intake idiom shared with the gi sibling; the standard/compound dispatch string and no-bare-deep-research are present for the audit gate; section count = 11 matches `check_section_count`.
