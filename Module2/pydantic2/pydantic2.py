from pydantic import BaseModel

class User(BaseModel):
	name: str
	age: int

print(User(name="Alice", age=30))
print(User(name="Bob", age="25"))
print(User(name="Carol", age="hello"))
