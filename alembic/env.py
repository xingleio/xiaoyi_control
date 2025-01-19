from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine
from alembic import context
import os
from dotenv import load_dotenv

# 导入 Base 和所有模型
from app.database import Base
from app.models import User, CourseMaster, CourseUser, UserSchedule

# 加载环境变量
load_dotenv()

# this is the Alembic Config object
config = context.config

# 直接使用 create_engine 创建引擎
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=False,
        compare_server_default=False,
        include_schemas=True,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=False,
            compare_server_default=False,
            include_schemas=True,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
