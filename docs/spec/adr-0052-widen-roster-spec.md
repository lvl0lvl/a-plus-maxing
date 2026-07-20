---
scope: "ADR-0052 (widen the plan dispatch roster from four to the always-on ten)"
adrs: [ADR-0052]
tier: 2
created: 2026-07-19
status: approved
---

# Spec: Widen the Effective Plan-Authoring Roster from Four to the Always-On Ten

## Component Overview

This spec implements ADR-0052: it widens the EFFECTIVE plan-authoring roster of the `/generate-plan` front door from the effective four (workout / nutrition / supplements / peptides) to the always-on TEN (adding endocrine / cardiovascular / recovery / sleep / longevity / mental-performance), so the plan the operator's identity-stripped record is authored against reflects the full always-on care team rather than four sections. It delivers two production changes plus one cross-task integration gate: (1) map the six always-on rich domains (§5–§10) into the single-source `client._AUTHOR_CONTRACT_SECTION` so `client._contract_section` sources their contract sections without raising `ValueError` (ADR-0052-T1); (2) raise the `plan_loop.active_plan_domains` activation floor from the conditional renderable-core-four to an UNCONDITIONAL union of the always-on ten, single-sourced as a new `activation.ALWAYS_ON_DOMAINS` constant, so even a partial-signal operator floors at ten (ADR-0052-T2); and (3) an end-to-end composition gate proving a generation over an all-signal fixture records authored programs for ≥10 domains in the `plan-model::` comprehensive record while the thin render stays at the four `RENDERABLE_DOMAINS` (ADR-0052-T3).

The root cause the spec fixes is grounded against the live tree on `feature/adr-0052-spec`. The registries are ALREADY the full 13: `plan_driver._ROLE_OF_DOMAIN` carries all §1–§13 card domains ([plan_driver.py:122-136](../../scripts/plan/plan_driver.py)) and `plan_schema.PLAN_DOMAINS` derives the same 13 from `activation.CARD_DOMAINS`. The effective four-domain ceiling is enforced by TWO still-narrow levers, only one of which this spec touches at each end. First, the authoring coupling: every author call routes `client.author` → `_author_system_prompt(domain)` → `_contract_section(domain)`, and `_contract_section` RAISES a domain-named `ValueError` for any domain absent from the four-entry `_AUTHOR_CONTRACT_SECTION` map ([client.py:513-518,538-544](../../scripts/model/client.py)) — so §5–§10 are dispatch-eligible yet structurally un-authorable. T1 removes this. Second, the activation floor: `plan_loop.active_plan_domains` floors the active set at the renderable core-four ONLY when the surface carries no renderable signal (the CONDITIONAL `if not (active & RENDERABLE_DOMAINS): active |= RENDERABLE_DOMAINS` idiom, [plan_loop.py:233-235](../../scripts/serve/plan_loop.py)) — so a partial-signal operator (touching only, say, `workout`) returns ONE domain, not ten. T2 makes the floor an unconditional always-on-ten union.

The load-bearing grounding finding is that the front door needs NO `server.py` change (the ADR's file manifest lists `scripts/serve/server.py`, but that premise is superseded by the live code). The front door's rich-author leg is `care_chat.synthesize(active, outcome, _author_rich, ...)` at [server.py:871](../../scripts/serve/server.py), which already passes the FULL `active` set — not the `renderable_active` narrow at [:817](../../scripts/serve/server.py). Inside `synthesize`, `rich = sorted(set(active) - set(plan_schema.RENDERABLE_DOMAINS))` ([care_chat.py:545](../../scripts/serve/care_chat.py)) authors each rich domain via `author_rich` → `_contract_section`. So once `active` carries the always-on ten (T2's floor) and `_contract_section` resolves §5–§10 (T1's map), the six always-on rich domains author into `plan-model::` through the already-wired `synthesize` path with zero `server.py` edits. The `renderable_active ∩ RENDERABLE_DOMAINS` thin loop at [:817,832](../../scripts/serve/server.py) stays the four — `RENDERABLE_DOMAINS = tuple(_PLAN_VALIDATORS)` stays at four (RT-009, [plan_schema.py:289](../../scripts/store/plan_schema.py)); the rich domains record first-class via `plan_model`, never the thin validator path.

This is a mock/fixture build at **$0**: fixture/spy model clients, synthetic operator surfaces, no live SDK call and no spend. The operator-present LIVE run — a real `/generate-plan` dispatch authoring up to ten always-on domains at ~2.5× the four-domain author budget (ADR-0052 OQ-4) — is operator-gated and OUT of this spec's build scope; it is recorded below as the operator-present exit gate, mirroring ADR-0050 OQ-3 / ADR-0051 OQ-4. This spec widens what is AUTHORED (the always-on ten into `plan-model::`), NOT what RENDERS: `_plan_zone` still shows the same ≤4 thin cards until the downstream rich render (ADR-E / bead `ahz9`); the cross-domain synthesis (ADR-C) and daily-execution compile (ADR-D) are separate downstream ADRs. The frozen ADR-0032 `<always-frozen>` core (`store.py` / `keying.py` / `pipeline.py` / `adjudicate.py` / `adjust.py` / `router.py`) plus the still-frozen glob member `track.py` stay byte-frozen (numstat = 0 vs `3ab1c3ab`); `orchestrate.generate_plans` is called, not modified. Every change lands in `client.py` / `activation.py` / `plan_loop.py` and their tests. This is a PUBLIC repo — every fixture is synthetic.

**Informing artifacts:** `docs/adr/ADR-0052-widen-plan-dispatch-roster.md` (read in full), `docs/spec/.pipeline/context-0052.md`, `docs/spec/.pipeline/dispositions-0052.md`, `design/specialist-plan-contracts.md` (the §1–§18 per-specialist authoring contract — the single source T1's contract map anchors §5–§10 against, read, never modified).

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0052 OQ-1 | Open Question | Progressive activation (§11–§13) triggers on a stated GOAL only, or on any tracked datum too? `derive_operator_surface` leaves the `data` channel empty. | Defer | ADR-C / assembler-stage concern; the ADR states it "does not change the always-on ten." OUT of this spec's scope — this spec floors §1–§10 and leaves §11–§13 progressive exactly as `active_domains` already gates them. Addressed in ADR-C. |
| ADR-0052 OQ-2 | Open Question | Do the genetics / labs cross-cutting outputs get PERSISTED as their own store entries, or only passed in-memory to the domain authors as today? | Defer | ADR-C synthesis concern; this spec records genetics/labs as INPUT layers regardless of the persistence answer and touches neither. Addressed in ADR-C. |
| ADR-0052 OQ-3 | Open Question | Is longevity-strategist (§9) an always-on card-emitting domain, or a cross-cutting synthesis / sequencing role that belongs with the care-agent (ADR-C)? | Proceed | **Documented assumption:** placed always-on here (it authors a Longevity card in the S146 mockup); the always-on ten includes `longevity`. Flagged for ADR-C reconciliation — if ADR-C re-homes it as a synthesis layer, the always-on set becomes nine cards + one synthesis role. The `ALWAYS_ON_DOMAINS` constant (T2) is the single edit point for that future narrowing. |
| ADR-0052 OQ-4 | Open Question | The operator-present LIVE run: a real `/generate-plan` authoring up to ten always-on domains spends ~2.5× the four-domain author budget and sends the operator's real record to the no-train API across ten calls. | Defer | Operator-gated downstream checkpoint, OUT of build scope (the build wires + mock/fixture-tests at $0). Recorded as the operator-present exit gate (Test Strategy), NOT a build task. Mirrors ADR-0050 OQ-3 / ADR-0051 OQ-4. |
| ADR-0052 OQ-5 | Open Question | The progressive three (§11–§13) have NO `_AUTHOR_CONTRACT_SECTION` entry, so an ACTIVATED dermatology / GI / lymphatic domain hits `_author_rich`→`None` (dispatches but authors nothing). | Defer | Mapping §11–§13 into `_AUTHOR_CONTRACT_SECTION` is OUT of ADR-0052's scope — deferred and beaded `a-plus-maxing-00kh`. Until then an activated progressive domain produces NO card (honest containment: the `_author_rich`→`None`→dropped path never ships a partial card). This spec's unsourceable-domain probe is deliberately scoped to the always-on ten (T1 AC-1 / T3 AC-4). |
| ADR-0052 Negative-1 | Unmitigated Risk (documented) | This ADR widens AUTHORING, not RENDERING — the operator still sees ≤4 thin cards after this spec alone; the widened always-on-ten authoring lands in the un-surfaced `plan-model::` record. | Proceed | Deliberate honest sequencing, not a defect. Covered by T3, which asserts the composition COUNT (≥10 authored programs in `plan-model::`) while asserting the render stays the four `RENDERABLE_DOMAINS` (unchanged). The rich render is ADR-E / `ahz9`; asserting the render shows ≥10 cards would be the WRONG test and would FAIL by design. |
| ADR-0052 Negative-6 | Unmitigated Risk (documented) | The roster widening MULTIPLIES the genetics egress surface (today the de-id `genetic-trait-classes`-token exposure scales 4→10 author calls; if ADR-0051-T1 lands, it scales the raw-genome egress 4→10). | Proceed | Documented forward residual, operator-weighed. This spec does NOT change the genetics mechanism (ADR-0051 owns that) — it SCALES the existing de-id token egress by widening the author count. No build mitigation is possible or in scope; the identity-stripping standard holds (the assembler's `pii_scan` gate, untouched). Parallel to the exemplar ADR-0051 re-identification residual — recorded, not blocked. |

**No Block dispositions.** Nothing blocks the mock/fixture build. No research-spike (`T0`) task is required. Every Proceed is resolved by a named task's acceptance criteria or the recorded operator-present exit gate; the two documented residuals (honest render-vs-author sequencing, genetics-egress multiplier) are Proceed-with-documentation, consistent with the ADR's own honest-sequencing framing.

**Deferred-and-beaded (NOT tasks in this spec):** `a-plus-maxing-y9wr` (upsert_plan refactor), `a-plus-maxing-k16z` (sibling record sites), `a-plus-maxing-00kh` (progressive-domain §11–§13 contract sections — OQ-5). None is in scope; each is recorded here so a downstream reader does not re-scope it into ADR-0052.

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/model/client.py` | Modify | (ADR-0052-T1) Add the six always-on rich domains to `_AUTHOR_CONTRACT_SECTION` — `endocrine`→(5, "endocrine-specialist"), `cardiovascular`→(6, "cardiovascular-specialist"), `recovery`→(7, "recovery-specialist"), `sleep`→(8, "sleep-coach"), `longevity`→(9, "longevity-strategist"), `mental-performance`→(10, "mental-performance-coach") — so `_contract_section` sources their §5–§10 sections without `ValueError` |
| `tests/model/test_client.py` | Modify | (ADR-0052-T1) RED-capable `_contract_section` / `_author_system_prompt` resolution + heading-slice + entry-removal-mutation assertions for the always-on ten |
| `scripts/plan/activation.py` | Modify | (ADR-0052-T2) Define `ALWAYS_ON_DOMAINS` (the §1–§10 slugs) as a named `frozenset`, single-source of the always-on vocabulary, with a load-time assert that it is a subset of `CARD_DOMAINS` and disjoint from the progressive three (§11–§13) |
| `scripts/serve/plan_loop.py` | Modify | (ADR-0052-T2) Replace the conditional renderable-core floor in `active_plan_domains` ([:233-235](../../scripts/serve/plan_loop.py)) with an UNCONDITIONAL union of `activation.ALWAYS_ON_DOMAINS` (`active |= set(activation.ALWAYS_ON_DOMAINS)`) |
| `tests/serve/test_plan_loop.py` | Modify | (ADR-0052-T2) Signal-less / partial-signal / all-signal floor probes + RED-capable conditional-idiom mutation + no-§11–§13-in-floor assertions for `active_plan_domains` |
| `tests/serve/test_plan_roster_widening.py` | Create | (ADR-0052-T3) The end-to-end composition gate: drives `_do_generate_plan` with a fixture client over an all-signal store; asserts ≥10 authored programs in the composed `plan-model::` version, `RENDERABLE_DOMAINS` unchanged at four, the floor set equals the authorable set, no §11–§13 fabrication on an empty-state surface, and the frozen-surface numstat |

**Cited input (read, not a manifest action):** `design/specialist-plan-contracts.md` is the single-source per-specialist authoring contract T1's map anchors §5–§10 against — read via `client._contract_section`'s heading-slice, never modified (listed for the RGC-3 cited-input probe, not the manifest).

**NOT in the manifest — the grounded no-change surfaces:** `scripts/serve/server.py` (the ADR's file-manifest lists it, but the grounded rich-author leg `care_chat.synthesize(active, ...)` at [:871](../../scripts/serve/server.py) already passes the FULL `active` set — see Repo-Grounding Ledger T3 RGC-2, Stale-Premise-Reconciled — so no `server.py` edit is needed); `scripts/plan/plan_driver.py` (`_ROLE_OF_DOMAIN` already carries the §1–§13 mappings); `scripts/store/plan_schema.py` (`RENDERABLE_DOMAINS` / `_PLAN_VALIDATORS` stay at four, RT-009); `scripts/serve/care_chat.py` (the `synthesize` rich-author leg is already correct); and the frozen ADR-0032 `<always-frozen>` core + `track.py` + `orchestrate.py` / `generate_plan.py` / `assemble.py` (byte-frozen / called-not-modified).

**Shared-file coordination:** No file is modified by more than one task. T1 (`client.py`) and T2 (`activation.py` + `plan_loop.py`) are file-disjoint and fully parallel entry points. T3 creates one new test file and modifies no production code; it depends on both T1 and T2 (see Dependency Map).

## Tasks

### ADR-0052-T1: Map the six always-on rich domains into `_AUTHOR_CONTRACT_SECTION`
**Status:** TODO
**ADR Source:** ADR-0052, Decision §3 (map the six always-on rich domains — endocrine / cardiovascular / recovery / sleep / longevity / mental-performance — into the single-source `_AUTHOR_CONTRACT_SECTION` so `_contract_section` sources their §5–§10 sections without ValueError); ADR-0052, Validation Approach (each always-on domain is authorable — 10/10 resolve non-empty, 0 ValueErrors, REDs today for §5–§10; the unsourceable-domain falsification probe); ADR-0052, Consequences-Negative (plan quality now depends on the §5–§10 contract content; the always-on domain vocabulary is a moderate-reversibility commitment)
**Files to create/modify:**
- `scripts/model/client.py` -- add the six `domain: (section-number, specialist-slug)` entries to `_AUTHOR_CONTRACT_SECTION` ([:513-518](../../scripts/model/client.py)); no other change (the `_contract_section` heading-slice at [:545-560](../../scripts/model/client.py) is already generic)
- `tests/model/test_client.py` -- the RED-capable resolution / heading-slice / entry-removal assertions for the always-on ten

**Acceptance Criteria:**
1. `_contract_section(domain)` returns a non-empty string and raises NO `ValueError` for EACH of the always-on ten (`workout`, `nutrition`, `peptides`, `supplements`, `endocrine`, `cardiovascular`, `recovery`, `sleep`, `longevity`, `mental-performance`): a test asserts `len(_contract_section(d)) > 0` for all ten and that `set(client._AUTHOR_CONTRACT_SECTION) == {the ten}`. Non-tautological / RED-today: before the change `_contract_section` raises for the six §5–§10 domains (6/10 raise), so the test REDs today and GREENs after.
2. Each newly-mapped §5–§10 section is sliced to its OWN heading only: `_contract_section("endocrine")` begins at the `## 5. endocrine-specialist —` heading and does NOT contain the `## 6. cardiovascular-specialist —` heading text; the analogous own-heading-present / next-heading-absent pair holds for cardiovascular (§6), recovery (§7), sleep (§8), longevity (§9), mental-performance (§10). A section that bleeds into the next domain's text FAILS.
3. `_author_system_prompt(domain)` returns a non-empty prompt that contains a section-unique substring of THAT domain's `specialist-plan-contracts.md` section for each of the always-on ten — exercising the full author-prompt build path (not just `_contract_section`), so an incidental break in `_author_system_prompt` for a newly-authorable domain FAILS.
4. RED-capable / non-tautological: removing any one of the six added `_AUTHOR_CONTRACT_SECTION` entries makes `_contract_section` for that domain raise `ValueError` again and REDs AC-1. The test asserts the CLEAN direction (all ten resolve) truthy first, then RED-gates the entry-removal mutation: the test is invalid — and fails — if removing an added entry does not RED it.
5. `git diff --numstat 3ab1c3abb6c995fbaaadcb179735759e4a61d73d -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py scripts/plan/track.py` prints nothing (the frozen ADR-0032 core + `track.py` byte-frozen — the change lands in `client.py`, outside them; AR-007).
6. `$0`: the test reads the contract file and calls pure string functions (no live SDK call, no spend); `.venv/bin/python -m pytest tests/model/test_client.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures vs the session baseline).

**Risk Mitigations:** ADR-0052 Consequence-Negative "plan quality now depends on the §5–§10 contract content" (AC-1 asserts each §5–§10 section resolves NON-EMPTY — a thin/stale/renamed section fails the non-empty or heading-slice AC); "the always-on domain vocabulary is a moderate-reversibility commitment" (AC-1's `set(_AUTHOR_CONTRACT_SECTION) == {the ten}` pins the recorded vocabulary); ADR-0052 falsification "unsourceable-domain probe" scoped to the always-on ten (AC-1/AC-4 — a dispatched always-on domain with no contract section would `_author_rich`→`None` silently; the probe stays scoped to the ten, not every dispatch-eligible domain, since §11–§13 remain un-mapped by OQ-5)
**Dependencies:** None (entry point)

---

### ADR-0052-T2: Raise the `active_plan_domains` floor to the always-on ten, UNCONDITIONALLY
**Status:** TODO
**ADR Source:** ADR-0052, Decision §1 + §3 (the always-on-ten activation floor; it must be an UNCONDITIONAL floor, `active |= always_on_ten` on EVERY surface, not the conditional `if not (active & RENDERABLE_DOMAINS)` idiom); ADR-0052, Decision §1(a) (the always-on ten = §1–§10, the non-progressive always-authoring set; §11–§13 stay progressive); ADR-0052, Validation Approach (the activation floor is the always-on ten unconditionally — signal-less / partial-signal / all-signal all return a superset of the ten; the partial-signal floor probe, AR-006); ADR-0052, Consequences-Negative (the floor must be raised without zeroing an existing operator's plan AND unconditionally — a floor that drops below ten for a partial-signal operator is the silent regression)
**Files to create/modify:**
- `scripts/plan/activation.py` -- add `ALWAYS_ON_DOMAINS` (the §1–§10 slugs: `workout`, `nutrition`, `peptides`, `supplements`, `endocrine`, `cardiovascular`, `recovery`, `sleep`, `longevity`, `mental-performance`) as a named `frozenset` beside `CARD_DOMAINS` ([:26-40](../../scripts/plan/activation.py)), with a load-time assert `ALWAYS_ON_DOMAINS <= CARD_DOMAINS` and `ALWAYS_ON_DOMAINS.isdisjoint(CARD_DOMAINS - ALWAYS_ON_DOMAINS)`-style containment so the progressive three (§11–§13) are exactly `CARD_DOMAINS - ALWAYS_ON_DOMAINS`
- `scripts/serve/plan_loop.py` -- in `active_plan_domains` ([:222-236](../../scripts/serve/plan_loop.py)) replace the conditional `if not (active & set(plan_schema.RENDERABLE_DOMAINS)): active |= set(plan_schema.RENDERABLE_DOMAINS)` floor with the unconditional `active |= set(activation.ALWAYS_ON_DOMAINS)`
- `tests/serve/test_plan_loop.py` -- the signal-less / partial-signal / all-signal floor probes + the RED-capable conditional-idiom mutation + no-§11–§13-in-floor assertions

**Acceptance Criteria:**
1. `active_plan_domains(summary)` returns a SUPERSET of the always-on ten for a SIGNAL-LESS surface: a test builds a summary whose `derive_operator_surface` yields no active card domain and asserts `set(activation.ALWAYS_ON_DOMAINS) <= active_plan_domains(summary)` (never zeroes — the baseline plan is preserved).
2. `active_plan_domains(summary)` returns a SUPERSET of the always-on ten for a PARTIAL-signal surface (touches only `workout` — a summary whose `derive_operator_surface` yields `{"goals": ["workout"], ...}`): the returned set contains all ten always-on domains, `len(result) >= 10`. This is the AR-006 probe — the load-bearing partial-signal case.
3. `active_plan_domains(summary)` returns a SUPERSET of the always-on ten for an ALL-signal surface (a summary touching every card domain): the returned set contains all ten always-on domains; any activated progressive domain (§11–§13) may additionally appear but the ten are always present.
4. RED-capable / non-tautological (the AR-006 guard): reverting `active_plan_domains` to the conditional `if not (active & set(plan_schema.RENDERABLE_DOMAINS)): active |= set(...)` idiom makes AC-2 FAIL — a partial-signal surface touching only `workout` returns `{workout}` (len 1) because `{workout} & RENDERABLE` is non-empty so the conditional floor does not fire. The test asserts the CLEAN direction (partial-signal ⊇ the ten) truthy first, then RED-gates the conditional-idiom mutation; the test is invalid unless that mutation REDs it.
5. The floor adds NO progressive domain: for a SIGNAL-LESS surface, `active_plan_domains(summary)` contains NONE of `{dermatology, gi, lymphatic}` — the floored set equals exactly the always-on ten (`active_plan_domains(signal_less) == set(activation.ALWAYS_ON_DOMAINS)`), so the floor never fabricates a §11–§13 activation.
6. `ALWAYS_ON_DOMAINS` is a correct subset partition: a test asserts `activation.ALWAYS_ON_DOMAINS <= activation.CARD_DOMAINS`, `activation.ALWAYS_ON_DOMAINS.isdisjoint(activation.CROSS_CUTTING_INPUTS)`, and `activation.CARD_DOMAINS - activation.ALWAYS_ON_DOMAINS == {"dermatology", "gi", "lymphatic"}` (the progressive three), and that `len(activation.ALWAYS_ON_DOMAINS) == 10`.
7. `git diff --numstat 3ab1c3abb6c995fbaaadcb179735759e4a61d73d -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py scripts/plan/track.py` prints nothing; `$0`: the test calls a pure set function (no SDK call); `.venv/bin/python -m pytest tests/serve/test_plan_loop.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures).

**Risk Mitigations:** ADR-0052 Consequence-Negative "the activation floor must be RAISED without zeroing an existing operator's plan, and UNCONDITIONALLY" (AC-1 the never-zeroes signal-less floor, AC-2 the unconditional partial-signal floor, AC-4 the RED-capable conditional-idiom mutation — the silent regression a signal-less-only probe misses); "the always-on domain vocabulary is a moderate-reversibility commitment" (AC-6 pins `ALWAYS_ON_DOMAINS` as the single-source ten and the exact progressive-three complement); ADR-0052 honesty-of-activation (AC-5 — the floor never fabricates a §11–§13 activation, keeping the progressive three progressive; Alternative D's failure)
**Dependencies:** None (entry point)

---

### ADR-0052-T3: End-to-end composition gate — ten authored into `plan-model::`, render stays four
**Status:** TODO
**ADR Source:** ADR-0052, Validation Approach (the comprehensive record carries >4 authored domains — generate over an all-signal fixture, assert the `plan-model::` composed version carries authored programs for ≥10 domains, the COUNT the rich render will lay out, NOT the rendered card count); ADR-0052, Decision §3 + Consequences-Neutral (`RENDERABLE_DOMAINS` / `_PLAN_VALIDATORS` stay four; the always-on rich domains record into `plan-model::` via `synthesize`, not the thin validator path); ADR-0052, falsification (frozen-surface probe; progressive-fabrication probe — an empty-state surface authors NO §11–§13 card); CLAUDE.md Integration-Verification mandate (verification means running the production path; E2E asserts placement, not existence)
**Files to create/modify:**
- `tests/serve/test_plan_roster_widening.py` -- CREATE the integration gate: drives `_do_generate_plan` ([server.py:742](../../scripts/serve/server.py)) with a fixture/spy `self.client` over a seeded store; no production code (the T1 + T2 production changes plus the already-correct `care_chat.synthesize(active, ...)` at [server.py:871](../../scripts/serve/server.py) compose to the widened authoring)

**Acceptance Criteria:**
1. A generation over an ALL-signal fixture surface records ≥10 authored programs in the composed `plan-model::` version: seed a store whose derived surface activates the always-on ten, drive `_do_generate_plan` with a fixture client returning a conformant thin envelope for each of the four `RENDERABLE_DOMAINS` (so ≥1 records and the Leg-2 gate at [server.py:865](../../scripts/serve/server.py) fires) AND a conformant `domain_program`-valid rich envelope for each §5–§10 domain, then assert the recorded `plan-model::` version ([care_chat.py:584-585](../../scripts/serve/care_chat.py)) carries authored programs for ≥10 domains (the four renderable + the six always-on rich). Threshold: ≥10 domain programs in the composed version. Non-tautological / RED-today: before T1+T2, §5–§10 either are not in `active` (no T2 floor) or `_author_rich`→`None` (no T1 map), so the composed version carries ≤4 programs and the ≥10 assertion REDs.
2. Placement, not existence (CLAUDE.md E2E mandate): the assertion checks the authored programs land in the DISJOINT `plan-model::` namespace ([plan_model.py](../../scripts/store/plan_model.py) `_PREFIX_MODEL`), and asserts the six always-on rich domains (`endocrine`, `cardiovascular`, `recovery`, `sleep`, `longevity`, `mental-performance`) are each present by domain key in the composed version — not merely a count of "some programs somewhere."
3. `RENDERABLE_DOMAINS` stays four (the render is NOT widened): the test asserts `len(plan_schema.RENDERABLE_DOMAINS) == 4` and `set(plan_schema.RENDERABLE_DOMAINS) == {"workout", "nutrition", "supplements", "peptides"}` after the run — the widening is AUTHORING (`plan-model::` count), never RENDERING (RT-009). Asserting the render shows ≥10 cards would be the WRONG test and would FAIL by design (Negative-1).
4. Floor ↔ authorable coherence (the unsourceable-domain guard, scoped to the always-on ten): the test asserts `set(activation.ALWAYS_ON_DOMAINS) == set(client._AUTHOR_CONTRACT_SECTION)` — the floor set and the authorable set are identical, so no floored always-on domain silently `_author_rich`→`None` and no authorable domain is left off the floor.
5. Progressive-fabrication probe → the empty-state case: a generation over a surface with NO dermatology / GI / lymphatic signal authors NO §11–§13 program — the composed `plan-model::` version contains none of `{dermatology, gi, lymphatic}` by domain key. Threshold: 0 progressive-domain programs for an empty-state surface; ≥1 means progressive activation regressed to always-on (Alternative D's failure). RED-capable: adding a §11–§13 domain to `ALWAYS_ON_DOMAINS` would make this assertion FAIL.
6. `git diff --numstat 3ab1c3abb6c995fbaaadcb179735759e4a61d73d -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py scripts/plan/track.py` prints nothing (the composition used the already-wired `synthesize(active, ...)` leg + T1/T2, so no frozen surface changed — RED if `server.py`'s frozen neighbors or the ADR-0032 core changed).
7. `$0`: fixture/spy client and synthetic store only (no live SDK call, no spend); `.venv/bin/python -m pytest tests/serve/test_plan_roster_widening.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures).

**Risk Mitigations:** ADR-0052 Consequence-Negative-1 "widens AUTHORING, NOT RENDERING" (AC-1/AC-3 — the composition COUNT in `plan-model::` while `RENDERABLE_DOMAINS` stays four); CLAUDE.md Integration-Verification mandate "E2E asserts placement, not existence" + "verification means running the production path" (AC-1/AC-2 drive the real `_do_generate_plan` front door, not a manually-configured `synthesize` call, and assert domain-keyed placement in `plan-model::`); ADR-0052 falsification "progressive-fabrication probe" (AC-5 — an empty-state surface authors no §11–§13 card); ADR-0052 falsification "unsourceable-domain probe" (AC-4 — the floor set equals the authorable set, so no floored domain silently thins)
**Dependencies:** ADR-0052-T1, ADR-0052-T2

---

## Dependency Map

```
ADR-0052-T1 --> ADR-0052-T3
ADR-0052-T2 --> ADR-0052-T3
```

**Data flow per edge:**
- `ADR-0052-T1 --> ADR-0052-T3`: a real feature-integration edge. T1 maps §5–§10 into `_AUTHOR_CONTRACT_SECTION`, so `_author_rich` → `_contract_section` resolves (does not `ValueError`→`None`) for the six always-on rich domains. Until T1 lands, T3's ≥10-authored composition CANNOT pass — the six rich domains author `None` and are dropped, so the composed version carries ≤4 programs. T3's fixture drives the real author path; the coherence AC (AC-4) reads `client._AUTHOR_CONTRACT_SECTION`.
- `ADR-0052-T2 --> ADR-0052-T3`: a real feature-integration edge. T2's unconditional floor makes `active` carry the always-on ten, so `care_chat.synthesize(active, ...)` computes `rich = active - RENDERABLE_DOMAINS ⊇ {§5–§10}` and authors them. Until T2 lands, a partial-signal (or the fixture's) `active` may omit §5–§10 and `synthesize` never authors them. T3's coherence AC (AC-4) reads `activation.ALWAYS_ON_DOMAINS`.

**Topological order (Kahn's; parallel groups):**
1. `ADR-0052-T1`, `ADR-0052-T2` (parallel — entry points, no dependencies; file-disjoint: `client.py` vs `activation.py` + `plan_loop.py`)
2. `ADR-0052-T3` (after both `ADR-0052-T1` and `ADR-0052-T2`)

**Entry points:** `ADR-0052-T1`, `ADR-0052-T2`
**Critical path:** `ADR-0052-T1 → ADR-0052-T3` (equal-length: `ADR-0052-T2 → ADR-0052-T3`); 2 tasks. Acyclic — Kahn's orders all 3 nodes with none remaining.

## Constraint Propagation

Cross-cutting constraints from ADR-0052 (constrained-by ADR-0032; depends-on ADR-0043/0044/0046/0050) and their enforcing acceptance criteria (each a falsifiable AC, not prose):

| Constraint | Source | Enforced in | Enforcing AC |
|-----------|--------|-------------|--------------|
| Frozen ADR-0032 `<always-frozen>` core + `track.py` numstat == 0 vs `3ab1c3ab` (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py`, `track.py`) | ADR-0052 Related Decisions (ADR-0032 `constrains`) + Validation (frozen-surface probe, AR-007) | ADR-0052-T1, ADR-0052-T2, ADR-0052-T3 | the `git diff --numstat 3ab1c3ab -- <six + track.py>` prints-nothing AC in each (T1 AC-5, T2 AC-7, T3 AC-6) |
| `RENDERABLE_DOMAINS` / `_PLAN_VALIDATORS` stay four — the widening is AUTHORING, not RENDERING (RT-009) | ADR-0052 Decision §3 + Consequences-Neutral | ADR-0052-T3 | AC-3 (`len(RENDERABLE_DOMAINS) == 4` and the set unchanged after the run) |
| The always-on ten must be AUTHORABLE (each resolves via `_contract_section` without ValueError) — ADR-0050's contract mechanism extended to §5–§10 | ADR-0052 Decision §3 (depends-on ADR-0050) + Validation (unsourceable-domain probe) | ADR-0052-T1, ADR-0052-T3 | T1 AC-1 (10/10 resolve non-empty, 0 ValueErrors); T3 AC-4 (floor set == authorable set) |
| The activation floor is the always-on ten UNCONDITIONALLY (partial-signal ⊇ ten) | ADR-0052 Decision §3 + Validation (partial-signal floor probe, AR-006) + Consequences-Negative | ADR-0052-T2 | AC-2 (partial-signal ⊇ ten), AC-4 (RED-capable conditional-idiom mutation) |
| §11–§13 stay progressive — the floor fabricates no empty-state dermatology / GI / lymphatic card (honesty-of-activation; Alternative D rejected) | ADR-0052 Decision §1(a)/(c) + Validation (progressive-fabrication probe) | ADR-0052-T2, ADR-0052-T3 | T2 AC-5 (floor excludes §11–§13), T3 AC-5 (empty-state authors no §11–§13 program) |
| The always-on rich domains record into the disjoint `plan-model::` namespace via `synthesize` (not the thin `plan::` path) — ADR-0044's comprehensive record | ADR-0052 Decision §3 (depends-on ADR-0044) + Validation (comprehensive-record count) | ADR-0052-T3 | AC-1/AC-2 (≥10 programs, domain-keyed placement in `plan-model::`) |
| `$0` build until the operator-present run (synthetic/fixture, PUBLIC repo) | ADR-0052 OQ-4 (LIVE run operator-gated, out of build scope) | ADR-0052-T1, ADR-0052-T2, ADR-0052-T3 | T1 AC-6, T2 AC-7, T3 AC-7 (fixture/spy client, no spend) |

## Test Strategy

### Unit Tests
- **Scope:** `scripts/model/client.py` (`_contract_section` / `_author_system_prompt` — ADR-0052-T1), `scripts/plan/activation.py` + `scripts/serve/plan_loop.py` (`ALWAYS_ON_DOMAINS` + `active_plan_domains` — ADR-0052-T2).
- **Approach:** pytest; `_contract_section(domain)` / `_author_system_prompt(domain)` asserted as pure string functions reading the checked-in (or monkeypatched-path) contract file — no model call; `active_plan_domains(summary)` asserted as a pure set function over synthetic summary fixtures projected through `derive_operator_surface`. No network, no live SDK.
- **Criteria covered:** ADR-0052-T1 AC-1..4; ADR-0052-T2 AC-1..6.

### Integration Tests
- **Scope:** the front-door `_do_generate_plan` authoring + synthesis path (`active_plan_domains` floor → `renderable_active` thin loop → `orchestrate.generate_plans` → Leg-2 `care_chat.synthesize(active, ...)` → `plan_model.record_plan_version`) — ADR-0052-T3, the composition gate spanning T1 + T2.
- **Approach:** in-process `_do_generate_plan` driven with a fixture/spy `self.client` (returns conformant thin envelopes for the four renderable so the Leg-2 gate fires, and `domain_program`-valid rich envelopes for §5–§10) over a seeded store on the single-operator instance root; the composed `plan-model::` version asserted to carry ≥10 domain-keyed programs (placement, not existence); a second empty-state surface asserted to author no §11–§13 program.
- **Criteria covered:** ADR-0052-T3 AC-1, AC-2, AC-3, AC-4, AC-5.

### Risk-Specific Tests
- **Scope:** the entry-removal RED (T1 AC-4), the conditional-idiom RED (T2 AC-4, the AR-006 silent-regression guard), the progressive-fabrication guard (T2 AC-5 / T3 AC-5), the floor↔authorable coherence guard (T3 AC-4), the render-stays-four guard (T3 AC-3), and the frozen-surface numstat probes (all three tasks).
- **Approach:** each ruling is mutation-gated — the test asserts the CLEAN direction truthy first, then a planted violation (removing an added `_AUTHOR_CONTRACT_SECTION` entry; reverting the floor to the conditional `if not (active & RENDERABLE_DOMAINS)` idiom; adding a §11–§13 slug to `ALWAYS_ON_DOMAINS`) must flip it RED, so the test cannot be built green-always.
- **Criteria covered:** ADR-0052-T1 AC-4, AC-5; ADR-0052-T2 AC-4, AC-5, AC-7; ADR-0052-T3 AC-3, AC-4, AC-5, AC-6.

**Self-verifying ACs (covered by execution, not a separate test asset):** each task's terminal `pytest …` AC is the run itself — ADR-0052-T1 AC-6, ADR-0052-T2 AC-7, ADR-0052-T3 AC-7. With these, every acceptance criterion maps to a test or a verification command.

### Operator-Present Exit Gate (out of build scope, `$0`-until-run)
The load-bearing NON-mock verification (ADR-0052 OQ-4). Every build AC above is mock/fixture-satisfiable at $0; only the operator-present run confirms real always-on-ten plan quality and the ~2.5× author spend. Recorded here, teed up in the HANDOFF — NOT a build task.
- **Operator-present exit gate (after T1 + T2 + T3 land):** the operator runs `/generate-plan` on their REAL data through the web app; the plan is authored by up to ten always-on specialists over the operator's identity-stripped record (real spend across ten no-train author calls) — resolves ADR-0052 OQ-4. Threshold: the `plan-model::` record carries authored programs for the active always-on domains (≥ the fixture-verified ten on an all-signal operator); a plan expressible from four sections fails. This is the first time the widened roster spends real budget (operator-gated).

## Repo-Grounding Ledger

Grounded against the live worktree on `feature/adr-0052-spec` (Phase-4 author RGC probes; the Phase-6 judge re-runs all four independently). Frozen ADR-0032 core + `track.py` numstat vs `3ab1c3ab` verified EMPTY at author time.

| Task | RGC-1 (manifest) | RGC-2 (premise) | RGC-3 (cited input) | RGC-4 (dup) | Disposition |
|------|------------------|-----------------|---------------------|-------------|-------------|
| ADR-0052-T1 | pass (`client.py` present → Modify; `tests/model/test_client.py` present → Modify) | pass (`_AUTHOR_CONTRACT_SECTION`@513-518 = 4 entries [workout/nutrition/peptides/supplements]; `_contract_section`@525 raises ValueError@539/550 for an unmapped domain; heading-slice `## {N}. {slug} —`@546-556 generic; `_AUTHOR_SPECIALIST`@491-496 / `_AUTHOR_PAYLOAD_GUIDE`@497+ carry only the four renderable — §5–§10 fall to the generic "Specialist"/generic-guide default, functional since the §N contract body names the specialist role; persona entries are author-discretion, OUT of the ADR's explicit `_AUTHOR_CONTRACT_SECTION`-only scope) | pass (`design/specialist-plan-contracts.md` §5–§10 headings confirmed on disk: `## 5. endocrine-specialist — Hormonal`@141, `## 6. cardiovascular-specialist —`@167, `## 7. recovery-specialist —`@194, `## 8. sleep-coach —`@219, `## 9. longevity-strategist —`@244, `## 10. mental-performance-coach —`@269; the domain keys match `_ROLE_OF_DOMAIN`@122-136 and `CARD_DOMAINS`@26-40 slugs) | pass (no §5–§10 contract map exists; the map extension is a new coupling, no duplicate) | Grounded |
| ADR-0052-T2 | pass (`activation.py` present → Modify; `plan_loop.py` present → Modify; `tests/serve/test_plan_loop.py` present → Modify) | pass (`active_plan_domains`@222-236 conditional floor `if not (active & RENDERABLE_DOMAINS): active |= RENDERABLE_DOMAINS`@234-235 confirmed; `derive_operator_surface`@180-219 projects goals/mentions/traits, `data` channel empty; `CARD_DOMAINS`@26-40 = 13, `CROSS_CUTTING_INPUTS`@45, partition assert@51-53; no `ALWAYS_ON` constant today) | pass (`activation.active_domains`@69-89 returns a subset of `CARD_DOMAINS`; the always-on ten §1–§10 ⊆ `CARD_DOMAINS`; `plan_schema.RENDERABLE_DOMAINS`@289 = `tuple(_PLAN_VALIDATORS)` = the four) | pass (no always-on floor / `ALWAYS_ON_DOMAINS` constant exists today; the unconditional floor is a new mechanism, no duplicate) | Grounded |
| ADR-0052-T3 | pass (`tests/serve/test_plan_roster_widening.py` absent → Create) | **Stale-Premise-Reconciled** (the ADR file-manifest lists `scripts/serve/server.py` as a Modify — "the author-loop narrowing at :817,832 repointed so the always-on ten reach `_author_rich`/synthesize" — but the LIVE code SUPERSEDES it: `_do_generate_plan`@742 computes `active = active_plan_domains(summary)`@816, narrows `renderable_active = active & RENDERABLE_DOMAINS`@817 for the THIN loop, and calls `care_chat.synthesize(active, ...)`@871 passing the FULL `active` set — not `renderable_active`. `synthesize`@528+ computes `rich = active - RENDERABLE_DOMAINS`@545 and authors each via `author_rich`@549 → `record_plan_version`@585, gated by `if any(recorded)`@865. So the always-on ten reach `_author_rich`/synthesize with NO `server.py` edit once `active` carries them [T2] and `_contract_section` resolves §5–§10 [T1]. The stale ADR premise is reconciled to "no `server.py` change needed"; `server.py` is NOT in this spec's manifest) | pass (`plan_model.record_plan_version` + `_compose_version`@584-585 the `plan-model::` record; `RENDERABLE_DOMAINS`@289 = 4; the fixture client returns conformant thin[4] + `domain_program`-valid rich[6] envelopes; the Leg-2 gate `if any(recorded)`@865 fires when ≥1 renderable records) | pass (`tests/serve/test_orchestrator_synthesize.py` exists but tests the synthesize unit, not the ≥10-authored front-door composition; the roster-widening composition gate is new, no duplicate) | Grounded (T3 RGC-2 Stale-Premise-Reconciled) |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task (ADR-0052: T1–T3)
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0052-widen-plan-dispatch-roster.md` read in full)

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion (ADR-0052-T1: 6, ADR-0052-T2: 7, ADR-0052-T3: 7)
- [x] All acceptance criteria are binary (a command/condition with a pass/fail outcome)
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in at least one task block
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (Kahn's orders all 3 nodes; none remain)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed (ADR-0052-T1, ADR-0052-T2) and have Dependencies: "None (entry point)"

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream ADR constraints in their acceptance criteria (frozen-core+track.py, RENDERABLE-stays-four, always-on-authorable, unconditional-floor, progressive-non-fabrication, plan-model::-record, $0 — see Constraint Propagation table)
- [x] Constraint Propagation Table entries have corresponding acceptance criteria in affected tasks

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present
- [x] Every open question / pending tension / unmitigated risk has a disposition (OQ-1..5 + Negative-1 + Negative-6; Proceed / Defer; no Block applies)
- [x] Block dispositions have corresponding research spike tasks (none — no Block dispositions)
- [x] Defer dispositions have justifications (OQ-1/OQ-2 → ADR-C; OQ-4 → operator-gated exit gate; OQ-5 → bead `a-plus-maxing-00kh`)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in in-scope ADRs is covered by at least one task's Risk Mitigations or a documented assumption (ADR-0052 negatives: honest-sequencing→T3 AC-1/AC-3, spend→OQ-4 exit gate, contract-content-quality→T1 AC-1, moderate-reversibility-vocabulary→T1 AC-1/T2 AC-6, floor-without-zeroing+unconditional→T2 AC-1/AC-2/AC-4, genetics-egress-multiplier→documented residual)

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (the entry-removal RED, the conditional-idiom RED, the progressive-fabrication guard, the floor↔authorable coherence guard, the render-stays-four guard, the frozen-surface probes)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the template (Component Overview → Unresolved Concerns → File Manifest → Tasks → Dependency Map → Test Strategy → Validation Checklist, plus Constraint Propagation + Repo-Grounding Ledger)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`client.py`, `activation.py`, `plan_loop.py`, `test_client.py`, `test_plan_loop.py` all present)
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`tests/serve/test_plan_roster_widening.py` confirmed absent)
- [x] Every ADR premise a task relies on was re-verified against the current repo (all seams confirmed at the cited lines; the ADR's `server.py`-repoint premise is Stale-Premise-Reconciled — the grounded `synthesize(active, ...)` leg already carries the full active set, so no `server.py` change is needed)
- [x] Every cited input a task reads declares its structural assumption AND the live file satisfies it (`_AUTHOR_CONTRACT_SECTION` 4-entry map; `_contract_section` heading-slice; `specialist-plan-contracts.md` §5–§10 headings; `CARD_DOMAINS`/`CROSS_CUTTING_INPUTS` partition; `RENDERABLE_DOMAINS` = 4; `synthesize` `rich = active - RENDERABLE_DOMAINS`)
- [x] No task proposes a new artifact that duplicates an existing repo capability (no §5–§10 contract map, no always-on floor, no ≥10-authored composition gate exists today)
- [x] Repo-Grounding Ledger present, one row per task, with a disposition (2 Grounded, 1 Grounded with T3 RGC-2 Stale-Premise-Reconciled)
