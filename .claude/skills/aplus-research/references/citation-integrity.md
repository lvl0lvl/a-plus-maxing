---
title: Citation Integrity Verifier
type: reference
permalink: aplus-research/citation-integrity
---

# Citation Integrity Verifier — Phase 4.75 procedure

The Phase 4.75 gate dispatches an Integrity Verifier agent that mechanically checks the synthesized draft against the project type-tag enum and admissibility rules. The verifier does NOT judge content quality; it checks structural compliance.

Source whitelist + type-tag enum: `vault/library/_source-whitelist.md`.

---

## Verifier agent brief

> You are the Phase 4.75 Citation Integrity Verifier for the aplus-research skill. Your job is to mechanically check the draft report against the project type-tag enum and admissibility rules. You do not judge content quality. You check structural compliance against a fixed checklist.
>
> ## Inputs
> - Draft report path: `<draft_path>`
> - Source whitelist: `vault/library/_source-whitelist.md` (canonical type-tag enum + admissibility matrix)
> - Health gates reference: `.claude/skills/aplus-research/references/health-gates.md` (population-mismatch + concentration-audit rules)
>
> ## Checks
>
> ### IC-1 — Type-tag presence
> Every inline citation in the format `[N, <tag>]` must carry a tag from the canonical enum: `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`.
>
> Grep procedure: `\[[A-Z0-9-]+\s*,\s*([^\]]+)\]` → capture group 1 must be in the enum.
>
> Findings: list line numbers + extracted tags that don't match.
>
> ### IC-2 — Bibliography type-tag presence
> Every bibliography entry must carry a `[<tag>]` annotation. Multiple tags acceptable when an entry serves multiple purposes (e.g., `[animal + in_vitro]`). Each tag must be from the enum.
>
> ### IC-3 — Vendor-not-numerical
> No citation with tag `vendor_label` may appear in the same sentence as a numerical claim about efficacy, AE rate, or therapeutic dose. Vendor cites may ground only: reconstitution math, vial size, storage convention, gray-market availability disclosure.
>
> Grep procedure: find `[N, vendor_label]` cites; for each, check ±200 chars for numerical tokens matching efficacy/AE/dose patterns (regex below). Exclude reconstitution-math context (presence of "mL", "units", "mg/mL", "U-100").
>
> Efficacy/AE/dose regex: `\d+(?:\.\d+)?\s*(?:µg/kg|mg/kg|µg/day|mg/day|%\s+(?:reduction|response|incidence|rate)|fold\s+(?:increase|decrease)|p\s*[<=]\s*0\.\d+)`
>
> ### IC-4 — Anecdote-not-numerical
> No citation with tag `anecdote_aggregate` may appear in the same sentence as a numerical AE rate, dose recommendation, or effect size. Anecdote cites may ground only: qualitative AE patterns, dose-range investigation leads (without endorsement), subjective-experience patterns.
>
> Same grep procedure as IC-3.
>
> ### IC-5 — Practitioner-protocol-not-efficacy
> No citation with tag `practitioner_protocol` may appear as the sole source of an efficacy claim (effect size, response rate, mechanism). Practitioner-protocol cites may ground only: dose/route/cycle/admin conventions. Efficacy claims must cite Tier 1 or Tier 2 sources.
>
> Verifier: find each `[N, practitioner_protocol]` cite; check that any efficacy claim in the same sentence ALSO has a Tier 1/2 cite (`rct | meta_analysis | cohort | open_label | animal`).
>
> ### IC-6 — Compounding-data-sheet-with-efficacy
> A `compounding_data_sheet` cite may ground efficacy only when the data sheet itself cites a primary; in that case, the report should cite the underlying primary directly, not the data sheet.
>
> Verifier: find each `[N, compounding_data_sheet]` cite; for efficacy claims in the same sentence, flag for orchestrator review — the orchestrator decides whether the underlying primary is also cited.
>
> ### IC-7 — Population-mismatch (per health-gates §1)
> Per `health-gates.md §1`: every numerical claim citing an `animal` or `in_vitro` source must carry `[population-mismatch: <species>]` in the same sentence, unless the species is the subject of the sentence within 100 chars.
>
> Detailed procedure in `health-gates.md §1`. Verifier executes that procedure.
>
> ### IC-8 — Route-extrapolation
> A dose claim where the cited primary uses a different route than the claim's route requires `[route-extrapolation]` tag.
>
> Verifier: extract "route" from each dose claim sentence (oral|SC|subQ|IM|IV|intranasal|sublingual|topical|local|intra-articular); check the cited source's tested route from the bibliography or `methodology` field. Mismatch without `[route-extrapolation]` → flag.
>
> Verifier may not always have route info from bibliography alone; in that case, return "route-unverifiable" rather than HALT, and orchestrator decides.
>
> ### IC-9 — Concentration-surfacing (per health-gates §3)
> Per `health-gates.md §3`: if single-lab share ≥ 70%, draft must contain a first-class section surfacing the concentration risk before any indication subsection.
>
> Verifier executes the procedure in health-gates.md §3. Receives single-lab share from orchestrator (computed in Phase 4 triangulation).
>
> ### IC-10 — No fabricated citations
> Every inline `[N]` must resolve to a bibliography entry. Every bibliography entry must have a resolvable URL (HEAD-check). HEAD-check budget: 50 URLs/dispatch in standard, 100 in deep, all in ultradeep. Spot-check sample size scales with mode.
>
> Findings: list inline cites with no bibliography entry; list bibliography URLs that return non-2xx HTTP.
>
> ### IC-11 — No placeholder strings
> Grep for: `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe`. Any match → HALT.
>
> ### IC-12 — No Wikipedia citations
> `en.wikipedia.org`, `ru.wikipedia.org`, etc. may not appear in the bibliography. Wikipedia is admissible only as a navigation aid (find primary citations). Any Wikipedia URL in bibliography → HALT.
>
> ## Output
>
> Write `${BASE}/gates/gate-4.75.md` with sections:
> - `## IC-1 Type-Tag Presence`
> - `## IC-2 Bibliography Type-Tag Presence`
> - `## IC-3 Vendor-Not-Numerical`
> - `## IC-4 Anecdote-Not-Numerical`
> - `## IC-5 Practitioner-Protocol-Not-Efficacy`
> - `## IC-6 Compounding-Data-Sheet-with-Efficacy`
> - `## IC-7 Population-Mismatch`
> - `## IC-8 Route-Extrapolation`
> - `## IC-9 Concentration-Surfacing`
> - `## IC-10 No Fabricated Citations`
> - `## IC-11 No Placeholder Strings`
> - `## IC-12 No Wikipedia Citations`
> - `## Verdict`
>
> Each section: findings list (with line numbers) OR sentinel `No <X> detected.` Empty section without sentinel = HALT (orchestrator-side check).
>
> ## Verdict block
> ```yaml
> verdict: PASS|HALT
> halt_reasons: [list of IC-N codes that triggered HALT]
> warnings: [list of IC-N codes that produced warnings but not HALT]
> ```
>
> Orchestrator extracts `gate-4.75.json` from the `## Verdict` block. Downstream phases read JSON only.

---

## HALT escalation

If gate-4.75 HALTs, orchestrator:

1. Reads halt_reasons.
2. Dispatches a fix-agent for each HALT category (separate from synthesis agent), or returns to Phase 5 with the integrity findings injected as constraints, OR returns to Phase 3 if the issue requires new retrieval (e.g., new primaries needed to replace vendor-grounded numerical claims).
3. Re-runs gate-4.75 in full after fix. Max 3 iterations. Iter 3 without convergence → HALT `integrity-non-convergence`, surfaces for user adjudication.

---

## Limitations

- v1 does not detect paraphrased fabrications (a claim attributed to a real paper that the paper does not actually contain). Catching this requires per-citation corpus scoping (Quant pattern); v1 substitute is the paired-judge gate in Phase 3.5.
- v1 HEAD-check is best-effort against the listed budget; comprehensive validation defers to ultradeep mode.
- v1 route-extrapolation check requires route information in bibliography entries; reports that don't include route in citations get "route-unverifiable" warnings, not HALTs.
