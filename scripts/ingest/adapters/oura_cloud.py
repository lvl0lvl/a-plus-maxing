"""Oura cloud-API ingestion adapter — parses the staged Oura pull into store readings.

The wired `"oura"` source (tracker-ingestion Build B): the shared OAuth/fetch layer
(`scripts/ingest/oauth_pull.py`) authenticates to Oura's API v2 and stages the pulled readings as a
JSON array of `{item, timepoint, value}` rows in this adapter's input shape; `read_readings` maps each
row into a Line-Field-Set store reading, adding `source="oura"`. Like every wired adapter it is a PURE
file parser — no network lives here (that is the fetch layer's sole concern), so it is fixture-testable
with a staged file and conforms to the frozen `ADR-0003-T1` contract (`source_tag` + `read_readings`).

This REPLACES the legacy file-drop `oura.py` as the sole WIRED `"oura"` source: the cloud pull stages
`{item, timepoint, value}` (not the legacy `{metric, day, average}`), so two adapters both emitting
`source="oura"` would either dedupe-collide on `(item, day, "oura")` or crash on the other's shape.
The legacy adapter is marked `UNWIRED` (retained for the manual-CLI / file-drop fallback), exactly the
Build-A whoop_cloud pattern. `source="oura"` is device-specific so an Oura reading and another
wearable's reading at the same (item, day) stay distinct under the (item, timepoint, source) key.
"""

from typing import Iterable

from scripts.ingest.adapters.staged_common import read_staged_rows


class OuraCloudAdapter:
    """The Oura cloud-API source adapter, parsing the staged pull export.

    Attributes:
        source_tag: Returns `"oura"`, the store `source` every reading this adapter emits carries —
            device-specific so an Oura reading and another wearable's reading at the same
            (item, timepoint) stay distinct under the (item, timepoint, source) dedupe key.
        read_readings: Maps the staged `{item, timepoint, value}` rows (produced by the OAuth/fetch
            layer) into Line-Field-Set readings, adding `source="oura"`.
    """

    def source_tag(self) -> str:
        return "oura"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Map the staged Oura pull rows into Line-Field-Set store readings (see `read_staged_rows`)."""
        return read_staged_rows(export_file, self.source_tag())
