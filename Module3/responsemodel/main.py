from pydantic import BaseModel

app = FastAPI()

# Full data model — includes password (stored internally)
class Item(BaseModel):
    name: str
    vendor: str
    price: float
    in_stock: bool = True
    password: str

# Response model — trims out password before sending back
class ItemPublic(BaseModel):
    name: str
    vendor: str
    price: float
    in_stock: bool

# In-memory "database"
items: list[Item] = []

# GET — return all items, filtered through ItemPublic
@app.get("/items", response_model=list[ItemPublic])
def list_items():
    return items