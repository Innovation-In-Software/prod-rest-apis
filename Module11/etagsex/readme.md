# ETags in FastAPI — Sample Code

A minimal FastAPI app showing the two things ETags are for: **caching** (skip
re-downloading data you already have) and **concurrency** (don't let one save
silently overwrite another). Here the ETag is just the product's version number.

## What's an ETag?

An ETag ("entity tag") is a **version stamp** the server attaches to a piece of
data. Every time the data changes, the stamp changes. The client holds onto it
and sends it back later to ask the server a question — either *"has this
changed?"* (to skip a download) or *"is this still the version I edited?"* (to
avoid clobbering someone else's work).

## How this sample works

Here the ETag is just the version number.

- **GET** hands back the version in the `ETag` header. If the client sends it
  back via `If-None-Match` and it still matches, it gets `304 Not Modified` —
  reuse your copy.
- **PUT** requires `If-Match`. If the version you're editing from doesn't match
  the current one, you get `412` instead of silently overwriting someone else's
  change. A successful save bumps the version, so old ETags stop working.

| Request | Header sent | If it matches | If it doesn't match |
|---------|-------------|---------------|---------------------|
| `GET`   | `If-None-Match` | `304 Not Modified` (no body — reuse your copy) | `200 OK` with the fresh data + new `ETag` |
| `PUT`   | `If-Match`      | Save succeeds, version bumps | `412 Precondition Failed` (fetch latest, retry) |

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install fastapi uvicorn
```

## Run it

```bash
fastapi dev main.py
```

Then open the interactive docs at http://127.0.0.1:8000/docs

## Try it with curl

**1. Fetch the product — note the `ETag` header in the response**

```bash
curl -i http://127.0.0.1:8000/product
```

You'll see `ETag: 1` in the response headers.

**2. Caching — send the ETag back, get `304`**

```bash
curl -i http://127.0.0.1:8000/product -H "If-None-Match: 1"
```

Version still 1, so you get `304 Not Modified` with no body. Nothing to
re-download — keep the copy you already have.

**3. Safe update — send the current version, it succeeds**

```bash
curl -i -X PUT "http://127.0.0.1:8000/product?price=9.99" -H "If-Match: 1"
```

Version matched, so the price updates and the version bumps to `2`.

**4. Stale update — send an old version, get `412`**

```bash
curl -i -X PUT "http://127.0.0.1:8000/product?price=5.00" -H "If-Match: 1"
```

The version is now `2`, but you sent `1` — so the save is rejected with
`412 Precondition Failed`. This is the guard against the "lost update" problem:
you were editing an out-of-date copy, so the server makes you fetch the latest
and try again instead of wiping out whoever saved before you.

## The "lost update" problem this prevents

Without `If-Match`:

1. Alice fetches the product (version 1).
2. Bob fetches the same product (version 1).
3. Alice saves a price change → version becomes 2.
4. Bob saves *his* change, still based on version 1 → **Alice's change is gone.**

With `If-Match`, Bob's save in step 4 sends `If-Match: 1`, the current version is
already `2`, the stamps don't match, and Bob gets a `412`. He fetches the latest,
re-applies his edit on top of Alice's, and no work is lost.

## Notes for real-world use

- **Real ETags aren't usually a plain integer.** A common approach is to hash
  the data (e.g. an MD5 of the JSON) so the stamp reflects the *content* — any
  change flips it automatically, no manual version counter to maintain.
- **ETags are wrapped in quotes** by the HTTP spec (e.g. `ETag: "abc123"`). This
  sample keeps them unquoted for simplicity; add quotes if you want to be strict.
- **`If-Match` vs `If-None-Match`** are opposites on purpose: `If-Match` means
  "only act if it *still matches*" (for safe writes); `If-None-Match` means
  "only send data if it *doesn't* match what I have" (for caching).
- **304 and 412 are the whole point.** They let the client and server cooperate
  without re-sending data or overwriting each other — cheaper traffic and safer
  edits, for the cost of one header.