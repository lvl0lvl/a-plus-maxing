# Gate 4.75 — Citation Integrity Verification
**Run date:** 2026-06-20
**Sections checked:** section-A.md, section-B.md, section-C.md, section-D.md, section-E.md
**Verifier:** IC-1 through IC-13 + population-mismatch + concentration-audit + corpus-scoping

---

## Verdict

verdict: PASS

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {
      "status": "PASS",
      "count_checked": 72,
      "count_flagged": 0
    },
    "IC-2": {
      "status": "PASS",
      "count_checked": 42,
      "count_flagged": 0
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 6,
      "count_flagged": 0
    },
    "IC-4": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0
    },
    "IC-5": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-6": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-7": {
      "status": "PASS",
      "count_checked": 28,
      "count_flagged": 0
    },
    "IC-8": {
      "status": "PASS",
      "count_checked": 6,
      "count_flagged": 0
    },
    "IC-9": {
      "status": "PASS",
      "count_checked": 8,
      "count_flagged": 0
    },
    "IC-10": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-11": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-12": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-13": {
      "status": "WARN",
      "count_checked": 6,
      "count_flagged": 3,
      "findings": [
        "Claim: '11.73-fold greater reduction in viability of senescent versus proliferating IMR90 cells' [B:section-B.md line 7, cite 1, in_vitro] — figure-level numerical claim; abstract of PMID 28340339 confirmed (title/author/year/journal match, selectivity described qualitatively) but exact figure not in abstract; PMC full text blocked by reCAPTCHA — corpus-missing WARN, not HALT",
        "Claim: 'approximately 5-fold higher binding affinity (Kd ~400 ± 280 nM for FOXO4-DRI vs. ~2.5 µM for FOXO4-FH)' [section-A.md, cite 2, in_vitro] — Kd values not present in PMID 40593617 abstract (p53 TAD2 binding target and phosphorylation-enhanced affinity confirmed; full-text paywall); corpus-missing WARN for specific Kd numbers",
        "Claim: 'n=7–8 mice per treatment group for the XpdTTD cohorts (Fig. 6K)' [section-B.md, cite 1, animal] — figure-caption-level claim; abstract of PMID 28340339 does not state n values; PMC full text blocked — corpus-missing WARN for n values"
      ]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 28,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 8,
    "largest_cluster_name": "de Keizer (Erasmus MC/UMC Utrecht)",
    "largest_cluster_count": 1,
    "share": 0.125,
    "threshold_triggered": false
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 6,
    "claims_failed": [
      {
        "claim": "11.73-fold greater reduction in viability of senescent versus proliferating IMR90 cells",
        "cite_key": "baar-2017-28340339",
        "failure_mode": "corpus-missing",
        "note": "PMC full text blocked by reCAPTCHA; abstract confirmed; claim consistent with abstract qualitative selectivity statement; WARN not HALT"
      },
      {
        "claim": "Kd ~400 ± 280 nM for FOXO4-DRI vs. ~2.5 µM for FOXO4-FH; approximately 5-fold higher binding affinity",
        "cite_key": "bourgeois-2025-40593617",
        "failure_mode": "corpus-missing",
        "note": "Abstract confirms p53 TAD2 as binding target and phosphorylation-enhanced affinity; Kd numbers not in abstract; full-text paywall (Nature Communications); WARN not HALT"
      },
      {
        "claim": "n=7–8 mice per treatment group for the XpdTTD cohorts (Fig. 6K)",
        "cite_key": "baar-2017-28340339",
        "failure_mode": "corpus-missing",
        "note": "Figure-caption detail; abstract confirmed; full text blocked; WARN not HALT"
      }
    ]
  },
  "halt_reasons": [],
  "warnings": [
    "IC-13: 3 corpus-missing WARNs (paywall/reCAPTCHA barrier) — no quote-not-found or number-not-found failures; all 5 spot-checked PMIDs confirmed by PubMed direct fetch"
  ]
}
```

---

## IC-1 — Type-Tag Presence

**Status: PASS**

Enumerated all inline citations across all 5 sections. Every `[N, tag]` pair carries a tag from the canonical 12-enum set. Count by tag across sections:
- `in_vitro`: sections A (×14), B (×6), C (×3), D (×3), E (×2) — all valid
- `animal`: sections A (×4), B (×19), C (×8), D (×4), E (×1) — all valid
- `mechanism_review`: sections A (×5), B (×0), C (×5), D (×3) — all valid
- `regulatory`: sections C (×2), D (×6), E (×2) — all valid
- `vendor_label`: section D (×2), E (×3) — all valid
- `anecdote_aggregate`: section D (×1) — valid
- `open_label`: section C (×1) — valid

**Special multimodal handling (Baar 2017 [1] in Section B):** Section B uses per-claim dual tags for Baar 2017: `[1, in_vitro]` for the IMR90 selectivity data and `[1, animal]` for the mouse in vivo data. This is INTENTIONAL multimodal tagging per the verifier brief and is accepted. No invalid tags detected.

No findings.

---

## IC-2 — Bibliography Type-Tag Presence

**Status: PASS**

Every bibliography entry across all 5 sections carries `— tag: X — tier: N` in the standard format. Enumerated all 42 bibliography entries (A:7, B:7, C:11, D:11, E:6). Every entry has both a `tag:` field and a `tier:` field. All tags are from the canonical enum.

Notable entries checked:
- Section A [1]: `tag: in_vitro — tier: 1` (Baar 2017 in Section A = in vitro foundational context; in Section B bib the same PMID appears with `tag: animal — tier: 1` for the in vivo data — dual-section bibliography with context-appropriate tags: PASS)
- Section D [3]: `tag: anecdote_aggregate — tier: 3` — valid
- Section D [2]: `tag: vendor_label — tier: 3` — valid
- Section E [5]: `tag: vendor_label — tier: 3` — valid (BusinessWire)

No findings.

---

## IC-3 — Vendor-Not-Numerical

**Status: PASS**

Identified all `vendor_label` citations across sections:
- Section D [2]: iRemedy Healthcare — used for "Research use only — not suitable for compounding" and "PK data gap corroboration." No numerical efficacy claim in sentence.
- Section D [8]: Peptpedia.org — used as secondary mechanism summary, no numerical claim.
- Section E [2]: Cleara Biotech — used for company pipeline description, COI disclosure. The "29% overall survival increase" figure appears in E.2 but is explicitly hedged as "a company relay of unpublished third-party data" and not presented as an established numerical finding. The sentence states: "Cleara's history page states that 'third party experiments showed CL04183 to induce an impressive 29% overall survival increase in geriatric mice' — this figure is a corporate relay of unpublished third-party data; it has not been independently verified in peer-reviewed literature." Tag = `vendor_label`, and the prose explicitly disavows the number as fact. IC-3 tests whether vendor_label grounds a numerical claim as a factual assertion; this sentence quotes and immediately disclaims the company claim. PASS.
- Section E [5]: BusinessWire seed-round figure ($2.5M) — financial figure, not efficacy/AE/dose. Excluded from IC-3 scope.
- Section E [6]: NovoPro Labs — used for "net peptide content of 69.92%" (reconstitution math context) and pricing. The 69.92% figure is explicitly purity/content math, not efficacy. PASS.

No efficacy, AE rate, or therapeutic dose numeric claim found grounded solely in a `vendor_label` citation.

---

## IC-4 — Anecdote-Not-Numerical

**Status: PASS**

One `anecdote_aggregate` citation exists: Section D [3] (Peptibase, "commonly 2–10 mg subcutaneous every other day for 3 doses per cycle"). The sentence reads: "Grey-market sources circulate community protocols (commonly 2–10 mg subcutaneous every other day for 3 doses per cycle, citing the mouse 5 mg/kg figure as a loose allometric proxy), but these figures are unvalidated and may NOT ground any numerical safety claim [3, anecdote_aggregate]."

The 2–10 mg range is characterized as unvalidated circulating-claims, explicitly denoted as non-evidentiary, and the tag appears with a caveat ("may NOT ground any numerical safety claim"). This is a qualitative characterization of community dosing lore, not a dose recommendation or efficacy figure grounded in the anecdote source. PASS.

---

## IC-5 — Practitioner-Protocol-Not-Efficacy

**Status: PASS**

No `practitioner_protocol` citations present in any section. Not applicable.

---

## IC-6 — Compounding-Data-Sheet-With-Efficacy

**Status: PASS**

No `compounding_data_sheet` citations present in any section. Not applicable.

---

## IC-7 — Population-Mismatch

**Status: PASS**

FOXO4-DRI is entirely preclinical. Checked 28 animal/in_vitro inline citations for population-mismatch compliance:

**Animal citations — species/model named in sentence or within 100 chars:**
- Section A [4, animal]: "naturally aged male mice (20–24 months old, n = 10/group)" — species, sex, age, n all stated within sentence. PASS.
- Section B [1, animal] (multiple): "Male C57BL/6 mice aged approximately 24 months," "XpdTTD mice carry a homozygous Xpd^TTD/TTD mutation," "Young male C57BL/6 mice" — species named each time. PASS.
- Section B [2, animal]: "naturally aged male C57BL/6 mice (n = 6 per treated group, ages 20–24 months; young controls 3 months, n = 10)" — full specification. PASS.
- Section B [3, animal]: "Aged male mice" with Sun Yat-sen context. PASS.
- Section B [4, in_vitro]: "in vitro expanded human articular chondrocytes from 8 non-osteoarthritic donors (ages 15–73)" — human primary cells clearly identified. PASS.
- Section B [5, animal]: "male C57BL/6J mice aged 6–8 weeks (n = 5 per group)" — named. PASS.
- Section B [6, animal]: "naturally aged male and female mice (17 months, n ≥ 4–6 per group) and a D-galactose progeroid model" — named. PASS.
- Section C [2, animal]: "INK-ATTAC progeroid mice, n = 21–32/group" — named. PASS.
- Section C [3, animal]: "wild-type C57BL/6 and F1 hybrid mice; median lifespan increase ~25% in males" — species named. PASS.

**Critical check — D+Q human data correctly attributed (NOT to FOXO4-DRI):**
- Section C [4, open_label]: "humans, n = 9, diabetic kidney disease, mean age 68.7 yr" — explicitly attributed to Hickson et al. (D+Q), clearly distinguished from FOXO4-DRI. PASS.
- Section B.4 explicitly states: "All efficacy data for FOXO4-DRI is preclinical — mouse models and cell culture." PASS.
- Section C.3 explicitly states: "No claim that FOXO4-DRI produces senolytic effects or any health benefit in humans is supported by evidence." PASS.

No animal finding is stated as human-established. No population-mismatch violation detected across all 28 checked citations.

---

## IC-8 — Route-Extrapolation

**Status: PASS**

Dose/route claims checked across sections:

1. **Section B.2, Model 1 (aged mice):** "5 mg/kg intraperitoneally (i.p.)" — report states IP, source (Baar 2017) used IP. Match. PASS.
2. **Section B.2, Model 2 (XpdTTD):** "5 mg/kg intravenously (i.v.) — distinct from the i.p. route used in the aged-mouse arm" — report flags the within-study route difference explicitly. PASS.
3. **Section B.2, Model 3 (doxorubicin):** "intravenously (i.v.) at 5 mg/kg" — consistent with Baar 2017 IV arm. PASS.
4. **Section D.1, grey-market community protocols:** "2–10 mg subcutaneous every other day" tagged `[3, anecdote_aggregate]` with explicit note that subcutaneous route "has not been formally evaluated in any published study" (D.2). The anecdote_aggregate tag correctly captures the non-evidence basis. No route-extrapolation tag required here since these are not presented as dose claims grounded in animal literature.
5. **Section D.2:** "Subcutaneous administration has not been formally evaluated in any published study" — explicit disclosure. PASS.
6. **Section B.3.1 (Zhang 2020):** "5 mg/kg i.p., every other day, three doses" — IP in both claim and source (PMID 31959736). PASS.

No untagged route-extrapolation from animal source to different human route detected.

---

## IC-9 — Concentration-Surfacing

**Status: PASS**

Section E.1 contains a full concentration audit table with 8 primary papers enumerated by lead/corresponding authorship group. Result:

| Group | Papers (lead author) | de Keizer? |
|-------|---------------------|------------|
| de Keizer (Erasmus/Utrecht) | 1/8 (PMID 28340339) | YES (sole) |
| Bourgeois/Madl (Graz) + de Keizer co-author | 1/8 (PMID 40593617) | PARTIAL co-author |
| 6 fully independent groups | 6/8 | NO |

**Largest single-group share:** 1/8 = 12.5% (de Keizer as lead/corresponding author). Even counting the Bourgeois 2025 co-authorship generously, maximum = 2/8 = 25%.

**70% threshold:** NOT triggered. Threshold_triggered = FALSE.

Section E.1 explicitly states: "The 70% single-group threshold is not met" and "de Keizer's group holds sole lead authorship on 1 of 8 primary papers (12.5%)." The concentration surface disclosure is present in Section E as a dedicated subsection prior to commercialization discussion. PASS.

---

## IC-10 — No Fabricated Citations

**Status: PASS**

Spot-checked 5 PMIDs via direct PubMed/eutils fetch:

| PMID | Expected | Confirmed |
|------|----------|-----------|
| 28340339 | Baar 2017, Cell, "Targeted Apoptosis..." | CONFIRMED: title, first author (Marjolein P. Baar), year 2017, journal Cell |
| 40593617 | Bourgeois 2025, Nat Commun, "disordered p53..." | CONFIRMED: title, first author (Benjamin Bourgeois), year 2025, journal Nature Communications |
| 31959736 | Zhang 2020, Aging Albany, "FOXO4-DRI alleviates age-related testosterone..." | CONFIRMED: title, first author (Chi Zhang), year 2020, journal Aging (Albany NY); n=6/group, 5 mg/kg IP confirmed |
| 34959346 | Lucana 2021, Pharmaceutics, "Protease-Resistant Peptides..." | CONFIRMED: title, first author (Maria C. Lucana), year 2021, journal Pharmaceutics |
| 35510614 | Han 2022, J Cell Mol Med, "FOXO4 peptide targets myofibroblast..." | CONFIRMED: title, first author (Xiaodan Han), year 2022, journal J Cellular and Molecular Medicine; n=5 per group, bleomycin model confirmed |

All bibliography entries resolve to numbered inline citations; no orphaned inline cites detected. No fabricated citations found.

---

## IC-11 — No Placeholder Strings

**Status: PASS**

Grepped all 5 sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No matches found in any section.

---

## IC-12 — No Wikipedia Citations

**Status: PASS**

Grepped all 5 sections and bibliography blocks for `wikipedia.org`, `en.wikipedia`, `ru.wikipedia` and all Wikipedia variants.

No Wikipedia URLs found in any bibliography entry or inline citation.

---

## IC-13 — Per-Citation Corpus Scoping

**Status: WARN** (3 corpus-missing; no number-not-found or quote-not-found failures)

**Claims checked (6 load-bearing numerical/scope claims):**

### Claim 1: 11.73-fold selectivity [section-B.md, cite 1, in_vitro]
- Cite: Baar 2017, PMID 28340339
- Fetch: PubMed abstract confirmed (title/author/year/journal); PMC full text (PMC5383082) blocked by reCAPTCHA
- Abstract says "selectively causes p53 nuclear exclusion and cell-intrinsic apoptosis" — qualitatively consistent; exact figure lives in paper body/figure
- **Result: corpus-missing WARN** — claim is plausible and consistent; PMID is genuine; exact figure unverifiable from abstract alone
- Not a HALT (no evidence of number-not-found; source is confirmed genuine)

### Claim 2: Kd ~400 ± 280 nM (FOXO4-DRI) vs ~2.5 µM (FOXO4-FH); 5-fold affinity difference [section-A.md, cite 2, in_vitro]
- Cite: Bourgeois 2025, PMID 40593617
- Fetch: PubMed abstract confirmed (title/author/year/journal: Nature Communications 2025); full text paywall
- Abstract confirms: p53 TAD2 as binding target, phosphorylation enhances affinity for both FOXO4 and FOXO4-DRI, cationic cell permeability peptide contributes to binding — all mechanistic claims in section A corroborated
- Specific Kd numbers not in abstract (they are NMR measurement results, typically in paper body)
- **Result: corpus-missing WARN** — paper is genuine, mechanism confirmed, specific values need full text

### Claim 3: n=7–8 mice per treatment group for XpdTTD cohorts (Fig. 6K) [section-B.md, cite 1, animal]
- Cite: Baar 2017, PMID 28340339
- Fetch: Abstract confirmed; figure-level n values not in abstract
- **Result: corpus-missing WARN** — figure-caption detail requires full text; source PMID confirmed genuine

### Claim 4: Zhang 2020 — n=6 per group, 20–24 month mice, 5 mg/kg IP [section-B.md, cite 2, animal]
- Cite: PMID 31959736
- Fetch: PubMed direct fetch confirmed n=6 per group, ages 20–24 months, dose 5 mg/kg IP every other day
- **Result: PASS** — numerical claims confirmed in PubMed-surfaced metadata

### Claim 5: Han 2022 — n=5 per group, bleomycin model [section-B.md, cite 5, animal]
- Cite: PMID 35510614
- Fetch: Confirmed n=5 per group, bleomycin-induced pulmonary fibrosis, C57BL/6 mice
- **Result: PASS** — confirmed

### Claim 6: Bourgeois 2025 — p53 TAD2 as binding target; cationic permeability peptide contributes to binding [section-A.md, cite 2, in_vitro; section-B.md, cite 7, in_vitro]
- Fetch: Abstract confirmed both claims verbatim: "the disordered FOXO4-DRI binds to the disordered p53TAD2 and forms a transiently folded complex" and "both, the FOXO4-derived region and the cationic cell permeability peptide contribute to the interaction"
- **Result: PASS** — paraphrase tokens confirmed in abstract

**Summary:** 3/6 claims PASS with direct corpus confirmation; 3/6 are corpus-missing WARNs (paywall/reCAPTCHA blocking full text for Baar 2017 and Bourgeois 2025). Zero `number-not-found` failures. Zero `quote-not-found` failures. No HALT warranted.

---

## Population-Mismatch (top-level mirror)

**Verdict: PASS**

FOXO4-DRI is entirely preclinical. Confirmed across all sections:
- All in vivo efficacy data attributed to mouse models with species/n/route stated
- D+Q human data (Hickson, n=9) explicitly attributed to the OTHER compound's evidence base in section C
- No human-established efficacy claim for FOXO4-DRI anywhere in 5 sections
- B.4 and C.3 contain explicit human-data-absence disclosures

Checked citations: 28. Flagged: 0.

---

## Concentration Audit (top-level mirror)

**Verdict: PASS**

Total primary papers enumerated: 8 (per Section E.1 table, PMIDs: 28340339, 31959736, 33996787, 36515093, 39025385, 39994346, 40593617, 41625068).

Largest single cluster: de Keizer group (Erasmus MC/UMC Utrecht) — lead authorship on 1/8 papers (12.5%). Co-authorship on 1 additional paper (Bourgeois 2025 — Graz-led with de Keizer as non-lead co-author). Even counting co-authorship generously: ≤ 2/8 = 25%.

70% threshold: NOT triggered. Multi-continental independent replication confirmed (Chinese university hospitals, French INSERM, US bioengineering, Beijing academic medical center, Austrian NMR group).

threshold_triggered: false
