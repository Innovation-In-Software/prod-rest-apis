# main.py — FastAPI Lab: Middleware & Filtering (starter)
#
# Run:  fastapi dev main.py
# Try:  http://127.0.0.1:8000/now
#
# You will:
#   1. Complete a middleware that counts requests and logs the running total.
#   2. Add a filtered response_model so the model's secret token is never sent.

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request counter — already provided for you. Use it in your middleware (Task 1).
request_count = 0


# ---------------------------------------------------------------------------
# The model returned by the route.
#
# `token` is a secret and must NEVER appear in the response body.
# `timestamp` is the one field you start with.
#
# LAB TASK 2 (filtering): add a `count` field to the RESPONSE model so the
# running request total is returned to the client — WITHOUT exposing `token`.
# Hint: create a separate output model, then set response_model=... on the
#       route (see slides 16–17).
# ---------------------------------------------------------------------------
class TimeReading(BaseModel):
    timestamp: str
    token: str   # secret — should not leave the server


@app.get("/now")
async def get_now():
    reading = TimeReading(
        timestamp=datetime.now(timezone.utc).isoformat(),
        token="super-secret-do-not-leak",
    )
    # Right now this returns the whole model — including token. Fix that in Task 2.
    return reading


# ---------------------------------------------------------------------------
# LAB TASK 1 (middleware): complete the function below.
#
#   - On the way IN:  increment request_count and log the new total.
#   - Hand off to the route with call_next and capture the response.
#   - On the way OUT: attach the total as an "X-Request-Count" header.
#   - Return the response.
# ---------------------------------------------------------------------------
@app.middleware("http")
async def count_requests(request, call_next):
    global request_count
    # your code here
