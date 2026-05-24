---
title: Source Whitelist — Tier Structure + Type-Tag Enum + Admissibility Matrix
type: decision
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
depends_on: ["2026-05-23-wiki-schema"]
superseded_by: null
review_cadence: phase (or on first wrong-source incident)
permalink: a-plus-maxing/decisions/2026-05-23-source-whitelist
---

# Decision: Source Whitelist

## Context

Peptide / supplement / hormone research is contaminated by vendor marketing dressed as evidence. Without an enforced source hierarchy, a research dispatch can launder a vendor "therapeutic dose" recommendation into the wiki as if it were primary literature. Quant has this discipline via `references/source-hierarchy.md` + `tier-2-5-host-whitelist.txt`; we need the health equivalent.

## Decisions

### 1. Whitelist lives at `vault/library/_source-whitelist.md`

Single source of truth. Domain-specific extensions (peptide-only compounders, lymphatic-only manual-therapy bodies) live at `vault/library/<domain>/_source-whitelist-extension.md` and layer on top — they do not replace the base.

### 2. Five standard tiers + 2 specialty tiers

- **Tier 1** — Primary peer-reviewed literature (PubMed, Cochrane, NEJM, Lancet, JAMA, Nature, Cell, Science, ScienceDirect, Springer, Wiley, OUP, Karger; Frontiers/MDPI admissible but flagged as open-access lower-trust; bioRxiv/medRxiv with `[not-peer-reviewed]` tag)
- **Tier 2** — Regulatory / institutional (FDA, EMA, TGA, Health Canada, NIH, WHO, CDC, DailyMed)
- **Tier 2.5** — Curated practitioner with cited primaries (Examine.com, Peter Attia, Huberman, FoundMyFitness) — admissible only when the page cites a primary; cite the primary, not the practitioner page
- **Tier 2.7** — Practitioner protocols (Seeds, IPS, A4M, IFM, AAOPM, named-physician stated protocols) — admissible for prescribing-practice dose/route/cycle claims ONLY, never efficacy
- **Tier 3** — Compounding pharmacies (Empower, Tailor Made, Hallandale, etc.) — admissible for admin protocol / reconstitution / dose forms
- **Tier 4** — Research-chemical vendors — admissible for reconstitution math + gray-market availability ONLY, NEVER efficacy
- **Tier 5** — Anecdote aggregates (Reddit, forums, podcasts without primary cites) — qualitative leads only, never numerical
- **Tier NE** — Non-English literature, tier-equivalent (Russian eLibrary / CyberLeninka, Chinese CNKI / Wanfang, Croatian Hrčak, Korean KCI, Japanese J-STAGE)

### 3. 12-tag type enum

Every cite carries exactly one tag: `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`

### 4. Admissibility matrix is enforced, not advisory

Vendor and anecdote cites cannot ground numerical claims (dose, effect size, n, AE rate, half-life). Practitioner protocols cannot ground efficacy claims. Compounding data sheets cannot ground efficacy unless the sheet cites its own primaries (in which case cite those primaries directly). This is enforced at Phase 4.75 of `aplus-research` via the Integrity Verifier IC-checks.

### 5. Non-English literature gets the same tier treatment as English

A Russian peer-reviewed paper from a Tier 1-equivalent venue is admissible as Tier 1, with translation status noted. Machine-translated numerical claims require `[translated:<tool>]` inline tag + source-language verification. Source-language-only cites without English abstract: cite bibliography but not content.

### 6. Adding a host requires manual review

Any new whitelist addition: review against tier criteria, add with one-line note on what claim types it supports, log to `vault/meta/log.md`, note in `vault/meta/contradictions.md` if the host has disagreed with a higher tier.

## Alternatives Considered

- **Reuse Quant's whitelist directly.** Rejected: Quant whitelists academic finance / NWP / state-estimation venues. Health domain requires PubMed-centered hierarchy + compounding-pharmacy + research-chemical-vendor tiers that Quant doesn't have.
- **No vendor tier — exclude vendors entirely.** Rejected: reconstitution math (vial sizes, diluent volumes, syringe units) literally only appears on vendor labels and compounding-pharmacy data sheets. Vendor tier is necessary for that specific claim type; it's the admissibility matrix that prevents misuse.
- **No practitioner-protocol tier — only academic literature.** Rejected: gap between "rodent 10 µg/kg" (literature) and "250 µg subQ daily" (what doctors actually prescribe) is the load-bearing question for any decision to use a compound. Practitioner protocols document this; the tier exists with explicit admissibility constraints (dose/route/cycle only, never efficacy).

## Breaks If

- Future research dispatches ignore the type-tag enum (caught at Phase 4.75 IC-1 / IC-2)
- A new compound class requires a tier this whitelist doesn't have (e.g., TCM research) — extend rather than abandon
- Tier-1 venues lose credibility (e.g., a major journal becomes a paid-publication mill) — Frontiers/MDPI are already flagged; further demotions handled case-by-case

## Relations

- [[decisions/2026-05-23-wiki-schema]] (parent — wiki that uses this whitelist)
- [[decisions/2026-05-23-aplus-research-skill]] (consumer — research skill that enforces this whitelist)
- [[library/_source-whitelist]] (the whitelist itself)
- [[library/methodology/evidence-tiers]] (companion — tier-tag → evidence-tier mapping)
