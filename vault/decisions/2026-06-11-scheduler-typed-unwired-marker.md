---
title: Scheduler wired-set membership marker is a typed module attribute (UNWIRED = True), not docstring prose
type: decision
permalink: a-plus-maxing/decisions/2026-06-11-scheduler-typed-unwired-marker
created: 2026-06-11
status: active
decided_by: S51 build dispatch (bead a-plus-maxing-7lt); mechanism latitude granted by the ADR-0003-T3 recipe
supersedes: null
relates_to: null
---

# Scheduler wired-set membership marker is a typed module attribute, not docstring prose

## Decision

The ingest scheduler's wired-set membership marker is a **typed module-level
attribute**: an adapter module in `scripts/ingest/adapters/` is excluded from the
unattended wired set iff it declares `UNWIRED = True`. **Absence of the
declaration means wired** — the `getattr(module, "UNWIRED", False)` default in
`scheduler._wired_adapters()` IS the contract's default-membership clause
(wired-by-default, identical semantics to the prior absence-of-marker rule), not
a defensive fallback. Docstring prose never affects membership.

This replaces the S40 mechanism, which excluded any adapter whose module
docstring contained the substring `"unwired"` (`_UNWIRED_MARKER` in
`scheduler.py`).

## Context / problem (bead a-plus-maxing-7lt)

The docstring-substring rule made natural-language prose load-bearing for
wired-set membership, with two failure modes:

- **(i)** A future wired adapter whose docstring legitimately mentions the word
  "unwired" would be **silently dropped** from the unattended run. This direction
  was NOT test-guarded.
- **(ii)** If `whoop.py`'s docstring were reworded, Whoop would be **silently
  re-included** in the wired set — the dangerous direction AC-4 (ADR-0003-T3)
  exists to prevent. Guarded only by S40 tests that pinned the fragile mechanism
  itself, pending this fix.

No ADR/spec text pinned the substring: the ADR-0003-T3 recipe (line 99) requires
only "interface conformance + a wired marker", leaving the mechanism
implementer-chosen — so this is a mechanism amendment recorded here (the
vault-native decision owner), with NO change to ADR-0003, the spec, or the frozen
task plan.

## Options considered

- **(a) Typed opt-out attribute (`UNWIRED = True`; absence = wired)** — CHOSEN.
  Preserves the wired-by-default contract verbatim, keeps the AC-6
  0-edit-adapter-add property (a new conformant module with no attribute joins
  the wired set with 0 scheduler edits), and keeps `scheduler.py` free of any
  per-source token (AC-4b: 0 `whoop` tokens).
- **(b) Opt-in registry** (the bead's floated alternative) — REJECTED. Inverts
  default membership: forgetting to register a new adapter becomes a silent data
  drop, and the registry edit breaks AC-6's 0-edit-add property
  (`test_adapter_add_zero_scheduler_edits` would RED).

## Resolution applied (S51)

- `scripts/ingest/scheduler.py`: `_UNWIRED_MARKER` substring check replaced by
  `_UNWIRED_ATTR = "UNWIRED"` + `getattr(module, _UNWIRED_ATTR, False)`;
  docstrings/comments state the wired-by-default contract explicitly.
- `scripts/ingest/adapters/whoop.py`: declares `UNWIRED = True`. Its docstring
  still says "unwired" — no longer load-bearing, which is the point.
- `tests/ingest/test_scheduler.py`: the two S40 mechanism guards rewritten to the
  typed marker (`test_whoop_carries_unwired_attribute`,
  `test_unwired_marker_governs_wired_set_membership` with fixtures differing only
  by the attribute), plus the previously missing fragility-(i) guard
  (`test_docstring_unwired_prose_does_not_exclude`: docstring prose mentioning
  "unwired" with no attribute stays wired — RED against the retired substring
  mechanism).

## Conditions for revisiting

- A need arises to carry unwired-ness OUTSIDE the adapter module (e.g.
  operator-toggled wiring without editing the adapter file) → that is a
  configuration surface, not a marker rename; design it as its own decision.
- The adapter contract (`adapter.py`) is ever formalized into a richer
  registration object → fold the marker into that surface then, not before.
