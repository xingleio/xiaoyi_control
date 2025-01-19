from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 课程主表相关模型
class CourseCreate(BaseModel):
    course_name: str
    course_type: str
    course_keywords: Optional[str] = None
    course_enabled: bool = True
    course_code: Optional[str] = None  # 课程代码可选，如果不提供可以自动生成

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    course_type: Optional[str] = None
    course_keywords: Optional[str] = None
    course_enabled: Optional[bool] = None

class CourseResponse(BaseModel):
    course_id: int
    course_code: str
    course_name: str
    course_type: str
    course_keywords: Optional[str] = None
    course_enabled: bool
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 用户课程相关模型
class CourseUserCreate(BaseModel):
    course_id: int
    course_alias: Optional[str] = None
    teacher_name: Optional[str] = None
    classroom: Optional[str] = None
    course_color: Optional[str] = "#1890FF"
    course_remark: Optional[str] = None

class CourseUserUpdate(BaseModel):
    course_alias: Optional[str] = None
    teacher_name: Optional[str] = None
    classroom: Optional[str] = None
    course_color: Optional[str] = None
    course_remark: Optional[str] = None

class CourseUserResponse(BaseModel):
    course_user_id: int
    user_id: int
    course_id: int
    course_alias: Optional[str]
    teacher_name: Optional[str]
    classroom: Optional[str]
    course_color: str
    course_remark: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 