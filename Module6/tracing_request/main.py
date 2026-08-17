import uuid

from fastapi import FastAPI, Request


app = FastAPI()


@app.middleware("http")
async def add_request_id(request: Request, call_next):
	request_id = str(uuid.uuid4())  # before: mint the ID
	request.state.request_id = request_id  # before: stash it where handlers can reach it
	response = await call_next(request)  # the handler runs here
	response.headers["X-Request-ID"] = request_id  # after: send it back
	return response


@app.get("/")
async def root(request: Request):
	return {
		"message": "hello",
		"request_id": request.state.request_id,
	}
