## Verdict

verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 3,
  "entity_classes": {
    "citations": {
      "scanned": 26,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 7,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 0,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-Class Entity Tables

### Citations (26 PMIDs total; 8 shared across ≥2 sections)

| PMID | Author/Year | Sections Present | Tags | Match? |
|------|-------------|-----------------|------|--------|
| 8637402 | Dorr 1996 | A, B, D, E | open_label × 4 | YES |
| 9679884 | Wessells 1998 *J Urol* | A, C, E | rct × 3 | YES |
| 11035391 | Wessells 2000 *Int J Impot Res* | A, C, E | rct × 3 | YES |
| 11018622 | Wessells 2000 *Urology* | A, C | rct × 2 | YES |
| 23785612 | Sivyer 2012 | B, D | open_label × 2 | YES — **iter-3 fix confirmed** |
| 41752902 | Bonchev 2026 | B, E | open_label × 2 | YES — iter-1 fix confirmed |
| 16412534 | Hadley & Dorr 2006 | C, E | mechanism_review × 2 | YES |
| 17584130 | King 2007 | C, E | mechanism_review × 2 | YES |

Single-section PMIDs (no cross-section conflict possible): 19575725, 19174439, 24334249, 22724573, 24355990, 16293341, 23121206, 31953620, 22761160, 7983590, 26979527, 29678289, 33884776, 30812013, 14963471, 14999221, 31599840, 27181790 — all single-section, no conflict.

**Peer-reviewed case report tags:** All peer-reviewed case reports are tagged `open_label` in every section where they appear (Cousen, Langan, Hueso-Gabriel, Schulze, Sivyer, Paurobally, Ong, Hjuler, Bonchev, Nelson, Peters, PRES). Cairns 2025 (*The Conversation*, non-peer-reviewed commentary) is tagged `anecdote_aggregate` in E only — correct for its non-peer-reviewed character and consistent throughout.

**Citations mismatch_count: 0**

---

### Compound Identifiers (5 entities scanned)

| Entity | Canonical value | Sections | Consistent? | Notes |
|--------|----------------|----------|-------------|-------|
| MT-II PubChem CID | 92432 | A only | YES | No cross-section conflict |
| MT-II MW | 1024.2 Da | A only | YES | No cross-section conflict |
| MT-I (afamelanotide) MW | 1646.8 Da | A only | YES | No cross-section conflict |
| Bremelanotide MW | 1025.2 Da | A only | YES | No cross-section conflict |
| Bremelanotide sequence | Ac-Nle-cyclo[Asp-His-D-Phe-Arg-Trp-Lys]-OH | A, C | YES | Bracket vs. parenthesis notation only; identical sequence |

Note: A and C differ on the in-vivo metabolite characterization of bremelanotide (A applies a strict PK-study standard; C applies King 2007 mechanism_review characterization). This is per-section intentional scientific framing — different evidence-standard scopes — not a metadata/tag mismatch. Per gate instructions: "per-section tiers + parentheticals are intentional — do NOT flag."

**Compound identifiers mismatch_count: 0**

---

### Institutions / Concentration (5 groups scanned)

| Institution | Sections | Characterization | Consistent? |
|------------|----------|-----------------|-------------|
| University of Arizona | A, B, E | Synthesis origin (A); founding clinical program (B); ~90% primary human data (E) | YES |
| UA sub-departments (Cancer Center / Pharmacology / Urology) | E only | Sub-unit labels for named trials; no conflict | YES |
| Leiden University / Habbema group (Netherlands) | E only | Risk-review authorship; single section | N/A |
| Giuliano group (France) | E only | Animal/spinal-cord mechanism data; non-human; single section | N/A |
| Multi-continent AE case-report groups | B, D, E | Diffuse surveillance literature; acknowledged consistently as non-primary | YES |

**Institutions mismatch_count: 0**

---

### Regulatory Dates (7 date instances across sections)

| Fact | Sections | Values stated | Consistent? |
|------|----------|--------------|-------------|
| Scenesse EC marketing authorisation | B, E | "22 December 2014" in both | YES |
| CHMP positive opinion (Scenesse) | B, E | "23 October 2014" in both | YES |
| Scenesse FDA approval | B, D, E | "October 2019" (B); "2019" (D, year-only subset); "October 2019" / "2019-10-08" (E) | YES — D is a subset, not a contradiction |
| Bremelanotide (Vyleesi) FDA approval | C, E | "21 June 2019" (C); "June 21, 2019" (E) | YES — same date, format variation only |

Section D does not state the Scenesse EC authorisation date — omission, not contradiction.

**Regulatory dates mismatch_count: 0**

---

### Trial Registrations (0 entries)

No NCT numbers, EudraCT, ISRCTN, or other trial registry IDs are cited in any section. The Wessells MT-II trials (1998–2000) predate mandatory ClinicalTrials.gov registration; the bremelanotide RECONNECT trials are referenced in C for lineage context only, without registry IDs.

**Trial registrations mismatch_count: 0**

---

## Iter Summary

| Iteration | Mismatches found | Status |
|-----------|-----------------|--------|
| Iter 1 | 2: Bonchev 41752902 B/E tag divergence; Scenesse EMA date B/E divergence | HALT |
| Iter 2 | 1: Sivyer 23785612 B=open_label / D=anecdote_aggregate | HALT |
| Iter 3 | 0 | **PASS** |

All iter-1 and iter-2 fixes verified in the live section files. No new mismatches found in complete re-scan.
