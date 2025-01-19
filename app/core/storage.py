import boto3
from botocore.client import Config
from fastapi import HTTPException
import os
from typing import Optional, BinaryIO
from datetime import datetime
import mimetypes

class StorageClient:
    """MinIO 存储客户端"""
    
    def __init__(self):
        """初始化 MinIO 客户端"""
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url='http://82.156.230.140:9000',  # MinIO服务器地址
                aws_access_key_id='minioadmin',
                aws_secret_access_key='minioadmin123',
                config=Config(signature_version='s3v4'),
                region_name='us-east-1'  # 默认区域
            )
            # 确保默认桶存在
            self._ensure_default_bucket()
        except Exception as e:
            print(f"MinIO连接失败: {str(e)}")
            raise HTTPException(status_code=500, detail="Storage service unavailable")

    def _ensure_default_bucket(self, bucket_name: str = "xiaoyi"):
        """确保默认桶存在"""
        try:
            # 检查桶是否存在
            exists = self.bucket_exists(bucket_name)
            print(f"Checking bucket '{bucket_name}': {'exists' if exists else 'not exists'}")
            
            if not exists:
                print(f"Creating bucket '{bucket_name}'...")
                self.s3_client.create_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' created successfully")
                
                # 设置桶的公共访问权限
                self.s3_client.put_bucket_acl(
                    Bucket=bucket_name,
                    ACL='public-read'
                )
                print(f"Bucket '{bucket_name}' ACL set to public-read")
        except Exception as e:
            print(f"Error in _ensure_default_bucket: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create storage bucket: {str(e)}")

    def bucket_exists(self, bucket_name: str) -> bool:
        """检查桶是否存在"""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except:
            return False

    def upload_file(
        self, 
        file: BinaryIO,
        filename: str,
        bucket: str = "xiaoyi",
        folder: str = None
    ) -> str:
        """
        上传文件
        :param file: 文件对象
        :param filename: 原始文件名
        :param bucket: 存储桶名称
        :param folder: 文件夹路径（可选）
        :return: 文件访问URL
        """
        try:
            # 生成唯一文件名
            ext = os.path.splitext(filename)[1]
            new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            
            # 添加文件夹路径
            if folder:
                new_filename = f"{folder}/{new_filename}"

            # 获取文件类型
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

            # 上传文件
            self.s3_client.upload_fileobj(
                file,
                bucket,
                new_filename,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )

            # 生成文件URL
            url = f"http://82.156.230.140:9000/{bucket}/{new_filename}"
            return url

        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            raise HTTPException(status_code=500, detail="File upload failed")

    def delete_file(self, file_path: str, bucket: str = "xiaoyi") -> bool:
        """
        删除文件
        :param file_path: 文件路径
        :param bucket: 存储桶名称
        :return: 是否删除成功
        """
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=file_path)
            return True
        except Exception as e:
            print(f"文件删除失败: {str(e)}")
            return False

    def get_file_url(self, file_path: str, bucket: str = "xiaoyi", expires: int = 3600) -> str:
        """
        获取文件访问URL
        :param file_path: 文件路径
        :param bucket: 存储桶名称
        :param expires: URL有效期（秒）
        :return: 文件访问URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': file_path
                },
                ExpiresIn=expires
            )
            return url
        except Exception as e:
            print(f"获取文件URL失败: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate file URL")

# 创建全局实例
storage = StorageClient() 