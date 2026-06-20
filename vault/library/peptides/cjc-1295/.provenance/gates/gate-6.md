# Gate 6 — CRITIQUE (red-team) — CJC-1295 research-report.md

Adversarial review of the Phase-5 synthesis draft against the nine red-team axes. I did not write the draft. I read the full draft (505 lines) and all six corpus sections (A–F) to test faithful representation. Mechanical citation audit run (inline tokens vs bibliography; Wikipedia scan).

---

## 1. Efficacy overstatement (biomarker ≠ clinical benefit)

**Clean — actively well-handled.** The draft does not let GH/IGF-1 elevation read as proven clinical benefit anywhere I could find, and it states the negative repeatedly and prominently:

- The DEFINING-FACT box: "The robust GH (2–10×) and IGF-1 (1.5–3×) rises that are real and durable are **biomarkers, not proven clinical benefit.**" plus "**No CJC-1295 trial of any kind has ever met a body-composition, anti-aging, or wound-healing efficacy endpoint.**"
- TL;DR: "that is a **biomarker** result."
- §3.1 ("What Teichman 2006 does and does not show"), §3.3 (explicit "human efficacy verdict: NONE MET"), §3.4, §3.7 table final row "**Human efficacy endpoint (any indication, either form) … NONE MET**", and §8 reason #2 all reinforce it.
- Commercial "10–15% visceral-fat / lean-mass" claims are named and explicitly rejected as inadmissible (§3.3) — matches section B verbatim.

This is the single most-at-risk axis for this compound and the draft passes it cleanly. No defect.

## 2. DAC vs no-DAC slips

**Clean.** I traced every load-bearing PK/PD/trial/dose number to the correct molecule:

- 5.8–8.1 d half-life, GH 2–10×, IGF-1 1.5–3×, the +7.5× basal GH (Ionescu), the NCT00267527 trial, and the trial death are all attributed to **with-DAC** throughout (§1.4, §2.3, §3, §6). Matches corpus.
- ~30-min half-life is attributed to **no-DAC / Mod GRF 1-29** and is explicitly flagged review/consensus, not a measured human value (§1.5, §6, §4 table). Matches corpus.
- Dosing conventions in §9.1 are correctly partitioned: ~1–2 mg SC once-weekly = DAC only; ~100 mcg daily 1–3× = no-DAC only, with an explicit "never cross-attributed" guard. Matches section F.
- §4 half-life table keeps rat-conjugate (>72 h, Jetté), human (5.8–8.1 d, Teichman), and no-DAC (~30 min, review) in separate rows with separate sources.

No cross-attribution defect detected.

## 3. The "deaths" claim

**Clean — correctly stated as event-partially-verified / causation-unverified.** §6.2 gives the verdict "**PARTIALLY VERIFIED as to the event, but UNVERIFIED / NOT ESTABLISHED as to causation.**" It (a) affirms a real death occurred with a primary news-of-record source (aidsmap/Bernard [9]); (b) states causation was never demonstrated and the attending-physician working assessment pointed to occult coronary disease, not the drug; (c) flags the "eleventh injection" detail as an anecdotal, unconfirmed participant report; (d) explicitly says any rendering that CJC-1295 "has killed people" as established fact is not supported. This faithfully mirrors section D and is neither over- nor under-stated. No defect.

## 4. Regulatory accuracy

**Substantively clean, with one minor internal date-presentation tension (below).** Verified against sections D/E/F:

- Never FDA-approved — stated §7.1, §6.1, §8. Correct.
- NOT among the April-2026 removed-12 — stated §7.2 item 3 and the bottom-line, with the removed-12 enumerated correctly (BPC-157, TB-500, KPV, MOTS-c, DSIP/Emideltide, Semax, Epitalon, GHK-Cu, Melanotan-II, Dihexa, PEG-MGF, LL-37) and CJC-1295 confirmed absent. Correct; matches section E.
- PCAC voted AGAINST on 4 Dec 2024 — stated §7.2 item 2, anchored to FR Doc 2024-24828 + FDA AdCom page. Correct.
- WADA S2.2.4 names it ("CJC-1293, CJC-1295, sermorelin, tesamorelin"), prohibited at all times — §7.3. Correct.
- No "resurrected removed-Sept-2024" claim; Sept **2023** is correctly used as the Category-2 *placement* date (§7.2 item 1), not a removal. Correct.
- "Removal ≠ approval, inclusion ≠ approval" caveat present (§7.2 bottom-line). Correct.
- The "still Cat-2 vs unclassified-gap" divergence is preserved as an honest caveat rather than resolved — appropriate.

MINOR (not blocking): §7.2 item 3 / §7.4 lean on FR Doc 2026-07361 [26] (a primary FR notice that enumerates only the 7 agenda peptides) jointly with the FDA Category-2 page [14] and secondary advisories [20][22] for the 12-removal tally and the "not mentioned in FR Doc" claim. The draft's own "Primary-source note" correctly discloses that the FR notice does not itself print the 12-removal tally and that absence-of-CJC-1295 is a cross-source inference. This is transparently flagged, so it is a disclosed limitation, not a misstatement. No drift on the protected facts.

## 5. Unsupported / corpus-exceeding claims

**Clean.** Spot-checked the load-bearing numbers and animal claims against the corpus:

- All efficacy/PK numbers (2–10× GH, 1.5–3× IGF-1, 5.8–8.1 d, +7.5× basal, ~28 d IGF-1, ~4× rat GH AUC, >72 h rat plasma, 2 µg/dose at 24/48/72 h in mice) trace verbatim to sections A/B/C.
- Every animal claim carries species: Jetté = Sprague-Dawley rat; Alba = GHRHKO mouse; Raun = animal; Rittmaster = rat anterior-pituitary cells in vitro. No species-missing animal claim.
- KIMS class-risk numbers (arthralgia 4.6%/2.6%, edema 3.8%/3.1%, carpal tunnel 1.2%/0.8%, T2DM ~0.4%, cancer SIR 0.92 CI 0.83–1.01) match section D and are correctly framed as borrowed GH-class data, NOT CJC-1295 findings.
- Per-arm n is honestly NOT asserted for Teichman/Ionescu/Jetté/Alba (paywalled); draft says "not stated in abstract." Good discipline.
- The circulating "80% injection-site / 22% flushing" AE percentages are flagged UNVERIFIED and not asserted (§6.1). Matches section D.
- No invented citation: all 31 bibliography entries carry a PMID/DOI/NCT/FR-doc or are explicitly typed as vendor/practice consensus ([30],[31]) or secondary-corroboration ([15],[20],[22]). [15] is a descriptive "secondary clinical reporting" entry with no fabricated identifier — honest rather than fabricated-looking.

No corpus-exceeding claim detected.

## 6. Citation integrity

**Clean (mechanically verified).** Ran token audit:
- Inline tokens used: exactly [1]–[31], every one resolves to a bibliography entry. No dangling [n].
- Every bibliography entry [1]–[31] is cited at least once (no orphan references).
- Crosswalk table present and maps all section-local origins to unified numbers; dedup of Teichman/Jetté/Alba/aidsmap/FDA-503A documented.
- No Wikipedia source anywhere (SportWiki explicitly excluded in §9.4 / section F).
- No duplicate inline [n] collisions (each unified number = one source).

MINOR cosmetic: in the rendered Bibliography the entries are grouped by category ("Safety class-evidence" lists [15][16][17] before "Regulatory" lists [14][18]…), so [14] physically appears after [17]. Numbering is non-contiguous in display order but every number still resolves correctly via the crosswalk. Cosmetic only; does not mislead.

## 7. Concentration audit surfaced first-class

**Clean.** §5 is a dedicated top-level section explicitly labeled "(first-class)" with a rationale ("not buried"). It enumerates denominator = 2 primaries, computes inclusive 2/2 = 100% ConjuChem-touched and strict 1/2 = 50% author-lineage, raises a CONCENTRATION ALERT against the ≥70% threshold, and notes the human layer also traces to ConjuChem (Teichman includes Castaigne; NCT00267527 was ConjuChem-sponsored). This is reproduced faithfully from section C and echoed in §8 reason #3 and the DEFINING-FACT/metadata. The "~100% of the 2 efficacy/PK primaries" framing the gate asks for is present and accurate. No defect.

## 8. evidence_tier C / risk_tier experimental justified by the body

**Clean.** §8 gives five converging, body-grounded reasons for C (no human efficacy of any design; biomarker ≠ outcome; severe evidentiary concentration; terminated trial with a death; no controlled long-term human safety dataset) and states the floor ("what keeps it at C rather than lower"). risk_tier=experimental is justified in the metadata bullet by unapproved status, no long-term safety data, the trial death/halt, days-long irreversibility, non-compoundability, and WADA prohibition — all of which are developed in §6/§7. Tiers are earned by the body, not asserted. No defect.

## 9. Internal contradictions

**None material.** Cross-checked the recurring figures across sections for consistency:
- NCT00267527 enrollment: "120 planned" vs "~192 reported" appears in §3.2, the §3.7 table, and §6.2 — and the discrepancy is explicitly reconciled each time (registry 120 taken as controlled value; 192 from contemporaneous reporting). Consistent, not contradictory.
- Half-life "5.8–8.1 d" (human, with-DAC) vs review "6–8 d" framing: §1 uses the measured Teichman value; the 6–8 d appears only as the review/[13] framing. Not in conflict.
- "Preserved pulsatility" (§2.3) is correctly qualified as pulse-shape-preserved while basal tone rises — not contradicted by the "non-pulsatile chronic exposure" language in §2.4/§6.3, which refers to the days-long flat depot. The draft itself draws this distinction explicitly, so it reads as nuance, not contradiction.
- Started December 2005 (§3.2) matches section B.

No internal contradiction rising to a defect.

---

## Verdict

All nine red-team axes pass. The defining risks for this compound — efficacy overstatement and DAC/no-DAC cross-attribution — are handled with active, repeated, correct discipline. The "deaths" claim, regulatory facts (never-approved, not in the removed-12, PCAC-declined Dec 4 2024, WADA S2.2.4), concentration audit (first-class, ~100%/2 primaries), and tier justifications are all faithful to the corpus. Citation integrity is mechanically sound (31/31 tokens resolve, no orphans, no Wikipedia). Only two MINOR cosmetic/disclosed-limitation findings remain, neither of which would mislead a reader; both are already self-flagged by the draft.

verdict: PASS

```json
{
  "phase": "6",
  "critique_agent_id": "critique-cjc-i1",
  "draft_path": "vault/library/peptides/cjc-1295/research-report.md",
  "findings": [
    {"category": "citation-incomplete", "severity": "minor", "description": "bibliography-display-order: Rendered Bibliography is grouped by category, so [14] (FDA 503A) physically appears after [15][16][17]; display order is non-contiguous. Every inline token [1]-[31] still resolves correctly via the crosswalk and all entries are cited; cosmetic only, not misleading."},
    {"category": "balance-issue", "severity": "minor", "description": "regulatory-removed12-cross-source-inference: The 'CJC-1295 not in the April-2026 removed-12' and the 12-peptide tally rely on FDA Category-2 page [14] + secondary advisories [20][22] jointly with primary FR Doc 2026-07361 [26], because [26] enumerates only the 7 agenda peptides. The draft transparently discloses this in its Primary-source note; protected facts are not drifted. Disclosed limitation, not a misstatement."}
  ],
  "additional_retrievals": [],
  "halt_reasons": [],
  "iterations": 1,
  "verdict": "PASS"
}
```
