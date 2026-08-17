from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Items API")

# In-memory "database"
items: dict[int, dict] = {}
next_id = 1


class Item(BaseModel):
    name: str
    price: float


@app.get("/items")
def list_items():
    return list(items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items[next_id] = new_item
    next_id += 1
    return new_item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]