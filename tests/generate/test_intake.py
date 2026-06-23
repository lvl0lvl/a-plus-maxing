"""Intake wizard render tests — the 6-step shell + the LIVE Step-1 load-state cards.

The wizard chrome + steps 2-6 are static shell; Step 1's "Link your documents" cards are
driven by the real ingestion load-state (wearable from the store, DNA/labs from the
dropzones), injected by `generate.run('intake')`.
"""

from scripts.generate import generate
from scripts.ingest import ingest
from scripts.ingest.adapters import healthkit
from vault.design.templates import intake

_HK_HRV = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"


def _hk_export(path, rows):
    recs = "".join(
        f'<Record type="{t}" startDate="{d} 08:00:00 -0500" value="{v}"/>\n' for t, d, v in rows)
    path.write_text(f'<?xml version="1.0"?>\n<HealthData>\n{recs}</HealthData>\n')


def test_intake_renders_all_six_steps_and_chrome():
    html = intake.render([])
    for n in range(1, 7):
        assert f"Step {n} of 6" in html
    for label in intake._STEPS:
        assert label in html
    assert "Build your plan" in html
    assert "nothing is uploaded" in html


def test_intake_step1_wearable_card_live_when_loaded(tmp_path):
    """The wearable card reflects the real store: a transposed source-count would red this."""
    store_root = tmp_path / "store"
    export = tmp_path / "export.xml"
    _hk_export(export, [(_HK_HRV, "2026-01-01", "55"), (_HK_HRV, "2026-01-02", "60")])
    ingest.run(healthkit.HealthKitAdapter(), export, root=store_root)
    path = generate.run("intake", _root=store_root, _out_dir=tmp_path / "out",
                        _dna_root=tmp_path / "dna", _labs_root=tmp_path / "labs")
    html = path.read_text()
    assert "healthkit · 2 readings" in html   # the live count, from the store
    assert "✓ loaded" in html


def test_intake_step1_wearable_not_loaded_shows_load_command(tmp_path):
    path = generate.run("intake", _root=tmp_path / "store", _out_dir=tmp_path / "out",
                        _dna_root=tmp_path / "dna", _labs_root=tmp_path / "labs")
    html = path.read_text()
    assert "python -m scripts.ingest export.xml" in html
    assert "Not linked" in html


def test_intake_dna_card_reflects_dropzone(tmp_path):
    dna_root = tmp_path / "dna"
    dna_root.mkdir()
    (dna_root / "genome.txt").write_text("# rsid\nrs1\t1\t1\tAA\n")
    path = generate.run("intake", _root=tmp_path / "store", _out_dir=tmp_path / "out",
                        _dna_root=dna_root, _labs_root=tmp_path / "labs")
    assert "genome.txt landed" in path.read_text()


def test_intake_escapes_dropzone_filenames(tmp_path):
    """A dropzone filename with HTML-special chars is escaped, not injected raw into the page."""
    dna_root = tmp_path / "dna"
    dna_root.mkdir()
    (dna_root / "x&y<z>.txt").write_text("# rsid\nrs1\t1\t1\tAA\n")
    path = generate.run("intake", _root=tmp_path / "store", _out_dir=tmp_path / "out",
                        _dna_root=dna_root, _labs_root=tmp_path / "labs")
    html = path.read_text()
    assert "x&amp;y&lt;z&gt;.txt" in html       # escaped
    assert "x&y<z>.txt landed" not in html      # never the raw string


def test_intake_markup_has_no_double_escaped_ampersand():
    """FIX-D: no placeholder/label renders a double-escaped ampersand (`&amp;amp;`).

    A pre-escaped string (`"name &amp; dose"`) passed where `_esc` escapes it again
    renders the literal `name &amp; dose` in the browser (the `&amp;amp;` artifact).
    The peptide placeholder hit this; assert the rendered HTML carries no `&amp;amp;`.
    """
    html = intake.render([])
    assert "&amp;amp;" not in html, "a pre-escaped string was escaped again (double-escape bug)"


# The four Step-1 demographic form field names (ADR-0018-T1): the activated objective-only
# form's ONLY capture fields. Birth year writes the `date-of-birth` raw source.
_DEMOGRAPHIC_FORM_NAMES = ("date-of-birth", "sex-for-dosing", "bodyweight-band", "equipment-access-class")
# The rich-section capture tokens that are now CHAT-only — they must NOT render as form
# fields (ADR-0018-T1 form-objective-only). Drawn from the wired/free-text token sets that
# were the old Steps 2-5 fields, minus the demographic tokens this task adds.
_CHAT_ONLY_TOKENS = ("goal-domains", "goal-targets", "goal-priority-order", "hard-limits",
                     "recovery-status-band", "train-around")


def test_intake_markup_form_fields_match_capture_demographic_tokens():
    """ADR-0018-T1: the activated form renders the four demographic inputs, 0 rich-section field.

    The form is OBJECTIVE-ONLY (ADR-0018-T1): only the four Step-1 demographic fields are
    rendered capture inputs; the rich-section tokens (goals/training/nutrition/supplements)
    moved to the `/chat` panel. Updated from FIX-E2 (which asserted every WIRED_TOKENS member
    rendered) to the new objective-only contract — a re-point to the new sourcing, not a
    weakening: it still REDs if a demographic field name typo'd, AND newly REDs if a
    rich-section field crept back onto the form.

    Failing-capable: rename a demographic markup field and the positive assertion reds; add a
    rich-section field back to the form and the negative assertion reds.
    """
    html = intake.render([])
    # Positive: each demographic field is a rendered capture input (markup<->token seam).
    for token in _DEMOGRAPHIC_FORM_NAMES:
        assert f"name='{token}'" in html, (
            f"the demographic token {token!r} has no rendered form field (markup<->token seam broken)"
        )
    # Negative (the objective-only contract): 0 rich-section token renders as a form field.
    for token in _CHAT_ONLY_TOKENS:
        assert f"name='{token}'" not in html, (
            f"the rich-section token {token!r} still renders as a form field (form not objective-only)"
        )


def test_intake_step5_subtitle_is_record_only_honest():
    """F6: the Step-5 subtitle makes no present-tense screening promise the form cannot keep.

    The rx-interaction form field routes RECORD-ONLY (Wave-B FIX-A) — its label says
    "saved to your record" and the panel recnote says the raw stack is "not yet used by the
    plan". The old subtitle ("interactions are screened before anything is recommended")
    asserted a screening capability the form no longer performs. Assert the dishonest
    present-tense promise is gone and the honest record-only text is rendered.

    Failing-capable: restore the old "screened before anything is recommended" subtitle and
    the negative assertion reds.
    """
    html = intake.render([])
    assert "screened before anything is recommended" not in html, (
        "the Step-5 subtitle still promises present-tense interaction screening the form does not perform"
    )
    assert "interaction screening runs later, in plan generation" in html, (
        "the Step-5 subtitle does not carry the honest record-only screening statement"
    )


def test_intake_demographic_selects_have_associated_labels():
    """ADR-0018-T1: each Step-1 demographic select has a programmatically associated label.

    Replaces FIX-F2's goal-domains fieldset/legend check: the goal-domains checkbox group is
    now CHAT-only (the form is objective-only), so its fieldset is gone — not weakened, the
    feature moved. The activated Step-1 demographic selects keep the accessible group
    semantics: each `<select name='<demographic>'>` is paired with a `<label for='<demographic>'>`
    (the `_select_field` helper's `for=`/`id=` association). Assert the label association for
    each bounded demographic select.

    Failing-capable: drop the `for=`/`id=` association in `_select_field` and this reds.
    """
    html = intake.render([])
    for name in ("sex-for-dosing", "bodyweight-band", "equipment-access-class"):
        assert f"<label for='{name}'>" in html, (
            f"the {name!r} demographic select has no associated <label for=...>"
        )
        assert f"id='{name}' name='{name}'" in html, (
            f"the {name!r} select's id/name do not match its label association"
        )


def test_intake_inputs_have_a_visible_focus_ring():
    """FIX-F1: the input focus state adds a visible ring (not the border swap alone).

    WCAG 2.4.7 / 1.4.11: a 1px border-color swap is not a sufficient focus indicator.
    Assert the `:focus` rule carries a `box-shadow` ring.
    """
    html = intake.render([])
    focus_rule = html[html.index(".inp:focus"):]
    focus_rule = focus_rule[:focus_rule.index("}")]
    assert "box-shadow" in focus_rule, "the input :focus state has no visible focus ring"


def test_intake_emits_self_contained_file(tmp_path):
    """generate.run -> render.emit RAISES on any external asset; a clean emit proves self-contained."""
    path = generate.run("intake", _root=tmp_path / "store", _out_dir=tmp_path / "out",
                        _dna_root=tmp_path / "dna", _labs_root=tmp_path / "labs")
    assert path.exists() and path.name == "intake.html"
