"""Oura ring ingestion adapter (ADR-0003-T2).

Maps an Oura export into Line-Field-Set store readings. All Oura-specific field
names (`metric`, `day`, `average`) are translated here, inside `read_readings`;
the shared routine (`ingest.run`) and the adapter contract (`adapter.py`) name
no Oura field. Conforms to the frozen `ADR-0003-T1` adapter contract:
`source_tag` + `read_readings(export_file)`.
"""

import json
from pathlib import Path
from typing import Iterable


class OuraAdapter:
    """The Oura ring source adapter.

    Attributes:
        source_tag: Returns `"oura"`, the store `source` every reading this
            adapter emits carries.
        read_readings: Maps an Oura JSON export (`metric`/`day`/`average` per
            sample) into Line-Field-Set readings.
    """

    def source_tag(self) -> str:
        return "oura"

    def read_readings(self, export_file) -> Iterable[dict]:
        records = json.loads(Path(export_file).read_text())
        for record in records:
            yield {
                "item": record["metric"],
                "timepoint": record["day"],
                "source": self.source_tag(),
                "value": record["average"],
            }
