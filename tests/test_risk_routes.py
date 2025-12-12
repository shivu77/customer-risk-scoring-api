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

def create_customer(name, age, income, activity_score):
    r = client.post("/customer/add", json={"name": name, "age": age, "income": income, "activity_score": activity_score})
    return r.json()["id"]

def test_post_risk_score_valid_200():
    cid = create_customer("Bob", 35, 45000, 55)
    payload = {"customer_id": cid, "age": 35, "income": 45000, "activity_score": 55}
    r = client.post("/risk/score", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "final_score" in data
    assert "explanation" in data

def test_post_risk_score_invalid_customer_404():
    payload = {"customer_id": 99999, "age": 35, "income": 45000, "activity_score": 55}
    r = client.post("/risk/score", json=payload)
    assert r.status_code == 404

def test_get_risk_scores_list_200():
    cid = create_customer("Carol", 40, 60000, 65)
    payload = {"customer_id": cid, "age": 40, "income": 60000, "activity_score": 65}
    client.post("/risk/score", json=payload)
    r = client.get(f"/risk/{cid}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

def test_get_risk_scores_empty_list_200():
    cid = create_customer("Dave", 30, 50000, 60)
    r = client.get(f"/risk/{cid}")
    assert r.status_code == 200
    assert r.json() == []

