"""Upload-routing seam tests (ADR-0013-T4).

`route.route_upload(staged_path, *, root, dna_root)` maps a staged upload to a
source by REUSING the CLI's `_EXT_SOURCE` / `_detect_source` (content-branching a
`.zip`: an Apple-Health-export shape -> healthkit; a 23andMe shape -> dna) and
dispatches into the UNCHANGED `ingest.run` (wearable) / `dna.land` (DNA). It adds
no extraction (an Apple-Health zip is passed AS-IS to the zip-aware healthkit
adapter, ADR-0013-T3) and defines NO second extension->source map (criterion 4 /
Risk reuse). The shared ingest routines stay byte-unchanged (criterion 6).

AC-1: a staged `export.xml` routes into `ingest.run` (healthkit) — `store.read`
returns the healthkit-mapped readings. AC-2: a staged DNA `.zip` (23andMe shape)
routes into `dna.land` — the landed file appears under `dna_root`. The Apple-Health
zip content-branch routes to healthkit (the disambiguation the website adds over the
CLI's `.zip -> dna` default). AC-4: `route.py` references `_EXT_SOURCE`/`_detect_source`
and carries 0 second extension->source map.
"""

import subprocess
import zipfile
from pathlib import Path

import pytest

from scripts.serve import route
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# The shared ingest routines this task must NOT touch (Risk 0-shared-routine-edit).
SHARED_ROUTINE_PATHS = (
    "scripts/ingest/ingest.py",
    "scripts/ingest/adapter.py",
    "scripts/ingest/scheduler.py",
    "scripts/ingest/dna.py",
)

# A synthetic 23andMe-format genotype table (the dna.land validator shape).
_DNA_HEADER = ["# rsid\tchromosome\tposition\tgenotype"]
_DNA_ROWS = [
    "rs4477212\t1\t82154\tAA",
    "rs3094315\t1\t752566\tAG",
    "rs3131972\t1\t752721\tGG",
]


def _write_healthkit_xml(path, *, day="2026-05-01", value="55"):
    """Write a minimal Apple-Health `export.xml` carrying one HRV record."""
    path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n'
        f' <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"'
        f' startDate="{day} 08:00:00 -0500" value="{value}"/>\n'
        '</HealthData>\n'
    )


def _apple_health_zip(zip_path, xml_bytes, *, member="apple_health_export/export.xml"):
    """Wrap `xml_bytes` as an Apple-Health export `.zip` (member under a dir + noise)."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("apple_health_export/", b"")
        zf.writestr("__MACOSX/._export.xml", b"resource-fork")
        zf.writestr(member, xml_bytes)


def _dna_zip(zip_path):
    """Write a synthetic 23andMe export `.zip` carrying a genotype `.txt` member."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("__MACOSX/._junk", "resource fork")
        zf.writestr("genome_v5.txt", "\n".join([*_DNA_HEADER, *_DNA_ROWS]) + "\n")


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 wearable dispatch; AC-2 DNA dispatch; AC-4 reuse
# --------------------------------------------------------------------------- #


def test_staged_export_xml_routes_into_ingest_run(tmp_path):
    """AC-1: a staged `export.xml` routes into the unchanged `ingest.run` (healthkit).

    `route_upload` detects the `.xml` as healthkit (reusing `_EXT_SOURCE`),
    constructs the healthkit adapter, and calls `ingest.run` — the HRV record lands
    on the `hrv` stream under the tmp store root with `source == "healthkit"`.
    """
    staged = tmp_path / "export.xml"
    _write_healthkit_xml(staged, day="2026-05-01", value="55")
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"

    route.route_upload(staged, root=store_root, dna_root=dna_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1, "the staged export.xml did not land an hrv reading via ingest.run"
    assert hrv[0]["value"] == 55.0 and hrv[0]["timepoint"] == "2026-05-01"
    assert hrv[0]["source"] == "healthkit"


def test_staged_apple_health_zip_routes_into_ingest_run(tmp_path):
    """AC-3 (route leg): an Apple-Health `.zip` content-branches to healthkit `ingest.run`.

    The `.zip` carries `*/export.xml`, so the content-branch routes it to healthkit
    (NOT the CLI's `.zip -> dna` default). The zip is passed AS-IS to the zip-aware
    adapter (ADR-0013-T3), which extracts `export.xml` internally — the route adds no
    extraction. The inner HRV record lands on the `hrv` stream under the tmp store root.
    """
    xml = tmp_path / "export.xml"
    _write_healthkit_xml(xml, day="2026-05-02", value="60")
    staged = tmp_path / "apple_health_export.zip"
    _apple_health_zip(staged, xml.read_bytes())
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"

    route.route_upload(staged, root=store_root, dna_root=dna_root)

    hrv = store.read("hrv", root=store_root)
    assert len(hrv) == 1, "the Apple-Health zip did not land via the healthkit adapter"
    assert hrv[0]["value"] == 60.0 and hrv[0]["timepoint"] == "2026-05-02"
    assert hrv[0]["source"] == "healthkit"
    # The DNA dropzone stayed empty — the zip routed to healthkit, not dna.
    assert not (dna_root.exists() and list(dna_root.glob("*"))), "Apple-Health zip wrongly landed in the DNA dropzone"


def test_staged_dna_zip_routes_into_dna_land(tmp_path):
    """AC-2: a staged 23andMe `.zip` routes into the unchanged `dna.land`.

    The `.zip` carries a genotype `.txt` (no `*/export.xml`), so the content-branch
    routes it to dna — the genotype member lands under `dna_root` and the store
    stays empty (DNA is not a time-series reading).
    """
    staged = tmp_path / "23andme_export.zip"
    _dna_zip(staged)
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"

    route.route_upload(staged, root=store_root, dna_root=dna_root)

    landed = list(dna_root.glob("*.txt"))
    assert landed, "the DNA zip did not land a genotype .txt under dna_root"
    assert landed[0].name == "genome_v5.txt"
    # The store stayed empty — DNA does not flow into the time-series store.
    assert store.read_all(store_root) == [], "the DNA zip wrongly wrote into the time-series store"


def test_route_default_roots_resolve_to_production_defaults(tmp_path, monkeypatch):
    """A `None` root/dna_root resolves to the production defaults (the operator-entry path).

    `build_server(port)` (no roots) passes `root=None`/`dna_root=None`; the router must
    resolve those to `store.DEFAULT_ROOT` / `vault/dna/raw/` rather than passing `None`
    into the seam (which would raise on the path-join). Monkeypatches the production
    defaults at a tmp root so the resolution is proved WITHOUT touching the real instance.
    """
    prod_store = tmp_path / "prod_store"
    prod_dna = tmp_path / "prod_dna"
    monkeypatch.setattr(store, "DEFAULT_ROOT", prod_store)
    monkeypatch.setattr(route, "_DEFAULT_DNA_ROOT", prod_dna)

    staged = tmp_path / "export.xml"
    _write_healthkit_xml(staged, day="2026-05-04", value="50")
    # No root/dna_root args — the production-default resolution path.
    route.route_upload(staged)

    hrv = store.read("hrv", root=prod_store)
    assert len(hrv) == 1 and hrv[0]["value"] == 50.0, "default root did not resolve to store.DEFAULT_ROOT"

    # And a DNA upload with default roots lands under the resolved production DNA root.
    dna_zip = tmp_path / "23andme_export.zip"
    _dna_zip(dna_zip)
    route.route_upload(dna_zip)
    assert list(prod_dna.glob("*.txt")), "default dna_root did not resolve to vault/dna/raw/"


def test_route_reuses_cli_source_detection_no_second_map(tmp_path):
    """AC-4 / Risk reuse: route.py references `_EXT_SOURCE`/`_detect_source`, 0 second map.

    The source-detection must CALL the CLI's `_EXT_SOURCE`/`_detect_source`, never
    re-derive the extension rules. Asserts the route module imports/references those
    names and defines no second `{".xml": ...}` extension->source mapping literal.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "route.py").read_text()
    assert "_detect_source" in src or "_EXT_SOURCE" in src, (
        "route.py does not reference the CLI's _EXT_SOURCE/_detect_source (re-derives the rules?)"
    )
    # A second extension->source map literal would fork the rule set (criterion-4 failure).
    assert '".xml"' not in src and "'.xml'" not in src, (
        "route.py defines a second .xml extension->source map (must reuse the CLI map)"
    )


def test_shared_ingest_routines_byte_unchanged():
    """AC-6 / Risk 0-shared-routine-edit: ingest.py/adapter.py/scheduler.py/dna.py unchanged.

    `git diff --numstat <fork-point> -- <shared routines>` emits 0 rows — the route
    adds no ingestion/store-write/land logic in the serve layer; it CALLS the
    unchanged seam. Falsifiable: a transient edit to any shared routine emits a row.
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    rows = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", *SHARED_ROUTINE_PATHS],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a shared ingest routine was edited (0-shared-routine-edit broken): {changed}"
