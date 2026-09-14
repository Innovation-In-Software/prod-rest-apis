from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}


@app.get("/subtract/{a}/{b}")
def subtract(a: int, b: int):
    return {"result": a - b}


@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    return {"result": a * b}


@app.get("/divide/{a}/{b}")
def divide(a: int, b: int):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}