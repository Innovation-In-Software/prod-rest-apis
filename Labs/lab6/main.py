# main.py — FastAPI Lab: Error Handling & Request Tracing (starter)
#
# Run:  fastapi dev main.py
# Try:  http://127.0.0.1:8000/add?a=4&b=2
#       http://127.0.0.1:8000/divide?a=4&b=0     <-- currently crashes
#
# A small calculator API with four routes: add, subtract, multiply, divide.
# Everything below runs as-is EXCEPT the two things you will build:
#
#   TASK 1 (tracing):  a middleware that stamps every request with a unique ID,
#                      stashes it on request.state, and returns it as the
#                      X-Request-ID response header.
#
#   TASK 2 (errors):   handle divide-by-zero by raising AppError, and register
#                      an exception handler that returns the standard error
#                      envelope — including the correlated request_id.

import uuid

from enum import Enum

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# ---------------------------------------------------------------------------
# Error codes — machine-readable strings naming exactly what went wrong.
# (Provided for you. You'll use DIVIDE_BY_ZERO in Task 2.)
# ---------------------------------------------------------------------------
class ErrorCode(str, Enum):
    DIVIDE_BY_ZERO = "DIVIDE_BY_ZERO"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# ---------------------------------------------------------------------------
# Structured exception — carries code, message, and status together.
# (Provided for you. You'll raise this in Task 2.)
# ---------------------------------------------------------------------------
class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


# ---------------------------------------------------------------------------
# TASK 1 (request tracing): add an HTTP middleware named add_request_id that:
#   - mints a unique ID with str(uuid.uuid4())        (before the handler)
#   - stashes it on request.state.request_id          (before the handler)
#   - calls the route with call_next
#   - attaches it to the response as the "X-Request-ID" header  (after)
#   - returns the response
#
# Skeleton to complete:
#
# @app.middleware("http")
# async def add_request_id(request: Request, call_next):
#     ...
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# TASK 2 (exception handler): register a handler for AppError that returns a
# JSONResponse using the standard error envelope. Read the code, message, and
# status back off exc, and include the correlated ID from
# request.state.request_id so the client can quote it.
#
# Envelope shape:
#   {"error": {"code": ..., "message": ..., "request_id": ...}}
#
# Skeleton to complete:
#
# @app.exception_handler(AppError)
# async def app_error_handler(request: Request, exc: AppError):
#     ...
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# The four calculator routes.
# ---------------------------------------------------------------------------
@app.get("/add")
async def add(a: float, b: float):
    return {"operation": "add", "a": a, "b": b, "result": a + b}


@app.get("/subtract")
async def subtract(a: float, b: float):
    return {"operation": "subtract", "a": a, "b": b, "result": a - b}


@app.get("/multiply")
async def multiply(a: float, b: float):
    return {"operation": "multiply", "a": a, "b": b, "result": a * b}


@app.get("/divide")
async def divide(a: float, b: float):
    # TASK 2: when b == 0, raise AppError(ErrorCode.DIVIDE_BY_ZERO, ...) instead
    # of letting Python raise ZeroDivisionError and crash the response.
    return {"operation": "divide", "a": a, "b": b, "result": a / b}