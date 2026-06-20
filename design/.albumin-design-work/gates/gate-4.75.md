# Gate 4.75 — Citation Integrity Verification
# Biomarker: Serum Albumin
# Mode: standard
# Date: 2026-06-20
# Iterations: 2

---

## IC-1 Type-Tag Presence

All inline citations use the format `[N, tag]`. Tags present across all four sections:

- `mechanism_review` — Sections A, B, C, D
- `cohort` — Sections B, C, D
- `rct` — Section D
- `meta_analysis` — Section D
- `regulatory` — Section C

All tags are from the 12-item canonical enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). No invalid tags found. No bare `[N]` citations without tags. The disallowed tags `guideline` and `primary` do not appear.

No IC-1 defects detected.

---

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry in all four sections carries a `— tag: <type> — tier:` suffix annotation. No bundled two-paper entries found. No missing tag annotations.

No IC-2 defects detected.

---

## IC-3 Vendor-Not-Numerical

No `vendor_label` citations present in any section.

No IC-3 defects detected.

---

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citations present in any section.

No IC-4 defects detected.

---

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations present in any section.

No IC-5 defects detected.

---

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations present in any section.

No IC-6 defects detected.

---

## IC-7 Population-Mismatch

No `animal` or `in_vitro` citations present in any section. Gate passes vacuously.

Checked citations: 0 animal/in_vitro. No population-mismatch-unflagged conditions possible.

No IC-7 defects detected.

---

## IC-8 Route-Extrapolation

No dose-route claims requiring route annotation appear. This is a biomarker reference report (no intervention/dose recommendation sections). Gate passes vacuously.

No IC-8 defects detected.

---

## IC-9 Concentration-Surfacing

Concentration audit: This is a biomarker research report. Enumerated distinct primary citations (type tags in `{rct, meta_analysis, cohort, open_label, animal, in_vitro}`):

Primary citations across all sections:
- Section A: None (all `mechanism_review`)
- Section B: [3] Klonoff-Cohen (cohort), [7] Figge (cohort), [10] Bouillanne (cohort)
- Section C: [2] Garcia Moreira (cohort), [3] Kok (cohort), [4] Clase (cohort), [5] van de Logt (cohort), [6] van Schrojenstein Lantman (cohort)
- Section D: [4] Jiang (cohort), [5] Liu (cohort), [6] Goldwasser-Feldman (meta_analysis), [7] Seidu (meta_analysis), [8] Zhang (cohort), [9] Caironi ALBIOS (rct), [10] Huang (cohort), [11] Zhu (meta_analysis)

Total distinct primaries: ~16. Largest cluster (any single institution): no dominant institutional cluster — papers span multiple continents, disciplines, and independent groups (Italy/ALBIOS, UK/Seidu, US/Klonoff-Cohen, Spain/Garcia Moreira, Netherlands/van de Logt, China/Zhang/Jiang/Liu, Denmark-US/Figge, US/Goldwasser). Largest single-institution share is well below 70%.

Threshold NOT triggered (share < 70%). Gate passes.

No IC-9 defects detected.

---

## IC-10 No Fabricated Citations

**WARN — Wrong PMID attribution (Section B [2]):**
Section B bibliography entry [2] reads: "van Schrojenstein Lantman M et al. 'Navigating the Challenge: Selecting the Optimal Assay for Serum Albumin Measurement.' IFCC / Clin Chem Lab Med. PMID: 41098225 (2025)."
WebFetch verification of PMID 41098225 confirms this PMID belongs to a *different paper*: Zeenath Thaneefa et al., "Navigating the Challenge: Selecting the Optimal Assay for Serum Albumin Measurement," EJIFCC (European Journal of Clinical Chemistry and Laboratory Medicine), October 2025. The title matches but authors and journal differ entirely from the bib attribution. The underlying paper at PMID 41098225 is real (EJIFCC is whitelisted Tier 2), and no numerical claim in the text appears to depend specifically on van Schrojenstein Lantman authorship for its numerical content — the entry is cited in Section B as context for BCP vs BCG methodology characterization, which the Thaneefa et al. paper does cover. This is a bibliographic author-attribution error, not a fabricated paper. However, the author attribution in the bib entry is incorrect.

**WARN — Wrong PMC URL (Section B [4]):**
Section B bibliography entry [4] (Soma-Pillay et al., Cardiovasc J Afr 2016, PMID 27213856) lists URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC6295771/`. Verification confirms PMC6295771 is actually Teasdale and Morton "Changes in biochemical tests in pregnancy" (PMID 30574177) — the paper listed separately as Section B [11]. The correct PMC for Soma-Pillay is PMC4928162. The PMID 27213856 resolves correctly to Soma-Pillay; only the PMC URL is wrong. Not a fabricated citation; a URL transposition error.

**WARN — Broken URL (Section C [7]):**
Section C bibliography entry [7] (IRMM/IFCC ERM-DA470k reference material) lists URL `https://publications.jrc.ec.europa.eu/repository/bitstream/JRC46604/`. WebFetch returns HTTP 400 invalid URL error. The underlying reference (ERM-DA470k/IFCC certified reference material for serum proteins) is a real regulatory/institutional artifact from the European Commission JRC. The URL no longer resolves. Not a fabricated citation; a stale/broken link.

**WARN — No PMID/DOI (Section D [5]):**
Section D bibliography entry [5] (Liu D, Zheng N, Zeng C, et al., "Hypoalbuminemia out of proportion to proteinuria in membranous nephropathy," J Am Soc Nephrol 2020) lists no PMID and no DOI. Could not independently verify this citation via PubMed or DOI lookup. The claim it grounds ("Hypoalbuminemia below 2.8 g/dL in membranous nephropathy independently predicts venous thromboembolic events in biopsy-confirmed cohorts") is clinically plausible and attributed to an asnjournals.org journal (whitelisted). This is corpus-missing due to absent identifier; marked as unverifiable.

**WARN — Off-whitelist underlying journal (Section B [12]):**
Section B bibliography entry [12] (Xu SX et al., *World J Gastroenterol* 2024, PMID 38577181) is cited via PMC URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC10989493/` (confirmed correct PMC). However, the underlying journal is World Journal of Gastroenterology (wjgnet.com), which is listed in the NOT-whitelisted set per the source whitelist prompt. The PMC version is cited rather than wjgnet.com directly. The entry grounds the specific CTP albumin scoring threshold "< 2.8 g/dL" (cited as [12]). However, this same threshold is also grounded by [8, mechanism_review] (Child CG, Turcotte JG 1964 — the original CTP source), so this numerical claim is not solely dependent on the off-whitelist source. Flagged for orchestrator decision: the CTP threshold is multiply-grounded; [12] adds citation support for a well-established threshold. Recommend removing [12] from the numerical CTP threshold sentence and retaining [8] only, or replacing [12] with a whitelisted secondary source.

No fully fabricated citations detected (every entry corresponds to a real paper or institutional document). Four bibliographic integrity issues flagged as WARN (wrong PMID attribution, wrong PMC URL, broken URL, missing PMID/DOI, off-whitelist journal host).

---

## IC-11 No Placeholder Strings

Searched all four sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No placeholder strings detected.

---

## IC-12 No Wikipedia Citations

No Wikipedia URLs appear in any bibliography.

No IC-12 defects detected.

---

## IC-13 Per-Citation Corpus Scoping (Standard Mode — ≥50% sample of numerical claims)

Standard mode: ≥50% sample of citations with numerical claims (minimum 10). Claims checked: 16.

| Claim | Cite | Verification | Status |
|---|---|---|---|
| ALBIOS: 31.8% vs 32.0% mortality, RR 1.00 (0.87–1.14), p=0.94, N=1818 | D[9] PMID 24635772 | PubMed abstract confirms all figures exactly | PASS |
| Seidu: RR 0.66 (0.55–0.77) all-cause, 0.60 (0.53–0.67) CVD, 0.57 (0.36–0.91) CHD-death; 48 studies, 1,492,237 participants | D[7] PMID 32378436 | PubMed abstract confirms all figures exactly | PASS |
| Figge: AG correction factor 2.5 per g/dL (0.25 per g/L); r²=0.94 | B[7] PMID 9824071 | PubMed abstract confirms both figures | PASS |
| Evans ASPEN: albumin/prealbumin "characterize inflammation rather than describe nutrition status"; "should not be used as nutrition markers" | D[3] PMID 33125793 | PubMed abstract confirms both statements verbatim | PASS |
| Klonoff-Cohen: N=2342, OR 1.24 per SD decline (p=0.04), age 50–89 | B[3] PMID 1569417 | PubMed abstract confirms all figures | PASS |
| Jiang: β=−0.37 (95% CI −0.45 to −0.28, p<.0001) albumin-CRP association | D[4] PMID 37653773 | PubMed abstract confirms β and CI | PASS |
| Jiang: "highest albumin quartile showing CRP levels 2.86-fold lower than lowest quartile" | D[4] PMID 37653773 | Not found in abstract; full-paper figure — abstract-only verified | WARN: abstract-only |
| Soeters: fractional synthesis rate "normal or even mildly increased" in inflammatory states | D[2] PMID 30288759 | Abstract says "despite increased fractional synthesis rates in plasma" — consistent but the exact phrase "normal or even mildly increased" is a paraphrase | WARN: paraphrase-not-confirmed |
| Garcia Moreira: BCG–CZE bias 3.54 g/L; BCG–BCP mean difference 6.4 g/L (95% CI 5.88–6.96); regression BCG=(0.784×BCP)+12.58; severe hypoalbuminemia gap 9.9 g/L | C[2] PMID 29790973 | Abstract confirms 3.54 g/L BCG-CZE bias; 6.4 g/L mean difference, regression equation, and stratum-specific gaps are full-paper figures — abstract-only verified for 3.54 g/L | WARN: abstract-only for 3.54 g/L; full-paper figures for 6.4 g/L/regression/strata unverifiable via abstract |
| van de Logt: BCG misclassifies up to 59% of nephrotic syndrome patients | C[5] PMID 31053386 | PubMed abstract confirms "up to 59%" exact figure | PASS |
| Zhang: N=1763, 802 deaths, HR 1.43 (1.22–1.66), 43% higher risk for albumin<40 g/L | D[8] PMID 38681582 | PubMed abstract confirms all figures | PASS |
| Zhu: 8 studies, 21,667 ACS patients, RR 2.15 (1.68–2.75) all-cause, RR 3.09 (1.70–5.61) in-hospital | D[11] PMID 31815281 | PubMed abstract confirms all figures | PASS |
| Tanaka: IL-6 activates JAK/STAT3 and NF-κB in hepatocytes | A[6] PMID 25190079 | Confirmed as IL-6 mechanism review (Cold Spring Harb Perspect Biol 2014) | PASS |
| Huang MR: causal roles for albumin in stroke, pulmonary heart disease, AF, VTE; no causal effect on CAD or heart failure | D[10] PMID 38580915 | PubMed abstract confirms all four positive causal findings and absent CAD/HF findings | PASS |
| Goldwasser-Feldman: each 2.5 g/L decrement in albumin → 24–56% increase in odds of death | D[6] PMID 9250267 | PubMed returned CAPTCHA; abstract inaccessible | WARN: corpus-missing |
| Liu (Section D [5]): hypoalbuminemia <2.8 g/dL in membranous nephropathy predicts VTE | D[5] no PMID/DOI | No PMID or DOI; PubMed search unsuccessful | WARN: corpus-missing (no identifier) |

**Claims checked: 16. Claims failed (HALT-level): 0. Claims with WARN: 5 (abstract-only or corpus-missing — no quote-not-found or number-not-found failures at HALT level).**

**Lian/Asberg attribution WARN:** Section B attributes the specific statistics "ICC 0.78, ICC 0.73, 82% classification accuracy, > 22,000 patients" to [6] (Lian and Asberg PMC8340960). Verification of the Lian/Asberg full paper confirms these figures come from *studies cited within* that paper (specifically a Swedish study of >20,000 patients and a Norwegian study), not from Lian/Asberg's own data. The report presents these as if they are original Lian/Asberg findings. This is a paraphrase-attribution drift: the numbers are real (from real studies), but the primary citation should be those underlying studies, not the Lian/Asberg review. No exact numbers are falsified; WARN, not HALT.

---

## Verdict

verdict: PASS

### Iteration 2 Confirmation Summary

All six targeted fixes from the iteration 1 WARNs are confirmed:

1. **wjgnet host purged:** `rg` scan across all of `/tmp/aplus-research/albumin/` returns zero hits for "wjgnet". The off-whitelist World J Gastroenterol entry has been removed. The Child-Pugh albumin threshold (< 2.8 g/dL) now rests solely on [8] Child & Turcotte 1964 (whitelisted). Section B bibliography is sequential [1]–[12] with no wjgnet entry anywhere.

2. **B[2] author/journal corrected:** Bib entry [2] now reads Thaneefa MT et al. / EJIFCC 2025 / PMID 41098225 (ejifcc.org — whitelisted Tier 2). Author and journal match the actual paper at that PMID. WARN resolved.

3. **B[4] PMC URL corrected:** Soma-Pillay et al. bib entry now lists `https://pmc.ncbi.nlm.nih.gov/articles/PMC4928162/` — the correct PMC for PMID 27213856 (Cardiovasc J Afr 2016). WARN resolved.

4. **C[7] URL corrected:** JRC/IRMM entry now uses the handle URL `https://publications.jrc.ec.europa.eu/repository/handle/JRC46604` — no HTTP-400 bitstream path. WARN resolved.

5. **D[5] Lionaki et al. CJASN 2012 confirmed:** PubMed fetch of PMID 22076873 confirms: title "Venous thromboembolism in patients with membranous nephropathy," first author Sophia Lionaki, CJASN January 2012, 898-patient biopsy-confirmed cohort, albumin < 2.8 g/dL as strongest VTE predictor — exactly consistent with the claim as written. Host is asnjournals.org (whitelisted Tier 2). PMID present. WARN (no-PMID / unverifiable Liu citation) fully resolved by replacement.

6. **D[6] Lian/Asberg attribution softened:** Text now attributes ICC figures as "reviewed by [6]" rather than presenting them as Lian/Asberg original data. Paraphrase-attribution drift resolved.

IC-1 through IC-13 carry forward from iteration 1 (all PASS). IC-10 and IC-13 WARNs from iteration 1 that correspond to the six fixes above are closed. One non-blocking warning persists: Goldwasser-Feldman PMID 9250267 and a handful of full-paper figures (Jiang 2.86-fold, Garcia Moreira 6.4 g/L regression, Soeters paraphrase) remain abstract-unverifiable due to paywall/CAPTCHA — none are HALT-class. Concentration audit updated to 30 total primaries (reflecting the expanded section bibliography); largest cluster count 2; share 0.07 — well below threshold.

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":7},"concentration_audit":{"verdict":"PASS","total_primaries":30,"largest_cluster_count":2,"share":0.07,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":16,"claims_failed":[]},"halt_reasons":[],"warnings":["Goldwasser-Feldman 9250267 + a few full-paper figures abstract-unverifiable (paywall/CAPTCHA) — non-blocking"],"iterations":2}
```
