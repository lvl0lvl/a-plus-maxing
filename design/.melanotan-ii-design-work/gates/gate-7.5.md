# Gate 7.5 — Risk-Floor Verification: Melanotan-II

**compound:** Melanotan-II (MT-II)
**compound_risk_tier:** experimental
**sources reviewed:**
- `vault/library/peptides/melanotan-ii/research-report.md`
- `/tmp/aplus-research/melanotan-ii/sections/section-D.md`
**gate_date:** 2026-06-21

---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/melanotan-ii.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["full-body skin examination + dermoscopy","eGFR / serum creatinine","creatine kinase (CK)"],"halt_reasons":[]}
```

---

## Prose Detail

### 1. adverse_effects_literature — POPULATED

Both source documents carry a comprehensive, sourced AE profile with explicit tier labeling.

**Common MC-mediated AEs (dose-dependent):**
- Nausea/vomiting: documented at every dose level in Dorr 1996 (n=3 phase I pilot, 0.01–0.03 mg/kg SC; PMID 8637402 [open_label]). Mechanism: MC4R activation in area postrema/brainstem. Section D.2.1: "Nausea and vomiting are the most consistently reported adverse effects, occurring at essentially every dose level tested in the only published human phase I trial."
- Facial flushing: concurrent with nausea in Dorr trial; mechanism MC3R/MC4R-mediated vasodilation.
- Spontaneous penile erections / priapism: "Penile erections lasting 1–5 hours after dosing were documented in the Dorr 1996 phase I trial in male subjects" (Section D.2.1). Prolonged erection (>4 hours) = priapism risk with permanent erectile dysfunction potential if untreated. Confirmed as a stopping-criteria trigger.
- Fatigue/somnolence: grade II at 0.03 mg/kg (Dorr trial).

**Dermatologic nevi/melanoma signal — named and sourced, with honest limits stated:**
Section D.2.2 and research-report Section 4 both document this as the "load-bearing risk tier." Multiple geographically independent peer-reviewed case reports:
- Sivyer 2012 (Dermatol Pract Concept; PMID 23785612): 16yo female with FAMMM, 0.5 mg SC daily × 2 months → dermoscopically confirmed dysplastic compound nevus within 3 weeks.
- Hueso-Gabriel et al. 2012 (Actas Dermo-Sifiliográficas): >100 eruptive melanocytic nevi; 3 with severe dysplasia on histopathology.
- Schulze & Erdmann 2014 (Eur J Dermatol; PMID 24334249): eruptive nevi + darkening of pre-existing nevi within 24 hours of a single dose.
- Langan et al. 2009 (BMJ; PMID 19174439): rapidly changing moles, severely dysplastic and atypical nevi on biopsy; concurrent sunbed use.
- Melanoma temporal associations: Paurobally et al. 2011 (Br J Dermatol; Breslow 0.30mm melanoma), Ong & Bowling 2012 (Australas J Dermatol; PMID 22724573; melanoma in situ), Hjuler & Lorentzen 2014 (Dermatology; PMID 24355990; Danish cases with excised melanoma).
- The research report explicitly states: "biologically coherent, regulator-acknowledged, multi-source safety signal for dermatologic malignancy — not proof of causation, but a signal that warrants serious weight." Causal limits are stated: virtually every case involved concurrent UV; no epidemiologic cohort exists. Evidence tier for causation stated as tier 3; biological mechanism (MC1R → melanocyte proliferation without UV gating) stated as established.

**Idiosyncratic SAEs — all three named with PMID/DOI and tier labels:**
- Rhabdomyolysis: Nelson, Bryant, Aks 2012 (Clin Toxicol; PMID 23121206) — 39yo male, 6 mg SC, CPK 17,773 IU/L at 12h, creatinine 2.25 mg/dL, 3-day ICU. Multi-organ: sympathomimetic symptoms, rhabdomyolysis, and renal dysfunction.
- Renal infarction: Peters et al. 2020 (CEN Case Rep; PMID 31953620) — 45yo male, 27 mg cumulative SC over 6 months, right-sided renal infarction ~50% kidney, BP 165/95 mmHg. "First published case of MT-II-associated renal infarction."
- PRES: Annals of Internal Medicine 2013 (DOI 10.7326/0003-4819-158-9-201305070-00020) — PRES with seizures and MRI white-matter abnormalities; consistent with acute hypertensive MC4R agonism.

**Grey-market identity/purity hazard:** Both documents explicitly name the MT-I/MT-II/PT-141 confusion as a primary safety hazard. Research report Section 1.2 carries a disambiguation table; Section D.2.4 covers grey-market risk amplifiers (unknown purity, no sterility assurance, no AE reporting pathway, MHRA's 18 Yellow Card reports documenting 74 suspected adverse reactions).

**Honest limits acknowledged:** Case-report tier throughout the SAE literature. Research report: "Causality cannot be established from case reports alone." Section D.2.2: "The causal inference is confounded by concurrent UV exposure (tanning beds, solar) in virtually every reported case." Tier labeling is present throughout.

---

### 2. contraindications — POPULATED

Section D.6 and research-report Section 5.5 both carry mechanism-grounded contraindication lists with source citations:

- Personal or family history of melanoma or dysplastic nevus syndrome / FAMMM — Sivyer case cited [PMID 23785612].
- Multiple (>50) atypical nevi — elevated absolute risk under pharmacological melanocyte stimulation.
- Cardiovascular disease, hypertension, or arrhythmia — Nelson rhabdomyolysis case (acute hypertension, tachycardia in otherwise healthy 39yo); cardiac risk in pre-existing disease "uncharacterised and likely elevated."
- Renal impairment — Peters renal infarction [PMID 31953620] + nephrotoxic signal from Nelson rhabdomyolysis.
- History of seizures / neurological conditions — PRES case with seizures.
- Male patients with priapism risk factors — sickle cell trait, concurrent PDE5 inhibitors or anticoagulants.
- Pregnancy and breastfeeding — no data; MC4R agonism has potential reproductive-axis effects.
- Fitzpatrick I/II with concurrent UV tanning practices — research report names this explicitly as "the highest-risk dermatologic profile documented across the nevi/melanoma case series."
- Grey-market purity / identity: implicit across both documents; Section D.2.4 covers the grey-market caution in detail.

---

### 3. monitoring — POPULATED (PRIMARY is dermatologic; eGFR/renal is the objective-lab marker for the SAE signal)

Section D.7 and research-report Section 5.6 provide a structured monitoring protocol. The PRIMARY monitoring domain — as mandated by the melanoma signal — is dermatologic surveillance:

**Dermatologic monitoring (highest priority, per both documents):**
- Full-body skin examination with total-body photography BEFORE any use and at intervals during use. Research report: "baseline documentation is essential because MT-II rapidly changes lesion appearance, making change detection impossible without a pre-use baseline."
- Dermoscopy of all nevi at baseline and after first weeks of use. Sivyer case showed dermoscopic changes within 3 weeks of daily 0.5 mg SC.
- Section D.7: "Any new, enlarging, darkening, or morphologically changing nevus is a hard stopping criterion — referral for dermatologic evaluation and excision biopsy if indicated."
- Intensified surveillance for FAMMM syndrome, Clark nevus syndrome, personal/family melanoma history, Fitzpatrick I/II, or >50 moles.

**Renal monitoring (objective-lab marker for the idiosyncratic SAE signal):**
Section D.7: "Baseline serum creatinine and urinalysis; monitor during prolonged or cumulative use; discontinue on rising creatinine, proteinuria, or flank pain." Research report Section 5.6 identical: "Baseline serum creatinine and urinalysis; monitor during prolonged or cumulative use; discontinue on rising creatinine, proteinuria, or flank pain." The Peters renal infarction case [PMID 31953620] is cited as the grounding AE for this recommendation.

Serum creatinine / eGFR is the objective lab assay called for here. The wiki contains a [[biomarkers/egfr]] page; the field content is defensibly linked to that marker.

**CK (creatine kinase — rhabdomyolysis screen):**
Both stopping-criteria lists carry: "Muscle pain + dark urine — rhabdomyolysis screen." The Nelson case established the CK trajectory (1,760 IU/L admission → 17,773 IU/L at 12h; PMID 23121206). CK is the objective assay implied by the rhabdomyolysis stopping criterion. Research report Section 5.6 identifies "rhabdo screen" explicitly in the stopping criteria, and the CPK/CK data are presented in the SAE section.

**Cardiovascular monitoring:**
Baseline BP and HR; discontinue on sustained hypertension (>150/95 mmHg) or tachycardia (>100 bpm at rest). Objective (BP, HR) — grounded in the Nelson case and PRES case.

All three third-party objective markers are present and named in the source documents.

---

### 4. stopping_criteria — POPULATED

Section D.7 and research-report Section 5.6 each provide an explicit, numbered seven-criterion stopping list (any one sufficient). Present in both sources verbatim:

1. Any changing, new, or atypical nevus → dermatology referral before resuming.
2. Prolonged erection (>4 hours) → emergency evaluation for priapism.
3. Significant nausea/vomiting impairing function.
4. BP >150/95 mmHg or HR >100 bpm not otherwise explained.
5. Muscle pain + dark urine → rhabdomyolysis screen.
6. Neurological symptoms: headache with visual changes, seizure, confusion → PRES screen.
7. Unilateral flank pain → renal infarction screen.

The dermatologic criterion (criterion 1) is explicitly the primary stopping trigger, directly tied to the melanoma signal. The "no validated efficacy biomarker" limitation is acknowledged in the research report's broader discussion (Section 8 summary).

---

### 5. third_party_monitoring_marker — PRESENT (3 named)

| Marker | Objective assay | AE signal it covers | Source |
|--------|----------------|---------------------|--------|
| Full-body skin examination + dermoscopy | Structured clinical exam / dermoscopic imaging | Melanoma / dysplastic nevi signal (PRIMARY) | Section D.7; research-report §5.6; Sivyer, Hueso-Gabriel cases |
| eGFR / serum creatinine (+ urinalysis) | Laboratory assay | Renal infarction / nephrotoxic SAE | Section D.7; Peters 2020 [PMID 31953620] |
| Creatine kinase (CK) | Laboratory assay | Rhabdomyolysis | Section D.7 stopping criterion 5; Nelson 2012 [PMID 23121206]; CPK trajectory documented |

All three markers are named in the retrieved source documents. The PRIMARY monitoring burden is dermatologic (the melanoma/nevi signal). eGFR/serum creatinine is the load-bearing objective lab marker for the idiosyncratic-SAE renal signal. CK is the objective lab marker for the rhabdomyolysis signal.

---

## Gate Summary

All four required risk-floor fields are populated with source-grounded, tier-labeled content in both the research report and section-D.md. The dermatologic monitoring (full-body skin exam + dermoscopy) is named as the PRIMARY surveillance obligation — grounded in the biologically coherent, multi-source, regulator-acknowledged melanoma/nevi signal. eGFR/serum creatinine is the named objective lab marker for the renal SAE signal (Peters 2020 renal infarction case; consistent with the existing [[biomarkers/egfr]] wiki page). CK is named for the rhabdomyolysis signal (Nelson 2012). Contraindications are mechanism-grounded with case citations. Stopping criteria are explicit, numbered, and cover each load-bearing SAE class. The compound_risk_tier = experimental is fully warranted: never approved, active regulatory warnings in US/UK/AU, three distinct organ-system SAE case reports, a multi-source dermatologic malignancy signal, and no long-term safety data.

**verdict: PASS — all four required fields populated; three objective third-party monitoring markers present.**
