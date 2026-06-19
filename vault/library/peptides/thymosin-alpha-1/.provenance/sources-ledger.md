# Thymosin Alpha-1 — Verified-Source Ledger

Every citation used, with type-tag + verification status. `VERIFIED:partial` = fact corroborated
across sources but a single authoritative primary could not be directly loaded (flagged, not overstated).

## Mechanism (Tier 1 / reviews)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| 28-aa N-acetyl fragment of prothymosin alpha (legumain cleavage) | in_vitro | PMID 24288480 (Liu 2013) | yes |
| DC maturation → Th1/IL-12 via MyD88/distinct-TLRs (specific TLR9/TLR2 attributed to the reviews, not this paper) | animal/in_vitro | PMID 14982877 (Romani, Blood 2004) | yes |
| TLR9 + type-I-IFN → IDO/Treg (immune rebalancing) | animal/in_vitro | PMID 16741252 (Romani, Blood 2006) | yes |
| Multi-TLR mechanism synthesis | mechanism_review | PMID 37110771 (Tao, Molecules 2023) | yes |
| Pleiotropic immunomodulator / immune restoration | mechanism_review | PMID 31555601 (Costantini, Front Oncol 2019) | yes |
| Immune-rebalancing in viral disease | mechanism_review | PMID 33362999 (Dominari, World J Virol 2020) | yes |

## Efficacy (Tier 1)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| **Sepsis NEGATIVE — the definitive trial (HR 0.99, n=1089)** | rct | PMID 39814420 (TESTS, BMJ 2025) | yes |
| Sepsis borderline (RR 0.74, n=361) | rct | PMID 23327199 (ETASS, Crit Care 2013) | yes |
| Sepsis meta OR 0.73 (small-trial artifact; HQ subgroup NS) | meta_analysis | PMID 40969554 (Front Cell Infect Microbiol 2025) | yes |
| COVID RCT mortality 11.1% vs 38.5% (severe subgroup; trial n=105 = 40 severe + 65 moderate) | rct | PMID 36042753 (Indian J Crit Care Med 2022) | yes |
| COVID retrospective (Wuhan) mortality 11.1% vs 30% | cohort | PMID 32442287 (Liu, Clin Infect Dis 2020) | yes |
| COVID meta RR 0.59 | meta_analysis | PMID 37845598 (Inflammopharmacology 2023) | yes |
| Hep B delayed virological response (OR 2.67 @12mo) | meta_analysis | PMID 11736720 (Aliment Pharmacol Ther 2001) | yes |
| Tα1 vs IFN-α hep B (OR 3.71 @6mo post-tx) | meta_analysis | PMID 18078676 (Antiviral Res 2008) | yes |
| Chinese hep B RCT (Tα1 vs IFN, Yunnan) | rct | PMID 15759817 (J Chin Med Assoc 2005) | yes |
| Elderly flu-vaccine antibody boost (n=90) | rct | PMID 2642497 (J Am Geriatr Soc 1989) | yes |
| Post-resection HBV-HCC OS (retrospective PSM) | cohort | DOI 10.1097/MD.0000000000025749 (Medicine 2021) | yes |

## Safety / PK / Regulatory
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| <1% drug-related AEs / injection-site / contraindications / PK (t½~2h, SC, 1.6mg 2×/wk) | regulatory/vendor_label | Zadaxin (thymalfasin) PI via RxList | yes (label-derived; SciClone PDF not directly loaded) |
| No Tα1-related SAE (sepsis RCT safety) | rct | PMID 23327199 (ETASS) | yes |
| Sepsis safety = placebo (n≈1089) | rct | PMID 39814420 (TESTS) | yes |
| NOT on WADA Prohibited List (contrast TB-500) | regulatory | WADA 2025 Prohibited List | yes (absence-of-listing + S2 catch-all caveat) |
| EU orphan designation (HCC) | regulatory | EMA EU/3/02/110 | yes |
| Removed from US 503A Category 2 (Sept 27, 2024) | regulatory | FDA interim-policy action (Fed Reg 2024-31546) | yes |
| Not FDA-approved; ~30+ countries; orphan designations | regulatory | SciClone SEC 10-K + FDA PCAC docs | **partial** (SEC PDF 403 + FDA media PDFs 404 on fetch; corroborated across secondaries) |
| Chinese Expert Consensus (only admissible protocol-tier) | practitioner_protocol | DOI 10.1097/IM9.0000000000000176 (Infect Microb Dis 2025) | yes (record confirmed; full text not loaded — scope only, no dose numbers extracted) |

## VERIFIED ABSENCES (load-bearing)
| Searched-for | Result |
|---|---|
| RCT for general post-illness recovery / deconditioning in healthy adults | **NO ADMISSIBLE PRIMARY FOUND** (goal-fit gap) |
| Admissible WESTERN practitioner_protocol (named prescriber, citable venue) | **NONE** — circulating regimens are vendor/forum (anecdote); only the Chinese Expert Consensus is admissible |
| Volume of distribution / absolute SC bioavailability | **NO ADMISSIBLE PRIMARY FOUND** (commonly-cited ~5–8 L not in the verifiable label) |
| HCV high-quality meta-analysis | NOT located within scope (flagged, not asserted) |

## Anti-fabrication catches
- Tα1 (thymosin ALPHA-1) is NOT WADA-prohibited; **thymosin BETA-4 / TB-500 IS** — the two were kept distinct.
- FDA orphan/503A PDFs returned 404/403 on fetch → marked VERIFIED:partial, not stated as directly-loaded primary.
- The narrative review (Dinetz & Lee 2024, lower-tier journal) was used only for "well-tolerated overall," NOT for hard AE rates.
- COVID retrospective (Liu 2020) tagged `cohort`, not RCT; HCC study tagged `cohort` (PSM), not RCT.
