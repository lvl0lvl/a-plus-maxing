#!/usr/bin/env python3
"""Self-test for the shared gate_attest engine (frameworks/rigor/toolkit/lib).

Exercises the domain-NEUTRAL attestation mechanics against GENERIC fixture
schemas (tests/fixtures/gate-attest/schemas/) — proving the engine works for any
project, not just a-plus-maxing. Covers the two bugs the engine was hardened for:
  AR-6  per-section freshness checked against each judge's CLAIMED iteration
        (partial remediation must not flag earlier-passed sections stale).
  AR-7  structured gate fields accepted as a fenced ```json block in gate-N.md
        (single self-contained source) — and still HALT when absent.
Plus the core anti-self-attestation guards (no-iteration, stale-source,
verify-chain tamper detection).

Run:  python3 gate_attest_selftest.py   (exit 0 = all pass)
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / "lib" / "gate_attest.py"
SCHEMAS = HERE / "fixtures" / "gate-attest" / "schemas"
ENV = {**os.environ, "GATE_ATTEST_SCHEMA_DIR": str(SCHEMAS)}

RESULTS = []


def test(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"{status}  {name}" + (f" — {detail}" if detail else ""))
    RESULTS.append(cond)


def run(args, expect_exit=0):
    p = subprocess.run([sys.executable, str(SCRIPT)] + args,
                       capture_output=True, text=True, env=ENV)
    return p.returncode, p.stdout, p.stderr


def make_base():
    base = pathlib.Path(tempfile.mkdtemp(prefix="gate-attest-self-"))
    (base / "gates").mkdir(parents=True, exist_ok=True)
    (base / "judges").mkdir(parents=True, exist_ok=True)
    return base


def write_simple_md(base, verdict="PASS", payload={"checked": 3}):
    body = f"# Gate\n\n## Verdict\n\nverdict: {verdict}\n"
    if payload is not None:
        body += "\n```json\n" + json.dumps({"phase": "4.75", "payload": payload,
                                            "halt_reasons": []}) + "\n```\n"
    (base / "gates/gate-4.75.md").write_text(body)


# ── T1: fresh PASS, structured payload via fenced json block (AR-7 positive) ──
base = make_base()
try:
    run(["start-iteration", "--base", str(base), "--phase", "4.75"])
    time.sleep(0.05)
    write_simple_md(base, "PASS")
    code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"])
    gate = json.loads((base / "gates/gate-4.75.json").read_text()) if code == 0 else {}
    test("T1 fresh PASS + fenced-json payload scaffold (AR-7)",
         code == 0 and gate.get("verdict") == "PASS"
         and gate.get("payload", {}).get("checked") == 3 and "attestation_chain" in gate,
         err.strip().splitlines()[-1] if (err and code) else "")
finally:
    shutil.rmtree(base)

# ── T2: attest without start-iteration → no-iteration-started ──
base = make_base()
try:
    write_simple_md(base, "PASS")
    code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"], expect_exit=2)
    test("T2 no start-iteration → HALT no-iteration-started",
         code == 2 and "no-iteration-started" in err, err.strip().splitlines()[-1] if err else "")
finally:
    shutil.rmtree(base)

# ── T3: source older than iter_start → stale-agent-source ──
base = make_base()
try:
    write_simple_md(base, "PASS")
    time.sleep(0.05)
    run(["start-iteration", "--base", str(base), "--phase", "4.75"])  # starts AFTER the write
    code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"], expect_exit=2)
    test("T3 stale source (written before iter_start) → HALT stale-agent-source",
         code == 2 and "stale-agent-source" in err, err.strip().splitlines()[-1] if err else "")
finally:
    shutil.rmtree(base)

# ── T4: AR-7 negative — no fenced block, required field missing → schema fail ──
base = make_base()
try:
    run(["start-iteration", "--base", str(base), "--phase", "4.75"])
    time.sleep(0.05)
    write_simple_md(base, "PASS", payload=None)  # no ```json block
    code, _, err = run(["attest", "--base", str(base), "--phase", "4.75"], expect_exit=2)
    test("T4 missing structured field (no fenced block) → schema-validation-failed + AR-7 hint",
         code == 2 and "schema-validation-failed" in err and "AR-7" in err,
         err.strip().splitlines()[-1] if err else "")
finally:
    shutil.rmtree(base)

# ── T5: AR-6 — judge gate, gate-global partial remediation, mixed iterations ──
base = make_base()
try:
    run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 1
    time.sleep(0.05)
    for sec in ("A", "B"):
        (base / f"judges/judge-{sec}.json").write_text(
            json.dumps({"section": sec, "verdict": "PASS", "total": 100, "iteration": 1}))
    time.sleep(0.1)
    run(["start-iteration", "--base", str(base), "--phase", "3.5"])  # iter 2 (gate-global)
    time.sleep(0.05)
    (base / "judges/judge-A.json").write_text(  # only A re-judged at iter 2
        json.dumps({"section": "A", "verdict": "PASS", "total": 100, "iteration": 2}))
    code, _, err = run(["attest", "--base", str(base), "--phase", "3.5"])
    gate = json.loads((base / "gates/gate-3.5.json").read_text()) if code == 0 else {}
    test("T5 AR-6 partial remediation: B(iter1) not flagged stale at iter2 → gate PASS",
         code == 0 and gate.get("verdict") == "PASS",
         err.strip().splitlines()[-1] if (err and code) else "")
finally:
    shutil.rmtree(base)

# ── T6: verify-chain detects a post-attest edit of the source ──
base = make_base()
try:
    run(["start-iteration", "--base", str(base), "--phase", "4.75"])
    time.sleep(0.05)
    write_simple_md(base, "PASS")
    run(["attest", "--base", str(base), "--phase", "4.75"])
    code0, _, _ = run(["verify-chain", "--base", str(base)])
    (base / "gates/gate-4.75.md").write_text((base / "gates/gate-4.75.md").read_text() + "\ntampered\n")
    code1, _, err = run(["verify-chain", "--base", str(base)], expect_exit=1)
    test("T6 verify-chain: intact before edit, sha-mismatch after post-attest edit",
         code0 == 0 and code1 == 1 and "sha mismatch" in err,
         err.strip().splitlines()[-1] if err else "")
finally:
    shutil.rmtree(base)

n = len(RESULTS)
ok = sum(RESULTS)
print(f"\n{ok}/{n} passed")
sys.exit(0 if ok == n else 1)
