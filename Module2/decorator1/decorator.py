def my_decorator(func):

	def wrapper():
		print("Before the function runs")
		func()
		print("After the function runs")
	return wrapper

@my_decorator
def greet():
	print("Hello!")

greet()
