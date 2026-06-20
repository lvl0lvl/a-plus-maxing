# Gate 4.75 — Citation Integrity Verification
**Biomarker:** eGFR / Creatinine
**Mode:** standard
**Sections reviewed:** section-A.md, section-B.md, section-C.md, section-D.md
**Date:** 2026-06-20
**Iterations:** 1

---

## IC-1 Type-Tag Presence

Scanned all inline citations across four sections for tags not in the canonical 12-enum.

**Findings:**

All inline tags present are from the valid enum (mechanism_review, cohort, regulatory, meta_analysis). No invalid tags (e.g., `guideline`, `primary`) found.

One tag-label discrepancy noted (WARN, not HALT — tag is valid enum member, and IC-1 only requires enum membership):
- **Section B, line 5:** `[1, regulatory]` — bib entry [1] (Levey 2006 MDRD, Ann Intern Med) is declared `cohort` in the bibliography; the inline citation tags it `regulatory` when grounding the IDMS standardization requirement. The inline tag is a valid enum member, but it diverges from the bib-declared type. The actual paper is a cohort derivation, not a regulatory document; the IDMS standardization claim would be better grounded by the NKDEP program document (Section C [5]) or KDIGO guideline.

One non-standard multi-citation format (WARN):
- **Section B, line 109:** `[2, 3, cohort]` — multi-citation with single shared tag. Technically non-standard; both refs [2] and [3] are legitimately `cohort` in the bib, so content is correct. Format is benign.

**Verdict: PASS** (with warnings logged above)

---

## IC-2 Bibliography Type-Tag Presence

Checked every bibliography entry in all four sections for `— tag: <type> — tier:` suffix.

**Section A (9 entries):** All carry `— tag: <type> — tier:` suffix. ✓
**Section B (5 entries):** All carry `— tag: <type> — tier:` suffix. ✓
**Section C (9 entries):** All carry `— tag: <type> — tier:` suffix. ✓
**Section D (7 entries):** All carry `— tag: <type> — tier:` suffix. ✓

Total bib entries: 30. All tagged. No untagged entries.

**Verdict: PASS**

---

## IC-3 Vendor-Not-Numerical

No citations with tag `vendor_label` appear in any section.

**Verdict: PASS** (vacuous)

---

## IC-4 Anecdote-Not-Numerical

No citations with tag `anecdote_aggregate` appear in any section.

**Verdict: PASS** (vacuous)

---

## IC-5 Practitioner-Protocol-Not-Efficacy

No citations with tag `practitioner_protocol` appear in any section.

**Verdict: PASS** (vacuous)

---

## IC-6 Compounding-Data-Sheet-with-Efficacy

No citations with tag `compounding_data_sheet` appear in any section.

**Verdict: PASS** (vacuous)

---

## IC-7 Population-Mismatch

No citations with tag `animal` or `in_vitro` appear in any inline citation across all four sections. The report covers human methodology, epidemiology, and clinical guidelines; no animal or in-vitro evidence is cited.

**Checked citations:** 0 animal/in_vitro citations.
**Flagged citations:** 0.

**Verdict: PASS** (vacuous)

---

## IC-8 Route-Extrapolation

No dose claims with route specifications are present in any section. This report covers biomarker physiology, estimating-equation methodology, and clinical significance — not therapeutic dosing. No route-extrapolation check required.

**Verdict: PASS** (vacuous)

---

## IC-9 Concentration-Surfacing

Concentration audit computed from all distinct primary citations (rct / meta_analysis / cohort / open_label / animal / in_vitro) across all sections, deduplicated:

**Distinct primaries enumerated (12 total):**
1. Nair 2014 (Diabetes Care) — cohort — Wilding group, Liverpool
2. Kannapiran 2010 (Indian J Clin Biochem) — cohort — India
3. Murty 2013 (Indian J Nephrol) — cohort — India
4. Zhang 2020 (BMC Nephrol) — cohort — Hsu/Rule/Lieske group, UCSF/Mayo
5. Levey 2006 (Ann Intern Med) — cohort — CKD-EPI Collaboration, Tufts
6. Levey 2009 (Ann Intern Med) — cohort — CKD-EPI Collaboration, Tufts
7. Inker 2021 (NEJM) — cohort — CKD-EPI Collaboration, Tufts/Johns Hopkins
8. Pottel 2022 (Clin Kidney J) — cohort — Pottel group, KU Leuven
9. Nankivell 2021 (eClinicalMedicine) — cohort — Nankivell group, Sydney
10. Groothof 2022 (J Cachexia Sarcopenia Muscle) — cohort — Groothof/Gansevoort, Groningen
11. Matsushita 2010 (Lancet) — meta_analysis — CKD-PC Consortium
12. CKD-PC 2015 (Lancet Diabetes Endocrinol) — meta_analysis — CKD-PC Consortium

**Largest cluster:** CKD-EPI Collaboration / Levey-Inker group (Tufts + collaborating institutions): refs 5, 6, 7 = 3 of 12 = **25%**. CKD-PC Consortium (Matsushita/Coresh group): refs 11, 12 = 2 of 12 = 17%. No cluster exceeds 70% threshold.

**Share:** 0.25 (25%). Threshold not triggered.

**Verdict: PASS**

---

## IC-10 No Fabricated Citations

**Inline orphan check:** All inline [N] references resolve to a bibliography entry in the same section. No orphaned inline citations found. No bib entries are missing inline references.

**PMID verification (WebFetch-confirmed):**
- PMID 34554658 (Inker 2021) — confirmed: N Engl J Med 2021, Inker LA et al., CKD-EPI Collaboration ✓
- PMID 20483451 (Matsushita 2010) — confirmed: Lancet 2010, Matsushita K et al., CKD-PC ✓
- PMID 21966109 (Kannapiran 2010) — confirmed: Indian J Clin Biochem, 11.6% finding ✓
- PMID 37222019 (Okamura 2023) — confirmed: J Cachexia Sarcopenia Muscle, HR 1.98, N=428,320 ✓
- PMID 35596604 (Groothof 2022) — confirmed: J Cachexia Sarcopenia Muscle, PREVEND N=8,076, 18.5%/15.2% ✓
- PMID 33437955 (Nankivell 2021) — confirmed: eClinicalMedicine, N=137, −5.9 ± 1.4 mL/min per 10 kg ✓
- PMID 24062331 (Nair 2014) — confirmed: Diabetes Care, cooked meat / 12h fasting ✓
- PMID 19414839 (Levey 2009) — confirmed: Ann Intern Med, 8,254 participants, P30 84.1%/80.6% ✓
- PMID 16908915 (Levey 2006) — confirmed: Ann Intern Med, MDRD standardized creatinine ✓
- PMID 27683410 (Rácz 2012) — confirmed: EJIFCC 2012, pitfalls in GFR measurement ✓
- PMID 36777447 (Thompson 2022) — confirmed: Curr Opin Toxicol, endogenous markers / filtration-secretion-reabsorption ✓
- PMID 23814415 (Murty 2013) — confirmed: Indian J Nephrol, cystatin C / AKI ✓
- Section C [8] Lepist 2014 (PMID 24646860, DOI 10.1038/ki.2014.66) — confirmed: Kidney Int, OAT2/creatinine/cobicistat ✓

**Host whitelist check (all 30 bib entries):**

All hosts confirmed whitelisted EXCEPT one borderline entry:

- **Section A, bib [8]** — Murty MSN et al., *Indian J Nephrol* (Medknow / Wolters Kluwer). The journal is published by Medknow Publications (now part of Wolters Kluwer LWW portfolio; available via journals.lww.com). `journals.lww.com` / `lww.com` is whitelisted as of 2026-06-20. This entry is considered within whitelist scope under the LWW umbrella. WARN only — the journal is peer-reviewed and PMC-indexed (PMID 23814415 resolves correctly). This source grounds a mechanistic statement about cystatin C as a filtration marker (not a numerical efficacy claim), reducing risk.

No off-whitelist hosts surviving from prior rounds (Adv Pharm Bull and non-whitelisted ejifcc are confirmed gone; ejifcc.org is now whitelisted; all bib entries checked).

**Verdict: PASS** (with WARN on Indian J Nephrol / LWW borderline host, logged in warnings)

---

## IC-11 No Placeholder Strings

Grepped all four sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No matches found in any section.

**Verdict: PASS**

---

## IC-12 No Wikipedia Citations

No `en.wikipedia.org` or any other `*.wikipedia.org` URLs in any bibliography entry across all four sections.

**Verdict: PASS**

---

## IC-13 Per-Citation Corpus Scoping (standard mode: ≥50% sample, minimum 10)

WebFetch retrieval performed for 12 of the highest-stakes numerical/specific claims. All abstract-level or full-text verified.

| # | Claim | Source | Verification | Result |
|---|-------|--------|--------------|--------|
| 1 | P30 creatinine 2021: Black 87.2%, Non-Black 86.5% | Inker 2021, PMID 34554658 | PubMed abstract + author list confirmed (Inker, Eneanya, Coresh et al.) | PASS |
| 2 | Combined cr-cysC P30 ≥90.5% across groups | Inker 2021, PMID 34554658 | PubMed abstract confirmed | PASS |
| 3 | ACR stratum N=105,872, 730,577 person-years; dipstick N=1,128,310, 4,732,110 person-years | Matsushita 2010, PMID 20483451 | PubMed abstract exact match ✓ | PASS |
| 4 | HRs: eGFR60→1.18(1.05-1.32); 45→1.57(1.39-1.78); 15→3.14(2.39-4.13) vs. eGFR 95 | Matsushita 2010, PMID 20483451 | PubMed abstract exact match ✓ | PASS |
| 5 | 11.6% of patients had normal SCr but eGFR <60 mL/min/1.73m² | Kannapiran 2010, PMID 21966109 | PubMed abstract: "SCr misrepresented 11.6% patients with impaired kidney function" ✓ | PASS |
| 6 | HR 1.98 (95% CI 1.45–2.70) for sarcopenic CKD → ESRD; N=428,320 | Okamura 2023, PMID 37222019 | PubMed abstract: exact figures confirmed ✓ | PASS |
| 7 | 18.5% men, 15.2% women misclassified; PREVEND N=8,076; 24.7 mL/min disagreement | Groothof 2022, PMID 35596604 | PubMed abstract: exact percentages, N=8,076, 24.7 mL/min confirmed ✓ | PASS |
| 8 | eGFR error −5.9 ± 1.4 mL/min per 10 kg lean mass; specificity 47.4%; PPV 54.5%; N=137 | Nankivell 2021, PMID 33437955 | PubMed abstract: all figures confirmed ✓ | PASS |
| 9 | Cooked meat raises SCr → CKD stage misclassification; resolves after 12h fasting | Nair 2014, PMID 24062331 | PubMed abstract confirmed (6/16 CKD 3a misclassified as 3b; 12h fasting reversal) ✓ | PASS |
| 10 | CKD-EPI 2009: 8,254 participants from 10 studies; P30 84.1% vs. MDRD 80.6%; bias 2.5 vs. 5.5 | Levey 2009, PMID 19414839 | PubMed abstract: exact figures confirmed ✓ | PASS |
| 11 | Rácz 2012, EJIFCC — pitfalls in GFR measurement | PMID 27683410 | PubMed: Rácz O, Lepej J, Fodor B et al., EJIFCC 2012 ✓ | PASS |
| 12 | Thompson 2022 — endogenous markers covering filtration/secretion/reabsorption | PMID 36777447 | PubMed abstract: exact scope confirmed ✓ | PASS |

**Claims checked:** 12
**Claims failed:** 0
**Paywalled (abstract-only):** Inker 2021 P30 figures are abstract-level only; stated in abstract ✓. Nankivell 2021 figures confirmed in abstract.

**Verdict: PASS**

---

## Verdict

verdict: PASS

**Summary:** All 13 IC checks PASS. No off-whitelist hosts grounding numerical claims. No fabricated, placeholder, or Wikipedia citations. No animal/in_vitro population-mismatch or route-extrapolation issues. Concentration audit: largest cluster (CKD-EPI Collaboration) = 25% — well below the 70% threshold. 12 of 12 highest-stakes numerical claims WebFetch-verified against source corpora with 0 failures.

Two WARN-level items (not HALT): (1) Section B line 5 uses `[1, regulatory]` where bib [1] (Levey 2006) is declared `cohort` — inline tag is a valid enum member but diverges from bib tag; the IDMS standardization claim could be more precisely grounded by a regulatory source (the NKDEP document in Section C [5]). (2) Section A bib [8] (Murty 2013, Indian J Nephrol / Medknow / LWW) is borderline whitelisted under the `journals.lww.com` umbrella; peer-reviewed, PMC-indexed, and grounds a mechanistic (not numerical efficacy) claim only.

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"WARN"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":12,"largest_cluster_count":3,"share":0.25,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":12,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-1: Section B line 5 uses [1, regulatory] but bib entry [1] (Levey 2006 MDRD cohort study) is declared tag:cohort — inline tag is valid enum member but diverges from bib-declared type; IDMS standardization claim would be more precisely grounded by a regulatory source","IC-10: Section A bib [8] Murty 2013 (Indian J Nephrol, Medknow/LWW) borderline whitelisted under journals.lww.com umbrella — peer-reviewed, PMC-indexed, grounds mechanistic claim only (not numerical efficacy)"],"iterations":1}
```
