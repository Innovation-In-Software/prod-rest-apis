import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_timing(request: Request, 
                     call_next):
    start = time.time()  
    response = await call_next(request)  
    duration = time.time()
    print(
        f"{request.method} {request.url.path} "
        f"took {duration:.3f}s"
    )
    return response

@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/")
async def cool():
    return {"message": "hello"}
