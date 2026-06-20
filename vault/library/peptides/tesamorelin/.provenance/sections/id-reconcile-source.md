# Phase 4.25 — ID-RECONCILE (shared-entity cross-section consistency)

Compound: tesamorelin | Sections scanned: A, B, C, D, E, F
Role: detect cross-section disagreements only (no content fixes). A fact appearing in a single section is not a mismatch.

---

## Citations

Shared citations appearing in >1 section were checked for agreement on author / year / title / venue / identifier.

- **Falutz 2007, NEJM (PMID 18057338)** — appears in **B [1]** and **D [2]**. Both render it as Falutz J et al., *N Engl J Med* 2007;357(23):2359–2370, PMID 18057338, "Metabolic effects of a growth hormone-releasing factor in patients with HIV." Identical volume/issue/pages/year/PMID. (Section A does NOT cite this PMID directly — A's ref [2] is Bedimo 2011 — so A is not part of this triad; the prompt's "A/B/D" expectation resolves to B/D agreement, with A discussing the trial only via the Bedimo review.) **AGREE.**
- **Falutz 2010, JCEM pooled** — **B [2]** (PMID 20554713) and **D [3]** (DOI 10.1210/jc.2010-0490). Both: *J Clin Endocrinol Metab* 2010;95(9):4291–4304, pooled N=806 (543 tesa / 263 placebo). B supplies the PMID, D supplies the DOI — complementary, non-conflicting identifiers for the same article. **AGREE.**
- **Falutz 2010, JAIDS confirmatory (PMID 20101189)** — **B [3]** primary citation; **D [4]** (LiverTox) and **B [5]** (LiverTox) both reference PMID 20101189 as the confirmatory trial with documented VAT reversal on discontinuation. **AGREE.**
- **LiverTox NBK548730** — **B [5]** and **D [4]**. Same NCBI Bookshelf ID; both summarize the two Falutz pivotal trials + 2010 approval. **AGREE.**
- **FDA Egrifta label (across D/E/F + A/B):** the SV label setid **3d783378-b02d-4f19-99dd-0fc91a042224** is cited identically in **A [1], B [6], E [1], F [1]**. **D [1]** cites the **EGRIFTA WR** label, setid **839334d3-8c1d-4c26-9036-2ab524a6ea75** — a *different formulation's* label with its own correct, distinct setid. This is a deliberate, correct distinction (SV vs WR are separate FDA labels), not a mismatch: the SV setid is byte-identical everywhere SV is cited, and D is the safety section that legitimately anchors to the newest (WR) label. **AGREE (no setid collision/contradiction).**

scanned = 5 shared citation entities; mismatches = 0.

## Institutions / sponsors

- **Theratechnologies Inc. (Montréal)** — A, C, D (label holder), E, F. Consistently the developer/sponsor/license-holder (U.S. License No. 2091 in E). **AGREE.**
- **Falutz et al. (registrational investigators)** — A, B, C, D consistently identify Falutz as lead of the pivotal/registrational program. **AGREE.**
- **MGH / Grinspoon–Stanley lineage** — C (Stanley 2014/2019 beyond-label) and F ("MGH/Grinspoon") consistently attribute the beyond-label NAFLD/VAT work to this group. **AGREE.**
- **EMD Serono (original U.S. marketing partner)** — appears only in **E**. Single-section → not subject to cross-check.

scanned = 3 multi-section institutions/sponsors; mismatches = 0.

## Compound identifiers

- **Structure: full GHRH/GRF(1-44) + trans-3-hexenoyl (Tyr1) cap** — A (detailed), B (mech one-liner "GHRH/GRF[1-44]"), D/E/F ("synthetic analogue of GHRH"). No section contradicts the (1-44)+hexenoyl structure. **AGREE.**
- **Developmental code TH9507** — A, B [2] title, D [3] title. **AGREE.**
- **Brand names Egrifta / Egrifta SV / Egrifta WR** — A, D, E, F all enumerate the same three formulations in the same order/spelling; B references Egrifta SV. **AGREE.**
- **Half-life / molecular weight figures** — discussed only in A (t½ ~8 min healthy; MW ~5136 Da; formula C221H366N72O67S). No other section restates these → no cross-section conflict possible.

scanned = 3 multi-section compound identifiers; mismatches = 0.

## Regulatory dates / facts

- **FDA approval 2010** — A ("November 2010"), B [5], D ("2010 FDA approval"), E ("2010"; action Nov 10 2010 / announce Nov 11 2010). All consistent; E's specific Nov dates refine, do not contradict, the others. **AGREE.**
- **Egrifta SV reformulation 2019** — stated in E; referenced as a formulation in A/D/F. Only E asserts the 2019 date → no conflicting date elsewhere. **AGREE (no disagreement).**
- **Egrifta WR 2025** — E (March 25 2025); D cites the WR label; F lists the WR formulation. Only E asserts the date; no conflict. **AGREE.**
- **Approved-indication wording** ("reduction of excess abdominal fat in HIV-infected adult patients with lipodystrophy") — A, B [3], C, D, E (verbatim), F. Consistent wording and consistent scope-limitation (weight-neutral, not for weight loss) in B and E. **AGREE.**
- **EMA withdrawn (2011, Ferrer Internacional)** — only **E**. Single-section → not cross-checked.
- **WADA S2.2.4, prohibited at all times** — only **E**. Single-section → not cross-checked.
- **Dose figures (2 mg / 1.4 mg / 1.28 mg):**
  - **2 mg** (original) — A, B, C, D, E, F. **AGREE.**
  - **1.4 mg SV** — A, B [53] (bioequivalent to 2 mg), D ("1.4–2 mg"), E, F ("1.4 mg / 0.35 mL"). **AGREE.**
  - **1.28 mg WR** — stated only in **F** ("1.28 mg / 0.16 mL"). D gives the approved regimen as "1.4–2 mg" and omits 1.28 mg, but omission ≠ contradiction; F is the dosing-detail section and the only one asserting the WR mg figure. **AGREE (no disagreement).**

scanned = 6 multi-section regulatory facts/dose figures; mismatches = 0.

## Trial registrations / efficacy figures

- **VAT reduction LIPO-010: −15.2% vs +5.0%** — B [11] and D [2] restate identically. **AGREE.**
- **Pooled treatment effect −15.4% / −24 cm²** — B [29]; consistent with D's pooled framing. **AGREE.**
- **IGF-1 +81.0% (LIPO-010)** — B [12] and D [32]. **AGREE.**
- **IGF-1 +108 ± 112 ng/mL (pooled)** — B [30] and D [32]. **AGREE.** C's qualitative "~50–100%" is consistent with both.
- **Subcutaneous fat unchanged / weight-neutral** — B [32] and E (Limitations of Use). **AGREE.**
- **Pooled N=806 (543/263)** — B [27] and D [3]; D's "~806–816" range encompasses the 806 pooled count + extension and does not contradict it. **AGREE.**
- **Population annotation (HIV-associated lipodystrophy)** — consistently annotated as the efficacy population across A/B/C/D/E/F; beyond-label/off-label uses consistently demarcated in C/E/F. **AGREE.**
- **NCT registrations** — LIPO-010 NCT00123253 (B), extension NCT00608023 (B), cognition NCT02572323 (C), COPD NCT01388920 (C), China MASLD NCT07481734 (F). Each appears in a single section → no cross-section duplication to reconcile. No conflicting NCT-to-trial mapping found.

scanned = 7 multi-section efficacy/registration entities; mismatches = 0.

---

## Verdict

verdict: PASS

All shared entities appearing in more than one section agree on their cross-section identity. The only superficially "different" identifiers (the WR-vs-SV label setids in D vs A/B/E/F, and PMID-vs-DOI for the JCEM pooled paper) are correct, non-conflicting representations of distinct-but-related objects, not disagreements. No genuine cross-section mismatch detected.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":5,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":3,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":3,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":6,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":7,"mismatch_count":0,"mismatches":[]}},"iterations":1,"halt_reasons":[]}
```
