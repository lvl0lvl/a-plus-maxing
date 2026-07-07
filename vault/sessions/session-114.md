---
title: Session 114 — aque OAuth-token secret scan (merged) + a 3-finding /review-pr
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-114
---

# Session 114 — block CLAUDE_CODE_OAUTH_TOKEN at commit (aque + 8s7i, merged)

Passed THROUGH the S113 close (never-stop-mid-loop) into the next high-value hardening item — the SEC-02 secret-scan gap the ADR-0039 review raised. Built + merged (PR #304, `fa13c692`): a leaked `CLAUDE_CODE_OAUTH_TOKEN` in a tracked file is now BLOCKED at commit + pre-push by the existing PII hooks.

## What was built
- **The secret pattern** (`ca2669ac`): `pii_scan.py` was an operator-PII scanner (name/contact/health-line/email/phone/postal) with NO secret/credential detection — so a `sk-ant-oat…`-shaped OAuth token passed `block-pii-commit.sh` + `pre-push-pii-scan.sh` clean (only the ADR-0039-T2 pytest tree-scan caught it, a backstop over already-tracked files that misses new-file/`--no-verify`/human-terminal commits). Added an operator-agnostic `SECRET_PATTERNS` set applied in `scan()` **unconditionally** (regardless of `include_structural`/`token_config`) so `scan_scoped` (the single policy both hooks run) blocks it trunk-wide — including on a `tests/` fixture path (where the structural net is off, a token is still a leak). High-signal by construction (the prefix isn't in legit content), so no clonability cost — the secrets-only scan over the real 2733-file tree returns 0. 3 tests; the token fragment-assembled at runtime so the tracked test file carries no matchable literal (PF-S112-01 discipline; 0 self-trips).
- **The coupled doc-fix** (`8s7i`): append-only `[AMENDED]` notes correcting the previously-ASPIRATIONAL "OAuth token denied at commit by block-pii-commit/pre-push-pii-scan" assurance in ADR-0039 Negative-5 + its ADR-0005 row + the ADR-0005 ADR-0039 row + an ADR-0039 revision row — now mechanically true for the token (the plist stays off-tree via `.gitignore`, a distinct mechanism).

## The /review-pr — 3 findings, all fixed or beaded
The REAL Tier-3 `Skill(review-pr, 304)` ran IN FULL (roster full-6). 6 agents, each EXECUTING its load-bearing claim:
- **Security** ran regex/ReDoS (<0.15ms on 200k pathological input — no cap needed), gap-closure (`scan_scoped` blocks the token in a fixture path), the mutation-RED, and a whole-tree clonability grep (0 matchable literals). It raised **SEC-01**: the sibling `sk-ant-api…` no-train API key is uncovered → ADR-0027's identically-worded assurance stays aspirational (a live-metered-spend credential leak in a PUBLIC repo). Blind-triaged **DEFERRED** (out of the OAuth scope) → beaded **P1**, per Security's own "do NOT expand this PR."
- **Contracts** raised **API-01**: I updated the module docstring for the new unconditional-secret behavior but left the `scan()`/`scan_scoped()` function docstrings stale (the `include_structural=False` param doc falsely still said "only config-driven tokens run there"). Confirmed empirically-false. LEGITIMATE → fixed.
- **Test Coverage** raised **TEST-01**: my anti-overbroad test omitted the file's own documented F-TEST1 liveness assert, so it would go vacuously green under a pattern-disabling regression. LEGITIMATE → fixed; the fix proven load-bearing by the reversion probe (RED at line 693 under `_COMPILED_SECRET=[]`).
- **Bug Hunter, Code Quality, Historical Context** — 0 findings, each executed (monkeypatch mutation, self-trip grep, secrets-only tree scan, the 3lv/dv3 evolution consistency).

Phase-3 blind triage + Phase-7 blind verification (both executed, profile-less) confirmed the classifications + the fixes RESOLVED. Phase-8 verdict CLEAN (SHA-bound `bf81df79`).

## Pipeline note
A clean demonstration of the layered review catching real quality issues in my OWN build: two of the three findings (API-01 stale docs, TEST-01 vacuous-under-regression test) were defects I introduced, caught by the agents whose lens owns them (Contracts, Test Coverage) and fixed + independently blind-verified. The third (SEC-01) was a genuine sibling-gap the OAuth-scoped PR correctly deferred + beaded rather than scope-crept. Frozen ADR-0032 spine byte-frozen throughout; crown-jewel net-HARDENED; 0 live spend.

Full detail: `memory/process-failures.md#session-114` + HANDOFF `## Scope Contract — Session 114`.
