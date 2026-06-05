"""HealthKit (Apple Watch) ingestion adapter (ADR-0003-T2).

Maps an Apple HealthKit export into Line-Field-Set store readings. All
HealthKit-specific field names (`type`, `startDate`, `qty`) are translated
here, inside `read_readings`; the shared routine (`ingest.run`) and the adapter
contract (`adapter.py`) name no HealthKit field. Conforms to the frozen
`ADR-0003-T1` adapter contract: `source_tag` + `read_readings(export_file)`.
"""

import json
from pathlib import Path
from typing import Iterable


class HealthKitAdapter:
    """The HealthKit (Apple Watch) source adapter.

    Attributes:
        source_tag: Returns `"healthkit"`, the store `source` every reading this
            adapter emits carries.
        read_readings: Maps a HealthKit JSON export (`type`/`startDate`/`qty`
            per sample) into Line-Field-Set readings.
    """

    def source_tag(self) -> str:
        return "healthkit"

    def read_readings(self, export_file) -> Iterable[dict]:
        records = json.loads(Path(export_file).read_text())
        for record in records:
            yield {
                "item": record["type"],
                "timepoint": record["startDate"],
                "source": self.source_tag(),
                "value": record["qty"],
            }
