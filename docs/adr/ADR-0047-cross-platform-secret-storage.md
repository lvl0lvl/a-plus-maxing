## ADR-0047: Cross-Platform Secret Storage via an OS-Native `keyring` Abstraction

> **Y-Statement:** In the context of three credential modules that all shell out to the macOS-only `security` binary while the alpha must onboard testers on Windows and Mac, facing the tension that a cross-platform secret path needs a portable backend yet the clonable PII-free trunk (ADR-0005) carries zero third-party dependencies on the secret path and the friction-first alpha cannot impose a master password, we decided to store secrets in the OS-native store through a single `keyring`-backed abstraction plugged into the modules' existing injectable credential seams, with an encrypted-file / environment-variable fallback tier for no-keyring or headless environments, rejecting an app-rolled crypto vault as the primary store, to achieve a login-session-unlocked cross-platform secret path with the three consumers on one backend, accepting `keyring` as the first third-party runtime dependency on the secret path, a per-OS backend-behaviour test matrix, and a fallback tier whose at-rest security is weaker than the OS stores'.

```yaml
id: ADR-0047
title: "Cross-Platform Secret Storage via an OS-Native keyring Abstraction"
status: accepted
date: 2026-07-14
decision-makers: [Walter McGivney]
tags: [secret-storage, cross-platform, keyring, credential-abstraction, fallback-tier, foundation, tier-1, alpha-onboarding]
related-adrs: [ADR-0048, ADR-0005, ADR-0039]
```

### Context

Three modules read and write the runtime secrets the system depends on, and every one of them shells out to the macOS-only `security` binary. `scripts/model/key_source.py` reads the no-train API key with `security find-generic-password` and writes it with `security add-generic-password` ([key_source.py:52-53,120-121](../../scripts/model/key_source.py) [VERIFIED]); `scripts/runner/auth_isolation.py` reads the subscription OAuth token the same way ([auth_isolation.py:74-75](../../scripts/runner/auth_isolation.py) [VERIFIED]); `scripts/ingest/oauth_pull.py` reads and writes per-source tracker refresh tokens the same way ([oauth_pull.py:197,223](../../scripts/ingest/oauth_pull.py) [VERIFIED]). Each already exposes an injectable seam — `resolve(keychain_runner=…)` / `store(key, *, keychain_writer=…)`, `build_subscription_env(base_env, *, keychain_reader=…)`, and `access_token/fetch(…, credential_reader=…, credential_writer=…)` ([key_source.py:65,135](../../scripts/model/key_source.py); [auth_isolation.py:87](../../scripts/runner/auth_isolation.py); [oauth_pull.py:320,382](../../scripts/ingest/oauth_pull.py) [VERIFIED]) — so the swap point exists, but the seam names are not uniform across the three, and one (`auth_isolation`) is read-only.

Two forces pull against each other. The alpha onboards testers on both Mac and Windows, and the `security` shell-out returns nothing on any non-macOS host ([.pipeline/discovery.md](.pipeline/discovery.md) [VERIFIED]), so a Windows tester cannot store or resolve a credential today. Against portability pull two constraints: the trunk is a clonable, PII-free repository whose secret path has zero third-party runtime dependencies (`requirements.txt` is `pytest` + `jsonschema` only ([requirements.txt:14-15](../../requirements.txt) [VERIFIED]); `keyring` appears nowhere in `scripts/` [VERIFIED]), and the friction-first alpha must not add a master-password step — the OS-native stores unlock with the login session, a property a self-managed vault would not have [UNVERIFIED: OS-store login-unlock behaviour, confirm per-OS at spec/build — OQ-1].

The decision binds more than the maintainer. The Windows/Mac **tester** needs the credential path to work at all and to unlock without a separate passphrase; the **data subject** needs the secret to stay OS/hardware-protected at rest and off the tracked tree (ADR-0005); the **maintainer** absorbs a new dependency, a per-OS test surface, and the reconciliation of three differently-named seams. Because the choice fixes the backend all three consumers sit on, it is a foundational decision, reused beyond the immediate onboarding feature.

### Decision

Store secrets in the OS-native secret store through a single cross-platform abstraction (`keyring`, mapping to macOS Keychain, Windows Credential Manager/DPAPI, and Linux Secret Service), plugged into the three modules' existing injectable credential seams, with a fallback tier (encrypted-file or environment variable) for no-keyring and headless environments. Reject an app-rolled crypto vault as the primary store. Refactor the three `security`-specific modules onto the abstraction, preserving the `credential_*` seam names in `scripts/ingest/` so the Risk-N3 `def .*key` scan stays green.

### Rationale

The backend was evaluated across four criteria the trunk makes load-bearing: cross-platform reach, unlock friction, secret-at-rest security, and buildability under extend-not-rebuild + the frozen spine.

On **reach**, `keyring` exposes one `get_password`/`set_password` API over each OS's native store, which is the only option that covers Mac and Windows testers without per-OS branching in the consumers [UNVERIFIED: keyring backend mapping, OQ-1]. On **friction**, the OS stores unlock with the login session, so no master password is introduced — the friction-first requirement the alpha sets, and the property that most sharply separates this from a rolled vault. On **security**, the OS stores hold key material under OS/hardware protection; an app-rolled vault would make us own the crypto, the KDF, and a master-key-provisioning problem, and would be weaker than the platform stores it replaced (see Alternative B). On **buildability**, the seams already exist, so this is a backend swap behind them: the `<always-frozen>` six (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py` ([tracker-ingestion-api-adapters.md §9](../design/tracker-ingestion-api-adapters.md) [VERIFIED])) are untouched, and every existing seam-injected test keeps its mock point.

The long-term cost is explicit and accepted (detailed in Consequences): `keyring` is the first third-party runtime dependency on the secret path, and the fallback tier is a weaker-at-rest surface to threat-model (OQ-2). The abstraction keeps the concrete backend swappable, so the North-Star hosted cutover can later replace the local OS store with a server-side broker behind the same seams.

### Consequences

**Positive:**
- Cross-platform onboarding is unblocked: a Windows tester can store and resolve a credential through the same code path as a Mac tester, closing the `security`-only gap ([.pipeline/discovery.md](.pipeline/discovery.md) [VERIFIED]).
- The OS store unlocks with the login session, so no master-password step is added — the friction-first alpha requirement holds [UNVERIFIED per-OS, OQ-1].
- One backend serves all three consumers, and because the injectable seams already exist the change is a bounded backend swap behind them, leaving the `<always-frozen>` six at `git diff --numstat` = 0 ([tracker-ingestion-api-adapters.md §9](../design/tracker-ingestion-api-adapters.md) [VERIFIED]).

**Negative:**
- `keyring` is the **first third-party runtime dependency on the secret path** — a fresh clone gains a `pip install keyring` step, a direct ADR-0005 clonable-trunk cost the current pure-stdlib path does not carry ([requirements.txt:14-15](../../requirements.txt) [VERIFIED]).
- No-keyring / headless environments (containers, servers, CI) fall to the fallback tier, whose environment-variable extractability and encrypted-file key-management are weaker at rest than the OS stores and constitute a security sub-surface that must be threat-modelled, not waved through (OQ-2).
- The abstraction adds an indirection layer plus a per-OS backend-behaviour test matrix (a read/write round-trip must be proven on each of the three backends, mocked per-OS in CI) — new maintenance surface over a 1+ year horizon.
- The three modules' seam names are non-uniform (`keychain_runner`/`keychain_writer`, read-only `keychain_reader`, `credential_reader`/`credential_writer`), so the refactor must reconcile them onto one interface **without renaming** `scripts/ingest/`'s `credential_*` seams, which are named to avoid the Risk-N3 `def .*key` dedupe-fork scan ([oauth_pull.py:21-23](../../scripts/ingest/oauth_pull.py); [test_ingest.py:107-109](../../tests/ingest/test_ingest.py) [VERIFIED]).

**Neutral:**
- The OS keychain item service names (`a-plus-maxing-api-key`, `a-plus-maxing-oauth-token`, `a-plus-maxing-<source>-oauth`) are unchanged; only the mechanism that reaches them moves from `security` to `keyring`.
- The abstraction module becomes a shared dependency of the model, runner, and ingest paths — one module three subsystems import.

### Alternatives Considered

#### Alternative A: OS-native store via `keyring` (Chosen)
See Decision. Covers Mac + Windows testers with one API, keeps the login-session unlock, and builds as a backend swap behind the existing seams with the frozen six untouched; trade-off is the first third-party dep on the secret path (ADR-0005) plus a per-OS test surface.

#### Alternative B: App-rolled encrypted crypto vault
Ship our own encrypted secret file with an app-managed cipher and key-derivation.
- **Supporting evidence:** No third-party dependency; fully self-contained and portable across every OS without relying on a platform store's presence.
- **Trade-offs:** We would own the crypto, the KDF, and a master-key problem; a master password would be required to unlock it, violating the friction-first requirement; and the result is weaker than the OS/hardware-protected key material the platform stores already provide. Rejected as primary.
- **When this becomes the right choice:** On a target platform with no OS secret store AND a secure headless way to provision the master secret — a condition the alpha's Mac/Windows machines do not meet.

#### Alternative C: Plaintext `.env` / config file
Read secrets from an unencrypted environment file or config.
- **Supporting evidence:** Zero dependency, zero unlock friction, works identically on every OS and in headless CI where a secret manager injects the value.
- **Trade-offs:** Insecure at rest — a plaintext secret on disk. Rejected as the primary store; retained only as a documented last-resort option WITHIN the fallback tier for headless environments.
- **When this becomes the right choice:** Ephemeral CI where the secret is injected by the CI secret manager and never persists to a durable disk.

#### Alternative D: Stay macOS-`security`-only
Keep the three modules shelling out to `security` and do nothing.
- **Supporting evidence:** No change, no new dependency, no refactor; it works on the author's macOS machine today.
- **Trade-offs:** Breaks every Windows tester — the shell-out returns nothing off macOS ([.pipeline/discovery.md](.pipeline/discovery.md) [VERIFIED]) — which is the entire reason this ADR exists. Rejected.
- **When this becomes the right choice:** If the alpha were Mac-only. It is not.

### Related Decisions

| ADR | Relationship | Description |
|-----|-------------|-------------|
| ADR-0048 | enables | Cross-platform storage is the precondition for a Mac+Windows onboarding; ADR-0048's OAuth flow and key/token writes read and write every credential through this abstraction. Reciprocal of ADR-0048's `depends-on ADR-0047`. |
| ADR-0005 | tensions-with | `keyring` is the first third-party runtime dependency on the secret path — a clonable-trunk cost against ADR-0005's PII-free / minimal-dependency trunk. Boundary: the dependency is accepted as the cross-platform cost, and the fallback tier (env / encrypted-file) is the no-extra-dep escape hatch. Reciprocal of ADR-0005's `tensions-with ADR-0047` (append-only backfill). |
| ADR-0039 | refines | Generalizes ADR-0039's keychain-OAuth-token-at-rest pattern to the cross-platform store; `auth_isolation.py` (an ADR-0039 artifact) is one of the three consumers now reading through the abstraction. Reciprocal of ADR-0039's `refined-by ADR-0047` (append-only backfill). |

This decision `constrains` the three credential consumer modules — `scripts/model/key_source.py`, `scripts/runner/auth_isolation.py`, and `scripts/ingest/oauth_pull.py`: all credential I/O routes through the abstraction (keyring primary + fallback), no module shells out to `security` directly, and the `credential_*` seam names in `scripts/ingest/` are preserved (else the Risk-N3 `def .*key` scan REDs). These are code modules, not ADRs, so they are named here rather than as table rows ([dag.md](.pipeline/dag.md) [VERIFIED]).

### Validation Approach

**Confirmation criteria:**
- A cross-platform write→read round-trips a secret through each backend (macOS Keychain / Windows Credential Manager / Linux Secret Service), mocked per-OS in CI — expected: ≥1 successful store-then-resolve per backend, key value recovered byte-for-byte.
- An **unattended** (no interactive login session) write→read round-trip succeeds on each backend — the ADR-0039-runner scheduled tracker-pull writes a rotated refresh token via `set_password` and re-reads it with no prompt or block — expected: ≥1 successful unattended store-then-resolve per backend, 0 prompts/blocks on the write; a backend that prompts or errors on the unattended write is routed to the fallback tier for that OS (OQ-1, the ADR-0047×ADR-0039 seam).
- The fallback tier engages **iff** `keyring` is unavailable — expected: with `keyring` importable, 0 fallback reads; with `keyring` absent, the fallback serves the secret and the consumer still resolves.
- Every existing seam-injected test stays green after the refactor (the seams are the test mock points) — expected: the full `.venv/bin/python -m pytest -q` baseline passes with 0 regressions.

**Falsification criteria:**
- If `grep -rnE "security (find|add)-generic-password" scripts/ --include="*.py"` returns ≥1 hit in any of the three consumer modules after the refactor (any residual localized to the single abstraction module only), a direct macOS shell-out survived — halt and route it through the abstraction. Threshold: 0 direct shell-outs in the three consumers (this grep lists all three today, pre-refactor [VERIFIED]).
- If `git diff --numstat` shows >0 on any of the `<always-frozen>` six (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py`), the frozen spine was edited — halt and re-route the change out of the engine ([tracker-ingestion-api-adapters.md §9](../design/tracker-ingestion-api-adapters.md) [VERIFIED]).
- If `tests/ingest/test_ingest.py` `_key_def_count()` returns >0 (the `def .*key` count under `scripts/ingest/` rises above its current 0), the seam rename tripped the Risk-N3 dedupe-fork scan — halt and restore the `credential_*` names ([test_ingest.py:107-109,197](../../tests/ingest/test_ingest.py) [VERIFIED]).
- Time horizon: run all four at the first build of the abstraction, at every release thereafter, and before the July-2026 physician-visit deliverable ships.

**Review triggers:**
- A `keyring` major-version release, or a deprecation/behaviour change in any target OS's secret store.
- A new credential consumer is added (it must adopt the abstraction, not a fourth `security` shell-out).
- A headless / container deployment target is added (exercises the fallback tier and its threat model — OQ-2).
- The North-Star hosted cutover begins — a server-side secret broker supersedes the local OS store behind the same seams.

### Open Questions

| # | Question | Owner | Target Date | Impact on This Decision |
|---|----------|-------|-------------|------------------------|
| OQ-1 | Confirm `keyring`'s backend mapping and the login-session unlock behaviour on each target OS (macOS Keychain / Windows Credential Manager-DPAPI / Linux Secret Service) — does any backend prompt on **read** rather than unlock with the session, AND does any backend prompt or block on **write** (`set_password`)? The unattended scheduled tracker-pull (the ADR-0039 runner cadence) writes rotated refresh tokens back through this abstraction on every fetch for rotating vendors (Google/Whoop), so a write-prompting backend breaks the unattended tick, not just the friction-first read path. | Walter McGivney | Spec/build stage | The cross-platform-reach and friction-first claims rest on this; a backend that prompts on read would need the fallback tier for that OS, and a backend that prompts/blocks on write under a locked/unattended session breaks the ADR-0039-runner refresh-token write-back at the ADR-0047×ADR-0039 seam — that path falls to the fallback tier for that OS. Tagged [UNVERIFIED] in this ADR. |
| OQ-2 | Threat-model the fallback tier: the encrypted-file key-management (where the file's key lives) and the environment-variable extractability. | Walter McGivney | Spec/build stage | Bounds how weak the no-keyring path is; pins the Negative consequence rather than leaving it "encrypted-file/env" hand-waved. |
| OQ-3 | What is the abstraction module's path and interface, and how do the three non-uniform seams (`keychain_runner`/`keychain_writer`, read-only `keychain_reader`, `credential_reader`/`credential_writer`) reconcile onto it **without** renaming `scripts/ingest/`'s `credential_*` (Risk-N3)? | Walter McGivney | Spec/build stage | The concrete refactor shape; a rename that reaches a `def …key` under `scripts/ingest/` REDs the Risk-N3 scan. |
| OQ-4 | Does the fallback tier's encrypted file need an at-rest location under ADR-0005 — gitignored and covered by `block-pii-commit.sh` / `pre-push-pii-scan.sh` so a fallback secret can never be committed? | Walter McGivney | Spec/build stage | Ties the fallback surface into the PII-free-trunk guard; an uncovered on-disk secret is an ADR-0005 leak vector. |

### Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-07-14 | Initial draft (Phase 4 AUTHOR, ADR-0047 — Tier-1 foundation of the alpha-tester credential storage + onboarding cluster, [.pipeline/discovery.md](.pipeline/discovery.md)). Selects an OS-native `keyring` abstraction over the three modules' existing injectable seams, with an encrypted-file/env fallback tier for headless/no-keyring; rejects an app-rolled crypto vault as primary (owns the crypto + a master-password friction that violates friction-first + weaker than OS/hardware-protected key material), plaintext `.env` as primary (insecure at rest; kept only as a fallback-tier option), and staying macOS-`security`-only (breaks every Windows tester). Refactors `key_source.py` / `auth_isolation.py` / `oauth_pull.py` onto the abstraction, preserving the `credential_*` seam names in `scripts/ingest/` (Risk-N3). Live-tree grounding [VERIFIED]: the 3 `security` shell-outs, the non-uniform seams, the frozen six, `keyring` absent from `requirements.txt`. keyring backend mapping + OS-store login-unlock tagged [UNVERIFIED] (OQ-1). enables ADR-0048; tensions-with ADR-0005; refines ADR-0039; constrains the three credential consumer modules. Reversibility Moderate-Hard (the injectable seam keeps the backend swappable, but keyring-primary + the new dependency + the fallback-tier posture is a durable commitment — not a full one-way door). | Walter McGivney |
| 2026-07-14 | Phase-8 red-team remediation (RT-04, RT-05). **RT-04:** extended OQ-1 to also probe backend **write** (`set_password`) prompting/blocking — the unattended ADR-0039-runner scheduled tracker-pull writes rotated refresh tokens back through this abstraction on every fetch for rotating vendors (Google/Whoop), so a write-prompting backend breaks the unattended tick (not just the friction-first read path); a write-prompting backend routes that path to the fallback tier, and a new Confirmation criterion asserts an unattended (no-interactive-session) write→read round-trip per backend. **RT-05:** dropped the ephemeral pipeline label "gap D" from the Consequences-Negative fallback-tier clause and OQ-2 (the concern is fully carried by OQ-2; no content lost). Also applied the append-only reciprocal Phase-8 backfills into ADR-0005 (`tensions-with ADR-0047`) and ADR-0039 (`refined-by ADR-0047`) — those target bodies otherwise unchanged. Decision, alternatives, and status UNCHANGED. | Walter McGivney |
