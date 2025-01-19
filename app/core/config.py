from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str

    PROJECT_NAME = "小怡课表"
    VERSION = "0.1.0"
    
    # API配置
    API_V1_STR = "/api/v1"
    
    # 服务器配置
    SERVER_HOST = "0.0.0.0"  # 允许所有IP访问
    SERVER_PORT = 8600       # 使用8600端口

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
