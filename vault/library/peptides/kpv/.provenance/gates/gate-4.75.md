# Phase 4.75 Integrity Gate — KPV

Independent Phase 4.75 Citation-Integrity verifier run over the validated corpus
(`sections/section-A.md` … `section-G.md`). Mechanical structural compliance only —
no content-quality judgement. Per-section `## Post-fix grep audit` blocks were excluded
from live checks (they intentionally contain the defect strings they remediated).

Mode: DEEP. IC-10 / IC-13 spot-verified live against PubMed/NCBI E-utilities.

## Verdict

verdict: PASS

No HALT condition triggered across the 13 IC checks or the population / concentration /
corpus sub-audits. Two non-blocking WARNs recorded (IC-1 tag-notation style; IC-13
abstract-only / paywalled magnitude figures). Both are WARN-class per the IC procedure
and the gate's stated policy (paywalled → corpus-missing WARN, not HALT).

---

## IC-1 Type-Tag Presence — PASS

Every inline `[N, <tag>]` citation carries a base tag from the canonical enum
(`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review |
regulatory | compounding_data_sheet | vendor_label | practitioner_protocol |
anecdote_aggregate`). Tally of inline tags (live checks): animal 35, regulatory 33,
in_vitro 33, mechanism_review 18, practitioner_protocol 12, anecdote_aggregate 5,
vendor_label 3.

Non-bare-enum tokens examined and cleared:
- `[N, tag]` literal (7 hits) — template/header text ("Claims (numbered; inline [N, tag]…")
  and one recount line, NOT real citations.
- `[S7/S8, regulatory(patent)]` (2) — base tag `regulatory`; `(patent)` is a sub-qualifier,
  not a distinct tag. WARN-style notation, enum-compliant.
- `[3/5/7, anecdote_aggregate→null]` (3, Section E) — base tag `anecdote_aggregate`; `→null`
  is a deliberate "resolves to no human evidence" marker. Enum-compliant base.
- `[1,8] [3,4] [2,10] [14,15]` — multi-reference groupings (ref-N + ref-M), not `[N, tag]`
  citations; correctly excluded.

WARN (non-blocking): the `(patent)` and `→null` decorations deviate from bare-enum style;
base tags are all valid, so no untagged-citation HALT.

count_checked = 119 ; count_flagged = 0

## IC-2 Bibliography Type-Tag Presence — PASS

Every bibliography entry carries a `tag=` annotation drawn from the enum; compound entries
(e.g. `animal+in_vitro`, `animal/in_vitro/mechanism_review`) are permitted and used.
Per-section source tallies internally recount and self-verify (A: 6 admissible; B: 7;
C: 7; D: 15; E: 10; F: 15; G: 18). All tag totals match enumerated entry counts.

## IC-3 Vendor-Not-Numerical — PASS

Two `vendor_label` inline cites:
- A[9] — MW "~400 Da" discrepancy flag, explicitly "(cited only to flag the discrepancy;
  not used to ground the number)". Authoritative 342.43 g/mol grounded on regulatory [6].
- F[6] — co-cited at the unverified-LD50 sentence, explicitly "(qualitative only — vendor/
  practitioner sources do not ground numerical AE rates)". The ≥100 mg/kg figure is surfaced
  as an explicitly-rejected practitioner/vendor claim, not grounded by the vendor cite.

No vendor cite grounds an efficacy / AE-rate / therapeutic-dose number.

## IC-4 Anecdote-Not-Numerical — PASS

`anecdote_aggregate` cites (E[9], E[10], G[S13], F[7], plus E `→null` markers) ground only
qualitative AE patterns, the null-human-evidence finding, or consensus-convergence context.
G[S13] aggregator dose ranges are explicitly labelled "NOT a practitioner protocol… cited
only to show consensus convergence, not as practitioner protocols." No anecdote cite grounds
a numerical AE rate, dose recommendation, or effect size.

## IC-5 Practitioner-Protocol-Not-Efficacy — PASS

`practitioner_protocol` cites (G[S10/S11/S12], F[5]) ground dose/route/cycle/contraindication
conventions only. Where they appear beside risk/efficacy framing (F claims 7, 8) they are
co-cited with a mechanism_review Tier source (F[3]); no efficacy claim rests solely on a
practitioner cite. F claim 5's dose figures are explicitly marked "treat as unverified."

## IC-6 Compounding-Data-Sheet-with-Efficacy — PASS

No `compounding_data_sheet` cites present in the corpus. Check vacuously satisfied.

## IC-7 Population-Mismatch — PASS

No literal `[population-mismatch: <species>]` token is used; instead every numerical
animal / in_vitro claim names its species/model as the sentence subject within the
same claim block (the IC-7 exemption: "species is the subject within 100 chars").
Conventions used corpus-wide: inline parentheticals `(mouse; …)`, `(rat, female
Sprague-Dawley, …)`, `(human intestinal epithelial …)` and `Species/n:` lines
immediately adjacent to each figure (e.g. C: "16 µg/kg/day" → next line "Species/n:
FVB male mice"; D23 "2 mg/kg/day … ~12%" → "(rat, female Sprague-Dawley, n=60…)").
Spot-scan of every µg/kg, mg/kg, n=, µM, mg/mL token found a species/model token within
the same claim block in all cases. Anti-fabrication intent fully met — every section's
headline also states there is NO human data.

WARN-style note (not a finding): the corpus encodes population via explicit-subject
adjacency rather than the literal bracket tag. Substantively compliant.

checked_citations = 24 ; flagged_citations = []

## IC-8 Route-Extrapolation — PASS

Dose/route claims annotate the source's tested route inline (`[route: oral/lumenal]`,
`[route: transdermal]`, `route=intravaginal gel`, `route=oral gavage`, `route=systemic/i.p.`,
`route=topical`). Where a model's route is extrapolation-relevant the corpus carries an
explicit `[route-extrapolation: intraperitoneal model]` tag (A claim 3) and a prose
route-extrapolation caveat (A coverage gaps; D6/D7 flag IV-vs-oral distinctly). No dose
claim asserts a route different from its cited primary without annotation.

## IC-9 Concentration-Surfacing — PASS

Single-lab concentration risk is surfaced FIRST-CLASS and FIRST in Section G: the
`## Concentration audit` heading is the opening content section (line 8, immediately after
scope), before any sourcing / prescribing / indication subsection. The Merlin/GSU cluster
is named explicitly with method and TWO denominators:
- All-cause in-vivo efficacy primaries (N=6): Merlin/GSU = 3/6 ≈ 0.50 (headline share).
- Gut/IBD subset (N=4): Merlin/GSU = 3/4 ≈ 0.75 → explicit "FLAG: ≥70% single-lab
  concentration within the gut/IBD efficacy literature."

The ~0.75 gut/IBD sub-domain concentration is surfaced as a first-class FLAG (the Section G
requirement); the headline corpus-wide share is 0.50, below the 0.70 trigger ⇒
threshold_triggered = false. Both numbers stated with method, exactly as required.

## IC-10 No Fabricated Citations — PASS

Every inline `[N]` resolves to a bibliography entry in its section; bibliography PMIDs/DOIs
spot-verified live against PubMed / NCBI E-utilities. 9 citations spot-checked, ALL real and
accurately attributed (title + first author + journal + year + DOI concordant):

| Cite | PMID | Verified |
|------|------|----------|
| Dalmasso 2008 (A2/B1/C1/D2/E3/F2/G-P1) | 18061177 | ✓ PepT1-mediated KPV, Gastroenterology 134(1):166-78, DOI 10.1053/j.gastro.2007.10.026 |
| Kannengiesser 2008 (A/B/C/D/E/G-P4) | 18092346 | ✓ Inflamm Bowel Dis 14(3):324-31, DOI 10.1002/ibd.20334 (Section C's prior 17973296 error confirmed corrected) |
| Viennois 2016 (B7/C3/D-/G-P2) | 27458604 | ✓ Cell Mol Gastroenterol Hepatol 2(3):340-357, DOI 10.1016/j.jcmgh.2016.01.006 |
| Bettenworth KdPT 2011 (A4/D5/E7) | 21741932 | ✓ "KdPT protects from intestinal inflammation…", Am J Pathol 179(3):1230-42 — KPV-vs-KdPT boundary cite, correctly distinguished |
| Cutuli 2000 (B8/D1/G-P6) | 10670585 | ✓ "Antimicrobial effects of alpha-MSH peptides", J Leukoc Biol 67(2):233-9 |
| Cheng 2026 proKPV (C5) | 41533788 | ✓ Sci Adv 2026, self-immolative oral peptide delivery, DOI 10.1126/sciadv.aea2989 |
| Xiao 2017 HA-NP (C4/D10/F4/G-P3) | 28143741 | ✓ Mol Ther, DOI 10.1016/j.ymthe.2016.11.020 |
| Getting 2003 (A1/D11/E5) | 12750433 | ✓ JPET, KPV core/C-terminal dissection |
| Hiltz 1989 (F1) | 2550304 | ✓ FASEB J, COOH-terminal α-MSH fragment |

No inline cite without a bibliography entry; no fabricated PMID/DOI detected.

## IC-11 No Placeholder Strings — PASS

Grep for `citation needed | TBD | TODO | Content continues | according to some reports |
research suggests | experts believe` across all sections (excluding post-fix audit blocks):
zero matches.

## IC-12 No Wikipedia Citations — PASS

Grep for `*.wikipedia.org` across all bibliographies: zero matches.

## IC-13 Per-Citation Corpus Scoping — WARN (non-blocking)

Load-bearing numerical/scope claims grep-verified against the cited primaries' retrievable
text (PubMed abstracts via E-utilities efetch):

- Dalmasso 18061177 — abstract verbatim confirms "Nanomolar concentrations of KPV inhibit…
  NF-kappaB and MAP kinase" (grounds the ~10 nM / nanomolar claims, A6/B2/C2/D15) and "oral
  administration of KPV reduces the incidence of DSS- and TNBS-induced colitis" (grounds the
  DSS+TNBS scope). PASS for these.
- Cutuli 10670585 — abstract confirms KPV(11-13) vs S. aureus + C. albicans, "physiological
  (picomolar) range," and neutrophil killing not reduced (enhanced) — grounds D1/D2/D3/B8.
  PASS.
- Kannengiesser 18092346, Viennois 27458604, Bettenworth 21741932, Cheng 41533788 — title +
  scope confirmed against PubMed records; consistent with claims as cited.

WARN (corpus-missing, paywall): several precise magnitude figures live only in paywalled
full text and are not surfaced in the retrievable abstract — specifically "100 µM in drinking
water" (Dalmasso), "16 µg/kg/day" (Xiao), the "~12,000×" potency figure (Xiao), and the
proKPV "20-fold / 5-ASA 50 mg/kg" deltas (Cheng). Per IC-13 policy these are `corpus-missing`
→ WARN, not HALT (paywalls happen). The corpus is honest about this: Section C coverage-gaps
explicitly flags publisher 403s and marks the 12,000× figure single-lab/intra-study, and
Section F marks the ≥100 mg/kg LD50 figure unverified. ~5 numerical claims checked at abstract
tier; abstract-verifiable subset all matched; full-text-only magnitudes are corpus-missing WARN.

claims_checked = 5 ; claims_failed = [] (no quote-not-found / number-not-found; corpus-missing
entries are WARN per policy and listed in warnings[])

---

## Population / Concentration / Corpus

**Population mismatch — PASS.** 24 numerical animal/in_vitro claims checked; 0 flagged. Every
such claim names its species/model as sentence subject within the claim block (IC-7 exemption
satisfied corpus-wide). No human number is grounded on animal/in_vitro data; every section
headlines the absence of human data.

**Concentration audit — PASS.** total_primaries = 6 (all-cause in-vivo efficacy primaries
P1–P6). largest_cluster = Merlin/GSU, count = 3. Headline share = 3/6 = 0.50, BELOW the 0.70
threshold ⇒ threshold_triggered = false. The gut/IBD sub-domain concentration (Merlin 3/4 ≈
0.75) is surfaced first-class as an explicit ≥70% FLAG in Section G's opening section
(IC-9 satisfied). Both shares stated with method; surfaced before any indication subsection.

**Corpus scoping — PASS (with corpus-missing WARNs).** 5 load-bearing numerical claims
checked; 0 hard failures. Abstract-verifiable numbers (nanomolar, picomolar, DSS/TNBS models,
organisms) all matched their primaries. Paywalled full-text-only magnitudes are corpus-missing
WARN per policy, and the corpus discloses these gaps honestly.

## Structured verdict

```json
{"phase":"4.75","verdict":"PASS","timestamp":"2026-06-19T16:05:00+00:00","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":119,"count_flagged":0,"findings":["base tags all enum-valid; (patent)/→null decorations are sub-qualifiers on valid base tags, not untagged citations"]},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS","count_checked":24,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":9,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"WARN","findings":["abstract-verifiable numbers (nanomolar, picomolar, DSS/TNBS, S. aureus/C. albicans) confirmed against cited primaries; full-text-only magnitudes (100 µM, 16 µg/kg/day, ~12,000×, proKPV deltas) are paywalled corpus-missing per IC-13 policy = WARN not HALT; corpus discloses these gaps honestly"]}},"population_mismatch":{"verdict":"PASS","checked_citations":24,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":6,"largest_cluster_name":"Merlin/GSU","largest_cluster_count":3,"share":0.5,"threshold_triggered":false,"surfaced_section_heading":"Concentration audit (dominant labs; estimated single-lab share + method)","surfaced_before_first_indication":true},"corpus_scoping":{"verdict":"PASS","claims_checked":5,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-1: (patent)/→null tag decorations deviate from bare-enum style; base tags valid","IC-13: paywalled full-text magnitude figures (100 µM, 16 µg/kg/day, ~12,000×, proKPV 20-fold/5-ASA deltas) are corpus-missing at abstract tier — WARN per policy, disclosed honestly in corpus"],"attestation_chain":{"iter_start_ts":"2026-06-19T15:53:29.983488+00:00","attest_ts":"2026-06-19T16:05:00+00:00","iteration":1,"agent_source_path":"sections/section-G.md","agent_source_sha256":"891dcfef63302b765893090bbe590121307b0a7755f6557e68c9d7145f5cd963","agent_source_mtime":"2026-06-19T15:47:28+00:00"}}
```
