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
> ### IC-13 — Per-citation corpus scoping (claims grep against source text)
>
> The most consequential check in v1. Addresses the failure mode where a claim is attributed to a paper that does not actually contain the claim (the He L 2022 attribution error in the 2026-05-23 BPC-157 dispatch was a milder version of this; the catastrophic version is fabricated quotes / fabricated numerical claims attributed to real papers).
>
> **Mode policy:**
> - quick: SKIP — gate phase 4.75 itself does not run in quick mode (see SKILL.md §Modes).
> - standard: ≥50% random sample of citations with numerical or quoted claims (minimum 10).
> - deep: ≥80% sample (minimum 20).
> - ultradeep: 100% (all numerical/quoted claims grep-verified).
>
> **Procedure (per checked claim):**
>
> 1. **Identify load-bearing claims.** Scan the draft for sentences containing:
>    - Numerical tokens (regex from IC-3): doses, n, effect sizes, %, p-values, half-lives, response rates.
>    - Verbatim quotations (text inside double quotes, block quotes, or `[N]†L<s>-L<e>` line-range markers).
>    - Specific scope claims ("the paper documents X", "the study shows Y", "the authors report Z").
>
> 2. **Fetch the cited primary's text.** For each claim, retrieve the cited paper's full text or abstract via:
>    - PubMed `efetch` (if PMID) — abstract minimum
>    - PMC full-text (if PMC ID)
>    - WebFetch on the direct URL (if no PubMed/PMC)
>    - For paywalled content: fetch abstract only; flag claim as `[abstract-only verified]` if found there, or `corpus-missing` if not retrievable
>    - Cache each retrieved corpus at `${BASE}/corpus/<cite_key>.md` to avoid re-fetching
>
> 3. **Grep the claim against the corpus:**
>    - **Verbatim quotes:** `rg -F -- '<quote text>' <corpus_file>`. Must match (with whitespace/typography normalization: NFKC + collapse-whitespace + smart-quote-to-ASCII).
>    - **Numerical claims:** `rg -F -- '<number with unit>' <corpus_file>`. If exact match not found, also try `±` variants and unit-normalized forms (e.g., "10 μg/kg" matches "10 microg/kg", "10 µg/kg", "10 ug/kg"). Author derivations (e.g., "calculated from data in [N]") are exempted if claim is annotated `[derived from N]`.
>    - **Paraphrased scope claims:** require ≥2 content tokens of ≥6 characters (non-stopword) from the claim to appear within 500 characters of each other in the corpus.
>
> 4. **Failure modes:**
>    - `quote-not-found` — verbatim quote does not appear in corpus
>    - `number-not-found` — numerical claim's exact value not in corpus (with normalization applied)
>    - `paraphrase-no-token-match` — paraphrased claim's content tokens not in corpus
>    - `corpus-missing` — corpus could not be retrieved at all (paywall + no abstract OR fetch failure)
>
> 5. **Verdict:**
>    - 0 failures → PASS
>    - Any `quote-not-found` or `number-not-found` → HALT `corpus-scoping-fail`
>    - `paraphrase-no-token-match` → WARN (orchestrator decides whether to demand rewrite or accept; multiple in same section → HALT)
>    - `corpus-missing` → WARN with explicit note in IC-13 findings; not a HALT (paywalls happen)
>
> **Caching contract.** All retrieved corpora cached at `${BASE}/corpus/<cite_key>.md`. Cache survives compaction. Re-runs of the gate reuse cached corpora; only newly-cited primaries trigger fetches.
>
> **JSON output (in `gate-4.75.json corpus_scoping` block):**
> ```json
> {
>   "corpus_scoping": {
>     "verdict": "PASS|HALT|SKIP-mode",
>     "claims_checked": 23,
>     "claims_failed": [
>       {
>         "claim": "BPC-157 reduced bleeding time by 47% [N, animal]",
>         "cite_key": "stupnisek-2012",
>         "failure_mode": "number-not-found",
>         "grep_command": "rg -F '47%' /tmp/aplus-research/bpc-157/corpus/stupnisek-2012.md",
>         "grep_output": "(no matches)"
>       }
>     ]
>   }
> }
> ```
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
> - `## IC-13 Per-Citation Corpus Scoping`
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

- v1 IC-13 covers verbatim quote + numerical-value + paraphrase-token grep. It does NOT catch high-fidelity paraphrase with full word substitution (a paraphrase that uses different words to describe the same concept the paper actually contains, where the paraphrase happens to mention something the paper does not contain). Mitigation: paired-judge gate in Phase 3.5 — judges are expected to flag conceptual paraphrase drift.
- v1 IC-13 corpus retrieval falls back to abstract-only for paywalled content; claims that the abstract doesn't cover get `corpus-missing` WARN, not HALT. Comprehensive paywall-bypass (institutional access, sci-hub, paper preprint chase) is not implemented in v1.
- v1 HEAD-check (IC-10) is best-effort against the listed budget; comprehensive validation defers to ultradeep mode.
- v1 route-extrapolation check (IC-8) requires route information in bibliography entries; reports that don't include route in citations get "route-unverifiable" warnings, not HALTs.
- v1 does not implement UUIDv4 agent-identity-ledger disjointness. Brief-hash uniqueness (sha256 of agent brief) is the v1 substitute, enforced at Phase 3.5 judge gate.
