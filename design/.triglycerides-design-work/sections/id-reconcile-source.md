# ID-Reconcile Source — Triglycerides (TG) — Phase 4.25

Independent cross-section identity reconciliation between `section-A.md` (Identity, Physiology & Causal Significance) and `section-B.md` (Reference Ranges, Measurement & Determinants). Only entities appearing in BOTH sections were compared. Each file's `## Post-fix grep audit` and `## Self-check` were ignored per scan rule.

## Verdict

verdict: PASS

All cross-section shared entities are identity-consistent. No disagreements found in citations, institutions, compound_identifiers, regulatory_dates, or trial_registrations. The single shared cite (Nordestgaard EAS/EFLM 2016) agrees on DOI; Section A omits the PMID that Section B supplies, which is an omission, not a divergence (no contradictory value). Shared compound identifiers (APOA5, APOC3/apoC-III, LPL, APOC2, GPIHBP1; fibrates, omega-3, icosapent ethyl) and the REDUCE-IT trial are used consistently. The Endocrine Society 2012 strata agree across both sections.

## Per-class reconciliation tables

### citations

| Entity (shared) | Section A | Section B | Consistent? |
|---|---|---|---|
| Nordestgaard EAS/EFLM 2016 consensus | A ref 3 — *Eur Heart J* 2016;37(25):1944–1958; DOI 10.1093/eurheartj/ehw152; no PMID; `mechanism_review` (society consensus) | B ref 2 — *Eur Heart J* 2016;37(25):1944-58; DOI 10.1093/eurheartj/ehw152; PMID 27122601; `mechanism_review` | YES — identical DOI, journal, volume/issue/pages, year, type-tag. A omits PMID (B supplies 27122601); omission ≠ divergence. |
| Endocrine Society 2012 hypertriglyceridemia guideline | A ref 4 — Berglund/Brunzell/Goldberg; *J Clin Endocrinol Metab* 2012;97(9):2969–2989; PMID 22962670; DOI 10.1210/jc.2011-3213; `mechanism_review` | B refs 1/3/9 (cited as Endocrine Society 2012 scheme inside Endotext/StatPearls reviews; not a standalone numbered primary) | YES — strata values agree (see regulatory_dates); B routes the same guideline through review sources without contradicting it. |
| Women's Health Study TG evidence | A ref 5 — Duran et al., *JACC* 2020;75(17):2122–2135 (TRL-cholesterol & MI) | B ref 11 — White et al., *Clin Chem* 2015;61(9):1156-63 (non-fasting cutpoint) | YES — DISTINCT papers/claims, not the same entity; no shared cite to disagree on. |

scanned (shared cites): 1 (Nordestgaard 2016). mismatches: 0.

### institutions

| Entity (shared) | Section A | Section B | Consistent? |
|---|---|---|---|
| Copenhagen / Nordestgaard group | Implicit via Varbo/Benn/Tybjærg-Hansen/Nordestgaard (A ref 2, Copenhagen cohorts) + Nordestgaard EAS/EFLM (A ref 3) | Nordestgaard EAS/EFLM (B ref 2) | YES — same group attribution; no divergent institutional naming. |

scanned: 1. mismatches: 0.

### compound_identifiers

| Entity (shared) | Section A | Section B | Consistent? |
|---|---|---|---|
| APOA5 | APOA5 −1131T>C (rs662799) TG/CHD MR variant | APOA5 = apoA-V, LPL cofactor; FCS gene | YES — same gene symbol, complementary roles. |
| APOC3 / apoC-III | APOC3 loss-of-function lowers TG/CHD | APOC3/apoC-III = LPL inhibitor upregulated by fructose | YES — consistent symbol & mechanism. |
| LPL / LpL | Lipoprotein lipase (LpL) hydrolyzes TRL core | LPL — FCS gene, 50–90% of FCS biallelic | YES — same enzyme/gene; casing (LpL vs LPL) is stylistic, not an identity conflict. |
| APOC2 (apoC-II) | — (not in A) | APOC2 cofactor, FCS gene | N/A — single-section; not compared. |
| GPIHBP1 | — (not in A) | GPIHBP1 anchors LPL at endothelium, FCS gene | N/A — single-section; not compared. |
| Fibrates | — (mentioned only as drug class generically; no figure) | ~30–50% TG; 10%/13% CV RR | N/A — A carries no fibrate identity to compare. |
| Omega-3 fatty acids | — | ~20–50%; Lovaza ≥500 mg/dL, 4 g/day | N/A — single-section detail. |
| Icosapent ethyl (EPA) | — | REDUCE-IT, 4 g/day, HR 0.75 | N/A — single-section detail. |

scanned (genes appearing in BOTH): 3 (APOA5, APOC3, LPL). mismatches: 0. (Drugs APOC2/GPIHBP1/fibrates/omega-3/icosapent appear in only one section → not counted as compared.)

### regulatory_dates

| Entity (shared) | Section A | Section B | Consistent? |
|---|---|---|---|
| Endocrine Society 2012 TG strata | normal <150 (<1.7); mild 150–199 (1.7–2.3); moderate 200–999 (2.3–11.2); severe 1000–1999 (11.2–22.4); very severe ≥2000 mg/dL (≥22.4) | mild 150–199; moderate 200–999; severe 1,000–1,999; very severe ≥2,000 mg/dL | YES — identical band boundaries and year (2012). |
| EAS/EFLM 2016 consensus year | 2016 | 2016 | YES. |

scanned: 2. mismatches: 0.

### trial_registrations

| Entity (shared) | Section A | Section B | Consistent? |
|---|---|---|---|
| REDUCE-IT | Not present in Section A | B ref 4 — Bhatt et al., *NEJM* 2019;380(1):11-22; HR 0.75; n=8,179; 4 g/day icosapent ethyl | N/A — REDUCE-IT appears only in Section B; no NCT number stated in either; nothing to cross-compare. |

scanned (registrations in BOTH): 0. mismatches: 0. (No NCT identifier is written in either section; REDUCE-IT is single-section.)

## Reconciliation summary

- Exactly one citation is genuinely shared (Nordestgaard EAS/EFLM 2016) — fully consistent on DOI/journal/year; A's missing PMID is a benign omission.
- Shared post-meal figure (+0.3 mmol/L / 26 mg/dL) and the fasting-repeat trigger (>5 mmol/L / 440 mg/dL) attributed to that same paper agree across A and B.
- Non-fasting abnormal threshold ≥2 mmol/L (175 mg/dL) agrees (A §"Fasting vs non-fasting", B §2).
- Endocrine Society 2012 strata agree band-for-band.
- Gene symbols (APOA5, APOC3, LPL) used identically.
- No regulatory date, institution, or trial-registration disagreement.

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "entity_classes": {
    "citations": {"scanned": 1, "mismatch_count": 0},
    "institutions": {"scanned": 1, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 3, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 2, "mismatch_count": 0},
    "trial_registrations": {"scanned": 0, "mismatch_count": 0}
  },
  "halt_reasons": [],
  "iterations": 1
}
```
