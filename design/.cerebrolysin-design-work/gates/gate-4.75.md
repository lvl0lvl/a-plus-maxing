# Gate 4.75 — Citation Integrity Verification
## Cerebrolysin | Deep Mode | Run: 2026-06-22

---

## IC-1 — Type-Tag Presence (inline citations)

**Procedure:** All inline citations of the form `[N, <tag>]` checked against the 12-enum:
`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`

**Sections scanned:** A, B, C, D, E

**Findings:**

All inline citation tags identified across all five sections are present in the canonical enum. Tags observed in use:
- `mechanism_review` — A: [1,8,9]; C: [1,2,3]
- `in_vitro` — A: [4,5,6,7,10,11,13,14]; D: [5]
- `animal` — A: [9,12]; C: [3,6,7]
- `meta_analysis` — A: [2]; B: [3,4,6,7,8,9,12]; C: [8,9,10]; D: [3,6,7,8]; E: [3,4,6,7,8]
- `rct` — B: [1,2,10,11]; C: [11,12]; E: [1,2,5]
- `cohort` — A: [3]; D: [9]
- `regulatory` — A: [15]; D: [1,2,4,11]; C: [4]
- `vendor_label` — A: [15]
- `anecdote_aggregate` — C: [5]; D: [4]; E: [9,10,11,12,13,14,15,16]

No unrecognized or missing tags detected.

**Status: PASS**

---

## IC-2 — Bibliography Type-Tag Presence

**Procedure:** Every bibliography entry must carry a `— tag: <tag>` annotation with a valid enum value.

**Section A:** All 15 entries carry valid tags. Entry [15] carries `vendor_label` — appropriate for manufacturer dossier.
**Section B:** All 12 entries carry valid tags.
**Section C:** All 12 entries carry valid tags. Entries [6] and [7] (retracted papers) carry `animal — tier: 5` — correct, retraction noted.
**Section D:** All 11 entries carry valid tags.
**Section E:** All 16 entries carry valid tags.

No missing or non-enum tags detected.

**Status: PASS**

---

## IC-3 — Vendor-Not-Numerical

**Procedure:** Find all `[N, vendor_label]` inline citations; check ±200 chars for numerical efficacy/AE/dose tokens.

**Identified vendor_label cites:**
- Section A, [15, vendor_label]: Used in sentences describing manufacturing process parameters (specific protease identities, ultrafiltration parameters, lot release criteria). The citation is in the context: "the specific protease identities and precise ultrafiltration parameters...are disclosed only in Ever Neuro Pharma's proprietary regulatory dossier (manufacturer product literature; not publicly available as of 2026) [15, vendor_label]." No numerical efficacy, AE rate, or therapeutic dose appears in ±200 chars of this citation.

No vendor_label cite appears near any numerical efficacy, AE, or dose claim.

**Status: PASS**

---

## IC-4 — Anecdote-Not-Numerical

**Procedure:** Find all `[N, anecdote_aggregate]` cites; check ±200 chars for numerical AE rates, dose recommendations, or effect sizes.

**Identified anecdote_aggregate cites and contexts:**
- Section C [5, anecdote_aggregate]: Piller/Science investigative report. Used to describe the NIH ORI misconduct dossier scope and Masliah-Moessler-EVER overlap. No numerical AE rate, dose, or effect size in proximity.
- Section D [4, anecdote_aggregate]: RealPeptides.co vendor blog. Used only to corroborate FDA non-approval status and grey-market context ("sold through some online vendors"). No numerical efficacy or dose claim.
- Section E [9,10,11,12,13,14,15,16, anecdote_aggregate]: Grey-market/community/manufacturer-overview sources. All used exclusively for qualitative context: market geography, sourcing channels, community-reported AE patterns (qualitative), authentication signals, prion community reasoning.
  - Section E [13, anecdote_aggregate] (RUPharma): "approximately USD 60 per pack (5–10 vials)" — a price figure, not an efficacy/AE/dose numerical claim. Does not trigger IC-4.
  - Section E [14, anecdote_aggregate]: "approximately 37% of grey-market peptide products... containing zero active ingredient." The text itself flags this figure as originating from a "source with a direct commercial interest" and cautions to "treat it as a qualitative hazard indicator, not an established rate." The citation carries explicit sourcing caveat language. This figure is a vendor-counterfeit-rate claim (not an efficacy rate, AE rate, or therapeutic dose); it is appropriately tagged anecdote_aggregate, is flagged inline as non-verified, and is not reproduced as a standing numerical claim. This is a borderline case but does not violate IC-4's scope (which covers AE rates, dose recommendations, and effect sizes — not vendor authentication statistics with explicit caveats).

No anecdote_aggregate cite grounds a numerical efficacy, AE rate, or therapeutic dose recommendation.

**Status: PASS**

---

## IC-5 — Practitioner-Protocol-Not-Efficacy

**Procedure:** Find each `[N, practitioner_protocol]` cite; verify no efficacy claim relies on it as sole source.

**Findings:** No `practitioner_protocol` tags appear in any of the five sections. The tag is absent from all bibliographies.

**Status: PASS** (not applicable — tag class absent)

---

## IC-6 — Compounding-Data-Sheet-with-Efficacy

**Procedure:** Find each `[N, compounding_data_sheet]` cite; flag efficacy claims citing it without an underlying primary.

**Findings:** No `compounding_data_sheet` tags appear in any of the five sections. The tag is absent from all bibliographies.

**Status: PASS** (not applicable — tag class absent)

---

## IC-7 — Population-Mismatch

**Per health-gates §1:** animal/in_vitro citations grounding numerical claims must carry `[population-mismatch: <species>]` inline unless the species is identified within 100 chars of the claim; and separately, the healthy-adult extrapolation gap from the disease-population evidence base must be surfaced.

### Part A — Animal/in_vitro inline population-mismatch tags

**Section A:** Animal/in_vitro citations used for mechanism claims; species called out inline:
- [10, in_vitro]: "purified mu- and m-calpain assays" — in vitro, no human subject. No numerical dose or efficacy claim; mechanism description only. Bibliography carries `[In vitro; purified mu- and m-calpain assays]`.
- [11, in_vitro]: "primary cultured chicken neurons" — bibliography annotates species.
- [12, animal]: "transgenic APP mice" — bibliography annotates species.
- [9, animal]: "transgenic APP/PS1 mouse; model: cholinergic deficit AD model" — annotated.

No numerical efficacy claims in Sections A, C, E are attributed to animal/in_vitro sources without species identification in bibliography.

### Part B — Healthy-adult population-mismatch callout (IC-7 critical requirement)

**Section D.2.1** carries an explicit block-quoted callout:

> "**Population mismatch — healthy adults:** All safety and tolerability data in this section derive from RCTs in **elderly disease populations** (acute ischemic stroke patients aged ~60–75 with high vascular comorbidity; dementia patients), administered Cerebrolysin IV in acute clinical settings under physician supervision. These populations differ fundamentally from the healthy-adult nootropic/grey-market users who constitute the wiki's primary audience. The extrapolation gap is unquantified: no controlled safety data exist in healthy adults."

**Section D.3.2** repeats the callout for the contraindications/monitoring subsection.

The wiki's primary audience is the healthy-adult enhancement user. The evidence base is entirely in elderly disease populations (stroke ~60–75, dementia). This gap is surfaced prominently, accurately, and at the head of the safety section.

**IC-7 population-mismatch population-level verdict:** The section is factually accurate — all efficacy and safety data are from elderly disease populations. The callout is explicit, prominent, and correctly characterizes the gap. The entire Section E.1/E.2 discussion reinforces this by documenting that no Western independent trial exists and that no controlled data in healthy adults is available.

**Mirrored into top-level `population_mismatch` JSON field:** verdcit PASS; the callout is present and accurate.

**Status: PASS**

---

## IC-8 — Route-Extrapolation

**Procedure:** Check dose claims for route mismatches between text and cited source; flag without `[route-extrapolation]` tag.

**Key route facts across sections:**
- Cerebrolysin is uniformly cited as **IV or IM** in all clinical trials (RCTs, Cochrane reviews, CASTA, CARS, CAPTAIN programs).
- Section A.1 states explicitly: "The preparation is supplied as a clear, amber, sterile injectable solution for **intravenous (IV) or intramuscular (IM) administration only**. It is not orally bioavailable."
- All dose numerical claims in clinical sections (B, C, D) cite RCT or Cochrane sources using IV administration. No oral route is presented for clinical doses.
- Section D notes grey-market IV/IM self-administration and its hazards — no dose numbers are cited from anecdote sources.
- Section E.4.1 documents community IV/IM use but explicitly states: "**No dose numbers from this source are endorsed or reproduced here.**"

No route-extrapolation occurs — all clinical numerical claims cite IV/IM trials and the preparation is correctly stated as parenterally administered only. No oral dose figures are present in the report.

**Status: PASS**

---

## IC-9 — Concentration-Surfacing

**Per health-gates §3:** if single-lab/sponsor share ≥ 70%, the draft must contain a first-class section surfacing concentration risk.

### Quantification of concentration

**Cochrane-set sponsor concentration (direct manufacturer support):**
- Cochrane acute stroke (Ziganshina 2023): 3 of 7 trials received direct manufacturer support = 43%
- Cochrane VaD (Cui 2019): 3-4 of 6 trials supported by pharmaceutical industry = 50-67%

**Broader pivotal trial/meta-analysis concentration (sponsor-funded OR key-author financial ties):**
- Section E.1.2 table: CARS (YES), CARS meta-analysis (YES), 9-RCT meta-analysis (YES), VaD Cochrane (Mixed), Stroke Cochrane (Mixed), CEREHETIS post-hoc (NO), GMERS 2025 meta-analysis (NO)
- Section E.1 narrative: "approximately 60–70% of the pivotal published evidence is manufacturer-sponsored or authored by investigators with documented Ever Neuro Pharma financial ties"

**Masliah/NIH misconduct deepening:** The author cluster producing the positive preclinical Cerebrolysin AD/tau literature includes an investigator (Masliah) found by NIH ORI to have fabricated data across 132 papers, 8 Cerebrolysin-specific. The Masliah-Moessler-EVER co-founder relationship adds a depth dimension to the concentration finding (documented in Sections C and E).

**Threshold assessment:**
- Direct Cochrane-set sponsor involvement: 43–67% (below the 70% single-lab strict threshold)
- Broader pivotal-literature concentration including financial-tie authors: ~60–70% (boundary)
- Qualitative: the positive preclinical AD literature is now substantially retracted from the Masliah cluster; the EVER Pharma-affiliated investigator network generates the majority of positive efficacy claims in the clinical literature

Per the task brief: "the Masliah/NIH-misconduct author-cluster deepening — confirm surfaced. ... set [threshold_triggered=]true" — the combination of the ~65% quantitative share plus the misconduct deepening justifies `threshold_triggered=true`.

### Surface verification

**Section E is entirely dedicated to concentration/commercialization:** E.1.1 names Ever Neuro Pharma's role; E.1.2 provides the quantified table; E.1.3 lists the recurring investigator network with named financial ties; E.1.4 summarizes the independent-evidence gap; E.2 covers geography concentration. The Masliah/misconduct deepening is documented in E.1.3.

**Section C.3** provides the "sponsor concentration and independent vs. affiliated evidence gap" analysis.

**Section B.6** provides the "load-bearing tension" table.

The concentration risk is surfaced as a first-class finding in multiple sections — not buried or minimized. The Cochrane authors themselves call it out directly (cited verbatim in E.1.2). This satisfies IC-9.

**Largest cluster:** "Ever-Pharma-sponsored/affiliated (incl. the Masliah misconduct cluster)" — share ~0.65 across pivotal evidence base.

**Status: PASS**

---

## IC-10 — No Fabricated Citations

**Procedure (deep mode):** Spot-check 6–8 PMIDs across all sections via NCBI eutils esummary/efetch; specifically re-verify the repaired Section D citation set and Rockenstein retraction PMIDs. Confirm each resolves to its stated authors/title.

### PMIDs verified via eutils esummary:

| PMID | Cited As | eutils Result | Match? |
|------|----------|---------------|--------|
| 38737662 | Seidl LF, Aigner L. "Comparing the biological activity and composition of Cerebrolysin with other peptide preparations." J Med Life 2024 | Title and authors confirmed: Seidl LF + Aigner L, J Med Life 2024 | YES |
| 34959697 | Strilciuc S et al. "Safety of Cerebrolysin... Twelve Randomized-Controlled Trials." Pharmaceuticals 2021 | Title confirmed; Strilciuc S first author; Pharmaceuticals (Basel) 2021 | YES |
| 22514795 | Thome J, Doppler E. "Safety profile of Cerebrolysin: clinical experience from dementia and stroke trials." Drugs Today 2012 | Title and authors confirmed; Drugs Today (Barc) 2012 | YES |
| 38249342 | Kalinin MN, Khasanova DR. "Heterogeneous treatment effects of Cerebrolysin as early add-on to reperfusion therapy: post hoc analysis of CEREHETIS trial." Front Pharmacol 2023 | Title and authors confirmed; Frontiers in Pharmacology 2023 | YES |
| 12655106 | Wells GAH et al. "Studies of the transmissibility of the agent of bovine spongiform encephalopathy to pigs." J Gen Virol 2003 | Title and authors confirmed; J Gen Virol 2003 | YES |
| 25047000 | Rockenstein E et al. "Cerebrolysin™ efficacy in a transgenic model of tauopathy: role in regulation of mitochondrial structure." BMC Neuroscience 2014 [RETRACTED] | Confirmed: BMC Neuroscience 2014; authors Rockenstein E, Ubhi K, Trejo M, Mante M, Patrick C, Adame A, Novak P, Jech M, Doppler E, Moessler H, Masliah E | YES |
| 41382024 | Retraction of Rockenstein 2014, BMC Neuroscience 2025 | Confirmed: "Retraction Note: Cerebrolysin™ efficacy in a transgenic model of tauopathy..." — same authors, BMC Neuroscience 2025. Confirmed retraction of PMID 25047000. | YES |
| 26611895 | Rockenstein E et al. "Neuroprotective effects of Cerebrolysin in triple repeat Tau transgenic model of Pick's disease." BMC Neuroscience 2015 [RETRACTED] | Confirmed: BMC Neuroscience 2015; authors Rockenstein E, Ubhi K, Mante M, Flojo J, Adame A, Winter S, Brandstaetter H, Meier D, Masliah E | YES |
| 40065222 | Retraction of Rockenstein 2015, BMC Neuroscience 2025 | Confirmed: "Retraction Note: Neuroprotective effects of Cerebrolysin in triple repeat Tau transgenic model..." — BMC Neuroscience 2025. Confirmed retraction of PMID 26611895. | YES |
| 22282884 | Heiss WD et al. (CASTA Investigators). "Cerebrolysin in patients with acute ischemic stroke in Asia." Stroke 2012 | Confirmed: Heiss WD, Brainin M, Bornstein NM, Tuomilehto J, Hong Z; Stroke 2012 | YES |
| 37818733 | Ziganshina LE et al. "Cerebrolysin for acute ischaemic stroke." Cochrane Database Syst Rev 2023 | Confirmed: Ziganshina LE, Abakumova T, Nurkhametova D, Ivanchenko K; Cochrane 2023 | YES |
| 22514792 | Masliah E, Díez-Tejedor E. "The pharmacology of neurotrophic treatment with Cerebrolysin." Drugs Today 2012 | Confirmed: Masliah E + Díez-Tejedor E; Drugs Today (Barc) 2012 | YES |

**All 12 PMIDs verified. No fabricated, misattributed, or misidentified citations detected.**

The two retraction PMIDs (41382024, 40065222) correctly identify as retraction notices for the two cited retracted papers (25047000, 26611895), confirming the retraction documentation in the text is accurate.

The Section D repair set (Seidl 38737662, Strilciuc 34959697, Thome 22514795, Kalinin 38249342, Wells 12655106) — the specific citations flagged by iter-2 as the repaired D set — all verify cleanly.

**Status: PASS**

---

## IC-11 — No Placeholder Strings

**Procedure:** Grep for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

**Scan result across all five sections:**

No instances of any prohibited placeholder string found. The draft uses phrases such as "research suggests" in zero instances; "experts believe" in zero instances. All claims are attributed to named sources with citations. No TBD or TODO markers appear in the five section files.

**Status: PASS**

---

## IC-12 — No Wikipedia/SCIRP/Predatory Citations

**Procedure:** Check for `wikipedia.org`, `scirp.org`, `cureus.com` (as citations), `for-better-science.com` (as citations), and other predatory/excluded sources in bibliographies.

**Scan result:**

- **Wikipedia:** No Wikipedia URLs appear in any bibliography across the five sections.
- **SCIRP:** No SCIRP citations present.
- **Cureus:** Section A Self-Check explicitly notes: "PMID 38524067 (Cureus, 2024) was identified from an initial search but **excluded** as Cureus is on the off-whitelist." Not cited in the bibliography.
- **for-better-science.com:** Section C Self-Check explicitly notes: "for-better-science.com excised entirely." Not cited in the bibliography.
- **Predatory/off-whitelist sources:** All off-whitelist sources (vendor blogs, community forums, grey-market channels) in Section E are correctly tagged `anecdote_aggregate` and carry no numerical efficacy, AE, or dose claims.
- **Longecity forum** (Section E [15]): Tagged `anecdote_aggregate — tier: 5`, cited only for qualitative community-level prion risk framing. Admissible under IC-12 — it is not Wikipedia/SCIRP/predatory, and it is correctly tagged.

**Status: PASS**

---

## IC-13 — Per-Citation Corpus Scoping

**Mode:** Deep — ≥80% sample of numerical/quoted claims, minimum 20 checks.

**Claims verified via eutils efetch (abstracts) or abstract-level search:**

| # | Claim | Cite | Verification Method | Result |
|---|-------|------|---------------------|--------|
| 1 | "638 unique peptides" identified from Cerebrolysin by Gevaert et al. | [4, in_vitro] PMID 26017115 | efetch abstract | CONFIRMED: "638 unique peptides" stated in abstract |
| 2 | "no peptide fragments corresponding to GDNF, NGF, BDNF, or CNTF were detected" | [4, in_vitro] PMID 26017115 | efetch abstract | CONFIRMED: abstract states "No fragments of known neurotrophic factors like GDNF, NGF, BDNF, and CNTF were found" |
| 3 | CASTA: 1,070 patients enrolled (529 Cerebrolysin, 541 placebo) | [1, rct] PMID 22282884 | efetch abstract | CONFIRMED: enrollment 1,070 (529/541) confirmed in abstract |
| 4 | CASTA: "confirmatory end point showed no significant difference" | [1, rct] PMID 22282884 | efetch abstract | CONFIRMED: abstract states "The confirmatory end point showed no significant difference between the treatment groups" |
| 5 | CASTA subgroup: "cumulative mortality by 90 days was 20.2% in the placebo and 10.5% in the Cerebrolysin group" | [1, rct] PMID 22282884 | efetch abstract | CONFIRMED: exact figures (20.2% vs 10.5%) confirmed in abstract |
| 6 | Cochrane 2023 stroke: 7 RCTs, 1,773 participants | [8/3, meta_analysis] PMID 37818733 | efetch abstract | CONFIRMED: "Seven RCTs (1773 participants)" in abstract |
| 7 | Non-fatal SAE: "RR 2.39 (95% CI 1.10–5.23); 3 trials, 1,335 participants; moderate-certainty evidence" | [8/3, meta_analysis] PMID 37818733 | efetch abstract | CONFIRMED: exact figures confirmed in Cochrane abstract |
| 8 | All-cause death: "RR 0.96 (95% CI 0.65–1.41)" | [8/3, meta_analysis] PMID 37818733 | efetch abstract | CONFIRMED: exact figures confirmed in abstract |
| 9 | Dose-response SAE: "RR 2.87 (95% CI 1.24–6.69); 2 trials, 1,189 participants" at 30 mL × 10-day dose | [8/3, meta_analysis] PMID 37818733 | efetch abstract | CONFIRMED: exact dose-response figures confirmed |
| 10 | VaD Cochrane: 6 RCTs, 597 participants | [9, meta_analysis] PMID 31710397 | efetch abstract | CONFIRMED: "six randomised controlled trials with a total of 597 participants" |
| 11 | VaD cognitive SMD 0.36 (95% CI 0.13–0.58) | [9, meta_analysis] PMID 31710397 | efetch abstract | CONFIRMED: "SMD 0.36 (95% CI 0.13 to 0.58)" in abstract |
| 12 | VaD global function RR 2.69 (95% CI 1.82–3.98) | [9, meta_analysis] PMID 31710397 | efetch abstract | CONFIRMED: "RR 2.69 (95% CI 1.82 to 3.98)" in abstract |
| 13 | VaD evidence: "very low-quality evidence" for all outcomes | [9, meta_analysis] PMID 31710397 | efetch abstract | CONFIRMED: "very low-quality evidence" stated for primary outcomes |
| 14 | Composition: "15% small peptides (< 10 kD) and 85% free amino acids" produced by "standardised enzymatic breakdown of lipid-free pig brain proteins" | [13, in_vitro] PMID 8901142 | efetch abstract | CONFIRMED: both composition ratio and enzymatic breakdown language confirmed verbatim in abstract |
| 15 | Wells/prion: incubation "69–150 weeks" via parenteral inoculation in pigs | [10, animal] PMID 12655106 | efetch abstract | CONFIRMED: "69-150 weeks" for parenteral route confirmed; pigs susceptible via parenteral, not oral |
| 16 | Strilciuc safety meta-analysis: 12 RCTs, n=2,202 | [6, meta_analysis] PMID 34959697 | eutils esummary + efetch abstract | CONFIRMED: "twelve randomized clinical trials, registering...2,202 patients" |
| 17 | 43.8% (Cerebrolysin) vs. 43.6% (placebo) overall AE rates; non-fatal SAE 3.8% vs. 3.0% | [6, meta_analysis] PMID 34959697 | efetch abstract | WARN [abstract-only verified: abstract does not report these exact percentages; confirms n=2,202, non-significant AE difference overall. Exact 43.8%/43.6% and 3.8%/3.0% figures are from full text, not abstract. Paywall/abstract-only — cannot confirm exact figures from abstract. Full-text access not available.] |
| 18 | Rockenstein 2014 retracted — "duplicated/manipulated figure panels" | [C-6] PMID 25047000 / retraction 41382024 | eutils esummary retraction notice | CONFIRMED: Retraction Note verified for PMID 25047000 |
| 19 | Rockenstein 2015 retracted — "image manipulation/figure integrity concerns" | [C-7] PMID 26611895 / retraction 40065222 | eutils esummary retraction notice | CONFIRMED: Retraction Note verified for PMID 26611895 |
| 20 | Seidl & Aigner 2024: other preparations "lack relevant biological activity" | [7/5, in_vitro] PMID 38737662 | eutils esummary (J Med Life 2024) | CONFIRMED to paper's existence and attribution; abstract-level claim consistent with compositional comparison study (comparative study, analytical); WARN [full text not accessible for verbatim quote check — paraphrase-level corpus-missing] |
| 21 | Kalinin & Khasanova: CEREHETIS trial, "no manufacturer funding declared" | [9, cohort] PMID 38249342 | eutils esummary (Front Pharmacol 2023) | CONFIRMED: paper exists; authorship confirmed. Funding statement is full-text content — abstract-only. WARN [corpus-missing for funding disclosure claim] |
| 22 | Masliah/Díez-Tejedor 2012: GSK-3β/tau-phosphorylation, neurogenesis, anti-apoptotic mechanisms | [8, mechanism_review] PMID 22514792 | eutils esummary confirmed | Confirmed authorship and journal; all specific mechanistic claims from this source are already marked "provisional" / "Masliah-authored; integrity caveat" inline. Abstract-only for numerical claims — but NO numerical claims (effect sizes, p-values) from this source appear in the report without being flagged as provisional. PASS at abstract-level. |

**Summary:**
- Claims checked: 22
- Confirmed (abstract or higher): 19
- WARN [abstract-only verified / corpus-missing]: 3 (items 17, 20, 21)
- HALT failures: 0

**Warn details:**
- Item 17 (43.8%/43.6% and 3.8%/3.0% from Strilciuc PMID 34959697): The overall non-significance of the difference is confirmed in the abstract; the exact percentage figures are full-text data. Paywall-disclosed → WARN, not HALT per IC-13 procedure.
- Item 20 (Seidl/Aigner verbatim quote): Paper confirmed to exist with correct attribution; compositional comparison framing consistent with claim; WARN for verbatim phrase not abstracted.
- Item 21 (Kalinin funding disclosure): Full-text funding statement — abstract-only. WARN, not HALT.

No `quote-not-found`, `number-not-found`, or `paraphrase-no-token-match` failures on any verifiable numerical claims.

**Status: WARN** (3 `corpus-missing` / abstract-only items; no HALT-class failures)

---

## Population-Mismatch (standalone audit)

**Conclusion:** The entire efficacy and safety evidence base for Cerebrolysin derives from elderly disease populations (acute ischemic stroke patients ~60–75 years, dementia patients, TBI patients) receiving IV/IM Cerebrolysin under clinical supervision. The wiki's target readership is healthy adults (nootropic/grey-market users).

**Gap characteristics:**
- No controlled safety or efficacy data in healthy adults exist anywhere in the literature
- The route (IV/IM injectable) is clinician-administered in all trials; grey-market self-injection adds contamination and administration risks not captured in trial data
- Age, comorbidity profile, and pharmacokinetics in healthy adults vs. elderly stroke/dementia patients are expected to differ substantially
- The extrapolation gap is explicitly surfaced in Section D (two callout boxes) and is described as "unquantified"

**Callout present in Section D:** YES — at D.2.1 and D.3.2, correctly labeled and prominently positioned before the safety data.
**Called out for WADA/anti-doping context:** Addressed in D.4.
**Surfaced in Section E:** E.4 (grey-market realism) acknowledges healthy-adult users explicitly.

**verdict:** PASS
**checked_citations:** All five sections reviewed
**flagged_citations:** 0 (gap is surfaced; no citation misattributes disease-population data to healthy adults without flagging)

---

## Concentration Audit (standalone audit)

**Largest cluster:** Ever-Pharma-sponsored/affiliated (including the Masliah NIH-ORI misconduct cluster)

**Quantified share:** ~0.65 (65%) of pivotal published evidence is manufacturer-sponsored or authored by investigators with documented financial ties to Ever Neuro Pharma

**Sub-breakdown:**
- Cochrane-confirmed direct sponsor involvement: 43% (stroke, 3/7) to 50–67% (VaD, 3–4/6)
- Broader financial-tie author cluster (CARS, CAPTAIN, CARS meta-analyses, 9-RCT meta-analysis): adds additional trial programs
- Masliah misconduct cluster: 8 Cerebrolysin-specific papers from NIH ORI finding; retracted Rockenstein cluster; Masliah-Moessler-EVER co-founder relationship

**Threshold triggered:** YES (qualitative + quantitative justification: ~65% by publication weight + misconduct deepening that compromises the AD/tau preclinical literature cluster)

**Surfaced in report:** YES — primary discussion in Sections B.6 (load-bearing tension table), C.3 (sponsor concentration analysis), E.1 (entire section dedicated to concentration/commercialization audit)

**verdict:** PASS
**total_primaries:** ~19 major trials/meta-analyses identified across the evidence base
**largest_cluster_name:** Ever-Pharma-sponsored/affiliated (incl. the Masliah misconduct cluster)
**largest_cluster_count:** ~12–13 of the pivotal publications
**share:** 0.65
**threshold_triggered:** true

---

## Verdict

verdict: PASS

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {
      "status": "PASS"
    },
    "IC-2": {
      "status": "PASS"
    },
    "IC-3": {
      "status": "PASS"
    },
    "IC-4": {
      "status": "PASS"
    },
    "IC-5": {
      "status": "PASS"
    },
    "IC-6": {
      "status": "PASS"
    },
    "IC-7": {
      "status": "PASS"
    },
    "IC-8": {
      "status": "PASS"
    },
    "IC-9": {
      "status": "PASS"
    },
    "IC-10": {
      "status": "PASS",
      "count_checked": 12,
      "count_flagged": 0,
      "findings": []
    },
    "IC-11": {
      "status": "PASS"
    },
    "IC-12": {
      "status": "PASS"
    },
    "IC-13": {
      "status": "WARN",
      "count_checked": 22,
      "count_flagged": 3,
      "findings": [
        "WARN [corpus-missing]: Strilciuc PMID 34959697 — exact AE percentages 43.8%/43.6% and SAE 3.8%/3.0% are full-text figures; abstract confirms non-significant overall difference but not the exact values. Paywall-disclosed.",
        "WARN [corpus-missing]: Seidl/Aigner PMID 38737662 — verbatim quote 'lack relevant biological activity' not confirmable from abstract alone; paper existence and attribution confirmed.",
        "WARN [corpus-missing]: Kalinin PMID 38249342 — 'no manufacturer funding declared' is full-text funding statement; paper exists with correct attribution."
      ]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 5,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 19,
    "largest_cluster_name": "Ever-Pharma-sponsored/affiliated (incl. the Masliah misconduct cluster)",
    "largest_cluster_count": 12,
    "share": 0.65,
    "threshold_triggered": true
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 22,
    "claims_failed": []
  },
  "halt_reasons": [],
  "warnings": [
    "IC-13: 3 corpus-missing items (full-text paywall; abstract-level PASS on numerical claims where verifiable)"
  ]
}
```

---

## Per-IC Summary

**IC-1 (Type-tag presence — inline):** All inline `[N, tag]` citations use valid enum tags. PASS.

**IC-2 (Bibliography type-tag presence):** All 66 bibliography entries across 5 sections carry valid `tag:` annotations. PASS.

**IC-3 (Vendor-not-numerical):** The single `vendor_label` citation ([A-15], manufacturer regulatory dossier) grounds only manufacturing process description (non-disclosed proteases, lot-release criteria) — no efficacy, AE rate, or dose number. PASS.

**IC-4 (Anecdote-not-numerical):** All `anecdote_aggregate` cites in Sections C, D, and E are used exclusively for qualitative framing (grey-market context, community AE patterns, market geography). A vendor authentication counterfeit-rate statistic (Section E [14]) is correctly flagged inline as a non-verified qualitative indicator from a commercially interested source; it is not presented as an established AE rate. PASS.

**IC-5 (Practitioner-protocol-not-efficacy):** Tag class entirely absent from report. PASS.

**IC-6 (Compounding-data-sheet-with-efficacy):** Tag class entirely absent from report. PASS.

**IC-7 (Population-mismatch):** Healthy-adult extrapolation gap explicitly surfaced in two prominent callout blocks in Section D; animal/in_vitro citations carry species annotations in bibliography. The critical finding that the entire evidence base is elderly disease populations (stroke ~60–75, dementia, TBI) — not healthy adults — is stated without minimization. PASS.

**IC-8 (Route-extrapolation):** Cerebrolysin is uniformly presented as IV/IM only; all clinical numerical claims cite IV-route trials; grey-market sources carry no dose numbers. No oral route presented for clinical doses. PASS.

**IC-9 (Concentration-surfacing):** ~65% of the pivotal evidence base is Ever-Pharma-sponsored or authored by investigators with documented financial ties. The Masliah NIH ORI misconduct cluster (132 papers, 8 Cerebrolysin-specific, 2025 retractions) deepens the concentration finding. Concentration is surfaced as a first-class structural concern across Sections B.6, C.3, and all of Section E. Threshold triggered by qualitative + quantitative combination. PASS.

**IC-10 (No fabricated citations):** 12 PMIDs verified via eutils esummary/efetch: all resolve to their stated authors, titles, journals, and years. The two retraction PMIDs (41382024, 40065222) confirmed as genuine retraction notices for the correct parent papers (25047000, 26611895). The repaired Section D citation set (Seidl 38737662, Strilciuc 34959697, Thome 22514795, Kalinin 38249342, Wells 12655106) all verified cleanly. No fabricated, misattributed, or misidentified citations found. PASS.

**IC-11 (No placeholder strings):** No prohibited placeholder strings found across any section. PASS.

**IC-12 (No Wikipedia/predatory):** No Wikipedia, SCIRP, or predatory citations in any bibliography. Cureus explicitly excluded (noted in Section A Self-Check). for-better-science.com explicitly excised (noted in Section C Self-Check). Off-whitelist sources correctly tagged anecdote_aggregate. PASS.

**IC-13 (Per-citation corpus scoping):** 22 numerical and quoted claims checked. 19 confirmed at abstract or higher. 3 WARN [corpus-missing] for full-text-only figures (Strilciuc exact AE percentages, Seidl verbatim phrase, Kalinin funding statement). Zero HALT-class failures (no quote-not-found or number-not-found on verified abstract-level claims). WARN.
