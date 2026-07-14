"""Oura ring ingestion adapter (ADR-0003-T2).

Maps an Oura file-drop export into Line-Field-Set store readings. All Oura-specific
field names (`metric`, `day`, `average`) are translated here, inside `read_readings`;
the shared routine (`ingest.run`) and the adapter contract (`adapter.py`) name
no Oura field. Conforms to the frozen `ADR-0003-T1` adapter contract:
`source_tag` + `read_readings(export_file)`. UNWIRED: the cloud-API `oura_cloud`
adapter is now the sole WIRED `"oura"` source (the tracker-ingestion Build B
API-pull build); the cloud pull stages `{item, timepoint, value}` (not this
adapter's legacy `{metric, day, average}` file-drop shape), so two wired adapters
both emitting `source="oura"` would dedupe-collide on `(item, day, "oura")` — this
legacy adapter is retired from the scheduler's data-driven wired set via the
`UNWIRED` marker below. It is retained for the manual-CLI (`python -m scripts.ingest
--source oura <file>`) / offline file-drop fallback — the class is unchanged; only
its wired-set membership is dropped, exactly the Build-A whoop_cloud pattern.
"""

import json
from pathlib import Path
from typing import Iterable

# UNWIRED (tracker-ingestion Build B API-pull build): the scheduler's data-driven discovery excludes
# this module because `oura_cloud.OuraCloudAdapter` is the sole wired `"oura"` source. A truthy
# `UNWIRED` is the typed exclusion contract (`scheduler._wired_adapters`); the legacy adapter stays
# importable for the manual-CLI / file-drop fallback path, it just no longer joins the wired set.
UNWIRED = True


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
