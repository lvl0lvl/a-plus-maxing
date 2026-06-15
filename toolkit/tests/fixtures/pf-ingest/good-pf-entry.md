## PF-S7-03 (2026-06-12): Shipped an audit with no negative test

**Pattern:** Added a presence-check audit to the toolkit and marked the bead
done without a test that proves it goes RED on bad input.

**Root cause:** No pre-merge mechanical gate requiring a paired negative test for
every shipped audit.

**Detection mode:** user catch — the operator noticed the missing test in review.

**surfaced_by:** user

**Lesson:** Ship every audit with its negative test before it counts as enforcing.

**Anti-pattern to avoid:** Trusting that a green audit means the property holds
when the audit was never shown to fail on a violation.

**Recurrence:** First documented; recurrence_count = 1.
