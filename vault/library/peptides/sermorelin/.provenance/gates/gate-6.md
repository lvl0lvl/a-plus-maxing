# Gate 6 — CRITIQUE (red-team) — Sermorelin research-report.md

Adversarial review by `critique-serm-i1` (did not author the draft). Reviewed the full 529-line synthesis against section files A–F.

## 1. Pediatric-vs-adult demarcation (the #1 axis)

**PASS — exemplary.** The pediatric-GHD + diagnostic vs adult off-label/biomarker seam is carried pervasively and never blurs:
- The "Read this first" box, TL;DR, §2 header ("Population integrity (carry throughout)"), §3 header ("Demarcation up front"), §7.1, §9, and the closing integrity invariants all repeat the seam.
- Every pediatric efficacy figure (Thorner 4.1→8.0→7.2 cm/yr; 74% good response) is explicitly tagged "(Pediatric GHD.)" and §2.5 affirms "No source in this section supports adult anti-aging, body-composition, or longevity efficacy."
- "Raises GH/IGF-1" is repeatedly labeled a **biomarker, not a demonstrated clinical benefit** (§3 header, §3.3, §3.4, §9). Nowhere does pediatric efficacy or biomarker change read as proven adult anti-aging benefit.
- Bonus rigor: Kirk 1994 is flagged as idiopathic-short-stature, NOT GHD, in three places — a demarcation the prompt did not even require.

No defect.

## 2. Tesamorelin / CJC / GHRH-1,44 non-miscredit

**PASS.** Faithful to section C lines 19–21. Baker 2012 (§3.2, §9, biblio [19]) is explicitly tesamorelin, "Do not credit to sermorelin." Friedman 2013 carried as a tesamorelin mis-credit guard. The walking-30m / stair-climb / visceral-fat results are correctly attributed to recombinant **GHRH-1,44-amide** (full-length), not sermorelin. §3.1 also flags the common vendor mis-attribution of "Vittone 1997 body comp" (the actual paper found no DEXA change). §4.4 makes the load-bearing point that miscrediting tesamorelin/GHRH-1,44 would spuriously inflate the single-lineage flag. §1.2 cleanly separates tesamorelin (1-44, N-acylated) from the GRF(1-29) family. No miscredit anywhere.

## 3. "Withdrawn ≠ unsafe"

**PASS.** Stated as a COMMERCIAL withdrawal anchored to the primary FR 2013-04827 ("Were Not Withdrawn From Sale for Reasons of Safety or Effectiveness"), in §2.2, §6.1, §9, and the integrity invariants. The report explicitly rebuts both lay errors: "FDA-approved" (no marketed product) AND "banned/pulled for safety" (§6.5). The 2008-event vs 2013-determination dating distinction is called out so the two are not conflated. Faithful to section E lines 10–12 and section B line 67.

## 4. Regulatory accuracy

**PASS.** All specifics check against section E:
- Geref Diagnostic NDA 19-863, approved Dec 28 1990 (diagnostic); Geref NDA 20-443, approved Sep 26 1997 (pediatric idiopathic-GHD). Correct.
- §503A: compoundable via the **component-of-an-approved-drug** pathway (§503A(b)(1)(A)(i)), correctly presented as the primary-anchored, load-bearing basis; the secondary "Category 1" claim is honestly hedged as not-primary-confirmable and explicitly NOT load-bearing (§6.2, §6.6, biblio [26]). Category honestly hedged, not over-claimed.
- Sermorelin **NOT** in the April-2026 action — primary-confirmed absent from FR 2026-07361 and absent from the secondary twelve-peptide set (§6.3). Correct.
- FR-2026-07361 is correctly identified as the **PCAC meeting notice** listing the **seven** agenda substances, explicitly NOT the "removal of 12" enumeration (which traces to the secondary Orrick/Lexology coverage). The 7-vs-12 split is hedged exactly as the corpus supports.
- WADA **S2.2.4** named, sermorelin named by name, prohibited at all times. Correct.

## 5. Citation integrity

**PASS.** Verified mechanically:
- Body (lines 24–382) cites unified tokens 1–5, 7–36. Bibliography defines 1–5, 7–36 plus the shared [3]/[23] entry. Every inline token resolves to a bibliography entry — **no dangling inline [n].**
- **[6] is confirmed absent from the body** (grep for `[6,` / `[6]` in lines 24–382 returns nothing) — matches the "intentionally vacant housekeeping placeholder" claim. Not a dangling citation.
- **[3]/[23]** correctly disclosed as one underlying paper (Clemmons 2017, PMID 28617838) used in two contexts; flagged in crosswalk and provenance note. Defensible, not a true duplicate-error.
- Crosswalk present and complete (maps all 36 unified entries to source sections + local numbers); dedupe notes present.
- **No Wikipedia citation** anywhere; the "Russian/Chinese Wikipedia excluded" lines are exclusion notes, not citations. Confirmed.
- PMIDs/DOIs/FR-docs carried verbatim from sections (spot-checked Thorner 8772599, Baker 22869065, Corpas 1379256, FR 2013-04827, FR 2026-07361 — all match).

## 6. Tier defensibility

**PASS.** evidence_tier **B** is well-argued in §7.1: real FDA approval history + controlled pediatric-GHD efficacy (clears C) but withdrawn, pediatric-scoped, and adult use only biomarker-level with zero healthy-adult RCTs (below S/A). risk_tier **medium** in §7.2: mechanistically favorable short-term safety (physiologic pulsatile augmentation, dominant AE injection-site, systemic <1%) held above "low" by GH-axis/IGF-1 class risk and the long-term-adult-data vacuum. Both are supported by the body (§2, §3, §5) — no tier inflation.

## 7. Unsupported / corpus-exceeding claims; contradictions

**PASS.** The provenance note credibly asserts corpus-only synthesis; spot-checks confirm no new numbers or citations were introduced. All quantitative AE figures (1-in-6, 3/350, 6.5% hypothyroidism, 4% tesamorelin hypersensitivity, arthralgia 4.6% / edema 3.8% / CTS 1.2%, SIR 0.92, +0.28 mmol/L) trace verbatim to section D. Adult-trial details (Corpas, Vittone, Khorram [Nle27], Vitiello) match section C exactly.

Minor observations (do not block):
- **(minor, balance)** §5.4 lists "Concomitant drugs that affect GH release" under "Contraindications," then immediately characterizes it as "a diagnostic-use caution" — these are interaction cautions, not true contraindications. The text self-corrects but the heading placement slightly overstates. Cosmetic.
- **(minor)** Section C dated the approval withdrawal "~2009"; the report uses "~2008." The report's 2008 framing is actually the more precise/correct reading (2008 discontinuation letters + withdrawal request; FDA later acted), so this is an improvement over the source, not a defect — noted only for completeness.

No contradictions, no corpus-exceeding claims, no objectivity/balance failures.

## Verdict

verdict: PASS

All seven red-team axes pass. The demarcation, non-miscredit, withdrawal-framing, and regulatory hedging are handled with above-required rigor. Citation integrity is mechanically clean (no dangling inline tokens, no Wikipedia, crosswalk complete, [6] genuinely unused, [3]/[23] honestly disclosed). Only two cosmetic minors, neither blocking.

```json
{"phase":"6","critique_agent_id":"critique-serm-i1","draft_path":"vault/library/peptides/sermorelin/research-report.md","findings":[{"category":"balance-issue","severity":"minor","description":"§5.4 lists 'Concomitant drugs that affect GH release' under the Contraindications heading, then immediately reclassifies it as a diagnostic-use/interaction caution; these are interaction cautions, not true contraindications. Self-corrected in body but heading placement slightly overstates."},{"category":"citation-incomplete","severity":"minor","description":"Section C source dated the approval withdrawal '~2009' while the report uses '~2008'; the report's 2008 framing is the more precise reading (2008 discontinuation letters + withdrawal request) and is internally consistent, so this is an improvement over the source rather than an error — flagged only for traceability."}],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
