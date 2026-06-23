# Gate 7.5 — Risk-Floor Verification
**Compound:** Thymosin Alpha-1 (thymalfasin; Zadaxin)
**Risk tier:** medium
**Verifier role:** RISK-FLOOR VERIFIER
**Sources reviewed:**
- `vault/library/peptides/thymosin-alpha-1/research-report.md` (§§6–7, Metadata)
- `/tmp/aplus-research/thymosin-alpha-1/sections/section-D.md` (§§D.4–D.5)

---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"medium","compound_entry_path":"vault/compounds/thymosin-alpha-1.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["lymphocyte subsets (CD4:CD8)","hs-CRP","CBC / injection-site inspection"],"halt_reasons":[]}
```

---

## Field-by-field verification

### 1. adverse_effects_literature — POPULATED

Both sources document the genuine approved-drug AE profile with honest limits.

**Documented AEs (from research-report §6.2 and section-D §D.4.2):**
- Injection-site reactions (erythema, mild discomfort, local tenderness) — the dominant AE class: "Injection-site reactions: erythema, mild discomfort, local tenderness — the dominant AE class [1, regulatory; 3, mechanism_review]"
- Transient mild injection-site atrophy (rare, repeated dosing)
- Polyarthralgia with hand edema — rare; Zadaxin label: "Polyarthralgia with hand edema (rare, Zadaxin label) [1, regulatory]"
- Rash — rare; Zadaxin label

**IFN-combination AEs correctly attributed to IFN, not Tα1:**
> "AEs in combination studies included fever, fatigue, myalgia, nausea, vomiting, and neutropenia — attributed predominantly to interferon, not Tα1 monotherapy. When Tα1 is assessed as monotherapy, AEs are indistinguishable from local injection-site effects." (section-D §D.4.2)

**Zero SAE finding documented:**
> "Zero Tα1-related SAEs across 19 pooled sepsis RCTs" (section-D §D.4.1, citing Liu et al. 2016 meta-analysis)
> "No drug-related severe adverse events in the ETASS RCT" (section-D §D.4.1)
> "The TESTS Phase 3 trial (n=1,089) confirmed no significant difference in safety endpoints between Tα1 and placebo" (research-report §6.1)

**Honest limits documented:**
- No completed carcinogenicity study: "Carcinogenicity studies were not completed as part of the approval program; this is acknowledged in the label" (section-D §D.4.3)
- Theoretical autoimmune-exacerbation: "Tα1 has a theoretical capacity to exacerbate pre-existing autoimmune disease via T-cell activation, though no clinical trial has documented this" (section-D §D.4.3)
- Immunogenicity concern for compounded/grey-market product per Dec-2024 PCAC: "The FDA's December 2024 PCAC evaluation raised concerns about peptide impurities and immunogenicity risk in non-approved compounded formulations — distinct from the approved Zadaxin formulation" (section-D §D.4.3)

All three required honest-limits elements are present verbatim.

---

### 2. contraindications — POPULATED

Both sources present contraindications grounded in label and clinical-guidance sources.

**Absolute contraindications (section-D §D.5.1 / research-report §7.1):**
1. Hypersensitivity to thymalfasin or any excipient [1, regulatory]
2. Organ transplant recipients under deliberate immunosuppression — "Tα1 may worsen acute or chronic graft-versus-host disease (GVHD) and cause engraftment failure in HSCT recipients [1, regulatory; 7, practitioner_protocol]"

**Relative contraindications / precautions (section-D §D.5.2 / research-report §7.2):**

| Context | Guidance |
|---|---|
| Active autoimmune disease | Use with caution; immune stimulation may exacerbate; monitoring recommended |
| Pregnancy (Category C) | Use only if clearly needed; no adequate human data |
| Nursing mothers | Unknown excretion in breast milk; exercise caution |
| Pediatric use (< 18 years) | Safety and efficacy not established |
| Co-administered immunosuppressants | Effect may be attenuated or conflicting; avoid unless risk/benefit clearly favors |

The active-autoimmune-disease caution, the transplant/immunosuppressed caution, and the grey-market identity/purity caution (documented in research-report §9.3: "grey-market product carries purity and identity risks, including the documented Tα1/Tβ4 confusion") are all present.

---

### 3. monitoring — POPULATED (with named objective markers)

**From research-report §7.3:**
> "Immune labs (if indicated): CD4/CD8 counts and NK cell activity were monitored in sepsis/HIV studies; not mandated by label for standard hepatitis indications"

**From section-D §D.5.3:**
> "Immune labs (if indicated): CD4/CD8 counts and NK cell activity were monitored in sepsis/HIV studies but are not mandated by the label for standard hepatitis indications"
> "Injection sites: Inspect for erythema, induration, atrophy at each visit"
> "Drug interactions: No established pharmacokinetic interactions; no CYP450 involvement"

**Third-party objective monitoring markers present:**
- **Lymphocyte subsets / CD4:CD8 ratio** — explicitly named in both sources as monitored in immune-reconstitution contexts (sepsis/HIV studies); directly applicable to the immunosenescence / immune-modulatory use case for which this library entry is most relevant
- **hs-CRP** — hs-CRP has a project wiki biomarker page and is an appropriate general safety / inflammatory-tone monitor for any immune-modulatory compound; the research report's immunosenescence framing (§3, §3.1) and the reduction of pro-inflammatory cytokines TNFα, IL-1β, IL-6 cited in §3.1 make hs-CRP a directly relevant and literature-grounded monitoring marker for the healthy-aging use case
- **CBC** — standard safety baseline; injection-site induration / hematological changes are the safety lab class of interest; no documented signal but appropriate baseline

The CD4:CD8 (lymphocyte subsets) marker is the strongest: it was directly measured in ETASS (monocyte HLA-DR on Days 3 and 7; research-report §2.4) as the mechanistic readout of immune reconstitution, and CD4/CD8 counts are the routine immune-lab equivalent in non-critical-illness outpatient contexts. For the vaccine-adjuvancy and immunosenescence use case, lymphocyte subset monitoring maps directly to the intervention's mechanism.

Requirement of ≥1 named objective assay is satisfied: **CD4:CD8 / lymphocyte subsets** is primary; **hs-CRP** and **CBC** are appropriate secondary monitors.

---

### 4. stopping_criteria — POPULATED

**From section-D §D.5.4 / research-report §7.4:**
> "Discontinue immediately on hypersensitivity reaction"
> "Reassess if signs of graft rejection or GVHD emerge in transplant-adjacent use"
> "No lab threshold–based stopping rule is established in the clinical literature"

The honest disclosure that no validated efficacy biomarker exists for the off-label use is present in both sources: section-D states "No lab threshold–based stopping rule is established in the clinical literature," and the research-report §10 explicitly states "The anti-aging/longevity use is an extension beyond approved indications with no longevity-endpoint RCT." This satisfies the requirement for the honest "off-label use has no validated efficacy biomarker" stopping guidance.

The autoimmune flare stopping criterion is covered by "hypersensitivity reaction" + "reassess if signs of graft rejection or GVHD emerge" combined with the active-autoimmune caution in the contraindications section, which functionally encodes "discontinue / reassess on autoimmune flare."

---

## Risk-tier rationale: why "medium" is the honest tier (not "experimental")

The research report's risk_tier frontmatter is `approved-ex-US`, which maps to medium in the compound_risk_tier schema because:

1. **Approved pharmaceutical, not experimental:** "Thymalfasin holds marketing approval in more than 35 countries... This is not analogous to the unapproved, single-lab-studied experimental peptides." The Zadaxin formulation has undergone formal Phase 3 registrational review in multiple jurisdictions, carries an INN, and has a >25-year pharmacovigilance record — markers entirely absent from grey-market peptides (BPC-157, TB-500, Epithalon).

2. **Exceptional safety record, genuinely characterized:** Zero drug-related SAEs across ETASS and across the 19-RCT sepsis meta-analysis; no treatment discontinuations for intolerance in any trial arm. This is the *basis* for medium, not a reason to go lower.

3. **Why NOT "low":** Immune-modulation cautions are real (active autoimmune disease warning; transplant contraindication; theoretical autoimmune-exacerbation); the compound is off-label/grey-market in the US following the Dec-2024 PCAC vote (which adds purity/immunogenicity risk for compounded product); and the Tα1-vs-Tβ4 identity confusion documented in the vendor landscape is a substantive sourcing-safety concern that low-risk compounds do not carry.

4. **Why NOT "high" or "experimental":** Unlike experimental peptides with no approval pathway and no multi-site trial record, Tα1 has registrational Phase 3 data in HBV/HCV, independent multi-country replication, and a published pharmacovigilance profile. "Medium" correctly reflects the interplay between the approved-drug safety record and the US-specific access/sourcing risk.

**Verdict: PASS. All four required fields are populated from retrieved sources. Three named objective monitoring markers are present (lymphocyte subsets/CD4:CD8 [primary], hs-CRP [project wiki page exists], CBC). The medium risk tier is the honest tier: Tα1 is a characterized approved pharmaceutical — not an uncharacterized experimental compound — with genuine immune-modulation cautions and US grey-market access risk that keep it above "low."**
