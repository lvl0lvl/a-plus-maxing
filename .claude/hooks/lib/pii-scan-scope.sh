#!/bin/bash
# pii-scan-scope.sh — SINGLE SOURCE for the PII-scan path scope shared by the two
# PII hooks: block-pii-commit.sh (commit-time gate) and pre-push-pii-scan.sh
# (push backstop). Sourced, not executed; each hook computes its own SCRIPT_DIR
# and runs `source "$SCRIPT_DIR/lib/pii-scan-scope.sh"` (block-pii-commit) /
# `source "$SCRIPT_DIR/lib/pii-scan-scope.sh"` (pre-push).
#
# Why a lib (PR#84 QUAL-1/HIST-3, citing the PR#80 mic precedent): the data-bearing
# prefix list and the per-se-deny path prefixes were duplicated across the two
# hooks, coordinated only by a "mirrors block-pii-commit.sh" comment. On this
# distribution boundary a one-hook divergence silently narrows the other's scan
# scope — the exact fail-open class PR#80 single-sourced the commit matcher to
# prevent. The path scope lives ONCE, here.
#
# CONSUMER OBLIGATION: a failed `source` is non-fatal under `set -uo pipefail`, so
# a consumer MUST assert this lib loaded before relying on it
# (`[[ -n "${STORE_PREFIX:-}" ]] || <fail per the consumer's posture>`); the
# fail-CLOSED consumers deny/block on a missing lib.

# Filled-scaffold-value prefix: the .gitignore exclusion, block-pii-commit's
# condition-1 matcher, and the test fixtures all key off this one literal (PR#81).
SCAFFOLD_PREFIX="vault/scaffold/filled/"
# Store prefix: gitignored operator-data root (ADR-0002/ADR-0005); condition-2 key.
STORE_PREFIX="vault/store/"
# Per-se-deny path prefixes: a staged/pushed file under any of these is operator
# data by location, denied regardless of token hits (block-pii-commit conditions
# 1+2; mirrored as the pre-push path-denial, PR#84 API-1).
PER_SE_DENY_PREFIXES=("$SCAFFOLD_PREFIX" "$STORE_PREFIX")
# Data-bearing dropzones (gitignored health-data paths) the identity scan covers.
# vault/artifacts/generated/ holds the maintained re-inserted-name plan render, so a
# re-inserted REAL name must be name-scanned there (ADR-0021 N2 / ADR-0025 N3); it is
# NOT a per-se-deny path — the same dropzone legitimately holds the clean initials-only
# render, which must stay allowed.
DATA_BEARING_PREFIXES=("$SCAFFOLD_PREFIX" "$STORE_PREFIX" "vault/dna/raw/" "vault/labs/raw/" "vault/artifacts/generated/")
