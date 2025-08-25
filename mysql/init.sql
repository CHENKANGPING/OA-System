-- OA系统数据库初始化脚本
-- 设置字符集
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS hiiaenoa DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE hiiaenoa;

-- 这里可以添加其他初始化SQL语句
-- 例如：创建初始用户、设置权限等

SET FOREIGN_KEY_CHECKS = 1;