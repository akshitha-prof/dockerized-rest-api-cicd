import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, Base, get_db

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Health ─────────────────────────────────────────────────────────────────────
def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


# ── Create ─────────────────────────────────────────────────────────────────────
def test_create_task():
    r = client.post("/tasks", json={"title": "Buy groceries", "description": "Milk and eggs"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_no_description():
    r = client.post("/tasks", json={"title": "Minimal task"})
    assert r.status_code == 201
    assert r.json()["description"] == ""


def test_create_task_missing_title():
    r = client.post("/tasks", json={"description": "No title here"})
    assert r.status_code == 422


# ── List ───────────────────────────────────────────────────────────────────────
def test_list_tasks_empty():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_returns_all():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    r = client.get("/tasks")
    assert len(r.json()) == 2


def test_list_tasks_filter_completed():
    client.post("/tasks", json={"title": "Task A"})
    r2 = client.post("/tasks", json={"title": "Task B"})
    task_id = r2.json()["id"]
    client.patch(f"/tasks/{task_id}", json={"completed": True})

    r = client.get("/tasks?completed=true")
    assert len(r.json()) == 1
    assert r.json()[0]["id"] == task_id

    r = client.get("/tasks?completed=false")
    assert len(r.json()) == 1


# ── Get ────────────────────────────────────────────────────────────────────────
def test_get_task():
    created = client.post("/tasks", json={"title": "Fetch me"}).json()
    r = client.get(f"/tasks/{created['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Fetch me"


def test_get_task_not_found():
    r = client.get("/tasks/9999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"]


# ── Update ─────────────────────────────────────────────────────────────────────
def test_update_task_title():
    created = client.post("/tasks", json={"title": "Old title"}).json()
    r = client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    assert r.status_code == 200
    assert r.json()["title"] == "New title"


def test_mark_task_completed():
    created = client.post("/tasks", json={"title": "Finish this"}).json()
    r = client.patch(f"/tasks/{created['id']}", json={"completed": True})
    assert r.status_code == 200
    assert r.json()["completed"] is True


def test_update_task_not_found():
    r = client.patch("/tasks/9999", json={"title": "Ghost"})
    assert r.status_code == 404


# ── Delete ─────────────────────────────────────────────────────────────────────
def test_delete_task():
    created = client.post("/tasks", json={"title": "Delete me"}).json()
    r = client.delete(f"/tasks/{created['id']}")
    assert r.status_code == 204
    r2 = client.get(f"/tasks/{created['id']}")
    assert r2.status_code == 404


def test_delete_task_not_found():
    r = client.delete("/tasks/9999")
    assert r.status_code == 404
