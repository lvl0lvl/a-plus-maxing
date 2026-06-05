---
title: Session 31 — Execute Wave 2 (store + PII/egress guard) + shareability
type: session
created: 2026-06-05
status: complete
permalink: a-plus-maxing/sessions/session-31
---

# Session 31 (2026-06-05) — Wave 2 of the V1 build

First **production-code** session. Built the two dependency-free Wave-2 modules
through their recipes' real-`pytest` TDD cycles, ran a full 6-agent `/review-pr`
(15 legitimate findings — 13 fixed, 2 beaded; 5 beaded total, 0 suppressed), made the PII scanner +
governance tooling **shareable** (operator name externalized to a gitignored
config, Walter-directed), and merged via PR #44 (`4efe907`). Closed `89a` + `e9m`.

## Built modules (published interfaces — durable provenance)

The deliverables are tracked code on `main`; this section is the at-a-glance
contract record so a future session need not re-read the source to know the surface.

### `scripts/store/keying.py` (ADR-0002-T1) — the single store-key definition
- `LINE_FIELDS = ("item", "timepoint", "source", "value")` — the Line Field Set.
- `DEDUPE_FIELDS` — **derived** as `tuple(f for f in LINE_FIELDS if f not in ("value",))` = `(item, timepoint, source)` (the subset is now structural, not a re-typed literal — review fix QUAL-01).
- `dedupe_key(reading) -> tuple` — `(item, timepoint, source)` identity (caller passes a conformant reading; raises `KeyError` otherwise — documented precondition).
- `is_conformant(reading) -> bool` — every `LINE_FIELDS` field present.
- The ONE key definition; `store.py` imports it, `ADR-0003-T1` must import it (never redefine — re-opens the spike's N3).

### `scripts/store/store.py` (ADR-0002-T1) — local NDJSON store
- `append(item, reading, root=Path("vault/store"))` — validates via `keying.is_conformant` (raises `ValueError`, 0 lines written, on a missing field); idempotent on the dedupe identity; appends one NDJSON line; local file I/O only.
- `read(item, root=...)` — whole-file scan, returns readings sorted ascending by `timepoint` (lexicographic == chronological assumes the spike's UTC-offset producer obligation).
- `vault/store/` is gitignored.

### `scripts/guard/egress_guard.py` (ADR-0001-T1) — the egress half of the V1 trust boundary
- `run(operation) -> bool` — runs a zero-arg `operation` under **OS-level network isolation** over the whole process tree, truthy-on-pass / falsy-on-fail. **Built the spike's FINAL selection (NOT the rejected in-process interceptor).** Per-OS via `platform.system()`: macOS `sandbox_init` (ctypes, profile `(version 1)(allow default)(deny network*)`); Linux `unshare(CLONE_NEWUSER|CLONE_NEWNET)`. Implemented as `os.fork()` + apply-isolation-in-child + run-operation; clean child exit → truthy.
- **Fail-closed** (default-deny) when isolation can't be established — incl. the `os.fork()`-failure path (review fix BUG-02) and a clean `SystemExit(0)` treated as pass (BUG-03). **Catches subprocess egress** (the OS deny is inherited by children) — empirically proven on-host: live network present, yet `run(reach)` falsy / `run(local)` truthy / `run(child_egress)` falsy.

### `scripts/guard/pii_scan.py` (ADR-0001-T1) — the PII-scan half + SHAREABLE
- `scan(tracked_files, identity_config=Path("vault/meta/operator-identity.txt")) -> int` — reads each file's **CONTENTS**, returns the operator-PII hit count, names offenders via a single `PII-HIT: <path>` **stderr** channel. `scan([]) == 0`. `tracked_files` is caller-supplied (no internal re-enumeration — the `ADR-0005-T1` hook passes its `--staged` set, the SEC-01(a) reuse contract).
- `AGNOSTIC_PATTERNS` (tracked, operator-agnostic, `re.DOTALL` + bounded `[\s\S]{0,400}?` gaps): generic `@gmail.com` + the two structural store-line patterns. The multi-line-JSON evasion the review found is fixed (DOTALL).
- **Operator-identity tokens are NOT hardcoded** — they load at runtime from the **gitignored** `vault/meta/operator-identity.txt` (per-instance; a tracked `.example` template shows a cloner the format). This is the shareability fix: tracked source carries zero operator PII.
- `store_is_gitignored(repo_root) -> bool` — the AC-4 `git check-ignore vault/store/` helper.
- Implemented in pure-Python `re` (documented deviation from the spike's literal `rg` command — this host's `rg` is a shell-function shim `xargs` can't exec; same patterns, same contents-search semantics).

## Pytest scaffold (first Python suite in the repo)
- `.venv/` (gitignored) = the reproducible runner — Python 3.14 + pytest 9.0.3. Run via `.venv/bin/python -m pytest`.
- Repo-root `conftest.py` puts the project root on `sys.path` (DEV-1; first Python package). `tests/store/` + `tests/guard/` are the first test packages. Suite: 38 passed, 2 skipped (Linux-only egress tests skip on Darwin).

## Independent review (PR #44) — why the trust boundary is actually sound
The 6-agent `/review-pr` + blind triage + blind verify caught REAL defects the orchestrator's mechanical verification AND the SE authors missed — PF-S3-01 earning its keep:
- the SE planted the operator's **real email + name** in test fixtures (removed → synthetic);
- the egress fail-direction tests were **vacuous on offline hosts** and **Darwin-only** (→ network-presence preconditions + a Linux fail test + a load-bearing AC-4 deny control — the failing-capable floor is now genuine);
- `os.fork()` failure wasn't fail-closed; `PermissionError` aborted the whole scan; the structural scan missed multi-line JSON.
13 of 15 legitimate fixed + blind-verified RESOLVED (2 legitimate beaded); 5 beaded total (`8s6`/`1ww`/`qwj`/`ivt`/`z2u`); 0 suppressed (PF-S26-01).

## Shareability (V1 will be shared)
Walter flagged the hardcoded operator name as a sharing blocker. Externalized the
identity tokens to the gitignored config in `pii_scan.py` AND the two governance
audit scripts (`audit-specialist-profile.sh` R13-6.7 leak detector + the
`audit-research-provenance.sh` comment). Tracked code + tests + governance scripts
are now operator-name-free. The remaining ~150-file operator name in **vault prose**
(session notes, HANDOFF, methodology) is the ADR-0005 clone-init sanitization
concern — bead `qwj`, to resolve before V1 ships (it also gates the ADR-0005-T1
pre-commit hook, which would otherwise block nearly every commit).

## Carried forward
- Beads `8s6` P1 (store corrupt-line policy), `1ww` P2 (concurrent-append lock), `qwj` P2 (PII-free-trunk / clone-init), `ivt` P3 (recipe↔spike interceptor drift — spec revision), `z2u` P3 (gitignore-test isolation).
- `ADR-0003-T1` (Wave 3) imports `keying.py` + consumes `egress_guard.run`.
- `pii_scan.scan` signature gained the optional `identity_config` param (backward-compatible with the hook's `scan(staged)`).

Links: [[session-30]] (Wave 1 spikes — the design this Wave built).
