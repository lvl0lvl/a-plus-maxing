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
