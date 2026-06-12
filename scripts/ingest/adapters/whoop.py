"""Whoop ingestion adapter — registered-but-unwired scaffold (ADR-0003-T2).

Maps a Whoop export into Line-Field-Set store readings. All Whoop-specific field
names (`metric_name`, `cycle_start`, `score`) are translated here, inside
`read_readings`; the shared routine (`ingest.run`) and the adapter contract
(`adapter.py`) name no Whoop field. This adapter conforms FULLY to the frozen
`ADR-0003-T1` contract (`source_tag` + `read_readings(export_file)`) — it is a
complete, pluggable adapter, NOT a crippled stub. It is the registered-but-
UNWIRED scaffold (ADR-0003 Risk N2): no scheduler/wired-set entry point imports
it yet, so until a later task wires it into the data-driven wired set (with 0
adapter-side edits), Whoop data narrows to `ingest.manual_entry`. "Unwired" is a
property of the absent scheduler wiring, not of this adapter.
"""

import json
from pathlib import Path
from typing import Iterable

# Typed unwired-scaffold declaration: the scheduler's wired-set discovery
# excludes any adapter module carrying this attribute (ADR-0003 Risk N2).
UNWIRED = True


class WhoopAdapter:
    """The Whoop source adapter (registered, pluggable, not yet wired).

    Attributes:
        source_tag: Returns `"whoop"`, the store `source` every reading this
            adapter emits carries.
        read_readings: Maps a Whoop JSON export (`metric_name`/`cycle_start`/
            `score` per sample) into Line-Field-Set readings.
    """

    def source_tag(self) -> str:
        return "whoop"

    def read_readings(self, export_file) -> Iterable[dict]:
        records = json.loads(Path(export_file).read_text())
        for record in records:
            yield {
                "item": record["metric_name"],
                "timepoint": record["cycle_start"],
                "source": self.source_tag(),
                "value": record["score"],
            }
