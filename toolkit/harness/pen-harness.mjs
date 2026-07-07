#!/usr/bin/env node
// pen-harness.mjs — the quarantined node/Playwright runtime for the design-process
// overhaul's RUNTIME gates. It implements `crawl` mode (§6.4 seam gate) and `e2e` mode
// (§6.3 res-3, task #45: executed E2E + dual mutation proofs — see the e2e section below).
//
// ROLE (harness-substrate-memo §4): the harness is a PRODUCER of observations, NOT a
// verdict authority. In crawl mode it drives a real headless-Chromium crawl of the hydrated
// app; in e2e mode it drives per-element E2Es + the two mutation proofs. Either way it writes
// observations.json; the bash gate (seam-gate.sh for §6.4 crawl, res3-gate.sh for §6.3 res-3
// e2e) turns that into a 0/1/2 verdict.
//
// crawl mode walks each machine's states from `initial`, induces every documented state
// (opens modals, selects tabs, induces error/empty states), and UNIONs the data-oids it
// sees across states — querying the WHOLE document, so portal roots are included. It
// records, per induced state, the observed (data-oid, data-oiid) nodes; which declared
// states were induced vs unreachable; and a role-heuristic WARN list (T-23 backstop —
// see the honesty note below).
//
// HONESTY LIMIT (memo §6): the T-23 "interactive element with a handler but no data-oid"
// backstop is NOT true handler-presence detection in a framework app (React attaches
// listeners via synthetic-event delegation at one root, so onClick nodes can't be
// enumerated from the DOM). It degrades to a ROLE HEURISTIC: a button / a[href] / input /
// select / textarea / [role] node carrying no data-oid. Reported, never gating.
//
// HONESTY LIMIT (e2e / dependence proof): the proof (a) stub neutralizes the element's handler
// via `window.__wire.disabled` (seeded before hydration). This is a FIXTURE CONTRACT — a real app
// must expose an equivalent addressable handler registry for res-1 symbols. An app that does NOT
// honor it makes disabling a no-op, so the E2E stays green under the stub and the gate reads
// dependence=GREEN → FAIL (vacuous) rather than a §4.4 "proof unconstructible" FATAL. Fail-closed
// either way (no false-pass); the FATAL-refinement for an un-addressable symbol is Phase-5 (T-25).
//
// Exit: 0 when observations.json was produced (whatever it says — the gate judges it);
//       non-zero ONLY on an operational failure the gate must read as FATAL (app never
//       ready, browser launch failure, unparseable input, cannot write the output).

import { writeFileSync, readFileSync } from 'node:fs'
import { spawn } from 'node:child_process'

function die(msg, code = 2) {
  process.stderr.write('[pen-harness] FATAL: ' + msg + '\n')
  process.exit(code)
}
function log(msg) { process.stderr.write('[pen-harness] ' + msg + '\n') }

// ---- arg parsing (frozen contract, memo §4.1) -------------------------------
function parseArgs(argv) {
  const a = {
    mode: null, appUrl: null, appCmd: null, machines: [], manifest: null,
    results: null, exceptions: null, out: null, oiid: false, timeout: 6000,
    browser: 'chromium', noInduce: false, e2es: [], schema: null,
  }
  const rest = argv.slice(2)
  if (rest.length && !rest[0].startsWith('--')) { a.mode = rest.shift() }
  for (let i = 0; i < rest.length; i++) {
    const t = rest[i]
    const val = () => { const v = rest[++i]; if (v === undefined) die('missing value for ' + t); return v }
    switch (t) {
      case '--app-url': a.appUrl = val(); break
      case '--app-cmd': a.appCmd = val(); break
      case '--machine': a.machines.push(val()); break
      case '--e2e': a.e2es.push(val()); break
      case '--schema': a.schema = val(); break
      case '--manifest': a.manifest = val(); break
      case '--results': a.results = val(); break
      case '--exceptions': a.exceptions = val(); break
      case '--out': a.out = val(); break
      case '--oiid': a.oiid = true; break
      case '--no-induce': a.noInduce = true; break
      case '--timeout': a.timeout = parseInt(val(), 10); break
      case '--browser': a.browser = val(); break
      default: die('unknown arg: ' + t)
    }
  }
  return a
}

// ---- machine → state graph --------------------------------------------------
// Descend a compound state to its initial leaf. path is an array of state names.
function descend(machine, path) {
  let node = machine
  for (const p of path) node = node.states[p]
  while (node && node.states && node.initial) { path = path.concat(node.initial); node = node.states[node.initial] }
  return path
}
function nodeAt(machine, path) { let n = machine; for (const p of path) n = n.states[p]; return n }

// Resolve a transition target NAME to a leaf path, relative to the source leaf.
// Prefer a sibling (child of the source's compound parent), else a top-level screen-state.
function resolveTarget(machine, sourcePath, targetName) {
  const parent = sourcePath.slice(0, -1)
  // sibling candidate
  try { if (nodeAt(machine, parent.concat(targetName))) return descend(machine, parent.concat(targetName)) } catch { /* not a sibling */ }
  // top-level candidate
  if (machine.states[targetName]) return descend(machine, [targetName])
  return null
}

// Enumerate every leaf state and every transition edge (source leaf -> target leaf).
function buildGraph(machine) {
  const leaves = []
  const edges = [] // {from:[..], to:[..], screen, event, fromWireId, selector}
  function walk(path) {
    const node = nodeAt(machine, path)
    const isLeaf = !(node.states && node.initial)
    if (isLeaf && path.length) leaves.push(path)
    if (node.on) {
      const screen = path[0]
      for (const [event, arr] of Object.entries(node.on)) {
        for (const tr of arr) {
          const to = resolveTarget(machine, path, tr.target)
          edges.push({
            from: path, to, screen, event, fromWireId: tr.fromWireId,
            selector: to ? `[data-oid="${screen}/${tr.fromWireId}"]` : null,
          })
        }
      }
    }
    if (node.states) for (const name of Object.keys(node.states)) walk(path.concat(name))
  }
  walk([])
  return { leaves, edges, initial: descend(machine, [machine.initial]) }
}

const key = (p) => p.join('.')

// BFS shortest click-path from initial to every leaf (static graph only).
function bfsPaths(graph) {
  const paths = { [key(graph.initial)]: [] }
  const q = [graph.initial]
  while (q.length) {
    const cur = q.shift()
    for (const e of graph.edges) {
      if (key(e.from) !== key(cur) || !e.to || !e.selector) continue
      const tk = key(e.to)
      if (paths[tk] !== undefined) continue
      paths[tk] = paths[key(cur)].concat([{ selector: e.selector, to: e.to }])
      q.push(e.to)
    }
  }
  return paths
}

// Outgoing trigger selectors of a leaf — used as a settle marker after induction.
function triggerSelectors(graph, leaf) {
  return graph.edges.filter((e) => key(e.from) === key(leaf) && e.selector).map((e) => e.selector)
}

// ---- browser observation ----------------------------------------------------
async function observe(page) {
  return page.evaluate(() => {
    const nodes = []
    document.querySelectorAll('[data-oid]').forEach((el) => {
      nodes.push({ oid: el.getAttribute('data-oid'), oiid: el.getAttribute('data-oiid') })
    })
    const warns = []
    document.querySelectorAll('button, a[href], input, select, textarea, [role]').forEach((el) => {
      if (!el.hasAttribute('data-oid')) {
        warns.push({ tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || null, text: (el.textContent || '').trim().slice(0, 40) })
      }
    })
    return { nodes, warns }
  })
}

async function driveTo(page, appUrl, path, timeout) {
  await page.goto(appUrl, { waitUntil: 'domcontentloaded', timeout })
  await page.waitForSelector('[data-app-ready]', { timeout })
  for (const step of path) {
    try {
      await page.waitForSelector(step.selector, { state: 'attached', timeout })
      await page.click(step.selector, { timeout })
    } catch {
      return { induced: false, failedAt: step.selector }
    }
  }
  return { induced: true }
}

// ---- app lifecycle (memo §4.2.2: harness owns start→wait-ready→teardown) -----
async function startApp(appCmd, appUrl, timeout) {
  log('starting app: ' + appCmd)
  const child = spawn(appCmd, { shell: true, detached: true, stdio: ['ignore', 'pipe', 'pipe'] })
  child.stdout.on('data', (d) => process.stderr.write('[app] ' + d))
  child.stderr.on('data', (d) => process.stderr.write('[app!] ' + d))
  // The readiness floor (min wait for the app to come up) is 15s. PEN_HARNESS_READY_FLOOR_MS
  // lets the F-007 suite shorten it to exercise the readiness-timeout FATAL fast; the guard is
  // unchanged (default floor, still fail-closed on timeout).
  const floor = Number(process.env.PEN_HARNESS_READY_FLOOR_MS || 15000)
  const deadline = Date.now() + Math.max(timeout, floor)
  while (Date.now() < deadline) {
    try {
      const r = await fetch(appUrl, { method: 'GET' })
      if (r.ok || r.status === 200) { log('app ready at ' + appUrl); return child }
    } catch { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 150))
  }
  stopApp(child)
  return null
}
function stopApp(child) {
  if (!child) return
  try { process.kill(-child.pid, 'SIGTERM') } catch { try { child.kill('SIGTERM') } catch { /* gone */ } }
}

async function fetchBuildConfig(appUrl) {
  try {
    // Resolve against the ORIGIN so a query string / path on --app-url (e.g. a fixture
    // scenario ?omit=…) does not mangle the build-config URL.
    const url = new URL('/build-config.json', appUrl).href
    const r = await fetch(url)
    if (!r.ok) return null
    return await r.json()
  } catch { return null }
}

// ---- crawl ------------------------------------------------------------------
async function crawl(a) {
  let pw
  try { pw = await import('playwright') } catch { die('playwright is not installed in the harness (run: npm --prefix <toolkit>/harness ci && npx playwright install chromium)') }

  let appChild = null
  if (a.appCmd) {
    appChild = await startApp(a.appCmd, a.appUrl, a.timeout)
    if (!appChild) die('app did not become ready at ' + a.appUrl + ' (hydration/readiness timeout)')
  }

  let browser
  try { browser = await pw.chromium.launch({ headless: true }) } catch (e) { stopApp(appChild); die('browser launch failed: ' + e.message.split('\n')[0]) }

  const out = {
    mode: 'crawl', appUrl: a.appUrl, generatedAt: new Date().toISOString(),
    noInduce: a.noInduce, buildConfig: null, machines: [], states: [],
    declaredStates: [], unreachableStates: [], union: [], warnList: [],
  }
  const unionSet = new Set()
  const warnMap = new Map()

  try {
    out.buildConfig = await fetchBuildConfig(a.appUrl)
    const page = await browser.newPage()

    for (const mfile of a.machines) {
      let machine
      // THROW (not die/process.exit) so the `finally` below tears down the browser + detached
      // app before the crawl().catch() converts this to FATAL exit 2 — a die() here would skip
      // the finally and orphan serve.mjs on a bound port (a first-class §4.4 FATAL input).
      try { machine = JSON.parse(readFileSync(mfile, 'utf8')) } catch (e) { throw new Error('cannot parse machine ' + mfile + ': ' + e.message) }
      const mid = machine.id || mfile
      out.machines.push(mid)
      const graph = buildGraph(machine)
      const paths = bfsPaths(graph)

      // With --no-induce (the lobotomize control) observe ONLY the initial state.
      const targets = a.noInduce ? [graph.initial] : graph.leaves

      for (const leaf of targets) {
        const lk = key(leaf)
        const path = paths[lk]
        const rec = { machine: mid, state: lk, screenState: leaf[0], induced: false, path: [] }
        if (path === undefined) {
          out.unreachableStates.push({ machine: mid, state: lk, reason: 'no transition path from initial in the machine graph' })
          out.declaredStates.push({ machine: mid, state: lk, induced: false })
          continue
        }
        rec.path = path.map((s) => s.selector)
        const drive = await driveTo(page, a.appUrl, path, a.timeout)
        if (!drive.induced) {
          out.unreachableStates.push({ machine: mid, state: lk, reason: 'induction failed at ' + drive.failedAt })
          out.declaredStates.push({ machine: mid, state: lk, induced: false })
          continue
        }
        // settle: wait for one of this state's outgoing triggers, else a short fixed wait
        const trigs = triggerSelectors(graph, leaf)
        if (trigs.length) { try { await page.waitForSelector(trigs[0], { timeout: 1500 }) } catch { /* terminal-ish */ } }
        else { await page.waitForTimeout(120) }

        const { nodes, warns } = await observe(page)
        rec.induced = true
        rec.nodes = nodes
        rec.oids = Array.from(new Set(nodes.map((n) => n.oid)))
        rec.oids.forEach((o) => unionSet.add(o))
        for (const w of warns) {
          const wk = w.tag + '|' + (w.role || '') + '|' + w.text
          if (!warnMap.has(wk)) warnMap.set(wk, { ...w, states: [] })
          if (!warnMap.get(wk).states.includes(lk)) warnMap.get(wk).states.push(lk)
        }
        out.states.push(rec)
        out.declaredStates.push({ machine: mid, state: lk, induced: true })
      }
    }
  } finally {
    // Both teardowns must run even if the first throws — otherwise a browser.close() error would
    // skip stopApp and orphan the detached app on its bound port (the G2 leak, defence in depth).
    try { await browser.close() } catch { /* browser may already be gone */ }
    stopApp(appChild)
  }

  out.union = Array.from(unionSet).sort()
  out.warnList = Array.from(warnMap.values())
  try { writeFileSync(a.out, JSON.stringify(out, null, 2) + '\n') } catch (e) { die('cannot write observations to ' + a.out + ': ' + e.message) }
  log('wrote ' + a.out + ' (' + out.states.length + ' induced state(s), union of ' + out.union.length + ' data-oid(s), ' + out.unreachableStates.length + ' unreachable)')
}

// ---- e2e (§6.3 res-3) -------------------------------------------------------
// The res-3 harness drives each declared E2E against the hydrated app and runs, per element, the
// two mutation proofs the spec mandates. It is a PRODUCER of per-row proof outcomes; the bash gate
// (res3-gate.sh) turns them into a 0/1/2 verdict and validates UNPROVABLE sign-offs.
//
//   PRIMARY   drive the element by data-oid (data-oiid per instance) and assert the data-effect
//             landed in the CORRECT place. e2ePass=false => the element's E2E is broken.
//   proof (a) DEPENDENCE — neutralize the res-1 handler symbol for THIS oid (window.__wire.disabled,
//             seeded via addInitScript before hydration) and re-drive: the effect assertion MUST go
//             RED. Staying GREEN => the E2E does not depend on the handler => vacuous => gate FAILs.
//   proof (b) PLACEMENT (rows declaring a persisted `writes` effect) — redirect the write at the
//             network seam (page.route body relabel) to a SIBLING field and re-drive: the effect
//             assertion MUST go RED *and* the value must land OBSERVABLY in the sibling. Single-field
//             entities have no observable sibling — a synthesized shadow field is discarded by the
//             schema-bounded backend, so the redirect degenerates to a dropped write (indistinct
//             from proof (a)) and placement is UNPROVABLE (fail-closed). ephemeral:true + empty
//             writes => NA-EPHEMERAL (no persisted write; proof (a) still runs on the localEffect).

function loadJSONorThrow(path, what) {
  try { return JSON.parse(readFileSync(path, 'utf8')) }
  catch (e) { throw new Error('cannot parse ' + what + ' (' + path + '): ' + e.message) }
}

const bareScreen = (s) => (typeof s === 'string' && s.startsWith('screen/')) ? s.slice('screen/'.length) : s
const oidSel = (oid) => '[data-oid="' + oid + '"]'

// Capturing route: forwards /api/** to the REAL backend, records each JSON echo, and (proof b)
// relabels the write body key `redirect.field` -> `redirect.target` at the seam so the value lands
// in a different field. The gate never trusts the harness's own store — placement is read from the
// backend's echo (memo A6: observable at the network seam), so the redirect proof is honest.
async function installApiRoute(page, captured, redirect) {
  await page.route('**/api/**', async (route) => {
    let sendData
    const pd = route.request().postData()
    if (redirect && pd) {
      try {
        const b = JSON.parse(pd)
        if (Object.prototype.hasOwnProperty.call(b, redirect.field)) {
          b[redirect.target] = b[redirect.field]
          delete b[redirect.field]
        }
        sendData = JSON.stringify(b)
      } catch { sendData = pd }
    }
    let resp
    try { resp = await route.fetch(sendData != null ? { postData: sendData } : undefined) }
    catch { try { await route.continue() } catch { /* request gone */ } return }
    try { captured.push(await resp.json()) } catch { /* non-JSON body */ }
    try { await route.fulfill({ response: resp }) } catch { /* page navigated away */ }
  })
}

// Evaluate an effect assertion. `captured` = the /api echoes seen this run; `k` = the driven
// instance index (for instanceAttr). Returns true iff the effect landed as declared.
async function assertEffect(page, effect, captured, k, timeout) {
  switch (effect.kind) {
    case 'persist':
      return captured.some((w) => w && w.state && w.state[effect.field] === effect.value)
    case 'present':
      try { await page.waitForSelector(oidSel(effect.oid), { timeout: Math.min(timeout, 1500) }) } catch { /* stays absent */ }
      return (await page.locator(oidSel(effect.oid)).count()) > 0
    case 'absent':
      return (await page.locator(oidSel(effect.oid)).count()) === 0
    case 'count': {
      const c = await page.locator(oidSel(effect.oid)).count()
      if (effect.op === 'eq') return c === effect.n
      if (effect.op === 'lt') return c < effect.n
      if (effect.op === 'gt') return c > effect.n
      throw new Error('unknown count op: ' + effect.op)
    }
    case 'instanceAttr': {
      const idx = (effect.index === '$k') ? k : effect.index
      return (await page.locator(oidSel(effect.oid)).nth(idx).getAttribute(effect.attr)) === effect.value
    }
    default:
      throw new Error('unknown effect kind: ' + effect.kind)
  }
}

// Execute the drive steps; `k` substitutes for "$k" in clickInstance.index.
async function drive(page, steps, k, timeout) {
  for (const step of steps) {
    if (step.click) {
      await page.waitForSelector(oidSel(step.click), { state: 'attached', timeout })
      await page.click(oidSel(step.click), { timeout })
    } else if (step.fill) {
      await page.waitForSelector(oidSel(step.fill), { state: 'attached', timeout })
      await page.fill(oidSel(step.fill), step.value, { timeout })
    } else if (step.clickInstance) {
      const idx = (step.index === '$k') ? k : step.index
      await page.locator(oidSel(step.clickInstance)).nth(idx).click({ timeout })
    } else {
      throw new Error('unknown drive step: ' + JSON.stringify(step))
    }
  }
}

// resetBackend — POST /api/__reset and CONFIRM it established a clean baseline for a persist run.
// fetch() rejects only on a NETWORK error, not on a 404 / lying no-op reset, so we inspect the
// response: `reset:true` AND, for a persist run, the asserted field is actually cleared in the
// returned store. A missing/lying reset returns false so the persist run can fail CLOSED (H3)
// instead of reading residual process-global store state. Non-persist runs (DOM localEffects) do
// not read the store, so the reset outcome is advisory for them.
async function resetBackend(appUrl, effect) {
  try {
    const r = await fetch(new URL('/api/__reset', appUrl).href, { method: 'POST' })
    if (!r.ok) return false
    const j = await r.json().catch(() => null)
    if (!j || j.reset !== true) return false
    if (effect && effect.kind === 'persist') {
      const ent = j.store && j.store[effect.entity]
      return !!ent && (ent[effect.field] ?? '') === ''
    }
    return true
  } catch { return false }
}

// One E2E run in a FRESH context (isolation between proofs). `disableOid` neutralizes that oid's
// handler before hydration (proof a); `redirect` relabels the write at the seam (proof b). A drive
// or assertion failure is a clean { pass: false } (a broken/missing element is a RED E2E, not a
// harness crash); a persist run whose reset could not be confirmed returns { resetFailed: true }
// (fail-closed, H3); only context/browser infra errors propagate to the caller.
async function runOnce(browser, a, spec, k, opts) {
  const { disableOid = null, redirect = null } = opts || {}
  const ctx = await browser.newContext()
  const captured = []
  try {
    if (disableOid) {
      await ctx.addInitScript((oid) => { window.__wire = { disabled: new Set([oid]) } }, disableOid)
    }
    const page = await ctx.newPage()
    await installApiRoute(page, captured, redirect)
    try {
      await page.goto(a.appUrl, { waitUntil: 'domcontentloaded', timeout: a.timeout })
      await page.waitForSelector('[data-app-ready]', { timeout: a.timeout })
      // Reset the backend store so a persist assertion reflects ONLY this run's write, not residual
      // from a prior run (the store is process-global). A persist run REQUIRES a CONFIRMED reset —
      // an unconfirmed one (404 / lying no-op) is fail-closed (H3), never swallowed.
      const resetOk = await resetBackend(a.appUrl, spec.effect)
      if (spec.effect && spec.effect.kind === 'persist' && !resetOk) {
        return { pass: false, captured, resetFailed: true }
      }
      await drive(page, spec.drive, k, a.timeout)
      await page.waitForTimeout(150) // settle: a state commit + any /api echo are observed
      const pass = await assertEffect(page, spec.effect, captured, k, a.timeout)
      return { pass, captured }
    } catch (e) {
      return { pass: false, captured, error: e && e.message ? e.message : String(e) }
    }
  } finally {
    await ctx.close()
  }
}

// computePlacement — proof (b) for a persisted, persist-effect row (H8, extracted from e2e()).
// Redirects the write to a sibling (or a synthesized shadow for a single-field entity) and reads the
// backend echo: RED (observable wrong-place landing), GREEN (vacuous — the redirect did not turn the
// E2E red), or UNPROVABLE (no observable sibling; fail-closed). Returns { placement, detail }, or
// { resetFailed: true } if the redirect run could not establish per-run isolation (H3).
async function computePlacement(browser, a, spec, schema) {
  const entity = spec.effect.entity
  const field = spec.effect.field
  const fields = Array.isArray(schema[entity]) ? schema[entity] : []
  const siblings = fields.filter((f) => f !== field)
  if (siblings.length) {
    const target = siblings[0]
    const rp = await runOnce(browser, a, spec, 0, { redirect: { field, target } })
    if (rp.resetFailed) return { resetFailed: true }
    const correctLost = rp.pass === false
    const landedWrong = rp.captured.some((w) => w && w.state && w.state[target] === spec.effect.value)
    if (!correctLost) return { placement: 'GREEN', detail: 'redirect to sibling ' + entity + '.' + target + ' did not turn the E2E RED — vacuous placement assertion' }
    if (landedWrong) return { placement: 'RED', detail: 'value observably redirected to sibling ' + entity + '.' + target + '; the correct field lost it' }
    return { placement: 'UNPROVABLE', detail: 'redirect to ' + entity + '.' + target + ' dropped the value with no observable landing' }
  }
  // Single-field entity (ARB-3-protected): no sibling. Synthesize a shadow field and redirect to it;
  // the schema-bounded backend discards it, so there is no observable wrong-place landing → UNPROVABLE.
  const shadow = field + '__shadow'
  const rp = await runOnce(browser, a, spec, 0, { redirect: { field, target: shadow } })
  if (rp.resetFailed) return { resetFailed: true }
  const landedWrong = rp.captured.some((w) => w && w.state && w.state[shadow] === spec.effect.value)
  if (landedWrong) return { placement: 'RED', detail: 'synthesized shadow field ' + entity + '.' + shadow + ' was observable at the seam' }
  return { placement: 'UNPROVABLE', detail: 'single-field entity ' + entity + ' (schema fields: [' + fields.join(', ') + ']) — a synthesized shadow field is discarded by the schema-bounded backend, so no observable wrong-place landing exists; placement cannot be redirected' }
}

async function e2e(a) {
  let pw
  try { pw = await import('playwright') } catch { die('playwright is not installed in the harness (run: npm --prefix <toolkit>/harness ci && npx playwright install chromium)') }

  let appChild = null
  if (a.appCmd) {
    appChild = await startApp(a.appCmd, a.appUrl, a.timeout)
    if (!appChild) die('app did not become ready at ' + a.appUrl + ' (hydration/readiness timeout)')
  }

  let manifest, schema, specs, journeys, waveRaw
  try {
    manifest = loadJSONorThrow(a.manifest, 'wiring-manifest.json')
    schema = loadJSONorThrow(a.schema, 'schema.json')
    specs = {}
    journeys = []
    for (const ef of a.e2es) {
      const j = loadJSONorThrow(ef, 'e2e spec')
      if (j.journey) journeys.push(j.journey)
      for (const [oid, s] of Object.entries((j && j.e2e) || {})) specs[oid] = s
    }
    // wave echo (informational; the GATE is the wave authority per the G4/G7 rulings)
    waveRaw = {}
    if (a.results) {
      const r = loadJSONorThrow(a.results, 'wiring-results.json')
      for (const rr of (r && r.rows) || []) {
        if (rr && rr.screen !== undefined && rr.wireId !== undefined) waveRaw[rr.screen + ' ' + rr.wireId] = rr.wave ?? null
      }
    }
  } catch (e) { stopApp(appChild); die(e.message) }

  const rowByOid = {}
  for (const row of Array.isArray(manifest) ? manifest : []) {
    if (row && typeof row === 'object') rowByOid[bareScreen(row.screen) + '/' + row.wireId] = row
  }

  let browser
  try { browser = await pw.chromium.launch({ headless: true }) }
  catch (e) { stopApp(appChild); die('browser launch failed: ' + e.message.split('\n')[0]) }

  const out = {
    mode: 'e2e', appUrl: a.appUrl, generatedAt: new Date().toISOString(),
    journeys, rows: [], problems: [],
  }
  const jpref = journeys[0] ? 'e2e.' + journeys[0] : 'e2e'

  try {
    for (const [oid, spec] of Object.entries(specs)) {
      const row = rowByOid[oid]
      if (!row) { out.problems.push({ oid, reason: 'e2e spec references an oid with no wiring-manifest row' }); continue }
      try {
        const writes = Array.isArray(row.writes) ? row.writes.filter((x) => typeof x === 'string') : []
        const persisted = writes.length > 0
        const ephemeral = row.ephemeral === true

        // H6: a persisted row whose E2E does not ASSERT the persist is mis-authored — its primary
        // e2ePass would check a non-persist condition (present/count) that can be true with nothing
        // persisted, and the placement proof cannot be constructed. Emit a `problem` (the gate FATALs
        // a closed gated row) rather than a sign-off-able UNPROVABLE (the H3 launder surface).
        if (persisted && (!spec.effect || spec.effect.kind !== 'persist')) {
          out.problems.push({ oid, reason: 'persisted row (writes=' + JSON.stringify(writes) + ') whose e2e effect is ' + JSON.stringify(spec.effect && spec.effect.kind) + ', not a persist assertion — the placement proof cannot be constructed (fail-closed, H6)' })
          continue
        }

        const isOiid = spec.oiid && typeof spec.oiid.instances === 'number'
        const rec = {
          screen: row.screen, wireId: row.wireId, oid, e2eRef: jpref + '#' + oid,
          persisted, ephemeral, wave: waveRaw[row.screen + ' ' + row.wireId] ?? null,
          e2ePass: false, lastRun: new Date().toISOString(),
          mutationProofs: { dependence: null, placement: null }, oiid: null,
        }

        // PRIMARY + proof (a) dependence. A persist run whose per-run isolation could not be
        // established (resetFailed) is UNCONSTRUCTIBLE — its reads would be polluted by residual store
        // state and could launder a non-writing element to PASS (H3). Fail closed with a `problem`.
        if (isOiid) {
          const n = spec.oiid.instances
          const perInstance = []
          for (let k = 0; k < n; k++) perInstance.push((await runOnce(browser, a, spec, k, {})).pass)
          rec.e2ePass = perInstance.every(Boolean)
          rec.oiid = { instances: n, perInstance, collapsed: !rec.e2ePass }
          const depK = n > 1 ? 1 : 0
          rec.mutationProofs.dependence = ((await runOnce(browser, a, spec, depK, { disableOid: oid })).pass === false) ? 'RED' : 'GREEN'
        } else {
          const primary = await runOnce(browser, a, spec, 0, {})
          const depRun = await runOnce(browser, a, spec, 0, { disableOid: oid })
          if (primary.resetFailed || depRun.resetFailed) {
            out.problems.push({ oid, reason: 'per-run store isolation could not be established (/api/__reset did not confirm a cleared field) — a persist assertion would read residual store state; fail-closed (H3)' })
            continue
          }
          rec.e2ePass = primary.pass
          rec.mutationProofs.dependence = (depRun.pass === false) ? 'RED' : 'GREEN'
        }

        // proof (b) placement
        if (persisted) {
          const pl = await computePlacement(browser, a, spec, schema)
          if (pl.resetFailed) {
            out.problems.push({ oid, reason: 'per-run store isolation could not be established during the placement proof (/api/__reset unconfirmed) — fail-closed (H3)' })
            continue
          }
          rec.mutationProofs.placement = pl.placement
          rec.placementDetail = pl.detail
        } else if (ephemeral) {
          rec.mutationProofs.placement = 'NA-EPHEMERAL'
          rec.placementDetail = 'ephemeral:true + empty writes — no persisted write to redirect (proof (b) inapplicable; no sign-off)'
        } else {
          // 'NA' is a HARNESS-INTERNAL marker for a non-gated row (no writes, not ephemeral): the gate
          // classifies these res-3 N/A from the manifest and never reads this placement value (H12).
          rec.mutationProofs.placement = 'NA'
          rec.placementDetail = 'row declares no persisted writes and is not ephemeral — not a res-3 data-effect row'
        }

        out.rows.push(rec)
      } catch (e) {
        out.problems.push({ oid, reason: 'e2e run error: ' + (e && e.message ? e.message : String(e)) })
      }
    }
  } finally {
    try { await browser.close() } catch { /* browser may already be gone */ }
    stopApp(appChild)
  }

  try { writeFileSync(a.out, JSON.stringify(out, null, 2) + '\n') } catch (e) { die('cannot write observations to ' + a.out + ': ' + e.message) }
  log('wrote ' + a.out + ' (' + out.rows.length + ' e2e row(s), ' + out.problems.length + ' problem(s))')
}

// ---- main -------------------------------------------------------------------
const a = parseArgs(process.argv)
if (!a.mode) die('usage: pen-harness <crawl|e2e> --app-url <url> [--app-cmd <cmd>] --out <observations.json> [--timeout ms] [--browser chromium]\n' +
  '  crawl: --machine <m.json> [--machine ...] [--no-induce]\n' +
  '  e2e:   --e2e <e2e.<journey>.json> [--e2e ...] --manifest <wiring-manifest.json> --schema <schema.json> --results <wiring-results.json> [--oiid]')
if (!a.appUrl) die('--app-url is required')
if (!a.out) die('--out <observations.json> is required')
// Chromium-only substrate (memo §3). An advertised-but-honored-elsewhere --browser must not
// silently run Chromium — validate rather than accept-and-ignore (F-008 no-silent-divergence).
if (a.browser !== 'chromium') die('--browser ' + JSON.stringify(a.browser) + ' is not supported — this harness drives headless Chromium only (memo §3); pass --browser chromium or omit it')

if (a.mode === 'crawl') {
  if (!a.machines.length) die('crawl mode needs at least one --machine')
  crawl(a).then(() => process.exit(0)).catch((e) => die('crawl failed: ' + (e && e.stack ? e.stack.split('\n').slice(0, 3).join(' | ') : e)))
} else if (a.mode === 'e2e') {
  if (!a.e2es.length) die('e2e mode needs at least one --e2e <e2e.<journey>.json>')
  if (!a.manifest) die('e2e mode needs --manifest (writes/ephemeral per row)')
  if (!a.schema) die('e2e mode needs --schema (the implemented data model — sibling fields for the placement proof)')
  e2e(a).then(() => process.exit(0)).catch((e) => die('e2e failed: ' + (e && e.stack ? e.stack.split('\n').slice(0, 3).join(' | ') : e)))
} else {
  die('unknown mode: ' + a.mode + ' (expected crawl|e2e)')
}
