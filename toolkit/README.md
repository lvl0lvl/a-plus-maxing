---
title: "Rigor Toolkit — runnable enforcement layer"
type: guide
owner: framework
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
review_cadence: manual
---

# Rigor Toolkit

The **runnable** half of the Rigor Framework. The framework document describes
the disciplines; this toolkit *ships the mechanical enforcement* so a project
gets a real day-one floor instead of 30 sessions of un-enforced prose.

> **Why this exists (Finding F-012):** across four long-running deployments, the
> single consistent gap was that the framework *described* its `[MECH]` layer but
> shipped only prose — so every painful drift was a runnable artifact nobody ever
> built. This directory is that artifact, assembled from the best field versions.

## The one rule that makes it trustworthy (F-007)

Every audit/hook ships **with a negative test that is executed** to prove it goes
RED on bad input. An audit that only proves it PASSes on good input is a
*false-green waiting to happen* — exactly the failure that recurred in the field
(a stale-hash audit with a broken `\b` regex that passed unconditionally; a
10/10 judge that rubber-stamped a fabricated claim). Run `tests/run-all-tests.sh`;
if a check can't prove it fails, it doesn't ship.

## Layout
```
toolkit/
├── lib/
│   ├── audit-helpers.sh   # emit/fail/warn/skipped/verdict; exit 0=PASS 1=FAIL 2=FATAL
│   ├── test-lib.sh        # expect_exit, assert_red_when_guard_removed
│   └── gate_attest.py     # gated-attestation engine (PF-S3-01); project-configurable via $GATE_ATTEST_CONFIG; needs python3+jsonschema
├── hooks/                 # PreToolUse hooks (wire into .claude/settings.json)
│   ├── enforce-role-inlining.sh   # F-002: full 11-section profile; accepts Modes|Audit Protocol|Task Routing
│   ├── block-dangerous.sh         # rm -rf /, git reset --hard, push --force (allows --force-with-lease), clean -fd
│   ├── block-push-main.sh         # deny push to main/master
│   ├── block-commit-main.sh       # deny direct commit to main
│   ├── enforce-heartbeat-clause.sh# agent-liveness / 0-silent-drops on dispatch
│   ├── enforce-commit-gate.sh     # CDM-1-14 (ADR-0001): DENY a commit over a RED $RIGOR_COMMIT_GATE roster; persists .rigor/commit-gate-verdict.json
│   ├── enforce-pr-readiness.sh    # CDM-1-21 (ADR-0002/0006): DENY gh pr create unless verdict reads GREEN, is SHA-bound to HEAD, AND a pr-authorized marker is present
│   └── enforce-merge-readiness.sh # ADR-0007: DENY gh pr merge unless .rigor/review-verdict.json reads CLEAN and is SHA-bound to HEAD (mechanical merge authorization; the 4th boundary gate)
├── scripts/               # session-close + audit gates
│   ├── rotation-stamp-audit.sh    # F-009: VOLATILE sections may only stamp {n-1,n,n+1,n+2}
│   ├── stale-hash-audit.sh        # no bare sha/commit hashes in narrative prose (correct regex)
│   ├── pf-attestation-audit.sh    # close must append a PF entry OR an explicit "no PF" attestation
│   ├── falsification-scan.sh      # advisory: flags the 4 falsification anti-patterns (CDM-8-10)
│   ├── close-audit.sh             # the mandatory close GATE: runs the others; FATALs if any can't RUN (F-008)
│   ├── design-gate.sh             # per-recipe DESIGN [MECH] gate: runs the vendored impeccable detector on changed UI files, fails CLOSED on blocking findings (RIGOR_DESIGN_GATE dial; needs node+python3)
│   ├── parity-audit.sh            # F-022: catalog<->disk<->deployed parity; dead refs/symlinks (the ~44%-broken class)
│   ├── consistency-audit.sh       # F-019/020/006/005: hook<->pipeline, nonexistent-role dispatch, threshold + protocol consistency
│   ├── role-completeness-audit.sh # at-rest twin of enforce-role-inlining: every roles/<slug>/agent.md carries the 11 canonical sections (per-harvest; optional PyYAML frontmatter lint)
│   ├── harvest-gate.sh            # F-017: a failure must be in PF + harvest.jsonl + a bead, or the close fails
│   ├── pf-ingest.sh               # F-018: turn a PF entry into a harvest record + the anti-pattern that hardens its role/skill
│   ├── run-attest.sh              # F-011 (ADR-0003): tool runs a designated command + sha-chains the captured output (capture-at-source)
│   ├── hygiene-audit.sh           # ADR-0004: G4 PF/vindication count-reconciliation + G6 bead close-reason rationale (per-close)
│   ├── pf-severity-audit.sh       # ADR-0004: G5 PF severity-monotonicity / no silent downgrade (per-harvest cadence)
│   ├── watchdog.sh                # ADR-0005: companion-watchdog active supervision (register/heartbeat/poll/close; no-args==poll); per-close (in DEFAULT_ROSTER)
│   ├── version-bump-audit.sh      # D11 forward guard (bd1): FAIL when watched toolkit paths changed since the last VERSION commit, or are dirty while VERSION is clean; per-harvest / pre-release
│   ├── update-rigor.sh            # D11 runnable pull: diff pinned rigor_version vs central VERSION, re-copy toolkit, re-run run-all-tests.sh as the gate (rollback-on-RED), re-pin; the /update-rigor command
│   ├── pen-lint.sh                # design-overhaul §6.1: design-time lint over the Interaction-Model exports
│   ├── pen-digest.sh              # design-overhaul §5: content digest over the export set (bare hash; export.digest wraps it)
│   ├── pen-integrity.sh           # design-overhaul §6.2: export-integrity gate (hand-edit FAIL) + pen-change trigger (PEN-CHANGED wave-close block)
│   ├── pen-saved-check.sh         # design-overhaul §5 PA-5 (b30): saved-state precondition — arm/verify/check save-witness; extraction from unsaved editor state cannot pass
│   ├── wiring-gate.sh             # design-overhaul §6.3 static: res-1 (data-oid+handler) + res-2 (route+schema join) under wave semantics
│   ├── seam-gate.sh               # design-overhaul §6.4 RUNTIME: statechart-driven crawl verdict (needs harness/ node+Playwright)
│   └── res3-gate.sh               # design-overhaul §6.3 res-3 RUNTIME: executed E2E + dual mutation proofs (needs harness/)
├── harness/                       # QUARANTINED node/Playwright runtime for the two runtime gates (static gates stay bash+python)
│   └── pen-harness.mjs            # post-hydration crawl (seam) + e2e mode (res-3); playwright pinned in package.json
├── schemas/
│   └── harvest-record.md          # the machine-readable evidence layer (harvest.jsonl), the automation's contract
├── SELF_IMPROVEMENT_PLAYBOOK.md   # F-017: the operational loop (Loop A per-artifact + Loop B cross-deployment)
└── tests/                 # one negative test per component + run-all-tests.sh
```

## The three master mechanisms (cross-cutting)
Most library defects collapse into three patterns; these three gates cure them in bulk:
- **`parity-audit.sh`** — the *described-but-not-shipped* disease (F-012/F-022): catalog↔disk↔deployed parity, fail-closed. One gate catches the whole "~44% non-functional as installed" class.
- **`harvest-gate.sh` + `pf-ingest.sh` + `schemas/` + the PLAYBOOK** — the *dead learning wire* (F-018/F-017): a failure must be captured in all three layers (PF narrative + machine `harvest.jsonl` + bead) or the close fails, and `pf-ingest` turns it into the anti-pattern that permanently hardens the role/skill that caused it.
- **`consistency-audit.sh`** — *self-inconsistency* (F-019/020/006/005): the library is not allowed to contradict itself (the hook denying its own pipeline, dispatching a nonexistent role, disagreeing thresholds, competing close protocols).

## Gated attestation (`lib/gate_attest.py`) — optional, for gated research/review pipelines
Cures the *orchestrator-self-attestation* disease (PF-S3-01: an orchestrator declares a blocking gate PASSed by writing the gate JSON itself from prose). Mechanical chain: `start-iteration` stamps an iteration clock → a **dispatched verifier** writes `gate-N.md` (a `## Verdict` block + the schema-required structured fields as a fenced ` ```json ` block) → `attest` composes `gate-N.json`, re-deriving the verdict from the markdown and schema-validating it → `verify-chain` re-hashes the sources to catch post-attest edits. The engine is **domain-neutral**: a project supplies its own gate schemas + phase set + per-phase source files via `$GATE_ATTEST_CONFIG` (`{schema_dir, attested_gates, source_md}`); defaults are a worked example. Built + battle-tested in a-plus-maxing's `aplus-research`, promoted here so any gated pipeline inherits it — and the **AR-6** (per-iteration freshness; partial remediation can't false-stale earlier-passed sections) + **AR-7** (structured fields via a fenced json block) fixes. Requires `python3` + `jsonschema`; `tests/test-gate-attest.sh` skips loudly when absent.

## Exit-code contract (F-008)
`0` PASS · `1` FAIL (real violation) · `2` FATAL (config/env error **or** a check
was SKIPPED). **SKIPPED is fail-closed by default** — "couldn't verify" never
equals "verified clean." Override per-run with `AUDIT_ALLOW_SKIP=1` only when a
skip is genuinely acceptable.

## Install (per project)
1. Copy `toolkit/` into the project (or reference it).
2. Wire the hooks into `.claude/settings.json` PreToolUse using
   `${CLAUDE_PROJECT_DIR}/...` paths (never absolute — F-003).
   **Dispatch-gating hooks have a wiring precondition (convergent: a-plus + safety-platform
   adoptions).** `enforce-role-inlining.sh` and `enforce-heartbeat-clause.sh` fire on Task
   dispatches — the heartbeat hook on *every* Task dispatch — and DENY any that don't satisfy
   the gate. If a flow you depend on dispatches agents that don't yet carry the full profile /
   the liveness clause (e.g. a multi-agent skill like `/review-pr` invoking its own internal
   agents, or the landing PR's own review), wiring the hook blind will **block that flow**.
   Wire the three Bash hooks (`block-dangerous`, `block-push-main`, `block-commit-main`) on day
   one; wire each dispatch-gating hook only AFTER verifying every Task-dispatching flow it
   governs already satisfies it. Both adopters deferred the heartbeat hook for exactly this
   reason — vendor it, document the precondition, wire when the dispatch convention carries the clause.
   The two commit/PR-boundary gates also wire on day one but need a little config before they
   bite (ADR-0001/0002): `enforce-commit-gate.sh` reads `$RIGOR_COMMIT_GATE` (the per-commit
   roster command; unconfigured → loud SKIP + ALLOW, never a false-block) and writes
   `${CLAUDE_PROJECT_DIR}/.rigor/commit-gate-verdict.json` — SHA-BOUND to the certified commit's
   parent set since ADR-0006; `enforce-pr-readiness.sh` consumes that verdict
   (absent/non-GREEN/unbound-to-HEAD → DENY) plus a `pr-authorized` readiness marker. Set
   `$RIGOR_COMMIT_GATE` and define the marker as you wire them (`fresh-start` scaffolds both
   by default, so absence-of-protection becomes the visible act of removing a tracked config).
   **The merge gate (`enforce-merge-readiness.sh`, ADR-0007) needs one operator action to be an
   AUTONOMY enabler rather than just a second block.** It DENIES `gh pr merge` unless
   `.rigor/review-verdict.json` (written by `/review-pr` on a CLEAN pass) reads CLEAN and is
   SHA-bound to HEAD. On its own it is fail-closed protection; to make the autonomous loop ROLL
   (merge without a human WHEN review ran CLEAN), also relax the harness auto-mode classifier so
   it stops blocking the command, letting this hook be the sole mechanical authority — add a
   settings permission rule allowing the merge, e.g. in `.claude/settings.json`:
   `{"permissions": {"allow": ["Bash(gh pr merge:*)"]}}`. Without the rule the classifier still
   blocks (safe, not autonomous); with it, rigor's fail-closed hook is the gate. Do NOT wire the
   hook expecting autonomy without the settings rule, and do NOT add the settings rule without
   the hook wired (that removes the gate entirely).
3. Add `scripts/close-audit.sh` to the session-close protocol (it blocks the
   close on any FAIL/FATAL and runs `tests/run-all-tests.sh` first).
4. Most scripts parameterize their target via args/env (continuity-doc path,
   current session N, PF-log path) with sane defaults.

## Lineage
Sourced + generalized from the best field implementations: `audit-helpers` +
`close-audit` (maquette FATAL≠clean-pass), `enforce-role-inlining` v2.5 synonyms
+ PII patterns + provenance (a-plus-maxing), `enforce-heartbeat-clause` +
rotation/stale-hash discipline (Quant). `falsification-scan` is framework-authored
(no project shipped it — a convergent absence).

**S17 ADR wave (`../docs/adr/ADR-0001..0004`) — five guards added in 1.3.0**, each
framework-authored against an S17-reconciliation GENUINE-UNBUILT failure class and
shipping its F-007 negative test:
- `hooks/enforce-commit-gate.sh` — commit-time fail-closed gate (CDM-1-14). Provenance: ADR-0001; closes giq.1.6 (commit-over-failing-gate) + giq.1.3 (silent gate-drift). Persists `.rigor/commit-gate-verdict.json` (the ADR-0002 read interface; SHA-bound via `certified_parent` since ADR-0006).
- `hooks/enforce-pr-readiness.sh` — no-premature-PR gate (CDM-1-21). Provenance: ADR-0002; the F-005 residual. Consumes ADR-0001's verdict artifact + a `pr-authorized` marker; since ADR-0006 the verdict must be BOUND to HEAD (certified_parent == HEAD's raw parent set), replacing the reverted wall-clock freshness (fail-open on un-gated/merge/shallow HEADs).
- `scripts/run-attest.sh` — executed-verification capture-at-source. Provenance: ADR-0003; mechanizes F-011, closes giq.3.6 / giq.3.3. Reuses `gate_attest.py`'s sha256 chain primitives as the anti-tamper layer.
- `scripts/hygiene-audit.sh` — PF/bead hygiene G4 (count-reconciliation) + G6 (close-reason rationale). Provenance: ADR-0004; closes giq.3.7 / giq.5.2. Per-close (in `close-audit.sh` `DEFAULT_ROSTER`).
- `scripts/pf-severity-audit.sh` — PF severity-monotonicity G5 (no silent downgrade). Provenance: ADR-0004; closes giq.4.2. Per-harvest / pre-release cadence (NOT the close roster — git-history dependency held off the critical path).

**S17 watchdog wave (`../docs/adr/ADR-0005`) — companion watchdog added in 1.4.0**, framework-authored as the runtime complement to the dispatch-time `enforce-heartbeat-clause.sh` and shipping its F-007 negative test:
- `scripts/watchdog.sh` — companion-watchdog active supervision (`register`/`heartbeat`/`poll`/`close`; no-args == `poll`) over a plain-file registry under `${CLAUDE_PROJECT_DIR}/.rigor/`. Provenance: ADR-0005; closes giq.1.7 (passive-supervision / companion-omission). The active runtime sibling of `enforce-heartbeat-clause.sh`: the hook proves the liveness clause is present at dispatch, the watchdog detects whether the heartbeats it promises actually arrive (catching the register-then-never-heartbeat drop-at-t=0 case). Wired into `close-audit.sh`'s `DEFAULT_ROSTER` (per-close) so `poll` self-triggers at every session boundary.

The full per-practice provenance
matrix and the F-numbered findings live in the meta-harness *distillation* project
that produced this toolkit (its `vault/matrix/` + `vault/findings/findings-log.md`),
not in this library — they are not shipped here. The per-deployment adoption logs
that the harvest consumes ARE shipped, in [`../deployments/`](../deployments/).

This section owns **per-script field-provenance** only. Discipline-level change
history lives in the framework's changelog, `../CHANGELOG.md`.

## Writing checkable RESUME claims (resume-claims-audit)

`scripts/resume-claims-audit.sh <doc>` verifies a continuity doc's `VOLATILE` region
against tracker/git reality. Claims written in these forms get verified; anything else
is counted as unparsed coverage (visible, never guessed at):

- bead status — ONE backticked token + a status keyword (open/closed/done/
  in_progress/blocked/ready — not "next") per sentence:
  ``bead `proj-ab1` is open`` / ``the fix for `proj-ab1` is closed``
  (two tokens sharing one keyword is ambiguous binding → counted unparsed)
- trunk position — ``main @ `<sha>` `` (FAIL off-main; WARN when main moved past)
- landed PR — ``landed in #NN`` / ``merged (#NN)`` (verified on the trunk log)
- a `YYYY-MM-DD` stamp anywhere in the region drives the staleness heartbeat

A region with zero parseable claims is loudly `PASS-VACUOUS` — a claim-free resume is
not a verified resume. Adoption is per-doc: no VOLATILE heading → loud SKIP, exit 0.
