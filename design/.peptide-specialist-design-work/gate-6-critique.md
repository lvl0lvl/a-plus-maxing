---
title: "Phase-6 Critique — Peptide-Specialist Domain-Research Synthesis"
gate: phase-6-critique
iteration: 2
target: domain-research.md
mode: deep
reviewer: phase-6-critique-agent
generated: 2026-05-29
---

## Verdict

verdict: PASS

Iteration 2 (post Phase-7 REFINE) clears all three iteration-1 required fixes and the minor Tailor Made widening. The two MAJOR defects that blocked iteration 1 — the H-class enum misstatement and the unlabeled H-class inference — are resolved, and the contract-provenance / fabrication-shaped-DOI gap on the 81.8% figure is handled correctly with an explicit footnote and re-verification deferral. No critical or major defects remain. The iteration-1 affirmatively-checked non-defects (dedup arithmetic 47−4−4=39, single-lab balance framing, all-15-Recommendations-grounded, downstream design-doc coverage) were not touched by the REFINE and still hold.

---

## Per-fix confirmation (iteration 2)

### Fix 1 (Gap 1a) — H-class labelled SYNTHESIS INFERENCE + runtime-emission framing — **CONFIRMED-FIXED**
domain-research.md:186 now reads: *"The per-compound worst-case H-class is a SYNTHESIS INFERENCE here (not a type-tagged source number) — reasoning from Findings 10–11 against the inherited H1–H8 scheme — and the binding value is the specialist's RUNTIME EMISSION (per health-implementer-design.md:131), not a figure this research fixes."* The assertive "→" derivation and the verb "reach" from iteration 1 are gone, replaced with "would be reasoned to." The inference is now admissibly labelled, and the runtime-emission framing matches `health-implementer-design.md:131` ("per-compound H-class is the specialist's runtime emission"). Self-check line 315 records the same.

### Fix 2 (Gap 1b) — enum misstatement removed; GH/metabolic at H7 with matching definition — **CONFIRMED-FIXED**
The string now reads: *"GH/metabolic peptides …, absent established hospitalization-grade decompensation, would be reasoned to at least H7 (an important medical event)."* The H7 *label* is now paired with the H7 *definition* ("important medical event"), per the canonical ICH-E2A/FDA-3500A enum in `health-specialist-architect-design.md:128`. The iteration-1 cross-pairing "important-medical-event/H4-class" is eliminated — verified by the synthesis's own post-edit grep (line 321: `H4-class` / `important-medical-event/H4` → NO HITS), which I independently confirmed: `rg 'H4-class|important-medical-event/H4'` returns nothing in the body. The "absent established hospitalization-grade decompensation" clause correctly reserves H4 (hospitalization) for the higher-severity case without mislabeling it.

### Fix 3 (Secondary) — angiogenic re-anchored at ≥H3 with the H2 worked example cited — **CONFIRMED-FIXED**
domain-research.md:186: *"angiogenic peptides (BPC-157/TB-500) … so worst-case-reachable would be reasoned to at least permanent-harm (H3), and the inherited contract's own worked example (health-implementer-design.md:535) reasons BPC-157 as high as H2 (life-threatening) under worst-case-reachable analysis — a downstream author must not under-anchor below that."* The contract's H2 worked example is now cited by exact locator, and the document explicitly warns against under-anchoring below it. This addresses the iteration-1 secondary note in full.

### Fix 4 (Gap 2) — 81.8% marked contract-inherited; bare slug dropped; DOI footnoted; mandate decoupled from the percentage — **CONFIRMED-FIXED**
domain-research.md:184 now: AUTHORITY_FRAMING_BYPASS is framed as *"mandatory for every specialist BY CONTRACT … independent of any specific jailbreak-prevalence figure"*; the 81.8% is a *"CONTRACT-INHERITED claim … carried from the refusal-taxonomy contract, NOT independently corpus-verified here,"* and *"its upstream source is flagged for re-verification (the cited medRxiv DOI prefix `10.64898/` is anomalous … flagged fabrication-shaped by Role 4's verifier per CONTINUATION_BRIEF.md:357; Pass-3 must re-verify the slug before treating it as load-bearing)."* The mandate is explicitly decoupled: *"stands on the contract regardless of the exact (unverified-at-source) percentage."* The bare slug `2026.02.26.26347212` is dropped from the live citation (confirmed: `rg '2026.02.26.26347212'` → no hits in the body); `10.64898/` survives only inside the fabrication-shaped footnote at lines 184 and 310, which is correct disposition. Self-check line 310 carries the matching provenance statement.

### Fix 5 (Minor) — Tailor Made `[corpus-unverifiable]` widened to cover guilty-plea/escalation — **CONFIRMED-FIXED**
domain-research.md:114 now separates the confirmed primary from the unverified escalation: *"the 2020-04-01 FDA Warning Letter to Tailor Made Compounding (BPC-157 among unapproved substances) is a confirmed FDA primary record `[regulatory]`; the reported subsequent escalation to a criminal guilty plea and ~$1.79M forfeiture is `[corpus-unverifiable]` (the guilty-plea/escalation claim, the forfeiture figure, and the docket all rest on secondary legal reporting, not a retrieved primary court/DOJ document …)."* The qualifier now explicitly covers the guilty-plea/escalation claim, not only the dollar figure and docket — exactly the iteration-1 minor ask.

---

## Residual / carried-forward checks

- **Dedup arithmetic (iteration-1 ADJUDICATED-OK):** untouched by the REFINE; 13 + 21 (incl. 5a) + 13 = 47 raw, −4 disjoint cross-section dupes, −4 disjoint held-out convention sources = 39 numbered. Still honest.
- **Single-lab balance, Recommendation grounding, downstream coverage (iteration-1 non-defects):** untouched; still hold.
- **No new numbers introduced (REFINE invariant):** confirmed — the edits relabel and re-anchor existing claims; no new numeral was added. The synthesis's own post-edit grep audit (lines 319–323) is consistent with my independent re-run.

## Minor notes (non-blocking, PASS stands)

1. **[MINOR]** Finding 12's H7 anchor for GH/metabolic now correctly carries the inference label (Fix 1 covers it), so the iteration-1 minor finding #1 (the insulin-sensitivity→worst-case leap needing an inference marker) is subsumed and resolved.
2. **[MINOR]** The `10.64898/` DOI appears twice (Finding 12 body + Self-check), both inside the fabrication-shaped footnote framing. Acceptable — it is flagged-for-removal context, not a live citation. If Pass-3 re-verification fails, both instances should be struck together; noting for the Pass-3 hand-off, not blocking here.

No critical or major defects remain. Verdict: PASS.
