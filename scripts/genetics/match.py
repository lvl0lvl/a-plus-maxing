"""Local genotype↔library matcher — pure, local, read-only, 0 egress.

Resolves the operator's curated-variant genotypes against the local
`vault/library/genetics/` pages. The operator's allele FACTS are read through
the INJECTED per-item `store_read` surface; the pinned-format genetics pages are
parsed off `library_root`. This module imports no outbound HTTP client and no
model SDK and writes nothing to the store: the operator's raw genotypes never
leave the machine, and an unresolved variant is reported as an honest research
gap, never a fabricated finding.
"""

import os
from pathlib import Path

from scripts.genetics.variants import PLANNING_RELEVANT_VARIANTS, variant_item


def _frontmatter(text):
    """Parse the leading `---`-delimited scalar frontmatter block into a dict."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def _normalize_genotype(genotype):
    """Canonicalize a genotype so allele orientation does not matter ((G;C)≡(C;G))."""
    token = genotype.strip()
    parenthesized = token.startswith("(") and token.endswith(")")
    inner = token[1:-1] if parenthesized else token
    if ";" in inner:
        inner = ";".join(sorted(allele.strip() for allele in inner.split(";")))
    return f"({inner})" if parenthesized else inner


def _genotype_findings(text):
    """Parse the `## Genotype Findings` section into {normalized-genotype: (trait_class, implication)}."""
    findings = {}
    in_section = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            in_section = line == "## Genotype Findings"
            continue
        if not in_section or not line.startswith("- "):
            continue
        body = line[2:]
        genotype, colon, rest = body.partition(":")
        trait_class, dash, implication = rest.partition("—")
        if not colon or not dash:
            continue
        findings[_normalize_genotype(genotype)] = (trait_class.strip(), implication.strip())
    return findings


def _find_page(library_root, gene, rsid):
    """Return the genetics page whose frontmatter `gene`+`rsid` match, or None."""
    for page in sorted(Path(library_root).glob("*.md")):
        if page.name.startswith("_"):
            continue  # never parse the `_template.md` scaffold as a real page
        fields = _frontmatter(page.read_text())
        if fields.get("gene") == gene and fields.get("rsid") == rsid:
            return page
    return None


def _store_safe_item(gene, rsid):
    """Derive the variant's `dna-report` store-item key, store-path-safe (BUG-1).

    The variant->store-item key derivation: `variant_item(gene, rsid)`, guarded so a
    path-escaping curated gene token can never reach `store.read`. The real fix is the
    curated data (`variants.py`: every gene token is a store-conformant name), but a
    future `/`-bearing (or otherwise path-traversing) curated gene MUST fail-closed
    HERE — naming the gene at the derivation seam — rather than crash mid-iteration in
    `store._item_path`'s cryptic path-escape raise (which the production matcher reads
    for EVERY curated variant). Mirrors the store's own direct-child item rule.
    """
    item = variant_item(gene, rsid)
    if "/" in item or os.sep in item or (os.altsep and os.altsep in item) or item in (
        "",
        ".",
        "..",
    ):
        raise ValueError(
            f"curated gene token {gene!r} derives a store-path-unsafe item key {item!r} "
            f"(BUG-1, ADR-0032-T3); curated gene tokens must be store-conformant"
        )
    return item


def _operator_genotype(store_read, gene, rsid):
    """Return the operator's latest `dna-report` allele call for a variant, or None."""
    readings = [r for r in store_read(_store_safe_item(gene, rsid)) if r.get("source") == "dna-report"]
    if not readings:
        return None
    return readings[-1]["value"]


def _resolve_finding(library_root, gene, rsid, genotype):
    """Return (trait_class, implication, page) for the operator's genotype, or None."""
    page = _find_page(library_root, gene, rsid)
    if page is None:
        return None
    finding = _genotype_findings(page.read_text()).get(_normalize_genotype(genotype))
    if finding is None:
        return None
    trait_class, implication = finding
    return trait_class, implication, str(page)


def match_genotypes(store_read, *, library_root):
    """Resolve each curated variant the operator carries against the local library.

    Iterates ONLY `PLANNING_RELEVANT_VARIANTS`, so a non-curated / excluded item
    is never read. For each curated variant the operator carries a `dna-report`
    genotype for, it finds the `vault/library/genetics/` page by `gene`+`rsid`
    and selects the per-genotype finding by the operator's LOCAL allele
    (orientation-normalized). An unresolved variant produces no match (the honest
    gap is reported by `unmatched_planning_variants`).

    Args:
        store_read (Callable): The per-item `store.read` surface, pre-bound to the
            instance root by the caller; `store_read("<GENE> <rsID>")` -> readings.
        library_root (str | Path): The `vault/library/genetics/` root.

    Returns:
        (list) One dict per resolved variant — `{gene, rsid, genotype, trait_class,
        implication, page}`. The `genotype` is LOCAL; the consumer collects only
        the coarse `trait_class`.
    """
    library_root = Path(library_root)
    matches = []
    for gene, rsid in PLANNING_RELEVANT_VARIANTS:
        genotype = _operator_genotype(store_read, gene, rsid)
        if genotype is None:
            continue
        resolved = _resolve_finding(library_root, gene, rsid, genotype)
        if resolved is None:
            continue
        trait_class, implication, page = resolved
        matches.append(
            {
                "gene": gene,
                "rsid": rsid,
                "genotype": genotype,
                "trait_class": trait_class,
                "implication": implication,
                "page": page,
            }
        )
    return matches


def unmatched_planning_variants(store_read, *, library_root):
    """Return the research-gap list — curated variants whose finding does not resolve.

    The honest other half of `match_genotypes`'s curated-set walk: a curated
    variant the operator carries a `dna-report` genotype for, but whose library
    finding does NOT resolve (page absent, OR no `## Genotype Findings` entry for
    the operator's normalized genotype). An unresolved variant is reported here,
    NEVER fabricated as a match. Bounded to the curated set, so an excluded /
    non-curated variant never appears.

    Args:
        store_read (Callable): The per-item `store.read` surface, pre-bound to the
            instance root by the caller.
        library_root (str | Path): The `vault/library/genetics/` root.

    Returns:
        (list) One `{gene, rsid}` dict per curated variant the operator carries but
        whose library finding does not resolve.
    """
    library_root = Path(library_root)
    gaps = []
    for gene, rsid in PLANNING_RELEVANT_VARIANTS:
        genotype = _operator_genotype(store_read, gene, rsid)
        if genotype is None:
            continue
        if _resolve_finding(library_root, gene, rsid, genotype) is None:
            gaps.append({"gene": gene, "rsid": rsid})
    return gaps
