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
import uuid
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


def _write_healthkit_rhr_resp_xml(path, pairs):
    """Write an export.xml with a RestingHeartRate + a RespiratoryRate record per (day, value)."""
    rows = "".join(
        f' <Record type="HKQuantityTypeIdentifierRestingHeartRate" startDate="{d} 08:00:00 -0500" value="{v}"/>\n'
        f' <Record type="HKQuantityTypeIdentifierRespiratoryRate" startDate="{d} 08:00:00 -0500" value="14"/>\n'
        for d, v in pairs
    )
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<HealthData locale="en_US">\n' + rows + "</HealthData>\n")


def test_wearable_upload_mirrors_registered_marker_into_trend_namespace(tmp_path):
    """The wearable land path mirrors a registered-polarity marker (rhr) into biomarker::; not others.

    The dead-feed fix on the wearable path: `route_upload` captures the readings `ingest.run` lands
    and mirrors the registered-polarity ones into the `biomarker::<marker>` namespace the router's
    recent-trend-direction feed reads. A healthkit export with rhr (registered, down-polarity) +
    resp-rate (mapped but UNregistered) over two days lands both bare, but only `rhr` mirrors into
    `biomarker::rhr` (both timepoints), while `resp-rate` does NOT. Mutation-proof: drop the route
    mirror and biomarker::rhr is empty.
    """
    staged = tmp_path / "export.xml"
    _write_healthkit_rhr_resp_xml(staged, [("2026-04-01", "50"), ("2026-05-01", "70")])
    store_root = tmp_path / "store"

    route.route_upload(staged, root=store_root, dna_root=tmp_path / "dna")

    # bare lands unchanged (additive): both rhr and resp-rate landed bare, two timepoints each.
    assert len(store.read("rhr", root=store_root)) == 2, "the wearable rhr readings did not land bare"
    assert len(store.read("resp-rate", root=store_root)) == 2, "the wearable resp-rate readings did not land bare"
    # the registered-polarity marker is mirrored into the trend namespace, BOTH timepoints.
    mirrored = store.read("biomarker::rhr", root=store_root)
    assert [r["value"] for r in mirrored] == [50.0, 70.0], (
        f"rhr was not mirrored into biomarker:: with both timepoints: {mirrored}"
    )
    # the mapped-but-unregistered marker is NOT mirrored (no polarity -> not in the trend feed).
    assert store.read("biomarker::resp-rate", root=store_root) == [], "an unregistered marker was wrongly mirrored"


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


# --------------------------------------------------------------------------- #
# Cycle 1 — ADR-0030-T2: the universal-extraction front door
#   AC-1 universal route; AC-2 no regression; AC-3 no auto-land;
#   AC-4 crown-jewel file-egress; AC-5 OQ-5 no tracked residue
# --------------------------------------------------------------------------- #

# A Line-Field-Set-conformant canned readings payload (what a mock client returns).
_CANNED_READINGS = [
    {"item": "ferritin", "timepoint": "2026-05-01", "source": "labs", "value": "120"},
    {"item": "vitamin-d", "timepoint": "2026-05-01", "source": "labs", "value": "44"},
]


class _RecordingClient:
    """A mock no-train model client recording its `extract_readings` calls (0 live spend).

    Records each `(file_content, media_type)` it receives and returns a canned readings list —
    no live API, no key, no network socket. The crown-jewel file-egress probe asserts the file
    content reached ONLY this recorded sink.

    Attributes:
        calls (list): The `(file_content, media_type)` tuples `extract_readings` was called with.
    """

    def __init__(self, readings=None):
        self._readings = list(_CANNED_READINGS if readings is None else readings)
        self.calls = []

    def extract_readings(self, file_content, media_type):
        self.calls.append((file_content, media_type))
        return list(self._readings)


def _spy_seam(monkeypatch):
    """Spy `ingest.run`/`dna.land`/`store.append` so the extraction path's 0-call is provable.

    The recognized-format dispatch and every store write flow through these three; the
    extraction branch must touch none of them. Returns a dict of recorded call args per seam.
    """
    calls = {"ingest_run": [], "dna_land": [], "store_append": []}
    monkeypatch.setattr(route.ingest, "run", lambda *a, **k: calls["ingest_run"].append((a, k)))
    monkeypatch.setattr(route.dna, "land", lambda *a, **k: calls["dna_land"].append((a, k)))
    monkeypatch.setattr(route.store, "append", lambda *a, **k: calls["store_append"].append((a, k)))
    return calls


def test_unrecognized_format_routes_through_extract_readings(tmp_path, monkeypatch):
    """AC-1: an unrecognized `.bin` + an injected client routes through `extract_readings`.

    The `.bin` extension is in no named-adapter map, so `_detect_source` SystemExits; with a
    client injected the staged file routes through the no-train lane — `client.extract_readings`
    is called exactly once with the staged file's content, and `ingest.run`/`dna.land` are NOT.
    (ADR-0031-T4 repoint: `.pdf` is now reserved for the local-extract-first branch; this test
    covers the PRESERVED non-PDF raw-content arm via `.bin` -> application/octet-stream.)
    """
    calls = _spy_seam(monkeypatch)
    content = b"synthetic lab report octet-stream body"
    staged = tmp_path / "labs.bin"
    staged.write_bytes(content)
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    assert len(client.calls) == 1, "extract_readings was not called exactly once"
    assert client.calls[0][0] == content, "extract_readings did not receive the staged file content"
    assert calls["ingest_run"] == [] and calls["dna_land"] == [], "the unrecognized format wrongly hit the named seam"


def test_unrecognized_format_no_client_preserves_systemexit(tmp_path):
    """No-client backward-compat: an unrecognized format with `client=None` SystemExits.

    Today's no-client contract is byte-unchanged — without an injected client the
    unrecognized-extension `_detect_source` SystemExit is preserved (the operator-entry
    callers are unaffected; T3 threads `self.client` in to activate extraction).
    """
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(b"synthetic")

    with pytest.raises(SystemExit):
        route.route_upload(staged, root=tmp_path / "store", dna_root=tmp_path / "dna")


def test_recognized_formats_do_not_call_extract_readings(tmp_path):
    """AC-2: recognized formats still route to the named seam; extract_readings call count 0.

    With the mock client injected, an `export.xml` still lands via `ingest.run` (healthkit) and
    a 23andMe `.zip` still lands via `dna.land` — the named/dna side-effects are unchanged AND
    `client.extract_readings` is never called on a recognized format.
    """
    client = _RecordingClient()
    store_root = tmp_path / "store"
    dna_root = tmp_path / "dna"

    xml = tmp_path / "export.xml"
    _write_healthkit_xml(xml, day="2026-05-03", value="58")
    src_xml = route.route_upload(xml, client=client, root=store_root, dna_root=dna_root)
    assert src_xml == "healthkit"
    assert store.read("hrv", root=store_root)[0]["value"] == 58.0

    dna_zip = tmp_path / "23andme_export.zip"
    _dna_zip(dna_zip)
    src_zip = route.route_upload(dna_zip, client=client, root=store_root, dna_root=dna_root)
    assert src_zip == "dna"
    assert list(dna_root.glob("*.txt")), "the DNA zip did not land via dna.land with a client injected"

    assert client.calls == [], "extract_readings was called on a recognized format (regression)"


def test_extraction_does_not_auto_land(tmp_path, monkeypatch):
    """AC-3: the extraction path makes 0 store.append/dna.land; readings await confirm.

    `route_upload` over an unrecognized format writes nothing — `store.read_all` is empty
    afterward and the spy records 0 store.append/dna.land — and RETURNS the extracted readings
    as the awaiting-confirm payload (a dict distinguishable from a landed-source string).
    """
    calls = _spy_seam(monkeypatch)
    store_root = tmp_path / "store"
    staged = tmp_path / "labs.bin"
    staged.write_bytes(b"synthetic lab report")
    client = _RecordingClient()

    result = route.route_upload(staged, client=client, root=store_root, dna_root=tmp_path / "dna")

    assert calls["store_append"] == [] and calls["dna_land"] == [], "the extraction path auto-landed a reading"
    assert store.read_all(store_root) == [], "the store is non-empty after the extraction route (auto-land)"
    assert not isinstance(result, str), "the extraction return is a source string (not distinguishable from a landed route)"
    assert result == {"extracted_readings": _CANNED_READINGS}, "the extraction route did not return the awaiting-confirm payload"


def test_extraction_file_reaches_only_the_injected_client(tmp_path, monkeypatch):
    """AC-4 (CROWN-JEWEL): the file content reaches ONLY `client.extract_readings`.

    The mock client records the bytes it received; the seam spies record what they received.
    Asserts the staged file content reached the injected client AND no other recorded sink
    (`ingest.run`/`dna.land`/`store.append`) received it — the single-egress crown-jewel bound.
    """
    calls = _spy_seam(monkeypatch)
    content = b"crown-jewel synthetic body bytes"
    staged = tmp_path / "report.png"
    staged.write_bytes(content)
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    assert [c[0] for c in client.calls] == [content], "the file content did not reach the injected client exactly once"
    assert calls["ingest_run"] == [], "ingest.run received the unrecognized-format file"
    assert calls["dna_land"] == [], "dna.land received the unrecognized-format file"
    assert calls["store_append"] == [], "store.append received the unrecognized-format file"


def test_extraction_leaves_no_tracked_residue(tmp_path):
    """AC-5 (OQ-5): the extraction route writes the raw file to no tracked path.

    Embeds a unique synthetic token (built at runtime so the literal never appears in any
    tracked source) in the staged file; after the extraction route, scans the tracked tree
    (`git grep`, excluding the gitignored dropzone prefixes) and asserts 0 tracked files carry
    the token — the raw file lived only in the gitignored staged path + the in-memory client call.
    """
    token = "OQ5-RAW-RESIDUE-" + uuid.uuid4().hex
    staged = tmp_path / "labs.bin"
    staged.write_bytes(f"synthetic lab report {token}".encode())
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    found = subprocess.run(
        ["git", "grep", "-l", token],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    ignored = ("vault/store/", "vault/dna/raw/", "vault/labs/raw/", "vault/scaffold/filled/")
    hits = [h for h in found.stdout.splitlines() if h.strip() and not h.startswith(ignored)]
    assert hits == [], f"the raw upload content leaked to a tracked path (OQ-5 residue): {hits}"


# --------------------------------------------------------------------------- #
# ADR-0031-T4 — the PDF local-extract-first branch (crown-jewel + honest signal)
#   AC-1 PDF local-extract route; AC-2 crown-jewel raw-binary egress;
#   AC-3 non-PDF unchanged; AC-4 honest-signal return; AC-5 no auto-land;
#   AC-6 OQ-3/OQ-5 residue (raw-binary + extracted-text tokens)
# --------------------------------------------------------------------------- #


def test_pdf_upload_routes_through_local_extract_first(tmp_path, monkeypatch):
    """AC-1: a `.pdf` routes pdf_extract.extract_text -> extract_chunked over the text path.

    A `.pdf` (media type application/pdf) routes through `pdf_extract.extract_text(path)` (called
    once with the staged path) and then the REAL `extract_chunked.extract_all(text, client)` — the
    recording client receives the `text/plain` chunk calls, never the raw `application/pdf`
    document path. STUBS `pdf_extract.extract_text` (no real pdftotext/marker run, 0 spend).
    """
    extract_calls = []
    monkeypatch.setattr(
        route.pdf_extract, "extract_text",
        lambda path: extract_calls.append(Path(path)) or "Ferritin 120 ng/mL on 2026-05-01\n",
    )
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(b"%PDF-1.4 raw binary body")
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    assert extract_calls == [staged], "pdf_extract.extract_text was not called once with the staged path"
    assert len(client.calls) >= 1, "the real extract_chunked did not call the recording client (text path not taken)"
    assert all(mt == "text/plain" for _c, mt in client.calls), (
        "a non-text/plain media_type reached the model (the raw application/pdf document path was taken)"
    )


def test_pdf_crown_jewel_raw_binary_reaches_only_local_extractor(tmp_path, monkeypatch):
    """AC-2 (CROWN-JEWEL): the raw PDF binary reaches ONLY the local extractor; the model gets text only.

    Stages a `.pdf` whose bytes carry a runtime-unique raw-binary token ABSENT from the stubbed
    extracted text. The recording client records every `(content, media_type)`; every recorded
    media_type must be `text/plain` AND the raw-binary token must appear in NO recorded call
    content (the raw bytes reach only `pdf_extract.extract_text`). The mock call-record is
    authoritative — not a substring grep alone.
    """
    raw_token = "RAW-BINARY-" + uuid.uuid4().hex
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "Ferritin 120 ng/mL on 2026-05-01\n")
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(f"%PDF-1.4 {raw_token}".encode())
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    assert client.calls, "the model client was never called (the text path did not run)"
    assert all(mt == "text/plain" for _c, mt in client.calls), "a non-text/plain media_type reached the model"
    for content, _mt in client.calls:
        as_text = content if isinstance(content, str) else content.decode("utf-8", errors="ignore")
        assert raw_token not in as_text, "the raw-binary token reached the model (crown-jewel breach)"


def test_pdf_honest_signal_in_route_return(tmp_path, monkeypatch):
    """AC-4 (route leg): the route maps extract_chunked's {readings,complete,note} onto the honest signal.

    STUBS `extract_chunked.extract_all` to script the partial signal: a `complete=False`+note run
    must surface as `extraction_complete=False`+the note in the route return; a `complete=True`,
    `note=None` run as `extraction_complete=True`/`extraction_note=None`. The return key is
    `extracted_readings` (the awaiting-confirm payload key the server + /confirm-extraction read).
    """
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "some extracted text")
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(b"%PDF-1.4 body")
    client = _RecordingClient()

    monkeypatch.setattr(
        route.extract_chunked, "extract_all",
        lambda text, c: {"readings": _CANNED_READINGS, "complete": False, "note": "document too large"},
    )
    partial = route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")
    assert partial == {
        "extracted_readings": _CANNED_READINGS,
        "extraction_complete": False,
        "extraction_note": "document too large",
    }, f"the route did not surface the partial honest signal: {partial}"

    monkeypatch.setattr(
        route.extract_chunked, "extract_all",
        lambda text, c: {"readings": _CANNED_READINGS, "complete": True, "note": None},
    )
    complete = route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")
    assert complete == {
        "extracted_readings": _CANNED_READINGS,
        "extraction_complete": True,
        "extraction_note": None,
    }, f"a complete extraction did not surface extraction_complete=True/note=None: {complete}"


def test_pdf_extraction_does_not_auto_land(tmp_path, monkeypatch):
    """AC-5: the PDF extraction path makes 0 store.append/dna.land; readings await confirm.

    `route_upload` over a `.pdf` writes nothing — the spy records 0 store.append/dna.land,
    `store.read_all` is empty afterward — and RETURNS the awaiting-confirm honest-signal dict
    (not a landed-source string).
    """
    calls = _spy_seam(monkeypatch)
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: "Ferritin 120 ng/mL on 2026-05-01\n")
    store_root = tmp_path / "store"
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(b"%PDF-1.4 synthetic lab report")
    client = _RecordingClient()

    result = route.route_upload(staged, client=client, root=store_root, dna_root=tmp_path / "dna")

    assert calls["store_append"] == [] and calls["dna_land"] == [], "the PDF extraction path auto-landed a reading"
    assert store.read_all(store_root) == [], "the store is non-empty after the PDF extraction route (auto-land)"
    assert not isinstance(result, str), "the PDF extraction return is a source string (not the awaiting-confirm payload)"
    assert "extracted_readings" in result and "extraction_complete" in result, (
        "the PDF route did not return the awaiting-confirm honest-signal payload"
    )


def test_pdf_extraction_leaves_no_tracked_residue_oq3(tmp_path, monkeypatch):
    """AC-6 (OQ-3/OQ-5): the PDF route leaks NO raw-binary OR extracted-text token to a tracked path.

    OQ-5 (ADR-0030) is the raw-FILE residue; OQ-3 (ADR-0031) is the raw-BINARY + EXTRACTED-TEXT
    residue — ONE tracked-tree scan covers BOTH. Seeds a runtime-unique raw-binary token into the
    staged PDF bytes AND a DISTINCT runtime-unique extracted-text token into the stubbed extractor
    return; after the route, `git grep` the tracked tree (excluding the gitignored dropzone
    prefixes) for BOTH tokens -> 0 hits each (the raw binary lived only in the gitignored staged
    path + the local extractor; the text lived only in the in-memory client call).
    """
    raw_token = "OQ3-RAW-BINARY-" + uuid.uuid4().hex
    text_token = "OQ3-EXTRACTED-TEXT-" + uuid.uuid4().hex
    monkeypatch.setattr(
        route.pdf_extract, "extract_text",
        lambda path: f"Ferritin 120 ng/mL on 2026-05-01 {text_token}\n",
    )
    staged = tmp_path / "labs.pdf"
    staged.write_bytes(f"%PDF-1.4 {raw_token}".encode())
    client = _RecordingClient()

    route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    ignored = ("vault/store/", "vault/dna/raw/", "vault/labs/raw/", "vault/scaffold/filled/")
    for token in (raw_token, text_token):
        found = subprocess.run(["git", "grep", "-l", token], cwd=REPO_ROOT, capture_output=True, text=True)
        hits = [h for h in found.stdout.splitlines() if h.strip() and not h.startswith(ignored)]
        assert hits == [], f"the {token!r} residue leaked to a tracked path (OQ-3 breach): {hits}"


def test_non_pdf_unrecognized_uses_unchanged_raw_content_path(tmp_path, monkeypatch):
    """AC-3: a NON-PDF unrecognized upload keeps the UNCHANGED raw-content path; extract_text uncalled.

    A `.bin` (unrecognized, NOT application/pdf) routes through the byte-unchanged
    `client.extract_readings(file_content, media_type)` raw-content arm — `pdf_extract.extract_text`
    is NEVER called (the local-extract-first branch is PDF-only, crit 3 no-regression) and the
    non-PDF return shape `{"extracted_readings": [...]}` is preserved (no honest-signal keys).
    """
    pdf_calls = []
    monkeypatch.setattr(route.pdf_extract, "extract_text", lambda path: pdf_calls.append(path) or "x")
    content = b"synthetic octet-stream body"
    staged = tmp_path / "labs.bin"
    staged.write_bytes(content)
    client = _RecordingClient()

    result = route.route_upload(staged, client=client, root=tmp_path / "store", dna_root=tmp_path / "dna")

    assert pdf_calls == [], "pdf_extract.extract_text was called on a NON-PDF unrecognized upload (scope error)"
    assert client.calls == [(content, "application/octet-stream")], (
        "the non-PDF arm did not call extract_readings once with the raw content + octet-stream media type"
    )
    assert result == {"extracted_readings": _CANNED_READINGS}, "the non-PDF arm return shape changed (regression)"


# --------------------------------------------------------------------------- #
# Cycle 2 — ADR-0030-T2: EXTEND-NOT-REBUILD (frozen engine + plan modules)
# --------------------------------------------------------------------------- #

# The byte-frozen set: the ingestion engine + every scripts/plan/*.py (incl. deid_in.py) +
# the store sink keying/store.append (ADR-0031-T4 NFR-3 EXTENSION — T4 dispatches to the
# UNCHANGED keying.dedupe_key / store sink via extract_chunked, never re-authoring them). T4
# EXTENDS the router + the /upload payload (NEW front-step edits), re-authoring none of these.
# ADR-0032-T3 sanctioned exception: scripts/plan/router.py is the NAMED additive seam
# for the de-identified `genetic-trait-classes` token (the DNA-aware planning build). The
# INNER engine modules (orchestrate/pipeline/assemble/generate_plan/adjudicate/adjust/track)
# stay byte-frozen; router.py is excluded from this frozen glob because T3 legitimately
# EXTENDS it (the genetics deriver + its field-set member). This is the "update the earlier
# E2E when a later phase changes the expected behavior" mandate — the additive router.py
# edit is sanctioned by ADR-0032-T3, so this prior-phase frozen-set test must not freeze it.
# See docs/adr/ADR-0032 + tests/plan/test_router.py (the T3 genetics ACs).
_FROZEN_ENGINE_PATHS = (
    "scripts/ingest/ingest.py",
    "scripts/ingest/adapter.py",
    "scripts/store/keying.py",
    "scripts/store/store.py",
    *sorted(
        str(p.relative_to(REPO_ROOT))
        for p in (REPO_ROOT / "scripts" / "plan").glob("*.py")
        if p.name != "router.py"  # additive seam — guarded by test_router_additive_only_from_fork
    ),
)

# HIST1 / PF-S63-02: router.py is excluded from the byte-frozen set above because
# ADR-0032-T3 legitimately EXTENDS it — but a WHOLESALE exclusion would let a future
# NON-ADDITIVE rewrite of router.py's existing ~600 lines (the de-id summary spine, a
# crown-jewel gate) pass CI silently. The additive-only guard below names that failure
# class and still protects router.py: DELETIONS are capped at the sanctioned ADR-0032-T3
# count (the `summarize` signature reflow + the removed redundant function-local
# `import re`, QUAL1 = 2), while INSERTIONS stay unbounded.
_ROUTER_ADDITIVE_PATH = "scripts/plan/router.py"
_ROUTER_SANCTIONED_DELETIONS = 2


def test_frozen_engine_byte_unchanged():
    """AC-6 / EXTEND-NOT-REBUILD: the ingestion engine + every scripts/plan/*.py unchanged.

    `git diff --numstat <fork-point> -- <frozen set>` emits 0 rows — T2 adds the
    universal-extraction front door onto the router; it re-authors no engine/plan module
    (incl. scripts/plan/deid_in.py). Falsifiable: a transient edit to any frozen file emits a
    row. Mirrors `test_shared_ingest_routines_byte_unchanged`, over the NFR-4 frozen set.
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    rows = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", *_FROZEN_ENGINE_PATHS],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen engine/plan file was edited (EXTEND-NOT-REBUILD broken): {changed}"


def test_router_additive_only_from_fork():
    """HIST1 / PF-S63-02: scripts/plan/router.py changed ADDITIVELY ONLY from the fork.

    router.py is the sanctioned ADR-0032-T3 additive seam, so it is NOT byte-frozen — but
    a NON-ADDITIVE rewrite of its existing engine logic (more deleted lines than the
    sanctioned change) is the crown-jewel-spine regression this guard catches. Falsifiable:
    deleting any existing non-sanctioned line pushes the deletion count over the threshold
    and REDs this test. INSERTIONS are unbounded (additive extension is allowed).
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    fields = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", _ROUTER_ADDITIVE_PATH],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    # numstat row: "<insertions>\t<deletions>\t<path>"; absent row -> unchanged -> 0 deletions.
    deletions = int(fields[1]) if fields else 0
    assert deletions <= _ROUTER_SANCTIONED_DELETIONS, (
        f"router.py deleted {deletions} lines (> {_ROUTER_SANCTIONED_DELETIONS} sanctioned) "
        f"— a NON-ADDITIVE rewrite of the de-id summary spine (PF-S63-02 guard-loosening)"
    )
