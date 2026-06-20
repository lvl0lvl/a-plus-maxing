# Phase 8.5 LAYERS Gate — MK-677 (deep mode, standard+ compound)

Both layers are mandatory at this mode. Verified against the three target files.

## Check 1 — Both layers exist, non-trivial, with Bibliography + Self-check

PASS. Both layers are present and substantive.
- **Practitioner layer** (`practitioner-layer.md`, sha256 `480822…e8ec`): full dose/route/cycle/formulation conventions, named-prescriber section, compounding gate, reconstitution N/A note, cost, an 8-item **Bibliography** (tag + tier), and a **Self-check** block. Non-trivial.
- **Non-English layer** (`non-english-layer.md`, sha256 `4f394b…8936`): Russian / Chinese / Japanese-other tracks each with explicit databases + search terms + none-located findings, translation-handling notes, a **Bibliography** (tag + tier + language, NE-MK-1..4), and a **Self-check** block. Non-trivial.

## Check 2 — Practitioner layer discipline

PASS.
- **No efficacy/AE-rate claim grounded on practice/vendor sources.** The scope banner and Self-check both state that `practitioner_protocol`/`compounding_data_sheet`/`vendor_label` sources ground ONLY dose/route/cycle/formulation/availability/cost. All efficacy + AE-rate magnitudes (glucose/HbA1c change, hip-fracture CHF signal, FFM +1.1 kg) are explicitly deferred to research report §5 (Tier-1) and NOT grounded here.
- **Oral ~10–25 mg/day once-daily convention NOT cross-attributed to injectable secretagogues.** The "Type discipline" banner, the dose-section closing note, and the Self-check all state the convention is for an oral small molecule and "must not be cross-attributed" to ipamorelin/CJC-1295/sermorelin injectables. No reconstitution arithmetic asserted (N/A).
- **Small-molecule-not-peptide** stated repeatedly and load-bearingly.
- **Honest gates.** Named-prescriber = NONE (explicit absence; telehealth workflow demoted to `vendor_label`/usage). Compounding = NONE (negative gate: not on §503A bulk list, cannot be lawfully compounded; standard channels Empower/Belmar/Tailormade/Hallandale/Strive searched, none found; affirmative vendor "503A available" claim flagged unreliable).

## Check 3 — Non-English layer honesty

PASS.
- **None-located clinical primary** across all three required tracks — clean, well-characterized null with explicit databases (eLibrary/CyberLeninka, CNKI/Wanfang, Google Patents/bibgraph/J-STAGE) and Cyrillic/Chinese/Japanese search terms.
- **Japanese patent ≠ clinical primary.** JP5336349B2 (Thorner, sarcopenia method) is correctly identified as the one genuine non-English-LANGUAGE primary *document* but a PATENT, not a clinical primary; grounds no efficacy claim.
- **Non-English-LANGUAGE vs -AUTHOR distinction** enforced throughout (banner + Self-check): Merck/UVA-Thorner/Göteborg English-published work excluded; bibgraph translated-abstract of Murphy et al. correctly excluded as an English primary indexed in Japanese.

## Check 4 — Compound entry

PASS.
- **Frontmatter correct:** `class: other`, `evidence_tier: B`, `risk_tier: medium`.
- **Framing present:** small-molecule (oral non-peptidic GHS-R1a agonist, not a peptide/not GHRH analogue); biomarker≠function (IGF-1↑ is target engagement, lean-mass↑ ≠ strength/function); FAILED programs (Alzheimer's Sevigny 2008 n=563; hip-fracture Adunsky 2011 + early CHF halt); metabolic framing (raised fasting glucose, reduced insulin sensitivity, raised HbA1c as dominant harm).
- **Relations link** research-report + practitioner-layer + non-english-layer + `[[biomarkers/igf-1]]` + `[[biomarkers/hba1c]]` + `[[biomarkers/fasting-glucose]]` + `[[compounds/ipamorelin]]`. All seven required relations present.
- **No Wikipedia** anywhere; non-English layer explicitly applies no-Wikipedia spirit to SportWiki (treated non-grounding).

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/mk-677/practitioner-layer.md","present":true,"sha256":"480822497d71d60537cb6ef9c56c06f26b95314b1c79ce52eb238e0ea353e8ec","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/mk-677/non-english-layer.md","present":true,"sha256":"4f394b0de1fb304f46d8be1a06395adefbdc1d801a272f3355175a2d3e918936","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
