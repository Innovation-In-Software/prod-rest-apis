from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)   # price must be a number greater than 0

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}