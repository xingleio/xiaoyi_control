import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import StorageClient
import io
import os

client = TestClient(app)

def get_test_token():
    """获取测试用token"""
    response = client.post("/api/v1/auth/wx-login", json={"code": "test_code"})
    return response.json()["token"]

def test_storage_connection():
    """测试存储服务连接"""
    try:
        storage = StorageClient()
        exists = storage.bucket_exists("xiaoyi")
        print(f"Bucket 'xiaoyi' exists: {exists}")
        assert exists == True
    except Exception as e:
        print(f"Storage connection error: {str(e)}")
        pytest.fail(f"Storage connection failed: {str(e)}")

def test_file_upload_and_download():
    """测试文件上传和下载"""
    token = get_test_token()
    
    # 1. 上传文件
    test_image_path = r"F:\code_scope\app\xiaoyi_control\docs\5.jpeg"
    
    with open(test_image_path, 'rb') as f:
        upload_response = client.post(
            "/api/v1/auth/upload-avatar",
            files={"file": ("5.jpeg", f, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    assert upload_response.status_code == 200
    data = upload_response.json()
    file_url = data["url"]
    print(f"Upload successful. File URL: {file_url}")
    
    # 2. 下载并验证文件
    import requests
    download_response = requests.get(file_url)
    assert download_response.status_code == 200
    
    # 3. 验证文件大小
    original_size = os.path.getsize(test_image_path)
    downloaded_size = len(download_response.content)
    print(f"Original file size: {original_size}")
    print(f"Downloaded file size: {downloaded_size}")
    
    return file_url

def test_upload_invalid_file():
    """测试上传无效文件类型"""
    token = get_test_token()
    
    # 创建测试文本文件
    file_content = b"text content"
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/auth/upload-avatar",
        files={"file": ("test.txt", file, "text/plain")},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400

def test_upload_without_auth():
    """测试未授权上传"""
    test_image_path = r"F:\code_scope\app\xiaoyi_control\docs\5.jpeg"
    
    with open(test_image_path, 'rb') as f:
        response = client.post(
            "/api/v1/auth/upload-avatar",
            files={"file": ("5.jpeg", f, "image/jpeg")}
        )
    
    assert response.status_code == 401 