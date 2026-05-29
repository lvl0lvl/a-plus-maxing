# Section B — Peptide regulatory status, legality & sourcing

Scope: canonical, goal-agnostic regulatory/legal/sourcing knowledge for a `peptide-specialist` LLM medical sub-agent. Regulatory state reported as of the most recent primary/secondary sources retrievable in May 2026. Where a 2024–2026 regulatory date or status could not be confirmed against a primary regulatory document (FDA.gov, Federal Register, WADA, TGA, Health Canada) it is flagged `[corpus-unverifiable]` rather than asserted.

---

### Finding B-1 — The US compounding pathway has three layers, and "compoundable" is not "approved"

Claim: Peptides reach US patients through three distinct legal routes — (a) FDA-approved peptide drugs (a small set, e.g. semaglutide, tirzepatide, teriparatide), (b) compounding under FD&C Act §503A (traditional patient-specific pharmacies) and §503B (registered outsourcing facilities), and (c) the gray "research-use-only" channel — and none of (b) or (c) constitutes FDA approval of the substance.

Evidence:
- §503A permits patient-specific compounding from bulk drug substances only if the substance is the subject of an applicable USP monograph, is a component of an FDA-approved drug, or appears on the FDA §503A bulks list; §503B governs outsourcing facilities that may compound without patient-specific prescriptions but face the parallel §503B bulks-list constraint. `[regulatory]` (FDA, "Bulk Drug Substances Used in Compounding Under Section 503A of the FD&C Act," fda.gov, accessed 2026-05).
- Compounded medications are not FDA-approved; FDA does not verify their safety, efficacy, or quality before marketing. `[regulatory]` (FDA, "Interim Policy on Compounding Using Bulk Drug Substances," FDA media #174456 / Federal Register 2024-31546, final interim guidance effective 2025-01-07).
- Patient-specific compounding (incl. compounded GLP-1 access via cash-pay clinics) is governed by §503A and remains outside FDA approval of the compounded product. `[regulatory]` (FDA, "Bulk Drug Substances Used in Compounding Under Section 503A of the FD&C Act," fda.gov, accessed 2026-05; FR 2024-31546 interim policy). The specific cash-pay pricing band (~$200–$500/month vs. >$1,000 brand) is a market-reporting figure not confirmed against an issuing-body primary. `[corpus-unverifiable]`

Agent-design implication: The peptide-specialist must never conflate "available from a compounding pharmacy" or "purchasable as RUO" with "FDA-approved" or "safe." It may describe the three pathways as goal-agnostic library knowledge. For any non-approved peptide it must flag the non-approved status explicitly and must not present compounding or RUO availability as evidence of safety or efficacy.

---

### Finding B-2 — Category 1/2/3 is a retired prospective framework, but legacy list placements (incl. BPC-157 Category 2) persisted until 2026 list action

Claim: Under the FDA interim bulks policy, Category 1 = nominated with sufficient information and not appearing to present a significant safety risk (eligible for enforcement-discretion compounding); Category 2 = nominated with sufficient information but raising significant safety concerns, NOT eligible, and not compoundable absent a final rule (§503A) / final Federal Register notice (§503B); Category 3 = insufficient information to evaluate — and the January 2025 final interim guidance retired the prospective Category 1/2/3 nomenclature for newly nominated substances, while existing list placements (including BPC-157's Category 2 placement, reported as September 2023 by secondary sources) remained in force until the April 2026 removal action.

Evidence:
- Category definitions as above. `[regulatory]` (FDA, "Certain Bulk Drug Substances for Use in Compounding that May Present Significant Safety Risks" + "Bulk Drug Substances Used in Compounding Under Section 503A," fda.gov, accessed 2026-05). Category 2 explicitly: substances that "raise significant safety concerns" and "cannot be used in compounding unless FDA publishes a final rule … or final Federal Register notice authorizing the particular substance's use." `[regulatory]`
- Effective 2025-01-07, FDA's final interim guidance stopped categorizing newly nominated bulk substances into Categories 1/2/3 going forward. `[regulatory]` (Federal Register 2024-31546, "Interim Policy on Compounding Using Bulk Drug Substances Under Section 503A," published 2025-01-07).
- BPC-157 was a Category-2 bulk substance with FDA rationale citing potential immune reactions, manufacturing impurities, and lack of human safety data. `[regulatory]` (FDA bulks list / Category 2 page, fda.gov; corroborated by USADA, usada.org, and DoD OPSS, opss.org). The specific placement date ("September 2023") is reported consistently across secondary sources (USADA; Loti Labs; BSCG) but the FDA Category-2 page did not retrieve directly this session, so the exact 2023 placement year is not confirmed against the issuing-body primary. `[corpus-unverifiable]` for the specific year; the fact of Category-2 placement is corroborated.

Agent-design implication: The agent may explain category semantics as library knowledge but must state precisely that Category 2 = "significant safety risks, not compoundable," and that the framework was retired prospectively in 2025 while legacy placements still bound pharmacies. It must not describe a peptide as "Category 1" loosely as if that meant FDA endorsement.

---

### Finding B-3 — The April 2026 removal of 12 peptides from Category 2 is NOT a safety clearance and NOT approval

Claim: In April 2026 HHS/FDA acted to remove 12 peptides from Category 2 and scheduled Pharmacy Compounding Advisory Committee (PCAC) review via Federal Register notice 2026-07361 (published 2026-04-16; the "2026-04-15" HHS-announcement date is secondary-sourced, `[corpus-unverifiable]`); removal from Category 2 does NOT make these substances eligible for §503A compounding, is NOT FDA approval, and is NOT a determination of safety.

Evidence:
- The 12 peptides removed: BPC-157, Cathelicidin LL-37, Dihexa Acetate, Emideltide (DSIP), Epitalon, GHK-Cu (injectable routes), KPV, PEG-MGF (pegylated Mechano Growth Factor), Melanotan II, MOTS-c, Semax (heptapeptide), Thymosin Beta-4 fragment (TB-500). `[regulatory]` (Frier Levitt, "FDA to Remove 12 Popular Peptides from the Category 2 'Do Not Compound' List," frierlevitt.com, 2026, citing FR 2026-07361).
- "Removal from Category 2 does not render these bulk drug substances eligible for compounding under section 503A"; the open question is whether FDA extends enforcement discretion pending rulemaking. `[regulatory]` analysis (Frier Levitt, 2026, quoting/interpreting the FR notice).
- PCAC meeting confirmed for 2026-07-23 and 2026-07-24, FDA White Oak Campus (Bldg. 31, Great Room), under Docket No. FDA-2026-N-2979; the 2026-07-23 session covers BPC-157, KPV, TB-500, and MOTS-c bulk substances (free-base/acetate forms). Comments by 2026-07-09 are provided to the Committee; comments by 2026-07-22 are still considered by FDA. `[regulatory]` (Federal Register, "Pharmacy Compounding Advisory Committee; Notice of Meeting; Establishment of a Public Docket; Request for Comments — Bulk Drug Substances Nominated for Inclusion on the Section 503A Bulk Drug Substances List," FR 2026-07361, published 2026-04-16, federalregister.gov; FDA, "July 23-24, 2026: Meeting of the Pharmacy Compounding Advisory Committee," fda.gov advisory-committee calendar).
- The 2026-07-24 session (DSIP, Semax, Epitalon) and the "before 2027-02-28" tranche for the remaining five (LL-37, Dihexa, GHK-Cu injectable, PEG-MGF, Melanotan II) are reported by secondary legal/trade analysis but the exact per-substance allocation of those later dates was not verified against the FR notice text this session. `[corpus-unverifiable]` for the 2026-07-24 / pre-2027-02-28 per-substance assignments (Frier Levitt 2026; FiercePharma 2026).
- The action originated from a 2026-02-27 HHS (Secretary R.F. Kennedy Jr.) directive to re-evaluate previously restricted peptides; PCAC review ≠ approval, and compounding remains not permitted until FDA formally acts. `[regulatory]` for the PCAC-review-≠-approval principle (FR 2026-07361 framing). The specific 2026-02-27 HHS-directive date is secondary-sourced. `[corpus-unverifiable]` (BSCG, "What's Changing With Peptide Regulation in 2026," bscg.org; STAT, "BPC-157: the peptide with big claims and scant evidence," statnews.com, 2026-02-03).
- FR 2026-07361 is now located on federalregister.gov (published 2026-04-16) confirming the meeting notice, docket, and 12-substance scope; the verbatim enforcement-discretion posture (whether FDA extends interim enforcement discretion pending rulemaking) was not transcribed against the full notice text this session. `[corpus-unverifiable]` for the verbatim enforcement-discretion language; the 12-peptide scope, July 23-24 dates, and "removal ≠ approval" characterization are corroborated by the FR notice plus two independent legal/trade analyses.

Agent-design implication: This is the highest-risk update for the agent. It MUST refuse to characterize the April 2026 removal as "BPC-157 is now legal/approved/safe." It must state: removal from Category 2 ≠ Category 1 placement ≠ enforcement discretion ≠ approval ≠ safety determination; PCAC review is pending (July 2026 onward) and compounding remains not permitted until FDA formally adds a substance to the §503A list. When asked about current status it should flag that the situation is actively evolving and time-stamp its answer.

---

### Finding B-4 — Tailor Made Compounding (2020 Warning Letter → criminal forfeiture) defines the enforcement floor

Claim: FDA's 2020-04-01 Warning Letter to Tailor Made Compounding LLC, which later escalated to a guilty plea for distributing unapproved new drugs (including BPC-157) and ~$1.79M forfeiture, establishes that distributing unapproved peptides for human use carries real civil and criminal enforcement risk — not merely a regulatory gray zone.

Evidence:
- FDA cited the firm for compounding drug products from multiple unapproved substances (BPC-157, Follistatin, GHRP-2, GHRP-6, and others) that failed §503A conditions. `[regulatory]` (FDA, "Tailor Made Compounding LLC — 594743 — 04/01/2020," Warning Letter, fda.gov, dated 2020-04-01).
- The matter escalated to a criminal guilty plea for distributing unapproved new drugs (2018–2020 conduct) with ~$1.79M forfeiture. `[regulatory]` (secondary legal reporting: Holt Law, djholtlaw.com; FDA enforcement context). The exact case caption/court docket was not retrieved against a primary court/DOJ document this session. `[corpus-unverifiable]` for the precise forfeiture figure and docket; the Warning Letter itself is a confirmed FDA primary record.

Agent-design implication: The agent may cite this as the canonical enforcement precedent demonstrating that "for research use only" labeling does not immunize human-use distribution. It must escalate / refuse to assist any request that amounts to sourcing, dosing, or reconstituting a non-approved peptide for human administration, framing such activity as carrying documented enforcement risk.

---

### Finding B-5 — Anti-doping and international status: prohibited or prescription-only across WADA, TGA, Health Canada, EU

Claim: Relevant peptides are broadly prohibited or restricted internationally — BPC-157 sits in WADA S0 (Non-Approved Substances), GH secretagogues and GHRH analogues sit in WADA S2, BPC-157 is TGA Schedule 4 (prescription-only) in Australia, peptides are prescription drugs in Canada with no RUO carve-out for human use, and BPC-157 has no EMA marketing authorization.

Evidence:
- WADA S0 (Non-Approved Substances) = any pharmacological substance not addressed elsewhere on the List "with no current approval by any governmental regulatory health authority for human therapeutic use"; BPC-157 is prohibited at all times under S0, effective 2022-01-01 and continuing on the 2026 List. `[regulatory]` (WADA, "The Prohibited List," wada-ama.org; USADA, "BPC-157: Experimental Peptide Creates Risk for Athletes," usada.org; DoD OPSS, opss.org).
- WADA S2 ("Peptide Hormones, Growth Factors, Related Substances and Mimetics") covers GH secretagogues — ibutamoren (MK-677), anamorelin, capromorelin, ipamorelin, lenomorelin, tabimorelin — GH-releasing peptides (GHRP-1…GHRP-6, alexamorelin, examorelin) and GHRH analogues (e.g., CJC-1295); all prohibited at all times. `[regulatory]` (WADA 2026 Prohibited List as published; mirrored at drugs.com "S2. Peptide Hormones, Growth Factors and Related Substances"; JADCO 2026 Prohibited List PDF). TB-500/thymosin-β4 is prohibited under the growth-factor provisions. `[regulatory]`
- Australia: BPC-157 added to Poisons Standard Schedule 4 (Prescription Only) effective 2024-06-01, per a TGA scheduling delegate interim/final decision; Australia was the first jurisdiction to specifically schedule BPC-157. `[regulatory]` (TGA, "Notice of interim decisions to amend (or not amend) the current Poisons Standard — ACMS-43/ACCS-37/Joint," tga.gov.au, 2024-04). Whether any 2025–2026 amendment altered this Schedule 4 entry was not confirmed against a current Poisons Standard primary text this session. `[corpus-unverifiable]` for any post-2024 change.
- Canada: peptides not authorized by Health Canada (no DIN) cannot legally be sold for human use; "research use only" labeling does not exempt a product from regulatory requirements; Health Canada has issued public warnings against injecting unauthorized peptides. `[regulatory]` (Health Canada / Canada.ca recall-alert "Think twice before injecting peptides bought online"; CBC News reporting on Health Canada warnings).
- EU: BPC-157 has no EMA marketing authorization and has not been reviewed by EMA; member states apply varying national pharmaceutical law. `[regulatory]` (no EMA authorization on record). Specific EU novel-food / national-scheduling status was not confirmed against an EMA or member-state primary document this session. `[corpus-unverifiable]` for granular EU member-state status.

Agent-design implication: For any athlete-context or competition-context user, the agent MUST flag WADA prohibition (S0 for BPC-157; S2 for GH secretagogues/GHRH analogues/GHRPs) and the strict-liability regime, and should escalate/refuse performance-doping guidance. For international users it must state prescription-only (AU) / prescription-drug-only (CA) / no-EMA-authorization (EU) status as goal-agnostic facts rather than implying lawful OTC access.

---

### Finding B-6 — The sourcing reality: RUO/gray-market vendors yield admissible purity/identity data ONLY, never efficacy, against a high counterfeit/contamination base rate

Claim: Research-chemical vendors sell peptides "for research use only, not for human consumption," and the ONLY admissible thing such vendors can provide is analytical purity/identity documentation (HPLC purity, mass-spec identity) used for reconstitution/concentration math and identity confirmation — never efficacy, dosing, or safety claims — and even that documentation sits against a documented base rate of fabricated COAs and contaminated product.

Evidence:
- Legitimate COAs carry batch numbers plus HPLC (purity) and mass-spec (identity) from the same batch; research-grade threshold commonly cited ≥96% HPLC purity, pharma-grade 98–99%+. `[vendor_label]` for any single vendor's stated number; `[corpus-unverifiable]` as a generalized standard (SubQ Protocol "How to Read a Peptide COA"; SeekPeptides; Verified Peptides knowledge-hub). Per type-tag discipline, `vendor_label` may not ground a numerical efficacy/dosing claim — purity percentages are admissible only as identity/purity context, not as efficacy.
- Fabricated COAs are documented: Photoshopped certificates, recycled batch numbers, and references to non-existent testing labs; third-party testing has confirmed low actual purity and contaminants (LPS endotoxin, heavy metals, microbial) in "research-grade" products. `[corpus-unverifiable]` aggregate (PeptideJournal "The Counterfeit Peptide Problem"; PeptideJournal "How to Identify Counterfeit or Degraded Peptides").
- RUO peptides are legally procurable for in-vitro/animal research but are explicitly not FDA-approved for human consumption, diagnosis, treatment, or prevention; legality of procurement does not depend on §503A/§503B status. `[regulatory]` framing (multiple legal-explainer secondary sources; consistent with FDA RUO labeling regime).

Agent-design implication: When a user has obtained or asks about RUO/gray-market product, the agent may (a) help interpret a COA for identity/purity and (b) perform reconstitution/concentration arithmetic ONLY as neutral math — while (c) refusing to endorse human use, (d) refusing to derive efficacy or therapeutic-dose claims from vendor labels or anecdote, and (e) flagging counterfeit/contamination base rates and the "not for human consumption" status. A vendor COA is admissible for purity/reconstitution; it is inadmissible as evidence the compound works or is safe.

---

## Bibliography

1. FDA — "Bulk Drug Substances Used in Compounding Under Section 503A of the FD&C Act," fda.gov (accessed 2026-05). Tier 2 regulatory primary. `[regulatory]`
2. FDA — "Certain Bulk Drug Substances for Use in Compounding that May Present Significant Safety Risks" (Category 2 page), fda.gov (accessed 2026-05). Tier 2 regulatory primary. `[regulatory]`
3. FDA / Federal Register — "Interim Policy on Compounding Using Bulk Drug Substances Under Section 503A," FR 2024-31546 (FDA media #174456), final interim guidance effective 2025-01-07. Tier 2 regulatory primary. `[regulatory]`
4. FDA — Warning Letter, "Tailor Made Compounding LLC — 594743 — 04/01/2020," fda.gov, dated 2020-04-01. Tier 2 regulatory primary. `[regulatory]`
5. Federal Register — "Pharmacy Compounding Advisory Committee; Notice of Meeting; Establishment of a Public Docket; Request for Comments — Bulk Drug Substances Nominated for Inclusion on the Section 503A Bulk Drug Substances List," FR 2026-07361, published 2026-04-16, Docket No. FDA-2026-N-2979, federalregister.gov/documents/2026/04/16/2026-07361. Tier 2 regulatory primary (notice located; verbatim enforcement-discretion text not transcribed this session). `[regulatory]` (source-character descriptor; partial `[corpus-unverifiable]` qualifier for un-transcribed verbatim language)
5a. FDA — "July 23-24, 2026: Meeting of the Pharmacy Compounding Advisory Committee," fda.gov advisory-committee calendar (confirms July 23-24 dates, White Oak venue, 2026-07-23 BPC-157/KPV/TB-500/MOTS-c session). Tier 2 regulatory primary. `[regulatory]`
6. Frier Levitt — "FDA to Remove 12 Popular Peptides from the Category 2 'Do Not Compound' List," frierlevitt.com, 2026. Tier 2.5 curated-with-primaries (law firm analysis citing FR 2026-07361). `[regulatory]`
7. FiercePharma — "Heeding RFK Jr.'s call, FDA reclassifies 12 unapproved peptides ahead of advisory committee meeting," fiercepharma.com, 2026. Tier 2.5 trade press. `[regulatory]`
8. STAT News — "BPC-157: the peptide with big claims and scant evidence," statnews.com, 2026-02-03. Tier 2.5 curated-with-primaries. `[regulatory]` / `[mechanism_review]` context
9. WADA — "The Prohibited List" (2026), wada-ama.org. Tier 2 regulatory primary. `[regulatory]`
10. USADA — "BPC-157: Experimental Peptide Creates Risk for Athletes," usada.org. Tier 2 institutional. `[regulatory]`
11. US DoD OPSS — "BPC-157: A prohibited peptide and an unapproved drug found in health and wellness products," opss.org. Tier 2 institutional. `[regulatory]`
12. Drugs.com mirror — "S2. Peptide Hormones, Growth Factors and Related Substances" (WADA S2 list contents). Tier 2.5 mirror of WADA primary. `[regulatory]`
13. JADCO — "2026 Prohibited List" PDF (national mirror of WADA List), jadco.gov.jm, 2026-01. Tier 2 regulatory (national ADO). `[regulatory]`
14. TGA — "Notice of interim decisions to amend (or not amend) the current Poisons Standard — ACMS-43/ACCS-37/Joint ACMS-ACCS-35," tga.gov.au, 2024-04 (BPC-157 → Schedule 4, eff. 2024-06-01). Tier 2 regulatory primary. `[regulatory]`
15. Health Canada / Canada.ca — recall-alert "Think twice before injecting peptides bought online: unauthorized products can seriously harm you," recalls-rappels.canada.ca. Tier 2 regulatory primary. `[regulatory]`
16. CBC News — "Health Canada warns against injecting unauthorized drugs…," cbc.ca. Tier 2.5 reporting on Health Canada action. `[regulatory]`
17. BSCG — "What's Changing With Peptide Regulation in 2026," bscg.org. Tier 2.5 institutional/anti-doping. `[regulatory]`
18. PeptideJournal — "The Counterfeit Peptide Problem: Industry Response" and "How to Identify Counterfeit or Degraded Peptides," peptidejournal.org. Tier 4/5 (purity/quality leads only). `[corpus-unverifiable]` / `[vendor_label]`-adjacent
19. SubQ Protocol — "How to Read a Peptide COA: Complete Verification Guide (2026)," subqprotocol.com. Tier 4 (COA-reading / purity only). `[vendor_label]`
20. SeekPeptides — "Peptide Testing Labs: third-party verification, purity testing" / Verified Peptides knowledge-hub. Tier 4 (purity/identity only). `[vendor_label]`

## Self-check

- Every INLINE factual claim carries exactly one type-tag from the allowed set (`regulatory`, `vendor_label`, `mechanism_review`, `corpus-unverifiable` used; no efficacy/numeric claim is grounded by `vendor_label` or `anecdote_aggregate` — purity percentages are explicitly marked admissible for identity/purity context only, not efficacy). PASS.
- Tag scope note (iter-2 fix #4): Bibliography entries describe each SOURCE'S tier/character and may carry a primary tag plus a qualifier (e.g., entry 5 `[regulatory]` + partial `[corpus-unverifiable]`; entry 8 `[regulatory]`/`[mechanism_review]`; entry 18 `[corpus-unverifiable]`/`[vendor_label]`-adjacent). These dual descriptors apply to source character and are DISTINCT from inline claim type-tags, which carry exactly one tag each. The one-tag-per-claim rule is not violated by multi-qualifier bibliography descriptors. PASS.
- All regulatory claims cite the issuing body + document + date where retrievable (FDA bulks pages, FR 2024-31546, FR 2026-07361 + FDA advisory-committee calendar, FDA Tailor Made Warning Letter 2020-04-01, WADA Prohibited List 2026, TGA ACMS-43 2024, Health Canada recall-alert). PASS.
- Unverifiable items flagged `[corpus-unverifiable]` (iter-2 expanded): (a) verbatim enforcement-discretion language of FR 2026-07361 (notice now located on federalregister.gov, published 2026-04-16, but full text not transcribed); (b) the 2026-07-24 and pre-2027-02-28 per-substance PCAC assignments (secondary-sourced); (c) the 2026-02-27 HHS-directive date (secondary-sourced); (d) BPC-157's specific Category-2 placement year ("September 2023") — fact of placement corroborated, exact year not primary-confirmed; (e) the GLP-1 cash-pay pricing band (~$200–$500 vs >$1,000); (f) precise Tailor Made forfeiture figure (~$1.79M) and court docket; (g) any post-2024 amendment to the Australian BPC-157 Schedule 4 entry; (h) granular EU member-state / novel-food status for BPC-157; (i) generalized HPLC purity thresholds as a standard. The July 23-24 2026 PCAC dates, Docket FDA-2026-N-2979, the 12-peptide scope, and the "removal ≠ approval" characterization ARE now confirmed against FR 2026-07361 + the FDA advisory-committee calendar (iter-2 upgrade from secondary-only).
- Iter-2 fix #2: the unverified FDA title "FDA clarifies policies for compounders as national GLP-1 supply begins to stabilize" was DROPPED from Finding B-1; GLP-1 cash-pay context re-grounded on the §503A primary (bibliography entry 1 / FR 2024-31546) with the pricing band flagged `[corpus-unverifiable]`. No fabricated/uncited title remains.
- Source count: 21 deduplicated entries (added entry 5a, FDA advisory-committee calendar); ≥15 are Tier 2 / Tier 2.5 regulatory/institutional primaries or curated-with-primaries; Tier 4 vendor sources confined to purity/COA/reconstitution context. PASS (≥10 admissible, Tier-2 prioritized).
- Findings: 6 (B-1 through B-6), each with a one-sentence claim, type-tagged evidence, and an Agent-design implication line. PASS.

## Post-fix grep audit

Each iter-2 fix recorded OLD→NEW, then grepped across the whole file; all hits dispositioned.

**Fix 1 (B-3 PCAC dates — citation_fidelity).**
OLD: PCAC dates (2026-07-23 / 2026-07-24 / before 2027-02-28) asserted `[regulatory]` on law-firm + trade-press only.
NEW: July 23-24, 2026 dates + Docket FDA-2026-N-2979 upgraded to `[regulatory]` grounded on FR 2026-07361 (federalregister.gov, published 2026-04-16) + FDA advisory-committee calendar page (new bibliography entry 5a). The 2026-07-24 and pre-2027-02-28 per-substance assignments downgraded to `[corpus-unverifiable]` (secondary-only).
Grep `2026-07-23|2026-07-24|2027-02-28|FDA-2026-N-2979|2026-07361|advisory-committee` → hits at lines 35, 38, 40-43, 95-97, 117, 118, 120. Dispositions: line 40 = primary-grounded confirmed dates; line 41 = secondary dates correctly flagged `[corpus-unverifiable]`; lines 35/42/43 = announcement-date + enforcement-discretion verbatim correctly flagged `[corpus-unverifiable]`; lines 95/96 = primary bibliography entries; line 38/97 = 12-peptide list via Frier Levitt (corroborated by primary scope); lines 117/118/120 = self-check. All resolved.

**Fix 2 (B-1 unverified GLP-1 FDA title — evidence_quality).**
OLD: cited FDA, "FDA clarifies policies for compounders as national GLP-1 supply begins to stabilize," not in bibliography.
NEW: title DROPPED; GLP-1 cash-pay context re-grounded on §503A primary (entry 1 / FR 2024-31546); pricing band flagged `[corpus-unverifiable]`.
Grep `clarifies policies for compounders` → only remaining hit is line 119 (self-check note documenting the removal). Grep `GLP-1|200.*500|cash-pay` → lines 14, 118, 119 only, all either re-grounded text or self-check. The dropped title appears nowhere as a live citation. Resolved.

**Fix 3 (B-2 BPC-157 2023 placement year — citation_fidelity).**
OLD: "BPC-157 was placed in Category 2 in 2023" asserted `[regulatory]` despite FDA page 404.
NEW: fact of Category-2 placement kept (corroborated USADA/OPSS); specific "September 2023" year flagged `[corpus-unverifiable]` at both the claim line (22) and evidence line (27).
Grep `2023|September 2023` → lines 22, 27, 118. Disposition: line 22 = claim line now reads "reported as September 2023 by secondary sources"; line 27 = evidence line flags the year `[corpus-unverifiable]`; line 118 = self-check item (d). No un-caveated 2023 primary-date assertion remains. Resolved.

**Fix 4 (dual-tag bibliography entries — type_tag).**
OLD: entries 5/8/18 carried dual tags with no scope note.
NEW: added Tag scope note (self-check, line 116) clarifying bibliography descriptors carry source-character qualifiers DISTINCT from the one-tag-per-inline-claim rule.
Grep `mechanism_review|vendor_label.*adjacent|partial .corpus-unverifiable|Tag scope note` → lines 95 (entry 5 qualifier), 99 (entry 8), 109 (entry 18), 116 (scope note). All dual descriptors are bibliography-only; no inline claim carries two tags. Resolved.
