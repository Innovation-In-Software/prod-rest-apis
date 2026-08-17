from datetime import datetime, timedelta, timezone

# PyJWT library - handles encoding (creating) and decoding (verifying) JWTs.
# The import name is "jwt" even though the package installed is "pyjwt".
import jwt

# Depends       -> tells FastAPI "run this function first and inject its result"
# FastAPI       -> the app class
# HTTPException -> the way to return an error response (like 401 Unauthorized)
from fastapi import Depends, FastAPI, HTTPException

# HTTPBearer                  -> a security scheme that reads the "Authorization: Bearer <token>" header
# HTTPAuthorizationCredentials -> the object HTTPBearer hands back; holds the scheme + the token string
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# The secret key used to SIGN and VERIFY tokens. Only the server knows it.
# If someone knows this, they can forge valid tokens. Use a long random value
# from an environment variable in real code - never hardcode it.
SECRET = "change-me"

# The signing algorithm. HS256 = HMAC + SHA-256 (symmetric: same secret signs and verifies).
ALGORITHM = "HS256"

# Create the web application.
app = FastAPI()

# Create the security scheme object. This one instance does two jobs:
#   1. Pulls the token out of the Authorization header on incoming requests.
#   2. Adds the "Authorize" button to the /docs Swagger UI.
security = HTTPBearer()


def create_token(username: str) -> str:
    """Build and sign a JWT for the given user."""
    payload = {
        # "sub" (subject) = who the token is about. A registered JWT claim.
        "sub": username,
        # "exp" (expiration) = when the token stops being valid.
        # PyJWT reads this automatically and rejects the token after this time.
        # timezone.utc keeps the time unambiguous across servers/regions.
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    # Sign the payload with the secret. Returns a compact string:
    # header.payload.signature  (three base64 parts joined by dots).
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency that protects an endpoint.

    Depends(security) means: before this function runs, FastAPI calls the
    HTTPBearer scheme, which reads the Authorization header. If the header is
    missing or malformed, HTTPBearer itself raises 401 - so by the time we get
    here, `creds` is guaranteed to hold a token string in creds.credentials.
    """
    try:
        # Verify the signature AND the expiration in one step.
        # If either fails, PyJWT raises an exception. On success we get the
        # decoded payload dict back (e.g. {"sub": "alice", "exp": ...}).
        return jwt.decode(creds.credentials, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        # PyJWTError is the base class for all PyJWT errors (bad signature,
        # expired token, malformed token, etc.), so this one catch covers them all.
        # Returning 401 tells the client the credentials were rejected.
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/login")
def login():
    """
    Demo endpoint that hands out a token. In a real app you'd first check a
    username/password here, and only issue a token if they're correct.
    """
    return {"token": create_token("alice")}


@app.get("/protected")
# The magic line: payload = Depends(verify_token).
# FastAPI runs verify_token first. If it raises 401, this handler never runs.
# If it succeeds, its return value (the decoded payload) is injected as `payload`.
def protected(payload: dict = Depends(verify_token)):
    """Only reachable with a valid, unexpired token."""
    # payload["sub"] is the username we stored when creating the token.
    return {"message": f"Hello {payload['sub']}"}