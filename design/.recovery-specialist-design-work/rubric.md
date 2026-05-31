# Phase 2.5 — RUBRIC (recovery-specialist, mode=standard, judge threshold 92/100)

Each Phase-3 retrieval section is scored by a paired judge against these dimensions (0–100). `risk_floor_readiness` is `null` for this reference/protocol research (no compound entry lands at risk_tier=experimental).

| Dimension | What the judge scores |
|---|---|
| evidence_quality | Are claims grounded in Tier-1/2 primaries (RCT/meta/cohort/consensus) appropriate to the claim type? Hierarchy respected (meta > RCT > cohort > mechanism > animal)? |
| citation_fidelity | Does each inline `[N, tag]` resolve to a real, correctly-attributed source (author/year/PMID/DOI plausible and matching)? No fabricated DOIs/PMIDs, no future-dates, no wrong-attribution. |
| type_tag_discipline | Every inline citation carries exactly one tag from the `_source-whitelist` enum; tag matches study design; `vendor_label`/`anecdote_aggregate` never ground a numeric (dose/effect/n/AE/correlation). |
| population_annotation | Every `animal`/`in_vitro` cite carries `[population-mismatch: <species>]` in the same sentence; no rodent finding presented as human-applicable without the tag. |
| route_fidelity | N/A-leaning for this domain (few dose claims); any modality "dose" (sauna temp/duration, CWI temp/duration, cold exposure) matches the cited protocol; no extrapolation across protocols without flag. |
| concentration_audit_handling | If one lab/group dominates a sub-topic (≥70% of primaries), the section surfaces it explicitly rather than presenting as settled consensus (e.g., a single sauna cohort group). |
| risk_floor_readiness | `null` (no experimental-tier compound). |
| reasoning_integrity | Distinguishes mechanism from outcome; hype-resistant (does NOT overclaim CWI/sauna/compression); separates correlation from causation (esp. HRV/readiness scores and CV-cohort sauna data); flags single-vendor "readiness score" black boxes. |
| completeness_vs_brief | Covers the section's assigned scope (per plan.md) including the boundary pointers and the safety/red-flag content where assigned to the section. |

**Auto-fail (SUB-AGENT level, per CONTINUATION_BRIEF Lesson 2 scoping):** any numerical claim grounded only by `vendor_label`/`anecdote_aggregate`; any fabricated-shape citation (anomalous DOI prefix, future date, fictitious TLD, PubMed slug-not-PMID); section < ~1,500 words; < 8 admissible sources in-section; body↔bibliography asymmetry within the section.

**Health-specific rubric additions (per aplus-research SKILL Phase 2.5):**
- Concentration audit — count distinct primaries by lab/group; flag ≥70% single-group.
- Population annotation — every animal cite carries species + n.
- Route fidelity — no protocol extrapolation without explicit flag.
- Risk-floor readiness — N/A (no experimental compound).

Verdict: PASS iff total ≥ 92 AND findings:[] (empty). Any HALT → re-dispatch that section's retrieval with judge findings injected, max 3 iterations (then HALT judge-non-convergence).
