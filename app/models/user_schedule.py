from sqlalchemy import Column, BigInteger, SmallInteger, DateTime, ForeignKey, UniqueConstraint, func
from app.database import Base

class UserSchedule(Base):
    __tablename__ = "user_schedule"

    schedule_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, comment='用户ID')
    day_of_week = Column(SmallInteger, nullable=False, comment='星期几(1-7)')
    
    # 9节课的外键关联
    course_user_id1 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第1节课')
    course_user_id2 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第2节课')
    course_user_id3 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第3节课')
    course_user_id4 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第4节课')
    course_user_id5 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第5节课')
    course_user_id6 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第6节课')
    course_user_id7 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第7节课')
    course_user_id8 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第8节课')
    course_user_id9 = Column(BigInteger, ForeignKey("course_user.course_user_id"), comment='第9节课')
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 确保一个用户在同一天只有一条记录
    __table_args__ = (
        UniqueConstraint('user_id', 'day_of_week', name='idx_user_day'),
    )