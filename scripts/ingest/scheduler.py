"""Unattended scheduler run: delta-since-last-run over the wired adapter set (ADR-0003-T3).

`run(exports)` is the unattended-run seam. It discovers the WIRED adapter set
data-driven from the `adapters/` package — every module exposing a conformant
`Adapter` whose module does NOT declare itself an unwired scaffold — and invokes
the UNCHANGED `ingest.run(adapter, export_file)` once per wired adapter. The
delta-since-last-run behaviour (only new-timepoint readings appended on a second
run) and the idempotent no-new re-run (0 lines appended) are inherited from
`ingest.run`'s shared-key `store.append` dedupe; the scheduler re-implements no
dedupe and defines no second key. It reads no stdin and prompts for no operator
input — it completes unattended with exit 0. The only sink is `ingest.run` ->
store: no model step, no outbound network call (ADR-0001 D1->D3).

The wired set is DATA-DRIVEN: a further adapter is added by dropping a new
conformant adapter module into `adapters/`, with 0 edits to this file. A
registered-but-unwired scaffold adapter is excluded by the wired-set membership
rule, NOT by a hardcoded per-adapter call list and NOT by naming any source here
— its own module declares itself an unwired scaffold, and the discovery skips any
adapter whose module so declares (the marker the wired adapters do not carry).
"""

import importlib
import inspect
from pathlib import Path

from scripts.ingest import ingest
from scripts.ingest.adapter import Adapter

_ADAPTERS_DIR = Path(__file__).resolve().parent / "adapters"
_ADAPTERS_PKG = "scripts.ingest.adapters"

# An adapter module that declares itself a not-yet-wired scaffold (in its module
# docstring) is excluded from the wired set — the membership marker the wired
# adapters do not carry. Matching the generic declaration, not a source name,
# keeps the wired set data-driven and this file free of any per-source token.
_UNWIRED_MARKER = "unwired"


def _wired_adapters():
    """Discover the wired adapter instances from the `adapters/` package.

    Iterates every adapter module in `adapters/`, yields one instance per module
    exposing a conformant `Adapter` class, and skips any module that declares
    itself an unwired scaffold (its module docstring carries the unwired marker).
    Data-driven: a new conformant adapter module joins the wired set with no edit
    to this file.

    Returns:
        (list) One conformant `Adapter` instance per wired adapter module.
    """
    wired = []
    for module_path in sorted(_ADAPTERS_DIR.glob("*.py")):
        if module_path.stem.startswith("_"):
            continue
        module = importlib.import_module(f"{_ADAPTERS_PKG}.{module_path.stem}")
        if _UNWIRED_MARKER in (module.__doc__ or "").lower():
            continue
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__ and isinstance(obj(), Adapter):
                wired.append(obj())
                break
    return wired


def run(exports, root=ingest.store.DEFAULT_ROOT):
    """Run the unattended ingestion over the wired adapter set; return exit 0.

    Invokes the UNCHANGED `ingest.run` once per wired adapter (discovered
    data-driven from the `adapters/` package), appending only readings new since
    the last run via `ingest.run`'s inherited dedupe. Reads no stdin and prompts
    for no operator input. Excludes any registered-but-unwired scaffold adapter.
    Makes 0 outbound network calls — every write path is `ingest.run` -> store.

    An adapter with no export in `exports` is skipped (the scheduler runs only the
    wired adapters it has an export for; a source the operator has not exported
    yet contributes nothing, rather than failing the unattended run).

    Args:
        exports (dict): Map of source tag -> export file path, one per wired
            adapter to run this invocation.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (int) 0 — the unattended run completed.
    """
    for adapter in _wired_adapters():
        export_file = exports.get(adapter.source_tag())
        if export_file is not None:
            ingest.run(adapter, export_file, root=root)
    return 0
