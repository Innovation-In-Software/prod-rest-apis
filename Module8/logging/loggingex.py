from fastapi import FastAPI, Request
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response

@app.get("/")
def hello():
    return {"message": "Hello"}

@app.get("/answer")
def theanswer():
    return {"message": "42"}

@app.get("/football")
def bestfootballteam():
    return {"message": "Cowboys"}