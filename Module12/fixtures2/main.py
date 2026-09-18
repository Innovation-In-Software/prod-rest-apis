from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    role: str

# A tiny stand-in for a real user database: token -> user
_FAKE_TOKENS = {
    "alice-token": User(name="Alice", role="admin"),
    "bob-token": User(name="Bob", role="user"),
}

def get_current_user(authorization: str | None = Header(default=None)) -> User:
    # normally: read the token, verify it, look up the user in the DB
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = _FAKE_TOKENS.get(authorization)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/admin")
def admin_panel(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    return {"secret": "data"}