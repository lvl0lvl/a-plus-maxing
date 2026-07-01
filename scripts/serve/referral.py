"""Read-only intake-referral collation (ADR-0033-0035-T3, ADR-0034 crown-jewel).

`collate` reads the `referral::*` store items written by the capture safety region and
returns the POSITIVE safety-screen referral flags for the doctor-visit / My-Info display
(a present `referral::<screen>` item -> its screen; absent -> not, so a negative safety
answer yields no flag). This is the INTAKE-time serve-layer collation — DISTINCT from the
plan-time medical-liaison doctor-visit queue, which this module neither imports nor
touches.

READ-ONLY / 0-egress by construction: it reads through the injected store read surface
only (mirroring `router.summarize`'s caller contract), never a write path (no append /
correct), and imports no outbound client and no model SDK.
"""

# The three intake safety screens whose positive referral flags this surface collates —
# the SAME pinned set the capture safety region writes (single source of truth).
_REFERRAL_SCREENS = ("exercise-safety", "phq2", "apnea")


def collate(store_read):
    """Collate the positive safety-screen referral flags for the doctor-visit display.

    Args:
        store_read (Callable): The instance-bound store read surface
            (`functools.partial(store.read, root=instance_root)`), mirroring the
            `router.summarize` `store_read` caller contract.

    Returns:
        (list) The screen names carrying a positive `referral::<screen>` flag, in the
        pinned screen order (a present item -> its screen; absent -> not). Read-only.
    """
    return [screen for screen in _REFERRAL_SCREENS if store_read(f"referral::{screen}")]
