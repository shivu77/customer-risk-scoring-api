from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.config.models_base import Base
from app.config.database import get_db

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_post_customer_add_valid_200():
    payload = {"name": "Rahul", "age": 28, "income": 45000, "activity_score": 62}
    r = client.post("/customer/add", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] > 0
    assert data["name"] == payload["name"]

def test_post_customer_add_invalid_age_422():
    payload = {"name": "Rahul", "age": 17, "income": 45000, "activity_score": 62}
    r = client.post("/customer/add", json=payload)
    assert r.status_code == 422

def test_post_customer_add_missing_fields_422():
    payload = {"name": "Rahul", "age": 28}
    r = client.post("/customer/add", json=payload)
    assert r.status_code == 422

def test_get_customer_existing_200():
    payload = {"name": "Alice", "age": 30, "income": 50000, "activity_score": 70}
    r = client.post("/customer/add", json=payload)
    cid = r.json()["id"]
    r2 = client.get(f"/customer/{cid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == cid

def test_get_customer_non_existing_404():
    r = client.get("/customer/99999")
    assert r.status_code == 404

