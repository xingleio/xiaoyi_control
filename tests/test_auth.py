from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_wx_login():
    """测试微信登录"""
    response = client.post("/api/v1/auth/wx-login", json={"code": "test_code"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["role"] == "user" 