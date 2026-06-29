"""Local genotype↔library matcher tests — pure/local, fixture-driven, 0 live spend."""

from pathlib import Path

from scripts.genetics import match, variants
from scripts.genetics.variants import (
    EXCLUDED_VARIANTS,
    PLANNING_RELEVANT_VARIANTS,
    variant_item,
)


class RecordingStoreRead:
    """A per-item `store.read` stand-in recording every item key it is called with.

    Attributes:
        calls (list): The item keys passed to each `__call__`, in order.
    """

    def __init__(self, readings_by_item=None):
        self._readings = dict(readings_by_item or {})
        self.calls = []

    def __call__(self, item):
        self.calls.append(item)
        return list(self._readings.get(item, []))


def _reading(item, value, source="dna-report", timepoint="2026-01-01T00:00:00+00:00"):
    return {"item": item, "timepoint": timepoint, "source": source, "value": value}


def _write_page(library_root, gene, rsid, findings, slug=None):
    """Write a fixture genetics page in the pinned T1↔T2 format to `library_root`."""
    slug = slug or f"{gene.replace('/', '-').lower()}-{rsid}"
    lines = [
        "---",
        f"title: {gene} {rsid}",
        "type: genetics",
        f"gene: {gene}",
        f"rsid: {rsid}",
        "evidence_tier: B",
        "last_verified: 2026-06-29",
        "provenance_dir: design/genetics-fixture",
        "provenance_slug: genetics-fixture",
        "---",
        "",
        f"# {gene} {rsid}",
        "",
        "## Genotype Findings",
    ]
    for genotype, trait_class, prose in findings:
        lines.append(f"- {genotype}: {trait_class} — {prose} [1]")
    page = Path(library_root) / f"{slug}.md"
    page.write_text("\n".join(lines) + "\n")
    return page


# --- Cycle 1: curated set + per-genotype matcher core ---


def test_curated_variant_set_is_exactly_oq3_and_excluded_disjoint():
    expected = {
        ("ACTN3", "rs1815739"),
        ("CYP1A2", "rs762551"),
        ("MTHFR", "rs1801131"),
        ("MTHFR", "rs1801133"),
        ("FADS2", "rs1535"),
        ("LCT/MCM6", "rs4988235"),
        ("MTNR1B", "rs10830963"),
        ("FTO", "rs9939609"),
        ("SOD2", "rs4880"),
        ("ADIPOQ", "rs17300539"),
    }
    assert set(PLANNING_RELEVANT_VARIANTS) == expected
    assert len(PLANNING_RELEVANT_VARIANTS) == 10

    excluded_genes = {gene for (gene, _) in EXCLUDED_VARIANTS}
    assert {"APOE", "DRD2", "BDNF"} <= excluded_genes

    planning_genes = {gene for (gene, _) in PLANNING_RELEVANT_VARIANTS}
    assert planning_genes.isdisjoint(excluded_genes)

    assert variant_item("MTNR1B", "rs10830963") == "MTNR1B rs10830963"


def test_genotype_selects_per_genotype_finding_by_operator_allele(tmp_path):
    gene, rsid = "CYP1A2", "rs762551"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    _write_page(
        tmp_path,
        gene,
        rsid,
        [
            ("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly"),
            ("(C;C)", "slow-caffeine-metabolism", "clears caffeine slowly"),
        ],
    )
    item = variant_item(gene, rsid)
    store_read = RecordingStoreRead({item: [_reading(item, "(A;A)")]})

    matches = match.match_genotypes(store_read, library_root=tmp_path)

    cyp = [m for m in matches if m["gene"] == gene and m["rsid"] == rsid]
    assert len(cyp) == 1
    assert cyp[0]["trait_class"] == "fast-caffeine-metabolism"
    assert "clears caffeine quickly" in cyp[0]["implication"]
    assert cyp[0]["genotype"] == "(A;A)"
    assert str(cyp[0]["page"]).endswith(".md")


def test_distinct_genotype_yields_distinct_trait_class(tmp_path):
    gene, rsid = "CYP1A2", "rs762551"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    _write_page(
        tmp_path,
        gene,
        rsid,
        [
            ("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly"),
            ("(C;C)", "slow-caffeine-metabolism", "clears caffeine slowly"),
        ],
    )
    item = variant_item(gene, rsid)

    matches_a = match.match_genotypes(
        RecordingStoreRead({item: [_reading(item, "(A;A)")]}), library_root=tmp_path
    )
    matches_b = match.match_genotypes(
        RecordingStoreRead({item: [_reading(item, "(C;C)")]}), library_root=tmp_path
    )

    trait_a = next(m["trait_class"] for m in matches_a if m["rsid"] == rsid)
    trait_b = next(m["trait_class"] for m in matches_b if m["rsid"] == rsid)
    assert trait_a == "fast-caffeine-metabolism"
    assert trait_b == "slow-caffeine-metabolism"
    assert trait_a != trait_b


def test_genotype_orientation_normalized_before_lookup(tmp_path):
    gene, rsid = "MTNR1B", "rs10830963"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    # page keyed (C;G); operator carries the reversed orientation (G;C)
    _write_page(
        tmp_path,
        gene,
        rsid,
        [("(C;G)", "elevated-fasting-glucose-risk", "associated with higher fasting glucose")],
    )
    item = variant_item(gene, rsid)

    matches = match.match_genotypes(
        RecordingStoreRead({item: [_reading(item, "(G;C)")]}), library_root=tmp_path
    )

    mtnr = [m for m in matches if m["rsid"] == rsid]
    assert len(mtnr) == 1
    assert mtnr[0]["trait_class"] == "elevated-fasting-glucose-risk"


def test_store_read_called_only_with_curated_keys_and_filters_dna_report_source(tmp_path):
    gene, rsid = "CYP1A2", "rs762551"
    _write_page(
        tmp_path,
        gene,
        rsid,
        [("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly")],
    )
    item = variant_item(gene, rsid)
    # a non-dna-report reading is seeded LAST under the same item — a matcher that
    # took the latest reading WITHOUT source-filtering would pick this and fail.
    store_read = RecordingStoreRead(
        {
            item: [
                _reading(item, "(A;A)", source="dna-report"),
                _reading(item, "manual-note", source="manual", timepoint="2026-02-01T00:00:00+00:00"),
            ]
        }
    )

    matches = match.match_genotypes(store_read, library_root=tmp_path)

    curated_keys = {variant_item(g, r) for (g, r) in PLANNING_RELEVANT_VARIANTS}
    assert set(store_read.calls) <= curated_keys

    cyp = [m for m in matches if m["rsid"] == rsid]
    assert len(cyp) == 1
    assert cyp[0]["genotype"] == "(A;A)"


# --- Cycle 2: honest no-match research-gap list + never-auto-cross + 0-egress ---


def test_honest_no_match_present_genotype_absent_page_is_research_gap(tmp_path):
    gene, rsid = "FTO", "rs9939609"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    # operator carries a genotype, but NO page exists under library_root (empty dir)
    item = variant_item(gene, rsid)
    store_read = RecordingStoreRead({item: [_reading(item, "(A;A)")]})

    matches = match.match_genotypes(store_read, library_root=tmp_path)
    assert not any(m["gene"] == gene and m["rsid"] == rsid for m in matches)

    gaps = match.unmatched_planning_variants(store_read, library_root=tmp_path)
    assert any(g["gene"] == gene and g["rsid"] == rsid for g in gaps)


def test_honest_no_match_no_genotype_finding_entry_is_research_gap(tmp_path):
    gene, rsid = "SOD2", "rs4880"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    # page present, but no `## Genotype Findings` entry for the operator's genotype
    _write_page(tmp_path, gene, rsid, [("(C;C)", "higher-oxidative-stress", "reduced SOD2 activity")])
    item = variant_item(gene, rsid)
    store_read = RecordingStoreRead({item: [_reading(item, "(T;T)")]})

    matches = match.match_genotypes(store_read, library_root=tmp_path)
    assert not any(m["rsid"] == rsid for m in matches)

    gaps = match.unmatched_planning_variants(store_read, library_root=tmp_path)
    assert any(g["gene"] == gene and g["rsid"] == rsid for g in gaps)


def test_excluded_variant_genotype_never_matched_never_in_gap_list(tmp_path):
    excluded = {
        "APOE": "rs429358",
        "DRD2": "rs1800497",
        "BDNF": "rs6265",
    }
    store_read = RecordingStoreRead(
        {f"{gene} {rsid}": [_reading(f"{gene} {rsid}", "(C;C)")] for gene, rsid in excluded.items()}
    )
    # even with a page present, an excluded variant must never be crossed
    _write_page(tmp_path, "APOE", "rs429358", [("(C;C)", "apoe-e4-carrier", "sensitive trait")])

    matches = match.match_genotypes(store_read, library_root=tmp_path)
    gaps = match.unmatched_planning_variants(store_read, library_root=tmp_path)

    for gene, rsid in excluded.items():
        assert not any(m["gene"] == gene for m in matches)
        assert not any(g["gene"] == gene for g in gaps)
        # the matcher never even READ the excluded item (curated-set iteration)
        assert f"{gene} {rsid}" not in store_read.calls


def test_noncurated_variant_genotype_never_matched(tmp_path):
    item = "XYZ rs9999999"
    store_read = RecordingStoreRead({item: [_reading(item, "(A;A)")]})

    matches = match.match_genotypes(store_read, library_root=tmp_path)
    gaps = match.unmatched_planning_variants(store_read, library_root=tmp_path)

    assert not any(m["gene"] == "XYZ" for m in matches)
    assert not any(g["gene"] == "XYZ" for g in gaps)
    assert item not in store_read.calls


def test_find_page_skips_underscore_prefixed_template(tmp_path):
    # a `_template.md` scaffold carrying matching gene/rsid frontmatter must never be
    # parsed as the real page (Arch-3). Without the skip, _find_page would resolve it
    # and surface the template's placeholder finding; with the skip it is an honest gap.
    gene, rsid = "CYP1A2", "rs762551"
    assert (gene, rsid) in PLANNING_RELEVANT_VARIANTS
    template = Path(tmp_path) / "_template.md"
    template.write_text(
        "---\ntype: genetics\n"
        f"gene: {gene}\nrsid: {rsid}\n---\n\n"
        "## Genotype Findings\n- (A;A): TEMPLATE-LEAK — should never resolve [1]\n"
    )
    item = variant_item(gene, rsid)
    store_read = RecordingStoreRead({item: [_reading(item, "(A;A)")]})

    matches = match.match_genotypes(store_read, library_root=tmp_path)
    assert not any(m["trait_class"] == "TEMPLATE-LEAK" for m in matches)

    gaps = match.unmatched_planning_variants(store_read, library_root=tmp_path)
    assert any(g["gene"] == gene and g["rsid"] == rsid for g in gaps)


def test_match_module_imports_no_outbound_client_no_sdk_no_store_write():
    forbidden = [
        "anthropic",
        "socket.create_connection",
        "urllib.request",
        "http.client",
        "requests",
        "httpx",
        "store.append",
        "store.correct",
    ]
    for module in (match, variants):
        src = Path(module.__file__).read_text()
        for marker in forbidden:
            assert marker not in src, f"{module.__name__} contains forbidden marker {marker!r}"
