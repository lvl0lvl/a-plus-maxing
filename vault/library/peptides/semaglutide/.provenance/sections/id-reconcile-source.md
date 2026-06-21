# Phase 4.25 — ID-RECONCILE verifier (Semaglutide)

Cross-section shared-entity consistency audit across sections A–F. Scope: detect cross-section disagreements only; content is not modified. A fact appearing in a single section is out of scope (not a mismatch). Special attention to (a) population conflation between the T2D and non-diabetic-obesity programs, and (b) dose/date mismatches.

## Citations (PMIDs / named trials appearing in >1 section)

Entities cross-checked for SAME author/year/journal/PMID across sections:

- **STEP-1 (Wilding)** — §B[4]: Wilding JPH et al., *N Engl J Med* 2021;384(11):989-1002, **PMID 33567185**. §F[7]: Wilding JPH et al., *N Engl J Med* 2021;384:989–1002 (same paper, no PMID printed but identical citation). **Agree.** Note: §D[4] cites a *distinct* paper — the STEP-1 trial *extension*, Wilding et al., *Diabetes, Obesity and Metabolism* 2022 (PMC9542252) — which is correctly differentiated as a separate publication, not a clashing duplicate of the same PMID. No mismatch.
- **SELECT (Lincoff)** — §C[1]: Lincoff AM et al., *NEJM* 2023, **PMID 37952131**, n=17,604, MACE 6.5% vs 8.0%, HR 0.80. §E[3]: SELECT, >17,600 participants, MACE 6.5% vs 8.0%. Author/year not re-stated in E but figures and trial identity agree. **Agree.**
- **SUSTAIN-6 (Marso)** — §C[2]: Marso SP et al., *NEJM* 2016, **PMID 27633186**, MACE HR 0.74; retinopathy HR 1.76. §D[2]: SUSTAIN-6 retinopathy 3.0% vs 1.8% (8.2% vs 5.2% in pre-existing). §E[1]: SUSTAIN-6 cited as basis for CV indication. Author/PMID stated only in C; D and E reference the same trial without contradiction. **Agree.**
- **FLOW (Perkovic)** — §C[3]: Perkovic V et al., *NEJM* 2024, **PMID 38785209**, HR 0.76, 1.0 mg, n=3,533. §E[1]: FLOW cited as basis for CKD indication. **Agree.**
- **FDA labels (Ozempic / Wegovy / Rybelsus)** — cited in A, D, E, F. Ozempic setid `adec4fd2-...` matches between §A[1] and §F[1]. Rybelsus setid `27f15fac-...` matches between §A[3] and §F[3]. Wegovy label cited in D, E, F (setid `ee06186f-...` in §F[2]; D/E cite DailyMed without setid — no conflict). **Agree.**

No citation maps to a different author/year/title/PMID across sections.

## Institutions / sponsor

Novo Nordisk named as developer/marketer/sponsor in §A, §C, §E (and implicitly the Wegovy/Ozempic/Rybelsus manufacturer in B/D/F). §C explicitly attributes SELECT, SUSTAIN-6, FLOW, ESSENCE, STEP-HFpEF to Novo Nordisk funding; §E names Novo Nordisk as authorization holder. Tirzepatide correctly attributed to **Eli Lilly** in §A and flagged as a *different drug* in §C (OSA/SURMOUNT-OSA) — no cross-attribution error. **Consistent.**

## Compound identifiers

- **Class / chemistry:** GLP-1 receptor agonist, acylated long-acting analogue, ~1-week (≈165 h) elimination half-life, >99% albumin-bound — §A (full mechanism) consistent with the once-weekly framing used in B/C/D/E/F.
- **Route/formulation split:** SC once-weekly = Ozempic (T2D) / Wegovy (obesity); oral once-daily = Rybelsus (T2D, SNAC-enabled). Stated identically in §A, §B, §C, §E, §F. **Agree.**
- **Doses:** Ozempic max **2 mg** weekly (§A, §E, §F); Wegovy maintenance **2.4 mg** weekly (§B, §C, §E, §F); Rybelsus max **14 mg** daily (§A, §B, §E, §F). Program-specific trial doses also internally consistent: SUSTAIN-6 0.5/1.0 mg, FLOW 1.0 mg, STEP/SELECT/ESSENCE/HFpEF 2.4 mg (§C), oral PIONEER 3/7/14 mg (§B/§F). **Agree — no dose mismatch.**

## Regulatory dates / facts

- **Approvals:** Ozempic 2017 (§E: Dec 5 2017), Rybelsus 2019 (§E: Sept 2019), Wegovy 2021 (§E: June 2021), Wegovy +CV indication 2024 (§E: Mar 8 2024). §A references the 2017/2019/2021 brand sequence consistently with §E. **Agree.**
- **WADA / sport:** semaglutide NOT prohibited (in or out of competition); GLP-1s reportedly added to the 2026 *Monitoring Program* (downgraded / reported-not-primary-verified, explicitly NOT a prohibition) — single-section fact (§E only). **Consistent** (no contradicting statement elsewhere).
- **Shortage resolution:** Feb 21 2025 declaratory order, with 503A wind-down ~Apr 22 2025 and 503B ~May 22 2025 — stated identically in §E[8] and §F[4]/[6]. **Agree** (this is the highest-risk cross-section date pair and it matches exactly).

## Trial registrations / efficacy figures + population labels

This is the integrity-critical class (population conflation between the T2D and non-diabetic-obesity programs).

- **STEP-1 efficacy:** −14.9% mean weight change, explicitly labeled **non-diabetic** overweight/obesity (§B[4]). §C, §D, §F reference STEP-1 only in non-diabetic-obesity context (SELECT contrast in C; body-composition/withdrawal in D; convention framing in F). No section attributes the −14.9% figure to a T2D population. **No conflation.**
- **STEP-2 vs STEP-1:** §B correctly separates STEP-2 (T2D obesity, −9.6%, same 2.4 mg dose) from STEP-1 (non-diabetic, −14.9%) and uses the gap to warn against cross-population generalization. **Consistent.**
- **SELECT vs SUSTAIN-6 (CV):** §C explicitly partitions SELECT (non-diabetic, BMI ≥27 + CVD, HR 0.80) from SUSTAIN-6 (T2D, HR 0.74) and from FLOW (T2D+CKD, HR 0.76). §E echoes the same partition (Wegovy CV indication is in a population *without* T2D, distinct from Ozempic's diabetes-tied CV indication). **Population labels agree across B/C/E — no conflation.**
- **MACE HR 0.80 / 6.5% vs 8.0%:** identical in §C[1] and §E[3]. **Agree.**
- **Safety numbers across C/D:** SUSTAIN-6 retinopathy presented as HR 1.76 in §C and as raw rates 3.0% vs 1.8% in §D — complementary, not contradictory (both attribute it to early rapid glycemic lowering, T2D population). GI rates, ~two-thirds regain on withdrawal, and the rodent-based thyroid boxed-warning framing are all internal to §D (and STEP-1-extension regain in §D is consistent with the "durability requires continuation" statement in §B[7]). **Consistent.**

No trial is mis-populationed; no efficacy figure from one program is applied to the other.

## Verdict

verdict: PASS

All shared entities appearing in more than one section agree. No cross-section citation, sponsor, identifier, dose, date, or population mismatch was found. The two highest-risk axes — population conflation (T2D vs non-diabetic obesity vs T2D+CKD) and the shortage-resolution / approval dates — are mutually consistent across all relevant sections.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":9,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":2,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":7,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":7,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
