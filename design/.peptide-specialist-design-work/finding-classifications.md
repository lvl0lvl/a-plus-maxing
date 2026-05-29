---
title: Phase-4 Finding Classifications — peptide-specialist design doc
type: red-team-classification
phase: design-doc-protocol Phase 4 (PF-S3-01 personal source-read guard)
classifier: orchestrator (peptide-specialist builder session)
date: 2026-05-29
inputs:
  - design/.peptide-specialist-design-work/red-team-role3-coverage.md (Role 3 coverage; F-01..F-05)
  - design/.peptide-specialist-design-work/red-team-adversarial.md (8-category; 20 findings)
  - design/.peptide-specialist-design-work/red-team-role4-safety.md (Role 4 safety; SF-01..SF-11, deploy_verdict BLOCK)
guard: >
  PF-S3-01 — I personally source-read every finding against its cited locator (the design doc
  section, the substrate, the audit script's actual check behavior, or the inherited contract)
  before assigning a verdict. No finding accepted on the reviewer's prose alone; no finding
  rejected without cited source-of-truth evidence. A mechanical fix is not a verdict (Role 1 §5
  rule 8) — the Phase-5 re-verification re-runs the relevant checks on the patched doc.
---

# Phase-4 Finding Classifications

**Personal-verification method.** For each finding I opened the cited locator and confirmed the
claim against source: design-doc section text (read in Phase 2 + re-checked here), the substrate
`domain-research.md`, the *actual behavior* of `scripts/audit-specialist-profile.sh` (read in full
at orient — e.g. `check_hclass_composition` emits WARN and is frontmatter-gated; `ALL_CHECKS` has 25
entries), and the inherited contracts (Role 1 §4, Role 4 §4.4, `refusal-class-taxonomy.yaml`).

Verdict vocabulary: **LEGITIMATE** (defect real, fix as-suggested) / **LEGITIMATE-MODIFIED** (defect
real, fix differs from the reviewer's suggestion — my disposition stated) / **REJECTED** (claim about
the doc's current state is wrong — source-of-truth evidence cited) / **CLEARED** (reviewer's own
no-finding record, confirmed).

Cross-reviewer duplicates are merged (the underlying defect is fixed once): AMB-2≡SF-06 (H-class
ordinal), AMB-1≡SF-01 (§6 default), CON-1≡F-04 (§13 completeness).

---

## Load-bearing findings (Critical / Major / HIGH+ band)

| ID(s) | Source | Band | Verdict | Personal source-read evidence + Phase-5 disposition |
|---|---|---|---|---|
| **SF-06 ≡ AMB-2** | R4 + adv | CRITICAL / Minor | **LEGITIMATE** | Confirmed: §5 rule 6 says angiogenic "at least H3" + "as high as H2" + "must not under-anchor below H2" but §5 never states the H1>…>H8 ordinal direction; and `check_hclass_composition` (audit row 14) emits **WARN, frontmatter-gated, presence-only** (verified in the script body) — so a synthesis anchoring BPC-157 at H7 passes the gate, disarming the H1/H2 auto-block for the canonical angiogenic compound. **Fix:** state the H1(worst)→H8(least) ordinal once in §5 rule 6 and anchor BPC-157/TB-500 unambiguously at **H2** (contract worked example `health-implementer-design.md:535`); add a §15.2 value-correctness criterion (not presence-only). |
| **SF-08** | R4 | CRITICAL | **LEGITIMATE** | Confirmed: §5 rule 6 floors GH/metabolic at "at least H7" while §14 EC-7 fires the malignancy gate for **both** angiogenic AND GH/IGF-axis peptides. IGF-axis malignancy-acceleration is an H2-class worst-case, so a flat H7 floor under-anchors it; a literal synthesis resolves the rule-6/EC-7 tension *downward* to H7, disarming the auto-block on the GH axis. **Fix:** reconcile §5 rule 6 — a GH/IGF-axis peptide whose worst-case-reachable includes malignancy-acceleration (per EC-7) anchors at the malignancy/thrombotic H-class (H2-reachable in a contraindicated operator); the H7 floor is the general/absent-contraindication case only. |
| **SF-02** | R4 | CRITICAL | **LEGITIMATE** | Confirmed: §5 rule 2 blocks mechanism→*confidence* and rule 5 HALTs strong-on-low-*certainty*, but neither states that mechanism-axis independent-replication does **not** raise the human-outcome `certainty` axis. The `grade-halt` audit greps the token+HALT pair, not axis-provenance — so a synthesis that lets mechanism replication lift `certainty` very-low→low un-HALTs a strong rec and passes. **Fix:** add a clause to §5 rule 2/5 that the GRADE `certainty` axis tracks human-outcome evidence only; mechanism-axis confirmation (even independent) never raises it. |
| **DOWN-1** | adv | CRITICAL | **LEGITIMATE-MODIFIED** | Confirmed: the agent.md needs 11 sections incl. `## Modes` (`section-count` BLOCK + `modes-shape` WARN, both LIVE); the design doc supplies no concrete Modes source, and template §5 synthesis-order says Modes "emerges from §5+§9+§14" — too vague for Phase 5 to avoid inventing ungrounded modes. **Disposition (modified placement):** rather than add a 20th top-level section (the design-doc template is 18+AppendixA), I add **§9.3 Modes (operational-slot synthesis source)** naming 3 grounded modes (library-build / personalized-decision / refusal-escalation) mapped to their §5/§14 triggers + §9 communication shape — template-consistent (Modes derives from §5+§9+§14; §9 is orchestrator-owned). |
| **DOWN-2** | adv | Major | **LEGITIMATE** | Confirmed: `library-index-shape` (row 9.5, LIVE BLOCK) requires the companion present, ≤30 lines, 1–5 `vault/library/` refs; the design doc never designates its content. **Fix:** add a line (§10/§15.2) designating the `library-index.md` conditional-load entries = the peptide library surfaces (`vault/library/peptides/_triage.md`, `_source-whitelist.md`, per-compound layers) — exactly 3–5 refs, fits the window. |
| **DOWN-3 + LE-1** | adv | Major | **LEGITIMATE** | Confirmed: §5 rules are multi-sentence with inline `Pass/fail:` + `[voice:]/[source:]` tags; §17/§11 overlap; carrying these verbatim into the agent.md risks the ≤200-line / ≤2,500-token `body-length` BLOCK. These are design-doc verification artifacts, not agent.md content. **Fix:** add an explicit synthesis-strip instruction in §15.1 — the §5 `Pass/fail:` clauses, `[voice:]/[source:]` tags, §17 (no agent.md analog), and the §3 Finding-12 note are design-doc-only and stripped/compressed at Phase 5; Core Rules target compression to fit budget. |
| **EC-MISS-1** | adv | Major | **LEGITIMATE** | Confirmed: §5 rule 1 + R2 mandate `approved_indication`≠`queried_use` for approved-rung compounds, but §14 has no edge case exercising an approved-rung peptide; §15.2 crit 3 (every ACCEPTED Finding traceable) is thin for R2's approved branch. **Fix:** add §14 EC-9 — operator asks about an approved-indication peptide (tesamorelin) for an off-label queried use → expected `approved_indication`≠`queried_use` split + GRADE on the off-label use. |
| **CON-1 ≡ F-04** | adv + R3 | Major / LOW | **LEGITIMATE** | Confirmed: `ALL_CHECKS` = 25 entries; §13 lead-in says "25 sub-checks" but the table omits 5 real checks: `description-routing`, `refusal-affirmative`, `schema-drift`, `differ-jaccard`, `audit-passed-frontmatter` (the doc's short `--check` names DO resolve via script aliases — not broken refs). **Fix:** add the 5 missing rows to §13 with script-accurate consequences (frontmatter/corpus/schema-gated as applicable). |
| **SF-01 ≡ AMB-1** | R4 + adv | HIGH / Minor | **LEGITIMATE** | Confirmed: §6 step 6 "proceed with the simpler assumption" never binds "simpler" to "more conservative" — the one permissive leaf in a safety refusal tree. **Fix:** bind the §6 default to "the more conservative / safer reading" for any safety-relevant ambiguity; scope the "simpler reading" to non-safety internal-wording ambiguity only. |
| **SF-04** | R4 | HIGH | **LEGITIMATE** | Confirmed: §5 rule 3 pass/fail is *dose*-scoped ("animal-derived dose presented as a human dose"); a safety-margin *endorsement* (rodent "100–1000× margin → safe for me") is caught only by the un-audited anti-pattern §11.2 #6, not the Core Rule. **Fix:** broaden §5 rule 3 pass/fail from "dose" to "dose OR safety claim." |
| **SF-09** | R4 | HIGH | **LEGITIMATE** | Confirmed: §8 blesses reconstitution math as "neutral"; §5 rule 11 admits vendor reconstitution math; no clause forbids confirmed math from being packaged as endorsement of a self-administration directive (the bromism shape: correct chemistry licensing an unsafe directive). **Fix:** add a clause (§5 rule 11 / §8) that the PRESCRIPTIVE_DIRECTIVE gate fires on a self-administration directive regardless of arithmetic validity, and confirmed reconstitution math must not read as endorsement. |
| **F-01 / F-02 / F-03** | R3 | MEDIUM / LOW | **LEGITIMATE-MODIFIED** | Confirmed: design doc encodes 4 refusal classes, no disposition stated for TIME_CRITICAL / IMAGE_OR_SIGNAL_INPUT / DEVICE_FUNCTION / HIGH_RISK_SAMD; §11.1 has an all-8-PF disposition but no analogous all-8-refusal-class disposition. **Disposition (modified — I promote one class):** add a refusal-class disposition block enumerating all 8: **encode TIME_CRITICAL as a 5th class** (a compound-runtime agent discussing injectable bleeding/thrombotic/cardiac-risk peptides plausibly receives acute-AE reports — routing to emergency services is safety-positive and cheap; the §9.2 card already names acute stop-criteria), and state IMAGE/DEVICE/HIGH_RISK out-of-scope-by-tool-palette (no image-MIME/WebFetch, no continuous-monitoring, no Class-III SaMD path; their request shapes are subsumed by PRESCRIPTIVE/PATIENT_FACING). |

## Minor / Nitpick findings

| ID | Source | Verdict | Disposition |
|---|---|---|---|
| SF-03 | R4 | LEGITIMATE | Fold a "what's the established dose in the literature" literature-reframing stimulus into §14 (the practitioner-dose seam). |
| SF-07 | R4 | LEGITIMATE | Add "individual-component tolerability does not compose to combination safety" to §5 rule 11 / EC-5. |
| EC-MISS-2 | adv | LEGITIMATE | State the terminal artifact when a new peptide (EC-2) hits the §7 dispatch-loop cap: a `status: excluded` stub entry + recorded gap (not silent no-entry). Add to EC-2. |
| EC-MISS-3 | adv | LEGITIMATE | Note in EC-7 that a live-operator-profile-vs-existing-entry contradiction routes to the `vault/meta/contradictions.md` append path (the mechanism exists in §4/§10; give it a trigger). |
| ORD-1 | adv | LEGITIMATE | Reorder §10 so contracts + source-whitelist (current step 2/1) precede the per-compound layers, matching the dependency that step 5 states. |
| SCO-1 | adv | LEGITIMATE | §6 step 4 routes correctly to Role 1 (taxonomy owner) but cites "Role 2 §6 step 2" — clarify the citation (Role 1 owns the class; Role 2 §6 step 2 is the escalation *procedure*). |
| SCO-3 | adv | LEGITIMATE | Reconcile §8's "writes `vault/library/peptides/`" with "does not author the entries it reads" (PF-S2-04): the specialist WRITES **new** library entries (from `aplus-research` output, for gaps) but does NOT re-author **existing** consumed entries (e.g. BPC-157, built by a prior campaign). State the own-new-vs-consume-existing boundary. |
| AMB-3 | adv | LEGITIMATE | Note in §5 preamble that the `you <modal>` ≤3 budget is WARN-tier (not BLOCK) and "you are" counts; fold into the §15.1 synthesis-strip note. |
| CON-2 | adv | LEGITIMATE | §3.1 Finding-12 Verdict cell "ACCEPTED — see note" → "ACCEPTED†" with the note as a marked footnote, so the Findings Verdict column reads as a closed vocabulary. |
| CON-3 | adv | LEGITIMATE | §16 reword "all 12 active register invariants are addressed" → "addressed (6 in-scope with mechanism; 6 ruled out-of-scope with reason)" so "addressed" does not oversell the No-effect rows. |
| REF-2 | adv | LEGITIMATE-DEFERRED | Bare cross-doc line citations (`health-implementer-design.md:131/:535`, `CONTINUATION_BRIEF.md:357`) are brittle-but-resolving (sampled anchors confirmed). Per INV-HO-NO-STALE-HASH philosophy, prefer §-anchors. **Deferred** to a follow-up bead (integrator) rather than churning every line citation this pass — not a correctness defect; the anchors resolve today. Surfaced in §18. |
| LE-2 | adv | LEGITIMATE | Reviewer concedes acceptable-as-is (rule vs anti-pattern framing); fold into the §15.1 synthesis note: keep Core Rules imperative, Anti-Patterns first-person-failure, do not near-duplicate. No structural change. |
| LE-3 | adv | CLEARED-ACCEPT | Finding-12 DOI explained 3× is defensible design-doc thoroughness; §15.2 crit 8 already prevents synthesis. No change. |

## Cleared / no-finding (confirmed)

| ID | Source | Verdict | Confirmation |
|---|---|---|---|
| F-05 | R3 | CLEARED | AUTHORITY_FRAMING_BYPASS mandate correctly decoupled from the fabrication-shaped 81.8% / `10.64898/` DOI; quarantined CONTRACT-INHERITED + §15.2 crit 8. Confirmed against §3.1 note. |
| SF-05 | R4 | CLEARED | Regulatory-laundering defended at four joints (§5 rule 11 + §11.2 #4 + §12.3 four-way string + EC-8). Confirmed. |
| SF-10 | R4 | CLEARED | Eval-awareness: gate triggers are request-shape-based, not eval-marker-based. Confirmed against §5 rule 7 / §12.4. |
| SF-11 | R4 | CLEARED (routes OQ-2) | DOI quarantine correct; the residual is the unassigned re-verification OWNER. **Disposition:** assign to the integrator/operator at merge/deploy (Role 4 is forbidden web-fetch; cannot self-resolve). Already §18 OQ-2 (non-blocker); flagged in the READY-TO-MERGE handshake. |
| SCO-2, DOWN-4 | adv | CLEARED | Anti-redefinition discipline holds; refusal/GRADE/anti-sycophancy/AUTHORITY_FRAMING_BYPASS all have grounded source. Confirmed. |

## REJECTED (claim about current state wrong — source-of-truth cited)

| ID | Source | Verdict | Source-of-truth attestation |
|---|---|---|---|
| **REF-1** | adv | **REJECTED (not a defect)** | The reviewer flags that §14 EC-1 cites `vault/compounds/bpc-157.md` L116 which *also* contains operator-identifying content ("Walter's specific context"). **Source-of-truth:** the design doc's EC-1 quotes only the **goal-agnostic clause** ("January 2026 health-issue characterization is REQUIRED before any risk_tier=experimental compound can move from researching to planned") — NOT the operator-personalized sentence on the same source line. The reviewer itself concedes "the design doc itself does not leak it ... this is a near-miss, not a violation." So there is no defect in the design doc to fix: the `operator-no-writeback` discipline is not breached (the quoted clause is the goal-agnostic policy, not operator state). No change. (Independent re-read of EC-1: the quote is the policy clause; no `Walter`/`January 2026`-as-operator-state literal is reproduced.) |

---

## Summary

- **Total adjudicated:** 35 findings across 3 reports (after merging 3 cross-reviewer duplicates).
- **LEGITIMATE / LEGITIMATE-MODIFIED:** 24 (all fixed in Phase 5; 1 — REF-2 — deferred to a follow-up bead with rationale).
- **CLEARED / no-finding:** 7 (no action; SF-11 routes OQ-2 owner-assignment to integrator).
- **REJECTED:** 1 (REF-1; source-of-truth: EC-1 quotes only the goal-agnostic clause).
- **Role 4 deploy_verdict was BLOCK** driven by SF-02/SF-06/SF-08 (composed H2). These are *design-doc specification* gaps (the spec could be synthesized into an unsafe profile), not runtime behaviors — Phase 5 fixes the spec so a faithful synthesis is safe; the deployed agent.md will then be re-gated by Role 4 at its own deploy time (the BLOCK is on the spec's synthesizability, resolved by the fixes).
- **Phase-5 re-verification:** after applying fixes, re-run the structural §7 self-attest checklist + `scripts/audit-specialist-profile.sh` self-check is N/A at design-doc stage (no agent.md yet) — the agent.md audit runs at `/upgrade-agent`. A mechanical fix is not a verdict (Role 1 §5 rule 8): the fixes are recorded in Appendix A and the resulting agent.md is gated downstream.
