# main.py — FastAPI Lab: Middleware & Filtering (SOLUTION KEY)
#
# Run:  fastapi dev main.py
# Try:  http://127.0.0.1:8000/now

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

request_count = 0


# Internal model — still holds the secret token.
class TimeReading(BaseModel):
    timestamp: str
    token: str


# TASK 2: output model — no token, adds count. This is the filter.
class TimeReadingOut(BaseModel):
    timestamp: str
    count: int


# TASK 2: response_model=TimeReadingOut filters every response through the
# output model, so token is dropped and only timestamp + count go out.
@app.get("/now", response_model=TimeReadingOut)
async def get_now():
    reading = TimeReading(
        timestamp=datetime.now(timezone.utc).isoformat(),
        token="super-secret-do-not-leak",
    )
    # Build the returned object with the current count. token still present on
    # `reading`, but the response_model filter removes it on the way out.
    return TimeReadingOut(timestamp=reading.timestamp, count=request_count)


# TASK 1: middleware runs on every request.
@app.middleware("http")
async def count_requests(request, call_next):
    global request_count
    request_count += 1                                    # way IN
    print(f"Total requests: {request_count}")
    response = await call_next(request)                   # hand off to route
    response.headers["X-Request-Count"] = str(request_count)  # way OUT
    return response