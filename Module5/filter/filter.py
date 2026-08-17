from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    password: str


class ItemOut(BaseModel):
    id: int
    name: str
    # note: no password field


@app.post("/items", response_model=ItemOut)
async def create(item: Item):
    return save(item)


# In-memory store standing in for a real database
_db = {}
_counter = 0

def save(item: Item):
    global _counter
    _counter += 1
    record = {
        "id": _counter,
        "name": item.name,
        "price": item.price,
        "password": item.password,
    }
    _db[_counter] = record
    return record