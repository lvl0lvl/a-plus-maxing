# Semaglutide — Verified-Source Ledger

Every citation + type-tag + verification status. FDA accessdata PDFs were not directly fetchable in this
environment (404/403); FDA-label claims are grounded in the **DailyMed label of record** (Wegovy setid
ee06186f-2aa3-4990-a760-757579d8f77b; Ozempic setid fdf509ac-7ae5-49be-9a3e-8465c76f38e1; Rybelsus
setid 27f15fac-7d98-4114-a2ec-92494a91da98) — flagged, not overstated.

## Mechanism / PK (Tier 1 / regulatory)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| GLP-1 analog 94% homology; glucose-dependent insulin/glucagon, gastric emptying; t½ ~1 wk | regulatory | FDA Ozempic label §12.1/§12.3 (DailyMed) | yes |
| Aib8 + Arg34 + C18-diacid acylation → albumin binding → once-weekly | mechanism_review | PMID 26308095 (Lau & Knudsen, J Med Chem 2015) | yes |
| Central appetite (area postrema/hypothalamus/NTS) | mechanism_review | PMC8820179 | yes |
| SC bioavailability ~89%; oral ~1% (SNAC); steady state 4–5 wk | regulatory/mechanism_review | FDA labels + PMC9272494 | yes |

## Efficacy (Tier 1)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| Obesity −14.9% vs −2.4% (n=1961, 68 wk) | rct | PMID 33567185 (STEP 1, NEJM 2021) | yes |
| Body comp: fat −19.3%, lean −9.7% absolute, ratio improves (n=140) | open_label (conf. abstract tier) | STEP 1 DEXA substudy, J Endocr Soc 2021;5(Suppl 1):A16 | yes (tier-limited — flagged) |
| Weight regain on withdrawal (+6.9%, wk 20→68) | rct | PMID 33755728 (STEP 4, JAMA 2021) | yes |
| T2D: HbA1c −1.1 to −1.4%; MACE HR 0.74 (0.58–0.95); retinopathy 3.0% vs 1.8% | rct | PMID 27633186 (SUSTAIN-6, NEJM 2016) | yes |
| CV: 3-pt MACE HR 0.80 (~20%) in non-diabetic CVD+obesity (n=17,604) | rct | PMID 37952131 (SELECT, NEJM 2023) | yes |
| CKD: major kidney events HR 0.76; −20% all-cause death | rct | DOI 10.1056/NEJMoa2403347 (FLOW, NEJM 2024) | yes |
| HFpEF: KCCQ +7.8, 6MWT +20.3 m | rct | DOI 10.1056/NEJMoa2306963 (STEP-HFpEF, NEJM 2023) | yes |
| MASH: resolution 62.9% vs 34.3% | rct | DOI 10.1056/NEJMoa2413258 (ESSENCE, NEJM 2025) | yes |

## Safety / Regulatory
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| Boxed thyroid C-cell/MTC; GI AE rates; pancreatitis/gallbladder/AKI/retinopathy/ileus/aspiration; contraindications | regulatory | FDA Wegovy + Ozempic labels (DailyMed) | yes |
| NAION a very rare effect (~1/10,000) | regulatory | EMA PRAC conclusion June 2025 | yes |
| NAION cohort HR 4.28 (T2D) / 7.64 (obese) | cohort | PMID 38958939 (JAMA Ophthalmol 2024) | yes |
| NOT WADA-prohibited — Monitoring Program (2026 list) | regulatory | WADA 2026 list + Monitoring Program | yes |
| FDA approvals: Ozempic 2017, Rybelsus 2019, Wegovy 2021 (+CV 2024), Ozempic CKD 2025; EMA 2018/2022 | regulatory | FDA approval history + EMA EPAR | yes |
| Shortage resolved Feb 21 2025; 503A wind-down Apr 22 2025, 503B May 22 2025; salt forms not approved API | regulatory | FDA shortage/compounding actions | yes (FDA HTML not machine-fetchable; corroborated across legal advisories + FDA index) |

## VERIFIED ABSENCES / catches
| Item | Result |
|---|---|
| RCT for lean-mass building / post-illness recovery | **NO ADMISSIBLE PRIMARY FOUND** (goal mismatch — it reduces lean mass) |
| Microdosing efficacy | **NO ADMISSIBLE PRIMARY (RCT) FOUND** — practitioner-tier only |
| Distinct non-English primary | **NONE** — global trials English-published |
| Vendor claim of "WADA S4 ban Jan 2026" | **EXCLUDED** — false (realpeptides.co); WADA primary says Monitoring Program, not prohibited |
| STEP 1 lean-mass figure | reported as absolute lean −9.7% with ratio improving — NOT the rosier "lean mass increased" secondary phrasing |
