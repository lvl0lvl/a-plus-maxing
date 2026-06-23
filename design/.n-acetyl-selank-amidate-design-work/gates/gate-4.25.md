## Phase 4.25 — ID-Reconcile: Cross-Section Shared-Entity Consistency (Iteration 2)

## Verdict
verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 2,
  "entity_classes": {
    "citations": {
      "scanned": 6,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 2,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 7,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 5,
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

### Per-class prose tables

#### 1. Citations (6 shared PMIDs scanned across sections)

| PMID | Paper | Sections present | Author consistent | Year consistent | Journal consistent | Design tag consistent | Result |
|---|---|---|---|---|---|---|---|
| 18454096 | Zozulia 2008 GAD/neurasthenia RCT | A[4], B[1], D[1], E[6] | YES — "Zozulia AA, Neznamov GG, Siuniakov TS…" in all | YES — 2008 | Zh Nevrol Psikhiatr Im S S Korsakova — all | YES — `rct` in all | PASS |
| 25176261 | Medvedev 2014 vs phenazepam | A[10], B[2], D[2] | YES — "Medvedev VE, Tereshchenko ON…" in all | YES — 2014 | Zh Nevrol Psikhiatr Im S S Korsakova — all | YES — `open_label` in all | PASS |
| 26924987 | Volkova 2016 GABAergic rat study | A[5], B[5], C[6], E[3] | YES — "Volkova A, Shadrina M, Kolomin T, Andreeva L, Limborska S, Myasoedov N, Slominsky P" in all | YES — 2016 | Front Pharmacol. 2016;7:31 — consistent | YES — `animal` in all (tier varies per-section by design; excluded per instructions) | PASS |
| 28293190 | Filatova 2017 IMR-32 in vitro | A[6], B[6], E[4] | YES — "Filatova E, Kasian A, Kolomin T…" in all | YES — 2017 | Front Pharmacol. 2017;8:89 — consistent | YES — `in_vitro` in all (tier varies per-section by design; excluded per instructions) | PASS |
| 30255741 | Vyunova 2018 mechanism review | B[8], E[1] | YES — "Vyunova TV, Andreeva L, Shevchenko K, Myasoedov N" in both | YES — 2018 | Protein Pept Lett. 2018;25(10) — consistent | YES — `mechanism_review` in both | PASS |
| 31625062 | Kolik 2019 BDNF/ethanol rat | A[11], D[9] | YES — "Kolik LG, Nadorova AV, Antipova TA…" in both | YES — 2019 | Bull Exp Biol Med. 2019;167(5) — consistent | YES — `animal` in both | PASS |

**Citation class verdict: 0 mismatches. PASS.**

*Note on tier divergence for PMIDs 26924987 and 28293190: Section A labels them tier-1; Section B labels them tier-3 (with lower-trust open-access flag); Section C labels 26924987 tier-2 and E labels both tier-1. Per-section tier assignments are intentional and excluded from mismatch scope per standing instructions. Design tags (animal / in_vitro) are consistent across all sections.*

---

#### 2. Compound Identifiers (7 entities scanned across A, B, C, D, E)

| Entity | Canonical value | Section A | Section B | Section C | Section D | Section E | Result |
|---|---|---|---|---|---|---|---|
| Selank sequence | Thr-Lys-Pro-Arg-Pro-Gly-Pro (TKPRPGP) | "Thr-Lys-Pro-Arg-Pro-Gly-Pro (single-letter: TKPRPGP)" ✓ | "Thr-Lys-Pro-Arg-Pro-Gly-Pro / TKPRPGP" ✓ (corrected from Iter-1) | "Thr-Lys-Pro-Arg-Pro-Gly-Pro" ✓ | "heptapeptide TKPRPGP" ✓ | "heptapeptide Thr-Lys-Pro-Arg-Pro-Gly-Pro" ✓ | PASS — consistent in all 5 sections |
| PubChem CID | 11765600 | 11765600 ✓ | Not stated (single-section; no cross-section conflict) | Not stated | Not stated | Not stated | PASS |
| Selank molecular formula | C₃₃H₅₇N₁₁O₉ | C₃₃H₅₇N₁₁O₉ ✓ | Not stated | Not stated | Not stated | Not stated | PASS (single-section; no conflict) |
| Selank MW | 751.89 g/mol | 751.89 g/mol ✓ | Not stated | Not stated | Not stated | Not stated | PASS (single-section; no conflict) |
| Tuftsin ancestry | Tuftsin = Thr-Lys-Pro-Arg; Selank extends C-terminally with Pro-Gly-Pro | Confirmed ✓ | "tuftsin analog" ✓ | Confirmed — Tuftsin = Thr-Lys-Pro-Arg ✓ | "derived from tuftsin" ✓ | Not explicitly restated; ancestry of IMG lineage described | PASS |
| N-Acetyl-Selank-Amidate modifications | N-terminal acetylation + C-terminal amidation of Selank backbone | Fully described ✓ | Described ✓ | Fully described ✓ | Described ✓ | Described ✓ | PASS |
| Parent-vs-analog distinction | Analog is a distinct entity from parent; zero analog-specific primary literature | Stated ✓ | Stated ✓ | Stated ✓ | Stated ✓ | Stated ✓ | PASS |

**Compound identifiers verdict: 0 mismatches. PASS.**

**Iter-1 mismatch resolved:** Section B line 5 previously read `TPGPGP-Ile-Lys` — a garbled sequence. As of this iteration, Section B line 5 reads `Thr-Lys-Pro-Arg-Pro-Gly-Pro / TKPRPGP`, matching the canonical sequence confirmed by PubChem CID 11765600 and used consistently in sections A, C, D, and E. The fix is confirmed.

---

#### 3. Institutions / Concentration (primary in C and E; secondary mentions in A, B, D)

| Fact | Section C | Section E | Sections A, B, D | Consistent? |
|---|---|---|---|---|
| Primary institutional lineage | IMG RAS + Zakusov Institute of Pharmacology, RAMS | Same two institutions named identically | A and B: "Institute of Molecular Genetics of the Russian Academy of Sciences"; D: "IMG RAS" ✓ | YES |
| Concentration figure | "near-total concentration in the originating Russian research group" (qualitative) | 87–93% IMG RAS + Zakusov lineage; ≥70% concentration threshold exceeded | — | PASS — C's qualitative claim is supported by E's quantitative enumeration; no contradiction |
| Inventor name | Nikolai Myasoedov / Myasoedov NF | Myasoedov NF + Lyudmila Andreeva | Consistent across all 5 sections; Andreeva LA named in A and E; not contradicted elsewhere | YES |
| Western replication | Essentially absent (C.4) | Not independently replicated (E.4) | A and B corroborate | YES |

**Institutions class verdict: 0 mismatches. PASS.**

---

#### 4. Regulatory Dates / Facts (primary D + E; secondary A, B, C)

| Fact | Section D | Section E | Sections A, B, C | Consistent? |
|---|---|---|---|---|
| Selank Russian registration status | Registered in Russian Federation for anxiety + neurasthenia (confirmed by 2 peer-reviewed reviews; GRLS access failed) | Registered ~2009, trade name Selanc, 0.15% nasal drops | A: registered in Russia, trade name Selanc ✓; C: "Russian-registered" ✓; B: "approved in Russia and Ukraine" (scope extension; not contradicted) | YES — Ukraine mention in B is additive, not contradictory |
| Selank NOT FDA/EMA approved | YES — no IND on record; cannot be compounded under 503A/503B | YES — no IND, NDA, EMA authorization | A and C corroborate ✓ | YES |
| Analog NOT approved anywhere in the world | YES | YES | Stated or implied in A, B, C | YES |
| FDA 503A Category 2 / Sept 2024 | Not discussed in D | Selank removed from Cat 2 Sept 2024 after nominator withdrawal; pending PCAC review | Not discussed in A, B, C | YES — no contradiction; E carries the specific timeline, D doesn't discuss it; no conflict |
| WADA status | Doubly hedged: S2-claim from MDPI review unconfirmed against primary WADA source; S0 identified as more plausible operative category | E.3 does not discuss WADA directly | A, B, C do not discuss WADA | YES — no contradiction |
| Analog as grey-market / unapproved research chemical | YES | YES | YES in A, B, C | YES |

**Regulatory dates class verdict: 0 mismatches. PASS.**

---

#### 5. Trial Registrations

No ClinicalTrials.gov NCT numbers, EudraCT numbers, or equivalent registry identifiers appear in any of the 5 sections. The Russian clinical trials are described narratively via PMID-indexed journal citations; none carry trial registration identifiers in the indexed abstracts available. Nothing to reconcile.

**Trial registrations class verdict: 0 entities scanned, 0 mismatches. PASS (vacuously).**

---

#### 6. Analog-Evidence-Absence Claim (all 5 sections — cross-check)

| Claim | A | B | C | D | E |
|---|---|---|---|---|---|
| Zero analog-specific primary literature | "zero peer-reviewed primary studies specifically on N-Acetyl-Selank-Amidate" ✓ | "no indexed clinical trials, no preclinical published studies, and no regulatory filings" ✓ | "no clinical or preclinical published studies on the analog as a distinct entity" ✓ | "NO direct safety data for N-Acetyl-Selank-Amidate" ✓ | "zero analog-specific primary literature in PubMed or indexed scientific databases" ✓ |

**Analog-evidence-absence verdict: consistent in all 5 sections. PASS.**

---

### Iteration 2 summary

All 5 entity classes: 0 mismatches. The sole Iter-1 halt reason (garbled Selank sequence in section-B line 5) is confirmed corrected to canonical **Thr-Lys-Pro-Arg-Pro-Gly-Pro (TKPRPGP)**, now consistent with sections A, C, D, E and with PubChem CID 11765600. No new divergences identified in the complete re-scan. Phase 4.25 is CLOSED. Proceed to Phase 4.5.
