---
title: Wiki Population Research Plan
type: plan
owner: Walter McGivney
created: 2026-06-14
last_reviewed: 2026-06-14
status: active
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/research-plan/wiki-population-research-plan
---

# Wiki Population Research Plan

The executable plan for filling the (currently near-empty) knowledge base. The
infrastructure — the `/aplus-research` gated pipeline, the 16-specialist consumer
roster, the commit-time ingestion gate, the provenance verifier, the periodic
lint — is **already built and tested**. This plan is the *content* track: what to
research, in what order, by what method, populated correctly, and verified correct.

> **Audience:** a future session that executes this end-to-end. Read it in full
> before starting (PF-S17-01 read-before-invoke). It tells you WHAT, HOW, and how
> to PROVE each entry is done — but it does not re-derive the gate internals; those
> live in `.claude/skills/aplus-research/SKILL.md` and `vault/WIKI.md`, which you
> also read in full before your first dispatch.

---

## 0. How to use this document

1. Read §1 (premises) so you don't rebuild built infrastructure.
2. Pick the current wave from §3 (the backlog is wave-ordered; do not jump ahead —
   §3 ordering is by operator relevance + dependency).
3. For each entry in the wave, run the §4 methodology (the `/aplus-research`
   pipeline), then §5 (populate the wiki page), then §6 (verify) — the §7 per-entry
   lifecycle is the exact command sequence.
4. A wave is DONE when every entry passes its §6 acceptance checklist AND the
   periodic `wiki-lint.sh` introduces no new blocking violation. One wave is a
   natural session boundary; PR the wave's entries together.
5. Surface the §8 decisions to the operator BEFORE they block you — several waves
   need an operator call (which compounds he's actually considering; the goal/limit
   anchors; whether a marker enters the doctor-handout queue).

---

## 1. Premises — what is already built (do NOT rebuild)

| Built | Where | Don't |
|---|---|---|
| The gated research skill (`/aplus-research`, 7 blocking gates — 6 attestation-chained; 2.75 is schema-only) | `.claude/skills/aplus-research/` | re-implement gates; invoke the skill |
| The wiki schema + 16-specialist consumer roster | `vault/WIKI.md` | redefine entity types |
| Entity templates (compound, biomarker) | `vault/{compounds,biomarkers}/_template.md` | invent a page shape |
| Source whitelist + 12-tag type enum + admissibility matrix | `vault/library/_source-whitelist.md` | cite off-list sources as anything but `anecdote_aggregate` |
| Commit-time ingestion gate (per-page battery) | `scripts/wiki-ingest-lint.sh` via `block-ungated-vault-write.sh` | bypass it; it BLOCKS a non-conforming page at commit |
| Provenance verifier (presence-then-integrity) | `scripts/audit-research-provenance.sh` (bda) → `gate_attest.py verify-chain` | hand-write gate JSON; `gate_attest.py` is the only canonical writer (PF-S3-01) |
| Periodic whole-vault graph lint (6 checks) | `scripts/wiki-lint.sh` | skip it at wave close |

**Current content state (the starting line):** 1 real compound (BPC-157, grandfathered),
0 biomarkers, 0 of the other 5 compound classes, 0 parameters, 0 labs. The engine is
built; the tank is empty.

---

## 2. Scope

**In scope — goal-agnostic library research** (the entries `/aplus-research` produces
and the ingestion gate governs):
- **Compound entries** — `vault/compounds/<slug>.md` + `vault/library/<class>s/<slug>/{research-report,practitioner-layer,non-english-layer}.md`
- **Biomarker entries** — `vault/biomarkers/<slug>.md` + `vault/library/biomarkers/<slug>/research-report.md`
- **Library reference entries** — domain `research-report`s where a specialist needs a grounding corpus

**Out of scope (a different track — do NOT do here):**
- **Operator-personalized** protocols (`protocols/meal-template`, exercise programming),
  parameters (his protein g/kg), n=1 experiments, lab VALUES — these are
  *specialist-agent dispatches against his data*, not goal-agnostic library research.
  A library entry says "what creatine IS and the evidence"; a protocol says "what
  Walter takes". This plan builds the former. (PF-S2-04: never inject operator fields
  into a library-build dispatch — the meta files load as context for linkage only.)
- The dashboard, the PII boundary, the clone story — all done.

**The goal-agnostic rule (load-bearing):** every entry is a canonical, reusable,
vetted source — written as if for any operator, never pre-filtered for Walter.
Walter's context informs the *order* (§3 priority), never the *content*.

---

## 3. The research backlog — WHAT to research (wave-ordered)

Ordering rationale: (a) the **July 13 doctor visit** is the first real consumer, so the
biomarker reference set the visit's labs will be read against comes first; (b) the
**peptide `_triage.md`** names healing + immune peptides as the highest-priority class
given the post-January-2026 recovery; (c) breadth (other compound classes) follows depth.

> Counts below are the *implied target set* from `vault/library/peptides/_triage.md`
> (~30 peptide bullets across 7 classes; **29 unique** — Humanin is listed under both
> Immune/longevity and Mitochondrial), `goals.md` (the named blood panel), and the
> per-specialist library-index namespaces. They are a research surface, not a
> commitment — §8 Decision D1 asks the operator to confirm/trim before Wave 2+.

### Wave 0 — back-fill BPC-157 provenance (cleanup, optional-first)
BPC-157 is on the grandfather allowlist (`vault/library/_ingest-grandfather.txt`) — a
**back-fill obligation, not a permanent waiver**. It already had a deep `/aplus-research`
run (S3, the `--update=suspect-fabrications` rebuild). Either (a) reconstruct its gated
provenance into a `design/.bpc-157-design-work/` dir + add the `provenance_dir`/`_slug`
frontmatter pointer and remove it from the grandfather list, or (b) leave it grandfathered
and note the obligation. Low effort; do it first to validate the §7 lifecycle against a
known-good entry before researching new ones.

### Wave 1 — the baseline biomarker reference set (visit-critical, researchable NOW)
The canonical reference entries (what each marker IS, target range, what affects it) — NOT
lab-gated (the operator's *value* arrives in July; the *entry* is goal-agnostic and
buildable today). This is what `labs-specialist` interprets the July panel against.
`target.type=biomarker` → **mode: standard** (biomarkers skip the 7.5 risk-floor + 8.5
layers gates; those are compound-only). ~20 entries, grouped:

- **Metabolic panel (CMP/CBC-derived):** fasting glucose, HbA1c, fasting insulin (+ HOMA-IR as `category: functional`/`calculation`), the CMP electrolyte/liver/kidney markers the executor judges worth their own entry (ALT, AST, eGFR, …).
- **Lipids / CV risk:** ApoB, Lp(a), LDL-C, HDL-C, triglycerides, GlycA, hs-CRP.
- **Thyroid:** TSH, free T3, free T4.
- **Hormones (endocrine-specialist class):** total testosterone, free testosterone, estradiol, cortisol (AM), DHEA-S, IGF-1, SHBG.
- **Vitamins/minerals:** vitamin D (25-OH), ferritin, B12, magnesium (RBC).
- **Wearable (Whoop via ADR-0011 `noop`; `source: wearable`, `category: wearable`; NOT lab-gated, buildable now):** HRV, resting HR, sleep efficiency, respiratory rate, recovery/strain (the Whoop-derived markers).

### Wave 2 — recovery + immune peptides (operator-relevant; triage-flagged top class)
The peptides `_triage.md` flags as the highest-priority first deep passes given the
post-illness deconditioning + immune recovery. `target.type=compound` → **mode: deep**
(peptides are the high-risk class; deep fires the 6-CRITIQUE gate + 7.5 + 8.5):
- **Healing/soft-tissue:** TB-500, GHK-Cu, KPV, LL-37 (BPC-157 ✓ already done) — the full `_triage.md` healing class, the top-priority post-illness recovery cluster.
- **Immune/recovery:** Thymosin Alpha-1 (triage: "strongest post-illness immune candidate").
- **GH secretagogues (paired with the IGF-1 biomarker from Wave 1):** Ipamorelin, CJC-1295 (no-DAC).

### Wave 3 — the rest of the triaged peptide library (breadth)
The remaining ~21 `_triage.md` peptides by class (29 unique − Wave 0's 1 − Wave 2's 7) — GH secretagogues (Tesamorelin,
Sermorelin, Hexarelin, MK-677), metabolic (Semaglutide, Tirzepatide, Retatrutide,
AOD-9604), cognitive (Selank, Semax, Cerebrolysin, Dihexa, …), sexual/dopaminergic
(PT-141, Melanotan II, Kisspeptin-10), immune/longevity (Epitalon, FOXO4-DRI, Humanin),
mitochondrial (SS-31, MOTS-c). **deep** mode each. Triage-scan with **quick** mode first
(non-canonical, cheap) to re-confirm priority order before committing deep passes.

### Wave 4 — other compound classes (supplement / hormone / nootropic / geroprotector)
Owner-specialist-implied, operator-confirmation-gated (§8 D1):
- **Supplements** (supplement-specialist): the common evidence-backed stack — creatine,
  magnesium glycinate, omega-3, vitamin D, etc. `target.type=compound`, **standard** mode
  for low-risk OTC (deep only if `risk_tier` lands high/experimental).
- **Hormones/TRT** (endocrine-specialist): testosterone, thyroid hormone, DHEA — **deep**
  (these will land `risk_tier: high`+, firing 7.5 risk-floor).
- **Nootropics / geroprotectors** (mental-performance-coach / longevity-strategist):
  operator-confirmation-gated; mode by risk_tier.

> **Per-class mode default:** peptide/hormone/experimental → **deep**; OTC
> supplement/herbal low-risk → **standard**; triage scans → **quick** (non-canonical).
> The authoritative floor per slug is `templates/specialist-risk-class.yaml` (the bda
> `mode_floor`); never go below it.

---

## 4. Methodology — HOW to research one entry (the `/aplus-research` pipeline)

Invocation:
```
/aplus-research "<research question>" --mode=<quick|standard|deep|ultradeep> --target=<class>/<slug> [--update[=<reason-slug>]]
```
- `--target` class enum: `peptide|supplement|hormone|nootropic|pharmaceutical|herbal|biomarker|protocol|other`; slug kebab-case.
- For a re-research of an existing entry, `--update=<reason-slug>` archives-before-write (Phase 2.75).
- **Goal-agnostic:** phrase the question canonically ("Build the canonical library entry for X"); do NOT inject Walter's profile — the meta files load as context only.

**The gate sequence the skill runs** (do not approximate it — invoke the skill, which
runs these; `gate_attest.py` is the only canonical gate-JSON writer):

| Gate | Fires in | What it enforces |
|---|---|---|
| 2.75 SCOPE | all | 4 context files loaded; target declared; output paths writable; overwrite/`--update` policy. *Mechanical, not attested.* |
| 3.5 JUDGE | all | N paired retrieval+judge dispatches; all judges PASS at the mode threshold (quick 85 / standard 92 / deep 99). Self-judging does NOT count (Hard Rule 1). |
| 4.25 ID-RECONCILE | standard+ | cross-section identity agreement (citations, institutions, compound IDs, regulatory dates, trial regs). |
| 4.75 INTEGRITY | standard+ | IC-1..IC-13 incl. **IC-7 population-mismatch** (animal/in-vitro numerical claims tagged), **IC-9 concentration-audit** (single-lab share ≥70% → mandatory first-class concentration section), **IC-13 per-citation corpus scoping** (grep claims against fetched primaries; ≥50% standard / ≥80% deep / 100% ultradeep). |
| 6 CRITIQUE | deep+ | independent red-team agent; no unaddressed `critical` finding. |
| 7.5 RISK-FLOOR | compounds | if `risk_tier` lands experimental/high → contraindications + monitoring + stopping-criteria populated from cited sources; **experimental → a third-party monitoring biomarker `[[biomarkers/<name>]]` is mandatory** (subjective self-report insufficient). |
| 8.5 LAYERS | standard+ compounds | `practitioner-layer.md` (≥1 compounding data sheet OR explicit null-finding + searched-vendor list) + `non-english-layer.md` (≥3 of Russian/Chinese/originator-country/Korean/Japanese, findings or explicit absence), each with its own `## Bibliography` + `## Self-check`. |

**HALT conditions to expect:** `context-load-missing` (a meta file or the whitelist absent
— fill `operator-profile.md`/`goals.md`/`current-state.md` first; see §8 D3),
`compound-entry-exists` (use `--update`), the per-gate non-convergence after 3 iterations
(user adjudication). The attestation chain is sha256-bound to each agent-written source;
`verify-chain` catches any post-attest edit.

**The mode→gate→artifact map and the full HALT enum are in `SKILL.md`** — read it before
the first dispatch. `gate_attest.py` / `bda` / `verify-chain` require the project `.venv`
(they import `jsonschema`, which system python3 lacks).

---

## 5. Populating the wiki correctly — the ingestion contract

A researched entry becomes a wiki page that MUST pass the commit-time gate
(`wiki-ingest-lint.sh`). The page carries a provenance pointer back to its gate dir.

**Frontmatter (every gated page):**
- `provenance_dir:` — the `design/.<slug>-design-work` dir holding the `gates/` (copy the
  bare `gates/`/`judges/`/`sections/` from `/tmp/aplus-research/<slug>/` into it).
- `provenance_slug:` — the bda slug keying `templates/specialist-risk-class.yaml`.

**Compound page** (`vault/compounds/<slug>.md`):
- frontmatter: `class` (supplement|peptide|nootropic|pharmaceutical|hormone|herbal),
  `evidence_tier` (S|A|B|C|D), `risk_tier` (low|medium|high|experimental), `status`
  (researching|planned|active|paused|trialed-stopped|excluded), `last_verified` (YYYY-MM-DD).
- required `## ` sections (gate-enforced): Metadata, Mechanism, Evidence Summary, Protocol,
  Risk Profile, Trial Status, Relations.
- template-mandated (NOT gate-enforced — assert manually): **Non-English Literature
  Coverage**, **Prescribing-Practice Layer** (their *content* is guaranteed upstream by
  gates 8.5/7.5 for a compound entry, but the commit gate doesn't check the headers).
- `risk_tier: experimental` → also: populated contraindications, ≥1 `[[biomarkers/...]]`
  monitoring link, populated stopping criteria.

**Biomarker page** (`vault/biomarkers/<slug>.md`):
- frontmatter: `category` (blood|wearable|functional|subjective), `unit`, `source`
  (lab|wearable|manual|calculation — Whoop-derived markers use `source: wearable`, the
  specific device recorded in the entry body per ADR-0011 D4), `confidence` (established|supported|provisional),
  `last_verified`.
- required `## ` sections (gate-enforced): Metadata, Target Range, Current Value,
  Affected By, Relations.

**Source discipline:** every numerical/dose/effect-size claim cites a whitelist source at
an admissible tier; each source carries exactly one of the 12 type tags; no efficacy from
Tier 2.7/3/4/5; no numerical claim grounded on `vendor_label`/`anecdote_aggregate`.

**Index sync:** register the page in `vault/meta/index.md` under its type heading as
`[[<type>/<slug>]]` **in the same commit** — the gate BLOCKS an unregistered page.

**Commit sequencing:** `git add <page> <index.md>` as its OWN command, then `git commit`
SEPARATELY — the hook denies single-call stage+commit, `git commit -a`, and pathspec
`git commit <path>` (their content is invisible to the staged-set scan).

---

## 6. Verifying it was done correctly — the per-entry acceptance gate

An entry is **DONE** only when ALL of the following hold. (C = enforced by the commit gate;
R = research-phase; M = template mandate not caught by the commit gate; P = periodic lint.)

**Provenance (upstream of the page):**
1. (R) Researched via `/aplus-research` at ≥ the slug's `mode_floor` (`specialist-risk-class.yaml`).
2. (R) `design/.<slug>-design-work/gates/` holds `gate-2.75.json` (with `target.type` correct) + every mode-required attested gate (3.5; +4.25/4.75 at standard; +6 at deep; +7.5/8.5 for a compound at standard+), each with an `attestation_chain`.
3. (C/R) `.venv/bin/python` → `scripts/audit-research-provenance.sh <design-work-dir> <slug>` exits 0 (presence-then-integrity; `verify-chain` reports no sha mismatch / missing source).
4. (R) Every numerical claim cites an admissible whitelist source, correctly type-tagged.

**Page (template + enums):**
5. (C) First line `---`; provenance frontmatter present (or grandfathered — provenance-exempt only).
6. (C) Required frontmatter fields present + enum-valid (per §5).
7. (C) All required `## ` sections present (per §5).
8. (C, experimental) contraindications + `[[biomarkers/...]]` + stopping-criteria populated.
9. (M, compound) Non-English Literature Coverage + Prescribing-Practice Layer present + populated.
10. (M) Real values, not pointers — actual dose/route/source on compounds, actual range on biomarkers; every claim cited; nothing from memory.

**Graph + commit:**
11. (C) Registered in `vault/meta/index.md` (same commit).
12. (C) `git add` + separate `git commit` lands (the PreToolUse gate runs `wiki-ingest-lint.sh`, exit 0, no VIOLATION lines).
13. (P) WIKI.md Ingest follow-ups: contradiction check vs existing pages (→ `meta/contradictions.md` if any), `meta/overview.md` if system state shifts, append to `meta/log.md`.

**Wave close (after all entries in the wave):**
14. (P) `scripts/wiki-lint.sh` introduces **no new blocking violation** (the 2 blocking checks: open contradiction; dead/typo'd namespace link).
15. The Python suite stays green (`.venv/bin/python -m pytest -q`).

> A green commit gate + a green `bda` chain + the M-items present + a clean periodic lint =
> the entry is correctly researched, populated, and verified. There is no "looks done" —
> the gates are the definition of done.

---

## 7. Execution model — per-entry lifecycle + batching

**Per-entry command sequence:**
```
1. /aplus-research "Build the canonical library entry for <X>" --mode=<m> --target=<class>/<slug>
   → runs the gates; artifacts land in /tmp/aplus-research/<slug>/{gates,judges,sections,corpus}/
2. cp -r the bare gates/ judges/ sections/  →  design/.<slug>-design-work/
3. .venv/bin/python scripts/audit-research-provenance.sh design/.<slug>-design-work <slug>   # must exit 0
4. author vault/<type>/<slug>.md (+ library/<class>s/<slug>/ layers for compounds) to the template,
   with provenance_dir/_slug frontmatter
5. register the page in vault/meta/index.md
6. git add <page> <layers> vault/meta/index.md   # its own command
   git commit -m "feat(wiki): <slug> <type> entry"   # separate; the gate fires here
7. run the §6 acceptance checklist; if any C-item blocked the commit, fix + re-commit
```

**Batching / session boundaries:**
- One **wave** per session (or the remaining entries of an open wave). A wave is the unit;
  it is not done until every entry passes §6 and the periodic lint is clean.
- PR the wave's entries together (one `feature/wiki-wave-<n>-<theme>` branch → `main`).
- Run the standard PR lifecycle on the wave PR: `/review-pr` (the entries are content +
  citations — a full or content-focused review catches fabrication/tier-misuse the gates
  can miss in prose) → fix legitimate findings → `/merge`. Verify-first each entry's claims.
- **Provenance dirs (`design/.<slug>-design-work/`) are git-ignored working artifacts** —
  do NOT commit them to the trunk; the frontmatter *pointer* + the bda pass at author-time
  is the contract. (Confirm the `.gitignore` posture before the first wave; if the gate
  needs the dir present at commit time on the trunk, resolve that in §8 D4.)

**Recovery after compaction (mid-dispatch):** read `/tmp/aplus-research/<slug>/gates/` for
the highest gate with `verdict: PASS`, resume at the next phase (SKILL.md recovery section).

**Scale estimate (for sequencing, not a commitment):** ~20 biomarkers (standard) +
~30 peptides (deep) + ~10-15 other compounds = ~60-65 gated dispatches. Deep dispatches are
expensive (N paired retrieval+judge agents + critique + layers). Sequence by wave; do not
fan all of them out at once. Each deep compound is roughly a session's worth of gated work.

---

## 8. Decisions the executor must surface to the operator

These block specific waves; get the operator's call before proceeding past them.

- **D1 — Compound shortlist (blocks Wave 2-4).** The `_triage.md` 30 peptides + the
  supplement/hormone classes are a *surface*, not a commitment. Ask the operator which
  compounds he is actually considering (for the July visit + his goals) so the deep passes
  (expensive) target the real shortlist, not all 30. The wiki entries stay goal-agnostic;
  only the *order/selection* is operator-informed.
- **D2 — Whoop biomarker mapping — RESOLVED by ADR-0011 D4 (propagated S62).** The biomarker
  `source` enum was generalized `oura`→`wearable` (device-agnostic); Whoop-derived markers use
  `source: wearable`, with the specific device (Whoop via noop) recorded in the entry
  body/metadata, not the enum. The propagation landed at S62 — `wiki-ingest-lint.sh`
  `check_biomarker` + the biomarker template + `vault/WIKI.md` all carry
  `lab|wearable|manual|calculation`, and `category: wearable` already exists. No further enum
  change is needed; the ingestion path is ADR-0011's noop CSV-export adapter.
- **D3 — Context-file fill (blocks ALL standard+ dispatches).** Gate 2.75 HALTs with
  `context-load-missing` if `operator-profile.md` / `goals.md` / `current-state.md` are
  unreadable. They are currently scaffolds. For *library* (goal-agnostic) dispatches they
  load as context only (not injected), but they must EXIST and be readable. Confirm the
  scaffolds satisfy the gate's read, or fill the minimum the gate requires, before Wave 1.
- **D4 — Provenance-dir trunk posture (blocks the first commit).** Confirm whether the
  `design/.<slug>-design-work/` provenance dirs are git-ignored (working artifact, pointer-only
  contract) or must be committed for the gate's `bda` call to resolve at commit time on a
  fresh checkout. Resolve before the first wiki-page commit (it determines what lands in the PR).
- **D5 — BPC-157 back-fill (Wave 0).** Reconstruct gated provenance + de-grandfather, or
  leave grandfathered with the obligation noted? Operator/executor call.

---

## 9. Appendix — quick reference

**Mode → gates → output floor:**

| Mode | Gates fired | Source floor | Report floor | Judge threshold | Canonical? |
|---|---|---|---|---|---|
| quick | 2.75, 3.5 | 10+ | 2,000w | 85 | NO (triage only) |
| standard | 2.75, 3.5, 4.25, 4.75, (7.5, 8.5 if compound) | 15+ | 4,000w | 92 | yes |
| deep | + 6 CRITIQUE | 25+ | 10,000w | 99 | yes |
| ultradeep | deep + extended critique/refine | 30+ | 15,000w | 99 | yes |

**12 source type-tags:** rct, meta_analysis, cohort, open_label, animal, in_vitro,
mechanism_review, regulatory, compounding_data_sheet, vendor_label, practitioner_protocol,
anecdote_aggregate.

**Key paths:** `.claude/skills/aplus-research/SKILL.md` (methodology) · `vault/WIKI.md`
(schema + Ingest/Lint ops) · `vault/library/_source-whitelist.md` (tiers + admissibility) ·
`vault/library/peptides/_triage.md` (the 30-peptide surface) · `vault/{compounds,biomarkers}/_template.md`
· `templates/specialist-risk-class.yaml` (mode_floor per slug) · `scripts/{wiki-ingest-lint,wiki-lint,audit-research-provenance}.sh`
· `vault/meta/index.md` (register here) · `vault/library/_ingest-grandfather.txt`.

**The one-line definition of done for the whole track:** every entry in the implied target
set (operator-trimmed per D1) has a green `bda` provenance chain, passed the commit gate,
carries real cited values to template, is registered in the index, and survives the periodic
`wiki-lint.sh` — at which point the 16 specialists have a knowledge base to reason over and
the July-visit handout has real entries to draw from.

---

## 10. Active research claims — cross-session coordination

Two sessions are populating the wiki in parallel. **Before picking a subject, read this
table; after picking, append your claim** so the two tracks don't duplicate. A claim is
(session, subject/cluster, wave, mode, status, date).

| Session | Subject / cluster | Wave | Mode | Status | Date |
|---|---|---|---|---|---|
| `feature/wiki-research` (merged) | **Lipids / CV-risk biomarkers** — ApoB, Lp(a), LDL-C, HDL-C, triglycerides, GlycA, hs-CRP (7 entries) | 1 | standard | **DONE — merged to main** (PR #160 squashed; gates 2.75/3.5/4.25/4.75 attested + bda-clean; `/review-pr` → 8 fixes incl. hs-CRP JUPITER cite + 7 `[[labs/]]` dead-links → `/merge`) | 2026-06-19 |
| `feature/research-bpc157-rerun` (other session) | **BPC-157** deep re-research + finished entry | 0 | deep | **DONE** — merged to `main` (PR #150, all gates attested) | 2026-06-18 |
| `feature/wiki-metabolic` worktree | **Metabolic — glycemic core** — fasting glucose ✓, HbA1c ✓, fasting insulin ✓, HOMA-IR ✓ (4 entries) | 1 | standard | **DONE — all 4 ingested** (gates 2.75/3.5/4.25/4.75 attested + bda-clean); cluster ready to PR → main | 2026-06-19 |
| `feature/wiki-metabolic` worktree | **Thyroid** — TSH ✓, free T4 ✓, free T3 ✓ (3 entries) | 1 | standard | **DONE — all 3 ingested** (gates 2.75/3.5/4.25/4.75 attested + bda-clean) | 2026-06-19 |
| `feature/wiki-metabolic` worktree | **Hormones (endocrine)** — total testosterone ✓, free testosterone ✓, SHBG ✓, estradiol ✓, cortisol (AM) ✓, DHEA-S ✓, IGF-1 ✓ (7 entries) | 1 | standard | **DONE — all 7 ingested** (gates 2.75/3.5/4.25/4.75 attested + bda-clean) | 2026-06-20 |
| `feature/wiki-metabolic` worktree | **Metabolic — CMP organ markers** — ALT ✓, AST, eGFR/creatinine, albumin, sodium, potassium (6 entries; the executor-judged CMP liver/kidney/electrolyte subset worth standalone entries) | 1 | standard | **IN PROGRESS** — 1/6 done (ALT ingested, gates attested + bda-clean); AST/eGFR/albumin/sodium/potassium remain | 2026-06-20 |

**Claim update mandate:** update this table when a subject is *claimed/started* (status `IN PROGRESS`), not only when it is done and ingested — so the parallel track never duplicates work that is underway. Flip a row to `DONE` as its entries land in the wiki.

**Still open (Wave 1 remaining clusters):** Metabolic — CMP organ markers
(ALT, AST, eGFR, electrolytes; the glycemic core glucose/HbA1c/insulin/HOMA-IR is CLAIMED above) · Thyroid (TSH, fT3, fT4) · Hormones (total/free
testosterone, estradiol, cortisol, DHEA-S, IGF-1, SHBG) · Vitamins/minerals (vit D, ferritin,
B12, RBC-Mg) · Wearable (HRV, RHR, sleep-efficiency, respiratory rate, recovery/strain).
**Wave 0** (BPC-157) is **DONE** (above).

**Gate before any Wave 1 research (§8 D3):** confirm `operator-profile.md` / `goals.md` /
`current-state.md` are readable so gate 2.75 doesn't HALT `context-load-missing` — they load
as context only for goal-agnostic library entries (PF-S2-04).
