from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    q: str | None = None):
    ...
# GET /items?skip=0&limit=5&q=book
