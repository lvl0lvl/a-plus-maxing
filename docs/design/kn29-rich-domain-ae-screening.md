---
title: "kn29 / SEC-W4-01 — Rich-Domain Adverse-Event Screening (Option B)"
type: design-note
status: draft
owner: architect
bead: a-plus-maxing-kn29
adr: [ADR-0041, ADR-0043]
created: 2026-07-13
consumes: [ADR-0041 §Consequences-Neutral (meta→seams fold), ADR-0043 Decision §3 + OQ-1]
---

# kn29 / SEC-W4-01 — Rich-Domain Adverse-Event Screening (Option B)

**What this is.** The buildable interface contract + falsification probes for wiring the additive-AE
and Rx-BPMH safety floors to screen the RICH specialist DOMAIN PROGRAMs — the P1 operator-present
live-run blocker (`a-plus-maxing-kn29`, promoted from PF-S133-02). The approach is **Option B**,
operator-decided: fold the adverse-event profile into `cross_domain_seams` as a strongly-typed
sub-structure (NOT a separate parallel `ae_profile` program field), and re-base the floors to read
it. This note specifies the contract the Senior Engineer builds against; it is NOT the code.

**Decision is fixed.** Option A (a parallel program-level `ae_profile` field) and Option B were
adjudicated by the operator → Option B. This note does not re-litigate that; it makes Option B
concrete.

---

## 1. Grounded current state

### 1a. The floor read path today — the COMPOUND band only

The two additive-AE floors read the author-declared AE profile from a candidate `meta` side-channel,
and are hard-wired to the compound band (supplements/peptides):

- `_ae_profile(candidate)` reads `candidate["meta"]["ae_profile"]` → `{additive_classes: [...],
  interactions: [...]}` ([orchestrate.py:112-135](../../scripts/plan/orchestrate.py), the read at
  `:134` [VERIFIED]). The profile is lifted into `meta` from the author `reconciliation` envelope by
  `compute_plan`; a candidate that declared none, OR a present-but-malformed declaration, contributes
  `{}` (no finding) — the deliberate trusted-author posture ([orchestrate.py:124-127,135](../../scripts/plan/orchestrate.py) [VERIFIED]).
- **Screen 4 (additive-AE, Phase 3)** runs *only* when BOTH a `supplements` and a `peptides` candidate
  carry a plan, comparing their two `_ae_profile`s and holding the supplement
  ([orchestrate.py:485-494](../../scripts/plan/orchestrate.py) [VERIFIED]). Two detection paths:
  (a) a SHARED normalized `additive_classes` token (`_normalized_ae_classes(supp) &
  _normalized_ae_classes(pep)`), and (b) an author-declared `interactions[].with` naming the other
  compound's identity ([orchestrate.py:166-232](../../scripts/plan/orchestrate.py) [VERIFIED]).
- **Screen 5 (Rx-BPMH, Phase 4)** iterates the hard-coded tuple `("supplements", "peptides")`, and for
  each intersects `_normalized_ae_classes(_ae_profile(cand))` with the operator's present
  `operator_rx_classes`, holding the compound in the independent `rx_bpmh_held` set
  ([orchestrate.py:321-339,505-512](../../scripts/plan/orchestrate.py) [VERIFIED]).

The canonical AE-class vocabulary (`bleeding-risk`, `serotonergic`, `hepatotoxicity`,
`nephrotoxicity`, `malignancy-risk`, `thrombotic`, `igf-elevation`, `cyp3a4-pgp`, `qt-prolongation`,
`hypoglycemia`, `immunomodulation`, `sedation`, `stimulant-load`) is documented in prose in
[docs/plan-generation/author-dispatch-process.md:160-175](../plan-generation/author-dispatch-process.md)
[VERIFIED]. It is NOT a code constant — matching is exact string-equality over normalized
(lowercase/strip) tokens ([orchestrate.py:166-171](../../scripts/plan/orchestrate.py) [VERIFIED]).

### 1b. The `cross_domain_seams` entry shape today — no AE payload

Each `cross_domain_seams` entry today carries exactly two reconciled keys, single-sourced in
`domain_program` (the "pule" constant block) and referenced by `orchestrate`:

- `SEAM_WITH_DOMAIN = "with_domain"` — the paired-domain reference.
- `SEAM_NATURE = "nature"` — a seam-nature token; a `SEAM_NATURE == SEAM_CONFLICT` (`"conflict"`) seam
  HOLDS the declaring domain (reusing the independent `conflict_held` set).

([domain_program.py:89-96](../../scripts/plan/domain_program.py); [orchestrate.py:78-80,514-547](../../scripts/plan/orchestrate.py) [VERIFIED]).

The uniform seam pass ([orchestrate.py:514-547](../../scripts/plan/orchestrate.py) [VERIFIED]) is ONE
loop over every candidate's `cross_domain_seams` (via `_cross_domain_seams`,
[orchestrate.py:138-163](../../scripts/plan/orchestrate.py) [VERIFIED]). It reads `with_domain` +
`nature` only; a seam with no string `with_domain` is inert (SEC-W3-04,
[orchestrate.py:527](../../scripts/plan/orchestrate.py) [VERIFIED]). **No AE class or interaction data
is read off a seam.** `domain_program.validate` does NOT check the seam edge shape at all — the edge
shape and its reconciliation are explicitly ADR-0043-T2-owned, not validated
([domain_program.py:35-42,153-231](../../scripts/plan/domain_program.py) [VERIFIED]).

### 1c. The precise gap (SEC-W4-01)

In the comprehensive plan (`care_chat.synthesize`), the RICH domains (active domains beyond
`plan_schema.RENDERABLE_DOMAINS`) are authored via `author_rich`, shaped into candidates with
**`meta` set to `{}`** ([care_chat.py:551-555](../../scripts/serve/care_chat.py) [VERIFIED]), and
reconciled through `care_chat.collect → orchestrate.reconcile`
([care_chat.py:538-577](../../scripts/serve/care_chat.py) [VERIFIED]). Because their `meta` is empty:

- `_ae_profile(rich_candidate)` returns `{}` → **screens 4 and 5 are structurally dead for every rich
  domain** (they read `meta.ae_profile`, which rich candidates lack), AND both are additionally
  hard-scoped to `supplements`/`peptides` regardless.
- The rich domain's DOMAIN PROGRAM DOES carry `cross_domain_seams` (preserved verbatim by
  `_rich_program_from_envelope` and through the `project_renderable` prescription-strip,
  [care_chat.py:470-478,574-576](../../scripts/serve/care_chat.py) [VERIFIED]) — but the seam pass reads
  only `with_domain` + `nature`, so **any additive-AE class or interaction a rich specialist declares is
  never screened.**

Net: two rich specialists that both contribute, e.g., `bleeding-risk`, or where one declares an
interaction with the other, are folded into the comprehensive plan un-screened. This is the SEC-W4-01
floor bypass — the same class PF-S133-02 named ("safety enforced PER-PATH, not at a shared
chokepoint"): each new program path must re-earn the floor coverage the compound band already has.

---

## 2. The Option-B schema contract — AE folded onto `cross_domain_seams`

**The fold.** The compound-band `ae_profile` shape (`{additive_classes, interactions}`) is relocated
from the `meta` side-channel onto each `cross_domain_seams` entry as an OPTIONAL, strongly-typed
sub-structure. There is ONE `ae_profile` shape in the system; Option B changes only WHERE a rich
domain carries it (on its seams) — the shape, keys, and canonical vocabulary are reused verbatim so a
shared-class token matches identically across the compound band and the rich seams.

### 2a. The extended seam-entry contract

A `cross_domain_seams` entry is now:

```
{
  "with_domain": <str>,          # REQUIRED to be reconcilable (existing). Missing/non-str → seam inert (existing SEC-W3-04).
  "nature":      <str>,          # existing. nature == "conflict" holds the declaring domain (existing, UNCHANGED).
  "ae_profile":  {               # OPTIONAL (NEW, Option B). Absent → no AE declaration on this seam.
     "additive_classes": [<AE-class token>, ...],     # OPTIONAL. Canonical vocabulary; the classes this
                                                       #   domain contributes (direction-agnostic; §3 path a).
     "interactions": [ {                               # OPTIONAL. Declared pairwise interactions toward with_domain.
        "with":      <intervention identity | domain>, # finding detail (the named element)
        "mechanism": <str>,                            # finding detail
        "severity":  "low" | "moderate" | "high"       # finding detail
     }, ... ]
  }
}
```

**Single-source constant.** Add `SEAM_AE_PROFILE = "ae_profile"` to the `domain_program` seam
key-name block (alongside `SEAM_WITH_DOMAIN` / `SEAM_NATURE` / `SEAM_CONFLICT`,
[domain_program.py:89-96](../../scripts/plan/domain_program.py)), referenced by `orchestrate` as
`domain_program.SEAM_AE_PROFILE` — the existing "pule" single-source discipline, so a divergent filler
key is caught by the reader, never silently dropped. The two inner keys (`additive_classes`,
`interactions`) and the interaction shape (`with` / `mechanism` / `severity`) REUSE the compound-band
literals verbatim ([orchestrate.py:167,191,197-203](../../scripts/plan/orchestrate.py) [VERIFIED]);
whether to hoist them to constants is SE discretion (the contract is the key NAMES + types).

### 2b. Types, preconditions, postconditions, error cases

- `additive_classes` — a list of free string tokens drawn from the canonical AE-class vocabulary
  (coordination contract, NOT a validated enum — matching is exact string-equality on normalized
  tokens, mirroring the compound band). Non-list → treated as empty. Non-string / empty-after-strip
  tokens dropped.
- `interactions` — a list of dicts `{with, mechanism, severity}`. Non-list → empty. Non-dict entries
  dropped. `with`/`mechanism` are finding detail (strings); `severity ∈ {low, moderate, high}` is
  finding detail (not gating).
- `ae_profile` not a dict → the WHOLE sub-structure is ignored (no AE finding); **the seam's other
  fields (`with_domain`, `nature`) still apply** — a malformed `ae_profile` MUST NOT invalidate the
  seam's existing conflict-nature hold (no regression). See §4.
- **Postcondition of a well-formed declaration:** the declaring domain's classes/interactions become
  visible to the §3 floors; a finding HOLDS the domain (fail-closed drop from the comprehensive plan).

### 2c. How a rich DOMAIN PROGRAM declares it

A rich specialist authoring its seven-field DOMAIN PROGRAM populates `cross_domain_seams` with one
entry per domain it interacts with, and, on those entries, an `ae_profile` sub-structure carrying the
AE classes it contributes + any explicitly known interactions. This is the rich domain's ONLY AE
channel — rich candidates have no `meta.ae_profile` ([care_chat.py:554](../../scripts/serve/care_chat.py)
[VERIFIED]). The author-contract doc
([docs/plan-generation/author-dispatch-process.md](../plan-generation/author-dispatch-process.md)) is
updated to document the seam `ae_profile` sub-structure as the rich-domain equivalent of the
compound band's top-level `reconciliation.ae_profile`.

---

## 3. The floor re-base contract

The rich-domain screen runs INSIDE the existing uniform seam pass
([orchestrate.py:514-547](../../scripts/plan/orchestrate.py)), so it is ONE additional pass over the
same seam loop, AFTER the three always-on compound-band floors (screens 1/4/5) which fire from their
own `meta`/`reason` triggers regardless. The compound-band read path (`_ae_profile` over `meta`) is
UNCHANGED — the seam source is strictly ADDITIVE.

### 3a. New readers (contracts, analogous to `_ae_profile`)

- `_seam_ae_profile(seam) -> dict` — the seam's `ae_profile` dict, or `{}` when absent/non-dict.
  Pure, never raises. Mirrors `_ae_profile`'s malformed-is-inert posture.
- `_seam_ae_classes(candidate) -> set` — the POOLED normalized union of `additive_classes` across ALL
  the candidate's valid seam entries' `ae_profile`s. `{}`/empty for no plan / no program / no seams.
  This is the seam-sourced analogue of `_normalized_ae_classes(_ae_profile(candidate))` — a
  direction-agnostic, program-wide "classes this domain contributes" set, reconstructed from the
  seams (the fold). Pure, never raises.

### 3b. The additive-AE screen over rich seams

Over candidates that carry a plan, mirroring the compound band's two paths but sourced from seams:

- **(a) Shared additive-AE class (symmetric).** For each unordered domain pair {X, Y} both
  present-with-plan, if `_seam_ae_classes(X) ∩ _seam_ae_classes(Y)` is non-empty → a shared-class
  finding over the intersection → HOLD **both** X and Y. (Mirrors compound-band path (a); "component
  tolerability does not compose to combination safety." Holds both because both are un-screened until
  adjudicated; dropping either breaks the stack, dropping both is the fail-closed default.)
- **(b) Declared interaction (directional).** For each candidate's each seam whose `ae_profile`
  carries a non-empty `interactions` list AND whose `with_domain` names a domain present-with-plan in
  the pass → an interaction finding (the `interactions` entries + `with_domain` as detail) → HOLD the
  declaring domain. (Mirrors compound-band path (b) + the existing seam-conflict "hold the declaring
  domain" precedent. The pairing is established by the seam's `with_domain` — rich domains expose no
  `_compound_identities`, so the intervention-identity match the compound band uses is NOT reused;
  the seam's `with_domain` IS the pairing.)

Both paths write findings to a NEW report key `report["seam_additive_ae"]` (a list, DISTINCT from the
compound band's `report["additive_ae"]` so Leg-1 adjudication/queue collation
[orchestrate.py:671,805](../../scripts/plan/orchestrate.py) stay byte-identical) and set
`holds[<domain>] = SEAM_ADDITIVE_AE_HELD` (a NEW `holds` reason constant).

**Why `holds` (not a new top-level set):** `care_chat.synthesize` already drops any domain in
`set(outcome["holds"]) | set(outcome["conflict_held"]) | set(outcome["rx_bpmh_held"])`
([care_chat.py:557-558](../../scripts/serve/care_chat.py) [VERIFIED]), and `generate_plans` already
suppresses recording for any domain in `holds` ([orchestrate.py:716-725](../../scripts/plan/orchestrate.py)
[VERIFIED]). Reusing `holds` therefore yields the fail-closed DROP with ZERO change to either consumer —
`care_chat.py` needs no functional edit. (A dedicated `seam_ae_held` set would force `synthesize` +
`generate_plans` edits for no safety gain; rejected as over-scoped.)

### 3c. The Rx-BPMH re-base over rich seams

Extend screen 5's class source (not its gate): for EACH candidate present-with-plan, screen
`_seam_ae_classes(candidate) ∩ operator_rx_classes` — in ADDITION to the existing
`_ae_profile`-over-`meta` source for `supplements`/`peptides`. A non-empty intersection → append to the
existing `report["rx_bpmh"]` + add the domain to the existing independent `rx_bpmh_held` set
([orchestrate.py:505-512](../../scripts/plan/orchestrate.py) [VERIFIED]). `operator_rx_classes` is
already derived inside `collect` ([care_chat.py:449](../../scripts/serve/care_chat.py) [VERIFIED]) and
`generate_plans` ([orchestrate.py:631](../../scripts/plan/orchestrate.py) [VERIFIED]), so the Rx surface
is available on both legs with no new plumbing.

### 3d. No regression on the compound band (transitional-additive)

Every existing fixture seeds AE data on `meta.ae_profile`, never on a seam `ae_profile`, so
`_seam_ae_classes` is empty for every existing candidate and the new screen contributes nothing on the
existing paths — the same transitional-additive property the current seam pass already relies on
([orchestrate.py:519-522](../../scripts/plan/orchestrate.py) [VERIFIED]). In Leg 1 (`generate_plans`),
the renderable candidates' lifted programs carry no seam `ae_profile`, so the new screen is inert
there; the compound-band screens 4/5 fire exactly as today.

---

## 4. Validation + the malformed-declaration posture

**`domain_program.validate` is NOT extended.** It does not check the `cross_domain_seams` edge shape
today (ADR-0043-T2-owned, reader-enforced; [domain_program.py:35-42](../../scripts/plan/domain_program.py)
[VERIFIED]), and Option B keeps that boundary: the seam `ae_profile` sub-structure is reader-enforced
(malformed → dropped by `_seam_ae_profile`/`_seam_ae_classes`), NOT validated by `validate`. This keeps
`validate` / `missing_required_fields` frozen-signature-intact — a listed frozen-seam element
([domain_program.py:66-71](../../scripts/plan/domain_program.py) [VERIFIED]) — so W4-02's
validate-before-fold in `synthesize` ([care_chat.py:566-569](../../scripts/serve/care_chat.py)
[VERIFIED]) is unaffected (it still rejects a program missing a REQUIRED field; a malformed OPTIONAL
seam ae_profile passes validate and is handled inertly by the reader).

**Malformed posture — [AMENDED 2026-07-13]: a PRESENT-but-malformed declaration now FAILS CLOSED
(holds), superseding the original trusted-author fail-open below.** A PRESENT-but-structurally-malformed
seam `ae_profile` (a non-dict `ae_profile`; an `additive_classes` that is not a list-of-strings — a
scalar or a list-of-dicts; an `interactions` that is not a list-of-dicts — a single dict or a list of
strings) now HOLDS the declaring domain fail-closed (`SEAM_ADDITIVE_AE_HELD`, the SAME drop a well-formed
finding produces) + emits a DISTINCT `malformed-ae-profile` diagnostic into `report["seam_additive_ae"]`
(auditable, not silent). ABSENT (no `ae_profile` key) and PRESENT-but-VALIDLY-EMPTY (`{"additive_classes":
[], "interactions": []}`) stay inert. The three-way distinction (absent / valid-empty / malformed) is made
by a new `_seam_ae_malformed` reader (the pre-amendment `_seam_ae_profile` had collapsed absent and
mistyped into the same inert `{}`); the malformed hold is scoped to the sub-structure, so the
conflict-nature hold on the same seam still fires (P5-ii preserved). **Reason:** the Tier-2 Security HIGH
ruling — Security executed 7 drift cases, 6 of which (the present-but-mistyped class) were silently dropped
un-screened; the screen already fail-closes on empty content, so the fix is local + consistent.
**Residual (NOT closed by this reader fix):** the 7th drift case, a MIS-NAMED `ae_profile` key (an author
typo — the real key is then ABSENT, indistinguishable from a legitimate no-declaration at the reader), is
NOT catchable here; it is deferred to the `validate_plan_version` store-write chokepoint's unknown-key
rejection (kn29 guard-2, §7 out of scope).

_The original fail-open rationale, SUPERSEDED 2026-07-13, retained for provenance:_ A
malformed `ae_profile` (non-dict; wrong-typed `additive_classes`/`interactions`) is treated as NO
declaration → no finding → the domain is not held on that axis. This is the SAME posture as
`_ae_profile` ([orchestrate.py:124-127](../../scripts/plan/orchestrate.py) [VERIFIED]),
`_cross_domain_seams` ([orchestrate.py:146-147](../../scripts/plan/orchestrate.py) [VERIFIED]), and the
seam pass's own malformed-seam handling ([orchestrate.py:527](../../scripts/plan/orchestrate.py)
[VERIFIED]). Rationale:

1. **Uniformity.** The seam `ae_profile` is read by the same trusted-author path as its two siblings;
   making ONE reader fail-loud while the others fail-inert is a surprising inconsistency, not a
   hardening.
2. **The right layer for fail-loud is the shared chokepoint, not this reader.** The PF-S133-02 root
   cause is that safety is enforced per-path; its prescribed fix (2) is to enforce validate +
   load-clearance at the `validate_plan_version` store-write chokepoint — defense-in-depth at the ONE
   place every plan version passes through. A per-reader fail-loud here would be a partial, inconsistent
   version of that. The chokepoint backstop is explicitly OUT of kn29's scope (§7) — so Option B keeps
   the fail-open declaration posture and DEFERS the loud upgrade to that chokepoint, rather than bolting
   an inconsistent loud path onto one reader.

**Malformed MUST be scoped to the sub-structure.** A malformed `ae_profile` on a seam that ALSO has
`nature == "conflict"` must still fire the conflict hold — the malformed AE data is ignored, the seam's
other fields are not. This is a no-regression requirement (probe P5).

---

## 5. Falsification probes (the build's RED tests)

Each is testable without seeing the implementation, over `orchestrate.reconcile` (and the
`care_chat.collect → synthesize` fold where noted). Mutation-RED = the assertion fails if the named
wiring is removed.

- **P1 — shared rich AE-class → HOLD (path a).** Two rich domains X, Y, each with a seam carrying
  `ae_profile.additive_classes = ["bleeding-risk"]`, both with plans. Assert: `reconcile` holds BOTH X
  and Y (each in `holds` with `SEAM_ADDITIVE_AE_HELD`) and `report["seam_additive_ae"]` records the
  `bleeding-risk` finding. Mutation-RED: delete the `_seam_ae_classes` intersection → no hold → both
  fold → RED.
- **P2 — rich declared interaction naming another domain → HOLD (path b).** Rich X with a seam
  `{with_domain: "Y", ae_profile: {interactions: [{with: "...", mechanism: "...", severity: "high"}]}}`,
  Y present-with-plan. Assert: X is held (`SEAM_ADDITIVE_AE_HELD`), finding carries the interaction
  detail + `with_domain`. Mutation-RED: skip the seam-interaction read → X not held → RED.
- **P3 — compound band STILL holds (no regression).** A `supplements` + `peptides` pair sharing a
  `meta.ae_profile.additive_classes` token (an existing test). Assert: the supplement is held via the
  UNCHANGED screen 4 (`holds["supplements"] == ADDITIVE_AE_HELD`), `report["additive_ae"]` populated,
  Leg-1 adjudication + queue collation byte-identical to today. Mutation-RED (inverse): if rich findings
  had leaked into `report["additive_ae"]`, the compound-band `finding_id` would change → RED.
- **P4 — clean rich pair records.** Two rich domains whose seams carry NO `ae_profile` (or
  non-intersecting classes and no interactions). Assert: neither is held on the AE/Rx axes; both fold
  into the composed comprehensive plan. Guards against a false-positive floor.
- **P5 — malformed seam-AE behaves per §4.** (i) [AMENDED 2026-07-13 — flipped to fail-closed] A seam
  with a PRESENT-but-malformed `ae_profile` (a non-dict; or `additive_classes` / `interactions` of the
  wrong type): assert the declaring domain IS held on the AE axis (`SEAM_ADDITIVE_AE_HELD`) + a distinct
  `malformed-ae-profile` diagnostic finding; ABSENT and VALIDLY-EMPTY stay inert (the boundary).
  Mutation-RED for (i): revert `_seam_ae_malformed` to treat malformed as absent → the domain is not held
  → RED. (ii) The SAME malformed seam also carries `nature: "conflict"`: assert the conflict hold STILL
  fires (the malformed AE data must not suppress the existing seam-conflict hold — the AE hold and the
  conflict hold are INDEPENDENT). Mutation-RED for (ii): if malformed-inert is applied to the whole seam,
  the conflict hold vanishes → RED.
- **P6 — rich Rx-BPMH → HOLD (path c).** A rich domain with a seam `ae_profile.additive_classes`
  intersecting `operator_rx_classes`. Assert: the domain is added to `rx_bpmh_held` and
  `report["rx_bpmh"]`. Mutation-RED: restrict screen 5's class source back to `("supplements",
  "peptides")` over `meta` only → rich domain not held → RED.
- **P7 — end-to-end fail-closed drop.** Through `care_chat.synthesize`: a held rich domain (from P1/P2/P6)
  is DROPPED from the composed `programs` (absent from the recorded comprehensive version), i.e. the
  honest no-plan-for-that-domain state, never folded un-screened. Mutation-RED: remove the
  `SEAM_ADDITIVE_AE_HELD`/`rx_bpmh_held` population → the rich domain appears in the composed version → RED.

---

## 6. Frozen-spine + scope impact

**Files touched:**

| File | Change |
|------|--------|
| `scripts/plan/domain_program.py` | Add `SEAM_AE_PROFILE = "ae_profile"` to the seam key-name block; document the seam `ae_profile` sub-structure in the `cross_domain_seams` contract docstring. `validate`/`missing_required_fields` signatures + bodies UNCHANGED (seam edge stays reader-enforced). |
| `scripts/plan/orchestrate.py` | Add `_seam_ae_profile` + `_seam_ae_classes` readers; add the rich additive-AE screen (paths a/b) + the Rx-BPMH class-source extension inside the existing seam pass; add `SEAM_ADDITIVE_AE_HELD` reason + `report["seam_additive_ae"]` key. |
| `scripts/serve/care_chat.py` | **No functional change** — `synthesize` already drops on `holds`/`rx_bpmh_held`. (Optional: a doc-comment cross-reference.) |
| `docs/plan-generation/author-dispatch-process.md` | Document the seam `ae_profile` sub-structure as the rich-domain AE channel. |
| `tests/plan/test_orchestrate.py` (+ `test_domain_program.py`) | Probes P1–P7. |

**`<always-frozen>` six stay numstat=0.** `store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`,
`adjust.py`, `router.py` are NOT touched. The change lives entirely in the ADR-0041-owned
(`domain_program.py`) and ADR-0043-superseded (`orchestrate.reconcile`, `care_chat`) surface — the
surface ADR-0043's freeze-break sign-off already covers. `adjudicate.py` (frozen) is unchanged: rich
findings fail-closed by DROP, not by adjudication (adjudication of rich findings is a follow-up, §7).

**"Breaks if" (Core Rule 2):**

- Breaks if a rich specialist carries AE data in a program-level field instead of on seams → the seam
  reader won't see it. Option B forbids the parallel field; the author contract MUST put rich AE on
  seams. (Enforced by convention + the author-dispatch doc, not by `validate`.)
- Breaks if the canonical AE-class vocabulary drifts between two authors (`bleeding-risk` vs
  `bleeding_risk`) → the shared-class match is exact-token and silently misses — the SAME V1 precision
  gap the compound band already carries (author-dispatch-process.md). Promoting the vocabulary to a
  shared constant would narrow this but is NOT required by Option B (the compound band has no such
  enum); left as an optional follow-up.
- Breaks if a rich↔COMPOUND interaction must be screened across legs → in `synthesize`, the rich
  `collect` pass contains ONLY rich candidates (the compound band is reconciled in Leg 1), so a rich
  domain sharing a class with `peptides`/`supplements` is not detected. This is the floor-vs-seam
  partition ADR-0043 OQ-1 owns; noted §7, NOT designed here.
- Breaks if a future change routes `SEAM_ADDITIVE_AE_HELD` domains to adjudication in `generate_plans`
  without adding a `_seam_additive_ae_safety_finding` builder → today they stay held (safe). A future
  adjudication wiring must add the finding builder (mirrors `_additive_ae_safety_finding`).

---

## 7. Out of scope (explicit)

- **The PF-S133-02 `validate_plan_version` chokepoint backstop.** The defense-in-depth enforcement of
  validate + load-clearance at the shared store-write chokepoint (so NO path can bypass the floors) is a
  SEPARATE kn29-adjacent concern (bead `a-plus-maxing-kn29` guard (2)); it is NOT the floor re-base and
  is NOT designed here. It is the correct home for a fail-LOUD upgrade of the malformed posture (§4).
- **Adjudication + doctor-visit-queue collation of rich-domain findings.** The compound band evolved
  screen (S73) → adjudication (S74) → queue (S77); Option B delivers the rich SCREEN (HOLD = fail-closed
  drop). Routing rich findings through the liaison gate + `collate_doctor_visit_queue` is a follow-up.
- **The rich↔compound cross-leg AE partition** (ADR-0043 OQ-1: which interactions are always-on floors
  vs specialist-declared seams). Option B screens rich↔rich within the rich pass; a unified rich+compound
  pass is a larger reconciliation-topology decision.
- **The daily-monitor / live-monitoring layer** (`daily_monitor.py`, beads `7nw7`/`yeo3`/`glzi`/`4wno`)
  — held pending the operator live-feed conversation.
- **The operator-present LIVE comprehensive-plan run** (real spend/data) — operator-gated (ADR-0041/0043
  OQ-4).

---

## Consumes / consistency

- ADR-0041 §Consequences-Neutral: "the `reconciliation`/`meta` side-channel … folds into
  `cross_domain_seams` … an ADR-0043 concern" — Option B IS that fold for the AE sub-structure.
- ADR-0043 Decision §3 + OQ-1: reconcile by reading `cross_domain_seams`, generalizing the five
  hard-coded holds; the safety-critical subset stays always-on. Option B keeps the compound band as an
  always-on floor (screens 4/5 over `meta`, unchanged) AND adds the seam-sourced rich screen — the
  floor-and-seam coexistence OQ-1 anticipates.
