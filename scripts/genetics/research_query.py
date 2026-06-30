"""Care-assistant→DNA-research-agent hookup: the de-associated variant-query egress + page landing.

The ONE new named egress class ADR-0032 adds to ADR-0001 — generic, operator-de-associated,
ALLELE-AGNOSTIC genetic-variant literature queries. `build_variant_query` carries only the variant
(gene + rsID), never the operator's allele; `assert_query_de_associated` is the fail-closed guard that
RAISES before any outbound query carrying an allele call or an operator-identity token can leave;
`dispatch_variant_research` refuses any variant ABSENT from the OQ-3 curated allowlist FIRST (the
EXCLUDED denylist kept as defense-in-depth), guards the query, runs the INJECTED dispatcher, and
`land_finding_page` writes the returned finding as a gated `vault/library/genetics/` page the local
matcher consumes. The default dispatch is still a 0-spend dry-run; the live, metered `aplus-research`
run (the dispatcher that produces the ingestion-gate attestation chain) is OQ-1.

The research engine `aplus-research` runs on the SUBSCRIPTION/agent research lane, NOT the no-train
`ModelClient` backend (`scripts/model/client.py`). The dispatcher is INJECTED, so this module itself
imports only `re`, `pathlib`, T2's curated/excluded set, and the read-only operator-PII scanner — no
outbound HTTP client, no model SDK. The landed page is variant-keyed + operator-free by construction.
"""

import re
from pathlib import Path

from scripts.genetics.variants import EXCLUDED_VARIANTS, PLANNING_RELEVANT_VARIANTS
from scripts.guard import pii_scan

# An allele call in an outbound query is the de-association breach: the paired-genotype form
# `(C;G)` OR a bare `genotype is <allele>` statement. The generic per-variant query carries
# neither (it asks about EACH genotype's implications, never the operator's own call).
_ALLELE_CALL = re.compile(r"\([ACGTDI]+;[ACGTDI]+\)|genotype is \(?[ACGTDI]")

# SEC2 path-traversal guard: a landed page's slug must be a safe lowercased filename token — no
# path separator, no `..`, no leading dot — so `Path(root)/f"{slug}.md"` can never escape the root.
_SAFE_SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")

# SEC3 raw-genotype guard (symmetric with the outbound `_ALLELE_CALL` egress guard): a coarse
# trait-class token must carry NO raw genotype — an rsID or a paired-allele call — or the landed
# page would leak a genotype into the PUBLIC wiki the page commits to.
_RAW_GENOTYPE = re.compile(r"rs\d+|\([ACGTDI]+;[ACGTDI]+\)")

# The OQ-3 curated planning-relevant allowlist: dispatch refuses ANY (gene, rsid) absent from
# this set FIRST — auto-research is scoped to the curated variants, never a non-curated one
# (even a non-excluded sensitive variant, e.g. BRCA1 rs80357906, is refused before any build).
_CURATED_VARIANTS = frozenset(PLANNING_RELEVANT_VARIANTS)

# The sensitive / non-actionable genes ADR-0032 never auto-researches (APOE/DRD2/BDNF). Kept as
# defense-in-depth — an excluded variant is, by construction, also absent from _CURATED_VARIANTS.
_EXCLUDED_GENES = frozenset(gene for (gene, _) in EXCLUDED_VARIANTS)


def build_variant_query(gene, rsid):
    """Build a generic, allele-agnostic literature query for a genetic variant.

    The query carries the variant (gene symbol + rs-id) and asks about the
    implications of each genotype — a question anyone could ask about the
    variant. The signature takes NO allele parameter: the operator's own allele
    call never enters the query by construction, so the outbound string is
    de-associated from the operator.

    Args:
        gene (str): The gene symbol (e.g. `ACTN3`).
        rsid (str): The rs-id (e.g. `rs1815739`).

    Returns:
        (str) A generic, allele-agnostic per-variant research query.
    """
    return (
        f"Current 2026 evidence on {gene} {rsid}: the implications of each "
        f"genotype for health, performance, and training."
    )


def assert_query_de_associated(query, *, identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG):
    """Raise (fail-closed) if an outbound variant query is not de-associated.

    The crown-jewel egress guard: an outbound query carrying the operator's
    allele call or an operator-identity token is the ADR-0032 de-association
    breach, so the guard RAISES rather than letting it leave. The identity scan
    reuses `pii_scan.scan_text` — the same operator-PII scanner the router's
    summary boundary raises on — mirroring its scan-then-raise discipline.

    Args:
        query (str): The outbound variant query to check.
        identity_config (str | Path, optional): The gitignored operator-identity
            token config `pii_scan.scan_text` loads; defaults to
            `pii_scan.DEFAULT_IDENTITY_CONFIG`. The structural value-class
            patterns (email/phone/postal) run regardless of the config.
    """
    if _ALLELE_CALL.search(query):
        raise ValueError(
            "variant query carries an allele call — operator de-association breach"
        )
    if pii_scan.scan_text(query, token_config=identity_config):
        raise ValueError(
            "variant query carries an operator-identity token — de-association breach"
        )


def land_finding_page(finding, *, library_root):
    """Write a de-associated variant finding as a gated `vault/library/genetics/` page.

    The variant-keyed, operator-free page the local matcher (`scripts.genetics.match`)
    consumes. The finding carries only variant-general, de-identified content — a
    gene/rsID key, the evidence + provenance frontmatter, and one coarse trait-class
    finding per genotype — so the written page is reusable across operators and never
    operator-associated. The emitted finding lines use the matcher↔gate grammar
    `- <genotype>: <trait-class> — <prose>` with the U+2014 em-dash both sides pin.

    Args:
        finding (dict): The de-identified variant finding. Keys: `gene`, `rsid`,
            `evidence_tier`, `created`, `last_verified`, `provenance_dir`,
            `provenance_slug`, and `genotype_findings` (a list of
            `(genotype, trait_class, prose)` tuples). An optional `slug` overrides
            the default `<gene-lower>-<rsid>`.
        library_root (str | Path): The `vault/library/genetics/` root to write into.

    Returns:
        (Path) The written page path.
    """
    gene = finding["gene"]
    rsid = finding["rsid"]
    slug = finding.get("slug") or f"{gene.lower()}-{rsid}"
    # SEC2 (path traversal): a slug is the page filename — fail-closed on any non-safe token BEFORE
    # any write, so `finding['slug']` can never drive a write outside the library root (e.g. a
    # `../../meta/...` slug). The validated slug also keys the frontmatter permalink below.
    if not _SAFE_SLUG.fullmatch(slug):
        raise ValueError(
            f"genetics page slug {slug!r} is not a safe filename token (^[a-z0-9][a-z0-9-]*$) — "
            f"refusing to write (path-traversal guard)"
        )
    # SEC3 (public-repo guard): the landed page commits to a PUBLIC repo, so each coarse trait-class
    # token must carry no raw genotype — symmetric with the outbound de-association guard. (The
    # whole-page operator-PII rescan runs below, over the rendered content.)
    for _genotype, trait_class, _prose in finding["genotype_findings"]:
        if _RAW_GENOTYPE.search(str(trait_class)):
            raise ValueError(
                f"genetics trait-class token {trait_class!r} carries a raw genotype — refusing to "
                f"land (public-repo guard)"
            )
    lines = [
        "---",
        f"title: {gene} {rsid}",
        "type: genetics",
        f"permalink: a-plus-maxing/library/genetics/{slug}",
        f"gene: {gene}",
        f"rsid: {rsid}",
        f"evidence_tier: {finding['evidence_tier']}",
        f"created: {finding['created']}",
        f"last_verified: {finding['last_verified']}",
        f"provenance_dir: {finding['provenance_dir']}",
        f"provenance_slug: {finding['provenance_slug']}",
        "---",
        "",
        f"# {gene} {rsid}",
        "",
        "## Genotype Findings",
    ]
    for genotype, trait_class, prose in finding["genotype_findings"]:
        lines.append(f"- {genotype}: {trait_class} — {prose}")
    content = "\n".join(lines) + "\n"
    # SEC3 (public-repo guard, symmetric with the outbound `assert_query_de_associated`): rescan the
    # rendered page for operator PII before it lands — the dispatcher content is otherwise verbatim,
    # and the page commits to a PUBLIC repo. Fail-closed rather than leak.
    if pii_scan.scan_text_full(content):
        raise ValueError(
            "genetics finding page carries operator PII — refusing to land (public-repo guard)"
        )
    root = Path(library_root)
    root.mkdir(parents=True, exist_ok=True)
    page = root / f"{slug}.md"
    # SEC2 belt-and-suspenders: even a pattern-valid slug must resolve INSIDE the library root.
    if root.resolve() not in page.resolve().parents:
        raise ValueError(f"genetics page path {page!r} escapes the library root — refusing to write")
    page.write_text(content, encoding="utf-8")
    return page


def dispatch_variant_research(gene, rsid, *, dispatcher=None, library_root=None):
    """Dispatch de-associated current-science research for a planning-relevant variant.

    Refuses any variant ABSENT from the OQ-3 curated allowlist FIRST — before any
    query is built — so a non-curated variant (even a non-excluded sensitive one,
    e.g. BRCA1 rs80357906) is never auto-researched; the EXCLUDED (APOE/DRD2/BDNF)
    denylist is kept as defense-in-depth (an excluded variant is, by construction,
    also non-curated). Otherwise it builds the generic allele-agnostic query, GUARDS
    it fail-closed via `assert_query_de_associated`, then:

    - `dispatcher=None` (the default): a 0-spend dry-run returning the guarded query.
    - `dispatcher` given, `library_root=None`: runs the dispatcher, returns its
      finding (no page written).
    - `dispatcher` AND `library_root` given: runs the dispatcher and LANDS the
      returned finding as a gated genetics page via `land_finding_page`, returning
      the page path.

    The live, metered `aplus-research` Agent dispatch (the dispatcher that produces
    the ingestion-gate attestation chain) is OQ-1; the dispatcher is injected, so no
    live call is made here by default.

    Args:
        gene (str): The gene symbol.
        rsid (str): The rs-id.
        dispatcher (callable, optional): A one-arg callable receiving the guarded
            query and returning a finding dict; when None, the call is a dry-run
            returning the query.
        library_root (str | Path, optional): When given with a dispatcher, the
            `vault/library/genetics/` root the returned finding is landed into.

    Returns:
        (str | dict | Path) The de-associated query (dry-run), the dispatcher's
        finding (no `library_root`), or the landed page path (`library_root` given).
    """
    if (gene, rsid) not in _CURATED_VARIANTS:
        raise ValueError(
            f"{gene} {rsid} is not in the OQ-3 curated planning-relevant set — never auto-researched"
        )
    if gene in _EXCLUDED_GENES:
        raise ValueError(f"{gene} is an excluded (sensitive) variant — never auto-researched")
    query = build_variant_query(gene, rsid)
    assert_query_de_associated(query)
    if dispatcher is None:
        return query
    finding = dispatcher(query)
    if library_root is None:
        return finding
    if finding.get("gene") != gene or finding.get("rsid") != rsid:
        raise ValueError(
            f"dispatched finding {finding.get('gene')} {finding.get('rsid')!r} does not match "
            f"the requested variant {gene} {rsid} — refusing to land a mismatched page"
        )
    return land_finding_page(finding, library_root=library_root)
