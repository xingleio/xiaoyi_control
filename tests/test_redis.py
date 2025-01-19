from app.core.redis_client import RedisClient

def test_redis_connection():
    """测试Redis连接"""
    try:
        client = RedisClient.get_instance()
        assert client.ping()
    except Exception as e:
        assert False, f"Redis connection failed: {str(e)}"

def test_token_operations():
    """测试Token操作"""
    test_token = "test_token"
    test_user_id = 1
    
    # 测试存储
    assert RedisClient.set_token(test_token, test_user_id)
    
    # 测试获取
    user_id = RedisClient.get_user_id(test_token)
    assert user_id == test_user_id
    
    # 测试删除
    assert RedisClient.delete_token(test_token) 