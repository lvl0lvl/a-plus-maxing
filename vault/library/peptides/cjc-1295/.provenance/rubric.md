# CJC-1295 — Phase 2.5 Rubric + Section Plan (deep mode, efficient calibration)

## Mode
deep mode (25+ sources total across sections, ~10k-word report floor) run under the
**efficient calibration**: judge bar **92** (sanctioned standard-mode value; documented
in [[project-aplus-peptide-deep-sweep]]), judges flag ONLY genuine defects
(fabrication / misattribution / wrong-PMID / regulatory-error / misleading-tally /
type-tag violation), not cosmetic nits; ONE remediation round per real defect.

## The defining fact (must be correct everywhere — like LL-37's dual nature)
CJC-1295 names TWO distinct molecules that are constantly conflated:
- **CJC-1295 WITH DAC** ("DAC:GRF", drug-affinity-complex): GRF(1-29) tetrasubstituted analogue
  + a maleimido-propionyl-Lys that covalently binds serum albumin → half-life ~days. The
  Teichman 2006 human trial is THIS molecule.
- **CJC-1295 WITHOUT DAC** = **"Modified GRF 1-29" / "Mod GRF 1-29" / CJC-1295 no-DAC**:
  same tetrasubstitutions, NO DAC, half-life ~30 min. Commonly stacked with ipamorelin.
NEVER attribute one's PK / trial / dosing to the other. Mislabeling is rampant in
vendor + practitioner sources — call it out.

## Section plan (6 lean sections)
- **A — Identity, structure, mechanism.** GHRH-analogue (GRF(1-29) = sermorelin core);
  the 4 substitutions (D-Ala2, Gln8, Ala15, Leu27) for protease resistance; DAC vs no-DAC
  + albumin binding; GHRH-receptor (NOT ghrelin/GHSR — contrast with ipamorelin); pulsatile
  vs tonic/"bleed" GH elevation; downstream IGF-1.
- **B — Human pharmacology & efficacy.** Teichman 2006 (DAC) PK/PD; any other human data;
  ConjuChem clinical program (indications pursued, outcomes, discontinuation); GH/IGF-1
  magnitude + duration; body-composition/anti-aging claims = human-proven? (expect NO).
- **C — Preclinical + concentration audit.** Animal GH/IGF-1 data (species + n); the
  originating lineage (ConjuChem / Teichman) single-lab share — compute & flag if ≥70%.
- **D — Safety / adverse effects / the disputed fatality reports.** Verify or refute the
  widely-repeated "CJC-1295 deaths" claim against a REAL source — if only anecdotal/forum,
  label it unverified, do NOT state as fact. GH-axis class risks (edema, arthralgia,
  carpal tunnel, insulin resistance); the DAC long-half-life amplifying any AE; tachyphylaxis.
- **E — Regulatory & sport status.** FDA never approved; 503A interim Category-2 history;
  **explicitly check the April-16-2026 FR Doc 2026-07361 action — is CJC-1295 in the
  removed-12 or NOT?** (canonical removed-12 does NOT list CJC-1295 — verify its actual
  current status; removal ≠ approval); PCAC timing; WADA S2.2 (GH secretagogues / GHRH);
  the no-DAC "Mod GRF 1-29" labeling gray zone.
- **F — Practitioner-practice layer + non-English literature.** Compounding data sheets
  (compounding_data_sheet) + named-prescriber conventions (practitioner_protocol) — typical
  DAC ~1–2 mg/wk vs no-DAC ~100 mcg pre-/post-stack with ipamorelin; Russian/Chinese
  literature survey.

## Mandatory rubric dimensions (health)
- Sikiric-style concentration audit (distinct primaries by lab affiliation; flag ≥70% single-lab).
- Population annotation (every animal cite: species + n).
- Route fidelity (no route extrapolation without explicit [route-extrapolation] tag).
- Risk-floor readiness (contraindications + monitoring + stopping criteria fillable).

## RECURRING-ERROR SELF-CHECKS — every retrieval agent runs these before returning
1. **Verify every PMID / DOI / NCT** resolves to the EXACT first-author + year + journal you
   claim. Do NOT cite an identifier you did not open/verify. (wrong-PMID-real-source class —
   it has bitten every prior entry.)
2. **FDA 503A April-2026 check:** state CJC-1295's actual status in/after FR Doc 2026-07361
   (2026-04-16). Removal ≠ approval. Do not guess — verify.
3. **NO Wikipedia citations** (mechanical HALT, IC-12). No vendor_label / anecdote_aggregate
   grounding any NUMERICAL claim.
4. **Tally-vs-enumeration:** any "N studies/trials show X" must be backed by an enumerated
   list of exactly N items.
5. **DAC vs no-DAC discipline:** never cross-attribute PK / trials / dosing between the two.
6. **"Deaths" claim:** verify against a real source or explicitly mark unverified.
7. **Type-tag every claim** from the enum; vendor/anecdote never ground numbers.
