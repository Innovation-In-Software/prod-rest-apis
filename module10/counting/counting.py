"""
FastAPI counter application.

  GET /even  ->  0, 2, 4, 6, ...   (starts at 0, +2 each call)
  GET /odd   ->  1, 3, 5, 7, ...   (starts at 1, +2 each call)

Simple logging: basicConfig is given the log file name directly.
An HTTP middleware runs on every request and writes the time to the log.

Then open http://127.0.0.1:8000/even and http://127.0.0.1:8000/odd
(refresh to increment), or the auto docs at http://127.0.0.1:8000/docs
"""

import logging
from datetime import datetime

from fastapi import FastAPI, Request

# Simple logging: just point basicConfig at the log file.
logging.basicConfig(filename="counter.log", level=logging.INFO)

app = FastAPI(title="Even / Odd Counter API", version="1.0")

# Counters persist between requests. even starts at 0, odd starts at 1.
even_count = 0
odd_count = 1


# Middleware runs on EVERY request and writes the current time to the log.
@app.middleware("http")
async def log_time(request: Request, call_next):
    logging.info("%s %s at %s", request.method, request.url.path, datetime.now())
    return await call_next(request)


@app.get("/even")
def get_even():
    """Return the next even number, then advance the counter by 2."""
    global even_count
    current = even_count
    even_count += 2
    logging.info("even count = %d", current)
    return {"even_count": current}


@app.get("/odd")
def get_odd():
    """Return the next odd number, then advance the counter by 2."""
    global odd_count
    current = odd_count
    odd_count += 2
    logging.info("odd count = %d", current)
    return {"odd_count": current}