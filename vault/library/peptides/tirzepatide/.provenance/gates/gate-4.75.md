# Gate 4.75 — Citation Integrity Verifier — Tirzepatide

Mode: deep. Corpus: six sibling sections A–F (`/tmp/aplus-research/tirzepatide/sections/section-{A..F}.md`) + rubric.md. IC-1..IC-13 + population_mismatch + concentration_audit + corpus_scoping executed. PMID resolution performed live via NCBI E-utilities (esummary + efetch).

## IC-1 Type-Tag Presence
Every inline `[N, <tag>]` / `[<tag>]` / `[type: <tag>]` token resolves to the canonical enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). Tag inventory: regulatory (60), mechanism_review (36), rct (26 + 14 `type: rct` + 9 `type: rct, Tier-1` + 3 `rct, Tier-1`), practitioner_protocol (9 + qualified variants), in_vitro (8), cohort (6), vendor_label (1 + 1 qualified), animal (1, `animal (mouse, n not stated)`), anecdote_aggregate (1), plus compound tags (`regulatory/mechanism_review`, `regulatory/rct`). All in-enum; compound/qualified annotations (Tier-N, parentheticals, em-dash scope notes) are acceptable composite tags. No off-enum tag detected.

## IC-2 Bibliography Type-Tag Presence
Every bibliography entry across A–F carries a `[type: ...]` / `[<tag>]` annotation. Section A entries [1]–[5], B [1]–[9], C [1]–[7], D [1]–[6], E [1]–[12], F [1]–[12] all annotated. Multi-purpose composite tags present and acceptable. PASS.

## IC-3 Vendor-Not-Numerical
One `vendor_label` inline cite (section-F line 21): "Dosing-error risk is elevated with multi-dose vials and 'units'/mg conversions versus the fixed-dose pens. `[vendor_label]` (dose/format caution only)". No efficacy/AE-rate/therapeutic-dose number in the sentence — it grounds only a format/dose-handling caution, the permitted use. Bibliography [6] vendor_label entry grounds only qualitative cost (~$1,000+/28d) and format caution, not efficacy. PASS.

## IC-4 Anecdote-Not-Numerical
One `anecdote_aggregate` cite (section-E line 48), co-tagged with `regulatory`, grounds the qualitative cost/access narrative ("on the order of roughly a thousand dollars per month"). The figure is explicitly hedged ("pricing figures vary by source and over time and are not anchored to a primary regulatory document here") and is a list-price order-of-magnitude, not an efficacy/AE rate or dose recommendation. No AE rate, dose recommendation, or effect size attached to the anecdote tag. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy
9 `practitioner_protocol` cites, all in section-F. The numerically-loaded ones (line 27: SURMOUNT-1 DXA "~75% fat / ~25% lean", −5.6 kg / −10.9%; line 23 cost tiers) are body-composition/cost CONTEXT. Section F opens with an explicit tier disclaimer: "nothing in this section grounds efficacy or adverse-event rates — those remain owned by Tier-1 controlled-trial evidence elsewhere." The load-bearing lean-mass efficacy/AE numbers are independently owned in section-D line 19 with `[rct]` tag citing Look 2025 (PMID 39996356, verified). No practitioner_protocol cite is the SOLE source of an efficacy claim. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy
No `compounding_data_sheet` tag present anywhere in the corpus. Vacuously PASS. No compounding-pharmacy data-sheet citations were used (consistent with an FDA-approved drug whose dosing is owned by the labels).

## IC-7 Population-Mismatch
One `animal` cite (section-A line 44): "central (intracerebroventricular) co-delivery of GIP and GLP-1 additively enhanced weight loss in mice [5] [animal (mouse, n not stated)]." Species ("mice") is the subject of the sentence within the override window; the claim is qualitative ("additively enhanced weight loss"), carrying no human dose/AE/effect-size number — the §1 override applies (species-as-subject, mechanism/background context). No `in_vitro` numerical claim mis-generalizes to human dose: the in_vitro cite [4] (Willard 2020) grounds binding-affinity/cAMP/β-arrestin pharmacology with the receptor system explicitly the subject. PASS. (Broader population annotation — T2D vs non-diabetic obesity vs OSA vs HFpEF — handled under population_mismatch below.)

## IC-8 Route-Extrapolation
All dose claims are subcutaneous once-weekly, matching the tested route of every cited trial and both labels. The only "oral"/"intravenous" tokens (section-A line 23) refer to the incretin-effect physiology definition (oral vs IV glucose), not a tirzepatide dose-route extrapolation. No route mismatch; no `[route-extrapolation]` tag required. PASS.

## IC-9 Concentration-Surfacing
Single-sponsor (Eli Lilly) share ≥ 0.70 (computed ≈0.95 — see concentration_audit). The corpus surfaces the concentration risk as a first-class, explicitly-headed subsection ("### Concentration / sponsor audit", section-C line 51) AND flags it in the section-C title ("...+ concentration audit"), with prose "single-sponsor evidence base, a notable concentration risk" + honest mitigating factors. The risk is NOT buried-in-bibliography (the HALT condition). NOTE (WARN): in this section-level corpus the audit sits at the end of section C, AFTER the OSA/CV/HFpEF/MASH indication subsections, rather than strictly before the first indication subsection. Because the corpus is six independent section files (pre-assembly), the strict before-first-indication ORDERING is an assembly-phase concern; the disclosure itself is present, salient, and first-class. WARN (ordering), not HALT.

## IC-10 No Fabricated Citations
All load-bearing PMIDs resolved live via NCBI esummary and matched bibliography (first author + year + journal): SURMOUNT-1 Jastreboff 2022 NEJM (35658024) ✓; SURPASS-2 Frías 2021 NEJM (34170647) ✓; SURMOUNT-OSA Malhotra 2024 NEJM (38912654) ✓; SURMOUNT-4 Aronne 2024 JAMA (38078870) ✓; SURPASS-CVOT Nicholls 2025 NEJM (41406444) ✓. Also verified: Sun 2022 PNAS (35333651), Schneck 2024 (38356317), Willard 2020 JCI Insight (32730231), Liu 2024 (39114288), Rosenstock SURPASS-1 (34186022), Ludvik SURPASS-3 (34370970), Del Prato SURPASS-4 (34672967), Dahl SURPASS-5 (35133415), Garvey SURMOUNT-2 (37385275), Wadden SURMOUNT-3 (37840095), Packer SUMMIT (39555826), Loomba SYNERGY-NASH (38856224), Cheskin (39348697), Borlaug (39551891), Kramer (39566869), Look (39996356), Kindel (39370500), Zhao SURMOUNT-CN (38819983). 24/24 resolve; 0 fabricated. The FDA labels are cited via DailyMed setids (Mounjaro d2d7da5d..., Zepbound 487cd7e7...) — resolvable label IDs. PASS.

## IC-11 No Placeholder Strings
Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe` → no matches across A–F. PASS.

## IC-12 No Wikipedia Citations
Grep for `wikipedia` (any TLD) across all six sections → ZERO matches in body or bibliographies. PASS (no HALT).

## IC-13 Per-Citation Corpus Scoping
Deep-mode sample of load-bearing numerical claims grep-verified against fetched source abstracts (cached `/tmp/aplus-research/tirzepatide/corpus/`):
- SURMOUNT-1 (35658024): −15.0/−19.5/−20.9% weight, n=2539 → all matched in abstract ✓
- SURPASS-2 (34170647): n=1879, HbA1c −2.01/−2.30, "noninferior" + "superior" vs semaglutide → matched ✓
- SURMOUNT-OSA (38912654): AHI treatment diff −20.0/−23.8 events/hr, 52 weeks, "apnea-hypopnea" → matched ✓
- SURMOUNT-4 (38078870): 14.0% regain on placebo, +5.5% continued, n=670, "regain" → matched ✓
- SURPASS-CVOT (41406444): n=13,299, HR 0.92, "noninferior" → matched ✓
0 quote-not-found, 0 number-not-found. corpus-missing WARN: fda.gov pages (E[10], F[5]) are bot-blocked to direct fetch — explicitly disclosed in-text ("fda.gov page blocked direct WebFetch"); agents substituted DailyMed/eutils/secondary regulatory summaries. Per IC-13 policy paywall/bot-block = WARN, not HALT. PASS (with corpus-missing WARN on bot-blocked fda.gov).

## Population-Mismatch (health-gates §1 — over-generalization sweep)
Every weight/glycemic figure is population-annotated and the corpus actively guards against the T2D-vs-obesity conflation: section-B line 3 ("must not be conflated… every figure below is annotated by population"); SURMOUNT-1 figures tagged "obesity but WITHOUT diabetes"; SURMOUNT-2 explicitly framed as "the critical population contrast" with the attenuation (≈14.7% T2D vs ≈20.9% non-diabetic) attributed to "a population effect, not a dosing difference." OSA figures scoped to "obese adults with moderate-to-severe OSA"; HFpEF to "HFpEF + obesity"; CVOT to "T2D + established ASCVD." No cross-population over-generalization detected. PASS.

## Concentration-Audit (health-gates §3 — single-sponsor)
Distinct deduplicated primaries (type ∈ rct/cohort/in_vitro/animal), substudies/same-trial-summaries deduped to parent trial:
- Eli Lilly cluster (18): SURPASS-1..5 (5), SURMOUNT-1/-2/-3/-4 (4), SURMOUNT-OSA, SURPASS-CVOT, SUMMIT, SYNERGY-NASH (4), Look 2025 DXA, SURMOUNT-CN, SURMOUNT-J, Schneck/Urva PK, Willard in_vitro (5) = 18, all Lilly-sponsored/-affiliated.
- Non-Lilly (1): the ICV mouse GIP+GLP-1 co-delivery preclinical work cited via the Liu review [animal].
Total distinct primaries = 19; largest cluster (Eli Lilly) = 18; share = 18/19 ≈ 0.95. threshold_triggered = true (≥0.70), EXPECTED for an approved single-manufacturer drug. Surfaced honestly in "### Concentration / sponsor audit" (section-C) with explicit single-sponsor caveat + mitigating factors (tier-1 peer review, objective adjudicated endpoints, active-comparator design) + the caution that even the comparator (dulaglutide) is a Lilly product. PASS (caveat surfaced, not buried).

## Corpus-Scoping (IC-13 retrieval coverage)
Numerical-claim retrieval succeeded for all spot-checked Tier-1 trial abstracts. Only corpus-missing: bot-blocked fda.gov pages — disclosed in-text, substituted by DailyMed label setids + eutils + secondary regulatory summaries (acceptable per CALIBRATION). WARN, not HALT.

## Verdict
verdict: PASS

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":196,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":2,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":1},"IC-5":{"status":"PASS","count_checked":9,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":0},"IC-7":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"WARN"},"IC-10":{"status":"PASS","count_checked":24,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","count_checked":0,"count_flagged":0},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":35,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":19,"largest_cluster_name":"Eli Lilly (sponsor)","largest_cluster_count":18,"share":0.95,"threshold_triggered":true,"surfaced_section_heading":"Concentration / sponsor audit"},"corpus_scoping":{"verdict":"PASS","claims_checked":24,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-9: concentration audit surfaced first-class but positioned after indication subsections within section-C (pre-assembly section-level corpus); strict before-first-indication ordering deferred to assembly phase","IC-13/corpus_scoping: fda.gov pages bot-blocked to direct fetch (E[10], F[5]); disclosed in-text, substituted with DailyMed/eutils/secondary regulatory — corpus-missing WARN, not HALT","concentration_audit: single-sponsor (Eli Lilly) share ~0.95, threshold_triggered=true as EXPECTED for an approved single-manufacturer drug; surfaced honestly"]}
```
