# Interaction Model — review

Inventory of every screen and interactive element in the incident-review
journey. The per-screen "Expected interactive elements" count is the independent
non-vacuity floor the design-time gate (§6.1) consumes; the §6.4 seam gate reads
the manifest, not this count. This is a synthetic Phase-2 fixture — a minimal but
real hydrating app whose only purpose is to exercise the seam-crawl mechanisms
(post-hydration union, portal query, statechart induction, `data-oiid` instances,
`_shell` shellStates). It is not extracted from a `.pen`; the pinned substrate in
config.json is reused only to satisfy the §6.2 hard dependency's freshness check.

## screen/_shell

Expected interactive elements: 2

| name | wireId | purpose |
|------|--------|---------|
| link/home | home | Persistent chrome; renders in every screen-state (shellStates "*") |
| btn/back | back | Chrome shown ONLY on the detail screen-state (shellStates screen/detail) |

## screen/list

Expected interactive elements: 5

| name | wireId | purpose |
|------|--------|---------|
| input/search | search | Ephemeral in-place filter (NA-EPHEMERAL substrate: ephemeral + empty writes) |
| row/incident-row | incident-row | Repeated instance list; each row carries a distinct data-oiid |
| btn/open-filters | open-filters | Opens the filters modal, rendered through a portal to document.body |
| btn/apply-filter | apply-filter | Lives INSIDE the portal modal; visible only after OPEN_FILTERS is induced |
| btn/open-detail | open-detail | Transitions to the detail screen-state |

## screen/detail

Expected interactive elements: 3

| name | wireId | purpose |
|------|--------|---------|
| btn/refresh | refresh | Induces the error child-state (REFRESH transition) |
| btn/retry | retry | Rendered only in the error child-state; visible only after REFRESH is induced |
| btn/status-note | status-note | Persists a single-field entity (UNPROVABLE substrate: writes note.text) |
