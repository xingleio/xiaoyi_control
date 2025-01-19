from pydantic import BaseModel
from typing import Optional

class WxLoginRequest(BaseModel):
    code: str

class UserInfo(BaseModel):
    id: int
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str

class LoginResponse(BaseModel):
    token: str
    user: UserInfo 