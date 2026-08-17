app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items = {1: Item(name="widget", price=9.99)}

@app.get('/items/{id}')
def get_item(id: int) -> Item:
    if id not in items:
        raise HTTPException(status_code=404, 
            detail="No item with that ID exists")
    return items[id]