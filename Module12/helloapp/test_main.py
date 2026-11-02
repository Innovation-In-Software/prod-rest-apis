from fastapi.testclient import TestClient

from main import app


client = TestClient(app) #proxy


def test_read_root_returns_ok() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello"}