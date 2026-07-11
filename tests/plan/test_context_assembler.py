"""Tests for the Context Assembler — identity-stripped full record + genetics carve-out.

`assemble_context(store_read, ...)` replaces `router.summarize`'s coarse 18-token collapse
on the plan path: it feeds each dispatched specialist the operator's FULL health-substance
record with ONLY pure identity (+ the 3 health-identifier classes) stripped. On the plan
path its output flows straight to the model with NO downstream de-id pass or field-set
whitelist, so the strip inside `assemble_context` is the SOLE control — the crown-jewel PII
boundary. AC-4 (identity-leak) and AC-5 (genetics carve-out) are therefore COMPLETE,
DEPTH-PROOF, mutation-RED-capable falsifiers: a de-id-bypass mutation turns each RED against
the GREEN implementation (the Step-2.5 mutation dance, run out-of-band, not in this file).

ALL fixtures are SYNTHETIC — 0 real operator PII (the repo is PUBLIC), 0 live-API calls
(the module reads a store-read callable + does string/de-id work only).
"""

import functools
import re
from pathlib import Path

import pytest

from scripts.genetics.variants import variant_item
from scripts.guard import pii_scan
from scripts.plan import context_assembler, router
from scripts.store import keying, store

PLAN_DATE = "2026-06-18"

# A distinctive SYNTHETIC operator name — never a real person (public repo).
SYNTH_NAME = "Zephyrina Testwood"


# --- fixtures ------------------------------------------------------------------


def _append(root, item, value, source="intake"):
    """store.append one reading carrying every Line Field Set field (mirrors the store fixtures)."""
    store.append(
        item,
        {f: None for f in keying.LINE_FIELDS}
        | {"item": item, "timepoint": PLAN_DATE, "source": source, "value": value},
        root=root,
    )


def _seed(root, items, source="intake"):
    """Seed synthetic `{item: value}` state into a real temp store; return a bound reader.

    Returns a `store.read` pre-bound to `root` — the instance-root-bound `store_read`
    callable `assemble_context` (and `router.summarize`) consume.
    """
    for item, value in items.items():
        _append(root, item, value, source)
    return functools.partial(store.read, root=root)


def _identity_config(tmp_path, name=SYNTH_NAME):
    """Write a gitignored-style operator-identity token config with one synthetic-name regex."""
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text(name + "\n")
    return cfg


def _write_genetics_page(library_root, gene, rsid, findings, slug=None):
    """Write a fixture genetics page in the pinned T1<->T2 format (mirrors tests/plan/test_router.py)."""
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


# The 10 identity/identifier classes of router.EXCLUDED_RAW_PII — each with a distinctive
# SYNTHETIC value. NONE is on the health-substance allowlist, so all are structurally
# unreadable (the crown-jewel exclusion). The 3 health-identifier classes
# (medical-record-number/insurance-id/provider-name) are the concrete Security-F1 leak a
# denylist would admit.
_IDENTITY_VALUES = {
    "legal-name": SYNTH_NAME,
    "date-of-birth": "1979-03-22",
    "government-id": "GOVT-SYNTH-88817766",
    "email-address": "zephyrina.synth@example.test",
    "phone-number": "+1-555-0100",
    "postal-address": "742 Synthetic Way, Testville, CA 90210",
    "geolocation": "37.4220,-122.0841",
    "medical-record-number": "MRN-SYNTH-4471",
    "insurance-id": "INS-SYNTH-99823",
    "provider-name": "Dr. Faux Synthwell",
}


def flatten_scalars(payload):
    """Yield EVERY leaf string in `payload`, recursing dict values AND list items.

    The shared RECURSIVE scan (Security-F2/QA-F1): defense-in-depth on top of the module's
    FLAT-SCALAR return contract. Walks to every leaf regardless of nesting so the
    identity/genotype scans below cannot false-GREEN on a nested leak. Validated
    INDEPENDENTLY by `test_flatten_scan_reaches_nested_leaf`.
    """

    def _walk(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                yield from _walk(value)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                yield from _walk(item)
        elif obj is not None:
            yield str(obj)

    yield from _walk(payload)


# --- AC-1 / AC-2: no-collapse, real detail present -----------------------------


def test_rich_free_text_survives_uncollapsed(tmp_path):
    """AC-1: a rich free-text program survives UNCOLLAPSED into the assembled context.

    A multi-day split + a multi-item stack are carried verbatim — 0 rich sources collapsed
    to a `SUMMARY_FIELD_SET`-only band. Mutation-RED under the literal-`summarize`-pass-through
    mutation (the rich detail becomes absent).
    """
    split = (
        "Mon: back squat 5x5 at RPE 8, romanian deadlift 4x8; "
        "Wed: bench press 5x5, weighted dip 3x10; "
        "Fri: front squat 4x6, barbell row 4x8"
    )
    stack = "creatine monohydrate 5g; l-citrulline 8g; ashwagandha 600mg"
    store_read = _seed(
        tmp_path,
        {"raw-training-detail-free-text": split, "raw-supplement-free-text": stack},
    )
    flat = list(flatten_scalars(context_assembler.assemble_context(store_read)))
    assert any(split in leaf for leaf in flat), "the multi-day split collapsed"
    assert any("l-citrulline 8g" in leaf for leaf in flat), "the stack item collapsed"


def test_operator_specific_detail_present_not_in_summary(tmp_path):
    """AC-2: >=1 operator-specific detail present that `router.summarize` DISCARDS.

    The seeded split parameter is present in `assemble_context`'s flattened values but ABSENT
    from `router.summarize`'s values (which carry only the coarse `training-volume-band`).
    """
    split = "Tuesday: paused front squat 6x3 at 82 percent, tempo pull 4x5"
    store_read = _seed(tmp_path, {"raw-training-detail-free-text": split})
    assembled = list(flatten_scalars(context_assembler.assemble_context(store_read)))
    summary = router.summarize(store_read)
    summarized = list(flatten_scalars(summary))
    assert any(split in leaf for leaf in assembled), "operator-specific detail absent"
    assert all(split not in leaf for leaf in summarized), "summarize unexpectedly carried the raw detail"
    assert "training-volume-band" in summary  # summarize carries only the coarse band


# --- AC-3 / AC-4: identity strip + crown-jewel falsification --------------------


def test_named_identity_items_stripped(tmp_path):
    """AC-3: named-identity store items are stripped — 0 identity tokens in the output."""
    cfg = _identity_config(tmp_path)
    store_read = _seed(
        tmp_path,
        {
            "legal-name": SYNTH_NAME,
            "date-of-birth": "1979-03-22",
            "email-address": "zephyrina.synth@example.test",
            "phone-number": "+1-555-0100",
            "postal-address": "742 Synthetic Way, Testville, CA 90210",
            "raw-supplement-free-text": "creatine monohydrate 5g",  # non-empty record
        },
    )
    result = context_assembler.assemble_context(store_read, identity_config=cfg)
    flat = list(flatten_scalars(result))
    for token in (
        SYNTH_NAME,
        "1979-03-22",
        "zephyrina.synth@example.test",
        "+1-555-0100",
        "742 Synthetic Way",
    ):
        assert all(token not in leaf for leaf in flat), f"pure-identity token leaked: {token}"
    assert sum(pii_scan.scan_text(leaf, token_config=cfg) for leaf in flat) == 0


def test_crown_jewel_no_identity_leak(tmp_path):
    """AC-4 primary (CROWN-JEWEL, LOAD-BEARING): 0 identity/identifier tokens, FULL 10-class partition.

    Seeds SYNTHETIC values for ALL 10 `router.EXCLUDED_RAW_PII` identity/identifier classes;
    RECURSIVE-flattens every returned value; for EACH of the 10 asserts its class is not a
    payload key AND its value appears in 0 flattened values; scans every carried value for
    identity tokens (tmp config) + structural email/phone/postal. Seeding ALL 10 (not a
    hand-picked 5) pins the falsifier at the full exclusion set — the 3 health-identifier
    classes are the concrete Security-F1 leak the denylist admitted. Mutation (i)-1 (add any
    identity/identifier class to the allowlist) drives this RED.
    """
    cfg = _identity_config(tmp_path)
    seed = dict(_IDENTITY_VALUES)
    seed["raw-supplement-free-text"] = "creatine monohydrate 5g"  # non-empty record
    store_read = _seed(tmp_path, seed)
    result = context_assembler.assemble_context(store_read, identity_config=cfg)
    flat = list(flatten_scalars(result))
    for cls, value in _IDENTITY_VALUES.items():
        assert cls not in result, f"identity/identifier class is a payload key (leak): {cls}"
        assert sum(value in leaf for leaf in flat) == 0, f"identity/identifier value leaked: {cls}={value}"
    assert sum(pii_scan.scan_text(leaf, token_config=cfg) for leaf in flat) == 0


def test_identity_in_carried_value_fails_closed(tmp_path):
    """AC-4 secondary (the 8j6 reuse): operator identity smuggled INTO a carried value fails-closed.

    The synthetic operator name embedded inside a carried `raw-training-detail-free-text`
    value is caught by the REUSED `pii_scan.scan_operator_value` gate — `assemble_context`
    RAISES a field-naming ValueError, so the embedded identity never reaches a returned
    payload. The `match=` binds to the value-gate raise (not an incidental ValueError).
    Mutation (i)-2 (drop the value gate) drives this RED (no raise where one was expected).
    """
    cfg = _identity_config(tmp_path)
    store_read = _seed(
        tmp_path,
        {"raw-training-detail-free-text": f"Friday deadlift session, coached by {SYNTH_NAME}"},
    )
    with pytest.raises(
        ValueError,
        match=r"carried field 'raw-training-detail-free-text' carries raw operator PII",
    ) as exc:
        context_assembler.assemble_context(store_read, identity_config=cfg)
    assert SYNTH_NAME not in str(exc.value)  # names the field, never echoes the value
    assert "fail-closed" in str(exc.value)


# --- AC-5: genetics carve-out (RT-008 / Security-F3) ---------------------------


def test_genetics_carve_out_only_coarse_token(tmp_path):
    """AC-5 (GENETICS CROWN-JEWEL): 0 raw rsID/allele tokens; only the coarse trait-class crosses.

    Seeds a raw `dna-report` rsID+allele genotype (`(G;G)` under `MCM6 rs4988235`) + a tmp
    library resolving it to a coarse `lactase-persistent` trait class. RECURSIVE-scans every
    returned value with `router._RAW_GENOTYPE_PATTERNS` — asserts 0 raw genotype tokens reach
    the payload AND the derived coarse token IS present. The raw `dna-report` item is not on
    the allowlist; genetics crosses ONLY via `summarize`'s `_genetic_trait_classes_token`
    branch. Mutation (g)-1 (read the raw `dna-report` item into a carried field) drives the
    raw-genotype scan RED.
    """
    lib = tmp_path / "genlib"
    lib.mkdir()
    _write_genetics_page(
        lib, "MCM6", "rs4988235", [("(G;G)", "lactase-persistent", "persistent lactase expression")]
    )
    _append(tmp_path, variant_item("MCM6", "rs4988235"), "(G;G)", source="dna-report")
    store_read = functools.partial(store.read, root=tmp_path)
    result = context_assembler.assemble_context(store_read, genetics_library_root=lib)
    flat = list(flatten_scalars(result))
    for leaf in flat:
        for pattern in router._RAW_GENOTYPE_PATTERNS:
            assert not pattern.search(leaf), f"raw genotype token leaked into the payload: {leaf}"
    assert any("lactase-persistent" in leaf for leaf in flat), "coarse trait-class token absent"
    assert result.get("genetic-trait-classes") == "lactase-persistent"


# --- AC-6: no-collapse falsification -------------------------------------------


def test_output_not_equal_to_summarize_band(tmp_path):
    """AC-6 (QA-F5 LOAD-BEARING conjunct): the payload is NOT confined to the 18-token band.

    The seeded substantive detail IS present among the flattened values, and the assembled
    values are NOT a subset of the summarize band (`assembled ⊄ band`). The `!= summarize`
    inequality is a SECONDARY / advisory conjunct only (vacuously true across container
    shapes). Mutation (ac6) (return `summarize` verbatim) drives AC-1 + AC-6 both RED.
    """
    split = "Thursday: safety-bar squat 5x5 at RPE 7, glute-ham raise 4x10"
    stack = "creatine 5g; beta-alanine 3.2g; l-theanine 200mg"
    store_read = _seed(
        tmp_path,
        {"raw-training-detail-free-text": split, "raw-supplement-free-text": stack},
    )
    result = context_assembler.assemble_context(store_read)
    band = router.summarize(store_read)
    flat = set(flatten_scalars(result))
    band_values = set(flatten_scalars(band))
    # LOAD-BEARING: substantive detail is present that the coarse band does not carry.
    assert any(split in leaf for leaf in flat), "substantive detail absent (payload confined to band)"
    assert flat - band_values, "assembled values are a subset of the summarize band"
    # advisory conjunct only (carries no RED capability alone).
    assert result != band


# --- Contract pins: flat-scalar return + recursive-scan reach ------------------


def test_return_is_flat_scalar(tmp_path):
    """Gate (a): the return is PINNED FLAT-SCALAR — scalar or list-of-scalar, NO nested dict.

    Nesting cannot exist for identity/genotype to hide in. Failing-capable: a nested-dict
    value introduced during GREEN reds this.
    """
    store_read = _seed(
        tmp_path,
        {
            "raw-supplement-free-text": "creatine 5g; omega-3 2g",
            "raw-symptom-free-text": "mild lower-back tightness after deadlifts",
        },
    )
    result = context_assembler.assemble_context(store_read)

    def _scalar(value):
        return value is None or isinstance(value, (str, int, float, bool))

    assert isinstance(result, dict)
    for key, value in result.items():
        if isinstance(value, list):
            assert all(_scalar(item) for item in value), f"{key} is a list with a non-scalar item"
        else:
            assert _scalar(value), f"{key} carries a non-scalar (nested) value: {type(value)}"


def test_flatten_scan_reaches_nested_leaf():
    """Scan-reach (M2/Security-F2): the recursive scan reaches a value inside a list inside a dict.

    Independent of the assembler / the mutation dance — proves the AC-4/AC-5 scans cannot
    false-GREEN on a nested leak. Failing-capable: a shallow flatten misses the nested sentinel.
    """
    sentinel = "ZZ-UNIQUE-NESTED-SENTINEL-9x7q"
    payload = {
        "top": "surface",
        "listed": ["a", "b"],
        "nested": {"inner": ["x", {"deepest": [sentinel]}]},
    }
    assert sentinel in list(flatten_scalars(payload))


# --- Risk residual: config-absent enlarged blast radius (S2) --------------------


def test_config_absent_residual(tmp_path):
    """Risk residual (S2): config-absent, the STRUCTURAL allowlist exclusion still holds.

    With `identity_config` ABSENT (empty identity-token set), the 10 structured
    identity/identifier classes are STILL excluded (config-independent — they are never on
    the allowlist). The documented enlarged blast radius: a name embedded in a carried
    free-text value is now caught only by the structural email/phone/postal patterns, NOT the
    (empty) operator-identity token set — so it flows verbatim (the residual the production
    precondition, identity_config PRESENT + instance-bound, closes).
    """
    absent = tmp_path / "no-such-identity.txt"
    assert not absent.exists()
    # A residual name DISTINCT from every structured `_IDENTITY_VALUES` value, so the
    # structural-exclusion checks (structured values absent) and the residual check (the
    # free-text name present) do not collide on one string.
    residual_name = "Faelith Mockborne"
    seed = dict(_IDENTITY_VALUES)
    seed["raw-training-detail-free-text"] = f"Monday session logged by {residual_name}"
    store_read = _seed(tmp_path, seed)
    # config absent -> the value-embedded name is NOT caught -> no raise (the residual).
    result = context_assembler.assemble_context(store_read, identity_config=absent)
    flat = list(flatten_scalars(result))
    # structural allowlist exclusion holds for all 10 structured classes regardless of config.
    for cls, value in _IDENTITY_VALUES.items():
        assert cls not in result, f"structured identity/identifier class leaked config-absent: {cls}"
        assert sum(value in leaf for leaf in flat) == 0, f"structured value leaked config-absent: {cls}"
    # the residual: the value-embedded name flows (caught only by structural patterns).
    assert any(residual_name in leaf for leaf in flat), "config-absent residual not demonstrated"
