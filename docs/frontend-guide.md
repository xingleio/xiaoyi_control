# 小怡课表前端开发指南

## 开发环境准备

### 1. 开发工具
- Cursor编辑器
- 微信开发者工具
- Postman（可选，用于API测试）

### 2. 项目配置
```javascript
// config.js
export const config = {
  // 开发环境
  development: {
    baseUrl: 'http://82.156.230.140:8600/api/v1',
    uploadUrl: 'http://82.156.230.140:9000/xiaoyi'
  },
  // 生产环境
  production: {
    baseUrl: 'http://82.156.230.140:8600/api/v1',
    uploadUrl: 'http://82.156.230.140:9000/xiaoyi'
  }
}
```

## API接口说明

### 1. 用户认证

#### 1.1 微信登录
```javascript
// pages/login/login.js
const login = async () => {
  try {
    // 1. 获取微信code
    const { code } = await wx.login()
    
    // 2. 调用后端登录接口
    const res = await wx.request({
      url: `${baseUrl}/auth/wx-login`,
      method: 'POST',
      data: { code }
    })
    
    // 3. 保存token
    wx.setStorageSync('token', res.data.token)
    
    // 4. 保存用户信息
    wx.setStorageSync('userInfo', res.data.user)
  } catch (error) {
    console.error('登录失败:', error)
  }
}
```

#### 1.2 上传头像
```javascript
// components/avatar-upload/index.js
const uploadAvatar = async () => {
  try {
    // 1. 选择图片
    const { tempFilePaths } = await wx.chooseImage({
      count: 1,
      sizeType: ['compressed']
    })
    
    // 2. 上传图片
    const res = await wx.uploadFile({
      url: `${baseUrl}/auth/upload-avatar`,
      filePath: tempFilePaths[0],
      name: 'file',
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      }
    })
    
    // 3. 更新头像URL
    const { url } = JSON.parse(res.data)
    this.setData({ avatarUrl: url })
  } catch (error) {
    console.error('上传失败:', error)
  }
}
```

### 2. 请求封装

#### 2.1 请求拦截器
```javascript
// utils/request.js
const request = (options) => {
  const token = wx.getStorageSync('token')
  
  return new Promise((resolve, reject) => {
    wx.request({
      ...options,
      url: `${baseUrl}${options.url}`,
      header: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json',
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 401) {
          // token失效，重新登录
          wx.redirectTo({ url: '/pages/login/login' })
          return
        }
        resolve(res.data)
      },
      fail: reject
    })
  })
}
```

### 3. 常见问题处理

#### 3.1 跨域问题
- 在微信开发者工具中勾选"不校验合法域名"
- 生产环境需要在小程序管理后台添加域名白名单：
  - `http://82.156.230.140:8600`
  - `http://82.156.230.140:9000`

#### 3.2 文件上传
- 图片大小限制：2MB
- 支持格式：jpg、jpeg、png
- 建议上传前压缩图片

#### 3.3 状态码说明
- 200: 请求成功
- 400: 请求参数错误
- 401: 未登录或token失效
- 403: 无权限
- 404: 资源不存在
- 500: 服务器错误

## 开发流程建议

1. 环境配置
   - 克隆前端项目
   - 配置开发环境
   - 测试API连接

2. 功能开发
   - 实现登录功能
   - 开发课表管理
   - 实现文件上传
   - 添加错误处理

3. 测试验证
   - 接口联调
   - 功能测试
   - 性能优化

## 注意事项

1. 安全性
   - 不要在代码中硬编码敏感信息
   - 所有请求需要携带token
   - 文件上传需要验证大小和类型

2. 性能优化
   - 合理使用缓存
   - 图片压缩后上传
   - 避免频繁请求

3. 用户体验
   - 添加加载提示
   - 友好的错误提示
   - 合理的页面跳转

## 调试技巧

1. 使用Cursor调试
   - 设置断点
   - 查看网络请求
   - 检查变量值

2. 微信开发者工具
   - 开启调试模式
   - 查看控制台日志
   - 使用Network面板

## 联系方式

如遇到问题，请联系后端开发人员：
- 邮箱：[邮箱地址]
- 微信：[微信号] 