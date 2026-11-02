from fastapi import FastAPI         # import the framework
 
app = FastAPI(title="My API",
    description="Does useful things",
    version="1.0.0",
)                     # creates the application object
 
@app.get("/")                       # handle GET requests to "/"
def read_root():
    return {"message": "Hello, World!"}     # dict → auto JSON
 
@app.get("/greet/{name}")           # {name} is a path parameter
def greet(name: str):               # typed & validated as str
    return {"message": f"Hello, {name}!"}   # returns JSON
