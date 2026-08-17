from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. Create the limiter, keyed by client IP
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# 2. Register the limiter and its 429 handler with the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# 3. Apply a limit to an endpoint with a decorator.
#    NOTE: the endpoint MUST accept `request: Request` or slowapi can't hook in.
@app.get("/ping")
@limiter.limit("5/minute")
async def ping(request: Request):
    return {"message": "pong"}