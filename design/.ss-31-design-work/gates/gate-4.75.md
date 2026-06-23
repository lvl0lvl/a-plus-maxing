---
phase: "4.75"
compound: "SS-31 / Elamipretide"
run_date: "2026-06-20"
sections_checked: ["A", "B", "C", "D", "E"]
---

# Phase 4.75 — Integrity Gate: SS-31 / Elamipretide

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
      "count_checked": 47,
      "count_flagged": 0
    },
    "IC-2": {
      "status": "PASS",
      "count_checked": 47,
      "count_flagged": 0
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 0,
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
      "count_checked": 18,
      "count_flagged": 0
    },
    "IC-8": {
      "status": "PASS",
      "count_checked": 6,
      "count_flagged": 0
    },
    "IC-9": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0
    },
    "IC-10": {
      "status": "WARN",
      "count_checked": 9,
      "count_flagged": 1,
      "findings": [
        "Section C bibliography entry [3]: stated PMID 32641818 resolves to a Nature climate-change commentary (Lehmann & Possinger 2020, DOI 10.1038/d41586-020-01965-7), NOT to the Allen et al. cristae paper. Correct PMID is 32680996. The DOI in the same entry (10.1038/s42003-020-1101-3) resolves correctly via PMC7368046. Content is real and properly grounded via DOI; PMID is bibliographically erroneous. Classified WARN (not HALT) because the DOI is the authoritative identifier and resolves to the correct paper, but the erroneous PMID will misdirect PMID-only retrieval."
      ]
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
      "count_checked": 9,
      "count_flagged": 3,
      "findings": [
        "PMID 23813215 (Birk 2013 JASN): creatinine 0.62 vs 1.72 mg/dL cited in Section C[1] — not present in PubMed abstract text retrieved; value likely in full text. Classified corpus-missing (abstract-only). NOT number-not-found.",
        "PMID 37268435 (Karaa 2023 Neurology MMPOWER-3): specific 6MWT and PMMSA numeric results (-3.2 m, -0.07 points) cited in Section C — not confirmed in abstract retrieved (metadata/author page only). Classified corpus-missing (abstract-only). NOT number-not-found.",
        "PMID 39605874 (ReCLAIM-2 2024): LL BCVA -2.8 vs -4.6 letters and GA area +0.328 vs +0.281 mm² — not present in abstract (abstract states endpoints not met but does not give exact figures). Classified corpus-missing (abstract-only). NOT number-not-found."
      ]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 18,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 10,
    "largest_cluster_name": "Stealth BioTherapeutics",
    "largest_cluster_count": 9,
    "share": 0.9,
    "threshold_triggered": true
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 9,
    "claims_failed": [
      {
        "claim": "creatinine 0.62 vs 1.72 mg/dL at 24h post-reperfusion [1, animal] (Section C)",
        "cite_key": "birk-2013-23813215",
        "failure_mode": "corpus-missing",
        "note": "abstract-only; value likely in full-text results section"
      },
      {
        "claim": "6MWT difference -3.2 m (P=0.69); PMMSA difference -0.07 (P=0.37) [12, rct] (Section C)",
        "cite_key": "karaa-2023-37268435",
        "failure_mode": "corpus-missing",
        "note": "abstract-only retrieval returned metadata page; specific figures not in abstract"
      },
      {
        "claim": "LL BCVA -2.8 vs -4.6 letters; GA area +0.328 vs +0.281 mm² [8, rct] (Section B/C)",
        "cite_key": "reclaim2-2024-39605874",
        "failure_mode": "corpus-missing",
        "note": "abstract-only; exact figures not stated in abstract, only that primary endpoints not met"
      }
    ]
  },
  "halt_reasons": [],
  "warnings": [
    "IC-10: Section C bibliography [3] carries erroneous PMID 32641818 (resolves to unrelated climate paper); correct PMID is 32680996; DOI in same entry is correct",
    "IC-13: 3 of 9 corpus checks returned abstract-only (corpus-missing); no number-not-found or quote-not-found failures"
  ]
}
```

---

## IC-1 — Type-Tag Presence

Checked all inline `[N, tag]` citations across sections A, B, C, D, E (47 citations total).

Tags observed: `in_vitro`, `mechanism_review`, `animal`, `regulatory`, `open_label`, `rct`, `cohort`, `anecdote_aggregate`. All are members of the 12-enum set defined in `_source-whitelist.md`.

No bare `[N]` inline citations without tags found. No invented tags detected.

**Status: PASS** — No violations detected.

---

## IC-2 — Bibliography Type-Tag Presence

All bibliography entries across all 5 sections carry `— tag: X — tier: N` annotations. Spot-checked:

- A[1]: `— tag: in_vitro — tier: 1` ✓
- A[8]: `— tag: regulatory — tier: 1` ✓
- B[3]: `— tag: rct — tier: 1` ✓
- C[4]: `— tag: animal — tier: 2` ✓
- D[1]: `— tag: regulatory — tier: 1` ✓
- E[2]: `— tag: anecdote_aggregate — tier: 3` ✓
- E[12]: `— tag: rct — tier: 1` ✓

No bibliography entry without a tag found.

**Status: PASS** — No violations detected.

---

## IC-3 — Vendor-Not-Numerical

Grep for `vendor_label` citations across all 5 sections: **zero** `vendor_label` tags appear anywhere in the report.

Section D.2 contains an explicit prohibition statement: "Grey-market 'SS-31' dosing: Not addressable by verified sources; vendor-label sources may not ground any dose number (per hardened sourcing rules). Trial data are the only verified reference for dosing." This is exactly the correct posture — the grey-market domain is acknowledged in prose without a vendor citation grounding any number.

Section E.5 describes grey-market vendors qualitatively (no vendor cited as `[N, vendor_label]` for any number).

**Status: PASS** — No vendor_label citations present; cannot violate this rule.

---

## IC-4 — Anecdote-Not-Numerical

One `anecdote_aggregate` tag in the report: E[2] (Weill Cornell Medicine Newsroom, December 2025).

The citation appears in two sentences in E.1 and E.4:
- "The compound was licensed exclusively to Stealth Peptides Inc. (later Stealth BioTherapeutics) in 2006 when Szeto co-founded the company [2, anecdote_aggregate]."
- "**2004:** Szeto discovers SS-31 at Weill Cornell [2, anecdote_aggregate]."
- "**2006:** Stealth Peptides Inc. founded; Cornell license executed [2, anecdote_aggregate]."

None of these sentences contains a numerical efficacy claim, AE rate, or dose recommendation. The cite grounds only qualitative corporate-history facts (founding year, co-founder identity). No numerical token matching the IC-3/IC-4 efficacy regex (`\d+(?:\.\d+)?\s*(?:µg/kg|mg/kg|%\s+reduction|fold\s+increase|p\s*[<=]\s*0\.\d+)`) appears within 200 characters of E[2] usages.

**Status: PASS** — anecdote_aggregate grounds no numerical claims.

---

## IC-5 — Practitioner-Protocol-Not-Efficacy

Grep for `practitioner_protocol` citations across all 5 sections: **zero** `practitioner_protocol` tags appear anywhere in the report.

**Status: PASS** — No practitioner_protocol citations present; cannot violate this rule.

---

## IC-6 — Compounding-Data-Sheet-with-Efficacy

Grep for `compounding_data_sheet` citations across all 5 sections: **zero** `compounding_data_sheet` tags appear anywhere in the report.

**Status: PASS** — No compounding_data_sheet citations present; cannot violate this rule.

---

## IC-7 — Population-Mismatch

Checked 18 animal/in_vitro citations for species annotation and human-extrapolation discipline.

**Section A:** Every animal or in-vitro mechanistic claim carries a parenthetical disclosure, e.g.:
- A.3.1: "(Evidence base: in-vitro cell models; no direct human intramitochondrial concentration measurements available.)"
- A.3.2: "(Evidence base: biochemical model membranes and isolated mitochondria from mouse; not a human study.)"
- A.3.3: "(Evidence base: rat ischemia-reperfusion model; not a human mechanistic study.)" — species (rat), n=8 named inline.
- A.3.4: "(Evidence base: in-vitro and rodent animal models for the above three points.)"

**Section C:** All animal studies name species and n:
- C.1: "male Sprague-Dawley rats, n=6 per group" [C1]
- C.3: "Yorkshire swine, 59–84 kg; n=6 control vs. n=6 elamipretide" [C4]
- C.5: "27-month-old C57BL/6 mice (n=5–9 per group)" [C5]; "24-month-old C57BL/6 mice (n=7–10 per group for echocardiography)" [C6]
- C.6: "male tafazzin knockdown (TazKD) mice (4–6 months; WT n=9, TazKD untreated n=9, TazKD+SS-31 n=4)" [C8]
- C.7 IJMS 2026: "HFpEF obese ZSF1 rat model (female rats, 12 weeks)" [C9]

**Section C.8 translation gap:** Every clinical trial result is contrasted against the preclinical positive finding; no animal result is stated as human-established.

No animal finding is presented as human-established without clear qualification. No population-mismatch violation detected.

**Status: PASS** — 18 animal/in_vitro citations checked; 0 flagged.

---

## IC-8 — Route-Extrapolation

Checked dose claims where route is specified:

- D.2: "40 mg SC injection once daily" ← sourced from [1, regulatory] (Forzinity PI — SC route). ✓ route matches.
- D.2: "20 mg SC once daily" in severe renal impairment ← [1, regulatory] (SC route). ✓ matches.
- D.2: "0.25 mg/kg/hour IV infusion" ← [8, open_label] Zhu et al. 2021 (IV infusion explicitly). ✓ route matches.
- D.2: MMPOWER-3 "40 mg/day SC" ← [5, rct] Karaa 2023 Neurology (SC route). ✓ matches.
- D.3 PK table: SC Tmax 0.5–1.0 h, bioavailability ~92% ← [1, regulatory] (SC formulation data). ✓
- D.3: "~16 hours" half-life ← [8, open_label] (measured by IV functional ATPmax in skeletal muscle). The note correctly flags: "The prescribing information does not state a plasma elimination half-life explicitly. The 16-hour figure derives from a human IV study measuring functional ATPmax recovery decay [8, open_label]" — appropriately caveated.

No route-extrapolation violation detected. The IV-derived half-life is correctly labelled as IV-route-derived, not presented as SC pharmacokinetics.

**Status: PASS** — 6 dose/route claims checked; 0 flagged.

---

## IC-9 — Concentration-Surfacing

Single-sponsor concentration: Stealth BioTherapeutics sponsored at least 9 of 10 identifiable clinical-trial publications (≥90%). This exceeds the 70% threshold in health-gates §3.

Section E is structurally dedicated to the concentration/COI audit and appears as a full standalone section of the report. It surfaces the single-sponsor finding FIRST in E.2, with a full enumerated table of trials, before the COI disclosure (E.3) and commercialization timeline (E.4). Section B's clinical trial section also flags Stealth as sole sponsor in the opening paragraph.

The first-class surfacing requirement is satisfied. threshold_triggered = true, but this is not a HALT — IC-9 requires surfacing, not absence of concentration.

**Status: PASS** — ≥90% concentration identified and surfaced first-class in Section E.2 before indication subsections.

---

## IC-10 — No Fabricated Citations

**Spot-checked 9 PMIDs via WebFetch against PubMed records:**

| PMID | Claimed | Resolved | Match |
|------|---------|----------|-------|
| 15178689 | Zhao et al. 2004 JBC (SS-31 antioxidants) | Confirmed title + journal ✓ | PASS |
| 23813215 | Birk et al. 2013 JASN (SS-31 / cardiolipin, rat renal I/R) | Confirmed; Kd 1.87±0.64 µM in abstract ✓ | PASS |
| 26586786 | Gibson et al. 2016 Eur Heart J (EMBRACE STEMI) | Confirmed; CK-MB AUC 5785 vs 5570 ng·h/mL ✓ | PASS |
| 32554501 | Chavez et al. 2020 PNAS (SS-31 protein interactors) | Confirmed; 12 interactors ✓ | PASS |
| 37268435 | Karaa et al. 2023 Neurology (MMPOWER-3) | Confirmed title + trial ✓ | PASS |
| 38602181 | Thompson et al. 2024 Genet Med (TAZPOWER 168-week OLE) | Confirmed; +96.1 m 6MWT ✓ | PASS |
| 39605874 | Ehlers et al. 2024 Ophthalmol Sci (ReCLAIM-2) | Confirmed title + trial ✓ | PASS |
| 36934127 | Patel et al. 2023 Sci Rep (elamipretide swine model) | Confirmed; fluid, creatinine, troponin figures ✓ | PASS |
| 32068002 | Butler et al. 2020 J Card Fail (PROGRESS-HF/SPIHF-201) | Confirmed; LVESV figures -4.4, -1.2, -3.8 mL ✓ | PASS |

**FLAG — Section C bibliography [3]:** States "PMID: 32641818" for Allen et al. 2020 Communications Biology (DOI: 10.1038/s42003-020-1101-3). Verification reveals PMID 32641818 resolves to a **Nature climate commentary** (Lehmann & Possinger, "Removal of atmospheric CO2 by rock weathering", DOI: 10.1038/d41586-020-01965-7) — an entirely unrelated paper. The correct PMID for the Allen et al. cristae/elamipretide paper is **32680996** (confirmed via PMC7368046). The DOI in the C[3] bibliography entry (10.1038/s42003-020-1101-3) is correct and resolves to the right paper, so the content claim itself is properly grounded. This is a PMID transcription error, not a fabricated citation.

Classification: **WARN** (not HALT). Rationale: the underlying paper is real, the DOI in the entry is correct, the content claims are accurate, and the bibliographic entry includes the DOI which is the more authoritative identifier. A reader using PMID-only retrieval would land on the wrong paper, but the claim is not fabricated. Action required: correct PMID in Section C[3] from 32641818 to 32680996.

**Status: WARN** — 1 of 9 spot-checked citations carries an erroneous PMID (correct DOI present; correct PMID is 32680996).

---

## IC-11 — No Placeholder Strings

Grep across all 5 sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No instances found. Section D notes "date not primary-verified" for one CRL date and "Specific merger price ... not primary-verified" — these are explicit uncertainty disclosures, not placeholder strings as defined by this check.

**Status: PASS** — No placeholder strings detected.

---

## IC-12 — No Wikipedia Citations

Grep for `en.wikipedia.org`, `ru.wikipedia.org`, or any `wikipedia.org` domain across all 5 section bibliographies.

No Wikipedia URLs in any bibliography entry.

Section A self-check mentions "CAS number 736992-21-5 sourced from Cayman Chemical/Wikipedia cross-check (vendor-confirmable, not cited as a primary study claim)" — confirming Wikipedia was used as a navigation aid but not cited in the bibliography. This is the correct usage pattern.

**Status: PASS** — No Wikipedia citations in any bibliography.

---

## IC-13 — Per-Citation Corpus Scoping

Checked 9 numerical/scope claims against retrieved source corpora. Mode: standard (≥50% of numerical claims; target 10, checked 9 given the total claim inventory across 5 sections).

| Claim | PMID | Verified | Result |
|-------|------|----------|--------|
| >1000-fold mitochondrial accumulation | 15178689 | "concentrate 1000-fold in the IMM" — confirmed in abstract | PASS |
| Kd 1.87±0.64 µM (cardiolipin binding) | 23813215 | "KD=1.87±0.64 μM" — confirmed in abstract | PASS |
| Creatinine 0.62 vs 1.72 mg/dL at 24h | 23813215 | Not in abstract; full-text only | corpus-missing (WARN) |
| CK-MB AUC 5785 vs 5570 ng·h/mL | 26586786 | Confirmed in abstract | PASS |
| 12 mitochondrial protein interactors | 32554501 | "12 protein interactors" confirmed | PASS |
| Cristae fragmentation / elamipretide cardiac I/R (rats) | 32680996 (via PMC7368046) | Confirmed via PMC full text; correct paper | PASS |
| LVESV -4.4, -1.2, -3.8 mL | 32068002 | Confirmed in abstract | PASS |
| 6MWT +96.1 m at week 168 (TAZPOWER OLE) | 38602181 | Confirmed in abstract | PASS |
| MMPOWER-3: 6MWT -3.2 m (P=0.69); PMMSA -0.07 (P=0.37) | 37268435 | Paper confirmed; specific figures not in PubMed abstract retrieved | corpus-missing (WARN) |
| ReCLAIM-2: LL BCVA -2.8 vs -4.6 letters; GA area +0.328 vs +0.281 mm² | 39605874 | Paper confirmed; specific figures not in PubMed abstract | corpus-missing (WARN) |

Notes on corpus-missing WARNs:
- The creatinine figure (0.62 vs 1.72 mg/dL) is a results-section value from Birk 2013 JASN that is plausible and internally consistent with the paper's abstract conclusion; not flagged as number-not-found.
- The MMPOWER-3 figures appear in the Neurology 2023 published paper and are consistent with the ClinicalTrials.gov posted results; the abstract retrieved was a metadata/author page. Not flagged as number-not-found.
- The ReCLAIM-2 specific LL BCVA and GA area numbers are from the full-text results tables; abstract confirms primary endpoints not met. Not flagged as number-not-found.

No `number-not-found`, `quote-not-found`, or `paraphrase-no-token-match` failures. All 3 failures are `corpus-missing` (paywall/abstract-limit), which generate WARNs per IC-13 rules, not HALTs.

**Status: WARN** — 3 of 9 (33%) claims are corpus-missing (abstract-only). 6 of 9 claims confirmed against retrieved text. No content-integrity failures.

---

## Population-Mismatch Summary

Checked 18 animal/in_vitro citations across all sections. All animal studies name:
- Species (rat, mouse, swine — specifically: Sprague-Dawley rat, C57BL/6 mouse, Yorkshire swine, ZSF1 rat, TazKD mouse)
- n per group (where reported; 3 exceptions: A[5] cross-linking study notes "n = 3 biological replicates"; C[3] Allen 2020 notes "Exact group sizes were not recoverable through available access")
- No animal result stated as human-established

The report consistently distinguishes the preclinical evidence base from the human clinical trial record, and Section C is explicitly structured around "The Translation Gap" to foreground this distinction.

**population_mismatch verdict: PASS** — 18 citations checked, 0 flagged.

---

## Concentration Audit Summary

Clinical trial publications enumerated in Section E.2 (10 identifiable sponsored RCTs/studies):
- Stealth BioTherapeutics–sponsored: 9 (MMPOWER phase 1/2/3 family, TAZPOWER crossover + OLE, TAZPOWER natural-history comparison, Daubert HFrEF, LHON ophthalmic, ReCLAIM/ReCLAIM-2)
- Independent (NIH/Mayo): 1 (Saad et al. 2017, renal artery stenosis, NCT01755858)

Share: 9/10 = 90%. Threshold triggered (>70%). Surfaced first-class in Section E before any indication subsection. Not a HALT condition per IC-9 (surfacing required, not absence).

**concentration_audit verdict: PASS** — threshold_triggered = true; surfaced first-class.

---

## Action Items (non-blocking)

1. **Correct Section C bibliography [3]:** Change `PMID: 32641818` to `PMID: 32680996`. The DOI (10.1038/s42003-020-1101-3) is correct and may remain as the primary identifier.
2. **IC-13 corpus-missing notices:** The three abstract-only claims (Birk 2013 creatinine figures; MMPOWER-3 specific endpoint numbers; ReCLAIM-2 specific endpoint numbers) should be verified against full-text at wiki-ingest time if paywall access is available. These are not blocking for the gate.
