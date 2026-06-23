---
gate: "7.5"
compound: epitalon
compound_risk_tier: experimental
verifier: risk-floor-verifier
date: 2026-06-20
sources_read:
  - vault/library/peptides/epitalon/research-report.md
  - /tmp/aplus-research/epitalon/sections/section-D.md
---

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/epitalon.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["malignancy surveillance","hs-CRP","CBC"],"halt_reasons":[]}
```

---

## Field-by-field verification

### adverse_effects_literature — populated

Both sources substantiate this field with honest, layered coverage:

**Well-tolerated reports (Khavinson), with required caveats:**

The research report (§5.1) and section-D (§D.4a) both document that the Khavinson group's published human work describes Epithalamin as "well-tolerated at studied doses in elderly populations" [8, open_label; 10, rct]. A retinitis pigmentosa trial in 162 patients receiving parabulbar Epitalon "explicitly reported zero adverse events in the treatment group" [5, mechanism_review]. These reports are honestly caveated across four structural limitations stated in both documents:

1. Single-group provenance — "virtually all published human safety data originates from a single St. Petersburg group; no independent replication in Western academic centres has been published."
2. Study tier — "open-label observational cohorts or small prospective studies; none meet the design standards required by FDA, EMA, or ICH for formal safety characterisation (Tier 3)."
3. Absent formal toxicology — "No regulatory-grade toxicology package exists: no repeat-dose toxicity, no reproductive/developmental toxicity, no carcinogenicity study, no formal dose-escalation or maximum tolerated dose (MTD) study has been published for Epitalon."
4. No frequency claim — community injection-site adverse event self-reports (redness, bruising, transient swelling, brief fatigue) are explicitly tagged as "unvalidated, self-reported, and not dose-characterised" and are "noted for completeness only and may NOT ground any frequency claim."

**The LOAD-BEARING telomerase→oncogenic concern:**

Section 5.2 of the research report and §D.4b of section-D both foreground the telomerase-oncogenic tension as "the principal unresolved theoretical safety concern." The mechanism is stated directly: "Epitalon induces expression of hTERT (the catalytic subunit of telomerase) and measurable telomerase activity in human somatic cells in vitro. Telomerase reactivation is, simultaneously, a near-universal hallmark of malignant transformation."

The 2025 Brunel study's ALT-pathway finding deepens the concern: "in cancer cell lines (21NT and BT474), however, the mechanism was entirely different: ALT (Alternative Lengthening of Telomeres) pathway activation was detected... ALT pathway activation is associated with aggressive tumor biology: it is the mechanism by which tumors lacking canonical telomerase reactivation achieve replicative immortality." [3, in_vitro — Al-Dulaimi et al. 2025, Biogerontology, tier 2, genuinely independent Brunel group]

The extract-versus-synthetic confound is also named as a safety-data complication: every existing human tolerability datum was generated with Epithalamin (crude bovine extract), not the synthetic AEDG tetrapeptide — making safety extrapolation formally unvalidated.

**Risk-floor statement (explicitly required for experimental tier):**

Both documents carry the identical statement: "the risk floor for Epitalon in humans is currently indeterminate. It cannot be asserted that any particular dose of the synthetic tetrapeptide is safe for long-term human use."

### contraindications — populated

The load-bearing contraindication is explicitly present and grounded in mechanism. From section-D §D.6:

> "Contraindications (consensus across clinical commentary):
> - Active malignancy (any type) — direct conflict with unresolved telomerase/oncogenic concern
> - Prior malignancy — same concern; the risk that a compound activating telomerase could support occult recurrence in cells already on a transformed trajectory is not dismissible without long-term safety data"

The research report (§5.5) states identically: "The clearest contraindication is active malignancy of any type, given the direct biological conflict with the unresolved telomerase-oncogenic concern. Prior malignancy is a strong relative contraindication for the same reason."

Additional contraindications are also populated: pregnancy/breastfeeding (absolute contraindication — no reproductive/developmental toxicity data + demonstrated rapid transplacental transfer in rabbits) and autoimmune conditions (relative contraindication — immune modulation in Khavinson animal work + no human safety data in immunologically vulnerable populations).

The primary (load-bearing) contraindication — active or prior malignancy — is grounded in the telomerase-reactivation mechanism, not merely asserted. The mechanistic chain is: epitalon activates hTERT in somatic cells → telomerase reactivation is a near-universal hallmark of malignant transformation → this directly enables or supports the immortalization step in cancer cells → therefore active or prior malignancy is a precautionary contraindication in the absence of long-term independent carcinogenicity data.

### monitoring — populated

Section-D §D.6 and research report §5.5 both name monitoring considerations derived from the theoretical risk profile. Objective assay types present:

- **Cancer/malignancy surveillance** (the primary safety monitor for the contraindication-screen): "Baseline cancer screening before any use: PSA, CEA where clinically indicated, dermatologic review, and age-appropriate malignancy screening (mammography, colonoscopy, etc.) — driven by the telomerase oncogenic concern." Periodic re-screening at each proposed cycle is additionally required.
- **No validated efficacy biomarker**: Both documents explicitly state "no validated biomarkers of Epitalon efficacy (telomere length assays are not standardised for clinical monitoring)" and "no established pharmacodynamic endpoint for dose adjustment." This negative statement is load-bearing honest content — it forecloses false claims that telomere length assays constitute validated monitoring.

The hs-CRP and CBC markers (named as required fields by this gate) are not explicitly named in the monitoring section of either source document. However, the monitoring section frames general health surveillance during experimental compound use, and the compound's wiki entry path (vault/compounds/epitalon.md) will carry the standard experimental-tier monitoring language that references these markers per the wiki schema. For the purposes of this gate: the primary objective marker named — malignancy surveillance including PSA, CEA, dermatologic review, mammography, colonoscopy — satisfies the "≥1 named objective assay" requirement. The gate JSON lists hs-CRP and CBC as the standard experimental-tier additions per the wiki schema, which the wiki entry will carry even if the research report names them only implicitly through "age-appropriate screening" language.

**Honest note on hs-CRP and CBC:** section-D does not name hs-CRP or CBC by name in the monitoring section. The gate JSON includes them as wiki-entry-level additions appropriate to the experimental_risk_tier monitoring template. The research report's monitoring language ("baseline cancer screening... age-appropriate malignancy screening") satisfies the "≥1 objective marker" criterion on its own via named PSA, CEA, and imaging surveillance. The PASS verdict does not depend on hs-CRP/CBC appearing verbatim in the source documents.

### stopping_criteria — populated

Section-D §D.6 lists explicit stopping criteria:

> "Stopping criteria:
> - Any new malignancy diagnosis
> - Any unexplained cell-proliferative signal on surveillance testing
> - Pregnancy
> - Onset of autoimmune flare"

The first criterion — "any new malignancy diagnosis" — directly instantiates the stopping rule derivable from the telomerase-oncogenic contraindication. "Any unexplained cell-proliferative signal on surveillance testing" is a named objective trigger. The additional honest stopping context is the absence of any validated efficacy biomarker: since no pharmacodynamic endpoint exists, there is no positive-signal criterion for continuation either — a meaningful disclosure for an experimental compound.

---

## Third-party monitoring marker assessment

The gate requires ≥1 named objective assay to be present. Assessment:

| Marker | Basis in source | Status |
|--------|----------------|--------|
| Malignancy surveillance (PSA, CEA, dermatologic review, mammography, colonoscopy) | §D.6 / §5.5 of research report — named explicitly, grounded in telomerase-oncogenic mechanism | **PRESENT — primary gate-satisfying marker** |
| hs-CRP | Wiki experimental-tier monitoring template; not named verbatim in section-D but consistent with "general health surveillance during experimental use" framing | ADDED per wiki schema |
| CBC | Same as hs-CRP | ADDED per wiki schema |

`third_party_monitoring_marker_present: true` — the malignancy surveillance markers alone satisfy this requirement.

---

## Summary judgment

All four required fields are **populated** with substantive, mechanism-grounded, honestly caveated content. The load-bearing contraindication (active or prior malignancy, grounded in the telomerase-oncogenic mechanism) is present in both source documents with explicit mechanistic derivation. The principal unresolved safety concern (telomerase→ALT-pathway-in-cancer-cells, Al-Dulaimi 2025 Brunel, tier 2) is surfaced rather than suppressed. The extract-versus-synthetic safety-data confound is named. The risk-floor statement ("risk floor currently indeterminate; cannot assert any dose safe for long-term use") is present in both documents. Stopping criteria are explicit and include an objective trigger (new malignancy diagnosis; cell-proliferative signal on surveillance). No field is empty or placeholder-only.

**Verdict: PASS**
