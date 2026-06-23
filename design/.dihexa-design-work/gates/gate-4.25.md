## Verdict

verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 2,
  "entity_classes": {
    "citations": {
      "scanned": 7,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 3,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 1,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

## Per-class prose tables

### Citations (shared PMIDs scanned: 7)

| PMID | Sections citing | Author/Year/Journal/Vol/Pages | Design tag | Integrity status | Status |
|------|-----------------|-------------------------------|------------|-----------------|--------|
| 25187433 (Benoist 2014) | A, B, E | Consistent across all sections: JPET 2014;351(2):390–402 | `animal` uniform (A,B,E) | RETRACTED April 2025 (PMID 40312093) — annotated in all citing sections | PASS |
| 23055539 (McCoy 2013) | A, B, C, D | Consistent: JPET 2013;344(1):141–154 | `animal` uniform | EoC September 2021 (PMID 34551989) — annotated in A, B, C, D | PASS |
| 29733881 (Ho & Nation 2018) | A, B | Consistent: Neurosci Biobehav Rev 2018;92:209–225 | `meta_analysis` uniform | No integrity flag — consistent | PASS |
| 25455861 (Wright/Kawas/Harding 2015) | A, B, D, E | Consistent: Prog Neurobiol 2015;125:26–46 | `mechanism_review` uniform | No integrity flag — consistent | PASS |
| 34827486 (Sun 2021) | B, C, D | Consistent: Brain Sci 2021;11(11):1487 | `animal` uniform | No integrity flag — consistent | PASS |
| 38489193 (Wells 2024) | B, D | Consistent: J Huntingtons Dis 2024;13(1):55–66 | `animal` uniform | No integrity flag — consistent | PASS |
| 22129598 (Kawas 2012) | C (full entry), E (anecdote_aggregate context) | C: JPET 2012;340(3):539–548 — E references via [3] anecdote_aggregate only | `animal` in C; `anecdote_aggregate` for the Retraction Watch source in E | RETRACTED April 2025 (PMID 40312092) — C annotates RETRACTED; E's [3] is the Retraction Watch article that IS the anecdote_aggregate source, not the paper itself — by design | PASS |

**Fixes applied (iteration 2, this pass):**

- **Section B, LIFT-AD enrollment figure:** "549 enrolled" corrected to "554 enrolled [actual per ClinicalTrials.gov NCT04488419 results posting, April 2025]". The ClinicalTrials.gov API returned enrollment type = ACTUAL and count = 554 (verified June 2026). Section B was citing an earlier topline-reporting figure; Section E's 554 was already correct.

### Institutions (scanned: 3 independent groups appearing across sections)

| Group | Sections | Stated affiliation | Status |
|-------|----------|--------------------|--------|
| Harding/Wright/WSU | A, B, C, D, E | Washington State University (± M3 Biotechnology) — consistent | PASS |
| Sun et al. (2021) | B, C, D | China Pharmaceutical University / Nanjing Medical University — consistent | PASS |
| Wells et al. (2024) | B, D | Whitworth University / OHSU / University of Washington — consistent | PASS |

### Compound identifiers (scanned across all 5 sections)

| Entity | Claim | Status |
|--------|-------|--------|
| Common name | Dihexa = PNB-0408 — consistent A, B, D | PASS |
| Chemical name | "N-hexanoyl-Tyr-Ile-(6)-aminohexanoic acid amide" — A (canonical, PubChem-matched); D previously read "N-hexanoic-Tyr-Ile-(6) aminohexanoic amide" (transcription error: "hexanoic" vs "hexanoyl"). **Fixed in D this iteration.** All sections now consistent. | PASS (fixed) |
| PubChem CID | 129010512 — stated in A only (other sections do not restate structural data); no conflict | PASS |
| Formula | C₂₇H₄₄N₄O₅ — stated in A only; no conflict | PASS |
| MW | 504.7 g/mol — stated in A only; no conflict | PASS |
| Mechanism framing | IRAP/AT4 (Albiston, independent) vs HGF/c-Met (WSU, retracted) as contested dual-target — stated in A (explicit), B (implicit via PI3K/AKT note), C (explicit C.4), D (D.1 HGF/c-Met); consistent across sections | PASS |
| Dihexa ≠ fosgonimeton | Explicitly distinguished in A, B, C, D, E — consistent | PASS |

### Regulatory dates (scanned across D + E primarily)

| Fact | Sections | Status |
|------|----------|--------|
| FDA not approved / zero ClinicalTrials.gov results | A, B, D, E | Consistent |
| WADA S0 classification analysis | D only | No cross-section conflict |
| Fosgonimeton LIFT-AD failure | B, D, E | After fix: all three cite 554 actual enrollment; all agree primary endpoint missed | PASS (B fixed) |
| c-Met oncogenic tension | C, D, E | Consistent framing — theoretical, unquantified, mechanistically grounded | PASS |
| $4M DOJ/False Claims Act settlement (LeonaBio/Athira, Jan 2025) | E [3] | Verified via Retraction Watch source citation |
| $10M securities fraud class action settlement (Athira, separate) | C | A different legal proceeding from the DOJ action — not a contradiction. C states "securities fraud lawsuits"; E states "DOJ… data falsification allegations." These are distinct proceedings that can both be correct. No reconciliation required. | PASS |

### Trial registrations (scanned: 1 shared — NCT04488419 LIFT-AD)

| Trial | Sections | Enrollment figure | Status |
|-------|----------|-------------------|--------|
| NCT04488419 (LIFT-AD fosgonimeton) | B, D, E | B: corrected to 554 (was 549); E: 554 (correct); D: no enrollment count stated — no conflict | PASS (B fixed) |

---

## Residual notes

**Settlement amounts (C vs E):** Section C ("$10 million to settle securities fraud lawsuits") and Section E ("$4 million to settle allegations of data falsification") refer to two distinct legal proceedings — a civil securities class action by investors vs. a DOJ False Claims Act settlement — and are not factually inconsistent. Both figures can be simultaneously correct. No reconciliation was performed; no edit was required.

**Per-section tiers and integrity annotations:** Per task instructions, per-section tier assignments (e.g., PMID 23055539 at tier 1 in A vs tier 2 in C/D; PMID 34827486 at "2-3" in B vs "2" in C/D) are intentionally per-section and were not flagged or modified.

**Fixes this iteration (2 total):**
1. Section B — LIFT-AD enrollment: 549 → 554 (ClinicalTrials.gov ACTUAL count, NCT04488419)
2. Section D — Chemical name: "N-hexanoic-Tyr-Ile-(6) aminohexanoic amide" → "N-hexanoyl-Tyr-Ile-(6)-aminohexanoic acid amide"
