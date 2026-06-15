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
│   └── test-lib.sh        # expect_exit, assert_red_when_guard_removed
├── hooks/                 # PreToolUse hooks (wire into .claude/settings.json)
│   ├── enforce-role-inlining.sh   # F-002: full 11-section profile; accepts Modes|Audit Protocol|Task Routing
│   ├── block-dangerous.sh         # rm -rf /, git reset --hard, push --force (allows --force-with-lease), clean -fd
│   ├── block-push-main.sh         # deny push to main/master
│   ├── block-commit-main.sh       # deny direct commit to main
│   └── enforce-heartbeat-clause.sh# agent-liveness / 0-silent-drops on dispatch
├── scripts/               # session-close + audit gates
│   ├── rotation-stamp-audit.sh    # F-009: VOLATILE sections may only stamp {n-1,n,n+1,n+2}
│   ├── stale-hash-audit.sh        # no bare sha/commit hashes in narrative prose (correct regex)
│   ├── pf-attestation-audit.sh    # close must append a PF entry OR an explicit "no PF" attestation
│   ├── falsification-scan.sh      # advisory: flags the 4 falsification anti-patterns (CDM-8-10)
│   ├── close-audit.sh             # the mandatory close GATE: runs the others; FATALs if any can't RUN (F-008)
│   ├── parity-audit.sh            # F-022: catalog<->disk<->deployed parity; dead refs/symlinks (the ~44%-broken class)
│   ├── consistency-audit.sh       # F-019/020/006/005: hook<->pipeline, nonexistent-role dispatch, threshold + protocol consistency
│   ├── harvest-gate.sh            # F-017: a failure must be in PF + harvest.jsonl + a bead, or the close fails
│   └── pf-ingest.sh               # F-018: turn a PF entry into a harvest record + the anti-pattern that hardens its role/skill
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

## Exit-code contract (F-008)
`0` PASS · `1` FAIL (real violation) · `2` FATAL (config/env error **or** a check
was SKIPPED). **SKIPPED is fail-closed by default** — "couldn't verify" never
equals "verified clean." Override per-run with `AUDIT_ALLOW_SKIP=1` only when a
skip is genuinely acceptable.

## Install (per project)
1. Copy `toolkit/` into the project (or reference it).
2. Wire the hooks into `.claude/settings.json` PreToolUse using
   `${CLAUDE_PROJECT_DIR}/...` paths (never absolute — F-003).
3. Add `scripts/close-audit.sh` to the session-close protocol (it blocks the
   close on any FAIL/FATAL and runs `tests/run-all-tests.sh` first).
4. Most scripts parameterize their target via args/env (continuity-doc path,
   current session N, PF-log path) with sane defaults.

## Lineage
Sourced + generalized from the best field implementations: `audit-helpers` +
`close-audit` (maquette FATAL≠clean-pass), `enforce-role-inlining` v2.5 synonyms
+ PII patterns + provenance (a-plus-maxing), `enforce-heartbeat-clause` +
rotation/stale-hash discipline (Quant). `falsification-scan` is framework-authored
(no project shipped it — a convergent absence). See `vault/matrix/` for the
per-practice provenance and `vault/findings/findings-log.md` for the F-numbers.

This section owns **per-script field-provenance** only. Discipline-level change
history lives in the framework's changelog, `../CHANGELOG.md`.
