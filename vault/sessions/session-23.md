---
title: Session 23 — wiki ingestion gated (bte); commit-time accuracy battery + periodic lint
type: session
permalink: a-plus-maxing/sessions/session-23
created: 2026-06-02
session: S23
---

# Session 23 (2026-06-02)

## Goal (as contracted)

Make wiki ingestion mechanical (`bte`, expanded at Walter's direction): turn the
already-written-but-unenforced WIKI.md accuracy rules into TWO controls — a commit-time
blocking gate over `vault/{compounds,biomarkers,library}/` entity pages, and a periodic
whole-vault lint (WIKI.md's 6-check Lint, never previously scripted). Provenance is one
control among several. Register the new invariant via change-discipline.

## What happened

1. **Answered Walter's "is there a wiki guide?"** Yes — `vault/WIKI.md` (schema + Ingest/Lint/
   Conventions + entity templates), `library/_source-whitelist.md`, the `_template.md`s,
   `evidence-tiers.md`, `DOCUMENT_RUBRIC.md`. NOT inherited from a clone (first commit is a
   fresh `initial project setup`, no `upstream`). The gap: all of it was documented discipline —
   zero enforcement scripts lint vault content. Walter then broadened `bte` from provenance-only
   to the full accuracy battery + folding in the periodic lint.

2. **Shared lib** `scripts/lib/wiki-helpers.sh` — frontmatter-field/section/wikilink parsing,
   link resolution, entity-type + gated-page predicate. Smoke-tested against the real bpc-157
   page (caught a `basename` PATH bug → switched to bash parameter expansion).

3. **Commit-time blocking gate** `scripts/wiki-ingest-lint.sh` (14/14): provenance (bda +
   verify-chain via a `provenance_dir`/`provenance_slug` frontmatter pointer, grandfather-aware),
   structural conformance (compounds/biomarkers strict, library lighter — heterogeneous),
   frontmatter/enum validity, index sync. Link-integrity is **advisory** here (the real bpc-157
   legitimately forward-references ~12 unbuilt biomarker pages — hard-blocking would false-block
   buildout). Running it against the real page caught a brittle experimental-contraindications
   regex that false-flagged richly-populated content → replaced with a format-tolerant
   `marker_populated` (handles bold headers + following numbered lists vs empty template).

4. **PreToolUse hook** `.claude/hooks/block-ungated-vault-write.sh` (6/6) — denies a `git commit`
   staging a failing gated page; wired into `.claude/settings.json`; bash-3.2-safe; deny JSON via
   jq. **Production-path validated** against the real repo (real bda): a staged ungated page is
   denied citing the invariant.

5. **Periodic whole-vault lint** `scripts/wiki-lint.sh` (9/9) — WIKI.md's 6 checks; violations
   for dead-namespace links + open contradictions, advisory for orphan/stale/coverage/provisional/
   forward-ref. Running against the real vault caught a false "1 open contradiction" (matched the
   `## Template` code-fence example) → fixed by stripping fenced blocks.

6. **Invariant** `INV-WIKI-INGESTION-GATED` registered (change-discipline; Walter approved at
   contract confirmation). WIKI.md Ingest/Lint/Conventions updated to describe both controls +
   the provenance-pointer convention. Grandfather allowlist `vault/library/_ingest-grandfather.txt`
   seeded with the 4 pre-gate bpc-157 pages (provenance-exempt only; back-fill obligation).

## Discipline notes

- Two real bugs surfaced ONLY by running against real artifacts, not fixtures (the experimental
  false-positive; the code-fence contradiction) — AP-ACT-BEFORE-VERIFY / the mhg false-positive
  lesson applied to my own gate.
- The PF-S21 non-tautology near-miss replayed exactly: a `/tmp` reverted-script copy failed on a
  missing `lib/audit-helpers.sh` (wrong reason). Caught by reading the output; re-ran the revert
  proof with the copy inside `scripts/` → REAL=1 / NEUTERED=0 (provenance check is load-bearing).
- Link-integrity reclassified blocking→advisory at commit (forward-refs legitimate mid-buildout),
  blocking in the periodic lint — surfaced as a data-forced adjustment to the confirmed set, not
  silent.

## State at close

- Commit-time gate + PreToolUse hook + periodic lint all live; 29/29 new smoke + all 12 existing
  suites green. `bte` CLOSED. `INV-WIKI-INGESTION-GATED` live.
- First real exercise = the library-population phase (also PF-S22-01's falsification window).
- Next: `hil` (PII vault, P1).

See [[decisions/2026-06-02-single-trunk-reconciliation]] (prior session), INVARIANTS Change Log
(S23), [[WIKI.md]] Ingest/Lint/Conventions, HANDOFF What-Is-Next.
