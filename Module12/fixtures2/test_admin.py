from main import app, get_current_user, User   # note: import User too

def fake_admin():
    return User(name="Alice", role="admin")

def fake_regular_user():
    return User(name="Bob", role="user")

def test_admin_can_access(client):
    app.dependency_overrides[get_current_user] = fake_admin
    response = client.get("/admin")
    assert response.status_code == 200
    assert response.json() == {"secret": "data"}
    app.dependency_overrides.clear()          # undo the override

def test_regular_user_forbidden(client):
    app.dependency_overrides[get_current_user] = fake_regular_user
    response = client.get("/admin")
    assert response.status_code == 403         # Bob is not an admin
    app.dependency_overrides.clear()

def test_unauthenticated_rejected(client):
    # No override at all -> the REAL get_current_user runs and finds no token
    response = client.get("/admin")
    assert response.status_code == 401