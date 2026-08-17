"""
MD291 Lab (STARTER) - FastAPI Depends + Liveness/Readiness (no JWT)
===================================================================

This is the STARTER file - the one YOU edit. Look for each  # TODO  marker
and replace the  ____  blank below it with your own code. The comments give
you HINTS, not the answer - work it out from the hint, then test it.

There are 9 TODOs across 3 scenarios. After each scenario, run that
scenario's curl commands and compare against the "You did it right if" table
in the lab guide.

Really stuck on a blank? main_answer_key.py has the finished version.

Run it:
    pip install "fastapi[standard]"
    uvicorn main_starter:app --reload

Interactive docs (click the routes instead of using curl):
    http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI(title="Vault API")


# ---------------------------------------------------------------------------
# Fake "database" - an object with an on/off switch. DONE FOR YOU.
# Stands in for a real database so the readiness check has something to test.
# ---------------------------------------------------------------------------
class FakeDB:
    def __init__(self) -> None:
        self.connected = True


fake_db = FakeDB()


# ===========================================================================
# SCENARIO 1 - protect routes with one reusable check
# ===========================================================================
API_KEY = "let-me-in"


def require_api_key(x_api_key: str = Header(default="")) -> str:
    """Dependency: check the X-API-Key header."""
    # TODO 1a: Write the condition that is TRUE when the key is wrong or
    #          missing. Hint: compare x_api_key against API_KEY.
    if ____:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    # TODO 1b: Hand the key back to the caller on success.
    #          Hint: which variable holds the key that was passed in?
    return ____


@app.get("/vault")
# TODO 2: Make this route run require_api_key BEFORE the handler.
#         Hint: the parameter's default value is Depends(<the check function>).
async def read_vault(api_key: str = ____):
    return {"secret": "the treasure is behind the third door"}


@app.get("/vault/status")
# TODO 3: Protect this route the SAME way as /vault - reuse the same check.
async def vault_status(api_key: str = ____):
    return {"vault": "locked", "guards": 3}


# ===========================================================================
# SCENARIO 2 - two kinds of health check
# ===========================================================================
def check_db() -> "FakeDB":
    """Dependency: only succeed when the database is connected."""
    # TODO 4a: Write the condition that is TRUE when the database is DOWN.
    #          Hint: fake_db has a .connected flag (True = up, False = down).
    if ____:
        raise HTTPException(status_code=503, detail="Database unavailable")
    # TODO 4b: Return the database object when it's healthy.
    #          Hint: which variable is the fake database?
    return ____


@app.get("/health/live")
async def live():
    """Liveness: 'is the process alive?' Has NO dependency on purpose, so it
    keeps answering 200 even when the database is down."""
    # TODO 5: Return a small dict that signals the app is alive.
    #         Hint: something like {"status": "..."} - you choose the value.
    return ____


@app.get("/health/ready")
# TODO 6: Make readiness actually check the database before it answers.
#         Hint: same Depends(...) pattern you used in Scenario 1, but with
#         the database check function.
async def ready(db: "FakeDB" = ____):
    return {"status": "ready"}


@app.get("/data")
# TODO 7: This real route should share readiness's fate - reuse the SAME
#         database check here so it also fails when the DB is down.
async def read_data(db: "FakeDB" = ____):
    return {"rows": [1, 2, 3]}


@app.post("/admin/toggle-db")
async def toggle_db():
    """Flip the fake DB between connected and disconnected. DONE FOR YOU."""
    fake_db.connected = not fake_db.connected
    return {"connected": fake_db.connected}


# ===========================================================================
# SCENARIO 3 - use several checks on one route
# ===========================================================================
def get_pagination(skip: int = 0, limit: int = 10) -> dict:
    """Dependency: read optional skip/limit values from the URL. DONE FOR YOU."""
    return {"skip": skip, "limit": limit}


def require_admin_key(api_key: str = Depends(require_api_key)) -> str:
    """A dependency that USES another dependency (nested).
    require_api_key runs first; this then adds an admin check."""
    # TODO 8: Write the condition that is TRUE when the caller is NOT an admin.
    #         Hint: in this lab the admin key is just the API_KEY itself.
    if ____:
        raise HTTPException(status_code=403, detail="Admins only")
    return api_key


@app.get("/reports")
async def list_reports(
    # TODO 9: Stack three checks on this one route by filling each blank with
    #         Depends(<function>). Match each name to the right function:
    #           page  -> the pagination reader
    #           admin -> the admin check
    #           db    -> the database check
    page: dict = ____,
    admin: str = ____,
    db: "FakeDB" = ____,
):
    return {"reports": ["q1", "q2", "q3"], "page": page}