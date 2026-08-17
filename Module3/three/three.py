from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
)

# GET — return all items
@app.get("/")
def hello():
    return JSONResponse("Hello, World!") 
