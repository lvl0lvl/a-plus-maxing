# Interaction Model — incident-mgmt

Inventory of every screen and interactive element. The per-screen "Expected
interactive elements" count is the independent non-vacuity floor the gates consume
(§5 / T-1): pen-lint FAILs a screen whose wiring-manifest rows fall short of it, and
FATALs a project with declared screens but a zero-row manifest.

## screen/incident-review

Expected interactive elements: 3

| name | wireId | purpose |
|------|--------|---------|
| btn/submit-report | submit-report | Submit the incident report for review |
| input/notes | notes | Edit the incident notes |
| toggle/details | details | Expand or collapse the incident detail panel |

## screen/dashboard

Expected interactive elements: 3

| name | wireId | purpose |
|------|--------|---------|
| btn/new-incident | new-incident | Open the new-incident screen |
| btn/drill | metric-open-incidents.drill | Drill from the open-incidents metric into review |
| input/search-incidents | search-incidents | Holds the incident search query for local filtering (action `input` = transient field entry, ephemeral-compatible) |

## screen/_shell

Expected interactive elements: 1

| name | wireId | purpose |
|------|--------|---------|
| nav/incidents | incidents | Navigate to the incidents dashboard |
