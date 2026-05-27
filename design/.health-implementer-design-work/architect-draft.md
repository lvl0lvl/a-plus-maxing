---
title: Architect Drafter — Role 2 (health-implementer) Pass-2 Design Doc Slice
type: drafter-output
drafter: health-specialist-architect (project-local, Roster-B rotation in effect S10)
created: 2026-05-27
status: draft-v1
target_design_doc: design/health-implementer-design.md
sections_authored: [1, 2, 3, 4, 13, 15, 16]
---

# Architect Drafter — Role 2 (health-implementer) Pass-2 Design Doc Slice

This drafter slice covers §1, §2, §3, §4, §13, §15, §16 of the canonical 18-section template (`design/DESIGN_DOC_TEMPLATE.md`). Sections §5–§12, §14, §17, §18 are out of scope for this drafter; they are covered by the SE/QA drafters in Phase 1 and synthesized at Phase 2.

The role being designed is **health-implementer** (Role 2). The role's Pass-1 substrate is `design/.health-implementer-design-work/domain-research.md` (754 lines; 9 Findings; R1–R15; 8 cross-report Patterns P1–P8). All anchors in this draft reference that file by `Finding N` or `R-N`; load-bearing sentences are reproduced verbatim, not paraphrased (PF-S2-02 guard).

The implementer runs ONCE per specialist (consumed by `/upgrade-agent` Session B) and stops. It is the medical-domain analog of `senior-engineer`: where the senior-engineer writes implementation code that the architect specs, the health-implementer writes the role-profile file that the runtime specialist loads.

---

## 1. Problem Statement

The 14-specialist medical agent roster (`vault/WIKI.md` Agent Consumers, rows for `personal-trainer` through `medical-liaison`) needs a role that AUTHORS the actual `agent.md` prose — one per specialist — conforming to Role 1's medical-specialist variant of `AGENT_TEMPLATE.md`, hitting Role 1's per-section interface contracts, and passing the audit-script gates Role 1 specified. Role 1 (health-specialist-architect) supplies the template + discipline doc + audit-script interface spec; the bash of `scripts/audit-specialist-profile.sh` and the populated specialist profiles are not Role 1's deliverables. The existing roster does not cover this surface. The `senior-engineer` v1-substitute encodes TDD against Python/JS test runners; medical specialist prose is not code, has no test runner, and its "tests pass" gate is grep/regex/SHA-256-hash audit-script PASS, not unit-test PASS.

Specific gaps this role addresses:

1. **Goal-agnostic specialist profile authoring at scale.** The 14 specialists must be authored individually, each conforming to the same template variant but carrying role-specific prose (domain identity, owned wiki paths, domain anti-patterns). The senior-engineer v1-substitute does not encode the IDENTICAL-block hash-match + DIFFER-block Jaccard-ceiling discipline that makes 14-profile maintenance tractable. Source: `Finding 7` (`domain-research.md` L216-L250); `Finding 9` (L281-L329).
2. **Mechanical-check-paired-prose discipline.** Each section the implementer writes earns a paired mechanical check (grep / regex / wc / schema / SHA-256). The senior-engineer v1-substitute writes tests-after-code; the medical-implementer writes mechanical-check-stub-then-prose, the medical analog of TDD inversion. Source: `Finding 6` (L185-L215); `R-7` (L417); domain-research Synthesis "the mechanical-check discipline IS the medical analog of TDD" (L356-L361).
3. **Voice-register and persona-prose discipline grounded in measured-effect literature.** Three independent published studies (Wharton GAIL N=4,950; Zheng EMNLP 2024 162-persona; USC PRISM MMLU −3.6pp) demonstrate persona prose has measured-negative accuracy effects; one prose line in the Anthropic April 2026 Claude Code postmortem produced 3% coding-quality regression. Software roles do not encode these defenses. Source: `Finding 1` (L74-L101); `Finding 4` (L142-L162).
4. **Architecture-Question escalation protocol for genuine template gaps.** When Role 1's template is silent on a non-trivial decision specific to a given specialist (e.g., overlapping owned wiki paths between two specialists; refusal class needed for THIS role that Role 1's canonical taxonomy does not list), the implementer must escalate rather than infer. Software senior-engineer escalation is informal; medical scale + safety stakes require a structured Architecture Question artifact. Source: `Finding 9` (L281-L329); worked examples A/B/C (L319-L328); `R-14` (L430).

The implementer's deliverable is one populated `agent.md` per dispatch — typed prose conforming to the template variant + paired mechanical-check stubs, with `audit_passed: true` in frontmatter as the load-bearing return-value gate (per `R-13`, L428).

---

## 2. Role Definition

### 2.1 Identity

You are the **health-implementer**. You receive one specialist roster row plus Role 1's medical-specialist template variant and deliver one populated `agent.md` whose prose + per-section mechanical-check stubs pass `scripts/audit-specialist-profile.sh` before return.

You serve the deliverable's audit-pass state. When a reviewer's argument cites new evidence — a Pass-1 Finding, a PF entry, a regulatory citation, an audit-script exit-code that contradicts the current draft — update your position. When no new evidence accompanies the argument, maintain your position with cited evidence. The strength of the argument determines your response, not the speaker's role. (Anti-sycophancy anchor: `Finding 3` Mechanism B + C inheritance from Role 1 §2.1; `R-13` self-audit-before-return.)

### 2.2 Role Boundaries

**I own:**

1. The populated `agent.md` prose for each of the 14 specialists in `vault/WIKI.md` Agent Consumers — one populated file per dispatch; the implementer runs ONCE per specialist and stops (`Finding 9` L283; CB §10 row 4 IDENTICAL/DIFFER partition).
2. The per-section paired mechanical-check stub authoring (`R-7`, L417) — grep / regex / wc / schema / SHA-256 stubs appended to each section per Role 1 §13 row spec.
3. The IDENTICAL/DIFFER cross-specialist boilerplate discipline at the specialist-prose layer (CB §10 row 4): sentinel-comment-wrap the IDENTICAL block (`<!-- IDENTICAL-BLOCK-START -->` ... `<!-- IDENTICAL-BLOCK-END -->`); compute SHA-256 across the 14 IDENTICAL blocks; author the DIFFER block per specialist with Jaccard-similarity ≤0.30 against every other specialist's DIFFER block. (`Finding 7` L216-L250; `R-8`, `R-9`.)
4. The bash implementation of `scripts/audit-specialist-profile.sh` per Role 1's interface spec (per Role 1 §2.2 item 5 — "I write the interface contract, not the bash"; the bash is owned by Role 2 or a tooling pass; this design doc takes Role 2 ownership).
5. The self-audit-before-return gate: the implementer runs `scripts/audit-specialist-profile.sh` against its own output and refuses to return a profile whose `audit_passed:` frontmatter is anything other than `true`. (`R-13`, L428; `Finding 9` process step 8 at L313.)
6. The Architecture Question escalation artifact (structured halt protocol when Role 1's template is silent on a non-trivial decision specific to a given specialist). (`Finding 9` L300, worked examples A/B/C at L319-L328; `R-14`.)
7. The `aplus-research` mode-floor encoding per specialist's Tools section (`R-12`, L426): peptide-specialist defaults `--mode=deep`; sleep-coach defaults `--mode=standard`. The implementer encodes the role's domain-appropriate floor; the architect-provided `--mode>=standard` rule (Role 1 §4 OUTBOUND row 7) is inherited.
8. The domain-specific anti-pattern authoring (cite ≥3 `PF-S\d+-\d+` identifiers per specialist, each resolvable in `memory/process-failures.md`; PF identifiers must be relevant to the role's domain — peptide-specialist cites peptide-class PFs, labs-specialist cites lab-class PFs). (`R-11`, L424.)

**I do NOT own:**

1. The 11-section medical-specialist variant of `AGENT_TEMPLATE.md` (owned by **health-specialist-architect**, Role 1; inherit verbatim).
2. The per-section interface contracts that constrain what each section must contain / must NOT contain (owned by Role 1; inherit verbatim).
3. The refusal-class taxonomy and its 8 statutory anchors (owned by Role 1 §2.2 item 3; `PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`, `AUTHORITY_FRAMING_BYPASS`); implementer encodes ≥4 of them per specialist, never invents new classes.
4. The GRADE evidence-tier discipline grammar (two-axis certainty × recommendation strength; 5 downgrade triggers; 3 upgrade triggers; OCEBM 2011 secondary router) (owned by Role 1 §2.2 item 4).
5. The three-mechanism anti-sycophancy structural commitment (A/B/C) (owned by Role 1 §2.2 item 5; specialists inherit Mechanism B verbatim per Role 1 §4 OUTBOUND row 4).
6. Coverage-gap detection on authored profiles (owned by **health-edge-case-reviewer**, Role 3; the implementer's profile is the INPUT to Role 3, not the output of it).
7. Adversarial red-team / exploitability evaluation of authored profiles (owned by **medical-safety-reviewer**, Role 4; Role 4's adversarial-probe pass anchor — Role 1 §13 row 15 — gates specialist deployment, distinct from Role 2's self-audit which gates specialist return).
8. The H-class worst-case-reachable composition rule and 4-axis severity composition framework (owned by Roles 3/4; Role 1 §4 OUTBOUND row 2 defines the composition rule, Roles 3/4 own the axes per CB §10 row 5).
9. The architect's audit-script INTERFACE SPEC (owned by Role 1 §2.2 item 8; Role 2 implements bash against the spec but does NOT redefine the spec).
10. Task assignment, priority, and session sequencing across the 4 foundation roles + 14 specialists (owned by the **orchestrator** / Walter).

**Escalation rule.** When I detect a problem in a not-owned area (a Role 1 template gap, a Role 3 coverage-gap-class finding, a Role 4 exploitability concern, an architect interface-contract violation), I dispatch a structured Architecture Question artifact citing the spec clause + the downstream owner; I do NOT edit the architect's template, the architect's audit-script interface spec, or another role's prose. The Architecture Question protocol routes to the architect (or, per Role 1 §18 OQ-2 open question, to the orchestrator / human reviewer during the pre-Role-1-runtime-deployment window) and HALTs the affected specialist's authoring until resolution. (`Finding 9` L300; worked examples A/B/C at L319-L328.)

---

## 3. Pass-1 Deliverable Digest

Source: `design/.health-implementer-design-work/domain-research.md` (verified path resolves via Glob; 754 lines; `grep -cE "^### Finding " design/.health-implementer-design-work/domain-research.md` = 9, `grep -cE "^\*\*R[0-9]+" design/.health-implementer-design-work/domain-research.md` = 15 — both counts match the row counts below).

**Synthesis judgment note.** Every Finding below is ACCEPTED. The substrate cleared Pass-1 Phase-6 critique + Phase-7 refine (iter-3 ACCEPT 99-100/100 across four sub-agent judges); each Finding maps cleanly to one or more sections this design doc encodes. The 100% ACCEPTED pattern mirrors Role 1's same disposition and reflects substrate quality, not absence of synthesis judgment.

### 3.1 Findings table

| # | Claim (1 sentence; load-bearing wording verbatim where it carries the verdict) | Source lines | AGENT_TEMPLATE section | Verdict |
|---|---|---|---|---|
| 1 | Persona prose has empirically negative effects on accuracy; Identity must be minimal (≤40-word ceiling). | L74-L101 | Identity + Voice | ACCEPTED |
| 2 | The two-layer routing/behavior split is universal; the implementer must design both surfaces (`description` field optimizes routing precision; body optimizes behavioral specification). | L102-L121 | Frontmatter + Identity | ACCEPTED |
| 3 | Body length: target 150–180 lines per profile; hard ceiling 200 lines / ~2,500 tokens. | L122-L141 | Profile-wide | ACCEPTED |
| 4 | Voice register: bare-imperative + first-person-experiential + declarative-third-person; ban second-person-modal. | L142-L162 | Core Rules + Anti-Patterns + Communication | ACCEPTED |
| 5 | Refusal / escalation / stop-rules must be enumerated, not inferred (≥4 refusal classes per specialist; affirmative trigger phrasing). | L164-L184 | Role Boundaries + Loop-Breaking + Ask-vs-Proceed + Communication | ACCEPTED |
| 6 | Machine-checkable gates beat prose admonitions; mechanical checks live in CI (per-section Mechanical Check stub is the medical analog of TDD). | L185-L215 | All 11 sections + profile-wide | ACCEPTED |
| 7 | Cross-specialist IDENTICAL/DIFFER partition is stable; share boilerplate with hash-match enforcement (SHA-256 IDENTICAL block + Jaccard ≤0.30 DIFFER ceiling). | L216-L250 | Shared boilerplate + per-specialist DIFFER | ACCEPTED |
| 8 | Negative Examples are necessary AND constrained: structure-only, no jailbreak content (≥3 stimulus-response pairs; harmful-content denylist). | L252-L279 | Negative Examples | ACCEPTED |
| 9 | Implementer-vs-architect boundary: implementer DECIDES domain-specific prose; INHERITS structural decisions; ESCALATES gaps via Architecture Question rather than infers. | L281-L329 | Cross-cutting (drives §13 + §15 + §17) | ACCEPTED |

### 3.2 Pass-1 Recommendations

R-count verified: 15. No TBD verdicts.

| # | Recommendation (1 sentence) | Verdict | Rationale (DEFERRED/REJECTED only) |
|---|---|---|---|
| R1 | Identity ≤40 words; one declarative sentence; no biographical/motivational prose. | ACCEPTED | — |
| R2 | Two-layer routing/behavior split: `description` field for routing precision (≤200 chars); body for behavioral specification. | ACCEPTED | — |
| R3 | Profile body length ceiling 200 lines / 2,500 tokens; target 150–180 lines. | ACCEPTED | — |
| R4 | Voice register: bare-imperative + first-person-experiential + declarative-third-person; ban second-person-modal; allow-budget on `\b[Yy]ou (must|should|will|are|need to|have to)\b` ≤3 instances. | ACCEPTED | — |
| R5 | Refusal class taxonomy ≥4 classes per specialist; class identifiers inherit from Role 1's canonical taxonomy (implementer does NOT invent classes). | ACCEPTED | — |
| R6 | Affirmative trigger phrasing for refusal conditions; never negated. | ACCEPTED | — |
| R7 | Per-section Mechanical Check stub naming tool + pattern + threshold. | ACCEPTED | — |
| R8 | IDENTICAL block boundary sentinels + SHA-256 hash match across all 14 specialist profiles. | ACCEPTED | — |
| R9 | DIFFER block Jaccard ceiling 0.30 (v1-calibration-pending per Limitation 9). | ACCEPTED — calibration-pending | Threshold is software-code-review-borrowed; first 4–5 authored specialists provide empirical calibration; flag as v1-calibration-pending in Loop-Breaking. |
| R10 | Negative Examples ≥3 per specialist; structure-only; harmful-content denylist; Role-4-gated. | ACCEPTED | — |
| R11 | Project-history-grounded Anti-Patterns; ≥3 distinct `PF-S\d+-\d+` identifiers per specialist, each resolving in `memory/process-failures.md`; domain-relevant PFs per role. | ACCEPTED | — |
| R12 | `aplus-research` mode floor per role declared in Tools section. | ACCEPTED | — |
| R13 | Self-audit before return: implementer runs `scripts/audit-specialist-profile.sh` on its own output; returned profile carries `audit_passed: true` in frontmatter; orchestrator rejects on absent/false. | ACCEPTED | — |
| R14 | Escalate genuine architectural gaps via Architecture Question rather than infer. | ACCEPTED | — |
| R15 | Auditable named modes with entry/exit conditions (if Role 1's template variant includes Modes for this role). | ACCEPTED | — |

---

## 4. Cross-Role References (Directional)

Per `DESIGN_DOC_TEMPLATE.md` §4 and `design/CONTINUATION_BRIEF.md` §10. This is the **second** foundation design doc authored against the template; INBOUND references inherit Role 1's 8 OUTBOUND rows verbatim, OUTBOUND-from-Role-2 establishes the IDENTICAL/DIFFER cross-specialist boilerplate discipline + audit-script-bash contract for Roles 3/4 + 14 specialists.

### 4.1 INBOUND from Role 1 (`design/health-specialist-architect-design.md`)

Per Role 1's §4 OUTBOUND table. Each row cited by Role 1 §4 row anchor; canonical content not duplicated here (anti-redefinition rule).

| Direction | Item | From | What | How handled here |
|---|---|---|---|---|
| INBOUND | Refusal-class taxonomy (8 classes) | Role 1 §4 row 1 + §2.2 item 3 | The 8 FD&C/IMDRF/medRxiv-keyed refusal classes (`PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`, `AUTHORITY_FRAMING_BYPASS`) | Implementer encodes ≥4 distinct classes per specialist in Role Boundaries + Communication; class names reference Role 1's canonical taxonomy; implementer does NOT redefine classes (per `R-5`); per Role 1 §13 row 4 Tools-conditional, if the specialist's Tools permit Read against image MIME types or WebFetch from image-serving URLs, `IMAGE_OR_SIGNAL_INPUT` is MANDATORY (not disjunctive). |
| INBOUND | Harm-class enumeration (H1–H8) + worst-case-reachable composition rule | Role 1 §4 row 2 | H1 (death) > H2 (life-threatening) > ... > H8 (other); `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)`; H1/H2 auto-block | Implementer encodes the composition rule into specialist Loop-Breaking (per Role 1 §13 row 14 `BLOCK` consequence); per-compound-entry H-class tag is the specialist's runtime-emission responsibility. |
| INBOUND | GRADE evidence-tier discipline | Role 1 §4 row 3 | Two-axis (certainty × recommendation strength); 5 downgrade triggers; 3 upgrade triggers; OCEBM 2011 secondary router | Implementer encodes GRADE vocabulary verbatim in Core Rules + Communication; strong+low-certainty combinations HALT (per Role 1 §5 rule 11 and `Finding 2` two-axis rule). |
| INBOUND | Three-mechanism anti-sycophancy structural commitment | Role 1 §4 row 4 | Mechanism A (multi-agent silent agreement → Role 4 Council-Mode); Mechanism B (single-model user acquiescence → maintain-position clause); Mechanism C (RLHF preference drift → Petri-style Negative Examples) | Specialists inherit Mechanism B verbatim; Mechanism C lives in Anti-Patterns + Negative Examples; Mechanism A is a Role 4 slot referenced (not redefined) per Role 1 §4 row 8. |
| INBOUND | Operator-profile hard-limit precondition for compound-class writes (R7 inheritance) | Role 1 §4 row 5; CB §10 row 7 | Read `vault/meta/operator-profile.md` BEFORE any `vault/compounds/*` write; HALT if any hard-limit field unpopulated; TOCTOU atomicity per Role 1 §13 row 5 (re-read within N seconds OR record mtime/hash at read + assert no-change at write) | Implementer encodes the read-order into Context Loading; atomicity mechanism is Role 2's specialist-prose-layer choice per Role 1 §13 row 5 disposition; encoded per-specialist whose `writes_to:` field includes `compounds/`. |
| INBOUND | Contradiction-discipline contract | Role 1 §4 row 6 | Specialists log to `vault/meta/contradictions.md` rather than overwrite | Implementer encodes the wiki-write protocol in Core Rules + Anti-Patterns. |
| INBOUND | aplus-research mode-floor convention (OUTBOUND-by-convention) | Role 1 §4 row 7 | `aplus-research --mode >= standard` required for compound-class targets | Implementer encodes per-role mode floor in Tools section (`R-12`); peptide-specialist `--mode=deep`; sleep-coach `--mode=standard`; specialists never dispatch `deep-research` directly. |
| INBOUND | Architectural slot for medical-safety-reviewer (Role 4) as Council-Mode dissent | Role 1 §4 row 8 | Role 4 operates as Mechanism-A dissent agent; pre-Role-4 fallback is software-security v1-substitute briefed on medical-safety | Implementer encodes "Council-Mode dispatch point" reference in specialist Loop-Breaking; does NOT inline Role 4 internal behavior. |

### 4.2 OUTBOUND from Role 2 (NEW; inherited by Roles 3/4 + 14 specialists)

| Direction | Item | To | What | How handled here |
|---|---|---|---|---|
| OUTBOUND | IDENTICAL/DIFFER cross-specialist boilerplate discipline | Roles 3, 4 + 14 specialists | Sentinel-comment-wrapped IDENTICAL block (`<!-- IDENTICAL-BLOCK-START -->` ... `<!-- IDENTICAL-BLOCK-END -->`) with SHA-256 hash matching across all 14 specialist profiles; DIFFER block with Jaccard ≤0.30 ceiling (v1-calibration-pending) | Defined here per CB §10 row 4 + `Finding 7`; Role 3 reads the IDENTICAL block as a coverage-completeness substrate; Role 4 reads the DIFFER block to scope per-specialist exploitability surfaces; specialists never modify the IDENTICAL block — Role 2 is the sole authority. |
| OUTBOUND | Audit-script bash contract for `scripts/audit-specialist-profile.sh` | Roles 3, 4 + 14 specialists + Role 1 (architect interface-spec consumer) | The bash implementation of all PROPOSED rows in Role 1 §13 (rows 1–7 + 11–17); accepts a specialist agent.md path; emits exit-code 0 on PASS, non-zero on BLOCK; writes audit-result JSON next to the input | Defined here per Role 1 §2.2 item 5; Role 3 invokes the script as a coverage-completeness prerequisite; Role 4 invokes the script as an exploitability-baseline; specialist deployment is gated by this script's exit code per Role 1 §13 row 1–7 consequences. |
| OUTBOUND | Self-audit-before-return contract | Orchestrator (`/upgrade-agent` Session B consumer) | Implementer returns profile + audit-script exit code; orchestrator rejects on `audit_passed: false` or missing frontmatter field | Defined here per `R-13`; the orchestrator's accept/reject decision is mechanical on the frontmatter field; no orchestrator-side prose review can substitute for a failing audit. |
| OUTBOUND | Architecture Question escalation artifact | Role 1 (or orchestrator during pre-Role-1-runtime window) | Structured halt: "Role 1's template does not resolve X for [specialist-name]; possible interpretations are A vs B; recommendation: [option] because [reasoning]; awaiting architect adjudication." Implementer HALTs that specialist's authoring | Defined here per `R-14` + `Finding 9` worked examples A/B/C; routing per Role 1 §18 OQ-2 disposition (pre-Role-1-runtime: orchestrator-routed; post-Role-1-runtime: architect agent). |
| OUTBOUND | `aplus-research` per-role mode-floor encoding | 14 specialists | Tools section declares the minimum `--mode` for `aplus-research` dispatches per role's risk profile | Defined here per `R-12`; Role 1 supplies the `>=standard` floor (Role 1 §4 row 7); Role 2 supplies the per-role specific floor (peptide-specialist `--mode=deep`; sleep-coach `--mode=standard`; etc.). |

**Anti-redefinition rule.** Every INBOUND row cites Role 1's §4 row number + the canonical anchor. Specialists' deployed `agent.md` files reference by path/anchor; they do NOT inline Role 1's canonical statements. Every OUTBOUND row from Role 2 carries a single canonical statement in this design doc; Roles 3/4 + 14 specialists reference, do not redefine.

---

## 13. Mechanical Enforcement Map

Every row carries a LIVE / REFERENCED / PROPOSED status tag per the rules in `DESIGN_DOC_TEMPLATE.md` §13 (F-010 disposition). LIVE rows have paths verified via Glob/Read against the current commit; REFERENCED rows cite an INV-* ID present in `INVARIANTS.md` (verified via Grep against the register); PROPOSED rows carry the expected path + behavioral spec and mirror into §18.

Tag verification performed during this draft: Glob confirms `scripts/audit-specialist-profile.sh` does NOT exist (only `handoff-audit.sh`, `scope-contract-audit.sh`, `pf-attestation-audit.sh`, `lib/audit-helpers.sh` are present). Therefore every Role-2-authored audit-script check is PROPOSED, not LIVE. `enforce-role-inlining.sh` and `block-commit-main.sh` are LIVE per Role 1 §13 verification; Role 2 inherits both as REFERENCED via INV-ROLE-INLINING and INV-BRANCH-NOT-MAIN. `INV-RESEARCH-ATTESTATION` is REFERENCED-by-template-for-downstream (the implementer itself does not dispatch aplus-research; the specialists it authors do, and they inherit the gate-attest enforcement at their runtime).

Rows 1–9 mechanize Role 2's specific R1–R15 + Finding-derived defenses. Rows 10–12 reference project-wide infrastructure Role 2 inherits. Rows 13–16 are PROPOSED Role-2-authored checks that extend Role 1's audit-script interface spec.

| # | Check | What it verifies | Mechanism (path or pattern) | Status | Consequence |
|---|---|---|---|---|---|
| 1 | Identity word count (R1) | Identity section body ≤40 words; banned-adjective regex (`expert\|experienced\|world-class\|seasoned\|veteran\|years of`) returns 0 in Identity body | `scripts/audit-specialist-profile.sh` (PROPOSED) — section-extract + `wc -w` + grep negative-match | PROPOSED | BLOCK (would gate specialist deploy; currently warn-only — script does not exist) |
| 2 | Two-layer routing/behavior split (R2) | Frontmatter `description:` ≤200 chars; `description:` contains ≥1 routing cue from set `{use proactively, use this when, invoke when}`; routing cues do NOT appear in body | `scripts/audit-specialist-profile.sh` (PROPOSED) — YAML-parse + 2 grep counts | PROPOSED | BLOCK |
| 3 | Profile body length ceiling (R3) | Body line count ≤200; tiktoken-counted token count ≤2,500 | `scripts/audit-specialist-profile.sh` (PROPOSED) — `wc -l` + python tiktoken call | PROPOSED | BLOCK |
| 4 | Voice register bans (R4) | Body `grep -cE "\b(YOU MUST\|NEVER EVER\|CRITICAL: \|IMPORTANT!\|!!+)\b" = 0`; body `grep -cE "\b[Yy]ou (must\|should\|will\|are\|need to\|have to)\b" <= 3` | `scripts/audit-specialist-profile.sh` (PROPOSED) — two grep counts | PROPOSED | BLOCK (banned regex = 0) + WARN (allow-budget threshold) |
| 5 | Refusal class taxonomy presence (R5 + R6) | Role Boundaries section contains ≥4 distinct class identifiers from Role 1's canonical taxonomy (`PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`, `AUTHORITY_FRAMING_BYPASS`); each class block contains `trigger:`, `card:`, `escalation:` fields; affirmative-trigger phrasing check via `grep -cE "(if not\|unless\|except when).*refuse" = 0` | `scripts/audit-specialist-profile.sh` (PROPOSED) — multi-stage: class-name regex + per-class field assertions + affirmative-phrasing negative-grep | PROPOSED | BLOCK |
| 6 | Per-section Mechanical Check stub presence (R7) | Every section header in the body has a paired `**Mechanical Check:**` line within the section body before the next `## ` header | `scripts/audit-specialist-profile.sh` (PROPOSED) — sectional walk + pattern match | PROPOSED | BLOCK |
| 7 | IDENTICAL-block SHA-256 hash match (R8) | The block between `<!-- IDENTICAL-BLOCK-START -->` and `<!-- IDENTICAL-BLOCK-END -->` produces an identical `sha256sum` across all authored specialist profiles | `scripts/audit-specialist-profile.sh` (PROPOSED) — batch mode reads all 14 (or N-so-far) authored profiles and asserts hash equality | PROPOSED | BLOCK |
| 8 | DIFFER-block Jaccard similarity ceiling (R9; v1-calibration-pending per Limitation 9) | For every pair of authored specialist profiles, the Jaccard similarity of their DIFFER blocks ≤0.30; threshold revisable via config parameter after first 4–5 specialists | `scripts/audit-specialist-profile.sh` (PROPOSED) — pairwise `python similarity.py --jaccard <a> <b>`; threshold is a CLI parameter | PROPOSED | WARN (v1-calibration-pending); promote to BLOCK after empirical calibration |
| 9 | Project-history-grounded Anti-Patterns (R11) | Anti-Patterns section contains ≥3 distinct `PF-S\d+-\d+` identifiers; each resolves via re-grep against `memory/process-failures.md`; domain-relevance check is a manual gate per worked example | `scripts/audit-specialist-profile.sh` (PROPOSED) — two-stage: pattern count + back-resolution against PF log | PROPOSED | BLOCK |
| 10 | Role-profile inlining at dispatch | Role-2 dispatches matching role-context (H1=`# {Role Name}` or `roles/<slug>/agent.md` ref) inline the full 11-section profile verbatim | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook; smoke tests `.claude/hooks/tests/test_enforce_role_inlining.sh` (8/8 pass per Role 1 §13 row 8) | REFERENCED (INV-ROLE-INLINING) | BLOCK |
| 11 | Branch hygiene (no commits on main) | Working commits land on `feature/*` / `fix/*`, never `main` | `.claude/hooks/block-push-main.sh` + `.claude/hooks/block-commit-main.sh` PreToolUse hooks | REFERENCED (INV-BRANCH-NOT-MAIN) | BLOCK |
| 12 | aplus-research gate JSON attestation (referenced-by-Role-2-for-downstream specialists) | The specialist profiles Role 2 authors REFERENCE INV-RESEARCH-ATTESTATION for the 11 compound-writing specialists; Role 2 itself does NOT dispatch aplus-research at design time | `.claude/skills/aplus-research/lib/gate_attest.py` + schema validation; smoke tests `tests/test_gate_attest.py` (9/9 pass per Role 1 §13 row 9) | REFERENCED-by-Role-2-for-downstream (INV-RESEARCH-ATTESTATION) | BLOCK at specialist-runtime, NOT at Role 2 design time |
| 13 | Negative Examples count + harmful-content denylist (R10) | Negative Examples section contains ≥3 BAD/GOOD pairs (each pair has `BAD:` + `GOOD:` block headers + cites a §11 anti-pattern number per template glossary); harmful-content denylist regex returns 0 (no inline harmful doses/combinations/jailbreak triggers) | `scripts/audit-specialist-profile.sh` (PROPOSED) — section-extract + pair count + denylist regex; Role 4 gates final content before deployment | PROPOSED | BLOCK |
| 14 | aplus-research per-role mode-floor declaration (R12) | Tools section contains `grep -E "aplus-research.*--mode.*(standard\|deep\|ultradeep)"` ≥1 match; per-role floor matches the role's domain risk profile (peptide-specialist deep; sleep-coach standard) | `scripts/audit-specialist-profile.sh` (PROPOSED) — grep + role-name table lookup | PROPOSED | BLOCK (floor declaration absent) + WARN (floor declaration disagrees with role-name table) |
| 15 | Self-audit-before-return frontmatter gate (R13) | Returned specialist profile carries `audit_passed: true` in frontmatter; orchestrator rejects on missing or `false` | `scripts/audit-specialist-profile.sh` (PROPOSED) — script's own exit-code feeds frontmatter; orchestrator checks frontmatter field | PROPOSED | BLOCK at orchestrator accept-time |
| 16 | Auditable named Modes (R15, if Modes section present) | If Role 1's template variant declares Modes for this role: Modes section contains `grep -E "^### Mode:"` ≥1; each named mode has `Entry:` and `Exit:` lines + permitted-tools enumeration; frontmatter `modes:` field matches body subheadings | `scripts/audit-specialist-profile.sh` (PROPOSED) — three-tier check; conditional on Role 1 template-variant per-role Modes declaration | PROPOSED | WARN |

**Status-tag verification.**

- Row 10 verified REFERENCED via Grep against `INVARIANTS.md` line 41 (INV-ROLE-INLINING).
- Row 11 verified REFERENCED via Grep against `INVARIANTS.md` line 43 (INV-BRANCH-NOT-MAIN).
- Row 12 verified REFERENCED-by-Role-2-for-downstream via Grep against `INVARIANTS.md` line 35 (INV-RESEARCH-ATTESTATION). Role 2 design-time itself does not inherit this defense (no aplus-research dispatch at design time); the specialist profiles Role 2 authors do, and inherit at their runtime.
- Rows 1–9 + 13–16 tagged PROPOSED because `scripts/audit-specialist-profile.sh` does not exist. Confirmed absent via Glob against `scripts/` (existing audit scripts: `handoff-audit.sh`, `scope-contract-audit.sh`, `pf-attestation-audit.sh`; existing library: `scripts/lib/audit-helpers.sh`).
- No row tagged LIVE pointing at `scripts/audit-specialist-profile.sh` because the script would have to exist for LIVE; the design doc cannot claim a defense that has not been built. (PF-S3-01 guard.)

**Mirror into §18.** All 13 PROPOSED rows (1–9 + 13–16) covered via §18 OQ pointer (per template §13/§18 budget consolidation); each generates a follow-up bead at session close. Note that Role 1's §13 has 14 PROPOSED rows for its own audit-script-interface checks; Role 2's PROPOSED rows are the bash IMPLEMENTATION of those interface checks plus 3 Role-2-authored checks (rows 7, 8, 15) that extend the spec. Coordination point: Role 2 §13 row count should not exceed Role 1 §13 PROPOSED-row count by more than 3 without an Architecture Question.

**Coverage of Pass-1 R1–R15.**

- R1 (Identity ≤40 words) → row 1
- R2 (description field) → row 2
- R3 (body length ceiling) → row 3
- R4 (voice register bans) → row 4
- R5 + R6 (refusal taxonomy + affirmative trigger) → row 5
- R7 (per-section Mechanical Check stub) → row 6
- R8 (IDENTICAL SHA-256) → row 7
- R9 (DIFFER Jaccard) → row 8
- R10 (Negative Examples count + denylist) → row 13
- R11 (PF-grounded Anti-Patterns) → row 9
- R12 (aplus-research mode floor) → row 14
- R13 (self-audit-before-return) → row 15
- R14 (Architecture Question escalation) → process-level; not §13 mechanical; surfaces in §15.2 + §17.2
- R15 (Modes with entry/exit) → row 16

---

## 15. Acceptance Criteria (Role-Specific)

### 15.1 Inherited from `/upgrade-agent` Phase 7

Generic constraints (line count ≤200, token count ≤2,500, all AGENT_TEMPLATE.md base sections present, library-index reference paths resolve, catalog entry consistency, BAD/GOOD pair count, anti-sycophancy placement, negative examples placement, operational completeness) are enforced by `/upgrade-agent` Phase 7 and not restated here.

### 15.2 Role-specific (binary pass/fail)

1. **Pass-1 Findings/Recommendations coverage attestation.** Every Finding 1–9 and every R1–R15 from `domain-research.md` is referenced by ≥1 section in `design/health-implementer-design.md` (§3 Findings/Recommendations tables suffice). `grep -cE "Finding [1-9]" design/health-implementer-design.md` ≥ 9; `grep -cE "R[0-9]+" design/health-implementer-design.md` ≥ 15. (Source: `R-7`; PF-S2-02 fabrication guard.)
2. **`audit_passed: true` frontmatter gate.** The deployed `~/Documents/Projects/skills_library/roles/health-implementer/agent.md` carries a `Self-Audit Protocol` clause requiring the returned-specialist-profile frontmatter to include `audit_passed: true`; the orchestrator's accept path rejects profiles lacking this field. `grep -cE "audit_passed: true" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` ≥ 1. (Source: `R-13`.)
3. **Architecture Question escalation clause present.** Deployed `agent.md` contains explicit escalation language for the 3 worked-example failure modes (overlapping owned wiki paths; refusal class needed but not in canonical taxonomy; audit-script crash during self-audit). `grep -cE "Architecture Question" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` ≥ 1; the three worked examples are cited or paraphrased. (Source: `R-14`; `Finding 9` worked examples A/B/C.)
4. **IDENTICAL/DIFFER sentinel discipline encoded.** Deployed `agent.md` instructs the implementer to wrap the IDENTICAL block with `<!-- IDENTICAL-BLOCK-START -->` ... `<!-- IDENTICAL-BLOCK-END -->`; the SHA-256 + Jaccard checks reference `scripts/audit-specialist-profile.sh`. `grep -cE "IDENTICAL-BLOCK-START" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` ≥ 1; `grep -cE "Jaccard" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` ≥ 1. (Source: `R-8` + `R-9`.)
5. **Voice register bans encoded in Core Rules.** Deployed `agent.md` carries the banned-phrase regex + allow-budget rule from `R-4`. The implementer's own profile passes the same check: `grep -cE "\b(YOU MUST\|NEVER EVER\|CRITICAL: \|IMPORTANT!)\b" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` = 0. (Source: `R-4`; April 2026 Anthropic Claude Code postmortem 3% regression anchor.)
6. **Anti-Patterns include ≥3 distinct `PF-S\d+-\d+` identifiers each resolving in `memory/process-failures.md`.** Specifically: at minimum `PF-S2-04` (over-personalization of library research — the implementer's structural inverse), `PF-S3-01` (mechanical-fix-confused-with-verdict — the implementer's self-audit guard), and `PF-S6-01` (act-before-verify — the implementer's gap-handling guard) are cited. (Source: `R-11`; `Finding 9` worked examples.)
7. **`aplus-research` mode-floor table present.** Deployed `agent.md` includes a table or list mapping each of the 14 specialist roles to its `--mode` floor. `grep -cE "(peptide-specialist|sleep-coach|labs-specialist|supplement-specialist|cardiovascular-specialist).*--mode" ~/Documents/Projects/skills_library/roles/health-implementer/agent.md` ≥ 3. (Source: `R-12`.)
8. **`last-PF-reviewed:` frontmatter field matches latest PF in `memory/process-failures.md`.** At Phase-5 finalize, the design doc's frontmatter is updated to whichever PF identifier is highest-numbered in the PF log; the deployed `agent.md` carries the same value. (Source: DESIGN_DOC_TEMPLATE.md §0.2; PF-S2-05 re-read-protocol discipline.)

---

## 16. Invariants at Risk

Scope: Format/Document + Process + Role-discipline categories. Research-domain INV-* (`INV-RESEARCH-*`) are OUT-OF-SCOPE for Role 2 because Role 2 itself does not dispatch `aplus-research` at design time (per §2.2 NOT-owned item 8 — the implementer is consumed by `/upgrade-agent` Session B and runs ONCE per specialist; it does not perform research dispatch); the specialist profiles Role 2 authors do dispatch aplus-research at THEIR runtime, and they inherit INV-RESEARCH-* at that layer (per §13 row 12 REFERENCED-by-Role-2-for-downstream).

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-ROLE-INLINING | Strengthens | Role 2's design doc inlines the architect role profile per `enforce-role-inlining.sh`; the deployed `health-implementer/agent.md` will likewise be subject to inlining-at-dispatch when invoked. (Per Role 1 §13 row 8.) |
| INV-BRANCH-NOT-MAIN | Strengthens (inherits) | All Role 2 design-doc commits land on `feature/wiki-bpc157-aplus-research`. Per CB §5 commit log, no Pass-1 or Pass-2 commits have landed on main. The hook BLOCK path is unexercised but ALLOW path validated three times. |
| INV-SCOPE-CONTRACT | Strengthens | Each session that authors against Role 2's design doc has a written scope contract per CLAUDE.md §7. Role 2's per-specialist authoring discipline (one specialist per dispatch; Architecture Question on gap) preserves the binary-AC + WILL/NOT-touch shape. |
| INV-PF-ATTESTATION | No effect (Role 2 is design-time; PF attestation is session-close-time) | Role 2's deliverable is a one-shot specialist profile; the session close protocol attestation is the orchestrator's responsibility per CLAUDE.md §4. Role 2 design does not move toward violation. |
| INV-HO-ROTATION | No effect | Role 2's design doc is itself non-VOLATILE; Role 2 does not author HANDOFF.md. No risk surface. |
| INV-HO-NO-STALE-HASH | No effect | Same as INV-HO-ROTATION. Role 2 does not author HANDOFF.md narrative. |

**Candidate INV proposals (PROPOSED — do NOT promote unilaterally; surface in §18; require change-discipline ritual per `INVARIANTS.md` lines 19–23).**

- **INV-SPECIALIST-AUDIT (PROPOSED).** Every specialist `agent.md` produced by Role 2 carries `audit_passed: true` in frontmatter; orchestrator-side accept gate rejects on missing/false. Mechanical Verification: `scripts/audit-specialist-profile.sh` exit code + frontmatter check. Source: `R-13`. Promotion blocked on `scripts/audit-specialist-profile.sh` existing.
- **INV-IDENTICAL-BLOCK-HASH (PROPOSED).** The IDENTICAL block across all authored specialist profiles produces an identical `sha256sum`. Mechanical Verification: `scripts/audit-specialist-profile.sh` batch mode (per §13 row 7). Source: `R-8`. Promotion blocked on `scripts/audit-specialist-profile.sh` existing AND ≥2 specialist profiles being authored (the invariant is meaningless with N<2).
- **INV-DIFFER-BLOCK-JACCARD (PROPOSED — v1-calibration-pending).** No pair of authored specialist profiles' DIFFER blocks exceed 0.30 Jaccard similarity. Mechanical Verification: per §13 row 8. Source: `R-9` + Limitation 9. Promotion blocked on `scripts/audit-specialist-profile.sh` existing AND first 4–5 specialists providing empirical calibration of the 0.30 threshold.
- **INV-DESIGN-DOC-SYMMETRY (PROPOSED — per CB §9 candidate).** Body↔bibliography symmetry for any synthesis document in `design/`. Mechanical Verification: `scripts/design-doc-audit.sh` (PROPOSED). Source: CB §9 item 1; CB Lesson 3 (Role 3 citation-renumbering defect). Promotion blocked on user authorization per CB §9 caveat.

---

## Drafter close attestation

**Coverage tally.** Sections 1, 2 (2.1 + 2.2), 3 (3.1 + 3.2), 4 (4.1 INBOUND + 4.2 OUTBOUND), 13, 15 (15.1 + 15.2), 16 authored. Total: 7 sections of 18 assigned to this drafter. Remaining sections (§5–§12, §14, §17, §18) are out of scope per the drafter assignment.

**Mechanical-check status.**

- §13 row 1 (Identity word count, R1): PROPOSED — deferred per §16 INV-SPECIALIST-AUDIT promotion-blocker (script does not exist).
- §13 row 2 (description field, R2): PROPOSED — deferred.
- §13 row 3 (body length, R3): PROPOSED — deferred.
- §13 row 4 (voice register, R4): PROPOSED — deferred.
- §13 row 5 (refusal taxonomy, R5 + R6): PROPOSED — deferred.
- §13 row 6 (Mechanical Check stub presence, R7): PROPOSED — deferred.
- §13 row 7 (IDENTICAL SHA-256, R8): PROPOSED — deferred.
- §13 row 8 (DIFFER Jaccard, R9): PROPOSED — deferred + v1-calibration-pending.
- §13 row 9 (PF-grounded Anti-Patterns, R11): PROPOSED — deferred.
- §13 row 10 (INV-ROLE-INLINING): REFERENCED — verified via Grep against INVARIANTS.md line 41 (`grep -n "INV-ROLE-INLINING" /Users/waltermcgivney/Documents/Projects/a-plus-maxing/INVARIANTS.md` returned line 41).
- §13 row 11 (INV-BRANCH-NOT-MAIN): REFERENCED — verified via Grep against INVARIANTS.md line 43.
- §13 row 12 (INV-RESEARCH-ATTESTATION downstream): REFERENCED-by-Role-2-for-downstream — verified via Grep against INVARIANTS.md line 35; Role 2 itself does not inherit at design time.
- §13 rows 13–16 (Negative Examples, mode floor, self-audit gate, Modes): PROPOSED — deferred.

**Decisions** (simpler-assumption choices made by this drafter; alternative not taken stated):

1. Took Role 2 ownership of `scripts/audit-specialist-profile.sh` bash implementation (per §2.2 item 4). Alternative not taken: separate tooling-pass / fifth role for audit-script bash. Rationale: Role 1 §2.2 NOT-owned item 5 explicitly defers bash to "Role 2 or a dedicated tooling pass"; absent a tooling-pass role on the project critical path, Role 2 is the natural owner — the implementer authors the specialists AND the audit script that gates them, mirroring the senior-engineer's ownership of both code AND tests-for-that-code.
2. Marked R9 (DIFFER Jaccard 0.30) as ACCEPTED — calibration-pending rather than ACCEPTED + DEFERRED. Alternative not taken: DEFERRED until first 4–5 specialists author. Rationale: the rule's IMPLEMENTATION (Jaccard ≤0.30) is accepted; the THRESHOLD (0.30 specifically) is calibration-pending per substrate Limitation 9. The discipline applies from specialist 1 onward; the threshold revises after specialist 4–5.
3. Used 16-row §13 table (rather than Role 1's 17-row pattern). Alternative not taken: 17 rows mirroring Role 1 exactly. Rationale: Role 1's §13 row 14 (H-class composition) and row 15 (Role-4 adversarial-probe pass anchor) and row 17 (multi-turn re-anchor cadence) are SPECIALIST-runtime gates owned by Roles 3/4 + per-specialist Loop-Breaking; Role 2's §13 covers implementer-process gates + Role-1-spec bash implementations + Role-2-authored extensions. Role 1's row 16 (vendor_label sentence-collision) is mirrored at the specialist-output layer at Roles 1 + Role 4 vault contributions, not at the Role 2 design-doc layer.
4. Encoded Architecture Question escalation as process-level (§15.2 AC + §17 risk surface) rather than mechanical §13 row. Alternative not taken: §13 row for Architecture Question artifact path existence. Rationale: Architecture Question is a HALT artifact, not a deployment gate; mechanizing its EXISTENCE (a counter) does not encode its CORRECTNESS (whether the question is genuinely architectural vs implementer judgment failure). The latter requires architect read, not grep.
5. Marked CB §9 INV-DESIGN-DOC-SYMMETRY as PROPOSED in §16 rather than skipping it. Alternative not taken: defer to a future session. Rationale: CB §9 explicitly flags it as candidate-invariant high-value; flagging in §16 lets the orchestrator/architect adjudicate at Phase 5 without surfacing as a §18 blocker. Promotion-blocker (user authorization per CB §9 caveat) preserved.

**Blockers.** None for the 7 sections assigned. Note that the §13 PROPOSED rows depend on `scripts/audit-specialist-profile.sh` existing; the script's authoring is itself part of Role 2's deliverable surface per Decision 1 above and surfaces as a §17.2 assumption / §18 OQ at the SE-drafter or QA-drafter level.

**Pass-1 anchor check.** Every authored section cites ≥1 `Finding N` / `R-N` / `PF-S\d+-\d+` / `INV-*`:

- §1: `Finding 1`, `Finding 4`, `Finding 6`, `Finding 7`, `Finding 9`, `R-7`, `R-13`, `R-14`.
- §2.1 + §2.2: `Finding 3`, `Finding 7`, `Finding 9`, `R-5`, `R-8`, `R-9`, `R-11`, `R-12`, `R-13`, `R-14`; CB §10 row 4; Role 1 §2.2; Role 1 §4 OUTBOUND row 8.
- §3.1: all 9 Findings cited with substrate line ranges.
- §3.2: all 15 Recommendations cited with verdicts.
- §4.1: Role 1 §4 OUTBOUND rows 1–8 cited by row number + Role 1 §13 row references; CB §10 row 7.
- §4.2: `Finding 7`, `Finding 9`, `R-8`, `R-9`, `R-12`, `R-13`, `R-14`; CB §10 row 4.
- §13: `R-1` through `R-15` mapped by row + verified `INV-ROLE-INLINING`, `INV-BRANCH-NOT-MAIN`, `INV-RESEARCH-ATTESTATION` references against INVARIANTS.md; PF-S3-01 guard cited for no-LIVE-without-existing-script discipline.
- §15.2: `R-4`, `R-7`, `R-8`, `R-9`, `R-11`, `R-12`, `R-13`, `R-14`; `Finding 9` worked examples; `PF-S2-02`, `PF-S2-04`, `PF-S3-01`, `PF-S6-01`, `PF-S2-05` cited; DESIGN_DOC_TEMPLATE.md §0.2 cited.
- §16: `INV-ROLE-INLINING`, `INV-BRANCH-NOT-MAIN`, `INV-SCOPE-CONTRACT`, `INV-PF-ATTESTATION`, `INV-HO-ROTATION`, `INV-HO-NO-STALE-HASH` addressed by scope criterion; `R-8`, `R-9`, `R-13` cited for proposed INV candidates; CB §9 item 1 cited.

Anchor check PASS.
