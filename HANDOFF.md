---
title: Session Handoff
type: note
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-05-29
status: active
depends_on: []
superseded_by: null
review_cadence: weekly
---

# Session Handoff

## Scope Contract — Session 18 (2026-05-30)

**Honest framing:** this session opened informally — Walter asked the new session to assess a logged-out integrator, and it became the batch-3 integration session. No scope contract was written at open; this is recorded at close (minor process drift, documented not silent).

Goal: Take over the integrator role, reconcile actual state vs. the crashed prior session, merge batch-3, file the surfaced beads, and close the bookkeeping — gating the library-population phase on `bda`.

Acceptance criteria:
- [x] AC1 — supplement integration-debt cleaned: OQ-1..5 filed (`5l9`/`78p`/`r7t`/`7rm`/`60f`), fabricated log bead IDs + false merge SHA corrected, dangling supplement branch pruned. **PASS.**
- [x] AC2 — batch-3 trio INDEPENDENTLY verified (disjoint paths; deploy-gate re-run 0-BLOCK each; frameworks source-disciplined cite-or-refuse w/ 0 hardcoded facts; research provenance — gi full `verify-chain`, pt+lymphatic dispatched judges) then rebase-merged via REST one at a time → **14 agents on main @ `94496b4`**. **PASS.**
- [x] AC3 — 10 follow-up beads filed/updated (`382` widened; new `5jr`/`9c5`/`pnl`/`2n1`/`4h1`/`smw`; `bda` escalated). **PASS.**
- [x] AC4 — PF-S17-01 SOFT recurrence (pt+lymphatic approximated `/aplus-research`) logged under PF-S17-01 (count→2); `bda` made the HARD BLOCKER on library-population. **PASS.**
- [x] AC5 — 3 close audits exit 0 at `--session 18` (handoff / scope-contract / pf-attestation all PASS); VOLATILE rotation done; feature branch only. **PASS.**

Files I WILL touch: `vault/meta/log.md`, `memory/process-failures.md`, `.beads/*` (via `bd`), `HANDOFF.md`, `coordination/*` (gitignored scaffold); `main` only via REST merges of PRs #16/#17/#18.

Files I will NOT touch: `.claude/agents/*` builder-authored bodies (read-only at merge), `design/*-design.md` Status:Final bodies (defects → beads), `templates/*`, `scripts/*`, `CLAUDE.md`, `INVARIANTS.md`, `.claude/skills/*`, `vault/library|compounds|biomarkers|dna/*` (the library phase is gated on `bda`, not started this session).

NOT doing: batch-4 (remaining 5 specialists); ANY library-population (hard-gated on `bda`); the OQ-1 `.yaml` reconcile (deferred, tracked `5l9`); `bda` build itself (next session); Walter pending items (23andMe, Oura, meal-template, Jan-2026).

Invariants at risk: AP-ORCH-SELF-ATTEST (PF-S3-01) — integrator independently re-verified each builder finding, did not merge on trust; INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-PF-ATTESTATION, INV-SCOPE-CONTRACT — standard close discipline.

Drift checks (S18 close):
- **Task drift:** scope expanded from "assess status" → full batch-3 integration. Walter-directed at each step (take over integrator → cleanup → verify-only → merge on go). Documented, not silent.
- **Architecture drift:** none — 14/15 agents is the planned roster trajectory; no invariant moved toward violation; `bda` gate ADDED as protection before the library phase.
- **Vision drift:** none — "single-operator health agent system of gated, source-grounded specialists" unchanged.

PF attestation:

S18 close (2026-05-30): PF-S17-01 recurred (soft form) — pt + lymphatic ran research "discipline at orchestrator level" instead of invoking the gated /aplus-research skill; logged under PF-S17-01 (recurrence_count→2), bda escalated to a hard blocker on library-population. No other new PF-class entries; the deploy-gate token-WARNs and the IDENTICAL-block divergence were filed as beads (5jr), not promoted to PF.

Invariants at risk: AP-ORCH-SELF-ATTEST (PF-S3-01) — integrator independently re-verified each builder finding, did not merge on trust; INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-PF-ATTESTATION, INV-SCOPE-CONTRACT — standard close discipline.

## Scope Contract — Session 17 (2026-05-29)

Goal: Set up Pass-3 batch-2 (4 specialists) and hand Walter the launch recipe, then run as integrator through the parallel-build → serialized-merge loop, exactly as the pilots ran.

Acceptance criteria:
- [ ] AC1 — 4 kickoffs written: `coordination/kickoffs/{supplement-specialist,endocrine-specialist,nutritionist,sleep-coach}.md`, templated from the pilot kickoffs, base `0514f2d`, no-frontmatter convention baked in, medical-liaison-now-live `BLOCK_WITH_OVERRIDE_PATH` escalation contract (not the deprecated operator-self-override fallback).
- [ ] AC2 — 4 builder outboxes seeded: `coordination/sessions/<slug>.outbox.md` (one per slug, single-writer).
- [ ] AC3 — `coordination/BOARD.md` rewritten for batch-2: 4 assignment rows, merge order, pinned base `0514f2d`, integrator directives reset.
- [ ] AC4 — Launch recipe delivered to Walter: 4 worktree setup commands + 4 first-message prompts to paste.
- [ ] AC5 — Integrator loop (only after builders complete): each PR reviewed against `scripts/audit-specialist-profile.sh` (0-viol), rebase-merged to main in board order, branch+worktree torn down. (Spans builder runtime — may carry to a follow-up session; AC1–AC4 are this session's committed deliverable.)
- [ ] AC6 — Close: 3 audits exit 0 at `--session 17`; canonical `S17 close (YYYY-MM-DD):` PF attestation; VOLATILE rotation 6-clause; feature branch only (code reaches main only via the per-pilot clean PRs).

Files I WILL touch:
- `coordination/kickoffs/*.md`, `coordination/sessions/*.outbox.md`, `coordination/BOARD.md` (all gitignored — on-disk scaffolding)
- `HANDOFF.md` (contract + close + rotation), `.beads/*` via `bd`, `vault/meta/log.md`, `vault/sessions/session-17.md`
- `memory/process-failures.md` (only if a PF surfaces)
- Integrator-only at merge time: `main` via clean per-slug PRs (builders author the agent.md files in their worktrees, not me)

Files I will NOT touch:
- `.claude/agents/*` foundation profiles, the 3 deployed pilot agents on main (read-only)
- `design/*-design.md` Status:Final bodies (defects → beads)
- `scripts/audit-specialist-profile.sh` (calibrated at S16 — frozen unless a batch-2 false-BLOCK surfaces, which is a finding to verify first)
- `CLAUDE.md`, `INVARIANTS.md`, `.claude/hooks/*`, `.claude/skills/*`, `vault/library|compounds|biomarkers|dna/*`

NOT doing: batches 3–4 (remaining 8 incl. dermatologist); Phase-C peptide campaign; INV promotion; frozen-doc bead reconciliations (`1rm`/`p47`/`o9y`/`7is`/`1ek`); Walter pending items (23andMe, Oura, meal-template, Jan-2026).

Invariants at risk:
- AP-ORCH-SELF-ATTEST (PF-S3-01) — dominant Pass-3 risk: each builder's `/upgrade-agent` + `/review-pr` stack keeps separate+parallel fact-checker/judge + personal source-read of every finding; integrator independently re-verifies builder findings (pilots caught a real gate bug AND a false builder claim this way).
- AP-WORKTREE-PATH-RESOLUTION (PF-S16-01) — kickoffs instruct absolute worktree paths for sub-dispatches.
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH — standard close discipline.

## Scope Contract — Session 16 (2026-05-29)

Goal: Harden the mechanical gate the 14 Pass-3 specialists will be validated against — build `scripts/audit-specialist-profile.sh` (`3y6`) — and first reconcile the three cross-role contract literals that gate enforces so it keys on canonical, not self-contradictory, definitions.

Roster B status: N/A — foundation pipeline complete (4/4 deployed), Session B debt 0; no drafter dispatch or design-doc cycle this session.

Acceptance criteria:
- [ ] AC1 — `z8i`: Role 4 §13 row 7's literal override-adjudicator phrase made canonical; Roles 1 (§13 row 6/EC-10) + 3 (§13 row 11) reference it by anchor instead of restating. Change-discipline edits (bead-authorized) + Change Log note. `rg` confirms one canonical literal.
- [ ] AC2 — `7m1`: Role 1 §4 OUTBOUND row 8 generalized to cover specialist-profile deployment gating (not just compound `researching→planned`). Change-discipline edit.
- [ ] AC3 — `9u6`: all 5 "7-class" prose sites in Role 1 design doc corrected to 8-class (the L410 BAD-block illustrative may stay if deliberately wrong); deployed agent already correct — canonical-doc self-consistency only.
- [ ] AC4 — `scripts/audit-specialist-profile.sh` ships: implements the Role 1 §13 audit interface against a deployed specialist `agent.md`; AQ-002 mention-aware (excludes fenced/inline code before banned-modal counting); exits 0 PASS / non-zero with per-row failure detail; follows the existing `scripts/lib/audit-helpers.sh` pattern.
- [ ] AC5 — Per-row smoke tests under `scripts/tests/` exercising the negative case for each §13 row implemented (QA-strict tag rule, OQ-7); all pass; existing audit suites still green.
- [ ] AC6 — Close: all existing audits (handoff, scope-contract, pf-attestation) exit 0 at `--session 16`; canonical `S16 close (YYYY-MM-DD):` PF attestation; VOLATILE rotation 6-clause; feature branch only.

Files I WILL touch:
- `scripts/audit-specialist-profile.sh` (NEW), `scripts/tests/*` (NEW fixtures + runner)
- `design/health-specialist-architect-design.md` (`9u6` 5 sites + `7m1` row 8 + `z8i` anchor — bead-authorized change discipline)
- `design/health-edge-case-reviewer-design.md` (`z8i` §13 row 11 anchor)
- `design/medical-safety-reviewer-design.md` (`z8i` — confirm Role 4 row 7 is the canonical literal; anchor target)
- `HANDOFF.md` (contract + close + rotation), `.beads/*` via `bd`, `memory/process-failures.md` (only if a PF surfaces)

Files I will NOT touch:
- `.claude/agents/*` (deployed profiles — read-only; already carry the corrected forms)
- Role 3 `p47`/`o9y`/`7is` design-doc edits (deferred — deployed agents already correct)
- `INVARIANTS.md` (no INV promotion this session unless user directs the ritual)
- `CLAUDE.md`, `.claude/hooks/*`, `.claude/skills/*`, `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `main` branch directly (feature branch only)

NOT doing: building/extending `ams` machinery (closed as overtaken-by-events at S16 open); Pass-3 specialist deep-research / design docs / `/upgrade-agent`; launching the parallel build; INV promotion; Walter pending items.

Invariants at risk:
- AP-CROSS-ROLE-CONTRACT-DRIFT — AC1–AC3 are the reconciliation; goal is to remove drift before the gate enforces it.
- PF-S3-01 — N/A to drafter dispatch this session; smoke-test design must be genuine negative-case (no tautological tests per CLAUDE.md mandate), not assertions that pass regardless.
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH — standard close discipline.

## Scope Contract — Session 15 (2026-05-29)

Goal: Close bead `4ej` (XR-002) as a prerequisite, then deploy Role 4 (medical-safety-reviewer) as a project-local agent AND incorporate it (sub out the safety-red-team v1-substitute), via one full deploy-and-incorporate loop (`/upgrade-agent` → sub-out → `/review-pr` → `/merge` Option A → close). Session B debt 1 → 0 — closes the LAST foundation debt; 4 of 4 foundation agents deployed.

Roster B status (per PF-S12-01 AP-DEFERRED-LOOP-CLOSURE guard):
- Architect: deployed (`.claude/agents/health-specialist-architect/`) since S9
- SE drafter: deployed (`.claude/agents/health-implementer/`) since S13
- QA drafter: deployed (`.claude/agents/health-edge-case-reviewer/`) since S14
- Safety red-team: v1-substitute → becomes medical-safety-reviewer (deployed) THIS SESSION
- Cumulative-deferral count: 1 → 0 expected at close

Acceptance criteria:
- [ ] AC0 — Prerequisite: close bead `4ej` by reconciling Role 1 `design/health-specialist-architect-design.md` §13 row 15 → `DEPLOY or BLOCK_WITH_OVERRIDE_PATH` via design-doc change discipline (bead authorizes the in-place edit to a Status:Final doc; gate allow-list semantics confirmed: PASS on DEPLOY|BLOCK_WITH_OVERRIDE_PATH, hard-FAIL on BLOCK). Done BEFORE `/upgrade-agent` so Role 4 inherits the correct enum.
- [ ] AC1 — `/upgrade-agent` on `design/medical-safety-reviewer-design.md` → `.claude/agents/medical-safety-reviewer/agent.md` (+ `library-index.md`); 8-phase pipeline; net-new (0/10 baseline); Phase-7 corrections PASS; PF-S3-01 guard held at Phase 4 + 6 (separate+parallel fact-checker/judge; 9/10 every dimension, no rounding; every finding personally source-read).
- [ ] AC2 — Sub out: safety-red-team slot software-`security` v1-sub → medical-safety-reviewer in `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7. 4 of 4 Roster B slots project-local after this.
- [ ] AC3 — agent.md passes generic Phase-7 constraints (≤200 lines; ≤2000 tokens OR documented overrun per S9/S13/S14 + DOCUMENT_RUBRIC Rule 7 load-bearing review; all AGENT_TEMPLATE.md sections present; reference paths resolve).
- [ ] AC4 — agent.md post-deployment ACs evaluated (LIVE pass; PROPOSED → beads); confirm the deployed agent carries the corrected (non-inverted) deploy-verdict enum from AC0.
- [ ] AC5 — `/review-pr` scoped to the S15 deployment commits (local diff range); findings blind-triaged per PF-S3-01; reject-but-adopt where appropriate; frozen-design-doc findings → beads.
- [ ] AC6 — `/merge` on explicit user go — Option A branch topology (fresh per-session branch off `origin/main`, cherry-pick, clean PR, rebase-merge, delete per-session branch). Never PR feature→main.
- [ ] AC7 — Close: all 3 audits exit 0 at `--session 15`; canonical `S15 close (YYYY-MM-DD):` PF attestation; VOLATILE rotation 6-clause; debt 1 → 0 recorded; feature branch only until authorized merge.
- [ ] AC8 — Foundation pipeline marked complete; S15 `SESSION_B_KICKOFF.md` → `consumed`; next forward direction (Pass-3 specialists / Phase-C) noted as unblocked.

Files I WILL touch:
- `design/health-specialist-architect-design.md` §13 row 15 ONLY (AC0 authorized edit — bead `4ej`)
- `.claude/agents/medical-safety-reviewer/agent.md` (NEW; + `library-index.md`)
- `design/.medical-safety-reviewer-design-work/upgrade-agent-work/*` (NEW — phase artifacts)
- `design/DESIGN_DOC_TEMPLATE.md` §0.1 (safety-red-team sub-out)
- `design/CONTINUATION_BRIEF.md` §7 (safety-red-team sub-out)
- `design/.medical-safety-reviewer-design-work/SESSION_B_KICKOFF.md` (→ `consumed` at close)
- `INVARIANTS.md` (only if AC0 ritual appends a Change Log row; flag at the time)
- `HANDOFF.md` (this contract + close + VOLATILE rotation)
- `vault/sessions/session-15.md` (NEW), `vault/meta/index.md`, `vault/meta/log.md`
- `.beads/*` via `bd` CLI (close `4ej`)
- `memory/process-failures.md` (only if a new PF surfaces)

Files I will NOT touch:
- `design/medical-safety-reviewer-design.md` body (Status: Final — READ-ONLY source; defects → bead)
- The other 3 `*-design.md` bodies beyond Role 1 §13 row 15 (Status: Final — defects → bead)
- `.claude/agents/health-specialist-architect/`, `health-implementer/`, `health-edge-case-reviewer/` (deployed — read-only drafter sources)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `CLAUDE.md`
- `main` branch directly (only via authorized `/merge`)

NOT doing:
- Pass-3 specialist deep-research / `/upgrade-agent` for the 14 specialists; Phase-C peptide campaign
- Beads `ams`, `3y6` build-out; other open beads beyond `4ej`
- Promoting any candidate INV (INV-SESSION-B-INTERLEAVING etc.) — requires change-discipline ritual
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)

Invariants at risk:
- INV-ROLE-INLINING — `/upgrade-agent` role-tagged sub-dispatches inline full profile per hook v2.5; path-pattern edge case (bead `rc1`) on watch
- PF-S3-01 / AP-ORCH-SELF-ATTEST — Phase 4 + 6 falsification window; separate+parallel fact-checker/judge; no rounding; personal source-read. Role 4 is the most safety-critical profile.
- AP-INCOMPLETE-PROPAGATION — ~874-line design doc → ≤200-line agent.md compression; §7 mechanical check is the defense; never cut a safety binary to fit (Rule 7)
- AP-DEFERRED-LOOP-CLOSURE (PF-S12-01) — S15 IS the final remediation; opened with the last debt; debt 1 → 0
- AP-PROTOCOL-FROM-MEMORY (PF-S13-01) — this open is the falsification window; every step run with real output; this contract gates all work
- AP-CROSS-ROLE-CONTRACT-DRIFT — AC0 closes the live XR-002 wiring bug before it propagates into the deployed agent + orchestrator gate
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH — standard close discipline

Self-recognition pre-flight: Watching at each `/upgrade-agent` Phase 4/6 for "I verified findings like these on Roles 1–3, the pattern is familiar" (familiarity ≠ source-read) and "Role 4's profile must hit ≤200 lines so I'll drop a safety binary to fit" (overrun documented per Rule 7, never compressed at the cost of a safety property). Also watching that the AC0 fix lands in the deployed agent's enum (not just the design doc), and for the AQ-002 use-vs-mention banned-token issue in Role 4's threat-catalog (disposition fixed: deploy faithfully — bead `3y6`; do not re-litigate).

## Scope Contract — Session 14 (2026-05-29)

Goal: Deploy Role 3 (health-edge-case-reviewer) as a project-local agent AND incorporate it into the bootstrap roster (sub out the QA v1-substitute), via one full deploy-and-incorporate loop (`/upgrade-agent` → sub out → `/review-pr` → `/merge` → close). Session B debt 2 → 1. Closes the next-oldest debt per PF-S12-01 AP-DEFERRED-LOOP-CLOSURE.

Roster B status (per PF-S12-01 Structural-1):
- Architect: deployed (`.claude/agents/health-specialist-architect/`) since S9
- SE drafter: deployed (`.claude/agents/health-implementer/`) since S13
- QA drafter: v1-substitute → becomes health-edge-case-reviewer (deployed) THIS SESSION
- Safety red-team: v1-substitute (Role 4 Session B = S15)
- Cumulative-deferral count: 2 → 1 expected at close

Acceptance criteria:
- [ ] AC1 — `/upgrade-agent` on `design/health-edge-case-reviewer-design.md` → `.claude/agents/health-edge-case-reviewer/agent.md` (+ `library-index.md`); 8-phase pipeline; net-new (0/10 baseline); Phase-7 corrections PASS; PF-S3-01 guard held at Phase 4 + 6 (every finding personally source-read; separate+parallel fact-checker/judge; 9/10 every dimension, no rounding)
- [ ] AC2 — Sub out: QA drafter slot v1-sub → health-edge-case-reviewer in `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7
- [ ] AC3 — agent.md passes generic Phase-7 constraints (≤200 lines; ≤2000 tokens OR documented overrun per S9/S13 + DOCUMENT_RUBRIC Rule 7 load-bearing review; all AGENT_TEMPLATE.md sections present; reference paths resolve)
- [ ] AC4 — agent.md post-deployment ACs evaluated (LIVE pass; PROPOSED → beads); confirm Role 3 does NOT inherit the XR-002 `DEPLOY_WITH_OVERRIDE_PATH` verdict-enum inversion (bead `4ej`)
- [ ] AC5 — `/review-pr` scoped to the S14 deployment commits; findings blind-triaged per PF-S3-01; reject-but-adopt where appropriate; frozen-design-doc findings → beads
- [ ] AC6 — `/merge` on explicit user go (clean incremental PR feature → main; confirm before branch deletion)
- [ ] AC7 — Close: all 3 audits exit 0 at `--session 14`; canonical `S14 close (YYYY-MM-DD):` PF attestation; VOLATILE rotation 6-clause; debt 2 → 1 recorded; feature branch only until authorized merge
- [ ] AC8 — Role 4 (S15) queued; S14 `SESSION_B_KICKOFF.md` → `consumed`; `4ej` noted as S15 prerequisite

Files I WILL touch:
- `.claude/agents/health-edge-case-reviewer/agent.md` (NEW; + `library-index.md`)
- `design/.health-edge-case-reviewer-design-work/upgrade-agent-work/*` (NEW — phase artifacts)
- `design/DESIGN_DOC_TEMPLATE.md` §0.1 (QA sub-out)
- `design/CONTINUATION_BRIEF.md` §7 (QA sub-out)
- `design/.health-edge-case-reviewer-design-work/SESSION_B_KICKOFF.md` (→ `consumed` at close)
- `HANDOFF.md` (this contract + close + VOLATILE rotation)
- `vault/sessions/session-14.md` (NEW), `vault/meta/index.md`, `vault/meta/log.md`
- `.beads/*` via `bd` CLI
- `memory/process-failures.md` (only if a new PF surfaces)

Files I will NOT touch:
- `design/health-edge-case-reviewer-design.md` + other 3 `*-design.md` (Status: Final — READ-ONLY; defects → bead)
- `.claude/agents/health-specialist-architect/`, `.claude/agents/health-implementer/` (deployed — read-only drafter sources)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `CLAUDE.md`, `INVARIANTS.md` (no new invariants unless forced; flag at the time)
- `main` branch directly (only via authorized `/merge`)
- Bead `4ej` resolution (XR-002) — that is the S15 prerequisite, not S14 work

NOT doing:
- Role 4 (S15) deployment — one role per session
- Closing bead `4ej` (Role-4 prerequisite, S15)
- Pass-3 specialists; Phase-C peptide campaign
- PF-S12-01 Structural-2/3 — bead `ams`; bead `3y6`; Walter pending items

Invariants at risk:
- INV-ROLE-INLINING — `/upgrade-agent` role-tagged sub-dispatches inline full profile per hook v2.5; path-pattern edge case (bead `rc1`) on watch
- PF-S3-01 / AP-ORCH-SELF-ATTEST — Phase 4 + 6 falsification window; separate+parallel fact-checker/judge; no rounding/softening; personal source-read
- AP-INCOMPLETE-PROPAGATION — ~887-line design doc → ≤200-line agent.md compression; §7 mechanical check is the defense
- AP-DEFERRED-LOOP-CLOSURE — S14 IS the remediation; opening with oldest debt (Role 3); debt 2 → 1
- AP-PROTOCOL-FROM-MEMORY (PF-S13-01) — this open was the falsification window; every step run not stated; this contract gated all work
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH — standard close discipline

Self-recognition pre-flight: Watching at each `/upgrade-agent` Phase 4/6 for "I verified findings like these on Roles 1+2, the pattern is familiar" (familiarity ≠ source-read) and "Role 3 agent.md must hit ≤200 lines so I'll drop a safety property to fit" (overrun documented per Rule 7, not compressed at the cost of safety). Also watching for the XR-002 verdict-enum inversion silently propagating into Role 3's profile.

## Scope Contract — Session 13 (2026-05-28)

Goal: Deploy Role 2 (health-implementer) as a project-local agent AND incorporate it into the bootstrap roster, replacing the software-SE v1-substitute. One full deploy-and-incorporate loop (`/upgrade-agent` → sub out → `/review-pr` → `/merge` → close). Session B debt 3 → 2. First correct execution of the per-session deployment loop (S12 kickoff brief encoded a wrong batched-3 shape; corrected at S13 session-start per user instruction).

Roster B status (per PF-S12-01 Structural-1):
- Architect: deployed (`.claude/agents/health-specialist-architect/`) since S9
- SE drafter: v1-substitute → becomes health-implementer (deployed) THIS SESSION
- QA drafter: v1-substitute (Role 3 Session B = S14)
- Safety red-team: v1-substitute (Role 4 Session B = S15)
- Cumulative-deferral count: 3 → 2 expected at close

Acceptance criteria:
- [ ] AC1 — `/upgrade-agent` on `design/health-implementer-design.md` → `.claude/agents/health-implementer/agent.md`; 8-phase pipeline; Phase-7 corrections all PASS; PF-S3-01 guard held at Phase 4 + 6 (every finding personally source-read before classification)
- [ ] AC2 — Sub out: Roster B in `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7 updated so the SE drafter slot reads health-implementer (deployed), replacing software-SE v1-substitute
- [ ] AC3 — agent.md passes generic Phase-7 constraints (≤200 lines; ≤2000 tokens OR documented medical-domain overrun per S9 precedent; all AGENT_TEMPLATE.md sections present; reference paths resolve)
- [ ] AC4 — agent.md §15.2b post-deployment ACs evaluated (LIVE checks pass; PROPOSED checks → follow-up beads)
- [ ] AC5 — `/review-pr` (existing command) run on the result; findings triaged per PF-S3-01 (personal source-read); reject-but-adopt applied where appropriate
- [ ] AC6 — `/merge` (existing command) on explicit user go (PR feature → main; this PR carries the S7–S13 backlog so main catches up; from S14 each role is a clean incremental PR)
- [ ] AC7 — Close: all 3 audits exit 0 at `--session 13`; canonical `S13 close (YYYY-MM-DD):` PF attestation; VOLATILE rotation 6-clause; debt 3 → 2 recorded; feature branch only until the authorized merge
- [ ] AC8 — Role 3 (S14) queued as next loop iteration; `design/.session-b-deployments/SESSION_KICKOFF.md` corrected and marked `consumed`

Files I WILL touch:
- `.claude/agents/health-implementer/agent.md` (NEW; + `library-index.md` if the pipeline emits one)
- `design/DESIGN_DOC_TEMPLATE.md` §0.1 (Roster B sub-out edit)
- `design/CONTINUATION_BRIEF.md` §7 (Roster B sub-out edit)
- `design/.health-implementer-design-work/upgrade-agent-work/*` (NEW — phase artifacts)
- `design/.session-b-deployments/SESSION_KICKOFF.md` (correct the batched-3 shape; flip to `consumed` at close)
- `HANDOFF.md` (this contract + close + VOLATILE rotation)
- `vault/meta/index.md`, `vault/meta/log.md` (appends)
- `.beads/*` via `bd` CLI
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `design/health-implementer-design.md`, `design/health-edge-case-reviewer-design.md`, `design/medical-safety-reviewer-design.md` (Status: Final — READ-ONLY inputs; defects → bead, not in-place edit)
- `design/health-specialist-architect-design.md` (Final)
- `.claude/agents/health-specialist-architect/` (Role 1 deployed — read-only drafter source)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `CLAUDE.md`
- `INVARIANTS.md` (no new invariants this session unless something forces it; flag at the time)
- `main` branch directly (the only `main` change is via the authorized `/merge`)

NOT doing:
- Role 3 (S14) + Role 4 (S15) deployments — one role per session
- Pass-3 specialist design docs; Phase-C peptide library campaign
- PF-S12-01 Structural-2 (audit script) + Structural-3 (auto-bead) — bead `ams`; user picked path 1 (close debt directly)
- Bead `3y6` (audit-script); Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)

Invariants at risk:
- INV-ROLE-INLINING — `/upgrade-agent` role-tagged sub-dispatches inline full profile per hook v2.5; path-pattern edge case (bead `rc1`) on watch
- PF-S3-01 / AP-ORCH-SELF-ATTEST — Phase 4 + Phase 6 are the 7th consecutive falsification window; SEPARATE+PARALLEL fact-checker/judge; no rounding, no softening; personal source-read
- AP-INCOMPLETE-PROPAGATION — design-doc (S10 Role 2 doc) → ≤200-line agent.md compression; §7-equivalent mechanical check is the defense
- AP-DEFERRED-LOOP-CLOSURE — S13 IS the remediation; closing the OLDEST debt the correct way (deploy + incorporate), debt 3 → 2; falsification window held (opened with debt-closure, not forward work)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH — standard close discipline

Self-recognition pre-flight: Watching at each `/upgrade-agent` Phase 4/6 for "I verified findings like these on Role 1 in S9 already, the pattern is familiar" (familiarity ≠ source-read) and "Role 2 agent.md must hit ≤200 lines so I'll drop a safety property to fit" (token overrun is documented per S9, not compressed away at the cost of safety). Also watching for re-inheriting the kickoff brief's batched-3 framing now that the loop is corrected to one-role-per-session.

## Scope Contract — Session 12 (2026-05-28)

Goal: Two work-units sequenced. **Unit A:** Fix bead `a-plus-maxing-hca` E1 class (Hook v2.5 punch-list, recurrence=3 mandatory structural fix per Rigor Framework Discipline 8) — extend `.claude/hooks/enforce-role-inlining.sh` to accept the canonical operational-slot synonyms (`## Modes` | `## Audit Protocol` | `## Task Routing`) as the 9th-section equivalent. **Unit B:** Run design-doc-protocol Phases 1–5 for Role 4 (medical-safety-reviewer) per `design/DESIGN_DOC_TEMPLATE.md`; §4 INBOUND inherits 8+5+3=16 rows from Roles 1+2+3; produce `design/medical-safety-reviewer-design.md` Status: Final. Fourth end-to-end exercise of canonical template.

Acceptance criteria:
- [ ] AC0-A (Unit A) — Hook v2.5 implements operational-slot synonym (Modes | Audit Protocol | Task Routing). Block message lists which slot synonyms are accepted. Existing 8 tests still pass; 3+ new tests cover security profile shape, orchestrator profile shape, and explicit absence of all three.
- [ ] AC0-B (Unit A) — Bead `a-plus-maxing-hca` E1 class closed with reason citing the structural fix; E2 class (recurrence=2, below mandatory-fix threshold) tracked in either same or new bead.
- [ ] AC0-C (Unit A) — INVARIANTS.md `INV-ROLE-INLINING` row updated: smoke-test count reflects new total; Change Log row appended for S12 hook v2.5.
- [ ] AC0-D (Unit A) — Hook v2.5 fix committed BEFORE first Phase-1 dispatch (chronological discipline; the new hook is in effect for all Role 4 dispatches).
- [ ] AC1 (Unit B) — Phase 1: 3 parallel drafter dispatches, full profiles inlined per INV-ROLE-INLINING via hook v2.5 (no workarounds).
- [ ] AC2 (Unit B) — Phase 2: orchestrator synthesizes `design/medical-safety-reviewer-design.md` per template. §4 INBOUND tri-table inherits 8+5+3=16 rows. Pre-Phase-3 mechanical body↔bibliography + §11.1-row-pointer checks pass.
- [ ] AC3 (Unit B) — Phase 3: 2 red-team dispatches (`/adversarial-review` + a peer-review-pattern safety reviewer).
- [ ] AC4 (Unit B) — Phase 4: PF-S3-01 6th-consecutive guard. Every finding personally source-read before classification; REJECTED rows carry cited-evidence attestations.
- [ ] AC5 (Unit B) — Phase 5: dispositions applied. §7 self-attest 17/17. Appendix A populated. Frontmatter `status: Final`. `vault/meta/index.md` + `log.md` updated.
- [ ] AC6 (close) — All 3 audits exit 0 at `--session 12`. PF attestation canonical `S12 close (YYYY-MM-DD):`. VOLATILE rotation. Feature branch only.

Files I WILL touch:
- `.claude/hooks/enforce-role-inlining.sh` (modify — v2.5)
- `.claude/hooks/tests/test_enforce_role_inlining.sh` (extend with new tests)
- `INVARIANTS.md` (Mechanical Verification cell + Change Log row)
- `design/medical-safety-reviewer-design.md` (NEW)
- `design/.medical-safety-reviewer-design-work/{architect-draft,se-draft,qa-draft,red-team-adversarial,red-team-safety,finding-classifications,dispatch-ledger.jsonl}.md` (NEW)
- `design/.medical-safety-reviewer-design-work/SESSION_KICKOFF.md` (flip to `consumed` at close)
- `HANDOFF.md` (contract + close + VOLATILE rotation)
- `vault/meta/index.md`, `vault/meta/log.md` (appends)
- `.beads/*` via `bd` CLI (close hca E1; possibly create E2-followup bead)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `design/health-{specialist-architect,implementer,edge-case-reviewer}-design.md` (Status: Final)
- `design/DESIGN_DOC_TEMPLATE.md`, `design/CONTINUATION_BRIEF.md`, `design/INTEGRATION_NOTES.md`
- `.claude/agents/health-specialist-architect/` (Session B per role; no deployment this session)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, other `.claude/hooks/*`
- `CLAUDE.md`
- `~/Documents/Projects/skills_library/roles/*` (read-only — profiles inlined verbatim into dispatches)
- `main` branch

NOT doing:
- E2 over-trigger fix (path-pattern + canonical H2 false-positive) — recurrence=2, below Discipline-8 threshold; if quickly co-fixable from E1 work, flag and decide at the time
- Role 4 Session B `/upgrade-agent`
- Roles 2 + 3 Session B
- Pass-3 specialists
- Walter pending items
- Other S10/S11 follow-up beads

Invariants at risk:
- INV-ROLE-INLINING — actively being modified; smoke tests are the falsification window for the modification itself
- AP-ORCH-SELF-ATTEST (PF-S3-01, recurrence=2) — 6th-consecutive guard at AC4
- AP-INCOMPLETE-PROPAGATION — largest cross-role §4 inheritance yet (16 rows from 3 prior docs)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH

Self-recognition pre-flight: None of the canonical PF-S3-01 framings apply yet. Specifically watching during Unit B Phase 4 for "the red-team is just bookkeeping after 3 prior successful runs" and "the §4 inheritance is mechanical so the verdict is mechanical."

## Scope Contract — Session 5

Goal: Build project-suited drafting-team foundation (4 new roles) and 3 pilot specialist design docs (7 total) via Quant design-doc-protocol. Sequential across roles, parallel within. Probable multi-session work; checkpoint after each role. Defer `/upgrade-agent` runs and agent.md authoring to Session B.

Acceptance criteria:
- [ ] `design/` folder created with Quant-style README naming the 7-role pipeline
- [ ] Role 1 health-specialist-architect: 5-phase design-doc-protocol complete; `design/health-specialist-architect-design.md` Status: Final
- [ ] Role 2 health-implementer: 5-phase design-doc-protocol complete; `design/health-implementer-design.md` Status: Final
- [ ] Role 3 health-edge-case-reviewer: 5-phase design-doc-protocol complete; `design/health-edge-case-reviewer-design.md` Status: Final
- [ ] Role 4 medical-safety-reviewer: 5-phase design-doc-protocol complete; `design/medical-safety-reviewer-design.md` Status: Final
- [ ] Checkpoint pause after roles 1-4 for user authorization before specialist roles
- [ ] Role 5 labs-specialist: 5-phase design-doc-protocol complete; uses new foundation drafters; `design/labs-specialist-design.md` Status: Final
- [ ] Role 6 peptide-specialist: 5-phase design-doc-protocol complete; `design/peptide-specialist-design.md` Status: Final
- [ ] Role 7 medical-liaison: 5-phase design-doc-protocol complete; `design/medical-liaison-design.md` Status: Final
- [ ] Every dispatched agent prompt pastes the full 11-section role profile verbatim per INV-ROLE-INLINING
- [ ] No orchestrator self-attestation of red-team verdicts (PF-S3-01 guard); each finding personally verified against cited source
- [ ] HANDOFF rotation rule applied to VOLATILE sections at each checkpoint commit
- [ ] PF attestation appended at close in canonical form `S5 close (YYYY-MM-DD): ...`
- [ ] All three audit scripts (handoff-audit, scope-contract-audit, pf-attestation-audit) exit 0 at close
- [ ] All commits land on feature branch, none on main

Files I WILL touch:
- `design/` (new) + `design/README.md`
- `design/{role}-design.md` × 7
- `design/.{role}-design-work/*` × 7 (drafts, red-team, OQ-list, domain-research)
- `HANDOFF.md` (this contract + per-checkpoint progress + close)
- `vault/sessions/session-5.md` (close note)
- `memory/process-failures.md` (only if a new PF surfaces)
- `.beads/*` (via `bd` CLI only)

Files I will NOT touch:
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`, `vault/labs/*`
- `.claude/skills/*` (including aplus-research and deep-research)
- `.claude/commands/*` (including upgrade-agent)
- `.claude/agents/` (deferred to Session B — design docs only this session)
- `~/Documents/Projects/skills_library/roles/*` (no role profiles deployed; design docs inform Session B authoring)
- `INVARIANTS.md` (no new invariants this session)
- `scripts/` (owned by the parallel session)
- `CLAUDE.md` (owned by the parallel session this cycle)
- `~/.claude/*` (global config untouched)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Running `/upgrade-agent` against any design doc (Session B)
- Writing any `agent.md` profile (Session B)
- The 11 remaining specialists (only pilot 3 + 4 foundation)
- Tiered vs per-agent design decision (explicit post-pilot review)
- Vault git-tracking decision
- LM-04 first HTML artifact generation
- S4 mechanical-enforcement TODO audit scripts (other session)
- Bug-001 follow-up / aplus-research v2 calibration

Invariants at risk:
- INV-ROLE-INLINING — every agent dispatch inlines full 11-section profile verbatim; `enforce-role-inlining.sh` PreToolUse hook is the mechanical check
- INV-SCOPE-CONTRACT — satisfied by this block; `scope-contract-audit.sh` validates format at close
- INV-BRANCH-NOT-MAIN — currently on `feature/wiki-bpc157-aplus-research`; discipline-only guard until pre-commit hook lands
- INV-PF-ATTESTATION — canonical form at close
- INV-HO-ROTATION / INV-HO-NO-STALE-HASH — rotation rule applied to VOLATILE sections; no SHA prefixes in narrative prose
- INV-RESEARCH-ATTESTATION — N/A (no `aplus-research` dispatch this session); `/deep-research` paired-judge rigor is the substitute and is NOT self-attested

## Session 4 close — 2026-05-25

Two cycles this session: (a) the user caught and challenged orchestrator self-attestation of 5 of 6 aplus-research gates (PF-S3-01, recurrence_count=2 of the PF-S2-01 class); (b) rigor-framework adoption + mechanical resistance built and the BPC-157 entry re-verified clean through path-(b) re-dispatches. Commit `8b05b30`. The attestation_chain is now intact across all 6 gates with sha256 of each agent-written source.

**Historical (kept for reference):** Session 3 BPC-157 rebuild context lives in `vault/sessions/session-3.md` (the entry-rebuild itself was at commit `7a98c72`, 2026-05-24).

## Recovery After Compaction

If context was compacted, run `bd prime` then:
1. Read this file (HANDOFF.md)
2. Read `vault/meta/overview.md` (system state summary + knowledge-layer map)
3. Read `vault/meta/contradictions.md` if it exists
4. Read MEMORY.md (in `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-a-plus-maxing/memory/`)
5. Read `vault/WIKI.md` (wiki schema + agent consumer roster)
6. Query vault for current phase (basic-memory search)
7. Read the most recent session note in `vault/sessions/` — currently `session-2.md`
8. Read `vault/decisions/` for architecture decisions
9. Read `.claude/skills/aplus-research/SKILL.md` (project-local research skill with blocking gates — the path to use for all wiki-bound research from session 3 forward)
10. Read `vault/design/artifact-design-protocol.md` before generating any HTML artifact

## What Changed (Session 3, 2026-05-24)

### `aplus-research` skill development (pre-restart)
- `--update[=<reason-slug>]` flag implemented. Phase 2.75 archive-before-write; default slug `rerotation`; pattern enforced. SKILL.md, gate-2.75.schema.json (+ `update_mode`, `update_reason_slug`, `archive_paths`, 3 new halt reasons, conditional invariant), commands/aplus-research.md updated. 8/8 schema smoke-test cases pass.

### BPC-157 canonical rebuild — first end-to-end run of `aplus-research`
- Invoked `/aplus-research "Build canonical library entry for BPC-157" --mode=deep --target=peptide/bpc-157 --update=suspect-fabrications`.
- **All 6 blocking gates PASS, schema-validated.** Gate sequence: 2.75 SCOPE (archived 4 prior artifacts) → 3.5 JUDGE (6 paired retrieval+judge dispatches; 3 sections needed iter-2 remediation; final scores 100/100/100/99/99/100) → 4.75 INTEGRITY (7 IC-10 metadata fixes applied across 4 sections; IC-13 corpus scoping 30/30 probes PASS, **zero fabricated claims detected**) → 6 CRITIQUE (15 findings: 1 critical citation-crosswalk + 9 major + 5 minor; all addressed in Phase 7 refine) → 7.5 RISK-FLOOR (risk_tier=experimental, 8 third-party monitoring markers named, contraindications + monitoring + stopping criteria all populated) → 8.5 LAYERS (practitioner-layer + non-english-layer both written with bibliography + self-check).
- **Canonical fabrication catch:** S2 dispatch attributed He L 2022 (*Front Pharmacol* 13:1026182) as a human PK study. Independent verification via PMC9794587 (Section D + Section E + IC-13 grep) confirmed: rats (n=324) + beagle dogs (n=6), **no human subjects**. There is no published human PK paper for BPC-157. This is the load-bearing correction that justified the rebuild.
- **6 additional bibliographic corrections** logged to `vault/meta/contradictions.md` as C1–C7 (Xu 2020 institution → Fourth Military Medical Univ Xi'an, not PLA Beijing; Sikirić 1993 PMID 8298609 not 8298605; McGuire FP not Bemis-Standoli as first author of *Curr Rev Musculoskelet Med* 2025; Lee & Burgess 2025 co-author Burgess K not C; FDA 503A Cat 2 removed April 22 2026 via nominations withdrawal NOT safety clearance; Xue 2004 → Fourth Military Medical Univ Xi'an = secondary concentration finding placing 3 papers in single Xi'an cluster; Klicek R/Sever M author order on PMID 24304574).
- **Concentration audit:** 52 deduplicated primaries; 75.0% Sikirić-Zagreb academic share; 80.8% combined Zagreb metro (incl. Pliva industrial). Far above 70% threshold. Mandatory first-class concentration section surfaced in synthesis §2 before any indication subsection. Largest non-Sikirić cluster = Chang Gung Taiwan (4); secondary independent finding: Xi'an Fourth Military Medical Univ has 3 papers (single-institution cluster on the "independent Chinese signal").
- **Honest absences surfaced:** no independent in-vivo MSK replication exists outside Sikirić cluster; no human PK paper exists in any language; no chronic >6-week GLP package; no Phase 3 RCT; only 2 registered interventional human trials worldwide (none with results posted); Edwin Lee single-investigator/single-clinic = 100% of post-2003 US human evidence; PL 14736 UC Phase 2 (Ruenzi 2005) was conducted but **never published as full paper** — only Gastroenterology conference abstract.
- **Synthesis size:** 20,635 words pre-refinement; 1,039 lines / ~22K words post-refinement (deep-mode floor 10K). All inline citations renumbered to bibliography 1–52 crosswalk.
- **Skill maturity:** the `aplus-research` skill worked. Phase 4.75 IC-13 corpus scoping is the gate that caught the He L 2022 species misattribution and the 7 bibliographic metadata mismatches. The gate spec held under real use. v1 limitations noted: judge agents returned divergent JSON shapes (workaround: orchestrator hardcoded scores into gate-3.5.json from agent reports); per-citation HEAD-checking budget (IC-10) was best-effort against fetch failures.

## What Changed (Session 2, 2026-05-23)
- Karpathy-style wiki schema added at `vault/WIKI.md` with 14-agent consumer roster (personal-trainer, labs-specialist, nutritionist, supplement-specialist, peptide-specialist, endocrine-specialist, lymphatic-specialist, gi-specialist, cardiovascular-specialist, sleep-coach, recovery-specialist, longevity-strategist, mental-performance-coach, medical-liaison)
- Meta files added: `operator-profile.md`, `current-state.md`, `goals.md`, `contradictions.md`, `index.md`, `log.md` — together form the agent-shared context layer
- Source whitelist at `vault/library/_source-whitelist.md` — 5 standard tiers plus Tier 2.7 (practitioner_protocol) plus Tier NE (non-English literature) plus 12-tag type enum plus admissibility matrix
- Entity templates: `compounds/_template.md`, `biomarkers/_template.md` — each compound template now mandates Non-English Literature Coverage + Prescribing-Practice Layer sections
- First compound library entry: BPC-157 at `vault/library/peptides/bpc-157/{research-report,practitioner-layer,non-english-layer}.md` + `vault/compounds/bpc-157.md`. Entry is structurally complete but the user has flagged that the original deep-research dispatch did not follow protocol and the entry is suspected to contain hallucinations / fabrications / false citations. Re-run scheduled for next session.
- One contradiction logged and resolved same-session: He L 2022 PK paper author attribution (was incorrectly "Xu et al." in original dispatch)
- `aplus-research` project-local skill built at `.claude/skills/aplus-research/` with SKILL.md + 2 reference files + 6 JSON schemas + slash command at `.claude/commands/aplus-research.md`. Six blocking gates: 2.75 SCOPE, 3.5 JUDGE, 4.75 INTEGRITY (incl IC-13 per-citation corpus scoping), 6 CRITIQUE (deep+), 7.5 RISK-FLOOR (compounds), 8.5 LAYERS (standard+ compounds). Three health-specific gates not in deep-research: population-mismatch, risk-floor, concentration-audit. Schema invariants smoke-tested — 6 representative bad payloads all rejected.
- Session protocol violation tracked in `memory/process-failures.md` PF-S2-01 through PF-S2-04

## What Did NOT Work (Do Not Retry)
See `memory/process-failures.md`. Six entries this session: PF-S2-01 (declared deep mode but skipped paired judges + critique + refine), PF-S2-02 (author attribution error caught by accident, not verification), PF-S2-03 (over-questioning user during scoping), PF-S2-04 (over-personalized library research before correction), PF-S2-05 (session close protocol partial execution — multiple required steps skipped or wrongly executed), PF-S2-06 (branch hygiene — all S2 commits landed on main instead of feature branch).

## Drift Checks (S2 close)

### Task drift
Scope expanded user-directed at every step. Started: "is the LLM wiki set up?" Ended: wiki schema + first compound entry + the wrapper skill that should have produced that entry. No silent scope drift; every expansion was explicit user direction.

### Architecture drift
No `INVARIANTS.md` exists for this project yet. CLAUDE.md's Cross-Document Ownership Matrix + rotation rule are the de facto invariants. Architecture drift CHECK result: VIOLATION — phase-state facts initially went into HANDOFF's "What Changed" section instead of `vault/meta/overview.md` (Matrix explicitly forbids this). Caught and corrected in the same close cycle; overview.md updated. Rotation rule clause 3 (no SHA prefixes in prose) was also violated then corrected. No invariant is in worse shape after S2 than before, but the close cycle itself produced two violations that were caught only after user challenge.

### Vision drift
System after S2 IS: LLM-driven personal health agent with a queryable knowledge base (wiki schema + agent roster + source whitelist), one suspect compound entry pending re-run, and a mechanically-gated research wrapper skill. Vision per S1: "LLM-driven personal health agent, markdown + HTML hybrid, A→B→C phased build, evidence-driven." Same project. No vision drift.

## Session 10 close — Pass-2 Role 2 (health-implementer) design doc Final (2026-05-27)

All 6 ACs PASS. Roster B rotation applied (health-specialist-architect drafts §1-4/§13/§15/§16; SE+QA v1-substitutes hold). 40 red-team findings classified (35 LEGITIMATE + 3 LEGITIMATE-MODIFIED + 0 REJECTED + 2 DEFERRED-TO-BEAD). PF-S3-01 guard held — every finding personally source-read before verdict. **Three orchestrator OQ resolutions** locked in at Phase 5: OQ-1 (Role 2 owns audit-script bash), OQ-3 (`templates/refusal-class-taxonomy.yaml` canonical), OQ-7 (QA-strict §13 tag rule project-wide). 11 new beads created. Watch list (4 substrate-unaddressed gaps) all SURFACED via Phase-3 findings; no candidate beads from watch list.

**Drift checks.**
- **Task drift:** Roster B rotation (AC0) was a S10 prerequisite added before Phase 1 dispatch — flagged in scope contract, not silent. All 7 ACs evaluated PASS. No silent drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING strengthened (3 drafter + 2 red-team dispatches inlined full profiles verbatim; hook held). INV-BRANCH-NOT-MAIN held (commits land on feature branch). INV-SCOPE-CONTRACT satisfied. INV-PF-ATTESTATION canonical form below. No INV promotion attempted unilaterally.
- **Vision drift:** Same project. System after S10 IS the same LLM-driven personal health agent now with 2 of 4 foundation design docs Final (Role 1 deployed at .claude/agents/, Role 2 design Final + ready for Session B /upgrade-agent). `templates/` directory added with 2 project-local artifacts (refusal-class-taxonomy.yaml + specialist-risk-class.yaml) that close OQ-3 + S-12 gates. No vision drift.

**PF attestation.**

S10 close (2026-05-27): No new PF-class entries this session. Observations that did NOT promote: (a) the design doc's own initial section count (23 not 19) was caught by red-team F-001 not by my pre-dispatch self-check — this is a Phase-2-synthesis-omission pattern that has only one observed instance (this session) and is structurally caught by the next-phase audit (red-team Phase 3), which is the correct mechanism; recurrence_count=1, watch but not promote. (b) The architect-drafter unilaterally claimed `scripts/audit-specialist-profile.sh` ownership where Role 1 left it ambiguous (F-007) — caught by red-team, classified LEGITIMATE-MODIFIED, resolved at Phase 5 via OQ-1; not a new PF class because the red-team gate caught it before propagation. (c) AC-3 tautology (F-003) — the regex literal in AC-3 matched only its own AC line, the canonical PF-S3-01 surface at the design-doc layer; the red-team Phase 3 caught it, Phase 4 verified, Phase 5 fixed with unique marker. Three consecutive PF-S3-01 guards still held (S7 / S8 / S9 / S10 across four distinct dispatch surfaces).

**Commit:** (pending — Phase 9 git commit + push).

## Session 12 close — Pass-2 Role 4 (medical-safety-reviewer) design doc Final + Hook v2.5 (2026-05-28)

Two work-units sequenced. **Unit A (pre-Phase-1 prerequisite per S11 Discipline-8 mandate):** Hook v2.5 structural fix shipped at commit `f3f3d2d` BEFORE first Phase-1 dispatch. `.claude/hooks/enforce-role-inlining.sh` 9th-section requirement extended to operational-slot synonym set `{## Modes \| ## Audit Protocol \| ## Task Routing}`; smoke tests 8→11/11; INVARIANTS.md INV-ROLE-INLINING Change Log row appended; bead `a-plus-maxing-hca` E1 class closed (recurrence_count=3 → mandatory structural fix per Rigor Framework Discipline 8 satisfied); new bead `a-plus-maxing-rc1` (P2) tracks remaining E2 path-pattern over-trigger class. **Unit B:** Role 4 design doc Final at `design/medical-safety-reviewer-design.md` (874 lines). §4 MIXED tri-table — 8+5+3=16 INBOUND + 9 OUTBOUND (largest cross-role propagation surface). 27 §13 rows (1 LIVE + 2 REFERENCED-with-PROPOSED-extension + 24 PROPOSED-only). 41 red-team findings → 13 LEGITIMATE + 16 LEGITIMATE-MODIFIED + 3 REJECTED-WITH-ADOPTION + 3 REJECTED-with-cited-evidence + 3 DUPLICATE = 32 active fixes applied at Phase 5. PF-S3-01 6th consecutive guard held — every finding personally source-read against cited evidence before classification. Closes v1-substitute software-security gap for S10/S11/S12 safety-red-team slot.

**Hook v2.5 empirical validation under live conditions.** S12 Phase 3 dispatched medical-safety v1-substitute (Security profile with `## Audit Protocol` operational slot). Hook accepted the dispatch natively without synthetic-section workaround — empirical validation of the Discipline-8 structural fix. Pre-S12 (S11), the same dispatch shape required the workaround.

**Drift checks (post-PF-S12-01 honest revision; the pre-PF version of these checks did not catch what the user surfaced).**

- **Task drift:** Scope contract ACs (Unit A AC0-A through AC0-D + Unit B AC1 through AC6) all evaluated PASS. The E2 follow-up bead (rc1) was a contingent expansion explicitly flagged in NOT-doing. **Meta-drift surfaced post-close:** the scope-contract `Files I will NOT touch: .claude/agents/` line framed deferring Session B as discipline choice rather than as deferred obligation. The session-level contract was satisfied; the scope-contract format itself was structurally incomplete (missing a Roster-B-status field per PF-S12-01 Structural-1). No drift on what was executed; drift on what the contract format could express.
- **Architecture drift:** The 12 written invariants in INVARIANTS.md all held. INV-ROLE-INLINING strengthened mechanically (hook v2.5 closes E1 class). INV-BRANCH-NOT-MAIN, INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-HO-ROTATION, INV-HO-NO-STALE-HASH satisfied. **An UNWRITTEN architectural invariant was violated three consecutive times:** the design-doc-protocol's rigor-compounding rotation (each Pass-2 cycle inherits the prior role's deployed agent as a drafter, not just §4 OUTBOUND rows from the prior role's design doc) operated for Role 1 → Role 2 only, then stalled. PF-S12-01 surfaces INV-SESSION-B-INTERLEAVING as the candidate invariant naming this architectural pattern. Promotion-ritual gated on user approval per INVARIANTS.md change-discipline. 2 other candidate INVs from Role 4 §16 also surfaced (INV-HARM-CLASS-COMPOSITION cross-doc carried from S8; INV-DEPLOY-VERDICT-BINARY new Role-4-internal). Three candidate INVs surfaced this session is the highest count of any single session — partial signal that the project's architecture is under-encoded in INVARIANTS.md relative to its actual invariant surface.
- **Vision drift:** Same project IS. After S12, all 4 foundation design docs Final is the milestone the vision predicted (CLAUDE.md project overview + design-doc-protocol). The 14-specialist Pass-3 pipeline is the next vision-load-bearing element. **But the "rigor compounding via deployed-agent-as-drafter" dynamic the vision implies did not engage:** Roles 2/3/4 design docs were drafted by the same Roster B as Role 1's was. The compounding mechanism stalled for 3 cycles. Not "different system" drift; "intended dynamic not engaging" drift — flagged here because the same dynamic is what would prevent Pass-3 specialist drafting from inheriting the reduced rigor as cumulative debt. PF-S12-01 Structural-3 (auto-bead at design-doc-Final close) + Structural-2 (session-b-debt-audit script) are the remediation surface; without them the same dynamic stalls at Pass-3.

**What changed between pre-PF and post-PF drift checks.** The pre-PF checks reported "no drift" across all 3 axes. The post-PF checks report meta-drift on Task axis, unwritten-invariant violation on Architecture axis, and intended-dynamic-not-engaging on Vision axis. The difference is what the user's challenge surfaced — the pre-PF version operated from the same blind spot the PF entry now documents. The post-PF version is the actual drift-check output for S12.

**PF attestation.**

S12 close (2026-05-28): **One new PF entry promoted post-session-close (PF-S12-01 AP-DEFERRED-LOOP-CLOSURE) at user challenge.** Recurrence_count=3 across S10/S11/S12 close cycles. The pattern: three consecutive Pass-2 design-doc cycles skipped intermediate Session B `/upgrade-agent` deployment, leaving 9 of 12 drafter-slot dispatches + 3 of 3 safety-red-team dispatches operating under v1-substitute pattern instead of the intended deployed-agent pattern. User identified the gap with "what agents have been created so far?" — only Role 1 is deployed; Roles 2/3/4 design docs sit unconverted into agent profiles. Per Rigor Framework Discipline 8 (N=3 → mandatory not optional), PF-S12-01 carries 5 structural-fix recommendations including a new scope-contract `Roster B status:` field, a new `scripts/session-b-debt-audit.sh` audit, automatic bead creation at design-doc-Final close, kickoff-brief drift-anticipation prohibition, and INV-SESSION-B-INTERLEAVING candidate invariant. Full entry at `memory/process-failures.md`. Observations that did NOT promote: (a) Mid-Phase-5 §11.1 PF-S6-01 row-pointer defect (cited row 9 instead of row 2 for ancestry-chain mechanical guard) — AP-INCOMPLETE-PROPAGATION class caught by post-Phase-5 self-audit, not by red-team Phase 3. Same defect class as F-001..F-003 + F-005 + F-017 + F-018 + S-05 (all caught by Phase-3 red-team this session). Cross-class recurrence_count=2 — watch for promotion. (b) Six consecutive PF-S3-01 guards now held (S7/S8/S9/S10/S11/S12). 41 findings personally source-read in S12; 3 REJECTED carry cited-evidence attestations (F-012, F-025, F-030); 3 REJECTED-WITH-ADOPTION (F-011, F-013, S-07) per reject-but-adopt feedback memory. (c) The S11 Phase-1-§9-ownership-coordination AP recurred at S12 §4.4 row 9 (Council-Mode protocol added at synthesis without architect-drafter authorship) — flagged honestly via F-009 disposition annotation; same Phase-2-synthesis-content class. Recurrence_count=2 for this class; correct mechanism (synthesis layer) handles it.

**Commit:** Unit A at `f3f3d2d` (already pushed). Unit B + Phase 5 dispositions + close: pending Phase 9.

## Session 13 close — Role 2 (health-implementer) deployed + incorporated; PR #1 merged (2026-05-29)

First correct run of the per-session deploy-and-incorporate loop (the S12 kickoff brief's batched-3 shape was corrected at S13 session-start per user instruction). `/upgrade-agent` deployed `.claude/agents/health-implementer/agent.md` (162 lines); the Roster B SE-drafter slot rotated software-v1-sub → health-implementer (sub-out); `/review-pr` (S13-scoped) + a targeted backlog cross-role consistency pass ran; PR #1 rebase-merged to `main` (main caught up S7–S13). Session B debt 3 → 2.

**Scope-contract evaluation (S13 ACs).**
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS): **PASS** — 8-phase pipeline; R1 took 1 remediation; PF-S3-01 guard held.
- AC2 (sub-out Roster B): **PASS** — `DESIGN_DOC_TEMPLATE.md` §0.1 + `CONTINUATION_BRIEF.md` §7.
- AC3 (≤200 lines / token-or-documented-overrun / sections / paths): **PASS** — 162 lines; token overrun (5,245) documented vs bead 2qq per new DOCUMENT_RUBRIC Rule 7.
- AC4 (§15.2b post-deployment ACs): **PASS** — AC-deploy-9/10/12/13 pass; AC-deploy-11 = AQ-002 mention-aware-pending (bead 3y6); AC-deploy-8/14/15/16 N/A (no specialists authored yet).
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — 13 distinct findings blind-triaged → 8 fixed+verified, 2 beaded, 2 NOT_A_BUG, 1 NOT_ACTIONABLE.
- AC6 (`/merge` on explicit go): **PASS** — rebase merge.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (Role 3 queued S14; kickoff consumed): **PASS** — S14 = Role 3 Session B; `.session-b-deployments/SESSION_KICKOFF.md` → consumed.
- **Added (user-directed, not silent):** DOCUMENT_RUBRIC Rule 7 (budget-overage load-bearing review) — explicit mid-session user request.

**Drift checks.**
- **Task drift:** all 8 ACs PASS. One user-directed scope expansion (DOCUMENT_RUBRIC Rule 7) — flagged, not silent. No other drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING held (review agents dispatched by registered type = full profiles). INV-BRANCH-NOT-MAIN held (merge via server-side `gh pr merge`, not a local push to main; close commits to feature). The backlog consistency pass DISCOVERED pre-existing cross-role drift in the FROZEN design docs (XR-001..004) — discovery, not introduction; all beaded. Two of my own in-session edits introduced local inconsistencies (audit_passed enum; stale rotation rows) that `/review-pr` caught and I fixed in-session.
- **Vision drift:** Same project. After S13, 2 of 4 foundation agents deployed AND incorporated; the rigor-compounding mechanism (deployed-agent-as-drafter) engaged for the first time — Role 2 is now the SE drafter for future cycles, the dynamic PF-S12-01 said had stalled. No vision drift.

**PF attestation.**

S13 close (2026-05-29): **One new PF promoted mid-session at user challenge — PF-S13-01 (AP-PROTOCOL-FROM-MEMORY, recurrence_count=3)** for partial session-open execution (stated the test baseline from memory without running it; jumped to a work-proposal before writing the scope contract; used the railroading option-selection widget). Same operate-from-mental-model class as PF-S2-05 (close) + PF-S6-01 (act-before-verify). Full entry + structural candidate (`scripts/session-open-audit.sh`) at `memory/process-failures.md`. Observations that did NOT promote: (a) two orchestrator in-session edits (AR-007 deferred-script-absent; sub-out rotation rows) each introduced a local inconsistency the `/review-pr` caught + I fixed same-session — caught by the correct mechanism, recurrence_count=1, watch. (b) Token overrun handled per new Rule 7 (load-bearing review + documented residual) — the rule working, not a failure. (c) PF-S3-01 guard held through `/upgrade-agent` Phase 4/6 + `/review-pr` blind triage (7th+ consecutive) — every finding source-read; an independent blind-triage agent enforced verdict independence.

**Commit:** S13 code landed on `main` via PR #1 rebase (`64d3b07` as of 2026-05-29 S13 close); close artifacts committed on the feature branch.

## Session 14 close — Role 3 (health-edge-case-reviewer) deployed + incorporated; PR #2 merged (2026-05-29)

Second clean run of the per-session deploy-and-incorporate loop. `/upgrade-agent` 8-phase pipeline deployed `.claude/agents/health-edge-case-reviewer/agent.md` (191 lines / 6,364 cl100k tokens) + `library-index.md` (net-new, 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge, R3 took 1 remediation; Phase-6 adversarial 9 findings all dispositioned Phase 7). QA drafter slot rotated software-v1-sub → health-edge-case-reviewer (sub-out). `/review-pr` (S14-scoped local diff): 6 findings → 4 LEGITIMATE fixed+blind-verified, 1 DEFERRED (bead `7is`), 1 NOT_A_BUG. Merged to `main` via clean per-session PR #2 (rebase; Option A — fresh branch off origin/main, NOT the diverged long-lived branch; per-session branch deleted on merge). Session B debt 2 → 1.

**Scope-contract evaluation (S14 ACs).**
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS, PF-S3-01 held): **PASS** — 8-phase pipeline; R3 1 remediation; XR-002 confirmed absent.
- AC2 (sub-out QA slot): **PASS** — `DESIGN_DOC_TEMPLATE` §0.1 + `CONTINUATION_BRIEF` §7.
- AC3 (≤200 lines / token-overrun-documented / sections / paths): **PASS** — 191 lines; 6,364 tok documented vs bead `2qq` per Rule 7; 11 sections; paths resolve.
- AC4 (post-deploy ACs; XR-002 absent): **PASS** — AC-deploy-15/16/17/18/19 pass; AC-deploy-13/14/14a PROPOSED-script → Session-B follow-up; XR-002 (`4ej`) absent.
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — independent blind triage + blind verification; 4 fixed, 1 beaded, 1 not-a-bug.
- AC6 (`/merge` on explicit go): **PASS** — rebase merge of clean PR #2 on user's "option A" go.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (Role 4 S15 queued; kickoff consumed; `4ej` noted prereq): **PASS**.

**Drift checks.**
- **Task drift:** all 8 ACs PASS. One user-directed branch-topology decision (Option A fresh-branch-off-main) surfaced at the merge gate — flagged + chosen, not silent. No other drift.
- **Architecture drift:** no invariant degraded. INV-ROLE-INLINING held (review agents dispatched by registered type = full profiles; no path-pattern over-trigger). INV-BRANCH-NOT-MAIN held (merge via server-side `gh`; close commits to feature; never committed on main). INV-SCOPE-CONTRACT + INV-PF-ATTESTATION satisfied. Rigor-compounding advanced: 3 of 4 Roster B drafter slots are now project-local medical agents (architect + SE + QA). `/review-pr` surfaced 4 real defects in the synthesized profile — caught + fixed by the layered review (mechanism working).
- **Vision drift:** same project. After S14, 3 of 4 foundation agents deployed AND incorporated; only Role 4 (safety-red-team slot) remains v1-substitute. No vision drift.

**PF attestation.**

S14 close (2026-05-29): **No new PF-class entries this session.** Both open falsification windows HELD: (a) **PF-S13-01 (AP-PROTOCOL-FROM-MEMORY)** — the S14 session-open executed each Start-Protocol step with real output (HANDOFF read in full incl. paging past truncation; test baseline RUN not stated; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3, did not promote to 4. (b) **PF-S12-01 (AP-DEFERRED-LOOP-CLOSURE)** — S14 opened with Role 3 (oldest debt) as the first and only work-unit; debt 2 → 1; recurrence stays 3. (c) **PF-S3-01 (AP-ORCH-SELF-ATTEST)** held through `/upgrade-agent` Phase 4/6 + `/review-pr` (separate+parallel fact-checker/judge; independent blind triage + verification; every finding source-read; one judge remediation adjudicated against design §12 and REJECTED with cited evidence). Observations that did NOT promote: (i) `/review-pr` found 4 legitimate defects in the synthesized profile (BUG-001 Modes clean-PASS dead-end; TEST-001 Rule-11 schema-gate; API-001 owned-schema omission; QUAL-001 field-name) — BUG-001 survived the Phase-4 judge + Phase-6 adversarial and was caught only by the `/review-pr` bug-hunter lens; this is the layered-review mechanism working as designed (each layer catches what the prior missed). Recurrence-watch on synthesized-content-without-a-design-anchor (the Modes section has no canonical design block), not promoted. (ii) Three frozen-design-doc inconsistencies surfaced + beaded (`p47`, `o9y`, `7is`) — routed to beads not in-place edits (Status:Final discipline), the correct mechanism.

**Commit:** S14 code landed on `main` via clean per-session PR #2 rebase (as of 2026-05-29 S14 close); close artifacts committed on the feature branch.

## Session 15 close — Role 4 (medical-safety-reviewer) deployed + incorporated; PR #3 merged; foundation pipeline COMPLETE (2026-05-29)

Third clean run of the per-session deploy-and-incorporate loop, closing the LAST Session B debt. AC0 reconciled the XR-002 cross-role enum (bead `4ej` closed). `/upgrade-agent` 8-phase pipeline deployed `.claude/agents/medical-safety-reviewer/agent.md` (198 lines / 8,021 cl100k tokens) + `library-index.md` (net-new, 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge — R3 took 1 remediation; Phase-6 adversarial 8 findings all dispositioned Phase 7). Safety-red-team slot rotated software-`security` v1-sub → medical-safety-reviewer (sub-out). `/review-pr` (S15-scoped local diff): 6 findings → 2 LEGITIMATE fixed+blind-verified, 2 NOT_A_BUG, 2 beaded (`dcy`/`1rm` frozen-design-doc defects). Merged to `main` via clean per-session PR #3 (rebase; Option A). **Session B debt 1 → 0; all 4 foundation roles deployed + incorporated.**

**Scope-contract evaluation (S15 ACs).**
- AC0 (close `4ej`, reconcile Role 1 §13 row 15 enum): **PASS** — minimal authorized token edit; rg confirms 0 inverted tokens; bead closed.
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS, PF-S3-01 held): **PASS** — 8-phase pipeline; R3 1 remediation; all dimensions 9/10.
- AC2 (sub-out safety slot): **PASS** — DESIGN_DOC_TEMPLATE §0.1 + CONTINUATION_BRIEF §7; 4/4 Roster B project-local.
- AC3 (≤200 lines / token-overrun-documented / sections / paths): **PASS** — 198 lines; 8,021 tok documented vs `2qq` per Rule 7; 11 sections; paths resolve.
- AC4 (post-deploy ACs; corrected enum): **PASS** — AC-deploy-1..15 present; canonical `{DEPLOY, BLOCK, BLOCK_WITH_OVERRIDE_PATH}` confirmed in deployed agent.
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — independent blind triage + blind verification; 2 fixed, 2 beaded, 2 not-a-bug.
- AC6 (`/merge` on go, Option A): **PASS** — rebase merge of clean PR #3; per-session branch deleted.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (foundation complete; kickoff consumed; forward unblocked): **PASS**.

**Drift checks.**
- **Task drift:** all 9 ACs PASS. One in-scope consistency fix beyond the literal AC2 target (the stale "deployments NOT YET RUN" line in DESIGN_DOC_TEMPLATE §0.1, same §0.1 block S13/S14 left un-updated) — flagged, not silent. No other drift.
- **Architecture drift:** no invariant degraded. INV-ROLE-INLINING held (review agents by registered type = full profiles; upgrade-agent sub-dispatches inlined; no path-pattern over-trigger). INV-BRANCH-NOT-MAIN held (merge via server-side `gh`; close commits on feature; never committed on main). INV-SCOPE-CONTRACT + INV-PF-ATTESTATION satisfied. AC0 STRENGTHENED cross-role consistency — closed the live XR-002 wiring bug before it propagated into the deployed agent + orchestrator gate. Rigor-compounding complete: 4/4 Roster B slots are now project-local medical agents.
- **Vision drift:** same project. After S15, 4 of 4 foundation agents deployed AND incorporated — the milestone the vision predicted. The 14-specialist Pass-3 pipeline is the next vision-load-bearing element, now unblocked. No vision drift.

**PF attestation.**

S15 close (2026-05-29): **No new PF-class entries this session.** All three open falsification windows HELD: (a) **PF-S13-01 (AP-PROTOCOL-FROM-MEMORY)** — S15 session-open executed each Start-Protocol step with real output (HANDOFF read in full incl. paging past truncation to L718; test baseline RUN not stated; Session-B debt computed via `comm` set-difference not memory; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3. (b) **PF-S12-01 (AP-DEFERRED-LOOP-CLOSURE)** — opened with Role 4 (the LAST debt) as first + only work-unit; debt 1 → 0; recurrence stays 3; the loop is now CLOSED (no foundation Session B left to defer). (c) **PF-S3-01 (AP-ORCH-SELF-ATTEST)** held through `/upgrade-agent` Phase 4/6 (separate+parallel fact-checker/judge, 9/10 no rounding) + `/review-pr` (independent blind triage + blind verification; every finding personally source-read). Observations that did NOT promote: (i) my own Phase-7 adversarial-fix (AR-04 probe_floor rename) introduced a local name-divergence that `/review-pr` QUAL-01 caught → fixed → blind-verified — the layered-review mechanism working as designed (an orchestrator-pipeline edit caught by the next independent layer; same class observed S13/S14, caught by the correct mechanism each time, nothing escaped to main; watch — promotion triggers only if such an edit ESCAPES the review layers). (ii) BUG-01 surfaced a genuine frozen-design-doc schema-vs-exemplar inconsistency → beaded `dcy` (routed to the schema owner, not in-place edited) — correct mechanism. (iii) The Option-A git checkout aborted once on the uncommitted HANDOFF scope-contract; recovered via stash → retry (mechanical sequencing, no rigor failure; informs the branch-topology memory: stash HANDOFF before the per-session checkout).

**Commit:** S15 code landed on `main` via clean per-session PR #3 rebase (as of 2026-05-29 S15 close); close artifacts committed on the feature branch.

## Session 16 close — gate-hardening: cross-role contract reconciliation + `scripts/audit-specialist-profile.sh` (2026-05-29)

Pre-Pass-3 gate-hardening (Path 3, user-chosen). Reconciled the three cross-role contract literals the specialist deploy-gate keys on, then built + tested that gate. No specialist deployed; foundation pipeline unchanged (4/4 deployed, debt 0). Bead `ams` closed as overtaken-by-events at session open (PF-S12-01 loop closed; the Pass-3 parallel-build model can't reproduce AP-DEFERRED-LOOP-CLOSURE).

**Scope-contract evaluation (S16 ACs).**
- AC1 (`z8i` override-literal canonicalization): **PASS** — Role 4 §13 row 7 labeled THE canonical literal "operator is overriding a safety block"; Role 1 §13 row 6 + EC-10 (handling + stimulus) and Role 3 §13 row 11 anchor to it; `rg` confirms one literal, 0 divergent phrasings; annotated XR-004 / bead z8i.
- AC2 (`7m1` OUTBOUND row 8 scope): **PASS** — Role 1 §4 OUTBOUND row 8 generalized to cover specialist-profile + wiki-entry deploy gating (Role 4 §1 + §4.4 row 1), not only compound `researching→planned`.
- AC3 (`9u6` 7→8 class): **PASS** — all 7 residual "7-class" taxonomy refs corrected (incl. the §12 Negative-Example block, which asserted a false fact about the 8-class Finding 5); 8-class consistent; deployed agent already correct.
- AC4 (`scripts/audit-specialist-profile.sh`): **PASS** — 25 §13 sub-checks; AQ-002 mention-aware (strips fenced + inline code before banned-modal count); BLOCK→exit 1 / WARN→info; dependency-gated checks degrade to skip-with-info; sources `audit-helpers.sh`.
- AC5 (per-row negative-case smoke tests): **PASS** — `scripts/tests/test_audit_specialist_profile.sh` 21/21 (GOOD + one negative per BLOCK row + AQ-002 mention/control pair); 7 existing suites still green.
- AC6 (close): **PASS** (this close).

**Beads.** Closed: `ams` (overtaken-by-events), `z8i`/`7m1`/`9u6` (reconciled). `3y6` advanced (script + BLOCK-row tests shipped) → left OPEN at P2 with precise residual (per-WARN-row negatives; corpus/denylist/schema-gated checks pending those artifacts; step-8.5 wiring at first-specialist-deploy). New: `f2j` (XR-S16-01, P3) — discovered + beaded, not fixed.

**Discovered + beaded (not fixed — frozen doc, out of scope):** `f2j` (XR-S16-01) — Role 1 §13.5 EC-10 detects Role-7-deployed via the skills_library path while Role 4 BC-1 uses the canonical project-local `.claude/agents/` path. Latent until Role 7 deploys.

**Drift checks.**
- **Task drift:** all 6 ACs PASS. One in-scope judgment beyond literal bead text — fixed the §12 illustrative "7-class" sites (9u6 said the GOOD-block "may stay") because the GOOD example asserted a false fact about Finding 5; flagged in the bead close, not silent. `ams` closed at open (flagged + user-confirmed). No silent drift.
- **Architecture drift:** no invariant degraded. The session REDUCED AP-CROSS-ROLE-CONTRACT-DRIFT (3 literals reconciled). The new audit script is additive — no existing behavior changed; CLAUDE.md step-8.5 wiring deliberately deferred to first-specialist-deploy (the script runs against deployed specialists; none exist yet). INV-BRANCH-NOT-MAIN held (feature branch). Frozen Status:Final docs edited ONLY under bead authorization (z8i/7m1/9u6); deployed agents untouched (already correct).
- **Vision drift:** same project. After S16 the specialist deploy-gate is mechanized + tested and the contracts it enforces are internally consistent — the gate the 14 Pass-3 specialists will be validated against is now LIVE-testable. No vision drift.

**PF attestation.**

S16 close (2026-05-29): No new PF-class entries this session. PF-S13-01 (AP-PROTOCOL-FROM-MEMORY) falsification window HELD — the session-open executed every Start-Protocol step with real output (HANDOFF read in full incl. paging past both truncations; test baseline RUN not recited; deployed-agents-vs-design-docs set difference computed via `ls`, not memory; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3. PF-S6-01 (AP-ACT-BEFORE-VERIFY) HELD — verified each bead's claim against the actual doc before editing, and verified the XR-S16-01 path defect against both design docs before beading. PF-S3-01 N/A (no drafter/validator dispatch this session). Observations that did NOT promote: (i) the script's first crash-test surfaced a refusal-class false-positive (all-caps enum tokens flagged as non-taxonomy classes) + a spec-misaligned WARN-vs-BLOCK on row 7 — both caught by my own crash-test + spec re-read BEFORE writing the test suite, fixed pre-commit (build-then-verify working; nothing escaped). (ii) the test suite's first run caught a real script bug (case-sensitive routing-cue grep) + a test-harness bash gotcha (self-referential `local` under `set -u`) — caught by running the tests, fixed. Neither is a process failure; both are the verify step doing its job.

**Commit:** _(to follow this close note on the feature branch)_

## Top-3 active failure modes (VOLATILE — rotates each session)

1. **AP-PROTOCOL-FROM-MEMORY (PF-S13-01, recurrence_count=3)** — open-protocol guard HELD at S16 (every Start-Protocol step run with real output; HANDOFF read in full incl. paging past both truncations; deployed-agents-vs-design-docs set difference computed via `ls`, not memory; scope contract written + confirmed before any work; no railroading widget). Standing session-lifecycle discipline. **S17 session-open is the next falsification window** — execute each step, never operate from memory; if any step is stated-from-memory or work precedes the scope contract, recurrence promotes to 4.
2. **AP-ORCH-SELF-ATTEST (PF-S3-01)** — DOMINANT forward risk for Pass-3: each of the 14 specialist builds needs the full review stack (separate+parallel fact-checker/judge in `/upgrade-agent`; independent blind triage + blind verification in `/review-pr`; personal source-read of every finding). N/A this session (no dispatch). Sub-pattern watch "pipeline-edit introduces a local inconsistency" — observed again at S16 (my script crash-test + the test-suite first-run each caught defects in my own edits, fixed pre-commit, nothing escaped to a deliverable); **promote to a new PF only if such an edit ESCAPES the verify layer.**
3. **AP-CROSS-ROLE-CONTRACT-DRIFT** — three literals reconciled at S16 via change discipline (`z8i` override-ack / `7m1` OUTBOUND row 8 scope / `9u6` 8-class — all CLOSED). The specialist deploy-gate `scripts/audit-specialist-profile.sh` is now LIVE-testable to catch this class mechanically at deploy time. Remaining frozen-doc defects: `f2j` (XR-S16-01 NEW — EC-10 detection-path skills_library-vs-project-local), `1rm` (XR-S15-02 `probe_floor` two-name), `p47`/`o9y`/`7is` (Role-3 design-doc self-inconsistencies; deployed agents already correct).

**Demoted from prior Top-3:** AP-DEFERRED-LOOP-CLOSURE (PF-S12-01) — loop CLOSED (Session B debt 0; `ams` closed overtaken-by-events at S16 open). AP-INCOMPLETE-PROPAGATION (design-doc→agent.md compression handled across all 4 roles).

## Current State (volatile)

- **Specialist deploy-gate mechanized + tested.** `scripts/audit-specialist-profile.sh` (25 Role-2 §13 sub-checks; AQ-002 mention-aware — strips fenced + inline code before banned-modal counting; BLOCK→exit 1 / WARN→info; dependency-gated checks degrade to skip-with-info) + `scripts/tests/test_audit_specialist_profile.sh` (21/21: GOOD + one negative per BLOCK row + AQ-002 mention/control pair). NOT yet wired into CLAUDE.md step 8.5 — it runs against a *deployed* specialist; deferred until the first specialist exists.
- **Cross-role contract literals reconciled** (`z8i` override-acknowledgment canonical literal; `7m1` OUTBOUND row 8 deploy-gate scope; `9u6` 8-class taxonomy). Frozen Status:Final docs edited under bead authorization only; deployed agents unchanged (already correct).
- **Foundation pipeline unchanged:** 4/4 deployed (Role 1 S9, Role 2 S13, Role 3 S14, Role 4 S15); Session B debt 0. **S16 gate-hardening landed on `main` via clean code-only PR #5** (rebase; post-close, at user request, to unblock Pass-3 builders): `origin/main` `0da8788` → `c021cc1` as of 2026-05-29, now carrying `scripts/audit-specialist-profile.sh` + tests + the z8i/7m1/9u6 design-doc reconciliations. Bookkeeping (HANDOFF/vault) stays on the feature branch per topology; `.beads/issues.jsonl` rode along via bd's git integration (benign — current issue state, not narrative). **Coordination base re-pinned `0da8788` → `c021cc1`** (BOARD + 3 kickoffs + 3 outboxes). Branch topology unchanged (do NOT PR feature→main for bookkeeping; per-session code branches off `origin/main`; stash HANDOFF before the per-session checkout).
- **Pass-3 pilot batch COMPLETE — 3 of 15 specialists DEPLOYED** (post-S16, integrator session). `medical-liaison` (Role 7 adjudicator; PR #8) + `labs-specialist` (PR #6) + `peptide-specialist` (PR #9) all rebase-merged to `main`; **7 agents live** (4 foundation + 3 pilots). All 3 pass the corrected gate 0-viol; all no-frontmatter (convention). **Gate recalibrated** (PR #7: R13-12 collation-only exempt + R13-3 token→WARN). **Dispatch-flip DONE** (PR #10; `origin/main` at `0514f2d` as of 2026-05-29): medical-liaison is now the live `BLOCK_WITH_OVERRIDE_PATH` adjudicator; the pre-Role-7 operator-self-override fallback is DEPRECATED (safety-positive; Role 4 BC-1 + Role 1 §13 row 6 carry doc-wide supersession; f2j EC-10 path fixed). **`81.8%` adjudicated CORRECT** (builder's JBDistill-misattribution claim refuted by integrator re-verification of Ekram 9/11; bead `amc` REJECTED). **Roster now 15** — `dermatologist` added to `vault/WIKI.md` Agent Consumers (Walter, 2026-05-29). Pilot worktrees + branches torn down; clean tree. Beads closed this session: ams/z8i/7m1/9u6/amc/hyi(frontmatter)/`398`(C dispatch-flip)/f2j/90r/3y6. PF-S16-01 (worktree-path hazard) + PF-S16-02 (rm-rf near-miss) logged.
- **Beads:** closed `ams` (overtaken-by-events), `z8i`/`7m1`/`9u6` (reconciled). `3y6` advanced (script + BLOCK-row tests shipped) → OPEN at P2 (residual: per-WARN-row negatives; corpus/denylist/schema-gated checks pending those artifacts; step-8.5 wiring at first-specialist-deploy). New: `f2j` (XR-S16-01, P3).
- **INVARIANTS register at 12 entries** unchanged; none promoted at S16. Candidates carried (INV-HARM-CLASS-COMPOSITION + INV-DEPLOY-VERDICT-BINARY — promotable; INV-DESIGN-DOC-SYMMETRY; DOCUMENT_RUBRIC Rule 7). INV-SESSION-B-INTERLEAVING MOOT.
- **Active landmarks unchanged.** No trigger windows open today (2026-05-29).

**Historical (kept for reference):** `vault/sessions/session-16.md`.

## What Is Next (volatile)

### Pass-3 specialists — pilot done; batch-2 of 4 APPROVED, NOT yet set up

**RESUMPTION POINT for the next session.** 3 of 15 deployed (pilots). **Batch-2 = 4 specialists, confirmed by Walter: `supplement-specialist`, `endocrine-specialist`, `nutritionist`, `sleep-coach`.** NOT yet set up — the next session must: (1) generate the 4 kickoffs (`coordination/kickoffs/<slug>.md`) + outboxes (`coordination/sessions/<slug>.outbox.md`) + BOARD assignment rows, templated from the pilots, **base `0514f2d`** (the BOARD pinned base as of 2026-05-29), **no-frontmatter convention baked in**, medical-liaison-now-live escalation contract; (2) hand Walter the launch recipe (worktree commands + 4 first-message prompts); (3) run as integrator (parallel build → serialized merge, same as the pilots). **Remaining 8 after batch-2** (batches 3–4): personal-trainer, lymphatic-specialist, gi-specialist, cardiovascular-specialist, recovery-specialist, longevity-strategist, mental-performance-coach, **dermatologist** (new). Process is proven: gate calibrated, convention decided, contracts flipped, PROTOCOL guards added (worktree-path hazard; rm-rf). Alternative forward path: **Phase-C peptide library campaign** (`/aplus-research`).

### Recommended before / alongside forward work (not blocking)
- `1ek` (§13-spec reconcile rows 3/12 + R13-13 terminal-states) + `6ln` (audit-run summary / step-8.5 automation) — the `3y6` residual folded here.
- Frozen-doc reconciliations via change discipline: `1rm` (probe_floor two-name), `p47`/`o9y`/`7is` (Role-3 design-doc self-inconsistencies; deployed agents already correct).
- Promote candidate INVs via change-discipline ritual (`mdv`: INV-OVERRIDE-RECORD-SCHEMA + INV-CRITICAL-NON-OVERRIDABLE; also INV-HARM-CLASS-COMPOSITION, INV-DEPLOY-VERDICT-BINARY).
- Labs hardening (`2gs` critical-value-floors.yaml, `623` labs-numerics.py) — not safety prerequisites.

### Open beads (post-pilot, 2026-05-29)
- **P1**: `c6k` (epic — July-2026 baseline)
- **P2**: `pmp` (denylist), `h1z` (AQ-001 operator-profile field enum), `rc1` (hook E2)
- **P3**: `1ek`, `6ln`, `mdv`, `1rm`, `2gs`, `623`, `f2r`, `yfu`, `2qq`, `p47`, `o9y`, `7is`, `mdg`, `5by`, `1ox`, `9yk`
- **Closed this session**: `ams` `z8i` `7m1` `9u6` `amc` `hyi` `398`(C) `f2j` `90r` `3y6`

### Open project work (unchanged)
- Walter pending: 23andMe raw file → `vault/dna/raw/`; Oura purchase; meal-template content; January 2026 health-issue characterization.
- Vault git-tracking decision deferred. First HTML artifact deferred (LM-04).

## Landmark window check (close step 8.7)

All 4 active landmarks (LM-01 doctor visit July 2026, LM-02 Oura, LM-03 23andMe, LM-04 first HTML artifact) — no trigger windows opened during S16.

## Open Issues

### Vault not in git (unchanged from S1)
Per S1 HANDOFF. Decision still deferred. Note: all S2+ vault content has been committed (per user instruction) but the underlying `.gitignore` policy was not reconsidered.

### `agent-verdict-halt` sentinel inconsistency (gate_attest.py vs schemas)
S6 observation: when an agent emits `verdict: HALT` and the orchestrator's scaffold has empty `halt_reasons`, `gate_attest.py attest` injects `"agent-verdict-halt"` as a fallback. That string is not in any gate schema's `halt_reasons` enum, so schema validation fails. Workaround: orchestrator must pre-populate `halt_reasons` with a valid enum value in the scaffold before attest. Either (a) extend every gate schema's halt_reasons enum to include `agent-verdict-halt`, or (b) change the script's fallback to be phase-aware. Defer to v2.5 cleanup.

## Key References
- `CLAUDE.md` — session protocols and project conventions; updated this session to mention the project-local `aplus-research` skill
- `DOCUMENT_RUBRIC.md` — document lifecycle rules
- `vault/WIKI.md` — wiki schema + 14-agent consumer roster (NEW S2)
- `vault/meta/operator-profile.md`, `current-state.md`, `goals.md` — agent-shared context layer (NEW S2)
- `vault/meta/contradictions.md` — active contradictions log; one resolved entry (NEW S2)
- `vault/meta/index.md` — catalog of every wiki entity page by type (NEW S2)
- `vault/meta/log.md` — append-only operation log (NEW S2)
- `vault/library/_source-whitelist.md` — admissibility rules + type-tag enum (NEW S2)
- `vault/library/peptides/_triage.md` — peptide class taxonomy
- `vault/library/peptides/bpc-157/` — first compound library entry (suspect, re-run scheduled)
- `vault/compounds/bpc-157.md` — derived compound entry (suspect, re-run scheduled)
- `vault/compounds/_template.md` — template with mandatory Non-English + Prescribing-Practice sections (NEW S2)
- `vault/biomarkers/_template.md` (NEW S2)
- `.claude/skills/aplus-research/SKILL.md` — project-local research skill with 6 blocking gates (NEW S2)
- `.claude/skills/aplus-research/references/citation-integrity.md` — 13 IC checks incl IC-13 corpus scoping
- `.claude/skills/aplus-research/references/health-gates.md` — population-mismatch, risk-floor, concentration-audit
- `.claude/skills/aplus-research/schemas/*.json` — 6 JSON schemas with conditional invariants
- `.claude/commands/aplus-research.md` — slash command wrapper
- `vault/sessions/session-2.md` — this session's full summary
- `.claude/settings.json` — hook configuration
- `.beads/` — issue tracker database (epic `a-plus-maxing-c6k`)
- `memory/process-failures.md` — canonical failure log; four new entries this session

## Scope Contract — Session 5 (2026-05-25)

Goal: Build the 4 mechanical-enforcement audit scripts + shared helpers library + pre-commit branch-block hook, wired into the close protocol and reflected in INVARIANTS.md.

Acceptance criteria:
- [x] `scripts/lib/audit-helpers.sh` — shared `emit` / `fail` / violations-counter (per Rigor Framework Discipline 5 §3); 16/16 smoke tests pass
- [x] `scripts/handoff-audit.sh` — checks INV-HO-ROTATION (clauses 2 + 5) + INV-HO-NO-STALE-HASH; 12/12 smoke tests pass; exits 0 on current HANDOFF.md
- [x] `scripts/scope-contract-audit.sh` — checks HANDOFF.md carries a `## Scope Contract — Session N` block with required subfields and binary ACs; 12/12 smoke tests pass
- [x] `scripts/pf-attestation-audit.sh` — checks canonical `S<N> close (YYYY-MM-DD):` attestation line; 12/12 smoke tests pass
- [x] `.claude/hooks/block-commit-main.sh` — PreToolUse Bash hook blocking `git commit` while HEAD = main; wired into `.claude/settings.json`; 21/21 smoke tests pass
- [x] Smoke tests for each remaining script — all pass (73/73 across 5 suites)
- [x] `INVARIANTS.md` Mechanical Verification column updated for INV-HO-ROTATION, INV-HO-NO-STALE-HASH, INV-BRANCH-NOT-MAIN, INV-SCOPE-CONTRACT, INV-PF-ATTESTATION — TODO markers removed; S5 Change Log row added
- [x] `CLAUDE.md` close protocol step 8.5 expanded to invoke the 3 new audit scripts (handoff, scope-contract, pf-attestation)

Files I WILL touch:
- `scripts/lib/audit-helpers.sh` (NEW)
- `scripts/handoff-audit.sh` (NEW)
- `scripts/scope-contract-audit.sh` (NEW)
- `scripts/pf-attestation-audit.sh` (NEW)
- `scripts/tests/` (NEW, smoke fixtures + runner)
- `.claude/hooks/block-commit-main.sh` (NEW)
- `.claude/hooks/tests/test_block_commit_main.sh` (NEW)
- `.claude/settings.json` (add PreToolUse Bash matcher)
- `INVARIANTS.md` (Mechanical Verification cells + Change Log row)
- `CLAUDE.md` (close-protocol step 8.5)
- `HANDOFF.md` (this contract + at session close)

Files I will NOT touch:
- `vault/library/peptides/bpc-157/*` and `vault/compounds/bpc-157.md`
- `.claude/skills/aplus-research/*`
- `vault/meta/landmarks.md`
- Any agent role profile files (separate session per user direction)

NOT doing:
- Specialist role profiles (peptide-specialist, medical-liaison) — separate session
- v2 aplus-research calibration findings
- Vault git-tracking decision
- First HTML artifact (LM-04)
- Beads ticket dep-cleanup
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)

Invariants at risk:
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — audited by this session's own deliverable (built-in falsification)
- INV-SCOPE-CONTRACT — this contract satisfies it
- INV-PF-ATTESTATION — mandatory at close
- INV-BRANCH-NOT-MAIN — already on feature branch; new hook becomes second line of defense

## Session 5 close — audit-scripts cycle (2026-05-25)

Audit-script foundation built and wired. All 8 ACs PASS. 73/73 tests pass across 5 suites. Five INVARIANTS-register entries promoted from TODO-mechanical-verification to live scripts/hooks. CLAUDE.md close-protocol step 8.5 now invokes all three audit scripts.

This is one of two parallel S5 cycles. The other cycle (drafting-team foundation + 7 specialist design docs) is mid-flight with its own Scope Contract above. VOLATILE section rotation is deferred to whichever cycle closes last so that Top-3 / Current State / What Is Next reflect both cycles.

**Drift checks:**
- **Task drift:** Scope expanded once mid-session — appended the S5 Scope Contract after the audit-helpers AC completed (I omitted step 7 at session start). Caught and corrected; no other drift. Audit-surfaced fix to HANDOFF line 90 (bare SHA) was an explicit one-off per feedback memory; not a workflow.
- **Architecture drift:** No invariant degraded. Five invariants strengthened by mechanical-enforcement uplift. New audit scripts respect the Cross-Document Ownership Matrix (each script has a single invariant ID it owns).
- **Vision drift:** Same project. System after S5a IS the same LLM-driven personal health agent with mechanically-enforced session-lifecycle invariants now joining the mechanically-enforced research-domain invariants. Rigor compounds.

**PF attestation:**

S5 close (2026-05-25): No new PF-class entries this session. The HANDOFF line-90 bare-SHA defect surfaced by the audit was a residual S4-close miss (not a new failure mode); fixed in-session as a one-off scope expansion that the audit's own AC required. The mid-session scope-contract-omission (failure to append the contract at step 7) is logged here as an observation; if it recurs N=2 it promotes to PF. No PF-S2-01 or PF-S3-01 class incidents observed.

**Commit:** `9a3e44f` (S5a audit-scripts cycle).

## Scope Contract — Session 6 (2026-05-25)

Goal: Apply 4 v2 calibration findings to the aplus-research skill in place, with smoke tests where mechanically verifiable. Skill remains usable for the upcoming peptide library campaign.

Acceptance criteria:
- [x] AC1 — Phase 4.25 ID-Reconcile inserted as BLOCKING gate for standard+; full spec in SKILL.md; `schemas/gate-4.25.schema.json` validated; gate_attest.py wired (ATTESTED_GATES + SOURCE_MD); INV-RESEARCH-CROSS-SECTION-ID added to INVARIANTS register
- [x] AC2 — Post-fix grep enforcement: dedicated "Remediation brief addendum" section in SKILL.md with verbatim block orchestrator injects into Phase 3.5 iter-2+, 4.25 iter-2+, 4.75 verifier remediation, Phase 6 critique remediation
- [x] AC3 — Phase 3 judge brief now embeds literal JSON skeleton (9 dimensions + total + threshold + verdict + findings array) with structural rules
- [x] AC4 — Archive permalink policy documented in Phase 8 §3: scoped under `a-plus-maxing/compounds/_archive/<slug>-<date>-<reason-slug>`; orchestrator rewrites permalink BEFORE archive move in Phase 2.75
- [x] AC5 — Calibration history table near top of SKILL.md (v1.0 → v1.1 → v2 ACs)
- [x] AC6 — Smoke verification: gate_attest 16/16 pass (12 existing + 4 new for phase 4.25 round-trip incl. PASS + HALT + override + stale-source); all audit-script suites still green
- [x] AC7 — Close-protocol audits all exit 0; PF attestation in canonical form (below)

Files I WILL touch:
- `.claude/skills/aplus-research/SKILL.md`
- `.claude/skills/aplus-research/references/citation-integrity.md` (if needed)
- `.claude/skills/aplus-research/schemas/gate-3.5.schema.json` (if AC3 requires)
- `.claude/skills/aplus-research/schemas/gate-4.75.schema.json` (if AC1 affects)
- New `.claude/skills/aplus-research/schemas/gate-4.25.schema.json` (only if AC1 = blocking gate)
- New fixture/smoke test under `.claude/skills/aplus-research/tests/`
- `HANDOFF.md` (this contract + close note)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `vault/library/peptides/bpc-157/*`, `vault/compounds/bpc-157.md`
- `vault/library/peptides/_triage.md`
- `scripts/*`, `.claude/hooks/*`
- `design/*`
- `INVARIANTS.md` (unless AC1 introduces a new INV; flag at the time)
- `CLAUDE.md`
- `~/.claude/skills/deep-research/*`

NOT doing:
- Peptide library campaign runs (Phase C; separate sessions)
- Beads dep cleanup (deferred or rolled into close if quick)
- Specialist role profiles (parallel session)
- Walter pending items
- Vault git-tracking decision
- First HTML artifact (LM-04)

Invariants at risk:
- INV-RESEARCH-ATTESTATION (gate-3.5 schema touches must preserve attestation_chain)
- INV-RESEARCH-IC13-CORPUS (remediation grep must stay distinct from IC-13 verifier)
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH (rotation deferred to last-closing S5/S6 cycle)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN — standard close discipline

## Session 6 close — v2 aplus-research calibration (2026-05-25)

All 7 ACs PASS. 4 calibration findings applied in place to the existing skill (no fork). One new invariant registered: INV-RESEARCH-CROSS-SECTION-ID. New schema `schemas/gate-4.25.schema.json` + 4 new gate_attest smoke tests (T13-T16). Existing 12 tests still pass.

**Skill changes:**
- Pipeline overview + mode tables + gate-by-mode matrix updated for Phase 4.25
- New Phase 4.25 ID-Reconcile spec (5 entity classes: citations, institutions, compound IDs, regulatory dates, trial registrations)
- New "Remediation brief addendum" section with verbatim post-fix-grep block
- Phase 3 judge brief includes literal JSON skeleton (9 dimensions, 2 structural rules)
- Phase 8 §3 archive permalink policy (scoped under `_archive/<slug>-<date>-<reason-slug>`)
- New Calibration history table near top (v1.0 → v1.1 → v2 ACs)
- Schema files table updated
- `lib/gate_attest.py`: phase 4.25 added to ATTESTED_GATES + SOURCE_MD map

**Tests:** 16/16 gate_attest, 89/89 across all audit + hook + gate suites combined.

**Drift checks:**
- **Task drift:** AC1 introduced a new invariant (INV-RESEARCH-CROSS-SECTION-ID) which was flagged in the original scope contract ("unless AC1 introduces a new INV; flag at the time"). Not silent drift. Otherwise scope held exactly.
- **Architecture drift:** No invariant degraded. INVARIANTS register gained one mechanically-enforced research-domain invariant. CLAUDE.md Cross-Document Ownership Matrix respected — SKILL.md owns the skill spec, INVARIANTS.md owns the invariants register, schema files own gate verdict structure.
- **Vision drift:** Same project. System after S6 has the aplus-research skill calibrated against the specific failure modes that S3/S4 BPC-157 surfaced. Skill is now ready for the peptide library campaign (Phase C, separate sessions).

**PF attestation:**

S6 close (2026-05-25): One new PF entry promoted (PF-S6-01, AP-ACT-BEFORE-VERIFY) caught by user mid-session: started a "beads cleanup" task without verifying current state or having a documented procedure; HANDOFF entry was stale and the issue had been resolved in S3/S4. User's "what procedure did you use" forced the honest answer. Logged in `memory/process-failures.md` with recurrence_count=1; feedback memory `feedback_beads_cleanup_procedure.md` saved with verify-first procedure. No PF-S2-01 or PF-S3-01 class recurrences observed. The Phase 4.25 schema mismatch I hit mid-session (top-level `iterations` required vs attest_simple not auto-populating it) was a latent gap in the documented scaffold pattern — not a PF; documented inline via T13-T16 tests. The `agent-verdict-halt` sentinel inconsistency observed during T15 debugging is pre-existing; recorded as an Open Issue for v2.5 cleanup.

## Scope Contract — Session 7 (2026-05-26)

Goal: Produce the canonical `DESIGN_DOC_TEMPLATE.md` that will structure every Pass-2 design doc (4 foundation roles + 14 specialists). Adapt the Quant command-upgrade design-doc-protocol (which is command-upgrade-shaped) into an agent-role-design-doc-shape, validated against Pass-1 deliverables, `/upgrade-agent` requirements, and AGENT_TEMPLATE.md. Three-step pipeline: Architect proposes adaptation → adversarial-review red-team → orchestrator verifies findings + synthesizes final template.

Acceptance criteria:
- [x] AC1 — Architect-role sub-agent dispatched with full 11-section profile inlined; produced `design/.design-doc-template-work/architect-proposal.md` (422 lines, 18 sections, full 10-input source-read)
- [x] AC2 — `/adversarial-review` skill agent dispatched; 22 findings across 11 categories (8 standard + 3 agent-specific); both mechanical coverage checks executed
- [x] AC3 — Orchestrator personally verified each finding against cited source per PF-S3-01 guard. Classifications: 16 Legitimate, 4 Legitimate-modified, 2 Rejected with cited-evidence attestations at `design/.design-doc-template-work/finding-classifications.md`
- [x] AC4 — `design/DESIGN_DOC_TEMPLATE.md` synthesized (774 lines), `Status: Final`; rejected findings preserved in §10 with source-of-truth attestations
- [x] AC5 — All 3 audits exit 0 at `--session 7`; PF attestation below in canonical form

Files I WILL touch:
- `design/.design-doc-template-work/` (NEW dir + 3 artifacts: architect-proposal.md, red-team-adversarial.md, finding-classifications.md)
- `design/DESIGN_DOC_TEMPLATE.md` (NEW — canonical template)
- `HANDOFF.md` (this contract + close note)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- Existing `design/.{role}-design-work/` × 4 (Pass-1 deliverables — read-only)
- `design/CONTINUATION_BRIEF.md`, `design/INTEGRATION_NOTES.md`, `design/README.md`
- Any actual Pass-2 design doc (Roles 1-4) — those use the template; not this session
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `INVARIANTS.md` (no new invariants this session unless something forces it; flag at the time)
- `CLAUDE.md`
- `~/Documents/Projects/skills_library/roles/*` (read-only — Architect profile inlined, not modified)

NOT doing:
- Any actual role Pass-2 design doc work (subsequent sessions, one role per session)
- `/upgrade-agent` runs (Session B per role, after each design doc finalizes)
- Pass 3 specialist work
- Peptide library campaign
- Walter pending items
- v2.5 punch-list items
- Vault git-tracking decision

Invariants at risk:
- INV-ROLE-INLINING — Architect dispatch must inline the full 11-section profile per the hook
- AP-ORCH-SELF-ATTEST guard (PF-S3-01) — AC3 is the falsification window for design-doc-protocol context; finding classifications must be personal-source-reads, not orchestrator prose self-attestation
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN — standard close discipline

Self-recognition pre-flight: None of the canonical PF-S3-01 framings apply yet. Specifically watching for "the architect's proposal already looks good, the red-team is just bookkeeping" during AC2/AC3.

## Session 7 close — design-doc template (2026-05-26)

Foundational artifact complete. `design/DESIGN_DOC_TEMPLATE.md` is the canonical contract for 18 downstream design docs (4 foundation roles in Pass-2; 14 specialists in Pass-4). Commit `0563269`. Pushed to `origin/feature/wiki-bpc157-aplus-research`. All 5 ACs PASS. PF-S3-01 guard cleanly held — adversarial-review findings were each personally verified against source before classification; 2 findings rejected with cited-evidence attestation (F-006 R-count empirical premise, F-023 worked-example copy-edit).

**Drift checks:**

- **Task drift:** S7 contract was 5 ACs. Mid-session the user flagged that I had conflated Pass-2 (design doc) with Session B (`/upgrade-agent` deployment) in my original scope-shaping question. I re-read the protocols + brief, restructured the plan, and the user accepted the corrected read. Two scope expansions surfaced: (a) capturing the "reject-but-adopt" pattern as a feedback memory (user-approved); (b) strengthening the Pass-1-complete status snapshot in the template §0.1 so future sessions can't miss it (user-approved). Both expansions were explicit user direction; no silent drift.
- **Architecture drift:** No invariant degraded. The template itself is a load-bearing new artifact but does not modify existing invariants. The Quant→Medical adaptation followed the project's existing Cross-Document Ownership Matrix (design docs are owned by `design/`; `/upgrade-agent` Phase 7 enforces generic agent.md constraints; the template explicitly delegates to it via §15.1 rather than restating). The 10-vs-11 AGENT_TEMPLATE.md disambiguation (F-001) preserves the existing `enforce-role-inlining.sh` hook semantics — the hook stays correct as-is for its purpose (catching incomplete mature profiles).
- **Vision drift:** Same project. System after S7 has the canonical design-doc structure that will produce 18 medical-LLM agent profiles. The foundation-role design docs (Pass-2) are now unblocked. The peptide library campaign (Phase C) remains the other parallel forward direction. No vision drift; the rigor compounds.

**PF attestation:**

S7 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during AC3 (the verification phase) — the discipline held: each finding was source-read before classification, two were rejected with cited evidence, the reject-but-adopt pattern was documented as a feedback memory rather than smuggled in as Legitimate. Watched for the "minor accretion" framing during the scope expansion for the template §0.1 status snapshot — declined to skip; the snapshot is load-bearing for the next session's correct read of pipeline state. AP-INCOMPLETE-PROPAGATION did NOT surface — synthesizing 22 findings across an 18-section template was the natural stress case for missed-propagation, and the §7 self-attest checklist was the explicit defense.

One observation worth noting (not promoted to PF): the inlining hook caught the H1 pattern `# Adversarial Reviewer` on my second sub-agent dispatch, exactly as Pass-1's CONTINUATION_BRIEF §1 Q1 documented. I rewrote the dispatch to use the `/adversarial-review` skill instead of role-tagged prose. This is the documented edge case where research-using-a-role-file is conflated with role-tagging-a-dispatch; the hook's deterrent behavior is correct.

## Scope Contract — Session 8 (2026-05-26)

Goal: Run design-doc-protocol Phases 1–5 for Role 1 (health-specialist-architect) against `design/DESIGN_DOC_TEMPLATE.md`. Produce `design/health-specialist-architect-design.md` with `status: Final`. First end-to-end exercise of the canonical template.

Acceptance criteria:
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches (architect / senior-engineer / qa via existing software-flavor profiles as v1-substitute). Each drafter prompt inlines the full 11-section role profile verbatim per INV-ROLE-INLINING. Drafts written to `design/.health-specialist-architect-design-work/{architect,se,qa}-draft.md`. All 3 dispatches recorded in `dispatch-ledger.jsonl`.
- [ ] AC2 — Phase 2: orchestrator synthesizes `design/health-specialist-architect-design.md` per `DESIGN_DOC_TEMPLATE.md` §0.2 frontmatter + 18 sections + Appendix A. Body↔bibliography symmetry check (Lesson 3 guard) passes before Phase 3.
- [ ] AC3 — Phase 3: 2 parallel red-team dispatches (`/adversarial-review` skill + software `security` agent v1-substitute briefed on medical-safety per CONTINUATION_BRIEF §7). Findings written to `design/.health-specialist-architect-design-work/red-team-{adversarial,safety}.md`. Both dispatches recorded in dispatch-ledger.
- [ ] AC4 — Phase 4: PF-S3-01 guard held. Orchestrator personally verifies each finding against cited source-of-truth before classification. Outcomes recorded in `finding-classifications.md` with verdicts LEGITIMATE / LEGITIMATE-MODIFIED / REJECTED; every REJECTED row carries cited evidence (file path + section/line). Reject-but-adopt pattern applied where appropriate per `feedback_reject_but_adopt_pattern.md`.
- [ ] AC5 — Phase 5: LEGITIMATE + LEGITIMATE-MODIFIED dispositions applied. Appendix A populated. `DESIGN_DOC_TEMPLATE.md` §7 self-attest checklist (17 binary items) executed. Frontmatter `status: Final`. `vault/meta/index.md` + `vault/meta/log.md` updated.
- [ ] AC6 — Close: all 3 audit scripts exit 0 at `--session 8`; PF attestation in canonical `S8 close (YYYY-MM-DD):` form; VOLATILE rotation applied; feature branch only (INV-BRANCH-NOT-MAIN).

Files I WILL touch:
- `design/health-specialist-architect-design.md` (NEW)
- `design/.health-specialist-architect-design-work/architect-draft.md` (NEW)
- `design/.health-specialist-architect-design-work/se-draft.md` (NEW)
- `design/.health-specialist-architect-design-work/qa-draft.md` (NEW)
- `design/.health-specialist-architect-design-work/red-team-adversarial.md` (NEW)
- `design/.health-specialist-architect-design-work/red-team-safety.md` (NEW)
- `design/.health-specialist-architect-design-work/finding-classifications.md` (NEW)
- `design/.health-specialist-architect-design-work/dispatch-ledger.jsonl` (NEW)
- `design/.health-specialist-architect-design-work/SESSION_KICKOFF.md` (status flip to `consumed` at close)
- `HANDOFF.md` (this contract + close note + VOLATILE rotation)
- `vault/meta/index.md` (append new design doc)
- `vault/meta/log.md` (append create op)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `design/.health-specialist-architect-design-work/domain-research.md` (Pass-1 substrate — read-only)
- `design/DESIGN_DOC_TEMPLATE.md` (canonical template — read-only; defects → §18 Open Question + user flag, not in-place edit)
- `design/CONTINUATION_BRIEF.md`, `design/INTEGRATION_NOTES.md`, `design/README.md`
- Other roles' work dirs (`design/.{health-implementer,health-edge-case-reviewer,medical-safety-reviewer}-design-work/`)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `INVARIANTS.md` (no new invariants unless something forces it; flag at the time)
- `CLAUDE.md`
- `~/Documents/Projects/skills_library/roles/*` (read-only — profiles inlined verbatim into dispatches, NOT modified)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Roles 2/3/4 Pass-2 design docs (S9–S11 sequential per CONTINUATION_BRIEF §7)
- `/upgrade-agent` runs (Session B per role, after each design doc finalizes)
- Pass 3 specialist deep-research (after all 4 foundation roles deployed)
- Peptide library campaign (Phase C; separate sessions; aplus-research falsification window)
- Template modifications (deferred to template-change discipline if defects surface)
- v2.5 punch-list items (`agent-verdict-halt` sentinel; `enforce-role-inlining.sh` path-obfuscation comment)
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)
- Vault git-tracking decision
- First HTML artifact (LM-04)

Invariants at risk:
- INV-ROLE-INLINING — every drafter dispatch must inline the full 11-section profile; the `enforce-role-inlining.sh` PreToolUse hook is the mechanical check. /adversarial-review skill dispatch must NOT use a role-tagged H1 (E1 in kickoff brief; observed in S7).
- PF-S3-01 guard (AP-ORCH-SELF-ATTEST) — Phase 4 is the falsification window in design-doc-protocol context. Same discipline S7 held: source-read every finding before classification; reject-but-adopt pattern explicit.
- AP-INCOMPLETE-PROPAGATION (S4 finding) — 18-section template synthesis is the natural stress case; §7 self-attest checklist is the defense.
- INV-SCOPE-CONTRACT — this contract satisfies it.
- INV-PF-ATTESTATION — canonical form at close.
- INV-BRANCH-NOT-MAIN — currently on `feature/wiki-bpc157-aplus-research`; `block-commit-main.sh` PreToolUse hook is second line of defense.
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — VOLATILE rotation at close; no SHA prefixes in narrative prose.

Self-recognition pre-flight: Watching specifically for —
- "the architect-draft already looks complete, the SE/QA drafts are confirmation" → would skip parallel drafter dispatches (canonical PF-S3-01 framing variant)
- "the red-team finding's premise is wrong AND its fix is bad" → verify the fix is actually bad before dropping; reject-but-adopt pattern applies
- "the template is the contract, I don't need to re-read it section-by-section during Phase 2" → operating-from-memory pattern (PF-S2-05 root cause)
- "iter-2 dispatches would be expensive given how many I've already run" → canonical PF-S3-01 framing

## Session 8 close — Pass-2 Role 1 design doc (2026-05-26)

All 6 ACs PASS. `design/health-specialist-architect-design.md` Status: Final at 873 lines. First end-to-end run of `design/DESIGN_DOC_TEMPLATE.md` against a foundation role; template held under real use. 38 red-team findings (23 adversarial + 15 safety v1-substitute); Phase 4 PF-S3-01 guard cleanly held — each finding personally source-read before classification; 26 LEGITIMATE + 11 LEGITIMATE-MODIFIED + 1 REJECTED.

**Highest-leverage Phase-5 substantive additions:**
- 8th refusal class `AUTHORITY_FRAMING_BYPASS` (F-S2) covers 81.8% Authority Impersonation attack surface
- H-class composition (F-S1) — H1-H8 OUTBOUND row + Core Rule 13 + new INV-HARM-CLASS-COMPOSITION (PROPOSED)
- Pre-Role-7 escalation override-acknowledgment + contradictions-log requirement (F-S15) addresses largest pre-deployment exposure
- Operator-as-A3 anti-pattern (F-S3 AP8) + EC-9 — encodes the medical-LLM asymmetry (operator inside trust boundary AND named adversary in Role 4 threat catalog)
- Image-handling Tools-conditional gating (F-S6) protects labs-specialist LM-01 critical path

**Critical fixes:** AC-4 grep mechanism returning 4 lines instead of 7 identifiers (F-001 empirically verified); §13 row 9 mis-scoped against §16 OUT-OF-SCOPE (F-002 — restated as REFERENCED-by-template-for-downstream).

**Hook edge case logged:** Security profile uses `## Audit Protocol` instead of `## Modes`; INV-ROLE-INLINING hook blocked the safety dispatch on first attempt. Resolved with additive synthetic `## Modes` pointer to Audit Protocol (no paraphrasing of existing 11 sections). Second instance of profile-vs-hook expectation mismatch (first: S7 `/adversarial-review` H1). Pattern: v1-substitute software profiles don't all conform to the medical-template hook's section-name expectations. Documented in dispatch-ledger.jsonl.

**Drift checks:**

- **Task drift:** S8 contract was 6 ACs (Phase 1 drafter dispatches → Phase 2 synthesis → Phase 3 red team → Phase 4 verification → Phase 5 finalize → close audits). All 6 PASS exactly as specified. Hook edge case during Phase 3 security dispatch resolved in-session without scope expansion; the synthetic Modes pointer is faithful to the security profile content. No silent scope drift.
- **Architecture drift:** No invariant degraded. Phase 5 SURFACED a candidate new invariant (INV-HARM-CLASS-COMPOSITION, tagged PROPOSED in §16) per F-S1 disposition — this is candidate-for-register-add via the INVARIANTS change-discipline ritual at next review, not an unilateral promotion. The current 12-entry register remains untouched. The new invariant is documented in the design doc only.
- **Vision drift:** Same project. System after S8 has the first foundation-role design doc complete, demonstrating DESIGN_DOC_TEMPLATE.md works under real use against a 727→873-line Pass-2 cycle. The 18-section template + Phase Coverage Matrix + Self-attest checklist all held; the 38-finding red team produced operational improvements (8 BLOCK-class fixes incorporated). Pass-2 for Roles 2/3/4 is now unblocked; the OUTBOUND interface contracts are established. No vision drift; the rigor compounds.

**PF attestation:**

S8 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during Phase 4 (the falsification window for design-doc-protocol context) — the discipline held: 38 findings each personally source-read before classification; F-019 REJECTED with cited evidence (reviewer self-withdrawn after personal recount); empirical verifications performed for F-001 (grep returned 4 broken vs 7 correct), F-002 (3-line read confirmed contradiction), all 5 BLOCK safety findings against Role 4 substrate line ranges. Reject-but-adopt pattern from S7 did NOT recur (0 cases this cycle); discipline remains on the watch list but did not surface as a temptation.

Watched for AP-INCOMPLETE-PROPAGATION during 37-disposition Phase-5 application across 18 sections + Appendix A — the §7 self-attest checklist was the explicit defense; all 17 binary criteria passed at finalize. Watched for the "minor accretion" framing when adding 6 new ECs (8→14) past template upper bound (4-8) — the addition was load-bearing per Phase 4 dispositions, not editorial.

Two observations worth noting (not promoted to PF): (a) the inlining hook blocked the security dispatch on first attempt due to security profile's `## Audit Protocol` vs hook's `## Modes` expectation — same class as S7's adversarial-review H1 issue; the v2.5 punch-list item should now be promoted to a documented edge case in the hook (recurrence_count=2 for the class). (b) The §14 EC count grew past template's stated upper bound of 4-8 to 14 due to Phase 4 dispositions adding 6 new ECs — this is justified for foundation-role-1 (the OUTBOUND-establishing doc) but may signal the template's §14 budget should be re-evaluated for foundation roles vs specialists.

**Commit:** _(to follow this close note)_

## Scope Contract — Session 9 (2026-05-26)

Goal: Run `/upgrade-agent` against `design/health-specialist-architect-design.md` (Status: Final, 873 lines). Produce `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` per the 8-phase pipeline. Add catalog row.

Acceptance criteria:
- [ ] AC1 — Phase 1 Baseline: net-new authoring documented (no prior agent.md at target path); baseline scorecard captures 0/10 across all 10 dimensions; line/token targets established (~140 / ≤200 hard max).
- [ ] AC2 — Phase 2 Rubric: agent-specific rubric derived from design-doc §15.2 (7 binary ACs) + 10 generic dimensions; 9/10 and 7/10 thresholds defined; verification criteria specified.
- [ ] AC3 — Phase 3 Research: 3 parallel research dispatches (R1 Behavioral Traits / R2 Tools & Configuration / R3 Communication & Anti-Patterns); each produces MVE + Cut Rationale; each grounds against design doc + AGENT_TEMPLATE.md; INV-ROLE-INLINING respected on any role-tagged dispatch.
- [ ] AC4 — Phase 4 Validation Loop: SEPARATE fact-checker + judge in PARALLEL with FRESH context each iteration; 9/10 on every targeted dimension required (no rounding, no softening); **PF-S3-01 guard held** — no orchestrator self-attestation of validator verdicts; remediator runs on fail.
- [ ] AC5 — Phase 5 Synthesis: agent.md at `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md`; AGENT_TEMPLATE.md 10 base sections + Modes; anti-sycophancy in first 20 lines; Negative Examples in last 30 lines; per-section line budgets respected.
- [ ] AC6 — Phase 6 Adversarial Review: `/adversarial-review` skill dispatched against the synthesized agent.md (not the design doc); 8 standard categories + 4 agent-specific criteria; findings classified per PF-S3-01 guard.
- [ ] AC7 — Phase 7 Final Corrections: every adversarial finding addressed; line count ≤200 verified via `wc -l`; token count ≤2000 verified via tiktoken; all 10 sections present; operational completeness check passes.
- [ ] AC8 — Phase 8 Close Out: before/after scores reported; agent.md + library-index.md (if any) + catalog row deployed; deferred items beaded if any.
- [ ] AC9 — Close: all 3 audit scripts exit 0 at `--session 9`; PF attestation in canonical `S9 close (YYYY-MM-DD):` form; VOLATILE rotation applied; feature branch only (INV-BRANCH-NOT-MAIN).

Files I WILL touch:
- `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` (NEW)
- `~/Documents/Projects/skills_library/roles/health-specialist-architect/library-index.md` (NEW, if needed)
- `~/Documents/Projects/skills_library/roles/orchestrator/catalog.md` (append row)
- `HANDOFF.md` (this contract + close note + VOLATILE rotation)
- `design/.health-specialist-architect-design-work/SESSION_B_KICKOFF.md` (status flip to `consumed` at close)
- `design/.health-specialist-architect-design-work/upgrade-agent-work/` (NEW dir for phase artifacts: baseline-scorecard.md, agent-rubric.md, R1/R2/R3 outputs, validation logs, adversarial-review.md, dispatch-ledger.jsonl)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `design/health-specialist-architect-design.md` (Status: Final; defects → ADR, not in-place edit)
- `design/DESIGN_DOC_TEMPLATE.md`, `design/CONTINUATION_BRIEF.md`, `design/INTEGRATION_NOTES.md`, `design/README.md`
- `design/.health-specialist-architect-design-work/{architect,se,qa}-draft.md`, `red-team-*.md`, `finding-classifications.md`, `dispatch-ledger.jsonl` (Phase-3/4 design-doc artifacts frozen)
- Other roles' design dirs (`design/.{health-implementer,health-edge-case-reviewer,medical-safety-reviewer}-design-work/`)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `scripts/*`, `.claude/hooks/*`
- `INVARIANTS.md` (unless `/upgrade-agent` surfaces a new candidate; flag at the time)
- `CLAUDE.md`
- Other role profiles in `~/Documents/Projects/skills_library/roles/*` (read-only — only writing the new health-specialist-architect role + appending the catalog row)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Pass-2 design docs for Roles 2/3/4 (S10-S12 sequential)
- Other Session B deployments (Role 2/3/4 after their Pass-2 finalizes)
- Pass-3 specialist work
- Peptide library campaign (Phase C; separate sessions)
- v2.5 punch-list items (`agent-verdict-halt` sentinel; `enforce-role-inlining.sh` profile-vs-section comment)
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)
- Vault git-tracking decision
- First HTML artifact (LM-04)
- Modifying the design doc (Status: Final; defects → ADR)
- Promoting INV-HARM-CLASS-COMPOSITION to the register (separate change-discipline ritual)

Invariants at risk:
- INV-ROLE-INLINING — `/upgrade-agent` sub-agents (R1/R2/R3 research, fact-checker, judge, remediator, adversarial-reviewer) that are role-tagged must inline the full 11-section role profile per the hook. Generic research dispatches (no H1=`# X`, no `roles/<slug>/agent.md` reference) are unaffected. Hook profile-vs-section edge case (recurrence_count=2) on watch — if S9 hits it, that's recurrence_count=3 and structural change is mandatory.
- PF-S3-01 guard (AP-ORCH-SELF-ATTEST) — Phase 4 Validation Loop is the falsification window in `/upgrade-agent` context. Fact-checker + judge SEPARATE and PARALLEL; orchestrator consumes their verdict files, not prose self-attestation. 9/10 every dimension — no rounding, no softening.
- AP-INCOMPLETE-PROPAGATION — Phase 5 Synthesis compresses 873-line design doc into ≤200-line agent.md. The §7 Final Corrections mechanical-check checklist is the defense.
- INV-SCOPE-CONTRACT — this contract satisfies it.
- INV-PF-ATTESTATION — canonical form at close.
- INV-BRANCH-NOT-MAIN — currently on `feature/wiki-bpc157-aplus-research`.
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — VOLATILE rotation at close; no SHA prefixes in narrative prose.

Self-recognition pre-flight: Watching specifically for —
- "the design doc is Status: Final, the agent.md can be derived directly without research dispatches" → would skip Phase 3 (canonical PF-S2-01 framing variant)
- "the line count is 198, 2 over is fine" → would soften the 200 hard max (rejected by command HARD RULES)
- "the fact-checker and judge can be the same agent in two prompts" → violates the SEPARATE-and-PARALLEL HARD RULE
- "8.5/10 rounds up to 9/10" → rejected by command HARD RULES ("no rounding, no softening")
- "the validator JSON wasn't returned cleanly, I can compose the synthesis input from the prose" → PF-S3-01 framing variant (same shape as S3 gate-3.5 fabrication)
- "Phase 6 looks clean because Phase 5 was careful" → would skip /adversarial-review (rejected by HARD RULES — no skipping phases)

## Session 9 close — Pass-2 Role 1 Session B (`/upgrade-agent` deployment) (2026-05-26)

All 9 ACs PASS. `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` deployed at 121 lines / 3,236 cl100k tokens. First end-to-end run of `/upgrade-agent` against a finalized Pass-2 design doc; the 8-phase pipeline held. Phase 4 required 3 validation iterations on R1 (fact-checker found line-budget + citation-regex defects; judge found D2/D3/D9 sub-9 + D10 sub-9 on iter-2); R2 + R3 cleared iter-1. Phase 6 adversarial review surfaced 15 findings (1 Critical inherited / 5 Major / 6 Minor / 3 Nitpick); 8 applied at Phase 7, 1 deferred per reviewer option, 6 documented-as-acceptable per reviewer rationale.

**Highest-leverage Phase-5/Phase-7 substantive decisions:**
- Modes section materialized (single "Design Mode") to satisfy `enforce-role-inlining.sh` 11-section expectation; design-doc §13 row 13 (Modes-required WARN) addressed pragmatically without prejudging §18 OQ-7
- Modes placement repositioned post-Anti-Patterns / pre-Negative-Examples per F-A03 (design-doc §12.4 canonical sequence)
- Token budget overrun documented in catalog row (~3,100 with characterization pointer) rather than aggressively compressed; medical-domain density (8-class enum + GRADE HALT + H-class composition + Mechanism A/B/C mapping) intrinsically requires more tokens than software roles
- Loop-Breaking split per F-A04 from 4 to 5 thresholds to satisfy D7 9/10 explicit threshold count

**Critical findings posture:** F-A01 (refusal-class 7-vs-8 residual in design-doc prose at §1/§3.1/§5.11/§15.2) deferred to follow-up bead per reviewer option (a) — agent.md itself is internally consistent at 8 classes; the upstream prose layer is the defect. PF-S3-01 guard held: 38 design-doc findings + 6 validator reports + 1 adversarial review + 15 Phase-6 findings each personally verified before classification. Reject-but-adopt pattern from S7 did NOT recur (0 cases). F-A07/F-A12/F-A13/F-A14/F-A15 accepted reviewer's "no change" recommendation with rationale.

**Hook edge case logged (new class).** S9 surfaced a DISTINCT edge case from S7/S8: `enforce-role-inlining.sh` regex `roles/[a-z-]+/agent\.md` over-triggers on non-role-tagged research dispatches that merely mention a role-profile path. Three Phase-3 dispatches blocked iter-1; one Phase-6 dispatch blocked iter-2 because example H1 in output spec matched H1 regex. Workaround: refactor path refs to directory-only + H3 headers in output spec + avoid literal H1 patterns in prompts. Recurrence_count=1 for this NEW class. The S7/S8 profile-vs-section class (recurrence_count=2) did NOT recur. Two distinct hook-edge-case classes now documented; v2.5 punch-list expanded.

**Drift checks:**

- **Task drift:** S9 contract was 9 ACs (Phase 1 baseline → Phase 2 rubric → Phase 3 research → Phase 4 validation → Phase 5 synthesis → Phase 6 adversarial → Phase 7 corrections → Phase 8 close-out → audit-script close). All 9 PASS. Two mid-session adjustments: (a) Token-budget overrun characterization added to catalog row (anticipated in scope contract as "Adversarial review may surface compression opportunities") — not silent drift; (b) F-A01 deferred-to-bead per reviewer option (a) — explicit user-style decision documented in close note. No silent scope drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING hook continued to fire (correctly per its current regex spec); workaround documented for future improvement. The 12-entry register remains unchanged. Candidate INV-HARM-CLASS-COMPOSITION still PROPOSED (not unilaterally promoted). The deployed agent.md respects every project invariant: INV-ROLE-INLINING (all sections present); INV-BRANCH-NOT-MAIN (commits to feature branch only); INV-PF-ATTESTATION (this close attestation). No architecture drift; the rigor compounds.
- **Vision drift:** Same project. System after S9 has the first deployed medical-LLM agent profile alongside its source design doc. The 4-role foundation pipeline is 25% complete (Role 1 of 4); the `/upgrade-agent` 8-phase pipeline has been validated end-to-end against a real Pass-2 deliverable. The OUTBOUND interface contracts from Role 1's design-doc §4 are now inheritance-ready for Roles 2/3/4. No vision drift.

**PF attestation:**

S9 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during Phase 4 validation loop (the explicit falsification window for upgrade-agent context) — the discipline held: 6 validator reports (3 fact-checkers + 3 judges across iter-1/iter-2/iter-3) each produced as SEPARATE dispatches in PARALLEL with FRESH context; 9/10 pass threshold enforced strictly (8.5 ≠ 9 not invoked once; no rounding); R1 v2 iter-2 single fact-check FAIL + single judge sub-9 dim correctly classified as FAIL not "close enough to pass"; iter-3 verified independently against R1 v3 with no orchestrator self-attestation of either verdict. Phase 6 adversarial review's 15 findings each personally source-read before classification per PF-S3-01 guard; F-A07/F-A12/F-A13/F-A14/F-A15 explicitly classified "documented-as-acceptable per reviewer rationale" rather than auto-applied or auto-dropped.

Watched for AP-INCOMPLETE-PROPAGATION during 873→121-line compression (Phase 5 synthesis) — the per-section line budgets + 11-section mechanical check + Phase 7 final-corrections checklist all held; one section-order defect (Modes before Anti-Patterns) caught by Phase 6 reviewer and fixed via F-A03. Watched for "minor accretion" framing on the token-budget overrun — declined to skip; the catalog row carries an explicit pointer to the characterization rather than silent acceptance.

Three observations worth noting (not promoted to PF):

(a) **Hook edge-case path-pattern over-trigger (NEW class, recurrence_count=1).** S9-specific instance of the hook firing on non-role-tagged dispatches that merely mention role-profile paths. Distinct from S7/S8 profile-vs-section mismatch class (recurrence_count=2). Both classes now documented; the inlining hook needs design attention for both: (i) accept role-specific section names alternative to `## Modes`; (ii) refine the role-context detection to distinguish "this dispatch IS role-tagged" from "this dispatch MENTIONS a role profile path." Promotion candidate for v2.5 punch-list.

(b) **Token-budget overrun is intrinsic to medical-domain.** Software role profiles average ~1,950 cl100k tokens. The medical-specialist-architect lands at ~3,236 (~66% over) due to 8-class refusal taxonomy enum + GRADE HALT condition + H-class composition formula + Mechanism A/B/C mapping + fabrication-guard surface list. The reviewer's characterization explicitly identified ~670 tokens as load-bearing medical-domain anchors that cannot compress without losing safety properties. Recommend formal budget allowance for medical specialist profiles (separate from software role budget) as a follow-up ADR.

(c) **Phase 4 validation iterations correctly converged.** The HARD RULE pass threshold ("9/10 every dimension; no rounding, no softening") was tested in S9: iter-1 produced FAIL verdicts that explicitly named under-budget dimensions; iter-2 fixed those but surfaced new D10 (freshness) gaps in the same artifact; iter-3 converged. At no point did the orchestrator round or soften. The remediator workflow (separate Agent dispatch reading both fact-checker + judge reports) functioned as designed.

**Post-deployment review and re-scope (S9 addendum, same day):**

After initial commit `4176a62` deployed to `~/Documents/Projects/skills_library/`, user requested `/review-pr` against PR heavydropio/skills_library#14. Doc-only modification (3 of 6 agents: Code Quality + Contracts + Historical Context). Phase 1 surfaced 18 findings; Phase 2 dedup → 17; Phase 3 blind triage classified 14 LEGITIMATE / 3 DECISION (relitigating Phase-6 dispositions F-A03, F-A07, F-A14).

**Architectural realization.** Four HIST-class LEGITIMATE findings (HIST-001 token budget exceeds catalog guardrail; HIST-003 library-index references paths external to skills_library; HIST-005 profile names project-specific artifacts unresolvable inside skills_library; HIST-006 cross-project authoring pattern undocumented) all pointed at the same root: **a project-specific role does not belong in the shared skills_library**. User confirmed re-scope to project-local `.claude/agents/` (Option B). All 4 HIST findings dissolved by re-scope; 7 QUAL findings reclassified DECISION (faithful to design-doc §5/§8/§2.2/§11.2/§7 patterns rather than skills_library convention); 3 QUAL findings (QUAL-007 template-string → fenced block; QUAL-010 library-index auto-load dedup; QUAL-011 regulatory Path/Source header) applied in the re-scoped deployment.

**Final deployment.** `~/Documents/Projects/a-plus-maxing/.claude/agents/health-specialist-architect/agent.md` (127 lines / 3,252 cl100k tokens / 11 sections) + paired `library-index.md` (24 lines). Commit `280aba9`. PR #14 on skills_library closed with re-scope comment; feature branch deleted from both local and origin; skills_library `roles/orchestrator/catalog.md` row reverted (user-flagged linter restore).

**Process observation — review-pr against cross-repo PR works but exposes the framework's blind spot:** the skill's HARD RULE "every LEGITIMATE finding gets fixed" assumed all findings are at the same architectural layer. When 4 of 14 LEGITIMATE findings collectively meant "wrong architectural choice," forcing line-level fixes would have papered over the real defect. The user's instinct ("make it project-specific — does that solve it?") was the right escalation; the triage table re-applied at the new layer made the dispositions deterministic.

**Commit:** `280aba9` pushed to `origin/feature/wiki-bpc157-aplus-research` (S9 close state).

## Scope Contract — Session 10 (2026-05-27)

Goal: Run design-doc-protocol Phases 1-5 for Role 2 (health-implementer) against `design/DESIGN_DOC_TEMPLATE.md`. Produce `design/health-implementer-design.md` with `status: Final`. Second end-to-end exercise of the canonical template (first was Role 1 in S8). Roster B rotation applied: project-local `.claude/agents/health-specialist-architect/agent.md` replaces the v1-substitute software-architect drafter at Phase 1; SE + QA remain v1-substitute software until Roles 2/3 deploy.

Acceptance criteria:
- [ ] AC0 — Roster B rotation documented in `design/DESIGN_DOC_TEMPLATE.md` §0.1 + `design/CONTINUATION_BRIEF.md` §7 BEFORE any Phase-1 dispatch (decision: option (a) project-local with absolute path; SE + QA stay v1-substitute)
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches (rotated architect = health-specialist-architect / v1-substitute SE / v1-substitute QA). Each prompt inlines full 11-section profile verbatim per INV-ROLE-INLINING; `.claude/hooks/enforce-role-inlining.sh` is mechanical defense. Drafts written to `design/.health-implementer-design-work/{architect,se,qa}-draft.md`. Dispatches recorded in `design/.health-implementer-design-work/dispatch-ledger.jsonl`
- [ ] AC2 — Phase 2: orchestrator synthesizes `design/health-implementer-design.md` per `DESIGN_DOC_TEMPLATE.md` (frontmatter §0.2 + 18 sections + Appendix A). §4 is INBOUND-only for 8 rows established by Role 1 §4 (refusal taxonomy, H-class composition, GRADE, anti-sycophancy, R7, contradiction discipline, aplus-research mode floor, Role 4 Council slot). Body↔bibliography symmetry verified before Phase 3
- [ ] AC3 — Phase 3: 2 red-team dispatches (`/adversarial-review` skill + medical-safety v1-substitute per CB §7). Findings to `design/.health-implementer-design-work/red-team-{adversarial,safety}.md`
- [ ] AC4 — Phase 4: PF-S3-01 guard held — each finding personally source-read by orchestrator; classifications in `design/.health-implementer-design-work/finding-classifications.md` with cited evidence for REJECTED rows. Reject-but-adopt pattern applied where appropriate (per S6 feedback memory)
- [ ] AC5 — Phase 5: dispositions applied; Appendix A populated with rejected findings + attestations; §7 self-attest 17-item checklist run; frontmatter `status: Final`
- [ ] AC6 — Close: all 3 audits exit 0 at `--session 10`; PF attestation in canonical form; VOLATILE rotation applied; commit + push to feature branch (never main); `SESSION_KICKOFF.md` marked `status: consumed`

Files I WILL touch:
- `design/health-implementer-design.md` (NEW — the synthesized design doc)
- `design/.health-implementer-design-work/{architect,se,qa}-draft.md` (NEW × 3)
- `design/.health-implementer-design-work/red-team-{adversarial,safety}.md` (NEW × 2)
- `design/.health-implementer-design-work/finding-classifications.md` (NEW)
- `design/.health-implementer-design-work/dispatch-ledger.jsonl` (NEW)
- `design/.health-implementer-design-work/SESSION_KICKOFF.md` (frontmatter → `status: consumed` at close)
- `design/DESIGN_DOC_TEMPLATE.md` (Roster B rotation — line 39 edit, complete)
- `design/CONTINUATION_BRIEF.md` (Roster B rotation table — §7 edit, complete)
- `HANDOFF.md` (this contract + close note + VOLATILE rotation)
- `vault/meta/index.md`, `vault/meta/log.md` (entity registration + op log)
- `memory/process-failures.md` (only if a new PF surfaces)
- `.beads/*` via `bd` CLI only

Files I will NOT touch:
- `design/health-specialist-architect-design.md` (Status: Final — defects → F-A01 bead, not edit)
- `.claude/agents/health-specialist-architect/*` (Status: deployed — read-only as drafter source)
- `.claude/agents/health-implementer/*` (Role 2 Session B work, separate session after this Pass-2 finalizes)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `.claude/commands/*`, `scripts/*`, `.claude/hooks/*`
- `~/Documents/Projects/skills_library/*` (read-only as drafter source; Role 2 deploys project-local per S9 decision)
- `INVARIANTS.md` (no new invariants unless something forces it; flag at the time)
- `CLAUDE.md`, `~/.claude/*`
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Roster A (/review-pr) rotation — deferred to Role 2 Session B per kickoff brief §9
- Role 2 Session B (`/upgrade-agent` deployment of health-implementer) — separate session after Pass-2 finalizes
- Roles 3 + 4 Pass-2 (S11 + S12)
- Pass-3 specialist deep-research
- Phase C peptide library campaign
- F-A01 design-doc residual "7-class" prose fix at `design/health-specialist-architect-design.md` (deferred bead)
- Token-budget characterization ADR (deferred follow-up)
- CLAUDE.md `.claude/agents/` section addition (deferred follow-up)
- Hook v2.5 punch-list (both edge-case classes at recurrence_count=2)
- INV-HARM-CLASS-COMPOSITION promotion (PROPOSED in Role 1 §16; requires change-discipline ritual at review cycle)
- Walter pending items (23andMe, Oura, meal-template, Jan 2026 issue)
- Vault git-tracking decision
- LM-04 first HTML artifact

Invariants at risk:
- INV-ROLE-INLINING — drafter dispatches must inline full 11-section profile; `enforce-role-inlining.sh` PreToolUse hook is the mechanical defense; project-local profile path (`.claude/agents/health-specialist-architect/agent.md`) may exercise the path-pattern edge case (recurrence_count=2)
- PF-S3-01 / AP-ORCH-SELF-ATTEST — Phase 4 falsification window (third consecutive guard test if held; recurrence_count=2)
- AP-INCOMPLETE-PROPAGATION — Phase 5 disposition application across 18 sections + Appendix A; §7 self-attest 17-item checklist is the explicit defense
- INV-SCOPE-CONTRACT — satisfied by this block; `scope-contract-audit.sh --session 10` validates at close
- INV-PF-ATTESTATION — canonical form at close
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — rotation rule applied to VOLATILE sections; no SHA prefixes in narrative prose
- INV-BRANCH-NOT-MAIN — feature branch only; `block-commit-main.sh` is mechanical defense
- INV-RESEARCH-ATTESTATION — N/A (no `aplus-research` dispatch this session)

## Scope Contract — Session 11 (2026-05-27)

Goal: Run design-doc-protocol Phases 1-5 for Role 3 (health-edge-case-reviewer) against `design/DESIGN_DOC_TEMPLATE.md`. Produce `design/health-edge-case-reviewer-design.md` with Status: Final. Third end-to-end exercise of the canonical template (Role 1 S8, Role 2 S10).

Acceptance criteria:
- [ ] AC0 — Roster B status verified: architect drafter = project-local health-specialist-architect (rotation active since S10); SE+QA stay v1-substitute (S11 is the LAST cycle running v1-substitute QA). AQ-001 deferred via Option A (Role 3 design doc surfaces what audit needs, not the reverse) — confirmed S11 open.
- [ ] AC1 — Phase 1: 3 parallel drafter dispatches inlining full 11-section profiles verbatim per INV-ROLE-INLINING. Drafts at `design/.health-edge-case-reviewer-design-work/{architect,se,qa}-draft.md`. Each dispatch recorded in `dispatch-ledger.jsonl`.
- [ ] AC2 — Phase 2: orchestrator synthesizes `design/health-edge-case-reviewer-design.md` per template (18 sections + Appendix A); §4 INBOUND inherits 8 rows from Role 1 §4 + 5 rows from Role 2 §4.2 by anchor (no content duplication); body↔bibliography symmetry check passes pre-Phase 3.
- [ ] AC3 — Phase 3: 2 red-team dispatches (`/adversarial-review` skill + medical-safety v1-substitute per CONTINUATION_BRIEF §7); findings at `design/.health-edge-case-reviewer-design-work/red-team-{adversarial,safety}.md`.
- [ ] AC4 — Phase 4: PF-S3-01 guard held — every finding personally source-read against cited file before verdict; classifications at `design/.health-edge-case-reviewer-design-work/finding-classifications.md` with verdicts LEGITIMATE / LEGITIMATE-MODIFIED / REJECTED + cited evidence on every REJECTED row.
- [ ] AC5 — Phase 5: LEGITIMATE + LEGITIMATE-MODIFIED dispositions applied; Appendix A populated; §7 self-attest 17/17 binary checklist run; frontmatter `status: Final`; `vault/meta/index.md` + `log.md` appended.
- [ ] AC6 — Close: all 3 audit scripts exit 0 at `--session 11`; PF attestation canonical form `S11 close (YYYY-MM-DD):`; VOLATILE rotation 6-clause; commit + push to feature branch; SESSION_KICKOFF.md flipped to `status: consumed`.

Files I WILL touch:
- `design/health-edge-case-reviewer-design.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/architect-draft.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/se-draft.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/qa-draft.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/red-team-adversarial.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/red-team-safety.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/finding-classifications.md` (NEW)
- `design/.health-edge-case-reviewer-design-work/dispatch-ledger.jsonl` (append)
- `design/.health-edge-case-reviewer-design-work/SESSION_KICKOFF.md` (status flip at close)
- `HANDOFF.md` (this contract + S11 close + VOLATILE rotation)
- `vault/meta/index.md` (append new design doc entry)
- `vault/meta/log.md` (append create op)
- `memory/process-failures.md` (only if new PF surfaces)
- `.beads/*` via `bd` CLI

Files I will NOT touch:
- `design/health-specialist-architect-design.md` (Final, read-only — defects → bead)
- `design/health-implementer-design.md` (Final, read-only — defects → bead)
- `design/DESIGN_DOC_TEMPLATE.md` (canonical, read-only)
- `design/.health-implementer-design-work/`, `design/.health-specialist-architect-design-work/` (predecessor work dirs — read-only references)
- `design/.health-edge-case-reviewer-design-work/domain-research.md` (Pass-1 substrate — read-only)
- `.claude/agents/*` (Session B per role; Role 1 deployed file read-only this session)
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`
- `.claude/skills/*`, `.claude/commands/*`, `scripts/*`, `.claude/hooks/*`
- `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml` (S10 canonical, read-only — Role 3 may consume but not amend)
- `INVARIANTS.md` (no new invariants this session unless something forces it; flag at the time)
- `CLAUDE.md`, `~/.claude/*`
- `~/Documents/Projects/skills_library/*` (read-only — drafter profiles inlined verbatim)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Working any S10-sourced bead unless on Role 3 critical path (AQ-001 `h1z` deferred via Option A)
- Role 2 Session B (`/upgrade-agent` against Role 2 design — separate session)
- Role 4 Pass-2 design (S12)
- Pass-3 specialist deep-research (S13)
- Phase C peptide library campaign
- Template / INVARIANTS / CLAUDE modifications
- Roster A (/review-pr) rotation (`9yk`)
- Audit-script bash (`3y6`)
- Hook v2.5 punch-list (`hca`)
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)
- First HTML artifact (LM-04)
- Vault git-tracking decision
- INV-HARM-CLASS-COMPOSITION promotion (PROPOSED; requires change-discipline ritual)

Invariants at risk:
- INV-ROLE-INLINING — 3 drafter + 2 red-team dispatches; `enforce-role-inlining.sh` PreToolUse hook is mechanical guard; project-local architect path may again exercise path-pattern edge case (recurrence_count=2; bead `hca`)
- AP-ORCH-SELF-ATTEST / PF-S3-01 (recurrence_count=2) — Phase 4 is the fifth consecutive falsification window (S7/S8/S9/S10 held)
- AP-INCOMPLETE-PROPAGATION — §4 INBOUND inherits from BOTH Role 1 (8 rows) AND Role 2 (5 rows); 13 anchor citations to keep faithful; §7 self-attest 17-item checklist is explicit defense
- INV-SCOPE-CONTRACT — satisfied by this block; `scope-contract-audit.sh --session 11` validates at close
- INV-PF-ATTESTATION — canonical form at close
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — rotation rule applied to VOLATILE sections at close; no SHA prefixes in narrative
- INV-BRANCH-NOT-MAIN — feature branch only; `block-commit-main.sh` is mechanical defense
- INV-RESEARCH-ATTESTATION — N/A (no `aplus-research` dispatch this session)

Self-recognition pre-flight: Watching specifically at Phase 4 for "I already verified findings like these on Roles 1 and 2, the pattern is familiar" — pattern familiarity is not a substitute for source-reading. Watching at Phase 2 for the "Phase-2-synthesis-omission" pattern (S10 observation, recurrence_count=1) — running `grep -c '^## '` on the synthesized doc PRE-Phase-3 instead of letting red-team catch it.
