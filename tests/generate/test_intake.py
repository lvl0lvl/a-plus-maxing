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


def test_intake_emits_self_contained_file(tmp_path):
    """generate.run -> render.emit RAISES on any external asset; a clean emit proves self-contained."""
    path = generate.run("intake", _root=tmp_path / "store", _out_dir=tmp_path / "out",
                        _dna_root=tmp_path / "dna", _labs_root=tmp_path / "labs")
    assert path.exists() and path.name == "intake.html"
