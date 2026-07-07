#!/usr/bin/env bash
# toolkit/lib/ui-class.sh — THE single source of the UI file class (bead 48d).
#
# One regex decides which files count as UI across the framework: design-gate.sh's
# scan set, review-pr's design-dimension trigger, and execute-plan's DESIGN GATE
# step all mean THIS class when they say "UI file"; roster-select's design flag
# (planned, bead gw5) will too. Before this lib existed the regex lived as three
# drifting copies (design-gate.sh local var + two command-doc literals) kept in
# sync by prose.
#
# Contract: sourcing this file defines RIGOR_UI_RE (an ERE matched against file
# paths). Consumers MUST fail closed when the source is missing or defines no
# RIGOR_UI_RE: emit a stderr line naming this lib and citing F-008, and exit with
# the consumer's FATAL code (2 under the toolkit's 0/1/2 convention). Never
# proceed with an unset or empty UI class — a gate that cannot know what "UI"
# means must not silently decide nothing is UI.
#
# Changing the class here changes it everywhere in the same pull — that is the
# point. Command docs QUOTE the value for readability but cite this file as owner;
# on divergence, this file wins.

RIGOR_UI_RE='\.(html?|css|s[ac]ss|less|jsx?|tsx?|vue|svelte|astro)$'
