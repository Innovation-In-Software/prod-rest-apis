from fastapi import FastAPI, APIRouter, Response
from email.utils import format_datetime
from datetime import datetime, timezone
from fastapi.responses import RedirectResponse


SUNSET = datetime(2026, 1, 1, tzinfo=timezone.utc)
app=FastAPI()

# ---------------------------------------------------------------------------
# v1 — DEPRECATED but still running during the overlap window
# ---------------------------------------------------------------------------
redwolf = APIRouter(prefix="/v2", tags=["v1 (deprecated)"])

@redwolf.get("/hello")
async def hello_v1(response: Response):
    # Deprecation: true  -> "this endpoint is deprecated"
    # Sunset: <date>      -> "it will be removed on this date"
    # Link                -> points clients to the replacement
    response.headers["Deprecation"] = "@1735689600"
    response.headers["Sunset"] = format_datetime(SUNSET, usegmt=True)
    response.headers["Link"] = '</v2/hello>; rel="successor-version"'
    return {"message": "Hello from v1", "version": "v1"}

# ---------------------------------------------------------------------------
# v2 — CURRENT
# ---------------------------------------------------------------------------
firestorm = APIRouter(prefix="/v2", tags=["v2 (current)"])

@firestorm.get("/hello")
async def hello_v2():
    return {"message": "Hello from v2", "version": "v2"}


@app.get("/hello")
async def hello_default():
    return RedirectResponse(url="/v2/hello")

app.include_router(redwolf)
app.include_router(firestorm)