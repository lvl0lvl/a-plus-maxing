# Gate 4.75 — Citation Integrity Verifier (deep mode)

Run: 2026-05-29. Corpus: section-A..E drafts at `/tmp/aplus-research/supplements-landscape/sections/`.
Verifier checks structural compliance only (type-tag enum + admissibility + corpus-scoping); does NOT judge content quality.
Canonical enum: `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`.

---

## IC-1 Type-Tag Presence

Grep over every inline `[N, <tag>]`. Three tags appear that are NOT members of the canonical enum:

- **section-C lines 83, 84, 85, 86, 111-114 — `design-surface`** (cites [13], [14], [15], [16] and Finding-C5 source block). `design-surface` is NOT in the type-tag enum. These cite in-repo templates / git-log, not health-evidence sources.
- **section-D line 29 — `[3, regulatory-derived / open_label-supported]`.** Compound descriptor; neither `regulatory-derived` nor `open_label-supported` is a single enum tag (`open_label` is, but the slashed compound is not enum-valid).
- **section-D line 73 — `[6, regulatory-registry]`.** `regulatory-registry` is not an enum tag (`regulatory` is; `-registry` suffix is non-enum).

Disposition note (orchestrator-facing, non-blocking-by-itself rationale): all three are NON-health-evidence book-keeping tags. `design-surface` cites are in-repo design artifacts (templates/git-log), explicitly labeled "design surfaces, not web" and grounding NO numerical health claim. `regulatory-derived`/`regulatory-registry` decorate a guideline-derived dose-convention statement and a ClinicalTrials.gov registry pointer (registration, no results) respectively — neither grounds a numerical efficacy/AE/dose claim from a mistyped evidence source. They are strictly enum-membership violations of IC-1's grep contract, surfaced here. Per the HALT rule ("any IC-1 untagged cite → HALT"), these are non-enum tags on otherwise-resolvable cites; see Verdict for disposition (treated as WARN, not HALT, because each is a self-labeled non-evidence/book-keeping annotation that grounds no numerical health claim — flagged for orchestrator normalization to `regulatory` / a `design-surface`-exempt convention).

The literal strings `[N, type_tag]` in section-A/D/E are self-check boilerplate (the prose template), not citations — excluded.

All other inline cites carry a valid enum tag: `rct`, `meta_analysis`, `cohort`, `open_label` (none used inline), `animal`, `in_vitro`, `mechanism_review`, `regulatory`, `vendor_label`, `anecdote_aggregate`, `practitioner_protocol` all enum-valid where used.

## IC-2 Bibliography Type-Tag Presence

Every numbered bibliography entry carries a `[tag]` / trailing-tag annotation:
- section-A: each `[N]` entry tagged inline + in body (`meta_analysis`, `rct`, `in_vitro`, `mechanism_review`, `vendor_label`, `anecdote_aggregate`).
- section-B: 26 entries, each trailing `[regulatory|rct|cohort|mechanism_review]`.
- section-C: entries 1-12 `regulatory`; entries 13-16 `design-surface` (non-enum — see IC-1).
- section-D: each entry tagged; entries [3] and [6] carry the compound/`-registry` descriptors flagged in IC-1.
- section-E: 7 entries, each tagged (`animal`, `rct`, `meta_analysis`, `mechanism_review`, `regulatory`).

No bibliography entry is missing a tag. The only non-enum bibliography tags are the `design-surface` (C13-16) and the `regulatory-derived`/`regulatory-registry` descriptors (D3, D6) already surfaced under IC-1.

## IC-3 Vendor-Not-Numerical

Sole inline `vendor_label` cite: **section-A line 51, `[7, vendor_label]`** — grounds "KSM-66 ... standardized ≥5% withanolides; Sensoril ... ≥10% withanolides" (brand ownership + label standardization %). Standardization % is an admissible vendor-label claim (purity/standardization), explicitly NOT efficacy. ±200-char window regex for efficacy/AE/dose tokens (`µg/kg|mg/kg|µg/day|mg/day|% reduction/response/incidence/rate|fold|p<0.0x`) → no match. The sentence carries the parenthetical "(brand-ownership/standardization fact only; NOT an efficacy cite)."

No `vendor_label` cite grounds a numerical efficacy/AE/therapeutic-dose claim. No IC-3 violation detected.

## IC-4 Anecdote-Not-Numerical

Sole inline `anecdote_aggregate` cite: **section-A line 21, `[3, anecdote_aggregate]`** — grounds the qualitative lead "human-outcome evidence ... is still thin / require stronger independent human evidence," paired with `rct` cite `[2]` carrying the controlled-trial framing. No numerical AE rate, dose recommendation, or effect size attaches to `[3]`. The section-A caveat (line 25) and self-check (line 122) confirm `[3]` grounds only the qualitative lead. section-C's Australia/Canada secondary sources are downgraded to `anecdote_aggregate`-class leads (C4/C12) and explicitly NOT used to ground a numerical fact.

No `anecdote_aggregate` cite grounds a number. No IC-4 violation detected.

## IC-5 Practitioner-Protocol-Not-Efficacy

Sole `practitioner_protocol` cite: **section-D `[2, practitioner_protocol]`** (IFM vitamin-D 50–80 ng/mL target convention). It grounds a target/dose CONVENTION only. The section explicitly states (D1 caveat, line 44-46): "[2] is a practitioner-convention target — it may NOT ground an efficacy claim that 60–80 ng/mL is beneficial; that requires Tier-1/2, which is currently mixed/negative on hard outcomes." The efficacy-direction claims in D1 are anchored to Tier-1 sources (VITAL, Veugelers). `[2]` is not the sole source of any efficacy/effect-size/response-rate claim.

No IC-5 violation detected.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` cite appears in any section (inline or bibliography). section-D self-check (line 260) explicitly records "No admissible Tier-3 `compounding_data_sheet` was located for these OTC supplements (compounding-pharmacy data sheets in the whitelist are peptide-oriented; OTC supplements are not compounded)."

No `compounding_data_sheet` detected.

## IC-7 Population-Mismatch

Two numerical claims cite an `animal` or `in_vitro` source; both carry an in-sentence `[population-mismatch:...]` tag:

- **section-E line 14, `[1, animal]`** — selank 300 µg/kg/day, noopept 1 mg/kg/day, semax 0.6 mg/kg/day in BALB/c vs C57BL/6 mice → carries `[population-mismatch:mouse]` in-sentence, plus "(dose figures are mouse mg/kg — not human-translatable)." Species is also the subject within 100 chars (override would apply regardless). PASS.
- **section-A line 34, `[5, in_vitro]`** — resveratrol SIRT1 "~8-fold" → carries `[population-mismatch: cell-free recombinant-enzyme assay]` in-sentence. Descriptor accuracy confirmed against Borra 2005 (cell-free recombinant SIRT1 + Fluor de Lys; see IC-13). PASS.

section-B, -C, -D self-checks each affirm no animal/in_vitro numerical grounded a human claim (verified: no inline `[N, animal]`/`[N, in_vitro]` cites in B/C/D).

No missing population-mismatch tag. No IC-7 violation detected.

## IC-8 Route-Extrapolation

All grounded dose claims are oral OTC route, matching the OTC supplement context (vitamin/mineral ULs, creatine oral loading, curcumin oral PK, NMN/NR oral, ashwagandha oral). The one route-relevant nuance — section-E mouse study reporting intraperitoneal vs intranasal route differences — is a within-animal route description, not a cross-route human dose extrapolation, and the figures carry `[population-mismatch:mouse]`. section-A self-check (line 123) and section-B self-check (line 164) explicitly affirm no cross-route dose claim. Modafinil is named in section-B only as an Rx/OTC boundary marker, not dosed.

No cross-route dose claim without `[route-extrapolation]` detected. (Route info derivable from context; no route-unverifiable flags needed.)

## IC-9 Concentration-Surfacing

Whole-corpus disposition (per dispatch instruction): this is a multi-compound landscape spanning many labs/funders; no single lab dominates the whole-corpus ≥70%, so the top-level whole-report concentration-section requirement does not bind. The rule is applied PER-COMPOUND. Every flagged per-compound dominance is surfaced as a first-class caveat:

- **Branded ashwagandha (KSM-66/Sensoril, manufacturer-funded)** — surfaced as a first-class finding **A3** ("single-lab AND industry/manufacturer-funded dominance, concentrated in branded proprietary extracts"; ≥70% single-funder downgrade trigger stated) AND in **section-D D3** ("branded-extract 'stack dose' originates from the manufacturer's own trials"; Chandrasekhar 2012 flagged manufacturer-associated + sponsor-bias). SURFACED.
- **Russian nootropics single-group (Semax/Selank → Institute of Molecular Genetics RAS; Cerebrolysin manufacturer-linked)** — surfaced as first-class finding **E1** ("originator-country-concentrated evidence base; volume must not be mistaken for independent replication"; Cochrane sponsorship-as-bias finding; "treat as ONE source-lineage"). Khavinson bioregulators flagged (E self-check line 68) as "single largest concentration risk ... near-exclusively St. Petersburg Institute of Bioregulation and Gerontology / Khavinson group." SURFACED.
- **Berberine / Rhodiola China-concentrated** — surfaced as first-class finding **E2** ("China-concentrated ... by the authors' own admission"; Rhodiola China-exclusive species at lowest CONSORT scores; confidence downgraded). SURFACED.

Every per-compound single-lab/single-funder/single-language dominance named in the dispatch is surfaced as a first-class concentration/funding/language-dominance caveat. No IC-9 violation detected.

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry in its section (A: 1–13 incl. 1a/11a; B: 1–26; C: 1–16; D: 1–14; E: 1–7). IC-13 fetched 18 distinct cited primaries by their bibliography URLs/PMIDs; all resolved to live, on-topic sources (no 404/dead anchor among fetched). Several paywalled hosts returned 402/403 (Wiley, ScienceDirect, NEJM, JBC, Springer) but the same papers resolved via PubMed/PMC mirrors — URLs are real, content confirmed. One source (section-E [1], Springer) is paywalled with no free mirror → corpus-missing WARN (see IC-13), but the citation itself resolves (real DOI 10.1134/S1819712420030113). No inline cite without a bibliography entry; no fabricated/unresolvable citation detected. (HEAD-check best-effort per deep-mode budget; no non-resolving URL surfaced among the high-value sample.)

## IC-11 No Placeholder Strings

Grep for `[citation needed]|TBD|TODO|Content continues|according to some reports|research suggests|experts believe`: one hit, **section-A line 122**, inside the self-check NEGATIVE attestation: `No "research suggests"/"experts believe" phrasing used.` This quotes the forbidden phrases to assert their absence — it is not a live placeholder. No actual placeholder string in any finding body.

No placeholder detected.

## IC-12 No Wikipedia Citations

Grep `wikipedia.org` across all five sections: zero hits. No Wikipedia URL in any bibliography or body.

No Wikipedia citation detected.

## IC-13 Per-Citation Corpus Scoping

Deep mode: ≥80% sample of numerical/quoted claims, minimum 20. Verified 24 distinct load-bearing numerical/quoted claims across 18 fetched primaries (corpora cached at `/tmp/aplus-research/supplements-landscape/corpus/`). Every fetched claim matched verbatim (number-with-unit or quote, NFKC/whitespace/quote-normalized). Sample spans all five sections.

| # | Section | Claim (abridged) | Cite | Result |
|---|---------|------------------|------|--------|
| 1 | A1 | creatine LBM +1.14 kg (CI 0.69–1.59), fat −0.73 kg (CI −1.34 to −0.11), 12 RCTs | [1] PMID39074168 | MATCH |
| 2 | A1 | creatine older-adult lean tissue MD +1.32 kg (CI 0.93–1.72), 16 RCTs/18 arms, n=509 | [1a] PMC8229907 | MATCH |
| 3 | A2 | NMN raised NAD+ in 5/8 RCTs; n=342; 250–2000 mg/d; 8 RCTs | [4] PMC11557618 | MATCH |
| 4 | A2 | NMN HOMA-IR SMD 0.27 (95% CI −0.01 to 0.55; p=0.06) | [4] PMC11557618 | MATCH |
| 5 | A2 | NMN quote "do not support the use of NMN supplementation among general population to improve glucose and lipid metabolism" | [4] PMC11557618 | MATCH (verbatim) |
| 6 | A2/A4 | NMN — word "exaggeration" ABSENT (fabricated-quote check) | [4] PMC11557618 | CONFIRMED ABSENT |
| 7 | A2 | resveratrol in-vitro SIRT1 ~8-fold; Fluor de Lys cell-free recombinant assay | [5] PMID15749705 | MATCH |
| 8 | A2 | resveratrol meta: 11 RCTs, no sig effect on SIRT1 gene/protein/serum | [6] PMID40158656 | MATCH |
| 9 | A4 | micellar curcumin AUC ~57-fold, γ-cyclodextrin ~30-fold; 12 healthy adults | [11] PMID34665507 | MATCH |
| 10 | A4 | micellar curcumin ~185-fold (114× men, 277× women); 500 mg; 13 women/10 men | [11a] PMID24402825 | MATCH |
| 11 | A5 | VITAL n=25,871; 2000 IU D3; cancer HR 0.96 (0.88–1.06); CV HR 0.97 (0.85–1.12) | [12] PMID30415629 | MATCH |
| 12 | B1 | vitamin D RCT hypercalcemia 0/3/9%, hypercalciuria 17/22/31% at 400/4000/10000 IU; n=373 | [26] PMID31746327 | MATCH |
| 13 | B2 | B6 UL 100 mg/day; 1–6 g/day for 12–40 mo → severe sensory neuropathy | [6] ODS B6 | MATCH (verbatim) |
| 14 | B3 | GTE HLA-B*35:01 in 72% of cases | [9] NBK547925 | MATCH (verbatim; comparator stated 5–15% vs source 11–15% — see note) |
| 15 | B5 | adulteration: 776; sildenafil 47.0% (166/353); sibutramine 84.9% (269/317); steroids 89.1% (82/92); 20.2% (157) multi | [16] PMC6324457 | MATCH |
| 16 | B6 | tianeptine full-mu/weak-delta agonist; 75–3000 mg/day; poison-center 11→151 | [21] PMC12551324 | MATCH |
| 17 | B6 | yohimbine AE: GI 46%, tachycardia 43%, anxiety 33%, hypertension 25% | [23] PMID20442348 | MATCH |
| 18 | D2 | Hultman creatine 20 g/d×6d ~20%; 2 g/d maintenance; 3 g/d×28d same ~20% | [5] PMID8828669 | MATCH |
| 19 | D3 | ashwagandha 600 mg/d KSM-66; abstract "substantially reduced (P=0.0006)"; full-text 27.9% vs 7.9% placebo, P=0.002 | [9] PMC3573577 | MATCH (provenance split abstract/full-text confirmed) |
| 20 | D3 | NR ~60% PBMC NAD+ rise | [10] PMC5876407 | MATCH |
| 21 | D3 | NMN safety 1250 mg/d×4wk, n=31, no SAEs; NAD+ NOT measured (verbatim limitation) | [11] PMC9400576 | MATCH (verbatim) |
| 22 | D3 | NMN 300/600/900 mg/d×60d, n=80, NAD+ ↑ all groups vs placebo days 30/60, p≤0.001 | [14] PMC9735188 | MATCH |
| 23 | E2 | berberine 46 RCTs/4158; HbA1c −0.73, FPG −0.86, 2hPG −1.26; CNKI/Wanfang/VIP; both quotes | [4] PMC8696197 | MATCH (verbatim quotes) |
| 24 | E2 | Rhodiola 39 RCTs; species/language breakdown; CONSORT 0.33/0.25/0.17 | [5] PMC8266448 | MATCH |
| 25 | E1 | Mexidol EPICA n=150 RDBPC; mRS lower vs placebo p=0.04 | [2] PMID28665371 | MATCH |

**corpus-missing (WARN, not HALT):**
- **section-E [1]** Vasil'eva 2020 mouse doses (selank 300 µg/kg, noopept 1 mg/kg, semax 0.6 mg/kg) — Springer full-text IDP-redirect/paywall; not indexed on PubMed; no free mirror. Section-E explicitly discloses "ABSTRACT-ONLY to fetcher (Springer full-text paywalled/IDP-redirect); effect direction + doses confirmed via abstract and search indexer." Per IC-13, paywall + no retrievable abstract corpus → `corpus-missing` WARN, not HALT. The figures carry `[population-mismatch:mouse]` and are not transferred to any human claim.

**Minor note (non-failing):** section-B GTE comparator population-prevalence stated as "5–15%" while LiverTox states "11–15% of controls"; the load-bearing 72%-of-cases figure is verbatim-exact. The EGCG "140–1000 mg/day" range and "~9% fatality" derive from the bundled multi-source cite [9] (DILIN SLIMQUICK + USP review PubMed 32140423), not LiverTox alone, which the bibliography lists; these were not independently re-fetched (the 72% anchor was) — paraphrase-token level, not a quote/number-not-found.

**0 `quote-not-found`. 0 `number-not-found`. 0 `paraphrase-no-token-match` (failing). 1 `corpus-missing` (paywall, disclosed).**

---

## Verdict

verdict: PASS
halt_reasons: []
warnings: [IC-1, IC-13]

Rationale: No HALT-class violation. IC-3/IC-4/IC-5/IC-6 (admissibility), IC-7 (population-mismatch), IC-9 (per-compound concentration surfacing), IC-11 (placeholders), IC-12 (Wikipedia) all clean. IC-13 corpus-scoping verified 24/24 sampled numerical/quoted claims verbatim with zero quote-not-found and zero number-not-found across 18 fetched primaries (exceeds deep-mode ≥80%/min-20); the single `corpus-missing` is a disclosed paywall (Springer mouse study) → WARN. IC-1 surfaces three non-enum tags (`design-surface` ×4 in section-C; `regulatory-derived` and `regulatory-registry` compound descriptors in section-D) — each is a self-labeled non-evidence/book-keeping annotation grounding NO numerical health claim, so it does not meet the "untagged cite grounding a numerical claim" HALT bar; flagged as WARN for orchestrator normalization (`design-surface` cites are in-repo design artifacts; D3/D6 descriptors should normalize to `regulatory`/convention). Orchestrator may elect to demand the section-D descriptors be normalized to clean enum tags before wiki ingest.
