---
title: KPV — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/kpv/practitioner-layer
class: peptide
layer: prescribing-practice
scope: dose/cycle/route/reconstitution conventions ONLY — NOT efficacy
created: 2026-06-19
last_verified: 2026-06-19
---

# KPV (Lys-Pro-Val) — Prescribing-Practice Layer

> **Scope discipline.** This document records *how KPV is actually prescribed, compounded, dosed, and reconstituted in practice* — the dose/cycle/route/reconstitution conventions that circulate among prescribers, peptide clinics, and compounding/vendor channels. It is **not** an efficacy document and **must not** be read as one. Per the source-tagging rule, `practitioner_protocol` (2.7), `compounding_data_sheet` (3), and `vendor_label` (4) sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/reconstitution math. **None** of these source classes grounds an efficacy claim, and none appears here for that purpose. The efficacy state (no completed published human RCT; mechanistic/preclinical + small in-vitro/animal literature) lives in the KPV research report and is unaffected by anything below.
>
> **Regulatory state, read first.** As of mid-2026 KPV is **not an FDA-approved drug for any indication** and is **not on the FDA 503A authorized-bulks list**. KPV sat in 503A **Category 2** until it was **removed from Category 2 (~April 15–22, 2026) because the nomination was withdrawn** — one of 12 peptides removed in that action. Removal from Category 2 is **not** the same as placement on the permissive Category-1/authorized-bulks list; it removes the explicit "do-not-compound" designation but **confers no FDA approval and no settled lawful compounding channel** [8, practitioner_protocol][9, practitioner_protocol]. FDA scheduled a **Pharmacy Compounding Advisory Committee (PCAC) meeting for 23–24 July 2026** to consider whether several of the removed peptides — KPV among them, including **KPV acetate** and **KPV free base** — should be formally added to the 503A bulks list [8, practitioner_protocol]. So the "prescribing practice" described here is a real but legally unsettled grey-market / telehealth / vendor-research practice, not an approved standard of care.

## Dose/route conventions by channel (oral / SC / topical)

KPV is dosed across **three distinct channels**, and the unit conventions differ sharply between them — which is exactly where the dosing-error risk lives (see the Campbell unit caveat below).

**Oral (PepT1-favored — the modal "gut" channel).** Oral is the route most clinics favor for GI / "leaky-gut" / IBD-framed use, because KPV is small and stable enough to be carried across intestinal epithelium by the **PepT1 di/tripeptide transporter** rather than fully degraded [4, vendor_label][5, practitioner_protocol]. The recurring oral convention:
- **200–500 mcg once or twice daily**, taken **on an empty stomach** (~30 min before food) to reduce competition from dietary peptides at PepT1 [2, practitioner_protocol]. A common titration is start **200 mcg/day** for week 1, increase to **500 mcg** if tolerated [1, practitioner_protocol].
- A wider band of **500 mcg up to 1 mg/day** is cited for higher-burden gut contexts; some research-planning protocols extend to **1,000 mcg/day** at the upper end [1, practitioner_protocol][2, practitioner_protocol].
- Capsule products on the market are sold at **250 mcg or 500 mcg per capsule** (e.g., 500 mcg/cap, 30-count bottles), and sublingual-spray/troche formats deliver **~500–600 mcg/dose** [4, vendor_label][6, vendor_label][7, vendor_label].

**Subcutaneous (SC injectable — gray-market).** SC is the convention for *systemic* anti-inflammatory framing; it is the lower-dose channel because it bypasses GI degradation [1, practitioner_protocol][2, practitioner_protocol]. The recurring SC convention:
- **200–500 mcg once daily** [1, practitioner_protocol][3, practitioner_protocol(Campbell)]. A phased version: initiation **200 mcg/day** (wk 1–2) → titrate **300–400 mcg/day** (wk 3–4, +~100 mcg/week) → maintenance **400–500 mcg/day** (wk 5–12) [2, practitioner_protocol].
- Upper-band research-planning protocols quote up to **1,000 mcg/day** [2, practitioner_protocol].
- **SC KPV is gray-market**: it is supplied as "research"/vendor vials, not as an FDA-approved or settled-compounded injectable (see regulatory state and §data-sheet gate). Parenteral routes also sit in the higher-immunogenicity-risk bucket than oral.

**Topical (cosmetic / derm).** Topical is the convention for **localized skin inflammation** (the framings seen are psoriasis and cystic acne) [3, practitioner_protocol(Campbell)][2, practitioner_protocol].
- Convention 1 — **cream/serum at 0.01–0.1% KPV**, applied **twice daily** to affected areas [1, practitioner_protocol].
- Convention 2 — a per-application figure of **~7.5 mg applied twice daily** (i.e., a *milligram* topical load, consistent with a cream concentration rather than a systemic dose) [3, practitioner_protocol(Campbell)].
- Topical courses are run **1–2×/day over 4–8+ weeks**; exact concentration varies by the compounding formulation [2, practitioner_protocol].

> **There is no validated human dose-finding study behind any of these numbers.** No published human Phase 2/3 dose-ranging trial for KPV exists, so every figure here is a *convention* extrapolated from preclinical (cell/animal) protocols and clinical/community anecdote, not an established therapeutic dose [2, practitioner_protocol].

## Named-prescriber protocols (practitioner_protocol — name + venue + date)

1. **Jay Campbell — "KPV Peptide Benefits, Side Effects & Dosage."** Venue: **JayCampbell.com**; medical reviewer **Dr. Michael Fortunato, MD**; **last updated 2026-04-29** [3, practitioner_protocol]. Stated by route, verbatim:
   - **Oral:** "Two 250 mg capsules taken with or without food, until your ailment is healed"; "Doses can be as high as 2000 mg per day depending on the condition being treated." → **UNIT CAVEAT, see below.**
   - **SC:** "200-500 mcg injected once a day" (systemic inflammation).
   - **Topical:** "7.5 mg applied to the affected area twice a day" (psoriasis, cystic acne).
   - Onset note: "Allow 3-4 weeks before expecting significant changes."

   > **⚠ Campbell mg/mcg unit caveat (load-bearing).** The Campbell page's **oral** figures — "**250 mg** capsules" and "up to **2000 mg per day**" — are an **apparent milligram/microgram unit error**. They are internally inconsistent with (a) Campbell's *own* SC figure on the same page ("200–500 **mcg**"), a ~1000× gap, and (b) every other oral KPV source located, which dose oral KPV at **250–500 mcg per capsule** and **500 mcg–1 mg/day** [1,2,4,5,6,7]. mg↔mcg confusion is a known 1000× peptide overdose vector. **Read Campbell's oral "mg" as "mcg."** The SC ("mcg") and topical ("7.5 mg" cream load) figures are internally plausible and are not flagged. This caveat is recorded so the error is *not* propagated downstream.

2. **Dr. Tyna Moore, ND, DC — interview, "What Women Need to Know About GLP-1 Microdosing, Peptides, Gut Health, and Hormonal Optimization."** Venue: **draliabadi.com** (THAIS ALIABADI MD blog), interview article from the *SHE MD* video; **dated 2026-03-09** [10, practitioner_protocol]. KPV appears here only as "an anti-inflammatory peptide available in supplement forms," named in the **gut-repair / mucosal-integrity** context; **no specific KPV dose, route, or cycle number is given** on this source.
   - **Pairing discipline (load-bearing — do NOT misattribute):** On this same source, the pairing Dr. Moore states is **"TB500 — often paired with BPC-157 for regenerative and anti-inflammatory effects."** She does **NOT** pair KPV with BPC-157. Any "KPV + BPC-157" combination must **not** be sourced to Moore/draliabadi. (A *separate* retail liposomal "BPC + KPV" product exists from Quicksilver, but that is a vendor formulation, unrelated to Moore's statement.)

3. **Dr. Sobo (Stamford, CT clinic) — "KPV Peptide Therapy for Gut Health," drsobo.com.** Listed for completeness as a named clinic offering KPV for gut health; the page was **HTTP 403 / not directly fetchable** at access time, so **no verbatim dose is recorded here** rather than fabricated [11, practitioner_protocol — unfetched].

4. **Bowery Clinic — "KPV," boweryclinic.com.** Clinic-prescribed **sublingual troche, 600 mcg**, "place under your tongue or between cheek and gum and let it fully dissolve"; cartridge "lasts approximately 30 days"; frequency "will change over time based on your goals and your provider's evaluation" [6, practitioner_protocol/vendor_label]. (This page *does* cite 3 primary papers, but it is used here only for the dose/route convention, never for efficacy.)

5. **Society / certification channel (A4M / SSRP / International Peptide Society).** A4M and SSRP run a **Peptide Therapy Certification** restricted to licensed practitioners (A4M or International Peptide Society membership required), with faculty case studies; KPV is covered in that curriculum. **No single named KPV dose/cycle from a certification handout was extractable from public pages** (gated content) — recorded as a *channel that exists* rather than a sourced protocol, to avoid fabrication [12, practitioner_protocol — channel only].

## Compounding data sheets (compounding_data_sheet) — gate result

**Gate finding: NO admissible compounding-pharmacy *clinical data sheet* (a pharmacy-issued monograph whose dose/route/indication claims cite their primary literature) was located for KPV.** This is reported honestly rather than papered over, and is consistent with the regulatory state: KPV has **no USP/NF monograph** and **no FDA-approved labeling**, and was only just removed from 503A Category 2 (nomination withdrawn) without being added to the authorized-bulks list, so there is no standardized clinical monograph for a 503A pharmacy to publish [8, practitioner_protocol]. Specifically:

- **Empower Pharmacy — does NOT list KPV** among its compounded peptides at all (its named peptide line is GHK-Cu, sermorelin, gonadorelin, semaglutide, tirzepatide). No KPV product, strength, or data sheet exists there [13, vendor_label].
- **Compounding Pharmacy of America — "KPV Ultra Oral Spray,"** 500 mcg α-MSH-fragment per formulation, peppermint liquid spray, "**two sprays once per day**." This is a **vendor product page with NO primary scientific references cited** → admissible only as `vendor_label` (dose-format), **not** as a clinical data sheet [7, vendor_label].
- **Tailor Made Compounding** — KPV described as a prescription-only compounded oral capsule (oral/topical 1–5 mg/day range referenced; 500 mcg/cap example), with the explicit note "no universal protocol exists; clinicians tailor dosing." **No citation-bearing clinical monograph** located → `vendor_label` only [4, vendor_label].
- **Hallandale, Belmar Pharma Solutions / APS Pharmacy, Strive** — searched; **no public KPV clinical monograph or data sheet** located. (Belmar/APS additionally carries a 2023 FDA warning letter re: compounding from ineligible bulk substances lacking USP/NF monographs — reinforcing that no KPV monograph exists to publish.) [9, practitioner_protocol]

**Vendors / pharmacies / source classes searched for an admissible data sheet** (none yielded a citation-bearing clinical data sheet): **Empower** (no KPV product at all), **Tailor Made Compounding** (vendor capsule, no monograph), **Hallandale**, **Belmar Pharma Solutions / APS Pharmacy**, **Strive**, **Compounding Pharmacy of America** (KPV Ultra spray, no references), plus generic compounding "monograph / fact sheet / data sheet / reconstitution" PDF queries and "KPV compounding" finder directories. **Result: explicit absence — no admissible compounding data sheet located.** The 8.5 gate is satisfied by this explicit-absence finding plus the searched-vendor list.

## Reconstitution / formulation notes (purity/dilution arithmetic only)

Injectable KPV is dispensed/sold as a **lyophilized powder** (commonly **10 mg vials**; also 5 mg / mixed-strength research vials) reconstituted with **bacteriostatic water** (sterile water + 0.9% benzyl alcohol) and stored refrigerated; conventions cite room-temp storage "away from light and humidity" for some finished products [1, vendor_label][3, vendor_label]. The arithmetic that recurs (admissible as reconstitution math only):

| Vial | + Bac. water | Concentration | Dose | Volume | On U-100 |
|------|--------------|---------------|------|--------|----------|
| 10 mg | 2 mL | 5,000 mcg/mL | 200 mcg | 0.04 mL | 4 U [2, practitioner_protocol] |
| 10 mg | 2 mL | 5,000 mcg/mL | 300 mcg | 0.06 mL | 6 U [2, practitioner_protocol] |
| 10 mg | 2 mL | 5,000 mcg/mL | 500 mcg | 0.10 mL | 10 U [2, practitioner_protocol] |

Convention note: a **lower concentration → larger draw volume → better precision** for microgram-level dosing on a U-100 insulin syringe [2, practitioner_protocol]. Oral capsules are filled at **250 or 500 mcg/cap**; sublingual sprays/troches at **~500–600 mcg/dose**; topicals are compounded to a **% concentration (0.01–0.1%)** rather than a per-dose mcg figure [1,4,6,7]. This is all route/strength bookkeeping only and carries **no efficacy or safety implication**.

## Bibliography (own; tag + tier)

1. **"KPV Peptide Dosing Guide: Gut Health, Protocol & Safety (2026)," peptidedosingprotocols.com** — https://www.peptidedosingprotocols.com/protocol/kpv — `practitioner_protocol` (2.7) / partial `vendor_label` (4). Used for oral 200–500 mcg titration, topical 0.01–0.1% cream, reconstitution/storage conventions. *(Aggregator; used for dose/route/reconstitution conventions only, never efficacy.)*
2. **"KPV Dosing Guide / Protocol," peptidedosingprotocols.com (protocol page, fetched)** — same host, fetched 2026-06-19 — `practitioner_protocol` (2.7). Used for oral/SC/topical bands, phased SC titration, cycle protocols (4–8 wk on / 2–4 wk off; extended 8–16/4–8; pulsed 4/2), and the 10 mg + 2 mL → 5,000 mcg/mL reconstitution table.
3. **Jay Campbell — "KPV Peptide Benefits, Side Effects & Dosage."** https://jaycampbell.com/gut-health/kpv-the-anti-inflammatory-peptide/ — `practitioner_protocol` (2.7). Author Jay Campbell; medical reviewer **Dr. Michael Fortunato, MD**; **last updated 2026-04-29**. Oral "250 mg cap / 2000 mg/day" (**flagged mg→mcg unit error**), SC "200–500 mcg/day," topical "7.5 mg twice daily." Dose/route conventions only.
4. **Tailor Made Compounding — KPV oral capsule** (via product/aggregator pages, incl. bhrcenter "KPV ORAL" 500 mcg/cap example) — `vendor_label` (4). Oral 500 mcg/cap; 1–5 mg/day oral/topical range; "no universal protocol." Dose-format only; **no clinical monograph**.
5. **"KPV Dosage Calculator and Chart," peptides.org** — https://www.peptides.org/kpv-dosage-calculator/ — `practitioner_protocol` (2.7) aggregator. PepT1-mediated oral uptake convention; oral-vs-SC channel split. Conventions only.
6. **Bowery Clinic — "KPV," boweryclinic.com** — https://boweryclinic.com/kpv — `practitioner_protocol` (2.7) / `vendor_label` (4). **600 mcg sublingual troche**, dissolve buccally, ~30-day supply. Dose/route only (page's 3 primary cites NOT used for efficacy here).
7. **Compounding Pharmacy of America — "KPV Ultra Oral Spray"** — https://compoundingrxusa.com/product/kpv-ultra-oral-spray/ — `vendor_label` (4). 500 mcg α-MSH fragment, peppermint spray, "two sprays once per day." **No references cited → not a clinical data sheet.**
8. **Orrick — "FDA Announces Removal of 12 Peptides from Category 2 and Schedules PCAC Meetings…"** — https://www.orrick.com/en/Insights/2026/04/FDA-Announces-Removal-of-12-Peptides-from-Category-2-and-Schedules-PCAC-Meetings — `practitioner_protocol` (2.7, regulatory). KPV removed from Category 2 (~April 2026, nomination withdrawn); PCAC 23–24 July 2026 to consider KPV acetate / KPV free base for 503A bulks. Regulatory status only.
9. **FDA warning letter — Belmar Pharma Solutions / APS Pharmacy (653740, 2023-03-31)** — https://www.fda.gov/.../belmar-pharma-solutions-drug-depot-llc-dba-aps-pharmacy-653740-03312023 — `practitioner_protocol` (2.7, regulatory). Cited only for the principle that drug products compounded from bulk substances lacking USP/NF monographs are not 503A-eligible — corroborates "no KPV monograph." Regulatory only.
10. **Dr. Tyna Moore interview — draliabadi.com (THAIS ALIABADI MD), 2026-03-09** — https://www.draliabadi.com/blog/glp1-microdosing-peptides-gut-health-women-guide/ — `practitioner_protocol` (2.7). KPV named for gut-repair/mucosal integrity (no specific dose); pairing on this source is **TB-500 + BPC-157**, NOT KPV. Used for naming + the non-pairing fact only.
11. **Dr. Sobo — "KPV Peptide Therapy for Gut Health," drsobo.com (Stamford, CT)** — https://drsobo.com/peptides/kpv/ — `practitioner_protocol` (2.7) **— UNFETCHED (HTTP 403)**. Listed as an existing named-clinic channel; no verbatim dose recorded (not fabricated).
12. **A4M / SSRP / International Peptide Society — Peptide Therapy Certification** — https://www.a4m.com/peptide-therapy-certification-on-demand-2026.html ; https://ssrpinstitute.org/courses/peptide-therapy-certification-2025/ — `practitioner_protocol` (2.7) **— channel only**, gated; no single KPV dose/cycle extractable from public pages.
13. **Empower Pharmacy — peptide line ("Expanding Access: Peptides")** — https://www.empowerpharmacy.com/expanding-access-peptides/ — `vendor_label` (4). Cited for the **negative** finding: **KPV is NOT among Empower's compounded peptides**. Availability/absence only.

## Self-check

**No efficacy on these tiers.** Every figure above is a dose/route/cycle/reconstitution *convention* or a regulatory-status fact, tagged `practitioner_protocol` (2.7), `compounding_data_sheet` (3 — none found), or `vendor_label` (4). **No efficacy claim is grounded on any source here**; the efficacy state lives in the KPV research report. Sources that *do* carry primary citations (Bowery's 3 papers; aggregator references) were used **only** for dose/route conventions, never for efficacy.

**Practitioners cite name + venue + date.** Campbell (JayCampbell.com, reviewer Fortunato MD, 2026-04-29 ✓); Tyna Moore (draliabadi.com, 2026-03-09 ✓); Bowery Clinic (boweryclinic.com ✓); Dr. Sobo (drsobo.com, Stamford CT — listed but **unfetched/403**, no dose claimed); A4M/SSRP/IPS (certification channel, gated — no dose claimed).

**Unit-error caveat carried.** Campbell's oral "250 mg / 2000 mg/day" is flagged as an apparent **mg→mcg unit error** (1000× inconsistent with his own SC mcg figure and with all other oral sources) and is **not propagated**.

**No KPV-BPC-157 pairing fabrication.** The draliabadi/Moore source pairs **TB-500 with BPC-157**, not KPV. No KPV+BPC-157 pairing is asserted from that (or any) source; the only "BPC + KPV" artifact noted is a separate retail liposomal supplement, explicitly distinguished.

**Data-sheet requirement satisfied (explicit absence).** **No admissible compounding data sheet located.** Searched vendors/pharmacies: Empower (no KPV product at all), Tailor Made Compounding, Hallandale, Belmar / APS Pharmacy, Strive, Compounding Pharmacy of America (KPV Ultra spray — no references), plus generic monograph/fact-sheet/reconstitution PDF queries and compounding-finder directories. Consistent with no USP/NF monograph, no FDA labeling, and post-Category-2-removal-but-not-on-bulks-list status pending the 23–24 July 2026 PCAC vote. Treat all availability as transient and jurisdiction-dependent; SC KPV is gray-market.
