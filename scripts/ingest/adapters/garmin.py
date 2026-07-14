"""Garmin ingestion adapter (ADR-0003-T2).

Maps a Garmin file-drop export into Line-Field-Set store readings. All Garmin-specific
field names (`summaryType`, `calendarDate`, and the measurement field) are
translated here, inside `read_readings`; the shared routine (`ingest.run`) and
the adapter contract (`adapter.py`) name no Garmin field. The measurement field
is read as `valueInMillis` if the renamed schema is present, else the original
`value` — both map to the store `value` field. Conforms to the frozen
`ADR-0003-T1` adapter contract: `source_tag` + `read_readings(export_file)`.
UNWIRED: the cloud-API `garmin_cloud` adapter is now the sole WIRED `"garmin"`
source (the tracker-ingestion Build B API-pull build); the cloud pull stages
`{item, timepoint, value}` (not this adapter's legacy `{summaryType, calendarDate,
value}` file-drop shape), so two wired adapters both emitting `source="garmin"`
would dedupe-collide on `(item, day, "garmin")` — this legacy adapter is retired
from the scheduler's data-driven wired set via the `UNWIRED` marker below. It is
retained for the manual-CLI (`python -m scripts.ingest --source garmin <file>`) /
offline file-drop fallback — the class is unchanged; only its wired-set membership
is dropped, exactly the Build-A whoop_cloud pattern.
"""

import json
from pathlib import Path
from typing import Iterable

# UNWIRED (tracker-ingestion Build B API-pull build): the scheduler's data-driven discovery excludes
# this module because `garmin_cloud.GarminCloudAdapter` is the sole wired `"garmin"` source. A truthy
# `UNWIRED` is the typed exclusion contract (`scheduler._wired_adapters`); the legacy adapter stays
# importable for the manual-CLI / file-drop fallback path, it just no longer joins the wired set.
UNWIRED = True


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
