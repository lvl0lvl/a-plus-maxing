---
phase: "7.5"
compound: dihexa
compound_risk_tier: experimental
verified_by: RISK-FLOOR VERIFIER
verified_date: 2026-06-22
---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/dihexa.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["clinical oncologic surveillance (cancer screening — primary, given HGF/c-Met oncogenic mechanism)","hs-CRP (systemic inflammatory/proliferative surveillance)","ALT/AST (baseline hepatic function monitoring)","bilirubin (referenced alongside LFTs in research-report)"],"halt_reasons":[]}
```

---

## Prose Detail

### Source documents reviewed

1. `vault/library/peptides/dihexa/research-report.md` — full 416-line research report, Section 4 (Safety, Dosing, Route, Regulatory Status, Monitoring) at §4.1–§4.6.
2. `/tmp/aplus-research/dihexa/sections/section-D.md` — Section D specialist write-up (§D.1–§D.4).

---

### Field-by-field verification

#### adverse_effects_literature — POPULATED

Both source documents explicitly and prominently state the honest safety reality:

**No published human safety data of any kind exist.** Quoted directly from research-report §4.1:

> "Dihexa has no published human safety data of any kind. There is no Phase 1 dose-escalation study, no human pharmacokinetic profile, no characterised adverse-effect spectrum in people, and no chronic toxicity, reproductive toxicity, genotoxicity, or carcinogenicity dataset in any species."

Section D §D.1 repeats this verbatim in slightly different phrasing.

**The load-bearing theoretical oncogenic risk is stated prominently and precisely.** Section 3 of the research report (§3.1–§3.2) and Section D §D.1 both frame the HGF/c-Met-potentiation → theoretical oncogenic/tumor-promotion risk as the most significant safety concern:

> "Any person or clinician weighing self-administration of a systemically bioavailable, brain-penetrant c-Met potentiator must treat this as a theoretical but mechanistically grounded oncogenic risk with no empirical safety data to bound it."

The report correctly grounds this in established oncology pharmacology — capmatinib (NDA 213591, approved 2020) and tepotinib (NDA 214096, approved 2021) as FDA-approved c-Met INHIBITORS approved specifically to block this pathway in cancer — then inverts that framing to expose the theoretical risk of a chronic c-Met potentiator.

**No carcinogenicity study exists** — stated explicitly:

> "No carcinogenicity study — rodent long-term or otherwise — has been conducted for Dihexa. Absence of a carcinogenicity study is the normal state for an academic compound that never reached IND development; it does not imply the risk was assessed and found absent."

**Grey-market identity/purity hazard** is present in §4.3 (research-report) and §D.1 (section-D): chemical identity unverifiable, purity unverifiable, sterility risk for injectable forms, dose accuracy unverified.

**Dihexa-vs-fosgonimeton confusion** is explicitly addressed — §4.1 (research-report), §D.3 (section-D), and multiple times throughout both documents:

> "The critical distinction that neither framing acknowledges: Fosgonimeton is not Dihexa."

The retraction integrity story (Kawas 2012 retracted April 2025, Benoist 2014 retracted April 2025, McCoy 2013 under Expression of Concern since September 2021) is documented with PMIDs at each use.

---

#### contraindications — POPULATED

Research-report §4.6 and section-D §D.4 both enumerate the precautionary contraindication set:

- **Personal or family cancer history (especially c-Met-implicated cancers: lung, breast, hepatocellular, glioblastoma, gastric, pancreatic)** — grounded explicitly in the HGF/c-Met oncogenic precaution; described as "a hard stop" for a clinician.
- **Concurrent approved or investigational c-Met inhibitor use (capmatinib/tepotinib) — ABSOLUTE** — described as "direct pharmacodynamic opposition: one agent potentiates the c-Met receptor while the other suppresses it. The net effect is unknown and the combination is mechanistically irrational." Both research-report §4.2 and section-D §D.4 call this an absolute contraindication.
- **Immunocompromised individuals** — HGF/c-Met roles in immune cell migration; net effect in immunocompromised states unknown.
- **Pregnancy and lactation** — no safety data; contraindicated by default for any unregistered investigational compound.
- **Grey-market purity caution** — embedded in grey-market-specific risk section (§4.3/§D.1).
- **No-safety-data caution** — structurally present throughout; the entire monitoring and contraindications section opens with: "No validated contraindication list, monitoring protocol, or stopping criteria exist for Dihexa, because the compound has never been evaluated in humans."

---

#### monitoring — POPULATED

Research-report §4.6 monitoring posture block and section-D §D.4 both address monitoring. The sources correctly state there is no validated Dihexa-specific biomarker, and identify the following objective monitoring items:

**Primary — clinical oncologic surveillance** (named explicitly, grounded in the HGF/c-Met tumor-promotion theoretical risk):

Research-report §4.6:
> "Routine cancer surveillance appropriate to age and family history, with heightened attention to any unexplained mass, lymphadenopathy, systemic symptoms, or laboratory changes that might prompt earlier oncological evaluation."

Section-D §D.4:
> "Routine cancer surveillance appropriate to age and family history (not a Dihexa-specific interval — standard clinical guidelines)" + "Heightened attention to any unexplained mass, lymphadenopathy, systemic symptoms, or laboratory changes that might prompt earlier oncological evaluation."

**Objective blood markers named:**

- **[[biomarkers/hs-crp]] (hs-CRP)** — explicitly wiki-linked in research-report §4.6:
  > "hs-CRP provides an objective inflammatory surveillance marker useful in the context of chronic use of a compound whose mechanism involves receptor tyrosine kinase potentiation and whose carcinogenicity is unstudied. A rising hs-CRP trend during use — absent an intercurrent infection or other identifiable cause — warrants clinical evaluation."

- **ALT and AST (liver function tests)** — named explicitly in research-report §4.6 as "Liver function tests (ALT, AST, bilirubin): Baseline and periodic monitoring given c-Met's role in hepatocyte biology."

- Section-D §D.4 confirms: "Hepatic function monitoring (LFTs at baseline and periodically) given c-Met's role in hepatocyte biology and the use of hepatotoxic c-Met inhibitors as a comparator class."

**Honest caveat present:**

Research-report §4.6 opens: "No biomarker validated as a Dihexa-specific safety signal exists. There is no established therapeutic window, no validated pharmacodynamic marker for on-target effect in humans, and no surrogate endpoint for monitoring c-Met potentiation in a clinical context."

**Note — IGF-1 wiki link:** The research-report monitoring section does not include an explicit `[[biomarkers/igf-1]]` wiki link. hs-CRP, ALT, and AST are named and linked/referenced; IGF-1 is not named as a monitoring marker in this report. The oncologic surveillance + hs-CRP + ALT/AST triple is sufficient for the third-party-monitoring-marker gate (≥1 named objective assay), so this does not block PASS. If the wiki entry's monitoring field is expected to include IGF-1 as a growth-signaling-axis proxy, that addition should be made in the wiki compound page rather than the research report.

---

#### stopping_criteria — POPULATED

Research-report §4.6 (stopping criteria block) and section-D §D.4 both state:

> "Any signal of unexplained proliferative, haematological, or hepatic change that emerges temporally with use should prompt cessation pending evaluation. The compound should not be resumed without oncological clearance."

Section-D §D.4:
> "the reasonable stopping criterion is any signal of unexplained proliferative, haematological, or hepatic change that emerges temporally with use, pending evaluation."

The honest "no validated efficacy biomarker" framing is present throughout — the monitoring section explicitly states no surrogate endpoint exists, which is the absence-of-safety-data conservative stopping rationale.

WADA S0 prohibition stopping criterion is also named in §4.5 (research-report): "immediate cessation and NADO consultation" for athletes subject to anti-doping rules.

---

### c-Met oncogenic surveillance basis

The basis for making clinical oncologic surveillance the PRIMARY monitoring item (rather than a secondary adjunct) is clearly grounded in both source documents. The argument chain is:

1. Dihexa is proposed as an HGF/c-Met potentiator (even if the foundational mechanism papers are retracted, this is still the proposed mechanism and the live safety concern).
2. HGF/c-Met is a primary oncogenic driver across NSCLC, hepatocellular carcinoma, glioblastoma, gastric cancer, and others.
3. FDA approved capmatinib and tepotinib as selective c-Met INHIBITORS for cancer — pharmacological proof that chronic c-Met activation drives clinically significant malignancy.
4. No carcinogenicity study of any kind exists for Dihexa. Absence of a study ≠ absence of risk.
5. Rodent behavioral studies run 4–12 weeks are structurally incapable of detecting tumor promotion (latency typically months to years).
6. Therefore: the mechanistically appropriate surveillance posture centers on **clinical oncologic vigilance** — heightened cancer screening, prompt evaluation of any unexplained mass or systemic symptom — as the primary monitoring item.

Both source documents make this argument explicitly and prominently. The c-Met-oncogenic → clinical surveillance chain is load-bearing and is not buried.

---

### no-safety-data honesty

Both source documents exhibit the required honesty throughout:

- No Phase-1, no PK, no tox, no carcinogenicity study in any species stated flatly.
- The fosgonimeton/Dihexa confusion is explicitly quarantined — fosgonimeton's Phase 1 safety data cannot be attributed to Dihexa (different compound, different route, different pharmacokinetics).
- The 26-week LIFT-AD fosgonimeton trial is explicitly noted as insufficient to bound the tumor-promotion risk for chronic Dihexa use (different compound; trial not designed for oncologic endpoints; duration shorter than typical carcinogenicity latency).
- The monitoring section opens with "No biomarker validated as a Dihexa-specific safety signal exists" — not buried, first sentence.

---

### Summary of third-party monitoring markers confirmed present

| Marker | Type | Source location |
|--------|------|-----------------|
| Clinical oncologic surveillance (cancer screening, heightened vigilance for new/changing lesions) | Clinical — PRIMARY | research-report §4.6; section-D §D.4 |
| hs-CRP (systemic inflammatory/proliferative surveillance) | Objective blood assay | research-report §4.6 (wiki-linked `[[biomarkers/hs-crp]]`) |
| ALT (baseline hepatic) | Objective blood assay | research-report §4.6; section-D §D.4 |
| AST (baseline hepatic) | Objective blood assay | research-report §4.6; section-D §D.4 |

All four markers named; ≥1 objective assay present — third-party-monitoring-marker gate PASSES.

---

### Open item (not a halt condition)

IGF-1 is not named as a monitoring marker in the current research-report or section-D. Given the growth-signaling-axis rationale for including it, this is worth considering for addition to the wiki compound page's monitoring field, but it does not affect the gate verdict — the existing named markers (oncologic surveillance + hs-CRP + ALT/AST) satisfy the gate requirement.
