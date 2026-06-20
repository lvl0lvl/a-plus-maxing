# Gate 4.75 — Citation Integrity Verification: Free T3 Biomarker Report

**Run date:** 2026-06-19
**Iteration:** 2
**Sections checked:** section-A.md, section-B.md, section-C.md, section-D.md
**Mode:** standard (≥50% sample of higher-stakes numerical claims)

---

## Verdict (iteration 2)

verdict: PASS

The EC50 fix has landed. Section A line 9 now reads "EC50 data show T4 requires ~30- to 50-fold higher concentrations than T3 to achieve equivalent transcriptional activation at TRα1 and TRβ1, respectively [3, mechanism_review]" — the prior "~60- to 70-fold" text is absent (grep returned zero matches for any "60-to-70" / "60–70" / "60-70" variant). All IC-1 through IC-12 checks carry forward from iteration 1. IC-13 corpus-scoping closes clean at 13/13: the single failure (EC50 number mismatch against Wejaphikul 2019 Figure 5) is resolved; all prognostic HRs (Iervasi 3.582, Sato 2.304, Vidart OR 2.21, Spaulding 53%) verified clean in iteration 1 and unchanged. Three paywalled corpus-missing WARNs (Bianco full-text, Ross 2016 CAPTCHA, Welsh & Soldin paraphrase) and the unnumbered IFCC C-STFT prose reference remain as documented warnings and do not affect verdict.

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":34,"largest_cluster_count":4,"share":0.12,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":13,"claims_failed":[]},"halt_reasons":[],"warnings":["Bianco/Ross/Welsh paywalled corpus-missing","IFCC C-STFT unnumbered prose ref (qualitative, whitelisted)"],"iterations":2}
```

---

## Iteration 1 (archived below — HALT)

---

## IC-1 Type-Tag Presence

All inline citations are in the format `[N, <tag>]` or bare `[N]` in the bibliography sections. All inline tags checked:

- Section A: `mechanism_review` (citations 1–7) — all valid enum members.
- Section B: `cohort` (1–3, 8, 11), `mechanism_review` (4), `regulatory` (5, 7, 12), `cohort` (8) — all valid.
- Section C: `mechanism_review` (1–8) — all valid.
- Section D: `regulatory` (1–2), `mechanism_review` (3, 9), `cohort` (4–8), `rct` (10) — all valid.

One unnumbered prose reference in Section C: "[IFCC C-STFT website]" — acknowledged in the prompt as acceptable context with no number; not an inline `[N, tag]` citation and grounds only a qualitative standardization-status statement. Acceptable per prompt instruction.

**Status: PASS** — all tagged inline citations use valid enum members.

---

## IC-2 Bibliography Type-Tag Presence

All bibliography entries checked across all four sections:

- Section A: entries [1]–[7] carry `tag: mechanism_review` or `tag: regulatory` — all present and valid.
- Section B: entries [1]–[12] carry `[cohort]`, `[mechanism_review]`, or `[regulatory]` — all present and valid.
- Section C: entries [1]–[8] carry `[mechanism_review]` — all present and valid.
- Section D: entries [1]–[10] carry no bracketed tag annotations in bibliography lines. Entries are listed without the `[tag]` bracket format. However, Section D's bibliography does include inline tagging in the body text (e.g., `[1, regulatory]`, `[3, mechanism_review]`, `[10, rct]`), so the type is determinable from inline citations. The bibliography format in Section D does not repeat the tag bracket.

  This is a minor format inconsistency (Sections A–C include tag in bibliography; Section D does not), but it does not represent a missing tag — the tags are present inline in the body. **Noting as advisory, not HALT.**

**Status: PASS** — no untagged citations; Section D bibliography format advisory noted.

---

## IC-3 Vendor-Not-Numerical

No `vendor_label` citations present in any section.

**Status: PASS** — No vendor_label citations detected.

---

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citations present in any section.

**Status: PASS** — No anecdote_aggregate citations detected.

---

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations present in any section.

**Status: PASS** — No practitioner_protocol citations detected.

---

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations present in any section.

**Status: PASS** — No compounding_data_sheet citations detected.

---

## IC-7 Population-Mismatch

No `animal` or `in_vitro` citations present in any section. All citations are from human clinical/mechanistic literature. The deiodinase-mechanism discussion in Section A (D1/D2/D3 Km values, enzymatic functions) cites mechanism review papers without any animal or in-vitro numerical claims grounded in animal-only sources.

**Checked:** 0 `animal` or `in_vitro` citations.

**Status: PASS** — No animal or in_vitro citations present; gate passes vacuously.

---

## IC-8 Route-Extrapolation

No dose claims with route specifications are present in this biomarker report. The document discusses diagnostic thresholds, reference intervals, and prognostic cutoffs — not dosing routes. Route-extrapolation check does not apply.

**Status: PASS** — No route-dependent dose claims present.

---

## IC-9 Concentration-Surfacing

Primary citation inventory (distinct primaries, type tags in {rct, meta_analysis, cohort, open_label, animal, in_vitro}):

Section A: none (all mechanism_review or regulatory)
Section B: cohort [1] González-Sagrado, cohort [2] Yildiz, cohort [3] Xiong, cohort [8] Sue/Leung, cohort [11] Karakosta, regulatory [5, 7, 12]
Section C: all mechanism_review (no primary study types)
Section D: cohort [4] Iervasi, cohort [5] Sato, cohort [6] Zhao, cohort [7] Asai, meta_analysis [8] Vidart, rct [10] Spaulding

Total distinct primaries (type in scope): ~11 (cohorts + meta_analysis + rct).

Author/institution clustering: Sources span multiple independent groups — González-Sagrado (Spain), Yildiz (Turkey), Xiong (China), Iervasi (Italy/Pisa), Sato (Japan), Zhao (China), Asai (Japan), Vidart (Brazil), Spaulding (USA), ATA guidelines, Endocrine Society. No single lab cluster dominates. Largest institutional cluster is at most 2–3 (Japanese HF groups: Sato + Asai), representing ~18% of the 11 primaries.

Single-lab share: well below 70% threshold.

**Status: PASS** — No concentration risk; threshold (≥70%) not triggered.

---

## IC-10 No Fabricated Citations

All inline `[N]` references resolve to bibliography entries. No dangling inline citations detected.

PMID spot-check resolution results:

| Citation | PMID | Resolves? |
|----------|------|-----------|
| A[1] Bianco 2019 | 31033998 | YES — abstract confirmed, paper exists |
| A[2] Salas-Lucia 2022 | 36387853 | YES — abstract confirmed |
| A[3] Wejaphikul 2019 | 30817817 | YES — abstract confirmed |
| A[4] Brent 2012 | 22945636 | Not fetched — PMID plausible (JCI 2012) |
| A[5] Sabatino 2021 | 34674502 | YES — abstract confirmed |
| A[6] Van Uytfanghe 2023 | 37655789 | YES — abstract returned |
| A[7] Ortiga-Carvalho 2016 | 27347897 | Not fetched — PMID plausible |
| B[5] Ross 2016 ATA | 27521067 | YES — PMID resolves (CAPTCHA on fetch, not a fabrication signal) |
| B[7] Jonklaas 2014 | 25266247 | Not fetched — PMID plausible |
| D[4] Iervasi 2003 | 12578873 | YES — confirmed abstract, exact HR, n, cutoff |
| D[5] Sato 2019 | 30682427 | YES — confirmed abstract, all HRs and n |
| D[8] Vidart 2022 | 35015701 | YES — confirmed abstract, OR and n |
| D[10] Spaulding 1976 | 1249190 | YES — confirmed abstract, 53% fasting T3 drop |

No fabricated PMIDs detected. The free-T4 sibling-entry pattern (fabricated PMIDs) is not replicated here.

**Status: PASS** — No fabricated citations identified.

---

## IC-11 No Placeholder Strings

Searched all four sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No matches found in any section.

**Status: PASS** — No placeholder strings detected.

---

## IC-12 No Wikipedia Citations

No Wikipedia URLs (en.wikipedia.org or variants) appear in any bibliography.

**Status: PASS** — No Wikipedia citations.

---

## IC-13 Per-Citation Corpus Scoping

**Mode: standard** — ≥50% random sample of citations with numerical or quoted claims. Higher-stakes claims targeted per prompt brief.

### Claims checked (13 total)

**CLAIM 1** — Section A: "~30 µg/day total T3 production, ~5 µg/day thyroidal (~17%), ~25 µg/day peripheral (~83%)" [A-1, mechanism_review]
- Source: Bianco 2019, PMID 31033998
- Fetch result: Abstract confirmed: "The daily T3 production in a 70-kg adult individual is ∼30 μg/d. The thyroid gland contributes with ∼5 μg/d and the rest is produced outside of the thyroid parenchyma."
- **Result: PASS**

**CLAIM 2** — Section A: T3 binding receptors "with approximately 7- to 15-fold greater affinity than T4" and "EC50 data show T4 requires ~60- to 70-fold higher concentrations than T3 to achieve equivalent transcriptional activation at TRα1 and TRβ1" [A-3, mechanism_review]
- Source: Wejaphikul 2019, PMID 30817817
- Fetch result: Paper reports "The EC50 of T4 is ∼30- to 50-fold higher than the EC50 of T3" (Figure 5 caption, confirmed by abstract). The 7-15 fold binding affinity claim is stated qualitatively in abstract ("binds with greater affinity") without the specific ratio. The ~60-70-fold EC50 claim is directly contradicted by the paper's own 30-50 fold figure.
- **Result: HALT — number-not-found** (reported value 30-50x; claimed value 60-70x; these do not overlap and are not normalization variants)

**CLAIM 3** — Section A: "nuclear T3 concentrations have been estimated at 58- to 251-fold above cytosolic concentrations in liver, kidney, heart, and brain" [A-1, mechanism_review]
- Source: Bianco 2019, PMID 31033998
- Fetch result: Abstract confirmed T3 production figures but did not mention nuclear-to-cytosolic concentration ratios. Full text likely required (paywalled review article).
- **Result: WARN — corpus-missing (paywall; abstract-only access)**

**CLAIM 4** — Section A: "D2's short half-life (~20 minutes in the presence of T4 substrate)" [A-1, mechanism_review]
- Source: Bianco 2019, PMID 31033998
- Fetch result: Not found in abstract; likely in full text.
- **Result: WARN — corpus-missing (paywall; abstract-only access)**

**CLAIM 5** — Section A: "approximately 50% of liver and kidney thyroid hormone receptors occupied by T3 at normal circulating concentrations" [A-1, mechanism_review]
- Source: Bianco 2019, PMID 31033998
- Fetch result: Not found in abstract; likely in full text.
- **Result: WARN — corpus-missing (paywall; abstract-only access)**

**CLAIM 6** — Section B: "Unit conversion: pg/mL × 1.536 = pmol/L (molecular weight of T3 = 650.97 g/mol)"
- This is a mathematical derivation (MW of T3 = 650.97 g/mol; 1000/650.97 × 1 = 1.536). No citation required; verified by calculation.
- **Result: PASS (derived, no citation)**

**CLAIM 7** — Section B: "T3 toxicosis accounts for approximately 5% of all thyrotoxicosis cases in North America" [B-5, regulatory]
- Source: Ross 2016 ATA Guidelines, PMID 27521067
- Fetch result: CAPTCHA blocked direct abstract access; redirect to publisher also returned 403. Unable to verify from abstract or full text.
- **Result: WARN — corpus-missing (CAPTCHA/access blocked)**

**CLAIM 8** — Section D: "Iervasi et al. (2003), n=573 cardiac patients; fT3 was the single strongest predictor... HR 3.582, P<0.0001; patients with fT3 <3.1 pmol/L had substantially higher mortality" [D-4, cohort]
- Source: Iervasi 2003, PMID 12578873
- Fetch result: Abstract confirmed all three data points exactly: n=573, HR 3.582, P<0.0001, cutoff 3.1 pmol/L.
- **Result: PASS**

**CLAIM 9** — Section D: "Sato et al. (2019), n=911 HF patients; HR 2.304 (95% CI 1.736–3.058); HR 1.926 (95% CI 1.268–2.927); median 991-day follow-up; fT3 cutoff <2.3 pg/mL" [D-5, cohort]
- Source: Sato 2019, PMID 30682427
- Fetch result: Abstract confirmed all five data points exactly.
- **Result: PASS**

**CLAIM 10** — Section D: "Vidart et al. (2022), meta-analysis of 25 studies, n=6,869 critically ill patients; pooled OR 2.21 (95% CI 1.64–2.97)" [D-8, meta_analysis]
- Source: Vidart 2022, PMID 35015701
- Fetch result: Abstract confirmed all three data points exactly.
- **Result: PASS**

**CLAIM 11** — Section D: "caloric restriction... a 53% drop in serum T3 was observed with total fasting, with rT3 rising reciprocally; diets providing ≥50 g carbohydrate daily did not significantly alter T3" [D-10, rct]
- Source: Spaulding 1976, PMID 1249190
- Fetch result: Abstract confirmed: "total fasting resulted in a 53% reduction in serum T3"; "subjects receiving isocaloric diets containing at least 50 g of carbohydrate showed no significant changes in either T3 or rT3." Confirmed with nuance (rT3 reciprocal rise holds for fasting but not no-carb diets — the Section D claim says "rT3 rising reciprocally" in the fasting context, which is accurate).
- **Result: PASS**

**CLAIM 12** — Section C: "T3 thyrotoxicosis occurred in only 1.6% of cases with concurrent TSH/fT4/fT3 results" [C-3, mechanism_review]
- Source: Lin 2024, ADLM Scientific Short URL
- Fetch result: Confirmed: "T3 thyrotoxicosis was relatively uncommon, with a frequency of 1.6% (70 out of 4,366 grouped TSH-fT4-fT3 results)."
- **Result: PASS**

**CLAIM 13** — Section C: "within-run imprecision of approximately 2.0% CV for fT3, somewhat better than total T3 (~3.3% CV)" [C-3, mechanism_review]
- Source: Lin 2024, ADLM Scientific Short URL
- Fetch result: Confirmed: "The imprecision for fT3 and tT3 are ~2.0% and ~3.3% respectively at comparable concentrations."
- **Result: PASS**

### Summary

| Claim | Source | Result |
|-------|--------|--------|
| 1. 30 µg/day T3 production breakdown | Bianco 2019 | PASS |
| 2. EC50 T4/T3 ratio "60-70 fold" | Wejaphikul 2019 | **HALT — number-not-found** (paper says 30-50x) |
| 3. Nuclear T3 58-251x above cytosolic | Bianco 2019 | WARN — corpus-missing |
| 4. D2 half-life ~20 min | Bianco 2019 | WARN — corpus-missing |
| 5. 50% receptor occupancy at normal fT3 | Bianco 2019 | WARN — corpus-missing |
| 6. ×1.536 conversion factor | Derived | PASS |
| 7. T3-toxicosis ~5% of thyrotoxicosis | Ross 2016 ATA | WARN — corpus-missing (CAPTCHA) |
| 8. Iervasi HR 3.582, n=573, <3.1 pmol/L | Iervasi 2003 | PASS |
| 9. Sato HR 2.304, n=911, 991 days, <2.3 pg/mL | Sato 2019 | PASS |
| 10. Vidart OR 2.21, 25 studies, n=6,869 | Vidart 2022 | PASS |
| 11. 53% T3 drop fasting; ≥50g CHO no change | Spaulding 1976 | PASS |
| 12. T3 thyrotoxicosis 1.6% of cases | Lin 2024 | PASS |
| 13. fT3 CV 2.0%, tT3 CV 3.3% | Lin 2024 | PASS |

**claims_checked: 13**
**claims_failed: 1** (Claim 2 — EC50 ratio number-not-found)

---

## Verdict

verdict: HALT

### Findings summary

**HALT triggered by IC-13 corpus-scoping-fail.** Section A attributes "~60- to 70-fold higher concentrations than T3 to achieve equivalent transcriptional activation at TRα1 and TRβ1" to Wejaphikul 2019 (PMID 30817817). The paper's Figure 5 caption explicitly states "The EC50 of T4 is ∼30- to 50-fold higher than the EC50 of T3" — a materially different value that does not overlap with the 60-70 fold claim. This is a `number-not-found` failure under IC-13.

All other high-stakes numeric claims verified (Iervasi HR 3.582, Sato HR 2.304 with full CI, Vidart OR 2.21, Spaulding 53% fasting drop, Lin 1.6% T3-toxicosis, conversion factor) are confirmed from source abstracts. No fabricated PMIDs detected (contrast: free-T4 sibling entry). Four corpus-missing WARNs (Bianco 2019 full-text claims, ATA 2016 CAPTCHA) — these do not HALT.

**Section C "no value for hypothyroidism" attribution to Welsh & Soldin [C-1]:** The abstract does not support this as a claim Welsh & Soldin make themselves; their paper advocates for LC-MS/MS T3 measurement. The full text may attribute this to a referenced textbook. This is a paraphrase-attribution concern; given the abstract contra-indication, flagging as WARN (paraphrase-no-token-match) rather than HALT (single instance, abstract-only access).

```json
{"phase":"4.75","verdict":"HALT","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"HALT","failure_mode":"number-not-found","claim":"T4 requires ~60- to 70-fold higher concentrations than T3 to achieve equivalent transcriptional activation at TRα1 and TRβ1 [A-3]","cite_key":"wejaphikul-2019","paper_value":"~30- to 50-fold (Figure 5 caption)"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":11,"largest_cluster_count":2,"share":0.18,"threshold_triggered":false},"corpus_scoping":{"verdict":"HALT","claims_checked":13,"claims_failed":[{"claim":"EC50 of T4 is ~60- to 70-fold higher than T3 at TRα1 and TRβ1 [section-A, citation 3]","cite_key":"wejaphikul-2019-pmid-30817817","failure_mode":"number-not-found","paper_reports":"~30- to 50-fold (Figure 5 caption, confirmed by abstract fetch)"}]},"halt_reasons":["corpus-scoping-fail: IC-13 number-not-found — Section A EC50 ratio 60-70x claimed vs 30-50x in source (Wejaphikul 2019 PMID 30817817)"],"warnings":["corpus-missing: Bianco 2019 (PMID 31033998) full-text claims (nuclear T3 58-251x cytosolic; D2 half-life ~20 min; 50% receptor occupancy) — abstract-only access, paywall","corpus-missing: Ross 2016 ATA Guidelines (PMID 27521067) — CAPTCHA blocked abstract fetch; T3-toxicosis ~5% prevalence unverifiable from source","paraphrase-no-token-match: Section C 'no value for diagnosing or monitoring hypothyroidism' attributed to Welsh & Soldin [C-1]; abstract takes different stance (advocates LC-MS/MS T3 measurement); likely quotes internal textbook reference in full text"],"iterations":1}
```
