curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name":"Notebook","price":12.5,"in_stock":true}'

  curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d '{"name":"Notebook","price":12.5,"in_stock":true}'

 For Windows Command Prompt, single quotes are a problem.They aren't treated as quoting characters, so your JSON gets mangled 
  and FastAPI receives empty/invalid body.

Use double quotes with escaped inner quotes:

curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d "{\"name\":\"Notebook\",\"price\":12.5,\"in_stock\":true}"

Or put the JSON in a file and reference it:

curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d @item.json

The @item.json approach avoids escaping headaches entirely and is worth showing students since it scales to larger payloads.