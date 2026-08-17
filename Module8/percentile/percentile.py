from fastapi import FastAPI, Request
from statistics import quantiles
import time

app = FastAPI()
durations = []  # stored in memory for demo purposes only

@app.middleware("http")
async def track_latency(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    durations.append(elapsed_ms)
    return response

@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/metrics")
async def metrics():
    if len(durations) < 2:
        return {"count": len(durations)}
    # quantiles(n=100) splits data into 100 buckets, giving p1..p99
    p = quantiles(durations, n=100)
    return {
        "count": len(durations),
        "p50_ms": round(p[49], 2),
        "p95_ms": round(p[94], 2),
        "p99_ms": round(p[98], 2),
    }