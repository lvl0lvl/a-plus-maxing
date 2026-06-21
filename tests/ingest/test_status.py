"""Ingestion load-state resolver tests — counts/presence only, never values or content."""

from scripts.ingest import status


def _hk(item, day, value):
    return {"item": item, "timepoint": f"{day} 08:00:00 -0500", "source": "healthkit", "value": value}


def test_wearable_loaded_reports_count_items_range(tmp_path):
    store_read = [_hk("hrv", "2026-01-01", 55), _hk("hrv", "2026-01-03", 60), _hk("rhr", "2026-01-02", 48)]
    out = status.resolve(store_read, dna_root=tmp_path / "dna", labs_root=tmp_path / "labs")
    assert out["wearable"]["loaded"] is True
    assert out["wearable"]["count"] == 3
    assert out["wearable"]["items"] == ["hrv", "rhr"]
    assert out["wearable"]["range"] == ("2026-01-01", "2026-01-03")
    assert out["wearable"]["source"] == "healthkit"


def test_empty_store_and_missing_dropzones_all_not_loaded(tmp_path):
    out = status.resolve([], dna_root=tmp_path / "nope-dna", labs_root=tmp_path / "nope-labs")
    assert out["wearable"]["loaded"] is False
    assert out["dna"] == {"loaded": False, "files": []}
    assert out["labs"] == {"loaded": False, "files": []}


def test_dna_dropzone_detects_landed_file(tmp_path):
    dna_root = tmp_path / "dna"
    dna_root.mkdir()
    (dna_root / "genome.txt").write_text("# rsid ...\n")
    out = status.resolve([], dna_root=dna_root, labs_root=tmp_path / "labs")
    assert out["dna"]["loaded"] is True
    assert out["dna"]["files"] == ["genome.txt"]


def test_labs_dropzone_accepts_pdf_csv_excludes_others(tmp_path):
    labs = tmp_path / "labs"
    labs.mkdir()
    (labs / "panel.pdf").write_bytes(b"%PDF")
    (labs / "markers.csv").write_text("a,b\n")
    (labs / "ignore.md").write_text("notes")
    out = status.resolve([], dna_root=tmp_path / "dna", labs_root=labs)
    assert out["labs"]["loaded"] is True
    assert out["labs"]["files"] == ["markers.csv", "panel.pdf"]   # .md excluded; sorted
