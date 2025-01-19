from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from app.core.security import SecurityUtils
from app.database import get_db
from app.models.user import User
from app.schemas.schemas_auth import WxLoginRequest, LoginResponse
from app.core.redis_client import RedisClient
from app.core.storage import storage

router = APIRouter()

@router.post("/wx-login", response_model=LoginResponse)
async def wx_login(request: WxLoginRequest, db: Session = Depends(get_db)):
    """微信登录接口"""
    try:
        # 获取openid
        openid = SecurityUtils.get_openid(request.code)
        if not openid:
            raise HTTPException(status_code=400, detail="Invalid code")
        
        # 查找或创建用户
        user = db.query(User).filter(User.openid == openid).first()
        if not user:
            user = User(
                openid=openid,
                nickname="测试用户",  # 添加默认值
                role="user"
            )
            db.add(user)
            try:
                db.commit()
                db.refresh(user)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
        
        # 生成token并存储
        token = SecurityUtils.create_token(openid)
        if not RedisClient.set_token(token, user.id):
            raise HTTPException(status_code=500, detail="Failed to store token")
        
        return {
            "token": token,
            "user": {
                "id": user.id,
                "nickname": user.nickname,
                "avatar_url": user.avatar_url,
                "role": user.role
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile):
    """上传用户头像"""
    try:
        # 检查文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files allowed")
            
        # 上传文件
        url = storage.upload_file(
            file.file,
            file.filename,
            folder='avatars'
        )
        
        return {"url": url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Upload failed")
