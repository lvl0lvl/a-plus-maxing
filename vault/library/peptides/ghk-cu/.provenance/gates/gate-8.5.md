# Phase 8.5 Layers Gate — GHK-Cu

## Verdict

verdict: PASS

Mode: deep. Both mandatory layers present, each with its own bibliography and self-check, and each meets its substantive gate requirement. No halt reasons.

## Practitioner layer (each required field: value)

- path: vault/library/peptides/ghk-cu/practitioner-layer.md
- present: true
- compounding_sheets_count: 4 (Empower compounded 0.5% GHK-Cu facial serum + 0.5% scalp solution; Avena Lab Copper Tripeptide-1 TDS 1000 ppm + 5000 ppm)
- compounding_sheets_or_null_finding: true (≥1 data sheet located — gate satisfied by located sheets, not by null-finding)
- named_physicians_count: 0 (explicit documented absence — §2.2: no named+venue+dated GHK-Cu prescriber protocol located; Seeds 2020 ISBN 9780578624358 does not cover GHK-Cu; no dated A4M/IPS/IFM per-substance handout; no named cosmetic-derm injectable protocol; searched list recorded, nothing invented)
- has_bibliography: true (own bibliography, 11 entries, each tagged tag= + tier=)
- has_self_check: true (Self-check section: scope/efficacy guard, named-prescriber attestation, data-sheet gate SATISFIED, both-channels documented, gaps/honesty notes)

Requirement met: ≥1 compounding/cosmetic data sheet documented (4 located). SATISFIED.

## Non-English layer (each required field: value)

- path: vault/library/peptides/ghk-cu/non-english-layer.md
- present: true
- languages_surveyed: Russian, Chinese, Other (originator-country = US/English → encoded as "Other")
- Russian: CITATIONS LOCATED — 3 verified peer-reviewed Russian-language sources (Polonskaya 2020 Pharmateca DOI 10.18565/pharmateca.2020.8.78-82; Rakhmetova 2022 VRGMU DOI 10.24075/vrgmu.2022.014 [copper-free GHK, flagged]; Zadubrovskaya 2020 FORCIPE)
- Chinese: explicit "none located via accessible channels" + full disclosed search terms + databases (CNKI/Wanfang/x-mol/Semantic Scholar) + honest channel-gap note (not proof of absence). Documented none-located counts as surveyed — does NOT halt the gate.
- Originator-country (Other): valid null finding — GHK discovered in the US by Pickart (1973, UCSF); originator literature is English by definition, no distinct non-English originator stream
- has_bibliography: true (own Bibliography section with tier key; 3 Russian entries with DOI/eLibrary IDs, tag=, tier=, language=, entity=)
- has_self_check: true (Self-check section: RU+ZH+originator each surveyed, no-fabrication attestation, translated-numeric tagging, tier/language rules, count of admissible sources)

Requirement met: ≥ Russian + Chinese + originator each surveyed, each with citations OR explicit none-located + search terms. SATISFIED (Russian = 3 cites; Chinese = documented channel-gap; originator = valid null).

## Structured verdict

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","timestamp":"2026-06-19T15:21:39Z","iterations":1,"practitioner_layer":{"path":"vault/library/peptides/ghk-cu/practitioner-layer.md","present":true,"sha256":"8ef0e853f9db4da38050981750b5f78aae09e06b4e219bfd8913caee98cf4ec4","compounding_sheets_count":4,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/ghk-cu/non-english-layer.md","present":true,"sha256":"9e0e600c833bb0671877a2b46f5753d7fefda2ef9f63327758022f4e55115ebf","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[],"attestation_chain":{"iter_start_ts":"2026-06-19T15:21:39Z","attest_ts":"2026-06-19T15:21:39Z","iteration":1,"agent_source_path":".claude/skills/aplus-research/SKILL.md","agent_source_sha256":"b0f80271dbcc82707bf847fdeabfaf7bf0ac03d284e06043c579235250a6fbee","agent_source_mtime":"2026-06-18T20:04:15Z"}}
```
