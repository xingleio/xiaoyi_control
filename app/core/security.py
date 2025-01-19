import os
import time
import hmac
import hashlib
import requests
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from dotenv import load_dotenv
from .redis_client import RedisClient

load_dotenv()

security = HTTPBearer()

class SecurityUtils:
    @staticmethod
    def create_token(openid: str) -> str:
        """生成用户token"""
        timestamp = str(int(time.time()))
        message = f"{openid}:{timestamp}"
        secret_key = os.getenv("SECRET_KEY", "your-secret-key")  # 添加默认值
        token = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return token

    @staticmethod
    def verify_token(token: str) -> User:
        """验证token并返回用户"""
        try:
            user_id = RedisClient.get_user_id(token)
            if not user_id:
                raise HTTPException(status_code=401, detail="Token expired or invalid")
            
            # 获取用户信息
            db = next(get_db())
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
                
            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authentication")

    @staticmethod
    def get_openid(code: str) -> str:
        """通过code获取openid"""
        try:
            # 测试模式：如果是test_code，直接返回测试openid
            if code == "test_code":
                return "test_openid"
                
            # 正式环境：调用微信接口
            appid = os.getenv("WX_APPID")
            secret = os.getenv("WX_SECRET")
            
            # 如果没有配置微信参数，抛出错误
            if not appid or not secret:
                raise HTTPException(
                    status_code=400,
                    detail="WeChat configuration missing"
                )
                
            url = "https://api.weixin.qq.com/sns/jscode2session"
            params = {
                "appid": appid,
                "secret": secret,
                "js_code": code,
                "grant_type": "authorization_code"
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "errcode" in data:
                raise HTTPException(
                    status_code=400, 
                    detail=f"WeChat error: {data.get('errmsg', 'Invalid code')}"
                )
            
            if "openid" not in data:
                raise HTTPException(status_code=400, detail="Invalid code")
                
            return data["openid"]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid code")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    try:
        token = credentials.credentials
        return SecurityUtils.verify_token(token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")