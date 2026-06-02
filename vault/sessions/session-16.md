---
title: Session 16 — gate-hardening (cross-role contract reconciliation + scripts/audit-specialist-profile.sh)
type: session-note
session: S16
date: 2026-05-29
status: complete
permalink: a-plus-maxing/sessions/session-16
---

# Session 16 (2026-05-29)

Pre-Pass-3 gate-hardening (Path 3, user-chosen over launch-parallel-build / build-one-pilot). Foundation pipeline complete and unchanged (4/4 deployed, Session B debt 0); no specialist built or deployed. The session reconciled the three cross-role contract literals the specialist deploy-gate keys on, then built + tested that gate so the 14 Pass-3 specialists inherit consistent, mechanically-enforced contracts.

## What happened

**Session open (PF-S13-01 falsification window — HELD).** Every Start-Protocol step run with real output: HANDOFF read in full (paged past both truncations, 1083 lines), INVARIANTS / process-failures / landmarks read, `git status` + log, test baseline RUN (not recited), deployed-agents-vs-design-docs set difference computed via `ls` (∅ — debt 0). Scope contract written + user-confirmed before any work. No AskUserQuestion widget.

**`ams` closed at open (overtaken-by-events).** PF-S12-01 session-b-debt machinery: fix #1 (CLAUDE.md Roster B status field) already shipped via S13–S16 contracts; #2/#3/#5 moot (foundation loop closed, debt 0; the Pass-3 parallel-build model runs research→design→upgrade→PR in one builder session, so no design-doc-Final-to-deploy gap can accumulate); #4 absorbed into `coordination/PROTOCOL.md`. Analysis stays in `memory/process-failures.md` PF-S12-01.

**AC1 — `z8i` (XR-004) override-acknowledgment literal canonicalized.** The pre-Role-7 override-acknowledgment phrase was stated three ways across Roles 1/3/4 — a latent literal-grep gate mismatch (a Role-1/3-faithful specialist would fail Role 4's exact-phrase grep). Made Role 4 §13 row 7 the canonical definer of `"operator is overriding a safety block"`; Role 1 §13 row 6 + EC-10 (handling + test stimulus) and Role 3 §13 row 11 now anchor to that exact string. `rg`: one canonical literal, zero divergent phrasings. Annotated `XR-004 / bead z8i`.

**AC2 — `7m1` (XR-003) OUTBOUND row 8 scope.** Role 1 §4 OUTBOUND row 8 scoped Role 4 to only `researching→planned` compound transitions, understating Role 4's actual immediate use (gating specialist `agent.md` profiles + wiki entries pre-deployment, per Role 4 §1 + §4.4 row 1). Generalized the row to cover both surfaces.

**AC3 — `9u6` (XR-001) 7-class → 8-class.** All 7 residual "7-class" taxonomy references in the Role 1 design doc corrected to 8-class (incl. the §12 Negative-Example block, whose GOOD example asserted a false fact about the canonical 8-class Finding 5). Canonical enumeration §2.2 item 3 (incl. `AUTHORITY_FRAMING_BYPASS`). Deployed Role 1 agent.md was already correct — this was canonical-doc self-consistency.

**AC4 + AC5 — the gate (`3y6`).** `scripts/audit-specialist-profile.sh` implements the Role 1/2 §13 audit interface — 25 sub-checks (15 base rows + 10 decimal extensions) consuming a deployed `.claude/agents/<slug>/agent.md` (+ `library-index.md`). Sources `scripts/lib/audit-helpers.sh`; BLOCK checks → exit 1, WARN checks → info (no exit-code change); dependency-gated checks (IDENTICAL/Jaccard corpus, denylist, operator-profile schema) degrade to skip-with-info rather than false-pass. **AQ-002 mention-aware:** the voice-register + denylist checks strip fenced code blocks and inline-code spans before counting banned-modal tokens, so a faithful profile that MENTIONS a banned token in a Negative-Example BAD block or an inline-code regex literal does not false-positive. `scripts/tests/test_audit_specialist_profile.sh` 21/21: a GOOD fixture passing all BLOCK checks, one negative per BLOCK row, and the AQ-002 mention/control pair (banned token inside a code span does NOT block; the same token in prose DOES). 7 existing suites still green.

Two self-caught defects during the build (the build-then-verify mechanism working, nothing escaped): crash-test surfaced a refusal-class false-positive (all-caps enum tokens flagged as non-taxonomy classes) + a spec-misaligned WARN-vs-BLOCK on row 7 — fixed before writing tests; the test suite's first run caught a case-sensitive routing-cue grep + a self-referential-`local` bash gotcha — fixed.

**Discovered + beaded (not fixed — frozen doc, out of scope):** `f2j` (XR-S16-01) — Role 1 §13.5 EC-10 detects Role-7-deployed via the skills_library path while Role 4 BC-1 uses the canonical project-local `.claude/agents/` path. Latent until Role 7 deploys.

## Drift checks
- **Task drift:** 6/6 ACs PASS. One in-scope judgment beyond literal bead text (fixed the §12 illustrative "7-class" sites that 9u6 said "may stay", because the GOOD example asserted a false fact) — flagged in the bead close. `ams` closed at open (flagged + confirmed). No silent drift.
- **Architecture drift:** no invariant degraded; AP-CROSS-ROLE-CONTRACT-DRIFT REDUCED (3 literals reconciled). Audit script additive (step-8.5 wiring deferred to first-specialist-deploy). Frozen docs edited under bead authorization only; deployed agents untouched. INV-BRANCH-NOT-MAIN held.
- **Vision drift:** none. The specialist deploy-gate is mechanized + tested and its contracts internally consistent.

## PF attestation
S16 close (2026-05-29): No new PF-class entries. PF-S13-01 HELD (full-protocol open). PF-S6-01 HELD (verified bead claims + the XR-S16-01 defect against source docs before acting). PF-S3-01 N/A (no dispatch). See HANDOFF S16 close note for the non-promoted observations.

## Beads
Closed: `ams`, `z8i`, `7m1`, `9u6`. Advanced → OPEN P2: `3y6` (residual: per-WARN-row negatives; corpus/denylist/schema-gated checks; step-8.5 wiring). New: `f2j` (XR-S16-01, P3).
