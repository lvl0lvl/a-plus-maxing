#!/usr/bin/env python3
"""Mechanical resistance against orchestrator self-attestation of gate verdicts.

Built in response to PF-S3-01 (memory/process-failures.md): the orchestrator
self-attested 5 of 6 blocking gates during the first end-to-end aplus-research
run by writing gate-N.json directly from prose agent reports. v1 brief-hash
uniqueness only enforced format, not provenance.

This script is the canonical writer for `gates/gate-N.json` (N in {3.5, 4.75,
6, 7.5, 8.5}). Each gate JSON carries an `attestation_chain` referencing the
sha256 + mtime of the agent-written source file (`gates/gate-N.md` or, for
3.5, the set of `judges/judge-<section>.json`). Downstream phases call
`verify-chain` and HALT if the chain is broken.

Workflow:

    # Start an iteration (records iter_start_ts to gates/_iter-state.json)
    python3 lib/gate_attest.py start-iteration --base BASE --phase 4.75

    # Orchestrator dispatches the verifier agent. Agent writes gates/gate-4.75.md
    # with a `## Verdict` block containing `verdict: PASS` or `verdict: HALT`.

    # Orchestrator calls attest to produce the canonical gates/gate-4.75.json
    python3 lib/gate_attest.py attest --base BASE --phase 4.75

The attest call HALTs with a specific reason if:
- start-iteration was not called for this phase (no-iteration-started)
- agent-source markdown is missing (missing-agent-source)
- agent-source mtime <= iter_start_ts (stale-agent-source)
- agent-source has no parsable `## Verdict` block (verdict-not-parsable)
- composed gate JSON fails schema validation (schema-validation-failed)
- max iterations exceeded (max-iterations-exceeded)

Phase 2.75 is exempt — it is legitimately orchestrator-side per spec
(mechanical sha256 of context files + filesystem archive ops; no agent verdict).

Phase 3.5 is special — composes from N per-section judge JSONs. Each judge
JSON must (a) exist, (b) be fresher than iter_start_ts, (c) have a `verdict`
field. Latest-iteration of each section is used.
"""

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

import jsonschema  # required dependency; pre-flight should verify presence

ITER_STATE_FNAME = "_iter-state.json"
SCHEMA_DIR = pathlib.Path(__file__).resolve().parent.parent / "schemas"

ATTESTED_GATES = ("3.5", "4.25", "4.75", "6", "7.5", "8.5")
SOURCE_MD = {
    "4.25": "sections/id-reconcile-source.md",
    "4.75": "gates/gate-4.75.md",
    "6": "gates/gate-6.md",
    "7.5": "gates/gate-7.5.md",
    "8.5": "gates/gate-8.5.md",
}


class GateAttestationError(Exception):
    def __init__(self, reason, detail=""):
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}" if detail else reason)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def iter_state_path(base):
    return pathlib.Path(base) / "gates" / ITER_STATE_FNAME


def load_iter_state(base):
    p = iter_state_path(base)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def save_iter_state(base, state):
    p = iter_state_path(base)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2))


def start_iteration(base, phase, section=None):
    """Record iter_start_ts for a phase, optionally scoped to a section.

    BUG-001 (2026-05-25): v1 used per-phase iter_start_ts only. When phase 3.5
    needed a remediation iteration on a subset of sections (e.g., A and C
    re-judged while B/D/E/F were already passing), the new phase-wide
    iter_start_ts retroactively invalidated the still-correct per-section
    judge JSONs. Fix: phase 3.5 supports per-section iter_start_ts; attest
    uses per-section iter_start_ts when present, falls back to phase-wide.
    Phases 4.75/6/7.5/8.5 still use phase-only (their source is single-file).
    """
    if phase not in ATTESTED_GATES:
        raise GateAttestationError("unsupported-phase", phase)
    if section is not None and phase != "3.5":
        raise GateAttestationError(
            "section-scope-not-supported",
            f"--section is only valid for phase 3.5, not {phase}",
        )
    state = load_iter_state(base)
    if section is None:
        iters = state.setdefault(phase, [])
        n = len(iters) + 1
        if n > 3:
            raise GateAttestationError(
                "max-iterations-exceeded", f"phase {phase} already at iter 3"
            )
        entry = {"iteration": n, "iter_start_ts": now_iso()}
        iters.append(entry)
    else:
        phase_state = state.setdefault(phase, [])
        # Migrate phase_state to dict-shape if previously list-only.
        if isinstance(phase_state, list):
            state[phase] = {"phase_iterations": phase_state, "sections": {}}
            phase_state = state[phase]
        if "sections" not in phase_state:
            phase_state["sections"] = {}
        sec_iters = phase_state["sections"].setdefault(section, [])
        n = len(sec_iters) + 1
        if n > 3:
            raise GateAttestationError(
                "max-iterations-exceeded",
                f"phase {phase} section {section} already at iter 3",
            )
        entry = {"iteration": n, "iter_start_ts": now_iso(), "section": section}
        sec_iters.append(entry)
    save_iter_state(base, state)
    return entry


def parse_verdict_from_md(md_text):
    """Extract verdict from a verifier's gate-N.md markdown.

    Looks for `## Verdict` heading followed by `verdict: PASS|HALT`."""
    m = re.search(r"^##\s*Verdict\b", md_text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    tail = md_text[m.end():]
    m2 = re.search(r"verdict\s*:\s*(PASS|HALT)", tail, re.IGNORECASE)
    if not m2:
        return None
    return m2.group(1).upper()


def schema_validate(gate_obj, phase):
    schema_path = SCHEMA_DIR / f"gate-{phase}.schema.json"
    if not schema_path.exists():
        raise GateAttestationError("schema-missing", str(schema_path))
    schema = json.loads(schema_path.read_text())
    try:
        jsonschema.validate(gate_obj, schema)
    except jsonschema.ValidationError as e:
        raise GateAttestationError("schema-validation-failed", str(e.message))


def attest_simple(base, phase):
    """Attest single-source gates: 4.75, 6, 7.5, 8.5."""
    state = load_iter_state(base)
    iters = state.get(phase, [])
    if not iters:
        raise GateAttestationError(
            "no-iteration-started",
            f"call: gate_attest.py start-iteration --base {base} --phase {phase}",
        )
    current = iters[-1]
    iter_n = current["iteration"]
    iter_start = current["iter_start_ts"]

    md_rel = SOURCE_MD[phase]
    md_path = pathlib.Path(base) / md_rel
    if not md_path.exists():
        raise GateAttestationError(
            "missing-agent-source",
            f"{md_rel} must exist (dispatched verifier writes it)",
        )

    md_mtime_dt = datetime.datetime.fromtimestamp(
        md_path.stat().st_mtime, tz=datetime.timezone.utc
    )
    md_mtime = md_mtime_dt.isoformat()
    if md_mtime <= iter_start:
        raise GateAttestationError(
            "stale-agent-source",
            f"{md_rel} mtime {md_mtime} predates iter_start {iter_start}; "
            f"re-dispatch the verifier",
        )

    md_bytes = md_path.read_bytes()
    md_text = md_bytes.decode("utf-8", errors="replace")
    verdict = parse_verdict_from_md(md_text)
    if verdict is None:
        raise GateAttestationError(
            "verdict-not-parsable",
            f"no '## Verdict' block with 'verdict: PASS|HALT' in {md_rel}",
        )

    md_sha = sha256_bytes(md_bytes)

    # If the agent also wrote a draft gate-N.json, use it as scaffold but
    # OVERRIDE verdict from the authoritative MD parse — orchestrator may
    # not disagree with the agent's verdict.
    json_path = pathlib.Path(base) / f"gates/gate-{phase}.json"
    if json_path.exists():
        try:
            gate_obj = json.loads(json_path.read_text())
        except json.JSONDecodeError:
            gate_obj = {}
    else:
        gate_obj = {}

    gate_obj.setdefault("phase", phase)
    gate_obj["verdict"] = verdict
    gate_obj.setdefault("timestamp", now_iso())
    if verdict == "HALT":
        if "halt_reasons" not in gate_obj or not gate_obj["halt_reasons"]:
            gate_obj["halt_reasons"] = ["agent-verdict-halt"]
    else:
        gate_obj["halt_reasons"] = []

    gate_obj["attestation_chain"] = {
        "iter_start_ts": iter_start,
        "attest_ts": now_iso(),
        "iteration": iter_n,
        "agent_source_path": md_rel,
        "agent_source_sha256": md_sha,
        "agent_source_mtime": md_mtime,
    }

    schema_validate(gate_obj, phase)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(gate_obj, indent=2))
    return verdict, iter_n


def _extract_judge_score(judge_json):
    """Best-effort extraction of integer score from a judge JSON of any shape."""
    for k in ("total", "total_score"):
        v = judge_json.get(k)
        if isinstance(v, (int, float)):
            return int(v)
    for k in ("scores", "dimension_scores", "dimensions"):
        blob = judge_json.get(k)
        if not isinstance(blob, dict):
            continue
        s = 0
        found = False
        for v in blob.values():
            if isinstance(v, (int, float)):
                s += v
                found = True
            elif isinstance(v, dict):
                inner = v.get("score")
                if isinstance(inner, (int, float)):
                    s += inner
                    found = True
        if found:
            return int(s)
    return None


def _phase_state_iters(phase_state):
    """Return list of phase-wide iterations regardless of v1/v2 shape."""
    if isinstance(phase_state, list):
        return phase_state
    if isinstance(phase_state, dict):
        return phase_state.get("phase_iterations", [])
    return []


def _phase_state_section_iters(phase_state, section):
    """Return list of section-scoped iterations (empty if none recorded)."""
    if isinstance(phase_state, dict):
        return phase_state.get("sections", {}).get(section, [])
    return []


def attest_judge_gate(base):
    """Phase 3.5: compose from all per-section judge JSONs.

    BUG-001 (2026-05-25): freshness check now uses per-section iter_start_ts
    when present in _iter-state.json, falling back to phase-wide. Per-section
    iter_start_ts is recorded by `start-iteration --phase 3.5 --section X`.
    BUG-001 also: latest-iteration-per-section reads JSON `iteration` field
    when present, falls back to filename-suffix parsing (legacy).
    """
    state = load_iter_state(base)
    phase_state = state.get("3.5")
    phase_iters = _phase_state_iters(phase_state)
    if not phase_iters and not (isinstance(phase_state, dict) and phase_state.get("sections")):
        raise GateAttestationError(
            "no-iteration-started",
            f"call: gate_attest.py start-iteration --base {base} --phase 3.5",
        )
    phase_iter_start = phase_iters[-1]["iter_start_ts"] if phase_iters else None
    iter_n = phase_iters[-1]["iteration"] if phase_iters else 1

    judges_dir = pathlib.Path(base) / "judges"
    if not judges_dir.exists():
        raise GateAttestationError("missing-agent-source", "judges/ directory absent")

    # Latest iteration per section — prefer JSON `iteration` field, fall back
    # to filename suffix. BUG-001: filename-only parsing meant a stale
    # `judge-A-iter2.json` (yesterday) could outrank fresh `judge-A.json`
    # (today, iteration=4 in JSON) because the regex saw -iter2 as iter 2 and
    # no suffix as iter 1.
    latest = {}
    pattern = re.compile(r"^judge-([A-Z])(?:-iter(\d+))?\.json$")
    for p in sorted(judges_dir.glob("judge-*.json")):
        m = pattern.match(p.name)
        if not m:
            continue
        section, iter_str = m.group(1), m.group(2)
        # Prefer JSON `iteration` field
        try:
            j = json.loads(p.read_text())
            iteration = int(j.get("iteration", 0)) or (int(iter_str) if iter_str else 1)
        except (json.JSONDecodeError, ValueError):
            iteration = int(iter_str) if iter_str else 1
        cur = latest.get(section)
        if cur is None or iteration > cur[0]:
            latest[section] = (iteration, p)

    if not latest:
        raise GateAttestationError(
            "missing-agent-source", "no judge-<section>.json files found"
        )

    judge_verdicts = []
    judge_sources = []
    for section, (iteration, p) in sorted(latest.items()):
        mtime = datetime.datetime.fromtimestamp(
            p.stat().st_mtime, tz=datetime.timezone.utc
        ).isoformat()
        # BUG-001: choose per-section iter_start_ts when present, else phase-wide
        sec_iters = _phase_state_section_iters(phase_state, section)
        if sec_iters:
            iter_start = sec_iters[-1]["iter_start_ts"]
        elif phase_iter_start is not None:
            iter_start = phase_iter_start
        else:
            raise GateAttestationError(
                "no-iteration-started",
                f"section {section}: no per-section or phase-wide iter_start_ts",
            )
        if mtime <= iter_start:
            raise GateAttestationError(
                "stale-agent-source",
                f"{p.name} mtime {mtime} predates iter_start {iter_start} (section {section})",
            )
        body = p.read_bytes()
        j = json.loads(body.decode("utf-8"))
        verdict = j.get("verdict")
        if verdict not in ("PASS", "HALT"):
            raise GateAttestationError(
                "verdict-not-parsable", f"{p.name} verdict missing or invalid"
            )
        score = _extract_judge_score(j)
        if score is None:
            raise GateAttestationError(
                "score-not-parsable", f"{p.name} score field missing or non-numeric"
            )
        brief_seed = f"aplus-research::section-{section}::iter-{iteration}::{iter_start}"
        brief_hash = sha256_bytes(brief_seed.encode())
        judge_verdicts.append(
            {
                "section": section,
                "retrieve_agent_id": f"retrieve-{section}-iter{iteration}",
                "judge_agent_id": f"judge-{section}-iter{iteration}",
                "brief_hash": brief_hash,
                "score": score,
                "verdict": verdict,
                "iteration": iteration,
            }
        )
        judge_sources.append(
            {
                "section": section,
                "iteration": iteration,
                "sha256": sha256_bytes(body),
                "path": str(p.relative_to(pathlib.Path(base))),
                "mtime": mtime,
            }
        )

    overall_pass = all(jv["verdict"] == "PASS" for jv in judge_verdicts)
    overall_verdict = "PASS" if overall_pass else "HALT"
    halt_reasons = [] if overall_pass else ["judge-below-threshold"]

    threshold = 99  # deep mode default; standard=92, ultradeep=99
    # BUG-001: surface per-section vs phase-wide iter_start_ts in chain so
    # `verify-chain` audit can re-resolve provenance unambiguously.
    chain_iter_start = phase_iter_start if phase_iter_start is not None else "per-section"
    gate_obj = {
        "phase": "3.5",
        "verdict": overall_verdict,
        "timestamp": now_iso(),
        "mode_threshold": threshold,
        "iterations": max(jv["iteration"] for jv in judge_verdicts),
        "judge_verdicts": judge_verdicts,
        "halt_reasons": halt_reasons,
        "attestation_chain": {
            # BUG-001: iter_start_ts is the phase-wide stamp when present;
            # individual sections may have used their own per-section iter_start_ts
            # which is recorded inside each judge_sources[i].iter_start_ts.
            "iter_start_ts": phase_iter_start or judge_sources[0]["mtime"],
            "attest_ts": now_iso(),
            "iteration": iter_n,
            "judge_sources": judge_sources,
        },
    }
    schema_validate(gate_obj, "3.5")
    out = pathlib.Path(base) / "gates/gate-3.5.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(gate_obj, indent=2))
    return overall_verdict, iter_n


def verify_chain(base, up_to_phase=None):
    """Verify attestation chains across all attested gates that have been written.

    Returns list of (phase, error_message) failures. Empty list = chain intact.
    """
    failures = []
    base_p = pathlib.Path(base)
    for phase in ATTESTED_GATES:
        if up_to_phase is not None and float(phase) > float(up_to_phase):
            break
        json_path = base_p / f"gates/gate-{phase}.json"
        if not json_path.exists():
            continue
        try:
            gate = json.loads(json_path.read_text())
        except json.JSONDecodeError as e:
            failures.append((phase, f"malformed JSON: {e}"))
            continue
        chain = gate.get("attestation_chain")
        if chain is None:
            failures.append((phase, "no-attestation-chain (likely orchestrator-fabricated)"))
            continue
        if phase == "3.5":
            sources = chain.get("judge_sources") or []
            if not sources:
                failures.append((phase, "judge_sources empty"))
                continue
            for src in sources:
                p = base_p / src["path"]
                if not p.exists():
                    failures.append((phase, f"missing judge source {src['path']}"))
                    continue
                actual = sha256_bytes(p.read_bytes())
                if actual != src["sha256"]:
                    failures.append(
                        (phase, f"sha mismatch on {src['path']} (file edited post-attest)")
                    )
        else:
            src = chain.get("agent_source_path")
            expected = chain.get("agent_source_sha256")
            if src is None or expected is None:
                failures.append((phase, "incomplete attestation_chain"))
                continue
            p = base_p / src
            if not p.exists():
                failures.append((phase, f"missing agent source {src}"))
                continue
            actual = sha256_bytes(p.read_bytes())
            if actual != expected:
                failures.append((phase, f"sha mismatch on {src} (file edited post-attest)"))
    return failures


def main():
    parser = argparse.ArgumentParser(
        description="aplus-research gate attestation (mechanical resistance per PF-S3-01)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser(
        "start-iteration", help="Record iter_start_ts for a phase (call before dispatching verifier)"
    )
    p1.add_argument("--base", required=True)
    p1.add_argument("--phase", required=True, choices=ATTESTED_GATES)
    # BUG-001: --section scopes the iter_start_ts to one section within phase 3.5.
    # When unset, the iter_start_ts is phase-wide (legacy behavior).
    p1.add_argument(
        "--section",
        default=None,
        help="(phase 3.5 only) record per-section iter_start_ts for partial-resume",
    )

    p2 = sub.add_parser(
        "attest", help="Compose gates/gate-N.json from agent-written source"
    )
    p2.add_argument("--base", required=True)
    p2.add_argument("--phase", required=True, choices=ATTESTED_GATES)

    p3 = sub.add_parser("verify-chain", help="Audit attestation chains of written gates")
    p3.add_argument("--base", required=True)
    p3.add_argument("--up-to", default=None, choices=ATTESTED_GATES + (None,))

    args = parser.parse_args()
    try:
        if args.cmd == "start-iteration":
            entry = start_iteration(args.base, args.phase, section=args.section)
            scope = f" section {args.section}" if args.section else ""
            print(
                f"phase {args.phase}{scope} iteration {entry['iteration']} started at {entry['iter_start_ts']}"
            )
        elif args.cmd == "attest":
            if args.phase == "3.5":
                verdict, iter_n = attest_judge_gate(args.base)
            else:
                verdict, iter_n = attest_simple(args.base, args.phase)
            print(f"phase {args.phase} attested iter {iter_n}: verdict={verdict}")
        elif args.cmd == "verify-chain":
            failures = verify_chain(args.base, args.up_to)
            if failures:
                for phase, msg in failures:
                    print(f"FAIL gate-{phase}: {msg}", file=sys.stderr)
                sys.exit(1)
            print("attestation chain intact")
    except GateAttestationError as e:
        print(f"HALT {e.reason}: {e.detail}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
