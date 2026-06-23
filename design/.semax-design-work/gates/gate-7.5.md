# Gate 7.5 — Risk-Floor Verification
## Compound: Semax (ACTH(4-7)PGP / Met-Glu-His-Phe-Pro-Gly-Pro)
## compound_risk_tier: experimental
## Sources verified: vault/library/peptides/semax/research-report.md + /tmp/aplus-research/semax/sections/section-D.md

---

## Verdict

verdict: PASS

```json
{
  "phase": "7.5",
  "verdict": "PASS",
  "iterations": 1,
  "compound_risk_tier": "experimental",
  "compound_entry_path": "vault/compounds/semax.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "populated"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": [
    "cognitive/symptom scales (MoCA, digit-span)"
  ],
  "halt_reasons": []
}
```

---

## Prose Detail

### 1. adverse_effects_literature — populated

The report covers the AE reality across two complementary layers.

**Favorable tolerability signal (honest but bounded):** Gusev et al. 2005 (n=187 cerebrovascular insufficiency patients) stated Semax "is featured by minor percent of side-effects and is well tolerated by patients, including those of older age groups" [13, open_label]. Gusev et al. 2018 (n=110 post-stroke, 6,000 µg/day 10-day courses) reported no serious adverse events [7, open_label]. The non-corticotropic design (ACTH(4-7) fragment lacks adrenocortical steroidogenesis sequences) is explicitly confirmed — users face no HPA-axis risk, no adrenal suppression, no hypercortisolemia — a real and well-established mechanism-level safety advantage.

**Evidence ceiling — stated explicitly (section 5.2 / D2):** Every AE data point derives from the same single-lineage Russian open-label studies. The report's evidence-ceiling box reads: "All human safety data for Semax derives from a single research lineage of Russian open-label clinical studies. No randomized controlled trials. No independent non-Russian replications. No published human pharmacokinetic data. No placebo-controlled adverse-event ascertainment with pre-specified endpoints. No long-term (≥1 year) safety data. Semax has never undergone Western regulatory safety review."

**Population mismatch (load-bearing, named explicitly):** Section 5.2 and D2 both flag this as a load-bearing limitation: "The AE base-rates and tolerability findings in the Semax literature derive from elderly Russian patients with cerebrovascular disease, stroke, or optic neuropathy... Healthy adults using self-administered grey-market Semax lack all three of those structural protections." The report explicitly states: "There are no controlled safety data for healthy-adult use."

**NASA near-zero evidence (named explicitly):** Section 1.1 and 4.4 address N-Acetyl-Semax-Amidate directly: "there are no published human studies, no animal pharmacology studies, no pharmacokinetic studies, and no safety studies for NASA as a distinct compound in any indexed database." The N-terminal acetylation was shown to abolish Semax's neuroprotective copper-chelation effect in vitro [11, in_vitro], demonstrating pharmacologically significant structural divergence.

**Grey-market purity hazards (named):** Section 4.4 names residual coupling reagents, incorrect-sequence peptides, aggregates, and microbial contamination as grey-market sourcing hazards, delivered directly to the olfactory epithelium and cribriform plate via intranasal route.

**Field: populated. The honest adverse-effects picture — genuine tolerability signal bounded by a single-lineage/open-label/disease-population ceiling, healthy-adult data void, and NASA near-zero evidence — is all present and prominently stated.**

---

### 2. contraindications — populated

Section 5.3 (research report) and D2 Contraindications block (section-D.md) both enumerate the formal Russian registration contraindications:

- **Hypersensitivity** to Semax or any formulation component
- **Acute psychosis or history of psychotic disorders** (standard language for neuropeptide preparations with dopaminergic/behavioral activation effects in Russian labeling)
- **Pregnancy and lactation** (contraindicated by absence of safety data; no controlled human teratogenicity data; "PubMed searches for Semax contraindications pregnancy returned zero results, confirming no indexed human pregnancy safety studies")

The no-healthy-adult-data and grey-market-purity cautions are woven through section 5.2 and D2 under the population-mismatch and evidence-ceiling headings. The NASA near-zero-data caution is explicit (sections 1.1, 4.4, and D1).

The report notes the source limitation: "These contraindications are drawn from the pattern of Russian prescribing information for Semax as described in the secondary Russian-language literature and pharmacological reviews. The primary regulatory source document (Росминздрав product insert) was not directly accessible in English-language format during this research sweep" — an appropriate provenance disclosure, not a gap.

**Field: populated.**

---

### 3. monitoring — populated

Section 5.4–5.6 (research report) and D4 (section-D.md) address monitoring in detail.

**No validated efficacy biomarker (stated explicitly):** Section 5.4 reads: "Semax has no validated clinical monitoring biomarker. BDNF has been proposed and measured in the Russian stroke rehabilitation literature as an exploratory pharmacodynamic marker [7, open_label]... However, BDNF has not been validated as a clinical monitoring endpoint — the correlation between a plasma BDNF increment and clinically meaningful cognitive or neurological outcomes has not been established in prospective trials with predefined endpoints." Section D4 repeats this judgment: "BDNF has not been validated as a clinical monitoring endpoint."

**Objective monitoring markers named (section 5.6 / D4):**
- **MoCA (Montreal Cognitive Assessment) and digit-span tests** — named explicitly in both documents as validated cognitive screening tools for attention, working memory, and fatigue tracking at baseline and after each course. These are the primary objective monitoring markers supported by the report.
- Nasal tolerance (mucosal irritation, epistaxis)
- Mood/behavioral monitoring (agitation, anxiety escalation, mood instability — particularly given the psychosis contraindication and dopaminergic behavioral effects in animals)
- Blood pressure / cardiovascular monitoring (appropriate given the cerebrovascular populations studied)

**hs-CRP and cortisol:** The task brief identifies these as expected markers. hs-CRP does not appear in the monitoring sections of either source document (the neuroinflammation anti-inflammatory mechanism is addressed in sections 3.3 and D2, but hs-CRP is not named as a monitoring marker). Cortisol likewise is addressed as a mechanism-level safety distinction (non-corticotropic; no HPA activation) in sections 5.1 and D2 Mechanism-Level Safety Basis, but cortisol is not named as a monitoring assay in sections 5.4–5.6 or D4. Per gate instructions, only markers actually supported by the report's monitoring content are listed. The third_party_markers field reflects this accurately.

**Field: populated. ≥1 objective marker (MoCA/digit-span cognitive scales) is present. The "no validated Semax-specific efficacy biomarker" and "BDNF-as-research-marker is NOT a validated clinical monitor" caveats are both explicitly stated.**

---

### 4. stopping_criteria — populated

Sections 5.3 and D4 enumerate:

- Emergence of **psychotic symptoms**, hallucinatory states, or acute agitation → discontinue immediately
- **Hypersensitivity reactions** (nasal anaphylaxis possible with peptide intranasal preparations) → discontinue immediately
- **Worsening of any pre-existing psychiatric condition**
- **Pregnancy recognition** → discontinue immediately per contraindication
- **Lack of subjective or objective benefit** after 2 full standard courses (5–10 days each, per the Russian clinical literature dosing pattern)

The conservative framing is appropriate for the evidence context: no healthy-adult data, single-lineage-evidence, and no validated efficacy biomarker underpin the "2 courses without benefit → stop" criterion.

**Field: populated.**

---

### 5. Single-lineage-open-label + healthy-adult-mismatch + non-corticotropic basis — attestation

All three load-bearing qualifications are present throughout both documents:

**Single-lineage open-label:** Quantified in section 4.1 — approximately 78–89% of verifiable English-language peer-reviewed publications carry IMG-RAS/Myasoedov authorship; approaching 90–95% for the mechanistic BDNF/neuroprotection corpus. "Zero independent non-Russian replication of the BDNF-induction mechanism exists." The evidence ceiling box in section 5.2 / D2 makes this the framing premise for all safety characterizations.

**Healthy-adult population mismatch:** Named explicitly as "load-bearing" in section 5.2 and D2. Section 6.2 has a dedicated subsection ("What Does Not Transfer from the Clinical Literature to Healthy-Adult Use") itemizing which findings do not transfer to healthy adults: the tolerability finding, the efficacy finding, the BDNF observation, and the dose.

**Non-corticotropic basis confirmed:** Section 5.1 / D2 Mechanism-Level Safety Basis confirms non-corticotropic design established in the foundational ACTH fragment literature [35, 36 mechanism_review] and corroborated in modern preclinical work [27, animal]. Evidence table (section 6.4) lists "Non-corticotropic (no HPA activation)" as "Established by design" with "Independent (class literature)" as the independence qualifier.

---

## Gate Summary

verdict: PASS — all 4 required risk-floor fields (adverse_effects_literature, contraindications, monitoring, stopping_criteria) are populated from retrieved sources. The primary third-party objective monitoring marker is cognitive/symptom scales (MoCA, digit-span), explicitly named in sections 5.6 and D4. hs-CRP and cortisol appear in mechanism and safety-basis sections but are not named in the monitoring content; only markers present in the monitoring sections are listed in third_party_markers. The "no validated Semax-specific efficacy biomarker" caveat and the single-lineage/open-label/healthy-adult-mismatch/non-corticotropic qualifications are all prominently stated in both source documents.
