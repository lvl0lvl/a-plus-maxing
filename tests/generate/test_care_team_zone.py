"""Tests for the dashboard zone 5 — Your Care Team freshness render (visual spec + care_team_rollup).

Pins that a populated store colors each specialist's status line with a data-state
status dot (PALETTE good/watch/muted via `.sdot-*`, NEVER an accent) plus a muted
recency caption; that streamless specialists read the honest "no data yet" grey
state; that an ALL-empty store keeps the static "no rollup yet" (the pre-data
zone-level empty state the existing care-team test pins); and that no raw store
key leaks. Fixtures use panel/watch-out/feedback/calendar streams (clinical/
fitness domain only), which render cleanly in their own zones.
"""
import datetime
import html as html_lib
import re

from vault.design.templates import component_set, dashboard

# Wednesday 2026-06-10 — the dashboard seam date (June 2026).
_TODAY = datetime.date(2026, 6, 10)


def _day(n):
    """The ISO date `n` days before _TODAY."""
    return (_TODAY - datetime.timedelta(days=n)).isoformat()


def _care_zone(store_read):
    """Render the dashboard and return the 'Your Care Team' <section> markup."""
    html = dashboard.render(store_read, _today=_TODAY)
    for section in re.findall(r"<section class='zone'[^>]*>.*?</section>", html, re.S):
        title = html_lib.unescape(re.search(r"<h2[^>]*>([^<]*)</h2>", section).group(1))
        if title == "Your Care Team":
            return section
    raise AssertionError("Your Care Team zone not found")


def _populated():
    """A store touching four specialists at known recencies (labs+trainer current,
    peptide stale, medical-liaison dormant); the other 12 specialists are streamless."""
    return [
        {"item": "panel::cbc", "timepoint": _day(0), "source": "m", "value": "pending"},
        {"item": "watch-out::sides", "timepoint": _day(40), "source": "m", "value": "none"},
        {"item": "feedback::physician-feedback", "timepoint": _day(90),
         "source": "m", "value": "hold the block"},
        {"item": "calendar::events", "timepoint": _day(3), "source": "c",
         "value": {"category": "training", "label": "Legs"}},
    ]


def test_empty_store_keeps_static_no_rollup_yet():
    """No readings at all -> the 16 cards keep the pre-data static 'no rollup yet'
    caption and carry NO status dot (the honest zone-level empty state)."""
    zone = _care_zone([])
    assert zone.count("<div class='card'>") == 16
    assert zone.count("no rollup yet") == 16
    assert "sdot" not in zone
    assert "no data yet" not in zone


def test_populated_colors_status_and_keeps_all_16_cards():
    """A populated store renders all 16 cards with per-specialist freshness: the
    four data-backed specialists carry a status dot + recency caption, the 12
    streamless ones read 'no data yet', and the static 'no rollup yet' is gone."""
    zone = _care_zone(_populated())
    assert zone.count("<div class='card'>") == 16
    assert "no rollup yet" not in zone
    assert zone.count("no data yet") == 12          # 16 - 4 data-backed
    assert zone.count("class='sdot ") == 16          # one status dot per card


def test_freshness_states_render_distinct_status_dots():
    """current/stale/dormant/none map to the right data-state dot: labs+trainer
    current (good), peptide stale (watch), medical-liaison dormant + the 12
    streamless none (muted)."""
    zone = _care_zone(_populated())
    assert zone.count("sdot-current") == 2           # panel today + training 3d ago
    assert zone.count("sdot-stale") == 1             # watch-out 40d ago
    assert zone.count("sdot-none") == 13             # feedback 90d (dormant) + 12 streamless


def test_recency_captions_state_the_exact_age():
    """The status caption is the literal age the dot bands; dormant data still
    shows its age (not 'no data yet')."""
    zone = _care_zone(_populated())
    assert "updated today" in zone                   # panel::cbc at _day(0)
    assert "updated 3d ago" in zone                  # calendar training at _day(3)
    assert "updated 40d ago" in zone                 # watch-out stale
    assert "updated 90d ago" in zone                 # feedback dormant (grey dot, dated caption)


def test_status_dot_is_data_state_never_accent():
    """The status dots use only the PALETTE data-state classes; no ACCENTS hex and
    no accent-category `tint-*` class leaks into the care-team zone (ADR-0009 D3)."""
    zone = _care_zone(_populated())
    for accent in component_set.ACCENTS.values():
        assert accent not in zone, f"accent {accent} leaked into the care-team zone"
    assert "tint-" not in zone


def test_no_raw_store_key_leaks_in_zone():
    """No raw store key (item prefix or calendar item) ever reaches the rendered zone."""
    zone = _care_zone(_populated())
    for key in ("panel::", "watch-out::", "feedback::", "calendar::events", "plan::"):
        assert key not in zone, f"raw store key {key!r} leaked into the care-team zone"
