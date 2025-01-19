# 小怡课表后端服务

基于FastAPI的中小学课表管理系统后端服务。

## 项目简介
小怡课表是一款面向中小学生的课程管理与作业记录系统，提供课程表管理、作业记录等功能。本仓库为后端服务部分。

## 功能特点
- 微信小程序登录认证
- 标准课程库管理（管理员）
- 个人课表管理（学生）
- 作业管理
- 文件存储（MinIO对象存储）
- 未来支持AI识别（OCR/语音）

## 技术栈
- Python 3.11
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- MySQL (数据库)
- Redis (缓存)
- MinIO (对象存储)
- uvicorn (ASGI服务器)

## 项目结构
```
xiaoyi_control/
├── alembic/                    # 数据库迁移工具
│   ├── versions/               # 迁移版本文件
│   └── env.py                  # 迁移环境配置
├── app/                        # 应用主目录
│   ├── core/                   # 核心模块
│   │   ├── config.py          # 配置管理
│   │   ├── redis_client.py    # Redis客户端
│   │   ├── security.py        # 安全相关
│   │   └── storage.py         # MinIO存储工具
│   ├── models/                 # 数据库模型
│   │   ├── course_master.py   # 课程主表模型
│   │   ├── course_user.py     # 用户课程模型
│   │   ├── user.py            # 用户模型
│   │   └── user_schedule.py   # 用户课表模型
│   ├── routers/               # API路由
│   │   └── v1/               # V1版本API
│   │       ├── endpoints/     # 具体接口实现
│   │       └── api.py        # 路由注册
│   ├── schemas/               # 数据验证模型
│   │   ├── course.py         # 课程相关
│   │   ├── schemas_auth.py   # 认证相关
│   │   └── user.py           # 用户相关
│   ├── database.py            # 数据库配置
│   └── main.py               # 应用入口
├── docs/                      # 文档
│   ├── api.md                # API文档
│   ├── database.sql          # 数据库脚本
│   ├── frontend-guide.md     # 前端对接指南
│   ├── openapi.yaml          # OpenAPI规范
│   ├── progress.md           # 开发进度
│   ├── project-status.md     # 项目状态
│   └── 小怡课表_prd.md        # 产品需求文档
├── tests/                     # 测试用例
│   ├── test_auth.py          # 认证测试
│   ├── test_course.py        # 课程测试
│   └── test_storage.py       # 存储测试
├── .env                      # 环境变量
├── alembic.ini              # 数据库迁移配置
├── deploy.sh                # 部署脚本
└── requirements.txt         # 项目依赖
```

## 环境要求
- Python 3.11+
- MySQL 5.7+
- Redis 6.0+
- MinIO Server

## 快速开始

1. 克隆项目
```bash
git clone [项目地址]
cd xiaoyi_control
```

2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
创建 `.env` 文件并配置：
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname

# Redis配置
REDIS_URL=redis://localhost:6379/0

# MinIO配置
MINIO_ENDPOINT=82.156.230.140:9000
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET=xiaoyi
MINIO_SECURE=False

# 微信小程序配置
WX_APPID=your_appid
WX_SECRET=your_secret
```

5. 初始化数据库
```bash
# 创建数据库
mysql -u root -p < docs/database.sql

# 执行迁移
alembic upgrade head
```

6. 运行服务
```bash
# 开发环境
uvicorn app.main:app --reload --port 8600

# 生产环境
./deploy.sh
```

## API文档
- Swagger UI: http://localhost:8600/docs
- ReDoc: http://localhost:8600/redoc
- API文档: /docs/api.md
- 前端对接: /docs/frontend-guide.md

## 部署说明
1. 服务器要求
   - CentOS/Ubuntu
   - Python 3.11+
   - MySQL 5.7+
   - Redis 6.0+
   - MinIO Server

2. 部署步骤
   - 上传代码
   - 安装依赖
   - 配置环境变量
   - 运行deploy.sh

3. 端口说明
   - API服务: 8600
   - MinIO: 9000

## 开发规范
1. 代码风格遵循PEP 8
2. 所有API需要编写文档字符串
3. 提交代码前需要进行测试
4. 重要更新记录到progress.md

## 版本历史
- v0.1.0 (开发中)
  - 微信登录
  - 文件存储
  - 课程管理

## 常见问题
1. 文件上传失败
   - 检查MinIO配置
   - 验证文件大小限制
   - 确认文件类型支持

2. 数据库连接错误
   - 检查MySQL服务状态
   - 验证连接字符串
   - 确认数据库权限

## 联系方式
[联系方式]
7635839@qq.com