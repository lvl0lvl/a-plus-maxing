# seam-gate fixture — a real hydrating app for the §6.4 post-hydration crawl

The static `wiring-gate/` fixture (plain HTML + one vanilla `app.js`) **cannot exercise a single
§6.4 obligation** (no framework, no hydration, no portals, no repeated instances, no interceptable
writes — harness-substrate-memo §7). This fixture is the runtime substrate the §6.4 seam gate
(`scripts/seam-gate.sh`) and its `pen-harness` crawl require: a minimal but **real hydrating React
app** served over localhost, driven by headless Chromium.

## Honest test boundary (T-25 — read this first)

Phase-2 proves the harness **mechanisms** (post-hydration crawl, portal-root union, statechart state
induction, `data-oiid` instance addressing, `_shell` shellStates scoping, duplicate-identity
detection, the PA-2 production-build assertion) against **this controlled fixture**. It does **not**
prove them against a real React/Next application — that is Phase-5 (T-25). The engine choice
(Playwright driving headless Chromium — the same engine a Phase-5 consumer ships on) is what makes
Phase-5 a **fixture swap, not a substrate change**. The boundary is a *scope* line, not a capability
gap: everything the harness does here it does with a real browser engine against a real hydrated DOM.

The fixture renders **client-side only** (CSR): the served `index.html` carries an empty `#root` and
**zero `data-oid` attributes**. Every `data-oid`, every portal node, and every induced state exists
only *after* the React engine runs — so a byte-scan of the served HTML finds nothing, and the crawl
must run the real engine to see anything (memo O1 in its strongest form).

## One-time setup (network at install time only; the crawl itself is localhost-only)

```
# the fixture app (React + Vite); node_modules and dist are NOT committed
cd frameworks/rigor/toolkit/tests/fixtures/seam-gate/app && npm ci && npm run build

# the quarantined harness runtime (Playwright); node_modules is NOT committed
cd frameworks/rigor/toolkit/harness && npm ci && npx playwright install chromium
```

Committed: `package.json` + `package-lock.json` for both (deterministic installs). Not committed:
`node_modules/`, `app/dist/` (a build artifact — `test-seam-gate.sh` rebuilds it if absent). Once
installed, no network is needed at test time; the crawl talks only to `127.0.0.1`.

## Layout

| Path | Role |
|---|---|
| `app/` | the React fixture: `src/App.jsx` (CSR), `serve.mjs` (hermetic static server + in-memory `/api`), `vite.config.js` (emits `dist/build-config.json` for the PA-2 assertion) |
| `app/routes.json`, `app/schema.json` | res-3 (task #45) substrate: served-route table + implemented data model (single-field `note` entity). `serve.mjs` is schema-bounded (a non-schema field is DISCARDED) — that is what makes `note` UNPROVABLE — and carries a `POST /api/__reset` test hook the harness calls before each proof run. |
| `design/interaction-model/` | the export set the gate consumes: `wiring-manifest.json`, `machine.review.json`, `index.md`, `config.json`, `retired-wireids.txt`, `exceptions.json`, `export.digest`, and `e2e.review.json` (the res-3 E2E definitions the harness drives — NOT in the §5 digest set, so it is test substrate, not a design export). `exceptions.json` carries the res-3 UNPROVABLE sign-off for `detail/status-note`, keyed to the design-digest. |
| `wiring-results.json` | the §6.6 wave register (all rows in a closed wave 1; an open wave 2 for the PENDING-variant proof) |

The `export.digest` reuses the committed auth `.pen` (`designs/fixtures/safety-auth-annotated.pen`)
as its pinned substrate — only so the §6.2 export-integrity **hard dependency** has a real, in-repo,
non-symlink `.pen` to hash. The fixture is **not** extracted from that `.pen`; it is hand-authored.

## What each element exercises (every element earns its place)

| manifest element | §6.4 obligation | res-3 (task #45) obligation |
|---|---|---|
| `_shell/home` (shellStates `*`) | shell chrome present in every screen-state | N/A (navigate, no data-effect) |
| `_shell/back` (shellStates `screen/detail`) | contextually-hidden chrome: present on detail, absent on list, must NOT false-fail | N/A (navigate) |
| `list/search` | — | `ephemeral:true` + empty `writes` → **NA-EPHEMERAL**; localEffect = filters the list in place; proof (a) RED-capable |
| `list/incident-row` | repeated-instance list; each row carries a distinct `data-oiid` (O4; the sanctioned multiplicity the duplicate check must NOT flag) | **instance-aware** (drive instance k → highlight row k); `?collapse=1` collapses to row 0 → e2ePass RED; NA-EPHEMERAL |
| `list/open-filters` | opens the filters modal | NA-EPHEMERAL (localEffect = opens the modal) |
| `list/apply-filter` | lives INSIDE the portal modal (portaled to `document.body`) — observable only AFTER OPEN_FILTERS is induced (O2 + O3) | NA-EPHEMERAL (localEffect = closes the modal) |
| `list/open-detail` | transitions to the detail screen-state | N/A (navigate) |
| `detail/refresh` | induces the error child-state (O3 tab/error/empty induction) | N/A (toggle, no writes) |
| `detail/retry` | rendered only in the error state — observable only AFTER REFRESH is induced | N/A (toggle, no writes) |
| `detail/status-note` | — | persists single-field `note.text` via `POST /api/note` → placement **UNPROVABLE** (no observable sibling); covered by an `exceptions.json` sign-off |

## Mutation surface (rebuild-free F-007 negatives)

`App.jsx` reads the URL query so the F-007 suite drives each guard RED without a rebuild:

- `?omit=<oid>[,<oid>]` — omit designed elements → the gate's **missing** guard.
- `?extra=1` — render an undesigned `data-oid` (`list/ghost`) → **built-not-designed**.
- `?dup=<oid>` — render `<oid>` twice with no distinguishing `data-oiid` → **duplicate identity** (BH7).
- `?warn=1` — render an interactive-role node with no `data-oid` → the T-23 **WARN** list (non-gating).
- `?collapse=1` — `list/incident-row` highlight always lands on row 0 (row-N-affects-row-0) → the res-3
  instance-aware placement assertion goes RED when driving instance k>0 (task #45 instance-collapse).

Export/build mutations (unreachable machine state, corrupt digest, PEN-CHANGED, zero-row manifest,
non-production or data-*-stripping build config) are made on copies in the test's temp dir. res-3
schema mutations (a temp multi-field `note` for the placement-RED path, or a mismatched sign-off
digest for the self-voiding path) are likewise made on temp copies.
