## Verdict

verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 1,
  "entity_classes": {
    "citations": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 0,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 5,
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

## Per-class prose tables

### Citations (shared PMIDs scanned: 4)

| PMID | Paper | Sections citing | Author consistent | Year/journal/vol/pages consistent | Design TAG consistent | Notes |
|------|-------|-----------------|-------------------|------------------------------------|-----------------------|-------|
| 18206919 | Safarinejad & Hosseini, J Urol 2008 | B [7], C [5] | YES | YES — J Urol 2008 Mar;179(3):1066–1071 in both | YES — `rct` in both | Tier differs (B=3, C=1); EoC PMID 36626345 present in both. **Per-section tier — exempted per pre-scan note.** |
| 31599840 | Kingsberg et al., Obstet Gynecol 2019 | A [7], B [1], D [3], E [3] | YES | YES — 2019;134(5):899–908, DOI .0000000000003500 in all | YES — `rct` in all | tier:1 in all 4 sections. Fully consistent. |
| 31599847 | Simon et al., Obstet Gynecol 2019 | A [8], B [3], D [4], E [5] | YES | YES — 2019;134(5):909–917, PMC6819023, DOI .0000000000003514 in all | YES — `open_label` in all | Tier differs (B=2 with explanatory bracket "[52-wk open-label extension; not an RCT]"; A/D/E=1). **Per-section tier — exempted per pre-scan note.** |
| 35076581 | Edinoff et al., Neurol Int 2022 | A [3], D [5], E [6] | YES | YES — 2022;14(1):75–88, PMC8788464, DOI 10.3390/neurolint14010006 in all | YES — `mechanism_review` in all | tier:2 in all 3 sections. Fully consistent. |

**Observed tier variation (exempted):** Safarinejad PMID 18206919 and Simon PMID 31599847 each carry different tier values across sections. These are per-section tier assignments reflecting each section author's local evidence-grading context, explicitly pre-declared as intentional and excluded from mismatch counting per the gate brief.

---

### Compound identifiers (entities scanned: 5)

| Entity | Claim checked | Cross-section consistent? |
|--------|--------------|---------------------------|
| PT-141 = bremelanotide | Identity equivalence stated or implied | YES — all 5 sections |
| Structural relationship: PT-141 = des-amide (C-terminal –OH) analog of MT-II (C-terminal –NH₂) | Section A: explicit ("carboxylate derivative of MT-II, free acid at carboxyl terminus per FDA label"). Section C: "lacking the C-terminal amide". Section E: "deamidated, carboxyl-terminated metabolite of MT-II, lacking the C-terminal amide". | YES — consistent across A, C, E |
| Sequence: Ac-Nle-cyclo[Asp-His-D-Phe-Arg-Trp-Lys]-OH, ~1025 Da, CID 9941379 | Section A only (A.1); no other section contradicts | YES — no conflict |
| MC potency order: MC1R > MC4R > MC3R > MC5R | Section A: verbatim from FDA label. Sections C/D/E abbreviate to MC3R/MC4R CNS focus — no contradiction of the stated order. | YES — no conflict |
| PT-141 / MT-II / afamelanotide 3-way disambiguation | Section A: fully disambiguated. Section C.3: MT-II distinct (cyclic, broader MCR, C-terminal amide). Section E.5: "three structurally distinct compounds from the same UA melanocortin platform." Consistent across all sections that address it. | YES |

---

### Regulatory dates/facts (entities scanned: 5)

| Fact | Sections | Consistent? |
|------|----------|-------------|
| FDA approval date | A: "June 2019"; B: "June 21, 2019 (NDA 210557)"; C: approval referenced (no date); D: "June 21, 2019 (NDA 210557)"; E: "June 2019" | YES — no section states a different date |
| Approved indication | All 5: premenopausal women, acquired generalized HSDD only | YES |
| Label dose | A, B, C, D, E: 1.75 mg SC | YES |
| Frequency cap ≤1/24h | A, B, C, D: stated; E: implied via label reference | YES |
| Monthly cap ≤8/month | C, D: explicitly stated; A, B, E: not stated but no contradiction | YES |
| WADA status | D only: not explicitly named on S2; Melanotan II appears S2-prohibited; catch-all may apply — uncertainty disclosed. No other section claims WADA exemption or prohibition. | YES — no cross-section conflict |
| Contraindications | A, C, D: uncontrolled HTN, known CVD | YES |

---

### Trial registrations (NCT numbers scanned: 0)

No NCT registration numbers appear in any of the 5 sections. RECONNECT is referenced as Study 301 / Study 302 throughout; no NCT-format identifiers are cited. No cross-section consistency check possible; no mismatches.

---

### Institutions (scanned: 0)

No institution entities were cited as trackable named entities requiring cross-section consistency checks. No mismatches.
