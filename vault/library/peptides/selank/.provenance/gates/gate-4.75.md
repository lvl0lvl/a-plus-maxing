# Phase 4.75 Citation Integrity — Selank

Scope: all six sections (A–F) read in full; `_source-whitelist.md` loaded for the type-tag enum + tier rules. 13 IC checks run.

- **IC-1 (one type-tag per claim) — PASS.** Every load-bearing claim carries exactly one backtick type-tag from the whitelist enum (`in_vitro`, `animal`, `cohort`, `open_label`, `mechanism_review`, `regulatory`, `vendor_label`, `practitioner_protocol`, `rct/comparative`). No untagged numerical claims; no double-tag conflicts (where two tags co-occur, e.g. A§1 `in_vitro` + `cohort`, they scope distinct sub-claims — biochemical assay vs. patient correlate — not one claim).
- **IC-2 (no vendor/anecdote grounding a number) — PASS.** Vendor figures are actively *excluded*: A§PK drops vendor half-life ("<2 min"/"20-30 min") as "not citable … vendor-grounded"; D drops vendor LD50 (">1000 mg/kg") per the no-vendor-numerical-rate rule. The only `vendor_label`-grounded numbers (F: ~250-500 mcg/dose gray-market convention) are dose-*convention*, not efficacy/AE rates — admissible for vendor tier and explicitly framed "as convention, not as evidence of dose-response." No efficacy/AE number rests on a vendor/anecdote tag.
- **IC-3 (no practitioner source grounds efficacy/AE number) — PASS.** F explicitly routes efficacy/AE to §B/§C/§D ("practitioner and vendor sources NEVER ground efficacy or AE-rate claims"). `practitioner_protocol` tags ground only cycle/route conventions.
- **IC-4 (population annotation) — PASS.** Animal cites carry species+n: "animal (Wistar rat, n=48)", "animal (Wistar rat, n=30)", "animal (mice: BALB/c, C57Bl/6)". Clinical cites carry population: GAD/neurasthenia n=62 (30/32), n=60, n=70 (30/40).
- **IC-5 (route fidelity) — PASS.** Intranasal is consistently named as the primary/preferred route; where i.p. dosing appears (A ethanol study, B Kolik, D withdrawal models) it is the actual route used in that study, stated as such — no cross-route efficacy extrapolation presented without flag. No `[route-extrapolation]` need triggered.
- **IC-6 (no fabricated citations) — PASS.** Pre-audited: 26924987=Volkova 2016 Front Pharmacol; 18454096=Zozulia 2008; 25176261/26356395=Medvedev. Newly spot-verified via NCBI eutils: 18841804=Inozemtseva, *Dokl Biol Sci* 2008 (BDNF); 28293190=Filatova, *Front Pharmacol* 2017 (IMR-32); 34396551=Doyno & White, *J Clin Pharmacol* 2021; 30255741=Vyunova, *Protein Pept Lett* 2018; 36322304=Konstantinopolsky, *Bull Exp Biol Med* 2022. All resolve to claimed author/year/journal.
- **IC-7 (no placeholders) — PASS.** Grep for `[X]`/TODO/TKTK/lorem/FIXME/TBD across all six sections returned zero hits.
- **IC-8 (no Wikipedia) — PASS.** Zero Wikipedia citations. The sole "Wikipedia" string (B§5) is a negative assertion ("No Wikipedia, vendor, or anecdote sources were used"). "peptidewiki" in F is a gray-market dosing aggregator tagged `vendor_label`, not Wikipedia.
- **IC-9 (population-mismatch) — PASS.** Rodent→human is consistently flagged (B: rodent findings "do not constitute human anxiolytic evidence"; C: nootropic claim is "mechanistic + anxiolytic-preservation, not demonstrated cognitive-enhancement"; D: rat-withdrawal data "animal evidence, not a human dependence study"). Strain-specific (BALB/c vs C57Bl/6) results reported as strain-dependent, not collapsed.
- **IC-10 (concentration audit) — PASS (surfaced).** §C enumerates 7 distinct primaries; single-network (IMG RAS / Zakusov–Serbsky lineage) share = 7/7 (1.00), strictest reading 6/7 (≈0.86). threshold_triggered=true (≥0.70). Surfaced FIRST-CLASS as the "DEFINING FACT (read first)" heading at the top of §C, before any indication, and echoed in the opening of §B, the defining-safety-fact of §D, and §E/§F ("no independent Western replication"). Per calibration, surfaced high concentration is PASS, not HALT.
- **IC-11 (regulatory tag discipline) — PASS.** All GRLS/FDA-503A/EMA/WADA-S0/Russian-registration facts in §E and §F carry `regulatory` tags.
- **IC-12 (corpus-scoping spot-grep) — PASS.** Load-bearing numbers trace to cited abstracts: IC50 15 µM (Zozulia 2001), TKPRPGP sequence (multi-source), n=62/30-vs-32 medazepam, BDNF 250/500 µg/kg dose+timecourse (Inozemtseva), Volkova gene-fold changes. Where a figure is full-text-unavailable the report flags it (C[7] "cited by record only"; B "dosing not in indexed abstract") rather than fabricating — integrity-honest.
- **IC-13 (cross-section consistency) — PASS.** Reconciled at 4.25 and confirmed clean: TKPRPGP consistent across A/B/F; medazepam pivotal trial consistently PMID 18454096 (2008); reg. no. ЛСР-003338/09, 503A Sept-2024 Category-2 removal, and WADA-not-listed consistent across §E/§F.

No genuine defects found: no untagged claim, no vendor-grounded efficacy/AE number, no fabricated citation, no Wikipedia. High single-lineage concentration is surfaced first-class, satisfying the IC-10 gate.

## Verdict
verdict: PASS

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "timestamp": "2026-06-20T00:00:00Z",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"},
    "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"},
    "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"},
    "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"},
    "IC-13": {"status": "PASS"}
  },
  "population_mismatch": {"verdict": "PASS", "checked_citations": 8},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 7, "largest_cluster_name": "IMG RAS / Zakusov lineage", "largest_cluster_count": 7, "share": 1.0, "threshold_triggered": true, "surfaced_section_heading": "Section C — DEFINING FACT (read first)", "surfaced_before_first_indication": true},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 6, "claims_failed": []},
  "halt_reasons": [],
  "warnings": []
}
```
