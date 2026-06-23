# Phase 7.5 — Risk-Floor Verification: FOXO4-DRI

**Compound:** FOXO4-DRI (Proxofim)
**Risk tier:** experimental
**Sources reviewed:** `vault/library/peptides/foxo4-dri/research-report.md` + `/tmp/aplus-research/foxo4-dri/sections/section-D.md`
**Verification date:** 2026-06-20

---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/foxo4-dri.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["troponin I/T (cardiac — cardiotoxicity concern flagged by Zhang 2020 Leydig study)","CK-MB (cardiac — same cardiotoxicity gap)","eGFR / BUN / creatinine (renal — Baar 2017 measured BUN/creatinine; eGFR has a wiki biomarker page)","CBC with differential (platelets, lymphocytes — apoptotic stress markers)"],"halt_reasons":[]}
```

---

## Field-by-Field Verification

### 1. `adverse_effects_literature` — POPULATED

All five load-bearing adverse concerns are present and cited:

**(a) On-target off-tumor p53-apoptosis risk in non-senescent cells**

Research report §4.3 (p53 activation / on-target off-tumor concern):
> "FOXO4-DRI directly engages p53 — a master regulator of apoptosis, cell-cycle arrest, DNA damage response, hypoxia response, and wound healing — and activates the p53-centric mitochondrial apoptosis pathway. A systemic p53-apoptosis activator could in principle trigger apoptosis in any non-senescent cell that happens to have elevated p53 activity at the moment of exposure."

Section D §D.3.2 canonically frames this as the mechanism-derived risk:
> "Systemic delivery of a p53-apoptosis activator could, in principle, trigger apoptosis in any non-senescent cell that happens to have elevated p53 activity at the time of exposure."

The FEBS Letters 2018 framing is quoted in both documents:
> "FOXO4-DRI targets the tumor suppressor p53, a crucial protein, which may lead to various side effects in clinical trials." (Bourgeois & Madl 2018, [11] in both sources)

Human safety is explicitly characterized as UNCHARACTERIZED: "no human clinical trial of FOXO4-DRI exists at any phase" (research report §2.4); "No Phase 1, 2, or 3 data exists" (section-D §D.1).

**(b) FOXO4 expression in heart/testis → cardiotoxicity flagged-but-unassessed (Leydig study)**

Research report §4.4:
> "FOXO4 protein is expressed in normal human heart and testis tissue in addition to senescent cells. This expression pattern is the basis of the cardiotoxicity concern flagged by the Zhang 2020 Leydig-cell study authors, who wrote explicitly that 'special attention must be paid to muscle damage, especially cardiotoxicity,' acknowledging an inability to fully assess this risk due to the technical limitations of their mouse model. To date, no published study has assessed cardiac tissue histopathology, troponin I/T, CK-MB, or other cardiac biomarkers at time points appropriate for detecting delayed myocardial injury following FOXO4-DRI administration."

Section-D §D.3.3 mirrors:
> "The Leydig cell study authors explicitly flagged this: 'special attention must be paid to muscle damage, especially cardiotoxicity,' acknowledging an inability to fully assess this risk due to technical limitations of the mouse model. No published study has directly evaluated cardiac tissue histopathology or biomarkers for muscle damage (CK, troponin) at time points appropriate for detecting delayed myocardial injury."

**(c) Chondrocyte p21-stressor signal**

Research report §4.4:
> "The chondrocyte p21 signal adds a second layer to this concern. The increase in p21 levels observed in FOXO4-DRI-treated senescent chondrocyte cultures — above and beyond the cell death in the senescent fraction — suggests the peptide may activate a cell-stress program in neighboring or partially-senescent cells that is distinct from the three-step senolytic mechanism."

Section-D §D.3.2:
> "The chondrocyte study added a relevant cautionary note: FOXO4-DRI treatment increased p21 levels even in the senescent cell cultures, suggesting the compound 'might be a potential stressor to cells' beyond simply executing apoptosis in target cells — warranting further investigation of unintended consequences."

**(d) Born/Adnot 2023 Circulation — senolysis WORSENED pulmonary hypertension**

Research report §3.1 and §2.3 (adverse finding, reference [28]):
> "The finding is adverse and important: eliminating senescent pulmonary endothelial cells worsened pulmonary hemodynamics rather than improving them, indicating that senescent cells in the pulmonary vascular niche exert a protective or compensatory function in this disease context. This is the only primary FOXO4-DRI study to report a pathological worsening of disease with senolytic treatment, and it directly demonstrates that the blanket 'senescent cells are harmful, remove them' framing does not hold across all tissue contexts. Published in a high-impact cardiovascular journal (*Circulation*), this paper is one of the most significant counterpoints in the FOXO4-DRI literature."

Full citation confirmed in bibliography [28]:
> "Born E, Lipskaia L, Breau M, et al. Eliminating Senescent Cells Can Promote Pulmonary Hypertension Development and Progression. *Circulation*. 2023;147(8):650–666. DOI: 10.1161/CIRCULATIONAHA.122.058794. PMID: 36515093. — tag: animal — adverse finding — senolytic clearance (including FOXO4-DRI) worsened pulmonary hemodynamics, demonstrating context-dependent beneficial roles for senescent pulmonary endothelial cells."

**(e) Immunogenicity of all-D-amino acid peptide — unknown**

Research report §4.5:
> "The immunogenicity of systemically administered all-D peptides in humans is unknown. It is possible that D-amino acid sequences are poorly recognized by antigen-presenting cells, resulting in low immunogenicity; it is also possible that DRI peptides generate novel antigenic epitopes not present in the natural proteome, resulting in unexpected immune reactions. No human immunogenicity data exist for FOXO4-DRI or any closely related DRI compound."

Section-D §D.3.1 self-check:
> "Human immune responses to a large all-D-amino acid peptide (a non-natural stereochemistry not present in the human proteome) are unknown and could include immunogenicity."

Monitoring panel includes anti-drug antibody (ADA) assay at 30 and 90 days, specifically to characterize this unknown.

---

### 2. `contraindications` — POPULATED

Research report §4.8 and section-D §D.5 provide explicit contraindication lists, grounded in mechanism:

**Absolute contraindications (both sources in agreement):**
- Active malignancy or history of treated malignancy (p53 pathway manipulation in oncology settings is unpredictable and carries uncharacterized risk)
- Active infection or systemic inflammatory state (p53 is an active effector in immune-cell apoptosis)
- Pregnancy (FOXO4 expressed in placenta; embryotoxic risk uncharacterized)
- Known hypersensitivity to D-amino acid peptides
- Thrombocytopenia or active bleeding disorder

**High-caution / relative contraindications:**
- Significant cardiac disease (FOXO4 muscle expression; cardiotoxicity risk not excluded)
- Pulmonary hypertension / contexts where senescence is protective (Born/Adnot 2023 FOXO4-DRI adverse finding in *Circulation* is the direct grounding)
- Athletes subject to WADA code (S0 prohibited)
- Concurrent chemotherapy or radiation
- Known germline TP53 mutations (Li-Fraumeni syndrome)

The Born 2023 *Circulation* paper provides specific empirical grounding for the pulmonary hypertension contraindication beyond theoretical caution — this is a direct adverse FOXO4-DRI finding in a peer-reviewed high-impact journal.

---

### 3. `monitoring` — POPULATED

Section-D §D.5 (monitoring section) and research report §4.8 both name ≥1 objective marker in each domain:

**Cardiac (troponin/CK-MB — named explicitly):**
> "Cardiac: troponin I/T, CK-MB, ECG (baseline, 48 h, 7 days) — specifically to address the cardiotoxicity gap flagged by animal authors." (section-D §D.5)
> "cardiac biomarkers (troponin I/T, CK-MB, and ECG at baseline, 48 hours, and 7 days, specifically to address the uncharacterized cardiotoxicity concern)" (research report §4.8)

**Hepatorenal (eGFR/BUN/creatinine — named explicitly):**
> "Renal function: BUN, creatinine, eGFR (same schedule)" (section-D §D.5)
> "renal function (BUN, creatinine, eGFR at the same schedule)" (research report §4.8)

Note: Baar 2017 measured BUN and creatinine as primary efficacy/safety readouts; eGFR has a dedicated wiki biomarker page. Both are grounded in the primary literature.

**CBC:**
> "Complete blood count with differential (platelets, lymphocytes — apoptotic stress markers)" (section-D §D.5)
> "complete blood count with differential" (research report §4.8)

**Hepatic:**
> "Hepatic function: ALT, AST, bilirubin (baseline, 7 days, 30 days post-dose)" (both sources)

**Immunogenicity:**
> "Immunogenicity: anti-drug antibody (ADA) assay at 30 and 90 days (novel D-amino acid scaffold, unknown antigenicity)" (section-D §D.5)

All monitoring items are named objective assays with explicit schedules (not vague "check labs" language).

---

### 4. `stopping_criteria` — POPULATED

Section-D §D.5 and research report §4.8 list specific quantitative stopping thresholds:

> - Any ALT/AST >3× upper limit of normal (ULN)
> - Creatinine rise >1.5× baseline
> - **Troponin elevation above ULN** (cardiac — directly addresses the unresolved cardiotoxicity concern)
> - Platelet count fall >30% from baseline
> - Grade 2 or higher injection-site reaction
> - Clinical signs of systemic immunogenic reaction (urticaria, angioedema, bronchospasm)

Research report §4.8 also adds:
> "Any sign of systemic immunogenic reaction."

The no-validated-efficacy-biomarker honesty is embedded in both documents' framing: because no human pharmacodynamic (senescence-clearance) biomarker is validated, there is no response threshold to titrate to — this is documented throughout as a core limitation of the human experimental context.

---

### 5. Third-Party Objective Monitoring Marker — PRESENT (multiple)

Named objective assays with the sources supporting them:

| Marker | Source grounding |
|--------|-----------------|
| Troponin I/T | Research report §4.4 (cardiotoxicity gap) + §4.8 + section-D §D.3.3 + §D.5 |
| CK-MB | Research report §4.4, §4.8 + section-D §D.3.3, §D.5 |
| eGFR / BUN / creatinine | Research report §4.8 + section-D §D.5; Baar 2017 measured BUN/creatinine [1]; eGFR has wiki biomarker page |
| CBC with differential | Research report §4.8 + section-D §D.5 |

`third_party_monitoring_marker_present: true` — troponin/CK-MB and eGFR each meet the criterion independently.

---

## Summary

The report fully populates all four required risk-floor fields with load-bearing content retrieved from primary sources, including the Born/Adnot 2023 *Circulation* adverse FOXO4-DRI finding (senolysis worsened pulmonary hypertension) and the Zhang 2020 cardiotoxicity flag (troponin/CK-MB monitoring explicitly named), and all five adverse-effects sub-concerns (p53 on-target off-tumor, cardiotoxicity gap, chondrocyte p21 stressor, Born 2023 pulmonary adverse finding, immunogenicity unknown) are present and cited; verdict is **PASS**.
