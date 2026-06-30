"""De-associated, allele-agnostic variant-query stub tests — string/stub-driven, 0 live spend."""

import inspect
import re
from pathlib import Path

import pytest

from scripts.genetics import research_query
from scripts.genetics.research_query import (
    assert_query_de_associated,
    build_variant_query,
)
from scripts.genetics.variants import EXCLUDED_VARIANTS, PLANNING_RELEVANT_VARIANTS

# The pinned allele-call shape the crown-jewel guard must trip on (and the generic
# query must never carry) — drawn from the spec/recipe, not re-derived per test.
_ALLELE_CALL = re.compile(r"\([ACGTDI]+;[ACGTDI]+\)")

_RESEARCH_QUERY_SRC = Path("scripts/genetics/research_query.py")


def _curated_variant():
    """Pick a curated (gene, rsid) from the set so the tests survive a curation retune."""
    return PLANNING_RELEVANT_VARIANTS[0]


class RecordingDispatcher:
    """A dispatcher stand-in recording every query it is handed; 0 live spend.

    Attributes:
        calls (list): The query strings passed to each `__call__`, in order.
        result: The sentinel value each call returns.
    """

    def __init__(self, result="STUB-DISPATCH-RESULT"):
        self.calls = []
        self.result = result

    def __call__(self, query):
        self.calls.append(query)
        return self.result


def _write_identity_token_config(tmp_path):
    """Write a gitignored-shape one-regex-per-line operator-identity token file."""
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text("# fake operator-identity token\nWalterMcGivneyFixtureToken\n", encoding="utf-8")
    return cfg


# --- Cycle 1: the allele-agnostic query + the fail-closed de-association guard ---


def test_build_variant_query_is_allele_agnostic_and_contains_gene_rsid():
    """AC-1: the query embeds gene+rsID, carries no allele-call pattern, and takes no allele param."""
    gene, rsid = _curated_variant()
    query = build_variant_query(gene, rsid)
    assert gene in query
    assert rsid in query
    assert _ALLELE_CALL.search(query) is None
    params = list(inspect.signature(build_variant_query).parameters)
    assert params == ["gene", "rsid"]


def test_built_query_passes_de_association_guard():
    """AC-3: the generic built query passes the guard (the positive control)."""
    gene, rsid = _curated_variant()
    query = build_variant_query(gene, rsid)
    assert assert_query_de_associated(query) is None


def test_assert_query_de_associated_raises_on_injected_allele():
    """AC-2 (allele): an injected allele call trips the fail-closed guard."""
    gene, rsid = _curated_variant()
    injected = build_variant_query(gene, rsid) + " the operator's genotype is (C;G)"
    with pytest.raises(ValueError):
        assert_query_de_associated(injected)


def test_assert_query_de_associated_raises_on_injected_identity_token():
    """AC-2 (identity): an injected operator-contact value-class token trips the guard."""
    gene, rsid = _curated_variant()
    injected = build_variant_query(gene, rsid) + " contact the operator at operator@example.com"
    with pytest.raises(ValueError):
        assert_query_de_associated(injected)


def test_assert_query_de_associated_threads_identity_config(tmp_path):
    """AC-2 (identity, config path): a fixture token_config identity token trips the guard."""
    gene, rsid = _curated_variant()
    cfg = _write_identity_token_config(tmp_path)
    injected = build_variant_query(gene, rsid) + " WalterMcGivneyFixtureToken"
    with pytest.raises(ValueError):
        assert_query_de_associated(injected, identity_config=cfg)


# --- Cycle 2: the EXCLUDED-variant refusal + the 0-spend stubbed dispatch ---


def test_dispatch_refuses_excluded_variant(monkeypatch):
    """AC-4: each EXCLUDED gene raises refuse-FIRST — the query is never built or dispatched."""
    recording = RecordingDispatcher()
    build_calls = []
    real_build = research_query.build_variant_query

    def spy_build(gene, rsid):
        build_calls.append((gene, rsid))
        return real_build(gene, rsid)

    monkeypatch.setattr(research_query, "build_variant_query", spy_build)
    for gene, rsid in EXCLUDED_VARIANTS:
        with pytest.raises(ValueError):
            research_query.dispatch_variant_research(gene, rsid, dispatcher=recording)
    assert recording.calls == []
    assert build_calls == []


def test_dispatch_refuses_non_curated_variant_before_build(monkeypatch):
    """SEC-1: a non-curated, non-excluded variant (BRCA1 rs80357906) is REFUSED before build.

    Auto-research is scoped to the OQ-3 curated allowlist; the dispatch refuses on ABSENCE
    from `PLANNING_RELEVANT_VARIANTS` FIRST — so a non-excluded BUT non-curated sensitive
    variant is never auto-crossed. The refusal precedes `build_variant_query`, so neither the
    build spy nor the recording dispatcher records a call. Failing-capable: moving the
    allowlist check AFTER the build reds this (`build_calls` would be non-empty).
    """
    non_curated = ("BRCA1", "rs80357906")
    assert non_curated not in set(PLANNING_RELEVANT_VARIANTS)  # not curated...
    assert non_curated[0] not in {gene for gene, _ in EXCLUDED_VARIANTS}  # ...and not excluded
    recording = RecordingDispatcher()
    build_calls = []
    real_build = research_query.build_variant_query

    def spy_build(gene, rsid):
        build_calls.append((gene, rsid))
        return real_build(gene, rsid)

    monkeypatch.setattr(research_query, "build_variant_query", spy_build)
    with pytest.raises(ValueError):
        research_query.dispatch_variant_research(*non_curated, dispatcher=recording)
    assert recording.calls == []
    assert build_calls == []


def test_dispatch_curated_variant_still_dispatches():
    """SEC-1 control: the allowlist still ADMITS a curated variant (no over-rejection).

    The curated set dispatches exactly as before the allowlist gate — the injected
    dispatcher is called once with the guarded query. Pins that refuse-on-absence did
    not close the happy path.
    """
    gene, rsid = _curated_variant()
    recording = RecordingDispatcher()
    result = research_query.dispatch_variant_research(gene, rsid, dispatcher=recording)
    assert len(recording.calls) == 1
    assert recording.calls[0] == build_variant_query(gene, rsid)
    assert result == recording.result


def test_dispatch_default_is_zero_spend_dry_run():
    """AC-5 (dry-run): the default dispatcher=None returns the guarded query, 0 outbound call."""
    gene, rsid = _curated_variant()
    result = research_query.dispatch_variant_research(gene, rsid)
    assert result == build_variant_query(gene, rsid)
    assert assert_query_de_associated(result) is None


def test_dispatch_calls_recording_dispatcher_once_with_guarded_query():
    """AC-5 (recording): an injected dispatcher is called exactly once with the guarded query."""
    gene, rsid = _curated_variant()
    recording = RecordingDispatcher()
    result = research_query.dispatch_variant_research(gene, rsid, dispatcher=recording)
    assert len(recording.calls) == 1
    assert recording.calls[0] == build_variant_query(gene, rsid)
    assert assert_query_de_associated(recording.calls[0]) is None
    assert result == recording.result


def test_research_query_imports_no_outbound_client_no_sdk():
    """AC-6 (crown-jewel structural): the module imports no outbound client and no model SDK."""
    source = _RESEARCH_QUERY_SRC.read_text(encoding="utf-8")
    for marker in (
        "import anthropic",
        "socket.create_connection",
        "urllib.request",
        "http.client",
        "requests",
        "httpx",
        "scripts.model.client",
        "scripts.model",
    ):
        assert marker not in source, f"outbound/SDK marker leaked into research_query.py: {marker!r}"


# --- Cycle 3: the un-stubbed landing mechanism (a finding -> a gated genetics page) ---

import functools  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402

from scripts.genetics import match  # noqa: E402
from scripts.genetics.research_query import (  # noqa: E402
    dispatch_variant_research,
    land_finding_page,
)
from scripts.genetics.variants import variant_item  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _finding(gene, rsid, genotype_findings, *, tier="B"):
    """A de-identified variant finding dict an injected dispatcher would return."""
    return {
        "gene": gene,
        "rsid": rsid,
        "evidence_tier": tier,
        "created": "2026-06-29",
        "last_verified": "2026-06-29",
        "provenance_dir": "design/.test-provenance",
        "provenance_slug": "genetics-specialist",
        "genotype_findings": genotype_findings,
    }


def _wiki_repo(tmp_path, slug):
    """Scaffold a temp wiki repo + a 0-spend stub bda; return (repo, genetics_dir, bda)."""
    repo = tmp_path / "wikirepo"
    gdir = repo / "vault/library/genetics"
    gdir.mkdir(parents=True)
    (repo / "vault/meta").mkdir(parents=True)
    (repo / "design/.test-provenance").mkdir(parents=True)
    (repo / "vault/meta/index.md").write_text(
        f"# Index\n## genetics\n- [[library/genetics/{slug}]]\n", encoding="utf-8"
    )
    bda = tmp_path / "bda-pass.sh"
    bda.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    bda.chmod(0o755)
    return repo, gdir, bda


def _run_gate(repo, bda, page_relpath):
    """Run wiki-ingest-lint.sh over a repo-relative page; return (exit_code, output)."""
    proc = subprocess.run(
        ["bash", str(_REPO_ROOT / "scripts/wiki-ingest-lint.sh"), page_relpath],
        cwd=repo,
        env={**os.environ, "WIKI_REPO_ROOT": str(repo), "WIKI_BDA_CMD": str(bda)},
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_dispatch_lands_gated_page_from_finding(tmp_path):
    """The un-stubbed dispatch lands a finding as a gate-valid genetics page (mock dispatcher, 0 spend).

    Non-tautological: the written page PASSES the real wiki-ingest-lint battery (bda stubbed
    0-spend), proving a structurally-gated page was written — not merely that a file exists. The
    dispatcher receives the GUARDED, allele-agnostic query (de-association held on the landing path).
    """
    gene, rsid = "CYP1A2", "rs762551"
    slug = f"{gene.lower()}-{rsid}"
    repo, gdir, bda = _wiki_repo(tmp_path, slug)
    finding = _finding(
        gene,
        rsid,
        [
            ("(A;A)", "fast-caffeine-metabolism", "fast clearance [http://example/1]"),
            ("(C;C)", "slow-caffeine-metabolism", "slow clearance [http://example/2]"),
        ],
    )
    seen = {}

    def dispatcher(query):
        seen["query"] = query
        return finding

    page = dispatch_variant_research(gene, rsid, dispatcher=dispatcher, library_root=gdir)

    # the dispatcher received the guarded, allele-agnostic query (de-association held)
    assert seen["query"] == build_variant_query(gene, rsid)
    assert assert_query_de_associated(seen["query"]) is None
    # a gate-valid page was written (passes the real ingestion battery, bda stubbed)
    assert page.exists()
    rc, out = _run_gate(repo, bda, f"vault/library/genetics/{slug}.md")
    assert rc == 0, out


def test_landed_page_round_trips_through_matcher(tmp_path):
    """The landed page resolves through the consumption matcher (mechanism -> consumption).

    A genotype the operator carries -> the dispatch-landed page -> match.match_genotypes -> the
    coarse trait class. Non-tautological: a DIFFERENT genotype -> a DIFFERENT trait class (A != B).
    """
    gene, rsid = "CYP1A2", "rs762551"
    finding = _finding(
        gene,
        rsid,
        [
            ("(A;A)", "fast-caffeine-metabolism", "fast [http://example/1]"),
            ("(C;C)", "slow-caffeine-metabolism", "slow [http://example/2]"),
        ],
    )
    dispatch_variant_research(gene, rsid, dispatcher=lambda q: finding, library_root=tmp_path)
    item = variant_item(gene, rsid)

    def read_a(it):
        return [{"item": it, "source": "dna-report", "value": "(A;A)"}] if it == item else []

    def read_c(it):
        return [{"item": it, "source": "dna-report", "value": "(C;C)"}] if it == item else []

    m_a = match.match_genotypes(read_a, library_root=tmp_path)
    m_c = match.match_genotypes(read_c, library_root=tmp_path)
    trait_a = next(m["trait_class"] for m in m_a if m["rsid"] == rsid)
    trait_c = next(m["trait_class"] for m in m_c if m["rsid"] == rsid)
    assert trait_a == "fast-caffeine-metabolism"
    assert trait_c == "slow-caffeine-metabolism"
    assert trait_a != trait_c


def test_land_finding_page_rejects_path_traversal_slug(tmp_path):
    """SEC2 (path traversal): a malicious `slug` raises and writes NOTHING — write-anywhere closed.

    `land_finding_page` builds the page filename from `finding['slug']`; an unvalidated slug like
    `../../meta/operator-identity` would write a `.md` OUTSIDE the library root (proven write-anywhere).
    The fix fail-closes on any non-safe slug (`^[a-z0-9][a-z0-9-]*$`) BEFORE any write. Asserts the
    call raises AND no `.md` was written anywhere under tmp (neither in nor outside the root).
    """
    gene, rsid = "CYP1A2", "rs762551"
    root = tmp_path / "wikirepo" / "vault/library/genetics"
    root.mkdir(parents=True)
    finding = _finding(gene, rsid, [("(A;A)", "fast-caffeine-metabolism", "fast [http://example/1]")])
    finding["slug"] = "../../meta/operator-identity"  # the proven traversal slug
    with pytest.raises(ValueError):
        land_finding_page(finding, library_root=root)
    assert list(tmp_path.rglob("*.md")) == [], "a page was written despite the path-traversal slug"


def test_land_finding_page_rejects_operator_pii(tmp_path):
    """SEC3 (public-repo PII): a finding whose rendered content carries operator PII raises, lands nothing.

    The landed page commits to a PUBLIC repo; `land_finding_page` rescans the rendered page for operator
    PII (symmetric with the outbound de-association guard) and fail-closes. A prose carrying an email
    address trips `pii_scan.scan_text_full`. Asserts the call raises and writes no page.
    """
    gene, rsid = "CYP1A2", "rs762551"
    finding = _finding(gene, rsid, [("(A;A)", "fast-caffeine-metabolism", "contact operator@example.com")])
    with pytest.raises(ValueError):
        land_finding_page(finding, library_root=tmp_path)
    assert list(tmp_path.glob("*.md")) == [], "a page leaked operator PII into the public wiki"


def test_land_finding_page_rejects_raw_genotype_in_trait_class(tmp_path):
    """SEC3 (raw genotype): a trait-class token carrying a raw genotype raises, lands nothing.

    A coarse trait-class token must carry no raw genotype (rs-id / paired-allele call) — symmetric with
    the outbound guard (the genotype field legitimately carries the per-genotype call; the CLASS token
    must not). A finding whose trait_class embeds a `(C;G)` call trips the guard. Asserts no page lands.
    """
    gene, rsid = "CYP1A2", "rs762551"
    finding = _finding(gene, rsid, [("(A;A)", "carries (C;G) allele", "x [http://example/1]")])
    with pytest.raises(ValueError):
        land_finding_page(finding, library_root=tmp_path)
    assert list(tmp_path.glob("*.md")) == [], "a page leaked a raw genotype into the public wiki"


def test_dispatch_without_library_root_writes_no_page(tmp_path):
    """A dispatcher WITHOUT library_root returns the finding and writes no page (back-compat control)."""
    gene, rsid = "CYP1A2", "rs762551"
    finding = _finding(gene, rsid, [("(A;A)", "fast-caffeine-metabolism", "fast [http://example/1]")])
    result = dispatch_variant_research(gene, rsid, dispatcher=lambda q: finding)
    assert result == finding
    assert not list(tmp_path.glob("*.md"))


def test_dispatch_refuses_finding_variant_mismatch(tmp_path):
    """A dispatcher returning a finding for a DIFFERENT variant raises and lands no page (boundary check)."""
    finding = _finding("MCM6", "rs4988235", [("(T;T)", "lactase-persistent", "x [http://example/1]")])
    with pytest.raises(ValueError):
        dispatch_variant_research(
            "CYP1A2", "rs762551", dispatcher=lambda q: finding, library_root=tmp_path
        )
    assert not list(tmp_path.glob("*.md"))


def test_landed_page_with_no_findings_fails_gate(tmp_path):
    """A finding with no genotype lines lands a page the gate REJECTS (the gate is not always-pass)."""
    gene, rsid = "CYP1A2", "rs762551"
    slug = f"{gene.lower()}-{rsid}"
    repo, gdir, bda = _wiki_repo(tmp_path, slug)
    dispatch_variant_research(gene, rsid, dispatcher=lambda q: _finding(gene, rsid, []), library_root=gdir)
    rc, out = _run_gate(repo, bda, f"vault/library/genetics/{slug}.md")
    assert rc == 1, out  # empty ## Genotype Findings -> a real gate violation


def test_landed_page_drives_genetic_trait_token_in_summary(tmp_path):
    """The LANDED page drives router.summarize's de-id genetic-trait-classes token (mechanism -> plan).

    Ties the un-stubbed landing to the plan-summary boundary: a genotype + the dispatch-landed page
    -> the coarse token (no raw genotype). Non-tautological: a no-DNA store -> the empty token.
    """
    from scripts.plan import router
    from scripts.store import keying, store

    gene, rsid = "CYP1A2", "rs762551"
    lib = tmp_path / "genlib"
    finding = _finding(gene, rsid, [("(A;A)", "fast-caffeine-metabolism", "fast [http://example/1]")])
    dispatch_variant_research(gene, rsid, dispatcher=lambda q: finding, library_root=lib)

    root = tmp_path / "inst"
    root.mkdir()
    item = variant_item(gene, rsid)
    store.append(
        item,
        {f: None for f in keying.LINE_FIELDS}
        | {"item": item, "timepoint": "2026-06-29T00:00:00+00:00", "source": "dna-report", "value": "(A;A)"},
        root=root,
    )
    summary = router.summarize(functools.partial(store.read, root=root), genetics_library_root=lib)
    assert summary["genetic-trait-classes"] == "fast-caffeine-metabolism"

    empty_root = tmp_path / "inst_empty"
    empty_root.mkdir()
    empty = router.summarize(functools.partial(store.read, root=empty_root), genetics_library_root=lib)
    assert empty["genetic-trait-classes"] == ""
