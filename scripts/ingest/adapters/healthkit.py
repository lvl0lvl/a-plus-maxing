"""HealthKit (Apple Health) ingestion adapter — reads the real Apple Health export.xml.

Apple Health exports a zip whose `export.xml` holds one `<Record>` element per RAW sample
(`type` = an HKQuantityTypeIdentifier, `startDate`/`endDate` timestamps, `value`, `unit`). This
adapter STREAMS that XML (`iterparse`, clearing each parsed element — the export can be hundreds of
MB) and AGGREGATES the raw per-sample records to ONE value per (item, day): Apple records many
samples a day (dozens of HRV / heart-rate readings), so the adapter takes the daily MEAN, keyed on
the sample's `startDate` calendar date, to match the store's one-reading-per-(item, day, source)
key. That daily roll-up is the granularity difference from the Whoop adapter, whose on-device DB
already gives one pre-aggregated row per day.

All HealthKit-specific names (the HK type identifiers, the export date format, the SpO2 fraction
convention) are translated HERE, inside `read_readings`; the shared routine (`ingest.run`) and the
adapter contract (`adapter.py`) name no HealthKit field — the ADR-0003-T2 0-shared-routine-edit
invariant. `source_tag` is `"healthkit"`, device-specific (not a shared `"wearable"` tag) so a
HealthKit reading and a Whoop reading at the same (item, day) stay distinct under the
(item, timepoint, source) dedupe key — a shared tag would collide them and silently drop one.

recovery/strain are NOT emitted — Apple Health has no recovery-score or strain equivalent (those are
Whoop-proprietary composites); the absence is honest and consistent with treating wearable readiness
composites as non-validated. `skin-temp-dev` and `sleep-efficiency` are deliberately not mapped here
(see the ADR): Apple's `AppleSleepingWristTemperature` is an ABSOLUTE °C, not the deviation the store
item expects, and sleep-efficiency needs a sleep-stage-duration roll-up — both deferred.

The "export" is a file the operator owns (exported from the Health app); the read is one-way +
read-only (parse only). Conforms to the frozen `ADR-0003-T1` contract (`source_tag` + `read_readings`).
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Iterable

# HealthKit `Record@type` -> the store `item` it maps to. The store items are already registered
# (shared with any other wearable; a HealthKit reading is distinct only by `source`). Only the
# value-domain-clean metrics are mapped: hrv (ms), rhr (bpm), resp-rate (breaths/min) carry the same
# unit as the store item; spo2 needs the fraction->percent scale below. recovery/strain (no Apple
# equivalent), skin-temp-dev (Apple's absolute wrist temp vs the store's deviation), and
# sleep-efficiency (a sleep-stage roll-up) are intentionally absent — see the module docstring + ADR.
_RECORD_TYPE_ITEMS = {
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv",
    "HKQuantityTypeIdentifierRestingHeartRate": "rhr",
    "HKQuantityTypeIdentifierRespiratoryRate": "resp-rate",
    "HKQuantityTypeIdentifierOxygenSaturation": "spo2",
}

# HealthKit `OxygenSaturation` stores the 0-1 fraction (HKUnit percent); the store `spo2` item is a
# percent (the Whoop adapter writes 97.0). Scale ×100 so a HealthKit 0.97 and a Whoop 97.0 land on
# the same scale. The other mapped metrics carry the store item's unit as-is (no scale).
_ITEM_SCALE = {"spo2": 100.0}


class HealthKitAdapter:
    """The HealthKit (Apple Health) source adapter, reading the real `export.xml`.

    Attributes:
        source_tag: Returns `"healthkit"`, the store `source` (device provenance) every reading this
            adapter emits carries — device-specific so a HealthKit reading and another wearable's
            reading at the same (item, timepoint) stay distinct under the (item, timepoint, source)
            dedupe key.
        read_readings: Streams Apple Health's `export.xml` and maps each mapped `<Record>`'s value
            into the daily MEAN per (item, day) as a Line-Field-Set reading.
    """

    def source_tag(self) -> str:
        return "healthkit"

    def read_readings(self, export_file) -> Iterable[dict]:
        """Stream `export.xml`'s `<Record>` samples into daily-mean Line-Field-Set readings.

        Accumulates every mapped record's value under (day, item), then yields the daily MEAN per
        (item, day). A day with no samples of a metric yields no reading (honest absence, never a
        fabricated value). A missing file or a non-XML / malformed file raises (the fail-loud signal
        of a misconfigured path or a non-Apple-Health export), rather than silently importing nothing.

        Args:
            export_file (str | Path): Path to Apple Health's `export.xml` (extracted from the export
                zip the operator produces in the Health app).
        """
        # day -> item -> [values] accumulated across the streamed records, then averaged. Holds only
        # floats (the parsed XML elements are cleared as we go), so memory is bounded by the number of
        # distinct (day, item) pairs, not the export size.
        per_day = defaultdict(lambda: defaultdict(list))
        context = ET.iterparse(export_file, events=("start", "end"))
        _, root = next(context)  # the root `<HealthData>` element, from its start event
        for event, elem in context:
            if event != "end" or elem.tag != "Record":
                continue
            item = _RECORD_TYPE_ITEMS.get(elem.get("type"))
            start = elem.get("startDate")
            value = elem.get("value")
            if item is not None and start and value is not None:
                # The day is the first 10 chars of "YYYY-MM-DD HH:MM:SS -ZZZZ".
                per_day[start[:10]][item].append(float(value))
            # Bounded memory over a 100s-of-MB export: drop root's ENTIRE accumulated child subtree on
            # each Record-end so the parsed tree does not grow (the stdlib iterparse memory-safety
            # pattern). Safe ONLY because this record's value was already copied into `per_day` above —
            # the extract-before-clear invariant; clearing earlier would discard an unread value.
            root.clear()

        for day in sorted(per_day):
            for item, values in sorted(per_day[day].items()):
                mean = sum(values) / len(values)
                # The daily mean + the spo2 ×100 scale produce binary-float artifacts (e.g.
                # 0.97*100 = 96.9999…); round to 2 decimals so the STORED value is clean (more
                # precision than these metrics carry is meaningless). A documented storage precision.
                yield {
                    "item": item,
                    "timepoint": day,
                    "source": self.source_tag(),
                    "value": round(mean * _ITEM_SCALE.get(item, 1.0), 2),
                }
