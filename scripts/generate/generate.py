"""On-demand + unattended (cron) generation entry point (ADR-0004-T3).

`run(artifact_name)` is a THIN entry point over the ADR-0004-T1 render engine. It
reads the cross-item store read model through the published `store.read_all`,
selects the named template, drives ONE `render.emit` invocation (which writes the
single self-contained HTML file and returns its path), and returns that path. The
SAME code path serves both the interactive (on-demand) invocation and the
unattended/cron invocation — it reads no stdin, prompts for nothing, opens no
server, and binds no listening socket (run-to-completion-and-exit). It does not
swallow `render.emit`'s external-asset refusal: that raise surfaces as a non-zero
exit rather than a partial artifact.

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


def run(artifact_name, *, _root=None, _out_dir=None, _today=None):
    """Render the named artifact from the current store state and return its path.

    One code path for both the on-demand and the unattended/cron entry mode:
    reads the store read model via the published `store.read_all`, selects the
    template by `artifact_name`, and drives exactly ONE `render.emit`, returning
    the path emit wrote. Reads no stdin and prompts for nothing; opens no server
    and binds no listening socket.

    Args:
        artifact_name (str): The artifact to render: 'dashboard' or 'report'.
        _root (str | Path, optional): Test-only store-root seam. Defaults to the
            store's `vault/store/`.
        _out_dir (Path, optional): Test-only output-dir seam, forwarded to
            `render.emit`. Defaults to the engine-owned `vault/artifacts/generated/`.
        _today (datetime.date, optional): Test-only date seam forwarded to the
            template render's `_today` (the dashboard's calendar + plan
            resolution; the report's prepared/generated dates + plan
            resolution). Defaults to the template's real current date.

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
    store_read = store.read_all(root)
    if _today is None:
        return render.emit(template, store_read, _out_dir=_out_dir)

    def seamed(store_read):
        return template.render(store_read, _today=_today)

    # Keep emit's module-derived output filename (e.g. `dashboard.html`).
    seamed.__name__ = template.__name__
    return render.emit(seamed, store_read, _out_dir=_out_dir)


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
