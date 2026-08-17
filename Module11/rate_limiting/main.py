import time
from collections import defaultdict
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# --- Config ---
LIMIT = 5          # max requests allowed per window
WINDOW = 60        # window length in seconds

# --- In-memory store: client_ip -> (window_start, count) ---
# NOTE: fine for a demo; use Redis in production (see note below).
buckets: dict[str, tuple[float, int]] = defaultdict(lambda: (0.0, 0))


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client = request.client.host          # identify the caller (here: by IP)
    now = time.time()
    window_start, count = buckets[client]

    # Start a fresh window if the old one has expired
    if now - window_start >= WINDOW:
        window_start, count = now, 0

    count += 1
    buckets[client] = (window_start, count)

    reset_at = int(window_start + WINDOW)   # when the counter refills (unix ts)
    remaining = max(0, LIMIT - count)

    # Over the limit -> reject with 429 + Retry-After
    if count > LIMIT:
        retry_after = max(1, reset_at - int(now))
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"},
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(LIMIT),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_at),
            },
        )

    # Under the limit -> proceed, and attach the signal headers
    response: Response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(LIMIT)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_at)
    return response


@app.get("/ping")
async def ping():
    return {"message": "pong"}