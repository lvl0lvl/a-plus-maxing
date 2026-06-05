"""Garmin ingestion adapter (ADR-0003-T2).

Maps a Garmin export into Line-Field-Set store readings. All Garmin-specific
field names (`summaryType`, `calendarDate`, and the measurement field) are
translated here, inside `read_readings`; the shared routine (`ingest.run`) and
the adapter contract (`adapter.py`) name no Garmin field. Adding this adapter
wires a new source by adding ONE module and nothing else (the ADR-0003-T2
0-shared-routine-edit proof). An upstream measurement-field rename (`value` ->
`valueInMillis`) is absorbed ENTIRELY here too (the ADR-0003-T2 format-rename
re-validation proof): the renamed field maps to the same `value` store field, so
the (item, timepoint, source) dedupe key is re-derived unchanged — no shared-
routine edit. Conforms to the frozen `ADR-0003-T1` adapter contract: `source_tag`
+ `read_readings(export_file)`.
"""

import json
from pathlib import Path
from typing import Iterable


class GarminAdapter:
    """The Garmin source adapter.

    Attributes:
        source_tag: Returns `"garmin"`, the store `source` every reading this
            adapter emits carries.
        read_readings: Maps a Garmin JSON export (`summaryType`/`calendarDate`/
            measurement per sample) into Line-Field-Set readings. The measurement
            field is read as `valueInMillis` if the renamed schema is present,
            else the original `value` — both map to the store `value` field.
    """

    def source_tag(self) -> str:
        return "garmin"

    def read_readings(self, export_file) -> Iterable[dict]:
        records = json.loads(Path(export_file).read_text())
        for record in records:
            measurement = (
                record["valueInMillis"]
                if "valueInMillis" in record
                else record["value"]
            )
            yield {
                "item": record["summaryType"],
                "timepoint": record["calendarDate"],
                "source": self.source_tag(),
                "value": measurement,
            }
