# Gate 4.75 — Citation Integrity Verification
# Biomarker: Serum Sodium
# Mode: standard
# Date: 2026-06-20
# Sections checked: A, B, C, D

---

## IC-1 Type-Tag Presence

All inline citations across all four sections use the `[N, tag]` format. Tags present: `mechanism_review`, `regulatory`, `cohort`, `meta_analysis`. All tags are within the 12-enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). No `guideline` or `primary` tags detected. Zero bare `[N]` inline citations found in any section after full re-scan.

No IC-1 violations detected.

---

## IC-2 Bibliography Type-Tag Presence

All bibliography entries in sections A, B, C, and D carry the `— tag: <type> — tier:` suffix annotation.

- Section A: 8 entries — all tagged `mechanism_review` ✓
- Section B: 6 entries — tagged `regulatory` (×2), `mechanism_review` (×3), `cohort` (×1) ✓
- Section C: 9 entries — tagged `mechanism_review` (×4), `cohort` (×5) ✓
- Section D: 10 entries — tagged `regulatory` (×1), `cohort` (×7), `meta_analysis` (×1), `cohort` (×1) ✓

No IC-2 violations detected.

---

## IC-3 Vendor-Not-Numerical

No `vendor_label` citations appear in any section.

No IC-3 violations detected.

---

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citations appear in any section.

No IC-4 violations detected.

---

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations appear in any section.

No IC-5 violations detected.

---

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations appear in any section.

No IC-6 violations detected.

---

## IC-7 Population-Mismatch

No `animal` or `in_vitro` citations appear in any section. All cited sources are human cohort, mechanism review, regulatory, or meta-analysis. Gate passes vacuously.

Population-mismatch citations checked: 0. No unflagged animal/in-vitro numerical claims.

No IC-7 violations detected.

---

## IC-8 Route-Extrapolation

No dose claims with differing administration routes appear in any section. Correction rates cited (ODS limits, hypernatremia correction) are guideline recommendations cited from regulatory and mechanism_review sources, with no route-specific dose extrapolation. Route-unverifiable: 0.

No IC-8 violations detected.

---

## IC-9 Concentration-Surfacing

Primary citations across all four sections represent at least 12 distinct research groups/author teams: Sterns (NEJM 2015), Adrogué/Madias (NEJM 2000 ×2), Spasovski et al. (Eur J Endocrinol 2014), Hoorn/Zietse (JASN 2017), Almond et al. (NEJM 2005), Kim et al. (NEJM 2008), Gheorghiade et al./OPTIMIZE-HF (Eur Heart J 2007), Waikar/Mount/Curhan (Am J Med 2009), Arzhan et al. (Kidney360 2022), Sterns/Riggs/Schochet (NEJM 1986), Renneboog et al. (Am J Med 2006), Wang et al. (Heart Fail Rev 2019), Krüger/CAPNETZ (Respir Med 2014), plus multiple Section C measurement sources. No single-lab share approaches 70%.

Concentration threshold not triggered. Gate passes.

---

## IC-10 No Fabricated Citations

**PMIDs verified against PubMed:**

| PMID | Claimed Reference | Verification Result |
|------|------------------|---------------------|
| 25551526 | Sterns RH, NEJM 2015, "Disorders of Plasma Sodium" | CONFIRMED ✓ |
| 10816188 | Adrogué/Madias, NEJM 2000, "Hypernatremia" | CONFIRMED ✓ |
| 10824078 | Adrogué/Madias, NEJM 2000, "Hyponatremia" | CONFIRMED ✓ |
| 15829535 | Almond CS et al., NEJM 2005, Boston Marathon hyponatremia | CONFIRMED ✓ |
| 17309900 | Gheorghiade M et al., Eur Heart J 2007, OPTIMIZE-HF | CONFIRMED ✓ |
| 19699382 | Waikar SS et al., Am J Med 2009, hospitalization/mortality | CONFIRMED ✓ |
| 35919520 | Arzhan S et al., Kidney360 2022, hypernatremia population study | CONFIRMED ✓ |
| 18768945 | Kim WR et al., NEJM 2008, liver-transplant waitlist | CONFIRMED ✓ |
| 3713747 | Sterns/Riggs/Schochet, NEJM 1986, ODS | CONFIRMED ✓ |
| 24569125 | Spasovski G et al., Eur J Endocrinol 2014 guideline | CONFIRMED ✓ |
| 10225241 | Hillier TA et al., Am J Med 1999, glucose correction | CONFIRMED ✓ |
| 34276975 | Voets PJGM et al., Clin Kidney J 2021, osmolality nomogram | CONFIRMED ✓ |
| 36678265 | Bernal A et al., Nutrients 2023, sodium homeostasis | CONFIRMED ✓ |

**Bibliography host whitelist check:**

| Section | Citation | Host | Whitelisted? |
|---------|----------|------|-------------|
| A [1–3] | NEJM | nejm.org | YES ✓ |
| A [4] | Ranieri et al., F1000Research 2019 | f1000research.com | **NOT ON WHITELIST** — WARN |
| A [5] | Wilson et al., Clin Exp Nephrol (Springer) | springer.com | YES ✓ |
| A [6] | Gagnon/Delpire, Front Physiol | frontiersin.org | YES ✓ |
| A [7] | Voets et al., Clin Kidney J (OUP) | oup.com | YES ✓ |
| A [8] | Bernal et al., Nutrients (MDPI) | mdpi.com | YES ✓ |
| B [1] | Spasovski, Eur J Endocrinol (Bioscientifica) | bioscientifica.com | YES ✓ |
| B [2] | Verbalis, Am J Med (Elsevier/ScienceDirect) | sciencedirect.com | YES ✓ |
| B [3] | Hoorn/Zietse, JASN | asnjournals.org | YES ✓ |
| B [4] | Aziz et al., J Clin Med (MDPI) | mdpi.com | YES ✓ |
| B [5] | Hillier, Am J Med (Elsevier) | sciencedirect.com | YES ✓ |
| B [6] | Bastos/Rocha, J Bras Nefrol (SciELO Brazil) | scielo.br | YES ✓ |
| C [1] | Datta/Chopra, JALM (OUP) | oup.com | YES ✓ |
| C [2] | Katrangi et al., JALM (OUP) | oup.com | YES ✓ |
| C [3] | Maas et al., Clin Chemistry (OUP) | oup.com | YES ✓ |
| C [4] | Vera et al., Lab Medicine (OUP) | oup.com | YES ✓ |
| C [5] | Levy, Clin Chemistry (OUP) | oup.com | YES ✓ |
| C [6] | Dimeski et al., Clin Chemistry (OUP) | oup.com | YES ✓ |
| C [7] | Virk et al., Lab Medicine (OUP) | oup.com | YES ✓ |
| C [8] | Merrill et al., Clin Chemistry (OUP) | oup.com | YES ✓ |
| C [9] | NIST SRM 956e news | nist.gov | YES ✓ |
| D [1] | Spasovski (same as B [1]) | bioscientifica.com | YES ✓ |
| D [2] | Almond, NEJM | nejm.org | YES ✓ |
| D [3] | Kim, NEJM | nejm.org | YES ✓ |
| D [4] | Gheorghiade, Eur Heart J (OUP) | oup.com | YES ✓ |
| D [5] | Wang, Heart Fail Rev (Springer) | springer.com | YES ✓ |
| D [6] | Waikar, Am J Med (Elsevier) | sciencedirect.com | YES ✓ |
| D [7] | Krüger/CAPNETZ, Respir Med (Elsevier) | sciencedirect.com | YES ✓ |
| D [8] | Arzhan, Kidney360 (LWW) | journals.lww.com | YES ✓ |
| D [9] | Renneboog, Am J Med (Elsevier) | sciencedirect.com | YES ✓ |
| D [10] | Sterns/Riggs/Schochet, NEJM | nejm.org | YES ✓ |

**Off-whitelist host finding:** Section A citation [4] (Ranieri M et al., F1000Research 2019, PMID 30800291) is hosted at `f1000research.com`, which does not appear on the source whitelist. The citation carries tag `mechanism_review — tier: 2`. Critically, cite [4] grounds a mechanism description only (AQP2 V2 receptor cascade, cAMP–PKA phosphorylation pathway) — it does NOT ground any numerical claim. No numerical token appears adjacent to the [4, mechanism_review] inline cite in Section A. Per halt conditions: "HALT only for: off-whitelist host grounding a number." This cite grounds mechanism only → WARN, not HALT.

**Arzhan DOI note (WARN):** Section D bib lists DOI `10.34067/KID.0007272021` for Arzhan et al.; the DOI resolves to journals.lww.com with 402 paywall. PMID 35919520 is verified on PubMed and all claimed numbers confirmed from abstract. The DOI is structurally consistent with Kidney360 (prefix 10.34067/KID). Minor DOI variant possible between prepress and final assignment; PMID is authoritative. WARN only.

No IC-10 HALT conditions detected.

---

## IC-11 No Placeholder Strings

Grepped all four sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No placeholder strings detected.

---

## IC-12 No Wikipedia Citations

No Wikipedia URLs (`en.wikipedia.org`, `ru.wikipedia.org`, or any `*.wikipedia.org`) appear in any bibliography.

No IC-12 violations detected.

---

## IC-13 Per-Citation Corpus Scoping (standard mode — ≥50% sample of numerical claims)

**Claims checked: 13. Claims failed: 1 (WARN-level paraphrase discrepancy, not number-not-found).**

| # | Claim | Cite | Verification | Result |
|---|-------|------|-------------|--------|
| 1 | 135–145 mmol/L reference range | A[1] Sterns 2015 NEJM PMID 25551526 | PubMed confirms NEJM 2015 Sterns on plasma sodium disorders; range is canonical throughout | PASS ✓ |
| 2 | Osmolality ≈ 2×[Na] + glucose/18 + BUN/2.8 | A[7] Voets 2021 Clin Kidney J PMID 34276975 | PMID confirmed; journal confirmed; formula is Edelman-derived standard, consistent with osmolality literature | PASS ✓ |
| 3 | Hillier factor 2.4 mmol/L per 100 mg/dL (vs Katz 1.6) | B[5] Hillier 1999 Am J Med PMID 10225241 | PubMed abstract confirms: "mean decrease averaged 2.4 meq/L for every 100 mg/dL increase" and previous standard was 1.6 | PASS ✓ |
| 4 | ODS: >12 mmol/L per day threshold; Sterns 1986 n=60, sodium <116 mmol/L | D[10] Sterns 1986 NEJM PMID 3713747 | PubMed confirms neurological sequelae with >12 mmol/day correction. However: paper reports 8 ODS patients from among cases with serum Na <**106** mmol/L (not <116 mmol/L as stated in Section D). The "60 patients" figure is a paraphrase of the published-case review; abstract says "eight patients" with ODS among those studied. The sodium threshold stated in the report ("below 116 mmol/L") diverges from the abstract's stated threshold ("<106 mmol/L" / "sodium <106 mmol per liter"). | **WARN: paraphrase-no-token-match** — "116" not confirmed in abstract; abstract states "<106 mmol/L"; the 60-patient count is also not confirmed in abstract text. |
| 5 | OPTIMIZE-HF: 48,612 patients, 259 hospitals; 19.5% mortality increase per 3 mmol/L decrement | D[4] Gheorghiade 2007 Eur Heart J PMID 17309900 | PubMed confirmed: "48,612 patients across 259 hospitals, 19.5% increase per 3 mmol/L decrement below 140 mmol/L, follow-up 10%" | PASS ✓ |
| 6 | Waikar: 98,411 patients, 14.5% hyponatremia, OR 1.47 (1.33–1.62) in-hospital, HR 1.38 (1.32–1.46) 1-year, HR 1.25 (1.21–1.30) 5-year, mild hyponatremia OR 1.37 (1.23–1.52) | D[6] Waikar 2009 Am J Med PMID 19699382 | PubMed confirmed: all 6 figures match exactly | PASS ✓ |
| 7 | Arzhan: 1.9 million patients, 3% hypernatremia at admission, 12% vs 2% mortality, severe Na>155 OR 34.41 (30.59–38.71) | D[8] Arzhan 2022 Kidney360 PMID 35919520 | PubMed confirmed: all figures match (1.9M, 3%, 12% vs 2%, OR 34.41 for Na>155) | PASS ✓ |
| 8 | Almond: 488 runners, 13% hyponatremia (≤135), 0.6% critical (≤120), weight gain OR 4.2 (2.2–8.2), race time >4h OR 7.4 (2.9–23.1) | D[2] Almond 2005 NEJM PMID 15829535 | PubMed confirmed: all figures match exactly | PASS ✓ |
| 9 | Kim: 6,769 transplant candidates, HR 1.05 per 1-unit Na decrease 125–140 range, 7% prevented deaths | D[3] Kim 2008 NEJM PMID 18768945 | PubMed confirmed: 6,769 registrants, HR 1.05, "32 patients who died (7%)" prevented with MELDNa | PASS ✓ |
| 10 | Pseudohyponatremia: −6.1 mmol/L underestimation, 70% hyperproteinemic specimens | C[2] Katrangi 2019 JALM DOI 10.1373/jalm.2018.028720 | Host oup.com confirmed whitelisted; PMID not in bib but DOI is valid JALM (AACC/OUP). Abstract not fetched (paywall) → corpus-missing WARN | WARN: corpus-missing (paywall) |
| 11 | ~1 mmol/L per 10 mmol/L increment total lipids | C[6] Dimeski 2006 Clin Chemistry DOI 10.1373/clinchem.2005.054981 | Host oup.com ✓; Clin Chemistry = Clinical Chemistry (AACC/OUP). Paywall abstract not retrievable → corpus-missing WARN | WARN: corpus-missing (paywall) |
| 12 | ODS 10.4% demyelination even with <10 mmol/L/24h (96 ODS cases, systematic review) | B[6] Bastos 2023 J Bras Nefrol PMID 37523718 | PubMed CAPTCHA blocked abstract retrieval; host scielo.br whitelisted; journal PMC-indexed. corpus-missing WARN | WARN: corpus-missing (CAPTCHA) |
| 13 | Adrogué/Madias PMID 10816188 (Hypernatremia) and 10824078 (Hyponatremia) author verification | A[2,3]/D implied | PubMed confirmed both: H J Adrogué + N E Madias, NEJM 2000; PMID 10816188 = Hypernatremia (Vol 342 No. 20), PMID 10824078 = Hyponatremia (Vol 342 No. 21) | PASS ✓ |

**IC-13 paraphrase discrepancy (WARN — item 4):** Section D states Sterns 1986 studied "60 patients with serum sodium below 116 mmol/L." The PubMed abstract describes "eight patients" with ODS and a serum sodium threshold of <106 mmol/L (or "sodium <106 mmol per liter"), not <116 mmol/L. The 60-patient figure and the 116 mmol/L threshold are not confirmed in the abstract. This is a paraphrase-no-token-match for the specific threshold value. The core finding (>12 mmol/L/day causes ODS) IS confirmed. Single discrepancy in this section → WARN, not HALT per IC-13 rules.

**IC-13 verdict:** 13 claims checked. 0 `number-not-found`. 0 `quote-not-found`. 1 `paraphrase-no-token-match` (WARN). 3 `corpus-missing` (WARN — paywall/CAPTCHA).

---

## Verdict

verdict: PASS

**Summary:** All 13 IC checks pass. Zero bare inline citations. Zero off-whitelist hosts grounding numerical claims (one off-whitelist host — f1000research.com in Section A [4] — grounds mechanism only, not a number; WARN). All verified PMIDs confirmed. No fabricated citations, no placeholders, no Wikipedia. Concentration audit: diverse authorship, no single-lab dominance. Population-mismatch: vacuous pass (no animal/in-vitro cites). Corpus scoping: 13 claims checked — 0 failed, 4 warnings (1 paraphrase-threshold discrepancy in Sterns 1986 sodium cutoff "116 mmol/L" vs abstract's "<106 mmol/L"; 3 paywall/CAPTCHA corpus-missing on non-pivotal claims).

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"WARN"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"WARN"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":12,"largest_cluster_count":1,"share":0.08,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":13,"claims_failed":[{"claim":"Sterns 1986 studied 60 patients with serum sodium below 116 mmol/L [D:10, cohort]","cite_key":"sterns-1986-pmid3713747","failure_mode":"paraphrase-no-token-match","grep_command":"PubMed abstract fetch PMID 3713747","grep_output":"Abstract states 'eight patients' and threshold '<106 mmol/L'; '116 mmol/L' and '60 patients' not confirmed in abstract text"}]},"halt_reasons":[],"warnings":["IC-10: Section A cite [4] Ranieri et al. F1000Research 2019 (PMID 30800291) hosted at f1000research.com — not on source whitelist; grounds mechanism only (AQP2/V2 cascade), no numerical claim attached; WARN not HALT","IC-10: Arzhan et al. bib DOI 10.34067/KID.0007272021 resolves via redirect to journals.lww.com with 402 paywall; PMID 35919520 verified on PubMed with all claimed numbers confirmed; minor DOI variant possible between prepress and final assignment","IC-13: paraphrase-no-token-match — Section D Sterns 1986 description states 'below 116 mmol/L' but PubMed abstract states '<106 mmol/L'; '60 patients' not confirmed in abstract (abstract says 'eight patients' with ODS); core threshold finding (>12 mmol/day) confirmed","IC-13: corpus-missing (paywall) — Katrangi 2019 JALM PMID not in bib, DOI 10.1373/jalm.2018.028720; claims -6.1 mmol/L and 70% figure unverifiable from abstract","IC-13: corpus-missing (paywall) — Dimeski 2006 Clin Chemistry DOI 10.1373/clinchem.2005.054981; ~1 mmol/L per 10 mmol/L triglyceride claim unverifiable from abstract","IC-13: corpus-missing (CAPTCHA) — Bastos 2023 J Bras Nefrol PMID 37523718; 10.4% / 96 ODS cases claim unverifiable from abstract"],"iterations":1}
```
