"""
MD291 Lab (ANSWER KEY) - API Versioning & Deprecation Signaling
===============================================================

The completed reference solution. Students should attempt api_starter.py
first and use this only to check their work.

Two routes:
  GET /v1/quote    - DEPRECATED but still running during the overlap window.
                     Sends Deprecation / Sunset / Link headers pointing to v2.
                     Sunset date: 01 Jan 2027.
  GET /v2/quote    - CURRENT version that replaces v1. No deprecation headers.

Run it:
    pip install "fastapi[standard]"

Docs:  http://127.0.0.1:8000/docs
"""

from datetime import datetime, timezone
from email.utils import format_datetime

from fastapi import APIRouter, FastAPI, Response

app = FastAPI(title="Quote API")

# The date v1 stops working. After this, clients should be on v2.
SUNSET = datetime(2027, 1, 1, tzinfo=timezone.utc)


# ===========================================================================
# v1 - DEPRECATED but still running during the overlap window
# ===========================================================================
v1 = APIRouter(prefix="/v1", tags=["v1 (deprecated)"])


@v1.get("/quote")
async def quote_v1(response: Response):
    # Deprecation: true   -> "this endpoint is deprecated"
    # Sunset: <date>       -> "it will be removed on this date"
    # Link                 -> points clients to the replacement
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = format_datetime(SUNSET, usegmt=True)
    response.headers["Link"] = '</v2/quote>; rel="successor-version"'
    return {"quote": "it was the best of times, it was the worst of times",
            "version": "v1"}


# ===========================================================================
# v2 - CURRENT version that replaces v1
# ===========================================================================
v2 = APIRouter(prefix="/v2", tags=["v2 (current)"])


@v2.get("/quote")
async def quote_v2():
    return {"quote": "it was the best of times, it was the worst of times",
            "version": "v2"}


app.include_router(v1)
app.include_router(v2)
