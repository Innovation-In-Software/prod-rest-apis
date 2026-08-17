class CountCalls:
	def __init__(self, func):
		self.func = func
		self.count = 0

	def __call__(self, *args, **kwargs):
		self.count += 1
		print(f"Call #{self.count} of {self.func.__name__}")
		return self.func(*args, **kwargs)

@CountCalls
def greet():
	print("Hello!")


greet()
greet()
