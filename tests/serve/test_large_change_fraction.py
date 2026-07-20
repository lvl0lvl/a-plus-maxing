"""Large-change HOLD threshold re-based as a STRICT MAJORITY of the active RENDERABLE set (ADR-0046-T2).

The Wave-5 re-base: the `plan_loop.regenerate` large-change hold no longer fires on the retired fixed
count `LARGE_CHANGE_THRESHOLD_DOMAINS = 3` — it fires when the changed-domain count is a STRICT MAJORITY
of `|renderable|` (`active & RENDERABLE_DOMAINS`, the `regenerate` local). The DENOMINATOR is
`|renderable|` (≤ 4, commensurable with the numerator that caps at 4), NOT `|active|`: a `len(active)`
bar is structurally unreachable for `|active| ≥ 8` and fails OPEN (F1/F2 binding ruling).

Everything is SYNTHETIC — scratch `tmp_path` stores, 0 live-API spend, 0 real operator PII. The Group-A
hold tests drive the REAL `plan_loop.regenerate` production path over the fixture dispatch / de-id seams,
so a revert of the denominator (`len(renderable)` -> `len(active)`) or the fraction (-> the retired `3`)
drives them RED (PF-S130-01 non-tautology, proven per-mutation in the recipe's Step 2.5).
"""

import re
import subprocess
from pathlib import Path

import pytest

from scripts.serve import plan_loop
from scripts.store import plan_confirm, plan_schema

from tests.serve.test_orchestrator_synthesize import _seed_surface_store
from tests.serve.test_plan_loop import (
    _FixedDeidClient,
    _LoopDispatch,
    _clean_authors,
    _deid_summary,
    _seed_prior_standing,
)

# The re-gen date; a prior standing plan is seeded at `_T4_PRIOR_DATE` (2026-06-01, well before), so
# every seeded-prior domain replaces a differing standing plan (a counted change).
_PLAN_DATE = "2026-07-13"
# Six rich (non-renderable) card domains: they raise `|active|` WITHOUT raising `|renderable|` (they
# carry no renderable-validator swap), the exact F1/F2 distinguisher. [VERIFIED] |active|=10 with the
# four renderable, |renderable|=4.
_RICH_SIX = ("sleep", "recovery", "endocrine", "cardiovascular", "longevity", "gi")

# The durable fork-point (Wave-4 merged main tip, a PERMANENT main ancestor) — the AC-5 numstat base and
# the Rollback target. NOT `git merge-base origin/main HEAD` (collapses to HEAD post-squash-merge, PF-
# S133-03) and NOT an intermediate feature-branch SHA (orphans on squash).
FORK_POINT = "1cd134c25a09d623af5ecc9c0eed08a49040c7de"
_FROZEN_SIX = (
    "scripts/store/store.py",
    "scripts/store/keying.py",
    "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    "scripts/plan/router.py",
)


def _drive(root, dispatch):
    """Drive the REAL `regenerate` production path over the synthetic dispatch / de-id seams."""
    return plan_loop.regenerate(
        root, dispatch=dispatch, deid_client=_FixedDeidClient(_deid_summary()),
        plan_date=_PLAN_DATE, trigger="test")


def _assert_held(result, root, swapped):
    """Assert the run HELD as a materially-large swap: flag + advisory + every promoted domain withheld.

    Mirrors `test_plan_loop_hold.py`'s hold assertions. The ADR-0040 hold marks EVERY promoted domain
    `pending` before `regenerate` returns and its plan does NOT surface. The SWAPPED domains (those with
    a prior standing plan) resolve `NO_PLAN_TODAY` specifically — the prior is withheld, not walked back
    to; a domain that ESTABLISHES (no prior) resolves `NO_PLAN` (filter_confirmed drops the sole held
    reading), so it is asserted only as pending + withheld. `swapped` is the prior-seeded subset. Returns
    the promoted-domain list.
    """
    assert result["large_change"] is True, (
        f"the materially-large swap did not hold (large_change): {result.get('large_change')}")
    assert result["large_change_advisory"], "the hold produced no confirm-prompt advisory payload"
    promoted = [d for d, r in result["results"].items() if r.get("recorded")]
    assert promoted, "nothing was promoted — the fixture never exercised the hold path"
    for domain in promoted:
        assert plan_confirm.decision_for(domain, _PLAN_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: the ADR-0040 hold did not mark the promoted domain pending")
        assert plan_schema.read_plan(domain, _PLAN_DATE, root)["plan"] is None, (
            f"{domain}: the held swap surfaced a standing plan instead of being withheld")
    for domain in swapped:
        assert plan_schema.read_plan(domain, _PLAN_DATE, root)["state"] == plan_schema.NO_PLAN_TODAY, (
            f"{domain}: the held swap stood instead of resolving NO_PLAN_TODAY")
    return promoted


def _predicate_comment_block(src):
    """The lowercased contiguous `#` comment block immediately above `def _is_renderable_majority`."""
    lines = src.splitlines()
    anchors = [i for i, line in enumerate(lines) if line.startswith("def _is_renderable_majority")]
    if not anchors:
        return ""
    block = []
    j = anchors[0] - 1
    while j >= 0 and lines[j].lstrip().startswith("#"):
        block.append(lines[j])
        j -= 1
    return "\n".join(reversed(block)).lower()


def _repo_root():
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
    ).stdout.strip()


# =========================================================================== #
# GROUP A — production-path hold tests (drive the REAL plan_loop.regenerate)
# =========================================================================== #


def test_majority_swap_holds_4_active_3_of_4(tmp_path):
    # AC-1 parity: a 3-of-4-renderable swap (|active|=|renderable|=4, magnitude 3) is a STRICT majority
    # (3 > 4/2) and HOLDS. The retired constant `3 >= 3` also held — parity, NOT a distinguisher.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=list(plan_schema.RENDERABLE_DOMAINS))
    _seed_prior_standing(root, ("workout", "nutrition", "supplements"))  # magnitude 3
    result = _drive(root, _LoopDispatch(_clean_authors()))
    _assert_held(result, root, swapped=("workout", "nutrition", "supplements"))


def test_renderable_swap_holds_even_with_rich_active(tmp_path):
    # AC-1 load-bearing (F1/F2 correct-direction distinguisher): 3 renderable swapped WITH 6 rich
    # domains ALSO active (|active|=10, |renderable|=4, magnitude 3). A strict majority of |renderable|
    # (bar 4//2+1=3) -> HOLDS. A len(active) denominator (bar 10//2+1=6 > 3) would NOT hold -> the
    # Step-2.5 len(active) mutation REDs this test. It catches the fail-OPEN denominator F1/F2 flagged.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=[*plan_schema.RENDERABLE_DOMAINS, *_RICH_SIX])
    _seed_prior_standing(root, ("workout", "nutrition", "supplements"))  # magnitude 3
    result = _drive(root, _LoopDispatch(_clean_authors()))
    promoted = _assert_held(result, root, swapped=("workout", "nutrition", "supplements"))
    assert set(promoted) == set(plan_schema.RENDERABLE_DOMAINS), (
        f"the promoted set is not the four renderable (only renderable carry the thin swap): {promoted}")


def test_full_renderable_swap_holds_4_of_4(tmp_path):
    # qa-0052-01 (the apex): ALL four renderable swapped over a differing prior (magnitude 4,
    # |renderable|=4) — the single largest materially-large re-gen the hold exists to catch. Post-T2
    # active_plan_domains pins |renderable| at 4, so 3 (test_renderable_swap_holds_even_with_rich_active)
    # and 4 (here) are the ONLY reachable front-door hold magnitudes; this pins the 4-of-4 apex that
    # shares the True branch with 3-of-4 but had no integration or unit pin before.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=[*plan_schema.RENDERABLE_DOMAINS, *_RICH_SIX])
    _seed_prior_standing(root, tuple(plan_schema.RENDERABLE_DOMAINS))  # magnitude 4 (all four replaced)
    result = _drive(root, _LoopDispatch(_clean_authors()))
    promoted = _assert_held(result, root, swapped=tuple(plan_schema.RENDERABLE_DOMAINS))
    assert set(promoted) == set(plan_schema.RENDERABLE_DOMAINS), (
        f"the promoted set is not the four renderable: {promoted}")


def test_narrow_signal_change_is_minority_of_floored_renderable(tmp_path):
    # ADR-0052-T2 INTERACTION with the ADR-0046-T2 large-change hold (flagged for review):
    # Pre-T2 a narrow-signal surface (workout+nutrition) had |renderable| = |active & RENDERABLE| = 2
    # (the conditional floor did not add supplements/peptides), so a 2-domain swap was a STRICT majority
    # (2 > 2/2) and HELD for confirmation. Post-T2 the UNCONDITIONAL always-on-ten floor makes ALL four
    # renderable active (|renderable| = 4) — supplements/peptides floor in as ESTABLISHES (no prior
    # standing, so they raise |renderable| WITHOUT adding to _change_magnitude). The SAME 2-domain swap
    # is therefore now a MINORITY (2-of-4, 2 not > 4/2=2) and does NOT hold: it applies without a
    # confirmation prompt. This is consistent with the strict-majority rule (2-of-4 does not hold — the
    # module docstring), but it DILUTES the pre-T2 "narrow surface scales the denominator down" property
    # (ADR-0046-T2) that this test used to exercise: the narrowed-renderable surface is now unreachable
    # via the front door. The reachable majority-holds path is test_renderable_swap_holds_even_with_rich_active
    # (3-of-4); the fraction-vs-constant boundary is test_renderable_majority_predicate_points[(2,4,False)].
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    _seed_prior_standing(root, ("workout", "nutrition"))  # magnitude 2, but |renderable| now floors to 4
    result = _drive(root, _LoopDispatch(_clean_authors()))
    assert result["large_change"] is False, (
        "a 2-of-4 minority swap must NOT trip the large-change hold post-T2 (floored |renderable|=4)")
    for domain in ("workout", "nutrition"):
        assert plan_schema.read_plan(domain, _PLAN_DATE, root)["plan"] is not None, (
            f"{domain}: a non-held minority swap must SURFACE its new plan (not be withheld)")


# =========================================================================== #
# GROUP B — the strict-majority predicate boundary curve (renderable sizes 1..4)
# =========================================================================== #


@pytest.mark.parametrize("changed,renderable,expected", [
    (1, 1, True),   # 1 > 1/2
    (1, 2, False),  # 1 == 2/2, not strict
    (2, 2, True),   # 2 > 2/2
    (2, 3, True),   # 2 > 3/2
    (1, 3, False),  # 1 < 3/2
    (3, 4, True),   # 3 > 4/2 (reproduces the retired 3-of-4)
    (2, 4, False),  # 2 == 4/2, not strict (2-of-4 stays below)
    (4, 4, True),   # 4 > 4/2 (the apex — post-T2 |renderable| is pinned at 4, so 3 and 4 are the only
])                  # reachable magnitudes; this pins the maximal full-renderable swap holds)
def test_renderable_majority_predicate_points(changed, renderable, expected):
    # AC-1/boundary: the STRICT-majority curve over renderable sizes 1..4 (the numerator cap). Strict
    # `> half`, NOT `>= ceil` — 2-of-4 does NOT hold, 3-of-4 does. Never (6, 10): a magnitude-6 swap is
    # not real-path-reachable given the numerator-4 cap (F5).
    assert plan_loop._is_renderable_majority(changed, renderable) is expected


# =========================================================================== #
# GROUP C — grep / spine guards
# =========================================================================== #


def test_no_fixed_3_residue():
    # AC-3 (F4): the hold computes against len(renderable) (the :273 active & RENDERABLE_DOMAINS local),
    # with NO retired constant, NO bare `>= 3` magnitude comparison, and NO fail-open len(active) bar.
    src = Path(plan_loop.__file__).read_text(encoding="utf-8")
    flat = " ".join(src.split())
    assert "LARGE_CHANGE_THRESHOLD_DOMAINS" not in src, "the retired fixed-3 constant is still present"
    assert re.search(r"_is_renderable_majority\(.*?len\(renderable\)\s*\)\s*:", flat), (
        "the hold is not gated by the strict-majority predicate computed over len(renderable)")
    gate = re.search(r"if\s+_is_renderable_majority\((.*?)\)\s*:", flat)
    assert gate, "the hold gate is not an `if _is_renderable_majority(...)` call"
    assert "len(active)" not in gate.group(1), (
        "the F1/F2 fail-open len(active) denominator is present in the hold gate")
    assert not re.search(r"_change_magnitude\([^:]*\)\s*>=\s*3\b", flat), (
        "a bare `_change_magnitude(...) >= 3` residue is present")


def test_rebase_documented_precondition():
    # AC-4: the re-based threshold documents (a) the strict-majority-of-RENDERABLE denominator (NOT
    # |active|) and (b) the hard sequencing precondition before the scaled 15+ roster runs live.
    src = Path(plan_loop.__file__).read_text(encoding="utf-8")
    doc = _predicate_comment_block(src)
    assert doc, "AC-4: no comment documents the re-based threshold predicate"
    assert "strict majority" in doc, "AC-4(a): the strict-majority rationale is undocumented"
    assert "renderable" in doc, "AC-4(a): the renderable denominator is unnamed"
    assert "|active|" in doc, "AC-4(a): the fail-open |active| denominator is not contrasted"
    assert "precondition" in doc, "AC-4(b): the sequencing precondition is undocumented"
    assert "roster" in doc and ("scaled" in doc or "15+" in doc), (
        "AC-4(b): the scaled-roster precondition is unnamed")


def test_no_operator_identity_literal_in_test_tree():
    # AC-5: 0 real operator-identity literal in this test file (mirror test_plan_model.py's guard).
    source = Path(__file__).read_text(encoding="utf-8").lower()
    forbidden = ["".join(parts) for parts in (
        ("wal", "ter"), ("mcgiv", "ney"), ("wmcgiv", "ney"), ("@", "gmail"),
    )]
    for token in forbidden:
        assert token not in source, "a real operator-identity literal leaked into the test tree"


def test_frozen_spine_numstat():
    # Task HARD (PF-S133-03 durable base): the <always-frozen> six are numstat=0 vs the FIXED fork-point
    # AND plan_loop.py IS non-empty vs it (the non-tautological pairing). FORK_POINT is a permanent main
    # ancestor, so this holds on the feature branch, on squashed main, and on a fresh clone.
    repo = _repo_root()
    frozen = subprocess.run(
        ["git", "diff", "--numstat", FORK_POINT, "--", *_FROZEN_SIX],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout.strip()
    assert frozen == "", f"a frozen-spine file changed vs the fork-point: {frozen!r}"
    rebased = subprocess.run(
        ["git", "diff", "--numstat", FORK_POINT, "--", "scripts/serve/plan_loop.py"],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout.strip()
    assert rebased != "", "plan_loop.py did not change vs the fork-point (tautological pairing)"
