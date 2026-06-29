"""Care-assistant→DNA-research-agent hookup (STUB): the de-associated variant-query egress.

The ONE new named egress class ADR-0032 adds to ADR-0001 — generic, operator-de-associated,
ALLELE-AGNOSTIC genetic-variant literature queries. `build_variant_query` carries only the variant
(gene + rsID), never the operator's allele; `assert_query_de_associated` is the fail-closed guard that
RAISES before any outbound query carrying an allele call or an operator-identity token can leave; and
`dispatch_variant_research` refuses any variant ABSENT from the OQ-3 curated allowlist FIRST (the
EXCLUDED denylist kept as defense-in-depth), guards the query, and STUBS the dispatch (the live,
metered `aplus-research` run is OQ-1 — 0 spend here).

The research engine `aplus-research` runs on the SUBSCRIPTION/agent research lane, NOT the no-train
`ModelClient` backend (`scripts/model/client.py`). This module imports only `re`, T2's curated/excluded
set, and the read-only operator-PII scanner — no outbound HTTP client, no model SDK.
"""

import re

from scripts.genetics.variants import EXCLUDED_VARIANTS, PLANNING_RELEVANT_VARIANTS
from scripts.guard import pii_scan

# An allele call in an outbound query is the de-association breach: the paired-genotype form
# `(C;G)` OR a bare `genotype is <allele>` statement. The generic per-variant query carries
# neither (it asks about EACH genotype's implications, never the operator's own call).
_ALLELE_CALL = re.compile(r"\([ACGTDI]+;[ACGTDI]+\)|genotype is \(?[ACGTDI]")

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


def dispatch_variant_research(gene, rsid, *, dispatcher=None):
    """Dispatch de-associated current-science research for a planning-relevant variant (STUB).

    Refuses any variant ABSENT from the OQ-3 curated allowlist FIRST — before any
    query is built — so a non-curated variant (even a non-excluded sensitive one,
    e.g. BRCA1 rs80357906) is never auto-researched; the EXCLUDED (APOE/DRD2/BDNF)
    denylist is kept as defense-in-depth (an excluded variant is, by construction,
    also non-curated). Otherwise it builds the generic
    allele-agnostic query, GUARDS it fail-closed via `assert_query_de_associated`,
    and either runs a 0-spend dry-run (the default) or hands the guarded query to
    an injected dispatcher. The live, metered `aplus-research` Agent dispatch is
    OQ-1 — this stub makes no live call.

    Args:
        gene (str): The gene symbol.
        rsid (str): The rs-id.
        dispatcher (callable, optional): A one-arg callable receiving the guarded
            query; when None, the call is a dry-run returning the query.

    Returns:
        (str | Any) The would-be de-associated query (dry-run), or the injected
        dispatcher's result.
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
    return dispatcher(query)
