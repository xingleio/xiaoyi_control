import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.database import Base, engine
from app.models import User, CourseMaster, CourseUser, UserSchedule

# 加载环境变量
load_dotenv()

def test_database_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("数据库连接成功！")
            return True
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")
        return False

def test_create_tables():
    """测试创建数据表"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("所有数据表创建成功！")
        return True
    except Exception as e:
        print(f"创建数据表失败：{str(e)}")
        return False

def test_check_tables():
    """检查所有表是否存在"""
    try:
        with engine.connect() as connection:
            # 检查每个表
            tables = [
                "user",
                "course_master",
                "course_user",
                "user_schedule"
            ]
            
            for table in tables:
                result = connection.execute(text(
                    f"SELECT COUNT(*) FROM information_schema.tables "
                    f"WHERE table_schema = 'xiaoyi_schedule' "
                    f"AND table_name = '{table}'"
                ))
                if result.scalar() == 0:
                    print(f"错误：表 {table} 不存在！")
                    return False
                print(f"表 {table} 检查通过")
            
            print("所有表检查完成！")
            return True
    except Exception as e:
        print(f"检查表失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("开始数据库测试...")
    
    # 测试数据库连接
    if not test_database_connection():
        print("数据库连接测试失败！")
        sys.exit(1)
    
    # 测试创建表
    if not test_create_tables():
        print("创建表测试失败！")
        sys.exit(1)
    
    # 检查表是否存在
    if not test_check_tables():
        print("表存在性检查失败！")
        sys.exit(1)
    
    print("所有测试通过！✨")
