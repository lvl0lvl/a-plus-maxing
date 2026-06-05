"""Single source of truth for the store line key and field set (ADR-0002-T0).

Defines the Line Field Set every store line carries, the dedupe identity for a
reading, and the field-presence check `store.append` uses to reject malformed
readings. Both the store append path and the ADR-0003 ingestion path import this
module — there is no second key definition in the codebase.
"""

# Line Field Set (ADR-0002-T0 spike). The complete set of top-level fields a
# store line carries: item identifier, timepoint, source tag, value.
LINE_FIELDS = ("item", "timepoint", "source", "value")

# Dedupe tuple (ADR-0003 OQ-2): a subset of LINE_FIELDS, excluding `value`.
DEDUPE_FIELDS = ("item", "timepoint", "source")


def dedupe_key(reading):
    """Derive a reading's dedupe identity from the (item, timepoint, source) tuple.

    Args:
        reading (dict): A store reading carrying the dedupe fields.

    Returns:
        (tuple) The (item, timepoint, source) identity.
    """
    return tuple(reading[field] for field in DEDUPE_FIELDS)


def is_conformant(reading):
    """Report whether a reading carries every required Line Field Set field.

    Args:
        reading (dict): A store reading to validate.

    Returns:
        (bool) True if every LINE_FIELDS field is present, else False.
    """
    return all(field in reading for field in LINE_FIELDS)
