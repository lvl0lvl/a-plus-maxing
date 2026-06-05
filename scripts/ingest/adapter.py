"""The common per-source export contract every ingestion adapter implements (ADR-0003-T1).

Defines the single stable surface the shared routine (`ingest.run`) consumes and
`ADR-0003-T2`'s adapters (HealthKit, Oura, Garmin, Whoop) plug into. The contract
is the frozen named surface — `source_tag` (zero-arg source-identity accessor) and
`read_readings(export_file)` (one-arg, yields Line-Field-Set readings in the store
reading shape). It carries NO dedupe or store-write logic: dedupe and the store
write belong to the shared routine, so an adapter cannot fork the dedupe key. The
interface names no per-source export field; all export-format specifics live inside
each adapter's `read_readings` mapping (the invariant the `ADR-0003-T2` 0-shared-
routine-edit proof rests on).
"""

from typing import Iterable, Protocol, runtime_checkable

from scripts.store import keying

# The Line Field Set field names a `read_readings` reading carries, re-exported
# from the single keying source so adapters target the store shape, not a copy.
READING_FIELDS = keying.LINE_FIELDS


@runtime_checkable
class Adapter(Protocol):
    """The per-source export contract: source identity + readings iterable.

    Attributes:
        source_tag: Zero-arg accessor returning the source tag string carried
            into each store reading per `keying.LINE_FIELDS`.
        read_readings: One-arg method taking the export file (path) and returning
            an iterable of readings; each reading carries every Line Field Set
            field in the store reading shape (an iterable of readings — not a
            count, not a write side effect).
    """

    def source_tag(self) -> str:
        ...

    def read_readings(self, export_file) -> Iterable[dict]:
        ...
