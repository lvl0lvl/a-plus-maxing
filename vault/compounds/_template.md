---
title: <Compound Name>
type: compound
permalink: a-plus-maxing/compounds/<slug>
class: supplement | peptide | nootropic | pharmaceutical | hormone | herbal
evidence_tier: S | A | B | C | D
risk_tier: low | medium | high | experimental
status: researching | planned | active | paused | trialed-stopped | excluded
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
---

# <Compound Name>

## Metadata
- class:
- evidence_tier:        # see [[library/methodology/evidence-tiers]]
- risk_tier:
- status:
- last_verified:

## Mechanism
One paragraph: pathway, receptors, expected physiological effect. Cite primary mechanism source.

## Evidence Summary
Strongest 2-3 sources, in order of weight:
- [Author YYYY] — n=N, design (RCT | cohort | open-label | animal | in-vitro), endpoint, effect size, [[library/<path>]]
- [Author YYYY] — ...
- [Author YYYY] — ...

Counter-evidence (if any):
- [Author YYYY] — null or contradictory result

## Non-English Literature Coverage
- Russian / Soviet: <surveyed yes/no; institutes / journals checked; key sources found or "no admissible primaries">
- Chinese: <surveyed yes/no; CNKI / Wanfang / journals checked; key sources found>
- Croatian / Eastern European: <relevant for any originator-country lit; surveyed yes/no>
- Japanese: <surveyed yes/no — relevant for some peptides>
- Other (Korean, German, French, Spanish): <as relevant>
- Translation notes: <which sources were full-text vs abstract-only; translator used; any concerns>

## Prescribing-Practice Layer
What licensed prescribers actually use to make dosing decisions — distinct from academic evidence. Source-tagged per `library/_source-whitelist.md` practitioner-protocols tier.

- **Compounding pharmacy clinical data sheets** — `[compounding_data_sheet]`. Document each pharmacy's published protocol (dose, route, cycle).
  - <Pharmacy> | <dose protocol> | <source URL>
- **Practitioner reference texts** — `[practitioner_protocol]`. Seeds Peptide Protocols, International Peptide Society protocols, A4M/IFM materials, AAOPM materials.
  - <Reference> | <dose protocol> | <citation>
- **Conference / CME-stated protocols** — `[practitioner_protocol]`. Slides, handouts, podcasts where named prescribing physicians explicitly state their protocols.
  - <Practitioner> | <protocol stated> | <venue + date>
- **Originator-group recommended dose (from narrative reviews)** — `[mechanism_review]`. The dose recommended by the lab that developed the compound, when distinct from practitioner consensus.
- **Consensus practitioner dose** — synthesized from above. Labeled as consensus, not RCT. Used by most prescribers in the absence of human trial data.
- **Gap between literature and practice** — if literature dose differs materially from consensus practitioner dose, document the gap.

## Protocol
- dose:               # e.g., 250 mcg subQ — populated from consensus practitioner dose unless human RCT exists
- route:              # oral | sublingual | subQ | IM | transdermal | intranasal
- timing:             # AM fasted | pre-bed | post-workout | etc.
- cycle:              # e.g., 5 days on, 2 off; 8 weeks on, 4 weeks washout
- stack:              # [[compound-x]], [[compound-y]] taken alongside
- source:             # vendor / compounding pharmacy
- regulated status:   # Rx | OTC | research-chemical | gray-market
- cost:               # $/month or $/cycle

## Reconstitution (peptides only)
- supplied as:        # e.g., 5 mg lyophilized vial
- diluent:            # bacteriostatic water, mL
- final concentration:
- dose volume:        # units on U-100 insulin syringe
- storage:            # fridge / freezer, days stable reconstituted

## Risk Profile
- adverse effects (literature):
- adverse effects (anecdotal):
- contraindications:    # DNA variants from [[dna/analysis]], biomarkers, other compounds
- monitoring:           # [[biomarkers/...]] to track, cadence
- known interactions:

## Trial Status
- linked experiment:    # [[experiments/<id>]] or "none"
- baseline biomarkers:  # [[biomarkers/...]] measured before start
- expected response window: # 2 weeks | 8 weeks | etc.
- stopping criteria:    # what would end the trial early (adverse marker, no response, side effects)

## Decision Notes
Per [[library/methodology/evidence-tiers]] matrix, this compound at evidence_tier=X / risk_tier=Y falls in cell Z → guidance: <adopt | trial | doctor-required | avoid>. Walter's specific context modifying this: <DNA, labs, current protocol>.

## Relations
- [[biomarkers/<target>]]
- [[experiments/<id>]]
- [[compounds/<stack-partner>]]
- [[protocols/<routine>]]
- [[decisions/<adr>]]
