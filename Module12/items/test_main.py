# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rejects_non_numeric_price():
    # "free" cannot become a float -> wrong type
    response = client.post("/items", json={"name": "X", "price": "free"})
    assert response.status_code == 422

def test_rejects_negative_price():
    # -5 is a number, but out of range (must be > 0)
    response = client.post("/items", json={"name": "X", "price": -5})
    assert response.status_code == 422

def test_rejects_missing_required_field():
    # no "price" field at all -> malformed
    response = client.post("/items", json={"name": "X"})
    assert response.status_code == 422

def test_error_identifies_the_bad_field():
    # Don't just check the status - check the error STRUCTURE
    response = client.post("/items", json={"name": "X", "price": "free"})
    assert response.status_code == 422

    detail = response.json()["detail"]
    # FastAPI returns a list of errors; each says where the problem is
    assert detail[0]["loc"] == ["body", "price"]
    assert detail[0]["type"] == "float_parsing"