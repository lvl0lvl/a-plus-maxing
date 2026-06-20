---
title: CJC-1295 — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/cjc-1295/practitioner-layer
class: peptide
layer: prescribing-practice
scope: dose/cycle/route/reconstitution conventions ONLY — NOT efficacy
created: 2026-06-20
last_verified: 2026-06-20
---

# CJC-1295 — Prescribing-Practice Layer

> **Scope discipline.** This document records *how CJC-1295 is actually prescribed, compounded, dosed, and reconstituted in practice* — the dose/cycle/route/reconstitution conventions that circulate among prescribers, peptide clinics, and compounding/vendor channels. It is **not** an efficacy document and **must not** be read as one. Per the source-tagging rule, `practitioner_protocol`, `compounding_data_sheet`, and `vendor_label` sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/reconstitution math. **None** of these source classes grounds an efficacy or adverse-event-rate claim, and none appears here for that purpose. The efficacy state (one biomarker-only human Phase 1 study; one terminated efficacy trial with no posted results; no human efficacy endpoint ever met) lives in [[library/peptides/cjc-1295/research-report]] and is unaffected by anything below.
>
> **The two-molecule rule, read first.** "CJC-1295" denotes **two** distinct molecules whose dosing conventions are **never cross-attributed**: **WITH DAC** (Drug Affinity Complex; albumin-binding; multi-day half-life → once-weekly milligram dosing) and **WITHOUT DAC = "Modified GRF 1-29"** (~30-min half-life → daily-microgram pulsatile dosing, stacked with ipamorelin). The once-weekly milligram convention belongs **ONLY** to the DAC form; the daily-microgram convention belongs **ONLY** to the no-DAC form.
>
> **Regulatory state, read first.** As of mid-2026 CJC-1295 is **not an FDA-approved drug for any indication** and is **not on the FDA 503A authorized-bulks (positive) list**. At the **4 December 2024** Pharmacy Compounding Advisory Committee (PCAC) meeting the committee **voted AGAINST** adding CJC-1295 to the positive list, and CJC-1295 was **NOT** among the twelve peptides removed from interim 503A Category 2 by the April 2026 FDA action — it remains non-compoundable. (Whether it is best described as "still in interim Category 2" or as sitting in an unclassified regulatory gap diverges across trackers; the firmly-established fact is that it is not eligible for routine 503A compounding.) So the "prescribing practice" described here is a real but legally unsettled gray-market / telehealth / vendor-research practice, not an approved standard of care. Regulatory detail is owned by the research report §7 — cited here as status context only, never to ground a practice claim.

## Dose/route conventions (DAC vs no-DAC — kept strictly separate)

CJC-1295 is dosed across **two distinct conventions** that track the two molecules. The unit conventions differ by ~1000× in per-dose mass and by orders of magnitude in frequency, which is exactly where the dosing-error and mislabeling risk lives.

**CJC-1295 WITH DAC** (long-acting, albumin-binding via the Drug Affinity Complex; multi-day half-life). The dominant practice convention reported across vendor and protocol sources:
- **~1–2 mg subcutaneously once weekly** (some sources extend to 2 mg/week split into one or two injections), with **timing-of-day treated as non-critical** because of the long half-life [4, vendor_label]. Route/frequency framing only — **NOT** an efficacy claim.
- A compounding-industry guide (503Pharma) frames it more conservatively as **"100–300 mcg subcutaneously 1–3 times weekly (with DAC)"** [3, compounding_data_sheet]. This is a lower/more conservative figure than the dominant ~1–2 mg/week vendor convention; the divergence is **reported as-is and not reconciled**, because practice sources do not ground a numeric "correct dose."

**CJC-1295 WITHOUT DAC = "Modified GRF 1-29"** (~30-minute half-life). The recurring practice convention:
- **~100 mcg (range 100–300 mcg) subcutaneously, dosed 1–3× per day**, classically **before bed and ≥2 h after the last meal**, and **stacked with ipamorelin** in the dominant commercial "CJC-1295/ipamorelin" blend [1, compounding_data_sheet][3, compounding_data_sheet].
- The historical Tailor Made Compounding monograph instruction — **0.10 mL SC 5 of 7 nights per week before bedtime on an empty stomach**, with a suggestion to combine with ipamorelin — is consistent with this no-DAC convention [1, compounding_data_sheet].

> **Cross-attribution prohibition (load-bearing).** The once-weekly **milligram** dosing belongs ONLY to the **DAC** form; the daily-**microgram** pulsatile dosing belongs ONLY to the **no-DAC / Mod-GRF** form. Vendor mislabeling — selling "Mod GRF 1-29" as "CJC-1295 without DAC" while quoting the DAC dosing or half-life — is documented and is both a regulatory gray zone and a product-identity/safety hazard. The compounding guide's individualization note ("1–2 mcg/kg, lower for elderly, titrate based on IGF-1") is recorded as convention only [3, compounding_data_sheet].

> **There is no validated human dose-finding study behind any of these numbers.** No published human Phase 2/3 dose-ranging trial for CJC-1295 (either form) exists; the only efficacy-powered trial was terminated. Every figure here is a *convention* extrapolated from vendor/compounding practice, not an established therapeutic dose.

## Named-prescriber protocols (practitioner_protocol — name + venue + date)

**Gate finding: NO named-prescriber primary source with a verifiable name + venue + date was located for CJC-1295.** Targeted searches surfaced only secondary clinic blogs that re-state the conventions above. Per the practitioner-layer attribution bar (every `practitioner_protocol` cite must carry name + venue + date), **no `practitioner_protocol` claim is asserted here** — an honest "not located with sufficient attribution" result rather than a citation to an unattributable secondary blog.

## Compounding data sheets (compounding_data_sheet) — gate result

**Gate finding: ONE historical compounding monograph located, flagged pre-restriction/withdrawn; no admissible *current* compounding data sheet.**

- **Tailor Made Compounding (TMC) — CJC-1295 monograph** [1, compounding_data_sheet]. Compounded injectable: dose form **2000 mcg/mL SC injection in a 2 mL vial**, purity **>98% (HPLC on request)**, molecular weight **3647.15**, molecular formula **C165H269N47O46**; suggested administration **0.10 mL SC 5 of 7 nights per week before bedtime on an empty stomach**, with a stated suggestion to combine with ipamorelin. The 2000 mcg/mL strength and per-night before-bed/empty-stomach instruction are consistent with the **no-DAC / Modified GRF 1-29** convention, NOT the once-weekly DAC convention. **Caveat (load-bearing):** TMC received an **FDA warning letter (04/01/2020)** and CJC-1295 was subsequently swept into 503A Category 2, so this monograph reflects a **historical / pre-restriction** offering, not a currently broadly available product [2, compounding_data_sheet].
- **503Pharma compounding guide** — "CJC-1295: The Complete Guide for Compounding Pharmacies" [3, compounding_data_sheet]. Describes the compounded dose-form envelope (see Reconstitution below) and the DAC-vs-no-DAC dosing framing. Industry guide, used for dose-form/reconstitution conventions only.
- **Empower and other major compounding pharmacies** — several no longer surface a public CJC-1295 monograph, **consistent with post-Category-2 withdrawal**. Reported as an observed absence, not a verified efficacy/safety finding.

**Result:** the only located compounding monograph is the **historical TMC sheet (pre-restriction/withdrawn)**; no admissible current compounding data sheet exists. This is consistent with no USP/NF monograph, no FDA labeling, and non-compoundable 503A status.

## Reconstitution / formulation notes (vendor/compounding math only)

Compounded dose-form envelope (503Pharma) [3, compounding_data_sheet]: injectable solutions **2–5 mg/mL** reconstituted with bacteriostatic water; lyophilized powder **2–10 mg/vial**; diluent/excipient **bacteriostatic water + mannitol**; pH **5–7**; reconstituted solutions **stable ~28 days refrigerated**; ipamorelin co-formulation noted; formulations described as lasting 14–28 days.

Vendor reconstitution math (numbers-as-math only, NOT evidence) [5, vendor_label]:

| Vial | + Bac. water | Concentration | Dose | Volume | On U-100 |
|------|--------------|---------------|------|--------|----------|
| 2 mg | 2 mL | 1 mg/mL | 100 mcg | 0.10 mL | 10 U |
| 5 mg | 2.0 mL | 2.5 mg/mL | 25 mcg | 0.01 mL | 1 U |
| 5 mg (no-DAC) | 2.5 mL | 2 mg/mL | 100 mcg | 0.05 mL | 5 U |

Standard handling: inject diluent slowly down the vial wall, swirl (do not shake), refrigerate at 2–8 °C, use within ~4 weeks [5, vendor_label]. These figures are gray-market vendor math and carry **no efficacy or purity assurance**.

## Bibliography (own; tag + tier)

1. **Tailor Made Compounding, Peptide Catalog — CJC-1295 monograph** (compounded injectable data sheet; 2000 mcg/mL, 2 mL vial; MW 3647.15; formula C165H269N47O46; >98% HPLC on request; 0.10 mL SC 5/7 nights before bed, empty stomach; combine-with-ipamorelin suggestion). Accessed via catalog mirror / search extraction. `compounding_data_sheet`. Used for the no-DAC dose-format/identity conventions only; **pre-restriction offering**.
2. **FDA, Warning Letter — Tailor Made Compounding LLC (594743), 04/01/2020** — CJC-1295 named among compounded products; basis for subsequent 503A Category 2 inclusion. `compounding_data_sheet` (regulatory context). Used only to flag the TMC monograph as pre-restriction.
3. **503Pharma, "CJC-1295: The Complete Guide for Compounding Pharmacies in 2025/2026,"** dated 19 June 2026 — https://503pharma.com/peptides/cjc-1295-the-complete-guide-for-compounding-pharmacies-in-2025 . `compounding_data_sheet`. Dose forms (2–5 mg/mL; 2–10 mg/vial), reconstitution (BAC water + mannitol, pH 5–7, 28-day stability), DAC-vs-no-DAC dosing framing (100–300 mcg 1–3×/week with DAC; daily without DAC; 1–2 mcg/kg individualized), ipamorelin co-formulation. Conventions only.
4. **Vendor/practice dosing convention for CJC-1295 WITH DAC** (~1–2 mg SC once weekly; timing non-critical) — gray-market vendor/protocol consensus, route/frequency only. `vendor_label`.
5. **Reconstitution math** (2 mg → 1 mg/mL; 5 mg + 2 mL → 2.5 mg/mL; 5 mg + 2.5 mL → 2 mg/mL; U-100 unit conversions; swirl/refrigerate handling) — vendor reconstitution guides. `vendor_label`. Math only, no purity/efficacy assurance.

> Regulatory status (PCAC vote 4 Dec 2024; not among the 12 removed Apr 2026; WADA S2.2.4) is owned by [[library/peptides/cjc-1295/research-report]] §7 and is referenced here as status context only, not to ground any practice claim.

## Self-check

**No efficacy / AE-rate on these tiers.** Every figure above is a dose/route/cycle/reconstitution *convention* or a regulatory-status fact, tagged `practitioner_protocol`, `compounding_data_sheet`, or `vendor_label`. **No efficacy claim and no adverse-event-rate claim is grounded on any source here**; the efficacy/safety state lives in the research report.

**DAC vs no-DAC never cross-attributed.** Once-weekly milligram dosing is attributed ONLY to the DAC form; daily-microgram pulsatile dosing (with ipamorelin) ONLY to the no-DAC / Mod-GRF form. The mislabeling hazard is flagged.

**Named-prescriber gate (name + venue + date).** No source meeting the bar was located → **no `practitioner_protocol` claim asserted** (honest "not located with sufficient attribution"), rather than citing an unattributable secondary blog.

**Compounding-data-sheet gate.** ONE monograph located — Tailor Made Compounding — **flagged pre-restriction/withdrawn** (FDA warning letter 04/01/2020; subsequent 503A Category 2). Empower and other major pharmacies no longer surface a public CJC-1295 monograph (observed absence). No admissible current data sheet. Gate satisfied by the historical-monograph finding plus the explicit-absence observation.

**Reconstitution = math only.** All reconstitution/dose-volume figures are vendor/compounding arithmetic with no purity or efficacy assurance; SC CJC-1295 (both forms) is gray-market. Treat all availability as transient and jurisdiction-dependent.
