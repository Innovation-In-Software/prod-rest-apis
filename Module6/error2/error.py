from enum import Enum
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# --- Slide 4: Stable, specific error codes (centralized) ---
class ErrorCode(str, Enum):
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"


# --- Slide 5: Structured exception carrying code + status + message ---
class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


# --- Slide 3: Standard error envelope (built once, in the handler) ---
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": [],
            }
        },
    )

@app.exception_handler(Exception)
async def unhandled_handler(request, exc):
    # log the real exception here
    return JSONResponse(
        status_code=500,
        content={"error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred.",
            "request_id": request.state.request_id,
        }},
    )

# --- Fake data store for the demo ---
ACCOUNTS = {
    "acc_100": {"balance": 500},
    "acc_200": {"balance": 0},
}


# --- Slide 2: Why it matters — routes raise clear, specific errors ---
@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    account = ACCOUNTS.get(account_id)
    if account is None:
        raise AppError(
            ErrorCode.ACCOUNT_NOT_FOUND,
            "No account exists with that ID.",
            status_code=404,
        )
    return {"account_id": account_id, "balance": account["balance"]}


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, amount: int):
    account = ACCOUNTS.get(account_id)
    if account is None:
        raise AppError(
            ErrorCode.ACCOUNT_NOT_FOUND,
            "No account exists with that ID.",
            status_code=404,
        )
    if amount > account["balance"]:
        raise AppError(
            ErrorCode.INSUFFICIENT_FUNDS,
            "Withdrawal amount exceeds the available balance.",
            status_code=409,
        )
    account["balance"] -= amount
    return {"account_id": account_id, "balance": account["balance"]}