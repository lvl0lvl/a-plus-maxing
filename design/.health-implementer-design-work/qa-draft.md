---
title: QA Drafter — Role 2 (health-implementer) Pass-2 Design Doc Slice
type: drafter-output
drafter: qa (v1-substitute per CONTINUATION_BRIEF §7; will rotate post-S11)
created: 2026-05-27
status: draft-v1
target_design_doc: design/health-implementer-design.md
sections_authored: [11.1, 13-QA, 14, 15.2, 17, 18]
---

# QA Drafter — Role 2 (health-implementer) Pass-2 Design Doc Slice

QA-perspective slice for the Pass-2 design doc of Role 2 (health-implementer). Authored per `design/DESIGN_DOC_TEMPLATE.md` §11/§13/§14/§15/§17/§18 specs. Every section anchors to ≥1 Pass-1 Finding (F1–F9), Pass-1 Recommendation (R1–R15), Pass-1 Pattern (P1–P8), Pass-1 Contradiction (C1–C5), Project PF entry (PF-S2-01 through PF-S6-01), or Project Invariant (INV-*). Role 1 final design doc (`design/health-specialist-architect-design.md`) is referenced by section for inherited interface contracts.

The QA stance: the implementer's deliverable is 14 specialist agent.md files (one per `vault/WIKI.md` Agent Consumers row). The QA-tested surface is the union of those 14 files. Untested cross-specialist seams (IDENTICAL-block hash drift, DIFFER-block Jaccard violation, refusal-taxonomy enum-membership drift) are higher-risk than any single specialist's prose quality. This drafter slice biases toward audit-tests-not-yet-written; PROPOSED rows in §13 are the dominant tag.

---

## 11.1 Project PF Coverage (QA-side)

All 8 PF entries enumerated. For each: how Role 2's design surface defends against recurrence. Gap PFs (no Role 2 defense surface) explicitly flagged.

| PF | Behavior | Role 2 verdict | Defense surface (Role 2 section / rule that addresses it) |
|---|---|---|---|
| PF-S2-01 (self-attestation: declared deep-mode but skipped paired judges) | Orchestrator self-attests rigor without dispatched verifier output | IN-SCOPE | R13 self-audit (Pass-1 §3 Findings → R13) requires implementer to run `scripts/audit-specialist-profile.sh` against its own output and include exit-code in the returned `audit_passed: true` frontmatter; orchestrator rejects profiles missing this. Direct medical analog: implementer claiming "profile complete" based on word-count alone (Pass-1 R4 Anti-Pattern table, PF-S2-01 row). §15.2 AC-2 requires the audit-script artifact to exist + exit 0 for AC pass. Role 2 Core Rules MUST contain "I do not declare a profile complete without running the audit script and seeing all checks PASS" (Pass-1 Anti-Pattern catalog row 1, PF-S2-01). |
| PF-S2-02 (citation/attribution error caught by accident) | Citation propagated without per-citation source verification | IN-SCOPE | Implementer's Anti-Patterns section MUST cite PF-S2-02 directly per Pass-1 R11 (project-history-grounded Anti-Patterns) and Pass-1 R4 Anti-Pattern table row 2: "I don't copy DIFFER sections from sibling specialists verbatim. PF identifiers must match this role's domain." Audit row 13.7 (PF identifier regex + back-resolution check in PF log) is the mechanical guard. EC-3 (specialist row missing fields) covers the cross-side citation drift. |
| PF-S2-03 (over-questioning during scoping) | Asked questions answerable from context | IN-SCOPE | Implementer's Ask-vs-Proceed section inherits the architect's decision tree shape; Pass-1 F9 (implementer-vs-architect boundary) Worked Example A specifies the discipline: when the architect's template did not resolve a gap, dispatch a structured Architecture Question — never an open-ended question to the user. The Architecture Question artifact has a fixed shape (gap + interpretations + recommendation + awaiting-adjudication), which bounds question count. Pass-1 R14 establishes the channel. |
| PF-S2-04 (over-personalized library research; library-vs-dispatch conflation) | Goal-agnostic library work treated as personalization opportunity | IN-SCOPE | Direct analog per Pass-1 R4 Anti-Pattern table row 3: "I don't reuse role-specific prose across specialists. Boilerplate goes in the IDENTICAL block; role-specific goes in DIFFER." Pass-1 F7 IDENTICAL/DIFFER partition is the structural defense; R8 sentinel-comment wrapping + R9 Jaccard-ceiling are the audits. Worked Example B (refusal class needed for THIS role but not in canonical taxonomy) is the canonical PF-S2-04 inverse: implementer over-personalizes a shared taxonomy. §14 EC-6 covers this. |
| PF-S2-05 (operated from mental model of protocol rather than re-reading) | Pattern-matched prior reading as current knowledge | IN-SCOPE | Pass-1 R4 Anti-Pattern table row 5 + Pass-1 F9 process step "re-read the architect's template variant at each section boundary; do not work from mental model." Implementer process step 1 (re-read inputs) and step 8 (self-audit) bracket every authoring cycle. §14 EC-2 (12th template section drift) is the specific surface — implementer authors a 10-section profile because mental model of AGENT_TEMPLATE said "10 sections" while the project hook expects 11. |
| PF-S2-06 (branch hygiene — commits on main) | State-mutating git on wrong branch | CONDITIONAL — depends on Role 2 tool palette finalization | Pass-1 §3 does NOT enumerate Role 2's tool palette (that is the architect's design slot in §8). If Role 2 final §8 forbids state-mutating Bash git (consistent with Role 1's §8.3 forbid + project hooks), PF-S2-06 resolves OUT-OF-SCOPE — structural (Role 1 §8.4 pattern). If §8 permits state-mutating git, PF-S2-06 remains IN-SCOPE. **Recommendation to Role 2 architect/SE drafters:** mirror Role 1 §8.3 forbid; defense-in-depth structural verdict cleanest. FINDING: this PF's verdict depends on a §8 decision Role 2's drafters have not yet locked. (See §18 OQ-2.) |
| PF-S3-01 (self-attested 5 of 6 gates; mechanical-fix-confused-with-verdict) | Treated mechanical fix as verdict; did not re-dispatch verifier | IN-SCOPE | The canonical Role 2 surface. Pass-1 R4 Anti-Pattern table row 4 cites it directly: "Audit-script-pass is necessary but not sufficient. After passing, I dispatch a medical-safety-reviewer for runtime-behavior gate before declaring the profile ready." Direct mechanism: implementer treats audit-script exit 0 as proof of correctness; CDS Hooks 87–92.7% override evidence (Pass-1 Finding 5 / Limitation 7) demonstrates mechanically-valid rules fail at runtime. Defense: Role 2 Loop-Breaking encodes the "audit pass + Role-4 review required" dual gate; §13 row 13.1 / 13.2 enforce. AC-3 verifies the dual-gate clause's presence. |
| PF-S6-01 (acted on prior-session-described state without verifying current state) | HANDOFF claim treated as ground truth without verification | IN-SCOPE | Implementer's process step 1 (Pass-1 F9): "re-read inputs" — operator-profile, current-state, INVARIANTS.md, PF log, Role 1 design doc — at every dispatch start. Pass-1 Limitation 7 explicitly flags this dependency. §14 EC-7 (audit-script path drift) is a direct PF-S6-01 surface: the path Role 1's design doc cited may have moved between Role 1 finalize and Role 2 dispatch. Defense: implementer re-resolves all cited paths via Glob at dispatch start, demotes any missing to PROPOSED in its own deliverable. Audit row 13.3 (path-resolve check) is the mechanical guard. |

**Coverage attestation.** 8 of 8 PFs have a named defense surface in Role 2's design. PF-S2-06 is the only conditional — flagged for §18 OQ-2 because Role 2's §8 (Tools) authoring slot is owned by SE drafter, not QA drafter, and the verdict depends on §8's final shape. No Role 2 defense GAP for the other 7 PFs.

**Cross-link to Role 1.** Role 1's §11.1 resolved PF-S2-06 to OUT-OF-SCOPE — structural via §8.4 tool-palette finalization. Role 2's resolution should follow the same structural pattern unless Role 2's deliverable (producing 14 specialist profiles) requires state-mutating Bash that Role 1 did not need.

---

## 13. Mechanical Enforcement Map (QA quality-gate side)

**QA-side tagging discipline.** For each row, the QA-side concern is: does the mechanical check have a TEST that proves the check works? A check is LIVE only if a smoke test exists (path resolvable via Glob) that exercises the check against a negative case (i.e., the test confirms the check FAILS when given malformed input). REFERENCED rows cite an INV-* ID whose mechanical verification is already proven (its smoke tests are already passing per INVARIANTS.md). PROPOSED rows are checks whose test-for-the-check does not exist yet — regardless of whether the check itself exists. This tagging is intentionally stricter than Role 1's §13 (which tagged based on whether the CHECK existed); QA's role is to verify the test exists.

**Verification methodology.** For each row, ran Glob against the cited test path. PROPOSED if the test file does not resolve; LIVE only with positive Glob match. REFERENCED is tagged when an existing INV-* row's mechanical-verification column already names a passing smoke-test suite (INVARIANTS.md columns).

| # | Check | What it verifies (QA-side: does the CHECK's test exist?) | Mechanism path + smoke-test path | Status (QA-perspective) | Reason for PROPOSED |
|---|---|---|---|---|---|
| 13.1 | Identity word-count + banned-adjective (R1) | `wc -w` ≤40; banned-adjective regex `expert\|experienced\|world-class\|seasoned\|veteran\|years of` returns 0 | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_identity_word_count_negative` (PROPOSED) | PROPOSED | Neither check script nor its smoke test exists (Glob `scripts/audit-specialist-profile.sh` → no match; Glob `scripts/tests/test_audit_specialist_profile*` → no match) |
| 13.2 | Two-layer routing/behavior split (R2) | YAML parser asserts `description` length ≤200 chars; grep `description.*\b(use proactively\|use this when\|invoke when)\b` ≥1 | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_description_field_too_long` + `::test_description_missing_routing_cue` (PROPOSED) | PROPOSED | No smoke test exercises the negative case (long description; missing routing cue) |
| 13.3 | Body length ceiling (R3) | `wc -l body.md` ≤200; `tiktoken` count ≤2500 | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_body_over_200_lines` (PROPOSED) | PROPOSED | tiktoken-counting test against a 201-line negative fixture absent |
| 13.4 | Voice-register bans (R4) | `grep -cE "(YOU MUST\|NEVER EVER\|CRITICAL: \|IMPORTANT!)" = 0`; `grep -cE "\b[Yy]ou (must\|should\|will\|are\|need to\|have to)\b" ≤ 3` | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_banned_phrase_detection` + `::test_second_person_modal_budget_exceeded` (PROPOSED) | PROPOSED | No smoke test against banned-phrase fixture; no smoke test against ≥4-instance `\bYou must\b` fixture |
| 13.5 | Refusal-class taxonomy enum-membership (R5) | ≥4 distinct class identifiers per specialist; each matches an entry in architect's canonical-taxonomy file (read at audit time) | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Canonical taxonomy file: location TBD per §18 OQ-3. Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_invented_refusal_class_rejected` (PROPOSED) | PROPOSED | The taxonomy file's canonical path is itself open (§18 OQ-3); smoke test can't be written until the path is fixed |
| 13.6 | Affirmative trigger phrasing (R6) | `grep -cE "(if not\|unless\|except when).*refuse"` low; affirmative-pattern grep ≥4 | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_negated_refusal_detected` (PROPOSED) | PROPOSED | No smoke test exercises the negated-trigger fixture; threshold "low" itself is under-specified |
| 13.7 | Per-section Mechanical Check stub presence (R7) | Pre-commit hook asserts every section header has a paired `**Mechanical Check:**` line | Check: `scripts/audit-specialist-profile.sh` (PROPOSED) OR project pre-commit hook (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_section_missing_mech_check` (PROPOSED) | PROPOSED | Pre-commit-hook path not yet decided; smoke test absent |
| 13.8 | IDENTICAL-block hash match (R8) | `sha256sum` of `<!-- IDENTICAL-BLOCK-START --> ... <!-- IDENTICAL-BLOCK-END -->` matches across all 14 specialist profiles | Check: `scripts/audit-specialist-profile.sh` (PROPOSED) cross-file pass. Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_identical_block_drift_detected` (PROPOSED) | PROPOSED | Cross-file hash audit is the highest-value novel check Role 2 introduces; no test fixture (2 specialists with intentional IDENTICAL drift) exists |
| 13.9 | DIFFER-block Jaccard ceiling (R9) | Pairwise Jaccard similarity ≤0.30 between any two specialists' DIFFER blocks | Check: `scripts/audit-specialist-profile.sh` (PROPOSED) + Python similarity script (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_jaccard_ceiling_violation` (PROPOSED) | PROPOSED | Threshold itself is v1-calibration-pending (Pass-1 Limitation 9); test cannot anchor against a threshold that may move |
| 13.10 | Negative Examples count + harmful-content denylist (R10) | ≥3 stimulus-response pairs per specialist; harmful-content denylist regex returns 0 | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_neg_example_count_below_3` + `::test_harmful_content_inlined_detected` (PROPOSED) | PROPOSED | Denylist regex itself not authored (Pass-1 Finding 8); cannot test against unauthored denylist |
| 13.11 | Project-history-grounded Anti-Patterns (R11) | Anti-Patterns section ≥3 distinct `PF-S\d+-\d+` identifiers; each resolves in `memory/process-failures.md` | Check: `scripts/audit-specialist-profile.sh` (PROPOSED) — pattern count + back-resolution. Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_unresolvable_pf_id_rejected` (PROPOSED) | PROPOSED | No smoke test against fabricated-PF-ID fixture (e.g., `PF-S99-99`) |
| 13.12 | aplus-research mode floor per role (R12) | `grep -E "aplus-research.*--mode.*(standard\|deep\|ultradeep)"` ≥1 in Tools section | Check: `scripts/audit-specialist-profile.sh` (PROPOSED). Smoke test: `scripts/tests/test_audit_specialist_profile.sh::test_mode_floor_missing` (PROPOSED) | PROPOSED | Mode-floor default per role is itself an open question (Pass-1 F9 + §18 OQ-1); cannot test against undefined default |
| 13.13 | Self-audit dual gate (R13 + PF-S3-01 medical analog) | Returned profile carries `audit_passed: true` in frontmatter AND a downstream-required Role-4 review log path is referenced | Check: orchestrator-level (PROPOSED at orchestrator side; not a `scripts/audit-specialist-profile.sh` row). Smoke test: not yet defined (PROPOSED) | PROPOSED | Orchestrator-side check; Pass-1 R13 specifies the mechanism but the orchestrator's enforcement path is not yet wired |
| 13.14 | Role-profile inlining at dispatch | Agent dispatches matching role-context inline the full 11-section profile verbatim | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook; smoke tests `hooks/tests/test_enforce_role_inlining.sh` (8/8 pass per INVARIANTS.md row 9) | REFERENCED (INV-ROLE-INLINING) | — (existing test suite passes; QA inherits) |
| 13.15 | Branch hygiene (no commits on main) | Working commits on `feature/*` / `fix/*`, never `main` | `.claude/hooks/block-push-main.sh` + `.claude/hooks/block-commit-main.sh`; smoke tests `.claude/hooks/tests/test_block_commit_main.sh` (21/21 pass per INVARIANTS.md row 11) | REFERENCED (INV-BRANCH-NOT-MAIN) | — (existing test suite passes; QA inherits) |
| 13.16 | aplus-research gate JSON attestation chain (downstream-template REFERENCE) | Specialists dispatching aplus-research inherit INV-RESEARCH-ATTESTATION at runtime | `.claude/skills/aplus-research/lib/gate_attest.py` + schema; smoke tests `tests/test_gate_attest.py` (9/9 pass per INVARIANTS.md row 3) | REFERENCED-by-template-for-downstream (INV-RESEARCH-ATTESTATION) | — (downstream-runtime reference; Role 2 implementer itself does not dispatch aplus-research, mirrors Role 1 §13 row 9 disposition) |

**QA-side tag counts.** LIVE: 0. REFERENCED: 3 (rows 13.14 / 13.15 / 13.16). PROPOSED: 13 (rows 13.1 through 13.13).

**Why zero LIVE.** The defining QA tag-rule: LIVE requires a smoke test that proves the check catches a negative case. `scripts/audit-specialist-profile.sh` does not exist (Glob confirmed); therefore no smoke tests for any of its sub-checks exist. The 3 REFERENCED rows are project-wide infrastructure with already-passing smoke suites recorded in INVARIANTS.md — those are LIVE at the project level, REFERENCED from Role 2's perspective (Role 2 inherits, does not own).

**§18 mirror.** All 13 PROPOSED rows mirror to §18 OQ-1 (collective pointer) per template §13/§18 budget compression pattern Role 1 §13 used (OQ-5 there).

**FINDING (against Role 1 §13).** Role 1 §13 tagged rows 1-7, 11-17 PROPOSED with rationale "`scripts/audit-specialist-profile.sh` does not exist." That is the **check-not-built** PROPOSED rationale. The **QA-stricter** PROPOSED rationale (used here in Role 2's §13) is "the test that proves the check works does not exist." Role 1 conflates the two in places — e.g., row 8 (Role 1) is tagged REFERENCED for INV-ROLE-INLINING citing the passing smoke suite, which is correct under the QA-strict rule; but Role 1 row 14 (H-class composition) is PROPOSED without distinguishing whether the H-class check or the H-class-check's test is the gap. FINDING: SHOULD FIX (Role 1 §13 row 14, line 488 of `design/health-specialist-architect-design.md`) — clarify whether the gap is the check or the test-for-the-check.

---

## 14. Edge Cases

Each EC: situation / handler (named §5/§6/§7/§11.2/§13/§14 surface in Role 2's design that addresses it) / test stimulus (concrete input the implementer must handle the named way). Following Role 1's 14-EC shape with Role-2-specific surfaces.

### EC-1 — Persona-prose creep into Identity

**Situation.** Implementer drafts `peptide-specialist` Identity as "You are an expert peptide pharmacologist with 20 years of compounded therapeutic experience..." per the naive intuition that medical specialists should be richly personified. Pass-1 Finding 1 + Limitation 10 establish this as the highest-stakes failure: Wharton/Zheng/USC PRISM evidence (9 negative effects, 0 positive; arXiv:2311.10054; 3.6pp negative on MMLU). Sub-domain personification (e.g., "expert peptide pharmacologist") has not been independently tested but inherits the parent finding's bound.

**Handling.** Audit row 13.1 (Identity word count ≤40 + banned-adjective regex) catches at audit time. Implementer's Core Rules MUST encode the ≤40-word ceiling (R1) AND the banned-adjective regex (Pass-1 Finding 1 "Implementer's discipline" table row 1). Process-step 8 self-audit catches before return. §11.2 Anti-Pattern (Role 2's): "I don't enrich Identity with persona prose; Identity is one declarative sentence ≤40 words."

**Test stimulus.** Synthetic peptide-specialist Identity prose 47 words long, containing "experienced" and "world-class" adjectives. Expected: audit row 13.1 returns FAIL (word count = 47 > 40; banned-adjective grep = 2 > 0); implementer halts return; redrafts to ≤40-word declarative-third-person form per Pass-1 Finding 1 voice-register reconciliation table.

### EC-2 — Section drift between AGENT_TEMPLATE.md (10 base + Modes) and project hook (11 sections expected)

**Situation.** AGENT_TEMPLATE.md defines 10 base sections; the project's `enforce-role-inlining.sh` hook expects 11 (the 10 base + Modes) for role-tagged dispatches. The implementer drafts a 10-section profile working from mental model of AGENT_TEMPLATE (the PF-S2-05 surface) and never opens the hook config to verify the expected count. The 14th specialist's profile is the first to surface the gap when dispatch fails.

**Handling.** Audit row 13.7 (per-section Mechanical Check stub presence) ALONE is insufficient — it audits within-section content, not section count. Need a dedicated section-count audit: `grep -cE '^## ' specialist.md` returns 11 (the 10 base sections + Modes when present per AGENT_TEMPLATE Phase-5 synthesis decision per Role 1 §5 line 626). §13 row 13.6.5 needed (FINDING: this audit is missing from §13 above; ADD: "Section header count" row at 13.6.5 with PROPOSED tag). §11.2 Anti-Pattern: "I don't enumerate template sections from memory; I re-open `enforce-role-inlining.sh` and `AGENT_TEMPLATE.md` at the section-count check." Process step 1 re-read inputs covers it.

**Test stimulus.** Synthetic specialist profile with 10 section headers (Identity through Negative Examples, no Modes). Dispatch attempt against `enforce-role-inlining.sh` PreToolUse hook. Expected: hook BLOCKs with `expected 11 sections, found 10`; specialist not dispatched. Audit-script side: `grep -cE '^## '` returns 10, audit row 13.6.5 returns FAIL (when added per FINDING above).

### EC-3 — Specialist row in WIKI.md missing or incomplete

**Situation.** Implementer is authoring `medical-liaison` but the WIKI.md row's "Dispatches research on" column is `none — collates only`. The implementer's process step 5 (Pass-1 F9) says "Author DIFFER block: Dispatched-research targets (which aplus-research target_class)." When the row says `none`, what does the implementer write in the Tools section's `aplus-research` mode-floor field?

**Handling.** Implementer dispatches an Architecture Question (Pass-1 R14) rather than picking a default. The Architecture Question states the row's `none` value, the section field requiring a value, and a recommended interpretation (e.g., "Tools section omits `aplus-research` entry entirely; medical-liaison does not dispatch research"). Halt authoring until adjudicated. §14 EC-3 handler is Pass-1 F9's escalation discipline, not a silent default. Audit row 13.12 (mode floor present) returns FAIL until the row is filled OR an explicit "no research dispatch" exception is encoded.

**Test stimulus.** Synthetic WIKI.md row with `Dispatches research on: none — collates only`. Implementer authors `medical-liaison` profile. Expected: Architecture Question artifact written to `design/.health-implementer-design-work/architecture-questions/AQ-001-medical-liaison-tools.md`; specialist profile NOT returned; orchestrator queue gains the question. If implementer instead silently writes `aplus-research --mode=standard` in Tools section, FINDING: pattern-matching shortcut consumed an architectural decision.

### EC-4 — IDENTICAL boilerplate diverges across specialists (hash mismatch)

**Situation.** Implementer authors specialists 1-7 with one version of the IDENTICAL block; between specialists 7 and 8, Role 1's design doc gains a Phase-6 disposition updating the refusal-class taxonomy (e.g., 8th class `AUTHORITY_FRAMING_BYPASS` added per Role 1 F-S2). Implementer drafts specialist 8 with the NEW taxonomy in the IDENTICAL block, not noticing that specialists 1-7 carry the OLD 7-class version. SHA-256 hash mismatch across the 14 deployed profiles.

**Handling.** Audit row 13.8 (IDENTICAL-block hash match across all 14) catches at the cross-file pass. Pass-1 Insight 7 (context-pressure failure) specifies the audit must run BETWEEN every specialist authoring, not at the end of a 14-profile batch. Process-step discipline: the implementer's return value includes a hash of the IDENTICAL block as authored; orchestrator compares against the prior specialist's hash; mismatch → HALT all subsequent authoring + dispatch a remediation pass to update specialists 1-7. §11.2 Anti-Pattern: "I don't author the IDENTICAL block from prose memory; I read the canonical block file at the start of every specialist authoring cycle."

**Test stimulus.** Synthetic: author specialists 1-7 with IDENTICAL block hash A; author specialist 8 with hash B (one differing character). Run cross-file audit. Expected: audit row 13.8 returns FAIL with both hashes named; orchestrator HALT signal; remediation queue gains 7 entries (specialists 1-7) for IDENTICAL-block re-sync.

### EC-5 — aplus-research mode-floor wrong default (compound-class specialist gets `--mode=standard`)

**Situation.** Implementer authors `peptide-specialist` (compound-class writer per WIKI.md row) and encodes Tools section's `aplus-research` entry with `--mode=standard`. Pass-1 R12 (Insight 8) specifies peptide-specialist defaults `--mode=deep` because all peptide research lands at `risk_tier=experimental`. The implementer pattern-matched the lower-friction default. The mode floor is a DIFFER field (Pass-1 R12), not IDENTICAL, so audit row 13.8 (IDENTICAL-block hash) does not catch it.

**Handling.** Audit row 13.12 (mode-floor present) catches "missing" but not "wrong default." Need a DIFFER-field correctness audit: for each specialist, mode-floor MUST be ≥ the role's risk-class-derived minimum (peptide-specialist + supplement-specialist + endocrine-specialist with TRT compounds → `deep`; sleep-coach + nutritionist → `standard` floor). FINDING: §13 row 13.12 is incomplete — it audits presence, not correctness. ADD row 13.12.5 "mode-floor correctness vs risk-class" PROPOSED. Implementer's process step 5 (DIFFER authoring) needs an explicit step "consult WIKI.md row + risk-class for mode-floor selection." §11.2 Anti-Pattern: "I don't default `aplus-research --mode` to `standard` for compound-class specialists; I look up the risk-class-derived floor."

**Test stimulus.** Synthetic `peptide-specialist` with `aplus-research --mode=standard` in Tools section. Expected: audit row 13.12.5 returns FAIL with "peptide-specialist risk-class implies `--mode=deep` floor; profile has `standard`"; implementer halts return.

### EC-6 — Operator-profile schema changes between specialists 1 and 14

**Situation.** Implementer authors specialists 1-5 referencing `vault/meta/operator-profile.md` fields `medications`, `allergies`, `hard_limits`. Between specialists 5 and 6, the operator-profile schema gains a new field `prescribing_practice` (the prescribing physician's name and contact). Specialists 6-14 reference the new field; specialists 1-5 do not. The implementer did not re-resolve the schema between specialists.

**Handling.** Process step 1 (re-read inputs) at every dispatch start must include operator-profile schema. Audit row 13.6.6 (PROPOSED — schema-drift check): for each specialist, the set of operator-profile fields referenced is a subset of the current operator-profile schema field set. If specialist references a field not in current schema OR schema gained a field that ≥N specialists should reference, audit returns WARN. §14 EC-6 handler: implementer halts authoring + dispatches an Architecture Question if schema drift detected. §11.2 Anti-Pattern: "I don't carry operator-profile field references from prior specialist authoring; I re-read the schema at every dispatch."

**Test stimulus.** Synthetic: specialist 1 authored against operator-profile schema v1 (3 fields); operator-profile schema bumps to v2 (4 fields) before specialist 2 authoring; specialist 2 authored without re-reading schema. Expected: audit row 13.6.6 returns WARN; orchestrator queue gains "schema-drift remediation for specialist 1" entry.

### EC-7 — Audit-script path drift (Role 1 cited path moved before Role 2 dispatch)

**Situation.** Role 1's design doc cited `scripts/audit-specialist-profile.sh` as the audit path. Between Role 1 finalize and Role 2's dispatch (sessions may pass), the script's canonical location is finalized at `scripts/specialist-audit/audit.sh` (different path). Implementer's process step 1 reads Role 1 design doc and references the OLD path. Implementer's self-audit step (process step 8) tries to invoke a path that does not resolve.

**Handling.** Process step 1 re-read includes path-resolution check: every audit-script path cited in Role 1 design doc is Glob-verified at implementer dispatch start. Mismatch → implementer halts authoring + dispatches an Architecture Question with the path-resolution failure. §11.2 Anti-Pattern: "I don't carry path strings from prior-session-finalized design docs; I re-resolve via Glob at dispatch start." Audit row 13.13 self-audit (R13) carries the path-resolution as a precondition.

**Test stimulus.** Synthetic: Role 1 design doc cites `scripts/audit-specialist-profile.sh`; actual path is `scripts/specialist-audit/audit.sh`. Implementer dispatches. Expected: implementer's process step 1 Glob fails; Architecture Question artifact created; specialist authoring not started until adjudicated. If implementer instead proceeds and invokes the OLD path (which fails with "file not found"), FINDING: process step 1 path-resolution was skipped.

### EC-8 — Refusal-class enumeration is incomplete (fewer than 4 classes)

**Situation.** Implementer authors `sleep-coach` (lower-risk role) and encodes only 2 refusal classes (`PATIENT_FACING_DIRECTIVE`, `PRESCRIPTIVE_DIRECTIVE`) on the reasoning that sleep-coach has lower regulatory exposure than peptide-specialist. Pass-1 R5 specifies ≥4 distinct canonical classes per specialist regardless of risk class.

**Handling.** Audit row 13.5 (≥4 distinct class identifiers per specialist) catches at audit time. Implementer's process step 5 (DIFFER authoring) must enumerate ≥4 from the architect's canonical taxonomy regardless of perceived role risk. §11.2 Anti-Pattern: "I don't drop refusal classes based on role-risk intuition; the ≥4 floor is structural per R5." Edge case is the inverse of EC-1's persona-prose enrichment: under-specification of a structural floor rather than over-specification of a banned section.

**Test stimulus.** Synthetic `sleep-coach` with 2 refusal classes in Role Boundaries. Expected: audit row 13.5 returns FAIL with "2 < 4 distinct refusal-class identifiers"; implementer adds 2 more from canonical taxonomy. If the 4 added are not all in the canonical taxonomy file (e.g., implementer invents `DROWSY_DRIVING_ADVICE`), audit 13.5 sub-check (enum-membership against architect's taxonomy file) returns FAIL — see also Worked Example B (Pass-1 F9, line 324 of `domain-research.md`).

### EC-9 — GRADE axis collapsed (certainty + recommendation-strength merged into one tag)

**Situation.** Implementer authors `cardiovascular-specialist` Core Rules and encodes "evidence rating: moderate" as a single tag rather than the two-axis tag `[certainty: moderate, strength: weak]` required by Role 1 §5 Rule 12 (GRADE two-axis tagging). The implementer pattern-matched a simpler tag form. Role 1 explicitly states "The architect does not collapse the two axes into a single 'evidence rating.'"

**Handling.** Audit row 13.X (PROPOSED — GRADE two-axis presence): `grep -cE "(certainty:\s*(high\|moderate\|low\|very-low))" + grep -cE "(strength:\s*(strong\|weak\|conditional))"` — both must be ≥1 per claim block. Implementer's Core Rules MUST inherit Role 1 §5 Rule 12 verbatim with HALT condition encoded. §11.2 Anti-Pattern: "I don't collapse GRADE's two axes into a single rating tag; certainty and strength are structurally distinct." FINDING: §13 above lacks an explicit GRADE two-axis row; ADD row 13.5.5 PROPOSED.

**Test stimulus.** Synthetic `cardiovascular-specialist` Core Rules containing 5 claim blocks, each tagged "evidence: moderate" (single axis). Expected: audit row 13.5.5 (when added) returns FAIL with "5 claims have single-axis tag; require two-axis [certainty + strength]"; implementer redrafts.

### EC-10 — H-class downgrade attempt (specialist encodes H4 for outcome Role 4 would call H2)

**Situation.** Implementer authors `peptide-specialist` and labels BPC-157 outcome as H-class H4 (hospitalization) when Role 4's worst-case-reachable analysis would classify it H2 (life-threatening) based on the bromism-class context-mismatch (Role 1 substrate citing Annals 2024/2025). Implementer's reasoning: BPC-157 has long anecdotal use without H2 outcomes. Role 1 §4 OUTBOUND row 2 + §5 Rule 13 specifies `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`; H1/H2 auto-block.

**Handling.** Audit row 13.X (PROPOSED — H-class composition correctness, inherits Role 1 §13 row 14): for each compound entry the specialist writes, the H-class tag is ≥ Role 4's worst-case-reachable analysis (read from Role 4 evaluation-log file per Role 1 §13 row 15). Implementer cannot downgrade. §11.2 Anti-Pattern: "I don't downgrade H-class based on long-use intuition; the composition rule selects max, not specialist-preferred." Implementer's process step 8 self-audit precondition includes Role 4 evaluation-log lookup.

**Test stimulus.** Synthetic compound entry with H-class H4 tag; Role 4 evaluation log file lists same compound with worst-case-reachable H2. Expected: audit returns FAIL via composition rule (max selects H2); implementer cannot ship the H4-labeled compound. If Role 4 log absent (pre-Role-4 phase), Role 1 §17.2 A-7 v1-substitute fallback applies: software security agent's verdict log substitutes.

### EC-11 — Upstream design-doc bibliography mismatch (Role 1 Findings table row count drift)

**Situation.** Role 1's design doc has 9 Findings rows in §3.1. The implementer's process step 1 reads Role 1 §3 and references "Finding N" for N ∈ [1, 9]. Between Role 1 finalize and Role 2 dispatch, Role 1 §3 gains a 10th Finding (e.g., from a post-Phase-5 disposition extension). Implementer's references are still bounded at N ≤ 9.

**Handling.** Process step 1 re-read includes counting Role 1 §3.1 rows via `grep -c "^| [0-9]"`; result must match the count the implementer cites in its own DIFFER content. Mismatch → implementer halts + Architecture Question. Audit row 13.X (PROPOSED — upstream bibliography sync): the count of "Finding N" references in specialist profiles is consistent with current Role 1 §3.1 row count. §11.2 Anti-Pattern: "I don't cite upstream Finding numbers from cached count; I re-grep the upstream §3.1 table at dispatch start."

**Test stimulus.** Synthetic: Role 1 §3.1 row count = 10; implementer's profile cites only Findings 1-9. Expected: process step 1 detects the count mismatch (10 ≠ 9); Architecture Question. If proceed silently, FINDING: PF-S2-05 mental-model invocation.

### EC-12 — BAD/GOOD pair count below floor (specialist ships with 2 pairs)

**Situation.** Implementer authors `gi-specialist` with 2 BAD/GOOD pairs in Negative Examples (Pass-1 R10 floor is ≥3 per specialist). Implementer's reasoning: the third anti-pattern in §11 is covered structurally by §13 mechanical check. Pass-1 R10 specifies the ≥3 floor structurally regardless of mechanical coverage.

**Handling.** Audit row 13.10 (≥3 stimulus-response pairs) catches at audit time. §11.2 Anti-Pattern: "I don't drop Negative Example pairs on the reasoning that §13 covers them; the floor is structural per R10." Note this distinguishes Role 2 from Role 1 §12 disposition (Role 1 has 4 pairs covering 4 of 8 anti-patterns with prose rationale for the other 4 covered by mechanical checks — Role 1 §12 line 369). Role 2's surface is different: Role 2 produces 14 specialists, each of which must meet the ≥3 floor independently; the rationale-shortcut Role 1 used does not transfer.

**Test stimulus.** Synthetic `gi-specialist` with 2 BAD/GOOD pairs. Expected: audit row 13.10 returns FAIL with "2 < 3 stimulus-response pairs"; implementer adds a third. The added pair must satisfy harmful-content denylist (Pass-1 Finding 8); if implementer adds a pair containing actual unsafe dose+drug pairing, denylist regex catches.

### EC-13 — Cross-specialist DIFFER content drift (Jaccard >0.30)

**Situation.** Implementer authors `endocrine-specialist` DIFFER block by largely copying `cardiovascular-specialist` DIFFER block and changing 25% of the prose. Jaccard similarity between the two DIFFER blocks: 0.62 > 0.30 threshold (Pass-1 R9). This is the canonical PF-S2-04 inverse failure mode (Pass-1 Anti-Pattern catalog row 3).

**Handling.** Audit row 13.9 (Jaccard ≤0.30 across all pairs) catches at audit time. §11.2 Anti-Pattern: "I don't copy DIFFER content from sibling specialist as starting point; I author from the WIKI.md row + this role's domain." Note Pass-1 Limitation 9 flags the 0.30 threshold as v1-calibration-pending; the audit's PROPOSED status is calibration-blocked.

**Test stimulus.** Synthetic: author `endocrine-specialist` DIFFER block as 75%-copy of `cardiovascular-specialist`. Run pairwise Jaccard. Expected: audit row 13.9 returns FAIL with Jaccard 0.62 > 0.30; implementer redrafts DIFFER from scratch using WIKI.md row.

### EC-14 — Duplicate section header in produced agent.md (e.g., two `## Core Rules`)

**Situation.** Implementer authors a specialist with mid-cycle context loss (e.g., long authoring session, fatigue per Pass-1 Insight 7) and produces an agent.md with two `## Core Rules` headers — one near the top, one mid-file. The 11-section count via `grep -cE '^## '` returns 12 (the duplicate + 11 legitimate); the section-count audit passes BUT the inlining hook chokes on the duplicate.

**Handling.** Audit row 13.X (PROPOSED — section-header uniqueness): `grep -E '^## ' specialist.md | sort | uniq -c | awk '$1 > 1'` returns empty (i.e., zero duplicate section headers). FINDING: §13 above lacks this row; ADD row 13.7.5 PROPOSED. §11.2 Anti-Pattern: "I don't return a profile without grep-checking section-header uniqueness; mid-file duplicates fail downstream consumers silently." Process step 8 self-audit must include the uniqueness check.

**Test stimulus.** Synthetic specialist with `## Core Rules` appearing twice. Expected: audit row 13.7.5 (when added) returns FAIL with the duplicated header name; implementer removes the duplicate.

---

**Edge case count: 14** (matches Role 1's 14 ECs structurally; covers persona drift, section drift, row gaps, IDENTICAL drift, DIFFER drift, mode-floor errors, schema drift, path drift, refusal-class under-spec, GRADE collapse, H-class downgrade, upstream bibliography drift, BAD/GOOD floor, duplicate headers).

---

## 15.2 Role-Specific Binary Acceptance Criteria

Each AC is binary: a single bash / grep / wc / exit-code command resolves PASS vs FAIL. ACs where pass/fail needs explanation are moved to §18 (not allowed in §15.2 per task constraint).

### AC-1 — `scripts/audit-specialist-profile.sh` artifact exists

**Mechanism.** `test -x scripts/audit-specialist-profile.sh && echo PASS || echo FAIL`

**Pass criterion.** Exit 0 + "PASS". Resolves binary.

**Anchor.** Pass-1 Finding 6 + Finding 9; Role 1 §13 PROPOSED rows depend on this script; Role 1 §15 AC-1.

### AC-2 — All 14 specialist profiles pass `scripts/audit-specialist-profile.sh`

**Mechanism.** `for f in .claude/agents/*-specialist/agent.md .claude/agents/*-coach/agent.md .claude/agents/*-trainer/agent.md .claude/agents/*-nutritionist/agent.md .claude/agents/*-strategist/agent.md .claude/agents/*-liaison/agent.md; do scripts/audit-specialist-profile.sh "$f" || exit 1; done && echo PASS`

**Pass criterion.** All 14 invocations exit 0. Binary on count + exit code.

**Anchor.** Pass-1 R13 (self-audit before return); Insight 7 (per-profile not batch-end audits).

### AC-3 — Self-audit dual gate clause present in Role 2 Loop-Breaking

**Mechanism.** `grep -cE "(audit.*pass.*necessary.*not.*sufficient|Role.4.*review.*before.*declar)" design/health-implementer-design.md` ≥1

**Pass criterion.** Grep count ≥1. Binary.

**Anchor.** Pass-1 R4 Anti-Pattern table row 4 (PF-S3-01 medical analog); CDS Hooks 87-92.7% override evidence (Pass-1 Finding 5 / Limitation 7).

### AC-4 — All 15 Pass-1 Recommendations have a verdict in §3.2

**Mechanism.** `awk -F'|' '/^\| R[0-9]+/{n++; if($4 !~ /ACCEPTED|DEFERRED|REJECTED/) exit 2}END{exit (n==15)?0:3}' design/health-implementer-design.md && echo PASS`

**Pass criterion.** Exit 0 (15 rows present, every verdict in allowed set, no TBD). Binary.

**Anchor.** Template §3 spec; Role 1 §15 AC-3 mirror.

### AC-5 — All 9 Pass-1 Findings have an AGENT_TEMPLATE section anchor in §3.1

**Mechanism.** `grep -c "^| [0-9]" design/health-implementer-design.md | head -1` ≥9 lines in §3.1 table AND `awk -F'|' '/^\| [0-9]/{if($4=="" || $4 ~ /^\s*$/) exit 2}END{exit 0}'`

**Pass criterion.** Row count ≥9 + every section-anchor column non-empty. Binary on count + non-emptiness.

**Anchor.** Template §3 spec; substrate Finding count = 9 (verified via `grep -cE "^### Finding " design/.health-implementer-design-work/domain-research.md` = 9).

### AC-6 — IDENTICAL-block sentinel comments present in canonical block file

**Mechanism.** `grep -cE "<!-- IDENTICAL-BLOCK-(START\|END) -->" templates/IDENTICAL-block.md` = 2

**Pass criterion.** Grep count = 2 (one START, one END). Binary.

**Anchor.** Pass-1 R8; Finding 7.

### AC-7 — Identity word count ≤40 across all 14 specialists

**Mechanism.** `for f in .claude/agents/*/agent.md; do c=$(awk '/^## Identity/,/^## /' "$f" | grep -v '^##' | wc -w); [ $c -le 40 ] || exit 1; done && echo PASS`

**Pass criterion.** Every specialist's Identity section ≤40 words. Exit 0. Binary.

**Anchor.** Pass-1 Finding 1 + R1; Wharton/Zheng/PRISM evidence.

### AC-8 — Banned voice-register phrases return zero across all 14 specialists

**Mechanism.** `grep -clE "(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)" .claude/agents/*/agent.md | awk '$1>0{exit 1}' && echo PASS`

**Pass criterion.** No specialist contains banned voice-register phrases. Exit 0. Binary.

**Anchor.** Pass-1 R4 / Finding 4; Anthropic 4.5/4.6 guidance; April 2026 postmortem (3% regression).

### AC-9 — Every specialist Anti-Patterns section cites ≥3 distinct PF-S\d+-\d+ identifiers resolving in PF log

**Mechanism.** `for f in .claude/agents/*/agent.md; do count=$(grep -oE "PF-S[0-9]+-[0-9]+" "$f" | sort -u | wc -l); [ $count -ge 3 ] || exit 1; for pf in $(grep -oE "PF-S[0-9]+-[0-9]+" "$f" | sort -u); do grep -q "^### $pf " memory/process-failures.md || exit 2; done; done && echo PASS`

**Pass criterion.** Every specialist has ≥3 distinct PF IDs AND every cited ID resolves in `memory/process-failures.md`. Exit 0. Binary.

**Anchor.** Pass-1 R11; Anti-Pattern catalog table.

### AC-10 — aplus-research mode floor declared in Tools section of every compound-class specialist

**Mechanism.** `for f in .claude/agents/{peptide,supplement,endocrine,cardiovascular,gi,longevity,mental-performance,sleep,recovery,lymphatic,medical-liaison}-{specialist,coach,strategist,liaison}/agent.md 2>/dev/null; do grep -qE "aplus-research.*--mode.*(standard\|deep\|ultradeep)" "$f" || exit 1; done && echo PASS`

**Pass criterion.** Every compound-class specialist Tools section names an aplus-research mode floor. Binary.

**Anchor.** Pass-1 R12 + Insight 8.

---

**AC count: 10** (within the 6-10 target range; binary mechanisms named for each).

**FINDING (against Role 1 §15.2).** Role 1 AC-4 (`design/health-specialist-architect-design.md` line 641) calls out an empirical defect: `grep -cE` counts lines not unique identifiers, returning 4 when the doc had all 8 identifiers. The fix is `grep -oE | sort -u | wc -l`. Role 2's ACs above use the `-oE | sort -u | wc -l` pattern proactively (AC-9 specifically) per Role 1's lesson. SHOULD FIX (already fixed in Role 1 per F-001 disposition, but worth carrying as a Role 2 drafter discipline).

---

## 17. Risk Assessment, Assumptions, and Break Conditions

### 17.1 Risk Assessment

| # | Risk | Mechanism | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | Implementer treats audit-script exit 0 as proof of correctness (PF-S3-01 medical analog) | CDS Hooks empirical floor: 87-92.7% override rate even when mechanical-check passes (Pass-1 Finding 5 / Limitation 7). Per-section grep counts pass while runtime behavior fails | BLOCK | Pass-1 R4 Anti-Pattern row 4 dual-gate clause in Loop-Breaking; AC-3 verifies the clause's presence; §13 row 13.13 audits the Role-4 review log reference; Pass-1 Insight 7 specifies between-specialist audits not batch-end |
| R-2 | 14-profile batch context-pressure degradation (Pass-1 Insight 7) | Implementer fatigue compounds across profiles 7+; copy-paste shortcuts increase; IDENTICAL-block drift and DIFFER-block similarity violations cluster in late profiles | BLOCK | §13 row 13.8 (IDENTICAL hash) + row 13.9 (Jaccard) catch at audit; orchestrator runs the audit BETWEEN every specialist authoring, not at batch end; if any profile fails, halt the whole batch and surface the failure-pattern (e.g., "profile 8 inherits profile 7's drifted IDENTICAL block") |
| R-3 | Architecture Question channel not yet operationalized (Pass-1 Limitation 8) | Implementer's escalation path assumes the orchestrator routes Architecture Questions to architect; if architect role not deployed or the routing path is undefined, Architecture Questions accumulate without resolution; implementer either halts indefinitely or starts inferring | WARN | §18 OQ-4 surfaces this; until OQ-4 is resolved, the Architecture Question artifact is a stored file at `design/.health-implementer-design-work/architecture-questions/AQ-NNN-*.md` rather than a synchronous dispatch; orchestrator manually drains the queue at session boundaries |
| R-4 | Persona-prose ban over-applied (sub-domain expert framings) | Pass-1 Limitation 10 flags that Wharton/Zheng/PRISM tested general expert framings; sub-domain (e.g., "expert peptide pharmacologist") may have different effects but is bounded by parent finding. Implementer may over-correct and produce Identity prose so sparse that routing precision suffers | NOTE | §13 row 13.1 ≤40-word ceiling is the floor; routing precision is verified by §13 row 13.2 (description field) which is structurally separate from Identity. Limitation 10 explicitly notes the ≤40-word ceiling holds regardless of sub-domain framing |
| R-5 | DIFFER-block Jaccard threshold (0.30) is uncalibrated (Pass-1 Limitation 9) | The 0.30 threshold is borrowed from software-code-review duplicate-detection conventions, not empirically derived for medical-specialist prose. First 4-5 specialists may show the true ceiling is 0.20 or 0.40 | NOTE | §13 row 13.9 PROPOSED status preserves recalibration option; Pass-1 R9 explicitly tags v1-calibration-pending; the architect's audit script should expose the threshold as a configurable parameter; §18 OQ-5 carries the recalibration trigger |
| R-6 | Refusal-class taxonomy file location uncertain (Pass-1 R5 + Worked Example B) | Pass-1 R5 requires the audit to read the architect's canonical-taxonomy file at runtime, but the canonical path is not yet fixed by Role 1 (it could be `vault/library/_refusal-class-taxonomy.md`, `templates/refusal-classes.yaml`, inline in Role 1 design doc §2.2 item 3). Implementer cannot encode taxonomy enum-membership check until path is fixed | WARN | §18 OQ-3 surfaces; until resolved, the §13 row 13.5 audit is PROPOSED with a path-TBD note; the audit-script's taxonomy-read step accepts a `--taxonomy-path` CLI argument that the orchestrator supplies at audit time |
| R-7 | Negative-example denylist regex not authored (Pass-1 Finding 8) | The harmful-content denylist regex pattern (specific Category X drug names with doses; specific contraindication pairs; documented jailbreak triggers) is not yet authored. Audit row 13.10 has the count check working but the denylist-pattern check is incomplete | WARN | §18 OQ-6 surfaces; Pass-1 Finding 8 specifies the denylist must be authored before the first specialist with Negative Examples deploys; the Role 4 medical-safety-reviewer (Role 4) owns the denylist content per Pass-1 R10 |

### 17.2 Assumptions

| # | Assumption | Breaks-if |
|---|---|---|
| A-1 | Role 1 (health-specialist-architect) design doc is Final before Role 2 dispatch | breaks-if: Role 2 dispatched against a Draft or Phase-3 Role 1 design doc. Role 2 references Role 1 §2.2, §4, §5 Rule 12/13, §13 by section/row; if those sections drift after Role 2 finalize, Role 2's audit checks become stale. Mitigation: Role 2's frontmatter pins `references_role_1_sha: <sha>` at dispatch start. |
| A-2 | The canonical 11-section count (10 AGENT_TEMPLATE base + Modes) is stable through Role 2's 14-specialist authoring run | breaks-if: AGENT_TEMPLATE.md gains a 12th section mid-batch; specialists 1-N have 11 sections, specialists N+1-14 have 12. EC-2 audit catches; orchestrator halts the batch. |
| A-3 | `scripts/audit-specialist-profile.sh` is owned by Role 2 (implementer) per Pass-1 F9; Role 1 §2.2 "I do NOT own" item 5 names Role 2 (or "dedicated tooling pass") as owner | breaks-if: ownership shifts to architect (would require Role 1 amendment) OR to Session B's deployment-time agent. Then §13 PROPOSED rows have a different mechanical-resistance owner. §18 OQ-1 surfaces. |
| A-4 | The 14 specialist roster (WIKI.md Agent Consumers section) is stable through Role 2's batch authoring | breaks-if: a 15th specialist (e.g., environmental-factors) gets promoted from "cross-cutting consultants" to own-agent mid-batch; IDENTICAL-block hash discipline must extend to 15. Mitigation: orchestrator coordinates roster changes outside Role 2 active batches; Role 2 reads the row count at dispatch start and pins it. |
| A-5 | `vault/meta/operator-profile.md` schema is stable during the batch | breaks-if: operator-profile gains a new field mid-batch (EC-6). Schema-drift audit (PROPOSED row 13.6.6) catches; orchestrator halts batch and queues remediation for specialists already authored. |
| A-6 | Pre-Role-4 phase: medical-safety-reviewer is v1-substituted per Role 1 §17.2 A-7; Role 2's Loop-Breaking dual-gate clause (Risk R-1 mitigation) accepts v1-substitute verdict logs in lieu of Role 4's | breaks-if: a specialist deploys with neither Role 4 nor v1-substitute verdict log present. Mitigation: orchestrator checks at deployment time; if no verdict log of either type, specialist's deployment is gated. |
| A-7 | Architecture Question channel resolves to a stored-file pattern (Pass-1 Limitation 8 option b) during the pre-architect-deployment phase | breaks-if: orchestrator selects option (a) synchronous human-reviewer or (c) sync dispatch to architect role. The implementer's process step 4 (escalate genuine gaps) is shape-neutral; the resolution latency differs but the implementer's local behavior does not. §18 OQ-4. |
| A-8 | The DIFFER-block Jaccard threshold is configurable per audit invocation (per Pass-1 R9 "the architect's audit script should expose the threshold as a configurable parameter") | breaks-if: the script hard-codes 0.30; Limitation 9 recalibration becomes a script-edit not a config change. Mitigation: §15.2 AC-1 audit-script existence + §18 OQ-5 calibration trigger together specify the contract. |

### 17.3 Break Conditions

| # | Condition | Named monitor (how a future session detects) |
|---|---|---|
| BC-1 | Any deployed specialist exceeds 200 lines OR 2500 tokens (Pass-1 R3 ceiling) | Monitor: `wc -l .claude/agents/*/agent.md \| awk '$1 > 200{print}'` returns non-empty AT ANY SESSION CLOSE; surfaces in `scripts/handoff-audit.sh` extension OR a dedicated `scripts/specialist-line-audit.sh` (PROPOSED). Pass-1 R3 hard ceiling at 200. |
| BC-2 | Any specialist Identity section contains a banned-lexicon token (`expert\|experienced\|world-class\|seasoned\|veteran\|years of`) at deployment | Monitor: AC-7 + a banned-adjective grep extension run at deployment time AND at every session close. Single hit = BC trip. Pass-1 Finding 1 + R1. |
| BC-3 | Role 3 (health-edge-case-reviewer) reports >5 coverage gaps across the deployed 14 specialists in any single review pass | Monitor: Role 3's review-output schema gains a `coverage_gaps: []` field; orchestrator's session-close hook checks `len(coverage_gaps) > 5` and trips. Indicates Role 2's template-following discipline failed structurally. Pass-1 Finding 9 + Insight 6. |
| BC-4 | A new PF entry of class AP-IMPL-* (implementer-specific anti-pattern) is logged with recurrence_count = 2 | Monitor: `scripts/pf-attestation-audit.sh` extension; on session close, parse PF log for class identifiers matching `AP-IMPL-*` and count occurrences. Recurrence ≥2 trips per Rigor Framework Discipline 8. Pass-1 Anti-Pattern catalog establishes the class. |
| BC-5 | IDENTICAL-block hash diverges across the 14 deployed specialists at any post-deployment audit run | Monitor: `scripts/audit-specialist-profile.sh --cross-file-hash-check` (PROPOSED) run at every session close once the script exists; non-zero exit code trips. Pass-1 R8. The hash discipline's whole-batch property makes this the load-bearing structural BC. |

---

## 18. Open Questions

### OQ-1 — Will `scripts/audit-specialist-profile.sh` be authored during Role 2's design-doc-protocol Phase 5, or deferred to a follow-up session?

**Why unresolvable now.** Pass-1 Finding 6 + Finding 9 + R7 + R13 all depend on the audit script. §13 has 13 PROPOSED rows citing it. Role 1 §18 OQ-1 surfaced the same question without resolution. Role 2 inherits the open status. The script's deliverable owner is Role 2 (per A-3); the design-doc protocol produces the design doc, not the script.

**Resolution path.** User adjudicates at Phase 5 finalize: either authorize Role 2 scope extension to include the script + its smoke tests in the same cycle OR confirm deferred to a follow-up bead. If deferred, the 13 PROPOSED §13 rows ship as paper claims; AC-1 (script exists) FAILs at Phase 5 close-check.

**Blocker.** Yes — blocks AC-1; collectively covers §13 PROPOSED rows 13.1 through 13.13.

### OQ-2 — Role 2's §8 (Tools) palette: state-mutating Bash git permitted, or forbidden (Role 1 §8.3 mirror)?

**Why unresolvable now.** QA drafter does not own §8; SE drafter does. PF-S2-06 verdict in §11.1 above is CONDITIONAL — resolves to OUT-OF-SCOPE — structural only if §8 mirrors Role 1's forbid. Role 2's deliverable (14 agent.md files) is a producer-of-many-files surface; if Role 2 needs to `git add` and `git commit` each profile individually, state-mutating git may be in-palette.

**Resolution path.** SE drafter at Role 2 Phase 1 + orchestrator synthesis at Phase 2. Recommendation: forbid state-mutating git (defer commits to orchestrator); cleanest structural verdict.

**Blocker.** Non-blocking for Role 2 design-doc finalize; flags PF-S2-06 verdict dependency.

### OQ-3 — Canonical refusal-class taxonomy file: location and format?

**Why unresolvable now.** Pass-1 R5 + Worked Example B specify the audit reads the architect's canonical-taxonomy file at runtime to enforce enum-membership. Role 1's design doc §2.2 item 3 enumerates the 8 classes inline but does not write them to a separate canonical file. Candidates: `vault/library/_refusal-class-taxonomy.md`, `templates/refusal-classes.yaml`, leave inline + audit reads Role 1 design doc by section anchor.

**Resolution path.** Role 1 amendment OR Role 2 architect-question to orchestrator. Recommendation: standalone `templates/refusal-class-taxonomy.yaml` (YAML for the audit's enum-parse).

**Blocker.** Blocks §13 row 13.5 LIVE transition; non-blocking for design-doc finalize.

### OQ-4 — Architecture Question channel resolution: stored-file batch, sync human reviewer, or sync dispatch to architect role?

**Why unresolvable now.** Pass-1 Limitation 8 explicitly flags. Implementer's process step 4 dispatches an Architecture Question when the architect's template did not resolve a gap. In Session B (first implementer run), Role 1 design doc is Final but architect runtime role may not yet be deployed.

**Resolution path.** Orchestrator decides one of: (a) stored-file pattern at `design/.health-implementer-design-work/architecture-questions/` drained at session boundaries; (b) sync human reviewer; (c) sync dispatch to architect role even pre-self-audit. Recommendation: option (a) for the pre-architect-deployment phase; transition to (c) once architect deploys.

**Blocker.** Non-blocking for design-doc finalize; affects R-3 mitigation latency.

### OQ-5 — DIFFER-block Jaccard threshold calibration trigger

**Why unresolvable now.** Pass-1 R9 + Limitation 9 flag the 0.30 threshold as v1-calibration-pending. No corpus exists; first 4-5 specialists provide calibration data. The recalibration trigger (when to revisit) is not specified.

**Resolution path.** Resolution at Role 2's 5th specialist deployment: run pairwise Jaccard on the first 5 deployed, report observed distribution, recalibrate threshold (probably 0.20-0.40 range). Roll the new threshold into `scripts/audit-specialist-profile.sh` config. Recalibration generates a follow-up bead.

**Blocker.** Non-blocking for first 5 deployments; blocks final Jaccard-audit LIVE status.

### OQ-6 — Negative-example denylist regex content authoring

**Why unresolvable now.** Pass-1 Finding 8 specifies the denylist's existence (specific Category X drug names with doses; specific contraindication pairs; documented jailbreak triggers) but does not author the regex content. Pass-1 R10 names Role 4 (medical-safety-reviewer) as owner; Role 4 is not yet deployed.

**Resolution path.** Pre-Role-4 phase: v1-substitute software security agent (per Role 1 §17.2 A-7) authors a starter denylist; Role 2's audit row 13.10 enforces presence-only until Role 4 deploys and replaces the starter with curated content. Role 4 design doc owns the curation discipline.

**Blocker.** Blocks denylist-content audit LIVE status; non-blocking for the count check (≥3 pairs).

### OQ-7 — §13 PROPOSED rows mirror: 13 rows vs §18 line budget

**Why unresolvable now.** Template §13/§18 budget interaction (Role 1 §18 OQ-5 surfaced the same defect). Role 2 has 13 PROPOSED rows + 4 additional PROPOSED rows surfaced in §14 ECs (13.5.5 GRADE two-axis; 13.6.5 section count; 13.6.6 schema-drift; 13.7.5 section-header uniqueness; 13.12.5 mode-floor correctness; 13.X H-class composition; 13.X upstream-bibliography-sync) = 17 PROPOSED rows. §18 budget is 10-20 lines.

**Resolution path.** Synthesis adopts Role 1's pattern: consolidate all 13 (or 17 after EC additions) PROPOSED rows into a single OQ-1 pointer back to §13. This OQ-7 is the meta-question of whether the consolidation pattern is acceptable for Role 2's higher PROPOSED count.

**Blocker.** Non-blocking; surface defect (template §13/§18 interaction at higher PROPOSED counts) is a candidate amendment for DESIGN_DOC_TEMPLATE.md Change Log.

---

## Anchor Check (per task constraint)

Every section authored cites ≥1 Pass-1 Finding / Recommendation / Pattern / Contradiction / PF / INV identifier:

- **§11.1.** 8 rows; each cites at least one of: PF-S2-01 through PF-S6-01 (8 IDs), R11, R13, R14, R8, R9, AND/OR Pass-1 F7 / F9 / Insight 7. Total anchor count ≥17.
- **§13.** 16 rows; each cites Pass-1 R1-R13 (each row maps to one) and/or INV-ROLE-INLINING / INV-BRANCH-NOT-MAIN / INV-RESEARCH-ATTESTATION (rows 13.14-13.16). Total anchor count = 16 R/INV identifiers.
- **§14.** 14 ECs; each cites at least one Pass-1 Finding, Recommendation, Insight, Limitation, or PF identifier. EC-1 (F1, R1, Limitation 10); EC-2 (PF-S2-05, Role 1 §5 line 626); EC-3 (R14, F9); EC-4 (F-S2, F7, R8, Insight 7); EC-5 (R12, Insight 8); EC-6 (F9 step 1, PF-S2-05); EC-7 (PF-S6-01, R13); EC-8 (R5, F9 Worked Example B); EC-9 (Role 1 §5 Rule 12, R2); EC-10 (Role 1 §4 OUTBOUND row 2, §5 Rule 13); EC-11 (PF-S2-05); EC-12 (R10, F8); EC-13 (R9, Limitation 9, PF-S2-04); EC-14 (PF-S2-05). Total anchor count ≥22.
- **§15.2.** 10 ACs; each names Pass-1 R or F anchor (R13, F6, F9, R4 row 4, F5/Limitation 7, R-no-TBD-template, R8, F7, F1/R1, R4/F4, R11, R12). Total anchor count = 10.
- **§17.1.** 7 risks; each names a Pass-1 anchor (R4 row 4 PF-S3-01; Insight 7; Limitation 8; Limitation 10; R9/Limitation 9; R5/Worked Example B; F8/R10). Total = 7.
- **§17.2.** 8 assumptions; each names a Role 1 or Pass-1 anchor (Role 1 §2.2/§4/§5/§13; AGENT_TEMPLATE; F9; WIKI.md; operator-profile schema; Role 1 §17.2 A-7; Limitation 8; R9). Total = 8.
- **§17.3.** 5 break conditions; each names a Pass-1 anchor (R3; F1/R1; F9/Insight 6; AP-IMPL class; R8). Total = 5.
- **§18.** 7 OQs; each anchors to specific Pass-1 / Role 1 / Limitation / Finding ID. Total = 7.

**Anchor coverage: PASS.** Every authored section cites ≥1 substantive anchor.

---

## Findings emitted against upstream artifacts during this drafter pass

1. **FINDING (SHOULD FIX) — Role 1 §13 row 14 (`design/health-specialist-architect-design.md` line 488).** Row 14 (H-class worst-case-reachable composition check) is tagged PROPOSED without distinguishing whether the gap is the check itself OR the test-for-the-check. The QA-strict rubric (used in this draft's §13) treats these as separate gaps. RECOMMENDATION: amend Role 1 §13 row 14 to indicate which gap kind it is, or add a second row distinguishing the test gap.

2. **FINDING (SHOULD FIX) — Role 1 §13 multiple rows: PROPOSED rationale conflates "check absent" with "test-for-check absent".** Rows 1-7, 11-17 are uniformly tagged PROPOSED with rationale "`scripts/audit-specialist-profile.sh` does not exist." This is correct under Role 1's tag-rule (check-existence-based) but the secondary gap (smoke tests for each sub-check) is not explicitly enumerated. When the script is authored, Role 1's PROPOSED rows would auto-promote to LIVE — but per the QA-strict rubric, they should remain PROPOSED until smoke tests for each sub-check also exist. RECOMMENDATION: Role 1 amendment OR a Role 2 SHOULD-FIX note documenting the stricter tag-rule.

3. **FINDING (MUST FIX) — Role 2 §13 above LACKS rows for at least 4 audit surfaces that §14 ECs reveal as needed.** ECs 2, 6, 9, 14 each surface a missing audit row: section count (13.6.5), schema drift (13.6.6), GRADE two-axis (13.5.5), section-header uniqueness (13.7.5). Also EC-5 surfaces mode-floor-correctness (13.12.5) and EC-10 surfaces H-class composition (13.X). RECOMMENDATION: orchestrator's Phase 2 synthesis adds these rows to the final Role 2 §13 table before Phase 3 dispatch. (These are surfaced here rather than added to §13 above because adding them creates 5 more PROPOSED rows that compound the §13/§18 budget interaction — see §18 OQ-7.)

4. **FINDING (SHOULD FIX) — `vault/WIKI.md` Agent Consumers section.** The kickoff brief references "14 specialist roles" but the WIKI table contains 14 rows (personal-trainer through medical-liaison) — count matches. However, the `medical-liaison` row's "Dispatches research on: none — collates only" creates the EC-3 surface (specialist row missing key field). RECOMMENDATION: explicit "no research dispatch" marker in WIKI.md for medical-liaison, OR Role 2's audit handles the empty case explicitly (e.g., "if research field == 'none', skip mode-floor audit").

5. **FINDING (SHOULD FIX) — Pass-1 substrate Limitation 9 + R9 calibration mechanism.** Pass-1 R9 names the 0.30 Jaccard threshold v1-calibration-pending but does not specify the recalibration trigger (after how many specialists? On what schedule? Who decides the new value?). §18 OQ-5 proposes "after 5 deployments" but this is the QA drafter's recommendation, not a Pass-1 substrate decision. RECOMMENDATION: Role 2 architect drafter adopts §18 OQ-5's recommendation OR orchestrator at Phase 2 explicitly amends.

---

## Return summary

**Status.** draft-emitted.

**File written.** `design/.health-implementer-design-work/qa-draft.md`.

**Coverage counts.**

- **PFs covered:** 8/8 (PF-S2-01 IN-SCOPE, PF-S2-02 IN-SCOPE, PF-S2-03 IN-SCOPE, PF-S2-04 IN-SCOPE, PF-S2-05 IN-SCOPE, PF-S2-06 CONDITIONAL pending §8 finalization, PF-S3-01 IN-SCOPE, PF-S6-01 IN-SCOPE). No gap PFs. PF-S2-06 flagged as CONDITIONAL in §18 OQ-2.
- **Edge cases authored:** 14 (EC-1 through EC-14).
- **Binary ACs authored:** 10 (AC-1 through AC-10).
- **Break conditions named:** 5 (BC-1 through BC-5), each with a named monitor (scripts/handoff-audit.sh extension, AC-7 banned-adjective extension, Role-3 review-schema field, scripts/pf-attestation-audit.sh extension, scripts/audit-specialist-profile.sh cross-file-hash check).

**§13 QA-side tagging.** LIVE: 0. REFERENCED: 3 (rows 13.14 INV-ROLE-INLINING, 13.15 INV-BRANCH-NOT-MAIN, 13.16 INV-RESEARCH-ATTESTATION). PROPOSED: 13 (rows 13.1 through 13.13). Reason for PROPOSED across all 13: `scripts/audit-specialist-profile.sh` does not exist (Glob confirmed) AND `scripts/tests/test_audit_specialist_profile.sh` does not exist (Glob confirmed); under the QA-strict tag rule (test-for-check must exist), every audit-script-sub-check is PROPOSED.

**Findings against upstream artifacts.** 5 emitted (2 SHOULD FIX against Role 1 §13; 1 MUST FIX surfacing missing Role 2 §13 rows; 1 SHOULD FIX against WIKI.md medical-liaison row; 1 SHOULD FIX against Pass-1 R9 calibration mechanism). All have file:line citations where applicable.

**Blockers.** None on the sections this drafter slice authored. §11.1 PF-S2-06 verdict depends on §8 (Tools) authoring by SE drafter — flagged in §18 OQ-2 but not blocking this slice's draft emission.

**Anchor check.** All 6 authored sections cite ≥1 Pass-1 Finding / Recommendation / Pattern / PF / INV identifier. Detailed per-section anchor counts in the Anchor Check block above.
