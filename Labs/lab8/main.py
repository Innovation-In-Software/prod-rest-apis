"""
MD291 Lab (STARTER) - API Versioning & Deprecation Signaling
============================================================

This is the STARTER file - the one YOU edit. Right now only a bare v1 route
exists. Your job is to migrate to the current solution:

  1. Make the deprecated v1 route SIGNAL its deprecation with headers.
  2. BUILD the new current v2 route that replaces it.

Look for each  # TODO  marker and replace the  ____  blank with your own
code. The comments give you HINTS, not the answer.

There are 5 TODOs. After finishing, run the curl commands in the lab guide
and compare against the "You did it right if" table.

Really stuck? api_answer_key.py has the finished version.

Run it:
    pip install "fastapi[standard]"

Docs:  http://127.0.0.1:8000/docs
"""

from datetime import datetime, timezone
from email.utils import format_datetime

from fastapi import APIRouter, FastAPI, Response

app = FastAPI(title="Quote API")

# The date v1 stops working. After this, clients should be on v2.
# TODO 1: Set the sunset date to 01 January 2027 (UTC).
#         Hint: datetime(YEAR, MONTH, DAY, tzinfo=timezone.utc)
SUNSET = ____


# ===========================================================================
# v1 - DEPRECATED but still running during the overlap window
# ===========================================================================
v1 = APIRouter(prefix="/v1", tags=["v1 (deprecated)"])


@v1.get("/quote")
async def quote_v1(response: Response):
    # The route works, but right now it does NOT tell clients it's going away.
    # Add the three signaling headers so callers know to migrate.
    #
    # TODO 2: Announce the endpoint is deprecated.
    #         Hint: set the "Deprecation" header to the string "true".
    response.headers[____] = ____
    # TODO 3: Tell clients WHEN it will be removed.
    #         Hint: the "Sunset" header, formatted from SUNSET.
    #         Use format_datetime(SUNSET, usegmt=True) for a proper HTTP date.
    response.headers["Sunset"] = ____
    # TODO 4: Point clients to the replacement.
    #         Hint: the "Link" header. The value should reference the v2 path
    #         and mark it as the successor, e.g.
    #             </v2/quote>; rel="successor-version"
    response.headers["Link"] = ____
    return {"quote": "it was the best of times, it was the worst of times",
            "version": "v1"}


# ===========================================================================
# v2 - CURRENT version that replaces v1
# ===========================================================================
v2 = APIRouter(prefix="/v2", tags=["v2 (current)"])


# TODO 5: Build the current route. It should be a GET at /quote on the v2
#         router that returns the same quote as v1 but WITHOUT any deprecation
#         headers (v2 is current, not going away).
#         Hint: mirror quote_v1, drop the response headers, set version "v2".
@v2.get("/quote")
async def quote_v2():
    return ____


app.include_router(v1)
app.include_router(v2)