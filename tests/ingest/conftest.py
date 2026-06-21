"""Shared ingest-test helpers: the canonical Apple Health export builder + record factory.

Single-sources the formerly-forked `_write_healthkit_export` / record-factory copies that lived in
both `test_adapters.py` and `test_scheduler.py` (QUAL-2/QUAL-3). pytest's default `prepend` import
mode puts this directory on `sys.path`, so both test modules `from conftest import ...`.
"""


def write_healthkit_export(path, records):
    """Write a real-shape Apple Health `export.xml` with the given `<Record>` samples.

    Mirrors the Apple Health export format: a `<HealthData>` root (with an `<ExportDate>` line) over
    per-sample `<Record>` elements (`type` = an HKQuantityTypeIdentifier, `startDate`/`endDate` =
    "YYYY-MM-DD HH:MM:SS -ZZZZ", `value`). `records` is a list of dicts keyed `type`/`startDate`/
    `value` (+ optional `endDate`, defaulting to `startDate`). Building the real XML shape (not a
    stand-in) keeps the test exercising the adapter's actual streamed-parse path.
    """
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<HealthData locale="en_US">',
             ' <ExportDate value="2026-06-20 12:00:00 -0500"/>']
    for r in records:
        lines.append(
            f' <Record type="{r["type"]}" sourceName="Apple Watch" '
            f'startDate="{r["startDate"]}" endDate="{r.get("endDate", r["startDate"])}" '
            f'value="{r["value"]}"/>'
        )
    lines.append('</HealthData>')
    path.write_text("\n".join(lines))


def hk_record(hk_type, start_date, value, end_date=None):
    """One HealthKit `export.xml` `<Record>` dict (a real HK type identifier + value)."""
    record = {"type": hk_type, "startDate": start_date, "value": value}
    if end_date is not None:
        record["endDate"] = end_date
    return record
