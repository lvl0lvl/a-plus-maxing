# ID-Reconcile (Phase 4.25) — HDL-C

Independent cross-section identity reconciliation between `section-A.md` (Identity, Physiology & Causal Significance) and `section-B.md` (Reference Ranges, Measurement & Determinants). Per-file `## Post-fix grep audit` and `## Self-check` blocks were excluded from the scan. Only entities appearing in BOTH sections were compared.

## Verdict

verdict: PASS

No identity disagreements found across the five entity classes. Every entity that appears in both sections carries consistent author/year, PMID/DOI, type-tag, institution, gene symbol, and population-count values. No regulatory dates or trial-registration identifiers (NCT) appear in either section, so those classes are vacuously consistent.

## Per-class reconciliation

### citations

| entity | Section A | Section B | match |
|--------|-----------|-----------|-------|
| Madsen 2017 (Extreme high HDL, U-shape) | Madsen CM, Varbo A, Nordestgaard BG; Eur Heart J 2017;38(32):2478–2486; DOI 10.1093/eurheartj/ehx163; PMID 28419274; `cohort` [A-ref2] | Madsen CM, Varbo A, Nordestgaard BG; Eur Heart J 2017; DOI 10.1093/eurheartj/ehx163; PMID 28419274; `cohort` [B-ref2] | YES — PMID/DOI/year/authors/tag identical |
| Ko 2016 (CANHEART) | Ko DT, Alter DA, Guo H, et al.; JACC 2016;68(19):2073–2083; DOI 10.1016/j.jacc.2016.08.038; PMID 27810046; `cohort` [A-ref9] | Ko DT, Alter DA, Guo H, et al.; JACC 2016; DOI 10.1016/j.jacc.2016.08.038; PMID 27810046; `cohort` [B-ref3] | YES — PMID/DOI/year/authors/tag identical |

Voight (MR) appears only in A; NCEP/ATP III and AHA/ACC 2018 guideline are not co-cited (A cites the AHA/ACC guideline `mechanism_review`; B cites NCEP/ATP III `regulatory` — distinct sources, not a shared entity → no comparison).

### institutions

| entity | Section A | Section B | match |
|--------|-----------|-----------|-------|
| Copenhagen cohorts (CCHS + CGPS) | "two Danish cohorts (52,268 men + 64,240 women, CCHS+CGPS)" | "Copenhagen City Heart Study + Copenhagen General Population Study (52,268 men, 64,240 women)" | YES — same institution + identical counts |

CDC / CRMLN appears only in B.

### compound_identifiers

| entity | Section A | Section B | match |
|--------|-----------|-----------|-------|
| CETP (gene/inhibitor class) | torcetrapib/dalcetrapib/evacetrapib named as the CETP-inhibitor class | CETP named as a high-HDL large-effect gene | YES — symbol `CETP` consistent |
| ABCA1 | efflux transporter, rate-limiting biogenesis step | Tangier-disease low-HDL gene | YES — symbol `ABCA1` consistent |
| LIPG | LIPG Asn396Ser MR variant (endothelial lipase) | LIPG (endothelial lipase) high-HDL gene | YES — symbol `LIPG` consistent |

Torcetrapib/dalcetrapib/evacetrapib/niacin, LIPC/APOA1 appear in only one section each (no cross-section conflict).

### regulatory_dates

No regulatory dates appear in either section. None to compare. (0 scanned.)

### trial_registrations

No trial-registration identifiers (NCT numbers) appear in either section. Trials are named only by acronym (ILLUMINATE, ACCELERATE, AIM-HIGH, HPS2-THRIVE, dal-OUTCOMES) in A and none in B → no shared identifier to compare. (0 scanned.)

## Machine-readable result

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 2, "mismatch_count": 0},
    "institutions": {"scanned": 1, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 3, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 0, "mismatch_count": 0},
    "trial_registrations": {"scanned": 0, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 1
}
```
