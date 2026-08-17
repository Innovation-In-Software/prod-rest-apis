from fastapi import FastAPI, APIRouter, Response, HTTPException
from datetime import datetime, timezone

app = FastAPI(title="Hello API")

# ---------------------------------------------------------------------------
# v1 — RETIRED
# Past its sunset date. The endpoint still exists so clients get a clear,
# correct answer (410 Gone) instead of a confusing 404, but it no longer works.
# ---------------------------------------------------------------------------
v1 = APIRouter(prefix="/v1", tags=["v1 (retired)"])

@v1.get("/hello")
async def hello_v1():
    # 410 Gone = "this used to exist and is permanently removed."
    # We point the client at the replacement so migration is obvious.
    raise HTTPException(
        status_code=410,
        detail={
            "error": "This version has been retired.",
            "replacement": "/v2/hello",
            "sunset_date": "2026-01-01",
        },
    )

# ---------------------------------------------------------------------------
# v2 — CURRENT
# The supported version. Returns the real response.
# ---------------------------------------------------------------------------
v2 = APIRouter(prefix="/v2", tags=["v2 (current)"])

@v2.get("/hello")
async def hello_v2():
    return {"message": "Hello from v2", "version": "v2"}

app.include_router(v1)
app.include_router(v2)