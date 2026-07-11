"""Context Assembler: the identity-stripped FULL record fed to each dispatched specialist.

`assemble_context` replaces `router.summarize`'s coarse 18-token collapse on the plan path
(`generate_plan.py:356`). On that path the assembled context flows straight to the model
(`client.author(domain, summary)`, `generate_plan.py:362`) with NO second de-id pass and NO
downstream field-set whitelist — so the strip HERE is the SOLE control (a PUBLIC repo, a
one-way door). The construction MIRRORS `care_chat._care_profile`: the de-id-safe base is
`router.summarize` — identity-safe BY CONSTRUCTION (its keys are `SUMMARY_FIELD_SET`, pinned
disjoint from `EXCLUDED_RAW_PII` at `router.py:668`, so no identity / contact /
health-identifier class appears; the genetics carve-out already reduced the raw genotype to
the coarse `genetic-trait-classes` token) — ENRICHED with an EXPLICIT allowlist of raw
health-substance free-text classes, each carried UNCOLLAPSED.

DESIGN DECISION — ALLOWLIST, not denylist (Security-F1). The read set is
`_HEALTH_SUBSTANCE_ALLOWLIST`, an EXPLICIT tuple of health-substance classes. A class NOT on
it fails CLOSED — it is STRUCTURALLY unreadable, never leaked by default. This excludes all
10 identity/identifier `EXCLUDED_RAW_PII` classes (name, exact DOB, government-id, contact,
geolocation, AND the 3 health-identifier classes medical-record-number / insurance-id /
provider-name) by simply not listing them. A denylist ("read `EXCLUDED_RAW_PII` minus a
hand-picked identity set") LEAKS the 3 health-identifier classes — they are neither derived
nor caught by the operator-identity value gate — the correct crown-jewel posture on a public
repo with no downstream backstop is the allowlist. "ALL health substance flows" is preserved:
the allowlist enumerates EVERY current health-substance class; adding a NEW one is an
auditable edit to this ONE tuple, never a silent default-read. This designs NO new de-id
scheme — it reuses `router.summarize` (the de-id-safe base), the `_care_profile`
explicit-allowlist precedent, and the `pii_scan` value gate.

De-id parked: raw health-substance free-text FLOWS uncollapsed; the ONE preserved
de-id-by-construction is the genetics crown jewel — the raw rsID+allele genotype is NEVER
read (the `dna-report` item is not on the allowlist), genetics crosses only as the coarse
`genetic-trait-classes` token via `summarize`'s `router._genetic_trait_classes_token` branch.
Each carried value transits the reused `pii_scan.scan_operator_value` value gate (the
`summarize` `:848` 8j6 precedent) and FAILS CLOSED on operator identity smuggled into
free-text. The return is a FLAT mapping of scalar / list-of-scalar values — NO nested dict at
any key — so identity or a genotype cannot hide at a nested leaf (the `_care_profile`
`health_detail`/`record` nesting is FLATTENED here: each allowlisted class maps to a flat key).
"""

from scripts.guard import pii_scan
from scripts.plan import router

# The EXPLICIT health-substance ALLOWLIST (Security-F1) — the auditable seam a NEW
# health-substance class is added to. Mirrors `care_chat._CARE_HEALTH_DETAIL`'s
# explicit-allowlist pattern, extended past its 5 to the full plan-relevant set. These are
# EXACTLY the non-identity members of `router.EXCLUDED_RAW_PII` (the raw health-substance
# classes `summarize` collapses to coarse bands FOR THE SPECIALIST); the assembler carries
# them UNCOLLAPSED. This tuple names ONLY health-substance classes — NEVER an identity /
# contact / health-identifier class (those are excluded by not being here).
_HEALTH_SUBSTANCE_ALLOWLIST = (
    "raw-nutrition-free-text",
    "raw-supplement-free-text",
    "raw-peptide-free-text",
    "raw-training-detail-free-text",
    "raw-symptom-free-text",
    "clinical-notes",
    "raw-lab-values",
    "medication-list",
    "raw-training-experience",
    "bodyweight-kg",
)


def assemble_context(store_read, identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG,
                     genetics_library_root=None):
    """Assemble the identity-stripped FULL record a dispatched specialist reasons over.

    The de-id-safe base is `router.summarize` (identity-safe by construction), ENRICHED with
    the operator's raw health-substance free-text read through the EXPLICIT
    `_HEALTH_SUBSTANCE_ALLOWLIST` and carried UNCOLLAPSED. Each carried value transits the
    reused `pii_scan.scan_operator_value` gate and fails closed on operator identity smuggled
    into the free-text. Genetics reaches the record ONLY as the coarse `genetic-trait-classes`
    token the base already carries — the raw rsID+allele genotype is never read (the crown
    jewel). The signature MIRRORS `router.summarize` (same three parameters, same defaults),
    so the plan-path one-arg swap resolves the two kwargs to their defaults exactly as
    `summarize(store_read)` does.

    Args:
        store_read (Callable): The store read surface (`store.read`), instance-root
            pre-bound by the caller (the `router.summarize` caller contract — an unbound
            reader silently reads the wrong instance).
        identity_config (str | Path, optional): The gitignored operator-identity token config
            for the reused `pii_scan` value gate; absent -> empty identity-token detection
            (the structural contact patterns still run). Production precondition (S2): on the
            plan path it MUST be PRESENT + instance-bound when the cwd diverges from the
            instance root (mirrors `summarize`, `router.py:762-767`).
        genetics_library_root (str | Path | None, optional): The `vault/library/genetics/`
            root the coarse-trait-class deriver resolves against; `None` -> the real library
            (production is DNA-aware without a caller edit, mirroring `summarize`).

    Returns:
        (dict) `specialist_input`: the identity-stripped FULL record — a FLAT mapping of
        scalar / list-of-scalar values (no nested dict at any key), carrying the operator's
        substantive health-substance detail UNCOLLAPSED (NOT the coarse 18-token band).

    Raises:
        ValueError: When a carried health-substance value carries raw operator PII (the reused
            `pii_scan` value gate) — surfaced at the boundary, never leaked downstream.
    """
    specialist_input = dict(
        router.summarize(store_read, identity_config, genetics_library_root)
    )
    for field in _HEALTH_SUBSTANCE_ALLOWLIST:
        readings = store_read(field)
        if not readings:
            continue
        value = readings[-1].get("value")
        if not value:
            continue
        # Reuse the `summarize` `:848` 8j6 gate: a carried free-text value is contracted
        # PII-free by store schema, but that contract is unenforced upstream, so enforce it
        # HERE — the assembler IS the 0-raw-PII boundary on the plan path. Names the field,
        # never the value (no PII echo).
        if pii_scan.scan_operator_value(str(value), token_config=identity_config):
            raise ValueError(
                f"assemble_context: carried field {field!r} carries raw operator "
                f"PII; the PII-free-by-store-schema assumption is violated "
                f"(fail-closed)"
            )
        specialist_input[field] = value
    return specialist_input
