from pydantic import BaseModel


class User(BaseModel):
	name: str
	age: int
	email: str


user = User(name="Ada", age="invalid", email="ada@example.com")
print(user)
