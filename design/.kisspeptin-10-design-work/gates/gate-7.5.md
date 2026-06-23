## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/kisspeptin-10.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["LH","FSH","total testosterone","free testosterone","estradiol"],"halt_reasons":[]}
```

## Prose Detail

### adverse_effects_literature — populated

Both source documents populate this field richly and honestly.

**Well-tolerated at academic doses (short exposure):** Section 4.3 of the research report states: "No serious adverse events have been attributed to KP-10 or KP-54 at study doses. Blood pressure, heart rate, and standard laboratory parameters remained stable across all reporting studies [9, 28, open_label]." The IVF safety record (n=60, Abbara et al. 2015) is cited: only 3/60 women (5%) developed mild early OHSS; zero moderate, severe, or critical OHSS; no participant required medical intervention. HSDD trials (n=32 men + n=32 women, Mills 2023, Thurston 2022): "No adverse effects reported in either crossover RCT."

**Honest limits / no long-term data:** Research report Section 4.3 states explicitly: "There are no long-term or chronic-dosing safety data in humans. Endocrine effects beyond the study window are not characterized." Studies are characterized as small (typically n=4–62), conducted in controlled research settings, and of short duration (hours to weeks).

**Documented DESENSITIZATION/HPG-suppression (tachyphylaxis; the core paradoxical-suppression risk):** Section 1.6 of the research report is titled "The Bolus-Stimulates / Continuous-Desensitizes Pharmacodynamic Dichotomy" and constitutes a primary caveat (Caveat 3). The desensitization mechanism is named directly: "KISS1R phosphorylation, β-arrestin recruitment, and clathrin-mediated receptor internalization." The human tachyphylaxis data are cited with specific numbers:

- Women with hypothalamic amenorrhea, twice-daily SC KP-54 for 14 days: "peak LH on Day 1 was 24.0 ± 3.5 IU/L and had fallen to 2.5 ± 2.2 IU/L by Day 14 — near-complete tachyphylaxis within two weeks [15, open_label]."
- Healthy men, higher IV bolus dose (3 µg/kg) produced blunted LH response vs. 1 µg/kg bolus: "an early signal of dose-dependent receptor saturation [9, open_label]."
- IV infusion in HA women at 1.0 nmol/kg/h: "LH secretion peaked at ~5 hours and then declined ~50% despite continued infusion [7, open_label]."

Section D.3 of section-D.md frames this explicitly as a clinical implication: "Pulsatile, lower-dose administration is the pharmacologically rational approach; continuous high-dose exposure risks converting a stimulatory agent into an HPG-suppressive one. The therapeutic window is narrow and context-dependent (gonadal steroid milieu, dose interval, cumulative exposure). This is not a theoretical risk — it is directly demonstrated in human subjects [3, 6, open_label]."

**Grey-market identity/purity risk + KP-10 vs. KP-54 confusion:** Section 5.2 of the research report covers this directly: "Research-chemical suppliers offer KP-10 as lyophilized powder with no independent quality oversight. Without verified mass spectrometry or HPLC documentation from a regulated facility, purity and sequence fidelity cannot be confirmed by the end user. The C-terminal amidation (–NH₂) required for receptor binding is frequently absent in low-quality syntheses, yielding a pharmacologically inactive preparation." The KP-10/KP-54 confusion is documented: "Consumer sources routinely conflate KP-10 and KP-54, which have meaningfully different circulating half-lives (~4 min vs. ~28 min), blood-brain barrier access profiles, and in vivo LH kinetics."

**Immunogenicity:** Section 4.3 documents the FDA PCAC's "theoretical immunogenicity risk via parenteral routes due to the peptide's structure, aggregation potential, and impurity profile in compounded preparations — a manufacturing-quality concern rather than an effect demonstrated in academic trials."

---

### contraindications — populated

Research report Section 4.3 states: "Contraindications (not formally established; no approved product): Hormone-sensitive conditions — hormone-receptor-positive malignancies, sex-steroid-dependent disorders, precocious puberty risk — are theoretical cautions given KP-10's capacity to raise LH, FSH, and gonadal steroids. Pregnancy warrants caution by mechanism (risk of premature LH surge, luteal disruption)."

Section D.4 of section-D.md mirrors this: "Hormone-sensitive conditions (hormone-receptor-positive malignancies, sex-steroid-dependent disorders, precocious puberty risk) are theoretical cautions given KP-10's capacity to raise LH, FSH, and downstream gonadal steroids. Pregnancy is a contraindication by mechanism (risk of LH surge triggering premature ovulation or luteal disruption)."

The HPG-axis-manipulation caution is embedded throughout — the desensitization risk with naive continuous use is documented as a contraindication class: the 503A denial and WADA S2.2.1 prohibition are cited in Section 4.4 (research report) and D.5 (section-D.md), grounding the regulatory caution.

---

### monitoring — populated (objective HPG-axis markers named)

Research report Section 4.6 provides a named monitoring table:

| Parameter | Rationale | Suggested timing |
|-----------|-----------|-----------------|
| Serum LH, FSH | Direct pharmacodynamic targets; confirm axis response or detect desensitization signal | Baseline + 30–60 min post-dose; at regular intervals during any multi-day protocol |
| Total and free testosterone (males) | Downstream endpoint; elevation confirms HPG engagement; suppression signals tachyphylaxis | Baseline; 24–48 h post-dose for bolus; end of infusion period |
| Estradiol (females) | Confirms ovarian response; required for IVF-trigger or HA-restoration context | Baseline; pre-trigger + 12–36 h post |
| Vitals (BP, HR) | Monitored in all academic trials; stable to date | Each administration visit |
| Injection-site assessment | Theoretical aggregation/immunogenicity concern at SC routes | Each SC administration |

Section D.6 of section-D.md reproduces the same table identically.

The objective markers are: LH, FSH, total testosterone, free testosterone, and estradiol — all named assays with explicit rationale and timing. The wiki biomarker pages noted in the task specification (total-testosterone, free-testosterone, estradiol, shbg) cover four of the five named objective markers.

---

### stopping_criteria — populated

Research report Section 4.6: "Stopping criteria framework: Unexpected LH/FSH suppression below baseline on repeat dosing (tachyphylaxis signal requiring dose interval reassessment); any systemic allergic or anaphylactoid response; unanticipated HPG stimulation in hormone-sensitive conditions."

Section D.6 of section-D.md: "Stopping criteria (framework): Unexpected LH/FSH suppression below baseline on repeat dosing (tachyphylaxis signal requiring dose interval reassessment); any systemic allergic or anaphylactoid response; unanticipated stimulation in hormone-sensitive conditions."

The tachyphylaxis/paradoxical-LH-decline criterion is explicitly present, which is the primary stopping trigger for naive grey-market HPG use. The criterion "no validated efficacy biomarker for the off-label libido/HPG use" is implicitly covered by the report's overall framing that all efficacy evidence was obtained under IV clinical supervision, not SC self-injection, and that no validated endpoint exists for consumer self-administration.

---

### third_party_monitoring_marker_present — true

Named objective assays: **LH, FSH, total testosterone, free testosterone, estradiol**. All are standard clinical laboratory assays available at third-party certified labs. Wiki biomarker pages exist for total testosterone, free testosterone, estradiol, and SHBG (per task specification).

---

### compound_risk_tier

Confirmed: `experimental` — no FDA-approved product, 503A pathway closed (PCAC October 2024), WADA S2.2.1-prohibited in males at all times, documented HPG-axis desensitization/suppression risk with continuous/naive dosing, no long-term safety data in humans, grey-market preparations only.
