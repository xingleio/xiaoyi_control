from sqlalchemy import Column, BigInteger, Integer, String, DateTime, func
from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    openid = Column(String(64), unique=True, nullable=False, comment='微信openid')
    nickname = Column(String(64), comment='用户昵称')
    avatar_url = Column(String(255), comment='头像URL')
    theme_id = Column(Integer, default=1, comment='主题ID')
    province = Column(String(50), comment='省份')
    city = Column(String(50), comment='城市')
    school = Column(String(100), comment='学校名称')
    role = Column(String(16), default="user", comment='用户角色：user/admin')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
