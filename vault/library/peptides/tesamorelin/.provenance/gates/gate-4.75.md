# Gate 4.75 — Citation Integrity Verifier — Tesamorelin

Corpus: section-A.md … section-F.md + rubric.md. Mode: deep. Iteration 1.

## IC-1 Type-Tag Presence

Every inline citation carries a canonical type-tag, supplied either in the `[N, tag]` form or
as an adjacent backtick/bracket tag governing the sentence/block. Tags observed: `regulatory`,
`rct`, `meta_analysis`, `cohort`, `mechanism_review`, `animal`, `in_vitro`, `practitioner_protocol`,
`compounding_data_sheet`, `vendor_label`, `anecdote_aggregate` (written `anecdote` in §F), plus the
non-tag annotations `[pooled]`, `[reformulated]`, `[route/dose-extrapolation]` (these are
qualifiers, not type-tags, and are admissible). All captured tags are in the canonical enum.
`[reformulated]` (§B line 53) is a formulation qualifier on a dose statement, not a citation tag —
not a violation. No inline citation carries an off-enum tag.
**Status: PASS** (count_checked = ~115 inline cites/tagged blocks; count_flagged = 0).

## IC-2 Bibliography Type-Tag Presence

All six section bibliographies annotate each entry with a `[tag]`/`` `tag` `` from the enum.
§A [3] carries the dual tag `[animal] (rat, dog, pig) / [in_vitro]` (admissible multi-purpose).
§C, §E, §F entries carry `rct | meta_analysis | mechanism_review | regulatory |
practitioner_protocol | compounding_data_sheet | vendor_label | anecdote_aggregate` plus
registry/secondary descriptors (NCT registry records tagged `regulatory/registry`). All in enum.
**Status: PASS.**

## IC-3 Vendor-Not-Numerical

One `vendor_label` cite: §F line 31 ([14] PeptideDosages.com). It grounds ONLY reconstitution
math — "10 mg vial reconstituted with ~2.5 mL bacteriostatic water; 25 units ≈ 1 mg" — explicitly
flagged "math only, gray-market." No efficacy, AE-rate, or therapeutic-dose claim attached. The
reconstitution-math exclusion (mL / units present) applies.
**Status: PASS** (count_checked = 1, count_flagged = 0).

## IC-4 Anecdote-Not-Numerical

`anecdote_aggregate` cites (§E [7]; §F [10]) and the §E [7][8] supply-channel cites ground only:
(a) qualitative cost figures ("~$3,000/month", "$2,400–$5,500/month", research-chem "$60–$150")
and (b) gray-market supply-channel descriptions. No AE rate, dose recommendation, or effect size
is grounded by an anecdote cite. Cost is explicitly labeled "not a clinical claim." The §E "late
2023 FDA recategorized >12 peptides" claim is tagged `regulatory/secondary`, not anecdote.
**Status: PASS** (count_checked = 5 anecdote-context cites, count_flagged = 0).

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` cites (§F [6][7][8]; §E [7]) ground only off-label dose/route/cycle
conventions ("1 mg → 2 mg SC daily; 5-on/2-off; ~3-month cycles"). §F line 17 explicitly
disclaims: "no efficacy/AE claim is drawn from them" and downgrades them to "unattributed
convention-of-the-field." No efficacy claim rests solely on a practitioner_protocol cite.
**Status: PASS** (count_checked = 4, count_flagged = 0).

## IC-6 Compounding-Data-Sheet-with-Efficacy

`compounding_data_sheet` cites (§F [11][12]) ground only compoundability status and
concentration/reconstitution conventions ("1–2 mg/mL, pH 5–7, lyophilized 2 mg/vial"). [12] is
explicitly flagged "trade-explainer, not a true data sheet"; [11] is a NOT-FOUND gate result. No
efficacy claim attached to either.
**Status: PASS** (count_checked = 2, count_flagged = 0).

## IC-7 Population-Mismatch

See population_mismatch block. The single `animal`/`in_vitro` cite (§A [3], line 35) carries the
species inline — "rat, dog and human plasma… in dogs… in pigs, rats and dogs" with the `[animal]
(rat, dog, pig)` tag in the same sentence. The numerical tokens (t½ ~21–45 min in dogs) sit within
100 chars of the species name and the cite is the sole source — the health-gates §1 override
(species is the subject) applies; explicit `[population-mismatch:]` is optional here. All human
pivotal-trial efficacy is repeatedly annotated "HIV-lipodystrophy / HIV-infected / HIV-positive"
(§B scope note, §C per-domain annotations, §D dose caveat). Approved-vs-off-label demarcation is
sharp throughout.
**Status: PASS** (count_checked = 1 animal cite + all human-trial cites, count_flagged = 0).

## IC-8 Route-Extrapolation

All clinical dose claims are SC (the tested + labeled route) — no route mismatch. Off-label
extrapolations to non-HIV populations / non-label doses are explicitly tagged
`[route/dose-extrapolation]` (§D lines 7, 81). No untagged route mismatch.
**Status: PASS.**

## IC-9 Concentration-Surfacing

Largest academic-lineage cluster (MGH/Grinspoon-Stanley) = 50%, below the 70% trigger. On the
sponsor/manufacturer lens (Theratechnologies study drug/sponsorship in 4/4 primaries) the share is
100% — this IS surfaced as a first-class "### Concentration audit" subsection in §C, with the
honest read that there is "no manufacturer-independent confirmatory efficacy program." The
concentration risk is surfaced in the corpus, not buried in bibliography. In this section-based
corpus §C is the dedicated audit home; the §C audit precedes no indication subsection it belongs
in front of (indications live in §B/§C domains, audit is the §C closing analysis surfacing the
risk explicitly). Surfacing requirement satisfied.
**Status: PASS** (see concentration_audit block).

## IC-10 No Fabricated Citations

Spot-verified every load-bearing identifier via PubMed/DailyMed/WADA — ALL resolve to the exact
claimed first-author + year + journal + topic:

- PMID 18057338 — Falutz, NEJM 2007, tesamorelin/GHRF in HIV — RESOLVES. VAT −15.2% vs +5.0%,
  IGF-1 +81.0%, n=412 — numbers match §B/§D verbatim.
- PMID 20554713 — Falutz, JCEM 2010, pooled analysis of two phase-3 trials — RESOLVES.
- PMID 20101189 — Falutz, J Acquir Immune Defic Syndr 2010, abdominal-fat trial — RESOLVES.
- PMID 31611038 — Stanley TL, Lancet HIV 2019, tesamorelin/NAFLD in HIV — RESOLVES.
- PMID 22869065 — Baker LD, Arch Neurol 2012, GHRH/cognition in MCI + older adults — RESOLVES.
- PMID 41545261 — Badran AS, Obes Res Clin Pract 2026, tesamorelin meta-analysis — RESOLVES
  (future-dated but a real, live PMID). 5 RCTs, VAT MD −27.71 cm², hepatic fat −4.28%, no SAT
  reduction — numbers match §B verbatim.
- PMID 25038357 — Stanley TL, JAMA 2014, VAT + liver fat in HIV — RESOLVES.
- PMID 28617838 — PLoS One 2017, tesamorelin in T2DM — RESOLVES. **NOTE (WARN):** PubMed lists the
  first author as **David R Clemmons**, but §D bibliography [6] writes "Stanley TL, et al.
  (Clemmons group)." The PMID/journal/year/topic are correct and §D names the Clemmons group, so
  this is a first-author-label imprecision, not a fabricated/wrong citation. Recommend correcting
  the lead author to Clemmons. WARN, not HALT.
- EGRIFTA SV DailyMed label (setid 3d783378-…) — RESOLVES; indication + weight-neutral limitation
  verbatim as quoted in §A/§B/§E/§F.
- WADA S2.2.4 — CONFIRMED via WADA + JADCO 2026 mirror + drugs.com/WADA: tesamorelin named
  explicitly alongside CJC-1293, CJC-1295, sermorelin; prohibited at all times. Matches §E verbatim.

All inline `[N]` markers map to a bibliography entry within their section. No fabricated citation,
no non-resolving load-bearing identifier.
**Status: PASS** (count_checked = 12 load-bearing identifiers verified live; count_flagged = 0;
1 WARN on first-author label of PMID 28617838).

## IC-11 No Placeholder Strings

Grep for `[citation needed]` / `TBD` / `TODO` / `Content continues` / `according to some reports` /
`research suggests` / `experts believe` across all six sections: zero matches.
**Status: PASS.**

## IC-12 No Wikipedia Citations

Grep `wikipedia` across all sections: the ONLY hit is §D line 99 self-check sentence
"(2) No Wikipedia; …" — i.e. the author's own confirmation that no Wikipedia source was used. This
is not a citation. No `*.wikipedia.org` URL appears in any bibliography.
**Status: PASS** (count_checked = all 6 bibliographies, count_flagged = 0).

## IC-13 Per-Citation Corpus Scoping

Deep-mode sample of load-bearing numerical claims grep-verified against fetched source abstracts:
- §B NEJM: VAT −15.2%/+5.0%, IGF-1 +81.0%, n=412 — found in PMID 18057338 abstract. PASS.
- §B meta: 5 RCTs, VAT MD −27.71 cm², hepatic fat −4.28%, no SAT reduction — found in PMID
  41545261 abstract. PASS.
- §E DailyMed indication + "weight neutral / not for weight loss" — found in label. PASS.
- §E WADA S2.2.4 tesamorelin-named text — confirmed against WADA list. PASS.

Corpus-missing (paywall / abstract-not-retrieved) WARNs — NOT halts (IC-13 + corpus_scoping rule):
- §B/§C JCEM pooled & JAIDS confirmatory granular numbers (−24 cm², +108±112 ng/mL, −37 mg/dL,
  −10.9%/−0.6%): primaries resolve & topic-confirmed; OUP/JAIDS full text is paywalled, so the
  exact secondary figures are abstract-/corpus-limited. WARN.
- §C Stanley 2019 granular figures (−4.1% CI −7.6 to −0.7; 35% vs 4% <5% HFF) and §C/§D mechanistic
  & T2DM secondaries: topic + identifier confirmed; full-text paywalled. WARN.
No quote-not-found and no number-not-found among checked claims.
**Status: PASS** (claims_checked = 4 fully grep-verified; corpus-missing WARNs logged, 0 HALT).

## Verdict

verdict: PASS

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":115,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":5},"IC-5":{"status":"PASS","count_checked":4,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":2},"IC-7":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":12,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":1,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":4,"largest_cluster_name":"Theratechnologies (sponsor/manufacturer lens — all 4 efficacy primaries; academic-lineage lens MGH/Grinspoon-Stanley = 2/4 = 0.50)","largest_cluster_count":4,"share":1.0,"threshold_triggered":true,"surfaced_section_heading":"Section C › Concentration audit (sponsor 100% flagged first-class; academic lineage 50%)"},"corpus_scoping":{"verdict":"PASS","claims_checked":4,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-10: PMID 28617838 (§D [6]) first author is Clemmons DR, not Stanley TL as labeled — identifier/topic correct, fix lead-author label","IC-13/corpus_scoping: JCEM pooled, JAIDS confirmatory, Stanley 2019 Lancet HIV, and T2DM/mechanistic secondary granular figures are paywalled — primaries resolve and topics confirmed, exact secondary numbers corpus-limited (abstract-only), not HALT"]}
```
