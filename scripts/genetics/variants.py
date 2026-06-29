"""Curated planning-relevant genetic variants (OQ-3) + the dna-report item-key deriver.

Data only — the operator-curated set of planning-relevant SNPs, the explicitly
excluded (sensitive / non-actionable) set, and the deriver of the durable
`dna-report` store item key. No I/O, no SDK.
"""

# The OQ-3 operator-curated planning-relevant set: (gene-symbol, rs-id) tuples.
# MTHFR contributes two variants (rs1801131 + rs1801133).
PLANNING_RELEVANT_VARIANTS = [
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
]

# Sensitive / non-actionable variants, NEVER auto-matched and NEVER auto-queried
# (ADR-0032 Non-goals + OQ-3). Disjoint from PLANNING_RELEVANT_VARIANTS by gene.
EXCLUDED_VARIANTS = [
    ("APOE", "rs429358"),
    ("DRD2", "rs1800497"),
    ("BDNF", "rs6265"),
]


def variant_item(gene, rsid):
    """Derive the `dna-report` store item key for a variant.

    Args:
        gene (str): The gene symbol (e.g. `MTNR1B`).
        rsid (str): The rs-id (e.g. `rs10830963`).

    Returns:
        (str) The space-joined item key, e.g. `MTNR1B rs10830963` — the durable
        FACT key ADR-0031 stores for a genotype reading.
    """
    return f"{gene} {rsid}"
