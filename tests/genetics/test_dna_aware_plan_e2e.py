"""End-to-end DNA-aware-plan proof + the five ADR-0032 falsification probes (ADR-0032-T5).

This is the terminal Wave-3 integration gate and the headline acceptance the whole
ADR-0032 DNA-aware-planning slice exists to satisfy: a fixture `dna-report` genotype +
a fixture `vault/library/genetics/` page produces a plan signal that VISIBLY carries a
current-science genetic-trait class — through the LOCAL match, the de-identified
`genetic-trait-classes` token, and the existing `summarize`/`dispatch`/`author` seam —
with the raw rsID+allele genotype proven NEVER to cross to the no-train planner and the
outbound variant query proven de-associated. It adds NO production code; it composes the
already-built chain end-to-end:

    fixture dna-report genotype (real store.append -> store.read)
      -> scripts.genetics.match.match_genotypes (T2) against a fixture genetics page
      -> router.summarize's `genetic-trait-classes` deriver (T3) — the coarse trait class
      -> router.dispatch's closed-field-set whitelist (the de-id payload passes)
      -> ModelClient.author(domain, summary) (the no-train planner seam; MOCKED at the
         ADR-0015 ModelClient(backend=...) seam — no live API, no key, 0 spend)
      -> a plan signal whose recommendation TRACES to the fixture finding's trait class.

Two load-bearing test properties:
  (a) NON-TAUTOLOGICAL: the headline asserts the plan signal's recommendation CONTAINS the
      FIXTURE finding's trait class (content-traceable), and a DIFFERENT fixture genotype ->
      a DIFFERENT plan trait (A != B) — proving the plan signal is the fixture's match, not a
      hardcoded constant. A failing-capable negative control proves the headline goes RED on
      the no-DNA state (empty token, no genetic trait in the plan). It NEVER asserts merely
      "a plan was produced". The headline is proven through BOTH the explicit-fixture-root
      call `summarize(store_read, genetics_library_root=<fixture>)` AND the frozen PRODUCTION
      no-arg signature `summarize(store_read)` (the deriver's module-level default root
      monkeypatched to the fixture library — FIX-1/CQ-1), with a matching-page-removed
      negative control distinguishing "wired to the real default, no match" from "feature
      disabled".
  (b) MOCK/FIXTURE-TESTABLE: the plan-author model is a fixture backend injected at the
      ADR-0015 seam, the variant dispatch is the T4 `dispatcher=None` dry-run, and a spy on
      `key_source.resolve` records 0 calls — so the run is deterministic + CI-runnable with
      no network, no key, 0 live spend, 0 aplus-research dispatch.

The five ADR-0032 falsification probes, each FAILING-CAPABLE (RED on the broken behavior;
QA-F3 per-probe RED-on-violation):
  (1) crown-jewel egress [de-association + library-association]
      -> test_probe_crown_jewel_egress_de_associated_and_library_operator_free. REDs if the
         `build_variant_query` output carries an operator-identity OR raw-genotype token or is
         not allele-agnostic (the guard fails to raise on a violation), OR if the fixture
         genetics page scan returns >= 1 operator token.
  (2) raw-genotype-never-reaches-the-no-train-planner
      -> test_probe_raw_genotype_never_reaches_no_train_planner. REDs if a seeded raw genotype
         (`rs\\d+` or `(allele;allele)`) appears in ANY dispatch payload value — i.e. the
         deriver leaked the raw genotype instead of the coarse trait class.
  (3) extend-not-rebuild numstat
      -> test_probe_extend_not_rebuild_frozen_set_numstat_zero. REDs if `git diff --numstat
         <fork-point>` over the nine frozen engine files + `scripts/store/*` emits any row.
  (4) ingestion-gated
      -> test_probe_ingestion_gated_ungated_genetics_page_blocked. REDs if an ungated genetics
         page is NOT blocked by wiki-ingest-lint.sh (exit 0 where exit 1 is required).
  (5) honest-no-match / never-auto-cross-excluded
      -> test_probe_honest_no_match_research_gap_and_excluded_never_crossed. REDs if a curated
         variant with no library page produces a fabricated trait token instead of a research
         gap, or if a seeded excluded (APOE) genotype is matched or queried.

LIVE run (operator-gated, NOT a CI gate). The operator-present real-`aplus-research` variant
lookups + real spend + real time, end-to-end through dispatch -> de-associated query -> gated
library cache -> local match -> DNA-aware plan (the OS-egress-guard LIVE form of the
de-association + raw-genotype-to-planner probes) is OQ-1 — the operator-present checkpoint
AFTER this build. It is deliberately NOT a `@pytest.mark.skipif` CI variant: it is an operator
checkpoint, not a collected-skipped test.
"""

import functools
import inspect
import os
import re
import subprocess
from pathlib import Path

import pytest

import scripts.model.key_source as key_source
from scripts.genetics import match as gmatch
from scripts.genetics import research_query, variants
from scripts.guard import pii_scan
from scripts.model.client import ModelClient
from scripts.plan import router
from scripts.store import keying, store

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAN_DATE = "2026-06-29T00:00:00+00:00"

# The raw-genotype patterns the crown-jewel probes scan for (mirroring the matcher /
# router / wiki-gate definitions): an rsID and a paired-allele genotype call.
_RSID_RE = re.compile(r"rs\d+")
_RAW_ALLELE_RE = re.compile(r"\([ACGTDI]+;[ACGTDI]+\)")

# The byte-frozen inner engine + store sink (AC-5). router.py is EXCLUDED — it is T3's
# sanctioned additive seam for the de-identified `genetic-trait-classes` token.
_FROZEN_SET = (
    # scripts/plan/orchestrate.py CARVED OUT — ADR-0043-T2 (reconcile via cross_domain_seams) superseded the orchestrator; behavioral guarantor tests/serve/test_orchestrator_reconcile.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
    "scripts/plan/pipeline.py",
    # scripts/plan/assemble.py CARVED OUT — ADR-0041-T2 (uniform-program migration) superseded the assemble composer; behavioral guarantor tests/plan/test_assemble.py + tests/plan/test_generate_plan_uniform.py. Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
    # scripts/plan/generate_plan.py CARVED OUT — ADR-0042/0041/0046/0043 operator-signed-off (HARD, ADR Phase-1 gate) superseded plan front door; guarded behaviorally by tests/plan/test_generate_plan.py + core-capability-audit.sh + the per-ADR numstat probes (NOT this byte-guard). Architect ruling docs/adr/.pipeline/frozen-guard-reconciliation-ruling.md §2, feature/comprehensive-plan-adr.
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    # scripts/plan/track.py CARVED OUT — ADR-0044-T2 (mixed-history reader re-point of resolve_plan_progress) superseded track.py; behavioral guarantor tests/store/test_plan_model_reader.py + tests/plan/test_track.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
    "scripts/store/keying.py",
    "scripts/store/store.py",
)

# The clean PII-free record set backing every pass-through Summary Field-Set field, so a
# `summarize` over a seeded store yields a dispatch-COMPLETE summary (mirrors
# tests/plan/test_router.py::_clean_records). Without it, dispatch would raise on a partial
# summary before the genetic-trait token could be inspected.
_CLEAN_RECORDS = (
    ("date-of-birth", "1986-04-12", "intake"),
    ("equipment-access-class", "full-home-gym", "intake"),
    ("raw-lab-values", "ALT 30; AST 28", "lab"),
    ("raw-symptom-free-text", "tweaked back in January", "intake"),
    ("sex-for-dosing", "male", "intake"),
    # OQ-5 re-key: bodyweight-band is now DERIVED from the local `bodyweight-kg` series, so
    # seed a `bodyweight-kg` reading (a single reading -> current + `flat`) — else `summarize`
    # omits the now-derived token and `dispatch` raises "partial summary, missing".
    ("bodyweight-kg", "82", "intake"),
    ("goal-domains", "strength;recovery", "intake"),
    ("goal-targets", "return to pre-Jan-2026 loading", "intake"),
    ("goal-priority-order", "recovery>strength", "intake"),
    ("recovery-status-band", "moderate", "intake"),
    ("hard-limits", "no overhead pressing", "intake"),
)


# --------------------------------------------------------------------------- #
# Fixtures / helpers (one home each — no copy-paste of the mock-author plumbing).
# --------------------------------------------------------------------------- #


class _TraitEchoBackend:
    """A deterministic plan-author backend that echoes the summary's genetic trait class.

    The trait class is the ONLY DNA-derived content in the authored plan, so the
    headline's content-trace is non-tautological: a constant or empty token could not
    carry the fixture finding's trait class into the plan signal. Records each
    `(domain, summary)` it receives so a test can assert the author saw the de-id token.

    Attributes:
        calls (list): The `(domain, summary)` pairs the backend's `author` received.
    """

    def __init__(self):
        self.calls = []

    def author(self, domain, summary):
        self.calls.append((domain, summary))
        trait = summary.get("genetic-trait-classes", "")
        return {
            "specialist": "personal-trainer",
            "recommendations": [
                {
                    "claim": f"caffeine-timing and recovery guidance informed by "
                    f"genetic trait class(es): {trait}",
                    "source": "ACSM resistance-training guidelines 2024",
                    "confidence_tier": "established",
                    "reversibility": "fully reversible on discontinuation",
                    "category": "training",
                    "payload": {"name": "Genotype-aware caffeine timing",
                                "detail": "per the matched trait class"},
                }
            ],
        }


def _seed_plan_store(root, *, dna=()):
    """Seed a dispatch-complete plan store + any `dna-report` genotypes; return a bound reader.

    Args:
        root (str | Path): The instance store root (a tmp dir).
        dna (iterable): `(item, value)` pairs appended under `source="dna-report"` (the
            T2 matcher's genotype read surface, e.g. `("CYP1A2 rs762551", "(A;A)")`).

    Returns:
        (Callable) `store.read` pre-bound to `root` (the summarize caller contract).
    """
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    def _append(item, value, source):
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": PLAN_DATE, "source": source, "value": value},
            root=root,
        )

    for item, value, source in _CLEAN_RECORDS:
        _append(item, value, source)
    for item, value in dna:
        _append(item, value, "dna-report")
    return functools.partial(store.read, root=root)


def _write_genetics_page(directory, *, gene, rsid, findings, slug=None,
                         provenance_dir="design/.test-design-work", provenance_slug="test"):
    """Write a genetics page in the pinned T1<->T2 format (matcher- AND gate-parseable).

    Args:
        directory (str | Path): The target genetics-library directory.
        gene (str): The gene symbol (frontmatter + `## Genotype Findings` selector key).
        rsid (str): The rs-id.
        findings (iterable): `(genotype, trait_class, prose)` tuples; each becomes a
            `- <genotype>: <trait-class> — <prose>` finding line (em-dash U+2014).
        slug (str, optional): The page slug; defaults to `<gene-lower>-<rsid>`.

    Returns:
        (Path) The written page.
    """
    slug = slug or f"{gene.lower()}-{rsid}"
    lines = [
        "---",
        f"title: {gene} {rsid}",
        "type: genetics",
        f"permalink: a-plus-maxing/library/genetics/{slug}",
        f"gene: {gene}",
        f"rsid: {rsid}",
        "evidence_tier: B",
        "created: 2026-06-02",
        "last_verified: 2026-06-02",
        f"provenance_dir: {provenance_dir}",
        f"provenance_slug: {provenance_slug}",
        "---",
        "",
        f"# {gene} {rsid}",
        "",
        "## Genotype Findings",
    ]
    for genotype, trait_class, prose in findings:
        lines.append(f"- {genotype}: {trait_class} — {prose}")
    page = Path(directory) / f"{slug}.md"
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return page


def _operator_identity_config(path):
    """Write a fixture operator-identity token config (one regex per line); return it.

    A non-vacuous, deterministic stand-in for the gitignored
    `pii_scan.DEFAULT_IDENTITY_CONFIG` (absent in CI), so the de-association /
    library-association scans can be proven to RED on a planted token, not merely
    pass because the config was empty.
    """
    Path(path).write_text("Waldo\\s+Testname\n", encoding="utf-8")
    return path


def _author_plan(store_read, *, genetics_library_root):
    """Drive the real summarize -> dispatch -> ModelClient.author plan-signal path.

    Only the model backend is mocked, injected at the ADR-0015 `ModelClient(backend=...)`
    seam; the de-id summary + the dispatch whitelist are the real production code.

    Returns:
        (tuple) `(summary, plan_signal, backend)`.
    """
    summary = router.summarize(store_read, genetics_library_root=genetics_library_root)
    router.dispatch(summary)  # the de-id payload passes the closed-field-set whitelist
    backend = _TraitEchoBackend()
    client = ModelClient(backend=backend)  # ADR-0015 mock-author seam
    plan_signal = client.author("workout", summary)
    return summary, plan_signal, backend


def _claim_text(plan_signal):
    """Concatenate every recommendation `claim` in an author envelope (the trace target)."""
    return " ".join(rec.get("claim", "") for rec in plan_signal.get("recommendations", []))


def _wiki_lint_repo(tmp_path):
    """Scaffold a temp wiki repo + a 0-spend bda stub for the ingestion-gate probe.

    Returns:
        (tuple) `(repo_root, bda_stub_path)`.
    """
    repo = tmp_path / "wikirepo"
    (repo / "vault/library/genetics").mkdir(parents=True)
    (repo / "vault/meta").mkdir(parents=True)
    (repo / "design/.test-design-work").mkdir(parents=True)
    (repo / "vault/meta/index.md").write_text(
        "# Wiki Index\n## genetics/\n- [[library/genetics/cyp1a2-rs762551]]\n",
        encoding="utf-8",
    )
    bda = tmp_path / "bda-pass.sh"
    bda.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    bda.chmod(0o755)
    return repo, bda


def _run_wiki_lint(repo, bda, page):
    """Run wiki-ingest-lint.sh over a repo-relative page; return its exit code."""
    proc = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts/wiki-ingest-lint.sh"), page],
        cwd=repo,
        env={**os.environ, "WIKI_REPO_ROOT": str(repo), "WIKI_BDA_CMD": str(bda)},
        capture_output=True,
        text=True,
    )
    return proc.returncode


# --------------------------------------------------------------------------- #
# Cycle 1 — the headline trait-in-plan land + the FIX-1 production no-arg path +
# the failing-capable negative control + the mock-tested 0-live-spend proof.
# --------------------------------------------------------------------------- #


def test_headline_dna_fixture_genotype_informs_plan_traced_trait_class(tmp_path):
    """AC-1: a fixture genotype -> match -> token -> dispatch -> author -> a traced plan trait.

    Non-tautological: the plan signal's recommendation CONTAINS the FIXTURE finding's trait
    class (content-traceable through the whole chain), never merely "a plan was produced".
    """
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[
            ("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]"),
            ("(C;C)", "slow-caffeine-metabolism", "slow clearance [3]"),
        ],
    )
    store_read = _seed_plan_store(tmp_path / "inst", dna=[("CYP1A2 rs762551", "(A;A)")])

    summary, plan_signal, backend = _author_plan(store_read, genetics_library_root=lib)

    assert "fast-caffeine-metabolism" in summary["genetic-trait-classes"]
    # the author RECEIVED the de-id summary carrying the coarse trait token
    assert backend.calls
    assert backend.calls[-1][1]["genetic-trait-classes"] == "fast-caffeine-metabolism"
    # the plan signal TRACES to the fixture finding's trait class (match -> ... -> author)
    assert "fast-caffeine-metabolism" in _claim_text(plan_signal)


def test_different_fixture_genotype_yields_different_plan_trait(tmp_path):
    """AC-1 (A != B): a DIFFERENT fixture genotype -> a DIFFERENT plan trait (not a constant)."""
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[
            ("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]"),
            ("(C;C)", "slow-caffeine-metabolism", "slow clearance [3]"),
        ],
    )
    read_a = _seed_plan_store(tmp_path / "inst_a", dna=[("CYP1A2 rs762551", "(A;A)")])
    read_b = _seed_plan_store(tmp_path / "inst_b", dna=[("CYP1A2 rs762551", "(C;C)")])

    summary_a, plan_a, _ = _author_plan(read_a, genetics_library_root=lib)
    summary_b, plan_b, _ = _author_plan(read_b, genetics_library_root=lib)

    assert summary_a["genetic-trait-classes"] == "fast-caffeine-metabolism"
    assert summary_b["genetic-trait-classes"] == "slow-caffeine-metabolism"
    assert summary_b["genetic-trait-classes"] != summary_a["genetic-trait-classes"]
    assert "fast-caffeine-metabolism" in _claim_text(plan_a)
    assert "slow-caffeine-metabolism" in _claim_text(plan_b)
    assert "fast-caffeine-metabolism" not in _claim_text(plan_b)


def test_headline_production_no_arg_summarize_is_dna_aware(tmp_path, monkeypatch):
    """FIX-1/CQ-1: the frozen `summarize(store_read)` no-arg signature is DNA-aware.

    Monkeypatches the deriver's MODULE-LEVEL default genetics-library root (not the param)
    to the fixture library — proving the call path the live `generate_plan` / `orchestrate`
    callers use carries the trait class without a caller edit.
    """
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]")],
    )
    store_read = _seed_plan_store(tmp_path / "inst", dna=[("CYP1A2 rs762551", "(A;A)")])
    monkeypatch.setattr(router, "GENETICS_LIBRARY_DEFAULT_ROOT", lib)

    summary = router.summarize(store_read)  # the frozen production no-arg signature

    assert "fast-caffeine-metabolism" in summary["genetic-trait-classes"]


def test_production_no_arg_negative_control_distinguishes_no_match_from_disabled(
    tmp_path, monkeypatch
):
    """FIX-1/CQ-1 negative control: wired-to-the-real-default-no-match yields the empty token.

    With the default root monkeypatched to a real-but-matching-page-REMOVED library, the
    no-arg `summarize` yields `""` — distinguishing "wired to the real default, no match"
    from "feature disabled". The always-set criterion alone cannot make this distinction.
    """
    empty_lib = tmp_path / "genlib_empty"
    empty_lib.mkdir()  # a real default root, but with NO matching page
    store_read = _seed_plan_store(tmp_path / "inst", dna=[("CYP1A2 rs762551", "(A;A)")])
    monkeypatch.setattr(router, "GENETICS_LIBRARY_DEFAULT_ROOT", empty_lib)

    summary = router.summarize(store_read)

    assert summary["genetic-trait-classes"] == ""


def test_negative_control_no_dna_readings_no_genetic_trait_in_plan(tmp_path):
    """AC-2: the failing-capable negative control — no dna-report readings -> no plan trait.

    Drives the SAME pipeline with no `dna-report` genotype: the token is `""` and the plan
    signal carries no genetic trait — proving the headline's trait-in-plan assertion goes RED
    on the no-DNA state (it is not a constant-pass).
    """
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]")],
    )
    store_read = _seed_plan_store(tmp_path / "inst", dna=[])  # no DNA-derived signal

    summary, plan_signal, _ = _author_plan(store_read, genetics_library_root=lib)

    assert summary["genetic-trait-classes"] == ""
    assert "fast-caffeine-metabolism" not in _claim_text(plan_signal)


def test_zero_live_spend_mock_seam_no_key_no_aplus_research(tmp_path, monkeypatch):
    """AC-7: the full E2E runs with no key, no network, 0 spend, 0 aplus-research dispatch.

    A spy on the live backend's lone key gate `key_source.resolve` records 0 calls (the live
    lane is never touched), and the T4 variant dispatch is the `dispatcher=None` dry-run.
    """
    resolve_calls = []

    def _spy(*args, **kwargs):
        resolve_calls.append(1)
        raise AssertionError("key_source.resolve must not run in the mock E2E (0 live spend)")

    monkeypatch.setattr(key_source, "resolve", _spy)

    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]")],
    )
    store_read = _seed_plan_store(tmp_path / "inst", dna=[("CYP1A2 rs762551", "(A;A)")])

    _summary, plan_signal, _backend = _author_plan(store_read, genetics_library_root=lib)

    # the T4 variant dispatch is the 0-spend dry-run stub (no live aplus-research Agent call)
    assert research_query.dispatch_variant_research("CYP1A2", "rs762551") == \
        research_query.build_variant_query("CYP1A2", "rs762551")

    assert resolve_calls == []  # the live key/spend lane was never reached
    assert "fast-caffeine-metabolism" in _claim_text(plan_signal)
    # the mock is injected at the ADR-0015 ModelClient(backend=...) seam (source self-assert)
    src = Path(__file__).read_text(encoding="utf-8")
    assert "ModelClient(backend=" in src


# --------------------------------------------------------------------------- #
# Cycle 2 — the composed runtime falsification probes.
# --------------------------------------------------------------------------- #


def test_probe_crown_jewel_egress_de_associated_and_library_operator_free(tmp_path):
    """AC-3: the outbound variant query is de-associated + allele-agnostic; the library is operator-free.

    Positive control: `build_variant_query` carries the gene + rsID, is allele-agnostic (no
    allele param, no paired-allele token), and PASSES the guard. Negative controls: injecting
    an allele OR an operator-identity token makes the guard RAISE (it trips ONLY on a
    violation). Library-association: the fixture genetics page scans 0 operator tokens.
    """
    cfg = _operator_identity_config(tmp_path / "op-identity.txt")

    query = research_query.build_variant_query("CYP1A2", "rs762551")
    assert "CYP1A2" in query and "rs762551" in query
    assert not _RAW_ALLELE_RE.search(query)  # allele-agnostic string
    assert "allele" not in inspect.signature(research_query.build_variant_query).parameters
    research_query.assert_query_de_associated(query, identity_config=cfg)  # passes clean

    # the guard trips ONLY on a violation (failing-capable, both axes)
    with pytest.raises(ValueError):
        research_query.assert_query_de_associated(
            query + " the operator genotype is (C;G)", identity_config=cfg
        )
    with pytest.raises(ValueError):
        research_query.assert_query_de_associated(
            query + " for Waldo Testname", identity_config=cfg
        )
    # the fixture token config is non-vacuous — a planted operator token IS detected
    assert pii_scan.scan_text("contact Waldo Testname today", token_config=cfg) >= 1

    # library-association: the variant-keyed page is operator-free. include_dob=False:
    # a genetics PAGE carries research/provenance DATES that are citations, not the
    # operator's DOB — the DOB class guards the operator-VALUE boundary, not public
    # library content (bead yduw; matches the research_query + wiki-ingest-lint guards).
    lib = tmp_path / "genlib"
    lib.mkdir()
    page = _write_genetics_page(
        lib, gene="CYP1A2", rsid="rs762551",
        findings=[("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]")],
    )
    # scan_public_content mirrors the production landed-page guard (research_query SEC3) —
    # base classes only; a research/provenance date or numeric citation is not flagged.
    assert pii_scan.scan_public_content(page.read_text(encoding="utf-8"),
                                        token_config=cfg, full=True) == 0


def test_probe_raw_genotype_never_reaches_no_train_planner(tmp_path):
    """AC-4: the raw rsID+allele genotype reaches NO dispatch payload value (only the coarse class).

    Seeds the operator's raw genotype, builds the dispatch payload, and asserts no payload
    VALUE carries an `rs\\d+` or `(allele;allele)` token — the coarse `genetic-trait-classes`
    axis crossed, the raw genotype did not.
    """
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, gene="MTNR1B", rsid="rs10830963",
        findings=[("(C;G)", "melatonin-glucose-sensitive",
                   "late-evening carbohydrate raises fasting glucose [1]")],
    )
    store_read = _seed_plan_store(tmp_path / "inst", dna=[("MTNR1B rs10830963", "(C;G)")])

    summary = router.summarize(store_read, genetics_library_root=lib)
    payloads = []
    router.dispatch(summary, sink=payloads.append)
    payload = payloads[0]

    for field, value in payload.items():
        if value is None:
            continue
        text = str(value)
        assert not _RSID_RE.search(text), f"rsID leaked into dispatch payload value {field!r}"
        assert not _RAW_ALLELE_RE.search(text), \
            f"raw allele leaked into dispatch payload value {field!r}"
    assert "(C;G)" not in str(payload) and "rs10830963" not in str(payload)
    # the coarse de-id axis DID cross (proving the field is wired, the raw value just stripped)
    assert payload["genetic-trait-classes"] == "melatonin-glucose-sensitive"


def test_probe_ingestion_gated_ungated_genetics_page_blocked(tmp_path):
    """AC-6 (ingestion-gated): an ungated genetics page is BLOCKED; a valid one PASSES.

    Re-asserts T1's gate end-to-end via the real `wiki-ingest-lint.sh` (subprocess, bda
    stubbed for 0 spend). Non-tautological — the gate is not always-fail.
    """
    repo, bda = _wiki_lint_repo(tmp_path)
    gn = repo / "vault/library/genetics"

    _write_genetics_page(
        gn, gene="CYP1A2", rsid="rs762551", slug="cyp1a2-rs762551",
        findings=[
            ("(A;A)", "fast-caffeine-metabolism", "clears caffeine quickly [1]"),
            ("(C;C)", "slow-caffeine-metabolism", "slow clearance [3]"),
        ],
    )
    assert _run_wiki_lint(repo, bda, "vault/library/genetics/cyp1a2-rs762551.md") == 0

    (gn / "ungated.md").write_text(
        "---\ntitle: Ungated\ntype: genetics\n"
        "permalink: a-plus-maxing/library/genetics/ungated\n---\n\n"
        "# Ungated\n\nProse, no gene/rsid/provenance/findings.\n",
        encoding="utf-8",
    )
    assert _run_wiki_lint(repo, bda, "vault/library/genetics/ungated.md") == 1


def test_probe_honest_no_match_research_gap_and_excluded_never_crossed(tmp_path):
    """AC-6 (honest-no-match / never-auto-cross): an absent page is a research gap; APOE is never crossed.

    (a) A curated variant the operator carries whose library page is ABSENT is NOT matched and
        NOT in the trait token (no fabrication), and IS reported in `unmatched_planning_variants`.
    (b) A seeded excluded (APOE) genotype is NEVER matched, and `dispatch_variant_research`
        RAISES for it (never queried).
    """
    assert ("APOE", "rs429358") in variants.EXCLUDED_VARIANTS
    lib = tmp_path / "genlib"
    lib.mkdir()  # deliberately EMPTY — no page for the curated ACTN3 variant
    store_read = _seed_plan_store(
        tmp_path / "inst",
        dna=[("ACTN3 rs1815739", "(C;T)"), ("APOE rs429358", "(C;C)")],
    )

    matches = gmatch.match_genotypes(store_read, library_root=lib)
    matched_genes = {m["gene"] for m in matches}
    assert "ACTN3" not in matched_genes  # absent page -> no fabricated match
    assert "APOE" not in matched_genes  # excluded -> never even read by the curated walk

    gaps = gmatch.unmatched_planning_variants(store_read, library_root=lib)
    assert {"gene": "ACTN3", "rsid": "rs1815739"} in gaps  # the honest research gap

    summary = router.summarize(store_read, genetics_library_root=lib)
    assert summary["genetic-trait-classes"] == ""  # nothing resolved -> no fabricated token

    with pytest.raises(ValueError):
        research_query.dispatch_variant_research("APOE", "rs429358")  # never queried


# --------------------------------------------------------------------------- #
# Cycle 3 — EXTEND-NOT-REBUILD.
# --------------------------------------------------------------------------- #


def test_probe_extend_not_rebuild_frozen_set_numstat_zero():
    """AC-5 (EXTEND-NOT-REBUILD): the frozen engine + store spine is byte-unchanged from the fork.

    `git diff --numstat <fork-point>` over the nine frozen files (`_FROZEN_SET`: the 7 plan-engine
    files + `scripts/store/keying.py` + `scripts/store/store.py`) emits 0 rows — the authoritative
    ADR-0032 frozen surface (ADR-0032 Decision "Extend-not-rebuild"). router.py is T3's sanctioned
    additive seam, not in the frozen set. Mirrors
    tests/serve/test_route.py::test_frozen_engine_byte_unchanged; failing-capable: a transient
    edit to any frozen file emits a row.

    Reconciled for ADR-0040 (large-change hold): the former whole-`scripts/store/*` over-freeze
    is dropped — it over-reached ADR-0032:107 (which names keying.py + store.py, not the whole
    dir) and forbade the ADR-0040-sanctioned additive store surface (the bounded `plan-confirm::`
    stream `scripts/store/plan_confirm.py`, OQ-1 amending ADR-0038; and `read_plan`'s AR-007
    read-side skip in `plan_schema.py`). `_FROZEN_SET` still byte-freezes the record spine.
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()

    rows = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", *_FROZEN_SET],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen engine/store file was edited (EXTEND-NOT-REBUILD broken): {changed}"
