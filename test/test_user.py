import time

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():
    unique_username = f"newuser_{int(time.time())}"  # Ensure unique username
    response = client.post(
        "/user/",
        json={
            "username": unique_username,
            "password": "newpassword",
            "email": f"{unique_username}@example.com",
            "name": "New User",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == unique_username


def test_get_all_users():
    response = client.get("/user/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    unique_username = f"testuser_{int(time.time())}"
    create_response = client.post(
        "/user/",
        json={
            "username": unique_username,
            "password": "password",
            "email": f"{unique_username}@example.com",
            "name": "Test User",
        },
    )
    assert create_response.status_code == 200
    user_id = create_response.json().get("id")
    assert user_id is not None  # Ensure the user was created

    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == unique_username


def test_delete_user():
    unique_username = f"deletetest_{int(time.time())}"
    create_response = client.post(
        "/user/",
        json={
            "username": unique_username,
            "password": "password",
            "email": f"{unique_username}@example.com",
            "name": "Delete User",
        },
    )
    assert create_response.status_code == 200
    user_id = create_response.json().get("id")
    assert user_id is not None

    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200

    # Verify user deletion
    get_response = client.get(f"/user/{user_id}")
    assert get_response.status_code == 404  # Should return "User not found"
