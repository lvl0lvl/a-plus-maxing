# Phase 6 Adversarial Review — genetics-specialist deployed profile

Reviewer: dedicated adversarial-review agent (fresh context), `/adversarial-review` DOCUMENT methodology (8 categories) + 4 agent-specific criteria + load-bearing faithfulness check.
Target: `.claude/agents/genetics-specialist/agent.md` (170 lines, ≤200 ceiling) + `library-index.md`, reviewed as a cohesive unit against `design/genetics-specialist-design.md` (Final) and the deployed sibling `cardiovascular-specialist/agent.md`.

## Summary

The deployed profile is **faithful to the Final design doc and DEPLOY-READY**. It passes the LIVE `scripts/audit-specialist-profile.sh` with **0 violations / EXIT=0** (1 documented WARN: 8622-token medical overrun under Rule 7, not a BLOCK). All four Phase-3 red-team safety fixes are encoded verbatim-equivalent. All 6 PF ids resolve in `process-failures.md`; all 8 refusal-class IDs resolve in `templates/refusal-class-taxonomy.yaml`; the `_source-whitelist.md`, `vault/dna/`, `vault/meta/contradictions.md`, and `templates/*.yaml` references resolve. No Critical or Major document defect was found after a full 8-category walk. Findings are 0 Critical / 0 Major / 6 Minor / 3 Nitpick — all editorial or theoretical-edge, none blocking.

Reference spot-check and the live audit were run against the worktree (`ad89d61`). Two design-doc-disclosed worktree-vs-integration gaps were confirmed as real but already dispositioned as integrator-side (OQ-3 genetics risk-class row, OQ-1 bda gate); they are NOT new findings.

## Findings

### AR-001: `vault/dna/raw/` directory does not exist in the worktree, yet four instructions say "read it before writing any variant page"

| Field | Value |
|-------|-------|
| **Category** | E — Edge Case Gaps |
| **Severity** | Minor |
| **Section** | Tools (L67, L69); Context Loading step 3 (L91); Modes empty-state (L118) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** The profile instructs the agent to `Read vault/dna/raw/ before writing any variant page` in four places. Filesystem check: `vault/dna/raw/` does NOT exist in the worktree (only `vault/dna/analysis.md` is present). A literal `Read`/`Glob` on a non-existent path errors rather than returning "empty." The profile DOES specify the correct fallback — "If `dna/raw` is empty, enter empty-state — do not fabricate a call" (L91) and the Modes empty-state (L118) — so the agent reaches the right terminal behavior. The gap is only that "empty" (directory exists, no files) and "absent" (directory missing) are not the same observable, and the empty-state clause is keyed on "empty." A deliberately literal agent could read the missing-path error as an exceptional state not covered by "empty."

**Evidence:** L91 — "Read `vault/dna/raw/` before authoring any variant page … If `dna/raw` is empty, enter empty-state — do not fabricate a call." Filesystem: `ABSENT vault/dna/raw/`.

**Fix:** Accept (low impact: empty-state is the intended terminal behavior whether the dir is empty or absent, and a missing-path read failing is itself fail-safe — it cannot fabricate a call). If touched, broaden L91/L118 to "empty or absent." Not a deploy blocker.

### AR-002: Identity (L11) and the description sentence (L3) duplicate ~70% of their content

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy |
| **Severity** | Minor |
| **Section** | Description (L3) + Identity (L11) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** L3 ("non-clinician genetics, pharmacogenomics, and nutrigenomic literacy-and-routing layer and the owner of `vault/dna/`: it holds sequence-variant apart from diagnosis and probability apart from certainty, and routes consequential findings to clinicians") and L11 Identity ("serves the DTC-raw and EMERGENCY safety floors and the `vault/dna/` provenance contract, holding a variant apart from a diagnosis and a probability apart from certainty, recognizing-and-routing consequential findings to care") restate the same "variant apart from diagnosis / probability apart from certainty / route to care" trio. This is the SAME pattern as the deployed sibling (cardiovascular L3 vs L11), so it is an established roster idiom — the description is the orchestrator-facing routing blurb, the Identity is the in-profile anchor with its own ≤40-word mechanical check (verified: 32 words). Load-bearing-test: removing either would break a different consumer.

**Evidence:** L3 and L11 quoted above.

**Fix:** Accept — matches sibling idiom; the two serve distinct consumers (routing-blurb vs identity-anchor) and the Identity carries the DTC/EMERGENCY-floor framing the description omits. No change.

### AR-003: "the four substrate safety floors are rules 1–4" (design §5) does not match the deployed rule numbering — but the agent.md does NOT make the claim

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradictions |
| **Severity** | Minor |
| **Section** | Core Rules (L19–L30) vs design doc §5 preamble + §15.2 AC-2 |
| **Resolution** | Prevent (design-doc-side; agent.md is clean) |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` (clean); `design/genetics-specialist-design.md` §5 (source of the mismatch) |

**Description:** The design doc §5 preamble asserts "The four substrate safety floors are rules 1–4," but §15.2 AC-2 names the four floors as DTC-raw≠diagnostic, risk-variant≠disease→counselor+MD, PGx-informs-not-authorizes, and genetic-exceptionalism/privacy. In the deployed agent.md those four map to rules **1, 2, 4, and 10** — the genetic-exceptionalism/privacy floor is rule 10, not rule 4; rule 3 is the disease-risk/EMERGENCY routing. So the design doc's "rules 1–4" framing is internally inconsistent with its own AC-2 floor list. Critically, the **deployed agent.md does NOT make the "rules 1–4" claim** — its Core Rules preamble (L17) says only "each rule is grep/field-resolvable." All four floors ARE present as Core Rules (verified: r1 DTC, r2 risk≠disease, r3 EMERGENCY-route, r4 PGx, r10 privacy), each with a "Mechanical Check" pass/fail clause, satisfying AC-2's actual requirement ("a Core Rule grep-resolves for each floor"). The contradiction lives only in the spec preamble; the compression correctly dropped the brittle numbering claim.

**Evidence:** Design §5 L128 — "The four substrate safety floors are rules 1–4." Design §15.2 AC-2 — names privacy/exceptionalism as the 4th floor (= deployed r10). Agent.md L17 makes no rule-range claim.

**Fix:** No agent.md change required (it correctly omitted the inaccurate claim — this is faithful compression, not a defect). Flag for the design-doc owner (Phase 8 follow-up): §5 preamble should read "the four substrate safety floors are Core Rules (DTC r1, risk≠disease r2, PGx r4, exceptionalism r10), the DTC and EMERGENCY floors evaluated first," to stop disagreeing with AC-2.

### AR-004: "evaluated first" applies to two floors (DTC + EMERGENCY) with no stated tie-break when both fire on one input

| Field | Value |
|-------|-------|
| **Category** | O — Ordering/Dependency Gaps |
| **Severity** | Minor |
| **Section** | Core Rules r1/r3 (L19, L21); Ask-vs-Proceed step 2 (L45); Loop-Breaking (L57) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** Two floors are each declared "evaluated first": r1 DTC-raw ("the dominant provenance behavior, evaluated first") and the EMERGENCY gene-class escalation (Ask-vs-Proceed step 2 bundles both as "evaluated FIRST"). EC-11 in the design doc is exactly the composite case (a third-party-interpretation export that is BOTH unconfirmed-raw AND could name an EMERGENCY gene class). The profile does not state which fires first when a raw/unconfirmed EMERGENCY-gene call arrives — does the DTC `BASIS_NOT_REVIEWABLE`/confirmation-required statement gate, or does `TIME_CRITICAL` escalation gate? Adversarial read: an agent could emit only the DTC confirmation-required statement and treat the EMERGENCY escalation as "deferred until confirmed," missing a time-critical finding. Mitigating: both are fail-safe (DTC refuses to ground action; EMERGENCY escalates), the Modes empty-state explicitly says a raw EMERGENCY-class call "still fires `TIME_CRITICAL`" even with zero data (L118), and "when uncertain, escalate" (r3) biases toward the safer of the two. So the composite resolves to escalate-and-flag-unconfirmed in practice, but the precedence is implicit, not stated.

**Evidence:** L19 "evaluated first"; L45 "DTC-raw / EMERGENCY floor — evaluated FIRST"; L118 "A presented DTC-raw actionable call still fires the confirmation-required floor … an arrhythmia/cardiomyopathy/aortopathy gene-class finding fires `TIME_CRITICAL`."

**Fix:** Accept (both paths are fail-safe and the EMERGENCY escalation is the strictly-safer dominant action, which L118 already encodes for the empty state). If desired, one clause in r3: "a finding that is BOTH unconfirmed-raw AND EMERGENCY-gene-class escalates `TIME_CRITICAL` first, carrying the unconfirmed-provenance flag — escalation is not deferred pending confirmation." Not blocking.

### AR-005: "facilitates referral" / "explains why" / "facilitate referral" — verbs with no concrete tool or routing channel

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions (agent-specific: operational completeness) |
| **Severity** | Minor |
| **Section** | Core Rules r3 (L21) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** r3 says a disease-risk class "routes to a certified genetic counselor + physician — the agent explains why, facilitates referral, delivers no verdict." "Facilitates referral" has no concrete mechanism in the Tools section — there is no tool/channel to a genetic counselor, and the only live routing channel the profile defines is the `medical-liaison` (`BLOCK_WITH_OVERRIDE_PATH`), which is named for the EMERGENCY class and disease-risk verdict surfaces but not explicitly tied to the counselor-referral verb. An agent could read "facilitate referral" as a real action it cannot perform (no counselor channel exists) and either stall or improvise. In practice the routing IS the medical-liaison (Loop-Breaking L60 routes "a disease-risk verdict surface" via the live medical-liaison), so the operational answer exists — it is just one indirection away from the r3 verb.

**Evidence:** L21 "routes to a certified genetic counselor + physician — the agent explains why, facilitates referral"; Tools (L67) defines no counselor channel; L60 routes disease-risk surfaces via the medical-liaison.

**Fix:** Accept (the medical-liaison is the documented routing target for disease-risk surfaces; "facilitate referral" = surface the structured recommendation + route via medical-liaison, which L60 already specifies). Optional: make r3's "facilitates referral" read "surfaces the referral recommendation via the medical-liaison." Not blocking.

### AR-006: Sibling encodes a `library-index.md` denylist/strip note for fenced BAD blocks (AQ-002); genetics `library-index.md` does not mention it

| Field | Value |
|-------|-------|
| **Category** | D — Downstream Breakage (cross-file consistency) |
| **Severity** | Minor |
| **Section** | `library-index.md` (whole file) vs agent.md Negative Examples (L125) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` (Negative Examples) |

**Description:** Negative Examples (L125) asserts "BAD blocks fenced so banned-modal/operator tokens strip per AQ-002." The live audit reports `negative-examples: 6 markers (denylist absent — content pending S-08 bead)`, i.e. the AQ-002 strip denylist is a known-pending mechanism, not yet live. The agent.md's BAD blocks ARE fenced (verified L129–139, L144–154, L159–169), which is the in-profile half of the contract, so the agent-side obligation is met. The downstream strip-denylist is a roster/maintainer artifact (S-08 bead), correctly out of this profile's ownership. No defect in the profile; flagging only that the L125 "strip per AQ-002" claim leans on a mechanism the audit marks pending — the fencing (the part this profile controls) is present and correct.

**Evidence:** L125 "BAD blocks fenced so banned-modal/operator tokens strip per AQ-002"; audit: "denylist absent — content pending S-08 bead"; BAD blocks fenced at L129/L144/L159.

**Fix:** Accept — the profile satisfies its half (fencing present); the strip denylist is the maintainer's S-08 bead, already tracked. No change.

### AR-007: "the strictest research floor in the roster" — unverifiable superlative carried in the profile body

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy / S — Scope (claim the profile cannot self-verify) |
| **Severity** | Nitpick |
| **Section** | Tools (L70) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** L70 calls `--mode=deep --target-class=reference` "the strictest research floor in the roster." This is a cross-roster comparative the genetics profile cannot verify from its own context (it would need the full `specialist-risk-class.yaml` of every sibling). It is true today (deep > standard, the cardiovascular sibling is standard/compound) but is a maintenance-fragile superlative — if a future specialist is also deep, the claim silently goes stale. It carries no behavioral load (the behavior is "dispatch deep/reference, never lower"; "strictest" adds nothing the floor itself does not).

**Evidence:** L70 "mode_floor `deep`, target_class `reference` — the strictest research floor in the roster."

**Fix:** Accept (cosmetic, currently accurate). If trimmed for token economy, drop "— the strictest research floor in the roster" (saves a clause, removes a stale-able comparative). Non-blocking.

### AR-008: Description sentence (L3) is unfenced narrative containing operator-routing language but no sentinel — relies on convention

| Field | Value |
|-------|-------|
| **Category** | R — Broken References (structural) |
| **Severity** | Nitpick |
| **Section** | Description (L1–L3) + IDENTICAL block (L5–L7) |
| **Resolution** | Accept |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** The IDENTICAL block is correctly sentinel-fenced (`<!-- IDENTICAL-BLOCK-START/END -->`, L5/L7) and the audit confirms it (anti-sycophancy A=1 B=1 C=1, identical-block check present-but-skipped as first specialist with no corpus). The L1–L3 description has no frontmatter (audit: "no frontmatter — foundation-shape profile — skipped"), matching the sibling's shape. This is consistent with the roster idiom, so no defect — noted only because the `description-routing` and `audit-passed-frontmatter` checks both skip on this profile, meaning two audit dimensions are unexercised here and rely on the sibling-shape convention rather than a positive check.

**Evidence:** Audit: "description-routing: no frontmatter (foundation-shape profile) — skipped"; "audit-passed-frontmatter: no frontmatter — skipped (orchestrator-accept gate)."

**Fix:** Accept — matches the deployed sibling's foundation shape; no frontmatter is the intended form for this profile class. No change.

### AR-009: `templates/specialist-risk-class.yaml` genetics row referenced as authoritative in two body locations but absent from the worktree

| Field | Value |
|-------|-------|
| **Category** | R — Broken References |
| **Severity** | Nitpick (disclosed; integrator-side) |
| **Section** | Tools (L70); Context Loading step 1 (L89) |
| **Resolution** | Handle (root cause is integration-environment; already disclosed) |
| **Affected File** | `.claude/agents/genetics-specialist/agent.md` |

**Description:** L70 and L89 reference "the genetics row" of `templates/specialist-risk-class.yaml` ("mode_floor `deep`, target_class `reference`") as a contract to read. Filesystem: the worktree `templates/specialist-risk-class.yaml` exists but has **NO genetics-specialist row** (`grep` returns nothing). The live audit confirms this: `mode-floor-correctness: genetics-specialist not in risk table — skipped`. This is exactly design-doc OQ-3 / SF-GEN-07 (LEGITIMATE-MODIFIED): the row is present in the integrator's main checkout and resolves at rebase-merge, and the floor is double-protected by the prose-hardcoded dispatch string in the profile body (L29, L70). So the reference is broken in the worktree but (a) disclosed, (b) integrator-resolving, and (c) the in-profile prose dispatch string is the standalone defense. Not a new finding — confirming the design doc's own disclosure is accurate.

**Evidence:** L70/L89 reference the genetics row; worktree grep: "NO genetics row in project worktree yaml"; audit: "genetics-specialist not in risk table — skipped." Matches design §18 OQ-3.

**Fix:** Handle — no profile change; the prose dispatch floor (L29/L70) is the in-profile defense and the row resolves at integration. The integrator MUST confirm the row is present (deep/reference) at merge, per OQ-3. Already tracked.

## Faithfulness check (the four Phase-3 red-team safety fixes)

| Safety fix (red-team finding) | Status | Line locator in agent.md |
|---|---|---|
| **1. EMERGENCY trigger = gene CLASS recognized by phenotype OR gene symbol (SCN5A/FBN1/KCNQ1/RYR2/CALM1–3) with "when uncertain, escalate"** (F-001/SF-GEN-01) | **PRESENT** | **L21** — "The trigger is the gene CLASS, not a closed triad-word list: a finding named only by gene symbol (SCN5A/KCNQ1/RYR2 channelopathies, FBN1 aortopathy, ACMG-SF CALM1–3) is in-class; when uncertain whether a gene belongs, escalate (fail toward escalation)." Reinforced in the Mechanical Check ("named by phenotype OR gene symbol alone"), Loop-Breaking L57, and Modes empty-state L118. |
| **2. `confirmation_status: confirmed-clinical-grade` bound to an agent-citable lab artifact, never operator say-so** (SF-GEN-04) | **PRESENT** | **L19** — "A page is stamped `confirmation_status: confirmed-clinical-grade` only against an agent-citable accredited-lab artifact, never an operator's asserted confirmation (operator is A3; an assertion is not evidence) → `BASIS_NOT_REVIEWABLE`, the page stays `unconfirmed-raw`." Mechanical Check on same line confirms "never stamped on an operator assertion." |
| **3. Out-of-scope recognize-and-refer rule (carrier/reproductive, somatic-vs-germline, mosaicism, mitochondrial, prenatal/pediatric incl. minors, embryo, pharmacovigilance)** (F-002/SF-GEN-02) | **PRESENT** | **L30 (Core Rule 12)** — names all seven undeveloped subdomains incl. "the predictive-testing-of-minors norm," maps to `BASIS_NOT_REVIEWABLE` / `HIGH_RISK_SAMD` + counselor+MD, "never an improvised in-domain interpretation." Restated in Role-Boundaries "I do NOT own" (L38). |
| **4. All four safety floors as Core Rules; 8 refusal classes incl. mandatory AUTHORITY_FRAMING_BYPASS** | **PRESENT** | Four floors: DTC **L19 (r1)**, risk≠disease **L20 (r2)**, PGx **L22 (r4)**, genetic-exceptionalism/privacy **L28 (r10)** — each with a Mechanical Check pass/fail. 8 refusal classes enumerated in Role Boundaries **L34**, AUTHORITY_FRAMING_BYPASS flagged "(mandatory)". Live audit: `refusal-classes: 8 … authority-framing: 4 mentions`. |

All four safety fixes are PRESENT. The compression is faithful: no fix was dropped, softened, or moved to a non-load-bearing location.

## Reference spot-check

**PF ids** (≥3 required to spot-check; all 6 in the profile verified):
- `PF-S2-01`, `PF-S2-02`, `PF-S2-04`, `PF-S2-05`, `PF-S3-01`, `PF-S6-01` — **all 6 resolve** in `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/memory/process-failures.md` (which carries PF-S2-01..06, PF-S3-01, PF-S6-01, plus orchestrator-class PF-S12/13/16/17 correctly excluded as out-of-scope per design §11.1). Live audit: `pf-resolution: 6 distinct PF ids` (≥3 required — PASS).

**8 refusal-class IDs** (verified in `templates/refusal-class-taxonomy.yaml`, worktree copy):
- `BASIS_NOT_REVIEWABLE`, `AUTHORITY_FRAMING_BYPASS`, `TIME_CRITICAL`, `PRESCRIPTIVE_DIRECTIVE`, `PATIENT_FACING_DIRECTIVE`, `HIGH_RISK_SAMD`, `IMAGE_OR_SIGNAL_INPUT`, `DEVICE_FUNCTION` — **all 8 resolve** in the taxonomy yaml AND all 8 are enumerated in the profile's Role Boundaries (L34). No invented class. Live audit: `refusal-classes: 8 taxonomy class(es) referenced`.

**Other references checked:** `vault/library/_source-whitelist.md` (resolves), `vault/dna/` (resolves; `analysis.md` present), `vault/meta/contradictions.md` (resolves), `templates/refusal-class-taxonomy.yaml` + `templates/specialist-risk-class.yaml` (both present; genetics row absent per OQ-3 → AR-009). `vault/dna/raw/` ABSENT → AR-001.

**Live audit:** `scripts/audit-specialist-profile.sh .claude/agents/genetics-specialist/agent.md` → **0 violations, 1 warning, EXIT=0**. Warning is the documented 8622-token medical overrun (Rule 7 / bead 2qq); the ≤200-line ceiling (the BLOCK condition) is met at 170 lines.

## Verdict

**DEPLOY-READY.**

The deployed genetics-specialist profile is faithful to the Final design doc, passes the live audit with 0 violations / EXIT=0, encodes all four Phase-3 red-team safety fixes verbatim-equivalent, and resolves every PF id and refusal-class reference checked. The 8-category adversarial walk plus the 4 agent-specific criteria surfaced **0 Critical, 0 Major, 6 Minor, 3 Nitpick** findings — every one is editorial, theoretical-edge, or already disclosed-and-dispositioned by the design doc (OQ-3/OQ-1). Per the skill's own DEPLOY criterion ("a profile that is faithful + passes audit + has no Critical/Major document defect is DEPLOY-READY"), this profile qualifies.

**Must-fix list:** none (no blocking findings).

**Recommended (non-blocking, Phase-8 follow-up — not deploy gates):**
- AR-003: correct the design-doc §5 "rules 1–4" preamble to match AC-2's floor list (agent.md is already correct; this is a spec-hygiene item).
- AR-009 / OQ-3: integrator MUST confirm the `genetics-specialist` deep/reference row resolves in `templates/specialist-risk-class.yaml` at rebase-merge and that `--check mode-floor-correctness` runs against the populated row.
- AR-001: optionally broaden the empty-state clause to "empty or absent" for `vault/dna/raw/`.
