from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey, func
from app.database import Base

class CourseUser(Base):
    __tablename__ = "course_user"

    course_user_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, comment='用户ID')
    course_id = Column(BigInteger, ForeignKey("course_master.course_id"), nullable=False, comment='课程ID')
    course_alias = Column(String(128), comment='课程别名')
    teacher_name = Column(String(64), comment='教师姓名')
    classroom = Column(String(128), comment='教室')
    course_color = Column(String(32), default="#1890FF", comment='显示颜色')
    course_remark = Column(Text, comment='备注')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
