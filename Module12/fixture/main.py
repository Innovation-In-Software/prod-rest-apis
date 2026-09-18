from fastapi import FastAPI

app = FastAPI()
items = {}

@app.post("/items/{name}")
def create_item(name: str):
    items[name] = {"name": name}
    return items[name]

@app.get("/items/{name}")
def read_item(name: str):
    return items.get(name, {"error": "not found"})