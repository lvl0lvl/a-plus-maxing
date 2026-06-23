# Gate 7.5 — Risk-Floor Verification (Humanin)

**compound_risk_tier:** experimental  
**compound_entry_path:** vault/compounds/humanin.md  
**verified_by:** Risk-Floor Verifier  
**date:** 2026-06-20  

---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/humanin.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["CBC with differential (parenteral/baseline cancer screen)","relevant tumor markers (malignancy surveillance, personal-risk-based)","fasting glucose / HbA1c (metabolic axis — supported by §5.3 IFG biomarker data and §4 metabolic sections)"],"halt_reasons":[]}
```

---

## Prose Detail

### adverse_effects_literature — POPULATED

The research report explicitly states human safety is **"essentially uncharacterized"** because no human administration trial of exogenous humanin or any humanin analog has been published, completed, or registered in ClinicalTrials.gov as of mid-2026 (§7.3 / section-D D.3):

> "Direct human safety evidence: none. Because no human administration trials have been conducted, there are no published human adverse event data, no maximum tolerated dose, no NOAEL, and no human dose-response curve for exogenous humanin or HNG."

**Animal tolerability (short-duration):** Section 7.3 / D.3 documents that rodent studies at pharmacologically active doses have not reported overt dose-limiting toxicity in short-duration experiments. The critical gap is also explicitly stated: "Repeat-dose, genotoxicity, and carcinogenicity studies in animals are not represented in the peer-reviewed literature."

**The load-bearing anti-apoptotic → pro-tumor counter-signal** is documented in §7.4 / D.4 with two independent preclinical studies:
- TNBC (Moreno Ayala et al., *Sci Rep* 2020, PMID 32444831): exogenous humanin accelerated tumor growth, promoted spontaneous lung metastases, protected TNBC cells from doxorubicin-induced apoptosis, and impaired chemotherapy's anti-metastatic effect.
- GBM (Ha et al., *Cell Death Dis* 2024, PMID 38942749): humanin activated integrin αV–TGFβ signaling, drove invasion, angiogenesis, and shortened orthotopic xenograft survival.

The report correctly frames this as a mechanism-based risk, not a theoretical one: "The anti-apoptotic mechanism is not a theoretical concern — it is documented in two separate cancer models across two different tumor types and two different signaling pathways."

This field is populated by: (a) the honest "human-uncharacterized" statement, (b) documented animal short-duration tolerability with explicit gap notation (no repeat-dose/genotox/carcinogenicity), and (c) the mechanism-based pro-tumor counter-signal grounded in two cited preclinical studies.

---

### contraindications — POPULATED

Section 7.6 / D.6 lists the load-bearing contraindications under "Absolute contraindications (precautionary, based on mechanism and animal data)":

> - Active malignancy (any type) — anti-apoptotic mechanism demonstrated to protect tumor cells from chemotherapy and promote metastasis in TNBC [28/3, animal]
> - Personal history of cancer where recurrence risk is active — same mechanistic concern
> - Glioblastoma or other aggressive CNS tumors — humanin activates pro-invasive integrin αV–TGFβ signaling [29/4, animal]
> - Competitive athletes subject to WADA code — S0 prohibited substance

The pro-tumor basis is explicitly grounded. Two further relative contraindications are listed: first-degree family history of breast cancer or GBM, and any context where apoptosis suppression is clinically undesirable (e.g., active antitumor immunotherapy).

The report's bottom line (§9) reiterates: "Active or recent malignancy is a precautionary contraindication."

This is the load-bearing contraindication: **active malignancy OR personal history of cancer with active recurrence risk**, grounded in TNBC (PMID 32444831) and GBM (PMID 38942749) preclinical data demonstrating that humanin's anti-apoptotic mechanism protects malignant cells and promotes tumor progression.

---

### monitoring — POPULATED (≥1 named objective marker present)

Section 7.6 / D.6 states under "Monitoring (if used in research/experimental context)":

> - Baseline cancer screening (CBC with differential, relevant tumor markers based on personal risk) before initiation
> - Periodic screening maintained during any extended use
> - Oncology consultation if cancer history is present

**Named objective markers:**
- **CBC with differential** — a named objective laboratory assay, covering general parenteral safety and baseline oncologic screen
- **Relevant tumor markers based on personal risk** — named conceptually (personalized to risk profile), covering malignancy surveillance

The metabolic axis is separately supported throughout §4 (metabolic evidence) and §5.3 (IFG biomarker data: plasma humanin significantly lower in impaired fasting glucose participants, Voigt & Jelinek 2016, PMID 27173674), which supports **fasting glucose / HbA1c** as objective monitoring markers along humanin's documented metabolic axis. The wiki has existing biomarker pages for both (noted in the gate task brief). These are not stated verbatim in D.6 but are robustly supported by the report's metabolic sections.

The requirement for ≥1 named objective assay/measure is satisfied by CBC with differential.

---

### stopping_criteria — POPULATED

Section 7.6 / D.6 states:

> - Any new cancer diagnosis during administration — STOP immediately; alert treating oncologist to anti-apoptotic mechanism
> - Unexplained lymphadenopathy, weight loss, or constitutional symptoms — STOP and evaluate
> - Any regulatory change reclassifying humanin explicitly for compounding or prohibiting it under a new enforcement category

The honest caveat about the absence of validated efficacy/safety biomarkers for exogenous humanin is implicitly embedded throughout the document ("no human dose-response curve," "no NOAEL," "no published human adverse event data") and is the reason the stopping criteria are framed as mechanism-based precautions rather than clinical-trial-derived thresholds.

All four required fields are populated. Third-party monitoring markers are present (CBC with differential; malignancy surveillance markers; fasting glucose / HbA1c via the metabolic axis). Verdict: **PASS**.
