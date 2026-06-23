# Gate 8.5 — Layers Verification: Thymosin Alpha-1 (mode=deep)

## Verdict

verdict: PASS

```json
{
  "phase": "8.5",
  "verdict": "PASS",
  "iterations": 1,
  "mode": "deep",
  "practitioner_layer": {
    "path": "vault/library/peptides/thymosin-alpha-1/practitioner-layer.md",
    "present": true,
    "compounding_sheets_count": 0,
    "named_physicians_count": 2,
    "has_bibliography": true,
    "has_self_check": true
  },
  "non_english_layer": {
    "path": "vault/library/peptides/thymosin-alpha-1/non-english-layer.md",
    "present": true,
    "languages_surveyed": [
      "Chinese",
      "Other",
      "Russian"
    ],
    "has_bibliography": true,
    "has_self_check": true
  },
  "halt_reasons": []
}
```

---

## Practitioner Layer

**File:** `vault/library/peptides/thymosin-alpha-1/practitioner-layer.md` — PRESENT.

**Bibliography:** Present. 20 numbered entries [1]–[20], each with full citation, identifier (DOI/PMID/URL), and source tag. Covers regulatory (Zadaxin PI, PCAC Dec 2024 materials), RCTs, meta-analyses, anecdote_aggregate, vendor_label, and practitioner_protocol tiers. PASS.

**Self-Check:** Present. Section titled `## Self-Check` at end of document. Explicitly attests: tier discipline, compounding data sheet absent (explicit-absence form), US regulatory status stated unambiguously, Tα1/Tβ4 identity hazard, approved vs. US reality maintained as distinct, named practitioners verified to venue+date, off-whitelist source check, and documented gaps/residual limits. PASS.

**Compounding data sheets (admissible):** `compounding_sheets_count = 0`. No admissible US compounding-pharmacy clinical data sheet was located. This is the permitted explicit-absence form: a "Compounding Data Sheet Status (Gate Finding)" section documents the absence explicitly, provides a structural explanation (December 2024 PCAC negative vote closed the 503A pathway that would generate such documents), and lists 9 searched vendor/compounder sources (Empower Pharmacy, Hallandale Pharmacy, Strive Pharmacy, Belmar Pharma Solutions, Tailor Made Compounding/Infiniwell, APS, RonanRx, Preferred Regen ATL, A4M professional monograph). Gate criterion MET via explicit-absence form with vendor-list.

**Named physicians:** `named_physicians_count = 2`.
- Dr. Audra Moran (Owner/Founder, Preferred Regen ATL, 650 Hamilton Ave SE Suite C, Atlanta GA 30312) — confirmed to venue + date; source [11, anecdote_aggregate].
- Dr. Dan Wool, NMD (Arizona License #18-1721; 20801 N Scottsdale Rd #205, Scottsdale, AZ 85255) — confirmed to venue + date + license number; source [19, practitioner_protocol].

Both practitioners named with clinic address, credentials, and dated retrieval. Four additional practitioners searched (Edwin Lee, Kent Holtorf, Neil Paulvin, Tracy Gapin) but not locatable to venue+date — correctly noted as "not fabricated." PASS.

**Additional practitioner-layer content verified:**
- Zadaxin ex-US approved prescribing pathway fully documented (indications, dosing, geography, contraindications, AEs, monitoring).
- US no-pathway documented: PCAC 4–17–0 vote against 503A Bulks List inclusion, December 4, 2024. Cited to primary FDA sources [7, regulatory] and [8, regulatory].
- Tα1/Tβ4 (TB-500) identity hazard documented in a dedicated comparative table covering amino acid sequence, family, mechanism, evidence base, WADA 2026 status, and US regulatory status. Described as "the most important practitioner safety point for the US grey-market context."
- Off-label/grey-market dose conventions documented with appropriate `anecdote_aggregate` tags.
- Monitoring framework derived from label precautions.

---

## Non-English Layer

**File:** `vault/library/peptides/thymosin-alpha-1/non-english-layer.md` — PRESENT.

**Bibliography:** Present. Tabular bibliography at end of document with 18 rows (C1–C9, I1–I3, R1–R6), each carrying: short citation, identifier (PMID ± DOI), tag, tier descriptor, and language. PASS.

**Self-Check:** Present. Section titled `## Self-check` at end of document. Explicitly attests per-language survey completion, ≥3 languages gate satisfaction, no fabricated citations, population annotations, genuine-non-English vs. English-published distinction enforcement, honest per-language findings, and off-compound exclusion. PASS.

**Languages surveyed:** Chinese, Italian, Russian — 3 languages with explicit per-language findings. Gate criterion (≥3) MET.

**Per-language admissible primary counts:**

- **Chinese: 9 primaries** — C1 (meta-analysis, *Zhonghua Gan Zang Bing Za Zhi*), C2 (human n=30 elderly oncology, *Zhejiang Da Xue Xue Bao Yi Xue Ban*), C3 (systematic review, *Zhongguo Wei Zhong Bing Ji Jiu Yi Xue*), C4 (human RCT n=80 COPD, *Sichuan Da Xue Xue Bao Yi Xue Ban*), C5 (in vitro, *Sheng Wu Gong Cheng Xue Bao*), C6 (in vitro anti-HBV, *Zhonghua Gan Zang Bing Za Zhi*), C7 (animal mouse radiation model, *Zhongguo Fei Ai Za Zhi*), C8 (human advanced HCC, *Zhonghua Yi Xue Za Zhi*), C9 (human n=95 retrospective COVID-19 cohort, *Zhonghua Wei Zhong Bing Ji Jiu Yi Xue*). All confirmed "[Article in Chinese]" by PubMed language indexing. All carry verified PMIDs.

- **Italian: 3 primaries** — I1 (1984, animal thymectomized mice), I2 (1985, animal murine splenocytes/thymocytes ex vivo), I3 (1988, animal C57BL murine thymocytes in vitro); all from Baldassarre/Mastino/Del Gobbo cluster; all in *Bollettino della Società Italiana di Biologia Sperimentale*; all confirmed "[Article in Italian]" by PubMed language indexing.

- **Russian: 6 primaries** — R1 (1990, Wistar rat n=219 behavioral pharmacology), R2 (1992, rat peritoneal mast cells thrombin modulation), R3 (1992, E. coli gene synthesis molecular biology), R4 (1994, mice+guinea pigs plague vaccine adjuvancy), R5 (1994, in vitro+animal immunobiological characterization), R6 (1995, E. coli+L-929 isolation/biochemistry); all from 1990–1995 Soviet/post-Soviet publication cluster; all confirmed "[Article in Russian]" by PubMed language indexing.

**Total admissible genuinely non-English primaries: 18** (Chinese 9, Italian 3, Russian 6).

**Admissibility distinction correctly applied:** English-published Chinese-institution trials (ETASS, TESTS, CUHK meta-analyses) excluded from non-English count and assigned to English layer. Garaci/Tor Vergata Italian group's primary work (all English-published) excluded. CyberLeninka Krebs 2003 Russian narrative review excluded as secondary (no verifiable DOI). PMID 2027873 (Shurlygina — thymoptin, off-compound) excluded with explicit explanation.

---

## Gate Summary

| Criterion | Status |
|-----------|--------|
| Both files present | PASS |
| Practitioner layer has bibliography | PASS |
| Practitioner layer has self-check | PASS |
| Practitioner layer has compounding data sheet OR explicit-absence+vendor-list | PASS (explicit absence; 9 vendors searched; structural cause documented) |
| Practitioner layer named physicians ≥1 (confirmed to venue+date) | PASS (2: Moran + Wool) |
| Ex-US Zadaxin prescribing pathway documented | PASS |
| US no-pathway (PCAC 4–17–0 Dec 2024) documented | PASS |
| Tα1/Tβ4 identity hazard documented | PASS |
| Non-English layer has bibliography | PASS |
| Non-English layer has self-check | PASS |
| Non-English layer ≥3 languages surveyed | PASS (Chinese, Italian, Russian) |
| Non-English layer explicit per-language findings | PASS |
| Non-English admissible primary count ≥3 total | PASS (18 total) |
| No fabricated citations | PASS (all 18 carry verified PMIDs) |

**Verdict: PASS. No halt reasons.**
