---
task-id: ADR-0026-T3
source-spec: docs/spec/live-wiring-spec.md
source-build-plan: docs/build-plan/build-plan-live-wiring.md
wave: 3
assigned-agent: SE
reviewers: [QA, Security]
created: 2026-06-24
status: draft
depends-on: [ADR-0026-T1, ADR-0026-T2, ADR-0027-T1]
---

# Recipe: `/generate-plan` Skill Front-Door (the V1 Subscription Driver)

Reconcile the superseded runtime-A `/generate-plan` skill (`.claude/skills/generate-plan/SKILL.md`,
Modify) to the A′ subscription-driver path: (1) de-id the raw intake via the ADR-0027 API client (a
synchronous Python `ModelClient.deidentify` call — NOT the deterministic `router.summarize`
substitute the current prose uses at [SKILL.md:48]); (2) dispatch each plan-domain specialist + each
safety lens as a SUBSCRIPTION Claude Code agent (full role profile inlined per INV-ROLE-INLINING)
over the de-identified summary, feeding each captured envelope to the ADR-0026-T1 shared driver per
yielded dispatch-request; (3) drive `plan_driver` (which runs assemble/gates/revise via the
ADR-0026-T2 composer) — the skill does NOT re-implement the loop; (4) `reinsert_out` (deterministic)
→ `reemit_maintained` render. Document the dispatch protocol + the no-fork-at-the-skill-level
constraint.

**What IS vs ISN'T mock-testable (load-bearing):** the LIVE subscription dispatch over REAL agents is
the S94 operator-present attestation, NOT a mock-test target. The recipe's TESTABLE cycles are (a)
the thin Python GLUE contract — the glue feeds the shared driver a fixture envelope per yielded
request, holds only the `deid_in` summary, and drives the driver (does not re-host the loop) — and
(b) the dispatch-protocol DOC in the skill prose. The skill prose explicitly documents the live
dispatch as the S94 deferral. The thin glue lives in `tests/plan/test_generate_plan_skill_glue.py`
(Create); the SKILL.md is prose-only (no Python is added to the skill file itself — the glue contract
is exercised against the existing `plan_driver` / `ModelClient.deidentify` seams).

This task touches NO inner-engine module (numstat = 0) and NO production Python (the skill is prose;
the glue test drives existing seams). `.claude/skills/generate-plan/SKILL.md` +
`tests/plan/test_generate_plan_skill_glue.py` are the only files. 0 live agent dispatch, 0 live spend.

## Entry State

**Prerequisites:**
- [ ] Task ADR-0026-T1 complete (the shared driver `scripts/plan/plan_driver.py` + its drive-protocol
      present + merged — the skill drives it).
- [ ] Task ADR-0026-T2 complete (the composed `scripts/plan/gate_dispatch.py` present + merged — the
      driver gates through it).
- [ ] Task ADR-0027-T1 complete (the live `_ClaudeNoTrainBackend.deidentify` behind
      `ModelClient.deidentify` present + merged — the skill's de-id-IN step calls it).
- [ ] Wave 2 checkpoint passed Go (the composer emits the exact 3-key disposition, fails closed on a
      malformed composite, runs both gates) + Wave 1 entry ADR-0027-T1 complete.
- [ ] Working tree clean: `git status` shows no changes (the daemon vault-frontmatter churn under
      `vault/**` is daemon noise — leave it uncommitted; see CLAUDE.md § Vault hygiene).
- [ ] Full test suite passes: `.venv/bin/python -m pytest -q`.
- [ ] Infrastructure prerequisite verified — the specialist + lens agents present:
      `for a in medical-safety-reviewer health-edge-case-reviewer medical-liaison personal-trainer
      nutritionist supplement-specialist peptide-specialist; do test -d .claude/agents/$a ||
      { echo "MISSING $a"; exit 1; }; done && echo OK`.
- [ ] On feature branch: `feature/generate-plan-skill-aprime` cut off
      `feature/engine-live-wiring-build`.

This entry state doubles as the rollback target — the entry-state commit is the Wave-2 → Wave-3
checkpoint HEAD (ADR-0026-T1/T2 + ADR-0027-T1 merged).

## Context Load List

**Files to read:**
- `.claude/skills/generate-plan/SKILL.md` — the file being reconciled: the superseded runtime-A prose
  (the `router.summarize(store_read) [0-raw-PII]` de-id-IN at [:48], the "agent-in-the-loop by
  design" + direct `pipeline.run_generation` dispatch at [:17-21, :49-57]) — the text the A′
  subscription path replaces.
- `scripts/plan/plan_driver.py` — the shared driver (ADR-0026-T1) the skill DRIVES: its drive-protocol
  (yields a dispatch-request, receives envelopes via `.send()`, gates through the composed
  `gate_dispatch`, promotes/halts) — read so the skill prose + the glue test name the correct seam.
- `scripts/model/client.py` — `ModelClient.deidentify(raw_intake) -> dict` ([:78-95]) — the
  ADR-0027-T1 de-id-IN call the skill names; `deid_in` ([scripts/plan/deid_in.py]) wraps it to the
  summary/sentinel.
- `scripts/plan/gate_dispatch.py` — the composer (ADR-0026-T2) the driver gates through (read for the
  3-key disposition the skill's dispatch protocol feeds — confirm the skill drives the driver, not
  the composer directly).
- `scripts/plan/reinsert_out.py` — `reinsert_out(html, target_path, *, _profile_paths, _repo_root)`
  ([:88]) — the deterministic de-id-OUT re-insertion the render path runs.
- `scripts/generate/maintained.py` — `reemit_maintained(*, root, _out_dir, _today, _profile_paths,
  _repo_root, ...)` ([:245]) — the store-mediated maintained render the skill names as the final
  stage.
- `scripts/plan/plan_orchestrator.py` — `_dispatch_prompt` ([:110]) + `_ROLE_OF_DOMAIN` ([:58]) — the
  existing de-identified-summary-only dispatch-prompt shape the skill's subscription dispatch mirrors
  (read to confirm the dispatch payload carries the summary only, never raw PII).

**Do NOT load:** the ADRs (`docs/adr/ADR-0026*.md`) — the spec distilled them; the inner-engine
modules (`orchestrate`/`pipeline`/`assemble`/`generate_plan`/`adjudicate`/`adjust`/`track`/`router`)
— byte-frozen, untouched; the audit + the self-test (`core-capability-audit.sh` /
`_a_prime_self_test.py`) — ADR-0026-T4, the parallel Wave-3 task with a disjoint manifest; any
`vault/**` file — daemon-churned.

## Risk Pre-Check

This task carries the spec's ADR-0026-T3 Risk Mitigations field (the crown-jewel 0-raw-PII-to-any-
dispatch + the skill-level no-fork). Before proceeding to RED, verify a test exists (or the RED phase
adds one) for EACH; a placeholder test (`assert True`) fails this gate.

- **Risk — raw PII reaches a subscription agent (Constraint ADR-0001 summaries-not-raw / the
  crown-jewel 0-leak).** Gate: over a synthetic raw-PII intake, every dispatch payload the glue/driver
  issues carries the de-identified summary only — count of raw-PII fields in any dispatch payload == 0,
  scanned RECURSIVELY over the FULL serialized payload (every nested envelope/context field), not just
  the top-level `summary` key (AC-2, QA-5).
- **Risk — a skill-prose copy of the safety loop (the A-naive forked-loop failure class ADR-0026
  rejects).** Gate: a grep over `.claude/skills/generate-plan/SKILL.md` finds 0 copies of the
  `while True:` / `safety_passed is True` / scratch-and-promote control flow — the skill drives the
  ONE shared driver, it does not re-host the loop (AC-3).
- **Risk — the de-id-IN step is a deterministic substitute, not the live client (Constraint
  ADR-0001).** Gate: the skill prose names the `deid_in` / `ModelClient.deidentify` path as the de-id
  IN (NOT `router.summarize`), and the glue test drives the de-id seam (AC-1).

The gate conditions reference live tests / grep checks, not subjective assessments.

## TDD Steps

Three TDD cycles. Cycle 1 the de-id-IN-via-`ModelClient.deidentify` + the glue drives the shared
driver. Cycle 2 the 0-raw-PII-to-any-dispatch RECURSIVE scan. Cycle 3 the no-fork-at-skill-level grep
+ the S94-deferral doc. The glue test is the only test code; the SKILL.md change is prose. 0 live
spend.

**Scope note (what IS vs ISN'T mock-testable):** the testable ACs are the Python-glue contract
(AC-2/4/6) + the documented dispatch protocol (AC-1/3/5). The LIVE subscription dispatch over REAL
agents is the S94 operator-present LIVE-test attestation, NOT a mock-test target — the glue test
drives the shared driver with a FIXTURE `dispatch`, never a real agent. The glue STRUCTURALLY only
ever holds the `deid_in` summary; whether a REAL subscription agent receives only the summary on the
LIVE path is the residual 0-leak property flagged for the S94 checkpoint owner (SEC-6).

### Cycle 1: Steps 1-4 — de-id-IN via `ModelClient.deidentify` + the glue drives the shared driver

#### Step 1: RED — Write Failing Tests
Call `/write-tests` for the skill glue (new suite `tests/plan/test_generate_plan_skill_glue.py`)
targeting:
- AC-1 (de-id via `ModelClient.deidentify`, NOT `router.summarize`): the glue test drives the de-id-IN
  step through `deid_in(raw_intake, ModelClient(backend=<fixture>))` (the ADR-0027 path) — assert the
  de-id seam is the `ModelClient.deidentify` call, not a `router.summarize` substitute. (The skill
  prose change is verified separately by AC-1's prose-grep in Cycle 3; this test pins the glue drives
  the de-id seam.)
- AC-4 (glue drives the shared driver): the glue feeds the shared driver a fixture envelope per
  yielded dispatch-request and the driver completes a synthetic run (de-id → loop → promote) — assert
  via `tests/plan/test_generate_plan_skill_glue.py` driving the glue with a fixture `dispatch` (0 live
  agent dispatch, 0 live spend). The glue CALLS `plan_driver`'s drive-protocol; it does not re-host
  the loop.

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: FAIL (the glue test references a glue contract over the shared driver + the de-id seam; the
test does not yet exist, and the de-id-IN-via-`ModelClient.deidentify` wiring it asserts is the new
contract).

#### Step 2: GREEN — Implement
Changes to make:
- `tests/plan/test_generate_plan_skill_glue.py` (Create): write the thin glue contract test — it
  exercises the EXISTING seams (`deid_in` over a fixture `ModelClient`, the `plan_driver`
  drive-protocol fed a fixture envelope per yielded request, the composed `gate_dispatch` over fixture
  judge/review) end-to-end on a synthetic PII-free fixture, asserting the de-id-IN routes through
  `ModelClient.deidentify` and the driver completes (promote on accept). No production Python is added
  — the glue is the documented call sequence the skill prose names, exercised against the merged
  seams. (satisfies AC-1, AC-4 at the glue-contract level)
- `.claude/skills/generate-plan/SKILL.md` (Modify): replace the de-id-IN prose — change the Phase-0
  `router.summarize(store_read) [0-raw-PII]` de-id-IN ([:48]) to the A′ de-id-IN: a synchronous Python
  `ModelClient.deidentify` call (via `deid_in`) over the raw intake, producing the de-identified
  summary the dispatches author over. State that `router.summarize` is NOT the de-id-IN on the A′ path
  (it is a deterministic store-summarizer, not the live no-train de-id boundary). (satisfies AC-1's
  prose half — the prose-grep verifies it in Cycle 3)

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: PASS

#### Step 3: REFACTOR
Review the glue test for duplication with the existing `test_plan_driver.py` drive-protocol tests —
the glue test asserts the SKILL'S call sequence (de-id-IN → driver → render), not the driver's
internals (those are ADR-0026-T1's); keep it thin, not a re-test of the driver. Run targets:
`tests/plan/test_generate_plan_skill_glue.py`. Expected: PASS, no behavior change.

#### Step 4: REGRESSION
Run: `.venv/bin/python -m pytest -q`
Expected: PASS (no tests outside task scope broken — the inner engine + the driver + the de-id backend
are unchanged).

### Cycle 2: Steps 5-6 — 0-raw-PII-to-any-dispatch (RECURSIVE payload scan, QA-5)

#### Step 5: RED — Write Failing Tests
Call `/write-tests` for the skill glue (`tests/plan/test_generate_plan_skill_glue.py`) targeting:
- AC-2 (0-raw-PII to any subscription agent, RECURSIVE): over a synthetic raw-PII intake (a seeded
  legal name + lab value), every dispatch payload the glue/driver issues carries the de-identified
  summary only — count of raw-PII tokens in any dispatch payload == 0. The count scans the FULL
  serialized dispatch payload RECURSIVELY (JSON-serialize the whole payload and grep, OR recurse all
  dict/list values — NOT just the top-level `summary` key), so a raw token smuggled into a NESTED
  field (an envelope's `context`/`metadata` sub-dict) goes RED. The glue only ever holds the `deid_in`
  summary, never the raw intake. RED-capable: a variant whose dispatch payload nested the raw intake
  in a `context` field would go RED on the recursive scan (and PASS a top-level-only scan — proving
  the recursion is load-bearing).

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: FAIL if the recursive scan is not yet wired (the scan is the new test code); PASS-on-the-
oracle if the glue structurally only holds the summary (then the RED proves the scan reaches a
seeded-raw payload). Demonstrate the scan goes RED against a nested-raw-token variant.

#### Step 6: GREEN — Implement
Changes to make:
- `tests/plan/test_generate_plan_skill_glue.py`: confirm the glue NEVER passes the raw intake into a
  dispatch payload — the glue holds ONLY the `deid_in` summary after the de-id-IN step, and every
  dispatch the driver yields carries `(domain, prompt, summary)` where `prompt` inlines the role
  profile + the de-identified summary (the `_dispatch_prompt` shape, summary-only). The recursive scan
  asserts this over a seeded-raw fixture. No production change — the property holds because the glue
  discards the raw intake after de-id-IN; pin it with the recursive scan.

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: PASS

#### (REFACTOR folded — the scan is a test helper. REGRESSION:)
Run: `.venv/bin/python -m pytest -q`
Expected: PASS

### Cycle 3: Steps 7-8 — no-fork-at-skill-level grep + the dispatch protocol + S94-deferral doc

#### Step 7: RED — Write Failing Tests
Call `/write-tests` for the skill glue (`tests/plan/test_generate_plan_skill_glue.py`) targeting:
- AC-3 (no-fork at the skill level): a grep over `.claude/skills/generate-plan/SKILL.md` finds 0
  copies of the `while True:` / `safety_passed is True` / scratch-and-promote control flow — the skill
  drives the ONE shared driver, it does not re-host the loop (the same probe as ADR-0026-T1 AC-2,
  applied to the skill). A test shells the grep and asserts the count == 0.
- AC-1 prose-half (de-id path named): a grep over `SKILL.md` finds the `deid_in` / `ModelClient.
  deidentify` de-id-IN path named AND finds the superseded `router.summarize(store_read) [0-raw-PII]`
  de-id-IN line REMOVED/replaced (it is no longer the de-id-IN).
- AC-5 (S94-deferral documented): a grep over `SKILL.md` finds prose documenting that the LIVE
  subscription dispatch is the S94 operator-present attestation (NOT a mock-test target) — so what IS
  vs ISN'T mock-testable is explicit.

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: FAIL (the SKILL.md prose does not yet carry the A′ subscription-driver protocol, the
no-fork constraint statement, or the S94-deferral doc — the Cycle-1 prose change was the de-id-IN line
only).

#### Step 8: GREEN — Implement
Changes to make:
- `.claude/skills/generate-plan/SKILL.md` (Modify): reconcile the superseded runtime-A prose to the
  A′ subscription-driver path. Replace the Phase-1/2 "agent-in-the-loop" + direct
  `pipeline.run_generation` dispatch ([:17-21, :49-57]) with: (1) the de-id-IN via
  `ModelClient.deidentify` (already done Cycle 1); (2) dispatch each plan-domain specialist + each
  safety lens as a SUBSCRIPTION Claude Code agent (full role profile inlined per INV-ROLE-INLINING)
  over the de-identified summary, feeding each captured envelope to the shared driver PER YIELDED
  dispatch-request; (3) drive `plan_driver` (which runs assemble/gates/revise via the composed
  `gate_dispatch`) — the skill CALLS the shared driver and does NOT re-implement the loop (state the
  no-fork-at-the-skill-level constraint explicitly); (4) `reinsert_out` (deterministic) →
  `reemit_maintained` render. Add the S94-deferral note: the LIVE subscription dispatch over real
  agents is the operator-present S94 attestation, not a mock-test target; the residual
  0-raw-PII-to-a-REAL-agent property is observed at S94 (SEC-6). Ensure NO `while True:` /
  `safety_passed is True` / scratch-and-promote control-flow copy appears in the prose (the skill
  drives the driver; the loop lives in `plan_driver.py` only). (satisfies AC-3, AC-1 prose, AC-5)

Run: `.venv/bin/python -m pytest tests/plan/test_generate_plan_skill_glue.py -q`
Expected: PASS

#### (REFACTOR folded — prose reconciliation. REGRESSION:)
Run: `.venv/bin/python -m pytest -q`
Expected: PASS (the full suite green; the skill prose change touches no Python).

**TDD step count: 8 (3 cycles, REFACTOR/REGRESSION folded on cycles 2-3).** Within the ≤10-cycles
guidance; the 6 ACs split into the glue contract (de-id-IN + drive-driver + recursive-0-PII) + the
prose-doc (no-fork + de-id-path + S94-deferral). One modified skill (prose) + one new test file.

## Interface Contracts

This task does NOT create or modify a shared Python interface — it RECONCILES the skill prose (a
front-door doc) and adds a glue-contract test over EXISTING seams. The skill CONSUMES the ADR-0026-T1
`plan_driver` drive-protocol, the ADR-0026-T2 composed `gate_dispatch`, and the ADR-0027-T1
`ModelClient.deidentify` — it defines no new contract. The dispatch protocol it DOCUMENTS (de-id-IN
via `ModelClient.deidentify` → subscription specialist/lens dispatch over the summary → drive
`plan_driver` → `reinsert_out` → `reemit_maintained`) is a USE of those upstream contracts, not a new
one. No downstream task consumes an interface this task introduces.

## Verification Checklist

- [ ] AC-1 (de-id via `ModelClient.deidentify`, not `router.summarize`) — verified by
      `test_glue_deid_in_routes_through_model_client` (the glue drives the `ModelClient.deidentify`
      seam) + `test_skill_prose_names_deid_in_path` (grep: `SKILL.md` names `deid_in`/`ModelClient.
      deidentify`, the `router.summarize` de-id-IN line removed).
- [ ] AC-2 (0-raw-PII to any dispatch, RECURSIVE scan) — verified by
      `test_no_raw_pii_in_any_dispatch_payload_recursive` (recursive scan of the full serialized
      payload → 0 raw tokens; demonstrated RED against a nested-raw-token variant).
- [ ] AC-3 (no-fork at the skill level) — verified by `test_skill_md_no_forked_loop` (grep `SKILL.md`
      for `while True:` / `safety_passed is True` / scratch-and-promote → 0 copies).
- [ ] AC-4 (glue drives the shared driver) — verified by `test_glue_drives_plan_driver_to_promote`
      (fixture envelope per yielded request → driver completes a synthetic run, 0 live spend).
- [ ] AC-5 (S94-deferral documented) — verified by `test_skill_prose_documents_s94_deferral` (grep
      `SKILL.md` for the live-dispatch-is-S94-attestation note).
- [ ] AC-6 (suite gate) — verified by `.venv/bin/python -m pytest
      tests/plan/test_generate_plan_skill_glue.py` (0 live calls).
- [ ] Wave-3 skill gates carried: 0-raw-PII-to-any-dispatch (recursive payload scan) [AC-2],
      no-fork-at-skill-level [AC-3], de-id-via-`ModelClient.deidentify` [AC-1], glue-drives-driver
      [AC-4], S94-deferral [AC-5]. The residual live-subscription-dispatch 0-raw-PII-to-a-REAL-agent
      property (SEC-6) is EXPLICITLY flagged for the S94 checkpoint owner — the mock-tested build
      verifies only the glue-contract level (the glue STRUCTURALLY holds only the summary).
- [ ] EXTEND-NOT-REBUILD gate green: `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine
      files → 0 changed lines (the skill is prose; the glue test drives existing seams).
- [ ] No regression in full test suite (`.venv/bin/python -m pytest -q`).
- [ ] Files modified match file manifest (`.claude/skills/generate-plan/SKILL.md` +
      `tests/plan/test_generate_plan_skill_glue.py`) — no scope creep.
- [ ] Interface contracts documented (the explicit "no new shared interface" statement; the
      dispatch-protocol DOC is a use of the upstream contracts).

## Commit

```
feat(skill): generate-plan A-prime subscription driver
```
Stage only:
- `.claude/skills/generate-plan/SKILL.md`
- `tests/plan/test_generate_plan_skill_glue.py`

Stage by explicit path (`git add <path>` as its own command, then `git commit` separately — the
PreToolUse hook denies single-call stage+commit, `git commit -a/--all`, and pathspec
`git commit <path>`). Do NOT `git add vault/` or the daemon frontmatter churn (CLAUDE.md § Vault
hygiene). Do NOT stage `.beads/issues.jsonl` / `harvest.jsonl` / `memory/process-failures.md`.

## Rollback

If verification fails after 3 fix cycles:
1. `git stash -m "failed-ADR-0026-T3-attempt-{N}"` — preserve work for diagnosis.
2. `git checkout {commit-before-task}` — revert to the entry-state commit (the Wave-2 → Wave-3
   checkpoint HEAD).
3. Update the bead tracker: flag ADR-0026-T3 as BLOCKED with the failure log.
4. Escalate: "Task ADR-0026-T3 failed verification after 3 attempts. Stash ref: {ref}. Failure log:
   {summary}."
5. After abandonment or re-planning, drop all `failed-ADR-0026-T3` entries from `git stash list`.

Do NOT: silently skip failing acceptance criteria, weaken tests to make them pass (especially the
recursive 0-raw-PII scan + the no-fork grep — a crown-jewel probe that cannot go RED is worthless),
or proceed to the wave checkpoint with a broken state. A no-fork-at-skill-level violation (a
skill-prose copy of the safety loop) is the A-naive forked-safety-loop failure class — HALT, route
back to drive the ONE shared driver. A 0-raw-PII RED is release-blocking (ADR-0005 falsification) —
HALT.
