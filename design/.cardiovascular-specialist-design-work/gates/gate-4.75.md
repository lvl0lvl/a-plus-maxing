# Gate 4.75 — Citation Integrity Verifier (cardiovascular-specialist, mode=standard)

Phase-4.75 mechanical integrity check of the four judged section drafts (`section-A.md`..`section-D.md`) against the project type-tag enum (`vault/library/_source-whitelist.md`), the IC-1..IC-13 procedure (`citation-integrity.md`), and the health gates (population-mismatch §1, concentration-audit §3). Verifier ran its own greps and independent web-fetches; section self-checks were NOT trusted.

## IC-1 Type-Tag Presence

Every LIVE inline `[N, tag]` carries exactly one tag from the enum. Distinct inline tags observed (excluding `[internal: ...]`, `[population-mismatch: ...]`, `[route-extrapolation]`, `[translated:...]`, and template/self-check text):

- Section A: `cohort`, `regulatory`, `meta_analysis`, `rct`, `mechanism_review` — all enum-valid. Body line 25 reads `[11, cohort]` (enum-valid).
- Section B: `meta_analysis`, `rct`, `practitioner_protocol`, `regulatory`, `mechanism_review` — all enum-valid. (`[3, practitioner_protocol]` ×6 and `[3, regulatory]` ×1; ref [3] is dual-purpose.)
- Section C: `cohort`, `meta_analysis`, `animal`, `mechanism_review`, `rct`, `regulatory`, `practitioner_protocol` — all enum-valid.
- Section D: `regulatory`, `cohort`, `meta_analysis` — all enum-valid. Compound cite `[3, regulatory; 4, meta_analysis]` resolves to two enum-valid tags.

The single out-of-enum token `[11, cohort/MR]` appears ONLY in Section A's self-check gap-list (line 84) and the post-fix audit table (the OLD value, quoted as "removed") — it is NOT a live body citation; the live body cite at line 25 is `[11, cohort]`. `[N, tag]` literals are template prose in all four self-checks. No out-of-enum LIVE inline tag detected.

count_checked: 110 inline tagged cites across 4 sections; count_flagged: 0.

## IC-2 Bibliography↔Inline Symmetry

Per-section inline `[N]` numbers resolve 1:1 to bibliography entry numbers and vice versa:

- Section A: inline {1–22} ↔ biblio {1–22}. Symmetric.
- Section B: inline {1–21} ↔ biblio {1–21}. Symmetric.
- Section C: inline {1–16} ↔ biblio {1–16}. Symmetric. (A spurious "89" surfaced from the audit-trail string `grep -inE '0\.6[89]'`; it is shell text, not a citation.)
- Section D: inline {1–12} ↔ biblio {1–12}. Symmetric. Ref [4] is cited inline only in the compound form `[3, regulatory; 4, meta_analysis]` and resolves correctly.

Every bibliography entry carries a `[tag]`. Section B ref [3] carries dual tag `[regulatory / practitioner_protocol]`; both enum-valid (IC-2 permits multiple tags). No orphan inline cites; no untagged bibliography entries.

## IC-3 Vendor-Not-Numerical

No `vendor_label` inline citation exists in any section. The only `vendor_label` string occurrences are self-check prose attesting their absence. No vendor cite grounds any numeric. No violation detected.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` inline citation exists in any section (only self-check attestations of absence). No anecdote cite grounds any numeric. No violation detected.

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` cites: Section B `[3]` (×6) and Section C `[10]` (×1). Each was sentence-inspected:

- B `[3, practitioner_protocol]` grounds ONLY statin intensity tiers (LDL-lowering-potency convention, explicitly labeled "NOT efficacy claim"), the four first-line antihypertensive classes, the pregnancy contraindication, and monitoring/stopping conventions (lipids+ALT, renal+K⁺ at 1–2 wk). These are dose/threshold/monitoring conventions — admissible for `practitioner_protocol`. No efficacy effect-size rests on it.
- C `[10, practitioner_protocol]` grounds the Karvonen %HRR formula (a prescription convention). No efficacy effect-size.
- All efficacy effect-sizes (SPRINT, CTT, JUPITER, CANTOS, LoDoCo2, IMPROVE-IT, FOURIER, CLEAR, REDUCE-IT, Sattar, SAMSON, StatinWISE, ASPREE, ARRIVE, VITAL, Mandsager, Kodama, Cornelissen, Cochrane) carry `rct`/`meta_analysis`/`cohort` tags.
- `regulatory` cites ground guideline thresholds/recommendations only (130/80, 140/90, ≥70/<55 mg/dL targets, 150–300 min PAG, FDA De Novo sens/spec) — permitted under IC-5.

No practitioner_protocol or regulatory cite is the sole source of an efficacy effect-size. No violation detected.

## IC-6 First-Author+Year Plausibility + Spot-Verify

**Fabrication-shape scan:** No bad DOI prefixes, fake TLDs, future dates beyond plausibility, or implausible PMIDs found. 2024/2025-dated refs (Meixner C[7], Apple Watch ECG MA D[6], Dial D[9], Svinin D[12]) are plausible given the 2026-05 date. NEJM/Lancet/JAMA/Circulation DOIs and PMIDs are well-formed.

**Independent web spot-verifies (6 load-bearing claims across all 4 sections; requirement ≥4 across different sections):**

| # | Section | Claim | Cite | Source verification | Result |
|---|---|---|---|---|---|
| 1 | A | SPRINT primary composite HR 0.75 (0.64–0.89), <120 vs <140 SBP, n=9,361 | A[5] | NEJM 2015 NEJMoa1511939 (PMID 26551272), Wright/SPRINT Group — 25% RRR = HR 0.75 | MATCH |
| 2 | A & B | CTT 2010: each 1 mmol/L LDL ↓ → MVE RR 0.78 (0.76–0.80), 170,000 / 26 trials, ~22% | A[6]=B[1] | Lancet 376:1670–1681 (PMID 21067804), Baigent/CTT — RR 0.78 (0.76–0.80), 22% per mmol/L | MATCH |
| 3 | B | FOURIER evolocumab: 27,564 pts, primary 11.3→9.8%, HR 0.85 (0.79–0.92), LDL 92→30 (~59%), key-2ndary HR 0.80 (0.73–0.88) | B[8] | NEJM 2017 NEJMoa1615664, Sabatine — all values exact | MATCH |
| 4 | C | Mandsager: 122,007 pts, 13,637 deaths, 8.4y; low-vs-elite HR 5.04 (4.10–6.20); elite-vs-high 0.77 (0.63–0.95) | C[1] | PMC6324439 (fetched) — HR 5.04 (4.10–6.20) and 0.77 (0.63–0.95) verbatim; n/deaths/follow-up exact | MATCH |
| 5 | C | Kodama per-MET RR 0.87 (mortality)/0.85 (CHD-CVD); 33 cohorts; ~7.9 MET boundary | C[2] | JAMA 2009;301(19):2024 (PMID 19454641) — paper, population, ~7.9 MET boundary confirmed; per-MET RR consistent with abstract | MATCH |
| 6 | D | Apple Heart: 419,297 enrolled, 2,161 (0.52%) notified, 450 patches, AF 34%, irregular-pulse PPV 0.84 (95% CI 0.76–0.92) | D[5] | NEJM 2019 NEJMoa1901183, Perez — n, 0.52%, 450, 34%, PPV 0.84 (0.76–0.92) exact | MATCH |
| 7 | D | China-PAR: 21,320 derivation; C-stat 0.794 (0.775–0.814) men / 0.811 (0.787–0.835) women; PCE worse in Chinese men | D[10] | Circulation 2016;134:1430 (PMID 27682885), Yang — C-stats and n exact; PCE worse in men confirmed | MATCH |

7/7 load-bearing claims verified across all four sections; 0 mismatches. count_checked: 7; count_flagged: 0.

## IC-7 Population-Mismatch

Exactly one `[N, animal]` inline cite exists: Section C `[3, animal]` (Holloszy 1967 rat treadmill). The sentence carries `[population-mismatch: rat]` in-sentence AND the species ("rats") is the sentence subject within 100 chars — satisfies the rule (and the override). The numerical token "doubled" is mechanism/background with the species as subject. Zero `[N, in_vitro]` cites exist. checked_citations: 1; flagged_citations: 0.

## IC-8 Route-Extrapolation

All Section B compound dose claims use the route the cited primary tested (oral: statins, ezetimibe, bempedoic acid, antihypertensives, aspirin, icosapent ethyl; subcutaneous: PCSK9 mAbs, inclisiran). No route mismatch between any dose claim and its cited primary. No `[route-extrapolation]` flag is required and none was omitted. No violation detected.

## IC-9 Concentration-Surfacing

Largest single-group cluster share = 0.038 (see Concentration Audit) << 0.70. The gate passes vacuously; no first-class concentration-risk section is required. No violation detected.

## IC-10 Cross-Section ID Concordance (FOLDS Phase 4.25)

Two primary citations appear in ≥2 sections; identifiers compared:

- **SPRINT** — A[5] vs B[12]: both SPRINT Research Group / Wright JT, 2015, NEJM 373(22):2103–2116. A cites PMID 26551272; B cites DOI 10.1056/NEJMoa1511939 (same paper). First-author/year/journal/volume/pages AGREE. HR 0.75 (0.64–0.89) value agrees across sections. CONCORDANT.
- **CTT 2010** — A[6] vs B[1]: both CTT Collaboration / Baigent C, 2010, Lancet 376(9753):1670–1681, PMID 21067804 (B adds NBK79008 — same paper). RR 0.78 (0.76–0.80) agrees across sections. CONCORDANT.

The SCORE2/Pooled-Cohort-Equations and JUPITER/CANTOS/Framingham name overlaps between A and D are narrative cross-references (D §D.5 explicitly defers the threshold/score divergence to Section A) — not duplicate numbered citations; no shared PMID, no discordance. No HALT-class identifier mismatch; no WARN-class tag-discordance. No violation detected.

## IC-11 No Placeholder Strings

Grep for `TBD|TODO|lorem|citation needed|content continues|research suggests|experts believe|according to some reports` across all four sections: no matches. No violation detected.

## IC-12 No Wikipedia / Excluded Sources

Grep for `wikipedia|healthline|medvidi|instagram|tiktok|bodybuilding` across all four bibliographies: no matches. All bibliography hosts are Tier-1 primary (NEJM, Lancet, JAMA, JACC, Circulation, BMJ, Eur Heart J, PMC, PLoS One, Front Neurol, Physiol Rep) or Tier-2 regulatory (FDA accessdata, AHA/ASA). No violation detected.

## IC-13 Per-Citation Corpus Scoping

SKIP-mode (standard mode does not run full per-citation corpus grep). The IC-6 independent web spot-verifies (7 load-bearing claims, 0 mismatches) are the adversarial sample for this dispatch.

## Concentration Audit

Enumerated all distinct PRIMARY citations (tags ∈ {rct, meta_analysis, cohort, open_label, animal, in_vitro}) across all 4 sections, deduplicated cross-section:

- Section A: 19 primaries; Section B: 18; Section C: 11; Section D: 7.
- Cross-section duplicates removed: SPRINT (A5=B12), CTT-2010 (A6=B1).
- **total_primaries = 53.**
- Largest single-group/sponsor cluster: at most 2 citations from any one group — CTT Collaboration (CTT-2010 + CTT-2012-Mihaylova), Ridker (JUPITER + CANTOS), or DeFilippis (2015 + 2017), each = 2.
- **largest_cluster_name = "CTT Collaboration (Baigent/Mihaylova)" (tie with Ridker, DeFilippis at 2 each); largest_cluster_count = 2; share = 0.038.**
- threshold_triggered (≥0.70): false. As expected — the cardiovascular literature is large and multi-group.

## Spot-Verify Summary

7 load-bearing numerical claims independently web-verified across all four sections (≥4 across different sections required); 7/7 MATCH, 0 mismatch:
- A: SPRINT HR 0.75; CTT RR 0.78/mmol/L.
- B: FOURIER 11.3→9.8% HR 0.85, LDL 92→30; CTT RR 0.78 (shared).
- C: Mandsager low-vs-elite HR 5.04 + elite-vs-high 0.77 (PMC fetch); Kodama per-MET RR / 7.9-MET boundary.
- D: Apple Heart PPV 0.84 (0.76–0.92), 419,297/0.52%/450/34%; China-PAR C-stat 0.794 men / 0.811 women.

No fabrication-shaped artifacts found. All verified DOIs/PMIDs resolve to the cited papers with matching first-author, year, and number.

## Verdict

verdict: PASS

halt_reasons: []

warnings: []

All 13 IC checks pass (IC-13 SKIP-mode per standard). Population-mismatch PASS (1 animal cite, correctly flagged + species-subject). Concentration audit PASS (53 distinct primaries, largest cluster share 0.038 << 0.70). Cross-section ID concordance PASS (SPRINT + CTT agree across A/B). 7/7 independent spot-verifies match. No integrity violations, no tag-discordances, no language-economy warnings.
