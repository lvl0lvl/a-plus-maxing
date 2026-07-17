"""Render-faithfulness tests for the credential-onboarding UI (ADR-0048-T4).

Two SERVED surfaces of the SPA (`vault/design/templates/app_view.html`, rendered by
`app_shell.render` -> `generate.run('app')`), faithful to the operator-signed-off mockup
`prototype/credential-onboarding-mockup.html`:

  * Surface A -- the `screen-wizard` step 9 ("Connect your data & keys"), PRESERVED in every
    render, so it is asserted against `app_shell.render([])` (the locked first-run body).
  * Surface B -- the `screen-profile` "Connections & Keys" panel, one of the four platform
    screens stripped when the profile is incomplete, so it is asserted against
    `app_shell.render(_complete_profile_readings())` (the unlocked full shell).

Per-source connection status is CLIENT-SIDE: a `fetch('/settings/trackers')`-on-load handler
sets each OAuth source's status/affordance (mirroring the `/settings/key` pill). No route,
no credential, no `client_id`/`client_secret` field is rendered. All fixture-driven: 0 live
network, 0 key read, 0 spend (the status fetch is client-side JS, never executed here).
"""

import re
import subprocess
from pathlib import Path

from scripts.generate import generate
from vault.design.templates import app_shell
from tests.serve.test_app_shell import _complete_profile_readings, _seed_complete_profile

REPO_ROOT = Path(__file__).resolve().parents[2]

# The frozen ADR-0032 spine (six byte-frozen files) + its fork-point (recipe frontmatter).
_FORKPOINT = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
_FROZEN_SIX = (
    "scripts/store/store.py",
    "scripts/store/keying.py",
    "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    "scripts/plan/router.py",
)

# An INPUT (not prose) whose name/id declares an OAuth client credential -- the AC-4 hazard.
_SECRET_INPUT = re.compile(r'<input[^>]*\b(?:name|id)="[^"]*client_(?:id|secret)', re.IGNORECASE)


def _surface_a():
    """The locked first-run body: `screen-wizard` (with step 9) is preserved, platforms stripped."""
    return app_shell.render([])


def _surface_b():
    """The unlocked full shell: a complete profile keeps `screen-profile` (Surface B) in the body."""
    return app_shell.render(_complete_profile_readings())


def _step9_region(html):
    """Slice the wizard step-9 `wstep` out of the rendered SPA (up to the following screen)."""
    start = html.index('data-step="9"')
    return html[start:html.index('id="screen-equipment"', start)]


def _profile_region(html):
    """Slice `screen-profile` (Surface B) out of the unlocked body (up to the following screen)."""
    start = html.index('id="screen-profile"')
    return html[start:html.index('id="screen-wizard"', start)]


def _stepper_step9_label(html):
    """The stepper's `data-go="9"` button label text (positive-identity check for AC-1)."""
    m = re.search(r'data-go="9"[^>]*>\s*<span class="step-num">9</span>([^<]*)</button>', html)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# AC-1 -- Surface A step 9 renders "Connect your data & keys" + all elements
# --------------------------------------------------------------------------- #
def test_ac1_surface_a_step9_connect_your_data_and_keys():
    """AC-1: step-9 h1 + stepper label EQUAL the new title; all Surface-A elements render.

    Positive identity (S1): assert the h1/label EQUAL "Connect your data & keys" -- NOT the
    absence of "API key" (which legitimately persists as the BYO input label + the "AI model
    key" seclab). Falsifier: drop any enumerated element -> RED.
    """
    html = _surface_a()
    region = _step9_region(html)
    # step h1 + stepper label EQUAL the new title (positive identity)
    assert '<div class="h1">Connect your data &amp; keys</div>' in region
    assert _stepper_step9_label(html) == "Connect your data &amp; keys"
    # the four wearable connect cards, by conn-name
    for name in ("Whoop", "Oura", "Garmin", "Google Health"):
        assert f">{name}<" in region, f"missing Surface-A wearable card: {name}"
    # the Oura PAT paste affordance
    assert "Paste it instead" in region
    # the Apple Health Shortcut affordance
    assert "Get the Shortcut" in region
    # the D5 key choice -- both branches
    assert "shared alpha key" in region.lower()
    assert "bring my own key" in region.lower()
    # the header stays "Step 1 of 9" (already a 9-step flow; no renumber)
    assert "Step 1 of 9" in html


# --------------------------------------------------------------------------- #
# AC-2 -- Surface B panel + client-side status hook (+ co-located Wave-6 negative)
# --------------------------------------------------------------------------- #
def test_ac2_surface_b_connections_panel_and_status_hook():
    """AC-2: the "Connections & Keys" panel (`.set-tab` sub-tabs), per-source rows, the PAT
    update, the AI model key card, AND the `fetch('/settings/trackers')` status hook render.

    Co-located NEGATIVE: NO Wave-6 "Update my plan now". Falsifiers: panel absent -> RED;
    inject "Update my plan now" -> the negative REDs; remove the fetch -> the hook REDs.
    """
    html = _surface_b()
    region = _profile_region(html)
    # the panel + the NEW .set-tab sub-tabs (NOT .ws-tab -- see AC-2b)
    assert "set-tabs" in region
    assert 'class="set-tab' in region
    assert "Connections &amp; Keys" in region
    # per-source rows by name
    for name in ("Whoop", "Oura", "Garmin", "Google Health", "Apple Health"):
        assert name in region, f"missing Surface-B source row: {name}"
    # the four OAuth rows the status JS drives, keyed to the /settings/trackers source keys
    for src in ("whoop", "oura", "garmin", "google-health"):
        assert f'data-src="{src}"' in region, f"missing OAuth status row: {src}"
    # the Oura PAT update affordance + the AI model key card
    assert "Update token" in region
    assert "AI model key" in region
    assert "shared alpha key" in region.lower()
    # the client-side status hook is wired (not a dead server render-seam)
    assert "fetch('/settings/trackers')" in html
    # co-located negative: the Wave-6 "Plan updates" section is NOT here
    assert "Update my plan now" not in html


# --------------------------------------------------------------------------- #
# AC-2b -- Surface B sub-tabs use .set-tab, never the global .ws-tab sweep
# --------------------------------------------------------------------------- #
def test_ac2b_no_ws_tab_collision_in_screen_profile():
    """AC-2b (D4 blocker): the unlocked body has EXACTLY ONE `class="ws-tab active"` (the
    workspace My-Info tab), AND the `screen-profile` slice has ZERO `class="ws-tab"` (active
    OR inactive) -- proving Surface-B's sub-tabs are `.set-tab`, not the `.ws-tab` the global
    `document.querySelectorAll('.ws-tab')` sweep drives. Falsifier: author them with `.ws-tab`
    -> the slice count >= 1 (and the active-count 2) -> RED.
    """
    html = _surface_b()
    region = _profile_region(html)
    assert html.count('class="ws-tab active"') == 1
    assert 'class="ws-tab' not in region


# --------------------------------------------------------------------------- #
# AC-3 -- skippable: the advance affordance + optional connect cards
# --------------------------------------------------------------------------- #
def test_ac3_skippable_connections_optional():
    """AC-3: step 9 renders the "Save & review ->" advance affordance and the connect cards
    carry no connection-gate (no `required`) -- a 0-connection render advances. Falsifier:
    gate advancement on a connection (a `required` attribute) -> RED.
    """
    region = _step9_region(_surface_a())
    assert "Save &amp; review" in region
    assert "show('equipment')" in region
    assert "required" not in region


# --------------------------------------------------------------------------- #
# AC-4 -- no client-secret field on EITHER surface (co-located with the positive)
# --------------------------------------------------------------------------- #
def test_ac4_no_client_secret_field_either_surface():
    """AC-4 (load-bearing): neither surface renders a `client_id`/`client_secret` INPUT
    (input-scoped, so the faithful prose "you never enter a client ID or a secret" does not
    false-RED). Co-located positive: the AI model key card + "shared alpha key" + the
    `a-plus-maxing-api-key` keychain note. Falsifier: inject a client_secret input -> RED.
    """
    for label, html in (("surface-a", _surface_a()), ("surface-b", _surface_b())):
        assert not _SECRET_INPUT.search(html), f"{label} renders a client-secret input"
        # co-located positive (the swappable D5 key card)
        assert "AI model key" in html, f"{label} missing the AI model key card"
        assert "shared alpha key" in html.lower(), f"{label} missing the shared-alpha choice"
        assert "a-plus-maxing-api-key" in html, f"{label} missing the keychain note"


# --------------------------------------------------------------------------- #
# AC-5 -- Garmin manual path (the discriminating note, not a bare one-click)
# --------------------------------------------------------------------------- #
def test_ac5_garmin_manual_path():
    """AC-5: Garmin's step-9 card renders the DISCRIMINATING "sign-in differs / token paste"
    note, not a bare one-click identical to Whoop's. Falsifier: render Garmin identical to the
    one-click cards (drop the note) -> RED.
    """
    region = _step9_region(_surface_a())
    assert "Garmin" in region
    assert "sign-in differs" in region


# --------------------------------------------------------------------------- #
# AC-6 -- the frozen ADR-0032 six are untouched
# --------------------------------------------------------------------------- #
def test_ac6_frozen_six_untouched():
    """AC-6: `git diff --numstat <forkpoint> -- <six>` prints nothing. Falsifier: any edit to a
    frozen file -> a numstat row -> RED.
    """
    result = subprocess.run(
        ["git", "diff", "--numstat", _FORKPOINT, "--", *_FROZEN_SIX],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == "", f"frozen-six changed:\n{result.stdout}"


# --------------------------------------------------------------------------- #
# AC-7 -- inline-only via the real emit probe; BOTH surfaces present
# --------------------------------------------------------------------------- #
def test_ac7_inline_only_emit_both_surfaces(tmp_path):
    """AC-7 (AUTHORITATIVE inline-only): `generate.run('app')` drives `render.emit`, which RAISES
    `ValueError` on any off-file asset ref. A returned Path that EXISTS therefore proves the two
    new surfaces added 0 external references. The written SPA carries BOTH surfaces. Falsifier: a
    CDN/off-file ref in the new markup -> emit RAISES -> RED (mirrors test_app_shell.py:112).
    """
    _seed_complete_profile(tmp_path / "store")
    path = generate.run(
        "app",
        _root=tmp_path / "store",
        _out_dir=tmp_path / "out",
        _dna_root=tmp_path / "dna",
        _labs_root=tmp_path / "labs",
    )
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit (off-file ref?)"
    written = path.read_text()
    assert "Connect your data &amp; keys" in written  # Surface A step 9
    assert "Connections &amp; Keys" in written  # Surface B panel
