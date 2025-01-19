from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1.api import api_router

app = FastAPI(
    title="小怡课表",
    description="小怡课表后端API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 测试根路由
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 添加健康检查接口
@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

# 注册v1版本的路由
app.include_router(api_router, prefix="/api/v1")
