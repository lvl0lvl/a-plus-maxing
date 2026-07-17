---
scope: "ADR-0047 ADR-0048 ADR-0049 (Tier-1 secret storage + Tier-2 credential onboarding + Tier-1 cost governance)"
adrs: [ADR-0047, ADR-0048, ADR-0049]
tier: 2
created: 2026-07-14
status: approved
---

# Spec: Alpha-Tester Credential Onboarding — Cross-Platform Secret Storage, App-Mediated OAuth, and Shared-Key Cost Governance

## Component Overview

This spec implements the three-ADR credential-onboarding cluster that lets an alpha tester connect a wearable and reach the model **in-app, on Mac or Windows, without a shell**. It delivers three coupled subsystems: (1) a cross-platform `keyring`-backed secret-store abstraction with an encrypted-file/env fallback tier (ADR-0047, Tier-1 foundation); (2) app-mediated OAuth onboarding — a localhost PKCE callback, N-per-source credential writes, the extended intake credential step and the My Info "Connections & Keys" panel, and out-of-band shared-credential distribution (ADR-0048, Tier-2); and (3) cost governance for the shared metered specialist lane the shared-key model creates — a bounded metered dispatch factory, a manual-default plan-update trigger with an Off/Weekly/Daily schedule setting, and a per-tester monthly spend cap (ADR-0049, Tier-1 sibling).

The dependency is forced by ADR-0047: it is the storage foundation both other arms sit on (`depends-on ADR-0047`). ADR-0047 is a **backend swap behind existing injectable seams** — the three credential modules (`key_source.py`, `auth_isolation.py`, `oauth_pull.py`) already expose injection points, so the refactor routes their default credential I/O through the abstraction while the ADR-0032 `<always-frozen>` six (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py`) stay byte-frozen. ADR-0048 brings the OAuth authorize + per-tester token write in-app (leaving only the shared app credentials out-of-band, D4 — operator-signed-off 2026-07-14) and RULES the authorization flow a non-egress class (D7, validated by a wire-scan). ADR-0049 routes the specialist/judge/lens dispatch onto the shared metered API — a bounded factory built into the injected `run_orchestrated`→`plan_driver.drive` seam, DOWNSTREAM of the `deid_in` de-id boundary — and RULES the routing a crown-jewel egress no-op (D2, validated by a lane-sensitive outbound-capturing mutation-gated wire-scan).

This spec consumes the accepted ADR-0047/0048/0049 records and produces the task breakdown, dependency map, and file manifest for the credential-onboarding build. It is a **mock/fixture build at $0**: fixture OAuth, fixture model clients, mocked per-OS keyring backends. The operator-present LIVE run (real shared key, real data, real spend, dev-app registration for the exact per-vendor client types) is operator-gated (bead `a-plus-maxing-m8ia`) and is **out of this spec's build scope**. The upstream design source for the two onboarding UI surfaces is the operator-signed-off `prototype/credential-onboarding-mockup.html` (Surface A — the intake credential step; Surface B — the My Info "Connections & Keys" + "Plan updates" sections).

**Informing artifacts:** `docs/spec/.pipeline/context.md` (Phase-2 ADR extraction + light grounding), `docs/spec/.pipeline/dispositions.md` (Phase-3 dispositions), `prototype/credential-onboarding-mockup.html` (both UI surfaces), `docs/checklists/store-adversarial-tests.md` (the store-surface gate — see the "Store-surface" note below; no task in this spec triggers it).

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0047 OQ-1 | Open Question | Per-OS `keyring` backend mapping + login-session unlock on read AND prompt/block on write (incl. unattended rotating-vendor write-back). | Proceed | VERIFY-AT-BUILD in ADR-0047-T1/T2/T3: per-OS mocked round-trip + an unattended write→read per backend; a prompting/blocking backend routes to the fallback tier for that OS. $0 fixture test. |
| ADR-0047 OQ-2 | Open Question | Threat-model the fallback tier (encrypted-file key location + env-var extractability). | Proceed | VERIFY-AT-BUILD in ADR-0047-T1: threat model documented in the module docstring; fallback engages iff keyring unavailable; encrypted-file location gitignored (AC-5). |
| ADR-0047 OQ-3 | Open Question | Abstraction module path + interface; reconcile the 3 non-uniform seams without renaming `credential_*` (Risk-N3). | Proceed | Pinned in this spec: `scripts/secret_store/` (`get_secret`/`set_secret`/`delete_secret`); consumers keep their seam parameter names (ADR-0047-T2/T3). |
| ADR-0047 OQ-4 | Open Question | Fallback encrypted-file at-rest location gitignored + hook-covered (ADR-0005). | Proceed | VERIFY-AT-BUILD in ADR-0047-T1 (AC-5): the location is gitignored (`git check-ignore` exits 0); `block-pii-commit`/`pre-push-pii-scan` cover the tree. |
| ADR-0048 OQ-1 | Open Question | Callback listener lifecycle — one-shot ephemeral socket vs a long-lived `GET /oauth/callback` route. | Proceed | Pinned to the one-shot short-lived 127.0.0.1 listener (ADR-0048-T2); both stay loopback-bound, only lifecycle differs. |
| ADR-0048 OQ-2 | Open Question | Shared alpha Anthropic key vs bring-your-own as the shipped default. | Proceed | Default = shared alpha key (D5, operator-signed-off); bring-your-own is a paste-field option in both UI surfaces (ADR-0048-T4). |
| ADR-0048 OQ-3 | Open Question | Garmin's auth tier — defer from one-click or adopt an OAuth-2.0 PKCE path. | Proceed | Garmin OAuth-1.0a is excluded from the one-click alpha flow; the UI renders its manual/deferred path (ADR-0048-T4 AC-5). No build impact. |
| ADR-0048 OQ-5 | Open Question | Exact per-vendor OAuth client type (confidential vs PKCE vs PAT) → the precise shared-secret vendor set. | Defer | LIVE-run / dev-app-registration prerequisite (bead `a-plus-maxing-m8ia`). The build parameterizes per-vendor client type (ADR-0048-T1 AC-2), defaulting to "≥Whoop confidential-client"; real types verified at registration. |
| ADR-0048 OQ-4 | Open Question | North-Star hosted token-broker cutover timing. | Defer | Post-V1, out of scope; the ADR-0047 seam keeps the shared secret swappable behind it. Tracked so the shared-secret acceptance is explicitly temporary. |
| ADR-0049 OQ-1 | Open Question | Is D5's per-tester cap built in the alpha? | Proceed | RESOLVED → INCLUDE (operator resolution). Built as ADR-0049-T3. |
| ADR-0049 OQ-2 | Open Question | Exact per-plan metered cost (~$1–3/plan Opus is an ESTIMATE, never live-metered). | Defer | Measured only at the operator-gated first LIVE run (bead `a-plus-maxing-m8ia`). The build ships the D4/D5 caps (dispatch-COUNT, never a dollar figure); the LIVE run sizes them. |
| ADR-0049 OQ-3 | Open Question | When bead `glzi` (daily-INTERVAL enable path) lands so the D4 Daily option ships. | Proceed | Build-sequencing dependency, not a design change: the manual trigger + Off/Weekly ship now; Daily renders inert pending `glzi` (ADR-0049-T2 AC-4). |
| ADR-0049 OQ-4 | Open Question | Which server surface hosts the alpha's metered plan generation. | Proceed | RESOLVED → the `run_orchestrated`→`drive` full-composition seam (operator resolution). The D2 wire-scan binds to this surface's post-`deid_in` gate (ADR-0049-T1). |
| Cross-cutting O-6 | Open Question | The operator-present LIVE run (real OAuth + real spend; the D7/D2 wire-scans + the cost figure re-run live). | Defer | Operator-gated (bead `a-plus-maxing-m8ia`). The build + mock-test proceed at $0; the LIVE run is teed up in the HANDOFF, not a build task. |

**No Block dispositions.** Nothing blocks the mock/fixture build (Phase-2/Phase-3 finding). No research-spike (`T0`) task is required. Every Proceed item is resolved by a named task's acceptance criteria; every Defer item is a LIVE-run / post-V1 prerequisite that the mock build parameterizes or tees up.

**Store-surface note (`docs/checklists/store-adversarial-tests.md`):** NO task in this spec reads from or writes to `scripts/store/`. The credential + model-access tasks touch `scripts/secret_store/`, `scripts/model/`, `scripts/runner/`, `scripts/ingest/`, `scripts/serve/`, and the UI templates only; the D5 spend ledger (ADR-0049-T3) persists to a gitignored instance-local path, never `scripts/store/`; the D2 wire-scan asserts the metered adapter performs 0 store reads. The store-adversarial blocking gate therefore does not trigger.

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/secret_store/__init__.py` | Create | Cross-platform `keyring`-backed secret abstraction (`get_secret`/`set_secret`/`delete_secret`) + encrypted-file/env fallback tier; fallback threat model in docstring |
| `tests/secret_store/test_secret_store.py` | Create | Per-backend (mocked per-OS) round-trip, unattended write→read, fallback-iff-unavailable, fallback threat properties |
| `requirements.txt` | Modify | Add `keyring` — the first third-party runtime dependency on the secret path (ADR-0047) |
| `.gitignore` | Modify | Gitignore the fallback encrypted-file at-rest location (ADR-0047-T1) AND the spend-ledger at-rest location (ADR-0049-T3) — two distinct append-only lines, added in different waves |
| `scripts/model/key_source.py` | Modify | Route `resolve()`/`store()` defaults through `scripts.secret_store`; preserve `keychain_runner`/`keychain_writer` seam names; drop the direct `security` shell-out |
| `scripts/runner/auth_isolation.py` | Modify | Route `build_subscription_env()` default read through `scripts.secret_store`; preserve `keychain_reader` seam name |
| `tests/model/test_key_source.py` | Modify | Abstraction round-trip + 0-direct-shell-out scan for `key_source` |
| `tests/runner/test_auth_isolation.py` | Modify | Abstraction read + 0-direct-shell-out scan for `auth_isolation` |
| `scripts/ingest/oauth_pull.py` | Modify | Route `_read/_write_oauth_credential` through `scripts.secret_store`; PRESERVE `credential_reader`/`credential_writer` seam names (Risk-N3); keep unattended rotating-vendor write-back |
| `tests/ingest/test_oauth_pull.py` | Modify | Abstraction round-trip + 0-direct-shell-out scan + unattended write-back for `oauth_pull` |
| `scripts/serve/alpha_config.py` | Create | Out-of-band alpha-build config loader — shared vendor `client_id`/`client_secret` (per confidential-client vendor) + optional shared Anthropic key from an env-var-pointed path outside the repo; + the D5 shared-key provisioning bridge (exports the shared key as in-process `ANTHROPIC_API_KEY` at server start when no BYO key resolves) |
| `tests/serve/test_alpha_config.py` | Create | Out-of-band load, per-vendor client-type parameterization, tracked-file secret scan == 0, in-repo-path rejection, shared-key bridge (resolve-returns-shared / mutate-out-REDs / BYO-precedence) |
| `scripts/serve/server.py` | Modify | (T3-0048) extend the `_save_key`/`_key_status` write class to N per-source tokens + a per-source write/status handler; (T2-0048) the connect-start route that spins up the one-shot OAuth listener; (T1-0049) inject `metered_dispatch` as the server `loop_dispatch` + invoke the ADR-0048-T1 shared-key bridge at server start; (T2-0049) the manual "Update my plan now" trigger wiring — four distinct sections (see Shared-file coordination) |
| `tests/serve/test_credential_writes.py` | Create | N-per-source token write→read through the ADR-0047 store; 0 tracked secrets; loopback + body-ceiling posture |
| `scripts/serve/oauth_callback.py` | Create | One-shot 127.0.0.1 OAuth listener + PKCE code-challenge + `state`/CSRF + code→token exchange; writes via the T3 per-source write class |
| `tests/serve/test_oauth_callback.py` | Create | `state`/PKCE/one-shot/loopback-bind assertions + the D7 crown-jewel wire-scan (0 store bytes, 0 model-lane, vendor-only outbound, mutation-RED) |
| `vault/design/templates/app_view.html` | Modify | **[AMENDED 2026-07-17 S143 — PF-S142-01 retarget]** The credential UI markup + JS: extend the SERVED SPA `screen-wizard` step 9 ("API key") into the "Connect your data & keys" credential step (Surface A) + extend `screen-profile` with the "Connections & Keys" panel (Surface B); the per-source connection status is delivered CLIENT-SIDE via a `fetch('/settings/trackers')` (the already-routed keychain-derived endpoint, mirroring the `/settings/key` pill) — no server render-state seam. (The prior manifest named `intake.py` — an UNSERVED CLI-only 6-step artifact; `server.py` serves only `generate.run('app')`, whose intake IS this SPA `screen-wizard`, already a 9-step flow with step 9 = "API key".) |
| ~~`vault/design/templates/app_shell.py` (T4)~~ | — | **[AMENDED S143 — REMOVED from T4]** T4 no longer touches `app_shell.py`: Surface B's connection status is client-side (`fetch('/settings/trackers')`), not a server render-state seam (the prior `connections=` inject was a dead extension point — `_tracker_status` is a JSON HTTP handler, not a render source; QA-M1/Arch-F1). `app_shell.py` remains ADR-0049-T2's (the "Plan updates" section render-state) — a Wave-6 concern, not T4's. |
| `tests/serve/test_credential_onboarding_ui.py` | Create | Both UI surfaces render faithful to the mockup, skippable/resumable, no client-secret field, Garmin manual path, inline-only assets |
| `scripts/runner/metered_dispatch.py` | Create | Bounded metered `dispatch(name,prompt,context)→envelope` factory over the shared `a-plus-maxing-api-key` lane (mirrors `subscription_dispatch`); T3-0049 adds the spend-cap consult |
| `tests/runner/test_metered_dispatch.py` | Create | The D2 crown-jewel wire-scan (placement / outbound-capture / lane-swap / mutation-gate) + frozen-six numstat probe |
| `tests/serve/test_loop_dispatch_wiring.py` | Modify | Reflect the metered `loop_dispatch` production injection (ADR-0049-T1) |
| `tests/serve/test_plan_update_trigger.py` | Create | Manual trigger fires exactly one re-gen; schedule setting persists; Daily inert (glzi-gated) |
| `scripts/runner/spend_cap.py` | Create | Cumulative monthly per-tester spend ledger (gitignored instance-local path) + fail-closed refusal past the cap |
| `tests/runner/test_spend_cap.py` | Create | Cap enforcement (≥1 past cap REDs), monthly rollover, per-tester isolation, D2-scan stays green after wiring |

**Shared-file coordination:**
- `scripts/serve/server.py` is Modified by four tasks (ADR-0048-T3, ADR-0048-T2, ADR-0049-T1, ADR-0049-T2), each in a **distinct section** (per-source write handlers / connect-start route / `main()`+`build_server` `loop_dispatch` injection + shared-key bridge call / manual-trigger route). ADR-0048-T3→ADR-0048-T2 and ADR-0049-T1→ADR-0049-T2 are dependency-ordered; the ADR-0048 arm (write handlers/route) and the ADR-0049 arm (loop-dispatch injection/trigger) touch non-overlapping regions. The build planner serializes same-file tasks within a wave.
- `.gitignore` is Modified by ADR-0047-T1 (fallback file, wave 1) and ADR-0049-T3 (spend ledger, wave 4) — distinct append-only lines, different waves, no concurrency.
- **[AMENDED S143 — PF-S142-01]** `vault/design/templates/app_view.html` is Modified by ADR-0048-T4 (the credential step 9 + Connections & Keys panel markup + the client-side `/settings/trackers` status JS). `vault/design/templates/app_shell.py` is Modified ONLY by ADR-0049-T2 (the Plan-updates section render-state) — ADR-0048-T4 no longer touches `app_shell.py` (Surface B's status is client-side, not a server render-state seam). ADR-0049-T2 depends on ADR-0048-T4, so ordered.
- `scripts/runner/metered_dispatch.py` is Created by ADR-0049-T1 and Modified by ADR-0049-T3 (the cap consult) — ADR-0049-T3 depends on ADR-0049-T1 (create-then-modify, ordered).

## Tasks

### ADR-0047-T1: Cross-platform secret-store abstraction + fallback tier
**Status:** TODO
**ADR Source:** ADR-0047, Decision (OS-native `keyring` abstraction + encrypted-file/env fallback tier); ADR-0047, Validation Approach (per-backend round-trip, unattended write→read, fallback-iff-unavailable); ADR-0047, Consequences-Negative (first third-party dep, fallback weaker-at-rest, per-OS matrix, OQ-2/OQ-4)
**Files to create/modify:**
- `scripts/secret_store/__init__.py` -- the abstraction: `get_secret(service)` / `set_secret(service, value)` / `delete_secret(service)` over `keyring` primary + an encrypted-file/env fallback tier; fallback threat model in the module docstring
- `tests/secret_store/test_secret_store.py` -- per-backend (mocked per-OS) round-trip, unattended write→read, fallback engagement, fallback threat properties
- `requirements.txt` -- add `keyring`
- `.gitignore` -- gitignore the fallback encrypted-file at-rest location

**Acceptance Criteria:**
1. `scripts.secret_store` exposes `get_secret`/`set_secret`/`delete_secret`; a `set_secret(s, v)` then `get_secret(s)` recovers `v` byte-for-byte through the keyring backend, exercised with a mocked backend per OS (macOS Keychain, Windows Credential Manager, Linux Secret Service) — ≥1 round-trip per mocked backend.
2. An unattended (no-interactive-session fixture) `set_secret`→`get_secret` round-trip completes with 0 prompts/blocks per mocked backend; a fixture backend that raises/prompts on `set_secret` routes that service to the fallback tier (the ADR-0047×ADR-0039 rotating-vendor write-back seam).
3. The fallback tier engages iff keyring is unavailable: with `keyring` importable, `get_secret` performs 0 fallback reads; with `keyring` import forced to fail, the fallback serves the value and the consumer still resolves it.
4. `keyring` is listed in `requirements.txt`; `python -c "import keyring"` exits 0 after `.venv/bin/python -m pip install -r requirements.txt` on a clean venv.
5. `git check-ignore <fallback-encrypted-file-path>` exits 0 (the fallback secret can never be committed), and the module docstring documents the fallback threat model — where the encrypted-file key lives and the env-var extractability (OQ-2).
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (frozen-six byte-frozen — the guard is asserted at the FIRST build of the abstraction, per ADR-0047 Falsification "run all four at the first build of the abstraction").
7. `pytest tests/secret_store/ -q` passes and `.venv/bin/python -m pytest -q` stays green (0 regressions).

**Risk Mitigations:** ADR-0047 Consequence-Negative "keyring first third-party dep" (AC-4); "fallback weaker-at-rest / OQ-2" (AC-2, AC-5); "per-OS test matrix" (AC-1, AC-2); "fallback file gitignored / OQ-4 / ADR-0005" (AC-5); "frozen six untouched at first build" (AC-6)
**Dependencies:** None (entry point)

---

### ADR-0047-T2: Refactor key_source + auth_isolation onto the abstraction
**Status:** TODO
**ADR Source:** ADR-0047, Decision (refactor consumers behind existing seams, no direct `security` shell-out); ADR-0047, Validation Approach (0 shell-outs in consumers, frozen-six numstat=0, seam-injected tests stay green)
**Files to create/modify:**
- `scripts/model/key_source.py` -- route `resolve()`/`store()` defaults through `scripts.secret_store` (service `a-plus-maxing-api-key`); keep `keychain_runner`/`keychain_writer` seam names
- `scripts/runner/auth_isolation.py` -- route `build_subscription_env()` default read through `scripts.secret_store` (service `a-plus-maxing-oauth-token`); keep `keychain_reader` seam name
- `tests/model/test_key_source.py` -- abstraction round-trip + 0-shell-out scan
- `tests/runner/test_auth_isolation.py` -- abstraction read + 0-shell-out scan

**Acceptance Criteria:**
1. `key_source.resolve(keychain_runner=...)` and `key_source.store(key, *, keychain_writer=...)` route their DEFAULT credential I/O through `scripts.secret_store` for service `a-plus-maxing-api-key`; the `keychain_runner`/`keychain_writer` parameter names are unchanged so injected tests keep their mock points.
2. `auth_isolation.build_subscription_env(base_env, *, keychain_reader=...)` routes its DEFAULT read through `scripts.secret_store` for service `a-plus-maxing-oauth-token`; the `keychain_reader` parameter name is unchanged.
3. `grep -rnE "security (find|add)-generic-password" scripts/model/key_source.py scripts/runner/auth_isolation.py` returns 0 hits (no direct macOS shell-out survives in either consumer).
4. A `store`→`resolve` round-trip on `key_source` recovers the key byte-for-byte through the mocked abstraction; a `build_subscription_env` read returns the token from the mocked abstraction.
5. Env-first precedence is PRESERVED across the refactor: with `ANTHROPIC_API_KEY` set, `key_source.resolve` returns the env value WITHOUT any `scripts.secret_store` read for the `a-plus-maxing-api-key` service (the env check stays ahead of the keyring backend — the pre-refactor order at `key_source.py:80-86`). Asserted by a test that REDs if `resolve` reads the abstraction while the env var is set; the existing env-precedence tests are NOT weakened to a keyring-primary order to match the refactor.
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (frozen-six byte-frozen).
7. `pytest tests/model/test_key_source.py tests/runner/test_auth_isolation.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0047 Consequence-Negative "non-uniform seams reconciled without breaking mock points" (AC-1, AC-2); "env-first precedence preserved — BYO-via-env resolves ahead of the keyring backend, and the ADR-0048-T1 shared-key bridge rides this same env-first path" (AC-5); "frozen six untouched" (AC-6)
**Dependencies:** ADR-0047-T1

---

### ADR-0047-T3: Refactor oauth_pull onto the abstraction (Risk-N3 preserve credential_*)
**Status:** TODO
**ADR Source:** ADR-0047, Decision (preserve `credential_*` seams so the Risk-N3 scan stays green); ADR-0047, Validation Approach (0 shell-outs, unattended write→read per backend, `_key_def_count()==0`)
**Files to create/modify:**
- `scripts/ingest/oauth_pull.py` -- route `_read_oauth_credential`/`_write_oauth_credential` through `scripts.secret_store` (service `a-plus-maxing-<source>-oauth`); PRESERVE `credential_reader`/`credential_writer` seam names; keep the unattended rotating-vendor write-back
- `tests/ingest/test_oauth_pull.py` -- abstraction round-trip + 0-shell-out scan + unattended write-back

**Acceptance Criteria:**
1. `oauth_pull.access_token(...)` and `oauth_pull.fetch(...)` route their DEFAULT `credential_reader`/`credential_writer` (the `_read/_write_oauth_credential` defaults) through `scripts.secret_store`; the `credential_reader`/`credential_writer` seam names are UNCHANGED (Risk-N3).
2. `tests/ingest/test_ingest.py::test_dedupe_uses_shared_keying` Half-(a) `_key_def_count()==0` stays green — the refactor introduces no `def .*key` definition under `scripts/ingest/`.
3. `grep -rnE "security (find|add)-generic-password" scripts/ingest/oauth_pull.py` returns 0 hits.
4. An unattended `credential_writer`→`credential_reader` round-trip (a rotated refresh-token write-back for a rotating vendor, e.g. Whoop/Google) recovers the payload with 0 prompts through the mocked abstraction.
5. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing.
6. `pytest tests/ingest/test_oauth_pull.py tests/ingest/test_ingest.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0047 Consequence-Negative "Risk-N3 preserve credential_*" (AC-1, AC-2); "unattended rotating-vendor write-back / OQ-1" (AC-4); "frozen six untouched" (AC-5)
**Dependencies:** ADR-0047-T1

---

### ADR-0048-T1: Out-of-band alpha-build config loader
**Status:** TODO
**ADR Source:** ADR-0048, Decision D4 (shared-alpha-credential distribution via out-of-band config, never a tracked file); ADR-0048, Decision D5 (shared alpha Anthropic key default — testers "touch nothing"; the provisioning bridge realizes that default onto the runtime key source `key_source.resolve` reads); ADR-0048, Validation Approach (tracked-file secret scan == 0); ADR-0048, Consequences-Negative (D4/D5 extractable-and-global-revoke shared secrets)
**Files to create/modify:**
- `scripts/serve/alpha_config.py` -- loads shared vendor `client_id`/`client_secret` (per confidential-client vendor) + the optional shared Anthropic key from an env-var-pointed path OUTSIDE the repo tree; per-vendor client-type parameterized; + the D5 shared-key provisioning bridge (exports the shared Anthropic key as in-process `ANTHROPIC_API_KEY` at server start when no bring-your-own key resolves)
- `tests/serve/test_alpha_config.py` -- out-of-band load, per-vendor client-type parameterization, tracked-secret scan, in-repo-path rejection, shared-key bridge (resolve-returns-shared / mutate-out-REDs / BYO-precedence)

**Acceptance Criteria:**
1. `alpha_config` loads the shared vendor credentials + optional shared Anthropic key from an out-of-band path named by an environment variable; with the variable unset it returns an empty config (no exception), and connect falls back to per-vendor manual/skip.
2. The loader parameterizes each vendor's client type — confidential (shared secret) / PKCE-public (no secret) / PAT (tester's own token) — defaulting to the grounded "≥Whoop confidential-client" set, with Garmin flagged excluded-from-one-click (OAuth 1.0a); the per-vendor set is data-driven (resolvable at OQ-5 dev-app registration without a code change).
3. A content scan of all tracked files (`git ls-files` → secret-pattern grep for `client_secret`-shaped and `sk-ant-`-shaped values) returns 0 hits.
4. `alpha_config` rejects a config path that resolves inside the repo working tree (an in-repo config path raises) — the config can only be out-of-band.
5. **Shared-key provisioning bridge (D5 default path):** at server start `alpha_config` provisions its loaded shared Anthropic key onto the source `key_source.resolve` reads — it attempts `key_source.resolve` and, ONLY if that raises `KeyUnavailableError` (no bring-your-own key in env or keychain), exports the shared key in-process as `ANTHROPIC_API_KEY` (the env-first branch at `key_source.py:80-82` then resolves it with no keychain write). A bring-your-own key set in env or written to the keychain therefore takes precedence and the bridge no-ops (D5's shared key is the "touch nothing" DEFAULT, not an override; consistent with the env-first order ADR-0047-T2 AC-5 preserves). RED-capable: with `alpha_config` carrying a shared key and NO BYO key set (env unset, mocked keychain empty), the bridge runs and `key_source.resolve` returns the shared key (not `KeyUnavailableError`); with the bridge mutated out, `key_source.resolve` raises `KeyUnavailableError` (RED); with a BYO key present the bridge exports nothing and `resolve` returns the BYO key.
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (the loader + bridge land in `scripts/serve/alpha_config.py`, outside the frozen six).
7. `pytest tests/serve/test_alpha_config.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0048 Consequence-Negative "D4 shared confidential-client secret extractable/global-revoke — out-of-band discipline" (AC-1, AC-3, AC-4); "D5 shared Anthropic key out-of-band" (AC-1, AC-3); "D5 shared-key default reaches the model lane — provisioning bridge, no BYO clobber" (AC-5); "frozen six untouched" (AC-6)
**Dependencies:** None (entry point)

---

### ADR-0048-T3: App-mediated N-per-source credential writes
**Status:** TODO
**ADR Source:** ADR-0048, Decision D3 (extend the ADR-0013 single-key keychain-write class to N per-source OAuth tokens, written through the ADR-0047 store); ADR-0048, Consequences-Negative (D3 expanded credential-write surface)
**Files to create/modify:**
- `scripts/serve/server.py` -- extend the `_save_key`/`_key_status` write class to N per-source tokens; add a per-source token write/status handler (writes through `scripts.secret_store`)
- `tests/serve/test_credential_writes.py` -- per-source write→read round-trip, loopback + body-ceiling posture, 0 tracked secrets

**Acceptance Criteria:**
1. A new POST handler writes a per-source credential (`source` + token) through `scripts.secret_store` (service `a-plus-maxing-<source>-oauth`); a subsequent status read reports that source connected; the existing single-key `/settings/key` write (service `a-plus-maxing-api-key`) is preserved unchanged.
2. The per-source write handler binds 127.0.0.1 only (inherits the ADR-0013 loopback posture) and rejects a request whose body exceeds the ADR-0013 16-KiB ceiling.
3. A per-source token round-trips: written via the route, then recovered by `oauth_pull`'s `credential_reader` (both on the ADR-0047 store).
4. A tracked-file content scan after a simulated per-source write returns 0 token/secret hits (the token lands only in the store).
5. The per-source token-write handler carries the same `application/json` CSRF gate as `_save_key` (the SEC-001 gate at `server.py:939-944`): a cross-site CORS-simple `text/plain` POST is refused 415 BEFORE any keychain write, mutation-proven by a test that REDs if the gate is dropped (the write proceeds on a `text/plain` body).
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing.
7. `pytest tests/serve/test_credential_writes.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0048 Consequence-Negative "D3 expands the credential-write trust boundary — N secrets off the tracked tree" (AC-1, AC-4); ADR-0013 CSRF posture "SEC-001 application/json gate on the new per-source secret-write route" (AC-5)
**Dependencies:** ADR-0047-T2, ADR-0047-T3

---

### ADR-0048-T2: App-mediated OAuth authorization-code flow + localhost PKCE callback
**Status:** TODO
**ADR Source:** ADR-0048, Decision D1 (localhost-only callback, PKCE, `state`/CSRF, one-shot listener); ADR-0048, Decision D7 (the ADR-0001 egress ruling) + Validation Approach (the D7 crown-jewel wire-scan, loopback-bind check)
**Files to create/modify:**
- `scripts/serve/oauth_callback.py` -- the one-shot 127.0.0.1 listener + PKCE code-challenge + `state`/CSRF + code→token exchange; on success writes via the ADR-0048-T3 per-source write class
- `scripts/serve/server.py` -- a connect-start route that spins up the one-shot listener and opens the vendor authorize URL
- `tests/serve/test_oauth_callback.py` -- `state`/PKCE/one-shot/loopback assertions + the D7 wire-scan

**Acceptance Criteria:**
1. The authorization request carries a `state`/CSRF parameter and a PKCE code-challenge; on a matching callback the flow exchanges the code for a token and writes it via the ADR-0048-T3 per-source write class (through the ADR-0047 store). PKCE's protection is on the EXCHANGE, not the authorize leg: the token-exchange request carries the `code_verifier` corresponding to the issued code-challenge, and a fixture vendor token endpoint that receives a missing or mismatched `code_verifier` rejects the exchange → 0 token writes.
2. The callback listener binds 127.0.0.1 only — an assertion that the bind address is never `0.0.0.0`/`""` (0 non-loopback binds).
3. The callback REJECTS a mismatched `state`: a callback whose `state` differs from the issued value produces 0 token writes.
4. The code→token exchange client DECLINES cross-host redirects: it host-locks the token endpoint and refuses to follow any 3xx, mirroring `oauth_pull.py`'s `_NoFollowRedirect` fail-closed opener (`oauth_pull.py:245-283` — the default opener copies `Authorization`/secret headers onto a redirect target with no cross-host stripping, so following a 3xx would leak the auth code + `client_secret` to the redirect host). A fixture token endpoint returning a 3xx-to-another-host aborts the exchange with 0 credential bytes reaching the redirect target and 0 token writes.
5. The listener is one-shot: after accepting exactly one callback it tears down (a second request to the ephemeral port is refused / the socket is closed).
6. **D7 crown-jewel wire-scan (load-bearing):** driving the authorization + callback + token-exchange path under a recording network seam asserts (a) 0 bytes of store content in any outbound request body/header, (b) 0 calls to the no-train model lane, (c) the only outbound host is the vendor's own authorize/token endpoint. The scan asserts the CLEAN direction truthy first, then RED-gates EACH asserted family with the "the test is invalid — and fails — if that mutation does not RED it" self-invalidation clause per family (mirroring the ADR-0049-T1 AC-5 D2 gold standard): a stub that adds a store-content byte to the outbound leg MUST flip the store-content assertion RED; a fixture token endpoint returning a 302-to-attacker-host MUST flip the vendor-only-host assertion RED (asserting 0 credential bytes reach the redirect target and the exchange aborts); a stub that opens a no-train model-lane call on the auth/callback path MUST flip the model-lane assertion RED.
7. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing.
8. `pytest tests/serve/test_oauth_callback.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0048 Consequence-Negative "D1 new inbound trust boundary" (AC-2, AC-3, AC-5); ADR-0048 D1 (amended 2026-07-15) "no cross-host redirect on the code→token exchange" (AC-4); ADR-0001 tension "D7 egress ruling — per-family RED-gated" (AC-6)
**Dependencies:** ADR-0048-T1, ADR-0048-T3

---

### ADR-0048-T4: Onboarding UI — intake credential step + My Info Connections & Keys
**Status:** TODO
**ADR Source:** ADR-0048, Decision D6 (extend the intake credential step + My Info with a "Connections & Keys" panel, wiring the operator-signed-off mockup; skippable + resumable, not a new wizard); ADR-0048, Consequences-Negative (Garmin excluded from one-click)
**Files to create/modify:**
- `vault/design/templates/app_view.html` -- **[AMENDED 2026-07-17 S143 — PF-S142-01]** extend the served SPA `screen-wizard` step 9 ("API key") into the "Connect your data & keys" credential step (Surface A) + extend `screen-profile` with the "Connections & Keys" panel (Surface B); Surface B's per-source status is client-side via `fetch('/settings/trackers')` (mirroring the `/settings/key` pill). (Retargeted from `intake.py`, which is unserved — see the amended File Manifest + Repo-Grounding Ledger. `app_shell.py` is NOT touched by T4 — the connection status is client-side, not a server render-state seam.)
- `tests/serve/test_credential_onboarding_ui.py` -- both surfaces render faithful to the mockup, skippable, secret-free, Garmin manual path, inline-only

**Acceptance Criteria:**
1. **[AMENDED 2026-07-17 S143 — PF-S142-01]** The served SPA `screen-wizard` step 9 (currently "API key", `app_view.html:751`) is EXTENDED into a "Connect your data & keys" step with one-click connect cards (Whoop, Oura, Garmin, Google), an Oura PAT paste fast-path, an Apple Health "Get the Shortcut" affordance, and the D5 model-key choice (shared alpha default / bring-your-own — the existing `sk-ant-` key input becomes the bring-your-own branch) — matching the enumerated elements of `prototype/credential-onboarding-mockup.html` Surface A. (The SPA `screen-wizard` is ALREADY a 9-step flow with step 9 = "API key", so the mockup's "Step 9 of 9" framing is ACCURATE for the served surface — no renumber, no rebuild; the prior "append to the 6-step intake.py stepper" reconciliation was grounded on the unserved `intake.py` and is superseded.)
2. The My Info surface renders a "Connections & Keys" panel (per-source connect/reconnect/disconnect + the PAT update + the shared/own key choice) matching the enumerated elements of Surface B, reachable from the `_PLATFORM_SCREENS` `screen-profile`.
3. The credential step is skippable and resumable: a "Skip for now" / "Finish setup" path renders with 0 connections made — no connection is required to complete onboarding.
4. Neither surface renders a `client_id` or `client_secret` input field (a tester never sees a client secret); the model-key card names the shared alpha key as the default with a keychain-storage note.
5. Garmin's card renders the manual/deferred path (not a one-click OAuth button), consistent with its OAuth-1.0a exclusion.
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (**[AMENDED S143]** the T4 UI edits touch `app_view.html` only, never the frozen six).
7. Both rendered surfaces carry 0 external asset references (the `render.emit` inline-only contract) and `pytest tests/serve/test_credential_onboarding_ui.py -q` passes; the full baseline stays green.

**Risk Mitigations:** ADR-0048 Consequence-Negative "Garmin excluded from one-click" (AC-5); "shared secret never surfaced to the tester" (AC-4); "frozen six untouched" (AC-6)
**Dependencies:** ADR-0048-T2, ADR-0048-T3

---

### ADR-0049-T1: Bounded metered dispatch factory into the injected seam + D2 crown-jewel wire-scan
**Status:** TODO
**ADR Source:** ADR-0049, Decision D1 (build a bounded metered dispatch factory into the injected `run_orchestrated`→`plan_driver.drive` seam, outside the frozen six; subscription adapter retained); ADR-0049, Decision D2 + Validation Approach (the lane-sensitive outbound-capturing mutation-gated egress wire-scan); ADR-0049, Consequences-Negative (subscription-lane-bypass)
**Files to create/modify:**
- `scripts/runner/metered_dispatch.py` -- the metered `dispatch(name, prompt, context) → author envelope` factory over the shared `a-plus-maxing-api-key` lane; mirrors `subscription_dispatch.build_dispatch`, normalizes via `normalize_author_output`
- `scripts/serve/server.py` -- inject `metered_dispatch` as the server's `loop_dispatch` in `main()`/`build_server`, and invoke the ADR-0048-T1 shared-key provisioning bridge at server start (so the metered lane's `key_source.resolve` returns the shared key on the D5 default)
- `tests/runner/test_metered_dispatch.py` -- the D2 wire-scan (placement / outbound-capture / lane-swap / mutation-gate) + frozen-six numstat probe
- `tests/serve/test_loop_dispatch_wiring.py` -- reflect the metered `loop_dispatch` production injection

**Acceptance Criteria:**
1. `metered_dispatch.build_dispatch(...)` returns a `dispatch(name, prompt, context) → envelope` seam that authenticates ONLY via the shared `a-plus-maxing-api-key` metered lane (through `key_source.resolve` on the ADR-0047 abstraction) and normalizes via `normalize_author_output`; `subscription_dispatch.build_dispatch` remains built and importable (the retained North-Star adapter).
2. `server.build_server`/`main()` injects `metered_dispatch` as `loop_dispatch` AND invokes the ADR-0048-T1 shared-key provisioning bridge at server start, so in-app plan generation dispatches specialists through the `run_orchestrated`→`plan_driver.drive` seam authenticating on the shared `a-plus-maxing-api-key` lane; a plan runs end-to-end for a tester with 0 subscription/OAuth credential reads AND the DEFAULT shared-key path resolves via the bridge (0 `KeyUnavailableError` on the D5 default — a fixture with the shared key in `alpha_config` + no BYO key completes the plan, and mutating the bridge out REDs it to `KeyUnavailableError`).
3. **D2 wire-scan (i) Placement:** with a sentinel-returning `deid_client` fixture (`{"deidentified": False}`), the injected metered factory is invoked EXACTLY 0 times and never receives `raw_intake` (the `deid_in` gate halts to 0 dispatches at `plan_orchestrator.py:227`).
4. **D2 wire-scan (ii) Outbound capture:** with a clean-summary `deid_client` fixture (`set(summary) ⊆ SUMMARY_FIELD_SET`) and a synthetic legal name + store-content sentinel seeded into `raw_intake`, the metered adapter's ACTUAL OUTBOUND request payload (the bytes it sends the model API, not the seam-inbound args) has 0 field outside `SUMMARY_FIELD_SET`, 0 raw-PII hits, 0 store-sentinel hits, and the adapter performs 0 store reads.
5. **D2 wire-scan (iii) lane-swap invariance + (iv) mutation gate:** a metered↔subscription swap changes 0 bytes of the OUTBOUND payload; and a metered-adapter stub that appends a raw field to its outbound call OR opens a store read turns the scan RED (the test is invalid — and fails — if that mutation does not RED it).
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (the factory lands in `scripts/runner/`, outside the six).
7. `pytest tests/runner/test_metered_dispatch.py tests/serve/test_loop_dispatch_wiring.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0049 Consequence-Negative "subscription-lane goes unused — adapter retained + re-pointable" (AC-1); ADR-0001 tension "D2 egress no-op" (AC-3, AC-4, AC-5); "frozen six untouched" (AC-6); ADR-0048 D5 "shared-key default reaches the metered lane via the ADR-0048-T1 bridge" (AC-2)
**Dependencies:** ADR-0047-T2, ADR-0048-T1

---

### ADR-0049-T2: Manual "Update my plan now" trigger + schedule setting
**Status:** TODO
**ADR Source:** ADR-0049, Decision D4 (manual-default "Update my plan now" trigger + optional Off/Weekly/Daily schedule setting; the daily-INTERVAL auto-run glzi-gated); ADR-0049, Consequences-Negative (D4 Daily partially unbuilt)
**Files to create/modify:**
- `scripts/serve/server.py` -- the manual "Update my plan now" trigger wiring, firing the `run_orchestrated`→`drive` loop with the metered `loop_dispatch` (reusing the loop path)
- `vault/design/templates/app_shell.py` -- the My Info "Plan updates" section: the Update-now button + the Off/Weekly/Daily schedule radio
- `tests/serve/test_plan_update_trigger.py` -- one-re-gen-per-request, schedule-setting persistence, Daily inert

**Acceptance Criteria:**
1. The "Update my plan now" trigger fires exactly ONE plan re-generation per explicit request through the `run_orchestrated`→`drive` seam (metered `loop_dispatch`), and 0 re-generations with no request and no armed schedule.
2. The My Info "Plan updates" section renders the manual trigger + an Off (default) / Weekly / Daily schedule radio, matching the enumerated elements of `credential-onboarding-mockup.html` Surface B.
3. The schedule SETTING persists the selected cadence (Off default); selecting Weekly records the weekly cadence intent read by the schedule surface.
4. The Daily option renders as inert / "coming soon": selecting Daily arms NO daily auto-run (the daily-INTERVAL enable path is glzi-gated — `activate.py` registers `DAILY_MONITOR_LABEL` but adds no daily enable path), and the UI states scheduled auto-runs are not yet live.
5. The "Update my plan now" trigger reuses the CSRF-gated `_do_plan_loop` handler (the SEC `application/json` gate at `server.py:873-876`; the `/plan-loop` loop path grounded at `server.py:216`), so a cross-site CORS-simple `text/plain` POST is refused 415 BEFORE any metered spend across the specialist/judge/lens dispatch; if the trigger instead adds a NEW route, that route carries the identical `application/json` gate. Mutation-proven by a test that REDs if the gate is absent (the loop tick fires on a `text/plain` body).
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing.
7. `pytest tests/serve/test_plan_update_trigger.py -q` passes and the full baseline stays green.

**Risk Mitigations:** ADR-0049 Consequence-Negative "D4 Daily-schedule partially unbuilt — honestly deferred" (AC-4); "metered cost bounded by manual-default" (AC-1); ADR-0013 CSRF posture "forced-spend trigger reuses the SEC application/json gate before any metered spend" (AC-5)
**Dependencies:** ADR-0049-T1, ADR-0048-T4

---

### ADR-0049-T3: Per-tester cumulative monthly spend cap
**Status:** TODO
**ADR Source:** ADR-0049, Decision D5 (cumulative monthly per-tester ceiling on the shared key, building on `dispatch_budget.DEFAULT_DISPATCH_CAP`); ADR-0049, Consequences-Negative (D5 cap is a new invariant to police)
**Files to create/modify:**
- `scripts/runner/spend_cap.py` -- the cumulative monthly per-tester ledger (gitignored instance-local path) + a fail-closed refusal past the ceiling
- `scripts/runner/metered_dispatch.py` -- consult the spend cap before each metered dispatch (create-then-modify of the ADR-0049-T1 factory)
- `tests/runner/test_spend_cap.py` -- cap enforcement, monthly rollover, per-tester isolation, D2-scan-stays-green
- `.gitignore` -- gitignore the spend-ledger at-rest location

**Acceptance Criteria:**
1. `spend_cap` maintains a cumulative monthly per-tester count in a ledger persisted OUTSIDE `scripts/store/` (a gitignored instance-local path); `git check-ignore <ledger-path>` exits 0.
2. With the per-tester monthly ceiling not reached a metered dispatch proceeds; with the ceiling reached the next dispatch is REFUSED for that tester (a `SpendCapExceeded`-class refusal) — a test that lets ≥1 dispatch past the cap flips RED (non-vacuous).
3. The cap rolls over on a new calendar month — a ledger entry from the prior month does not count against the current month's ceiling.
4. The cap is per-tester isolated (one tester reaching the ceiling does not refuse another tester's dispatch) and composes with the existing per-run `dispatch_budget.DEFAULT_DISPATCH_CAP` (per-run count + cumulative monthly are independent ceilings).
5. `metered_dispatch` consults `spend_cap` before each outbound dispatch, and the ADR-0049-T1 D2 wire-scan stays green after the cap wiring (the cap adds 0 outbound payload field and performs 0 store read).
6. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing; `pytest tests/runner/test_spend_cap.py tests/runner/test_metered_dispatch.py -q` passes; the full baseline stays green.

**Risk Mitigations:** ADR-0049 Consequence-Negative "D5 per-tester cap is a new invariant to police — enforcement + non-bypass" (AC-2, AC-5)
**Dependencies:** ADR-0049-T1

---

## Dependency Map

```
ADR-0047-T1 --> ADR-0047-T2
ADR-0047-T1 --> ADR-0047-T3
ADR-0047-T2 --> ADR-0048-T3
ADR-0047-T3 --> ADR-0048-T3
ADR-0047-T2 --> ADR-0049-T1
ADR-0048-T1 --> ADR-0049-T1
ADR-0048-T1 --> ADR-0048-T2
ADR-0048-T3 --> ADR-0048-T2
ADR-0048-T2 --> ADR-0048-T4
ADR-0048-T3 --> ADR-0048-T4
ADR-0049-T1 --> ADR-0049-T3
ADR-0049-T1 --> ADR-0049-T2
ADR-0048-T4 --> ADR-0049-T2
```

**Data flow per edge:**
- `ADR-0047-T1 → ADR-0047-T2` / `→ ADR-0047-T3`: the `scripts.secret_store` abstraction the consumers route their defaults through.
- `ADR-0047-T2 → ADR-0048-T3`: `key_source.store` on the abstraction (the api-key write path the N-token class extends).
- `ADR-0047-T3 → ADR-0048-T3`: `oauth_pull`'s `credential_writer` on the abstraction (the per-source token write path).
- `ADR-0048-T1 → ADR-0048-T2`: the vendor `client_id`/`client_secret` the OAuth flow needs.
- `ADR-0048-T3 → ADR-0048-T2`: the per-source write class the callback writes the exchanged token through.
- `ADR-0048-T2 → ADR-0048-T4`: the connect-start route the UI "Connect" cards call.
- `ADR-0048-T3 → ADR-0048-T4`: the per-source write/status the UI PAT paste + connection status read.
- `ADR-0047-T2 → ADR-0049-T1`: `key_source.resolve` on the abstraction (the shared-key metered lane's credential resolve).
- `ADR-0048-T1 → ADR-0049-T1`: the shared-key provisioning bridge — `alpha_config` exports the loaded shared Anthropic key as in-process `ANTHROPIC_API_KEY` at server start so the metered lane's `key_source.resolve` returns it on the D5 default (without the bridge the default "touch nothing" path raises `KeyUnavailableError`).
- `ADR-0049-T1 → ADR-0049-T3`: the `metered_dispatch` factory the spend cap gates.
- `ADR-0049-T1 → ADR-0049-T2`: the metered `loop_dispatch` the manual trigger fires.
- `ADR-0048-T4 → ADR-0049-T2`: the My Info settings shell the "Plan updates" section extends.

**Topological order (Kahn's; parallel groups):**
1. `ADR-0047-T1`, `ADR-0048-T1` (parallel — entry points, no dependencies)
2. `ADR-0047-T2`, `ADR-0047-T3` (parallel — each depends only on ADR-0047-T1)
3. `ADR-0048-T3`, `ADR-0049-T1` (parallel — ADR-0048-T3 after {ADR-0047-T2, ADR-0047-T3}; ADR-0049-T1 after {ADR-0047-T2 (tier 2), ADR-0048-T1 (tier 1)} — the max-depth predecessor is ADR-0047-T2, so ADR-0049-T1 stays tier 3)
4. `ADR-0048-T2`, `ADR-0049-T3` (parallel — ADR-0048-T2 after {ADR-0048-T1, ADR-0048-T3}; ADR-0049-T3 after ADR-0049-T1)
5. `ADR-0048-T4` (after {ADR-0048-T2, ADR-0048-T3})
6. `ADR-0049-T2` (after {ADR-0049-T1, ADR-0048-T4})

**Entry points:** `ADR-0047-T1`, `ADR-0048-T1`
**Critical path:** `ADR-0047-T1 → ADR-0047-T2 → ADR-0048-T3 → ADR-0048-T2 → ADR-0048-T4 → ADR-0049-T2` (6 tasks; the parallel path through `ADR-0047-T3` is equal length). Acyclic — all 10 nodes ordered by Kahn's with none remaining.

## Constraint Propagation

Cross-cutting constraints from the ADRs and their enforcing acceptance criteria (each is a falsifiable AC, not prose):

| Constraint | Source | Enforced in | Enforcing AC |
|-----------|--------|-------------|--------------|
| Frozen-six numstat == 0 (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py`) | ADR-0047 + ADR-0049 Validation | ADR-0047-T1, ADR-0047-T2, ADR-0047-T3, ADR-0048-T1, ADR-0048-T2, ADR-0048-T3, ADR-0048-T4, ADR-0049-T1, ADR-0049-T2, ADR-0049-T3 | the `git diff --numstat 3ab1c3ab -- <six>` prints-nothing AC in each (asserted at the first build of the abstraction per ADR-0047 Falsification) |
| Risk-N3: preserve `credential_*` (`_key_def_count()==0` under `scripts/ingest/`) | ADR-0047 Decision/Falsification | ADR-0047-T3 | AC-1 (names unchanged), AC-2 (`_key_def_count()==0` green) |
| 0 direct `security` shell-out in the 3 consumers | ADR-0047 Falsification | ADR-0047-T2, ADR-0047-T3 | the `grep security (find|add)-generic-password ... == 0` AC in each |
| ADR-0001 crown-jewel: OAuth path carries 0 store bytes / 0 model-lane calls; code→token exchange declines cross-host redirects | ADR-0048 D7 + D1 (amended) | ADR-0048-T2 | AC-4 (exchange declines cross-host 3xx / host-lock), AC-6 (D7 wire-scan, per-family mutation-RED) |
| ADR-0001 crown-jewel: metered OUTBOUND payload ⊆ `SUMMARY_FIELD_SET`, 0 side-channel, injected downstream of `deid_in` | ADR-0049 D2 + constraint-propagation | ADR-0049-T1 (and ADR-0049-T3 AC-5 keeps it green) | AC-3/AC-4/AC-5 (placement / outbound-capture / lane-swap+mutation) |
| ADR-0005: shared secrets never on the tracked tree (out-of-band only) | ADR-0048 D4/D5 | ADR-0048-T1, ADR-0048-T3 | ADR-0048-T1 AC-3/AC-4; ADR-0048-T3 AC-4 |
| ADR-0005: fallback encrypted file gitignored + hook-covered | ADR-0047 OQ-4 | ADR-0047-T1 | AC-5 (`git check-ignore` exits 0) |
| ADR-0013: 127.0.0.1-only loopback + body ceiling on new write paths | ADR-0048 D1/D3 (constrains ADR-0013) | ADR-0048-T2, ADR-0048-T3 | ADR-0048-T2 AC-2; ADR-0048-T3 AC-2 |

## Test Strategy

### Unit Tests
- **Scope:** `scripts/secret_store/__init__.py`, `scripts/model/key_source.py`, `scripts/runner/auth_isolation.py`, `scripts/ingest/oauth_pull.py`, `scripts/serve/alpha_config.py`, `scripts/runner/metered_dispatch.py`, `scripts/runner/spend_cap.py`.
- **Approach:** pytest with mocked per-OS keyring backends and forced-import-failure fixtures (fallback tier); injected credential seams as mock points; fixture model clients (no live SDK — the 0-live-spend guard). No network, no real keychain.
- **Criteria covered:** ADR-0047-T1 AC-1..3,5; ADR-0047-T2 AC-1..4; ADR-0047-T3 AC-1,3,4; ADR-0048-T1 AC-1..4; ADR-0049-T1 AC-1; ADR-0049-T3 AC-1..4.

### Integration Tests
- **Scope:** the serve credential-write path (route → `secret_store` → `oauth_pull` reader), the OAuth connect-start → one-shot callback → per-source write chain, the `run_orchestrated`→`drive` seam with the metered factory injected as `loop_dispatch`, and the manual-trigger → loop re-gen path.
- **Approach:** in-process serve handlers on 127.0.0.1 with a recording network seam and fixture OAuth/model clients; the SPA/template render assertions drive the UI surfaces.
- **Criteria covered:** ADR-0047-T2 AC-4; ADR-0047-T3 AC-4; ADR-0048-T3 AC-1,3; ADR-0048-T2 AC-1,5; ADR-0048-T4 AC-1..3,7; ADR-0049-T1 AC-2; ADR-0049-T2 AC-1..4.

### Risk-Specific Tests
- **Scope:** the two crown-jewel wire-scans (ADR-0048 D7, ADR-0049 D2), the frozen-six numstat probe, the Risk-N3 `_key_def_count()==0` guard, the tracked-secret scans (ADR-0005), the `application/json` CSRF gates on the new secret-write + forced-spend routes, the code→token exchange redirect-decline, the env-first key precedence, the shared-key provisioning bridge (D5 default), the loopback-bind check, the per-tester spend-cap ceiling, and the D4 Daily-inert (glzi-gated) assertion.
- **Approach:** each risk test is mutation-gated where it is a ruling — the scan asserts the CLEAN direction truthy first, then a planted violation (a store-content byte on the OAuth outbound; a 302-to-attacker-host on the token exchange; a `text/plain` cross-site POST on a secret-write/forced-spend route; a keyring read while `ANTHROPIC_API_KEY` is set; the provisioning bridge mutated out; a raw field / store read on the metered outbound; a `def make_key` under `scripts/ingest/`; a dispatch past the cap) must flip it RED, so the test cannot be built green-always.
- **Criteria covered:** ADR-0048-T2 AC-2,3,4,6,7 (D1 inbound boundary + D7 egress + code→token redirect-decline); ADR-0049-T1 AC-3,4,5,6 (D2 egress + frozen six); ADR-0047-T2 AC-3,5,6; ADR-0047-T3 AC-2,3,5; ADR-0048-T1 AC-3,4,5,6; ADR-0048-T3 AC-2,4,5,6; ADR-0048-T4 AC-4,5,6; ADR-0049-T2 AC-4,5,6; ADR-0049-T3 AC-1,2,5,6.

**Self-verifying ACs (covered by execution, not a separate test asset):** each task's terminal `pytest …` AC is the run itself — ADR-0047-T1 AC-7, ADR-0047-T2 AC-7, ADR-0047-T3 AC-6, ADR-0048-T1 AC-7, ADR-0048-T3 AC-7, ADR-0048-T2 AC-8, ADR-0049-T1 AC-7, ADR-0049-T2 AC-7 — and the dependency/import build AC names its own command (ADR-0047-T1 AC-4: `keyring` in `requirements.txt` + `import keyring` exits 0 on a clean venv). With these, plus the ADR-0048-T3 AC-2 loopback/body-ceiling check now mapped in Risk-Specific above, every acceptance criterion maps to a test or a verification command.

## Repo-Grounding Ledger

Grounded against the live worktree on `feature/credential-onboarding-build` (Phase-4 author RGC probes; the Phase-6 judge re-runs all four independently).

| Task | RGC-1 (manifest) | RGC-2 (premise) | RGC-3 (cited input) | RGC-4 (dup) | Disposition |
|------|------------------|-----------------|---------------------|-------------|-------------|
| ADR-0047-T1 | pass (`scripts/secret_store/` absent → Create; `requirements.txt`/`.gitignore` present → Modify) | pass (`keyring` absent from `scripts/`+`requirements.txt`, confirmed) | pass (`requirements.txt` = pytest+jsonschema; `.gitignore` has `.env*`) | pass (no `secret_store`/keyring module anywhere) | Grounded |
| ADR-0047-T2 | pass (`key_source.py`, `auth_isolation.py` + their tests present → Modify) | pass (seams `resolve`@65/`store`@135/`build_subscription_env`@87 + shell-outs at cited lines) | pass (`keychain_runner`, `keychain_writer`, `keychain_reader` resolve) | pass (abstraction is the only new surface, from T1) | Grounded |
| ADR-0047-T3 | pass (`oauth_pull.py` + `test_oauth_pull.py` present → Modify) | pass (`credential_reader`/`credential_writer`@320/382; `_key_def_count()`@107 == 0) | pass (`_read/_write_oauth_credential`@186/208 shell-out; `test_ingest.py::_key_def_count`) | pass | Grounded |
| ADR-0048-T1 | pass (`scripts/serve/alpha_config.py` absent → Create) | pass (out-of-band posture; `block-pii-commit`/`pre-push-pii-scan` hooks present) | pass (`.gitignore` `.env*`; ADR-0005 hooks confirmed; the D5 bridge's cited input `key_source.resolve`@65 reads env `ANTHROPIC_API_KEY` first at `key_source.py:80-82` then the keychain then raises `KeyUnavailableError`@88 — the env-first branch the bridge provisions onto [VERIFIED]) | pass (no `alpha_config`/build-config loader present) | Grounded |
| ADR-0048-T3 | pass (`server.py` present → Modify; `test_credential_writes.py` absent → Create) | pass (`_save_key`@925/`_key_status`@916; `/settings/key` route @183/201) | pass (the ADR-0013 single-key write class resolves; `oauth_pull` credential_reader) | pass | Grounded |
| ADR-0048-T2 | pass (`oauth_callback.py` absent → Create; `server.py` → Modify; `test_oauth_callback.py` absent → Create) | pass (no `oauth`/`callback`/`redirect_uri`/`pkce` in `server.py` today — new inbound arm) | pass (`do_GET`@178/`do_POST`@194 `if self.path` chains; Garmin OAuth-1.0a at `oauth_pull.py:110-122` (`_GARMIN` manifest `"auth": "oauth1a"`), canonical anchor `oauth_pull.py:584` `_read_garmin`) | pass (no callback route exists) | Grounded |
| ADR-0048-T4 | **[AMENDED 2026-07-17 S143 — PF-S142-01]** pass (`app_view.html` present → Modify; UI test absent → Create) | **[AMENDED S143 — supersedes the prior `intake.py` reconciliation]:** the prior row targeted `intake.py` (a 6-step flow) and reconciled the mockup's "Step 9 of 9" as stale-vs-6. That was mis-grounded: `intake.py` is UNSERVED — `server.py:133/:139` serves ONLY `generate.run('app')` (the SPA); `generate.py:27` maps `'app'→app_shell`, `'intake'→intake` as INDEPENDENT templates; `app_shell.py` references `intake.py` nowhere. The LIVE intake surface is the SPA's `screen-wizard` (`app_view.html:631`), ALREADY a **9-step** flow whose step 9 IS "API key" (`app_view.html:649` stepper, `:751` `wstep`, header "Step 1 of 9" `:634`). So the mockup's "Step 9 of 9" is ACCURATE for the served surface — the credential step EXTENDS the existing step 9 (add wearables + Apple + the D5 shared/BYO choice; the existing `wiz-key` `sk-ant-` input `:758` = the BYO branch). No renumber, no rebuild. The credential-step UI is sourced faithfully from `credential-onboarding-mockup.html` Surface A. | pass (`screen-profile` at `app_view.html:607` — the served My-Info surface, extended with the Connections & Keys panel; per-source status is client-side via the already-routed `GET /settings/trackers`, mirroring the `/settings/key` pill) | pass (extends existing served surfaces, no new wizard) | **Grounded (S143 re-reconciled)** |
| ADR-0049-T1 | pass (`metered_dispatch.py` absent → Create; `server.py`/`test_loop_dispatch_wiring.py` → Modify; `test_metered_dispatch.py` → Create) | pass (`run_orchestrated`@127/`deid_in`@223/sentinel-halt@227/`_dispatch_domains`@358; `subscription_dispatch.build_dispatch`@45 the only adapter; `loop_dispatch`@170) | pass (`SUMMARY_FIELD_SET`@router:23 + `deid_in`@90; `normalize_author_output`; `session(name,prompt,context)`@subscription:67) | pass (no metered adapter for the seam exists) | Grounded |
| ADR-0049-T2 | pass (`server.py`/`app_shell.py` → Modify; `test_plan_update_trigger.py` absent → Create) | pass (`/plan-loop`@216/`_do_plan_loop`@846 loop path; `DAILY_MONITOR_LABEL`@activate:52 label-only, no daily enable) | pass (`plan_loop.signal`→`run_orchestrated`; the mockup "Plan updates" section) | pass | Grounded |
| ADR-0049-T3 | pass (`spend_cap.py` absent → Create; `metered_dispatch.py` → Modify from T1; `.gitignore` → Modify; `test_spend_cap.py` → Create) | pass (`DEFAULT_DISPATCH_CAP=64`@dispatch_budget:35 per-run cap; no monthly/per-tester ledger exists) | pass (`dispatch_budget` per-run cap resolves) | pass (no cumulative-spend ledger anywhere) | Grounded |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task (ADR-0047: T1–T3; ADR-0048: T1–T4; ADR-0049: T1–T3)
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0047…0049…md` read in full)

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion (each has 5–8)
- [x] All acceptance criteria are binary (a command/condition with a pass/fail outcome)
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in at least one task block
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (Kahn's orders all 10 nodes; none remain)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed (ADR-0047-T1, ADR-0048-T1) and have Dependencies: "None (entry point)"

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream ADR constraints in their acceptance criteria (frozen-six, Risk-N3, ADR-0001 crown-jewel, ADR-0005 out-of-band, ADR-0013 loopback — see Constraint Propagation table)
- [x] Constraint Propagation Table entries have corresponding acceptance criteria in affected tasks

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present
- [x] Every open question / pending tension / unmitigated risk has a disposition (Proceed/Defer; no Block applies)
- [x] Block dispositions have corresponding research spike tasks (none — no Block dispositions)
- [x] Defer dispositions have justifications (OQ-5/OQ-4/OQ-2/O-6 — LIVE-run or post-V1, each justified)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in in-scope ADRs is covered by at least one task's Risk Mitigations (ADR-0047: 4/4; ADR-0048: 5/5; ADR-0049: 4/4)

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (the two wire-scans, frozen-six, Risk-N3, tracked-secret scans, spend cap, Daily-inert)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the template (Component Overview → Unresolved Concerns → File Manifest → Tasks → Dependency Map → Test Strategy → Validation Checklist, plus Constraint Propagation + Repo-Grounding Ledger)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (or is `Create`d by a prior task in dependency order — `metered_dispatch.py` created by ADR-0049-T1 before ADR-0049-T3 modifies it)
- [x] Every File Manifest `Create` row names a path that does NOT already exist (RGC-4 confirmed absent for all new modules/tests)
- [x] Every ADR premise a task relies on was re-verified against the current repo (the ADR-0048-T4 "Step-9" premise is Stale-Premise-Reconciled in the Ledger; all others current)
- [x] Every cited input a task reads declares its structural assumption AND the live file satisfies it (seams, routes, `SUMMARY_FIELD_SET`, `_key_def_count`, `DEFAULT_DISPATCH_CAP` all resolve at cited lines)
- [x] No task proposes a new artifact that duplicates an existing repo capability (no `secret_store`/`alpha_config`/`oauth_callback`/`metered_dispatch`/`spend_cap` exists today)
- [x] Repo-Grounding Ledger present, one row per task, with a disposition (9 Grounded, 1 Stale-Premise-Reconciled)
