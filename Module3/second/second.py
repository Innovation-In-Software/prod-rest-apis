from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Donis Greatest API")

# Pydantic model — defines the shape of an Item
class Item(BaseModel):
    name: str
    vendor: str
    price: float
    in_stock: bool = True        

# In-memory "database"
items: list[Item] = []

# GET — return all items
@app.get("/items")  # abstracting from the plumbing
def list_items():
    return items

# POST — add a new item 
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item added", "item": item}