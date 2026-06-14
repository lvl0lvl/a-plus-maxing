---
title: Clone-init bd contract — the issue tracker is db-less-by-design dev tooling, not initialized by init_instance
type: decision
owner: Walter McGivney
created: 2026-06-14
last_reviewed: 2026-06-14
status: active
permalink: a-plus-maxing/decisions/2026-06-14-clone-init-bd-contract
---

# Clone-init bd contract (adopted 2026-06-14, S60)

Resolves bead `a-plus-maxing-vjsw` ("Clone-init contract never runs bd init: fresh clones
carry .beads/ without a db"). Records the adjudication of the bead's `bd-init-step` vs
`no-db-decision` fork. Operator decision: Walter, "C sounds right" (S60), on the third
disposition surfaced after verify-first.

## The problem the bead named

`.beads/` is tracked (`issues.jsonl`, `config.yaml`, `metadata.json`) but `beads.db` is
gitignored (`.beads/.gitignore` ignores `*.db`), so a fresh clone carries the issue records
without a database. `scripts/clone/init_instance.py` and `docs/clone-init.md` had **zero bd
references** — nothing in the clone contract accounted for bd. The bead's reported symptom:
`bd sync --flush-only` exits 1 (`no beads database found`) on a fresh clone (bd 0.49.0).

## What verify-first found (why the bead's two framings were both wrong)

The bead framed the fix as `bd-init-step` OR `no-db-decision` — both of which make bd
operational in the clone. The live behavior says neither is warranted:

1. **bd self-heals for normal use.** `config.yaml` ships `no-auto-import: false` (the
   default), so `bd list` / `bd ready` / `bd create` auto-import `issues.jsonl` and create
   `beads.db` on first use. Verified on a fresh fixture: `bd list` created the db and worked.
2. **Only `bd sync --flush-only` fails first-command** — it is the one command that does not
   auto-import; it errors with `no beads database found` plus its own "This looks like a fresh
   clone… Options:" guidance.
3. **Clone *commits* are already safe.** Per CLAUDE.md, the `block-pii-commit` hook skips the
   `bd sync --flush-only` flush when no database exists (PR #107 / bead `ycqo`) — so the one
   failing command does not block anything in a clone.
4. **bd is dev-tooling.** The `a-plus-maxing-*` issues track *building the project*, not the
   operator's health data. A health-app operator has no use for bd.
5. **`init_instance` is a documented THIN LEAF** (ADR-0005-T2, 0 outgoing dependency edges).

## Options considered

- **A — bd-init subprocess in `init_instance.run()`** (`bd init --from-jsonl`). REJECTED:
  couples dev-tooling into the pure product-init (violates the ADR-0005-T2 0-outgoing-dep
  design; the existing egress test pins run() as subprocess-free), needs `bd` installed,
  writes a stray `AGENTS.md` side-effect, and forces the tracker on operators who never use it.
- **B — `no-db: true` in the tracked `config.yaml`.** REJECTED: `config.yaml` is tracked, so
  this flips the **dev repo's** bd mode too — and the `block-pii-commit` hook depends on
  `bd sync --flush-only` in SQLite mode. Out of scope + risky for the dev workflow.
- **C — document the contract (ADOPTED).** `.beads/` ships db-less by design (the db is a
  local cache rebuilt from the tracked JSONL); bd self-heals on normal use; a contributor runs
  `bd init --from-jsonl` once. Document it in `docs/clone-init.md`, make the non-responsibility
  explicit in `init_instance`'s module docstring, keep `run` pure.

## The decision (Option C)

`init_instance.run()` does NOT initialize bd. The clone-init contract documents that `.beads/`
is db-less-by-design dev-tooling: a health-app operator ignores it; a contributor runs
`bd init --from-jsonl` (bd auto-imports on most commands; only `bd sync --flush-only` needs the
db first). This closes the "zero bd references / no contract" gap honestly without coupling the
THIN-LEAF product-init to the dev tracker.

## Consequences

- **Positive:** `init_instance` stays a 0-outgoing-dependency THIN LEAF (no `bd` install
  dependency, no subprocess, no `AGENTS.md` side-effect); the dev repo's SQLite bd mode is
  unchanged (the PII hook's flush still works); the clone contract is now complete + honest.
- **Negative (accepted):** a contributor who runs `bd sync --flush-only` as their literal first
  command on a never-touched clone still gets `no beads database found` — but bd's own message
  guides them, and the documented `bd init --from-jsonl` resolves it. The health-app operator,
  the V1 target, is unaffected (they ignore `.beads/`).

## Falsification

`tests/clone/test_init_instance.py` pins the decision: `init_instance.run()` over a clone
carrying a tracked `.beads/issues.jsonl` creates no `.beads/beads.db` (REDs if a bd-init step
is ever added to `run`, forcing a conscious decision-reversal), and `docs/clone-init.md` carries
the bd-tracker contract section (RED before this change — the doc had zero bd references).
