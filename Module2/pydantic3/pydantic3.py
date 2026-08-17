from pydantic import BaseModel, ValidationError

class User(BaseModel):
	name: str
	age: int


print(User(name="Alice", age=30))
print(User(name="Bob", age="25"))

try:
	print(User(name="Carol", age="hello"))
except ValidationError as error:
	print(error)
