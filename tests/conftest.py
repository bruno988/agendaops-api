import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agendaops.db.base import Base
from agendaops.db.session import get_db
from agendaops.main import app

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    client.post("/api/v1/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass"},
    )
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client