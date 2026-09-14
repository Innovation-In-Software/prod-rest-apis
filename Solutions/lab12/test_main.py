from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add():
    response = client.get("/add/2/3")
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_subtract():
    response = client.get("/subtract/10/7")
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_multiply():
    response = client.get("/multiply/4/5")
    assert response.status_code == 200
    assert response.json() == {"result": 20}


def test_divide():
    response = client.get("/divide/20/4")
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_divide_by_zero():
    response = client.get("/divide/10/0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero"}