"""Lab-loop / watch-out / physician-feedback store schemas.

The data-in loop schemas record three operator-facing streams — plan-recommended
panels, watch-out check-in answers, and physician-feedback entries — and read them
back as four published store states. Every write goes THROUGH ``scripts.store.store``
(``append`` / ``read``) keyed by the one ``scripts.store.keying`` Line Field Set; this
module defines no second key and reimplements no store I/O. It reads no operator
answer against a cutoff and raises no automated signal: it stores only
operator-entered answers and derives the watch-out question SET from the operator's
active protocols. All persistence is local file I/O; 0 model-bound send.

The five published states are read 1:1 by ADR-0007-T2's render views:
    pending             a recommended-but-undrawn panel; persists until a result lands
    not-yet-answered    a watch-out check-in with no stored operator answer
    no-data             a biomarker never recorded (zero stored timepoints)
    no-prior            a biomarker with exactly one stored timepoint
    answered-over-time  an answer / feedback entry carried into the next generation

A landed panel result is a VALUE returned by ``read_panel``, NOT a fifth published
state marker — the 4-marker render map is unchanged; the render layer renders a
result as a value row. ``read_panel`` resolves pending->result by source PROVENANCE,
order-independently: the most-recent result reading wins regardless of how its
timepoint sorts against the pending marker's, and the result reading carries a source
tag DISTINCT from the pending marker's so it cannot dedupe-collide with it.
"""

import hashlib

from scripts.store import keying, store

PENDING = "pending"
NOT_YET_ANSWERED = "not-yet-answered"
NO_DATA = "no-data"
NO_PRIOR = "no-prior"
ANSWERED_OVER_TIME = "answered-over-time"

# Source tags distinguishing the data-in streams within the shared store.
# _TAG_PANEL_RESULT is DISTINCT from _TAG_PANEL: the dedupe identity
# (item, timepoint, source) excludes value, so a result reusing the pending
# marker's tag at the marker's own timepoint would be a silent append no-op.
_TAG_PANEL = "plan-recommendation"
_TAG_PANEL_RESULT = "panel-result"
_TAG_WATCHOUT = "watch-out"
_TAG_FEEDBACK = "physician-feedback"
_TAG_BIOMARKER = "manual"

# Per-stream item-id prefixes. The four streams occupy disjoint store-item namespaces
# so a name shared across streams (e.g. "ferritin" as both panel and biomarker) does
# not cross-read. The "::" separator is not a path separator, so the prefixed id stays
# a direct child of the store root (store._item_path guard).
_PREFIX_PANEL = "panel::"
_PREFIX_WATCHOUT = "watch-out::"
_PREFIX_BIOMARKER = "biomarker::"

# The fixed item id under which all physician-feedback entries accrue as one stream.
_FEEDBACK_ITEM = "feedback::physician-feedback"


def _content_tag(prefix, value):
    """Fold a stable content discriminator of a value into a stream's source tag.

    The store dedupe identity is (item, timepoint, source) and EXCLUDES value, so two
    distinct entries at the same timepoint under a constant source would collide and
    the second would be dropped. Folding a short hash of the value into the source tag
    gives distinct values distinct keys (both persist) while an identical re-entry
    keeps the same key (idempotent no-op). Reads match by the `prefix`, not an exact tag.
    """
    digest = hashlib.sha256(repr(value).encode()).hexdigest()[:16]
    return f"{prefix}{digest}"

# Watch-out questions implied by an active protocol/compound. The deriver returns the
# question SET to ASK the operator — it stores no answer and compares no value.
_PROTOCOL_WATCHOUTS = {
    "bpc-157": ("injection_site_reaction", "appetite_change"),
}


def _reading(item, timepoint, source, value):
    """Build a reading carrying every keying.LINE_FIELDS field.

    keying derives the store dedupe identity from (item, timepoint, source) and
    EXCLUDES value, so two appends with the same tuple are idempotent no-ops (the
    second is dropped). Distinct same-timepoint entries in a constant-source stream
    therefore need a varying source — see `_content_tag`.
    """
    return {field: None for field in keying.LINE_FIELDS} | {
        "item": item,
        "timepoint": timepoint,
        "source": source,
        "value": value,
    }


def record_pending_panel(panel, timepoint, root):
    """Record a plan-recommended-but-undrawn panel as state "pending"."""
    item = f"{_PREFIX_PANEL}{panel}"
    store.append(
        item, _reading(item, timepoint, _TAG_PANEL, PENDING), root=root
    )


def record_panel_result(panel, result, timepoint, root):
    """Record a landed result for a recommended panel.

    The result reading carries a source tag distinct from the pending marker's
    (folded through `_content_tag` so two distinct same-timepoint results both
    persist), because the dedupe identity (item, timepoint, source) excludes
    value — a result reusing the pending marker's tag at the marker's own
    timepoint would be silently dropped and the panel would read stuck-pending.

    Args:
        panel (str): The panel the result lands for.
        result: The operator-entered result value (stored verbatim).
        timepoint (str): The result's timepoint.
        root (str | Path): The store root.
    """
    item = f"{_PREFIX_PANEL}{panel}"
    store.append(
        item,
        _reading(item, timepoint, _content_tag(_TAG_PANEL_RESULT, result), result),
        root=root,
    )


def read_panel(panel, root):
    """Resolve a panel's state: the most-recent landed result, else "pending".

    Resolution is by source PROVENANCE, not a value sentinel: the pending marker is
    the only reading written under the plan-recommendation tag, so the most-recent
    result reading wins (its value returned verbatim — even a result whose value
    equals the "pending" string) and a panel with only pending markers reads
    pending. The provenance scan stays order-independent across the store's
    lexicographic timepoint sort: a result recorded for an earlier-sorting
    timepoint still wins over a later pending marker, and the empty stream's
    PENDING return is the published default state, not a guard. The render
    boundary still routes a result VALUE equal to "pending" to the pending marker
    row — a known residual tracked as bead r3pq.
    """
    for reading in reversed(store.read(f"{_PREFIX_PANEL}{panel}", root=root)):
        if reading["source"] != _TAG_PANEL:
            return reading["value"]
    return PENDING


def record_watchout_answer(watchout, answer, timepoint, root):
    """Record an operator's watch-out check-in answer."""
    item = f"{_PREFIX_WATCHOUT}{watchout}"
    store.append(
        item,
        _reading(item, timepoint, _content_tag(_TAG_WATCHOUT, answer), answer),
        root=root,
    )


def read_watchout(watchout, root):
    """Return a watch-out's state: not-yet-answered if no answer, else answered-over-time."""
    if not read_watchout_answers(watchout, root=root):
        return NOT_YET_ANSWERED
    return ANSWERED_OVER_TIME


def read_watchout_answers(watchout, root):
    """Return a watch-out's stored answers, carried forward as next-generation input.

    The store is the carry-forward medium: an answer appended in one generation is
    returned by any later generation's read because ``store.read`` returns all
    appended readings. No stored answer is dropped, expired, or overwritten.
    """
    return store.read(f"{_PREFIX_WATCHOUT}{watchout}", root=root)


def record_biomarker(item, timepoint, value, root):
    """Record one biomarker timepoint."""
    stored = f"{_PREFIX_BIOMARKER}{item}"
    store.append(
        stored, _reading(stored, timepoint, _TAG_BIOMARKER, value), root=root
    )


def read_biomarker(item, root):
    """Return a biomarker's stored timepoints; zero reads "no-data", one reads "no-prior".

    No stored timepoint returns the no-data marker (never-recorded) with an empty
    timepoint list — distinct from the single-timepoint no-prior case and from the
    ≥2-timepoint trend case. A single stored timepoint returns the no-prior marker
    plus that one timepoint — it synthesizes no trend, delta, or projection over a
    single point. Two or more timepoints return the stored readings as-is (the render
    view owns any projection).
    """
    readings = store.read(f"{_PREFIX_BIOMARKER}{item}", root=root)
    if not readings:
        return {"state": NO_DATA, "timepoints": []}
    if len(readings) == 1:
        return {"state": NO_PRIOR, "timepoints": readings}
    return {"state": None, "timepoints": readings}


def derive_watchout_questions(active_protocols):
    """Derive the watch-out question set implied by the operator's active protocols.

    Returns the questions to ASK the operator, keyed off the active protocols/compounds.
    Derives the question SET only — it stores no answer and compares no value to a cutoff.
    """
    questions = set()
    for protocol in active_protocols:
        questions.update(_PROTOCOL_WATCHOUTS.get(protocol, ()))
    return questions


def record_physician_feedback(content, timepoint, root):
    """Record a post-visit physician-feedback entry."""
    store.append(
        _FEEDBACK_ITEM,
        _reading(
            _FEEDBACK_ITEM, timepoint, _content_tag(_TAG_FEEDBACK, content), content
        ),
        root=root,
    )


def read_physician_feedback(root):
    """Return all recorded physician-feedback entries as next-generation input.

    Same carry-forward medium as the watch-out answer: a recorded entry is returned
    by any later generation's read via ``store.read``; no entry is dropped, expired,
    or overwritten.
    """
    return store.read(_FEEDBACK_ITEM, root=root)
