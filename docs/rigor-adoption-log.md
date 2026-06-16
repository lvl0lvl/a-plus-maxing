---
title: Rigor Framework Adoption Log — a-plus-maxing
type: ledger
owner: Walter McGivney
created: 2026-06-15
last_reviewed: 2026-06-15
status: complete
review_cadence: frozen-post-adoption
rigor_version_adopting: 1.0.0
permalink: a-plus-maxing/rigor-adoption-log
---

# Rigor Framework Adoption Log — a-plus-maxing

> **Instance identity (read first).** This is the **a-plus-maxing** adoption instance — one project's
> deployment record. **Each project that adopts the Rigor Framework keeps its OWN adoption log** with
> its own deployment specifics, issues, and version pin. When the Discipline-11 / Loop-B harvest lays
> these side by side, they are compared as DISTINCT instances — do NOT merge, generalize, or copy this
> log's a-plus-specifics into another project's log. The framework-generic patterns (what recurs across
> ≥2 instances) belong in the framework doc / a future implementation skill, NOT here. a-plus pinned
> `rigor_version: 1.0.0` (root `rigor_version`); another instance may pin a different version.

**What this is.** A living, project-specific record of how a-plus-maxing adopted the
Rigor Framework v1.0.0 toolkit (`~/Documents/Projects/skills_library/frameworks/rigor/`):
the method, the per-step implementation, the issues hit (especially the ones that forced
an adjustment or failed outright), and the verification evidence. It is **not** written to
be generic — it is the specifics, with enough context that another project can extrapolate
to its own situation.

**Why it exists / how it gets used.** This is the per-deployment **ledger** that the
framework's own Discipline 11 (Cross-Deployment Learning) / Loop B harvest consumes:
multiple projects' adoption logs get laid side by side, and recurring issues (convergence
≥2 projects) are promoted into a framework change, a new toolkit audit, or an *implementation
skill* for future adopters. So the high-value content here is the **Issues** section — the
friction another adopter will also hit.

**Maintenance contract (read this).** This log is maintained **through the full adoption**
(updated at each adoption-session close — see the Change Log at the bottom) until every
wave is merged and the loop is fully wired. **Post-adoption it freezes** — it is retained
(never deleted) as the Loop-B harvest input, but it stops being actively maintained because
the standing self-improvement system takes over (PF log + `harvest.jsonl` + `harvest-gate`
+ the close-disclosure ledger catch new issues going forward). The ONE thing that is NOT
"done forever": the Discipline 11 **pull cadence** — at each drift-audit boundary we diff
`rigor_version` against the framework's `VERSION`, read the CHANGELOG delta, and pull
(re-running `toolkit/tests/run-all-tests.sh` first). That is steady-state maintenance of the
*toolkit dependency*, not of this log. See §8.

---

## 0. Status (current)

| Wave | Scope | State |
|---|---|---|
| **A** | Mechanical floor + version pin + self-improvement loop + close gate | **DONE + MERGED (S64, PR #139 → `main`)** |
| **B** | Approaches ledger + disclosure ledger + `falsification-scan` advisory + core-capability-first forcing function | **DONE (S65)** — mechanical core-capability gate script deferred WITH `71s4` (its checks depend on the path shape) |
| **C** | `plan-integrity` role wiring + INVARIANTS rows for the new gates (change-discipline ritual) | **DONE in-repo (S65)** — `INV-CLOSE-AUDIT` + `INV-HARVEST-CAPTURE` registered (Walter-approved); plan-integrity wired into V1 Build Execution |
| **D** | Sync stale global `~/.claude/skills` + `~/.claude/commands` to the library | **DONE (S66)** via the library's own `deploy-and-verify` (anchor + symlink-deploy + parity), then a full mirror of the 50 stale-April shadows → library symlinks; 9 local-only skills preserved; 0 dead symlinks |

**All four waves complete (S64–S66). This log is now FROZEN** (`status: complete`) and retained as the Loop-B harvest input; the standing self-improvement system (PF log + `harvest.jsonl` + `harvest-gate` + the close-disclosure ledger) takes over. The ONLY ongoing discipline is the Discipline-11 **pull cadence** (§8).

Post-adoption follow-ons (tracked by the standing system, NOT this log): `0qf6` (wire `enforce-heartbeat-clause` once a dispatch convention carries the liveness clause), `9etx` (the PF-S64-01 standing fix — non-mutating git for review agents + post-dispatch branch re-verify), `po4x` (UPSTREAM toolkit harvest-gate/pf-ingest fix — framework-side), `p5wx` (init_instance auto-provision `.venv`), `7may` (provenance-audit interpolation hardening). The core deliverable `71s4` (plan generation + the mechanical core-capability gate) is parked pending design + Pencil. **`d1kc` / `ckl1` / `eyn4` / `4hmo` CLOSED.** Library-side parity residual (not a-plus's): `upgrade-skill.md` references 2 transient staging paths that aren't deployed at rest (a skills_library artifact-repair item).

---

## 1. Why we adopted (the trigger)

a-plus relaxed its homegrown rigor framework on agent advice and drifted for ~a week of
sessions, shipping a large individually-tested substrate (store, ingestion incl. the WHOOP
adapter, PII routing, plan-composition logic, render/dashboard/report) while **never wiring
the one capability the system exists for: generating a followable health plan end-to-end**
(`memory/process-failures.md` PF-S63-02). The Rigor Framework v1.0.0 — which a-plus is itself
a named source deployment of — had meanwhile shipped a *re-tightened*, runnable toolkit with
exactly the missing machinery (a self-improvement loop, a fail-closed close gate). Adopting it
is the governance precondition for safely rebuilding the core deliverable under rigor.

**Extrapolation note for other projects:** the trigger here was a specific drift failure, but
the adoption value is the same for any project that has been running un-enforced prose
disciplines — the toolkit converts "we have a rule" into "the gate bites and proves it can."

---

## 2. Starting state — a-plus was a MATURE re-adopter, not greenfield

This is the most important context for extrapolation: **a-plus already implemented Disciplines
1–9 bespoke** over ~63 sessions (an INVARIANTS register with 16 IDs, a 6-clause rotation rule,
an in-repo PF log, per-invariant audit scripts, a role-inlining hook at v2.5, PII/wiki commit
hooks). So adoption was **the delta**, not `fresh-start` from scratch. If your project is
greenfield, run the `/fresh-start` command instead — it scaffolds all of this at once. If
your project is mature, do what this log describes: a gap analysis, then take only what you lack.

The gap analysis that drove the plan (toolkit artifact → did a-plus already have it):

| Toolkit artifact | a-plus status | Action taken |
|---|---|---|
| `hooks/block-{dangerous,push-main,commit-main}.sh` | ALREADY HAVE (bespoke, wired) | keep ours |
| `hooks/enforce-role-inlining.sh` | ALREADY HAVE (at v2.5 — *more* evolved than toolkit) | keep ours |
| `hooks/enforce-heartbeat-clause.sh` | NEW | vendored; **wiring deferred** (see Issue #1) |
| `scripts/pf-attestation-audit.sh`, rotation/stale-hash | ALREADY HAVE (in `handoff-audit.sh` + `pf-attestation-audit.sh`) | keep ours; toolkit = upstream |
| `scripts/close-audit.sh` | NEW (had a prose list, no meta-gate) | adopted as `scripts/close-audit.sh` (Issue #4) |
| `scripts/harvest-gate.sh` + `pf-ingest.sh` + `schemas/harvest-record.md` | NEW | adopted (self-improvement loop) |
| `scripts/falsification-scan.sh` | NEW | deferred to Wave B (advisory) |
| `scripts/parity-audit.sh`, `consistency-audit.sh`, `role-completeness-audit.sh` | NEW, library-tree-scoped | not applicable to a-plus's tree; deferred |
| `lib/audit-helpers.sh` | ALREADY HAVE (diverged interface, no `skipped()`) | backported `skipped()`/FATAL-on-skip (Issue #3) |
| `lib/test-lib.sh` + `tests/run-all-tests.sh` | NEW (had 11 tests, no runner) | added a-plus aggregator `scripts/tests/run-all-tests.sh` |
| a-plus-only: wiki-ingest, research-provenance, scope-contract, skill-trace, branch-completeness, PII hooks | n/a (no toolkit counterpart) | kept — domain-specific |

**Decisions locked with the operator before building** (these are the load-bearing choices an
adopter must make):
1. **Vendor the toolkit (copy), don't reference by symlink.** Copied to `toolkit/` so it
   survives clone/move and `close-audit` resolves from `${CLAUDE_PROJECT_DIR}`. Symlinking
   recreates the absolute-path fragility the framework warns against (F-003).
2. **Keep bespoke audits; toolkit is the upstream for future pulls.** Do not replace
   domain-tuned, more-evolved scripts with the generics.
3. **Wave A first** (mechanical floor + loop + close gate), B–D beaded as follow-ons.
4. **Global skills/commands sync (Wave D) is a separate task** — it touches `~/.claude/`,
   not the repo, so it cannot ride in the adoption PR.

---

## 3. Method (how the work was scoped)

1. Read the framework + toolkit **myself** (RIGOR_FRAMEWORK.md 1185 lines, toolkit README,
   SELF_IMPROVEMENT_PLAYBOOK, CHANGELOG, VERSION, the `plan-integrity` role) — the synthesis
   is the orchestrator's, not delegable.
2. Fanned out **read-only catalog/gap agents** in parallel: (a) role catalog, (b) skills/commands
   catalog + staleness vs the live global dirs, (c) the toolkit-vs-a-plus gap analysis above.
3. Read `commands/fresh-start.md` as the **yardstick** for the target scaffolded shape.
4. Wrote a phased scope contract; got operator sign-off on the four locked decisions.

---

## 4. Wave A — per-AC implementation

All on branch `feature/rigor-toolkit-adoption`, commit `56c0ab9`.

- **AC1 — vendor `toolkit/`.** `cp -Rp "$LIB/frameworks/rigor/toolkit/." toolkit/ && chmod +x
  toolkit/{hooks,scripts,tests}/*.sh`. Verified pristine: `toolkit/tests/run-all-tests.sh` → 14/14.
- **AC2 — pin `rigor_version: 1.0.0`.** New "Rigor Framework (vendored toolkit)" section in
  CLAUDE.md: version + Discipline-11 pull cadence + "don't edit vendored scripts" + what we
  adopted vs kept.
- **AC3 — heartbeat hook (CHANGED → vendored only).** See Issue #1.
- **AC4 — self-improvement loop.** Created `harvest.jsonl`; **back-filled PF-S63-02** as the
  first gate-valid FAIL record (dogfooding the loop on the failure that motivated it) + bead
  `71s4`. Verified `harvest-gate.sh --pf <fixture> --harvest harvest.jsonl --beads
  .beads/issues.jsonl --session 63` → PASS (3-layer), and FAIL on a missing layer. Added a
  close step 8.6 in CLAUDE.md.
- **AC5 — close gate.** Built `scripts/close-audit.sh` (Issue #4) + `scripts/tests/run-all-tests.sh`
  aggregator + `scripts/tests/test_close_audit.sh` (8/8, proves it bites). Repointed CLAUDE.md
  close step 8.5 at the gate.
- **AC6 — `skipped()`/FATAL-on-skip.** Backported into `scripts/lib/audit-helpers.sh`
  backward-compatibly (Issue #3); `test_audit_helpers.sh` extended 9→14 cases → 23/23.

---

## 5. Issues encountered (the part future adopters need most)

### Issue #1 — `enforce-heartbeat-clause.sh` fires on EVERY Task dispatch → would break gated skills. **(forced an adjustment)**
The hook DENYs any Task dispatch whose prompt lacks all 3 liveness markers — with **no
role-tag gating** (unlike `enforce-role-inlining`, which only fires on role-shaped dispatches).
Wiring it would deny `/review-pr`'s and `/aplus-research`'s own internal agent dispatches,
including the `/review-pr` + `/merge` needed at this very session's close.
- **Resolution:** vendor + document the hook, **defer live-wiring** (bead `0qf6`) until the
  dispatch flows (the synced skills + a project dispatch convention) carry the clause. This is
  correct sequencing, not a dodge — you don't switch on a dispatch-gating hook before the
  dispatch templates satisfy it.
- **Extrapolation:** any project wiring this hook must FIRST ensure every Task-dispatching skill
  it uses (review-pr, research pipelines, custom orchestration) inlines the liveness clause.
  Likely a convergent issue → candidate for the implementation skill to call out explicitly.

### Issue #2 — `test_settings_hook_paths.sh` hardcodes the `.claude/hooks/` prefix. **(latent; deferred with #1)**
a-plus's settings-path test asserts every wired hook lives under
`${CLAUDE_PROJECT_DIR}/.claude/hooks/`. A vendored toolkit hook lives under `toolkit/hooks/`,
so wiring it would RED that test.
- **Resolution (planned, lands with `0qf6`):** extend the test to also accept the
  `${CLAUDE_PROJECT_DIR}/toolkit/hooks/` portable prefix (still enforcing no-absolute-paths +
  existence), rather than copying the hook out of the toolkit (which would break pull-in-place).
- **Extrapolation:** if your project enforces hook-path portability, it must learn the
  `toolkit/hooks/` location before you wire any toolkit hook.

### Issue #3 — `audit-helpers.sh` interface divergence. **(reconciled, not swapped)**
a-plus's lib uses `audit_init/violation/info/audit_summary/audit_exit` (exit 0/1); the toolkit's
uses `emit/warn/fail/skipped/verdict` (exit 0/1/2). The real capability gap was **`skipped()` /
FATAL-on-skip** (F-008) — a-plus audits couldn't distinguish "ran clean" from "couldn't run."
- **Resolution:** **backport** `skipped()` + a FATAL-on-skip path into `audit_exit` (violations
  take precedence; `AUDIT_ALLOW_SKIP=1` opt-out) rather than swapping the whole interface and
  rewriting 9 audits. Kept backward compatibility: existing audits never call `skipped()`, so
  their behavior is byte-identical. The summary line gained `, N skipped` — substring-compatible,
  so existing `assert_contains` tests stayed green.
- **Extrapolation:** prefer additive backport over interface migration when many call sites exist.

### Issue #4 — toolkit `close-audit.sh` forwards ONE child-arg set; a-plus audits have heterogeneous args. **(forced a build choice)**
The toolkit's `close-audit.sh` is parameterizable but forwards the same `CLOSE_AUDIT_CHILD_ARGS`
to every constituent. a-plus's audits are heterogeneous: some need `--session N`
(scope-contract, pf-attestation, skill-trace), some take no args (handoff, branch-completeness).
A single child-arg set can't drive them.
- **Resolution:** build a **self-contained `scripts/close-audit.sh`** that embodies the toolkit's
  fail-closed pattern (run the negative-test floor first; map exit 0→PASS, 1→FAIL, ≥2/missing→
  SKIPPED/FATAL) but carries an a-plus roster with per-entry args (a `script|args` list with a
  `{SESSION}` placeholder). The vendored toolkit `close-audit.sh` stays **pristine** (no fork).
  Shipped with its own negative test (`test_close_audit.sh`, 8/8).
- **Extrapolation:** if your close audits have uniform args, you can drive the vendored
  `close-audit.sh` directly via `$CLOSE_AUDIT_SCRIPTS`. If heterogeneous, write a thin
  project wrapper — but keep the vendored script unforked so future pulls apply.

### Issue #5 — `pf-ingest` output schema ≠ `harvest-gate` required fields. **(impedance mismatch; worked around)**
`pf-ingest.sh` emits a record keyed `record_type/pf_id/.../nominated`; `harvest-gate.sh` requires
`id/class/source_refs/detection_mode/recurrence_count` (per `harvest-record.md`). Piping
`pf-ingest` straight into `harvest.jsonl` would NOT pass the gate. Separately, `harvest-gate`
matches on the **PF-id token** appearing as the record's `id`, while the schema's example `id`
is `FAIL-<DEPLOY>-<NNN>`.
- **Resolution:** hand-write **gate-valid** FAIL records following `harvest-record.md`, with
  `id` set to the a-plus **PF-id token** (e.g. `"PF-S63-02"`) so `harvest-gate` discovers it.
  Use `pf-ingest` for its other job — generating the anti-pattern stub that hardens the role/skill.
- **Extrapolation:** likely a convergent toolkit rough edge (pf-ingest↔harvest-gate↔schema
  three-way drift) — flag for the framework harvest. Until reconciled upstream, hand-author the
  gate-valid record and key `id` on your project's PF-id scheme.

### Issue #6 — `scope-contract-audit.sh` requires the exact `Acceptance criteria:` label + a binary `[ ]`/`[x]` checkbox. **(self-caught, fixed)**
The S64 scope contract first used `Acceptance criteria (Wave A):` (colon not adjacent) and a
`- [~]` marker. The audit's regex is `^\s*Acceptance criteria:` and it accepts only `- [ ]`/`- [x]`.
Both the audit AND its negative test (which exercises the real HANDOFF) went RED.
- **Resolution:** `Acceptance criteria: (Wave A)` + change `[~]` → `[x]`. Green.
- **Extrapolation:** when you add the adoption session's scope contract, match your
  scope-contract audit's exact field labels/markers — don't decorate the field headers.

### Issue #7 — pre-existing environmental red surfaced by the new aggregator. **(NOT ours; beaded + excluded loudly)**
The new `scripts/tests/run-all-tests.sh` surfaced that `test_audit_research_provenance.sh` fails
2 valid-chain cases. **Isolated as pre-existing** (reverting `audit-helpers.sh` to HEAD reproduces
it). Root cause: `gate_attest.py verify-chain` needs `jsonschema`, absent from both `.venv` and
`python3`. It tests a *conditional* audit, not a per-close roster member.
- **Resolution:** bead `d1kc`; the close gate **default-excludes** it from the a-plus floor with
  a printed reason (`RUN_ALL_TESTS_EXCLUDE` is loud — a stale exclusion naming a missing test
  fails the run, so exclusions can't rot silently). **(S65: FIXED via `d1kc` — `jsonschema`
  installed into `.venv` + the audit repointed at the `.venv` python; the default exclusion was
  DROPPED, full floor 13/13 green. See Issue #9.)**
- **Extrapolation:** a new aggregator often surfaces pre-existing reds. Don't chase them inside
  the adoption (scope discipline) — isolate, bead, and exclude *loudly with a reason*, never silently.

### Issue #8 — `harvest-gate` over-extracts prior-PF-id tokens; `skill-trace` escape sentence must be line-anchored. **(hit at the FIRST close using the gates; documented + beaded `po4x`)**
The first session-close *using* the adopted gates surfaced two close-attestation format constraints
that another adopter's first close will also hit:
- `harvest-gate.sh` token-greps the current session's PF section for every `PF-S{N}-{NN}` / `FAIL-…`
  token and requires EACH to be captured in `harvest.jsonl` + a bead. A "No new PF" close whose
  attestation cites PRIOR PFs by token (e.g. `PF-S6-01 HELD`) **false-fails** — the gate cannot tell
  a this-session failure from a prose reference to a prior one (and the framework's own PF template
  has a `Recurrence: prior-ids` field that invites exactly such references).
- `skill-trace-audit.sh` requires the zero-PR escape sentence `No PR lifecycles ran this session.`
  to be **line-anchored** (start of line, optional leading `**`); a mid-prose mention after a bold
  label on the same line does NOT waive the per-PR table requirement.
- **Resolution / workaround:** reference prior PFs DESCRIPTIVELY in the session's PF section (keep
  only genuinely-captured tokens — here, the back-filled `PF-S63-02`); put the escape sentence on its
  own line. Beaded `po4x`.
- **Extrapolation:** likely **convergent** (every adopter's first close). Strong candidate for the
  implementation skill to pre-empt with a close-attestation template that is harvest-gate /
  skill-trace-clean by construction, and for the framework harvest to consider tightening
  `harvest-gate`'s extraction so a `Recurrence:` reference is not read as a this-session failure.
  **(S65: a-plus-side mitigation landed — the close-attestation template is now in CLAUDE.md close
  step 8.6, clean by construction; bead `po4x` stays open for the UPSTREAM toolkit fix.)**

### Issue #9 — the governance script called system `python3`, but the dep lived in the project venv. **(Wave B/C deferred fix `d1kc`; fixed S65)**
`scripts/audit-research-provenance.sh` delegates chain-integrity to `gate_attest.py verify-chain`,
which imports `jsonschema`. The audit called bare `python3` (homebrew, `/opt/homebrew/bin/python3`)
— a SEPARATE interpreter from the project's `.venv` (an isolated venv, `include-system-site-packages
= false`). Neither carried `jsonschema`, so 2 valid-chain test cases failed and the close gate
default-excluded the test (Issue #7).
- **Resolution:** install `jsonschema` into `.venv` (`.venv/bin/python -m pip install jsonschema`)
  and resolve a `PY="$REPO_ROOT/.venv/bin/python"` once in the audit, using it for all three python
  invocations — the project's canonical runtime is `.venv` (CLAUDE.md; the whole pytest baseline uses
  it), so no fallback chain is needed (a missing `.venv` fails the governance check CLOSED, which is
  correct). Test → 8/8; the close-gate floor exclusion was then dropped (full floor 13/13).
- **Extrapolation:** a vendored gate with a third-party dependency must run under the interpreter that
  actually carries the dep. If your test baseline already uses a venv, point every governance script's
  python at that SAME venv (not bare `python3`) — a split interpreter is the silent cause of "the audit
  can't import X here." A NEW aggregator surfacing this (Issue #7) is the same story from the other end.

### Issue #10 — wiring an ADVISORY check into a FAIL-CLOSED gate. **(Wave B; build choice)**
`falsification-scan` is WARN-only by design (heuristic prose match; the framework keeps it advisory so
operators don't route around a noisy hard-fail). But `close-audit.sh` maps every constituent's exit
≥2 → FATAL — so adding the scan to the blocking roster would FATAL exactly when there is no note to
scan, and its WARNs (exit 0) would be invisible. Advisory ≠ roster member.
- **Resolution:** a clearly-marked NON-GATING block in `close-audit.sh` AFTER the roster — it extracts
  ONLY the current session's `## Session <N>` PF section (scanning the whole log false-WARNs on
  historical entries that quote an anti-pattern to refute it), pipes it to the vendored scan, and
  `info`-logs the result with the exit code intentionally DISCARDED. A negative-test case (C14) proves
  a PF section that trips an anti-pattern still exits 0 AND that the WARN is surfaced.
- **Extrapolation:** integrate advisory checks OUTSIDE the pass/fail roster and prove non-gating with a
  test. Scope the scan to the current unit (this session's note), never the whole historical log.

### Issue #11 — Wave D "sync" was a 50-shadow machine-wide MIRROR, not a few stale files. **(S66; the bead under-described the scope)**
The `ckl1` bead read "sync stale global `~/.claude/skills`+`commands` to the library." The reality:
the global dirs were 40 real skills + 33 real commands, of which **50 were stale-April real copies
SHADOWING the now-current (June) library** (the 50 span 31 library-overlapping skills + 19 commands;
the library had caught up 72 commits at adoption), plus **9 genuinely-local skills** (UI/quant, some
symlinked into a separate `~/.agents/skills/` collection) that must be PRESERVED. A blind symlink-swap
or overwrite would have lost the 9 local skills. (The library also held 12 skills the global dir lacked
entirely — `deploy-and-verify` symlinked those in cleanly, which is why the end-state 43 library skills
exceeds the 40 the global started with.)
- **Resolution:** use the library's OWN sanctioned mechanism — the `deploy-and-verify` command
  (idempotent, non-clobbering, fail-closed via `parity-audit`): it established the
  `~/.claude/skills_library` anchor, symlinked the entirely-missing library items, and SKIP-reported
  the 50 shadows (never clobbering). Then, after confirming the shadows were stale-old not locally-edited
  (global `review-pr.md` mtime 2026-04-09 vs library `skills/` last commit 2026-06-15; the diffs were the
  72 commits), a **full mirror** replaced the 50 shadows with library symlinks under a pre-made backup
  tarball. The 9 local-only skills were never iterated (not library-named) → preserved. End state:
  43 library skills + 33 commands as symlinks (track the library, no future staleness), 0 dead links.
- **Extrapolation:** a mature project's global skills/commands almost always carry BOTH stale shared
  copies AND genuinely-local items. NEVER blind-overwrite. Use `deploy-and-verify` (non-clobbering) to
  surface the shadows, confirm direction (stale vs local-edit, by mtime/diff), back up, then mirror. The
  symlink model (matching how `roles`/`library` already deploy) ends staleness permanently.
- **Issues left as library-side residual (NOT the adopter's):** `parity-audit` stays `rc=1` on
  `upgrade-skill.md`'s references to 2 transient staging paths (`.upgrade-skill.in-progress`,
  `upgrade-skill.md.staged`) that exist only DURING an upgrade-skill run — a skills_library artifact;
  `deploy-and-verify`'s own spec says to report these as remaining library work, not a deploy failure.
- **Near-miss noted (no harm):** the post-mirror integrity check first used `[ -d ] && [ ! -L ]` to
  assert the local skills survived, which FALSE-alarmed on the 7 `~/.agents/skills/` symlinks (they are
  symlinks, not real dirs). Nothing was lost (the loop never touched them); the lesson is to verify a
  destructive op with a RESOLVE check (`[ -e ]` + `readlink`), not a structural-type assumption.

---

## 6. Verification evidence (S64 / Wave A)
- `toolkit/tests/run-all-tests.sh` → 14/14
- `scripts/tests/test_audit_helpers.sh` → 23/23 (9 original + new skipped/FATAL cases)
- `scripts/tests/test_close_audit.sh` → 8/8 (PASS/FAIL/FATAL/precedence/{SESSION}/allow-skip all bite)
- `scripts/tests/run-all-tests.sh` (with close-gate exclusion) → 11 passed, 0 failed, 1 excluded
- `scope-contract-audit.sh --session 64` → PASS; `handoff-audit.sh` → PASS
- `harvest-gate` → PASS (3-layer) and FAIL on a missing layer
- product baseline `.venv/bin/python -m pytest -q` → 833 passed, 2 skipped (unaffected)

---

## 7. Deferred / open (beaded)
- `ckl1` (P2) — **Wave D:** sync stale global `~/.claude/skills` + `~/.claude/commands` to the library (parity-audit verified). Its own focused session — touches `~/.claude/` (machine-wide, every project on the box), so it cannot ride the in-repo PR.
- `0qf6` (P2) — wire `enforce-heartbeat-clause` (+ extend `test_settings_hook_paths.sh` for the `toolkit/hooks/` prefix) once the dispatch flows (the synced skills + a dispatch convention) carry the liveness clause; couples with Wave D. Wiring it earlier would deny every Task dispatch incl. `/review-pr`'s own.
- `71s4` (P1) — build the core plan-generation path + the core-capability MECHANICAL gate (the actual PF-S63-02 fix; the forcing-function half landed S65).
- `po4x` (P3) — the UPSTREAM toolkit fix (harvest-gate over-extraction + pf-ingest↔harvest-gate schema drift). The a-plus-side workaround (close-attestation template) landed S65; stays open as a framework-harvest (Loop-B) input.
- `d1kc` — **CLOSED S65** (`jsonschema` in `.venv` + the provenance audit repointed at the `.venv` python; close-gate floor exclusion dropped; full floor 13/13).

---

## 8. Maintenance plan + answer to "can we move on post-implementation?"

**During adoption (Waves A→D):** maintain this log — append a Change Log row at each adoption
session close (state what wave landed, new issues, resolutions).

**Post-adoption:** freeze this log (status → `superseded`/`complete`) but **retain** it as the
Loop-B harvest input. You are right that we can then move on from actively maintaining it,
**because** the standing self-improvement system takes over: every future failure is caught and
captured by PF log + `harvest.jsonl` + `harvest-gate` (three-layer, fail-closed at close) and
the close-disclosure ledger. That is the system "catching future issues" you described.

**The one nuance worth flagging (in case it reads as a gap):** "move on" applies to *this log*,
not to the framework dependency. The Discipline 11 **pull cadence** is ongoing, low-effort,
steady-state maintenance — at each drift-audit boundary, diff `rigor_version` (1.0.0) against the
framework `VERSION`, read the CHANGELOG delta, and pull, re-running `toolkit/tests/run-all-tests.sh`
before adopting any new audit. That is not adoption work; it is keeping a pinned dependency current,
and it is itself a standing discipline rather than a thing we babysit.

---

## 9. Change Log (the living-log part — append at each adoption session close)

| Date | Session | Wave | What landed / changed | New issues |
|---|---|---|---|---|
| 2026-06-15 | S64 | A | Vendored toolkit, pinned `rigor_version 1.0.0`, built close gate + self-improvement loop + `skipped()`/FATAL-on-skip; committed `56c0ab9`. Close ran clean: `close-audit --session 64` 0 violations, `harvest-gate` PASS, pytest 833/2. | #1 heartbeat-on-every-dispatch (deferred `0qf6`), #5 pf-ingest↔harvest-gate schema mismatch, #7 pre-existing provenance red `d1kc`, **#8 harvest-gate/skill-trace close-attestation format constraints `po4x` (hit at the first close)**. |
| 2026-06-15 | S64 | A | **Landed Wave A** — opened PR #139, ran `/review-pr` (6-agent, blind triage + blind verify) + `/merge`. Review found 18 findings → 14 LEGITIMATE fixed + blind-verified 14/14, 4 NOT_A_BUG. The fixes hardened the new code: F1 closed a real fail-OPEN (an exported `AUDIT_ALLOW_SKIP=1` defeating F-008 across constituents — `unset` on lib source); F3 `local` in `run_one`; F5 `--session=` empty→exit 2; F7/F8/F9 added floor-path + allow-skip-vs-FAIL + stale-exclusion test coverage (the gates' RED paths now bite); F15/F16/F17 doc corrections (pf-ingest seeding wording, direct-invocation note, `rigor_version` file created). | The review earned its keep — a real fail-open (F1) and several untested gate paths (F7/F8/F9) that the first close had not exercised. Confirms the value of running `/review-pr` even on a governance PR. |
| 2026-06-15 | S65 | B + C | **Landed Waves B + C (in-repo).** Wave B: vendored `falsification-scan` wired as a NON-GATING close advisory (scans only the current session's PF section; test C14 proves non-gating; close-audit 15/15); approaches ledger created (`vault/approaches/` + `_template.md` + `README.md` + 1 genuine seed — the S63 `biomarker_meta` wearable-marker revert); disclosure ledger formalized as a named close step (CLAUDE.md step 4); core-capability-first FORCING FUNCTION adopted as a session-open step (mechanical gate deferred WITH `71s4`). Wave C: `plan-integrity` role wired into V1 Build Execution (read-only review role, NOT a deployed agent — correctly absent from branch-completeness); `INV-CLOSE-AUDIT` + `INV-HARVEST-CAPTURE` registered via the Walter-approved change-discipline ritual. `d1kc` FIXED (jsonschema in `.venv` + audit repointed; floor exclusion dropped, full floor 13/13); `po4x` a-plus-side template landed (CLAUDE.md step 8.6). | #9 split python interpreter (system `python3` vs project `.venv` — the dep lived only in the venv); #10 advisory-in-a-fail-closed-gate (advisory ≠ roster member; integrate outside the pass/fail roster + prove non-gating with a test). |
| 2026-06-15 | S66 | D | **Landed Wave D — the global skills/commands sync (machine-wide, not in-repo).** Ran the library's `deploy-and-verify` (anchor `~/.claude/skills_library` + non-clobbering symlink-deploy + `parity-audit`), then a full mirror of the 50 stale-April shadows → library symlinks (backup tarball pre-made; confirmed stale-not-local-edit by mtime/diff). 9 local-only skills preserved, 0 dead symlinks. **All 4 waves complete → this log FROZEN** (`status: complete`). `ckl1` closed. | #11 (Wave D was a 50-shadow mirror, not a few files — use `deploy-and-verify` non-clobbering + back up + mirror); library-side `upgrade-skill` parity residual (2 transient staging-path refs, not the adopter's); a verify-logic near-miss (use a resolve-check, not `[ -d ]`, after a destructive op). |

---

## 10. Pull-cadence log (post-adoption, ongoing — the ONE discipline that survives the freeze)

The adoption (§0–§9) is FROZEN. The Discipline-11 **pull cadence** is the one ongoing discipline (§8):
at each drift-audit boundary, diff the pinned `rigor_version` against the library `VERSION`, read the
`CHANGELOG` delta, and pull the `toolkit/` delta (re-running `toolkit/tests/run-all-tests.sh` first),
then bump the root `rigor_version`. This section logs each real run — it is the high-value reference
content for other adopters (the cadence's behaviour under real upstream drift).

| Date | Pinned | Library `VERSION` | Origin delta | Action | Outcome |
|---|---|---|---|---|---|
| 2026-06-15 (S66 post-close) | 1.0.0 | 1.0.0 | origin/main **+19 commits** ahead of the adopted `86a1a26` → `9b8b721` | **HELD the pin** (no versioned delta); ff-merged the LOCAL skills_library checkout to origin/main (refreshes the global `~/.claude` symlinks from Wave D — non-destructive; 0 new unlinked items, 0 dead symlinks) | **First real pull-cadence run.** The version pin worked AS DESIGNED — a-plus did NOT get pulled by 19 unversioned main commits. |

**Finding from the first run (the reference lesson — bead `lczu`):** the library shipped **toolkit
changes WITHOUT a `VERSION`/`CHANGELOG` bump** — `frameworks/rigor/toolkit/{consistency-audit,role-completeness-audit}.sh`
+ a new test changed (+326 lines) while `VERSION` stayed `1.0.0`. Because the a-plus pull cadence is
**keyed on `VERSION`**, it correctly reported "no delta" and held — BUT a version-pinned consumer will
therefore **MISS toolkit changes until the library cuts a versioned release**. For a-plus this is benign
(those two audits are library-tree-scoped, vendored-but-unused — `close-audit`/`harvest-gate`/`falsification-scan`
unaffected), and pulling unversioned mid-`main` changes would corrupt the meaning of "pinned at 1.0.0",
so the correct posture is to HOLD.

**Extrapolation for other adopters:** your version-keyed pull cadence is only as reliable as the
upstream's version discipline. If the library lets `toolkit/` drift on `main` without bumping `VERSION`,
your cadence silently won't see it. Mitigation: at the drift-audit boundary, ALSO `git fetch` the
library and check whether `main` is ahead of your adopted SHA (not just whether `VERSION` moved); if the
delta touches `toolkit/`, flag it upstream to bump `VERSION` rather than pulling unversioned changes.
(a-plus tracks this as bead `lczu`; the upstream fix is the library bumping `VERSION` + a `CHANGELOG` row.)
