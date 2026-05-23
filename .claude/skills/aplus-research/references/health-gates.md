---
title: Health-Specific Research Gates
type: reference
permalink: aplus-research/health-gates
---

# Health-Specific Research Gates

Three gates that the `deep-research` skill does not have natively. Each is mechanically enforced by the orchestrator at the phase indicated, with a machine-readable JSON verdict that blocks downstream phases.

These gates exist because they catch failure modes that produced documented errors in the project's first compound dispatch (BPC-157, 2026-05-23). Quant has equivalent gates for its domain (manifest gate, citation gate); these are the health equivalents.

---

## §1. Population-Mismatch Gate (Phase 4.75)

**Failure mode caught:** rodent or in-vitro evidence cited as if it grounds a human dose, AE rate, or efficacy claim. Most BPC-157 practitioner doses are mg/kg extrapolations from rodent work — without `[population-mismatch: species]` annotation, the report would silently present these as human-evidence-grounded.

**Rule.** Any claim that names a numerical value (dose, effect size, n, AE rate, response window, half-life) AND cites a source tagged `animal` or `in_vitro` MUST carry an inline `[population-mismatch: <species>]` tag in the same sentence. Female-only or male-only cohort cites require `[population-mismatch: <sex>]`.

**Verifier procedure.**
1. Grep the draft report for `[N, animal]` and `[N, in_vitro]` citations.
2. For each, check the surrounding sentence (±200 chars) for a numerical token (regex: `\d+(?:\.\d+)?\s*(?:µg|mg|ng|pg|kg|min|hr|h|%|fold|/d|/day|/wk|/mo|/yr|±|to)`).
3. If a numerical token is present and no `[population-mismatch:` tag appears in the same sentence → HALT `population-mismatch-unflagged`.

**Override.** If the numerical token is in a Background or Mechanism context where the species is the subject of the sentence (e.g., "rat Achilles tendon transection at 10 µg/kg [N, animal]"), the population is implicit and `[population-mismatch]` is optional. Verifier whitelist matches this pattern: numerical token within 100 chars of a species name AND the cite is the only source for the claim.

**JSON output (in `gate-4.75.json`):**
```json
{
  "population_mismatch": {
    "verdict": "PASS|HALT",
    "checked_citations": 47,
    "flagged_citations": [
      {"line": 142, "claim": "...", "missing_tag": "population-mismatch:rat"}
    ]
  }
}
```

---

## §2. Risk-Floor Gate (Phase 7.5)

**Failure mode caught:** a compound entry at `risk_tier: experimental` is written with empty `contraindications`, `monitoring`, or `stopping criteria` fields — i.e., a high-risk compound enters the wiki without the safety scaffolding that the project's evidence-tier methodology requires for that risk level.

**Rule.** If the synthesized compound entry would have `risk_tier: experimental` OR `risk_tier: high`, the following template fields must be populated from retrieved sources (cited):

- `Risk Profile › adverse effects (literature)` — non-empty
- `Risk Profile › contraindications` — non-empty
- `Risk Profile › monitoring` — non-empty
- `Trial Status › stopping criteria` — non-empty (may be operator-specific placeholder for library entries, but field must be present and non-empty)

**Verifier procedure.**
1. Read the draft compound entry at the planned output path.
2. Parse the four named fields.
3. For each: empty, missing, or placeholder-only (`<...>` or "TBD" or "n/a" without "n/a — library-canonical because operator-specific") → HALT `risk-floor-incomplete`.

**Special case: `risk_tier: experimental` always requires a third-party monitoring biomarker.** Self-reported subjective monitoring is insufficient. At least one item in `monitoring` must reference `[[biomarkers/<name>]]` or a named lab assay.

**Override.** Library-canonical entries (operator-agnostic) may set `stopping criteria` to `*(operator-specific — populated per trial)*` literally, but the section header and pointer must be present.

**JSON output (in `gate-7.5.json`):**
```json
{
  "risk_floor": {
    "verdict": "PASS|HALT",
    "compound_risk_tier": "experimental",
    "required_fields": {
      "adverse_effects_literature": "populated|empty",
      "contraindications": "populated|empty",
      "monitoring": "populated|empty",
      "stopping_criteria": "populated|empty"
    },
    "third_party_monitoring_marker_present": true,
    "halt_reasons": []
  }
}
```

---

## §3. Concentration-Audit Gate (Phase 4.75)

**Failure mode caught:** an entire compound's evidence base derives from a single research lab (BPC-157 is ~76-80% Sikiric-affiliated; in-vivo MSK efficacy is 100% Sikiric). Without a first-class concentration-risk section, specialist agents querying the entry may read indication tiers in isolation and miss that the entire literature rests on one group's work.

**Rule.** During Phase 4 triangulation, the orchestrator computes single-lab share of distinct primaries across all sections (deduplicated). If single-lab share ≥ 70%, the draft report MUST contain a first-class section (top-level heading) surfacing the concentration risk before any indication subsection. Buried-only-in-bibliography → HALT.

**Calculation.**
1. Enumerate all distinct primary citations (type tag ∈ {`rct`, `meta_analysis`, `cohort`, `open_label`, `animal`, `in_vitro`}).
2. For each, extract author affiliation from the bibliography entry (institution name from the citation).
3. Compute the largest cluster (typically defined by first-author institution, but verifier accepts orchestrator-supplied cluster definition for groups that span multiple institutions — e.g., Sikiric Zagreb is one cluster regardless of which Pliva-era subsidiary authored).
4. Share = largest-cluster-count / total-distinct-primaries.

**Verifier procedure.**
1. If share ≥ 70%: grep the draft report's top-level section headings for keywords matching `concentration|single.lab|laboratory dominance|<cluster-name>`. If no matching top-level section → HALT `concentration-not-surfaced`.
2. If share ≥ 70%: the concentration section must appear BEFORE the first indication subsection (verified by line-number ordering).
3. If share < 70%: gate passes vacuously, no first-class section required.

**Sub-cluster detection.** Independent labs working in collaboration with the dominant lab should count toward the dominant cluster, not as independent (e.g., Sikiric-trained postdocs at other institutions publishing with Sikiric as senior author = Sikiric cluster). Orchestrator may need manual disambiguation; default is first-author institution.

**JSON output (in `gate-4.75.json`):**
```json
{
  "concentration_audit": {
    "verdict": "PASS|HALT",
    "total_primaries": 50,
    "largest_cluster_name": "Sikiric (Zagreb)",
    "largest_cluster_count": 38,
    "share": 0.76,
    "threshold_triggered": true,
    "surfaced_section_heading": "Evidence Landscape and Concentration Risk",
    "surfaced_before_first_indication": true
  }
}
```

---

## §4. Mandatory-Layers Spec (Phase 8 + 8.5)

**Failure mode caught:** a compound entry is written from the academic literature alone, missing the prescribing-practice ecosystem (what doctors actually use) and the non-English literature (Croatian/Chinese for BPC-157 — caught an author-attribution error and surfaced new indications in the supplementary dispatch).

**Rule.** All compound research at `--mode=standard|deep|ultradeep` MUST produce three artifacts:

1. `vault/library/<class>s/<slug>/research-report.md` (academic layer)
2. `vault/library/<class>s/<slug>/practitioner-layer.md` (prescribing-practice)
3. `vault/library/<class>s/<slug>/non-english-layer.md` (non-English coverage)

`--mode=quick` may skip the two supplementary layers (latency).

### §4.1 Prescribing-practice layer agent brief

Dispatched in Phase 8 as a separate agent. Brief:

> Build the prescribing-practice layer for `<compound_name>` per `vault/compounds/_template.md`'s "Prescribing-Practice Layer" section. Source whitelist: `vault/library/_source-whitelist.md` Tiers 2.7 (`practitioner_protocol`) and 3 (`compounding_data_sheet`).
>
> Required sections:
> 1. Compounding pharmacy clinical data sheets — table format (Pharmacy | Dose | Route | Cycle | Indications | Source). Survey at minimum: Tailor Made Compounding, Empower, Hallandale, Belmar, APS, Strive, AnazaoHealth, Olympia, plus any compound-class-specific compounders. Document "no current sheet" findings explicitly with cause if known (FDA enforcement, etc.).
> 2. Practitioner reference texts — Seeds Peptide Protocols, International Peptide Society, A4M, AAOPM, IFM, Clinical Peptide Society materials.
> 3. Named-physician stated protocols — table format (Practitioner | Dose | Route | Cycle | Indications | Venue+date | Source URL). Survey at minimum: Edwin Lee, William Seeds, Kent Holtorf, Neil Paulvin, Tracy Gapin, Suzanne Turner, Peter Attia.
> 4. Originator-group recommended dose — if the originator group states a human dose recommendation, capture it; if not, say so explicitly.
> 5. Consensus practitioner dose — synthesized; explicitly labeled as consensus, not RCT.
> 6. Gaps and divergences — areas of consensus, divergent schools, areas without consensus.
>
> Type-tag every cite. `practitioner_protocol` and `compounding_data_sheet` cites may ground dose/route/cycle/admin only — never efficacy. Vendor sites and Reddit/forums never ground dose claims.

### §4.2 Non-English literature layer agent brief

Dispatched in Phase 8 as a separate agent. Brief:

> Build the non-English literature layer for `<compound_name>` per `vault/library/_source-whitelist.md` Tier NE.
>
> Required survey languages (in priority order, adjusted per compound origin):
> 1. Originator-country language (if non-English): full survey
> 2. Russian: eLibrary.ru, CyberLeninka, Springer-translated Bulletin of Experimental Biology and Medicine; especially relevant for Khavinson-group peptides (Epitalon, Vilon, Thymalin, Cortexin), Selank, Semax, Cerebrolysin derivatives
> 3. Chinese: CNKI, Wanfang, VIP, Acta Pharmacologica Sinica; especially relevant for replication work and PLA medical research apparatus
> 4. Croatian/Eastern European: relevant for Pliva-era compounds (BPC-157), Slovenian patent estate
> 5. Korean: KCI, Kosin Med J, JDAPM
> 6. Japanese: J-STAGE — opportunistic
>
> Required output sections:
> - Survey scope + methodology (databases, search terms, translation tools)
> - Per-language findings (new sources with full citations)
> - Confirmed absences (explicit "no admissible primaries located in <databases>")
> - Contradictions with English-language report (log for `meta/contradictions.md`)
> - New indications / doses / AEs surfaced
>
> Translation rules per whitelist Tier NE: machine-translated numerical claims require `[translated:<tool>]` inline tag + source-language verification. Source-language-only cites without English abstract: cite bibliographic reference but not content claims.

### §4.3 Layers gate verification

`gate-8.5.json` verifies:

1. Both layer files exist at `vault/library/<class>s/<slug>/practitioner-layer.md` and `non-english-layer.md`.
2. Each layer file has its own `## Bibliography` and `## Self-check` sections.
3. Practitioner layer documents at least 1 compounding-pharmacy data sheet OR explicit "no admissible data sheet located" with searched-vendor list.
4. Non-English layer documents survey of at least 3 of {Russian, Chinese, originator-country, Korean, Japanese} with explicit findings or "no admissible primaries located".

**JSON output (in `gate-8.5.json`):**
```json
{
  "layers": {
    "verdict": "PASS|HALT",
    "practitioner_layer_path": "vault/library/peptides/bpc-157/practitioner-layer.md",
    "practitioner_layer_present": true,
    "practitioner_compounding_sheets_count": 1,
    "non_english_layer_path": "vault/library/peptides/bpc-157/non-english-layer.md",
    "non_english_layer_present": true,
    "non_english_languages_surveyed": ["Russian", "Chinese", "Croatian", "Korean", "Japanese"],
    "halt_reasons": []
  }
}
```
