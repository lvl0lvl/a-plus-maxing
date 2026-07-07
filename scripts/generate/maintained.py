"""Unified maintained-HTML output — re-emit + folded tracking (ADR-0025-T1).

`reemit_maintained(...)` is the maintained output lifecycle that AMENDS — does not
replace — ADR-0004's on-demand single-file render (`generate.run`). It RE-EMITS one
living plan artifact as new wearable/lab data arrives, preserving prior content
(annotations, tracking history) across re-emits, folds the
`track.resolve_plan_progress` plan-vs-actual MEASURE-leg view into the same artifact
as its OWN section, and writes the PII-bearing artifact only to the gitignored
`vault/artifacts/generated/`.

The pipeline runs the format-then-fill order (ADR-0021 rationale): the content render
(`render.emit`) runs FIRST, producing the de-identified initials-only HTML; ADR-0021's
deterministic `reinsert_out` is then the FINAL pass over the produced HTML, re-inserting
the real operator full name when the target is confirmable-gitignored. Fill-then-render
would clobber the re-inserted name — the order is load-bearing and lives in one place.

The CALLER owns the write (the SEC-01 caller-precondition): before writing the
name-bearing artifact, `_assert_contained` runs a REALPATH-CONTAINMENT check —
`os.path.realpath(target)` MUST resolve lexically under `os.path.realpath(out_dir)`,
ELSE the write is REFUSED (fail-closed). This is a genuine independent guard catching the
symlink-escape `reinsert_out`'s best-effort `git check-ignore` cannot: a symlink under the
gitignored dir whose realpath escapes to a tracked path exits `check-ignore` 0 on its lexical
name, yet the realpath escapes — the name-bearing HTML would write THROUGH the symlink into a
tracked file. `git check-ignore` alone is symlink-bypassable; the realpath containment is the
primary guard. A symlinked out_dir ROOT is rejected SEPARATELY (before the containment check
resolves it), so a symlinked root cannot launder its target into the accepted realpath root.

The artifact write is the maintained module's OWN atomic temp-then-rename (mirroring
`store._write_atomic`: write the full file to a temp sibling, `fsync`, `os.replace`), so an
interrupted re-emit leaves either the prior good artifact or the new complete one — never a
partial-state file. `render.emit` is DRIVEN for the content render (inheriting its inline-only
/ 0-external-ref / <500KB budget) but the maintained artifact write goes through this atomic
path, leaving `render.py` unedited.

This module reads/writes the store ENTIRELY through `track.resolve_plan_progress` /
`track.record_tracking` (which route through `plan_schema` -> `store`, keyed by the single
`keying.py` identity): it defines no store key, opens no new stream, re-derives no dedupe
identity. The store-keying guarantees (cross-stream namespacing, `(item, timepoint, source)`
dedupe) are inherited by routing through `track`.
"""

import datetime
import os
import tempfile
from html import escape
from pathlib import Path

from scripts.generate import render
from scripts.plan import reinsert_out, track
from scripts.store import plan_schema, store
from vault.design.templates import report

# The maintained artifact's basename under the gitignored out-dir. The maintained
# output is the living report render (the artifact reinsert_out re-inserts the name onto).
_ARTIFACT_NAME = "maintained.html"

# The tracked domains the folded plan-vs-actual section iterates, in render order.
_FOLD_DOMAINS = plan_schema.TRACKED_DOMAINS


def _assert_contained(target, out_dir):
    """Refuse `target` unless its realpath resolves lexically under `out_dir`'s realpath.

    The SEC-01 caller-precondition (the crown jewel). A genuine independent containment
    guard, in two parts:

      1. The realpath-containment check catches a symlinked TARGET under a real root:
         `git check-ignore` (reinsert_out's best-effort confirm) exits 0 on a symlink's lexical
         name under the gitignored prefix even when the symlink's realpath escapes to a tracked
         path — so a name-bearing artifact could write THROUGH the symlink into a tracked file.
         Resolving the realpath of both the target and the out-dir defeats the symlinked target,
         the `..`-traversal, and the non-contained-path escapes identically.
      2. The root-symlink case is rejected SEPARATELY: if `out_dir` itself is a symlink (its final
         component redirects elsewhere), the realpath check would silently adopt the symlink's
         TARGET as the root and accept a write the gitignored-prefix contract never sanctioned. So
         a symlinked out_dir is refused independently, before the containment check resolves it.
         (Ancestor symlinks like macOS `/var`->`/private/var` are NOT the out_dir's own final
         component, so a legitimate out-dir under such a path is unaffected.)

    Fail-closed: any escape raises before a byte is written.

    Args:
        target (str | Path): The destination the name-bearing artifact would be written to.
        out_dir (str | Path): The gitignored output root the target must resolve under.

    Raises:
        ValueError: `out_dir` itself traverses a symlink, OR `target`'s realpath does not resolve
            lexically under `out_dir`'s realpath.
    """
    # (2) the out_dir must not ITSELF be a symlink — a symlinked root would let the realpath check
    # below adopt the symlink's target as the root and sanction a write outside the real gitignored
    # tree. Rejected independently of the target containment below.
    if os.path.islink(out_dir):
        raise ValueError(
            f"refusing to write the maintained artifact: the output root {os.fspath(out_dir)!r} "
            f"is itself a symlink (it redirects to {os.path.realpath(out_dir)!r}) — fail-closed"
        )

    real_target = os.path.realpath(target)
    real_root = os.path.realpath(out_dir)
    if real_target != real_root and not real_target.startswith(real_root + os.sep):
        raise ValueError(
            f"refusing to write the maintained artifact outside its gitignored root: "
            f"{real_target!r} does not resolve under {real_root!r} (symlink / `..` / "
            f"non-contained escape — fail-closed)"
        )


def _write_atomic(target, text):
    """Write `text` to `target` atomically (temp sibling -> fsync -> os.replace).

    Mirrors `store._write_atomic`'s shape: an interrupted write leaves either the prior good
    file or the new complete one — never a truncated/half-written artifact. The temp sibling
    is `os.replace`-renamed (atomic on POSIX) only after its bytes are fsync'd durable.

    Args:
        target (Path): The artifact destination.
        text (str): The full artifact content to write.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=f"{target.name}.", suffix=".tmp")
    try:
        try:
            fh = os.fdopen(fd, "w", encoding="utf-8")
        except BaseException:
            os.close(fd)
            raise
        with fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, target)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _fold_tracking_section(root, on_date):
    """Render the maintained module's OWN folded plan-vs-actual section.

    Calls `track.resolve_plan_progress(domain, on_date, root)` DIRECTLY (the store-surface
    read — not a re-derived join, and not a reused dashboard plan-zone renderer; there is no
    dashboard renderer keyed on `resolve_plan_progress`) for each tracked domain and renders a
    distinct section of the maintained artifact. This folded section is a surface IN the
    gitignored maintained HTML, NOT the deferred dashboard plan-vs-actual surface.

    Args:
        root (str | Path): The store root.
        on_date (str): The render/progress date, YYYY-MM-DD.

    Returns:
        (str) The folded tracking section's HTML.
    """
    rows = []
    for domain in _FOLD_DOMAINS:
        progress = track.resolve_plan_progress(domain, on_date, root)
        plan_cell = "—" if not progress["has_plan"] else escape(str(progress["plan"]))
        track_cell = "—" if not progress["has_tracking"] else escape(str(progress["tracking"]))
        rows.append(
            f"<tr><td class='mt-domain'>{escape(domain)}</td>"
            f"<td class='mt-plan'>{plan_cell}</td>"
            f"<td class='mt-actual'>{track_cell}</td></tr>"
        )
    return (
        "<section class='maintained-tracking'>"
        "<h2>Plan vs actual (tracking)</h2>"
        "<table><thead><tr><th>Domain</th><th>Plan</th><th>Actual</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
        "</section>"
    )


def _read_prior(target):
    """Return the prior maintained artifact's text if it exists, else None."""
    p = Path(target)
    return p.read_text(encoding="utf-8") if p.exists() else None


def _preserve_prior_content(new_html, prior_html):
    """Carry the prior artifact's preserved blocks into the re-emitted HTML.

    A re-emit is NOT a stateless regenerate (the ADR-0004 Negative-2 behavior this amends):
    prior annotations/tracking-history blocks survive the re-emit. The preserved blocks live
    in a single `<div class='maintained-preserved'>...</div>` container; on re-emit the prior
    container's inner content is folded into the new render so prior entries are not dropped.

    Args:
        new_html (str): The freshly rendered maintained HTML (with an empty preserved container).
        prior_html (str | None): The prior maintained artifact's full text, or None on first emit.

    Returns:
        (str) The re-emitted HTML carrying the prior preserved content.
    """
    if prior_html is None:
        return new_html
    open_tag = "<div class='maintained-preserved'>"
    close_tag = "</div><!--/maintained-preserved-->"
    start = prior_html.find(open_tag)
    if start == -1:
        return new_html
    inner_start = start + len(open_tag)
    inner_end = prior_html.find(close_tag, inner_start)
    if inner_end == -1:
        return new_html
    prior_inner = prior_html[inner_start:inner_end]
    return new_html.replace(open_tag + close_tag, open_tag + prior_inner + close_tag, 1)


def _render_report(store_read, today, profile_paths, root):
    """Render the ADR-0004 report, optionally over a test-only profile source, without leaking.

    The report header reads `report._PROFILE_PATHS` internally (a module constant). To point the
    header at a synthetic test profile WITHOUT a persistent global side-effect (which would leak
    into other suites sharing the process), the constant is overridden ONLY across this render and
    restored in a finally — production (`profile_paths is None`) leaves the real default untouched.

    `root` is threaded into `report.render` so the regimen/asks sections drop HELD (un-confirmed)
    `plan::` readings via `plan_confirm.filter_confirmed` (bead a-plus-maxing-zsre).
    """
    if profile_paths is None:
        return report.render(store_read, _today=today, _root=root)
    saved = report._PROFILE_PATHS
    report._PROFILE_PATHS = tuple(profile_paths)
    try:
        return report.render(store_read, _today=today, _root=root)
    finally:
        report._PROFILE_PATHS = saved


def _tailored_sections_html(tailored_sections):
    """Render the care-lane tailored per-domain sections into HTML, or "" when there are none.

    The ADR-0037-T1 injection surface: a `{domain: tailored-text}` mapping (from the care-lane
    tailoring pass) rendered as distinct `care-tailored` sections. Escaped (the tailored text is
    model/operator content, never trusted HTML). Rendered in the FRESH body — outside the
    `maintained-preserved` container — so a re-emit replaces rather than accretes it (idempotent).

    Args:
        tailored_sections (dict | None): domain -> the tailored section text, or None.

    Returns:
        (str) The concatenated tailored-section HTML, or "" when the mapping is empty.
    """
    if not tailored_sections:
        return ""
    blocks = []
    for domain in sorted(tailored_sections):
        blocks.append(
            f"<section class='care-tailored' data-domain='{escape(domain)}'>"
            f"<h2>Personalized: {escape(domain)}</h2>"
            f"<div class='care-tailored-body'>{escape(str(tailored_sections[domain]))}</div>"
            "</section>"
        )
    return "".join(blocks)


def _assemble_maintained(store_read, root, on_date, today, profile_paths, tailored_sections=None):
    """Assemble the maintained HTML: the report render + the folded tracking section.

    A template-callable for `render.emit`: it renders the ADR-0004 report against `store_read`
    (the de-identified initials-only content, carrying the `Patient <initials>` header
    reinsert_out targets), appends the maintained module's OWN folded plan-vs-actual section,
    the ADR-0037-T1 care-lane tailored sections (when present), and a preserved-content container
    the re-emit folds prior entries into.
    """
    body = _render_report(store_read, today, profile_paths, root)
    fold = _fold_tracking_section(root, on_date)
    tailored = _tailored_sections_html(tailored_sections)
    preserved = "<div class='maintained-preserved'></div><!--/maintained-preserved-->"
    insert = tailored + fold + preserved
    if "</body>" in body:
        return body.replace("</body>", insert + "</body>", 1)
    return body + insert


def reemit_maintained(
    *,
    root=None,
    _out_dir=None,
    _today=None,
    _profile_paths=None,
    _repo_root=None,
    _target_override=None,
    _fail_after_render=False,
    tailored_sections=None,
):
    """Re-emit the unified maintained-HTML artifact and return its path.

    Runs the format-then-fill order: the maintained content render (`render.emit`) FIRST,
    then `reinsert_out` as the FINAL pass over the produced HTML. Before writing the
    name-bearing artifact, runs the REALPATH-CONTAINMENT precondition (`_assert_contained`)
    and writes atomically (temp-then-rename). Preserves prior content across re-emits and folds
    the `track.resolve_plan_progress` plan-vs-actual view in as its own section. All store
    access routes through `track`.

    Args:
        root (str | Path, optional): The store root. Defaults to the store's `vault/store/`.
        _out_dir (Path, optional): Test-only output-dir seam — the gitignored artifacts root.
            Defaults to the engine-owned `render.DEFAULT_OUT_DIR`.
        _today (datetime.date, optional): Test-only date seam for the render + the fold's
            progress date. Defaults to the real current date.
        _profile_paths (tuple, optional): Test-only synthetic-identity seam — the gitignored
            profile sources forwarded to BOTH the report header read and `reinsert_out`.
            Defaults to the engine-owned profiles (real operator identity).
        _repo_root (str | Path, optional): Test-only repo-root seam for `reinsert_out`'s
            `git check-ignore` confirm. Defaults to the current working directory.
        _target_override (str | Path, optional): Test-only seam to drive a specific (possibly
            escaping) target through the containment guard. Defaults to the in-dir artifact.
        _fail_after_render (bool, optional): Test-only fault-injection seam — raise after the
            render but before the atomic replace, to prove the artifact is never partial-state.
        tailored_sections (dict, optional): The ADR-0037-T1 care-lane tailored-section injector —
            a `{domain: tailored-text}` mapping injected into the assembled HTML via the existing
            `_assemble_maintained` path. Defaults to None (unchanged pre-T1 behavior). Adds no store
            key and no second writer; preserves the format-then-fill order and the realpath guard.

    Returns:
        (Path) The path of the maintained artifact written.

    Raises:
        ValueError: The target's realpath escapes the gitignored out-dir (containment refused),
            or `render.emit` refused an external-asset reference (propagated).
    """
    out_dir = Path(_out_dir) if _out_dir is not None else render.DEFAULT_OUT_DIR
    store_root = root if root is not None else store.DEFAULT_ROOT
    today = _today if _today is not None else datetime.date.today()
    on_date = today.isoformat()

    store_read = store.read_all(store_root)
    target = Path(_target_override) if _target_override is not None else out_dir / _ARTIFACT_NAME

    # --- render FIRST (the content render; the budget/external-ref gate lives in render.emit) ---
    def _template(sr):
        return _assemble_maintained(
            sr, store_root, on_date, today, _profile_paths, tailored_sections)

    _template.__name__ = "maintained"
    # Render into an auto-cleaned temp staging dir UNDER the (gitignored) out-dir, so the staging
    # directory never accretes (BUG-03 — the old fixed `out_dir/.staging` was never removed). The
    # `TemporaryDirectory` unwinds the dir + its contents on exit, including when `render.emit`
    # raises mid-render (the external-ref budget gate) — leaving 0 staged artifact behind.
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out_dir, prefix=".staging.") as staged_dir:
        rendered_path = render.emit(_template, store_read, _out_dir=Path(staged_dir))
        html = rendered_path.read_text(encoding="utf-8")

    # --- preserve prior content across re-emits ---
    html = _preserve_prior_content(html, _read_prior(target))

    # --- fill LAST (reinsert_out is the FINAL pass over the produced HTML) ---
    reinsert_kwargs = {"_repo_root": _repo_root}
    if _profile_paths is not None:
        reinsert_kwargs["_profile_paths"] = tuple(_profile_paths)
    html = reinsert_out.reinsert_out(html, target, **reinsert_kwargs)

    # --- CROWN JEWEL: realpath-containment before the name-bearing write (fail-closed) ---
    _assert_contained(target, out_dir)

    if _fail_after_render:
        raise RuntimeError("injected mid-write failure (after render, before atomic replace)")

    _write_atomic(target, html)
    return target
