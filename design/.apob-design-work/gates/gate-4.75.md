# Gate 4.75 — Citation Integrity Verifier (ApoB biomarker, mode=standard)

Independent Phase-4.75 integrity verification of the ApoB corpus: `sections/section-A.md` (Identity, Physiology & Causal Significance), `sections/section-B.md` (Reference Ranges, Measurement & Determinants), and all `corpus/*.txt` source files (9 A-corpus + 8 B-corpus = 17 fetched primaries). Full 13 IC-checks run. Structural compliance only — content quality is the judges' domain.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: []
```

verdict: PASS

All 13 IC-checks PASS. No live `regulatory`/`vendor_label`/`anecdote_aggregate`/`practitioner_protocol`/`compounding_data_sheet` tag carries a number; the EAS, NLA, and ESC/EAS professional-society guideline sources are correctly tagged `mechanism_review` (the only `regulatory` tokens in either file live inside the post-fix audit prose describing the REMOVED tag — verified by region-scoped grep, not in any body citation). Population-mismatch passes affirmatively (human biomarker; zero animal/in_vitro sources). Concentration audit: 16 distinct primaries, largest author cluster = 2 (Sniderman), share 0.125 — multi-cohort, threshold not triggered. Corpus scoping: ~40 load-bearing numerical/verbatim claims grep-verified, 100% found — far above the standard ≥50% floor.

---

## IC-1 Type-Tag Presence

Every inline `[N, tag]` in both section bodies carries a tag from the canonical enum. Tags in use: `meta_analysis`, `cohort`, `mechanism_review`, `rct`. No out-of-enum tag.

The `[7, regulatory]` / `[7,regulatory]` (Section A) and `[1, regulatory]` ×n (Section B) hits surfaced by a naive whole-file grep are confined to the `## Post-fix grep audit` prose (Section A L60–63; Section B L93–106), where they appear as descriptions of the OLD/removed tag and as the literal grep PATTERN strings. Region-scoped greps of the body confirm: Section A lines 1–49 contain zero `[7, regulatory]`; Section B lines 1–87 contain zero `[N, regulatory]` of any ref number. The Phase-4.25 cross-section remediation (society → `mechanism_review`) is genuinely applied in the live citations.

`[N, tag]` literals at Section A L45, Section B L73/L115 are self-check prose describing the citation FORMAT, not placeholder citations.

No type-tag violations detected.

## IC-2 Bibliography Type-Tag Presence

Section A: 9 bibliography entries [1]–[9], each `— tag: <enum>` (3× meta_analysis-equivalent count: meta_analysis ×2, cohort ×4, mechanism_review ×3). Section B: 14 bibliography keys ([1]–[11] + determinants/diet/pharma bundles), each carrying a `tag:`/`tags:` annotation; multi-purpose bundles use accepted multi-tag form (`mechanism_review / rct`, `meta_analysis / rct`, `meta_analysis / mechanism_review`). All tags within enum.

No bibliography type-tag omissions detected.

## IC-3 Vendor-Not-Numerical

No `vendor_label` citation appears anywhere in either section. Check passes vacuously.

No vendor-not-numerical violations detected.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citation appears in either section body. (Section B L74 / corpus B-4 note that lola/siphox/levels aggregators were used ONLY to surface mechanism leads and explicitly downgraded; no number rests on them.) Check passes vacuously for body citations.

No anecdote-not-numerical violations detected.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citation appears in either section. Check passes vacuously.

No practitioner-protocol-efficacy violations detected.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citation appears in either section. Check passes vacuously.

No compounding-data-sheet-efficacy violations detected.

## IC-7 Population-Mismatch

ApoB is a human biomarker; the corpus is entirely human (RCTs, prospective/retrospective human cohorts, human MR/meta-analyses, society consensus, analytical-method standardization). Grep confirms ZERO `[N, animal]` and ZERO `[N, in_vitro]` citations in either section. No animal or in-vitro number is presented as a human figure. Every dose/effect-size/n/AE/percentile is human-sourced and population-annotated in the bibliography (NHANES US adults; Korean cohort; Swedish AMORIS; EuBIVAS 6-EU-lab; multinational NEJM outcome trials; UK Biobank). No `[population-mismatch:]` tags are required and none are missing.

checked_citations: 0 animal/in_vitro cites (all 23 distinct primaries are human). PASS affirmatively.

No population-mismatch violations detected.

## IC-8 Route-Extrapolation

ApoB is a measured plasma analyte, not a dosed compound for the biomarker entry. The dose claims present are lipid-lowering-drug doses (statin 40 mg, evolocumab 140 mg q2w, alirocumab 75–150 mg, ezetimibe 10 mg, inclisiran), each grounded on the corresponding outcome-trial primary that used that exact agent/dose/route; no cross-route extrapolation is asserted. No route mismatch.

No route-extrapolation violations detected.

## IC-9 Concentration-Surfacing

Distinct primaries (tag ∈ rct|meta_analysis|cohort|animal|in_vitro), deduplicated across A+B = 16:
Ference 2019 JAMA; Sniderman 2011 Circ; Marston 2022 JAMA Cardiol; McQueen/INTERHEART 2008 Lancet; Walldius/AMORIS 2021; Sniderman 2024 EHJ; Choi 2023 (Korean RI); Ritchie 2006 (RI meta); Clouet-Foraison 2020 (EuBIVAS); Cannon 2015 (IMPROVE-IT); Sabatine 2017 (FOURIER); Schwartz 2018 (ODYSSEY OUTCOMES); Thanassoulis 2014 (statin apoB meta); Robinson 2012 (LLT apoB meta); Mensink 2003 (diet meta); Mensink-Katan 1990 (trans-FA RCT).

Largest author/group cluster = Sniderman (2 papers: 2011 + 2024) = 2. Share = 2 / 16 = 0.125 (12.5%). The literature spans many independent groups, journals, countries, and institutions (US JAMA/NEJM, Lancet 52-country, Swedish AMORIS, Korean, 6-lab European EuBIVAS, multinational PCSK9 outcome trials) — a genuinely multi-cohort base, as expected for ApoB.

Share 0.125 < 0.70 → threshold NOT triggered. No first-class concentration-risk section is required; gate passes vacuously.

No concentration-surfacing failure detected.

## IC-10 No Fabricated Citations

Section A: all inline ref numbers 1–9 resolve to bibliography entries [1]–[9]. Section B: all inline keys (1–11, determinants, pharma) resolve to bibliography entries. The `[diet]` bibliography key is present but cited inline via the `[determinants, …]` channel rather than a `[diet, …]` token — a dangling (unused) bib entry, not a fabricated/unresolved inline citation; IC-10 (inline→bibliography resolution) passes. Every entry carries a PMID/DOI and a corpus pointer. No Wikipedia in bibliography (see IC-12).

No fabricated citations detected.

## IC-11 No Placeholder Strings

Grep for `citation needed | TBD | TODO | Content continues | according to some reports | research suggests | experts believe` across both sections → zero matches. (`[N, tag]` literals are format descriptions in self-check prose, not placeholders.)

No placeholder strings detected.

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` across both sections and all 17 corpus files → zero matches.

No Wikipedia citations detected.

## IC-13 Per-Citation Corpus Scoping

Standard mode: ≥50% sample of numerical/quoted claims required (min 10). ~40 distinct load-bearing claims grep-verified against the cached corpus — effectively a 100% pass over the load-bearing set, well above the floor.

Section A (all verified, exact match):
- [A1] Ference: 654,783 / 63 studies / 91,129 CHD; LPL OR 0.771 (0.741–0.802); LDLR OR 0.773 (0.747–0.801); TG OR 1.014 P=.19; LDL-C OR 1.010 P=.19 → A-1.
- [A2] Sniderman: 233,455 / 22,950; apoB RRR 1.43 (1.35–1.51); non-HDL-C 1.34; LDL-C 1.25; +5.7% / +12.0% within-study → A-2.
- [A3] Marston: 389,529, HR 1.27 (1.15–1.40); 40,430, HR 1.17 (1.00–1.36) → A-3.
- [A4/A6] physiology: 4536 aa apoB-100; ~512,000 Da; 2152 aa apoB-48; "eight potential proteoglycan-binding sites"; single-molecule-per-particle and MTTP verbatim → A-4, A-6.
- [A5] INTERHEART: 12,461 / 14,637 / 52 countries; PAR 54%; OR 1.59 (1.53–1.64); LDL/HDL 37%; TC/HDL 32%; index OR ~3.25 → A-5.
- [A7] EAS verbatim retention-model + "may more accurately reflect the causal effect" → A-7.
- [A8] AMORIS: 137,100 / 22,473 / 17.8 yr; MACE HR 1.7; non-fatal MI HR 2.7; ~20-yr lead → A-8.
- [A9] discordance: 293,876 / 19,982; residual apoB HR 1.06 (1.04–1.07) and 1.04 (1.03–1.06); LDL-C 130 → 7.3% vs 4.0%; "not adequate proxies" verbatim → A-9.

Section B (all verified, exact match):
- [B1] NLA: NHANES n=12,696; percentiles 54/61/90/125/137; thresholds 60/70/90; CV 5–6%; statin 33% vs 42% LDL-C; fasting verbatim → B-1.
- [B2] standardization: SP3-07 = 1.22 g/L = 122 mg/dL; among-lab CV 3.1–6.7%; pre-cal >19% → ~6–7%; ~20%→~7%; ~4% inter-assay → B-2.
- [B3/B4/B5] Korean RIs 50–131/51–127 (np), 46–134/49–129 (±2SD), means 90.2/88.9, n=334, 59.6 y; Ritchie 82 publications, Jungner 147,576; EuBIVAS 91 / 10 wk / 6 labs → B-3.
- [B4] determinants: FH LDLR ~90% / APOB 5–10% / PCSK9 ~1%; HeFH ~1:250; HoFH ~1:160,000–300,000; LDL-C >500 mg/dL; APOB Arg3527Gln (R3500Q); inclisiran 33.7%; bempedoic 15–18%/30%; PCSK9 evolo ~55% / aliro ~58%; Mensink 60 trials; trans-FA ~10.9% energy → B-4.
- [B8] IMPROVE-IT 92.7→81.3 (12.3%), →70.3, achieved ~70/67 → B-5.
- [B9] FOURIER −46%, 83→45, median 38 → B-6.
- [B10] ODYSSEY 79→39 (~50.6%), mean 49 → B-7.
- [B11] each 10-mg/dL apoB → ~9% CHD / ~6% CVD; statin 12.3%→~39.5% (JUPITER 66 from ~109) bracketing ~33% mean → B-8.

claims_checked: 40. claims_failed: [] (zero quote-not-found, number-not-found, or paraphrase-no-token-match; zero corpus-missing — all cited corpora cached and present).

No corpus-scoping failures detected.

---

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {
    "IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"},
    "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"},
    "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"},
    "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"},
    "IC-13": {"status": "PASS"}
  },
  "population_mismatch": {"verdict": "PASS", "checked_citations": 0},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 16, "largest_cluster_count": 2, "share": 0.125, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 40, "claims_failed": []},
  "halt_reasons": [],
  "warnings": [],
  "iterations": 1
}
```
