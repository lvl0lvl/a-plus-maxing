# Phase 4.75 Integrity Gate — GHK-Cu

Independent integrity verifier (anti-fabrication gate). Corpus: section-A … section-G.
Live-content scope only — every `## Post-fix grep audit` block was stripped before mechanical
checks (audit blocks legitimately quote retired/incorrect strings in OLD→NEW records).
IC-10/IC-13 numerical spot-checks performed against PubMed via WebFetch/WebSearch.

## Verdict

**verdict: PASS** — no HALT-level IC failure. Two non-blocking WARNs (IC-13 abstract-only /
corpus-missing on a paywalled numeric, plus a residual paywall note). Iterations: 1.

---

## IC-1 Type-Tag Presence
**PASS.** All inline `[N, tag]` tokens across A–G carry a tag from the canonical enum
(`mechanism_review | in_vitro | animal | regulatory | rct | open_label | vendor_label |
anecdote_aggregate | practitioner_protocol | compounding_data_sheet`). Section E uses the
documented transition annotation `anecdote_aggregate→open_label` for the two AAD cosmetic
posters — both sides are enum tags and the annotation is an honesty downgrade-marker, not an
out-of-enum tag. count_checked ≈ 150 inline tag-tokens; count_flagged = 0.

## IC-2 Bibliography Type-Tag Presence
**PASS.** Every admissible bibliography entry carries `tag=…`. The only tag-less line is
Section A `[5]` — the explicitly reserved/unused placeholder ("merged into [8]; NOT counted in
tally"), which carries no claim and grounds nothing. Multi-line wrapped entries (C, D) carry
their `tag=` on a continuation line (confirmed: section-C has 17 `tag=` matches for its
14 primaries + R1/R2/OOS).

## IC-3 Vendor-Not-Numerical
**PASS.** Every `vendor_label` inline cite grounds only permitted content (formulation
concentration, vial size, purity, reconstitution/stability):
- F-Claim 2 `[7, vendor_label]` → "~0.05–2%" formulation range (the `<10 ppm` efficacy-adjacent
  figure is grounded to CIR `[1, regulatory]`, not the vendor); flagged "vendor figure,
  qualitative only."
- F-Claim 7 `[6, vendor_label]` → "very rarely reported" (qualitative, no number).
- G `[4, vendor_label]` → "0.05–1%", "5–10% solutions" (formulation); `[4,14, vendor_label]` →
  "50/100 mg vials", "≥98–99% by HPLC" (vial size + identity/purity).
No vendor cite grounds an efficacy/AE-rate/therapeutic-dose number. count_flagged = 0.

## IC-4 Anecdote-Not-Numerical
**PASS.** Every `anecdote_aggregate` cite grounds qualitative existence-of-AE or qualitative
caution only. The single numerical AE figure adjacent to an anecdote cite — F-Claim 8 "8–12%"
`[9, anecdote_aggregate]` — is explicitly **repudiated, not grounded**: "reported numerical
frequencies … are NOT admissible as AE rates because no controlled human injectable trial
exists." This is the textbook correct handling (quote-to-reject). All other anecdote cites
(F-7, F-36, F-37, F-39, F-40) are qualitative. count_flagged = 0.

## IC-5 Practitioner-Protocol-Not-Efficacy
**PASS.** All `practitioner_protocol` cites are in Section G and are firewalled to
route/dose/cycle/handling convention only, under an explicit "Tier 2.7 — captured for
route/dose/cycle convention ONLY; NOT evidence of efficacy" banner. Section G coverage-gaps
confirms "No efficacy claim in this section rests on a practitioner_protocol, vendor_label, or
compounding sheet." Seeds/PDP/Grant protocol cites ground SubQ/topical dosing conventions, never
an effect size or response rate. count_flagged = 0.

## IC-6 Compounding-Data-Sheet-with-Efficacy
**PASS.** Only `[4]` in Section G carries a dual `vendor_label/compounding_data_sheet` tag; it
grounds purity/reconstitution/concentration only ("NEVER efficacy", flagged inline). No
compounding-data-sheet cite grounds an efficacy claim. count_flagged = 0.

## IC-7 Population-Mismatch
**PASS.** Every animal numerical claim carries its species in-sentence (rat, rabbit, mouse,
Wistar, pig — verified across B/C/D). Section B's intro states the cellular cascade is
"extrapolated to humans rather than demonstrated in them," and every section's coverage-gaps
repeats the in-vitro/animal→human caveat. No animal or in-vitro number is presented as a human
finding without a population flag. checked = all animal/in_vitro numerical claims; flagged = 0.

## IC-8 Route-Extrapolation
**PASS.** The topical↔injectable route problem (the defining GHK-Cu route issue) is surfaced
forcefully and correctly:
- Section E headline + coverage-gap #1: "ALL human GHK-Cu evidence is topical … NO human RCT …
  for INJECTABLE or systemic GHK-Cu … must be labeled as [extrapolation]."
- Section F: "the topical→injectable safety extrapolation is invalid"; CIR safety "does NOT
  extend to injection."
- Section A-Claim 13: PK figures carry `[route-extrapolation across topical vs. systemic]`.
- Section C: culture→wound-chamber `[route→8]`; AHK-analog `[route→analog]`.
No dose claim crosses routes without an explicit flag. flagged = 0.

## IC-9 Concentration-Surfacing
**PASS.** The Pickart-nexus COI / review-layer dominance is surfaced as a **first-class
dedicated section** (Section G, `## Concentration/COI audit (Pickart/Margolina share estimate …
commercial COI surfaced)`), opening with a mandatory "COMMERCIAL COI — surfaced as first-class
(mandatory regardless of share)" block that names the discoverer-seller-reviewer triple role,
the Skin Biology R&D affiliation of the review co-author, and the **denied-COI disclosure gap**
(PMID 26236730 declares "no conflict of interests" despite all-author commercial affiliation).
The ~70–85% review-layer share is stated explicitly with method. It is **not buried**: the COI
is also flagged in Section B's intro (preceding all indication sections) and in every section's
coverage-gaps. surfaced_before_first_indication = true (COI raised in the mechanism section that
precedes the indication-bearing sections C–E, and owned first-class in G).

## IC-10 No Fabricated Citations
**PASS.** (a) Internal resolution: every inline `[N]` resolves to a bibliography entry in every
section (inline ⊆ bib, all seven sections). No dangling inline cite. (b) Live spot-check
(6 citations, PubMed):
1. **Maquart 1988, PMID 3169264** [B4/C1/G7] → VERIFIED. Title/authors (Maquart, Pickart,
   Laurent, Gillery, Monboisse, Borel) / FEBS Lett / 1988 / 238(2):343-6 / DOI
   10.1016/0014-5793(88)80509-x all match. (Confirms the iter-2 PMID-transposition fix off
   8227352 and the Phase-4.25 fix off 3049153 landed on the correct PMID.)
2. **Mulder 1994, PMID 17147644** [E5/F16/G13] → VERIFIED. "multicenter, randomized,
   evaluator-blinded, placebo-controlled"; 98.5% vs 60.8% closure; 7% vs 34% infection — all
   match. (Confirms the Phase-4.25 Mulder design-conflation fix is correct.)
3. **Pickart & Margolina 2018, PMID 29986520** (Pickart review) → VERIFIED. Title/authors/
   Int J Mol Sci/2018/19(7):1987; R&D Skin Biology affiliation confirmed (supports the COI flag).
4. **Hostynek 2011, PMID 20721598** (independent primary) → VERIFIED. Permeability coeff
   2.43±0.51×10⁻⁴ cm/h, 136.2±17.5 µg/cm², 97±6.6 µg/cm² — match Section A Claim 10 verbatim.
5. **Hong 2010, PMID 20143136** (independent primary) → VERIFIED. 54-gene/74-probe-set
   signature; GHK + securinine cMap reversal — match B7/D10.
6. **Ufnalska/Bal 2021, PMID 34781677** (independent primary) → VERIFIED as a real, on-topic
   paper (title/authors/Inorg Chem/2021 match A3). The specific value log cK(7.4)=12.62 was NOT
   present in the abstract; full-text PDF is paywalled (403). → corpus-missing for that value
   (see IC-13 WARN); the citation itself is genuine, not fabricated.
No fabricated citations. count_flagged = 0.

## IC-11 No Placeholder Strings
**PASS.** Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, "according to some
reports", "research suggests", "experts believe", placeholder/lorem/XXXX across live content →
0 hits. count_flagged = 0.

## IC-12 No Wikipedia Citations
**PASS.** No `wikipedia.org` URL anywhere in the corpus (bibliography or body). count_flagged = 0.

## IC-13 Per-Citation Corpus Scoping
**WARN** (non-HALT). ~6 load-bearing numerical/scope claims grep-verified against fetched
source text:
- Maquart 1988: collagen onset 10⁻¹²–10⁻¹¹ M / peak ~10⁻⁹ M → FOUND in abstract. PASS.
- Mulder 1994: 98.5% / 60.8% / 7% / 34% → FOUND in abstract. PASS.
- Hostynek 2011: 2.43×10⁻⁴ cm/h, 136.2 µg/cm², 97 µg/cm² → FOUND in abstract. PASS.
- Hong 2010: 54-gene / 74-probe-set; GHK+securinine cMap reversal → FOUND in abstract. PASS.
  ("~1 µM" GHK concentration is abstract-not-present / full-text level — minor, correctly framed
  as a predicted active concentration, not asserted as measured.)
- Ufnalska 2021: log cK(7.4)=12.62 → **corpus-missing** (abstract does not state it; full-text
  PDF paywalled, HTTP 403). Per the paywall rule this is a WARN, not a HALT — the paper is real
  and on-topic, and the synthesis note marks it "VERIFIED (PMC fetched, citation cross-checked)"
  at synthesis time.
0 `quote-not-found`, 0 `number-not-found`. claims_checked = 6; claims_failed = []
(1 corpus-missing WARN: ufnalska-2021 / log cK 12.62).

---

## Population / Concentration / Corpus

### population_mismatch
- **verdict: PASS** — checked_citations: all animal + in_vitro numerical claims (B, C, D);
  flagged_citations: []. Every animal claim names its species in-sentence; every cellular claim
  is flagged human-extrapolated.

### concentration_audit
- **verdict: PASS**
- total_primaries (distinct efficacy primaries, de-duplicated across sections; reviews/
  regulatory/vendor/practitioner/registry excluded): **28**
- largest_cluster_name: **Pickart/Skin Biology nexus**
- largest_cluster_count: **3** (Pickart-authored/affiliated efficacy primaries: Maquart&Pickart
  1988 FEBS; Pickart/Margolina 2021 OBM cMap; + JCI-1993 counted nexus-adjacent via ProCyte
  Patt/Trachy co-authorship — conservative over-count). Strict Pickart-authored = 2.
- **share (EFFICACY-PRIMARY basis): ≈ 0.11** (3/28; strict 2/28 = 0.07). Range 0.07–0.25
  depending on nexus definition — BELOW 0.70.
- **threshold_triggered: false** (primary-share basis, per the brief's stated rule: the in-vivo/
  experimental Pickart-nexus share is a minority).
- **Two-layer statement (both surfaced clearly in Section G):** the ~70–85% concentration figure
  is the **REVIEW / claims-synthesis layer**, not the primary-evidence layer. That review-layer
  dominance + denied COI is the first-class COI caveat (IC-9), and is correctly NOT used as the
  primary-share number. The primary experimental literature is genuinely distributed (≈0.11).
- surfaced_section_heading: "Concentration/COI audit (Pickart/Margolina share estimate + method;
  commercial COI surfaced)" (Section G), with COI also raised in Section B's intro.
- surfaced_before_first_indication: true.

### corpus_scoping
- **verdict: PASS** (with 1 corpus-missing WARN) — claims_checked: 6; claims_failed: [].
  Only non-pass item is the paywalled Ufnalska log cK 12.62 → corpus-missing WARN.

---

## Structured verdict

```json
{"phase":"4.75","ic_checks":{"IC-1":{"status":"PASS","count_checked":150,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":6,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"WARN","findings":["ufnalska-2021 log cK(7.4)=12.62 corpus-missing: value not in abstract, full-text PDF paywalled (HTTP 403); citation genuine and on-topic; paywall->WARN not HALT","Hong-2010 '~1 uM' GHK concentration is full-text-level (not in abstract); correctly framed as predicted active concentration, not asserted as measured"]}},"population_mismatch":{"verdict":"PASS","checked_citations":50,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":28,"largest_cluster_name":"Pickart/Skin Biology nexus","largest_cluster_count":3,"share":0.11,"threshold_triggered":false,"surfaced_section_heading":"Concentration/COI audit (Pickart/Margolina share estimate + method; commercial COI surfaced)","surfaced_before_first_indication":true},"corpus_scoping":{"verdict":"PASS","claims_checked":6,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-13: ufnalska-2021 log cK(7.4)=12.62 corpus-missing (paywalled full text)","IC-13: hong-2010 ~1 uM is full-text-level, framed as prediction not measurement","IC-9 residual: review-layer share is a calibrated estimate not a full bibliometric census (Section G self-discloses)"],"iterations":1}
```

`halt_reasons` enum (none triggered): untagged-citation | vendor-grounds-numerical |
anecdote-grounds-numerical | practitioner-grounds-efficacy | population-mismatch-unflagged |
route-extrapolation-unflagged | concentration-not-surfaced | fabricated-citation |
placeholder-string | wikipedia-cited | corpus-scoping-fail.
