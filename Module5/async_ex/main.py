import asyncio

from fastapi import FastAPI

app = FastAPI()


# Simulates a slow I/O task, like an
# external API call or a database query.
# asyncio.sleep is the non-blocking
# version of time.sleep: while it waits,
# the event loop can handle other requests.
async def fetch_account_balance(account_id: int) -> float:
	await asyncio.sleep(2)
	return 1000.0 + account_id


@app.get("/balance/{account_id}")
async def get_balance(account_id: int):
	# await = step aside while waiting
	balance = await fetch_account_balance(account_id)
	return {"account_id": account_id, "balance": balance}

