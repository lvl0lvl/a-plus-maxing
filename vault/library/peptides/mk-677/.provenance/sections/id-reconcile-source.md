# Phase 4.25 — ID-RECONCILE (cross-section entity consistency)

**Report:** MK-677 (Ibutamoren) — sections A–F
**Task:** detect cross-section disagreements on shared entities. Content NOT fixed; consistency only. A fact present in a single section is out of scope.

---

## Citations (shared PMIDs across sections)

Seven primary studies are each cited in more than one section. Each was checked for agreement on author / year / title / journal / PMID.

- **Nass 2008 — PMID 18981485** — B[1], C[5], D[1]. All three render it as Nass R, Pezzoli SS, Oliveri MC, Patrie JT, Harrell FE Jr, Clasey JL, Heymsfield SB, Bach MA, Vance ML, Thorner MO, *"Effects of an oral ghrelin mimetic on body composition and clinical outcomes in healthy older adults: a randomized trial,"* Ann Intern Med 2008;149(9):601–611, PMID 18981485. **Agree.**
- **Chapman 1996 — PMID 8954023** — A[3], B[2], C[6], D[2]. All four: Chapman IM, Bach MA, Van Cauter E, … Thorner MO, *"Stimulation of the GH–IGF-I axis by daily oral administration of a GH secretagogue (MK-677) in healthy elderly subjects,"* JCEM 1996;81(12):4249–4257. A[3] expresses the identifier as doi:10.1210/jcem.81.12.**8954023** (the PMID is embedded in the DOI stem and matches C/D's explicit PMID 8954023). **Agree.**
- **Sevigny 2008 — PMID 19015485** — B[8], C[1], D[6]. All three: Sevigny JJ, Ryan JM, van Dyck CH, Peng Y, Lines CR, Nessly ML (MK-677 Protocol 30 Study Group), *"Growth hormone secretagogue MK-677: no clinical effect on AD progression in a randomized trial,"* Neurology 2008;71(21):1702–1708, PMID 19015485. **Agree.**
- **Adunsky 2011 — PMID 21067829** — C[2], D[4]. Both: Adunsky A, Chandler J, Heyden N, …, *"MK-0677 (ibutamoren mesylate) for the treatment of patients recovering from hip fracture: a multicenter, randomized, placebo-controlled phase IIb study,"* Arch Gerontol Geriatr 2011;53(2):183–189, PMID 21067829. **Agree.**
- **Svensson 1998 — PMID 9467542** — B[3], C[4], D[3]. JCEM 1998;83(2):362–369, obese-subjects trial. **Agree.**
- **Murphy (catabolism) 1998 — PMID 9467534** — B[4], C[3]. JCEM 1998;83(2):320–325, diet-induced catabolism. **Agree.**
- **Copinschi (sleep) 1997 — PMID 9349662** — B[7], C[8]. Neuroendocrinology 1997;66(4):278–286. **Agree.**

No cross-section citation maps to a different author/year/title. **0 mismatches.**

## Institutions / sponsor

- **Merck** as originator/sponsor, development code **MK-0677**, chemical lineage **L-163,191**: stated in A, B, C, D, E, F. All agree Merck developed it, advanced it through Phase II, and **discontinued** development (B, C, E). **Agree.**
- **Thorner / UVA** group attribution: A (Thorner foundational lineage, Chapman/Copinschi co-author), C (lineage table: Nass/Chapman/Chapman-1997 = UVA/Thorner group), F (Japanese patent JP5336349B2 assignee Michael O. Thorner). Consistent across A/C/F. **Agree.**
- Successor program **LUM-201** (pediatric GHD, still investigational): named only in E. Single-section — out of scope, no conflict.

No cross-section institutional disagreement. **0 mismatches.**

## Compound identifiers (LOAD-BEARING: molecular vs PD half-life)

- **Small molecule, non-peptide, GHS-R1a agonist, NOT a GHRH analogue, oral:** asserted identically in A, B, C, D, E, F. **Agree.**
- **Half-life — molecular vs pharmacodynamic.** This was the priority residual-conflict check:
  - **Section A:** molecular elimination t½ **≈4.7 h** (≈4–6 h preclinical), and explicitly states the "~24 h half-life" widely quoted by aggregators is **NOT** the molecular elimination half-life but the **pharmacodynamic duration of effect** (sustained IGF-1 across the 24-h interval).
  - **Section F:** "the molecule's elimination half-life is ~4–6 h, but its pharmacodynamic GH/IGF-1 effect persists ~24 h — see §A; do not confuse the two."
  - A and F are **mutually consistent** and both partition molecular (~4–6 h) from PD (~24 h) correctly.
  - **No section states "~24 h" as the molecular/elimination half-life.** B, C, D, E make no contradictory half-life claim. The previously-flagged inconsistency is resolved.
- **Mesylate salt / CAS 159752-10-0 / PubChem CID 178024:** A (mesylate, CID 178024), C (ibutamoren mesylate), F (CAS 159752-10-0). No conflict.

No cross-section disagreement. **0 mismatches.**

## Regulatory dates / facts

- **Never approved (FDA/EMA, anywhere):** E (explicit), D ("never received marketing approval"), F (OPSS "never approved for human use"). **Agree.**
- **NOT a lawful dietary ingredient; FDA Dec-2025 warning letters:** E (Prime Sports Nutrition 2025-12-12; **Agebox Inc. 2025-12-19**), F (**Agebox Inc. 2025-12-19**, undeclared ibutamoren mesylate in children's product). The shared Agebox letter date (2025-12-19) agrees across E and F. **Agree.**
- **§503A peptide action / FR Doc 2026-07361 does NOT capture MK-677 (small molecule, not peptide):** E (full treatment, FR-2026-07361 / 91 FR 20465 / Apr-16-2026, MK-677 absent), F (not on FDA 503A bulk list, cannot be compounded). **Agree** — both keep MK-677 outside the peptide framework.
- **WADA S2 (GH secretagogue / ghrelin-mimetic), prohibited at all times:** E (S2, ibutamoren named), F (on WADA prohibited list), D (class context). **Agree.**

No cross-section disagreement. **0 mismatches.**

## Trial registrations / dose & key-number cross-checks (no formal NCT IDs present)

No NCT/EudraCT registration identifiers appear in any section, so there are zero trial-registration entities to reconcile (scanned = 0). The dose and key-number cross-checks belong here for completeness:

- **Trial dose 25 mg/day** (Nass, Chapman, Svensson, Sevigny, Adunsky): consistent in A, B, C, D. **Practitioner ~10–25 mg/day** (F) is presented as gray-market convention with the clinical 25 mg explicitly distinguished from ~10–15 mg anti-aging use — **not conflated.** **Agree.**
- **Nass FFM +1.1 kg:** B (+1.1 kg, 95% CI 0.7–1.5) and C[5] (+1.1 kg). Placebo comparator: C gives −0.5 kg; B describes the placebo arm qualitatively as "a decrease" — same direction, no contradiction. The +1.1-kg-without-function dissociation is consistent in B and C. **Agree.**
- **CHF signal 4/62 (~6.5%) vs 1/61 (~1.7%):** identical in C and D. **Agree.**
- **Chapman 4-wk fasting glucose 5.4 → 6.8 mmol/L:** A, B, D — identical. **Nass +0.3 mmol/L:** B, D — identical. **Agree.**
- **Sevigny IGF-1 +60.1% (6 wk) / +72.9% (12 mo):** B, C, D — identical. **Agree.**

No cross-section disagreement. **0 mismatches.**

---

## Verdict

verdict: PASS

All shared entities appearing in more than one section agree. The priority check — any residual molecular-vs-pharmacodynamic half-life inconsistency — is clean: Sections A and F both state ~4–6 h molecular elimination vs ~24 h PD duration, and no section reports "~24 h" as the molecular half-life.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":7,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":3,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":6,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":4,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":0,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
