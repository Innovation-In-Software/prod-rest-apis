import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()


@app.middleware("http")
async def add_request_id(request: Request, call_next):
	request_id = str(uuid.uuid4())
	request.state.request_id = request_id
	response = await call_next(request)
	response.headers["X-Request-ID"] = request_id
	return response


@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
	return JSONResponse(
		status_code=500,
		content={
			"error": {
				"code": "INTERNAL_ERROR",
				"message": "An unexpected error occurred.",
				"request_id": request.state.request_id,
			}
		},
	)


@app.get("/")
async def root(request: Request):
	return {
		"message": "global exception handler example",
		"request_id": request.state.request_id,
	}


@app.get("/boom")
async def boom():
	raise RuntimeError("unexpected failure")
