# wiring-gate fixture app (§6.3 static substrate)

The minimal static fixture the §6.3 wiring gate (`scripts/wiring-gate.sh`) checks its STATIC
resolutions (res-1, res-2) against. No framework, no `npm install` — plain HTML + one JS file +
two JSON referents. It is the Phase-2 substrate §10 requires. The GOOD state here fully satisfies
res-1 AND res-2 for every row of the real auth manifest.

## What maps to what

The gate joins `designs/fixtures/auth-interaction-model/wiring-manifest.json` (25 interactive-element
rows, 7 screens — `screen/dashboard` declares 0) against this app.

| Manifest field | Fixture referent | Real project reads instead |
|---|---|---|
| `(screen, wireId)` | `data-oid` attribute on a rendered element | the rendered DOM |
| handler symbol | `data-handler` attribute → a function in `app.js` | the component's bound handler |
| `endpoint` (`METHOD /path`) | `app/routes.json` (served route table) | the app's REAL route table |
| `reads`/`writes` (`entity.field`) | `app/schema.json` (entity → fields) | the IMPLEMENTED data model (migrations / ORM / OpenAPI) |

`routes.json` and `schema.json` are STAND-INS. In a real project res-2 reads the app's actual served
route table and its implemented data model (§6.3-res-2: "NEVER §8's derived draft"). The fixture
collapses both into two hand-authored JSON files so the gate is hermetic and needs no running server
or migration engine.

## The `data-oid` convention (format-v0)

`data-oid = "<bare-screen>/<wireId>"`, where `<bare-screen>` is the manifest `screen` value with its
`screen/` role prefix stripped. So `(screen/login, email)` → `data-oid="login/email"`. This is the
only reading consistent with the §6.3-res-1 shell example, which renders the pseudo-screen
`screen/_shell` as `data-oid="_shell/<wireId>"` (prefix stripped). The FULL `(screen, wireId)` join
key still crosses the seam [NEW-4]; the prefix is dropped only in the attribute spelling.

## The handler convention

Every interactive element carries `data-handler="<symbol>"` naming a function defined in `app.js`.
res-1 requires the symbol to exist with a NON-EMPTY body. A non-empty no-op passes (T-22 — res-1 is
a STATIC check; only res-3/E2E proves the handler actually does anything). res-1 REJECTS: a missing
`data-handler`, a link whose only action is `href="#"`, an undefined symbol, or an empty body
(`function f(){}` / `() => {}`). res-1 reports `STATIC-PASS`, never "wired" [QA S1].

## HTML parsing boundary (honest limit)

The gate scans this fixture's HTML with a per-tag regex (`<…>`-delimited), after stripping
`<!-- … -->` comment regions so a commented-out element cannot satisfy res-1. The authoring rule
the regex relies on: each interactive element is a single opening tag with no `>` inside an
attribute value. That is acceptable for THIS fixture format. A real-project adapter would use a DOM
parser over the rendered output — that adapter is future work, not built here.

## Out of scope here

- **res-3** (executed E2E + mutation proofs): the NEXT increment, not this gate.
- **§6.4 seam gate** (the reverse direction: a `data-oid` in the app with no manifest row —
  "built-not-designed"). This gate only checks manifest → app (every designed row is built + served).
  Extra `data-oid`s are the seam gate's territory.
- **§6.1 pen-lint** runs upstream as a separate gate; the wiring gate does not re-run it.
