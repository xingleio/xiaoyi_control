from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, BigInteger, ForeignKey, func, UniqueConstraint
from app.database import Base

class CourseMaster(Base):
    __tablename__ = "course_master"

    course_id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_code = Column(String(64), unique=False, nullable=True, comment='课程编码')
    course_name = Column(String(128), nullable=False, comment='课程名称')
    course_type = Column(String(32), nullable=False, comment='课程类型')
    course_keywords = Column(Text, comment='课程关键词')
    course_enabled = Column(Boolean, default=True, comment='是否启用')
    creator_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, comment='创建者ID')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')

    __table_args__ = (
        # 添加联合唯一约束：课程名称+创建者ID
        UniqueConstraint('course_name', 'creator_id', name='uix_course_name_creator'),
    )
