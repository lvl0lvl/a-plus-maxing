# Gate 7.5 — Risk-Floor Verification
**Compound:** Cerebrolysin (porcine-brain peptide hydrolysate; EVER Neuro Pharma GmbH, Austria)
**compound_risk_tier:** medium
**Sources verified:**
- `vault/library/peptides/cerebrolysin/research-report.md` (§5.1–5.6)
- `/tmp/aplus-research/cerebrolysin/sections/section-D.md` (§D.2, D.3)

---

## Verdict

verdict: PASS

```json
{
  "phase": "7.5",
  "verdict": "PASS",
  "iterations": 1,
  "compound_risk_tier": "medium",
  "compound_entry_path": "vault/compounds/cerebrolysin.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "populated"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": [
    "clinical infusion-monitoring (hypersensitivity/anaphylactoid during infusion)",
    "renal function assessment / eGFR (pre-treatment baseline — severe renal impairment contraindication)"
  ],
  "halt_reasons": []
}
```

---

## Prose Verification

### adverse_effects_literature — POPULATED

Both sources carry all six load-bearing safety items:

**1. Cochrane 2023 non-fatal SAE signal.**
Research report §5.2 and section-D §D.2.2 both quote: "Non-fatal SAE: RR 2.39 (95% CI 1.10–5.23) — 3 trials, 1,335 participants; moderate-certainty evidence" and the 30 mL×10-day dose-response refinement "RR 2.87 (95% CI 1.24–6.69) — 2 trials, 1,189 participants." The Cochrane reviewers characterize this as moderate-certainty, and the report explicitly distinguishes this from the null all-cause death and null total-SAE findings, making clear the non-fatal-SAE subset is the safety signal.

**2. Common non-serious AEs.**
Research report §5.1 and section-D §D.2.1 both enumerate: "agitation, insomnia, dizziness, sensation of heat/warmth, nausea, headache, tremor, and injection-site pain/swelling." Source: Thome & Doppler 2012 safety pooled review plus SmPC-derived prescribing information [ref 40/7 in respective bibliographies].

**3. Hypersensitivity/anaphylactoid reactions.**
Research report §5.2 (final paragraph) and section-D §D.2.3 both list the reaction profile: "skin reactions, local inflammatory reactions, headache, neck pain, limb pain, fever, low back pain, dyspnea, chills, and shock-like state." Both describe these as "very rare" but characterize them as the most clinically serious acute administration risks.

**4. Porcine-CNS prion theoretical consideration.**
Research report §1.3 and section-D §D.2.4 both cover: pigs not a natural TSE reservoir; experimental parenteral BSE inoculation produced disease at 69–150 weeks (Wells et al. 2003, PMID 12655106); porcine brain cortex is the highest-risk anatomical compartment for prion contamination; manufacturer GMP controls acknowledged; no documented human case; theoretical and regulatory in character. Grey-market product lacks GMP oversight, materially elevating the unaudited theoretical risk.

**5. Healthy-adult population-mismatch (load-bearing caveat).**
Research report §5.1 opens with an explicit mandatory callout: "The population-mismatch caveat is mandatory and load-bearing: All safety and tolerability data in this section derive from RCTs in elderly disease populations... No controlled safety data exist in healthy adults." Section-D §D.2.1 carries the same callout verbatim as a boxed note: "no controlled safety data exist in healthy adults. The extrapolation gap is unquantified."

**6. Grey-market supply-chain hazards.**
Research report §6.3 and section-D §D.1.2 both document: cold-chain requirement unenforceable in grey-market international shipments; counterfeiting risk (qualitative hazard indicator; ~37% adulteration figure from a vendor source, flagged as self-interested); endotoxin/microbial contamination risk from improperly stored biologics; no legal US prescribing pathway; no Western regulatory audit of grey-market product.

---

### contraindications — POPULATED

Research report §5.3 and section-D §D.3.1 both provide the complete labeled contraindication set from the Austrian SmPC and regional equivalents:
1. Known hypersensitivity to any component (including porcine-derived products)
2. Epilepsy / status epilepticus / grand mal convulsions
3. Severe renal impairment (low-molecular-weight peptide accumulation; population excluded from trials)
4. Pregnancy and breastfeeding (absent reproductive safety data)
5. Drug interactions: avoid concurrent MAO inhibitors; caution with antidepressants

The no-healthy-adult-data caution and grey-market-purity risk are each documented explicitly in both sources (see adverse_effects_literature §5, §6 above) and are tied directly to the contraindication context through the population-mismatch callout in §D.3.2: "The contraindications, monitoring parameters, and stopping criteria in D.3 are derived from labeling and RCT data in stroke/dementia populations... not a complete safety picture for healthy-adult off-label use, for which no controlled data exist."

---

### monitoring — POPULATED

Research report §5.4 and section-D §D.3.2 address monitoring. Key verified content:

**Infusion-phase clinical monitoring (primary objective monitoring):**
Section-D §D.3.2: "Clinical observation for hypersensitivity reactions (skin changes, dyspnea, chills, hemodynamic instability) — particularly in the first 20–60 minutes of each infusion cycle." This is the primary monitoring requirement given the anaphylactoid risk, and it is an objective clinical-observation protocol (not a self-report).

**Renal function baseline (objective assay — maps to eGFR):**
Section-D §D.3.2: "Pre-treatment baseline: Renal function assessment (to exclude severe impairment)." Research report §5.3 lists "Severe renal impairment" as a labeled contraindication, making pre-treatment renal function assessment the objective assay directly tied to a label-based exclusion criterion. This maps to eGFR as the standard clinical measure of renal function; the text uses "renal function assessment" rather than naming eGFR by abbreviation, but the clinical referent is unambiguous.

**No validated efficacy biomarker — honest caveat present:**
Both sources explicitly state this. Section-D §D.3.2: "There is no validated laboratory biomarker for Cerebrolysin's neurotrophic effect. Outcome monitoring is functional-scale based (e.g., NIHSS, mRS, Barthel Index in stroke; ADAS-Cog in dementia). No surrogate biochemical endpoint guides dosing or continuation decisions." Research report §5.4: "No surrogate biochemical endpoint validates neurotrophic effect or guides dosing; monitoring is functional-scale-based."

**ALT/AST and hs-CRP status:** These markers are NOT explicitly named in either source document. The gate JSON above accurately reflects only the markers the report actually supports; ALT/AST and hs-CRP are reasonable additions for a wiki entry covering hepatic baseline and immunogenicity of a foreign-protein injectable, but they are not documented in the retrieved research evidence and are therefore not listed as source-derived markers. The wiki entry author may add them with independent justification, but this gate documents only what the research supports.

---

### stopping_criteria — POPULATED

Section-D §D.3.3 provides:
- "Immediate cessation: Any sign of hypersensitivity/anaphylactoid reaction during infusion (skin reactions, dyspnea, chills, hemodynamic instability)"
- "Reassess: New-onset seizures or increased seizure frequency during a treatment course"
- "Escalating non-fatal SAEs: Given the Cochrane dose-response signal at higher cumulative doses, any unexpected serious non-fatal events during a course warrant reassessment of benefit-risk"

These are conservative and appropriate given the SAE signal + no-healthy-adult-data context. The "ANY hypersensitivity" trigger and the SAE-escalation clause are consistent with a medium-tier compound with a characterized non-fatal SAE signal.

---

## Summary of SAE Signal, Prion, and Population-Mismatch Basis

The non-fatal SAE signal is sourced from the highest-tier independent evidence available (Cochrane 2023, Tier 1): RR 2.39 (95% CI 1.10–5.23), moderate-certainty, from 3 trials and 1,335 participants — not from manufacturer-associated analyses. The dose-response refinement (RR 2.87 at the standard 30 mL×10-day regimen) strengthens the signal's plausibility and is reported accurately in both source documents without minimization.

The prion consideration is grounded in peer-reviewed animal evidence (Wells et al. 2003, PMID 12655106, Tier 2/government lab) and is characterized precisely as theoretical and regulatory in character — neither dismissed nor amplified. The healthy-adult population-mismatch is stated as a mandatory, load-bearing caveat in both sources, not a footnote.

These three items — the Cochrane SAE signal, the prion theoretical, and the population-mismatch — collectively constitute the core risk-floor basis for the medium compound_risk_tier designation, and all three are well-evidenced in the retrieved sources.
