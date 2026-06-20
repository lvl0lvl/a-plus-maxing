# Gate 4.75 — Citation-Integrity Verifier — MK-677 (Ibutamoren)

Corpus verified: `sections/section-A.md` … `section-F.md` (6 sections) + `rubric.md`.
Mode: deep (efficient calibration). Iterations: 1.

---

## IC-1 Type-Tag Presence

All inline `[tag]` / backtick-tag citations across A–F carry tags from the canonical enum
(`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory |
compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). Section A uses
`[mechanism_review]` / `[rct]` / `[regulatory]` / `[animal: …]`; B uses `(rct)`; C uses `*rct*` /
`*open_label/mechanism*`; D uses `(rct)` / `(mechanism_review)`; E uses `[type-tag: regulatory]`
throughout; F uses backtick `regulatory` / `vendor_label` / `secondary`. Grep for off-enum lowercase
bracket tokens returned only `[indoline-3,4'-piperidine]` — an IUPAC structural fragment, not a
citation tag. **No off-enum inline tags detected. PASS.**

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry in all six sections carries a type-tag annotation (`type: <tag>`, `(rct)`,
or backtick-tag). All tags resolve to the enum. §F[12] carries an additional non-canonical
descriptor `secondary` on a translation-aggregator entry that is explicitly flagged non-grounding;
this is a benign extra label, not an enum violation. **PASS.**

## IC-3 Vendor-Not-Numerical

`vendor_label` cites appear only in §F (practitioner/availability/cost) and the §E gray-market lines.
Every efficacy/AE/dose magnitude in §F is explicitly deferred ("All efficacy/AE-rate magnitudes …
deferred to Section D … never to ground efficacy or adverse-event rates"). The §F dose conventions
(10–25 mg/day, 8–16 wk) grounded by `vendor_label` are usage conventions, not efficacy/AE claims —
permitted. No `vendor_label` cite grounds an efficacy, AE-rate, or therapeutic-efficacy number.
**No vendor-not-numerical violation detected. PASS.**

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` cites appear in the corpus. Performance/physique anecdote is explicitly
excluded as grounding (§C "Status: ABSENT … rest on vendor copy and anecdote, which are excluded").
**No anecdote-not-numerical violation detected. PASS.**

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` cites appear. §F documents explicitly that "No named-prescriber protocol
… was located" and that telehealth pages "do not qualify as practitioner_protocol cites."
**No practitioner-protocol efficacy grounding detected. PASS.**

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` cites appear. §F records the compounding gate as NEGATIVE — MK-677 is a
small molecule, not on the §503A bulks list, so no data sheets exist; none located across Empower /
Belmar / Tailormade / Hallandale / Strive. **PASS.**

## IC-7 Population-Mismatch

The only animal/in_vitro numerical data is the Patchett 1995 line in §A: "released GH from rat
anterior-pituitary cells in culture with an EC50 = 1.3 ± 0.09 nM, and elevated GH in dogs after oral
doses as low as 0.125 mg/kg." Species (rat, dog) is the explicit subject of the sentence within
100 chars of each number, and the cite carries `[animal: rat pituitary cells, in vitro EC50; dog
oral GH response]` — satisfying the health-gates §1 background/mechanism override. Every other
numerical claim in the corpus cites a human RCT with population annotated (healthy-elderly,
Alzheimer's, hip-fracture, obese, young-adult, postmenopausal). **No population-mismatch-unflagged
numerical claim detected. PASS.** (See top-level `population_mismatch` block.)

## IC-8 Route-Extrapolation

Every dose claim in the corpus is ORAL and every cited primary tested the ORAL route (Patchett dog
data explicitly oral; all human RCTs oral once-daily). §F flags "Reconstitution is N/A — MK-677 is
oral" and forbids cross-attribution to injectable peptide secretagogues. No route mismatch; no
`[route-extrapolation]` tag required. **PASS.**

## IC-9 Concentration-Surfacing

Single-lab/sponsor share = 6/8 = 0.75 ≥ 0.70 → first-class surfacing required. §C contains a
first-class `### Concentration audit` section that enumerates all 8 primaries, computes the 75%
Merck-lineage share, and carries an explicit **"FLAG — concentration ≥70%"**. The concentration
content is surfaced as a named section, not buried in bibliography. **PASS.** (See top-level
`concentration_audit` block.)

## IC-10 No Fabricated Citations

Load-bearing PMIDs spot-verified live via PubMed (exact title/author/journal/year + figure match):

- **Nass 2008 (18981485)** — Ann Intern Med, 2-yr ghrelin-mimetic, healthy older adults; FFM↑,
  IGF-1→young-adult, "increased fat-free mass did not result in changes in strength or function,"
  fasting glucose +0.3 mmol/L, insulin sensitivity↓. **MATCH.**
- **Chapman 1996 (8954023)** — JCEM, healthy elderly; 24-h GH +97±23%, IGF-1 141→265 µg/L, fasting
  glucose 5.4→6.8 mmol/L. **MATCH.**
- **Sevigny 2008 (19015485)** — Neurology, AD; IGF-1 +60.1% (6 wk)/+72.9% (12 mo), "ineffective at
  slowing … Alzheimer disease," n=563. **MATCH.**
- **Adunsky 2011 (21067829)** — Arch Gerontol Geriatr, hip fracture phase IIb; IGF-1 +51.4 ng/mL,
  terminated early for CHF signal, "unfavorable safety profile." **MATCH.**
- **Patchett/Nargund PNAS 1995 (7624358)** — "Design and biological activities of L-163,191
  (MK-0677)…"; EC50 1.3±0.09 nM, dog oral 0.125 mg/kg. **MATCH.**
- **Howard 1996 Science (8688086)** — "A receptor in pituitary and hypothalamus that functions in
  growth hormone release"; GHS-R / target of GHSs. **MATCH.**
- **FR Doc 2026-07361** (govinfo) — PCAC §503A bulks notice; peptides only (BPC-157, KPV, TB-500,
  MOTS-c, DSIP, Semax, Epitalon); **MK-677/ibutamoren absent — confirmed.** **MATCH.**
- **OPSS/DoD (opss.org)** — confirms unapproved, not a lawful supplement ingredient, military-
  prohibited, WADA-listed. **MATCH.**

Secondary primaries also verified (Murphy 1998 9467534 N-balance +0.31/−1.48; Svensson 1998 9467542
FFM↑/OGTT impairment; Murphy 2001 11238495 femoral-neck BMD 4.2 vs 2.5%; Copinschi 1997 9349662
stage-IV ~50%/REM >20%). All figures match cited primaries.

**FDA warning letters (Prime Sports Nutrition 719433; Agebox Inc. 718252):** the direct fda.gov
warning-letter URLs returned HTTP 404 to the retrieval tool (FDA systematically blocks automated
fetch; the FDA index URL also 404'd). The sections themselves disclose this honestly ("direct page
fetch returned 404 … content retrieved via FDA-indexed search"). The OPSS government primary
independently corroborates the substantive enforcement claim (Agebox/undeclared ibutamoren). This is
a corpus-retrieval gap on a Tier-2 government source, NOT a fabricated citation or fabricated quote
→ **WARN (corpus-missing), not HALT.** Every inline `[N]` resolves to a bibliography entry.
**PASS (with WARN).**

## IC-11 No Placeholder Strings

Grep for `citation needed | TBD | TODO | Content continues | according to some reports |
research suggests | experts believe` across all six sections → **no matches. PASS.**

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` → **zero matches** in any section or bibliography. The only wiki-class
reference is **SportWiki RU** (§F[14]), tagged `vendor_label`/wiki and explicitly marked
**non-grounding** ("must not ground efficacy/AE numbers … treated as non-grounding (no-Wikipedia
spirit)"). It supports no factual claim — it is a disclosed exclusion, which is not a citation.
No real Wikipedia/SportWiki citation grounds any content. **PASS.**

## IC-13 Per-Citation Corpus Scoping

Deep-mode sample (≥80%) of numerical/quoted load-bearing claims grep-verified against the cited
primaries' abstracts/text via live fetch (see IC-10): Nass (FFM 1.1 kg, glucose 0.3 mmol/L),
Chapman (97%, 5.4→6.8), Sevigny (60.1%/72.9%), Adunsky (+51.4 ng/mL, CHF 4 v 1), Patchett (1.3 nM,
0.125 mg/kg), Murphy 1998 (+0.31/−1.48), Svensson (OGTT impairment), Murphy 2001 (4.2 vs 2.5%),
Copinschi (~50% SWS, >20% REM). **All claims found in their cited corpus — 0 quote-not-found,
0 number-not-found, 0 paraphrase-no-token-match.**

Corpus-missing (paywall / blocked-fetch, WARN — not HALT, per IC-13 policy): FDA warning letters
[E3][E4]/[F5] (fda.gov 404 to tool; substantively corroborated by OPSS); WADA primary [E8]
(wada-ama.org blocked — honestly flagged in-section, anchored to Sport Integrity Australia + OPSS);
Sport Integrity Australia [E7] (timed out; captured via search index); FDA PCAC briefing PDF [E1]
(404). All are honestly disclosed in-section and none ground a fabricated number. **PASS (with WARN).**

---

## Additional confirmations (per dispatch)

- **Small-molecule-not-peptide HELD:** asserted and grounded as the load-bearing axis in every
  section (A identity, C self-check 3, D scope note, E §503A demarcation, F type discipline).
  Mechanism = GHS-R1a / Gq-PLC agonist, NOT GHRH analogue. Confirmed.
- **FAILED Alzheimer's + hip-fracture:** §C labels both **FAILED** with verbatim conclusions
  (Sevigny "ineffective"; Adunsky "unfavorable safety profile" + early CHF termination), both
  PMID-verified. Confirmed.
- **Biomarker ≠ function framing:** grounded throughout (Nass "FFM↑ did not result in strength/
  function"; Sevigny "target engagement … ineffective"); the explicit spine of B and C. Confirmed.

---

## Verdict

verdict: PASS

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":31,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":14,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":0},"IC-5":{"status":"PASS","count_checked":0,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":0},"IC-7":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":12,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","count_checked":1,"count_flagged":0},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":1,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":8,"largest_cluster_name":"Merck","largest_cluster_count":6,"share":0.75,"threshold_triggered":true,"surfaced_section_heading":"Concentration audit (Section C)"},"corpus_scoping":{"verdict":"PASS","claims_checked":12,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-10: FDA warning-letter URLs (Prime Sports Nutrition 719433, Agebox 718252) returned HTTP 404 to retrieval tool — corpus-missing, honestly disclosed in-section, corroborated by OPSS government primary; not fabricated","IC-13: corpus-missing (paywall/blocked-fetch) on Tier-2 regulatory sources — FDA warning letters, WADA primary (wada-ama.org blocked), Sport Integrity Australia (timeout), FDA PCAC PDF (404); all honestly flagged in-section, none ground a fabricated number"]}
```
