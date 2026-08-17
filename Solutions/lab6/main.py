# main.py — FastAPI Lab: Error Handling & Request Tracing (SOLUTION KEY)
#
# Run:  fastapi dev main.py

import uuid

from enum import Enum

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class ErrorCode(str, Enum):
    DIVIDE_BY_ZERO = "DIVIDE_BY_ZERO"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


# TASK 1: request tracing middleware — mint an ID, stash it, return it.
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())              # before: mint the ID
    request.state.request_id = request_id       # before: stash for handlers
    response = await call_next(request)         # the route runs here
    response.headers["X-Request-ID"] = request_id  # after: send it back
    return response


# TASK 2: exception handler — standard envelope, with the correlated ID.
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {
            "code": exc.code,
            "message": exc.message,
            "request_id": request.state.request_id,
        }},
    )


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
    # TASK 2: guard the divide-by-zero and raise a structured error.
    if b == 0:
        raise AppError(
            ErrorCode.DIVIDE_BY_ZERO,
            "Cannot divide by zero.",
            status_code=400,
        )
    return {"operation": "divide", "a": a, "b": b, "result": a / b}