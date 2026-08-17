from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float          # a number is required here


@app.post("/items")
async def create(item: Item):
    # This line only runs if validation passed
    return {"received": item}