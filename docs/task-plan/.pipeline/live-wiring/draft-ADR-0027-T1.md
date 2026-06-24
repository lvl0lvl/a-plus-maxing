---
task-id: ADR-0027-T1
source-spec: docs/spec/live-wiring-spec.md
source-build-plan: docs/build-plan/build-plan-live-wiring.md
wave: 1
assigned-agent: SE
reviewers: [Architect, QA, Security]
created: 2026-06-24
status: draft
depends-on: []
---

# Recipe: Live No-Train De-Id Backend (`_ClaudeNoTrainBackend.deidentify`)

Fill the `NotImplementedError` stub in `_ClaudeNoTrainBackend.deidentify` ([client.py:156-160])
with a real `claude-opus-4-8` no-train API call: read the model id from the `MODEL` class
attribute ([client.py:135]), build the SDK client through the existing lazy `self._client()`
(which resolves the key via `key_source.resolve` at call time, [client.py:137-142]), prompt the
model to emit ONLY a de-identified `SUMMARY_FIELD_SET`-shaped summary, retry a bounded number of
times under a timeout, and return the parsed summary mapping. The CROWN JEWEL is 0-leak: the raw
plan-intake transits the no-train API and is held IN MEMORY ONLY — it is never written to any path
(tracked or gitignored), and no raw-PII token survives past the de-id boundary. Every failure mode
fails closed to `ModelCallError` (via the existing `_call` wrapper) → `deid_in`'s `DEID_CALL_FAILED`
sentinel; the `ModelClient.deidentify` `isinstance(result, dict)` check + `deid_in`'s
`⊆ SUMMARY_FIELD_SET` whitelist are the downstream gates the ACs assert.

This task WIRES the live call behind a frozen seam; it re-authors nothing. The inner engine,
`router.py`, `deid_in.py`, and `key_source.py` stay BYTE-UNCHANGED (numstat = 0).
`scripts/model/client.py` is the single wired production file. Every test runs against a PATCHED
`anthropic` SDK injected at the lazy import site — the real SDK is NOT installed in `.venv`, so the
suite makes 0 live calls (0 live spend); the live end-to-end run is the operator-present S94
checkpoint AFTER this build.

## Entry State

**Prerequisites:**
- [ ] Working tree clean: `git status` shows no changes (the daemon vault-frontmatter churn under
      `vault/**` is daemon noise — leave it uncommitted, do not stage it; see CLAUDE.md § Vault
      hygiene).
- [ ] Full test suite passes at the behavior-preservation baseline:
      `.venv/bin/python -m pytest -q` → `1611 passed, 2 skipped` (re-baseline with a recorded count
      delta if the live count differs; the gate is the suite staying green, not the absolute integer).
- [ ] Infrastructure prerequisite verified — the `anthropic` SDK is NOT installed in `.venv`
      (the patch-driven posture): `.venv/bin/python -c "import importlib.util,sys; sys.exit(0 if
      importlib.util.find_spec('anthropic') is None else 1)" && echo "SDK absent"`.
- [ ] Infrastructure prerequisite verified — the de-id seam + downstream gates present:
      `grep -q "def deidentify" scripts/model/client.py && grep -q "NotImplementedError"
      scripts/model/client.py && grep -q "ModelCallError" scripts/model/client.py && test -f
      scripts/plan/deid_in.py && grep -q "SUMMARY_FIELD_SET" scripts/plan/router.py && echo OK`.
- [ ] On feature branch: `feature/live-deid-backend` cut off `feature/engine-live-wiring-build`
      (the wave branch).

This entry state doubles as the rollback target — the entry-state commit is the
`feature/engine-live-wiring-build` HEAD this branch was cut from.

## Context Load List

**Files to read:**
- `scripts/model/client.py` — the single wired file: the `_ClaudeNoTrainBackend.deidentify`
  `NotImplementedError` stub being filled ([:156-160]), the `MODEL` class attribute the call reads
  ([:135]), the lazy `self._client()` that resolves the key via `key_source.resolve` ([:137-142]),
  the `_call` fail-closed wrapper + its SEC-01 constant-message control ([:105-123]), and the
  `ModelClient.deidentify` wrapper's `isinstance(result, dict)` check ([:92-95]).
- `tests/model/test_client.py` — the existing backend tests this task EXTENDS: the `_FixtureBackend`
  + its `deidentify_result` seam ([:32-59]), the `_good_deidentify_fixture` shape helper ([:90]),
  the `test_deidentify_*` cases ([:138-148], [:282]), and the `test_no_model_client_import_outside_
  the_seam` guard ([:157]). The new patched-SDK cases live alongside these.
- `scripts/plan/router.py` — `SUMMARY_FIELD_SET` ([:20]), the whitelist the returned summary keys
  must be a subset of (read for the AC-3/AC-5 oracle; NOT modified).
- `scripts/plan/deid_in.py` — `deid_in`'s `⊆ SUMMARY_FIELD_SET` whitelist ([:71]) + the
  `DEID_CALL_FAILED` sentinel ([:27]); the downstream gate the fail-closed ACs assert (read for the
  oracle; NOT modified).
- `scripts/model/key_source.py` — `resolve(...)` ([:64]), the env→keychain key resolver the
  `_client()` calls at call time (read to confirm the key is never tracked/printed; NOT modified).

**Do NOT load:** the ADRs (`docs/adr/ADR-0027*.md`) — the spec already distilled them; the
`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track}.py` inner
engine — this task does not touch the plan pipeline; the other live-wiring recipes
(`plan_driver` / `gate_dispatch` / the skill / the audit) — disjoint scope; any `vault/**`
knowledge-graph file — daemon-churned, not part of this task.

## Risk Pre-Check

This task carries the spec's ADR-0027-T1 Risk Mitigations field (the crown-jewel egress boundary).
Before proceeding to RED, verify a test exists (or the RED phase adds one) for EACH; a placeholder
test (`assert True`) fails this gate.

- **Risk N1 — raw plan-intake PII transits the no-train API (ADR-0027 Consequence-Negative-1 /
  Constraint ADR-0001).** Gate: a test seeds a synthetic legal name + a synthetic lab value into the
  raw intake and asserts the de-identified summary `deid_in` surfaces carries 0 of those raw tokens
  — count of raw-PII tokens past the boundary = 0 (Cycle 4, the crown-jewel raw-PII-leak probe).
- **Risk N4 — new raw-input surface / committed-PII (ADR-0027 Consequence-Negative-4 / Constraint
  ADR-0005).** Gate: a test runs the live-wired backend over a synthetic raw-PII intake under an
  isolated tmp `HOME`/`CWD`, then `rglob("*")` over the whole tmp tree and greps EVERY file written
  during the call for the synthetic raw-PII token → count of files carrying the token = 0 (Cycle 3,
  the raw-intake-in-memory-only tmp-tree scan). A MUTATION step (a deliberately-injected
  `path.write_text(raw_intake)` inside the call boundary) makes the same scan find ≥1 file and go RED
  — proving the scan is non-vacuous.
- **Risk N3 — hard runtime API dependency (ADR-0027 Consequence-Negative-3).** Gate: an injected SDK
  exception → `ModelCallError` → `deid_in` returns the `DEID_CALL_FAILED` sentinel, count of
  fabricated/partial summaries past the boundary = 0 (Cycle 2, the fail-closed probe).
- **Risk SEC-4 — the error surface leaks a secret (locks the SEC-01 constant-message control).**
  Gate: a test seeds a synthetic key + a synthetic raw-PII token, forces the failure path, and
  asserts `str(exc)` and the exception's `.args` contain 0 occurrences of either token — the raised
  `ModelCallError` carries no resolved-key substring AND no raw-intake substring (Cycle 2). This
  LOCKS the existing `_call` constant-message control, it does not add a new control.

The gate conditions reference live tests, not subjective assessments.

## TDD Steps

Four TDD cycles. Cycle 1 establishes the live call (patched-SDK return-dict + prompt-carries-raw +
`MODEL`-swappable + summary ⊆ `SUMMARY_FIELD_SET`). Cycle 2 is the fail-closed family (injected SDK
exception, out-of-set field, bounded retry, error-surface-carries-no-secret). Cycle 3 is the
raw-intake-in-memory-only tmp-tree scan WITH MUTATION. Cycle 4 is the crown-jewel raw-PII-leak probe.
All patched-SDK / synthetic-PII, 0 live spend.

**Patched-SDK construction note (read before RED):** the real `anthropic` SDK is absent from
`.venv`. The tests inject a fake `Anthropic` at the lazy import site (`_ClaudeNoTrainBackend._client`)
— `monkeypatch` the `_client` method (or the `anthropic` module entry the import resolves) so it
returns a fake whose `messages.create(...)` returns a canned envelope and records its call args.
The real package is NEVER imported; the absence is what proves the test is patch-driven (0 live
spend). This is the same posture the existing `_FixtureBackend` tests use at the BACKEND seam,
moved one level down to the SDK seam for the live-call cases.

### Cycle 1: Steps 1-4 — the live de-id call (return-dict + prompt-carries-raw + MODEL-swappable + summary-subset)

#### Step 1: RED — Write Failing Tests
Call `/write-tests` for `scripts/model/client.py` (extend `tests/model/test_client.py`) targeting:
- AC-1 (patched-SDK return-dict + prompt-carries-raw): with a patched `anthropic` SDK whose
  `messages.create` returns a canned `SUMMARY_FIELD_SET`-shaped envelope injected at the
  `_ClaudeNoTrainBackend._client` import site, `_ClaudeNoTrainBackend().deidentify(raw_intake)`
  returns a `dict`, AND the prompt passed to the fake `messages.create` carries the raw intake —
  asserted by inspecting the captured call args (the fake records `messages` / the prompt string and
  the test greps the raw-intake token into it).
- AC-2 (`MODEL`-attribute-swappable): set `_ClaudeNoTrainBackend.MODEL` to a sentinel value and
  assert the fake `messages.create` was called with that sentinel `model=` — swapping `MODEL`
  changes the model id with 0 caller-side edits (read the model id off the captured call).
- AC-3 (summary ⊆ `SUMMARY_FIELD_SET`): the parsed summary the backend returns has keys that are a
  subset of `router.SUMMARY_FIELD_SET` — count of out-of-set keys = 0; AND `deid_in` over that
  summary returns the summary (not the `DEID_CALL_FAILED` sentinel).

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: FAIL (the live `deidentify` does not yet exist — the stub raises `NotImplementedError`; a
patched-SDK call hits the stub, not a parsed summary).

#### Step 2: GREEN — Implement
Changes to make:
- `scripts/model/client.py`: replace the `NotImplementedError` body of
  `_ClaudeNoTrainBackend.deidentify(self, raw_intake)` with the live call. Read the model id from
  `self.MODEL` (the class attribute, not a buried literal — so AC-2's swap works with 0 caller-side
  edits). Construct the SDK client via the existing `self._client()` (unchanged — it resolves the key
  via `key_source.resolve` at call time). Build a prompt that inlines the raw intake and instructs
  the model to emit ONLY a de-identified summary whose keys are drawn from `SUMMARY_FIELD_SET` (no
  raw PII, no novel fields). Call `messages.create(model=self.MODEL, ...)` under a bounded
  retry-with-timeout loop, parse the model's response into a summary mapping, and return that
  mapping. Hold the raw intake in a LOCAL VARIABLE only — never write it to any path (satisfies
  AC-7). Do NOT add the `SUMMARY_FIELD_SET` subset check here — that is `deid_in`'s downstream gate
  (this method returns the parsed mapping; the wrapper + `deid_in` fail it closed if out-of-set).
  The method imports `SUMMARY_FIELD_SET` from `router` only if the prompt construction needs the
  field roster (a read of the existing whitelist, not a new one). (satisfies AC-1, AC-2, AC-3)

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: PASS

#### Step 3: REFACTOR
Review for:
- Duplication between the new live `deidentify` and the (still-stubbed) `converse`/`author` SDK call
  shapes — if a shared `_messages_create_with_retry` helper would serve all three when they are later
  wired, extract it ONLY if `deidentify`'s use alone justifies it (do not pre-build for the unwired
  methods — TP-06 / Core Rule 4). The bounded-retry loop is `deidentify`'s; leave `converse`/`author`
  as `NotImplementedError` stubs (out of scope).
- Naming consistency: the prompt builder / parse helper follow the module's existing private-helper
  idiom (`_call`, `_is_author_envelope`).
- No behavior change.

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: PASS (no behavior change)

#### Step 4: REGRESSION
Run: `.venv/bin/python -m pytest -q`
Expected: PASS — `1611 passed, 2 skipped` (no tests outside task scope broken; the inner engine +
`router`/`deid_in`/`key_source` are byte-unchanged).

### Cycle 2: Steps 5-8 — fail-closed (injected exception → ModelCallError; bounded retry; error-surface-carries-no-secret)

#### Step 5: RED — Write Failing Tests
Call `/write-tests` for `scripts/model/client.py` (`tests/model/test_client.py`) targeting:
- AC-4 (injected SDK exception → `ModelCallError` → sentinel): the fake `messages.create` RAISES;
  assert `_ClaudeNoTrainBackend().deidentify(...)` raises `ModelCallError` (via the `_call` wrapper),
  and `deid_in` over a `ModelClient` built on that backend returns the
  `{"deidentified": False, "reason": DEID_CALL_FAILED}` sentinel — count of fabricated/partial
  summaries past the boundary = 0.
- AC-5 (out-of-`SUMMARY_FIELD_SET` field → sentinel): the fake returns a summary carrying a field
  OUTSIDE `SUMMARY_FIELD_SET`; assert `deid_in` returns the `DEID_CALL_FAILED` sentinel (the
  whitelist fails closed) — count of out-of-set summaries surfaced = 0.
- AC-6 (bounded retry): with the fake raising on the first N-1 attempts and succeeding on the Nth,
  the call succeeds within the bound (assert success + the fake invoked N times); with the fake
  raising on ALL attempts, the call raises `ModelCallError` after EXACTLY the bounded number of
  attempts (assert the fake's invocation count == the bound) — never an unbounded retry.
- SEC-4 (error-surface-carries-no-secret): seed a synthetic key (patch `key_source.resolve` to
  return a synthetic token) + a synthetic raw-PII token in the intake, force the failure path
  (`messages.create` raises with a message embedding the key/raw token), and assert `str(exc)` AND
  `exc.args` over the raised `ModelCallError` contain 0 occurrences of EITHER token — the
  constant-message `_call` surface ([client.py:118-120]) carries no secret. RED-capable: a variant
  that interpolated `{exc!r}` into the `ModelCallError` message would leak the token → RED.

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: FAIL (the bounded-retry mechanics + the error-surface lock are exercised by the Cycle-1
implementation; if Cycle 1's retry loop is unbounded or interpolates the exception, these RED).

#### Step 6: GREEN — Implement
Changes to make:
- `scripts/model/client.py`: confirm/finalize the bounded retry-with-timeout loop in
  `_ClaudeNoTrainBackend.deidentify` — the loop attempts the `messages.create` at most a fixed bound
  (a named module/method constant, NOT a hard-coded literal at the call site; an in-task design
  decision per disposition #8), and re-raises after the bound is exhausted so the `_call` wrapper
  converts it to `ModelCallError`. The raised exception text stays the constant `_call` message
  (never interpolated with the raw input or the resolved key — preserve the SEC-01 control; do NOT
  weaken it). The fail-closed shape checks (the `isinstance(result, dict)` in `ModelClient.deidentify`
  + the `⊆ SUMMARY_FIELD_SET` in `deid_in`) are the existing downstream gates — this method does not
  re-implement them, it relies on them (the out-of-set field falls through to `deid_in`'s whitelist).
  (satisfies AC-4, AC-5, AC-6, SEC-4)

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: PASS

#### Step 7: REFACTOR
Review the retry loop for an off-by-one at the bound boundary (the bound must mean "at most N
attempts," not N+1) and for naming consistency with the existing constant idiom. Run targets:
`tests/model/test_client.py`. Expected: PASS, no behavior change.

#### Step 8: REGRESSION
Run: `.venv/bin/python -m pytest -q`
Expected: PASS

### Cycle 3: Steps 9-10 — raw-intake-in-memory-only (tmp-tree scan WITH MUTATION)

#### Step 9: RED — Write Failing Tests
Call `/write-tests` for `scripts/model/client.py` (`tests/model/test_client.py`) targeting:
- AC-7 (raw-intake-in-memory-only, LOAD-BEARING for ADR-0005): run the live-wired backend over a
  synthetic raw-PII intake under an isolated tmp `HOME`/`CWD` (`tmp_path` set as BOTH via
  `monkeypatch.chdir(tmp_path)` + `monkeypatch.setenv("HOME", str(tmp_path))`), then `rglob("*")`
  over the whole tmp tree and grep EVERY file written during the de-id call for the synthetic
  raw-PII token → count of files carrying the token = 0. The scan is a tmp-tree filesystem rglob
  (NOT only a `builtins.open` write-spy — a write-spy misses `os.write` / `pathlib.Path.write_text`
  / `tempfile` / SDK-internal write paths).
- AC-7 MUTATION (proves the scan is non-vacuous): a deliberately-injected `path.write_text(raw_intake)`
  inside the call boundary (a test variant that monkeypatches the backend to write the raw intake to
  a tmp file mid-call) makes the SAME rglob scan find ≥1 file and go RED — asserted by a mutation
  test that injects the leak and expects the scan to FAIL, confirming the scan can detect a real
  on-disk raw-PII write before it is trusted.

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: FAIL on the mutation case if the scan cannot detect an injected on-disk write (the scan is
the new code); the clean AC-7 case PASSES once the live method holds the raw intake in-memory only.
(If both pass immediately, investigate — the scan may not actually rglob the right tree, or the
mutation may not actually write.)

#### Step 10: GREEN — Implement
Changes to make:
- `scripts/model/client.py`: confirm `_ClaudeNoTrainBackend.deidentify` holds the raw intake ONLY as
  the in-memory argument + the prompt string, and writes it to NO path — no `tempfile`, no debug
  dump, no cache file. (This is a no-NEW-write assertion on the Cycle-1 implementation; the GREEN
  here is "the method already writes nothing" — pin it. If Cycle 1 introduced any disk write of the
  raw intake, remove it.) No new control flow.

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: PASS (the clean AC-7 case; the mutation variant asserts the scan RED-capability separately)

#### (REFACTOR folded — no new structure. REGRESSION:)
Run: `.venv/bin/python -m pytest -q`
Expected: PASS

### Cycle 4: Steps 11-12 — the crown-jewel raw-PII-leak probe (0 raw tokens past the boundary)

#### Step 11: RED — Write Failing Tests
Call `/write-tests` for `scripts/model/client.py` (`tests/model/test_client.py`) targeting:
- AC-8 (raw-PII-leak probe, crown-jewel): seed a synthetic legal name + a synthetic lab value into
  the raw intake; the patched SDK returns a `SUMMARY_FIELD_SET`-shaped summary (band/class values,
  no raw tokens). Assert the de-identified summary the backend returns AND the summary `deid_in`
  surfaces carry 0 of those raw tokens — count of raw-PII tokens past the boundary = 0. Failing-
  capable: a variant whose patched SDK echoed the raw name into a summary value would go RED.
- AC-9 (0 live spend, integration): the full `tests/model/test_client.py` run is entirely against
  the patched SDK — assert (via the SDK-absent precondition + the no-import guard
  `test_no_model_client_import_outside_the_seam` staying green) that 0 live-API calls are made. (This
  is a suite-level invariant; the AC-9 verification is the green run with the real SDK absent.)

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: FAIL if the boundary echoes a raw token (the probe is the new code); PASS-on-the-oracle if
the live method only ever returns the patched summary (then the RED proves the probe is wired and the
seed reaches the assertion). Demonstrate the probe goes RED against a leak variant (a patched SDK
echoing the raw name) — a probe that cannot go RED is worthless.

#### Step 12: GREEN — Implement
Changes to make:
- `scripts/model/client.py`: no NEW control flow — the live `deidentify` returns ONLY the model's
  parsed `SUMMARY_FIELD_SET`-shaped summary (the band/class mapping), never the raw intake or a field
  derived from it. The 0-leak property holds because the method returns the parsed summary and the
  `deid_in` whitelist rejects any out-of-set (including raw-token-bearing) field. Pin it: the returned
  mapping is the parse of the model response, not the raw intake. If Cycle 1's parse passed a raw
  field through, constrain the parse to the `SUMMARY_FIELD_SET` keys here.

Run: `.venv/bin/python -m pytest tests/model/test_client.py -q`
Expected: PASS

#### (REFACTOR folded. REGRESSION:)
Run: `.venv/bin/python -m pytest -q`
Expected: PASS (the full integrated suite green, 0 live spend)

**TDD step count: 12 (4 cycles × ≤4 steps, REFACTOR/REGRESSION folded on cycles 3-4).** Within the
task-planning ≤10-cycles guidance (4 cycles); the step count is bounded by the spec's 9 ACs mapping
to crown-jewel probes that are not splittable. One production file + one extended test file.

## Interface Contracts

This task fills a method body behind a FROZEN seam — it does NOT create or modify a shared interface.
The published `ModelClient` surface (`converse` / `author` / `deidentify`) is unchanged
([client.py:11-13] documents it as frozen at ADR-0015-T1); `_ClaudeNoTrainBackend.deidentify`'s
signature (`(self, raw_intake)`) and the `deidentify(raw_intake) -> dict` contract are unchanged —
only the body moves from `NotImplementedError` to a live call returning the same `dict` shape.

The downstream contract this task SATISFIES (does not define): `_ClaudeNoTrainBackend.deidentify`
returns a `dict` summary whose keys are drawn from `router.SUMMARY_FIELD_SET`; `ModelClient.deidentify`
re-checks `isinstance(result, dict)`; `deid_in` re-checks `⊆ SUMMARY_FIELD_SET` and emits the
`DEID_CALL_FAILED` sentinel on any failure. ADR-0026-T3 (the skill front-door) consumes this method
through `ModelClient.deidentify` as the de-id-IN step — that is a consumption of the EXISTING seam,
not a new contract this task introduces. No other task changes this method.

## Verification Checklist

- [ ] AC-1 (patched-SDK return-dict + prompt-carries-raw) — verified by
      `test_deidentify_live_returns_dict_and_prompt_carries_raw` (asserts a `dict` return + the
      raw-intake token in the captured `messages.create` prompt args).
- [ ] AC-2 (`MODEL`-attribute-swappable, 0 caller edits) — verified by
      `test_deidentify_model_id_read_from_MODEL_attribute` (sets `MODEL` to a sentinel, reads it off
      the captured `model=` arg).
- [ ] AC-3 (summary ⊆ `SUMMARY_FIELD_SET`) — verified by
      `test_deidentify_summary_keys_subset_of_field_set` (count of out-of-set keys == 0; `deid_in`
      returns the summary, not the sentinel).
- [ ] AC-4 (injected SDK exception → `ModelCallError` → sentinel) — verified by
      `test_deidentify_sdk_exception_fails_closed_to_sentinel` (`ModelCallError` raised; `deid_in`
      returns `DEID_CALL_FAILED`; 0 fabricated/partial summaries past the boundary).
- [ ] AC-5 (out-of-set field → sentinel) — verified by
      `test_deidentify_out_of_set_field_fails_closed` (count of out-of-set summaries surfaced == 0).
- [ ] AC-6 (bounded retry) — verified by `test_deidentify_bounded_retry_then_fail` (succeeds within
      the bound when the Nth attempt succeeds; raises after EXACTLY the bounded count when all raise;
      the fake's invocation count == the bound — never unbounded).
- [ ] AC-7 (raw-intake-in-memory-only, tmp-tree scan WITH MUTATION) — verified by
      `test_deidentify_raw_intake_never_written_to_disk` (rglob the tmp `HOME`/`CWD` tree → 0 files
      carrying the raw token) + `test_deidentify_in_memory_scan_red_on_injected_write` (the mutation:
      an injected `write_text(raw_intake)` makes the scan find ≥1 file and go RED — the non-vacuous
      lock).
- [ ] AC-8 (raw-PII-leak probe, crown-jewel) — verified by
      `test_deidentify_no_raw_pii_token_past_boundary` (seeded synthetic name + lab; 0 raw tokens in
      the returned + `deid_in`-surfaced summary; demonstrated RED against a leak variant).
- [ ] AC-9 (0 live spend) — verified by the green `tests/model/test_client.py` run with the real
      `anthropic` SDK absent from `.venv` + `test_no_model_client_import_outside_the_seam` staying
      green (0 live-API calls).
- [ ] SEC-4 (error-surface-carries-no-secret) — verified by
      `test_deidentify_error_surface_carries_no_key_or_raw` (`str(exc)` + `exc.args` carry 0
      occurrences of the synthetic key OR the synthetic raw-PII token — the SEC-01 constant-message
      lock).
- [ ] Wave-1 de-id crown-jewel 0-leak checkpoint gates carried: raw-PII-past-the-boundary [AC-8],
      raw-intake-in-memory-only (non-vacuous tmp-tree rglob + mutation) [AC-7], fail-closed (SDK
      exception → sentinel [AC-4], out-of-set → sentinel [AC-5], bounded retry [AC-6], summary subset
      [AC-3], `MODEL`-driven id [AC-2]), key-never-committed (`grep` over the diff for a literal key
      == 0 hits — the key resolves via `key_source.resolve` at call time, never tracked), and
      error-surface-carries-no-secret [SEC-4].
- [ ] No regression in full test suite (`.venv/bin/python -m pytest -q` → `1611 passed, 2 skipped`).
- [ ] EXTEND-NOT-REBUILD gate green: `git diff --numstat <wave-base>..HEAD -- scripts/plan/router.py
      scripts/plan/deid_in.py scripts/model/key_source.py` → 0 changed lines (this task wires only
      `client.py`; the downstream gates + the key resolver are byte-unchanged).
- [ ] Files modified match file manifest (`scripts/model/client.py` + `tests/model/test_client.py`)
      — no scope creep.
- [ ] Interface contracts documented (the frozen seam preserved; the downstream summary-subset +
      sentinel contract satisfied).

## Commit

```
feat(model): live no-train de-id backend call
```
Stage only:
- `scripts/model/client.py`
- `tests/model/test_client.py`

Stage by explicit path (`git add <path>` as its own command, then `git commit` separately — the
PreToolUse hook denies single-call stage+commit, `git commit -a/--all`, and pathspec
`git commit <path>`). Do NOT `git add vault/` or the daemon frontmatter churn (CLAUDE.md § Vault
hygiene). Do NOT stage `.beads/issues.jsonl` / `harvest.jsonl` / `memory/process-failures.md` — those
are close-protocol artifacts, committed at session close, not in the build commit.

## Rollback

If verification fails after 3 fix cycles:
1. `git stash -m "failed-ADR-0027-T1-attempt-{N}"` — preserve work for diagnosis.
2. `git checkout {commit-before-task}` — revert to the entry-state commit (the
   `feature/engine-live-wiring-build` HEAD this branch was cut from).
3. Update the bead tracker: flag ADR-0027-T1 as BLOCKED with the failure log.
4. Escalate: "Task ADR-0027-T1 failed verification after 3 attempts. Stash ref: {ref}. Failure log:
   {summary}."
5. After abandonment or re-planning, drop all `failed-ADR-0027-T1` entries from `git stash list`.

Do NOT: silently skip failing acceptance criteria, weaken tests to make them pass (especially the
crown-jewel 0-leak probes — a leak probe that cannot go RED is worthless), or proceed to the wave
checkpoint with a broken state. The crown-jewel 0-leak gate RED at the checkout is release-blocking
(ADR-0005 falsification) — HALT, do not advance.
