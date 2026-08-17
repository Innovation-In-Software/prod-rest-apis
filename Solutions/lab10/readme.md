# Scenario A — The Checkout API · Answer Key

## Extracted requirements, tiers, and ratings

| # | Requirement | Tier | Rating | Why |
|---|-------------|------|--------|-----|
| 1 | Core purpose works — processes a valid order and charges the card | Tier 1 | Pass | Demonstrated repeatedly, works reliably |
| 2 | Authentication protects all sensitive endpoints | Tier 1 | Fail | Login/order endpoints are protected, but the "apply coupon" endpoint skips the token check — an auth bypass |
| 3 | Handles errors without crashing or corrupting data | Tier 1 | Fail | Processor timeout returns 500 and leaves the order half-charged (card charged, no order) — data corruption |
| 4 | You can tell whether the service is up or down | Tier 1 | Pass | Health endpoint accurately reports up/down |
| 5 | Someone is alerted when the service goes down | Tier 1 | Pass | Fire-drill confirmed the on-call alert fires |
| 6 | Tests catch problems before customers do (meaningful coverage) | Tier 2 | Partial | Happy-path tests pass, but none for declined cards or timeouts |
| 7 | API is documented (OpenAPI spec complete) | Tier 2 | Partial | 5 of 8 endpoints documented; 3 missing |
| 8 | Retry-with-backoff wrapper around the payment processor | Tier 3 | Fail (not built) | Scoped but never built; polish/resilience extra |

**Completed requirements:** #1, #4, and #5 are done (Tier 1 Passes). Partial credit exists on #6 and #7.

## Release verdict: NO — cannot ship tomorrow

The release gate is Tier 1, and every Tier 1 item must pass with no exceptions. Two Tier 1 items fail:

- **#2 (auth bypass on the coupon endpoint)** — a security hole; sensitive functionality reachable by anyone with the URL.
- **#3 (half-charged order on timeout)** — error handling that corrupts data and charges customers without recording an order.

Either one alone stops the launch; both are present. No amount of strength elsewhere overrides a hard Tier 1 failure.

## What each remaining item means for the decision

- **Tier 2 items (#6 test coverage, #7 documentation)** are real gaps but do **not** block release. They may be deferred only with a **conscious, visible sign-off**, and once deferred they become **technical debt** — the healthy, deliberate kind the tiered model exists to make visible. Each Partial must name what's left (write tests for declined-card and timeout paths; document the three missing endpoints) so it becomes a tracked action item.
- **Tier 3 item (#8 retry-with-backoff)** can be **dropped freely** — no ceremony, no sign-off — since time is short.

## Bottom line

Fix #2 and #3 to clear the gate, then re-assess. The Tier 2 gaps can ship as recorded technical debt with sign-off; the Tier 3 wrapper can wait.