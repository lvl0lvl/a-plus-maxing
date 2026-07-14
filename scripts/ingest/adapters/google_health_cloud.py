"""Google Health cloud-API ingestion adapter — parses the staged Google Health pull into readings.

The wired `"google-health"` source (tracker-ingestion Build B): the shared OAuth/fetch layer
(`scripts/ingest/oauth_pull.py`) authenticates to the Google Health API (health.googleapis.com/v4,
covering Fitbit / Pixel devices; the legacy Fitbit Web API sunsets Sep 2026, so this is greenfield on
the new API) and stages the pulled readings as a JSON array of `{item, timepoint, value}` rows in this
adapter's input shape; `read_readings` maps each row into a Line-Field-Set store reading, adding
`source="google-health"`. Like every wired adapter it is a PURE file parser — no network lives here
(that is the fetch layer's sole concern), so it is fixture-testable with a staged file and conforms to
the frozen `ADR-0003-T1` contract (`source_tag` + `read_readings`).

Google Health is NEW — there is no legacy file-drop adapter to retire (unlike oura/garmin). This is
the sole `"google-health"` source. `source="google-health"` is device-specific so a Google-Health
reading and another wearable's reading at the same (item, day) stay distinct under the
(item, timepoint, source) dedupe key.
"""

from typing import Iterable

from scripts.ingest.adapters.staged_common import read_staged_rows


class GoogleHealthCloudAdapter:
    """The Google Health cloud-API source adapter, parsing the staged pull export.

    Attributes:
        source_tag: Returns `"google-health"`, the store `source` every reading this adapter emits
            carries — device-specific so a Google-Health reading and another wearable's reading at the
            same (item, timepoint) stay distinct under the (item, timepoint, source) dedupe key.
        read_readings: Maps the staged `{item, timepoint, value}` rows (produced by the OAuth/fetch
            layer) into Line-Field-Set readings, adding `source="google-health"`.
    """

    def source_tag(self) -> str:
        return "google-health"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Map the staged Google Health pull rows into Line-Field-Set readings (see `read_staged_rows`)."""
        return read_staged_rows(export_file, self.source_tag())
