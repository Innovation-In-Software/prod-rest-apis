"""
MD291 Lab (ANSWER KEY) - FastAPI Depends + Liveness/Readiness (no JWT)
=====================================================================

This is the completed reference solution for the lab. Students should attempt
main_starter.py first and use this only to check their work. It includes all
three scenarios: the API-key gate, readiness via a shared dependency, and the
stacked/nested dependencies on /reports.

Run it:
    pip install "fastapi[standard]"
    uvicorn main_answer_key:app --reload

Interactive docs:
    http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI(title="Vault API")


# ---------------------------------------------------------------------------
# Fake "database" - just an object with an on/off switch we can toggle at
# runtime. Stands in for a real DB connection so readiness has something real
# to check.
# ---------------------------------------------------------------------------
class FakeDB:
    def __init__(self) -> None:
        self.connected = True


fake_db = FakeDB()


# ===========================================================================
# SCENARIO 1 - a simple API-key gate, injected with Depends
# ===========================================================================
# require_api_key runs before any handler that depends on it. If the header is
# missing or wrong, it raises 401 and the handler never runs. Attach it to as
# many routes as you like - that is the "one dependency, reused everywhere"
# point from the slides, minus the JWT.

API_KEY = "let-me-in"


def require_api_key(x_api_key: str = Header(default="")) -> str:
    """Dependency: verify the X-API-Key header. Returns the key on success."""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key


@app.get("/vault")
async def read_vault(api_key: str = Depends(require_api_key)) -> dict:
    """Protected route. Only reachable with a correct X-API-Key header."""
    return {"secret": "the treasure is behind the third door"}


@app.get("/vault/status")
async def vault_status(api_key: str = Depends(require_api_key)) -> dict:
    """A SECOND protected route - same dependency, zero extra work."""
    return {"vault": "locked", "guards": 3}


# ===========================================================================
# SCENARIO 2 - readiness THROUGH Depends (Option B)
# ===========================================================================
# check_db is a dependency that fails with 503 when the fake DB is "down".
# We inject it into BOTH the readiness probe AND a business route, so toggling
# the DB off takes them both down together - while liveness stays up.


def check_db() -> FakeDB:
    """Dependency: only succeeds when the database is connected."""
    if not fake_db.connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return fake_db


@app.get("/health/live")
async def live() -> dict:
    """Liveness: is the process alive? Never touches dependencies."""
    return {"status": "ok"}


@app.get("/health/ready")
async def ready(db: FakeDB = Depends(check_db)) -> dict:
    """Readiness: can we serve traffic? Fails 503 when the DB is down."""
    return {"status": "ready"}


@app.get("/data")
async def read_data(db: FakeDB = Depends(check_db)) -> dict:
    """A business route reusing the SAME check_db dependency as readiness."""
    return {"rows": [1, 2, 3]}


@app.post("/admin/toggle-db")
async def toggle_db() -> dict:
    """Flip the fake DB between connected and disconnected, for testing."""
    fake_db.connected = not fake_db.connected
    return {"connected": fake_db.connected}


# ===========================================================================
# SCENARIO 3 - stacked and nested dependencies on one route
# ===========================================================================
# A handler can depend on several things at once and still stay focused on
# business logic. get_pagination parses shared query params; require_admin_key
# is a SECOND dependency that itself depends on require_api_key (nested).


def get_pagination(skip: int = 0, limit: int = 10) -> dict:
    """Dependency: parse shared pagination query params."""
    return {"skip": skip, "limit": limit}


def require_admin_key(api_key: str = Depends(require_api_key)) -> str:
    """Dependency that DEPENDS ON another dependency (nested).

    require_api_key runs first (must pass the API key), then this adds a
    second condition: the key must be the admin key.
    """
    if api_key != API_KEY:  # in this lab the same key doubles as admin
        raise HTTPException(status_code=403, detail="Admins only")
    return api_key


@app.get("/reports")
async def list_reports(
    page: dict = Depends(get_pagination),
    admin: str = Depends(require_admin_key),
    db: FakeDB = Depends(check_db),
) -> dict:
    """Three stacked dependencies: pagination + nested admin check + DB check.
    The handler body stays tiny - all the guarding happens in the deps."""
    return {"reports": ["q1", "q2", "q3"], "page": page}