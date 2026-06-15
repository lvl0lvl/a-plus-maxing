# Handoff — known BAD input

## Current State (VOLATILE)

We reverted to deadbeef0 yesterday and things are stable now.

This is the F-007 false-green case: a bare hash standing in narrative prose with NO
date, NO "sha256"/"hash" label, NO fenced/indented code. A naive BSD-ERE check using
`\b[0-9a-f]{7,}\b` does NOT reliably match this on a POSIX grep (\b is undefined in
ERE), so it silently reported PASS. This version MUST catch it.
