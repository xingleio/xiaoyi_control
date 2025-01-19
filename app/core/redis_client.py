import redis
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    _instance = None
    _client = None

    @classmethod
    def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            cls._instance = cls()
            # 测试连接
            try:
                cls._client.ping()
            except Exception as e:
                logger.error(f"Redis connection failed: {str(e)}")
                raise
        return cls._client

    def __init__(self):
        if RedisClient._client is None:
            try:
                RedisClient._client = redis.Redis(
                    host='82.156.230.140',
                    port=6379,
                    password='xiaoyi',
                    decode_responses=True,
                    socket_timeout=5,  # 添加超时设置
                    socket_connect_timeout=5
                )
            except Exception as e:
                logger.error(f"Redis initialization failed: {str(e)}")
                raise

    @classmethod
    def set_token(cls, token: str, user_id: int, expires: int = 7200) -> bool:
        """存储token，默认2小时过期"""
        try:
            return cls.get_instance().set(
                f"token:{token}", 
                str(user_id), 
                ex=expires
            )
        except Exception as e:
            logger.error(f"Failed to set token: {str(e)}")
            return False

    @classmethod
    def get_user_id(cls, token: str) -> Optional[int]:
        """获取token对应的用户ID"""
        try:
            user_id = cls.get_instance().get(f"token:{token}")
            return int(user_id) if user_id else None
        except Exception as e:
            logger.error(f"Failed to get user_id: {str(e)}")
            return None

    @classmethod
    def delete_token(cls, token: str) -> bool:
        """删除token"""
        try:
            return cls.get_instance().delete(f"token:{token}") > 0
        except Exception as e:
            logger.error(f"Failed to delete token: {str(e)}")
            return False 