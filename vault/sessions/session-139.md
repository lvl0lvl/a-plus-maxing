---
title: Session 139
type: session
created: 2026-07-15
permalink: a-plus-maxing/sessions/session-139
---

# Session 139 (2026-07-15) — Credential-onboarding build Wave 1 (security foundation)

## Goal
Build **Wave 1** of the credential-onboarding code build via `/run-pipeline` — the security foundation — driving continuously without stopping at boundaries. Operator: "close S138, open S139, /run-pipeline" + repeated "continue".

## What landed (both merged to `main`, Wave-1→2 checkpoint GREEN)
- **ADR-0047-T1** (#352 → `dffb89e5`) — cross-platform `keyring` OS-native secret-store abstraction + an encrypted-file/env fallback tier. Public trio `get_secret`/`set_secret`/`delete_secret` over an injected keyring-backend seam. Tier-3 full-6 `/review-pr` found + fixed the **fallback-tier robustness cluster** (unguarded `_fallback_clear` → stale-serve/resurrection; non-atomic `_write_fallback_file` → sibling-loss, fixed by mirroring `store._write_atomic`; non-dict-file crash) — all guards **revert-RED proven** load-bearing. 33 tests.
- **ADR-0048-T1** (#353 → `525ae5dc`) — out-of-band alpha-config loader + the **D5 shared-key provisioning bridge**. Loader reads shared vendor creds + shared Anthropic key from an env-var-pointed OUT-OF-BAND path (in-repo rejected **case-folded** via `str.casefold()` — the macOS/APFS bypass closed); the bridge exports the shared key onto the env-first key path ONLY when no BYO key resolves (**0 clobber**), stdlib-only, no model call. Created + tested in isolation; the server-start wiring is **ADR-0049-T1's**. 23 tests.

## Pipeline (per task)
`/create-task-plan` (SE author → QA/Architect/Security 3-lens → judge ACCEPT 10/10) → `adversarial-review` → `/execute-plan` (TDD) → Tier-2 wave review (QA/Security/Architect + plan-integrity) → Tier-3 full-6 `/review-pr` (blind triage + blind verify) → `/merge`. Every tier earned its keep by EXECUTION.

## Key decisions / findings
- ADR-0048-T1 recipe authored **orchestrator-direct** (the SE-author subagent stalled the stream watchdog twice on the ~50KB synthesis — PF-S139-01); independence preserved by the separate Phase-4 review + Phase-7 judge + adversarial pass, which found 15 + 5 real executed findings.
- The `adversarial-review` caught 2 **false tool-behavior claims** in my own remediation (the `os.path.normcase` POSIX no-op → `str.casefold()`; a `client_secret` `{32,}` scan matching 2170 files → a labeled-context scan) — both re-verified by execution. This is the adversarial layer earning its keep on an orchestrator-authored recipe.
- AR-003 "total fail-loud" hardened iteratively across the gates: value-type validation (Tier-2), then RecursionError + vendor-entry validation (Tier-3).

## Frozen-six / safety
The ADR-0032 six byte-frozen (numstat=0 vs the durable `3ab1c3ab`) across both merges + on main; `$0` mock (injected seams + `monkeypatch`-scoped env; `anthropic` SDK absent); no secret in the tree (synthetic fixtures, out-of-band configs on `tmp_path`; value-shape scan 0 hits). Full suite `2883 passed / 2 pre-existing env-floor / 8 skipped`.

## Next
- **Wave 2** (the credential-consumer refactor, `$0` mock): ADR-0047-T2 (refactor `key_source`+`auth_isolation` onto the secret_store abstraction) + ADR-0047-T3 (refactor `oauth_pull`). Resume via `/run-pipeline` at P3 Wave 2.
- Beads: `a-plus-maxing-e0wp` (HIST01 — ADR-0049-T1 wiring must preserve BYO-wins ordering), `a-plus-maxing-fgmx` (PF-S139-01), the recipe scope-check anchor follow-up.
- Operator-gated (teed up): `a-plus-maxing-m8ia` (LIVE OAuth + metered run), `kn29` (LIVE comprehensive-plan run), the daily-monitor co-arming.