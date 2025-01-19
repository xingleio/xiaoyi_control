import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import SecurityUtils

client = TestClient(app)

def get_test_token():
    """获取测试用token"""
    response = client.post("/api/v1/auth/wx-login", json={"code": "test_code"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data, "Response missing token"
    assert "user" in data, "Response missing user info"
    print(f"Login response: {data}")  # 添加调试信息
    return data["token"]

def test_create_course():
    """测试创建课程"""
    token = get_test_token()
    course_data = {
        "course_name": "Python编程基础",
        "course_type": "编程类",
        "course_keywords": "Python,编程,基础",
        "course_enabled": True
    }
    
    # 第一次创建
    response = client.post(
        "/api/v1/courses/master",
        json=course_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["course_name"] == course_data["course_name"]
    first_course_id = data["course_id"]

    # 再次创建同名课程应该返回更新后的记录
    response = client.post(
        "/api/v1/courses/master",
        json=course_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == first_course_id  # 应该是同一条记录
    
    return data["course_id"]

def test_create_user_course():
    """测试创建用户课程"""
    token = get_test_token()
    course_id = test_create_course()
    
    course_data = {
        "course_id": course_id,
        "course_alias": "Python基础",
        "teacher_name": "张老师",
        "classroom": "教室A101"
    }
    
    response = client.post(
        "/api/v1/courses/user",
        json=course_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["course_alias"] == course_data["course_alias"]
    return data["course_user_id"] 

def test_wx_login_invalid_code():
    """测试无效code登录"""
    response = client.post("/api/v1/auth/wx-login", json={"code": "invalid_code"})
    assert response.status_code == 400  # 只验证状态码

def test_create_course_unauthorized():
    """测试未授权创建课程"""
    response = client.post("/api/v1/courses/master", json={})
    assert response.status_code == 401  # 只验证状态码

def test_get_nonexistent_course():
    """测试获取不存在的课程"""
    token = get_test_token()
    response = client.get(
        "/api/v1/courses/master/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404  # 只验证状态码 