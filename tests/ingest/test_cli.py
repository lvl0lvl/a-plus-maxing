"""Operator ingestion CLI tests — `python -m scripts.ingest` auto-detect + dispatch.

Exercises the thin operator CLI over the UNCHANGED `ingest.run` (wearable) + `dna.land`
(DNA), against SYNTHETIC fixtures. The CLI's job is detection + dispatch + a load summary;
the underlying parse/store/land paths are covered by their own suites.
"""

import zipfile

import pytest

from conftest import hk_record, write_healthkit_export
from scripts.ingest import __main__ as cli
from scripts.store import store

_HK_HRV = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"


def test_cli_loads_apple_health_xml_into_store(tmp_path, capsys):
    """An Apple Health export.xml auto-detects as healthkit and lands in the store."""
    export = tmp_path / "export.xml"
    write_healthkit_export(export, [hk_record(_HK_HRV, "2026-01-01 08:00:00 -0500", "55")])
    store_root = tmp_path / "store"
    rc = cli.main([str(export), "--root", str(store_root)])   # no --source: auto-detect .xml
    assert rc == 0
    assert len(store.read("hrv", root=store_root)) == 1
    out = capsys.readouterr().out
    assert "healthkit" in out and "hrv" in out and "nothing was uploaded" in out


def test_cli_lands_dna_zip_into_dropzone(tmp_path, capsys):
    """A DNA .zip auto-detects as dna and lands in the dropzone, reporting variant count only."""
    src = tmp_path / "23andme.zip"
    rows = "rs4477212\t1\t82154\tAA\nrs3094315\t1\t752566\tAG\n"
    with zipfile.ZipFile(src, "w") as zf:
        zf.writestr("genome.txt", "# rsid\tchromosome\tposition\tgenotype\n" + rows)
    dna_root = tmp_path / "dna"
    rc = cli.main([str(src), "--dna-root", str(dna_root)])     # .zip auto-detects dna
    assert rc == 0
    assert (dna_root / "genome.txt").exists()
    out = capsys.readouterr().out
    assert "2 variant" in out and "nothing was uploaded" in out


def test_cli_source_override_forces_adapter(tmp_path):
    """--source forces the adapter rather than relying on extension auto-detect."""
    export = tmp_path / "export.xml"
    write_healthkit_export(export, [hk_record(_HK_HRV, "2026-01-03 08:00:00 -0500", "58")])
    store_root = tmp_path / "store"
    rc = cli.main([str(export), "--source", "healthkit", "--root", str(store_root)])
    assert rc == 0 and len(store.read("hrv", root=store_root)) == 1


def test_cli_missing_file_exits(tmp_path):
    """A missing path exits non-zero with a clear message (never a traceback for the obvious case)."""
    with pytest.raises(SystemExit):
        cli.main([str(tmp_path / "nope.xml")])


def test_cli_ambiguous_extension_requires_source(tmp_path):
    """A `.json` is oura|garmin — auto-detect refuses and asks for --source rather than guess."""
    ambiguous = tmp_path / "data.json"
    ambiguous.write_text("[]")
    with pytest.raises(SystemExit):
        cli.main([str(ambiguous)])
