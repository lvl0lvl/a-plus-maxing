#!/usr/bin/env bash
# tests/test-pen-integrity.sh — F-007 negative test for scripts/pen-integrity.sh (the §6.2 gate).
#
# F-007 obligation: a gate that cannot prove it goes RED on bad input enforces nothing. The
# §6.2 export-integrity gate has TWO checks (spec §6.2); this suite proves each one's verdict
# and every FATAL/SKIP boundary:
#   GOOD              intact exports + matching content-sha256 + matching pen-sha256 -> PASS (0).
#   BAD  (integrity)  hand-edit an export without re-stamping export.digest        -> FAIL (1).
#   BOUNDARY (forge)  edit an export AND re-stamp content-sha256                    -> PASS (0),
#                     the DOCUMENTED honest limit: CHECK 1 is integrity, not authenticity
#                     (BH-F4). The defense against a recompute-forger is CHECK 2 + §6.5, never
#                     CHECK 1 — so this case MUST pass, and the test pins that boundary.
#   SIGNAL (pen-chg)  a .pen whose bytes differ from the recorded pen-sha256 -> PEN-CHANGED
#                     signal: exit 0 (does NOT fail, §6.2) BUT a distinct RESULT + the
#                     wave-close-block wording — not a plain pass, not a FAIL.
#   FATAL             missing .pen at the recorded penPath (repo-residency §5, fail-closed);
#                     a SYMLINK pin or an unreadable/unhashable .pen; an a-plus-maxing penPath
#                     [NEW-5]; a config/envelope pin mismatch; an absent / empty / unparseable
#                     envelope (unknown format:, missing content-sha256 / pen-sha256 / pen-path
#                     / stamped).
#   assert_red_when_guard_removed on the load-bearing EXIT-CODE checks (CHECK 1, missing-.pen).
#                     The a-plus guard is mutation-proven by its OWN message anchor instead: an
#                     exit-code pairing cannot isolate it (an a-plus penPath also exits 2 via the
#                     pin-mismatch FATAL, and creating a real a-plus file is forbidden), so the
#                     guard-fires proof is assert_output_contains on a phrase only the a-plus
#                     fatal() emits ("never verify against that tree").
#
# NOT hermetic BY DESIGN: CHECK 2 is proven against the REAL committed .pen at
# designs/fixtures/safety-auth-annotated.pen (resolved via --base = repo root). Hashing the
# .pen as opaque ciphertext bytes is exactly what CHECK 2 does — the whole point of the
# trigger. Bad/signal cases copy the auth export set to a temp dir and mutate the COPY; the
# .pen is always resolved (unchanged) from the repo. The a-plus case only ever puts an
# a-plus-maxing STRING in penPath — the gate FATALs on the lexical check with no FS access, so
# no a-plus path is ever created, resolved, or read. The symlink / unreadable cases point the
# pin at a throwaway decoy under a temp base (never the real .pen, never an a-plus path).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

GATE="${TEST_DIR}/../scripts/pen-integrity.sh"
DIGEST="${TEST_DIR}/../scripts/pen-digest.sh"
REPO="$(cd "${TEST_DIR}/../../../.." && pwd)"          # skills_library repo root
AUTH="${REPO}/designs/fixtures/auth-interaction-model" # real journey, .pen committed in-repo
# Portability (update-rigor): this test reads a design fixture OUTSIDE toolkit/ that does not
# travel with a toolkit copy. In a consuming project without designs/fixtures/ (or where the
# framework-repo REPO resolution overshoots), LOUD-SKIP (exit 0) so the pulled suite stays
# green — the framework repo, where the fixture is present, still runs the full test.
[ -d "$AUTH" ] || { echo "[test-pen-integrity] SKIP (loud): design fixture absent ($AUTH) — not a design-pipeline checkout"; exit 0; }
INCIDENT="${TEST_DIR}/fixtures/pen-lint/good"          # synthetic; penPath -> a .pen absent here

WORK="$(mktemp -d "${TMPDIR:-/tmp}/pen-integrity-fix.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

# --- mutation helpers ---------------------------------------------------------
newcase() { local d="$WORK/$1"; rm -rf "$d"; cp -R "$AUTH" "$d"; echo "$d"; }

edit_export() { # $1=dir — one-byte-class content edit to an export (breaks content-sha256)
  python3 -c "p='$1/index.md'; s=open(p).read(); open(p,'w').write(s.replace('Expected','Xxpected',1))"
}

set_env_field() { # $1=dir $2=key $3=value  (rewrites the envelope line; one trailing newline)
  python3 - "$1/export.digest" "$2" "$3" <<'PY'
import sys
f, k, v = sys.argv[1], sys.argv[2], sys.argv[3]
out = []
for ln in open(f).read().splitlines():
    out.append("%s: %s" % (k, v) if ln.startswith(k + ":") else ln)
open(f, "w").write("\n".join(out) + "\n")
PY
}

set_penpath() { # $1=dir $2=penPath value in config.json
  python3 -c "import json,sys; p='$1/config.json'; c=json.load(open(p)); c['penPath']='$2'; json.dump(c,open(p,'w'),sort_keys=True,indent=2); open(p,'a').write(chr(10))"
}

restamp_content() { # $1=dir — recompute the content digest and write it as content-sha256
  set_env_field "$1" content-sha256 "$(bash "$DIGEST" "$1")"
}

point_pen() { # $1=dir $2=penpath — repoint the pin (config + envelope) and re-stamp so CHECK 1
  # stays clean and pin-consistency holds, reaching CHECK 2 with the .pen at <base>/<penpath>.
  set_penpath "$1" "$2"
  set_env_field "$1" pen-path "$2"
  restamp_content "$1"
}

# assert_output_contains <ere> <cmd...> — combined stdout/stderr must match <ere>.
assert_output_contains() {
  pattern="$1"; shift
  TESTS_RUN=$((TESTS_RUN + 1))
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qE "$pattern"; then
    echo "[PASS] output matches /$pattern/"
  else
    echo "[FAIL] output lacked /$pattern/: $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# =============================================================================
# GOOD: intact auth exports + matching content-sha256 + matching pen-sha256 -> PASS (0).
# =============================================================================
expect_exit 0 bash "$GATE" "$AUTH" --base "$REPO"

# =============================================================================
# CHECK 1 — integrity: hand-edit an export without re-stamping -> FAIL (1).
# =============================================================================
d="$(newcase c1-handedit)"; edit_export "$d"
expect_exit 1 bash "$GATE" "$d" --base "$REPO"
# Anchor on FAIL-ONLY text (T11): "CHECK 1 export integrity" also appears on the ok: line.
assert_output_contains "hand-edited without re-stamping" bash "$GATE" "$d" --base "$REPO"

# BOUNDARY (forge): edit an export AND re-stamp content-sha256 -> CHECK 1 passes -> PASS (0).
# This is the DOCUMENTED honest limit (BH-F4): integrity, not authenticity. Must pass.
d="$(newcase c1-forge-restamp)"; edit_export "$d"; restamp_content "$d"
expect_exit 0 bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# CHECK 2 — pen-change SIGNAL: recorded pen-sha256 differs from the real .pen -> exit 0 +
# distinct PEN-CHANGED output + wave-close-block wording (NOT a plain pass, NOT a FAIL).
# =============================================================================
d="$(newcase c2-pen-changed)"
set_env_field "$d" pen-sha256 deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
expect_exit 0 bash "$GATE" "$d" --base "$REPO"
assert_output_contains "PEN-CHANGED" bash "$GATE" "$d" --base "$REPO"
assert_output_contains "wave-close is BLOCKED" bash "$GATE" "$d" --base "$REPO"
assert_output_contains "RESULT: PASS-WITH-PEN-CHANGED" bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — missing .pen at the recorded penPath (repo-residency §5, fail-closed) -> FATAL (2);
# AUDIT_ALLOW_SKIP=1 downgrades it (a .pen deliberately kept out-of-repo, declared) -> PASS (0).
# The synthetic incident fixture's penPath points at a safety-platform .pen absent from THIS repo.
# =============================================================================
expect_exit 2 bash "$GATE" "$INCIDENT" --base "$REPO"
assert_output_contains "pinned .pen not found" bash "$GATE" "$INCIDENT" --base "$REPO"
expect_exit 0 env AUDIT_ALLOW_SKIP=1 bash "$GATE" "$INCIDENT" --base "$REPO"

# =============================================================================
# FATAL — a-plus-maxing penPath [NEW-5] -> FATAL (2). Lexical only; no a-plus path is created,
# resolved, or read (the gate FATALs before any FS access to penPath).
# The output anchor is a-plus-EXCLUSIVE (T1 fix): "a-plus-maxing" alone would ALSO appear in
# the pin-mismatch FATAL's echo of the penPath, so with the a-plus fatal() removed that anchor
# survives (vacuous — QA proof). "never verify against that tree" is emitted ONLY by the a-plus
# fatal(), so this assertion goes RED when the guard is removed — the real guard-fires proof.
# =============================================================================
d="$(newcase aplus-denylist)"; set_penpath "$d" "some/a-plus-maxing/secret.pen"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"
assert_output_contains "never verify against that tree" bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — pin mismatch: config penPath != recorded envelope pen-path -> FATAL (2).
# (non-a-plus, non-existent path; the gate FATALs on the mismatch before touching the FS.)
# =============================================================================
d="$(newcase pin-mismatch)"; set_penpath "$d" "designs/fixtures/other.pen"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"
assert_output_contains "stale or tampered pin" bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — absent / empty / unparseable envelope (the zero/empty boundary for this gate:
# a §6.2 gate with no recorded digest cannot run) -> FATAL (2).
# =============================================================================
d="$(newcase env-absent)"; rm -f "$d/export.digest"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

d="$(newcase env-empty)"; : > "$d/export.digest"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

d="$(newcase env-no-content)"; set_env_field "$d" content-sha256 ""
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

d="$(newcase env-no-pen)"; set_env_field "$d" pen-sha256 ""
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

# A short (non-64-hex) content-sha256 is unparseable too -> FATAL (2).
d="$(newcase env-shorthash)"; set_env_field "$d" content-sha256 "abc123"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — envelope completeness: unknown format: (T6), missing stamped: (T7), empty pen-path (T9).
# =============================================================================
d="$(newcase env-bad-format)"; set_env_field "$d" format "pen-export-envelope-v9"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

d="$(newcase env-no-stamped)"; set_env_field "$d" stamped ""
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

d="$(newcase env-no-penpath)"; set_env_field "$d" pen-path ""
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — CHECK 1 cannot even compute: pen-digest.sh FATALs on a missing export -> FATAL (2) (T10).
# =============================================================================
d="$(newcase c1-compute-fail)"; rm -f "$d/index.md"
expect_exit 2 bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# PASS — env_field tolerates a column-aligned (multi-space) envelope with real values (T3).
# =============================================================================
d="$(newcase env-aligned)"
python3 - "$d/export.digest" <<'PY'
import sys
f = sys.argv[1]
out = []
for ln in open(f).read().splitlines():
    if ":" in ln:
        k, v = ln.split(":", 1)
        out.append("%s:     %s" % (k, v.strip()))   # 5-space column alignment
    else:
        out.append(ln)
open(f, "w").write("\n".join(out) + "\n")
PY
expect_exit 0 bash "$GATE" "$d" --base "$REPO"

# =============================================================================
# FATAL — CHECK 2 rejects a SYMLINKED pin outright (arch-F2), before hashing its target. point_pen
# keeps CHECK 1 clean so CHECK 2 is reached; the .pen lives under a throwaway base (never the real
# .pen, never an a-plus path).
# =============================================================================
symbase="$WORK/symbase"; mkdir -p "$symbase"; printf 'decoy-bytes' > "$symbase/decoy.pen"; ln -s decoy.pen "$symbase/link.pen"
d="$(newcase c2-symlink)"; point_pen "$d" "link.pen"
expect_exit 2 bash "$GATE" "$d" --base "$symbase"
assert_output_contains "must not be a symlink" bash "$GATE" "$d" --base "$symbase"

# =============================================================================
# FATAL — CHECK 2 fails closed on an unreadable/unhashable .pen (BH1): an empty shasum result
# must NOT read as PEN-CHANGED. A chmod-000 decoy under a throwaway base.
# =============================================================================
unbase="$WORK/unbase"; mkdir -p "$unbase"; printf 'opaque-bytes' > "$unbase/fake.pen"; chmod 000 "$unbase/fake.pen"
d="$(newcase c2-unhashable)"; point_pen "$d" "fake.pen"
expect_exit 2 bash "$GATE" "$d" --base "$unbase"
assert_output_contains "could not hash pinned .pen" bash "$GATE" "$d" --base "$unbase"
chmod 644 "$unbase/fake.pen"

# =============================================================================
# Guard-fires pairings on the load-bearing checks (good GREEN, mutant RED).
# =============================================================================
# CHECK 1 integrity guard.
gc1="$WORK/gp-c1-good"; rm -rf "$gc1"; cp -R "$AUTH" "$gc1"
bc1="$WORK/gp-c1-bad";  rm -rf "$bc1"; cp -R "$AUTH" "$bc1"; edit_export "$bc1"
assert_red_when_guard_removed "bash '$GATE' '$gc1' --base '$REPO'" "bash '$GATE' '$bc1' --base '$REPO'"

# Missing-.pen fail-closed guard (auth GREEN vs incident RED/FATAL).
assert_red_when_guard_removed "bash '$GATE' '$AUTH' --base '$REPO'" "bash '$GATE' '$INCIDENT' --base '$REPO'"

# (No a-plus exit-code guard-pairing [T1 fix]: an a-plus penPath ALSO exits 2 via the
# pin-mismatch FATAL, so a good/bad exit pairing cannot isolate the a-plus guard, and creating
# a real a-plus file is forbidden. The a-plus guard is mutation-proven above by the
# assert_output_contains "never verify against that tree" — a phrase only the a-plus fatal()
# emits, so removing that fatal() turns the assertion RED.)

test_summary
