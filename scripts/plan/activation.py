"""Progressive-activation gate — the active card-emitting domain set for an operator surface.

The comprehensive plan is PROGRESSIVE (ADR-0046, disposition #24): a domain card renders only
when the operator has a goal or data there, not a fixed template of every specialist for everyone
(`design/specialist-plan-contracts.md` §11-§13 progressive-activation design note). This module is
the gate that decides, from a de-id-safe operator surface, WHICH card-emitting domains are active —
the set a wired dispatcher briefs (gate-at-DISPATCH: don't brief an inactive specialist).

`CARD_DOMAINS` is the §1-§13 card-emitting roster (grounded against
`design/specialist-plan-contracts.md`), DECOUPLED from `scripts.store.plan_schema.PLAN_DOMAINS`
(the closed four the dispatch registries stay at until the Wave-4 roster growth — ADR-0043-T3 — grows
`PLAN_DOMAINS` to match this set). The gate reasons over the full card roster now so its consumers
(ADR-0043-T3 front-door wiring, ADR-0046-T2's fan-out threshold) build against a stable contract.

The §14-genetics / §15-labs specialists are CROSS-CUTTING INPUTS (disposition #25): they feed every
domain's biomarker / PGx substrate but emit NO domain card, so they are never in `CARD_DOMAINS` and
never returned by `active_domains`.

Leaf module: pure literals + set operations, no imports — so no dependency cycle with the plan
front door / generation path can form.
"""

# The §1-§13 CARD-EMITTING domain slugs (design/specialist-plan-contracts.md). The four existing
# plan_schema.PLAN_DOMAINS members (workout / nutrition / supplements / peptides) are a subset — the
# Wave-4 growth (ADR-0043-T3) grows PLAN_DOMAINS to this full set; this gate reasons over it now.
CARD_DOMAINS = frozenset({
    "workout",              # §1  personal-trainer         — Training
    "nutrition",            # §2  nutritionist             — Nutrition
    "peptides",             # §3  peptide-specialist       — Peptides
    "supplements",          # §4  supplement-specialist    — Supplements
    "endocrine",            # §5  endocrine-specialist     — Hormonal
    "cardiovascular",       # §6  cardiovascular-specialist— CV / Metabolic
    "recovery",             # §7  recovery-specialist      — Recovery
    "sleep",                # §8  sleep-coach              — Sleep
    "longevity",            # §9  longevity-strategist     — Longevity
    "mental-performance",   # §10 mental-performance-coach — Mind
    "dermatology",          # §11 dermatologist            — Skin / Hair
    "gi",                   # §12 gi-specialist            — Gut
    "lymphatic",            # §13 lymphatic-specialist     — Lymphatic
})

# §14 genetics-specialist + §15 labs-specialist are CROSS-CUTTING INPUTS (disposition #25): they
# feed every domain's biomarker / PGx substrate but emit NO domain card, so they are NEVER card
# domains. Held as a named partition alongside CARD_DOMAINS (single source of truth), not re-listed.
CROSS_CUTTING_INPUTS = frozenset({"genetics", "labs"})

# Partition tripwire (disposition #25, mirrors the module-load `_DOMAIN_KIND` assert in
# generate_plan.py): a genetics/labs slug leaking into CARD_DOMAINS would give a cross-cutting input
# a domain card it must never emit — the card/input partition is a safety property, so fail closed at
# import if the two sets ever overlap rather than silently ship a genetics "card".
assert CARD_DOMAINS.isdisjoint(CROSS_CUTTING_INPUTS), (
    f"CARD_DOMAINS overlaps the cross-cutting inputs: {CARD_DOMAINS & CROSS_CUTTING_INPUTS}"
)

# The §1-§10 ALWAYS-ON card domains (ADR-0052): the non-progressive set every comprehensive plan
# authors. The progressive three (§11-§13: dermatology/gi/lymphatic) stay progressive — activated
# only on a surface signal (`active_domains`), NEVER floored (`plan_loop.active_plan_domains` unions
# THIS set unconditionally). The single source of the always-on vocabulary; ADR-0052-T2 is the one
# edit point if a §9 longevity-strategist re-home (OQ-3) later narrows the set to nine cards.
ALWAYS_ON_DOMAINS = frozenset({
    "workout", "nutrition", "peptides", "supplements", "endocrine",
    "cardiovascular", "recovery", "sleep", "longevity", "mental-performance",
})

# Substantive load-time pin (NOT `ALWAYS_ON_DOMAINS.isdisjoint(CARD_DOMAINS - ALWAYS_ON_DOMAINS)` —
# that is a tautology, any set is disjoint from its own relative complement, and guards nothing):
# the always-on ten are a proper subset of the card roster and their complement is EXACTLY the
# progressive three, so a slug added/dropped in either set fails closed at import.
assert ALWAYS_ON_DOMAINS <= CARD_DOMAINS, (
    f"ALWAYS_ON_DOMAINS leaks a non-card slug: {ALWAYS_ON_DOMAINS - CARD_DOMAINS}"
)
assert len(ALWAYS_ON_DOMAINS) == 10, f"ALWAYS_ON_DOMAINS must be the §1-§10 ten, got {len(ALWAYS_ON_DOMAINS)}"
assert CARD_DOMAINS - ALWAYS_ON_DOMAINS == frozenset({"dermatology", "gi", "lymphatic"}), (
    "the progressive three (§11-§13) must be exactly CARD_DOMAINS minus the always-on ten: "
    f"{CARD_DOMAINS - ALWAYS_ON_DOMAINS}"
)

# The operator-surface activation channels (disposition #23). A card domain is ACTIVE when the
# surface carries a signal for it in ANY channel: a stated goal, tracked-stream data / a reading, a
# care-conversation mention, or a lab-value / genetic-trait-class touch.
_SURFACE_CHANNELS = ("goals", "data", "mentions", "lab_or_trait_touches")


def _touched_domains(operator_surface):
    """Return the domain slugs the surface carries an activation signal for, across every channel."""
    touched = set()
    for channel in _SURFACE_CHANNELS:
        touched.update(operator_surface.get(channel, ()))
    return touched


def active_domains(operator_surface):
    """Return the active CARD-EMITTING domain set for an operator surface.

    A card domain is ACTIVE when the surface carries an activation signal for it (disposition #23):
    a stated goal, tracked-stream data / a reading, a care-conversation mention, or a lab-value /
    genetic-trait-class touch in that domain. The result is a subset of `CARD_DOMAINS`: the
    §14-genetics / §15-labs cross-cutting inputs are never returned as card domains (disposition
    #25), and a surface signal naming a non-card token is ignored (the gate never dispatches a
    non-card domain). A wired dispatcher briefs ONLY this set (gate-at-DISPATCH, disposition #24;
    ADR-0043-T3 wires it at the front door).

    Args:
        operator_surface (Mapping): A de-id-safe view of the operator's activation signals — the
            channels `goals` / `data` / `mentions` / `lab_or_trait_touches`, each an iterable of
            domain slugs. Carries no raw PII and originates no new operator-state source (it is a
            projection of what the assembled context already holds).

    Returns:
        (frozenset[str]) The active card-emitting domains — a subset of `CARD_DOMAINS`.
    """
    return frozenset(_touched_domains(operator_surface) & CARD_DOMAINS)
