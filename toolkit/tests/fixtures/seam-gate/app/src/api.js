// The single network seam the res-3 harness (task #45) intercepts with page.route
// to run the placement mutation proof against the single-field `note` entity.
// The §6.4 seam crawl never drives this — it is res-3 substrate carried now so the
// fixture is not rebuilt in task #45.
export async function saveNote(text) {
  try {
    const r = await fetch('/api/note', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    return await r.json()
  } catch {
    return { ok: false }
  }
}
