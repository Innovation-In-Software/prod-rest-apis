from fastapi import FastAPI

app = FastAPI()


async def check_db() -> None:
	return None


@app.get("/health/live")
async def live() -> dict[str, str]:
	return {"status": "ok"}


@app.get("/health/ready")
async def ready() -> dict[str, str]:
	await check_db()
	return {"status": "ready"}
