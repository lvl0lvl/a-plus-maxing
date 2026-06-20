---
title: Tesamorelin — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/tesamorelin/practitioner-layer
class: peptide
layer: prescribing-practice
scope: dose/cycle/route/reconstitution conventions ONLY — NOT efficacy
created: 2026-06-20
last_verified: 2026-06-20
---

# Tesamorelin — Prescribing-Practice Layer

> **Scope discipline.** This document records *how tesamorelin is dosed, prescribed, compounded, and reconstituted in practice* — the dose/cycle/route/reconstitution conventions only. It is **not** an efficacy document and **must not** be read as one. Per type-tag discipline: the **FDA-label doses are `regulatory` (authoritative)**; all other practitioner/vendor/compounding material is admissible **only** for dose/route/reconstitution conventions (and, for vendor labels, reconstitution math). **No source class here grounds an efficacy or adverse-event-rate claim** — those live in the research report (§2–§5) and are unaffected by anything below.
>
> **Regulatory state, read first.** Unlike most peptides in this library, tesamorelin is an **FDA-approved brand drug** (Egrifta / Egrifta SV / Egrifta WR; Theratechnologies), approved in 2010 for one indication only: *reduction of excess abdominal fat in HIV-infected adult patients with lipodystrophy.* Its approved/biologic status **restricts** ordinary 503A bulk compounding (see the compounding gate below), and any non-HIV / body-composition / anti-aging use is **off-label**.

## Dose/route conventions

### Authoritative label doses (`regulatory`)
Tesamorelin is approved across all three marketed formulations for the single HIV-lipodystrophy indication. The three FDA-labeled doses, each verified against DailyMed / accessdata:

- **Original EGRIFTA (1 mg/vial formulation):** **2 mg SC once daily**, into the abdomen. Each single-use vial contains 1 mg, so the 2 mg daily dose requires reconstituting and administering **two vials** per dose. `regulatory`
- **EGRIFTA SV (2 mg/vial formulation):** **1.4 mg SC once daily**, delivered as **0.35 mL** of reconstituted solution into the abdomen. `regulatory`
- **EGRIFTA WR (11.6 mg multi-dose vial):** **1.28 mg SC once daily**, delivered as **0.16 mL**. `regulatory`

The successive reformulations (SV, then WR) lowered the milligram dose and injection volume while delivering comparable tesamorelin exposure — the headline "2 mg → ~1.4 mg → 1.28 mg" reduction reflects formulation/concentration changes, **not** a deliberate de-escalation of the active. Route (SC, abdomen, rotate sites) and the once-daily frequency are identical across all three. `regulatory`

### Off-label practitioner conventions (`practitioner_protocol` — UNATTRIBUTED)
Tesamorelin is widely discussed in the anti-aging / body-composition prescriber space for visceral-fat reduction in non-HIV adults. The conventions that recur across these sources:
- starting at **1 mg SC daily** and titrating toward the labeled **2 mg daily**;
- dosing **at night / on an empty stomach**;
- intermittent schedules such as **5 days on / 2 days off**, run in **~3-month cycles** with rest intervals;
- alongside baseline + follow-up **IGF-1, fasting glucose / HbA1c, and lipid** monitoring.

> **⚠ Honest attribution gap (load-bearing).** The aplus-research standard requires every `practitioner_protocol` claim to carry a **named prescriber + venue + date**. **None** of the off-label sources located meet that bar — they are anonymous med-spa / clinic blog pages and peptide-vendor "dosing guides" (TrimRX, PerfectB, Swolverine, et al.) with no identified author, institution, or presentation date. The A4M runs CME conferences and a peptide-therapy curriculum covering tesamorelin dosing, but no citable, dated A4M/IFM/named-prescriber protocol document specifying a dose was located. **Therefore the off-label conventions above are reported as an unattributed convention-of-the-field, NOT as a properly attributed `practitioner_protocol`.** They should not be relied on as authoritative, and no efficacy/AE claim is drawn from them.

### Cost (qualitative; `regulatory`/`anecdote`)
Brand Egrifta is expensive. Cost aggregators / patient-assistance pages place brand Egrifta SV in the **multiple-thousands-of-dollars-per-month** range for a 30-day supply (reported figures span roughly **$2,400 to $5,500/month** before insurance, varying by source/pharmacy), with manufacturer (Theratechnologies / THERA) patient-support and copay programs cited for eligible patients. These are price-aggregator/anecdote figures, not a clinical claim. `anecdote`

## Named-prescriber protocols (practitioner_protocol — name + venue + date)

**None located that meet the bar.** No named prescriber with a citable venue + date stating a tesamorelin dose/cycle was found. The off-label dosing guides above are all anonymous clinic/vendor pages; the A4M peptide curriculum is a *channel that exists* (it covers tesamorelin dosing in CME) but yielded no extractable named-prescriber dose statement from public pages. Recorded as an explicit absence rather than fabricated — there is no properly attributed named-prescriber tesamorelin protocol in this corpus.

## Compounding data sheets (compounding_data_sheet) — gate result

**Gate finding: NO live tesamorelin product page on a major 503A/503B compounder's own catalog was located, and NO admissible compounding-pharmacy clinical data sheet for tesamorelin was found.** This is reported honestly rather than papered over, and is consistent with tesamorelin's approved-drug/biologic status restricting bulk compounding. Specifically:

- **Empower Pharmacy** — published catalog surfaced **sermorelin acetate injection** and other GH-axis peptides, but **no retrievable tesamorelin product page**. `compounding_data_sheet` (gate: NOT found)
- **503Pharma** — a compounding-pharmacy **trade explainer** ("Tesamorelin: The Complete Guide for Compounding Pharmacies") describes tesamorelin as compoundable "for specific needs under regulations," suggesting injectable solutions at **1–2 mg/mL** (bacteriostatic water, pH 5–7) or **lyophilized 2 mg/vial** preparations — while simultaneously flagging that tesamorelin's **approved/biologic status restricts bulk compounding**, and that any preparation must be patient-specific under 503A/B with documented necessity. This is a trade explainer, **not** a citation-bearing clinical data sheet. `compounding_data_sheet` (trade explainer, conditional)

Regulatory context: FDA moved a batch of peptides into Category 2 of the interim 503A bulks list (Sept 2023), then removed five (AOD-9604, CJC-1295, ipamorelin, thymosin alpha-1, Selank) in Sept 2024 after nominators withdrew. **Tesamorelin was NOT reported among either the added or removed Category-2 peptides** in the sources opened; its compoundability is constrained chiefly by its **approved-drug/biologic status** rather than by an explicit bulks-list placement.

**Net gate result: no verified compounding data sheet from a named compounder offering tesamorelin was located; only a trade explainer asserting conditional compoundability.**

## Reconstitution / formulation notes (math only; `regulatory` for label, `vendor_label` for off-label)

- **EGRIFTA SV (label):** reconstitute one 2 mg lyophilized vial with **0.5 mL Sterile Water for Injection** → **2 mg / 0.5 mL** (4 mg/mL); roll gently 30 s, **do not shake**; draw **0.35 mL = 1.4 mg**; **use immediately, discard remainder**. `regulatory`
- **EGRIFTA WR (label):** reconstitute the 11.6 mg vial with **1.3 mL Bacteriostatic Water for Injection** → seven daily doses of **1.28 mg / 0.16 mL**; one vial mixed per week; **store at room temperature, do not freeze/refrigerate after mixing**. `regulatory`
- **Original EGRIFTA (label):** each 1 mg vial reconstituted with **2.2 mL** diluent; **two vials per 2 mg dose**. `regulatory`
- **Off-label / vendor reconstitution math (no efficacy):** vendor and clinic guides commonly describe a **10 mg "research" vial reconstituted with ~2.5 mL bacteriostatic water**, where **"25 units" on an insulin syringe ≈ 1 mg**. This is gray-market reconstitution arithmetic only and is flagged as such. `vendor_label`

## Bibliography (own; tag + tier)

1. **DailyMed — EGRIFTA SV (tesamorelin) full prescribing information.** https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=3d783378-b02d-4f19-99dd-0fc91a042224 — `regulatory`. SV 1.4 mg SC daily / 0.35 mL; 0.5 mL Sterile Water reconstitution. Label dose/reconstitution only.
2. **EGRIFTA WR — HCP Dosing & Administration,** hcp.egriftawr.com. https://hcp.egriftawr.com/dosing/ — `regulatory`. WR 1.28 mg SC daily / 0.16 mL; 11.6 mg vial + 1.3 mL bacteriostatic water, weekly reconstitution. Label dose/reconstitution only.
3. **EGRIFTA (original formulation) prescribing information,** accessdata 022505 (s012/s013, 2019). https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/022505s012s013lbl.pdf — `regulatory`. 1 mg/vial, 2 mg SC daily (two-vial dose), 2.2 mL reconstitution. (PDF 404 on direct fetch; referenced via search.) Label dose/reconstitution only.
4. **TrimRX — "Tesamorelin Dosing Protocol"** (clinic blog, no named author/date). https://trimrx.com/blog/tesamorelin-dosing-protocol/ — `practitioner_protocol` (**UNATTRIBUTED — fails name+venue+date**). Off-label dose/cycle conventions only.
5. **PerfectB — "Tesamorelin Dosage and Injection Protocol"** + cost page (clinic blog, no named author/date). https://www.perfectb.com/tesamorelin-dosage-protocol/ ; https://www.perfectb.com/tesamorelin-cost/ — `practitioner_protocol` (UNATTRIBUTED) / `anecdote_aggregate` (cost). Conventions + ~$3,000/mo brand cost context only.
6. **Swolverine — "Tesamorelin for Beginners"** (vendor blog, no named author/date). https://swolverine.com/blogs/blog/tesamorelin-for-beginners-benefits-dosage-and-peptide-stacking-tips — `practitioner_protocol` (UNATTRIBUTED). Off-label dose conventions only.
7. **A4M (American Academy of Anti-Aging Medicine) — conferences & peptide curriculum.** https://www.a4m.com/conferences-and-educational-events.html — venue context only; **no citable dated tesamorelin-dose lecture located**.
8. **Egrifta cost aggregators / patient-assistance** (PrescriptionHope; price-guide blogs). https://prescriptionhope.com/medication/egrifta-tesamorelin/ — `anecdote` (price aggregation, not clinical). ~$2,400–$5,500/mo before insurance.
9. **Empower Pharmacy drug catalog** (compounding gate: **no retrievable tesamorelin product page**; sermorelin acetate + other GH-axis peptides surfaced instead). https://www.empowerpharmacy.com/compounding-pharmacy/ — `compounding_data_sheet` (NOT found).
10. **503Pharma — "Tesamorelin: The Complete Guide for Compounding Pharmacies"** (trade explainer). https://503pharma.com/peptides/tesamorelin-the-complete-guide-for-compounding-pharmacies — `compounding_data_sheet` (trade explainer, conditional). 1–2 mg/mL or lyophilized 2 mg/vial; approved/biologic status restricts bulk compounding.
11. **FDA — Bulk drug substances used in compounding under section 503A** + peptide bulks-list actions 2023–2024 (tesamorelin not reported among added/removed in opened sources). https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503a-fdc-act — regulatory context.
12. **PeptideDosages.com — "Tesamorelin 10 mg vial dosage chart"** (gray-market reconstitution math). https://peptidedosages.com/single-peptide-dosages/tesamorelin-10-mg-vial-dosage-protocol/ — `vendor_label` (math only; gray-market flagged). ~2.5 mL bac. water; "25 units" ≈ 1 mg.

## Self-check

- **No efficacy / no AE-rates on these tiers.** Every figure above is a dose/route/cycle/reconstitution *convention* or a regulatory-status/cost fact. The label doses are tagged `regulatory`; all other material is `practitioner_protocol`/`compounding_data_sheet`/`vendor_label`/`anecdote`. **No efficacy or adverse-event-rate claim is grounded on any source here** — those live in the research report.
- **Label doses authoritative and verified.** Egrifta 2 mg / Egrifta SV 1.4 mg / Egrifta WR 1.28 mg SC once daily, each tagged `regulatory` and verified against DailyMed / accessdata.
- **Practitioner-attribution bar enforced (honest absence).** No named prescriber + venue + date tesamorelin protocol was located; the off-label conventions are flagged UNATTRIBUTED (convention-of-the-field) and are not presented as a sourced `practitioner_protocol`. Not fabricated.
- **Compounding data-sheet gate satisfied (explicit absence).** No live named-compounder tesamorelin product page (Empower carries sermorelin, not tesamorelin); only a 503Pharma trade explainer asserting conditional compoundability. Consistent with tesamorelin's approved-drug/biologic status restricting bulk compounding.
