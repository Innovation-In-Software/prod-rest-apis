import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


# The problem: builds the entire list in memory, then serializes it all at once.
# For a large dataset this can spike memory and delay the first byte.
@app.get("/all-at-once")
def read_all_at_once():
    data = [{"id": i, "value": i * 2} for i in range(1_000_000)]
    return data  # FastAPI serializes the whole thing in memory before sending


# The fix: stream the data out in chunks so nothing large is held in memory,
# and the client starts receiving bytes immediately.
def generate_json():
    yield "["
    for i in range(1_000_000):
        if i > 0:
            yield ","
        yield json.dumps({"id": i, "value": i * 2})
    yield "]"


@app.get("/streamed")
def read_streamed():
    return StreamingResponse(generate_json(), media_type="application/json")