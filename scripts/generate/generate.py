"""On-demand + unattended (cron) generation entry point (ADR-0004-T3).

`run(artifact_name)` is a THIN entry point over the ADR-0004-T1 render engine. It
assembles the cross-item store read model, selects the named template, drives ONE
`render.emit` invocation (which writes the single self-contained HTML file and
returns its path), and returns that path. The SAME code path serves both the
interactive (on-demand) invocation and the unattended/cron invocation — it reads
no stdin, prompts for nothing, opens no server, and binds no listening socket
(run-to-completion-and-exit). It does not swallow `render.emit`'s external-asset
refusal: that raise surfaces as a non-zero exit rather than a partial artifact.

The cron-/operator-invocable surface is `python -m scripts.generate.generate
<artifact_name>`, wired through `main` -> `run` -> exit 0.
"""

import argparse
import sys
from pathlib import Path

from scripts.generate import render
from scripts.store import store
from vault.design.templates import dashboard, report

# The artifact_name -> template-module selection. A template is a module exposing
# render(store_read); render.emit names the output file from the module.
_TEMPLATES = {"dashboard": dashboard, "report": report}


def _read_store(root):
    """Assemble the flat cross-item store read model the templates consume.

    The published store surface is per-item (`store.read(item, root)`); there is
    no read-all. This enumerates the item files under the store root and
    concatenates their readings into the flat list the templates expect.

    NOTE: this couples `generate.run` to the store's on-disk layout (one
    `<item>.ndjson` per item). A future published `store.read_all` / `store.items`
    surface should replace this helper in one line.

    Args:
        root (str | Path): The store root holding one `.ndjson` file per item.

    Returns:
        (list) The flat list of reading dicts across every item, item-name sorted.
    """
    items = sorted(p.stem for p in Path(root).glob("*.ndjson"))
    readings = []
    for item in items:
        readings.extend(store.read(item, root=root))
    return readings


def run(artifact_name, *, _root=None, _out_dir=None):
    """Render the named artifact from the current store state and return its path.

    One code path for both the on-demand and the unattended/cron entry mode:
    assembles the store read model, selects the template by `artifact_name`, and
    drives exactly ONE `render.emit`, returning the path emit wrote. Reads no
    stdin and prompts for nothing; opens no server and binds no listening socket.

    Args:
        artifact_name (str): The artifact to render: 'dashboard' or 'report'.
        _root (str | Path, optional): Test-only store-root seam. Defaults to the
            store's `vault/store/`.
        _out_dir (Path, optional): Test-only output-dir seam, forwarded to
            `render.emit`. Defaults to the engine-owned `vault/artifacts/generated/`.

    Returns:
        (Path) The path of the single self-contained HTML file written.

    Raises:
        KeyError: `artifact_name` is not a known template.
        ValueError: `render.emit` refused an external-asset reference (propagated).
    """
    if artifact_name not in _TEMPLATES:
        raise KeyError(
            f"unknown artifact {artifact_name!r}; known: {sorted(_TEMPLATES)}"
        )
    template = _TEMPLATES[artifact_name]
    root = _root if _root is not None else store.DEFAULT_ROOT
    store_read = _read_store(root)
    return render.emit(template, store_read, _out_dir=_out_dir)


def main(argv=None):
    """Run the named artifact, print its path, and return 0.

    Args:
        argv (list, optional): Argument vector; defaults to `sys.argv[1:]`.

    Returns:
        (int) 0 on success. A `run` failure propagates (non-zero exit).
    """
    parser = argparse.ArgumentParser(prog="generate")
    parser.add_argument("artifact_name", choices=sorted(_TEMPLATES))
    parser.add_argument("--root", default=None)
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir) if args.out_dir is not None else None
    path = run(args.artifact_name, _root=args.root, _out_dir=out_dir)
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
