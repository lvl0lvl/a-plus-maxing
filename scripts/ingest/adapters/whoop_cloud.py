"""Whoop cloud-API ingestion adapter — parses the staged Whoop pull into store readings.

The wired `"whoop"` source (tracker-ingestion Build A): the shared OAuth/fetch layer
(`scripts/ingest/oauth_pull.py`) authenticates to Whoop's cloud API and stages the pulled readings
as a JSON array of `{item, timepoint, value}` rows in this adapter's input shape; `read_readings`
maps each row into a Line-Field-Set store reading, adding `source="whoop"`. Like every wired adapter
it is a PURE file parser — no network lives here (that is the fetch layer's sole concern), so it is
fixture-testable with a staged file and conforms to the frozen `ADR-0003-T1` contract (`source_tag`
+ `read_readings(export_file)`).

This REPLACES the noop on-device-SQLite `whoop.py` as the sole WIRED `"whoop"` source: two adapters
both emitting `source="whoop"` would dedupe-collide on `(item, day, "whoop")`, so the noop adapter is
marked `UNWIRED` (retained only as the manual-CLI / offline fallback). `source="whoop"` is
device-specific (not a shared `"wearable"` tag) so a Whoop reading and another wearable's reading at
the same (item, day) stay distinct under the (item, timepoint, source) dedupe key.
"""

from typing import Iterable

from scripts.ingest.adapters.staged_common import read_staged_rows


class WhoopCloudAdapter:
    """The Whoop cloud-API source adapter, parsing the staged pull export.

    Attributes:
        source_tag: Returns `"whoop"`, the store `source` every reading this adapter emits carries —
            device-specific so a Whoop reading and another wearable's reading at the same
            (item, timepoint) stay distinct under the (item, timepoint, source) dedupe key.
        read_readings: Maps the staged `{item, timepoint, value}` rows (produced by the OAuth/fetch
            layer) into Line-Field-Set readings, adding `source="whoop"`.
    """

    def source_tag(self) -> str:
        return "whoop"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Map the staged Whoop pull rows into Line-Field-Set store readings (see `read_staged_rows`)."""
        return read_staged_rows(export_file, self.source_tag())
