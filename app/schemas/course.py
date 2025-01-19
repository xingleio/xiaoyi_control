from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CourseMasterBase(BaseModel):
    course_name: str = Field(..., min_length=2, max_length=128, description="课程名称")
    subject_type: str = Field(..., min_length=2, max_length=32, description="学科类型")
    grade_level: str = Field(..., min_length=2, max_length=32, description="年级")
    semester: str = Field(..., min_length=2, max_length=32, description="学期")
    course_keywords: Optional[str] = Field(None, description="课程关键词，用于搜索")

class CourseMasterCreate(CourseMasterBase):
    course_code: Optional[str] = Field(None, max_length=64, description="课程编码（选填）")
    course_enabled: Optional[bool] = Field(True, description="是否启用")

class CourseMasterUpdate(BaseModel):
    course_name: Optional[str] = Field(None, min_length=2, max_length=128)
    subject_type: Optional[str] = Field(None, min_length=2, max_length=32)
    grade_level: Optional[str] = Field(None, min_length=2, max_length=32)
    semester: Optional[str] = Field(None, min_length=2, max_length=32)
    course_keywords: Optional[str] = None
    course_enabled: Optional[bool] = None

class CourseMasterResponse(CourseMasterBase):
    course_id: int
    course_code: Optional[str]
    course_enabled: bool
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
