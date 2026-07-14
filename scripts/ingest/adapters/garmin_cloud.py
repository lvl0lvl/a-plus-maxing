"""Garmin cloud-API ingestion adapter — parses the staged Garmin pull into store readings.

The wired `"garmin"` source (tracker-ingestion Build B): the shared OAuth/fetch layer
(`scripts/ingest/oauth_pull.py`) authenticates to Garmin's Health API (the OAuth 1.0a signing fork,
design §10.2) and stages the pulled readings as a JSON array of `{item, timepoint, value}` rows in
this adapter's input shape; `read_readings` maps each row into a Line-Field-Set store reading, adding
`source="garmin"`. Like every wired adapter it is a PURE file parser — no network (and no OAuth
signing) lives here (that is the fetch layer's sole concern), so it is fixture-testable with a staged
file and conforms to the frozen `ADR-0003-T1` contract (`source_tag` + `read_readings`).

This REPLACES the legacy file-drop `garmin.py` as the sole WIRED `"garmin"` source: the cloud pull
stages `{item, timepoint, value}` (not the legacy `{summaryType, calendarDate, value}`), so two
adapters both emitting `source="garmin"` would either dedupe-collide on `(item, day, "garmin")` or
crash on the other's shape. The legacy adapter is marked `UNWIRED` (retained for the manual-CLI /
file-drop fallback), exactly the Build-A whoop_cloud pattern. `source="garmin"` is device-specific so
a Garmin reading and another wearable's reading at the same (item, day) stay distinct under the
(item, timepoint, source) key.
"""

from typing import Iterable

from scripts.ingest.adapters.staged_common import read_staged_rows


class GarminCloudAdapter:
    """The Garmin cloud-API source adapter, parsing the staged pull export.

    Attributes:
        source_tag: Returns `"garmin"`, the store `source` every reading this adapter emits carries —
            device-specific so a Garmin reading and another wearable's reading at the same
            (item, timepoint) stay distinct under the (item, timepoint, source) dedupe key.
        read_readings: Maps the staged `{item, timepoint, value}` rows (produced by the OAuth/fetch
            layer) into Line-Field-Set readings, adding `source="garmin"`.
    """

    def source_tag(self) -> str:
        return "garmin"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Map the staged Garmin pull rows into Line-Field-Set store readings (see `read_staged_rows`)."""
        return read_staged_rows(export_file, self.source_tag())
