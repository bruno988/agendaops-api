from fastapi.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "bruno", "password": "123456"},
    )
    assert response.status_code == 201
    assert response.json()["username"] == "bruno"
    assert response.json()["is_active"] is True


def test_register_duplicate_user(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "bruno", "password": "123456"})
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "bruno", "password": "123456"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_login_success(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "bruno", "password": "123456"})
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "bruno", "password": "123456"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"username": "bruno", "password": "123456"})
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "bruno", "password": "senhaerrada"},
    )
    assert response.status_code == 401