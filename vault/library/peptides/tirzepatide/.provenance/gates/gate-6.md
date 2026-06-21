# Phase 6 CRITIQUE (red-team) — Tirzepatide — Iteration 2

## Scope of this re-review

Iteration 1 HALTed (major) on **citation integrity**: inline body tokens were section-local, so collided numbers (`[1]` = cryo-EM in §1 vs SURMOUNT-1 in §2; `[9]` = SURMOUNT-4 vs SURMOUNT-OSA), and several tokens dangled ([16]/[22]/[35]/[40]/[41]/[42]). The ~20.9% headline therefore resolved to the wrong paper. A renumber pass applied a `-trial`/`-osa`/`-summit`/`-mmo`/`-periop` suffix scheme to split collided numbers. This iteration re-checks the HALT cause mechanically and re-confirms the substantive axes.

## 1. Citation integrity — RESOLVED

**Mechanical token↔bibliography reconciliation (grep-based, full file):**
- Every inline `[n]` / `[n-suffix]` token that grounds a claim resolves to **exactly one** `## Bibliography` entry. Set diff of body tokens vs bibliography-defined entries yields **zero dangling** claim citations and **zero orphaned** bibliography entries.
- The only token that appears in the body without a line-start bibliography entry is `[6]`, and it occurs **once**, inside the Provenance/Deduplication note, as a description of the *original per-section* numbering ("...Section E [6]..."). It is documentation of the dedup history, not a claim citation. This is not a dangling reference.
- **Previously-dangling tokens** [16], [22], [35], [40], [41], [42] are **fully gone** — neither cited nor defined anywhere. Confirmed.

**Collision pairs — now distinct, self-consistent, one-entry-each:**
- `[1]` = Sun, cryo-EM structure (PNAS 2022, PMID 35333651) — mechanism/structure only.
- `[1-trial]` = Jastreboff, SURMOUNT-1 (NEJM 2022, PMID 35658024) — the ~20.9% headline.
- `[9]` = Aronne, SURMOUNT-4 (JAMA 2024, PMID 38078870) — +14.0% regain.
- `[9-osa]` = Malhotra, SURMOUNT-OSA (NEJM 2024, PMID 38912654) — AHI/approval.
- `[10]` = Rosenstock, SURPASS-1 (Lancet 2021) vs `[10-osa]` = Cheskin, OSA summary (Ann Intern Med 2024) — also cleanly split.

Verified that bare `[1]` attaches **only** to structural/mechanism/PK claims (co-formulation, twincretin, 39-aa, acylation linker, cryo-EM, ~5-day half-life) — no efficacy figure leaks onto the cryo-EM paper. The original collision is genuinely cured.

**Suffix scheme:** per the calibration note, the `-trial`/`-osa`/etc. labels are unusual aesthetically but every token maps to one unambiguous entry with no residual collision or wrong-paper resolution — so this is ACCEPTABLE and is NOT a HALT cause.

## 2. Four load-bearing spot-checks — ALL CORRECT

1. **SURMOUNT-1 ~20.9%** (§1 line 25, TL;DR line 31, §2.2 line 102, §2.3 line 109) → `[1-trial]` → **Jastreboff 2022 SURMOUNT-1**. CORRECT (no longer cryo-EM).
2. **SURPASS-2 superiority over semaglutide 1 mg** (§1, TL;DR, §2.1) → `[2]` → **Frías 2021 SURPASS-2 NEJM**. CORRECT.
3. **SURMOUNT-OSA AHI −20.0 / −23.8 events/hr** (§3.1 lines 129–130) → `[9-osa]` → **Malhotra 2024 SURMOUNT-OSA NEJM**. CORRECT.
4. **SURMOUNT-4 regain +14.0%** (§1, TL;DR, §2.2 line 105, §5.2, §7) → `[9]` → **Aronne 2024 SURMOUNT-4 JAMA**. CORRECT.

## 3. Crosswalk table — removed, no orphan pointer

The body now uses unified numbers directly. No "crosswalk", "see table", "renumber", or "old numbering" pointer survives anywhere in the file. The Provenance/Deduplication note documents the section→unified mapping in prose but does not reference a removed table or leave a dangling pointer to one. Clean.

## 4. Substantive axes — re-confirmed (still hold)

- **Balance:** benefits and caveats explicitly paired in §1 "Read this first," TL;DR, §7, and the closing balance check (line 424).
- **Dual mechanism:** GIP+GLP-1 "twincretin," distinct from semaglutide's GLP-1-only, stated up front and throughout (§1.1–1.6).
- **Population annotation:** every efficacy figure tagged T2D vs non-diabetic obesity vs OSA vs HFpEF; SURMOUNT-1 vs SURMOUNT-2 attenuation framed explicitly as a population effect, not dosing (§2.2 line 103).
- **OSA belongs here:** carried as an APPROVED indication (FDA Dec 2024) on objective AHI endpoint (§3.1), correctly inside scope.
- **SURPASS-CVOT non-superiority:** stated as non-inferior, NOT superior; explicitly a safety result, not a CV risk-reduction label (§3.2, line 138).
- **Thyroid C-cell:** carried as RODENT-based with human relevance "has not been determined," not a demonstrated human carcinogenicity finding (§5.6 verbatim label quote).
- **Regain:** honestly stated as maintenance-dependent; +14% on placebo (§5.2, §2.2, §7).
- **Regulatory/WADA:** FDA/EMA dates correct; WADA NOT prohibited, Monitoring Program from 1 Jan 2026 (surveillance, not ban) (§6.4).
- **No Wikipedia:** confirmed — no Wikipedia source in bibliography or body; Provenance note attests this.
- **Sponsor concentration:** single-sponsor (~95% Lilly) caveat carried transparently (§4, §7).

## Findings

One minor cosmetic note (NOT a HALT): the `[6]` mention inside the Deduplication prose references old per-section numbering and could momentarily read as a stray token to a naive grep; it is correctly a historical description, not a claim citation. No action required; flagged only for transparency.

## Verdict

verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-tzp-i2","draft_path":"vault/library/peptides/tirzepatide/research-report.md","findings":[{"category":"citation-incomplete","severity":"minor","description":"The token [6] appears once inside the Provenance/Deduplication prose ('Section E [6]') describing the original per-section numbering; it is historical documentation, not a claim citation, and has no line-start bibliography entry by design. Harmless but could read as a stray token to a naive grep. No fix required."}],"additional_retrievals":[],"halt_reasons":[],"iterations":2,"verdict":"PASS"}
```
