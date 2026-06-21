# Phase 4.25 ID-Reconcile — Selank (iteration 2)

Re-scan of section-A.md through section-F.md across 5 entity classes. The iteration-1 remediation (PMID 26924987 / PMC4757669 first-author correction from Kolomin → Volkova A in §D and §E) is re-verified below and CONFIRMED HELD.

## citations (scanned: 9)

Target citation PMID 26924987 / PMC4757669 (Volkova A et al., "Selank Administration Affects the Expression of Some Genes Involved in GABAergic Neurotransmission," *Front Pharmacol* 7:31, 2016):
- §C[4]: "Volkova A, Shadrina M, Kolomin T, Andreeva L, Limborska S, Myasoedov N, Slominsky P" — PMID 26924987, PMC4757669, 2016. First author = **Volkova A**. CONSISTENT.
- §D[2]: "Volkova A, Shadrina M, Kolomin T, et al." — PMC4757669. First author = **Volkova A**. CONSISTENT.
- §E[3]: "Volkova A, et al." — PMC4757669, 2016. First author = **Volkova A**. CONSISTENT.
CONVERGED across §C/§D/§E — all three now read first author Volkova A. No residual Kolomin first-author attribution anywhere. The iteration-1 fix HELD.

Other multi-section primaries re-checked (PMID/DOI → identical author/year/journal):
- **Zozulia/Zozulya, Neznamov et al. 2008 anxiolytic trial** (PMID 18454096, *Zh Nevrol Psikhiatr Im S S Korsakova* 108(4):38-48): §B[1], §C[1], §D[3], §F[1] — CONSISTENT.
- **Zozulya et al. 2001 enkephalinase mechanism** (PMID 11550013, *Bull Exp Biol Med* 131(4):315-7): §A[1], §B[5] — CONSISTENT (distinct from the 2008 trial).
- **Uchakina et al. 2008 immunomodulation** (PMID 18577961, *Zh Nevrol Psikhiatr* 108(5):71-5): §A[8], §B[4] — CONSISTENT.
- **Inozemtseva et al. 2008 BDNF** (PMID 18841804, DOI 10.1134/S0012496608040066, *Dokl Biol Sci* 421): §A[4], §C[3] — CONSISTENT.
- **Kasian et al. 2017** (PMID 28280289 / PMC5322660, *Behav Neurol* 2017:5091027): §B[7], §C[2], §D[4] — CONSISTENT.
- **Kolik et al. 2014 alcohol-withdrawal** (PMID 24913576, *Bull Exp Biol Med* 157(1):52-5): §B[8], §D[8] — CONSISTENT.
- **Medvedev 2014 vs phenazepam** (PMID 25176261, 114(7):17-22): §B[3], §D[1], §F[9] — CONSISTENT.
- **Filatova et al. 2017** (PMID 28293190, *Front Pharmacol* 8:89): §A[5], §C[5] — CONSISTENT.
No same-PMID/DOI → different-author divergence remains.

## institutions (scanned: 4)

- **IMG RAS / Institute of Molecular Genetics RAS**: §A, §B, §C, §E, §F — consistent. CONSISTENT.
- **V. V. Zakusov Research Institute of Pharmacology**: §A, §B, §C, §E, §F — consistent. CONSISTENT.
- **Serbsky (Korsakov/Serbsky psychiatry milieu)**: §B, §C — consistent. CONSISTENT.
- **Peptogen (ЗАО «ИНПЦ «Пептоген»)**: §E only (marketing-authorisation holder). Single-section; no conflict. CONSISTENT.

## compound_identifiers (scanned: 4)

- **Sequence Thr-Lys-Pro-Arg-Pro-Gly-Pro (TKPRPGP)**: §A, §B, §C, §D, §E, §F — identical. CONSISTENT.
- **Russian reg code ЛСР-003338/09** (incl. full form ЛСР-003338/09-300409): §E — correct ЛСР prefix in all instances; NO ЛРС transposition present. CONSISTENT.
- **Tuftsin-analogue framing** (TKPR core + PGP stabilizer): §A, §B, §C, §D, §E, §F — consistent. CONSISTENT.
- **Distinctness from Semax & N-Acetyl-Selank-Amidate**: §A, §C, §E, §F all hold Selank distinct from both. CONSISTENT.

## regulatory_dates (scanned: 3)

- **Russia registration ~2009**: §E (reg suffix /09, 30.04.2009) and §F (~2009) — CONSISTENT.
- **§503A Category-2 removal eff. Sept 27 2024 + nomination withdrawal + PCAC referral; no finalized Cat-1 reclassification**: §E and §F state identically (both reject the "RFK Jr Category-1" framing; both describe the 2026 action as pending/not-finalized). CONSISTENT.
- **2026 PCAC meeting Jul 23-24 2026**: §E and §F — consistent. CONSISTENT.

## trial_registrations (scanned: 3)

No formal trial-registry identifiers (NCT/EudraCT) are claimed in any section; human trials are cited by PMID only (18454096, 25176261, 26356395), consistently across §B/§C/§D/§F. The GRLS state register + reg no. ЛСР-003338/09 appear in §E; §F references the Russian registration with no conflicting registry ID. No trial/registry-ID divergence. CONSISTENT.

## Verdict
verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "timestamp": "2026-06-21T02:44:00Z",
  "iterations": 2,
  "entity_classes": {
    "citations": {"scanned": 9, "mismatch_count": 0},
    "institutions": {"scanned": 4, "mismatch_count": 0},
    "compound_identifiers": {"scanned": 4, "mismatch_count": 0},
    "regulatory_dates": {"scanned": 3, "mismatch_count": 0},
    "trial_registrations": {"scanned": 3, "mismatch_count": 0}
  },
  "halt_reasons": []
}
```
