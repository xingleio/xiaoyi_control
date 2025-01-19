# 小怡课表 API 文档

## 基础信息
- 基础URL: `http://localhost:8000/api/v1`
- 认证方式: 请求头携带 token
  ```
  Authorization: Bearer {token}
  ```

## 1. 用户认证

### 1.1 微信登录
- **接口**：`POST /auth/wx-login`
- **描述**：小程序登录，获取token
- **请求体**：
```json
{
    "code": "string"  // 小程序 wx.login() 获取的 code
}
```
- **响应**：
```json
{
    "token": "string",  // 后续请求需要携带的token
    "user": {
        "id": "integer",
        "nickname": "string",
        "avatar_url": "string",
        "role": "string"
    }
}
```

## 2. 课程管理

### 2.1 获取标准课程列表
- **接口**：`GET /courses/master`
- **描述**：获取系统预设的课程列表
- **参数**：
  - `enabled`：（可选）布尔值，是否启用
  - `type`：（可选）字符串，课程类型
- **响应**：
```json
{
    "total": "integer",
    "items": [
        {
            "course_id": "integer",
            "course_code": "string",
            "course_name": "string",
            "course_type": "string"
        }
    ]
}
```

### 2.2 获取用户课程列表
- **接口**：`GET /courses/user`
- **描述**：获取当前用户的所有课程
- **响应**：
```json
{
    "total": "integer",
    "items": [
        {
            "course_user_id": "integer",
            "course_name": "string",
            "course_alias": "string",  // 课程别名
            "teacher_name": "string",
            "classroom": "string",
            "course_color": "string"   // 课程颜色
        }
    ]
}
```

### 2.3 添加用户课程
- **接口**：`POST /courses/user`
- **描述**：添加课程到个人课表
- **请求体**：
```json
{
    "course_id": "integer",    // 标准课程ID
    "course_alias": "string",  // 可选，课程别名
    "teacher_name": "string",  // 可选，教师姓名
    "classroom": "string",     // 可选，教室
    "course_color": "string"   // 可选，显示颜色
}
```
- **响应**：返回创建的课程信息
```json
{
    "course_user_id": "integer",
    "course_name": "string",
    "course_alias": "string",
    "teacher_name": "string",
    "classroom": "string",
    "course_color": "string"
}
```

## 3. 课表管理

### 3.1 获取某天课表
- **接口**：`GET /schedule/{day}`
- **描述**：获取指定日期的课表
- **参数**：
  - `day`: 数字1-7，代表周一到周日
- **响应**：
```json
{
    "day_of_week": "integer",  // 1-7
    "courses": [
        {
            "slot": 1,         // 第几节课，1-9
            "course": {
                "course_user_id": "integer",
                "course_name": "string",
                "course_alias": "string",
                "teacher_name": "string",
                "classroom": "string",
                "course_color": "string"
            }
        }
    ]
}
```

### 3.2 设置某天课表
- **接口**：`PUT /schedule/{day}`
- **描述**：设置指定日期的课表
- **参数**：
  - `day`: 数字1-7，代表周一到周日
- **请求体**：
```json
{
    "course_user_id1": "integer",  // 第1节课的课程ID
    "course_user_id2": "integer",  // 第2节课的课程ID
    "course_user_id3": "integer",  // 第3节课的课程ID
    "course_user_id4": "integer",  // 第4节课的课程ID
    "course_user_id5": "integer",  // 第5节课的课程ID
    "course_user_id6": "integer",  // 第6节课的课程ID
    "course_user_id7": "integer",  // 第7节课的课程ID
    "course_user_id8": "integer",  // 第8节课的课程ID
    "course_user_id9": "integer"   // 第9节课的课程ID
}
```

## 4. 文件存储

### 4.1 上传头像
- **接口**：`POST /auth/upload-avatar`
- **描述**：上传用户头像到MinIO存储
- **请求头**：
  - `Authorization: Bearer {token}`
  - `Content-Type: multipart/form-data`
- **请求参数**：
  - `file`: 图片文件（支持jpg、jpeg、png格式）
- **响应**：
```json
{
    "url": "http://82.156.230.140:9000/xiaoyi/avatars/filename.jpg"
}
```
- **错误码**：
  - 400: 无效的文件类型
  - 401: 未授权
  - 500: 上传失败

### 4.2 文件访问说明
- 文件访问基础URL: `http://82.156.230.140:9000`
- 存储桶: `xiaoyi`
- 文件夹结构:
  - `/avatars`: 用户头像
  - `/course`: 课程相关文件
- 完整URL格式: `http://82.156.230.140:9000/xiaoyi/{folder}/{filename}`

### 4.3 文件命名规则
- 上传的文件会自动重命名为: `{timestamp}_{original_filename}`
- 示例: `20240119_111055_avatar.jpg`

### 4.4 注意事项
1. 头像上传大小限制：2MB
2. 支持的图片格式：jpg、jpeg、png
3. 文件URL可直接访问，无需认证
4. 建议在客户端对图片进行压缩后再上传

## 5. 错误处理
所有接口的错误响应格式：
```json
{
    "detail": "错误信息描述"
}
```

### 状态码说明
- 200: 请求成功
- 400: 请求参数错误
- 401: 未登录或token失效
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误

## 6. 注意事项
1. 所有请求必须携带token（除了登录接口）
2. token失效需要重新登录获取
3. 课程颜色使用十六进制颜色码，如 "#FF5733"
4. 时间段说明：
   - 1-2节：上午第一大节
   - 3-4节：上午第二大节
   - 5-6节：下午第一大节
   - 7-8节：下午第二大节
   - 9节：晚课