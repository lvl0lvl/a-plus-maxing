---
permalink: a-plus-maxing/sessions/session-37
---

---
title: Session 37 — Phase B: clear the two W3/W4 design blockers (5wo + qwj/ko5)
type: session
permalink: a-plus-maxing/sessions/session-37
created: 2026-06-06
status: complete
---

# Session 37 — Phase B of the `/execute-plan` re-entry (2026-06-06)

## What this session was

Phase B of the execute-plan re-entry (after S36 banked the verified baseline). **Design / remediation only — no V1 task built, `/execute-plan` not invoked.** Cleared the two blockers gating the Wave-3/Wave-4 build, each via a dispatched-Architect analysis with the decision-fork surfaced to Walter for adjudication. Both resolved + the Phase-B PR (#60) reviewed and merged.

## `5wo` — `render.emit` return contract (option b)

- **Conflict (real, embedded in the T2 recipe):** ADR-0004-T2 (`yo6`, W4) requires an over-cap render to paginate into ≥2 output files (AC-2), while the published primitive is `emit(template, store_read) -> Path` (single) and the ADR-0004-T1 Change-control clause forbids changing the path-return contract without Architect review. The recipe simultaneously claimed "≥2 returned paths" and "does not modify a shared interface."
- **Architect arbitration** (full profile inlined): fork **(a)** widen `emit` return to `Path | list[Path]` vs **(b)** caller-orchestrated pagination above a single-`Path` `emit`. Recommended (b): zero built-code blast radius (the BUILT `generate.run`/T3 + 8+ built tests assert a single `Path`; (a) breaks all of them), faithful to ADR-0004 OQ-1 ("pagination = multiple single-file artifacts").
- **Walter adjudicated: (b).** Resolution: 2 `[AMENDED]` reconciliations in `docs/task-plan/ADR-0004-T2.md` (the "split returns the list" line re-attributed to the caller-side render path; the "does not modify a shared interface" claim grounded). `emit -> Path` preserved verbatim. Decision recorded at `vault/decisions/2026-06-06-render-emit-pagination-caller-orchestrated.md`. `5wo` CLOSED.

## `qwj` + `ko5` — PII-free-trunk policy (option iii)

- **Premise corrected (PF-S6-01):** the bead claimed `pii_scan.py` hard-codes the operator name, but commit `179d154` had already externalized the identity tokens to the gitignored `vault/meta/operator-identity.txt` (`scan(tracked_files, identity_config=...)`, fresh clone → empty identity set). Verified before acting — **no `pii_scan.py` change needed.** The real remaining question was the policy.
- **Policy fork:** on the operator's machine `scan` over tracked files returns ~1043 hits/159 files (the operator name in governance/session/design prose). Options — (i) scope the hook to data-bearing paths; (ii) strict hook + sanitize ~150 files at clone-init; (iii) ratify "PII-free = health-DATA-free" + scope (clarify ADR-0005, resolves `ko5`).
- **Walter adjudicated: (iii).** Architect drafted the amendment text (read-only). Resolution: `docs/adr/ADR-0005-...md` Decision + Validation clarified (PII-free trunk = operator-health-DATA-free; operator name in prose = accepted provenance; identity check scoped to data-bearing paths, agnostic structural + `@gmail.com` contact patterns trunk-wide); `docs/task-plan/ADR-0005-T1.md` (the unbuilt `xlu` hook recipe) amended so the hook builds the SCOPED two-call check (NOT block-everything). `qwj` CLOSED; `ko5` CLOSED (ratifies the vault knowledge-graph as the tracked PII-free trunk; closes the S1 "vault not in git" deferral).
- **Open sub-decision (noted, not blocking):** the `@gmail.com` contact pattern runs trunk-wide, so a tracked author-byline email would be flagged. Architect recommended keeping this protective default (no carve-out); reversible later via a narrow allowlist. No tracked byline emails exist today (only a test fixture).

## Review + merge (PR #60)

Docs-subset `/review-pr` (Code Quality + Contracts + Historical Context, all by registered profile-carrying types). 9 findings after dedup → blind triage:
- **4 LEGITIMATE, fixed + blind-verified:** T1 (the two `[AMENDED]` markers were wrapped in an outer backtick span garbling Markdown), T2 (the `xlu` agnostic-scan call said "empty `identity_config`" — `""` → `Path(".")` exists → `IsADirectoryError` → fail-closed always-DENY; only a non-existent path works), T4 (un-amended AC lines still framed the list-return as `render.emit`'s own), T5 (ADR-0005 `[VERIFIED]` Validation lines contradicted the PRD NFR-2 "name" token → reconciled + PRD-align beaded).
- **2 beaded:** T5 PRD-alignment (out-of-scope PRD edit, P3), T9 changelog-v1.1 gap (pre-existing/deferred, P3).
- **3 no-action with cited evidence:** T3 (ADR-0007-T2 carries no actual contradiction under option b), T7 (number figures explicitly approximate), T8 (the run-on amendment's inline detail is load-bearing — the recipe executor is told not to read ADRs).
- **0 suppressed** (PF-S26-01). The layered review caught a real defect the orchestrator introduced (T2 — faithfully copied the Architect's "empty/absent" phrasing).
- Suite 120/2 pre+post. Rebase-merged at `c22a0a3`.

## State after S37

- Build 9/18 (unchanged — Phase B built no task). **W3 (`br1`+`xlu`) and W4 (`yo6`) are now unblocked.**
- Next (S38) = Phase C: `/execute-plan` in WAVE mode, Wave 3 — read its SKILL.md in full first; write a `v1-build` scope contract citing W3 + attesting the W2→W3 checkpoint.
- Beads: `5wo`/`qwj`/`ko5` CLOSED; T5-PRD-align + T9-changelog filed (P3).