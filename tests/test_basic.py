from fastapi.testclient import TestClient
from app.main import app
from app.core.security import SecurityUtils

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_auth_required():
    """测试需要认证的接口"""
    response = client.get("/api/v1/courses/master")
    assert response.status_code == 403  # 没有token应该返回403

def test_invalid_token():
    """测试无效token"""
    response = client.get(
        "/api/v1/courses/master",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401  # 无效token应该返回401 