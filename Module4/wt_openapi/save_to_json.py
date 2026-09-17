import json
from main import app          # imports your FastAPI app WITHOUT serving it

spec = app.openapi()          # builds the OpenAPI spec as a Python dict
with open("openapi.json", "w") as f:
    json.dump(spec, f, indent=2)

print("Wrote openapi.json")