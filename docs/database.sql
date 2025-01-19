-- 创建数据库
CREATE DATABASE IF NOT EXISTS xiaoyi_schedule DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE xiaoyi_schedule;

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    openid VARCHAR(64) UNIQUE NOT NULL COMMENT '微信openid',
    nickname VARCHAR(64) COMMENT '用户昵称',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    theme_id INT DEFAULT 1 COMMENT '主题ID',
    province VARCHAR(50) COMMENT '省份',
    city VARCHAR(50) COMMENT '城市',
    school VARCHAR(100) COMMENT '学校名称',
    role VARCHAR(16) DEFAULT 'user' COMMENT '用户角色：user/admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '用户表';

-- 课程主表
CREATE TABLE IF NOT EXISTS course_master (
    course_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(64) UNIQUE NOT NULL COMMENT '课程编码',
    course_name VARCHAR(128) NOT NULL COMMENT '课程名称',
    course_type VARCHAR(32) NOT NULL COMMENT '课程类型',
    course_keywords TEXT COMMENT '课程关键词',
    course_enabled TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    creator_id BIGINT NOT NULL COMMENT '创建者ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '课程主表';

-- 用户课程表
CREATE TABLE IF NOT EXISTS course_user (
    course_user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    course_id BIGINT NOT NULL COMMENT '课程ID',
    course_alias VARCHAR(128) COMMENT '课程别名',
    teacher_name VARCHAR(64) COMMENT '教师姓名',
    classroom VARCHAR(128) COMMENT '教室',
    course_color VARCHAR(32) DEFAULT '#1890FF' COMMENT '显示颜色',
    course_remark TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (course_id) REFERENCES course_master(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '用户课程表';

-- 用户课表
CREATE TABLE IF NOT EXISTS user_schedule (
    schedule_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    day_of_week TINYINT NOT NULL COMMENT '星期几(1-7)',
    course_user_id1 BIGINT COMMENT '第1节课',
    course_user_id2 BIGINT COMMENT '第2节课',
    course_user_id3 BIGINT COMMENT '第3节课',
    course_user_id4 BIGINT COMMENT '第4节课',
    course_user_id5 BIGINT COMMENT '第5节课',
    course_user_id6 BIGINT COMMENT '第6节课',
    course_user_id7 BIGINT COMMENT '第7节课',
    course_user_id8 BIGINT COMMENT '第8节课',
    course_user_id9 BIGINT COMMENT '第9节课',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (course_user_id1) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id2) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id3) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id4) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id5) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id6) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id7) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id8) REFERENCES course_user(course_user_id),
    FOREIGN KEY (course_user_id9) REFERENCES course_user(course_user_id),
    UNIQUE KEY `idx_user_day` (user_id, day_of_week)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '用户课表'; 