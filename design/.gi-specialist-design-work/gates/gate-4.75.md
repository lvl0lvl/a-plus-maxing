# Gate 4.75 — Citation Integrity Verifier (GI-specialist, mode=standard)

Phase 4.75 independent adversarial integrity audit of the three judged GI-domain sections:
- `sections/section-A.md` — GI physiology, microbiome, gut barrier, biomarker validity (29 refs)
- `sections/section-B.md` — GI compounds: evidence, safety, regulatory, prescribing (33 refs incl. 2b)
- `sections/section-C.md` — clinical red-flags, consumer-test validity, safety architecture (14 refs)

Verifier ran 13 IC checks + concentration audit + 3 independent spot-verifications. All checks were
run with the verifier's OWN greps and web-fetches, not by trusting the sections' self-checks.

---

## IC-1 Type-Tag Presence

Extracted every inline `[N, tag]` citation across all three sections and validated the captured tag
against the canonical enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro |
mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol |
anecdote_aggregate`).

- Section A: tags used = `mechanism_review` (45), `meta_analysis` (13), `cohort` (8), `in_vitro` (5),
  `regulatory` (3), `animal` (1). All canonical.
- Section B: tags used = `meta_analysis` (19), `rct` (18), `regulatory` (12), `practitioner_protocol`
  (10), `mechanism_review` (4), `cohort` (3), `animal` (2). All canonical.
- Section C: tags used = `regulatory` (45), `cohort` (21), `mechanism_review` (11), `rct` (1). All
  canonical.

No untagged numeric claim was found. Every numeric effect size / sens-spec / dose / n that I sampled
carries exactly one inline single-tag citation at its point of first statement.

**Compound-tag observation (WARN, not HALT):** the multi-reference SUMMARY roll-up bundles in the
"Key claims for the agent design" sections use compound tags in two section-B lines
(`[2,3,4,5, meta_analysis/rct]` and `[17,18, meta_analysis/rct]`). These are not single `[N, tag]`
inline cites grounding a fresh numeric — they are recap bundles citing already-tagged claims, and the
compound `meta_analysis/rct` accurately spans the mixed evidence types of the bundled refs (e.g.
refs 2,3,5 are meta_analysis, ref 4 is rct). Both component tokens are in the enum. The underlying
numeric claims are each properly single-tagged where first asserted in the body. Recorded as a
language-economy WARN; does not breach IC-1 (no fresh numeric is left untagged or mis-tagged).

**Status: PASS** (count_checked ≈ 145 inline cites; count_flagged = 0).

---

## IC-2 Bibliography ↔ Inline Symmetry

Per-section, every inline `[N]` must resolve to a bibliography entry and vice versa.

- **Section A:** inline IDs {1–29} == bibliography IDs {1–29}. Symmetric. PASS.
- **Section B:** inline IDs {1–32, 2b} == bibliography IDs {1–32, 2b}. Verified `[2b, meta_analysis]`
  IS cited inline (the Hempel concordant RR 0.58 / n≈11,811 figure) and has bibliography entry 2b.
  Symmetric. PASS.
- **Section C:** inline IDs {1–14} == bibliography IDs {1–14}. Investigated an apparent orphan `[15]`:
  every literal `[15` string in section-C lives inside the iter-2/iter-3 audit-trail prose documenting
  the OLD→NEW renumber (former [15] → [14]); NONE is a live citation in the body (C-1…Key-claims). The
  former non-primary ScienceDirect aggregator (old [14]) was removed entirely and grounds no claim. No
  live orphan cite. Symmetric. PASS.

**Status: PASS.**

---

## IC-3 Vendor-Not-Numerical

Grepped all three sections for `vendor_label`. The tag appears ONLY in self-check / convention prose
asserting it is NOT used to ground numbers (e.g. "No vendor_label … grounds any number"). Zero
`[N, vendor_label]` inline citations exist; therefore no vendor cite grounds any dose/effect/n/AE/
sens/spec claim.

**Status: PASS.**

---

## IC-4 Anecdote-Not-Numerical

Grepped all three sections for `anecdote_aggregate`. Same result: appears only in self-check prose
stating non-use. Zero `[N, anecdote_aggregate]` inline citations. No anecdote cite grounds any numeric.

**Status: PASS.**

---

## IC-5 Practitioner-Protocol / Compounding-Data-Sheet Not Efficacy

`practitioner_protocol` is used in section-B (10×) and grounds the AGA/ACG prescribing-restraint
guidance and the dosing-convention table (B "Prescribing-practice conventions"). Each efficacy/effect
claim in those neighborhoods is independently grounded by a Tier-1/2 cite: e.g. the AGA/ACG cites
`[6,7, practitioner_protocol]` accompany — but do not solely ground — the AAD/CDAD/pouchitis effect
sizes, which carry their own `[2/2b/3/4/5, meta_analysis/rct]`. The dosing-convention list is
explicitly labeled "consensus dosing/cycling — explicitly NOT-efficacy." No `practitioner_protocol`
cite is the SOLE source of an efficacy claim. No `compounding_data_sheet` tag is used anywhere.

**Status: PASS.**

---

## IC-6 First-Author + Year Plausibility (fabrication-shape + spot-verify)

Scanned bibliography entries for fabrication-shaped artifacts (anomalous DOI prefixes, future dates,
fake TLDs, implausible PMIDs). All hosts are Tier-1/2 (pmc.ncbi.nlm.nih.gov, pubmed.ncbi.nlm.nih.gov,
nature.com, science.org, cochranelibrary.com, gastrojournal.org, jamanetwork.com, gi.org, fda.gov,
allergy.org.au, ncbi.nlm.nih.gov/books). DOIs/PMCIDs are well-formed; the lone 2026-dated entry
(Servetas, Commun Biol) is a real recently-indexed paper, not a future-fabrication.

Independent spot-verification of 3 load-bearing numerical claims against the cited primary sources:

1. **PROPATRIA (section-B [8, rct], PMID 18279948).** WebFetch of the PubMed record confirms VERBATIM:
   mortality 24/152 (16%) probiotic vs 9/144 (6%) placebo; **RR 2.53, 95% CI 1.22–5.25**; bowel
   ischaemia "Nine patients … (eight with fatal outcome)" vs "none in the placebo group (p=0.004)";
   298 randomized. Every figure in section-B matches the source. ✓
2. **EAACI IgG4 statement (section-C [3, regulatory], Stapel 2008, PMID 18489614).** WebFetch confirms
   the title/conclusion "Testing for IgG4 against foods is not recommended as a diagnostic tool" and the
   tolerance-not-hypersensitivity framing ("indicator for immunological tolerance, linked to … regulatory
   T cells"). Section-C's characterization matches. ✓
3. **Fecal calprotectin sens/spec (section-A [18, meta_analysis], Waugh 2013, NBK261318).** WebFetch of
   the NIHR HTA results page confirms VERBATIM "sensitivity 93% and specificity 94%, for ELISA tests, at
   a 50 µg/g cut-off … based on five studies." Section-A's 93%/94% @ 50 µg/g matches. ✓

(PubMed record for the 2023 calprotectin meta PMID 37823411 returned a reCAPTCHA wall; not load-bearing
because the Waugh 93/94 anchor independently verified. No fabrication signal anywhere.)

**Status: PASS** (0 fabrication findings; 3/3 spot-checks matched source verbatim).

---

## IC-7 Population-Mismatch

Grepped every `[N, animal]` and `[N, in_vitro]` inline cite and checked the surrounding sentence for a
numerical token and a `[population-mismatch: <species>]` tag.

- **Section A [13, animal]** (colonic MMC, mouse): carries `[population-mismatch: mouse]`; grounds a
  qualitative mechanistic statement ("altered in slow-transit constipation"), no human numeric. PASS.
- **Section A [8, in_vitro]** (zonulin ELISA): grounds qualitative assay-characterization (cross-reacts
  with properdin/C3/albumin). "C3 / pre-HP2 / haptoglobin-2" are protein names, not clinical numerics.
  No dose/effect numeric. PASS.
- **Section A [28, in_vitro]** (DTC analytical benchtest): only numeric is "seven DTC services" — a
  study-design count, not a human dose/effect/AE/sens-spec value. No population-mismatch trigger.
  (The "17 of 18 taxa" numeric for the same underlying paper lives in section-C tagged
  `mechanism_review`, not animal/in_vitro — outside IC-7 scope; see IC-10.) PASS.
- **Section B [31, animal]** (gingerols, cisplatin rodent/in-vitro model): carries
  `[population-mismatch: rodent/in-vitro cisplatin model]`; grounds a qualitative "accelerate delayed
  gastric emptying" mechanism claim, no human numeric. PASS.
- **Section C:** zero `animal`/`in_vitro` tags used. Vacuously PASS.

The zinc-carnosine numerics (threefold rise; lactulose:rhamnose 0.35→0.88; 37.5 mg BID) are grounded by
`[23, rct]` — a HUMAN n=10 crossover RCT, not animal/in_vitro — so no population-mismatch tag is
required. Correctly not flagged.

**Status: PASS** (checked_citations = 8 animal/in_vitro inline cites; flagged = 0).

---

## IC-8 Route-Extrapolation

No cross-route dose extrapolation is made. Section A carries no compound dosing. Section B doses are
route-matched: PROPATRIA = enteral (source enteral); PERT / lactase / peppermint oil / glutamine /
ginger = oral (source oral); betaine-HCl pH data is drug-induced (rabeprazole) hypochlorhydria, flagged
in-text as a POPULATION model limitation, not a route mismatch. No `[route-extrapolation]` tag is
required and none is missing. Section C carries no dose claims.

**Status: PASS.**

---

## IC-9 Concentration-Surfacing

See Concentration Audit below. Single-group share = 0.05 (« 0.70 threshold). No first-class
concentration-risk section is required; gate passes vacuously. The corpus is a diverse, multi-group GI
literature as expected.

**Status: PASS.**

---

## IC-10 Cross-Section ID Concordance

Identified every citation / identifier appearing in 2+ sections and checked agreement.

- **Massier 2021 "Blurring the picture" zonulin** — A[9] PMC8355880 / C[12] PMC8355880, PMID 33037053.
  Identifier AGREES; both tagged `mechanism_review`. PASS.
- **Power 2021 Crohn-FDR serum-zonulin cohort** — A[10] PMC8027468 / C[13] PMC8027468, PMID 33841181.
  Identifier AGREES; both tagged `cohort`. (A's byline reads "Sapone-type cohort," C's reads "Power N et
  al."; same title + same PMCID resolve to the SAME paper, C's named byline is the precise one — minor
  byline looseness in A, not an identifier mismatch.) PASS.
- **USPSTF CRC age threshold** — appears only in section-C [9] (Davidson 2021, JAMA, 2779985): age 45,
  Grade A 50–75, Grade B 45–49. Internally consistent across its three section-C mentions; sections A/B
  do not reference it, so no cross-section conflict. PASS.
- **PROPATRIA** — appears only in section-B. No cross-section conflict.

**Tag-discordance WARN (not HALT):** two sources are tagged DIFFERENTLY across sections, though their
identifiers agree:
  - DTC analytical benchtest (PMC12946161 / DOI 10.1038/s42003-025-09301-3): A[28] `in_vitro` vs C[7]
    `mechanism_review`.
  - DTC-regulation analysis (PMC12728816): A[29] `regulatory` vs C[8] `mechanism_review`.
  In each case the IC-10-scoped identifier (PMCID/DOI) AGREES, the divergent tag is independently
  defensible for the source class (an analytical benchtest reads as either in_vitro or methods-review;
  a regulatory-framework analysis reads as either regulatory or mechanism_review), and — decisively for
  integrity — NEITHER tagging grounds a population-mismatch-required clinical numeric (the cited claims
  are methodological/qualitative: "seven services," "17/18 taxa," "no regulator-approved test"). No
  numeric-integrity rule is breached under either tag. Recorded as WARN for downstream tag-harmonization,
  not a HALT.

**Status: PASS** (identifier concordance holds for every shared source; 2 tag-discordance WARNs).

---

## IC-11 No Placeholder Strings

Grepped for `TBD | TODO | lorem | <...> | [citation needed] | "Content continues" | "according to some
reports" | "research suggests" | "experts believe" | XXX`. The only match ("todo") was a substring of
the author surname "Chris**todo**ulides" (section-B [13]) — a false positive, not a placeholder. No
real placeholder strings present.

**Status: PASS.**

---

## IC-12 No Wikipedia / Excluded Sources

Grepped for `wikipedia.org | reddit.com | examine.com` in all bibliographies. Zero hits. No Wikipedia or
excluded source is cited as primary. All bibliography hosts are Tier-1/2 whitelisted.

**Status: PASS.**

---

## IC-13 Per-Citation Corpus Scoping

Full per-citation corpus grep is a deep+/ultradeep check. In standard mode this check is SKIP-mode per
`citation-integrity.md §IC-13` mode policy. (Note: the IC-6 spot-verify above independently corpus-checked
3 load-bearing claims against their primaries as an adversarial sample, all PASS — but the systematic
≥50% corpus-scoping sweep is not run in standard mode here.)

**Status: SKIP-mode.**

---

## Concentration Audit

Enumerated all distinct PRIMARY citations (tags ∈ {rct, meta_analysis, cohort, open_label, animal,
in_vitro}) across all three sections and deduplicated.

- Section A primaries: 12 (refs 4, 5, 8, 10, 12, 13, 18, 19, 20, 21, 24, 28).
- Section B primaries: 24 (refs 1, 2, 2b, 3, 4, 5, 8, 11, 12, 13, 14, 15, 17, 18, 20, 22, 23, 25, 26,
  27, 28, 29, 30, 31).
- Section C primaries: 3 (refs 10, 13, 14). [C-7/C-8/C-11/C-12 are `mechanism_review` → non-primary.]
- Raw total = 39. Cross-section duplicate: Power 2021 zonulin (A[10] == C[13], PMC8027468) → −1.
  (Servetas DTC paper counts once as a primary via A[28] `in_vitro`; C[7] tags it `mechanism_review`,
  non-primary.)
- **Distinct primaries = 38.**

Largest single-lab / single-group cluster: the SBI sponsor-linked cluster (B[25] Wilson 2013 + B[26]
pediatric d-IBS) = 2. (Ford AC is senior author on B[12] and B[28] — also 2, different first authors.)
No group exceeds 2.

- **largest_cluster_count = 2** (SBI sponsor cluster).
- **share = 2 / 38 = 0.053** (well below the 0.70 threshold).
- **threshold_triggered = false.**

Section-B already surfaces the SBI single-cluster flag first-class in the B-5 "Concentration-audit note"
and Self-check; this is correct hygiene even though the global share does not mandate a first-class
section. Gate passes vacuously.

**Status: PASS.**

---

## Spot-Verify Summary

3/3 independent web-verifications matched the cited sources verbatim:
1. PROPATRIA RR 2.53 (95% CI 1.22–5.25), 16% vs 6% mortality, bowel ischaemia 9 vs 0 p=0.004, n=298
   — PMID 18279948. ✓
2. EAACI/Stapel 2008 "IgG4 … not recommended as a diagnostic tool" + tolerance framing — PMID 18489614. ✓
3. Fecal calprotectin sensitivity 93% / specificity 94% @ 50 µg/g (5 ELISA studies) — Waugh 2013
   NBK261318. ✓

No discrepancy surfaced. No IC-6 fabrication finding.

---

## Verdict

verdict: PASS

- All 12 active IC checks PASS (IC-13 SKIP-mode per standard mode).
- population_mismatch: PASS (8 animal/in_vitro cites checked, 0 unflagged numeric).
- concentration_audit: PASS (38 distinct primaries, largest cluster 2, share 0.05, threshold not
  triggered).
- corpus_scoping: SKIP-mode (standard).
- halt_reasons: none.
- warnings: (1) IC-1 compound `meta_analysis/rct` tags in two section-B summary roll-up bundles
  (language-economy only; underlying claims single-tagged); (2) IC-10 tag-discordance on two shared DTC
  sources (A in_vitro/regulatory vs C mechanism_review) — identifiers agree, no numeric-integrity breach
  under either tag, flagged for downstream tag-harmonization.

No real integrity violation found. Gate does not HALT.
