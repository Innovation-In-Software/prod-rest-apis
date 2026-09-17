from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_read_root_returns_ok() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello"}


def test_rejects_non_numeric_price():
    response = client.post("/items", json={"name": "X", "price": "free"})
    assert response.status_code == 422

def test_missing_item_returns_404():
    response = client.get("/items/does-not-exist")
    assert response.status_code == 404

        