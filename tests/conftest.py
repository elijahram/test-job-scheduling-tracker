import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.security import hash_password
from app.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_headers(client):
    db = TestingSessionLocal()
    admin_user = User(
        username="adminuser",
        email="adminuser@example.com",
        hashed_password=hash_password("adminpassword"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.close()

    login_response = client.post(
        "auth/login/", data={"username": "adminuser", "password": "adminpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
