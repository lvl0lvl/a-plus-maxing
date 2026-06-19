# Tesamorelin — Verified-Source Ledger

Every citation used in the entry, with its type-tag and verification status. Anti-fabrication
discipline: each identifier was independently checked to resolve (PubMed / ClinicalTrials.gov /
DailyMed / EMA). `VERIFIED:partial` = the fact is corroborated across sources but a single
authoritative primary could not be directly loaded (flagged so it is not overstated).

## Primary literature (Tier 1)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| Pivotal RCT: VAT −15.2% vs +5.0%, IGF-1 +81%, TG −50 (n=412, 26 wk) | rct | PMID 18057338 (NEJM 2007, Falutz) | yes |
| Pivotal RCT #2: VAT −10.9%, loss on discontinuation (n, 6–12 mo) | rct | PMID 20101189 (JAIDS 2010, Falutz) | yes |
| Single-center RCT: VAT −42 cm², liver fat −2.9% (n=50) | rct | PMID 25038357 (JAMA 2014, Stanley) | yes |
| NAFLD RCT: hepatic fat −37% relative (n=61, 12 mo) | rct | PMID 31611038 (Lancet HIV 2019, Stanley) | yes |
| ONLY non-HIV RCT — cognition (NOT body comp), IGF-1 +117% (n=152) | rct | PMID 22869065 (Arch Neurol 2012, Baker) | yes |
| Meta-analysis: 5 RCTs (all HIV), VAT −27.71 cm² | meta_analysis | PMID 41545261 (Obes Res Clin Pract 2026, Badran) | yes |
| Pooled metabolic review / discontinuation | rct-pooled review | PMID 22495074 (Clin Infect Dis 2012, Stanley & Grinspoon) | yes |
| Mechanism: pulsatile GH + IGF-1 +181 µg/L, glucose preserved (n=13) | open_label | PMID 20943777 (JCEM 2011, Stanley) | yes |
| Population PK: clearance ~1060 L/h, Vd ~200 L (n=38) | open_label/pop-PK | PMID 25358450 (Clin Pharmacokinet 2015, González-Sales) | yes |
| Mechanism review: DPP-4 resistance, pulsatile-vs-rhGH, VAT lipolysis | mechanism_review | PMID 22096409 / PMC3218714 (Bedimo 2011) | yes |

## Regulatory (Tier 2)
| Claim anchor | Type tag | Identifier | Verified |
|---|---|---|---|
| FDA label of record (mechanism, AEs, IGF-1, glucose, PK, dosing, contraindications) | regulatory | DailyMed EGRIFTA SV, setid 3d783378-b02d-4f19-99dd-0fc91a042224 (NDA 022505) | yes (loaded) |
| FDA approval 2010-11-10, HIV-lipodystrophy indication | regulatory | NDA 022505 approval (accessdata) | yes (fact corroborated; PDF 404 via fetch) |
| Egrifta WR: CRL 2024-01-24 → approved 2025-03-25 | regulatory | FDA / trade reporting | yes |
| EMA: never approved; application withdrawn June 2012 (CHMP notification 2012-06-21) | regulatory | EMA withdrawal notice | yes |
| Health Canada: approved (same indication) | regulatory | CADTH review NBK539137 | yes |
| WADA: prohibited at all times, S2.2.4 (GH-releasing factors); named by token | regulatory | WADA Prohibited List + GHRF guidance | yes (review independently confirmed "sermorelin and tesamorelin" named under S2.2.4) |
| US compounding restricted: deemed biologic (deemed-BLA 2020-03-23) bars bulk 503A/503B; earlier interim 503A Category 2 (framework restructured early 2025) | regulatory | FDA biologics-transition (BPCI Act) + 503A framework | yes (biologic transition verified; interim Cat-2 historical) |
| Insurance restricted to on-label HIV use (imaging-confirmed VAT) | payer policy | Centene/Molina PA criteria | yes |

## VERIFIED ABSENCES (load-bearing — the population-transfer caveat rests on these)
| Searched-for | Result |
|---|---|
| RCT of tesamorelin for body comp / VAT / recovery in healthy/general/post-illness HIV-NEGATIVE adults | **NO ADMISSIBLE PRIMARY FOUND** (aggregator-claimed "Stanley non-HIV obesity RCT" confirmed non-existent) |
| Admissible `practitioner_protocol` for off-label dosing (named clinician, citable venue) | **NO ADMISSIBLE PRIMARY FOUND** (circulating regimens are vendor/forum = anecdote_aggregate) |
| Non-English primary literature | **NONE LOCATED** (Chinese hits = secondary commentary; no French primary) |

## Anti-fabrication catches during retrieval (documented, not hidden)
- Falutz NEJM 2007 PMID is **18057338**; PMID 18057339 resolves to an UNRELATED article — the off-by-one was caught and discarded.
- A surfaced "~107 ng/mL IGF-1" label figure was NOT independently corroborated → excluded; IGF-1 numerics come from Stanley 2011 (+181 µg/L) and the label SDS percentages.
- A "18.6/37.8 min" half-life pair (wikidoc-style) did not match the label's 26/38 min → label values used.
- accessdata.fda.gov PDF mirrors returned 404/403 via fetch → all FDA-label claims grounded in the DailyMed label of record instead; PDF URLs not cited as independently loaded.
- Pooled n for the 2026 meta-analysis not stated in the abstract → flagged, not invented.
