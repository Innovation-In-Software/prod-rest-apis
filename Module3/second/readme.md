# POST /items Examples

## Basic cURL Request

```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name":"Notebook","price":12.5,"in_stock":true}'
```

```bash
curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d '{"name":"Notebook","price":12.5,"in_stock":true}'
```

## Windows Command Prompt Note

For Windows Command Prompt, single quotes are a problem. They are not treated as quoting characters, so the JSON gets mangled and FastAPI receives an empty or invalid body.

## Windows Command Prompt Example

Use double quotes with escaped inner quotes:

```bash
curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d "{\"name\":\"Notebook\",\"price\":12.5,\"in_stock\":true}"
```

## Using a JSON File

Or put the JSON in a file and reference it:

```bash
curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d @item.json
```

The `@item.json` approach avoids escaping headaches entirely and is worth showing students since it scales to larger payloads.