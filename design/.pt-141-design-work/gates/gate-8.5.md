# Gate 8.5 — Layers Verification (PT-141 / Bremelanotide, mode=deep)

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/pt-141/practitioner-layer.md","present":true,"compounding_sheets_count":3,"named_physicians_count":1,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/pt-141/non-english-layer.md","present":true,"languages_surveyed":["Chinese","German","Russian"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

---

## Practitioner Layer — Detailed Findings

**File present:** YES — `vault/library/peptides/pt-141/practitioner-layer.md`

**`## Bibliography` section:** PRESENT (17 numbered entries spanning regulatory, rct, anecdote_aggregate, practitioner_protocol, and vendor_label tiers).

**`## Self-Check` section:** PRESENT (dedicated section covering tier-tagging compliance, compounding data sheet gate finding, three-compound identity hazard coverage, named practitioner verification, and residual gaps).

**Compounding data sheets located (count = 3):**
1. Wells Pharmacy Network (wellsrx.com) — bremelanotide nasal spray 10 mg/mL; product page with indication, contraindications, AEs, FDA non-approval disclaimer. [7, vendor_label]
2. Belmar Pharma Solutions (belmarpharmasolutions.com) — nasal spray + sublingual troche; dosing limits (1/24h, ≤8/month), peak onset, contraindications, Lexicomp reference. [8, vendor_label]
3. Formulaterx (formulaterx.com) — PT-141 nasal spray; prescriber-customized dosing; women and men; combination with oxytocin noted. [9, vendor_label]

The document includes the regulatory basis for the compounding market's legitimacy: the different-route exemption from the "essentially a copy" doctrine under 503A, documented with the FDA guidance citation [6, regulatory].

**FDA-approved prescribing pathway (Vyleesi):** Fully documented. Label dose: 1.75 mg SC autoinjector, ≥45 min before activity, max 1/24h, max 8/month. Discontinue at 8 weeks if no improvement. Contraindications: uncontrolled hypertension, known CVD. All label-derived.

**Commercial reality (AMAG → Cosette):** Documented in full. AMAG licensed 2017, terminated 2020; Palatin managed 2020–2023; Cosette acquired December 19, 2023 for $12M + up to $159M in milestones; consecutive double-digit Rx growth since acquisition. [3, anecdote_aggregate]

**Three-compound hazard table (MT-II / PT-141 / Afamelanotide):** PRESENT. Full comparison table covering structure, receptor selectivity (MC1R/MC3R/MC4R/MC5R profiles), primary clinical use, FDA approval status, route, tanning effect, nausea, BP effect, WADA status, and confusion hazard for each compound. Dedicated section with operational rule for practitioners on confirming product identity via vendor CoA.

**Off-label male evidence — Safarinejad et al. (2008):** DOCUMENTED. n=342 married men, sildenafil-resistant ED, RDBPC, intranasal formulation, 62% improvement vs. 21% placebo, p<0.001.

**CRITICAL — Safarinejad Expression of Concern:** CONFIRMED FLAGGED. The document carries the following explicit flag in two locations:

- In the Safarinejad entry body (§"Off-Label Use in Men"): "INTEGRITY FLAG: This paper carries an active Expression of Concern issued by J Urol in 2023 (PMID 36626345) on data-integrity grounds. Efficacy claims from this study should NOT be treated as reliable; it is the sole large male RCT in this literature and it is integrity-flagged."
- In the bibliography entry [12, rct]: "[Expression of Concern issued J Urol 2023, PMID 36626345, data-integrity grounds — efficacy claims unreliable]"
- In the "Honest assessment of the male evidence base" paragraph: the EoC is repeated with PMID citation and the explicit statement "its efficacy claims must not be treated as reliable."

The EoC is flagged prominently, with PMID specificity, in the narrative, in the summary assessment, and in the bibliography — three placements. This load-bearing item is present and correctly handled.

**Named practitioner (verified to venue + credentials + date):** Dr. Justin Houman, MD, FACS — fellowship-trained urologist, male reproductive medicine, Tower Urology Los Angeles, (855) 246-2700. Protocol elements: SC or intranasal, 45 min pre-activity, ≤8/month, CV assessment + BP review + medication review pre-treatment, contraindications (uncontrolled hypertension, CVD) applied. Dose cited in clinic materials: "7 mg or exceeding" — tagged practitioner_protocol, explicitly flagged as lacking primary source and as far exceeding the approved dose. Named_physicians_count = 1.

**WADA note (softened):** The document states bremelanotide is "Not on 2026 Prohibited List" (in the three-compound table), with a Gaps note that no 2026 WADA PDF was fetched directly and practitioners with athlete patients must independently verify. This is the "softened-WADA" framing consistent with the research brief — confirmed.

---

## Non-English Layer — Detailed Findings

**File present:** YES — `vault/library/peptides/pt-141/non-english-layer.md`

**`## Bibliography` section:** PRESENT (table format with 1 admissible entry G1 + full excluded list with identifiers for all excluded items).

**Self-check section:** PRESENT (`## Self-check` with six checked items covering each language, gate satisfaction, no-fabrication attestation, population annotations, genuine-vs-English-published distinction, and honest per-language findings).

**Languages surveyed: Chinese, German, Russian** — all three explicitly documented with per-language findings, databases searched, search terms tried, and explicit "0 admissible primaries" / "1 admissible entry (narrative review)" statements.

**Per-language results:**

- **Chinese:** 0 genuinely Chinese-language admissible primaries. One Chinese-language narrative review located (Chen Benchuan 2020, *Yiyao Daobao*, DOI 10.3870/j.issn.1004-0781.2020.01.028) — correctly excluded as secondary (综述). PubMed returned 3 PMIDs (all confirmed off-compound: pediatric endocrine disorders). CNKI, Wanfang Data, Baidu Xueshu surveyed. Eight Chinese-character search string variants documented.

- **German:** 1 admissible German-language entry (G1 — Porst H., "Therapie der erektilen Dysfunktion im Jahr 2005," *Urologe A* 2003;42(10):1330–6, PMID 14569381, DOI 10.1007/s00120-003-0418-0) — a narrative clinical review, not a primary interventional study. PubMed language filter returned G1 as the sole result. Google Scholar German-language filter returned G1 plus trade press and wiki entries (excluded). The Porst review's PT-141 mention is from 2003, predating FDA approval and the SC formulation; documents contemporaneous European clinical commentary. 0 German-language primary interventional studies.

- **Russian:** 0 genuinely Russian-language admissible primaries. PubMed language filter returned 11 PMIDs; all 11 individually reviewed and confirmed off-compound (general melanocortin biology, different compounds, unrelated animal models — none address bremelanotide/PT-141/HSDD). CyberLeninka searched; eLibrary.ru access-restricted; web search returned only vendor/forum/news content. Eight Russian-language search string variants documented.

**≥3 languages gate satisfied:** YES — Chinese + German + Russian explicitly surveyed with per-language explicit findings.

**Fabrication check:** The single admissible entry (G1) carries verified PMID and DOI confirmed via PubMed E-utilities. The Chen 2020 review carries verified DOI confirmed via the journal's open-access website. Self-check attests no fabricated citations.

---

## Gate Determination

All mandatory criteria for PASS are met:

| Criterion | Status |
|---|---|
| Both layer files exist | PASS |
| Practitioner layer has `## Bibliography` | PASS |
| Practitioner layer has `## Self-Check` | PASS |
| Practitioner layer: ≥1 compounding data sheet located (or explicit no-sheet + vendor list) | PASS — 3 sheets located (Wells, Belmar, Formulaterx) |
| Practitioner layer: Vyleesi FDA label dose/limits/contraindications documented | PASS — 1.75 mg SC, ≤1/24h, ≤8/month, uncontrolled HTN + CVD contraindicated |
| Practitioner layer: AMAG → Cosette commercial reality documented | PASS |
| Practitioner layer: MT-II / PT-141 / Afamelanotide 3-compound hazard table | PASS |
| Practitioner layer: Safarinejad n=342 male RCT documented | PASS |
| Practitioner layer: Safarinejad Expression of Concern FLAGGED (CRITICAL) | PASS — flagged in narrative (×2) + bibliography (×1), with PMID 36626345 |
| Practitioner layer: Named verified practitioner | PASS — Dr. Justin Houman, MD, FACS (Tower Urology) |
| Practitioner layer: Softened-WADA (not on 2026 prohibited list; verify note) | PASS |
| Non-English layer has `## Bibliography` | PASS |
| Non-English layer has `## Self-check` | PASS |
| Non-English layer: ≥3 languages surveyed with explicit per-language findings | PASS — Chinese (0), German (1 review), Russian (0) |
| Non-English layer: Explicit "0 admissible primaries" statements with databases searched | PASS — all three languages carry explicit statements + database + search term documentation |

**verdict: PASS. halt_reasons: []**
