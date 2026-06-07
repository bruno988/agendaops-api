from fastapi.testclient import TestClient


APPOINTMENT_PAYLOAD = {
    "customer_name": "Carlos",
    "professional_name": "Dr. Lima",
    "service_name": "Consulta",
    "scheduled_at": "2026-07-01T10:00:00Z",
}


def test_list_appointments_without_token(client: TestClient) -> None:
    response = client.get("/api/v1/appointments")
    assert response.status_code == 401


def test_create_appointment(auth_client: TestClient) -> None:
    response = auth_client.post("/api/v1/appointments", json=APPOINTMENT_PAYLOAD)
    assert response.status_code == 201
    assert response.json()["customer_name"] == "Carlos"
    assert response.json()["status"] == "scheduled"


def test_list_appointments(auth_client: TestClient) -> None:
    auth_client.post("/api/v1/appointments", json=APPOINTMENT_PAYLOAD)
    response = auth_client.get("/api/v1/appointments")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment_not_found(auth_client: TestClient) -> None:
    response = auth_client.get("/api/v1/appointments/999")
    assert response.status_code == 404


def test_idempotency(auth_client: TestClient) -> None:
    headers = {"Idempotency-Key": "chave-unica-001"}
    auth_client.post("/api/v1/appointments", json=APPOINTMENT_PAYLOAD, headers=headers)
    auth_client.post("/api/v1/appointments", json=APPOINTMENT_PAYLOAD, headers=headers)
    response = auth_client.get("/api/v1/appointments")
    assert len(response.json()) == 1