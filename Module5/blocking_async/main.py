import time

from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool

app = FastAPI()


# In-memory data used to stand in for a real database.
db = {
	1: {"id": 1, "name": "Ada"},
	2: {"id": 2, "name": "Linus"},
	3: {"id": 3, "name": "Grace"},
}


def blocking_db_query(user_id: int) -> dict | None:
	# Simulate a slow synchronous database call.
	time.sleep(2)
	return db.get(user_id)


@app.get("/user/{user_id}")
async def get_user(user_id: int):
	result = await run_in_threadpool(blocking_db_query, user_id)

	if result is None:
		raise HTTPException(status_code=404, detail="User not found")

	return result
