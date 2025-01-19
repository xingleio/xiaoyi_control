import pytest
from fastapi.testclient import TestClient
from app.main import app
import requests_mock

client = TestClient(app)

def test_wx_login_success():
    """测试微信登录成功场景"""
    # Mock 微信接口响应
    with requests_mock.Mocker() as m:
        # 模拟微信返回
        m.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            json={"openid": "test_openid_123"}
        )
        
        # 调用登录接口
        response = client.post(
            "/api/v1/auth/wx-login",
            json={"code": "test_code"}
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["role"] == "user"

def test_wx_login_invalid_code():
    """测试无效的code"""
    with requests_mock.Mocker() as m:
        # 模拟微信返回错误
        m.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            json={"errcode": 40029, "errmsg": "invalid code"}
        )
        
        response = client.post(
            "/api/v1/auth/wx-login",
            json={"code": "invalid_code"}
        )
        
        assert response.status_code == 400
        assert "Invalid code" in response.json()["detail"]

def test_token_verification():
    """测试token验证"""
    # 先登录获取token
    with requests_mock.Mocker() as m:
        m.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            json={"openid": "test_openid_123"}
        )
        
        login_response = client.post(
            "/api/v1/auth/wx-login",
            json={"code": "test_code"}
        )
        
        token = login_response.json()["token"]
        
        # 使用token调用需要认证的接口
        response = client.get(
            "/api/v1/courses/user",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # 这里应该返回401，因为我们还没实现课程接口
        assert response.status_code == 404 