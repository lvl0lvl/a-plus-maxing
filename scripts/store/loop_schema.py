"""Lab-loop / watch-out / physician-feedback store schemas.

The data-in loop schemas record three operator-facing streams — plan-recommended
panels, watch-out check-in answers, and physician-feedback entries — and read them
back as four published store states. Every write goes THROUGH ``scripts.store.store``
(``append`` / ``read``) keyed by the one ``scripts.store.keying`` Line Field Set; this
module defines no second key and reimplements no store I/O. It reads no operator
answer against a cutoff and raises no automated signal: it stores only
operator-entered answers and derives the watch-out question SET from the operator's
active protocols. All persistence is local file I/O; 0 model-bound send.

The four published states are read 1:1 by ADR-0007-T2's render views:
    pending             a recommended-but-undrawn panel; persists until a result lands
    not-yet-answered    a watch-out check-in with no stored operator answer
    no-prior            a biomarker with exactly one stored timepoint
    answered-over-time  an answer / feedback entry carried into the next generation
"""

from scripts.store import keying, store

PENDING = "pending"
NOT_YET_ANSWERED = "not-yet-answered"
NO_PRIOR = "no-prior"
ANSWERED_OVER_TIME = "answered-over-time"

# Source tags distinguishing the data-in streams within the shared store.
_TAG_PANEL = "plan-recommendation"
_TAG_WATCHOUT = "watch-out"
_TAG_FEEDBACK = "physician-feedback"

# The fixed item id under which all physician-feedback entries accrue as one stream.
_FEEDBACK_ITEM = "physician-feedback"

# Watch-out questions implied by an active protocol/compound. The deriver returns the
# question SET to ASK the operator — it stores no answer and compares no value.
_PROTOCOL_WATCHOUTS = {
    "bpc-157": ("injection_site_reaction", "appetite_change"),
}


def _reading(item, timepoint, source, value):
    """Build a reading carrying every keying.LINE_FIELDS field."""
    return {field: None for field in keying.LINE_FIELDS} | {
        "item": item,
        "timepoint": timepoint,
        "source": source,
        "value": value,
    }


def record_pending_panel(panel, timepoint, root):
    """Record a plan-recommended-but-undrawn panel as state "pending"."""
    store.append(
        panel, _reading(panel, timepoint, _TAG_PANEL, PENDING), root=root
    )


def read_panel(panel, root):
    """Return a panel's stored state verbatim — "pending" until a result is appended."""
    readings = store.read(panel, root=root)
    if not readings:
        return PENDING
    return readings[-1]["value"]


def record_watchout_answer(watchout, answer, timepoint, root):
    """Record an operator's watch-out check-in answer."""
    store.append(
        watchout, _reading(watchout, timepoint, _TAG_WATCHOUT, answer), root=root
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
    return store.read(watchout, root=root)


def record_biomarker(item, timepoint, value, root):
    """Record one biomarker timepoint."""
    store.append(
        item, _reading(item, timepoint, "manual", value), root=root
    )


def read_biomarker(item, root):
    """Return a biomarker's stored timepoints; one timepoint reads "no-prior".

    A single stored timepoint returns the no-prior marker plus that one timepoint —
    it synthesizes no trend, delta, or projection over a single point. Two or more
    timepoints return the stored readings as-is (the render view owns any projection).
    """
    readings = store.read(item, root=root)
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
        _reading(_FEEDBACK_ITEM, timepoint, _TAG_FEEDBACK, content),
        root=root,
    )


def read_physician_feedback(root):
    """Return all recorded physician-feedback entries as next-generation input.

    Same carry-forward medium as the watch-out answer: a recorded entry is returned
    by any later generation's read via ``store.read``; no entry is dropped, expired,
    or overwritten.
    """
    return store.read(_FEEDBACK_ITEM, root=root)
