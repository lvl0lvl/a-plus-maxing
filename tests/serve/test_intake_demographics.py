"""Step-1 demographic activation tests (ADR-0018-T1).

This task lights the four orphan `SUMMARY_FIELD_SET` demographic tokens — `training-age-band`,
`sex-for-dosing`, `bodyweight-band`, `equipment-access-class` — by activating the Step-1
"About you" demographic layer of the intake form. Each demographic input POSTs into the
capture form, `capture.persist_capture` routes it BY ITS DATA CLASS, and `summarize`
derives each token from a real submitted value (0 orphans, against today's baseline of 4).

Cycle 1 (AC-1, AC-2, AC-3) — the per-token round-trip + de-identification + the
`equipment-access-class` source reconciliation:
  - AC-1 (orphan-lit): each of the four tokens resolves through `summarize` from a real
    Step-1 demographic POST. Each token carries a one-time negative control proving the
    round-trip assertion is failing-capable, not constant-true.
  - AC-2 (per-token de-identification): a crafted raw value at the source -> 0 raw value in
    the emitted token (an INDEPENDENT per-token output scan; the derived path runs no 8j6 scan).
  - AC-3 (reconciliation): `equipment-access-class` derives from the demographic equipment
    selection AND `import scripts.plan.router` loads clean (the disjointness tripwires green);
    `postal-address` no longer maps to `equipment-access-class`.

Cycle 2 (AC-4, AC-5, AC-6) — Step-1 markup activation + form objective-only + markup<->gate
no-drift (in the second test block below).
"""

import functools
import importlib

from scripts.plan import router
from scripts.plan.router import SUMMARY_FIELD_SET, summarize
from scripts.serve import capture
from scripts.store import store

# An identity config ABSENT on disk: identity-token detection is empty (the fresh-clone
# posture), while the value-class patterns (any-domain email, phone, postal) still run.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"

# The four demographic FORM fields -> their submitted (de-identified) values. Birth year
# writes the named-excluded `date-of-birth` raw source (summarize derives training-age-band);
# the other three are bounded pass-through tokens written under their own name.
_BIRTH_YEAR_VALUE = "1986"  # a 4-digit birth year -> date-of-birth store item -> born-1980s
_SEX_VALUE = "male"
_BODYWEIGHT_BAND_VALUE = "80-90kg"
_EQUIPMENT_VALUE = "full-home-gym"

# Each orphan token paired with the resolved value `summarize` must return for it.
_TOKEN_EXPECTED = {
    "training-age-band": "born-1980s",
    "sex-for-dosing": _SEX_VALUE,
    "bodyweight-band": _BODYWEIGHT_BAND_VALUE,
    "equipment-access-class": _EQUIPMENT_VALUE,
}

# The demographic FORM fields POSTed for each token (the field name the capture seam reads).
_DEMOGRAPHIC_FIELDS = {
    "date-of-birth": _BIRTH_YEAR_VALUE,  # birth year -> the raw date-of-birth source item
    "sex-for-dosing": _SEX_VALUE,
    "bodyweight-band": _BODYWEIGHT_BAND_VALUE,
    "equipment-access-class": _EQUIPMENT_VALUE,
}


def _bound(root):
    """The instance-bound store_read `summarize` requires (recipe caller contract)."""
    return functools.partial(store.read, root=root)


def _summary(root):
    """Run `summarize` over a tmp instance with an absent identity config."""
    return summarize(_bound(root), identity_config=_ABSENT_IDENTITY)


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 orphan-lit: each of the four tokens derives from a real input
# --------------------------------------------------------------------------- #


def test_four_orphan_tokens_are_field_set_members():
    """AC-1: the four demographic tokens are SUMMARY_FIELD_SET members (the orphans being lit)."""
    for token in _TOKEN_EXPECTED:
        assert token in SUMMARY_FIELD_SET, f"{token!r} is not a SUMMARY_FIELD_SET token"


def test_each_demographic_token_resolves_from_a_real_post(tmp_path):
    """AC-1 (orphan-lit): each of the four tokens resolves through summarize from a Step-1 POST.

    POST the Step-1 demographic fields through `persist_capture` into a tmp store, then
    assert `summarize` returns EACH of the four demographic tokens resolved from the
    submitted value (0 of the four stays orphaned). The birth-year field writes the
    `date-of-birth` raw source item that summarize DERIVES into `training-age-band`; the
    other three are pass-through tokens read under their own name.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        dict(_DEMOGRAPHIC_FIELDS), root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )

    summary = _summary(store_root)
    orphaned = [t for t in _TOKEN_EXPECTED if summary.get(t) != _TOKEN_EXPECTED[t]]
    assert not orphaned, f"these demographic tokens stayed orphaned (no producer): {orphaned}"
    for token, expected in _TOKEN_EXPECTED.items():
        assert summary.get(token) == expected, (
            f"summarize did not resolve {token!r} from the Step-1 POST (got {summary.get(token)!r})"
        )


def test_birth_year_writes_date_of_birth_source_never_training_age_band(tmp_path):
    """AC-1 / contract: birth year writes the date-of-birth RAW source, never training-age-band.

    The birth-year field is a wired DERIVED field — it writes the named-excluded
    `date-of-birth` raw source item (which summarize derives into `training-age-band` via
    `_age_band`), NOT the `training-age-band` token directly. Mirrors the
    `train-around -> raw-symptom-free-text` special-case.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"date-of-birth": _BIRTH_YEAR_VALUE},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The raw source item is written under date-of-birth, NOT training-age-band.
    assert store.read("date-of-birth", root=store_root), "birth year did not write the date-of-birth source item"
    assert store.read("training-age-band", root=store_root) == [], (
        "birth year wrongly wrote training-age-band directly (must be derived, not stored)"
    )
    summary = _summary(store_root)
    assert summary.get("training-age-band") == "born-1980s", (
        "summarize did not derive training-age-band from the date-of-birth source item"
    )


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 NEGATIVE CONTROLS (one per token, proving failing-capable)
# --------------------------------------------------------------------------- #
# Each control runs the round-trip assertion against an UN-submitted seam (no POST of
# that field) and confirms the token does NOT resolve — proving the orphan-lit assertion
# above is failing-capable (it goes RED when the token has no producer), not constant-true.


def test_negative_control_sex_unwired_stays_orphaned(tmp_path):
    """AC-1 negative control: with NO sex POST, `sex-for-dosing` does not resolve (orphaned)."""
    store_root = tmp_path / "store"
    # POST every demographic field EXCEPT sex-for-dosing.
    fields = {k: v for k, v in _DEMOGRAPHIC_FIELDS.items() if k != "sex-for-dosing"}
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = _summary(store_root)
    assert summary.get("sex-for-dosing") is None, (
        "sex-for-dosing resolved with no producer — the orphan-lit assertion is not failing-capable"
    )


def test_negative_control_bodyweight_unwired_stays_orphaned(tmp_path):
    """AC-1 negative control: with NO bodyweight POST, `bodyweight-band` does not resolve."""
    store_root = tmp_path / "store"
    fields = {k: v for k, v in _DEMOGRAPHIC_FIELDS.items() if k != "bodyweight-band"}
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = _summary(store_root)
    assert summary.get("bodyweight-band") is None, (
        "bodyweight-band resolved with no producer — the orphan-lit assertion is not failing-capable"
    )


def test_negative_control_equipment_unwired_stays_orphaned(tmp_path):
    """AC-1 negative control: with NO equipment POST, `equipment-access-class` does not resolve."""
    store_root = tmp_path / "store"
    fields = {k: v for k, v in _DEMOGRAPHIC_FIELDS.items() if k != "equipment-access-class"}
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = _summary(store_root)
    assert summary.get("equipment-access-class") is None, (
        "equipment-access-class resolved with no producer — the orphan-lit assertion is not failing-capable"
    )


def test_negative_control_training_age_unwired_stays_orphaned(tmp_path):
    """AC-1 negative control: with NO birth-year POST, `training-age-band` does not resolve."""
    store_root = tmp_path / "store"
    fields = {k: v for k, v in _DEMOGRAPHIC_FIELDS.items() if k != "date-of-birth"}
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = _summary(store_root)
    assert summary.get("training-age-band") is None, (
        "training-age-band resolved with no producer — the orphan-lit assertion is not failing-capable"
    )


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-2 per-token de-identification (independent per-token output scan)
# --------------------------------------------------------------------------- #


def test_birth_year_raw_value_never_appears_in_training_age_band(tmp_path):
    """AC-2: a crafted full DOB at the source -> 0 raw DOB in the training-age-band token.

    Seed a full birth date with a distinctive sentinel year at the `date-of-birth` source;
    `summarize` must emit `training-age-band` as a born-decade band (`born-NNN0s`) with the
    raw DOB value NOWHERE in the token. The derived path runs NO 8j6 scan, so this
    INDEPENDENT per-token output scan is the de-identification proof.
    """
    store_root = tmp_path / "store"
    crafted = "1986-04-12"  # a full DOB string — the day/month must never survive into the token
    capture.persist_capture(
        {"date-of-birth": crafted},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    token = _summary(store_root).get("training-age-band")
    assert token == "born-1980s", f"training-age-band was not the born-decade band (got {token!r})"
    assert "04" not in token and "12" not in token, "a raw DOB day/month survived into training-age-band"
    assert crafted not in token, "the raw DOB string survived into training-age-band"


def test_bodyweight_band_carries_no_raw_kg(tmp_path):
    """AC-2: the bodyweight-band token is a coarse band, never a raw kg value.

    The form submits a de-identified band (the band-select shape); the emitted token is the
    band itself. Assert the token equals the submitted band and that no raw-kg artifact
    (a bare 2-3 digit weight like `83`) reaches the token — the band is the coarsest unit.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"bodyweight-band": _BODYWEIGHT_BAND_VALUE},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    token = _summary(store_root).get("bodyweight-band")
    assert token == _BODYWEIGHT_BAND_VALUE, f"bodyweight-band stored the wrong value: {token!r}"
    # The band is a coarse range token, not a precise weight — assert it is in the bounded enum.
    assert token in capture.BODYWEIGHT_BANDS, "bodyweight-band is not a coarse enum band (raw-kg risk)"


def test_sex_and_equipment_carry_only_their_class(tmp_path):
    """AC-2: sex-for-dosing / equipment-access-class carry only their de-identified class token.

    Both are bounded pass-through tokens — the emitted token is exactly the submitted class,
    a member of its bounded enum (no raw free-text survives).
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"sex-for-dosing": _SEX_VALUE, "equipment-access-class": _EQUIPMENT_VALUE},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = _summary(store_root)
    assert summary.get("sex-for-dosing") == _SEX_VALUE
    assert summary.get("sex-for-dosing") in capture.SEX_OPTIONS, "sex-for-dosing is not a bounded class token"
    assert summary.get("equipment-access-class") == _EQUIPMENT_VALUE
    assert summary.get("equipment-access-class") in capture.EQUIPMENT_ACCESS_CLASSES, (
        "equipment-access-class is not a bounded class token"
    )


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-3 equipment-access-class source reconciliation
# --------------------------------------------------------------------------- #


def test_equipment_access_class_has_one_source_the_demographic_selection(tmp_path):
    """AC-3: equipment-access-class derives from the demographic selection, not postal-address.

    After the reconciliation the demographic equipment selection is the ONE source: a POST
    of the equipment select -> `summarize` returns the class. And `postal-address` no
    longer maps to `equipment-access-class` (the double-source is removed).
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"equipment-access-class": _EQUIPMENT_VALUE},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert _summary(store_root).get("equipment-access-class") == _EQUIPMENT_VALUE, (
        "equipment-access-class did not resolve from the demographic equipment selection"
    )
    # The double-source is reconciled: postal-address no longer maps to the token.
    assert router._RAW_TO_FIELD.get("postal-address") != "equipment-access-class", (
        "postal-address still maps to equipment-access-class — the double-source is not reconciled"
    )
    assert "equipment-access-class" not in router._FIELD_DERIVATION, (
        "equipment-access-class is still a derived field — it must be a pass-through token"
    )


def test_router_imports_clean_disjointness_tripwires_green():
    """AC-3: scripts.plan.router imports clean (the module-load disjointness tripwires hold).

    A reimport runs the L312-313 change-control asserts: `set(_RAW_TO_FIELD) <=
    EXCLUDED_RAW_PII` and `SUMMARY_FIELD_SET.isdisjoint(EXCLUDED_RAW_PII)`. The
    reconciliation must keep both green.
    """
    importlib.reload(router)  # re-runs the module-load tripwires; raises if either reds
    # postal-address stays named-excluded raw PII (still excluded, just not a derivation source).
    assert "postal-address" in router.EXCLUDED_RAW_PII, (
        "postal-address was wrongly dropped from EXCLUDED_RAW_PII (it stays named-excluded raw PII)"
    )
    assert set(router._RAW_TO_FIELD) <= set(router.EXCLUDED_RAW_PII)
    assert set(router.SUMMARY_FIELD_SET).isdisjoint(set(router.EXCLUDED_RAW_PII))


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-4 / AC-5 / AC-6 markup activation + form objective-only + no-drift
# --------------------------------------------------------------------------- #
import re

from vault.design.templates import intake

# The rich-section form field names that MUST NOT appear in the activated objective-only
# `capture_form` — they are CHAT-only (the Wave-A `/chat` panel) after activation.
_RICH_SECTION_NAMES = (
    "goal-domains", "goal-targets", "goal-priority-order", "hard-limits",
    "recovery-status-band", "train-around", "dietary-pattern", "meals-per-day",
    "allergies", "food-preferences", "supplement-stack", "peptide-stack",
    "rx-interaction-classes",
)

# The demographic FORM field names the activated Step-1 must POST (the capture contract).
_DEMOGRAPHIC_NAMES = ("date-of-birth", "sex-for-dosing", "bodyweight-band", "equipment-access-class")


def _capture_form_html(html):
    """Extract the POSTing `<form ... action='/upload' ...>...</form>` body from the render."""
    m = re.search(r"<form[^>]*action='/upload'[^>]*>(.*?)</form>", html, re.DOTALL)
    assert m is not None, "the render has no POSTing capture form (action='/upload')"
    return m.group(0)


def _form_field_names(form_html):
    """Every `name='...'` attribute submitted by the form (input/select/textarea)."""
    return set(re.findall(r"name='([^']+)'", form_html))


def test_capture_form_carries_the_four_demographic_inputs():
    """AC-4: the activated Step-1 demographic inputs POST inside `capture_form`.

    After activation the four demographic placeholders are real `name=` inputs INSIDE the
    POSTing form (not the dead `box ph` static boxes outside it). Assert every demographic
    field name appears in the capture form.
    """
    form = _capture_form_html(intake.render([]))
    names = _form_field_names(form)
    missing = [n for n in _DEMOGRAPHIC_NAMES if n not in names]
    assert not missing, f"the capture form does not POST these demographic inputs: {missing}"


def test_capture_form_is_objective_only_zero_rich_section_fields():
    """AC-4 / Risk Negative-1: the capture form carries 0 rich-section fields.

    Enumerate the POSTing form's field `name=` attributes and assert the set is EXACTLY the
    demographic names (rich-section goals/training/nutrition/supplement/peptide fields moved
    to the `/chat` panel). 0 rich-section `name=` may appear in the form.
    """
    form = _capture_form_html(intake.render([]))
    names = _form_field_names(form)
    leaked = [n for n in _RICH_SECTION_NAMES if n in names]
    assert not leaked, f"the objective-only form still carries rich-section fields: {leaked}"
    # The form's DATA-CAPTURE field names are EXACTLY the demographic set. `step` is the
    # Step-6 submit-button control (routes the /generate-plan handoff re-render), not a
    # rich-section data field — it is allowed; everything else must be a demographic input.
    capture_fields = names - {"step"}
    assert capture_fields == set(_DEMOGRAPHIC_NAMES), (
        f"the capture form's data fields are not exactly the demographic set: {sorted(capture_fields)}"
    )


def test_chat_panel_affordance_replaces_the_rich_sections():
    """AC-4: the form links to the Wave-A `/chat` panel in place of the rich sections.

    The rich sections are chat-only — the activated form carries a thin `/chat` affordance
    (a link/panel to the Wave-A route) so the operator reaches the conversational intake.
    """
    html = intake.render([])
    assert "/chat" in html, "the activated intake has no /chat panel affordance (the rich-section replacement)"


def test_content_upload_routes_through_route_upload_not_chat():
    """AC-5: a content upload routes through the unchanged `/upload` seam, never `/chat`.

    The capture form posts (multipart) to `/upload` — the `route.route_upload` content-upload
    seam (DNA/HealthKit/labs) — and the document-upload affordances (`_doc_cards`) remain. 0
    file-upload affordance routes through `/chat`. The byte-unchanged `route_upload` is the
    live E2E dispatch (covered in test_server.py); this asserts the form is wired to it.
    """
    html = intake.render([])
    form = _capture_form_html(html)
    assert "action='/upload'" in form, "the capture form does not POST to the /upload seam"
    assert "enctype='multipart/form-data'" in form, "the form is not multipart (no file-upload path)"
    # The document-upload affordances remain (the content-upload seam the form keeps).
    assert "Link your documents" in html, "the document-upload affordances were dropped"
    # No file-upload affordance routes through /chat (a file part posts to /upload, never chat).
    assert "action='/chat'" not in html, "a form posts files to /chat (must route through /upload)"
    # route_upload is the byte-unchanged reused seam.
    from scripts.serve import route
    assert hasattr(route, "route_upload"), "the route_upload content-upload seam is missing"


def test_demographic_select_options_are_built_from_the_gate_constants():
    """AC-6: the demographic `<select>` options are BUILT FROM the gate's enum constants.

    The Step-1 bounded selects (`sex-for-dosing`, `bodyweight-band`, `equipment-access-class`)
    render their `<option value=...>` set from the SAME constants the capture gate validates
    against (`capture.SEX_OPTIONS` / `BODYWEIGHT_BANDS` / `EQUIPMENT_ACCESS_CLASSES`, the
    `_BOUNDED_ENUMS`-backing constants) — 0 hardcoded option list that is not the gate
    constant. Mirrors the RECOVERY_STATUS_BANDS / GOAL_DOMAINS pattern. Reds if the markup
    drifts from the gate enum (an option value not in the constant, or a constant value with
    no option).
    """
    html = intake.render([])
    for name, constant in (
        ("sex-for-dosing", capture.SEX_OPTIONS),
        ("bodyweight-band", capture.BODYWEIGHT_BANDS),
        ("equipment-access-class", capture.EQUIPMENT_ACCESS_CLASSES),
    ):
        # Extract the <select name='<name>'>...</select> block and its option values.
        m = re.search(rf"<select[^>]*name='{re.escape(name)}'[^>]*>(.*?)</select>", html, re.DOTALL)
        assert m is not None, f"the {name!r} demographic select is not rendered"
        option_values = set(re.findall(r"<option value='([^']*)'", m.group(1)))
        # Drop the empty prompt option (value='') — the real options must EQUAL the gate constant.
        option_values.discard("")
        assert option_values == set(constant), (
            f"the {name!r} select options {sorted(option_values)} drifted from the gate "
            f"constant {sorted(constant)} (markup<->gate no-drift broken)"
        )
