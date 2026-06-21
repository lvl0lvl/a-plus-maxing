# Gate 4.75 — Citation Integrity Verifier — AOD-9604

Corpus: six per-section drafts (`sections/section-A.md` … `section-F.md`) + `rubric.md`.
Mode: deep. Iteration 1. Verdict: **PASS** (2 WARNs, 0 HALTs).

---

## IC-1 Type-Tag Presence

Every inline citation carries (or is accompanied in-sentence by) a type-tag drawn from the canonical enum. Tags observed across the corpus: `animal` (48), `regulatory` (61), `mechanism_review` (22), `vendor_label` (18), `in_vitro` (6), `practitioner_protocol` (6), `rct` (5), `cohort` (2), `compounding_data_sheet` (1). All map to the enum; no out-of-enum tag found. The sections use a per-sentence parenthetical/backtick tagging convention (e.g. `(animal: obese Zucker rats [3])`, `` `[regulatory] [4]` ``) rather than the strict `[N, tag]` glyph — semantically equivalent and unambiguous; every numbered cite is tagged. PASS.

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry in all six sections carries an explicit type annotation (e.g. "— **animal** (obese Zucker rats)", "— `regulatory`", "— type: rct (conference abstract)"). Multi-purpose entries correctly carry compound tags ("animal + mechanism", "mechanism_review / regulatory", "in_vitro / regulatory (patent)"). All tags in enum. PASS.

## IC-3 Vendor-Not-Numerical

18 `vendor_label` cites, all confined to Section F. Each grounds ONLY: gray-market dosing *convention* (explicitly labeled "convention, not a label", never efficacy/AE-rate), reconstitution math (mL / mg/mL / mcg / U-100 units — IC-3 reconstitution exemption), stability handling, qualitative cost, and gray-market-availability disclosure. The ~300 mcg / 500 mcg / 1000 mcg figures are framed as convention or trial-derived-misattribution-risk, not as efficacy claims. No vendor cite grounds an efficacy %, AE rate, or therapeutic-dose endorsement. PASS.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` cites appear anywhere in the corpus. Vacuously PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

6 `practitioner_protocol` cites (Section F: Empire Medical Training [1], Dr. Dan Wool [5], venue-only clinic pages [3]). All ground dose/route/cycle/admin conventions only. Section F's framing sentence states explicitly: "No practitioner or vendor source in this section grounds any efficacy or adverse-event-rate claim — those are Tier-1 only and live in §B." Efficacy is sourced exclusively to Tier-1/2 (rct/animal/mechanism_review) in §A/B/D. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

1 `compounding_data_sheet` token, and it is a NEGATIVE finding ("Compounding data-sheet search result: NONE FOUND" — no admissible sheet located, with searched-vendor list). No data sheet grounds any efficacy claim. PASS.

## IC-7 Population-Mismatch

Every numerical claim citing an `animal` or `in_vitro` source carries its species/model as the sentence subject within the health-gates §1 override window, and each cite is the sole source for its claim:
- Zucker rats, oral 500 µg/kg/day × 19 days, 15.8 vs 35.6 g [3]/[5]
- C57BL/6J ob/ob mice, 14 days, fat oxidation/glycerol [4]/[6]
- β3-AR knockout mice, chronic vs acute [1]/[7]
- New Zealand white rabbit OA, n=32, intra-articular 0.25 mg [3]
- cynomolgus monkey NOAEL 50 mg/kg/day; rat NOAEL ≥100 mg/kg/day [2]
- in-vitro chondrocyte culture, 100 µg/mL [2]
The human Phase-2b obesity population is never conflated with animal numbers; §B explicitly partitions "Preclinical lipolysis (animal and in vitro) — clearly NOT human fat loss." PASS (override pattern satisfied).

## IC-8 Route-Extrapolation

Routes are labeled at point of use and match the cited sources: oral (Zucker rats; human METAOD003–006), IV (human METAOD001–002; pig PK), intra-articular (rabbit OA), IP (β3-AR mouse study), SC (gray-market convention). The oral/IV-trial vs SC-gray-market route mismatch is explicitly surfaced in §D ("no published human exposure data exist for the subcutaneous… route" [FDA]) and §F (SC convention flagged as not trial-validated). No unflagged route extrapolation grounding a dose recommendation. PASS.

## IC-9 Concentration-Surfacing

Single-lineage share = 100% (≥70% threshold breached). The concentration risk IS surfaced as a first-class, headed subsection ("### Concentration audit") in Section C with an explicit "FLAG (≥70% threshold breached): YES — single-lineage concentration ~100%" and the full enumerated-primary table. PASS at section level. **WARN (synthesis):** in the per-section corpus the audit sits within Section C after the OA indication subsections; at assembly, synthesis should hoist a concentration-risk section to top-level ordering BEFORE the first indication subsection per health-gates §3.2.

## IC-10 No Fabricated Citations

All inline `[N]` resolve to bibliography entries — max inline cite == max bib entry in every section (A 6/6, B 7/7, C 6/6, D 4/4, E 8/8, F 12/12), contiguous, no orphans. Load-bearing PMIDs spot-verified live via NCBI E-utilities esummary — all four resolve with exact title/journal/volume/pages/first-author match:
- 11713213 — Heffernan, *Endocrinology* 142(12):5182-9, 2001 ✓
- 11673763 — Heffernan, *Int J Obes Relat Metab Disord* 25(10):1442-9, 2001 ✓
- 11146367 — Ng FM, *Horm Res* 53(6):274-8, 2000 ✓
- 26275694 — Kwon DR, *Ann Clin Lab Sci* 45(4):426-32, 2015 ✓
Stier 2013 (DOI 10.4021/jem157w) and Moré 2014 (DOI 10.14740/jem213w) — non-PubMed journal (J Endocrinol Metab); DOIs resolve 302→jofem.org and the cited article URLs return HTTP 200. US Patent 10,111,933 B2 (Google Patents) returns 200. The unverifiable 2020 "Joint Dis Relat Surg" human-OA paper was correctly OMITTED per verify-or-omit. No fabricated citation. PASS.

## IC-11 No Placeholder Strings

Grep for `[citation needed] | TBD | TODO | Content continues | according to some reports | research suggests | experts believe` across all sections: zero matches. PASS.

## IC-12 No Wikipedia Citations

No `*.wikipedia.org` URL appears in any bibliography. The only "wikipedia" string occurrences are self-check assertions ("No Wikipedia used"; "no Wikipedia, no vendor/anecdote grounding numbers") in §C/§E — these are negative compliance statements, not citations. PASS.

## IC-13 Per-Citation Corpus Scoping

Deep-mode sample: load-bearing numerical/quoted claims grep-verified against retrieved PubMed corpora (cached at `corpus/`):
- Ng 2000: "500 microg/kg", "19 days", "15.8 ± 0.6 vs 35.6 ± 0.8", ">50%", "no adverse effect on insulin sensitivity", "orally usable and safe therapeutic agent for obesity" — all MATCH.
- Heffernan IJO 2001: "does not compete for the hGH receptor", "did not induce hyperglycaemia", "14 days", "glycerol" — all MATCH (after whitespace normalization of wrapped lines).
- Heffernan Endo 2001: "not mediated directly through the beta(3)-AR", "increasing energy expenditure and fat oxidation in the beta(3)-AR knock-out mice" (acute), "β3-AR RNA expression restored toward lean" — all MATCH.
- Kwon&Park 2015: "n=32", "0.25 mg AOD9604", "6 mg HA", four-arm design, "combined AOD9604 and HA more effective than either alone", "Group 4 lameness significantly shorter" — all MATCH.

**One corpus-missing WARN:** the §C specific lameness numbers "11 ± 4 days (combination) vs 25 ± 2 days (control)" are full-text-only; not present in the PubMed abstract (paywall full-text). The qualitative direction (Group 4 lameness significantly shorter than control) IS confirmed in the abstract. Per IC-13/corpus-scoping policy, paywalled full-text = `corpus-missing` WARN, not HALT. The §B 12-week conference-abstract figures (~2.6–2.8 kg vs ~0.8 kg placebo, Herd 2005) are sourced to a non-PubMed-indexed conference abstract, correctly tagged lower-tier and abstract/metadata-only — also corpus-limited, not a fabrication. PASS with WARN.

---

## CRITICAL discipline checks (entry-specific)

- **(a) FAILED-Phase-2b discipline — HELD.** "No proven human fat-loss efficacy" in §B BLUF, body, and verdict; preclinical lipolysis explicitly partitioned as "clearly NOT human fat loss." No preclinical-as-proven-human-fat-loss leakage.
- **(b) No-IGF-1 / GH-axis-sparing — VERIFIED.** §A and §D ground it in primary data: GHR non-binding/no proliferation (quoted), "no significant change in the levels of IGF-1 in any of the treatment groups," no glucose/insulin impairment. Labeled VERIFIED/CONFIRMED with cites.
- **(c) Paradigm-OA = pentosan-NOT-AOD — correctly EXCLUDED.** §C explicitly flags the conflation, identifies Paradigm's asset as injectable pentosan polysulfate (iPPS/Zilosul), states AOD-9604 has no Phase II human OA program, and excludes the Paradigm data as out of scope.
- **(d) Supplement status NOT overstated.** §E states self-affirmed GRAS is industry-side, "not an FDA approval, not a drug approval," and not a lawful US dietary ingredient under DSHEA drug-exclusion.
- **(e) WADA prohibited (S0/S2) — confirmed.** §E documents S0 catch-all (WADA-confirmed 2013) and S2 GH-fragment scope; Essendon/CAS saga anchored.

## Concentration audit (honest report)

Single-lineage (Monash/Ng → Metabolic Pharmaceuticals) share = 5/5 distinct primaries = **100%**. threshold_triggered = true. This is the expected ceiling — AOD-9604 is essentially one company's molecule; even the one independent investigator group (Kwon/Park) used sponsor-supplied drug substance. Surfaced as a first-class subsection in §C. Reported honestly, no HALT (surfacing requirement met).

## Verdict

verdict: PASS
halt_reasons: []
warnings: [IC-9, IC-13]

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":169,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":18,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":0},"IC-5":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":1},"IC-7":{"status":"PASS","count_checked":7,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":12,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","count_checked":0,"count_flagged":0},"IC-13":{"status":"PASS","count_checked":18,"count_flagged":0}},"population_mismatch":{"verdict":"PASS","checked_citations":7,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":5,"largest_cluster_name":"Metabolic Pharmaceuticals / Monash","largest_cluster_count":5,"share":1.0,"threshold_triggered":true,"surfaced_section_heading":"Concentration audit (Section C)"},"corpus_scoping":{"verdict":"PASS","claims_checked":18,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-9: concentration-risk surfaced as Section-C subsection; at synthesis hoist to top-level section before first indication per health-gates §3.2","IC-13: Kwon&Park lameness numbers 11±4 vs 25±2 days are full-text-only (paywall) corpus-missing — qualitative direction verified in abstract; Herd 2005 12-week figures are non-PubMed conference-abstract, correctly lower-tier-tagged"]}
```
