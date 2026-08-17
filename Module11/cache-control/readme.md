# Cache-Control in FastAPI — Implementation Guide

A small, teaching-focused FastAPI app that demonstrates how to set the
`Cache-Control` header correctly across the situations you actually meet in
production: aggressively cacheable public data, sensitive data that must never
be stored, user-specific data, data that must be revalidated, and a blanket
policy applied through middleware.

---

## Quick start

```bash
pip install "fastapi[standard]"
fastapi dev main.py
```

Then inspect the header on any endpoint (the `-i` flag prints response headers):

```bash
curl -i http://127.0.0.1:8000/products
```

You should see the rule you set come back on the response, e.g.:

```
Cache-Control: public, max-age=3600
```

---

## How each endpoint maps to a real decision

The whole point of `Cache-Control` is matching the *rule* to the *nature of the
data*. Each endpoint below represents a different, common decision.

### `/products` — `public, max-age=3600`

Harmless, slow-changing data that everyone sees the same way, so cache it
aggressively and let shared caches help too. This is the big performance win:
the answer is served from a nearby copy instead of hitting the server every
time.

### `/account/balance` — `no-store`

The opposite extreme: sensitive and always-live, so it must never be saved
anywhere. When in doubt, this is the safe default — you can always loosen a rule
later, but a leaked or stale balance is a real problem.

### `/me/profile` — `private, max-age=300`

The important distinction here is `private` vs `public`: this data is fine to
keep, but *only* in the individual user's browser. A shared cache holding it
could serve one person's profile to another — a privacy bug, not just a
performance one.

### `/news/headline` — `no-cache`

The most commonly misunderstood directive. It does **not** mean "don't cache" —
it means "keep a copy, but always check with the server before reusing it."
Good for data that usually stays the same but occasionally changes and must
never be shown stale.

### `/static/logo` — set by middleware

Shows how to apply one blanket rule (cache assets for a day) across many routes
without repeating the header on each endpoint.

---

## The directives at a glance

| Directive | Meaning | Typical use |
|---|---|---|
| `public` | Any cache may store it | Shared, non-personalized data |
| `private` | Only the end user's browser may store it | User-specific data |
| `no-store` | Never save it anywhere | Sensitive or always-live data |
| `max-age=N` | Fresh for N **seconds**, then recheck | Almost everything cacheable |
| `no-cache` | May store, but must revalidate before reuse | Rarely-changing but must-be-fresh data |

### `max-age` cheat sheet (it's always in seconds)

The single biggest source of confusion. There are no minutes or hours — only
seconds.

| You want | Value |
|---|---|
| 1 minute | `max-age=60` |
| 5 minutes | `max-age=300` |
| 1 hour | `max-age=3600` |
| 1 day | `max-age=86400` |
| 1 week | `max-age=604800` |

---

## Practical tips

- **Start strict, loosen deliberately.** Default new endpoints to `no-store`,
  then relax to a cached rule only once you're sure a saved copy stays
  trustworthy. It's far safer to under-cache than to leak or stale data.

- **Match `max-age` to how often the data actually changes.** This one number
  is the heart of every caching decision. Too high and users see stale info;
  too low and you throw away the performance benefit. There's no universal right
  answer — it's a per-endpoint judgment call, which is exactly why the *server*
  makes it.

- **`private` is about privacy, not performance.** Any data tied to a specific
  logged-in user should be `private` (or `no-store`), never `public` — otherwise
  a shared cache between the user and your server could hand one person's data
  to someone else.

- **`no-cache` and `no-store` are not the same thing.** `no-store` keeps no copy
  at all. `no-cache` *does* keep a copy but forces a check-in with the server
  before reuse. The names are misleading; when you mean "never save this," you
  want `no-store`.

- **Use middleware for blanket policies, per-endpoint headers for exceptions.**
  A middleware rule ("cache all `/static/*` for a day") keeps things DRY, while
  individual endpoints can still override it when their data is special.

- **Anything with a personalized or authenticated response should not be
  `public`.** Search results tied to a user, dashboards, account pages, and
  API responses that vary by token all belong in `private` or `no-store`.

- **Caching also improves resilience, not just speed.** A valid cached copy can
  keep serving users during a brief server hiccup — a quiet reliability bonus on
  top of the performance and cost savings.

- **Verify with `curl -i` (or your browser's dev tools).** Don't assume the
  header is set — look at it. Seeing the actual `Cache-Control` line on the
  response is the fastest way to catch a typo or a rule that didn't apply.

---

## A note on timestamps

Where responses include a time (e.g. `as_of` on the balance endpoint), serialize
it in UTC using ISO 8601 so every client can parse it unambiguously:

```python
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()   # e.g. 2026-08-11T14:30:00+00:00
```

Avoid `datetime.utcnow()` — it's deprecated in modern Python and produces a
"naive" timestamp with no timezone attached, which is a classic source of
off-by-hours bugs.