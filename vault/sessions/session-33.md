---
title: Session 33 — Wave-3 wired adapters (ADR-0003-T2 / n9h)
type: session
created: 2026-06-05
status: complete
permalink: a-plus-maxing/sessions/session-33
---

# Session 33 (2026-06-05) — Wave-3 wired adapters (ADR-0003-T2)

One deliverable, one PR, rebase-merged to `main` (PR #50 @ `aab93cc`): the four
per-source ingestion adapters that implement the frozen `ADR-0003-T1` `Adapter`
Protocol, built by a dispatched SE worker through the recipe's 4-cycle/16-step TDD,
then a full 6-agent `/review-pr` + blind triage + blind verify (PF-S3-01 —
load-bearing because ONE SE built everything, Walter's explicit condition). Closed
`n9h`; `oaf` (ADR-0003-T3 scheduler) unblocked.

## Published interfaces (durable contract record)

Four adapter modules under `scripts/ingest/adapters/`, each a plain class IMPLEMENTING
the frozen `ADR-0003-T1` Protocol (`source_tag(self) -> str` + `read_readings(self,
export_file) -> Iterable[dict]`) and run through the **UNCHANGED** `ingest.run`. Each
maps its own export shape into the `keying.LINE_FIELDS` store reading shape
`(item, timepoint, source, value)`; all per-source format specifics live inside
`read_readings`:

- **`healthkit.py`** — `HealthKitAdapter`, `source_tag()="healthkit"`; maps `type`/`startDate`/`qty`.
- **`oura.py`** — `OuraAdapter`, `source_tag()="oura"`; maps `metric`/`day`/`average`.
- **`garmin.py`** — `GarminAdapter`, `source_tag()="garmin"`; maps `summaryType`/`calendarDate`/(`valueInMillis` if present else `value`). The dual measurement-field branch is the format-rename absorption (AC-6): the renamed field maps to the same `value` store field, so the `(item,timepoint,source)` dedupe key is re-derived unchanged.
- **`whoop.py`** — `WhoopAdapter`, `source_tag()="whoop"`; maps `metric_name`/`cycle_start`/`score`. The registered-but-**UNWIRED** scaffold (ADR-0003 Risk N2): fully conformant (not a crippled stub), but no entry point wires it — until a later task adds it to the scheduler's data-driven set, Whoop data narrows to `ingest.manual_entry`. "Unwired" is a property of the absent scheduler wiring, not of the adapter.

`isinstance(adapter, Adapter)` holds for all four (the contract is a
`@runtime_checkable typing.Protocol`; the adapters satisfy it structurally). No
`__init__.py` is needed — `scripts.ingest.adapters.<name>` resolves as a namespace
package via the repo-root `conftest.py` sys.path. This task published NO new shared
interface; it implements an existing one. The wired set (HealthKit+Oura+Garmin) is
consumed by `ADR-0003-T3`'s scheduler, which owns the wired-set declaration.

## The two 0-shared-routine-edit extensibility proofs (the load-bearing evidence)

`tests/ingest/test_adapters.py` carries the ADR-0003 source-extensibility criterion as
two `git diff --numstat` proofs over `scripts/ingest/ingest.py` + `scripts/ingest/adapter.py`,
each against a DISTINCT committed-tree baseline (`pre-garmin` Cycle 2 AC-3;
`pre-format-rename` Cycle 4 AC-6). The pass condition is an EMPTY numstat (an unchanged
path emits no row); the merged commit's `git diff origin/main HEAD --` over those two
paths is empty (the seam did not leak).

**The falsifiability fix (the session's central correctness thread).** The baseline
mechanism went through two corrections before it was sound:

1. The recipe specified transient local tags via `git stash create` — those live only in
   `.git/refs` and would ERROR in a fresh review checkout. The SE switched to a
   `git commit-tree`-built baseline so it regenerates deterministically.
2. But the SE's `commit-tree` was over **HEAD's** tree, making the baseline HEAD-relative
   — `git diff --numstat <baseline> -- …` then compares HEAD-content vs the working tree,
   which is **always empty in a clean checkout regardless of whether the task edited the
   shared routine**. Tautological. Orchestrator independent verification caught it BEFORE
   review and proved it empirically (a committed one-line edit to `ingest.py` was MISSED by
   the HEAD-relative baseline but CAUGHT by the entry/fork-point baseline). Fixed to a
   baseline built over the **FORK-POINT tree** (`git merge-base HEAD origin/main`), which
   carries the pre-task blobs and reds on a committed edit.

The review (TEST-001) then found the *negative-control* tests exercised `git diff
--no-index` against a probe copy — a different code path than the main assertion's
`_numstat_rows(_baseline_ref(...))` — so they didn't prove the real gate could turn red.
The fix added a **committed-probe falsifiability test** that drives the real path; the
orchestrator teeth-checked it (neutered `_baseline_ref` to HEAD-relative → the test
FAILS; restored → passes). Lesson: a working-tree edit is caught by any baseline and
cannot prove a baseline is non-tautological — only a COMMITTED probe distinguishes them.

## Review outcome (PR #50)

6-agent `/review-pr` → 12 findings → blind triage → **7 LEGITIMATE** (all fixed + 7/7
blind-verified RESOLVED), 3 NOT_A_BUG, 2 NOT_ACTIONABLE; **0 suppressed** (PF-S26-01;
the 5 no-action findings each FAILED the 6-condition legitimacy test, not a severity
gate). The standouts:

- **HIST-001** — the adapter path is a NEW untrusted-`item` entry point (export field →
  `reading["item"]` → `ingest.run` → `store.append` → `store._item_path`, the S32 SEC-001
  guard). The guard holds, but had no adapter-path regression test → added a parametrized
  traversal test (`../escaped/pwn`, absolute, `a/b` → `ValueError`, nothing written outside root).
- **TEST-001** — the falsifiability hole above → committed-probe test.
- **TEST-002** — the Whoop unwired-gate regex missed `import scripts.ingest.adapters.whoop as w` → broadened + 3-form negative control.
- **TEST-004** — cross-source non-dedupe (same item+timepoint, different `source` must NOT collapse) was unproven → added.
- 3 QUAL — garmin docstring proof-narrative trimmed; triplicated baseline rationale reduced to a `_baseline_ref` pointer; `import re as _re` moved to the top-of-file block.

Security/Bug-Hunter/Contracts returned 0 findings and independently confirmed the
fork-point 0-edit proofs are non-tautological (re-deriving the fix's correctness without
being told about it), the 0-egress boundary (adapters import only `json`/`pathlib`/`typing`),
and exact Protocol conformance.

## Recipe↔built drifts (surfaced, not silently followed)

- Baseline mechanism: `git stash create` tags → `commit-tree` over the fork-point tree (portability + correctness; see above).
- AC-5's literal `rg "whoop" scripts/ingest/scheduler.py = 0` is deferred to the Wave 4→5 boundary — `scheduler.py` is `ADR-0003-T3`'s deliverable and does not exist yet; the T2-ownable assertion (Whoop importable+conformant AND no wiring ref in any shipped adapter file) is tested instead.
- `rg` is a non-executable shim → in-test static scans are pure-Python (`re`/`pathlib`).
- `/write-tests` is not invocable from a dispatched worker → the SE authored RED tests directly.
- Namespace-package import works without `__init__.py` → the 5-file manifest holds (no 6th file).

## Carried forward

- **`oaf` (ADR-0003-T3 scheduler)** is now READY (unblocked by `n9h`): unattended `ingest.run`
  over the wired set (HealthKit+Oura+Garmin), delta-only, 0-egress; Whoop excluded. The literal
  `rg "whoop" scheduler.py = 0` Wave 4→5 boundary check lands there once `scheduler.py` exists.
- Still open from prior reviews: `1vi` P3 (PR #47, re-ingest can't correct a value), `1ww` P2 /
  `qwj` P2 / `ivt` P3 / `z2u` P3 (PR #44). S33's review produced 0 new carry-forward beads.
- Parallel-ready frontier: `gu4` (render, unblocks the most downstream), `xlu` (pre-commit hook —
  resolve `qwj` first), `br1` (router spike).

Links: [[session-32]] (the store-hardening + the ingestion routine/`Adapter` Protocol this session's adapters implement).
