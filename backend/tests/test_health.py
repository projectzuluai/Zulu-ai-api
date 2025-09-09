from fastapi.testclient import TestClient
from app.main import app

def test_status_endpoint():
    client = TestClient(app)
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "ai_mode" in data
    assert "gemini_configured" in data
    assert "live_mode" in data

if __name__ == "__main__":
    test_status_endpoint()
    print("/status endpoint test passed.")