---
title: Adversarial Review — Role 2 (health-implementer) Pass-2 Design Doc
type: red-team-output
reviewer: /adversarial-review skill
target: design/health-implementer-design.md
target_commit_sha: 7ac6a0ccbc27b1383f046f4e1906a87704527fde
target_line_count: 679
created: 2026-05-27
session: S10
total_findings: 27
categories_walked: [Ambiguity, Edge Cases, Contradictions, References, Ordering, Scope, Downstream, Language Economy]
---

# Adversarial Review — Role 2 (health-implementer) Pass-2 Design Doc

Walk applied per `~/.claude/skills/adversarial-review/SKILL.md` 8-category protocol. Substrate (`design/.health-implementer-design-work/domain-research.md`, 754 lines, 9 Findings + 15 Recommendations) cross-referenced. Role 1 design doc (`design/health-specialist-architect-design.md`, Status: Final) cross-referenced for INBOUND fidelity. Template (`design/DESIGN_DOC_TEMPLATE.md`) cross-referenced for spec compliance. INVARIANTS register and PF log verified.

## Inventory snapshot

- Sections (`^## ` headings): **23** observed in `grep -cE '^## '`. Of these, 18 are top-level template sections (§1–§18) + Appendix A; the additional 4 are raw `## Context Loading` and `## Loop-Breaking` headings inside §12 Negative Example BAD/GOOD code blocks. This is load-bearing — see F-001.
- §13 row count: **23 rows** total; **20 PROPOSED**, 3 REFERENCED, 0 LIVE. Text claims "PROPOSED: 18 (... note total 20 row IDs)" — see F-002.
- §3.1 Findings: 9 rows. §3.2 Recommendations: 15 rows. Substrate matches.
- §11.1 PF coverage: all 8 PF entries cited and verdicted.
- §15.2 Acceptance Criteria: 10 items.
- §14 Edge Cases: EC-1 … EC-14 (14 items).
- §18 Open Questions: OQ-1 … OQ-8 (8 items).
- §4.1 INBOUND rows: 8 (matches Role 1 §4 OUTBOUND count of 8). §4.2 OUTBOUND rows: 5.

---

## Findings

---

### F-001: §12 Negative Example BAD/GOOD code blocks emit raw H2 headings that pollute structural section count

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / S — Scope Violations |
| **Severity** | Critical |
| **Section** | §12 (Negative Examples) interacting with §13 row 6.5 (section-count audit) |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §12.3 and §12.4 contain BAD/GOOD code blocks that begin lines with `## Context Loading` and `## Loop-Breaking`. Markdown does NOT treat these as headings (they live inside fenced or unfenced code blocks — they need verification) but `grep -cE '^## '` returns **23**, not 19 (= 18 template sections + Appendix A). The Role 2 §13 row 6.5 spec says: "`grep -cE '^## '` in body = 11 (10 base + Modes)". For the implementer's downstream specialist authoring this means: any specialist Negative Example that demonstrates a BAD section header **will fail the very audit Role 2 designed**. The Role 2 design doc itself fails an audit modeled on its own row 6.5 today.

**Evidence.** `grep -cE '^## ' design/health-implementer-design.md` → 23. Lines 383, 391 (`## Context Loading` inside §12.3 BAD/GOOD), 410, 418 (`## Loop-Breaking` inside §12.4 BAD/GOOD). Per `Bash -c "grep -nE '^## ' design/health-implementer-design.md"` output, these are at lines that fall inside §12 example blocks, not at template-section boundaries.

**Fix.** Wrap §12.3 and §12.4 BAD/GOOD blocks in triple-backtick fences (` ``` `) OR indent the section-header lines OR escape with HTML comments — choose whichever produces a stable `grep -cE '^## '` result that matches template-section topology. Then re-state §13 row 6.5 mechanism to reflect: either grep against a stripped body (code-block fences excluded) or use a different anchor. The "raw H2 in code block" failure mode must be added to §14 (probably EC-15) — it is exactly the kind of authoring mistake a fatigued implementer will make on profile 7+, and Role 2 itself demonstrates the failure mode now.

---

### F-002: §13 status-tag count contradiction — "PROPOSED: 18" but actual count is 20

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions |
| **Severity** | High |
| **Section** | §13 (Status-tag count line) + §18 OQ-8 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** Line 464 says: `**Status-tag count.** LIVE: 0. REFERENCED: 3 (rows 16/17/18). PROPOSED: 18 (rows 1, 2, 3, 4, 5, 5.5, 6, 6.5, 6.6, 7, 7.5, 8, 9, 10, 11, 12, 12.5, 13, 14, 15 — note total 20 row IDs because of decimal extensions surfaced from §14 ECs).` The enumeration parenthetical contradicts the headline figure: the 20-element list IS the PROPOSED count. OQ-8 inherits the wrong figure: `### OQ-8 — §13 PROPOSED row count vs §18 budget (18 PROPOSED rows in Role 2 §13)`. Mechanical re-count via `awk '/^## 13/,/^## 14/' | grep -cE '\| PROPOSED \|'` = **20**.

**Evidence.** Lines 464–466, plus OQ-8 line 665. Verified by bash count.

**Fix.** Replace "PROPOSED: 18" with "PROPOSED: 20" in line 464; correct OQ-8 title to "20 PROPOSED rows" and adjust its budget-rationale prose. If the original intent was "18 base rows" vs "5 decimal-extended rows", state both numbers explicitly: `13 base PROPOSED + 7 decimal-extended PROPOSED = 20 total`. (Decimal extensions are rows 5.5, 6.5, 6.6, 7.5, 12.5 — that's 5, not 7; recount the partition.)

---

### F-003: AC-3 mechanism is tautological — passes via self-reference, not the dual-gate clause it claims to verify

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguity / S — Scope (tautological test) |
| **Severity** | Critical |
| **Section** | §15.2 AC-3 + §7 Loop-Breaking |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** AC-3 says: "Self-audit dual-gate clause present in Role 2 **Loop-Breaking**. `grep -cE '(audit.*pass.*necessary.*not.*sufficient|Role.4.*review.*before)' design/health-implementer-design.md` ≥1." Two defects:
(a) `grep -cE` on the entire file returns **1** match — and that match is on **line 556 itself** (the AC-3 line, because its regex literal contains `audit.*pass.*necessary.*not.*sufficient` as a string).
(b) §7 Loop-Breaking does NOT contain a "dual-gate" clause. The closest prose ("Mechanical-check pass is necessary but not sufficient — Role 3's review is the runtime-behavior gate") lives at §8.5 line 228, NOT in Loop-Breaking. And that line does NOT match the regex anyway: the regex requires `audit.*pass`, the line says `Mechanical-check pass` (no preceding `audit` token).

The AC is a **tautology**: it passes today because the regex literal exists inside the AC's own definition. If the AC's prose were ever rewritten to use a different regex literal in the AC line, the AC would silently FAIL even though the prose dual-gate clause at §8.5 still exists. The verdict and the prose are decoupled. This is the canonical **PF-S3-01 surface** — "verdict attests presence of a thing without verifying the thing is actually where the AC says it is" — which Role 2 §11.1 claims to defend against IN-SCOPE.

**Evidence.** Line 556 (AC-3 definition); line 228 (`Mechanical-check pass is necessary but not sufficient — Role 3's review is the runtime-behavior gate`); bash `grep -nE "(audit.*pass.*necessary.*not.*sufficient|Role.4.*review.*before)" design/health-implementer-design.md` returns ONLY line 556.

**Fix.** Either (a) move the dual-gate clause into §7 Loop-Breaking as a numbered threshold so the AC-3 wording "in Role 2 Loop-Breaking" is true, AND rewrite the regex to be unique to the clause's actual wording (e.g., `audit-pass-necessary-Role-3-sufficient` as a deliberate marker phrase that does NOT appear in AC-3's own line); OR (b) restate AC-3 to grep a marker phrase that's only in the Loop-Breaking section AND escape the regex inside AC-3's text so the AC line itself cannot match. The current AC encodes broken behavior — silence is currently equivalent to absence.

---

### F-004: AC-2 glob `.claude/agents/*/agent.md` includes foundation roles, not just 14 specialists

| Field | Value |
|-------|-------|
| **Category** | E — Edge Cases / S — Scope Violations |
| **Severity** | High |
| **Section** | §15.2 AC-2 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** AC-2 says "All 14 specialist profiles pass `scripts/audit-specialist-profile.sh`" using glob `.claude/agents/*/agent.md`. But `.claude/agents/` currently contains `health-specialist-architect/` (a foundation role, not a specialist), and post-deployment it will contain `health-implementer/`, `health-edge-case-reviewer/`, `medical-safety-reviewer/` — all foundation roles, NOT specialists. The glob does NOT restrict to specialist slugs. When AC-2 runs at Session B completion, it will try to audit foundation profiles against a script designed for specialist profiles — guaranteed failure or false-pass depending on script implementation. This conflates "agent directory" with "specialist directory".

**Evidence.** Line 555. `ls .claude/agents/` returns `health-specialist-architect` (the only currently-deployed agent, a foundation role). WIKI.md lines 276–289 enumerate the 14 specialists with suffixes `-specialist`, `-coach`, `-strategist`, `-trainer`, `-nutritionist`, `-liaison` — none of which appear in the AC-2 glob.

**Fix.** Restrict the glob to specialist slugs explicitly, or maintain a `vault/WIKI.md` -> bash array. E.g., `for slug in peptide-specialist labs-specialist nutritionist supplement-specialist endocrine-specialist lymphatic-specialist gi-specialist cardiovascular-specialist sleep-coach recovery-specialist longevity-strategist mental-performance-coach medical-liaison personal-trainer; do scripts/audit-specialist-profile.sh ".claude/agents/$slug/agent.md" || exit 1; done`. This also fixes WG-3 surface: the explicit slug-list becomes the single source of truth across AC-2, AC-10, and any §13 row that needs to enumerate specialists.

---

### F-005: AC-3 / AC-6 / AC-7 / AC-8 / AC-9 / AC-10 check `.claude/agents/health-implementer/agent.md` which does not exist

| Field | Value |
|-------|-------|
| **Category** | R — Broken References / O — Ordering |
| **Severity** | High |
| **Section** | §15.2 AC-3, AC-6, AC-7, AC-8, AC-9, AC-10 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** Six of the ten Acceptance Criteria grep against `.claude/agents/health-implementer/agent.md`. That file does not yet exist (Glob: directory `.claude/agents/health-implementer/` does NOT exist; only `health-specialist-architect/` exists). The ACs cannot be evaluated at design-doc finalize time — they are post-`/upgrade-agent`-deployment ACs masquerading as design-doc acceptance criteria. Template §15 spec calls for "binary pass/fail" criteria; criteria that are unrunnable at the document's stated `status: Phase-3 Red-Team Pending` are non-binary at this moment.

**Evidence.** Lines 559–563; `ls .claude/agents/` shows only `health-specialist-architect/`.

**Fix.** Partition §15.2 into two sub-blocks: (a) design-doc-time ACs (gradeable against the design doc itself before deployment — e.g., AC-1 script existence, AC-4 Recommendation-verdict completeness, AC-5 Finding citation count, the dual-gate clause's existence at the design-doc layer); (b) post-deployment ACs (gradeable only after `/upgrade-agent` produces the `.claude/agents/health-implementer/agent.md` file). Label the second block "AC-deploy-N" and explicitly note: these gate Session B exit, not design-doc finalize. Phase 5 finalize today cannot tick boxes (b) — confusing them produces the canonical PF-S2-05 invocation ("I read the AC, mental-modeled it as runnable").

---

### F-006: §16 Invariants table claims INV-RESEARCH-* OUT-OF-SCOPE while §13 row 18 REFERENCES INV-RESEARCH-ATTESTATION

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions |
| **Severity** | High |
| **Section** | §16 (header text) + §13 row 18 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §16 header (line 568–569) says: "Research-domain `INV-RESEARCH-*` OUT-OF-SCOPE for Role 2 at design time (Role 2 does NOT dispatch `aplus-research` at design time; specialists Role 2 authors inherit at THEIR runtime per §13 row 18)." But §13 row 18 (line 462) tags status as `REFERENCED-by-Role-2-for-downstream (INV-RESEARCH-ATTESTATION)`. If INV-RESEARCH-* is OUT-OF-SCOPE at §16, it cannot be REFERENCED at §13. The doc tries to have it both ways — claim non-scope at §16 while claiming a reference relationship at §13. This breaks INVARIANTS register discipline (a REFERENCED status carries the invariant's mechanical-verification guarantee; OUT-OF-SCOPE explicitly disclaims it).

**Evidence.** Lines 462, 568–569. INVARIANTS.md row 3 confirms INV-RESEARCH-ATTESTATION's scope is "aplus-research" — not Role 2's design-time deliverable.

**Fix.** §13 row 18 is downstream-only (specialists' runtime inherit, not Role 2's deliverable). Either (a) remove row 18 from §13 entirely — it doesn't audit Role 2's output and the §16 OUT-OF-SCOPE claim is the right framing; OR (b) add a separate §13 sub-table "Downstream-runtime References (specialist deploy gate; not Role 2 design-time)" with row 18 alone, AND amend §16 from "OUT-OF-SCOPE for Role 2 at design time" to "OUT-OF-SCOPE for Role 2's deliverable; downstream-inherited at specialist runtime per §13 sub-table." Status semantics must be consistent across §13 and §16.

---

### F-007: §4.2 OUTBOUND row 2 unilaterally claims ownership of `scripts/audit-specialist-profile.sh` bash; Role 1 §2.2 NOT-owned item 5 says "Role 2 OR dedicated tooling pass"

| Field | Value |
|-------|-------|
| **Category** | S — Scope Violations / R — Broken References |
| **Severity** | High |
| **Section** | §2.2 owned item 4 + §4.2 OUTBOUND row 2 |
| **Resolution** | Prevent (escalate via Architecture Question per §6 step 2) |
| **Affected File** | design/health-implementer-design.md |

**Description.** Role 1 §2.2 item 5 (NOT-owned) says: "Implementation of `scripts/audit-specialist-profile.sh` (owned by **health-implementer** or a dedicated tooling pass; I write the interface contract, not the bash)." The "**or a dedicated tooling pass**" leaves ownership ambiguous; Role 2 unilaterally takes it (§2.2 owned item 4: "The bash implementation of `scripts/audit-specialist-profile.sh` per Role 1's interface spec"). Per Role 2's own §6 step 2 (Implementer-vs-architect ownership check) and the Architecture Question discipline, **this is exactly the surface the implementer is required to escalate, not infer**. Role 2 chose option A; Role 1 left options A or B. There's no cited evidence that the orchestrator resolved this between Role 1 finalize and Role 2 dispatch.

Compounding: §17.2 A-3 candidly notes the same ambiguity ("Role 1 §2.2 NOT-owned item 5 names Role 2 (or 'dedicated tooling pass') as owner") and routes it to §18 OQ-1. So the doc IS aware of the ambiguity — but the §2.2 owned-item-4 sentence asserts the resolution before OQ-1 resolves it. The §2.2 statement and the §17.2 + §18 framing contradict at the speech-act level (declarative ownership vs. open question).

**Evidence.** Role 1 design doc line 66 (`(owned by health-implementer or a dedicated tooling pass; I write the interface contract, not the bash)`); Role 2 §2.2 line 54 (`The bash implementation of scripts/audit-specialist-profile.sh per Role 1's interface spec`); Role 2 §17.2 A-3 line 609; Role 2 §18 OQ-1 line 630.

**Fix.** Two options. (a) Remove the unilateral ownership claim from §2.2 owned item 4; replace with "candidate owner pending OQ-1 resolution" and move the bash implementation under §2.2 conditional ("becomes owned if OQ-1 resolves to Role 2"). (b) Escalate via the Architecture Question protocol Role 2 itself defines (§6 step 2; §11.2 anti-pattern 6 "I author the check first…"), producing AQ-000 BEFORE Phase 5 finalize. The current state — declaring ownership AND naming the same item as an open question — encodes the AP-ORCH-SELF-ATTEST class of failure that PF-S3-01's lessons exist to prevent.

---

### F-008: §13 QA-strict tag rule divergence is load-bearing AND silently inconsistent — Role 2 PROPOSED rows could pass Role 1 LIVE rule

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / D — Downstream Breakage |
| **Severity** | High |
| **Section** | §13 header (line 434) + §18 OQ-7 |
| **Resolution** | Prevent (route to architect amendment) |
| **Affected File** | design/health-implementer-design.md (+ design/health-specialist-architect-design.md cross-reference) |

**Description.** Role 2 §13 line 434 adopts QA-strict tagging: `LIVE requires both (a) the check script/hook exists and (b) a smoke test exercises it against a negative case.` Role 1 §13 (per Role 1 line 469) adopts a weaker rule: `LIVE rows have their paths verified to resolve via Glob/Read against the current commit`. OQ-7 documents the divergence as "non-blocking for design-doc finalize" but the downstream consequences are not "non-blocking" — they break cross-doc audit consistency:

- When `scripts/audit-specialist-profile.sh` ships AND the script alone passes Role 1's check, **Role 1's §13 rows auto-promote to LIVE while Role 2's matching rows stay PROPOSED** until the smoke test ships separately. The same row, same script, two states. Roles 3 and 4 (which inherit `INBOUND` from both) cannot decide whether to treat the row as LIVE or PROPOSED.
- The "QA-strict" choice is a unilateral implementer act against an architect-authored spec (Role 1's §13 tag rule). Per Role 2 §6 step 2, this is an architect-decision that must be escalated, not adopted with a footnote.

**Evidence.** Role 2 line 434; Role 1 line 469; OQ-7 line 660.

**Fix.** Architecture Question to Role 1 (or orchestrator pre-architect-deployment): "Role 2 §13 adopts QA-strict tagging (test-existence-based) divergent from Role 1 §13 (check-existence-based). Recommendation: amend Role 1 §13 to QA-strict for consistency across the four foundation docs, OR amend Role 2 to check-existence and restore alignment, OR document the divergence with an explicit per-doc tag-rule note in DESIGN_DOC_TEMPLATE.md §13 spec." Phase 5 finalize should NOT proceed with the divergence carrying only an OQ-7 pointer — this is exactly the "silent inference" failure mode that §6 escalates.

---

### F-009: §15.2 AC numbering inconsistent — AC list runs 1–10 but §15.2 prose contains references to "AC-2 mechanism" / "AC-3 dual-gate" with no hyphen, while §11.1 says "AC-3" and §17.1 R-1 says "§15.2 AC-3"

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / R — Broken References |
| **Severity** | Low |
| **Section** | §15.2 + cross-refs in §11.1, §17.1 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** Style is internally inconsistent between `AC-N` (with hyphen) and `AC N` (without) and `AC<n>`. Acceptance criteria are numbered `1.`, `2.`, ... `10.` in §15.2 (line 554+) but referred to as "AC-3" in §11.1 (line 308, "AC-3 dual-gate clause defend") and §17.1 R-1 (line 595, "§15.2 AC-3 verifies dual-gate clause"). No place in §15.2 actually says "AC-3" — the AC list is bare-numbered.

**Evidence.** Line 308: `R13 self-audit + AC-3 dual-gate clause defend`; line 595: `§15.2 AC-3 verifies dual-gate clause`; lines 554–563 (numbered without "AC-" prefix).

**Fix.** Prefix each criterion in §15.2 with `AC-1`, `AC-2`, ..., `AC-10`. Make all cross-refs match.

---

### F-010: §5 rule 4 voice-budget regex over-counts "non-aggressive" `[Yy]ou` instances — the design doc itself violates the rule it imposes on specialists

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / D — Downstream Breakage |
| **Severity** | High |
| **Section** | §5 rule 4 + entire design doc |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §5 rule 4: `non-aggressive \b[Yy]ou (must|should|will|are|need to|have to)\b allow-budget ≤3`. Audit on the design doc itself: `grep -ciE "\b[Yy]ou (must|should|will|are|need to|have to)\b" design/health-implementer-design.md` → **9 matches**. The Role 2 design doc fails its own rule. If the implementer at deploy time runs `.claude/agents/health-implementer/agent.md` through `enforce-role-inlining.sh` which loads the full 11-section profile — and the profile inherits the same regex from the design doc — the deployed agent profile carries forward the violation surface.

Note: the AGENT_TEMPLATE-conforming `agent.md` is downstream of THIS design doc; if §5 rule 4 says "≤3" and the design doc has 9, the deployed profile may or may not (depending on `/upgrade-agent` Phase 5 synthesis). But the design doc serves as exemplar; this is the "the prose first, derive the check after" failure that §11.2 anti-pattern 6 names.

Also `grep -cE '\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b' design/health-implementer-design.md` → **7 matches**. These appear in §12.2 BAD example block and §13 row 4 regex literal — they're "quoted" demonstrations, but they will fail the same regex that AC-8 imposes on the deployed agent.md. The doc anticipates this surface in EC-14 (duplicate header in a Negative Example tripping the audit) but not for the BAD-content jailbreak-content asymmetry of the regex.

**Evidence.** `Bash grep` counts above. Section §12.2 lines 360–365 (BAD block); §13 row 4 line 443; §11.2 line 320 (recognition cue prose).

**Fix.** Add a paragraph to §5 rule 4 (or §13 row 4) clarifying: "Banned-phrase regex applies to the deployed `agent.md`, not to the design doc itself. The design doc legitimately quotes the banned phrases inside BAD code blocks; the deployed profile must not. Mechanical-check should scope the grep to `.claude/agents/*/agent.md`, never to `design/*.md`." Without this scoping note, an implementer running an audit on their own work-in-progress design doc will trip the very rule that's supposed to apply to deployed agents only.

---

### F-011: Substrate-unaddressed gap WG-1 surfaces — §10.1 auto-loads `domain-research.md` for specialists that have no Pass-1 substrate

| Field | Value |
|-------|-------|
| **Category** | E — Edge Cases / R — Broken References |
| **Severity** | High |
| **Section** | §10.1 (item 1) + §10.5 (cross-role triggers) |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §10.1 item 1: `design/health-specialist-architect-design.md — architect's design doc. Cannot author against unread architect doc.` This auto-load works for Role 2's first task (authoring 14 specialists). BUT the design doc says nothing about whether `domain-research.md` for the specialist being authored is also auto-loaded — and per template §0.1 line 30–32, **the 14 specialists have NO Pass-1 substrate yet** (Pass-3 lands after specialists deploy). When Role 2 authors `sleep-coach/agent.md`, there's no `design/.sleep-coach-design-work/domain-research.md` to read.

§17.2 A-4 mentions "14-specialist roster stable through Role 2's batch authoring" but does NOT address the substrate-gap. The implementer's process step 1 (Pass-1 substrate read) is undefined for specialist authoring during Session B before Pass-3 lands. This is canonical WG-1 from the Phase 3 Watch List.

**Evidence.** §10.1 line 265–270; DESIGN_DOC_TEMPLATE.md §0.1 line 32 ("specialist design docs follow this template too, with the §3 specialist-fallback content path until their own Pass-1 lands in Pass-3").

**Fix.** Add §10.1 item 5.5 (or amend item 1): "If authoring a specialist whose Pass-3 substrate has not landed, substitute Role 1's `domain-research.md` for the foundation-class inheritance (per template §3 specialist-fallback path). Substrate-absent case is HALT-condition `pass1-substrate-missing` (not `context-load-missing`) — orchestrator decides between proceeding via foundation inheritance OR deferring specialist authoring until Pass-3." Also amend §10.5 OUTBOUND cross-references to list "Pass-1-substrate-fallback discipline" as something Role 2 establishes for the 14 specialists.

---

### F-012: Substrate-unaddressed gap WG-2 surfaces — §8.1 hedges on `library-index.md` authoring; ownership undefined

| Field | Value |
|-------|-------|
| **Category** | S — Scope Violations / R — Broken References |
| **Severity** | High |
| **Section** | §2.2 owned/not-owned + §8.1 Write/Edit |
| **Resolution** | Prevent (escalate via Architecture Question) |
| **Affected File** | design/health-implementer-design.md |

**Description.** §8.1 line 201: `Write / Edit — author .claude/agents/<specialist-slug>/agent.md and (if template variant requires) library-index.md`. The "if template variant requires" hedge is undefined: Role 1's deployed deliverable includes a paired `library-index.md` (Role 1 had one; 24 lines, 5 conditional refs). Spec for whether the implementer authors a per-specialist `library-index.md` is not in substrate; not in design doc; not in Role 1's §13. Either commit the library-index.md authoring to implementer ownership OR escalate via Architecture Question OR explicitly defer — the current hedge is neither.

§2.2 owned-items list (8 items) does NOT include `library-index.md`. §2.2 not-owned list (10 items) does NOT explicitly disclaim it either. The ownership is dangling. This is canonical WG-2 from the Phase 3 Watch List.

**Evidence.** §8.1 line 201; §2.2 lines 50–71.

**Fix.** Either (a) add `library-index.md` to §2.2 owned-items list with explicit spec ("≤30 lines; ≤5 conditional refs to vault/library/<class>/ paths; auto-load only when specialist's Tools section requires"), and add a §13 row 9.5 PROPOSED auditing its shape; OR (b) escalate via AQ — "Should Role 2 author a per-specialist library-index.md? Role 1 deployed with one; the spec is silent; recommend (a)." Avoid the §8.1 hedge: an implementer at deploy time reads "if template variant requires" and has no way to decide.

---

### F-013: Substrate-unaddressed gap WG-3 surfaces — §13 row 12 audits `--mode` only; `target_class` declaration not audited

| Field | Value |
|-------|-------|
| **Category** | E — Edge Cases / D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §13 row 12 / §13 row 12.5 + §14 EC-5 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** R12 covers `--mode` floor per specialist; §13 row 12 audits mode-floor presence; §13 row 12.5 audits mode-floor correctness vs risk-class. None of them audit the **`target_class` enumeration** the SPECIALIST needs to invoke `aplus-research` correctly (per `aplus-research` SKILL.md §1.2: `--target-class` is a required parameter — `compound | biomarker | protocol | reference`). A specialist Tools section that declares `aplus-research --mode=deep` without a target_class still fails `aplus-research`'s own argument validation at runtime. This is canonical WG-3.

**Evidence.** §13 rows 12 and 12.5 (lines 455–456); §14 EC-5 (lines 494–497, covers wrong mode-floor default but not target_class).

**Fix.** Add §13 row 12.6 PROPOSED: `target_class declaration per specialist`. Mechanism: `grep -E "aplus-research.*--target-class.*(compound|biomarker|protocol|reference)"` ≥1. Consequence: WARN initially (target_class can be inferred from WIKI.md "Dispatches research on:" column for 13 of 14 specialists; the medical-liaison's "none — collates only" requires AQ). Add §14 EC-15: "Specialist Tools section declares aplus-research --mode without --target-class; SKILL.md argument validation rejects at runtime."

---

### F-014: Substrate-unaddressed gap WG-4 surfaces — per-specialist operator-profile field enumeration not specified

| Field | Value |
|-------|-------|
| **Category** | E — Edge Cases / R — Broken References |
| **Severity** | Medium |
| **Section** | §10.3 + §4.1 INBOUND row 5 |
| **Resolution** | Defer to follow-up bead (per WG-4 watch-list directive) |
| **Affected File** | design/health-implementer-design.md |

**Description.** §10.3 names `vault/meta/operator-profile.md` as NOT-auto-loaded by implementer (specialist-load only). §4.1 INBOUND row 5 says "Implementer encodes the read-order into specialist Context Loading; atomicity mechanism is the specialist-prose-layer choice per Role 1 §13 row 5." Neither specifies which operator-profile fields each specialist-class is expected to read. The cardiovascular-specialist needs `medications`, `cardiovascular_history`, `allergies`; the sleep-coach needs `sleep_baseline`, `caffeine_intake`, `medications`; the gi-specialist needs `dietary_restrictions`, `medications`, `gi_history`. Without per-specialist-class field enumeration, specialists may diverge silently — and the §13 row 6.6 schema-drift audit detects DRIFT but not under-coverage of fields. This is canonical WG-4.

**Evidence.** §10.3 lines 278–285; §4.1 INBOUND row 5 line 131; §13 row 6.6 line 448.

**Fix.** Either (a) add a §10.3 sub-table "per-specialist-class operator-profile field enumeration" (small — maps 5–8 specialist classes to a 2–4 field set each); OR (b) escalate via AQ to Role 1 ("operator-profile field schema is owned by Role 1's §4 row 5 contract; should Role 1 enumerate per-specialist or should Role 2?"). The watch-list disposition says defer to bead if not surfaced; surfacing this here means the orchestrator now decides between (a) and (b) at Phase 4.

---

### F-015: §4.2 OUTBOUND row 3 "Self-audit-before-return contract" duplicates §15.2 AC-13 conceptually but is not anchored to it

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions / L — Language Economy (duplication) |
| **Severity** | Low |
| **Section** | §4.2 OUTBOUND row 3 + §13 row 13 + §15 inheritance |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §4.2 OUTBOUND row 3 states "Self-audit-before-return contract" as a Role-2-emitted contract to orchestrator. §13 row 13 mechanizes it (`audit_passed: true` frontmatter + audit-run artifact path). §15.1 says "audit_passed frontmatter" is inherited from `/upgrade-agent` Phase 7 inherited constraints. But §15.2 (role-specific binary ACs) does not enumerate an AC for the contract — only the dual-gate AC-3, which is about Role 3 review (not self-audit). The triangular relationship (§4.2 establishes contract; §13 mechanizes; §15.2 should test) has a missing leg.

**Evidence.** §4.2 row 3 line 142; §13 row 13 line 457; §15.1 line 550; §15.2 lines 554–563.

**Fix.** Add §15.2 AC-11: "`audit_passed: true` frontmatter present in deployed specialist `agent.md` files. `grep -E '^audit_passed: true$' .claude/agents/<specialist-slug>/agent.md` ≥1 for every specialist authored." This closes the triangle and creates a deployed-specialist-time AC (sister to the design-doc-time partition recommended in F-005).

---

### F-016: §11.1 PF-S2-04 row claims §10.3 + §11.2 AP3 + §12.3 cover the failure — but §11.2 AP3 says "I don't auto-load operator-profile" which doesn't cover the over-personalization-via-WIKI-row-quote surface

| Field | Value |
|-------|-------|
| **Category** | E — Edge Cases / D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §11.1 PF-S2-04 row + §11.2 AP3 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §11.1 says PF-S2-04 (over-personalized library research) is IN-SCOPE because "§10.3 explicit NOT-auto-load of operator-profile; §11.2 AP3 + §12.3 BAD/GOOD; Finding 7 IDENTICAL/DIFFER partition." But PF-S2-04 (per `memory/process-failures.md`) is about CONFLATING library research (goal-agnostic) with specialist dispatch (personalized). The implementer surface is: implementer reads WIKI.md row for a specialist and silently bakes operator-bound personalization into the specialist's profile DIFFER block. §11.2 AP3 covers only the operator-profile-inlining case; it does NOT cover the "implementer reads WIKI.md row that mentions operator-class context (e.g., medical-liaison's 'operator-profile (Jan 2026 issue)' note) and inlines that note into the deployed profile." That's a different surface and §11.2 doesn't have an AP for it.

**Evidence.** PF log line 46–48 (`Conflated library research with specialist-agent dispatch`); WIKI.md line 289 (medical-liaison row: `operator-profile (Jan 2026 issue)`); §11.2 AP3 lines 321–322.

**Fix.** Add a sub-clause to §11.2 AP3 (or new AP3.5): "I don't read forward from a WIKI.md row's operator-context note (e.g., 'Jan 2026 issue') into the specialist profile body. The WIKI.md row tells me what the specialist READS at runtime; the implementer authors the read-instruction, never the read-content." Add §14 EC-15: "Implementer authors `medical-liaison/agent.md` and copies WIKI.md row's `(Jan 2026 issue)` parenthetical into the Identity sentence."

---

### F-017: §13 row 5.5 GRADE two-axis check uses regex requiring exact strings `certainty:` and `strength:` — but Role 1 §5 Rule 12 uses GRADE without colon-separated key:value format

| Field | Value |
|-------|-------|
| **Category** | R — Broken References / D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §13 row 5.5 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §13 row 5.5: `Per claim block: grep -E "certainty: (high|moderate|low|very-low)" ≥1 AND grep -E "strength: (strong|weak|conditional)" ≥1`. The regex requires literal `certainty: ` and `strength: ` tokens. But Role 1 §5 Rule 12 ("GRADE two-axis tagging is the medical equivalent of static types") doesn't mandate that the deployed specialist write GRADE tags in `key: value` syntax — it mandates the two tags exist somewhere on each claim. A specialist writing `[certainty moderate, strength weak]` (no colon) or `<certainty=moderate strength=weak>` or YAML-block GRADE annotations passes Role 1's invariant but fails Role 2's audit.

**Evidence.** §13 row 5.5 line 445; Role 1 line 170 ("a GRADE certainty tag (high/moderate/low/very-low) AND a recommendation-strength tag (strong/weak/conditional)").

**Fix.** Either (a) loosen the regex: `grep -E "certainty[: =]+(high|moderate|low|very-low)"` + analogous for `strength`; OR (b) document a stricter format and add to IDENTICAL block ("specialists use `certainty: X, strength: Y` syntax verbatim"). Don't leave the mismatch — it produces false-positive audit failures.

---

### F-018: §13 row 17 "Branch hygiene" is IRRELEVANT to specialist-profile audits and pollutes §13's scope

| Field | Value |
|-------|-------|
| **Category** | S — Scope Violations |
| **Section** | §13 row 17 |
| **Severity** | Low |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §13 row 17 references `INV-BRANCH-NOT-MAIN`. The hooks `block-push-main.sh` + `block-commit-main.sh` enforce branch hygiene at git operations — they have nothing to do with auditing a specialist `agent.md` file's contents. §13 is the **Mechanical Enforcement Map** for the deliverable; row 17 is a session-protocol invariant unrelated to deliverable shape. Including it in §13 (claiming REFERENCED-status coverage) inflates the perceived coverage and makes "the §13 row count" a misleading proxy for "how thoroughly the deliverable is audited."

**Evidence.** §13 row 17 line 461.

**Fix.** Move row 17 to §16 Invariants at Risk (where it already appears as `INV-BRANCH-NOT-MAIN: Strengthens (inherits)`) and remove from §13. §13 should audit deliverable shape; §16 audits session-discipline invariants. Cross-table promotion-to-LIVE counting is misleading otherwise.

---

### F-019: §17.1 R-6 mitigation cites OQ-3 but OQ-3 resolution path conflicts with §11.2 AP3 wording

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions |
| **Severity** | Low |
| **Section** | §17.1 R-6 + §18 OQ-3 + §11.2 AP3 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** OQ-3 says canonical refusal-class taxonomy location is undecided ("Candidates: `vault/library/_refusal-class-taxonomy.md`, `templates/refusal-classes.yaml`, leave inline + audit reads by section anchor."). §13 row 5 says `--taxonomy <path>` is a CLI arg the orchestrator supplies. §17.1 R-6 mitigation says "audit accepts `--taxonomy-path` CLI arg orchestrator supplies" (note the hyphen difference: §13 uses `--taxonomy`, §17.1 uses `--taxonomy-path`). Either is fine but the doc must pick one.

**Evidence.** §13 row 5 line 444 (`--taxonomy <path>`); §17.1 R-6 line 600 (`--taxonomy-path CLI arg`).

**Fix.** Make CLI-flag wording consistent across §13 row 5, §17.1 R-6, and any reference in §18.

---

### F-020: §17.2 A-1 says Role 2 frontmatter pins `references_role_1_sha:` — but frontmatter has `references_role_1_sha: design/health-specialist-architect-design.md (Status: Final, S8 close)`, not a sha256

| Field | Value |
|-------|-------|
| **Category** | R — Broken References / L — Language Economy |
| **Severity** | Medium |
| **Section** | Frontmatter + §17.2 A-1 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** Frontmatter line 13: `references_role_1_sha: design/health-specialist-architect-design.md (Status: Final, S8 close)`. The field name literally says "sha" but the value is a file path + status annotation, NOT a sha256 or commit SHA. §17.2 A-1 says "Role 2 frontmatter pins `references_role_1_sha:` at dispatch start" — implying the field carries cryptographic provenance. The field name and value are semantically mismatched.

CLAUDE.md §5 / INV-HO-NO-STALE-HASH disallows sha256/commit-hash prefixes in HANDOFF prose precisely because they go stale — but this is a frontmatter pin where a pinned reference (commit SHA OR file-content-sha256 OR file-mtime OR `last_reviewed` date) would be load-bearing. The field name promises one thing; the value delivers another.

**Evidence.** Frontmatter line 13; §17.2 A-1 line 607.

**Fix.** Either (a) rename the field to `references_role_1_path:` or `references_role_1_at:` and keep the file+status annotation as-is; OR (b) keep the field name `_sha:` and replace the value with an actual sha256 (e.g., `sha256sum design/health-specialist-architect-design.md`). The current state is a contract-name violation that downstream `/upgrade-agent` consumers will be confused by.

---

### F-021: §3.1 row count claim "all 9 Findings ACCEPTED" matches table, but §3.2 R9 is "ACCEPTED — calibration-pending" — verdict mixing breaks the table's binary verdict convention

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / D — Downstream Breakage |
| **Severity** | Low |
| **Section** | §3.2 R9 verdict |
| **Resolution** | Accept (note this is the canonical R9 phrasing per substrate, but flag for clarity) |
| **Affected File** | design/health-implementer-design.md |

**Description.** Template §3 spec: "Each Recommendation tagged ACCEPTED / DEFERRED / REJECTED. Deferrals and rejections require one-line rationale. No 'TBD' verdicts." R9's verdict is "ACCEPTED — calibration-pending" — a hyphenated qualifier that does NOT match the three canonical labels. AC-4's awk mechanism (line 557): `if($4 !~ /ACCEPTED|DEFERRED|REJECTED/) exit 2` would still PASS R9 because the regex `ACCEPTED` is anchored as substring — but a stricter equality check would fail.

The verdict's qualifier carries real meaning ("threshold revises after first 4-5 specialists"); it's not "TBD" exactly. But the template's binary discipline is degraded by hyphenated qualifiers.

**Evidence.** §3.2 R9 line 109; §15.2 AC-4 line 557.

**Fix.** Either (a) tighten AC-4's awk to anchor `($4 == "ACCEPTED" || $4 == "DEFERRED" || $4 == "REJECTED")` and demote R9 to `DEFERRED — calibration-pending`; OR (b) leave as-is but add a note to §3.2 documenting that hyphenated qualifiers are permitted for ACCEPTED-with-conditional-on-future-evidence cases. Either is fine; the current mismatch between template spec and AC mechanism is the load-bearing thing to fix.

---

### F-022: §4.1 INBOUND row 1 inserts a sub-clause Role 1 doesn't make canonical

| Field | Value |
|-------|-------|
| **Category** | R — Broken References / S — Scope Violations |
| **Severity** | Medium |
| **Section** | §4.1 INBOUND row 1 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §4.1 INBOUND row 1: "Implementer encodes ≥4 distinct classes per specialist; does NOT redefine (per `R-5`); per Role 1 §13 row 4 Tools-conditional, **if specialist Tools permit image MIME Reads or image-URL WebFetch, `IMAGE_OR_SIGNAL_INPUT` is MANDATORY**." This Tools-conditional mandatory clause is genuinely in Role 1 §13 row 4 (line 478). But Role 2's framing makes it sound like a Role 2-authored extension. Either fine, but the anti-redefinition rule of §4 (line 146 "Every INBOUND row cites Role 1's §4 row number; specialists' deployed `agent.md` files reference by path/anchor and do NOT inline Role 1's canonical statements") is being walked close: Role 2 is paraphrasing the Role 1 §13 row 4 conditional, not just citing it by anchor.

**Evidence.** §4.1 row 1 line 127; Role 1 §13 row 4 line 478.

**Fix.** Tighten the inline statement to a pure anchor reference: "Implementer encodes ≥4 distinct classes per specialist (`R-5`); the per-row §13 row 4 Tools-conditional `IMAGE_OR_SIGNAL_INPUT` mandatory clause inherits verbatim per Role 1 §13 row 4 (do NOT re-state)." This restores anti-redefinition discipline.

---

### F-023: §6 step 5 ("Internal-component-only check") allows simpler-assumption proceed without naming a default fail-safe

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguity / E — Edge Cases |
| **Severity** | Medium |
| **Section** | §6 step 5 + §6 step 6 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §6 step 5: "Does the ambiguity affect only one section's wording without changing a cross-specialist invariant or interface? If yes → pick simpler option, state assumption inline, proceed." Compared to Role 1 §6 step 5 ("Does the ambiguity affect only structure within a single template section without changing any cross-role interface? If yes → pick the simpler option, state the assumption in a one-line comment, proceed"), Role 2's version drops "in a one-line comment." This is small but matters: the inline-assumption discipline needs explicit length-cap (one line, not paragraph), and Role 1's wording captures it. Role 2 implementer at dispatch time will produce paragraphs of inline assumption justification, blowing the body-length R3 ceiling.

**Evidence.** Role 2 §6 step 5 line 175; Role 1 §6 step 5 line 182.

**Fix.** Restore "in a one-line comment" to §6 step 5. Add to §11.2 (new AP): "I don't justify a §6-step-5 simpler-assumption inline beyond one line. If the justification needs more, the case isn't internal-component-only — escalate to step 2."

---

### F-024: §14 EC-11 mentions "upstream design-doc bibliography mismatch" but its handling cites a §13 audit row that is PROPOSED — deferred to §18 budget. The EC handling is conceptual, not mechanical.

| Field | Value |
|-------|-------|
| **Category** | O — Ordering / D — Downstream Breakage |
| **Severity** | Low |
| **Section** | §14 EC-11 |
| **Resolution** | Defer to follow-up bead |
| **Affected File** | design/health-implementer-design.md |

**Description.** §14 EC-11 handling says: "Audit row (PROPOSED — upstream bibliography sync; deferred per §13 budget — see §18 OQ-budget)". §18 has no OQ titled "OQ-budget" — the closest is OQ-8 ("§13 PROPOSED row count vs §18 budget"). The cross-reference is loose; an implementer chasing the reference would Glob for "OQ-budget" and find nothing.

**Evidence.** §14 EC-11 line 526; §18 lists OQ-1 … OQ-8.

**Fix.** Replace "see §18 OQ-budget" with "see §18 OQ-8". Single-character precision.

---

### F-025: §11.2 anti-pattern 3 wording confuses operator-profile inlining with WIKI.md row content inlining

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguity / L — Language Economy |
| **Severity** | Low |
| **Section** | §11.2 anti-pattern 3 + §12.3 BAD/GOOD |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §11.2 AP3: "I don't auto-load `vault/meta/operator-profile.md` at the implementer layer, and I don't reference Walter's January 2026 issue (or any specific operator state) in the specialist profile body." The first half is about NOT-auto-loading at implementer; the second half is about NOT-inlining into profile body. These are TWO distinct disciplines. An implementer at scale might respect (a) "I won't Read operator-profile.md" but still inline "Walter's January 2026 issue" if a user mentions it in conversation — these are independent surfaces. Sub-finding F-016 captures the WIKI-row-quote sub-surface; F-025 is the broader pattern.

**Evidence.** §11.2 AP3 lines 321–322; §12.3 BAD lines 386–388 (which demonstrates the inlining failure but not the load failure).

**Fix.** Split AP3 into two: AP3a "I don't auto-load `vault/meta/*`" and AP3b "I don't inline operator-specific state into specialist profile bodies, regardless of how I came to know about it." This is a Language Economy fix (current AP3 conflates two disciplines that need separate recognition cues).

---

### F-026: §1 Problem Statement gap #1 phrasing "Goal-agnostic specialist profile authoring at scale" is internally contradictory — specialist profiles ARE goal-anchored by definition

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguity / C — Internal Contradictions |
| **Severity** | Low |
| **Section** | §1 gap #1 |
| **Resolution** | Prevent |
| **Affected File** | design/health-implementer-design.md |

**Description.** §1 numbered gap #1 (line 30): "**Goal-agnostic specialist profile authoring at scale.** The 14 specialists must each conform to the same template variant but carry role-specific prose..." But specialist profiles are NOT goal-agnostic — they carry specialist domain identity, owned wiki paths, refusal classes specific to the specialist's regulatory exposure. The "goal-agnostic" label is borrowed from `feedback_library_research_goal_agnostic.md` (PF-S2-04) and refers to **library entries**, not **specialist profiles**. Conflating the two breeds the same confusion §11.1 PF-S2-04 row is meant to defend against.

**Evidence.** §1 gap #1 line 30; PF-S2-04 + `feedback_library_research_goal_agnostic.md` from project memory.

**Fix.** Rewrite gap #1: "**Template-conformant specialist profile authoring at scale.**" The "goal-agnostic" qualifier is wrong here — what's goal-agnostic is the IDENTICAL block (shared across specialists, no per-operator personalization). The DIFFER block is role-anchored, not goal-agnostic.

---

### F-027: §15.1 says "library-index reference paths resolve" is inherited from `/upgrade-agent` Phase 7 — but the deployed agent has no library-index.md per F-012

| Field | Value |
|-------|-------|
| **Category** | D — Downstream Breakage |
| **Severity** | Medium |
| **Section** | §15.1 + (see F-012 chain) |
| **Resolution** | Prevent — depends on F-012 resolution |
| **Affected File** | design/health-implementer-design.md |

**Description.** §15.1 line 550: "library-index reference paths resolve" is listed among `/upgrade-agent` Phase 7 inherited ACs. But Role 2 §8.1 hedges on whether the implementer authors library-index.md (per F-012). If the implementer chooses not to author it, the inherited AC has nothing to verify — a vacuously-passing AC. If the implementer authors it without a spec, the AC verifies "paths resolve" without anchoring to a content spec, allowing 0-line library-index.md files to pass.

**Evidence.** §15.1 line 550; (intersects with F-012).

**Fix.** Resolve F-012 first. Then either (a) add §15.2 AC-11 "library-index.md exists at `.claude/agents/<specialist-slug>/library-index.md` AND has ≥1 path reference" if implementer authors; OR (b) remove the inherited-AC mention from §15.1 if library-index.md is not Role 2's responsibility.

---

## Summary table

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| Critical | 3 | F-001, F-003, F-004 (note: per AP-R1 self-check, Critical = 3/27 = 11%; well under 40% inflation threshold) |
| High | 7 | F-002, F-005, F-006, F-007, F-008, F-010, F-011 |
| Medium | 9 | F-012, F-013, F-014, F-016, F-017, F-020, F-022, F-023, F-027 |
| Low | 8 | F-009, F-015, F-018, F-019, F-021, F-024, F-025, F-026 |
| **Total** | **27** | |

## Category coverage attestation

The 8 adversarial-review categories per `~/.claude/skills/adversarial-review/SKILL.md` were each walked:

| Category | Findings touching | Walked Probes |
|----------|-------------------|----------------|
| A — Ambiguity | F-003, F-023, F-025, F-026 | Identity sentence ≤40-word ceiling probed; §6 simpler-assumption clause probed; §11.2 AP3 conflation probed |
| E — Edge Cases | F-001, F-004, F-011, F-013, F-014, F-016 | Specialist-Pass-1-absence probed; per-class field enumeration probed; WIKI-row-quote inlining probed |
| C — Internal Contradictions | F-001, F-002, F-006, F-008, F-010, F-015, F-019, F-026 | §13 status-tag count probed; §16 + §13 row 18 cross-table probed; design-doc-fails-own-regex probed |
| R — Broken References | F-005, F-009, F-011, F-017, F-019, F-020, F-022, F-024 | AC-N hyphenation probed; references_role_1_sha vs file path probed; EC-11 OQ-budget alias probed |
| O — Ordering | F-005, F-024 | Design-doc-time vs deployed-agent-time AC ordering probed |
| S — Scope Violations | F-001, F-004, F-007, F-012, F-018, F-022 | scripts/audit ownership probed; library-index.md ownership probed; §13 row 17 branch-hygiene scope probed |
| D — Downstream Breakage | F-008, F-010, F-013, F-016, F-017, F-021, F-024, F-027 | QA-strict tag divergence Roles 3/4 downstream probed; GRADE-regex format-mismatch probed |
| L — Language Economy | F-009, F-015, F-020, F-021, F-025 | AC-N hyphenation probed; ACCEPTED-calibration-pending qualifier probed; AP3 conflation probed |

All 8 categories returned ≥2 findings (minimum per AP-R6); none were category-abdicated. Total = 27 honest findings; no padding to quota.

## Phase 3 Watch List cross-reference

The four watched gaps from `phase-3-watch-list.md` are explicitly mapped:

| Watched Gap | Surfaced? | Finding ID(s) |
|-------------|-----------|---------------|
| WG-1 — Specialist-Pass-1-fallback discipline | **SURFACED** | F-011 |
| WG-2 — library-index.md authoring spec for specialists | **SURFACED** | F-012, F-027 |
| WG-3 — aplus-research target_class enumeration per specialist | **SURFACED** | F-013 |
| WG-4 — Operator-profile field enumeration per specialist class | **SURFACED** | F-014 |

All four watched gaps surfaced independently from substrate + design doc reading. Phase 4 classification can proceed against the watch-list disposition directives.

## Particular-focus-area dispositions

The orchestrator pre-identified 7 surfaces of stress. Disposition:

1. **§13 QA-strict tagging divergence** — load-bearing; cross-doc incoherence (F-008).
2. **PF-S2-06 resolution** — sound. §8.3 forbid-state-mutating-git is a structural defense; the verdict OUT-OF-SCOPE structural is appropriate. NO finding.
3. **§13 row count (claim 18 vs actual 20)** — surfaced (F-002). Consolidation pattern (OQ-1 collective pointer) is adequate to the consolidation goal but the count itself is wrong.
4. **§4.2 OUTBOUND row 2 `scripts/audit-specialist-profile.sh` ownership** — unilateral; needs AQ (F-007).
5. **Identity sentence at ~line 80 ≤40 words / no banned adjectives** — verified clean. Sentence is 31 words; no `expert|experienced|world-class|seasoned|veteran|years of` tokens in the Identity body. NO finding.
6. **§9.1 7-field structured-list spec** — matches Role 1's 7-field convention; appropriate inheritance. NO finding.
7. **AC-2 mechanism glob** — surfaced (F-004). Glob `.claude/agents/*/agent.md` does NOT restrict to specialist slugs; includes foundation roles. The orchestrator brief asked about a glob enumerating suffixes (`*-specialist *-coach ...`) — that wasn't found in the doc; the actual flat glob has a different defect (over-inclusive of foundation roles).

## Coverage check (per SKILL.md §Coverage Check)

- [x] Minimum 2 findings per category — all 8 categories ≥2.
- [x] Every procedure probed with A + O — §6 + §10 + §13 walks completed.
- [x] Every cross-reference probed with R — Role 1 §4 + INVARIANTS + PF log + AGENT_TEMPLATE.md cited paths verified.
- [x] Every section boundary probed with S — §2.2 owned/not-owned cross-checked against Role 1.
- [x] Every stated count probed with C — §13 PROPOSED count, §3.1 Findings count, §3.2 Recommendation count, §11.1 PF count, §15.2 AC count.
- [x] Every procedure's error/empty/boundary paths probed with E — §6 step-5 fallback, §10 substrate-absent, AC-2 glob over-inclusion.
- [x] Every section defining output format probed with D — §9.1 structured-list, §9.2 sample output, §15.2 deployed-agent grep checks.
- [x] Language economy (L) sweep done — AC-N hyphenation, R-N vs RN, calibration-pending qualifier.
- [x] Each finding has severity and resolution assigned.
- [x] Coverage matrix cells filled (every category has ≥2 finding IDs).

No coverage gaps. Review complete.
