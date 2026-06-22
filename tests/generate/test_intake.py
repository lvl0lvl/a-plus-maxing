"""Intake wizard render tests — the 6-step shell + the LIVE Step-1 load-state cards.

The wizard chrome + steps 2-6 are static shell; Step 1's "Link your documents" cards are
driven by the real ingestion load-state (wearable from the store, DNA/labs from the
dropzones), injected by `generate.run('intake')`.
"""

from scripts.generate import generate
from scripts.ingest import ingest
from scripts.ingest.adapters import healthkit
from scripts.serve import capture
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


def test_intake_markup_form_fields_match_capture_wired_tokens():
    """FIX-E2: every wired capture token (+ `train-around`) is a rendered form field.

    Closes the markup<->token wiring seam: a field-name typo in the markup would
    silently break the capture round-trip with the suite otherwise green. Assert each
    `capture.WIRED_TOKENS` member and `train-around` appears as a `name='<token>'`
    attribute in the rendered HTML. Failing-capable: rename a markup field and this reds.
    """
    html = intake.render([])
    for token in (*capture.WIRED_TOKENS, "train-around"):
        assert f"name='{token}'" in html, (
            f"the wired token {token!r} has no rendered form field (markup<->token seam broken)"
        )


def test_intake_goal_domains_group_has_fieldset_legend():
    """FIX-F2: the goal-domains checkbox group is a `<fieldset>` with a `<legend>`.

    Group semantics: the chip group's purpose is programmatically associated so the
    grouping is conveyed to assistive tech. Assert the rendered markup wraps the
    `goal-domains` checkboxes in a fieldset whose legend names the group.
    """
    html = intake.render([])
    assert "<fieldset" in html and "<legend" in html, "the goal-domains group is not a fieldset/legend"
    # The legend names the group, and the group contains the goal-domains checkboxes.
    fs_start = html.index("<fieldset")
    fs_end = html.index("</fieldset>", fs_start)
    group = html[fs_start:fs_end]
    assert "Goal areas" in group, "the goal-domains group legend does not name the group"
    assert "name='goal-domains'" in group, "the fieldset does not wrap the goal-domains checkboxes"


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
