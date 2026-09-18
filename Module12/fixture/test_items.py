
def test_create_item(client):
    response = client.post("/items/widget")
    assert response.status_code == 200
    assert response.json() == {"name": "widget"}

def test_read_missing_item(client):
    # Thanks to teardown, "widget" from the previous test is GONE here
    response = client.get("/items/widget")
    assert response.json() == {"error": "not found"}