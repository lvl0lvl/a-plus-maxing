"""Whoop ingestion adapter — reads noop's read-only on-device SQLite (ADR-0011 D2 v2).

Reads the WHOOP metrics that noop (`github.com/NoopApp/noop`) computes on-device
and stores in its local SQLite DB (`whoop.sqlite`, documented in noop's
`docs/DATA_MODEL.md`, schemaVersion 9). The "export" this adapter reads IS that DB
file: `read_readings(export_file)` opens it READ-ONLY (`sqlite3` URI `mode=ro`) and
maps each `dailyMetric` row (one per calendar `day`) into Line-Field-Set store
readings. No noop code is bundled or linked — the adapter parses a file the
operator owns (ADR-0011 license path (a)); the read is one-way and read-only by
construction, so it never mutates noop's DB.

Mechanism choice (ADR-0011 OQ-2/OQ-3, resolved at this build): a read-only
`sqlite3` read over the documented schema, NOT the `noop-local-access` MCP
subprocess. The adapter contract is file-based (`read_readings(export_file)`), so a
DB-file read fits the ADR-0003 seam with 0 edits to the shared routine/scheduler;
it is Python-native and license-safe. The MCP path is the documented fallback if
the schema read ever proves insufficient.

Conforms to the frozen `ADR-0003-T1` contract (`source_tag` + `read_readings`); all
noop-specific names (the `dailyMetric` columns) are translated here, so the shared
routine (`ingest.run`) and the contract (`adapter.py`) name no Whoop field. WIRED:
this module declares no `UNWIRED` marker, so the scheduler's data-driven discovery
includes it (ADR-0011 D2 — replaces the prior registered-but-unwired scaffold).
"""

import sqlite3
from pathlib import Path
from typing import Iterable

# noop `dailyMetric` column -> the store `item` it maps to. One DB row per calendar
# `day`; each non-null metric below becomes one reading on the (item, day, source)
# key. Item names follow the `biomarker_meta` registry convention (hyphenated;
# `hrv`/`rhr` are already registered, so a Whoop reading shares those streams with
# any other wearable and stays distinct only by `source`). `strain` carries
# WHOOP's 0-21 Day-Strain scale UNSCALED (ADR-0011: a 0-100 render is ~5x wrong);
# `skin-temp-dev` is a deviation from baseline in °C, not an absolute temperature.
_DAILY_METRIC_ITEMS = {
    "recovery": "recovery",            # recovery score, 0-100
    "strain": "strain",                # day strain, 0-21 (NOT 0-100)
    "avgHrv": "hrv",                   # average HRV, ms
    "restingHr": "rhr",                # resting heart rate, bpm
    "efficiency": "sleep-efficiency",  # sleep efficiency, %
    "spo2Pct": "spo2",                 # mean SpO2 during sleep, %
    "respRateBpm": "resp-rate",        # mean respiration rate, breaths/min
    "skinTempDevC": "skin-temp-dev",   # skin-temperature deviation, °C from baseline
}


class WhoopAdapter:
    """The Whoop source adapter, reading noop's read-only on-device SQLite.

    Attributes:
        source_tag: Returns `"whoop"`, the store `source` (device provenance) every
            reading this adapter emits carries. Device-specific (not a shared
            `"wearable"` tag) so a Whoop reading and another wearable's reading at
            the same (item, timepoint) stay distinct under the
            (item, timepoint, source) dedupe key — a shared tag would collide them
            and silently drop one. The biomarker-page `source: wearable` enum
            (ADR-0011 D4) is a separate layer.
        read_readings: Opens noop's `whoop.sqlite` READ-ONLY and maps each
            `dailyMetric` row's non-null metrics into Line-Field-Set readings.
    """

    def source_tag(self) -> str:
        return "whoop"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Map noop's `dailyMetric` rows into Line-Field-Set store readings.

        Opens `export_file` (noop's `whoop.sqlite`) read-only and yields one
        reading per non-null mapped metric per day. A NULL metric column yields no
        reading (honest absence, never a fabricated value). A missing file, a
        non-SQLite file, or a DB without the `dailyMetric` table raises (the
        fail-loud signal of a misconfigured path or a non-noop DB), rather than
        silently importing nothing.

        Args:
            export_file (str | Path): Path to noop's `whoop.sqlite`.
        """
        # `as_uri()` percent-encodes the path (incl. `?`/`#`) so the appended
        # `?mode=ro` query cannot be defeated by a special char in the path — a raw
        # f-string would let a `?` in the path swallow the read-only flag (open
        # writable) or a `#` truncate to the wrong file.
        uri = Path(export_file).resolve().as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        try:
            conn.row_factory = sqlite3.Row
            columns = ", ".join(_DAILY_METRIC_ITEMS)
            rows = conn.execute(
                f"SELECT day, {columns} FROM dailyMetric ORDER BY day"
            ).fetchall()
        finally:
            conn.close()

        for row in rows:
            day = row["day"]
            for column, item in _DAILY_METRIC_ITEMS.items():
                value = row[column]
                if value is None:
                    continue
                yield {
                    "item": item,
                    "timepoint": day,
                    "source": self.source_tag(),
                    "value": value,
                }
