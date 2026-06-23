# Gate 4.75 — Citation Integrity Verification
**Compound:** PT-141 / bremelanotide (Vyleesi)
**Sections checked:** A, B, C, D, E
**Run date:** 2026-06-21
**Verifier:** Phase 4.75 IC battery (IC-1 through IC-13) + population-mismatch + concentration-audit + corpus-scoping

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
      "status": "PASS",
      "count_checked": 47,
      "count_flagged": 0
    },
    "IC-2": {
      "status": "PASS",
      "count_checked": 47,
      "count_flagged": 0
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 4,
      "count_flagged": 0
    },
    "IC-4": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-5": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-6": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-7": {
      "status": "PASS",
      "count_checked": 8,
      "count_flagged": 0
    },
    "IC-8": {
      "status": "PASS",
      "count_checked": 6,
      "count_flagged": 0
    },
    "IC-9": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0,
      "findings": [
        "Palatin/AMAG sponsor-concentration for Phase 3 pivotal evidence = 1.0 (100%); disclosed prominently in Section E.2 with a first-class COI section before any efficacy subsection; structurally normal for single-company FDA-approved drug but disclosed as material — threshold_triggered=true, not a HALT"
      ]
    },
    "IC-10": {
      "status": "PASS",
      "count_checked": 10,
      "count_flagged": 0,
      "findings": [
        "PMID 31599840 confirmed — Kingsberg 2019, Obstet Gynecol, FSFI-D +0.35 integrated",
        "PMID 31599847 confirmed — Simon 2019 open-label extension, nausea 40.4%, OL discontinuation 23.4%/18.7%",
        "PMID 35076581 confirmed — Edinoff 2022, Neurol Int, mechanism review",
        "PMID 18206919 confirmed — Safarinejad 2008, J Urol, EoC notation present on PubMed page",
        "PMID 36626345 confirmed — J Urol 2023 EoC on Safarinejad",
        "DailyMed SetID 8c9607a2-5b57-4a59-b159-cf196deebdd9 confirmed — nausea 40%, flushing 20.3%, BP +6/+3 mmHg",
        "PMID 17584130 confirmed — King 2007, Curr Top Med Chem, 'PT-141 is the carboxylate derivative of MT-II' verbatim in abstract",
        "PMID 27977473 confirmed — White 2017 (not Portman as stated in Section B [5]); see IC-10 finding below",
        "PMID 35147466 confirmed — Clayton 2022 J Womens Health, 43 studies ~3500 subjects",
        "PMID 19224885 confirmed — Evans-Brown 2009, BMJ"
      ]
    },
    "IC-11": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-12": {
      "status": "PASS",
      "count_checked": 47,
      "count_flagged": 0
    },
    "IC-13": {
      "status": "WARN",
      "count_checked": 12,
      "count_flagged": 2,
      "findings": [
        "CLAIM: 'Cohen's d effect sizes for the integrated RECONNECT data were approximately 0.39 for the desire domain and 0.27 for the distress item' [Section B, attributed to [2, rct] Clayton J Sex Med 2019 Suppl abstract DOI 10.1016/j.jsxm.2019.09.100] — corpus-missing: DOI returns HTTP 404 (conference supplement abstract; unstable DOI). PMID 31599840 abstract (fetched) does not state Cohen's d. Claim is consistent with published integrated RECONNECT data and FSFI-D scale properties but cannot be verified against the cited corpus. verdict: corpus-missing WARN, not HALT. Recommend orchestrator verify via J Sex Med 2019 Suppl 4 print or Semantic Scholar.",
        "CLAIM: Section B [5] describes the cardiovascular BP study as 'Portman DJ, Brown L, Yuan J, Kissling R, Kingsberg SA' (PMID 27977473) but the fetched PubMed record names first author as William B White, not Portman DJ. Author list in Section B bibliography entry [5] is incorrect. Numerical BP data (+3.1/+3.2 mmHg for 1.75 mg SC, <15 min peak) confirmed in the abstract. This is a bibliography-entry author-list error, not a fabricated citation — the PMID is correct and the data are in the paper. verdict: WARN (not HALT — the claim is verified; the bib author list needs correction)."
      ]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 12,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 8,
    "largest_cluster_name": "Palatin Technologies / AMAG Pharmaceuticals RECONNECT registration program",
    "largest_cluster_count": 8,
    "share": 1.0,
    "threshold_triggered": true
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 12,
    "claims_failed": [
      {
        "claim": "Cohen's d effect sizes for the integrated RECONNECT data were approximately 0.39 for the desire domain and 0.27 for the distress item [Section B, cite [2]]",
        "cite_key": "clayton-2019-jsexmed-abstract",
        "failure_mode": "corpus-missing"
      }
    ]
  },
  "halt_reasons": [],
  "warnings": [
    "IC-13: Cohen's d claim [Section B, cite B[2]] corpus-missing (DOI 404 — conference supplement abstract). Claim consistent with published data; recommend verification against J Sex Med 2019 Suppl 4 print.",
    "IC-13: Section B bibliography [5] lists Portman DJ as first author of PMID 27977473; actual first author is White WB. PMID correct; numerical claims verified. Bib entry needs correction before wiki ingest."
  ]
}
```

---

## IC-1 — Type-Tag Presence

Scanned all inline citations across Sections A–E (47 citation instances). Every `[N, tag]` inline cite carries a tag from the canonical enum:

- `regulatory` — all FDA label, DailyMed, LiverTox, FDA guidance cites
- `rct` — all RECONNECT primary trial cites and male ED Phase I/II cites
- `open_label` — Simon 2019 52-week extension (correctly tagged `open_label`, not `rct`)
- `mechanism_review` — King 2007, Edinoff 2022, Molinoff 2003, Evans-Brown 2009, Mills 2018, LiverTox
- `meta_analysis` — Clayton 2022 J Womens Health
- `vendor_label` — Competitive Technologies press release (E[1]), Palatin/AMAG termination press releases (E[8],[9])
- `anecdote_aggregate` — Pharmaceutical Technology analyst comment (E[7]), Swolverine blog (E[10])

No tag outside the enum detected. No untagged inline cites found.

**PASS — 47 checked, 0 flagged.**

---

## IC-2 — Bibliography Type-Tag Presence

All 47 bibliography entries across Sections A–E carry `— tag: <tag>` annotations in the required format. Each tag verified against the canonical enum.

Notable correct multi-use: Evans-Brown 2009 [C6] tagged `mechanism_review` with an inline note explaining the BMJ pub-type is Editorial/short-report (no `mechanism_review` sub-enum exists; this is the closest admissible tag — acceptable under whitelist rules where `mechanism_review` covers "narrative or systematic review of pathway/mechanism" and this short report documents grey-market use patterns rather than primary data).

Tier annotations (`tier: 1/2/3`) also present throughout and consistent with whitelist tier definitions.

Safarinejad [B7, C5] correctly tagged `rct — tier: 3 (integrity-flagged)` — the EoC degrades trust tier; the tag is appropriate.

**PASS — 47 checked, 0 flagged.**

---

## IC-3 — Vendor-Not-Numerical

Four `vendor_label` citations identified across all sections:

- Section E[1]: Competitive Technologies 2001 press release — used to establish lineage/platform origin. No numerical efficacy, AE rate, or dose claim in the sentence citing it. PASS.
- Section E[8]: Palatin Technologies July 2020 press release (mutual termination) — used for commercial/contractual facts ($12M, $4.3M, FY2021/2022 revenue figures). These are commercial revenue figures, not therapeutic dose/efficacy/AE numbers. Admissible as vendor_label for regulated-status/commercialization disclosure. PASS.
- Section E[9]: Palatin Technologies December 2023 press release (sale to Cosette) — commercial facts ($12M upfront, $159M milestone). Same category. PASS.
- Section D[1]: AMAG PR Newswire press release used to establish FDA approval date — regulatory fact. PASS.

No `vendor_label` cite appears adjacent to an efficacy rate, AE rate (%), or therapeutic dose number.

**PASS — 4 vendor_label cites checked, 0 flagged.**

---

## IC-4 — Anecdote-Not-Numerical

Five `anecdote_aggregate` citations identified:

- Section C[6] (D6 in Section D context): Evans-Brown 2009 — tagged `mechanism_review` in the bibliography (BMJ short report), not `anecdote_aggregate`. The inline cite for grey-market melanotan AE patterns cites [6, mechanism_review], not anecdote. The Swolverine blog [E10] is the only true `anecdote_aggregate` source.
- Section D (grey-market compounded formulations): the phrase `[vendor_label/anecdote_aggregate — no number grounded from these sources]` is an explicit source declaration that deliberately grounds NO numerical claim. This is the correct use of anecdote_aggregate — it explicitly excludes numerical grounding.
- Section D[7]: USADA 2026 page — tagged `regulatory`, not `anecdote_aggregate`. The WADA section carries a `thepeptideguides.com` reference with `[anecdote_aggregate — not citable as definitive]` and explicitly excludes it as a definitive source. The sentence containing it does not cite any number to this source.
- Section E[7]: Pharmaceutical Technology analyst comment — `anecdote_aggregate`. Used for "analysts characterized it as likely finding niche use" — qualitative characterization. No numerical AE rate or dose grounded here.
- Section E[10]: Swolverine blog — `anecdote_aggregate`. Used to describe "health authorities in the UK, Australia, and the US have issued warnings" — no numerical claim attributed to this source.

**PASS — 5 anecdote_aggregate cites checked, 0 flagged.**

---

## IC-5 — Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations appear anywhere in Sections A–E.

**PASS — 0 practitioner_protocol cites (check not applicable).**

---

## IC-6 — Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations appear anywhere in Sections A–E. Section D.2 discusses compounded bremelanotide in prose but cites only `regulatory` (FDA guidance) sources for any factual claims.

**PASS — 0 compounding_data_sheet cites (check not applicable).**

---

## IC-7 — Population-Mismatch

Checked all numerical claims for population scope. Eight distinct population-boundary claim instances reviewed:

1. **RECONNECT efficacy numbers** (FSFI-D +0.35, Cohen's d ~0.39, nausea 40%, FSDS-DAO −0.33) — all attributed to [rct] cites for "premenopausal women with HSDD"; population annotation present in section headers and body text. PASS.

2. **Male Phase I/II trial data** (Diamond 2004 RigiScan response, Rosen 2004 SC PT-141, Diamond 2005 combination) — all attributed to male ED trial populations in Section C.1, with "off-label," "no Phase III data," and "not approved in men" statements adjacent. PASS.

3. **Safarinejad 2008 male trial** (33.5% response rate, 8.5% placebo) — cited in Sections B.2 and C.1 with active EoC flag; population correctly identified as "342 married men aged 28–59 with sildenafil-unresponsive ED." PASS — and flagged for integrity, as required.

4. **MT-II human data** (Wessells 2000 n=20 men, n=10 organic ED men) — attributed to MT-II, not PT-141, in Section C.3 with explicit "Attribution rule" paragraph stating "MT-II evidence does not generalize to PT-141." PASS.

5. **Animal/rodent mechanism data** (King 2007 rat/mouse model erections, spinal MC4R) — Section A.2 explicitly labels "In male rats and mice" within the sentence and in a sub-header "Animal and in-vitro receptor evidence (population-annotated)." No population-mismatch tag required per IC-7 procedure since the species is the subject of the sentence within 100 chars. PASS.

6. **BP safety data** (Section D.4.4, +6/+3 mmHg FDA label; +3.1/+3.2 mmHg Portman/White 2017) — correctly attributed to the screened RECONNECT premenopausal women population, with explicit note in C.4 that "conditions... are substantially more prevalent in the male population most likely to use PT-141 off-label." PASS.

7. **Nausea 40% AE rate** (Section D.4.2) — correctly sourced to FDA label [2, regulatory] drawn from pooled RECONNECT phase 3 (n=1,247 premenopausal women with HSDD). Not extrapolated to men. PASS.

8. **Hyperpigmentation 38% at daily dosing** (Section D.4.3) — sourced to FDA label [2, regulatory], population = clinical trial participants. PASS.

**PASS — 8 population-boundary claims checked, 0 flagged.** `population_mismatch` verdict: PASS.

---

## IC-8 — Route-Extrapolation

Checked 6 dose/route claim instances:

1. **Vyleesi approved dose: 1.75 mg SC** — Section A.3, D.2, cited to [1/2, regulatory] (FDA label). Route in source = SC. Route in claim = SC. PASS.

2. **Section B.2 intranasal bremelanotide 10 mg** (Safarinejad 2008, male ED) — cited to [7, rct]; the source explicitly tested intranasal 10 mg. Route matches claim. PASS.

3. **Section C Diamond 2004 intranasal PT-141 (>7 mg)** — cited to [2, rct]; Diamond 2004 tested intranasal. Matches. PASS.

4. **Section C Rosen 2004 SC PT-141 (>1.0 mg healthy; 4–6 mg sildenafil-failure)** — cited to [3, rct]; Rosen 2004 tested SC. Matches. PASS.

5. **Section D grey-market nasal spray** — described with `[vendor_label/anecdote_aggregate — no number grounded]` and correctly noted as not FDA-approved. No dose number cited for this route. PASS.

6. **Section C.4 label BP cap: ≤1 dose/24h, ≤8/month** — SC route. Consistent with label. PASS.

No route extrapolation detected where a dose claim for route X is sourced to a study using route Y without `[route-extrapolation]` flag.

**PASS — 6 route claims checked, 0 flagged.**

---

## IC-9 — Concentration-Surfacing

Single-sponsor share for Phase 3 pivotal efficacy evidence: **1.0 (100% Palatin/AMAG)**.

Threshold ≥70% → concentration-surfacing disclosure REQUIRED per health-gates §3.

**Compliance check:** Section E is titled "Section E — Concentration / COI audit, commercialization & sourcing realism." Section E.2 is "RECONNECT sponsorship and primary-evidence concentration" — a dedicated first-class section that:

- Explicitly states: "100% of the Phase 3 pivotal evidence... originates from the Palatin/AMAG-sponsored trial program."
- Calculates "0% non-sponsor Phase 3 RCT data; 100% Palatin/AMAG registration-program data."
- Contextualizes: "structurally normal for a single-company FDA-approved drug and does not by itself invalidate the efficacy signal."
- Names author COI at Section E.3 including AMAG employees and Palatin VP on author bylines.

The concentration disclosure appears in a dedicated section before the commercial arc subsections (E.4, E.5). This satisfies the health-gates §3 requirement.

`threshold_triggered = true`. This is NOT a HALT — a flagged-but-surfaced sponsor-concentration is compliant.

**PASS.**

---

## IC-10 — No Fabricated Citations

Spot-checked 10 citations via WebFetch/PubMed:

| Citation | PMID/URL | Fetch result | Claim verified |
|---|---|---|---|
| Kingsberg 2019 [B1] | PMID 31599840 | CONFIRMED | FSFI-D +0.35 integrated, +0.30/+0.42 per study |
| Simon 2019 OL extension [B3] | PMID 31599847, PMC6819023 | CONFIRMED | Nausea 40.4%, OL discontinuation 23.4%/18.7%, FSFI-D +1.25–1.30 |
| Edinoff 2022 [A3] | PMID 35076581 | CONFIRMED | Mechanism review, Neurol Int, 2022 |
| Safarinejad 2008 [B7] | PMID 18206919 | CONFIRMED | EoC link to PMID 36626345 present on PubMed page |
| EoC for Safarinejad [B7 note] | PMID 36626345 | CONFIRMED | J Urol 2023 EoC on "Salvage of Sildenafil Failures" |
| DailyMed Vyleesi | SetID 8c9607a2... | CONFIRMED | Nausea 40%, flushing 20.3%, BP +6 sys/+3 dia mmHg, dose 1.75 mg SC |
| King 2007 [A5] | PMID 17584130 | CONFIRMED | "PT-141, which is the carboxylate derivative of MT-II" verbatim in abstract |
| Clayton 2022 safety [C11] | PMID 35147466 | CONFIRMED | 43 studies ~3500 subjects, J Womens Health 2022 |
| Evans-Brown 2009 [C6] | PMID 19224885 | CONFIRMED | BMJ 2009, grey-market melanotan use |
| White 2017 BP study [B5] | PMID 27977473 | CONFIRMED | BP +3.1/+3.2 mmHg for 1.75 mg SC, HR −4.6 to −4.7 bpm |

**Author-list discrepancy found (IC-13 WARN):** Section B bibliography [5] lists "Portman DJ, Brown L, Yuan J, Kissling R, Kingsberg SA" as authors of PMID 27977473. The actual PubMed record lists first author as **William B White** with authors "White WB, Myers MG, Jordan R, Lucas J." The PMID is correct and the numerical BP data are present in the abstract. This is a bibliography error (wrong author list), not a fabricated citation. The numerical claim is verified.

**No fabricated citations detected. PASS with one bib-author-list WARN (see IC-13).**

---

## IC-11 — No Placeholder Strings

Searched all five sections for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`.

No matches found in any of Sections A–E.

The WADA section (D.6) uses language like "is not confirmed explicitly named" and "is unverified from primary source" — these are honest disclosure statements, not placeholder strings. They represent completed research with a disclosed fetch-failure gap, not deferred writing. PASS.

**PASS — 0 placeholder strings detected.**

---

## IC-12 — No Wikipedia Citations

Searched all bibliography entries and inline cites across Sections A–E for `wikipedia.org` URLs.

Section A self-check [line 65] explicitly notes: "IC-12 compliant, replaces prior inadmissible Wikipedia citation" — referring to the Melanotan-II identity fact that was previously sourced to Wikipedia but was replaced with PubChem CID 92432 (NCBI/NLM regulatory database, `regulatory` tag, tier 1).

No `wikipedia.org` URL appears in any bibliography. The replacement PubChem citation [A2] is confirmed as a legitimate NCBI/NLM source (whitelist: `ncbi.nlm.nih.gov`, Tier 1).

**PASS — 0 Wikipedia citations found.**

---

## IC-13 — Per-Citation Corpus Scoping

Checked 12 load-bearing numerical/quoted claims:

| # | Claim | Source | Fetch | Result |
|---|---|---|---|---|
| 1 | FSFI-D +0.35 integrated (p<0.001) | [B1] PMID 31599840 | PubMed abstract + eFetch | CONFIRMED: "+0.35 increase (P<.001)" in abstract |
| 2 | FSFI-D +0.30 Study 301 / +0.42 Study 302 | [B1] PMID 31599840 | PubMed abstract | CONFIRMED: both values in abstract |
| 3 | FSDS-DAO −0.37 Study 301 / −0.29 Study 302 / −0.33 integrated | [B1] PMID 31599840 | PubMed eFetch | CONFIRMED via eFetch abstract |
| 4 | Cohen's d ~0.39 desire / ~0.27 distress | [B2] DOI 10.1016/j.jsxm.2019.09.100 | HTTP 404 | CORPUS-MISSING WARN: conference supplement DOI not resolvable; claim consistent with scale properties and integrated RECONNECT Ns but cannot be verified against cited corpus |
| 5 | Nausea 40.0% vs 1.3% placebo | [A7/B-D] FDA label via DailyMed | DailyMed fetched | CONFIRMED: "40% of VYLEESI-treated patients" vs "1.3%" in label |
| 6 | BP +6 mmHg systolic / +3 mmHg diastolic (FDA label) | [C4/D] FDA label DailyMed | DailyMed fetched | CONFIRMED: "Mean increases of 6 mmHg systolic and 3 mmHg diastolic" |
| 7 | BP +3.1/+3.2 mmHg systolic for 1.75 mg SC (White/Portman 2017 ambulatory) | [B5] PMID 27977473 | PubMed abstract | CONFIRMED: "+3.1 and +3.2 mmHg" for 1.75 mg SC dose; NOTE: first author is White WB not Portman DJ — bib entry [B5] has incorrect author list (WARN) |
| 8 | Nausea 40.4% OL extension; Study 301: 42.7%, Study 302: 37.7% | [B3/D4] PMID 31599847 + PMC6819023 | PMC fetched | CONFIRMED: "40.4%" across both; "42.7%" Study 301; "37.7%" Study 302 |
| 9 | OL discontinuation 23.4% (Study 301) / 18.7% (Study 302) | [B3] Simon 2019 OL PMC6819023 | PMC fetched | CONFIRMED: "23.4%" and "18.7%" discontinuation due to AEs |
| 10 | "PT-141 is the carboxylate derivative of MT-II" | [A5] PMID 17584130 | PubMed abstract | CONFIRMED VERBATIM: "PT-141, which is the carboxylate derivative of MT-II" in abstract |
| 11 | 43 studies ~3,500 subjects (Clayton safety meta) | [C11] PMID 35147466 | PubMed abstract | CONFIRMED: "3500 subjects in 43 completed studies" in abstract |
| 12 | EoC on Safarinejad 2008 PMID 18206919 | PMID 36626345 | PubMed | CONFIRMED: EoC notation present on PubMed page for PMID 18206919; PMID 36626345 exists and is linked |

**Claims checked: 12. Confirmed: 10. Corpus-missing WARN: 1 (Cohen's d DOI 404). Bib-author-mismatch WARN: 1 (White/Portman).** No `number-not-found` or `quote-not-found` failures. No HALT.

**Verdict: WARN (2 findings — not HALT).**

---

## Population-Mismatch (top-level summary)

**Verdict: PASS.** See IC-7 for full detail.

Key confirmations:
- RECONNECT efficacy numbers (premenopausal women HSDD) not generalized to men or postmenopausal women anywhere in the five sections.
- Male off-label evidence clearly labeled off-label, early-phase, and without Phase III support.
- Safarinejad 2008 (only large male RCT) flagged with active EoC throughout.
- Animal mechanism data population-annotated within the sentence.
- MT-II evidence not extrapolated to PT-141 — explicit attribution rule stated.

---

## Concentration-Audit (top-level summary)

**Verdict: PASS.** Threshold triggered (share = 1.0).

- Palatin/AMAG are the sole sponsors of all Phase 3 pivotal efficacy evidence for bremelanotide.
- This is structurally normal for an FDA-approved drug with a single developer/commercialization chain.
- Section E.2 is a first-class disclosure section appearing before efficacy subsection content.
- Author COI disclosures name employer-level conflicts (AMAG employees Williams + Krop; Palatin VP Jordan on author bylines).
- The concentration flag is disclosed without overclaiming invalidation — the correct posture for a drug with genuine regulatory approval.

---

## Warnings (non-HALT)

1. **IC-13 / corpus-missing:** Cohen's d ~0.39/~0.27 claim [Section B, cite B2, DOI 10.1016/j.jsxm.2019.09.100] — conference supplement DOI returns HTTP 404. Claim is consistent with RECONNECT data and scale properties but cannot be verified against the cited corpus. Recommend verifying via J Sex Med 2019 Suppl 4 print or Semantic Scholar before wiki ingest.

2. **IC-13 / bib-author-mismatch:** Section B bibliography [5] attributes PMID 27977473 to "Portman DJ, Brown L, Yuan J, Kissling R, Kingsberg SA." Actual first author is **White WB** (White, Myers, Jordan, Lucas). The PMID is correct and the BP numerical data (+3.1/+3.2 mmHg) are confirmed present in the abstract. The bibliography entry needs author-list correction before wiki ingest.
