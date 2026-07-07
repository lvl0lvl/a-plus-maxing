---
title: Session 111 — ADR-0039 scheduled-agent-runner build (merged)
type: session
date: 2026-07-06
status: complete
permalink: a-plus-maxing/sessions/session-111
---

# Session 111 — ADR-0039 build (local scheduled headless subscription runner)

Continuation of the operator-authorized continuous autonomous build loop ("run the loop until you have everything" / "continue through the whole build"). Built ADR-0039 — the plan-loop **cadence runtime**: a LOCAL scheduled headless Claude-Code **subscription** runner, **disabled by default**, greenfield `scripts/runner/` — end-to-end and **merged to `main`** (PR #298, merge commit `f384f3ae`).

## What was built
- **T1** — the runner driver (`cadence_runner.py`) + subscription-sub-agent dispatch seam (`subscription_dispatch.py`) + the single `plan_loop.signal(CADENCE_TRIGGER)` entry + the `python -m scripts.runner.cadence_runner` module entry (the T3 plist target). Raw `store.read_all` + `deid_in` stay in the Python driver → the subscription lane carries only de-identified summaries (crown-jewel non-egress, proven-non-empty + faithless-leak mutation-RED). SEC-04 default-factory refusal.
- **T2** — auth-isolation `build_subscription_env` (drops the metered/cloud-routing env surface, sets `CLAUDE_CODE_OAUTH_TOKEN` from the keychain, COPY-not-`os.environ`); `sk-ant-oat` token-VALUE scan = 0.
- **T3** — launchd (primary) + cron (fallback) scheduler + operator-owned enable/disable/status + the NAMED anti-implicit-activation guard (EXECUTED mutation-RED over real launchd state); placeholder-only templates, OAuth token never in the plist.
- **T4** — store-concurrency `fcntl.flock` advisory lock + crash-semantics debounce invariant (store-adversarial four-category battery, cat-(d) flock-removal mutation-RED).

EXTEND-NOT-REBUILD held: the ADR-0032 frozen spine + `scripts/serve/plan_loop.py` byte-frozen (numstat=0) across all 9 commits. 0 live spend, 0 real PII; the LIVE activation is operator-gated (disabled by default).

## Pipeline / review lineage
`/create-task-plan` (4 recipes, 3 executed reviewers → 3 blockers fixed pre-build → judge GO ≥9) → `/execute-plan` Wave-1 + terminal Wave-2 checkpoints RAN green → **Tier-2** wave review (executed) caught + fixed the crontab-hang, the kill-switch edge, the unbounded-wait → the REAL **Tier-3 `/review-pr`** (6 agents, blind triage, executed blind verification + reversion probes) found + fixed SEC-01 / TEST-001 / QUAL-001, verdict CLEAN → merged.

## PF + carry-forward
- **PF-S111-01** — a real-state hardening test I directed mutated the global user crontab → TCC-hangs the mandatory `pytest -q` gate headless + leaked an un-cleanable armed entry; caught by the executed Tier-2 QA review, fixed by moving to the reversible launchd-file real-state path (`0da61f84`). Lesson: real-state OS-mutating tests must use the reversible/cleanable mechanism + subprocess timeouts + capability-gate + teardown.
- **Operator action:** remove the leaked `com.aplusmaxing.cadence-runner.test-de4cc3ce…` crontab entry interactively (harmless — SEC-04-refuses on fire, 0 spend).
- Operational: repeated heavy-parallel-foreground-agent connection deaths → switched all heavy dispatches to `run_in_background: true` + resumed terminated agents via SendMessage.

Full detail: `memory/process-failures.md#session-111` + HANDOFF `## Scope Contract — Session 111`.