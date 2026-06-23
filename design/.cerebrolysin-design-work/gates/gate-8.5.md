## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/cerebrolysin/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/cerebrolysin/non-english-layer.md","present":true,"languages_surveyed":["Russian","Chinese","German"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

---

## Practitioner Layer — Detailed Verification

**File:** `vault/library/peptides/cerebrolysin/practitioner-layer.md`
**Present:** YES
**`## Bibliography`:** YES (present; 15 numbered entries, lines 279–342)
**`## Self-Check`:** YES (section present, lines 313–343)

### Data-sheet gate finding
The dedicated section "Compounding Status / Data-Sheet Gate Finding" explicitly states: "Gate finding: NO compounding data sheet — Cerebrolysin is a finished manufactured biologic." Four structural reasons for non-compoundability are documented (complex biologic hydrolysate, not a defined chemical entity; not a 503A candidate; no US compounder identified; no FDA-approved form). The EVER Neuro Pharma SmPC / product information is identified as the functional data-sheet equivalent [reference 3, regulatory]. Grey-market vendors (RUPharma.com, CosmicNootropic.com, Limitless Life Nootropics) are listed explicitly in the Grey-Market Vendors table. `compounding_sheets_count: 0` — correctly reflects "by design, not by omission."

### ~50-country approved pathway (labeled posology)
YES. Section "Approved Prescribing: National Registrations (~50 Countries)" (lines 17–57) documents the EVER Neuro Pharma product, the approved jurisdictions (Russia, China, South Korea, Austria, Romania, Bulgaria, Hungary, Czech Republic, Slovakia, Ukraine, Kazakhstan, Uzbekistan, Georgia, Vietnam, and others), the four approved indications (ischemic stroke, TBI, vascular dementia, Alzheimer's disease), and the labeled dosing regimens in a full posology table (IV/IM routes, dose ranges, course durations, monitoring settings). The posology is tagged `[3, regulatory]` and `[4, regulatory]` throughout.

### NOT FDA / NOT EMA-centrally-authorized
YES. Explicitly stated in the introductory regulatory state block: "It is NOT FDA-approved and NOT EMA-centrally-authorized." Repeated in the approved jurisdictions section and in the self-check.

### Independent-null: CASTA + 2023 Cochrane SAE signal
YES. CASTA (PMID 22282884; n=1,070; 14-country Asian trial) documented in full: null on pre-specified primary composite endpoint (mRS + BI + NIHSS global directional test); post-hoc NIHSS subgroup signal labeled hypothesis-generating only. 2023 Cochrane review (PMID 37818733; 7 RCTs, n=1,773) documented: all-cause mortality RR 0.96 (no benefit); non-fatal SAEs RR 2.39 (95% CI 1.10–5.23; moderate-certainty; statistically significant increase); at labeled 30 mL/10-day dose: RR 2.87 (95% CI 1.24–6.69). The discrepancy with the Strilciuc 2021 meta-analysis (PMID 34959697; RR 1.18 non-significant) is documented transparently as unresolved, with the Cochrane methodology weighted more heavily.

### Two integrity axes
YES. Both axes present:
- **Axis 1 (Masliah/NIH misconduct):** NIH ORI finding of "falsification and/or fabrication involving re-use and relabel of figure panels" against Eliezer Masliah; ~132 papers flagged; 8 specifically concern Cerebrolysin; Herbert Mössler (EVER Pharma GM) co-authored 57 Cerebrolysin papers and co-founded Neuropore Therapies with Masliah. Two confirmed retractions documented: Rockenstein et al. BMC Neurosci 2015 (PMID 26611895; retracted March 2025, retraction PMID 40065222); Rockenstein et al. BMC Neurosci 2014 (PMID 25047000; retracted December 2025, retraction DOI 10.1186/s12868-025-00985-1). Impact scoped correctly: retracted papers compromise AD/tau mechanism narrative; clinical RCT evidence is structurally distinct.
- **Axis 2 (Sharma/Muresanu high-volume industry-linked publications):** Hari Shanker Sharma and Aruna Sharma — 39 Cerebrolysin papers; 25 flagged on PubPeer; 5 retractions; entire Springer volume retracted. Dafin Muresanu — 60 Cerebrolysin papers since 2008 while serving as journal editor.

### Healthy-adult population mismatch
YES. Explicit and unqualified: "ALL efficacy and safety data for Cerebrolysin comes from disease populations." CASTA trial required acute ischemic stroke within 72 hours. Uncontrolled oral pilot in healthy elderly is noted but disqualified (uncontrolled; possible placebo; oral route with no established bioavailability). "No controlled RCT in healthy adults documents safety or efficacy." Mismatch characterized as "fundamental population boundary" with no softening language. The "Honest Expectation-Setting" subsection reiterates: "The healthy-adult use case has no evidentiary floor."

### Injectable-biologic hazards
YES. All four hazard categories present:
- Hypersensitivity/anaphylaxis: Grade III case (PMID 39055722; 85-year-old; hemodynamic collapse, bronchospasm, tryptase/histamine elevation) documented; reaction occurred at ~30 min post-infusion; label states "very rare (<1/10,000)" but case emphasizes it can occur on any infusion day including the first.
- Porcine-CNS prion-theoretical: enzymatic hydrolysis reduces to <10 kDa fragments; manufacturers and regulators accepted this mitigation; theoretical concern not eliminated — "reduced but residual"; acknowledged as "recognized consideration in the biologic manufacturing risk framework, not a documented clinical event."
- Cold-chain failure (grey market): storage ≤25°C, no freezing, light protection, 5-year shelf life; grey-market routes (Dubai, Russia, EU-to-USA) with variable temperatures, no chain-of-custody; "Degraded Cerebrolysin is a biologic with unknown composition."
- Counterfeiting/impurity: no GMP verification possible for grey-market product; vendor authenticity claims unverifiable; off-whitelist vendors explicitly flagged.

### WADA status
NOT overclaimed. Cerebrolysin described as "not explicitly named" on 2026 WADA Prohibited List, labeled as "reasoned inference based on available information." Document explicitly states "This is not a clearance for athlete use" and defers to GlobalDRO.com and NADO for verification. Self-check confirms: "WADA status: reasoned inference, not overclaim."

### Off-enum tags
ZERO off-enum tags. Tags in bibliography: `rct` (refs 1, 5), `meta_analysis` (refs 2, 7, 8), `regulatory` (refs 3, 4, 9, 12, 13), `open_label` (ref 6), `animal` (refs 10, 11), `anecdote_aggregate` (refs 14, 15). All are within the valid source-tag enum for this project.

### Fabricated citations
ZERO. Self-check explicitly states: "All PMIDs verified via NCBI eutils. PMIDs 22282884, 37818733, 34959697, 39055722, 28707130, 26611895, 40065222, 25047000 confirmed via NCBI eutils esummary. Titles and authors match cited content. Retraction note PMIDs (40065222, 25047000 retraction DOI) confirmed in search and eutils results."

### Named physicians count
0. The "Named Practitioners" section documents: "No named US or UK practitioner with a public, verifiable, date-stamped clinical protocol for Cerebrolysin in the grey-market/nootropic context was located." In approving jurisdictions (~50 countries), prescribing is standard formulary neurology practice; no individually-named prescribers are cited. "Explicitly NOT documented (searched; not locatable to venue + date; not fabricated)" is stated explicitly.

---

## Non-English Layer — Detailed Verification

**File:** `vault/library/peptides/cerebrolysin/non-english-layer.md`
**Present:** YES
**`## Bibliography`:** YES (present; tabular format, lines 560–579, 14 entries across Russian/Chinese/German)
**`## Self-check`:** YES (section present, lines 583–596)

### Languages surveyed (≥3 required)
YES — three languages confirmed: **Russian**, **Chinese**, **German**.

### Per-language explicit findings
- **Russian:** 154 PubMed-indexed items (LA=rus confirmed). 7 primary studies selected (R1–R7): CEREHETIS RCT program (R1 PMID 37682097; R2 PMID 38512096; R3 PMID 40123141), expert consensus (R4 PMID 37796079), 3-year MCI-to-dementia prospective comparative study (R5 PMID 39435777), animal antioxidant pharmacology (R6 PMID 34460162), 2026 systematic review of post-stroke rehabilitation (R7 PMID 41782528). Russian layer is the largest active non-English evidence corpus.
- **Chinese:** PubMed eutils (LA=chi) returned 2 verified results: C1 (PMID 12947679; pharmaceutical quality study documenting elemental profile differences between Chinese domestic generic and Austrian original), C2 (PMID 39968589; Cerebrolysin as standard background neurotrophic care in Chinese ICUs). Broader CNKI corpus is acknowledged as existing but not directly verified — stated explicitly.
- **German:** 13 PubMed-indexed items (LA=ger confirmed). 5 primary studies selected (G1–G5): Windisch 1985 animal pharmacology x2 (PMID 4084338, 4074439), Kofler/Harrer 1990 early RCT (PMID 2123433), Koppi/Barolin 1996 comparative study (PMID 8867272), Biesenbach et al. 1997 controlled trial in diabetic neuropathy (PMID 9173675). Austrian SmPC (Fachinformation AT 5.1; Zulassungsdatum 25.03.1996) documented as regulatory landmark.

### Cross-language conclusion (reinforces-not-resolves-concentration)
YES. The net honest assessment section (lines 541–556) and the self-check (line 589) explicitly state the conclusion: all three non-English layers "reinforce rather than resolve the concentration concern" — Russian literature is concentrated in the drug's largest market; Chinese literature is in an authorization market with domestic generic compositional differences; German/Austrian literature is the manufacturer-origin early-era corpus. The self-check line confirms: "Cross-language summary note confirms: 'reinforces rather than resolves the concentration concern.'"

### Off-enum tags
ZERO off-enum tags. Tags in bibliography: `rct`, `meta_analysis`, `cohort`, `animal`, `in_vitro`, `mechanism_review` — all within the valid source-tag enum.

### Fabricated citations
ZERO. Self-check line 592 explicitly states: "No fabricated citations. All 14 items carry verified PMIDs confirmed via PubMed eutils efetch (LA field confirmed for each). No CyberLeninka-only items included. CNKI corpus mentioned as 'inferred, not directly verified' — no CNKI items included in the numbered bibliography."

---

## Summary

Both layers PASS all gate requirements. Practitioner layer correctly resolves the data-sheet question ("no compounding data sheet — by design, manufactured biologic; SmPC as functional equivalent; grey-market vendor list documented"), documents CASTA null + 2023 Cochrane SAE signal, both integrity axes (Masliah/NIH misconduct + Rockenstein retractions; Sharma/Muresanu high-volume industry-linked), healthy-adult population mismatch (unqualified), all four injectable-biologic hazards, and WADA status without overclaim. Zero off-enum tags. Zero fabricated cites (PMIDs eutils-verified per self-check). Named physicians count = 0 (none located; explicitly documented as searched-and-null, not fabricated). Non-English layer surveys Russian (7 verified PMID-bearing primaries from 154-item corpus), Chinese (2 verified PMIDs; CNKI inferred-not-verified explicitly stated), and German (5 verified PMID-bearing primaries from 13-item corpus), with explicit per-language findings and the honest "reinforces-not-resolves-concentration" cross-language conclusion. Zero off-enum tags. Zero fabricated cites.
