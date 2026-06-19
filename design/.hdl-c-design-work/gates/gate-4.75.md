# Gate 4.75 — Citation Integrity Verifier (HDL-C) — iteration 2

Independent re-verification after IC-13 remediation. Mode = standard. All 13 IC checks run fresh against the live corpus (`/tmp/aplus-research/hdl-c/corpus/*.txt`) and both section drafts (`section-A.md`, `section-B.md`).

**Remediation under review:** iter-1 HALTed on IC-13 — three NCEP metabolic-syndrome companion thresholds (TG ≥ 150 mg/dL, BP ≥ 130/85 mmHg, fasting glucose ≥ 100 mg/dL) were cited to `[8, regulatory]` but absent from corpus `B-ref8-ncep-atp3.txt`. The remediation TRIMMED them, keeping only HDL-C's own metabolic-syndrome role (< 40 mg/dL men / < 50 mg/dL women), which IS grounded in B-ref8. **Confirmed removed** — see IC-13 below.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: []
```

## IC-1 Type-Tag Presence

Every inline `[N, tag]` carries a canonical-enum tag. Distinct tags observed across both sections: `meta_analysis`, `rct`, `cohort`, `mechanism_review`, `regulatory`, plus the multi-tag `cohort/open_label` on ref 11. All ∈ enum. No malformed or out-of-enum tags detected.

## IC-2 Bibliography Type-Tag Presence

Section A: all 10 bibliography entries carry a single enum tag. Section B: all 11 entries carry a tag; entry 11 carries the multi-tag `rct / cohort / open_label` (multiple tags acceptable per IC-2 when an entry serves multiple purposes). No untagged entries detected.

## IC-3 Vendor-Not-Numerical

No `vendor_label` cite appears in either section's live claims (the only string matches are in the self-check prose listing tags NOT used). No vendor-grounded numerical claim detected.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` cite appears in either section's live claims. No anecdote-grounded numerical claim detected.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` cite present. Check vacuous. No practitioner-grounded efficacy claim detected.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` cite present. Check vacuous. No compounding-sheet-grounded efficacy claim detected.

## IC-7 Population-Mismatch (health-gates §1)

No `[N, animal]` or `[N, in_vitro]` inline cites in either section — the entire HDL-C evidence base is human (rct/meta/cohort/regulatory/mechanism_review). No numerical claim requires a `[population-mismatch:]` tag. Vacuously PASS. 0 animal/in_vitro cites checked.

## IC-8 Route-Extrapolation

No dose claim carries a route mismatch — interventions are oral drugs (niacin, CETP inhibitors), lifestyle (exercise, alcohol, smoking cessation, diet), or genetic/measurement facts. No SC/IM/IV route extrapolation present. No `[route-extrapolation]` requirement triggered.

## IC-9 Concentration-Surfacing (health-gates §3)

Single-lab share 1/14 ≈ 0.07 (see concentration audit below), well under the 0.70 threshold. No first-class concentration-risk section required. Gate passes vacuously.

## IC-10 No Fabricated Citations

Every inline `[N]` in Section A resolves to entries 1–10; every inline `[N]` in Section B resolves to entries 1–11. Every bibliography entry maps to a saved corpus file (`A-ref1…A-ref10`, `B-ref1…B-ref11`) present on disk and read this verification. No inline cite without a bibliography entry; no orphan entry. (URL HEAD-checks not re-run this iteration — corpus files already cached from prior retrieval; provenance notes for the NEJM 403/CAPTCHA refs preserved in corpus headers.)

## IC-11 No Placeholder Strings

Grep for `citation needed | TBD | TODO | Content continues | according to some reports | research suggests | experts believe` → zero matches in either section.

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` in bibliographies → zero matches.

## IC-13 Per-Citation Corpus Scoping

**Remediation confirmed.** The three trimmed companion numbers (`triglycerides ≥ 150`, `130/85`, `fasting glucose ≥ 100 mg/dL`) now appear in section-B ONLY inside the IC-13 resolution note (line 60) and the `## Post-fix grep audit` documentation block (lines 66, 70, 72, 76) — these are documentation of the OLD claim, not live claims, as the prompt anticipated. The live line-7 metabolic-syndrome sentence now reads "Low HDL-C (< 40 mg/dL in men, < 50 mg/dL in women) is one of the five NCEP ATP III metabolic-syndrome criteria; three of five confer the diagnosis [8, regulatory]" — every number in it (< 40, < 50, five-criteria framing) grounds in `B-ref8-ncep-atp3.txt`. **IC-13 now PASSES.**

Standard mode requires ≥50% sample of numerical/quoted claims (min 10). Sampled and grep-verified **all** load-bearing numerical claims across both sections (well above the 50% floor):

- **Section A (27 claims):** all PASS — Voight MR ORs/SNP scores/n=116,320 → A-ref1; Rohatgi efflux HR 0.33 + C-stat 0.841 → A-ref7; ILLUMINATE n/72.1%/HRs → A-ref10; ACCELERATE n/131.6/37.1 → A-ref5; AIM-HIGH n/25% → A-ref4; HPS2-THRIVE n/RR 0.96 → A-ref3; Madsen n/nadirs/HRs → A-ref2.
- **Section B (40 claims):** all PASS — metsyn HDL thresholds → B-ref8; U-shape inflections (96%/71%/2.6-fold/80%) → B-ref1; Madsen Copenhagen n/745,452/HRs → B-ref2; CANHEART 631,762/55.2/>70/>90 → B-ref3; Kodama 2.53/900 kcal/120 min/1.4/35 RCTs/1,404 → B-ref4; Dron 18.7%/10.9%/0.8/1.4/1.8 mmol/L → B-ref5; Brien 0.094/0.072/0.103/0.141/P-trend → B-ref6; Maeda 0.100/27 studies → B-ref7; unit 38.67/386.65 + CV/error figures → B-ref10; EFLM CVI 7.3%/CVG 21.2%/3.65/5.61/11.63 → B-ref9; diet 1.21→1.07/0.057 + steroid 60-80%/>90%/50% → B-ref11.

Zero `quote-not-found`, zero `number-not-found`, zero `paraphrase-no-token-match`, zero `corpus-missing`. claims_checked = 67, claims_failed = [].

## Concentration Audit (health-gates §3)

Distinct primaries (tags ∈ {rct, meta_analysis, cohort, open_label, animal, in_vitro}): **14** — Voight2012, Madsen2017, Ko/CANHEART2016, HPS2-THRIVE, AIM-HIGH, ACCELERATE/evacetrapib, ILLUMINATE/torcetrapib, Rohatgi2014, Kodama2007, Dron2017, Brien2011, Maeda2003, low-fat-diet-crossover, AAS-pooled. These span independent multi-center consortia and unrelated groups (Copenhagen/Nordestgaard, Ontario/CANHEART, Dallas Heart Study, separate independent meta-analyses). Largest single cluster (Nordestgaard Copenhagen) = 1 paper (Madsen2017). **Share = 1/14 ≈ 0.07**, threshold 0.70 NOT triggered. No first-class concentration section required.

## JSON

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {"IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"}, "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"}, "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"}, "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"}, "IC-13": {"status": "PASS"}},
  "population_mismatch": {"verdict": "PASS", "checked_citations": 0},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 14, "largest_cluster_count": 1, "share": 0.07, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 67, "claims_failed": []},
  "halt_reasons": [],
  "warnings": [],
  "iterations": 2
}
```
