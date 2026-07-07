import { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'
import { saveNote } from './api.js'

// Mutation surface (rebuild-free F-007 negatives): read from the URL query.
//   ?omit=<oid>[,<oid>]  omit designed elements     -> seam gate "missing"
//   ?extra=1             render an undesigned oid    -> seam gate "built-not-designed"
//   ?dup=<oid>           render <oid> twice, no oiid -> seam gate duplicate-identity FAIL
//   ?warn=1              interactive-role, no oid    -> seam gate T-23 WARN (non-gating)
//   ?collapse=1          incident-row highlight always lands on row 0 (row-N-affects-row-0)
//                        -> res-3 (task #45) instance-collapse negative: the instance-aware
//                        placement assertion goes RED when driving instance k>0.
//   ?dead=<oid>          neutralize <oid>'s handler in the running app (a shipped DEAD handler)
//                        -> res-3 primary E2E for <oid> never lands its effect -> e2ePass RED.
// The default (no query) is the GOOD build: every designed element, nothing extra.
function readParams() {
  const q = new URLSearchParams(window.location.search)
  return {
    omit: new Set((q.get('omit') || '').split(',').filter(Boolean)),
    extra: q.get('extra') === '1',
    dup: q.get('dup') || '',
    warn: q.get('warn') === '1',
    collapse: q.get('collapse') === '1',
    dead: q.get('dead') || '',
    twowriters: q.get('twowriters') === '1',
  }
}

const INCIDENTS = [
  { id: 'inc-0', title: 'Sensor A offline' },
  { id: 'inc-1', title: 'Sensor B degraded' },
  { id: 'inc-2', title: 'Pump C overpressure' },
]

export function App() {
  const p = readParams()
  const [screen, setScreen] = useState('list') // 'list' | 'detail'
  const [mode, setMode] = useState('idle') // list: idle|filtering ; detail: idle|error
  const [query, setQuery] = useState('') // list/search localEffect: filters the list in place
  const [selected, setSelected] = useState(-1) // list/incident-row localEffect: highlighted row

  // Marks "React has committed" independent of how many data-oids render, so the
  // crawl can tell "app mounted, zero elements" (a floor FAIL) from "app not ready".
  useEffect(() => { document.documentElement.setAttribute('data-app-ready', '1') }, [])

  const show = (oid) => !p.omit.has(oid)
  // dup renders a non-instance element twice with NO data-oiid: two nodes claiming
  // one identity (BH7). Instances stay legitimate — they differ by data-oiid.
  const times = (oid) => (p.dup === oid ? 2 : 1)

  // Addressable handler registry — the res-1 "handler symbol" layer the res-3 harness
  // (task #45) neutralizes per-oid for the dependence proof (memo A7: the res-1 symbol must
  // be addressable at runtime to stub). Every interactive element dispatches through
  // window.__wire.call(<oid>); the harness disables one oid (page.addInitScript /
  // page.evaluate adds it to window.__wire.disabled) and re-drives to prove the E2E depends
  // on that handler. `disabled` is created ONCE so a harness-installed stub survives React
  // re-renders; `handlers`/`call` are refreshed each render (closures over current state).
  const handlers = {
    '_shell/home': () => { setScreen('list'); setMode('idle'); setSelected(-1); setQuery('') },
    '_shell/back': () => { setScreen('list'); setMode('idle') },
    'list/search': (v) => setQuery(v),
    'list/incident-row': (i) => setSelected(p.collapse ? 0 : i),
    'list/open-filters': () => setMode('filtering'),
    'list/apply-filter': () => setMode('idle'),
    'list/open-detail': () => { setScreen('detail'); setMode('idle') },
    'detail/status-note': () => saveNote('reviewed'),
    // ?twowriters mis-wired writer: POSTs {wrong:'reviewed'} → the schema-bounded backend discards
    // 'wrong', so it NEVER sets note.text. Used only for the res-3 H3 reset-isolation proof.
    'detail/status-note2': () => { try { fetch('/api/note', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ wrong: 'reviewed' }) }) } catch { /* ignore */ } },
    'detail/refresh': () => setMode('error'),
    'detail/retry': () => setMode('idle'),
  }
  if (typeof window !== 'undefined') {
    if (!window.__wire) window.__wire = { disabled: new Set() }
    if (p.dead) window.__wire.disabled.add(p.dead) // ?dead=<oid>: a shipped dead handler
    window.__wire.handlers = handlers
    window.__wire.call = (oid, ...a) => {
      if (window.__wire.disabled && window.__wire.disabled.has(oid)) return
      const h = window.__wire.handlers[oid]
      return h ? h(...a) : undefined
    }
  }
  const call = (oid, ...a) => window.__wire.call(oid, ...a)

  const q = query.trim().toLowerCase()
  const incidents = q ? INCIDENTS.filter((it) => it.title.toLowerCase().includes(q)) : INCIDENTS

  return (
    <>
      <header data-shell="1">
        {show('_shell/home') &&
          Array.from({ length: times('_shell/home') }).map((_, i) => (
            <a key={i} data-oid="_shell/home" href="#/list"
              onClick={(e) => { e.preventDefault(); call('_shell/home') }}>Home</a>
          ))}
        {/* contextually-hidden chrome: rendered ONLY on detail (shellStates screen/detail) */}
        {screen === 'detail' && show('_shell/back') && (
          <button data-oid="_shell/back" type="button"
            onClick={() => call('_shell/back')}>Back</button>
        )}
      </header>

      {screen === 'list' && (
        <main data-screen="screen/list">
          {show('list/search') && (
            <input data-oid="list/search" type="search" value={query} placeholder="Filter incidents"
              onChange={(e) => call('list/search', e.target.value)} />
          )}
          <ul>
            {show('list/incident-row') &&
              incidents.map((it, i) => (
                <li key={it.id} data-oid="list/incident-row" data-oiid={'list/incident-row#' + i}
                  aria-selected={selected === i ? 'true' : 'false'}
                  onClick={() => call('list/incident-row', i)}>
                  {it.title}
                </li>
              ))}
          </ul>
          {show('list/open-filters') &&
            Array.from({ length: times('list/open-filters') }).map((_, i) => (
              <button key={i} data-oid="list/open-filters" type="button"
                onClick={() => call('list/open-filters')}>Filters</button>
            ))}
          {show('list/open-detail') && (
            <button data-oid="list/open-detail" type="button"
              onClick={() => call('list/open-detail')}>Open detail</button>
          )}
          {p.extra && <button data-oid="list/ghost" type="button">Undesigned</button>}
          {/* T-23 backstop demonstrator: an interactive-role node carrying NO data-oid.
              Not an "extra" (the diff is over data-oid nodes only, T-31) — it surfaces on
              the role-heuristic WARN list for design review, and does NOT gate. */}
          {p.warn && <button type="button">Unmapped action</button>}
        </main>
      )}

      {screen === 'detail' && (
        <main data-screen="screen/detail">
          {show('detail/status-note') && (
            <button data-oid="detail/status-note" type="button"
              onClick={() => call('detail/status-note')}>Save note</button>
          )}
          {/* ?twowriters: a SECOND persisted writer that is mis-wired (never sets note.text). Off by
              default (no data-oid rendered) so the seam crawl is unaffected; the res-3 H3 test opts in. */}
          {p.twowriters && show('detail/status-note2') && (
            <button data-oid="detail/status-note2" type="button"
              onClick={() => call('detail/status-note2')}>Save note 2</button>
          )}
          {show('detail/refresh') && (
            <button data-oid="detail/refresh" type="button"
              onClick={() => call('detail/refresh')}>Refresh</button>
          )}
          {mode === 'error' && show('detail/retry') && (
            <button data-oid="detail/retry" type="button"
              onClick={() => call('detail/retry')}>Retry</button>
          )}
        </main>
      )}

      {/* portal modal: apply-filter is attached to document.body, not the main tree */}
      {screen === 'list' && mode === 'filtering' &&
        createPortal(
          <div data-portal="filters-modal">
            {show('list/apply-filter') && (
              <button data-oid="list/apply-filter" type="button"
                onClick={() => call('list/apply-filter')}>Apply</button>
            )}
          </div>,
          document.body
        )}
    </>
  )
}
