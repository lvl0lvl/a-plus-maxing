#!/usr/bin/env python3
"""Smoke tests for gate_attest.py mechanical resistance.

Run with: python3 tests/test_gate_attest.py
Exits 0 on all-pass, 1 on any failure. Stdout names each test as PASS or FAIL.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = SKILL_DIR / "lib/gate_attest.py"


def run(args, expect_exit=0):
    """Run gate_attest.py and return (returncode, stdout, stderr)."""
    p = subprocess.run(
        ["python3", str(SCRIPT)] + args,
        capture_output=True,
        text=True,
    )
    return p.returncode, p.stdout, p.stderr


def make_base():
    base = pathlib.Path(tempfile.mkdtemp(prefix="gate-attest-test-"))
    (base / "gates").mkdir(parents=True, exist_ok=True)
    (base / "judges").mkdir(parents=True, exist_ok=True)
    return base


def write_verdict_md(path, verdict="PASS", extra=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    body = f"# Agent verdict\n\nFindings: ...\n\n## Verdict\n\nverdict: {verdict}\n\n{extra}"
    path.write_text(body)


def write_judge_json(path, section, score, verdict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "section": section,
        "verdict": verdict,
        "total": score,
        "scores": {"d1": {"score": score // 9}}
    }))


RESULTS = []


def test(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"{status}  {name}" + (f" — {detail}" if detail else ""))
    RESULTS.append((status, name, detail))


def main():
    # T1: attest without start-iteration → HALT no-iteration-started
    base = make_base()
    try:
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"], expect_exit=2)
        test("T1 attest-without-start-iteration HALTs",
             code == 2 and "no-iteration-started" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T2: start-iteration then attest without agent-source → HALT missing-agent-source
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "4.75"])
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"])
        test("T2 attest-without-agent-source HALTs",
             code == 2 and "missing-agent-source" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T3: pre-existing agent-source (older than iter-start) → HALT stale-agent-source
    base = make_base()
    try:
        md = base / "gates/gate-4.75.md"
        write_verdict_md(md, verdict="PASS")
        # Make file old
        old_ts = time.time() - 3600
        import os
        os.utime(md, (old_ts, old_ts))
        time.sleep(0.1)  # ensure iter_start > md mtime
        run(["start-iteration", "--base", str(base), "--phase", "4.75"])
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"])
        test("T3 stale-agent-source HALTs",
             code == 2 and "stale-agent-source" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T4: fresh agent-source with PASS verdict → attest writes gate-4.75.json
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "4.75"])
        time.sleep(0.1)
        md = base / "gates/gate-4.75.md"
        write_verdict_md(md, verdict="PASS")
        # Need to pre-populate a minimum-shape gate-4.75.json (because schema is strict)
        gate_seed = {
            "phase": "4.75",
            "verdict": "PASS",  # will be overridden by attest
            "timestamp": "2026-05-24T00:00:00+00:00",
            "iterations": 1,
            "ic_checks": {
                f"IC-{i}": {"status": "PASS", "findings": []} for i in range(1, 14)
            },
            "population_mismatch": {"verdict": "PASS", "checked_citations": 0, "flagged_citations": []},
            "concentration_audit": {
                "verdict": "PASS", "total_primaries": 0, "largest_cluster_count": 0,
                "share": 0.0, "threshold_triggered": False
            },
            "corpus_scoping": {"verdict": "PASS", "claims_checked": 0, "claims_failed": []},
            "halt_reasons": [],
            "warnings": []
        }
        (base / "gates/gate-4.75.json").write_text(json.dumps(gate_seed))
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"])
        gate = json.loads((base / "gates/gate-4.75.json").read_text())
        chain_ok = (
            "attestation_chain" in gate
            and gate["attestation_chain"]["agent_source_sha256"]
            and gate["attestation_chain"]["iter_start_ts"]
        )
        test("T4 fresh-source-PASS attests successfully",
             code == 0 and gate["verdict"] == "PASS" and chain_ok,
             err.strip())
    finally:
        shutil.rmtree(base)

    # T5: HALT verdict in markdown → attest writes HALT gate (orchestrator cannot override)
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "4.75"])
        time.sleep(0.1)
        write_verdict_md(base / "gates/gate-4.75.md", verdict="HALT")
        gate_seed = {
            "phase": "4.75",
            "verdict": "PASS",  # orchestrator's lie — attest overrides
            "timestamp": "2026-05-24T00:00:00+00:00",
            "iterations": 1,
            "ic_checks": {f"IC-{i}": {"status": "PASS", "findings": []} for i in range(1, 14)},
            "population_mismatch": {"verdict": "HALT", "checked_citations": 0, "flagged_citations": []},
            "concentration_audit": {"verdict": "HALT", "total_primaries": 0, "largest_cluster_count": 0,
                                    "share": 0.0, "threshold_triggered": False},
            "corpus_scoping": {"verdict": "HALT", "claims_checked": 0, "claims_failed": []},
            "halt_reasons": ["fabricated-citation"],
            "warnings": []
        }
        (base / "gates/gate-4.75.json").write_text(json.dumps(gate_seed))
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"])
        gate = json.loads((base / "gates/gate-4.75.json").read_text())
        test("T5 orchestrator-PASS-overridden-by-agent-HALT",
             code == 0 and gate["verdict"] == "HALT",
             f"final verdict={gate['verdict']}")
    finally:
        shutil.rmtree(base)

    # T6: Phase 3.5 — composes from judge JSONs, all PASS
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])
        time.sleep(0.1)
        for sec, score in [("A", 100), ("B", 100), ("C", 100), ("D", 99), ("E", 99), ("F", 100)]:
            write_judge_json(base / f"judges/judge-{sec}.json", sec, score, "PASS")
        code, out, err = run(["attest", "--base", str(base), "--phase", "3.5"])
        gate = json.loads((base / "gates/gate-3.5.json").read_text())
        test("T6 phase-3.5 attest composes from judge JSONs",
             code == 0
             and gate["verdict"] == "PASS"
             and len(gate["judge_verdicts"]) == 6
             and gate["attestation_chain"]["judge_sources"][0]["sha256"],
             f"sections={len(gate['judge_verdicts'])} verdict={gate['verdict']}")
    finally:
        shutil.rmtree(base)

    # T7: Phase 3.5 with one judge HALT → composed gate is HALT
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])
        time.sleep(0.1)
        for sec, score in [("A", 100), ("B", 80), ("C", 100)]:
            verdict = "PASS" if score >= 99 else "HALT"
            write_judge_json(base / f"judges/judge-{sec}.json", sec, score, verdict)
        code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"])
        gate = json.loads((base / "gates/gate-3.5.json").read_text())
        test("T7 phase-3.5 single-judge-HALT yields gate-HALT",
             code == 0 and gate["verdict"] == "HALT" and "judge-below-threshold" in gate["halt_reasons"],
             f"verdict={gate['verdict']}")
    finally:
        shutil.rmtree(base)

    # T8: verify-chain detects post-attest edit to agent source
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "4.75"])
        time.sleep(0.1)
        md = base / "gates/gate-4.75.md"
        write_verdict_md(md, verdict="PASS")
        gate_seed = {
            "phase": "4.75", "verdict": "PASS",
            "timestamp": "2026-05-24T00:00:00+00:00", "iterations": 1,
            "ic_checks": {f"IC-{i}": {"status": "PASS", "findings": []} for i in range(1, 14)},
            "population_mismatch": {"verdict": "PASS", "checked_citations": 0, "flagged_citations": []},
            "concentration_audit": {"verdict": "PASS", "total_primaries": 0, "largest_cluster_count": 0,
                                    "share": 0.0, "threshold_triggered": False},
            "corpus_scoping": {"verdict": "PASS", "claims_checked": 0, "claims_failed": []},
            "halt_reasons": [], "warnings": []
        }
        (base / "gates/gate-4.75.json").write_text(json.dumps(gate_seed))
        run(["attest", "--base", str(base), "--phase", "4.75"])
        # Tamper with the markdown after attestation
        md.write_text(md.read_text() + "\n\nTAMPERED.\n")
        code, _, err = run(["verify-chain", "--base", str(base)])
        test("T8 verify-chain detects post-attest tampering",
             code == 1 and "sha mismatch" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T9: max-iterations-exceeded
    base = make_base()
    try:
        for _ in range(3):
            run(["start-iteration", "--base", str(base), "--phase", "6"])
        code, _, err = run(["start-iteration", "--base", str(base), "--phase", "6"])
        test("T9 max-iterations-exceeded HALTs at iter 4",
             code == 2 and "max-iterations-exceeded" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T10 (BUG-001): phase 3.5 latest-iter uses JSON `iteration` field, not filename.
    # Stale `judge-A-iter2.json` (yesterday) should NOT outrank fresh `judge-A.json` with
    # iteration=4 inside JSON.
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])
        time.sleep(0.1)
        # Write a stale iter2 file (old mtime, iteration:2 in JSON)
        stale = base / "judges/judge-A-iter2.json"
        stale.parent.mkdir(parents=True, exist_ok=True)
        stale.write_text(json.dumps({"section": "A", "verdict": "PASS", "total": 80, "iteration": 2}))
        old = time.time() - 7200
        import os
        os.utime(stale, (old, old))
        # Write a fresh canonical file with iteration:3 in JSON (higher than stale's 2)
        fresh = base / "judges/judge-A.json"
        fresh.write_text(json.dumps({"section": "A", "verdict": "PASS", "total": 100, "iteration": 3}))
        code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"])
        if code == 0:
            gate = json.loads((base / "gates/gate-3.5.json").read_text())
            # The judge_verdicts should record section A with score 100 (from fresh file), iteration 4
            sec_a = [v for v in gate["judge_verdicts"] if v["section"] == "A"][0]
            test("T10 BUG-001 fresh JSON iteration field outranks stale -iter2 filename",
                 sec_a["score"] == 100 and sec_a["iteration"] == 3,
                 f"score={sec_a['score']} iter={sec_a['iteration']}")
        else:
            test("T10 BUG-001 fresh JSON iteration field outranks stale -iter2 filename",
                 False, err.strip().splitlines()[-1] if err else "attest failed")
    finally:
        shutil.rmtree(base)

    # T11 (BUG-001): per-section iter_start_ts via --section flag isolates one section's
    # window from a separate phase-wide start-iteration call.
    base = make_base()
    try:
        # Phase-wide iter 1 at T0
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])
        t0 = time.time()
        time.sleep(0.1)
        # Write 3 judge JSONs against T0 window (fresh)
        for sec in ("A", "B", "C"):
            (base / f"judges/judge-{sec}.json").write_text(
                json.dumps({"section": sec, "verdict": "PASS", "total": 100, "iteration": 1})
            )
        # Later, start a per-section iter for B only — simulating the path-a remediation case
        time.sleep(0.2)
        run(["start-iteration", "--base", str(base), "--phase", "3.5", "--section", "B"])
        time.sleep(0.1)
        # Re-write only judge-B with fresher content; A and C are still at the old phase-wide window
        (base / "judges/judge-B.json").write_text(
            json.dumps({"section": "B", "verdict": "PASS", "total": 100, "iteration": 2})
        )
        # Attest should succeed: A/C use phase-wide iter_start_ts; B uses its per-section ts
        code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"])
        test("T11 BUG-001 per-section --section iter_start_ts isolates from phase-wide",
             code == 0,
             err.strip().splitlines()[-1] if (err and code != 0) else "")
    finally:
        shutil.rmtree(base)

    # T12 (BUG-001): --section is rejected for phases other than 3.5.
    base = make_base()
    try:
        code, _, err = run(
            ["start-iteration", "--base", str(base), "--phase", "4.75", "--section", "A"]
        )
        test("T12 BUG-001 --section rejected outside phase 3.5",
             code == 2 and "section-scope-not-supported" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # T_AR6a (AR-6, 2026-06-18): gate-global start-iteration with PARTIAL
    # remediation. The doc/orchestrator calls `start-iteration --phase 3.5`
    # (no --section) each pass and re-judges only the HALTed sections, so passed
    # sections keep an earlier-iteration judge. Each judge must be checked against
    # the start of the iteration IT claims, not the latest gate clock — else the
    # gate can never PASS. (Pre-fix this HALTed stale-agent-source on B/C.)
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 1
        time.sleep(0.1)
        for sec in ("A", "B", "C"):
            (base / f"judges/judge-{sec}.json").write_text(
                json.dumps({"section": sec, "verdict": "PASS", "total": 100, "iteration": 1}))
        time.sleep(0.2)
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 2 (gate-global)
        time.sleep(0.1)
        (base / "judges/judge-A.json").write_text(  # only A re-judged at iter 2
            json.dumps({"section": "A", "verdict": "PASS", "total": 100, "iteration": 2}))
        code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"])
        gate = json.loads((base / "gates/gate-3.5.json").read_text()) if code == 0 else {}
        test("T_AR6a gate-global partial remediation does not flag passed-earlier sections stale",
             code == 0 and gate.get("verdict") == "PASS",
             err.strip().splitlines()[-1] if (err and code != 0) else "")
    finally:
        shutil.rmtree(base)

    # T_AR6b (AR-6 negative): anti-stale intent preserved. A judge CLAIMING
    # iteration N but written BEFORE iteration N started is still stale → HALT.
    base = make_base()
    try:
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 1
        time.sleep(0.1)
        (base / "judges/judge-A.json").write_text(  # claims iter 2, but written pre-iter-2
            json.dumps({"section": "A", "verdict": "PASS", "total": 100, "iteration": 2}))
        time.sleep(0.2)
        run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 2 starts AFTER the write
        code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"], expect_exit=2)
        test("T_AR6b judge claiming iter-N written before iter-N start is still stale → HALT",
             code == 2 and "stale-agent-source" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    # ─── v2 AC1 calibration (S6 2026-05-25): Phase 4.25 ID-Reconcile gate ────
    # Source path is sections/id-reconcile-source.md (not gates/gate-4.25.md
    # — the agent's deliverable lives with sections, the gate JSON lives in
    # gates/).

    def empty_4_25_classes():
        return {k: {"scanned": 0, "mismatch_count": 0} for k in
                ("citations", "institutions", "compound_identifiers",
                 "regulatory_dates", "trial_registrations")}

    # T13: phase-4.25 PASS round-trip — start-iteration, write source, scaffold
    # JSON, attest, then verify-chain.
    base = make_base()
    try:
        (base / "sections").mkdir(parents=True, exist_ok=True)
        run(["start-iteration", "--base", str(base), "--phase", "4.25"])
        time.sleep(0.1)
        (base / "sections/id-reconcile-source.md").write_text(
            "## Verdict\n\nverdict: PASS\n"
        )
        cls = empty_4_25_classes()
        cls["citations"]["scanned"] = 52
        seed = {
            "phase": "4.25", "iterations": 1, "entity_classes": cls,
            "halt_reasons": [], "timestamp": "2026-05-25T12:00:00+00:00",
        }
        (base / "gates/gate-4.25.json").write_text(json.dumps(seed))
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.25"])
        gate = json.loads((base / "gates/gate-4.25.json").read_text())
        code2, _, _ = run(["verify-chain", "--base", str(base), "--up-to", "4.25"])
        test("T13 phase-4.25 PASS round-trip + verify-chain",
             code == 0 and gate["verdict"] == "PASS" and
             gate["entity_classes"]["citations"]["scanned"] == 52 and code2 == 0,
             f"verdict={gate.get('verdict')}")
    finally:
        shutil.rmtree(base)

    # T14: phase-4.25 HALT round-trip with mismatch detail preserved.
    base = make_base()
    try:
        (base / "sections").mkdir(parents=True, exist_ok=True)
        run(["start-iteration", "--base", str(base), "--phase", "4.25"])
        time.sleep(0.1)
        (base / "sections/id-reconcile-source.md").write_text(
            "## Verdict\n\nverdict: HALT\n"
        )
        cls = empty_4_25_classes()
        cls["citations"] = {
            "scanned": 52, "mismatch_count": 1,
            "mismatches": [{
                "entity_id": "He L 2022 PMID",
                "sections": ["A", "D"],
                "divergent_values": ["33051527", "33051481"],
                "suggested_canonical": "33051481",
                "justification": "PMC9794587 crosswalk",
            }],
        }
        seed = {
            "phase": "4.25", "iterations": 1, "entity_classes": cls,
            "halt_reasons": ["citation-mismatch"],
            "timestamp": "2026-05-25T12:00:00+00:00",
        }
        (base / "gates/gate-4.25.json").write_text(json.dumps(seed))
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.25"])
        gate = json.loads((base / "gates/gate-4.25.json").read_text())
        test("T14 phase-4.25 HALT round-trip — halt_reasons preserved",
             code == 0 and gate["verdict"] == "HALT" and
             "citation-mismatch" in gate["halt_reasons"],
             f"verdict={gate.get('verdict')} halts={gate.get('halt_reasons')}")
    finally:
        shutil.rmtree(base)

    # T15: phase-4.25 orchestrator-PASS overridden by agent-HALT (markdown is
    # authoritative). Scaffold must pre-populate halt_reasons with a valid
    # enum value per documented scaffold pattern.
    base = make_base()
    try:
        (base / "sections").mkdir(parents=True, exist_ok=True)
        run(["start-iteration", "--base", str(base), "--phase", "4.25"])
        time.sleep(0.1)
        (base / "sections/id-reconcile-source.md").write_text(
            "## Verdict\n\nverdict: HALT\n"
        )
        seed = {
            "phase": "4.25", "iterations": 1,
            "entity_classes": empty_4_25_classes(),
            "verdict": "PASS",  # orchestrator's lie
            "halt_reasons": ["citation-mismatch"],
            "timestamp": "2026-05-25T12:00:00+00:00",
        }
        (base / "gates/gate-4.25.json").write_text(json.dumps(seed))
        code, _, _ = run(["attest", "--base", str(base), "--phase", "4.25"])
        gate = json.loads((base / "gates/gate-4.25.json").read_text())
        test("T15 phase-4.25 orchestrator-PASS-overridden-by-agent-HALT",
             code == 0 and gate["verdict"] == "HALT",
             f"final verdict={gate.get('verdict')}")
    finally:
        shutil.rmtree(base)

    # T16: phase-4.25 stale-source HALT — source written BEFORE start-iteration
    # so mtime ≤ iter_start_ts.
    base = make_base()
    try:
        (base / "sections").mkdir(parents=True, exist_ok=True)
        (base / "sections/id-reconcile-source.md").write_text(
            "## Verdict\n\nverdict: PASS\n"
        )
        time.sleep(0.1)
        run(["start-iteration", "--base", str(base), "--phase", "4.25"])
        seed = {
            "phase": "4.25", "iterations": 1,
            "entity_classes": empty_4_25_classes(),
            "halt_reasons": [],
            "timestamp": "2026-05-25T12:00:00+00:00",
        }
        (base / "gates/gate-4.25.json").write_text(json.dumps(seed))
        code, _, err = run(["attest", "--base", str(base), "--phase", "4.25"])
        test("T16 phase-4.25 stale-source HALTs",
             code != 0 and "stale-agent-source" in err,
             err.strip().splitlines()[-1] if err else "")
    finally:
        shutil.rmtree(base)

    failed = [r for r in RESULTS if r[0] == "FAIL"]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} passed")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
