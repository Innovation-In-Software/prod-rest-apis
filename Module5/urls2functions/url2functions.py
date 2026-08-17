from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def list_items():
    return [{"id": 1}]