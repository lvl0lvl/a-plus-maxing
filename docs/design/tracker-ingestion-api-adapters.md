# Design Note — Mechanical Tracker Ingestion via API-Pull Adapters

```yaml
kind: design-note
author: Architect (design mode)
date: 2026-07-13
branch: feature/tracker-ingestion-adapters
base: main @ fad06615
status: operator-approved (Option A, "go" S137); amended 2026-07-13 post-Tier-2 review (F1 retire-not-reuse, F3 seam-naming)
scope: EXTENDS ADR-0003 (source-extensible ingestion). Does NOT rebuild it.
extends-adrs: [ADR-0003, ADR-0039]
constrained-by: [ADR-0001, ADR-0005]
frozen: <always-frozen> six + ingest.run + scheduler.run + store.append + the Adapter protocol
```

## 0. Summary (the five load-bearing lines)

1. **Fetch→land contract:** a shared OAuth/fetch layer authenticates and pulls each source's readings-new-since-last-run into a **gitignored staged export file** in the shape a *file-reading* adapter already parses; the UNCHANGED `ingest.run(adapter, staged_file, root)` → `store.append` lands them. `ingest.run`, `scheduler.run`, `store.append`, the `Adapter` protocol, and the `(item, timepoint, source)` dedup key are all reused **byte-unchanged** (chosen Option A of two).
2. **OAuth/keychain model:** a per-source refresh token lives in a per-source OS-keychain item (`a-plus-maxing-<source>-oauth`), read at call time via the exact `security find-generic-password -w -s <service>` shape `key_source.py` and `auth_isolation.py` already use — never a tracked file. The adapter mints a short-lived access token from it and fetches. The one-time dev-app registration + first authorization is the operator-gated LIVE step; the build is fixture-tested with fake keychain + fake HTTP seams.
3. **ADR-0001 ruling:** the API pull is **INBOUND** (the operator's own data, from the operator's own wearable cloud account, into the local store). It is **NOT a new egress class** and requires **no ADR-0001 amendment** — the outbound request carries only an OAuth bearer token + a date-range cursor (0 bytes of store content, 0 model-lane calls), and it introduces **no model step on the ingestion axis** (the exact inverse of ADR-0030, which *did* add an outbound operator-data→model egress and correctly owned it).
4. **Apple-Health watched-folder:** an operator Shortcut periodically drops an Apple Health export into a gitignored watched folder; the scheduled tick picks it up through the **existing, byte-unchanged `healthkit` adapter**. Automated *placement*, not a new adapter.
5. **Top falsification probes (mock/fixture, $0):** (functional) fixture token + fixture API response → correct readings land, and a re-run appends **0** duplicates; (privacy) a network-seam wire-scan of the fetch path shows **0 store-content bytes outbound, 0 model-lane calls, only the vendor host**.

> **Post-Tier-2 hardening (2026-07-13, as-built).** Four hardenings landed after the whole-change review, all fixture-tested at $0: (a) **per-source landing isolation** — `pull.main` lands each source in its own `scheduler.run({tag: path})` try/except, so a malformed watched export (a partial Shortcut write) is skipped loud and can neither crash the tick nor block already-fetched data (QA M1); (b) **3xx fail-closed on the authenticated fetch seam** — `_http` refuses to follow any redirect and raises, closing a cross-host `Authorization: Bearer` leak the default urllib opener allows on the LIVE run (Security SEC-01); (c) **loud non-fatal rotation-write diagnostic** — a failed keychain write-back of a rotated refresh token is surfaced, not swallowed (Security SEC-02); (d) the fetchable-source set is **derived from `_MANIFESTS` under a congruence guard**, closing a silent wired-but-never-fetched drift trap (Architect F2).

---

## 1. Grounded current state — what EXISTS vs what is NEW

Everything below is read from the live tree, not the brief.

### The frozen ingest/land seam (EXISTS — file-based, idempotent, schedulable)

| Contract | Where | Shape |
|---|---|---|
| Shared land routine | `ingest.run(adapter, export_file, root)` [VERIFIED `scripts/ingest/ingest.py:39`] | Iterates `adapter.read_readings(export_file)` and calls `store.append` once per reading [VERIFIED `ingest.py:57-58, 36`]. Idempotent; writes only to the store; invokes no model step. |
| Adapter protocol | `Adapter` = `source_tag()` + `read_readings(export_file) -> Iterable[dict]` [VERIFIED `scripts/ingest/adapter.py:23-44`] | Frozen named surface. Carries **no** dedupe/store logic — "an adapter cannot fork the dedupe key" [VERIFIED `adapter.py:5-11`]. `READING_FIELDS = keying.LINE_FIELDS` [VERIFIED `adapter.py:20`]. |
| Reading shape / dedup key | `LINE_FIELDS = (item, timepoint, source, value)`; `DEDUPE_FIELDS` = the same minus `value` [VERIFIED `scripts/store/keying.py:11,15-16`] | The single dedupe identity is `(item, timepoint, source)` [VERIFIED `keying.py:19-32`]. |
| Idempotent sink | `store.append(item, reading, root)` [VERIFIED `scripts/store/store.py:134-162`] | Re-appending a reading whose `(item, timepoint, source)` is already stored is a **no-op** [VERIFIED `store.py:160-161`]; atomic per-file rewrite [VERIFIED `store.py:75-110`]. |
| Unattended scheduler | `scheduler.run(exports, root)` [VERIFIED `scripts/ingest/scheduler.py:71`] | Data-driven discovery of the wired adapter set from `adapters/` [VERIFIED `scheduler.py:42-68`]; runs the UNCHANGED `ingest.run` once per wired adapter that has an entry in `exports` (`exports[source_tag] = path`) [VERIFIED `scheduler.py:92-95`]; a source with no export is skipped [VERIFIED `scheduler.py:93-94`]; makes **0 outbound network calls** today [VERIFIED `scheduler.py:11-12`]. A new adapter joins the wired set with **0 edits** to this file [VERIFIED `scheduler.py:16-20`]. |
| Existing FILE-reading adapters | | `oura.py` reads a JSON array of `{metric, day, average}` [VERIFIED `adapters/oura.py:28-36`]; `garmin.py` reads `{summaryType, calendarDate, value|valueInMillis}` [VERIFIED `adapters/garmin.py:32-45`]; `whoop.py` reads **noop's on-device SQLite** `dailyMetric` table (NOT a cloud API) [VERIFIED `adapters/whoop.py:67-107`]; `healthkit.py` reads an Apple export `.zip`/`.xml`, streaming to a daily MEAN per `(item, day)` [VERIFIED `adapters/healthkit.py:99-168`]. |
| Credential pattern | `key_source.resolve()` — env var then keychain, at call time [VERIFIED `scripts/model/key_source.py:65-91`] | Reads `security find-generic-password -w -s a-plus-maxing-api-key` [VERIFIED `key_source.py:44-62,30`]; writes with `add-generic-password -U -A` [VERIFIED `key_source.py:103-157`]; **never** a tracked file; a `keychain_runner` seam makes it test-mockable [VERIFIED `key_source.py:65-69`]. |
| OAuth-token-at-rest precedent | `auth_isolation._oauth_keychain_reader` [VERIFIED `scripts/runner/auth_isolation.py:65-84`] | ADR-0039 already established a **second** keychain item `a-plus-maxing-oauth-token` read via the identical `security find-generic-password -w -s <service>` shape, with an injectable `keychain_reader` seam [VERIFIED `auth_isolation.py:50,87-99`]. This is the exact pattern the per-source OAuth tokens reuse. |
| Operator-gated activation | `schedule/activate.py` — `enable/disable/status` [VERIFIED `scripts/runner/schedule/activate.py:307-345,255-266`] | launchd-primary / cron-fallback, **disabled by default**, importing arms nothing, an anti-implicit-activation guard forbids any build/provision step arming it [VERIFIED `activate.py:1-31,269-304`]. |
| Store concurrency lock | `store_lock.cadence_lock(root)` [VERIFIED `scripts/runner/store_lock.py:33-61`] | Advisory `flock(LOCK_EX\|LOCK_NB)` over the read→regenerate→promote critical section; busy tick defers, crash releases [VERIFIED `store_lock.py:1-21`]. |

### What is NEW

Exactly one new capability class: **an OAuth network fetch that produces the staged export a file-reading adapter consumes.** Everything downstream of the staged file — the adapter parse, `ingest.run`, the dedup, `store.append`, the scheduler's wired-set discovery — is the existing, frozen machinery. The scheduler is unattended and idempotent **today**; it has simply never had a network producer feeding its `exports` map, and (separately) it has **no OS-timer host wired yet** — `scheduler.run` has no `__main__`/launchd entry (the ADR-0039 `cadence_runner` schedules the *plan-evolution loop*, not ingestion). Both gaps are additive; neither is an edit to the frozen seam.

---

## 2. The API-pull adapter contract (fetch → land)

### The contract

A file-reading adapter answers "given a local export file, yield store readings." An API-pull source answers "given credentials and a delta boundary, produce that local export file." The design keeps those two responsibilities in **separate** layers so the frozen `Adapter` protocol and `ingest.run` do not change:

```
fetch(source, credentials, since) -> staged_path          # NEW shared layer (network lives here)
    authenticate: refresh_token (keychain) -> access_token (source token endpoint)
    GET the source's read endpoint(s) for readings with timepoint > since
    normalize the response -> a gitignored staged file in the file-reading adapter's shape
ingest.run(adapter, staged_path, root)                     # UNCHANGED  [ingest.py:39]
    adapter.read_readings(staged_path) -> readings          # a PURE file parser (no network)
    store.append(...)                                       # UNCHANGED  (item,timepoint,source) dedup
```

**Interface the new layer must expose (testable without implementation):**

- `oauth.access_token(source, *, keychain_reader=..., http=...) -> str` — mints a short-lived access token from the per-source refresh token; both the keychain read and the HTTP POST are **injectable seams** (fake in tests, exactly as `auth_isolation.build_subscription_env(..., keychain_reader=...)` and `key_source.resolve(keychain_runner=...)` are).
- `fetch(source, *, since, staged_dir, keychain_reader=..., http=...) -> Path` — pulls the delta window and writes the normalized staged export; returns its path. **Precondition:** a valid per-source refresh token in the keychain. **Postcondition:** a staged file parseable by `source`'s wired adapter, OR a raised error and **0** bytes written (fail-closed; §3). **Error cases:** missing/expired/revoked token → raise (no partial file); network/HTTP-error → raise; malformed response → raise. The staged file is gitignored and never committed.
- `pull.main(argv=None) -> int` — the orchestration entry (`python -m scripts.ingest.pull`): for each wired API-pull source, `fetch(...)` → `exports[source_tag] = staged_path`; merge the watched-folder scan (§6); call the **UNCHANGED** `scheduler.run(exports, root)`. This is a **new caller of** `scheduler.run`, not an edit to it.

> **[AMENDED 2026-07-13 — Tier-2 Architect F3]:** the as-built injectable credential seams are named **`credential_reader` / `credential_writer`** (macOS keychain underneath), NOT `keychain_reader`/`keychain_runner` as the illustrative signatures above show — a `keychain_*` / `*key*` parameter name inside `scripts/ingest/` false-positives the pre-existing Risk-N3 `def .*key` dedupe-fork scan (`tests/ingest/test_ingest.py`). The seam *contract* (an injectable reader/writer over the OS keychain) is unchanged; only the kwarg name differs. (The scan itself is over-broad; refining it is a separate beaded change.)

### Two options considered; one chosen

**Option A — fetch stages a file; the adapter stays a pure file-parser (CHOSEN).**
The network layer produces a staged export in the adapter's existing input shape; `ingest.run(adapter, staged_file)` lands it verbatim. Oura/Garmin already parse JSON arrays [VERIFIED `oura.py:29`, `garmin.py:33`], so a normalized staged JSON array reuses their adapters directly.

> **[AMENDED 2026-07-13 — Tier-2 Architect F1]:** as built, the fetch layer normalizes **all** sources into one uniform `{item, timepoint, value}` staged shape, and each source gets a **dedicated** `*_cloud` adapter (`whoop_cloud`/`oura_cloud`/`garmin_cloud`/`google_health_cloud`). The legacy file-drop `oura.py`/`garmin.py` (and the noop-SQLite `whoop.py`) are **retired as `UNWIRED`** — kept only as a manual-CLI/offline fallback, NOT reused as the wired source. Reason: one uniform staged shape + one cloud-adapter pattern; leaving a legacy adapter wired alongside its `*_cloud` twin would dedupe-collide on `(item, day, source)`. The frozen seam, the `(item, timepoint, source)` dedup, and one-wired-adapter-per-source are all intact (Tier-2-verified). There is direct precedent for adapter-local staging: `healthkit.read_readings` already stages a zip member to a temp path before its own read [VERIFIED `healthkit.py:116-126`], and `dna.land` stages into a gitignored dropzone [VERIFIED `dna.py:92-97`].
- *Why:* it edits **zero** frozen files (`ingest.run`/`scheduler.run`/`store.append`/`Adapter` unchanged), keeps the adapter network-free (fixture-testable with a file, no HTTP), and confines the network to one shared, seam-injected layer. The `(item, timepoint, source)` dedup is inherited, so idempotency holds across the fetch boundary for free.

**Option B — the adapter gains a `fetch(credentials, since)` mode and emits readings directly.**
- *Rejected:* coupling network + parse in the adapter forces `ingest.run`/`scheduler.run` to learn a "fetch mode" branch — i.e. it **edits the shared routine**, violating ADR-0003's 0-shared-routine-edit invariant [VERIFIED `ADR-0003` Falsification #2] and the `Adapter`-carries-no-IO-logic contract [VERIFIED `adapter.py:5-11`]. It also makes the adapter un-testable without a network mock.

(A third shape — a new API-scheduler that drives `fetch→readings→store.append` itself, bypassing `ingest.run` — is rejected outright: it forks the single land path and re-implements the dedup the store owns.)

**Breaks if:**
- the source's live API JSON shape diverges from the staged shape the file-reading adapter expects → mitigated by the fetch layer **normalizing** into the adapter's shape (implementer discretion), or a 0-shared-routine-edit tweak to the adapter's *own* field map (the adapter is not frozen; ADR-0003 AC-6's format-rename proof shows this stays inside the adapter [VERIFIED `tests/ingest/test_adapters.py:939-977`]).
- a source returns readings at a **finer timepoint granularity** than the store's `(item, timepoint)` key (e.g. intraday HR) → the adapter rolls up to the stored key, exactly as `healthkit` takes a daily mean per `(item, day)` [VERIFIED `healthkit.py:157-168`]. Which granularity each source lands at is a per-source mapping decision (§5), not a seam change.
- **Robustness guarantee (not a break):** because dedup is on `(item, timepoint, source)` and `value` is excluded from the key [VERIFIED `keying.py:15-16`], a fetch that over-fetches (a stale/coarse `since`, an overlapping window, a full re-pull) lands **0** duplicates. Correctness therefore does **not** depend on `since` precision — `since` is a bandwidth optimization, and the store key is the idempotency guarantee. This is falsification probe §8.5.

---

## 3. OAuth + credential model

**Storage (reuse, do not invent).** Per source, one OS-keychain item holds the OAuth **refresh token** (plus client-id/secret if the vendor requires them at refresh time): `a-plus-maxing-whoop-oauth`, `a-plus-maxing-oura-oauth`, `a-plus-maxing-garmin-oauth`, `a-plus-maxing-google-health-oauth`. Read at call time with `security find-generic-password -w -s <service>` — the exact shape `key_source._keychain_runner` [VERIFIED `key_source.py:44-62`] and `auth_isolation._oauth_keychain_reader` [VERIFIED `auth_isolation.py:65-84`] already use — via an injectable **`credential_reader`** seam (named `keychain_reader` in this note's original draft — see the §2 F3 amendment) so tests touch no real keychain. **Never** the repo, the store, or any tracked file (NFR-3: the repo is PUBLIC). This is the same at-rest-secret posture ADR-0039 accepted for `CLAUDE_CODE_OAUTH_TOKEN` [VERIFIED `ADR-0039` Consequences-Negative-5] — see the §10 operator ack.

**One-time operator flow (the LIVE step, operator-gated):**
1. Register a developer app per vendor → obtain client-id/secret.
2. Run the OAuth authorize + consent once (browser) → receive an auth code.
3. Exchange the code for a **refresh token**.
4. Store the refresh token in the per-source keychain item (a `security add-generic-password -U` command, mirroring `keychain-setup.md` Option B [VERIFIED `scripts/model/keychain-setup.md:48-58`], or an in-app "connect <source>" affordance that calls a `store`-style writer [VERIFIED `key_source.py:135-157`]).

**Runtime refresh.** At fetch time the layer POSTs the refresh token to the source's token endpoint → a short-lived **access token** → used as `Authorization: Bearer` on the read GET. Some vendors **rotate** the refresh token on each use (Google and Whoop do); on a rotated token the layer writes the new refresh token back to the keychain (`add-generic-password -U`, the same update path `key_source.store` uses [VERIFIED `key_source.py:121-122`]). Access tokens are held in-process only, never persisted.

**Fail-closed (a hard contract).** A missing / expired / revoked refresh token, or a token-endpoint/read-endpoint error, **raises** (a fail-loud error mirroring `OAuthTokenUnavailableError` [VERIFIED `auth_isolation.py:55-62,113-117`]) and lands **0** readings — no partial file, no garbage store write. The operator re-authorizes (repeat the one-time flow). This is falsification probe §8.2.

---

## 4. ADR-0001 privacy framing — the ruling

This is the load-bearing decision. I rule, per the Architect profile, rather than defer.

**The boundary, precisely.** ADR-0001's crown jewel forbids operator **data** (labs, readings, DNA, health history) **EGRESSING** to a model/training party — "route only plan reasoning to the model over summaries rather than raw PII," and, on the ingestion axis, "the import/ingestion routine … model-independently, sending zero operator PII to any model" [VERIFIED `ADR-0001:24`]. Every amendment to date (ADR-0016 conversation, ADR-0030 file-extraction, ADR-0032 variant queries, ADR-0035 med names, ADR-0037 tailoring, ADR-0042 identity-stripped record) added a **named OUTBOUND egress class** where operator data leaves *to the no-train model* [VERIFIED `ADR-0001` Related Decisions rows]. ADR-0039 established that a scheduled ingestion-adjacent runner may make an outbound call, but bounded its **only** metered egress to the de-id-IN call and disqualified any path that ships raw local store content to a non-local runtime [VERIFIED `ADR-0039:33,111-112`].

**RULING: the API pull is NOT a new egress class and requires NO ADR-0001 amendment.** Four grounds:

1. **Direction.** Operator data flows **inbound** — from the operator's own wearable cloud account into the local store. The crown jewel governs operator data flowing **outbound** to a model. These are opposite directions across the boundary.
2. **Recipient.** The only outbound recipient is the **wearable vendor that already originates and holds the operator's data** (the operator's own account — they wear the device and sync it to that cloud). The pull discloses **no** operator data to any party that does not already have it; it **authenticates** to *retrieve* the operator's data from where it already lives. No new recipient of operator data is created. (Contrast ADR-0030, which made the no-train **model** a *new* recipient of whole operator files — a genuine boundary extension it owned as Negative [VERIFIED `ADR-0030:43`].)
3. **Content.** The outbound request carries only an OAuth bearer **token** (a credential authorizing the read, not operator health data) + request **parameters** (a date-range / `since` cursor). It carries **0 bytes of store content** and makes **0 model-lane calls**. ADR-0001's own confirmation criterion — "during an ingestion run, 0 PII bytes **from the store** leave the local machine" [VERIFIED `ADR-0001:111`] — is satisfied *as literally written*: the store is the **sink** of this flow, not its source; nothing leaves the store.
4. **No model step.** Unlike ADR-0030, the API pull introduces **no model call on the ingestion axis at all**. The ingestion→store write path stays model-independent — so ADR-0001's ingestion-model-independence clause is **preserved, not scoped**. The API pull is *more* aligned with ADR-0001 than ADR-0030 is.

**Framing:** the API pull is the mirror image of ADR-0030. ADR-0030 = **outbound** operator-data→model egress → owned as a new class + four amendments. API pull = **inbound** operator-data←vendor fetch → **no** new class, **no** amendment. There is no new counting frame on the no-train-model-egress axis, because the fetch never touches the model lane.

**Breaks if:** a fetched payload is ever forwarded to the no-train model lane **un-de-identified** — e.g. wiring fetched readings into a specialist dispatch without passing the existing store→model boundary (`router.summarize` / the ADR-0042 identity-stripped record). **It is not:** fetched readings land in the local store via the **unchanged** `store.append`, exactly like a file import, and every downstream model use is governed by the same, unchanged store→model de-id boundary that already governs every stored reading. The API pull touches only the **write** side (ingestion), which was already model-independent and stays so. Mechanically proven by falsification probe §8.3 (the inbound-only wire-scan).

**One honest residual (surfaced, not hidden):** the design adds a **new outbound network dependency** and a **new authenticated relationship** to four external vendors, plus four long-lived at-rest OAuth secrets. That is an ADR-0005 at-rest-secret surface (identical in kind to ADR-0039's `CLAUDE_CODE_OAUTH_TOKEN`), and a new-vendor-relationship the operator should explicitly acknowledge — §10.1. It is **not** an ADR-0001 crown-jewel egress, for the four grounds above.

---

## 5. Per-source specifics

The auth **shape** (OAuth 2.0 authorize + token + read endpoints; bearer access token; refresh token) and the reading-type→store-item mapping are contract-level below. **Exact endpoint paths and scope strings are marked `[VERIFY-AT-BUILD]`** — per the Architect profile I do not fabricate external API contracts; the SE fills a per-source manifest against each vendor's live developer docs before wiring that source. The Google Health facts are as supplied and dated in the brief (accurate as of 2026-07); still `[VERIFY-AT-BUILD]` for the exact data-type/scope tokens.

| Source | Auth | Read surface | Maps to store items | Notes |
|---|---|---|---|---|
| **Whoop** | OAuth 2.0, refresh-token; refresh rotates | recovery / sleep / cycles / workout collections `[VERIFY-AT-BUILD]` | `recovery, hrv, rhr, spo2, sleep-efficiency, resp-rate, strain` (strain on WHOOP's **0–21** scale, unscaled — the existing adapter's invariant [VERIFIED `whoop.py:37-46`]) | Cloud API ≠ the existing **noop-SQLite** adapter. Needs a **new** file-reading adapter for the staged cloud JSON; see §9 + §10.3 on which one owns the `"whoop"` source tag. |
| **Oura** | OAuth 2.0, refresh-token | Oura API v2 daily collections + heartrate `[VERIFY-AT-BUILD]` | `hrv, rhr, sleep, readiness, activity` | Existing `oura.py` already parses a JSON array [VERIFIED `oura.py:29`]. *[AMENDED 2026-07-13: built as a dedicated `oura_cloud.py` on the uniform `{item, timepoint, value}` staged shape; the legacy `oura.py` is retired `UNWIRED` — §2/§9 F1.]* |
| **Garmin** | **FORK — VERIFY.** Garmin's Health API has historically used **OAuth 1.0a** (per-request HMAC-signed, long-lived token+secret), NOT OAuth 2.0 refresh-tokens | Garmin Health/Connect summaries `[VERIFY-AT-BUILD]` | `hrv, rhr, sleep, activity, stress` | If still OAuth 1.0a, the shared layer needs a Garmin-specific auth **strategy** (see §10.2). Existing `garmin.py` parses a JSON array [VERIFIED `garmin.py:33`]. *[AMENDED 2026-07-13: built as a dedicated `garmin_cloud.py`; the legacy `garmin.py` is retired `UNWIRED` — §2/§9 F1.]* The *auth* is the genuine §10.2 fork (OAuth 1.0a as built). |
| **Google Health** | **Google OAuth 2.0**, refresh-token | `health.googleapis.com/v4/` — four uniform read methods (list, reconcile, rollUp, dailyRollUp), ~31 data types `[VERIFY-AT-BUILD exact type/scope tokens]` | `sleep, hrv, rhr, heart-rate, activity, spo2` | Covers **Fitbit Air + Pixel Watch + all Fitbit devices**. **Do NOT** build on the legacy Fitbit Web API (sunsets **Sep 2026**) — greenfield on the new API, no migration. Standard OAuth 2.0 fits the shared layer cleanly. New file-reading adapter for the staged response. |

Item names follow the `biomarker_meta` registry convention already used by the wired adapters (`hrv`/`rhr` shared across sources, distinct only by `source` [VERIFIED `whoop.py:34-46`, `healthkit.py:48-53`]). A reading from two sources at the same `(item, day)` **both persist** — `source` is in the dedupe key [VERIFIED `keying.py:15-16`; `tests/ingest/test_adapters.py:1034-1060`].

---

## 6. Apple-Health watched-folder

Apple exposes **no** cloud REST API for HealthKit (it is on-device), so Apple is **not** an API-pull source. The mechanical path is automated **placement**:

- An operator **Shortcut** (Shortcuts app, on a personal-automation schedule) exports the Apple Health data and writes the export file into a **gitignored watched folder** on the local machine (e.g. `vault/inbox/healthkit/`, or a configured path — a folder an iCloud-Drive-synced Shortcut can write to).
- The scheduled tick's watched-folder scan (part of `pull.main`, §2/§7) picks up the newest export and adds `exports["healthkit"] = <that path>`; `scheduler.run` → the **existing, byte-unchanged** `healthkit` adapter ingests it (it already accepts `.zip` or `.xml` and streams to a daily mean [VERIFIED `healthkit.py:99-168`]). **Zero new adapter code.**

**Watched-folder contract:**
- *Location:* a single gitignored directory, configured (not operator-hardcoded in a tracked file — the multi-user rule).
- *Pick-up trigger:* the scheduled tick (same cadence as the API pulls). The scan selects the newest `export.zip`/`export.xml` in the folder.
- *Idempotency:* Apple exports are full cumulative dumps; the `healthkit` daily-mean → `(item, day, "healthkit")` dedup means re-ingesting the same or an overlapping export appends **0** new lines. Re-processing an already-seen file is a safe no-op (probe §8.6).

**Breaks if:** the Shortcut cannot run **headless/periodically** (iOS Shortcuts automations can require device-unlock/interaction). This is an operator-environment constraint to verify (§10.3 item 3); the fallback is a manual periodic export drop into the same folder — still mechanical *placement*, still zero adapter change.

---

## 7. Scheduling

**Reuse `scheduler.run` unchanged.** The API-pull adapters register into its data-driven wired set for free — dropping a conformant adapter module into `adapters/` joins the wired set with **0** scheduler edits [VERIFIED `scheduler.py:16-20,42-68`]. The delta-since-last-run + idempotent-no-new-re-run behaviour is inherited from the store dedup [VERIFIED `scheduler.py:6-12`]. **No new scheduler, no new dedup, no new store key.**

**The genuinely-new control step** is `pull.main` (§2): build the `exports` map (fetch each API source's delta to a staged file + scan the watched folder) then call the unchanged `scheduler.run(exports, root)`. This is a **new caller**, not an edit.

**The OS-timer host — reuse the ADR-0039 *activation mechanism*, precisely scoped.** There is no OS-timer host for ingestion today (`scheduler.run` has no `__main__`/launchd entry; the ADR-0039 `cadence_runner` schedules the *plan loop*, a different job). Reuse the **`schedule/activate.py` pattern** — launchd-primary / cron-fallback, **disabled by default**, `enable/disable/status`, the anti-implicit-activation guard, operator-agnostic placeholder-only templates [VERIFIED `activate.py:1-31,109-131,269-345`] — under a **distinct label** (e.g. `com.aplusmaxing.tracker-pull`) pointing at `python -m scripts.ingest.pull`. This honors "mechanical once armed" **and** the PF-S63-02 operator-gated-activation posture: building the runner arms nothing; the operator runs `enable` once. (This is the ADR-0039 disabled-by-default precedent [VERIFIED `ADR-0039:27,49`].)

**Store concurrency:** the tracker-pull tick does a read-modify-write on the same gitignored store the server and the plan-loop runner touch. It should acquire an advisory lock over its critical section — reuse the `store_lock.cadence_lock` flock pattern [VERIFIED `store_lock.py:33-61`] (ADR-0039 OQ-7's exact concern, already solved). Whether tracker-pull and the plan-loop cadence share one lock file or use sibling locks is a spec/SE detail.

**Cost note (a positive vs the ADR-0039 pattern):** wearable developer APIs are free within rate limits — the API pull adds **no recurring metered spend** (contrast ADR-0039, which arms recurring de-id spend [VERIFIED `ADR-0039:52`]). The operator-gated LIVE step is gated on the one-time OAuth setup + the at-rest-secret ack, **not** on spend.

---

## 8. Falsification probes (all mock/fixture, $0 live spend)

Modeled on the existing `tests/ingest/` style (tmp store root fixture; fake seams; the `_baseline_ref`/`_numstat_rows` 0-edit gate [VERIFIED `tests/ingest/test_adapters.py:46-97,519-536`]).

1. **Fetch→land correctness + idempotency (top functional probe).** Fake keychain seam (returns a fixture refresh token) + fake HTTP seam (returns a fixture API response) → `fetch` stages the normalized export → `ingest.run(adapter, staged)` lands the expected `(item, timepoint, source, value)` readings with correct per-stream values; a **second** identical run appends **0** new lines. (Extends `test_whoop_rerun_appends_zero_duplicates` across the fetch boundary.)
2. **Fail-closed on missing/expired token.** Fake keychain seam returns `None` (or fake HTTP returns 401) → `fetch` raises → the store is **unchanged** (0 partial/garbage writes). (Analog of the fail-loud-on-bad-file tests [VERIFIED `test_adapters.py:192-207`].)
3. **Crown-jewel inbound-only wire-scan (top privacy probe).** Run the fetch path under a recording network seam → assert: (a) **0** bytes of store content in any outbound request body/header; (b) **0** calls to the no-train model lane; (c) the only outbound host is the source's own API host; (d) the outbound payload is only the OAuth token + date-range params. Mechanizes the §4 ruling. (Mirrors ADR-0039's non-egress wire-scan [VERIFIED `ADR-0039:111-112`], inverted: here there is no de-id call at all.)
4. **0-frozen-edit proof.** `git diff --numstat <baseline> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/ingest/scheduler.py scripts/store/store.py scripts/store/keying.py` == `[]` after the build — extends the existing ADR-0003 gate to also cover `scheduler.py` + the frozen store files. Negative control (a one-line probe edit reds it) as in `test_garmin_zero_edit_gate_is_falsifiable` [VERIFIED `test_adapters.py:539-565`].
5. **Delta-since is an optimization, not a correctness dependency.** Fetch a **wider** window than needed (overlapping already-stored readings) → assert **0** duplicates land. Proves idempotency rests on the store key, not on `since` precision.
6. **Apple watched-folder pickup idempotency.** Drop a fixture export into the watched dir → one tick ingests it via the unchanged `healthkit` adapter → a second tick over the same/overlapping export appends **0** new lines.

---

## 9. Frozen-spine, extend-not-rebuild, scope

**Byte-unchanged (the new code CALLS these; a numstat gate proves it — §8.4):**
- the `<always-frozen>` six: `scripts/store/store.py`, `scripts/store/keying.py`, `scripts/plan/pipeline.py`, `scripts/plan/adjudicate.py`, `scripts/plan/adjust.py`, `scripts/plan/router.py` [all VERIFIED present];
- `scripts/ingest/ingest.py` (`ingest.run`), `scripts/ingest/scheduler.py` (`scheduler.run`), `scripts/ingest/adapter.py` (the `Adapter` protocol);
- the plan engine (untouched). **No new store key.**

**New / extended files:**
- a shared OAuth/fetch layer — e.g. `scripts/ingest/fetch/oauth.py` (refresh→access + keychain, seam-injected) + `scripts/ingest/fetch/pull.py` (per-source fetch + normalize) + `scripts/ingest/pull.py` (`main` = build `exports` → unchanged `scheduler.run`);
- **[AMENDED 2026-07-13 — Tier-2 Architect F1]** four new file-reading adapters, one per source — `whoop_cloud.py`, `oura_cloud.py`, `garmin_cloud.py`, `google_health_cloud.py` — each a pure `read_readings(file)` parser conforming to the frozen `Adapter` protocol, all consuming the uniform `{item, timepoint, value}` staged shape. *(Original draft: new whoop-cloud + google-health adapters, reusing `oura.py`/`garmin.py`. Superseded — the build normalized all sources to one staged shape, so oura/garmin got dedicated `*_cloud` adapters too.)*
- the legacy file-drop `oura.py`/`garmin.py` and the noop-SQLite `whoop.py` are **retired as `UNWIRED`** (kept as a manual-CLI/offline fallback), not reused as the wired source;
- the tracker-pull OS-timer activation — a new label + template reusing `schedule/activate.py`'s disabled-by-default pattern;
- the watched-folder scan feeding `exports["healthkit"]` (the `healthkit` adapter reused byte-unchanged);
- tests under `tests/ingest/`.

**Out of scope:**
- the **LIVE pull** — per-vendor dev-app registration + real OAuth consent + real refresh tokens (operator-gated; the build is fixture-tested). Note: vendor API pulls are $0-metered, so "spend" is not the gate — the one-time OAuth setup + the §10 acks are;
- the **daily-monitor** layer (ADR-0045);
- the **plan engine** and any change to the store→model de-id boundary (frozen).

---

## 10. Operator decisions to surface for sign-off

1. **Four new long-lived at-rest OAuth secrets + four authenticated-vendor relationships (ADR-0005 tension).** The design holds a per-source refresh token in the keychain — off the tracked tree, exactly like the existing API key and the ADR-0039 `CLAUDE_CODE_OAUTH_TOKEN`. You already sync these devices to these clouds, so the pull discloses **no new operator data** (the §4 ruling) — but registering this instance as an OAuth client to Whoop / Oura / Garmin / Google and holding four long-lived refresh tokens locally is a real new secret-surface + vendor relationship. **Not a blocker** (you chose these sources); an explicit ack, the sibling of the ADR-0039 token-at-rest sign-off.
2. **Garmin's auth model — the one genuine per-source fork.** Garmin's Health API has historically used **OAuth 1.0a** (per-request HMAC-signed, long-lived token+secret), not OAuth 2.0 refresh-tokens — materially different plumbing the shared OAuth-2.0 layer does not cover. Decision: the SE verifies Garmin's **current** offering (they may now offer OAuth 2.0 PKCE); if it is still OAuth 1.0a, accept a Garmin-specific auth **strategy** inside the shared layer (the layer abstracts "produce a valid `Authorization` for source X," OAuth2-refresh the default, OAuth1a-sign the Garmin case). A spec-stage decision, flagged so Garmin is not built against a fabricated OAuth2 contract.
3. **The scheduled-pull posture + the Apple Shortcut's headless-ability.** (a) I have assumed **disabled-by-default, operator-armed-once** scheduling (the ADR-0039 / PF-S63-02 pattern) — mechanical once armed, but not silently self-arming. Confirm you want the scheduled unattended pull (that authenticates to four vendors on a cadence) vs. an on-demand `python -m scripts.ingest.pull` you run by hand. (b) Confirm your Apple **Shortcut** can run on a headless schedule; if iOS requires device-interaction, the Apple path degrades to a manual periodic export drop into the watched folder (still mechanical placement, still zero adapter change).

*(In-body recommendation, not an operator question: the Whoop cloud-API adapter should **replace** the existing noop-SQLite `whoop.py` as the sole wired `"whoop"` source — two adapters both emitting `source="whoop"` would dedupe-collide on `(item, day, "whoop")`. Mark the noop-SQLite adapter `UNWIRED` [VERIFIED `scheduler.py:33-39`] or retire it; keep it only if you want the offline noop path as a fallback. SE/spec detail.)*
