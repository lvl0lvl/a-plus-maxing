---
title: BPC-157 — Prescribing-Practice Layer
type: reference
permalink: a-plus-maxing/library/peptides/bpc-157/practitioner-layer
class: peptide
layer: prescribing-practice
scope: dose/cycle/route/reconstitution conventions ONLY — NOT efficacy
created: 2026-06-18
last_verified: 2026-06-18
---

# BPC-157 — Prescribing-Practice Layer

> **Scope discipline.** This document records *how BPC-157 is actually prescribed, compounded, dosed, and reconstituted in practice* — the dose/cycle/route/reconstitution conventions that circulate among prescribers, peptide clinics, and compounding pharmacies. It is **not** an efficacy document and **must not** be read as one. Per the source-tagging rule, `practitioner_protocol`, `compounding_data_sheet`, and `vendor_label` sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/reconstitution math. **None** of these source classes grounds an efficacy claim, and none appears here for that purpose. The efficacy state (no completed published human RCT; ~85% single-lab animal literature) lives in the research report and is unaffected by anything below.
>
> **Regulatory state, read first.** As of mid-2026 BPC-157 is **not an FDA-approved drug for any indication**. It was placed in FDA **503A Category 2** ("significant safety risk," excluded from the interim compounding-enforcement policy) on **2023-09-29**, then **removed from Category 2 under HHS direction effective ~April 2026** (corroborated by Federal Register notice **2026-07361**, Docket FDA-2025-N-6895), with a **Pharmacy Compounding Advisory Committee (PCAC) meeting scheduled 23–24 July 2026**. Removal from Category 2 is **not** placement on the permissive Category-1 list and confers **no FDA approval and no settled lawful compounding channel** [1, practitioner_protocol]. So the "prescribing practice" described here is a real but legally unsettled grey-market/telehealth practice, not an approved standard of care.

## 1. Dose conventions (the modal practitioner protocol)

The convention that recurs across peptide-clinic and prescriber-facing dosing references is **250–500 mcg per dose, once or twice daily**, by subcutaneous injection, given for a bounded cycle [2, practitioner_protocol][3, vendor_label]. The most common pattern stated is:

- **Starting / systemic dose:** ~250 mcg once daily, often for the first 1–2 weeks [2, practitioner_protocol].
- **Standard:** 250 mcg twice daily (≈500 mcg/day total) [2, practitioner_protocol].
- **Upper band:** up to 500 mcg twice daily, cited for short-term acute-injury use [2, practitioner_protocol].
- **Provider-guide band:** at least one unbranded prescriber dosing handout gives a wider **250–750 mcg** range (with a dosing table mapping 5 U → 250 mcg, 10 U → 500 mcg, 15 U → 750 mcg, 20 U → 1 mg on a U-100 syringe), daily frequency, SC or IM [4, practitioner_protocol].

A bodyweight heuristic of **~10 µg/kg/day** is sometimes quoted; for typical adults this collapses back into the same 200–500 mcg/day band [2, practitioner_protocol]. **There is no validated human dose-finding study behind any of these numbers** — no published human Phase 2/3 dose-ranging trial exists, so every figure here is a *convention*, extrapolated from preclinical (largely rat) protocols and clinical anecdote, not an established therapeutic dose [2, practitioner_protocol].

## 2. Route conventions (oral vs SC vs IM)

- **Subcutaneous (SC)** is the modal injectable route, typically into the abdominal subcutaneous fat or — by widespread convention — into the SC tissue *near the target injury* ("local" dosing) [2, practitioner_protocol][4, practitioner_protocol]. Note the route-risk asymmetry carried in the research report: parenteral routes (SC/IM/IV) sit in the *higher* immunogenicity-risk bucket in FDA's framework than oral — relevant because the most common practitioner route is the higher-risk one.
- **Intramuscular (IM)** appears as an alternative injectable route in prescriber handouts [4, practitioner_protocol].
- **Oral (capsule / sublingual troche)** is the convention for **GI-targeted** use (gut/"leaky gut"/systemic anti-inflammatory framing). Oral formats are dosed *higher* than SC to offset absorption losses; some oral products add **SNAC (Salcaprozate Sodium)** as an absorption enhancer, and sublingual troches are claimed to reduce first-pass loss [3, vendor_label][5, vendor_label]. Representative oral products are sold at **250–500 mcg per capsule, "twice per day,"** with no cycle length specified on-label [5, vendor_label][6, vendor_label].

## 3. Cycle-length conventions

The recurring cycle convention is **4–8 weeks for acute injury** and **8–12 weeks for chronic conditions**, with **2–4 week off-periods** between cycles commonly suggested [2, practitioner_protocol]. A tighter "4–6 week cycle" is also frequently stated as the default [2, practitioner_protocol][3, vendor_label]. These are convention/heuristic, not trial-derived.

## 4. Reconstitution math (purity/dilution arithmetic only)

Injectable BPC-157 is dispensed as a **lyophilized powder** reconstituted with **bacteriostatic water** (sterile water + 0.9% benzyl alcohol), which by convention keeps a multi-dose vial usable ~28 days refrigerated (2–8 °C) [3, vendor_label]. The arithmetic that recurs (admissible as vendor-label reconstitution math only):

| Vial | + Bac. water | Concentration | 250 mcg dose | On U-100 |
|------|--------------|---------------|--------------|----------|
| 5 mg | 2 mL | 2,500 mcg/mL | 0.10 mL | 10 U [3, vendor_label] |
| 5 mg | 5 mL | 1,000 mcg/mL | 0.25 mL | 25 U [3, vendor_label] |
| 10 mg | 2 mL | 5,000 mcg/mL | 0.05 mL | 5 U [2, practitioner_protocol] |

(The unbranded provider handout's "0.035 mg/unit" for a 10 mg + ~3 mL fill is internally consistent with the same U-100 arithmetic [4, practitioner_protocol].) This math is route/strength bookkeeping only and carries no efficacy or safety implication.

## 5. Compounding-pharmacy availability and the data-sheet gate

**Gate finding: NO admissible compounding-pharmacy *clinical data sheet* (i.e., a pharmacy-issued monograph whose dose/route/indication claims cite their primary literature) was located.** This is reported honestly rather than papered over, and is consistent with the regulatory state: BPC-157 has **no USP/NF monograph** and **no FDA-approved labeling**, so there is no standardized clinical monograph for a pharmacy to publish [1, practitioner_protocol]. What *does* exist in this niche is:

- **Vendor product pages / patient-instruction inserts** (Morgan Compounding "BPC-157 Rapid PRO" 500 mcg oral capsules; Vios; Infiniwell/formerly Tailor Made oral capsules with SNAC) — these give dose-per-capsule and "twice per day" instructions but cite **no primary references**, so they are admissible only as `vendor_label` purity/dose-format data, **not** as clinical data sheets [5, vendor_label][6, vendor_label].
- **A vendor sales catalog** (Tailor Made Compounding / "TMC Catalog") described as carrying per-peptide "descriptions, protocols, and clinical research summaries." This is a **product catalog**, not a per-substance clinical data sheet citing its own primaries, and could not be confirmed to meet the admissibility bar (catalog access was rate-limited at fetch time); treated as **vendor catalog, not admissible as a data sheet** [7, vendor_label].
- **Unbranded prescriber dosing handout** (HubSpot-hosted "BPC-157 Dosing — provider guide") — a `practitioner_protocol` for dose/route/reconstitution conventions, but it carries **zero scientific citations** and **no publisher identity**, so it is *not* a compounding-pharmacy clinical data sheet [4, practitioner_protocol].

**Vendors / pharmacies / source classes searched for an admissible data sheet** (none yielded a citation-bearing clinical data sheet): Empower Pharmacy, Tailor Made Compounding / Infiniwell, Belmar Pharma Solutions, Strive, Hallandale, Revive, Morgan Compounding, Vios Compounding, plus generic queries for compounding-pharmacy "monograph"/"fact sheet"/"data sheet" PDFs with references. Empower, Belmar, Strive, Hallandale, and Revive returned **no public BPC-157 monograph** at all.

**Current compounding availability (in flux).** Because BPC-157 was removed from Category 2 (~April 2026) but **not** added to the permissive Category-1 bulks list, 503A pharmacies dispensing it are operating in a legally unsettled window pending the **23–24 July 2026 PCAC** vote; telehealth/clinic channels were dispensing 5 mg vials with patient inserts at the 250–500 mcg/day convention, at roughly $180–280/month, with providers relying on "published preclinical literature (primarily Sikiric et al.), clinical experience, and compounding-pharmacy guidance" rather than any approved monograph [1, practitioner_protocol]. Treat availability as **transient and jurisdiction-dependent**, not settled.

## Bibliography

1. **Telehealth Ally — "Is BPC-157 Legal in 2026? FDA Status, Compounding Rules & Telehealth Access."** Fetched https://www.telehealthally.com/guides/bpc-157-legal-status-guide — `practitioner_protocol` (used for compounding-status/availability and the convention that providers lean on preclinical lit + pharmacy guidance; NOT efficacy). *(Regulatory specifics here are corroborated against the research-report's Federal Register 2026-07361 primary; the Holt Law regulatory-alert page, https://djholtlaw.com/regulatory-alert-the-legal-status-of-bpc-157-in-compounding-and-clinical-practice/, returned HTTP 403 and could not be fetched.)*
2. **"BPC-157 Dosing Guide: Protocol, Reconstitution & Safety (2026)," peptidedosingprotocols.com.** Fetched https://www.peptidedosingprotocols.com/protocol/bpc-157 — `practitioner_protocol` (dose band 250 mcg×1–2/day up to 500 mcg×2/day; ~10 µg/kg/day heuristic; 4–6/6–8/8–12-week cycles; 2–4-week off-periods; 10 mg+2 mL → 5,000 mcg/mL → 250 mcg = 0.05 mL = 5 U). Note: this aggregator *does* cite primaries (He 2022; Sikiric 2011; Lee 2025; Vasireddi 2025) but is used here only for dose/route/cycle/reconstitution conventions, never for efficacy.
3. **"BPC-157 Dosage Guide / Reconstitution," practitioner & calculator references (Swolverine; medsbase BPC-157 reconstitution calculator).** Fetched via https://www.peptidedosingprotocols.com/protocol/bpc-157 and search snapshots — `vendor_label` (bacteriostatic-water reconstitution, ~28-day cold storage, dilution/units arithmetic; oral-vs-SC format conventions). Reconstitution/format math only.
4. **"BPC-157 Dosing — provider guide" (unbranded prescriber handout, HubSpot-hosted PDF).** Fetched https://45330025.fs1.hubspotusercontent-na1.net/hubfs/45330025/BPC-157%20Dosing-FINAL.pdf — `practitioner_protocol` (250–750 mcg range; unit table 5 U/250 mcg … 20 U/1 mg; SC or IM; daily; 10 mg+2 mL → 0.035 mg/unit). **No publisher identity, no citations** — explicitly NOT a compounding clinical data sheet.
5. **Morgan Compounding Pharmacy — "BPC-157 Rapid PRO."** Fetched https://morgancompounding.com/product/bpc-157-rapid-pro/ — `vendor_label` (oral capsule, 500 mcg/capsule, "one capsule twice per day"; no citations). Dose-format only.
6. **Infiniwell (formerly Tailor Made) BPC-157 oral capsules; Vios Compounding BPC-157 capsules.** Search-indexed product pages (https://infiniwell.com/products/bpc-157, https://www.vioscompounding.com/product/bpc-157-capsules/) — `vendor_label` (250 mcg/capsule oral formats; SNAC absorption-enhancer convention). Dose-format only.
7. **"Tailor Made Compounding Peptide Catalog (TMC Catalog)."** https://www.scribd.com/document/495397628/TMC-Catalog / https://studylib.net/doc/25835966/ — `vendor_label` (vendor product catalog with per-peptide "protocols/clinical research summaries"). Fetch was rate-limited (HTTP 429); characterized from search index only. **Not confirmed citation-bearing → not admissible as a compounding clinical data sheet.**

## Self-check

**What was searched.** (a) Dose/route/cycle/reconstitution conventions across prescriber-facing dosing references and peptide clinics; (b) named compounding pharmacies for a citation-bearing clinical data sheet — Empower, Tailor Made/Infiniwell, Belmar, Strive, Hallandale, Revive, Morgan, Vios; (c) named-physician / society protocol channels — SSRP/Seeds Scientific certification, A4M / peptide-society conference handouts; (d) generic compounding "monograph/fact sheet/data sheet" PDF queries; (e) regulatory-status sources (Telehealth Ally fetched; Holt Law 403'd; FR 2026-07361 cross-checked against the research report).

**What is admissible.** Dose conventions (250–500 mcg, modal; up to 750 mcg in one handout), route conventions (SC modal, IM alt, oral/SNAC for GI), cycle conventions (4–8 wk acute / 8–12 wk chronic, 2–4 wk off), and reconstitution math — all admissible **only** as prescribing-practice conventions, tagged `practitioner_protocol` / `vendor_label`. **No efficacy claim is grounded on any source here.**

**Gate result (§4.1).** **No admissible compounding-pharmacy clinical data sheet located.** A compounding clinical data sheet requires pharmacy-issued claims that cite their primary literature; every compounding/vendor artifact found was either citation-free (Morgan, Vios, Infiniwell, the unbranded provider PDF) or an unverifiable vendor catalog (TMC). The explicit searched-vendor list is recorded in §5 and above. This is consistent with the regulatory reality: no USP/NF monograph and no FDA labeling exist, so no standardized clinical monograph is published, and post-Category-2-removal compounding availability is legally unsettled pending the 23–24 July 2026 PCAC vote.

**Gaps / dropped claims.**
- *Dropped:* the Holt Law regulatory-alert page (HTTP 403) — its compounding-legality detail was not citable directly; regulatory facts retained here are the ones independently corroborated by FR 2026-07361 in the research report.
- *Dropped:* the TMC catalog as a data-sheet candidate (HTTP 429; could not confirm it cites primaries) — downgraded to vendor catalog.
- *Not located:* any A4M / International Peptide Society / SSRP **dated, citable dosing handout** naming an attributable physician protocol — the SSRP certification exists but no public per-substance BPC-157 protocol document with citations was retrievable.
- *Caveat:* all dose/cycle figures are conventions, not trial-derived; no human dose-finding study exists. The modal SC route is in FDA's higher immunogenicity-risk bucket — a prescribing-practice fact worth flagging, carried without efficacy implication.
