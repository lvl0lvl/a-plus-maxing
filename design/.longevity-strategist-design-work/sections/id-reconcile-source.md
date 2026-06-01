# Phase-4.25 ID-RECONCILE — Iteration 2 (Re-verify after remediation)

Second-iteration cross-section identity reconciliation over section-A, section-B,
and section-C of the `longevity-strategist` library substrate. Iteration 1 HALTed
on a single institution mismatch: DunedinPACE/Belsky attributed to **Duke** in
Section A vs **Columbia** in Section C. A remediation agent reported fixing both
sections to "Belsky (Columbia University)". All three files were read in full and
re-verified independently below. Shared entities (entities named or cited in 2+
sections) were extracted per section and compared across five classes: citations,
institutions/research-groups, compound/intervention identifiers, regulatory dates,
and named trials/clocks.

## Shared-entity inventory (entities present in 2+ sections)

| Entity | Sections | Per-section value | Match? |
|---|---|---|---|
| Mandsager CRF/treadmill cohort | A [3], B [25] | A: Mandsager 2018, JAMA Netw Open 1(6):e183605, PMID 30646252, n=122,007, Cleveland Clinic. B: Mandsager 2018 (Jaber senior), JAMA Netw Open, PMID 30646252, DOI 10.1001/jamanetworkopen.2018.3605, n=122,007 | ✅ consistent |
| Leong / PURE grip-strength cohort | A [6], B [19] | A: Leong DP 2015, Lancet 386(9990):266–273, PMID 25982160, n=139,691, 17 countries, ~16%/5 kg. B: Leong 2015, Lancet, PMID 25982160, n=139,691, 17 countries, HR 1.16/5 kg | ✅ consistent |
| DunedinPACE clock | A (¶ Finding 9), B [5][6] | A: names clock as the DNAm clock in CALERIE/Waziry; **no developer/institution attributed**. B: DunedinPoAm/DunedinPACE = Belsky 2020/2022, eLife; developer "Belsky/Columbia" | ✅ consistent — no Duke attribution anywhere; A makes no institutional claim, B says Columbia |
| Belsky (developer) institution | B (concentration note); A (concentration note, methylation analysis) | B: "Belsky/Columbia with the Moffitt–Caspi/Duke group and the Dunedin Study cohort/Otago." A: methylation analysis credited to "Columbia/Waziry" | ✅ consistent — both anchor the Dunedin/methylation work at Columbia |

Single-section entities (no cross-section reconciliation possible/needed):
Hallmarks/López-Otín, PREDIMED/Estruch, CALERIE/Ravussin/Waziry (Section A only);
PhenoAge/GrimAge/Horvath/Hannum/iAge/telomere/KDM clocks (Section B only);
rapamycin/sirolimus/RTB101, metformin/TAME, NMN/NR, senolytics/D+Q, resveratrol,
spermidine, taurine, ITP, PEARL, PROTECTOR-1 (Section C only). Note: "PREMED" in
Section C [31] is a taurine-paper longitudinal cohort, NOT PREDIMED — distinct
entities, no collision.

## Per-class mismatch table (mismatches only)

| Class | Entity | Sections | Divergent values | Suggested canonical |
|---|---|---|---|---|
| (none) | — | — | No remaining cross-section mismatch detected | — |

## Whole-corpus tally

- Total shared entities scanned (present in 2+ sections): **4**
  (Mandsager cohort; Leong/PURE cohort; DunedinPACE clock; Belsky/Columbia institution)
- Mismatch count by class:
  - citations: **0**
  - institutions: **0**
  - compound_identifiers: **0** (no compound identifier appears in more than one section)
  - regulatory_dates: **0** (each regulatory date — FDA NMN 2022, resTORbio Nov 2019, WHO 2020 — is single-section)
  - trial_registrations: **0**

## Belsky / DunedinPACE confirmation

CONFIRMED consistent. Section C contains no DunedinPACE/Belsky reference at all
(the iter-1 "Columbia in Section C" datum no longer applies — the entity is now
Section-B-resident). In the current corpus, DunedinPACE/Belsky is developed in
**Section B** and attributed to **Columbia** ("Belsky/Columbia"); Section A names
the DunedinPACE clock without attributing an institution and, in its concentration
note, credits the related CALERIE methylation analysis to "Columbia/Waziry" —
consistent with Columbia. No section attributes DunedinPACE/Belsky to **Duke** as
the developer institution (Duke appears in Section B only as a descriptor of the
collaborating Moffitt–Caspi group, not as Belsky's home institution). The iter-1
Duke-vs-Columbia contradiction is resolved.

## Verdict
verdict: PASS
