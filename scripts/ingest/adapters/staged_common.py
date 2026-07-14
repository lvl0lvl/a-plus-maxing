"""Shared staged-row reader for the cloud-API adapters (whoop / oura / garmin / google-health).

The four `*_cloud` adapters stage the OAuth/fetch layer's `{item, timepoint, value}` rows identically;
only their `source_tag()` differs. `read_staged_rows` is that one shared body — each adapter's
`read_readings` is a one-liner delegating here with its own source tag — so the parser lives in ONE
place while the four dedicated adapters (design-note F1: one dedicated `*_cloud` adapter per source)
stay distinct. This module is not an adapter itself (it declares no `Adapter` class), so the
scheduler's data-driven `_wired_adapters()` discovery never wires it.
"""

import json
from pathlib import Path
from typing import Iterable


def read_staged_rows(export_file, source) -> Iterable[dict]:
    """Map a staged pull export's `{item, timepoint, value}` rows into Line-Field-Set store readings.

    Reads the staged JSON array (`[{item, timepoint, value}, ...]`) the OAuth/fetch layer wrote and
    yields one reading per row, adding `source`. A missing / non-JSON staged file raises in the read
    (the fail-loud signal of a misconfigured path), rather than silently importing nothing.

    Args:
        export_file (str | Path): Path to the staged pull JSON.
        source (str): The device-specific store `source` tag stamped on each emitted reading.
    """
    records = json.loads(Path(export_file).read_text())
    for record in records:
        yield {
            "item": record["item"],
            "timepoint": record["timepoint"],
            "source": source,
            "value": record["value"],
        }
