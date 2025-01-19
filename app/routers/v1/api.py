from fastapi import APIRouter
from .endpoints.router_auth import router as auth_router
from .endpoints.router_course import router as course_router

api_router = APIRouter()

# 注册认证路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(course_router, prefix="/courses", tags=["课程"])
