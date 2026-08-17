# no hint — just a label
age = 30

# hinted — 'age is an int'
age: int = 30
name: str = "Ada"

print(f"{name} is {age} years old.")

# function with a type hint

def read_item(item_id: int):
    return {"id": item_id}
