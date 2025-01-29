import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register():
    unique_username = "testuser" + str(int(time.time()))  # Unique username
    response = client.post(
        "/auth/register",
        json={
            "username": unique_username,
            "password": "securepass",
            "email": f"{unique_username}@example.com",
            "name": "Test User",
        },
    )
    assert response.status_code == 200
    token = response.json()  # API returns a raw JWT, not a dictionary
    assert isinstance(token, str) and len(token) > 0  # Ensure it's a non-empty string


def test_login():
    username = "testuser" + str(int(time.time()))  # Ensure unique username

    # Register first
    client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "securepass",
            "email": f"{username}@example.com",
            "name": "Test User",
        },
    )

    response = client.post(
        "/auth/login",
        json={"username": username, "password": "securepass"},
    )
    assert response.status_code == 200
    token = response.json()  # API returns raw JWT
    assert isinstance(token, str) and len(token) > 0  # Ensure it's a valid JWT

    return token  # Returning token for next test


def test_get_me():
    token = test_login()  # Get a valid token from test_login

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "username" in response.json()
