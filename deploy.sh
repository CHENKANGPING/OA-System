#!/bin/bash

set -e  # 遇到错误立即退出

echo "🚀 开始部署OA系统..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker服务"
    exit 1
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker compose down

# 清理旧镜像（可选）
echo "🧹 清理Docker系统..."
docker system prune -f

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker compose up --build -d

# 等待MySQL启动
echo "⏳ 等待MySQL启动..."
for i in {1..30}; do
    if docker compose exec mysql mysqladmin ping -h localhost --silent; then
        echo "✅ MySQL已启动"
        break
    fi
    echo "等待MySQL启动... ($i/30)"
    sleep 2
done

# 检查MySQL是否成功启动
if ! docker compose exec mysql mysqladmin ping -h localhost --silent; then
    echo "❌ MySQL启动失败"
    docker compose logs mysql
    exit 1
fi

# 等待Redis启动
echo "⏳ 等待Redis启动..."
for i in {1..10}; do
    if docker compose exec redis redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis已启动"
        break
    fi
    echo "等待Redis启动... ($i/10)"
    sleep 1
done

# 执行数据库迁移
echo "📊 执行数据库迁移..."
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# 收集静态文件
echo "📁 收集静态文件..."
docker compose exec backend python manage.py collectstatic --noinput

# 检查服务状态
echo "🔍 检查服务状态..."
docker compose ps

echo "✅ 部署完成！"
echo "🌐 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:8000"
echo "📊 查看日志: docker compose logs -f"