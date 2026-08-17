Here's a complete, runnable FastAPI application demonstrating Cache-Control across the common scenarios. I'll give you the full file, then walk through what each part teaches.

python
from fastapi import FastAPI, Response, Request
from datetime import datetime, timezone

app = FastAPI()


# ---------------------------------------------------------------------------
# 1. Aggressive caching — slow-changing PUBLIC data
#    A product catalog rarely changes minute to minute, so let anyone
#    (browsers AND shared caches) keep it for an hour.
# ---------------------------------------------------------------------------
@app.get("/products")
async def list_products(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"  # 1 hour
    return {
        "products": [
            {"id": 1, "name": "Coffee Mug", "price": 12.99},
            {"id": 2, "name": "Tea Kettle", "price": 34.50},
        ]
    }


# ---------------------------------------------------------------------------
# 2. No caching — SENSITIVE, always-live data
#    A bank balance must never be served from a saved copy. `no-store`
#    means: don't keep this anywhere, ever.
# ---------------------------------------------------------------------------
@app.get("/account/balance")
async def balance(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return {"balance": 4820.55, "as_of": datetime.now(timezone.utc).isoformat()}


# ---------------------------------------------------------------------------
# 3. Private caching — user-specific but cacheable briefly
#    A user's profile can sit in THEIR browser for 5 minutes, but shared
#    caches must not keep it (or one user could see another's data).
# ---------------------------------------------------------------------------
@app.get("/me/profile")
async def my_profile(response: Response):
    response.headers["Cache-Control"] = "private, max-age=300"  # 5 minutes
    return {"user": "donis", "plan": "pro"}


# ---------------------------------------------------------------------------
# 4. Must-revalidate — keep a copy, but check before trusting it
#    `no-cache` is misleadingly named: it DOES store a copy, but forces
#    the client to ask the server "is my copy still good?" before reuse.
# ---------------------------------------------------------------------------
@app.get("/news/headline")
async def headline(response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return {"headline": "Markets steady as trading opens"}


# ---------------------------------------------------------------------------
# 5. Blanket policy via middleware — one rule for many routes
#    Cache every /static/* asset for a full day without repeating
#    the header on each endpoint.
# ---------------------------------------------------------------------------
@app.middleware("http")
async def cache_static_assets(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "public, max-age=86400"  # 1 day
    return response


@app.get("/static/logo")
async def logo():
    return {"file": "logo.png", "note": "cached by middleware for 24h"}