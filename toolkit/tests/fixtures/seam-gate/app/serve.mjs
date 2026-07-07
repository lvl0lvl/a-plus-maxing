// serve.mjs — hermetic static server for the built fixture (node builtins only).
//
// Serves the production build (dist/) with an SPA fallback, plus an in-memory
// /api backend. The seam crawl (§6.4) never hits the backend; it exists so the
// res-3 harness (task #45) has a real network seam to intercept with page.route
// and observe where a persisted write LANDS (the placement mutation proof).
//
// SCHEMA-BOUNDED STORE (res-3 UNPROVABLE substrate): the store mirrors the
// IMPLEMENTED data model (schema.json) — POST /api/<entity> stores/echoes ONLY the
// entity's schema fields; a posted key that is NOT a schema field is DISCARDED (not
// stored, not echoed). That is what makes a single-field entity (`note`) UNPROVABLE:
// a harness-synthesized shadow field is discarded here, so a redirect to it cannot
// be OBSERVED landing in a wrong place — indistinguishable from a dropped write. A
// multi-field entity redirects to a real sibling, which IS echoed -> placement RED.
//
// Usage: node serve.mjs --dir <build-dir> --port <port> [--schema <schema.json>]
import { createServer } from 'node:http'
import { readFile, stat } from 'node:fs/promises'
import { readFileSync } from 'node:fs'
import { resolve, extname, join, normalize } from 'node:path'
import { fileURLToPath } from 'node:url'

const argv = process.argv.slice(2)
const args = {}
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) { args[argv[i].slice(2)] = argv[i + 1]; i++ }
}
const DIR = resolve(args.dir || 'dist')
const PORT = Number(args.port || 0)
// schema.json lives next to this file unless overridden (a res-3 test copy points --schema
// at a temp schema to exercise the multi-field placement-RED path against the same server).
const SCHEMA_PATH = resolve(args.schema || join(fileURLToPath(new URL('.', import.meta.url)), 'schema.json'))
const SCHEMA = JSON.parse(readFileSync(SCHEMA_PATH, 'utf8'))

// store: one record per entity, initialised to the entity's schema fields (all empty).
const store = {}
for (const [ent, fields] of Object.entries(SCHEMA)) {
  store[ent] = Object.fromEntries((fields || []).map((f) => [f, '']))
}

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.map': 'application/json', '.ico': 'image/x-icon',
}

function resetStore() {
  for (const [ent, fields] of Object.entries(SCHEMA)) store[ent] = Object.fromEntries((fields || []).map((f) => [f, '']))
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1')
  if (url.pathname.startsWith('/api/')) {
    // res-3 test hook: the harness resets the store before EACH proof run so a placement
    // assertion reflects only the current run's write, not a residual from a prior run (the
    // store is process-global). A real Phase-5 backend isolates per-test differently (fresh
    // DB / transaction rollback) — that is the T-25 boundary, not a harness change.
    if (req.method === 'POST' && url.pathname === '/api/__reset') {
      // The response ECHOES the store so the harness can CONFIRM the reset actually cleared the
      // field it will assert on — a swallowed 404 / lying no-op would otherwise leave residual state
      // and launder a non-writing element to PASS (H3). PEN_SERVE_NOOP_RESET (test-only): a lying
      // reset that returns 200 + reset:true but does NOT clear, so the harness must catch it by
      // inspecting the returned store, not just the status.
      if (process.env.PEN_SERVE_NOOP_RESET !== '1') resetStore()
      res.writeHead(200, { 'content-type': 'application/json' })
      res.end(JSON.stringify({ ok: true, reset: true, store }))
      return
    }
    const m = url.pathname.match(/^\/api\/([a-zA-Z][\w-]*)$/)
    if (req.method === 'POST' && m && store[m[1]]) {
      const ent = m[1]
      const fields = SCHEMA[ent] || []
      let body = ''
      for await (const chunk of req) body += chunk
      let parsed = {}
      try { parsed = JSON.parse(body) } catch { /* ignore */ }
      // schema-bounded merge: only fields declared in the entity's schema are stored; any other key
      // (e.g. a harness shadow field) is discarded and never echoed. PEN_SERVE_KEYBLIND (test-only):
      // echo-both — store the posted value into EVERY schema field, ignoring the key, so a redirected
      // write still lands in the correct field and the placement proof stays GREEN (H4 negative).
      if (process.env.PEN_SERVE_KEYBLIND === '1') {
        const v = Object.values(parsed)[0]
        for (const f of fields) store[ent][f] = v ?? ''
      } else {
        for (const [k, v] of Object.entries(parsed)) {
          if (fields.includes(k)) store[ent][k] = v ?? ''
        }
      }
      res.writeHead(200, { 'content-type': 'application/json' })
      res.end(JSON.stringify({ ok: true, entity: ent, state: store[ent] }))
      return
    }
    res.writeHead(404, { 'content-type': 'application/json' })
    res.end(JSON.stringify({ error: 'no such endpoint' }))
    return
  }
  let p = decodeURIComponent(url.pathname)
  if (p === '/' || p.endsWith('/')) p = '/index.html'
  // contain path traversal within DIR
  let fp = normalize(join(DIR, p))
  if (!fp.startsWith(DIR)) { res.writeHead(403); res.end('forbidden'); return }
  try {
    const s = await stat(fp)
    if (s.isDirectory()) fp = join(fp, 'index.html')
    const data = await readFile(fp)
    res.writeHead(200, { 'content-type': MIME[extname(fp)] || 'application/octet-stream' })
    res.end(data)
  } catch {
    try {
      const data = await readFile(join(DIR, 'index.html'))
      res.writeHead(200, { 'content-type': 'text/html' })
      res.end(data)
    } catch { res.writeHead(404); res.end('not found') }
  }
})

server.listen(PORT, '127.0.0.1', () => {
  const port = server.address().port
  console.log('SEAM_FIXTURE_READY http://127.0.0.1:' + port + '/')
})
