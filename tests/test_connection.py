import os
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_direct_connection():
    try:
        # 从环境变量获取连接信息
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("未找到DATABASE_URL环境变量")
            return
        
        # 解析连接字符串
        # 示例: mysql+pymysql://user:pass@host:port/dbname
        parts = db_url.replace('mysql+pymysql://', '').split('@')
        user_pass = parts[0].split(':')
        host_db = parts[1].split('/')
        
        # 建立连接
        connection = pymysql.connect(
            host=host_db[0].split(':')[0],
            port=int(host_db[0].split(':')[1]),
            user=user_pass[0],
            password=user_pass[1].replace('%40', '@').replace('%23', '#'),
            database=host_db[1].split('?')[0]
        )
        
        print("数据库连接成功！")
        connection.close()
        
    except Exception as e:
        print(f"连接失败：{str(e)}")

if __name__ == "__main__":
    test_direct_connection() 