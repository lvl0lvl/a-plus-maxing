# Section G — Concentration Audit + Sourcing + Prescribing (KPV)

Target: **KPV (Lys-Pro-Val; α-MSH(11–13))**. Owner: Section G — concentration/lab-provenance audit + sourcing + prescribing practice. Mode: DEEP.
Scope discipline: efficacy claims are grounded ONLY on Tier ≤2 primaries (animal/in_vitro/regulatory). Tier 2.7 practitioner_protocol and vendor_label sources are used for dose/route/sourcing ONLY, never efficacy.

---

## Concentration audit (dominant labs; estimated single-lab share + method)

**Method.** I enumerated the *in-vivo efficacy primaries* for KPV that are retrievable with a verifiable citation (PMID/DOI), then attributed each to its senior/corresponding lab. "Single-lab share" = (in-vivo efficacy primaries from the dominant lab) / (total enumerated in-vivo efficacy primaries). I report two denominators because the literature splits cleanly into an IBD/gut track and a small non-gut track, and the dominant-lab share is sensitive to which you count.

**Enumerated in-vivo efficacy primaries (verified):**

| # | Citation | Senior lab / institution | In-vivo model |
|---|----------|--------------------------|---------------|
| P1 | Dalmasso et al. 2008, *Gastroenterology*, PMID 18061177 | **Merlin — Georgia State U / Atlanta VA** | DSS + TNBS colitis (mouse) |
| P2 | Viennois et al. 2016, *Cell Mol Gastroenterol Hepatol*, PMID 27458604 | **Merlin — Georgia State U** | colitis-associated cancer (AOM/DSS, mouse) |
| P3 | Xiao et al. 2017, *Molecular Therapy*, PMID 28143741 | **Merlin — Georgia State U** (Xiao corresp., Southwest U co-lead) | DSS ulcerative colitis (mouse), HA-NP-delivered |
| P4 | Kannengiesser et al. 2008, *Inflamm Bowel Dis*, PMID 18092346 | Kucharzik/Luger — U Münster, Germany (**independent**) | DSS + CD45RB-hi transfer colitis (mouse) |
| P5 | Bonfiglio et al. 2006, *Exp Eye Res*, PMID 16965771 | Drago — U Catania, Italy (**independent**) | corneal epithelial wound healing (rabbit) |
| P6 | Cutuli et al. 2000, *J Leukoc Biol*, DOI 10.1002/jlb.67.2.233, PMID 10670585 | Catania/Lipton α-MSH lineage (**independent of Merlin**) | antimicrobial vs *S. aureus* / *C. albicans* (in-vivo + in-vitro) |

**Estimated single-lab share.**
- **All-cause in-vivo efficacy primaries (N=6):** Merlin/Georgia State = **3/6 ≈ 50%**.
- **IBD/gut-inflammation in-vivo efficacy primaries (N=4: P1–P4):** Merlin/Georgia State = **3/4 ≈ 75%** → **FLAG: ≥70% single-lab concentration within the gut/IBD efficacy literature** that practitioner and vendor claims most lean on.

**Dominant group(s):**
1. **Didier Merlin lab (Georgia State University Institute for Biomedical Sciences / Atlanta VA)** — the modern KPV-efficacy engine. It established the central mechanistic claim (KPV anti-inflammatory effect is **PepT1-mediated, MCR-independent**) and authored the colitis, colitis-associated-cancer, and oral-nanoparticle-delivery primaries. Recurrent co-authors form a tight cluster (Dalmasso, Viennois, Xiao, Laroui, Charrier-Hisamuddin, Sitaraman).
2. **Catania/Lipton α-MSH lineage** — the *origin* lineage. James M. Lipton & Anna Catania (1980s–2000s, Weill Cornell / Italy) identified KPV as the minimal anti-inflammatory/antipyretic message of α-MSH and hold the foundational US patents (US 5,028,592 [1991]; US 5,157,023 [1992]). The Italian Catania/Drago axis (U Catania) also produced the independent antimicrobial (Cutuli 2000) and corneal (Bonfiglio 2006) primaries.

**Provenance caveat.** Because the gut/IBD efficacy base is ~75% one lab, the strongest KPV efficacy narrative (oral, PepT1-targeted, IBD) rests heavily on a single group whose findings have **not been independently reproduced in humans** and have limited cross-lab in-vivo replication outside the shared mechanism. The independent primaries (Münster IBD; Catania antimicrobial/corneal) corroborate the *direction* of effect but in different models and at different concentrations — they reduce, but do not eliminate, single-lab concentration risk.

---

## Sourcing landscape (cosmetic/oral/injectable; purity caveats) [N, tag]

**1. Cosmetic / topical (oldest legitimate channel).**
- KPV has a documented cosmetic-use lineage: **L'Oréal patent WO2003002087A1** (inventor Y. Mahé; priority 2001, pub. 2003) claims KPV for epidermal renewal and superficial cutaneous micro-repair at **10⁻¹²–10⁻³ M (preferred 10⁻⁹–10⁻⁴ M)** in cosmetic compositions. [S7, regulatory(patent)] — purity/formulation only, NOT efficacy.
- A US dermatological-use patent **US6894028B2** ("Use of KPV tripeptide for dermatological disorders") sits alongside the Lipton anti-inflammatory composition patents. [S8, regulatory(patent)]
- Transdermal/iontophoretic delivery of KPV across microporated human skin has been formulated and characterized (J Pharm Sci, Boddu/Vaka-type work). [S9, in_vitro] — delivery characterization only.

**2. Oral / compounded (clinical-adjacent channel).**
- KPV's best-supported route mechanistically is **oral**, because uptake is **PepT1-mediated** in inflamed gut epithelium (Dalmasso 2008). [P1, animal]
- Compounded oral KPV exists in the US compounding ecosystem, but its legal status is contested (see regulatory note below). [S1/S5, regulatory]

**3. Research-chem gray-market (injectable — GRAY-MARKET FLAG).**
- KPV is sold widely online as a lyophilized "research only / not for human consumption" injectable powder (commonly **5 mg, 10 mg, 15 mg** vials) by numerous research-chemical vendors. This is an **unregulated gray-market channel**: KPV is **not an FDA-approved drug**, so injectable material from these vendors is research-grade and not established as fit for human use. [S2/S3, vendor_label — purity/reconstitution context only, gray-market flagged]
- **Purity/identity caveats:** vendors self-report HPLC ≥98–99% purity with optional COAs from third-party labs commonly named in this space (Janoshik Analytical, MZ Biolabs, Colmaric). These COAs are **vendor-commissioned, batch-specific, and not independently auditable at the buyer level**; absence of a public COA, sequence-identity confirmation by MS, and chain-of-custody are recurring gaps. Identity (is it actually Lys-Pro-Val and not a contaminant/diluent?) and endotoxin/sterility for an injectable are the principal unverifiable risks. [S2/S3, vendor_label]
- **Honest limit:** I did not retrieve any independent (non-vendor) assay survey of marketed KPV purity. Any purity figure cited by a seller should be treated as a self-report, not verified provenance.

---

## Prescribing-practice conventions (name+venue+date) [N, practitioner_protocol]

These are Tier 2.7 sources — used for **dose/route/cycle ONLY**, never efficacy. Each carries a name + venue + date.

- **Jay Campbell — JayCampbell.com, "KPV Peptide: Everything You Should Know" (medically reviewed by Dr. Michael Fortunato, MD; last-updated 29 Apr 2026).** States routes/doses: Oral "two 250 [mc]g capsules… up to 2000 [mc]g/day depending on condition"; Subcutaneous "200–500 mcg once a day"; Topical cream "7.5 mg applied to affected area twice a day"; expects 3–4 weeks before results. [S10, practitioner_protocol]
  - **Unit-error flag:** the oral figures are printed as "mg" (250 mg capsules, up to 2000 mg/day); given the SC range is in mcg and a 2000 mg/day oral tripeptide dose is implausible, this is almost certainly a **mg/mcg typo**. Do not propagate the mg figure without caveat.
- **Jay Campbell — "KLOW" stack content (JayCampbell.com, peptides section, 2024–2026).** KPV is described as the fourth component blended with BPC-157 + TB-500 + GHK-Cu in compounded multi-peptide vials. Route/composition only. [S11, practitioner_protocol]
- **Dr. Tyna Moore, ND, DC — interview, draliabadi.com blog "GLP-1 Microdosing, Peptides, Gut Health…" (2026-03-09).** Describes KPV as an anti-inflammatory peptide considered among the "least concerning for long-term use." Cycle/route framing only. [S12, practitioner_protocol]
- **Aggregator dosing pages** (peptides.org, peptidedossier.com, etc.) converge on **oral 200–500 mcg/day (up to ~1 mg)** and **SC 250–500 mcg 1–2×/day**, **4–8-week cycles**. These are **NOT named-practitioner/venue/date sources** — they are anonymous commercial aggregators, so they do NOT satisfy the Tier 2.7 name+venue+date bar and are cited here only to show consensus convergence, not as practitioner protocols. [S13, anecdote_aggregate]

**Convergent practice picture (route/dose only):** oral low-mcg for gut indications; SC 200–500 mcg/day for systemic; topical mg-scale for skin; short 2–8-week trials. No published human dose-finding study exists, so all of the above are convention/extrapolation, not evidence-based dosing.

---

## Regulatory note (sourcing-relevant; affects legal availability)

- KPV (free base **and** acetate) was placed by FDA in **Category 2** of the interim 503A bulk-drug-substances list in **2023** ("significant safety concerns" → not permitted for bulk compounding). [S1, regulatory]
- Per **RAPS (16 Apr 2026)** and FDA notices, KPV was **removed from Category 2** and scheduled for **Pharmacy Compounding Advisory Committee (PCAC) review on 23–24 Jul 2026** ("KPV-related bulk drug substances (free base and acetate) for wound healing and inflammatory conditions"). [S1/S5, regulatory]
- **Critical:** removal from Category 2 is **not** authorization to compound. KPV is **not** on the Category 1 / 503A Bulks List, so compounding remains at enforcement risk until affirmatively listed. This is the legal status as of the cited 2026 sources. [S5/S6, regulatory]

---

## Bibliography

**Efficacy primaries (Tier ≤2 — efficacy-eligible):**
- [P1] Dalmasso G, Charrier-Hisamuddin L, Nguyen HTT, Yan Y, Sitaraman S, Merlin D. "PepT1-mediated tripeptide KPV uptake reduces intestinal inflammation." *Gastroenterology*. 2008. PMID 18061177; DOI 10.1053/j.gastro.2007.10.026. tag=animal; tier=1; notes=Merlin/GSU; oral KPV 100 µM; DSS + TNBS colitis; foundational PepT1-mediated/MCR-independent claim.
- [P2] Viennois E, Merlin D, et al. "Critical Role of PepT1 in Promoting Colitis-Associated Cancer and Therapeutic Benefits of the Anti-inflammatory PepT1-Mediated Tripeptide KPV in a Murine Model." *Cell Mol Gastroenterol Hepatol*. 2016. PMID 27458604; DOI 10.1016/j.jcmgh.2016.01.006. tag=animal; tier=1; notes=Merlin/GSU; AOM/DSS CAC model; effect PepT1-dependent.
- [P3] Xiao B, Xu Z, Viennois E, Zhang Y, Zhang Z, Zhang M, Han MK, Kang Y, Merlin D. "Orally Targeted Delivery of Tripeptide KPV via Hyaluronic Acid-Functionalized Nanoparticles Efficiently Alleviates Ulcerative Colitis." *Molecular Therapy*. 2017. PMID 28143741; DOI 10.1016/j.ymthe.2016.11.020. tag=animal; tier=1; notes=Merlin/GSU + Southwest U; DSS colitis; KPV 16 µg/kg/day oral gavage in HA-NPs.
- [P4] Kannengiesser K, Maaser C, Heidemann J, Luegering A, Ross M, Brzoska T, Böhm M, Luger TA, Domschke W, Kucharzik T. "Melanocortin-derived tripeptide KPV has anti-inflammatory potential in murine models of inflammatory bowel disease." *Inflamm Bowel Dis*. 2008;14(3):324–331. PMID 18092346; DOI 10.1002/ibd.20334. tag=animal; tier=1; notes=INDEPENDENT (U Münster); DSS + CD45RB-hi transfer colitis; effect persists with nonfunctional MC1R.
- [P5] Bonfiglio V, Camillieri G, Avitabile T, Leggio GM, Drago F. "Effects of the COOH-terminal tripeptide α-MSH(11–13) on corneal epithelial wound healing: role of nitric oxide." *Exp Eye Res*. 2006;83(6):1366–1372. PMID 16965771. tag=animal; tier=1; notes=INDEPENDENT (U Catania); rabbit corneal wounds; KPV 1/5/10 mg/mL drops; effect blocked by L-NAME (NO-dependent).
- [P6] Cutuli M, Cristiani S, Lipton JM, Catania A. "Antimicrobial effects of α-MSH peptides." *J Leukoc Biol*. 2000;67(2):233–239. PMID 10670585; DOI 10.1002/jlb.67.2.233. tag=animal+in_vitro; tier=1; notes=Catania/Lipton lineage; KPV vs S. aureus & C. albicans incl. picomolar range; cAMP-linked.

**Sourcing / regulatory / patent (NOT efficacy):**
- [S1] FDA / RAPS coverage of 503A interim bulks list, KPV Category-2 placement (2023) and removal. tag=regulatory; tier=1; notes=via RAPS 2026-04-16.
- [S5] RAPS. "FDA considers adding a dozen peptides to its bulk drug compounding list." raps.org, 2026-04-16. URL https://www.raps.org/resource/fda-considers-adding-a-dozen-peptides-to-its-bulk-drug-compounding-list.html. tag=regulatory; tier=1; notes=KPV free base+acetate; PCAC 23–24 Jul 2026.
- [S6] FDA Category 2 removal / PCAC-review secondary coverage (Lexology / Sheppard Mullin "What to Watch: Status Update on Peptide Regulation"). tag=regulatory; tier=2; notes=corroborates not-yet-authorized status.
- [S7] L'Oréal SA (inventor Mahé Y). "Use of a lys-pro-val (KPV) tripeptide in cosmetics." WO2003002087A1; priority 2001-06-29, pub 2003-01-09. tag=regulatory(patent); tier=2; notes=cosmetic conc. 10⁻¹²–10⁻³ M; formulation only.
- [S8] "Use of KPV tripeptide for dermatological disorders." US6894028B2. tag=regulatory(patent); tier=2; notes=dermatological-use patent; formulation/IP only.
- [S9] Transdermal iontophoretic delivery of KPV across microporated human skin. *J Pharm Sci* (ScienceDirect S0022354917301740). tag=in_vitro; tier=2; notes=delivery characterization only, not efficacy.
- [S2] Research-chem vendor labels (e.g., Limitless Biotech, researchchemical.com, DL Peptides) — KPV 5/10/15 mg "research only." tag=vendor_label; tier=4; notes=GRAY-MARKET; purity/reconstitution only; self-reported ≥98–99% HPLC.
- [S3] Vendor COA practice (Janoshik / MZ Biolabs / Colmaric named by sellers). tag=vendor_label; tier=4; notes=vendor-commissioned, batch-specific, not buyer-auditable.

**Prescribing-practice (Tier 2.7 — dose/route ONLY):**
- [S10] Campbell J (med-reviewed Fortunato M, MD). "KPV Peptide: Everything You Should Know." JayCampbell.com, last-updated 2026-04-29. URL https://jaycampbell.com/gut-health/kpv-the-anti-inflammatory-peptide/. tag=practitioner_protocol; tier=2.7; notes=oral (mg/mcg unit-error flagged), SC 200–500 mcg/day, topical 7.5 mg 2×/day.
- [S11] Campbell J. "KLOW peptide protocol" (BPC-157+TB-500+GHK-Cu+KPV). JayCampbell.com peptides section, 2024–2026. tag=practitioner_protocol; tier=2.7; notes=composition/route only.
- [S12] Moore T (ND, DC), interview, draliabadi.com "GLP-1 Microdosing, Peptides, Gut Health…", 2026-03-09. URL https://www.draliabadi.com/blog/glp1-microdosing-peptides-gut-health-women-guide/. tag=practitioner_protocol; tier=2.7; notes=KPV among "least concerning for long-term use"; cycle/route framing only (source pairs TB-500—not KPV—with BPC-157).
- [S13] Aggregator dosing pages (peptides.org, peptidedossier.com, peptidedosingprotocols.com). tag=anecdote_aggregate; tier=3; notes=NOT name+venue+date; convergence reference only, not a practitioner protocol.

---

## Source tally (by tag) — RECOUNT vs enumerated; MUST match

Enumerated source IDs: P1, P2, P3, P4, P5, P6, S1, S2, S3, S5, S6, S7, S8, S9, S10, S11, S12, S13 = **18 source IDs**.

By tag (counting each ID's primary tag; P6 dual-tagged animal+in_vitro counted once under animal):
- animal: P1, P2, P3, P4, P5, P6 = **6**
- in_vitro: S9 = **1** (P6 also has in_vitro component — secondary, not double-counted)
- regulatory: S1, S5, S6 = **3**
- regulatory(patent): S7, S8 = **2**
- vendor_label: S2, S3 = **2**
- practitioner_protocol: S10, S11, S12 = **3**
- anecdote_aggregate: S13 = **1**

Sum = 6 + 1 + 3 + 2 + 2 + 3 + 1 = **18**. ✔ Matches enumerated count (18).

---

## Coverage gaps / honest limits

1. **No independent purity survey.** All purity/identity data for gray-market injectable KPV is vendor self-report; I found no third-party assay study of marketed KPV products. Identity, endotoxin, and sterility for injectable material are unverifiable from public sources.
2. **Single-lab concentration is real but framing-sensitive.** Merlin/GSU is 75% of the *gut/IBD* in-vivo efficacy primaries (FLAG) but ~50% of *all* in-vivo efficacy primaries. The number you quote depends on the denominator; I gave both with the method.
3. **No human efficacy or human dose-finding data exists.** Every prescribing convention is extrapolated from rodent/in-vitro work + practitioner experience; the entire dosing landscape is convention, not evidence.
4. **Practitioner sourcing is thin.** Only two genuinely name+venue+date practitioner sources (Campbell; Moore-via-Aliabadi) met the Tier 2.7 bar; both are wellness-industry, not peer-reviewed or institutional derm/GI. No academic dermatology or gastroenterology society guidance on KPV dosing exists (consistent with its non-approved status).
5. **Unit-error in the most-cited practitioner page** (Campbell oral mg vs mcg) shows how dosing misinformation can propagate; flagged but could not locate a corrected version.
6. **Regulatory status is in active flux** (PCAC review 23–24 Jul 2026); the Category-1/503A-Bulks outcome was undetermined as of the cited April 2026 sources.

## Post-fix grep audit

Remediation (citation_fidelity), verified via WebFetch before editing:

1. **Moore / draliabadi date** — source dateModified is **2026-03-09** (schema markup), not 2025.
   - OLD: `…Gut Health…" (2025).` / S12 `…Gut Health…", 2025.`
   - NEW: `…Gut Health…" (2026-03-09).` / S12 `…Gut Health…", 2026-03-09.`
2. **Moore / unsupported KPV+BPC-157 pairing** — source pairs **TB-500** with BPC-157, makes no KPV+BPC-157 claim. Quote: "TB500 — often paired with BPC-157 for regenerative and anti-inflammatory effects." KPV is listed separately ("among the least concerning for long-term use"). Unsupported assertion removed.
   - OLD (body): `…symptom monitoring, often paired with oral BPC-157 for mucosal repair.`
   - NEW (body): `…considered among the "least concerning for long-term use." Cycle/route framing only.`
   - OLD (S12 notes): `low starting dose, 10–14-day initial cycle, paired w/ oral BPC-157.`
   - NEW (S12 notes): `KPV among "least concerning for long-term use"; cycle/route framing only (source pairs TB-500—not KPV—with BPC-157).`
3. **Campbell title** — live H1 is **"KPV Peptide: Everything You Should Know"** (JayCampbell.com, reviewed by Fortunato MD, last-updated 2026-04-29). Doses + mg/mcg unit-error flag re-verified and retained.
   - OLD (body + S10): `"KPV: The Anti-Inflammatory Peptide"`
   - NEW (body + S10): `"KPV Peptide: Everything You Should Know"`

**Post-fix grep:** `grep "KPV: The Anti-Inflammatory"` → no hits; `grep "2025"` → no hits; `grep "paired.*BPC|BPC.*paired"` → no hits (line 59 KLOW stack mention is a legitimate stack-composition reference, not a Moore-sourced pairing claim). All three defect targets resolved. ✔

NO HALT.
