# Phase 4.75 Integrity Gate — Ipamorelin (iter-2)

## Verdict

verdict: PASS

Re-run after the IC-12 fix. The prior HALT (Section D bibliography [5] = Wikipedia URL) is resolved: [5] removed, D bibliography now has 4 entries [1]–[4], the discontinuation/non-approval claims (D-4, D-5) are re-grounded on the ClinicalTrials.gov registry records [3][4] + Beck 2014 RCT [1], no dangling [5] in the live body, no Wikipedia URL anywhere in any live section. All 13 IC checks plus population-mismatch, concentration-audit, and corpus-scoping PASS (IC-13 carries 2 paywall corpus-missing WARNs — tolerated, not a HALT). No new HALT introduced by the fix.

(Per directive: each file's `## Post-fix grep audit` block legitimately quotes the now-removed Wikipedia URL and old strings for documentation; those blocks are excluded from all live-content checks below.)

---

## IC-1 — Type-Tag Presence

status: PASS (count_checked = 41 distinct inline cite-instances; count_flagged = 0)

Every inline `[N, tag]` carries a tag from the canonical enum. Compound slash-tags (`animal/in_vitro`, `open_label/rct`, `animal/ex_vivo`, `rct/animal`, `mechanism_review/animal`, `regulatory/vendor`) decompose into enum members. Species/route suffixes after `;` are annotations, not tags; the grounding tag precedes the `;`. Grouped back-references in §E/§F monitoring prose (`[3,4]`, `[5,6]`, `[8,9,10,12]`) point to already-tagged sources and assert no new efficacy claim. No untagged inline citation.

## IC-2 — Bibliography Type-Tag Presence

status: PASS

Every bibliography entry across §A–§F carries `tag=` from the enum (multi-tag entries `tag=animal+in_vitro`, `tag=mechanism_review/animal`, `tag=regulatory/vendor` admissible). No entry lacks a tag. §D now has 4 entries, each tagged ([1] rct, [2] open_label, [3] rct, [4] rct).

## IC-3 — Vendor-Not-Numerical

status: PASS (count_checked = 6 vendor_label cite-instances; count_flagged = 0)

`vendor_label` cites ([6],[7] in §F; [6] in §A) ground only physical description (white/off-white powder), salt form (acetate), vial sizes, gray-market pricing, CAS/formula/MW identity, and reconstitution/storage math. No vendor cite shares a sentence with an efficacy, AE-rate, or therapeutic-dose claim. §A explicitly: "Vendor cite supports physical description only; not used to ground any numeric pharmacology value."

## IC-4 — Anecdote-Not-Numerical

status: PASS (count_checked = 0)

No `anecdote_aggregate` cites anywhere. Vacuously satisfied.

## IC-5 — Practitioner-Protocol-Not-Efficacy

status: PASS (count_checked = 2 practitioner_protocol cite-instances; count_flagged = 0)

`practitioner_protocol` cites ([13] Wittmer, [14] Optimal Clinic) ground only dose/cycle/route conventions (~100–300 mcg SC nightly, CJC-1295 stacking, cycle length). §F states: "These are clinic/community conventions, not regulatory-sanctioned dosing; no human efficacy is asserted from them." No practitioner cite is the sole source of an efficacy claim.

## IC-6 — Compounding-Data-Sheet-with-Efficacy

status: PASS (count_checked = 0)

No `compounding_data_sheet` cites present (§F: "No admissible compounding-pharmacy data sheet for ipamorelin was located"). Vacuously satisfied.

## IC-7 — Population-Mismatch

status: PASS (checked_citations = 13; count_flagged = 0)

Every numerical claim citing an `animal`/`in_vitro` source names its species in-sentence (rat / Sprague-Dawley rat / swine·pig / dog / primary rat pituitary cells) or carries `species=`. The keystone selectivity claim (no ACTH/cortisol/prolactin co-release, ">200× ED50") is `[1, animal]` with "In rats" / "rats and swine" in-sentence; §A/§B gaps explicitly flag it as animal-supported, NOT human-proven. No unflagged population mismatch.

## IC-8 — Route-Extrapolation

status: PASS

The canonical "~2 h half-life" human PK is tagged IV-infusion-derived (`[4, open_label; route=IV infusion]`). §A carries a first-class ROUTE NOTE: SC PK is "an extrapolation from IV human + animal data, not directly measured." IV→SC mismatch surfaced, not silently extrapolated. Animal PK claims carry `route=` (IV / intranasal). No unflagged route extrapolation.

## IC-9 — Concentration-Surfacing

status: PASS

Single-lineage (Novo Nordisk-origin) share of in-vivo efficacy primaries = ~80% (4 of 5; only the 2014 Beck human RCT is independent — and it failed). Threshold ≥70% triggered. Surfaced FIRST-CLASS: §F's opening content section is "## Concentration audit (dominant labs; estimated single-lab share + method)" (first heading after the title, before any sourcing/prescribing/indication subsection), with explicit "FLAG: single-lineage dominance ≥70% — confirmed." Surfaced ⇒ PASS.

## IC-10 — No Fabricated Citations

status: PASS (count_checked = 10; count_flagged = 0)

Spot-verified PMIDs resolve exactly to cited title/author/journal/year (PubMed E-utilities): 9849822 (Raun, Eur J Endocrinol 1998), 10496658 (Gobburu, Pharm Res 1999), 25331030 (Beck, Int J Colorectal Dis 2014), 10828840 (Svensson, J Endocrinol 2000), 10373343 (Johansen, Growth Horm IGF Res 1999), 24651458 (Yin, Int J Mol Sci 2014), 17227934 (Liu, Ann Intern Med 2007), 20472501 (Key/EHBCCG, Lancet Oncol 2010), 26042199 (Müller, Mol Metab 2015), 19289567 (Venkova, J Pharmacol Exp Ther 2009). No inline `[N]` lacks a bibliography entry. No fabricated citation.

## IC-11 — No Placeholder Strings

status: PASS

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`, `lorem ipsum`: no matches in the live corpus.

## IC-12 — No Wikipedia Citations

status: PASS (count_checked = all live bibliography + inline cites across §A–§F; count_flagged = 0)

**Prior HALT RESOLVED.** Live-body verification (each file's `## Post-fix grep audit` block excluded, per directive):
- `grep -in "wikipedia"` over live bodies of §A–§F → 0 matches. (All "wikipedia" hits in §D lines 92–113 are inside the Post-fix grep audit block, which documents the *removed* URL and is excluded.)
- §D bibliography now enumerates exactly **4** entries: [1] Beck 2014 (rct), [2] Gobburu 1999 (open_label), [3] NCT00672074 (rct, ClinicalTrials.gov), [4] NCT01280344 (rct, ClinicalTrials.gov). No `[5]` bibliography entry.
- No dangling inline `[5` / `[5,` token in §D's live body (the only `[5]` in the corpus is §F's legitimate Beck-2014 entry, a different and valid source; §F has 14 entries).
- The discontinuation/non-approval claims (D-4, D-5) are re-grounded on `[1, rct]` (Beck failed primary endpoint) + `[3, rct]` (NCT00672074 registry, hasResults=false) + `[4, rct]` (NCT01280344 registry, hasResults=false, no positive efficacy publication) — all non-Wikipedia. The remaining bibliography URLs in §D are both clinicaltrials.gov registry records.

No Wikipedia URL in any live bibliography or inline citation anywhere in the corpus.

## IC-13 — Per-Citation Corpus Scoping

status: WARN (claims_checked = 6; quote-not-found = 0; number-not-found = 0; corpus-missing = 2)

Load-bearing numerical claims spot-verified against retrieved source abstracts:
- Beck 2014 [25331030]: primary endpoint NOT met (25.3 vs 32.6 h, p=0.15); n=114 mITT / 117 enrolled — abstract confirms verbatim. MATCH (§D-3, §F[5]).
- Gobburu 1999 [10496658]: t½ ~2 h, CL 0.078 L/h/kg, Vss 0.22 L/kg, SC50 214 nmol/L, 8/dose — abstract confirms. MATCH (§A-8/9, §B-9, §D-2).
- Raun 1998 [9849822]: title/selectivity + potency values (EC50 1.3 nmol/L; rat ED50 80 nmol/kg; swine 2.3 nmol/kg) corroborated.
- Svensson 2000 [10828840] + Venkova 2009 [19289567]: PMIDs resolve to exact cited titles/journals/years (efetch).

corpus-missing WARNs (paywall, per sources' own notes — NOT a HALT per IC-13 policy):
- §F [4] glucocorticoid-induced-bone-loss 2001 (ScienceDirect full text 403 / paywalled).
- §C [2] / §F [3] Svensson 2000 full text paywalled (PMID resolves; abstract figures corroborated via search).

No quote-not-found, no number-not-found. corpus_scoping verdict = PASS with 2 WARNs.

---

## Population / Concentration / Corpus

**Population-mismatch:** PASS. 13 animal/in_vitro numerical citations checked; 0 unflagged. Every animal numerical claim names species in-sentence; animal→human selectivity extrapolation explicitly flagged in §A/§B gaps.

**Concentration-audit:** PASS. total_primaries = 5; largest cluster = Novo Nordisk lineage, count = 4; share ≈ 0.80; threshold (≥70%) triggered = true; surfaced first-class under "Concentration audit (dominant labs; estimated single-lab share + method)" as §F's opening content section, before the first indication/sourcing subsection. Surfaced ⇒ PASS.

**Corpus-scoping:** PASS (with 2 corpus-missing WARNs). 6 load-bearing numerical claims abstract-verified; 0 quote-not-found; 0 number-not-found; 2 paywalled primaries = corpus-missing WARN.

---

## Structured verdict

```json
{"phase":"4.75","verdict":"PASS","timestamp":"2026-06-20T16:50:06.828415+00:00","iterations":2,"ic_checks":{"IC-1":{"status":"PASS","count_checked":41,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":0},"IC-5":{"status":"PASS","count_checked":2,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":0},"IC-7":{"status":"PASS","count_checked":13,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":10,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","findings":["Prior IC-12 HALT resolved: Section D bibliography [5] (en.wikipedia.org/wiki/Ipamorelin) removed; D bibliography now 4 entries [1]-[4]; no dangling [5] in D live body; D-4/D-5 re-grounded on [1]+[3]+[4] (Beck RCT + 2 ClinicalTrials.gov registry records); grep 'wikipedia' over all live section bodies (Post-fix grep audit blocks excluded) = 0 matches."],"count_checked":1,"count_flagged":0},"IC-13":{"status":"WARN","findings":["6 load-bearing numerical claims spot-verified (Beck 2014 25.3/32.6h p=0.15 n=114; Gobburu t1/2 2h, CL 0.078, Vss 0.22, SC50 214; Raun potency; Svensson + Venkova PMIDs resolve) — all MATCH.","corpus-missing (paywall, WARN not HALT): glucocorticoid-bone 2001 (§F[4], ScienceDirect 403) and Svensson 2000 (§C[2]/§F[3], paywalled full text)."]}},"population_mismatch":{"verdict":"PASS","checked_citations":13,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":5,"largest_cluster_name":"Novo Nordisk","largest_cluster_count":4,"share":0.8,"threshold_triggered":true,"surfaced_section_heading":"Concentration audit (dominant labs; estimated single-lab share + method)","surfaced_before_first_indication":true},"corpus_scoping":{"verdict":"PASS","claims_checked":6,"claims_failed":[{"claim":"ipamorelin counteracts glucocorticoid-induced decrease in bone formation (Growth Horm IGF Res 2001)","cite_key":"glucocorticoid-bone-2001","failure_mode":"corpus-missing","grep_command":"WebFetch ScienceDirect S1096637401902394","grep_output":"403 paywalled — full text not retrievable; bibliographic listing verified"},{"claim":"ipamorelin 0.5 mg/kg/day continuous SC increased tibial/vertebral BMC (Svensson 2000)","cite_key":"svensson-2000","failure_mode":"corpus-missing","grep_command":"efetch PMID 10828840 + journal full text (J Endocrinol 165:569)","grep_output":"PMID 10828840 resolves to exact cited title/journal/year; full text paywalled, abstract figures corroborated via search"}]},"halt_reasons":[],"warnings":["IC-13: 2 corpus-missing (paywalled primaries: glucocorticoid-bone 2001, Svensson 2000) — WARN not HALT per IC-13 policy.","corpus_scoping.claims_failed entries are corpus-missing (paywall) WARNs, not quote/number-not-found failures."],"attestation_chain":{"iter_start_ts":"2026-06-20T16:43:37.131910+00:00","attest_ts":"2026-06-20T16:50:06.828415+00:00","iteration":2,"agent_source_path":".claude/skills/aplus-research/references/citation-integrity.md","agent_source_sha256":"25d90d756057f7f9d68a89a930f8d90095a0126a67e58044e4fa371aa92d1e06","agent_source_mtime":"2026-06-19T12:12:42.101696+00:00"}}
```
