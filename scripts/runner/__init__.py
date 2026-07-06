"""The cadence-runtime package (ADR-0039): the scheduled-agent runner driver + dispatch seam.

Importing this package or its modules arms NOTHING — 0 `signal` / de-id / dispatch fires on import
(disabled-by-default, ADR-0039 governing invariant 3). The driver runs only when
`cadence_runner.run` is called (per scheduled tick) or `python -m scripts.runner.cadence_runner`
is executed. The package holds no module-level side effects.
"""
