from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.course_master import CourseMaster
from app.models.course_user import CourseUser
from app.schemas.schemas_course import (
    CourseCreate, CourseUpdate, CourseResponse,
    CourseUserCreate, CourseUserUpdate, CourseUserResponse
)
from app.core.security import get_current_user

router = APIRouter()

# 课程主表接口
@router.post("/master", response_model=CourseResponse)
async def create_course(
    course: CourseCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建或更新课程"""
    try:
        # 检查当前用户是否已有同名课程
        exists = db.query(CourseMaster).filter(
            CourseMaster.course_name == course.course_name,
            CourseMaster.creator_id == current_user.id
        ).first()
        
        if exists:
            # 如果存在，更新课程信息
            for key, value in course.model_dump(exclude_unset=True).items():
                setattr(exists, key, value)
            db.commit()
            db.refresh(exists)
            return exists
        else:
            # 如果不存在，创建新课程
            db_course = CourseMaster(
                **course.model_dump(),
                creator_id=current_user.id
            )
            db.add(db_course)
            db.commit()
            db.refresh(db_course)
            return db_course
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/master/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取课程详情"""
    course = db.query(CourseMaster).filter(
        CourseMaster.course_id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/master", response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取课程列表"""
    courses = db.query(CourseMaster).filter(
        CourseMaster.course_enabled == True
    ).offset(skip).limit(limit).all()
    return courses

@router.put("/master/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int, 
    course: CourseUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新课程信息"""
    db_course = db.query(CourseMaster).filter(
        CourseMaster.course_id == course_id,
        CourseMaster.creator_id == current_user.id
    ).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

# 用户课程接口
@router.post("/user", response_model=CourseUserResponse)
async def create_user_course(
    course: CourseUserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建用户课程"""
    # 检查课程是否存在
    master_course = db.query(CourseMaster).filter(
        CourseMaster.course_id == course.course_id,
        CourseMaster.course_enabled == True
    ).first()
    if not master_course:
        raise HTTPException(status_code=404, detail="Course not found or disabled")
    
    db_course = CourseUser(
        **course.model_dump(),
        user_id=current_user.id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/user/{course_user_id}", response_model=CourseUserResponse)
async def get_user_course(
    course_user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户课程详情"""
    course = db.query(CourseUser).filter(
        CourseUser.course_user_id == course_user_id,
        CourseUser.user_id == current_user.id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/user", response_model=List[CourseUserResponse])
async def list_user_courses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户课程列表"""
    courses = db.query(CourseUser).filter(
        CourseUser.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return courses 