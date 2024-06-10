import pytest
from fastapi.testclient import TestClient
from main import app, accounts, Account

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clean up before each test
    accounts.clear()
    yield
    # Clean up after each test
    accounts.clear()

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": True}

def test_create_account():
    response = client.put("/accounts/1", json={"name": "Juan's Account", "description": "A test account", "balance": 100.0, "active": True})
    assert response.status_code == 201
    assert response.json() == {
        "name": "Juan's Account",
        "description": "A test account",
        "balance": 100.0,
        "active": True
    }

def test_read_account():
    client.put("/accounts/1", json={"name": "Juan's Account", "description": "A test account", "balance": 100.0, "active": True})
    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Juan's Account",
        "description": "A test account",
        "balance": 100.0,
        "active": True
    }

def test_read_nonexistent_account():
    response = client.get("/accounts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}

def test_create_existing_account():
    client.put("/accounts/1", json={"name": "Juan's Account", "description": "A test account", "balance": 100.0, "active": True})
    response = client.put("/accounts/1", json={"name": "Juan's Account", "description": "A test account", "balance": 100.0, "active": True})
    assert response.status_code == 409
    assert response.json() == {"detail": "Account exists"}

def test_delete_account():
    client.put("/accounts/1", json={"name": "Juan's Account", "description": "A test account", "balance": 100.0, "active": True})
    response = client.delete("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Successful"}

def test_delete_nonexistent_account():
    response = client.delete("/accounts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}
