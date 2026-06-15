---
title: "Self-Improvement Loop — operational playbook"
type: guide
owner: framework
created: 2026-06-13
last_reviewed: 2026-06-13
status: active
review_cadence: manual
---

# Self-Improvement Loop — Playbook

The operational companion to **Discipline 11 (Cross-Deployment Learning)**. This is
the mechanism that keeps the whole system — framework, roles, skills, toolkit —
getting *less wrong* every deployment instead of re-shipping the same hole.

**It is a playbook, run by a human/agent — but its inputs are mechanically enforced
(F-017).** The judgment is human; the data-capture is unskippable. Designed so that
once it has been run enough, the accumulated records become the spec + training data
to hardwire it as automation.

## The three layers (separate the evidence from the handle)

| Layer | Artifact | Job | Reader |
|---|---|---|---|
| Evidence (narrative) | the **PF log** | why a failure happened, root cause | humans |
| Evidence (machine) | **`harvest.jsonl`** (append-only; `schemas/harvest-record.md`) | the harvestable record | the harvest + future automation |
| Tracking + surfacing | **beads** | priority/status/dependencies; surface it | the operator |
| Enforcement | the **toolkit gates** | make capture unskippable | mechanical |

A failure that isn't in all of PF + `harvest.jsonl` + a bead does not exist as far as
the loop is concerned — and `harvest-gate.sh` refuses to close the session until it is.

---

## Loop A — per-artifact wire (every session; the fast loop)

When a failure implicates a specific artifact (a role, a skill, the framework):

1. **Capture** — write the PF entry (narrative). Run `pf-ingest.sh --pf-entry <entry>
   --target-artifact <role/skill>` → it emits the `harvest.jsonl` FAIL record **and** a
   nominated anti-pattern / negative-example stub ("I don't <inverse-rule>…").
2. **Track + surface** — file a bead pointing at the record; the close-disclosure step
   (Discipline 1) surfaces it to the user, tagged `surfaced_by`.
3. **Improve the artifact** — feed the nominated stub to `/upgrade-agent` (role) or
   `/upgrade-skill` (skill): the failure becomes a permanent anti-pattern/negative
   example in that artifact's profile. **This is the wire that is dead today (F-018):
   no role's anti-patterns grow from PF data.** This step closes it.
4. **Enforce** — `harvest-gate.sh` blocks a clean close if any session failure is
   missing from any layer. No quiet hand-waving.

> The single most important fix this loop ships: a failure that cost trust once now
> permanently hardens the artifact that caused it.

---

## Loop B — cross-deployment harvest (periodic; the compounding loop)

The promotion trigger is **convergence**: a failure/practice seen in **≥2 independent
deployments** stops being local and becomes a framework-level change. Run on a cadence
(every framework review boundary, or when a new deployment closes its first ~30 sessions):

1. **Ledger** — one structured record-set per deployment (`harvest.jsonl` + the PF log),
   practices classified `adopted-as-is / mutated / added / absent` against the canonical
   disciplines.
2. **Matrix** — lay the ledgers side by side, one row per practice, one column per
   deployment, with a **convergence verdict** (`convergent / divergent / convergent-absence
   / unique-to-one`). Convergence and convergent-absence are the promotion signals.
3. **Rubric + skeptic** — score each nomination (generality · evidence · enforceability ·
   composability · maturity · cost · convergence). Then an **independent skeptic** that may
   only `uphold / downgrade / reject` — never silently raise a score. The skeptic catches
   the false-green at the *promotion* layer (a "3-project convergence" that is really 2 solid
   legs plus one false-green must be downgraded). Record the audit trail.
4. **Promote, gated by a negative test** — a nominated audit/hook that cannot prove it
   FAILs on bad input (`tests/run-all-tests.sh`) does **not** ship (F-007). A convergent
   *absence* — a discipline nobody enforces — is a first-class, framework-authored target.
5. **Version + pull** — the framework + toolkit version bumps; deployments pull on their
   next boundary and re-run `run-all-tests.sh` before adopting. Learning also **subtracts**:
   when ≥2 deployments disprove a rule (e.g. the literal 99/100, F-006), the harvest removes
   or rewrites it.

---

## Enforced inputs (which gate enforces what)

| Gate | Enforces | When |
|---|---|---|
| `harvest-gate.sh` | every failure in PF + `harvest.jsonl` + a bead (Loop A) | session close |
| `close-audit.sh` | runs `run-all-tests.sh` + the invariant audits; FATAL if any can't run (F-008) | session close |
| `parity-audit.sh` | catalog ↔ disk ↔ deployed parity; no dead refs (F-022) | per harvest / pre-release |
| `consistency-audit.sh` | no skill↔role↔framework contradiction (F-019/020/006/005) | per harvest / pre-release |
| `run-all-tests.sh` | every promoted audit proves it goes RED on bad input (F-007) | before any toolkit pull |

## Surfacing (make failures un-ignorable)
- **Close-disclosure** (Discipline 1) — at close, catalogue failures the operator caught
  that the user did NOT flag, tagged `surfaced_by`.
- **Top-N forward pointer** — the most-live failure modes carried in the continuity doc.
- **Harvest digest** — Loop B's matrix output, surfaced at each review boundary.

## Graduation to automation
Every step above with a defined input gate + output record is an **automation seam**.
The schemas (`harvest-record.md`) are the contracts an automated harvester implements
unchanged. "Run it enough" = accumulate enough `harvest.jsonl` that the machine is
writable. `bd`'s `patrol`/heartbeat primitives are the recurring-ops substrate for that day.

## Dogfood note
This playbook is not theoretical: the distillation that produced this framework **was its
own reference run** — ledgers per deployment → cross-reference matrix → rubric + independent
skeptic (which caught real fabricated convergences and a false-green audit) → promotions
gated by negative tests. The loop built the framework; the framework now ships the loop.
