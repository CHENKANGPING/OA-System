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

# 首先启动数据库服务
echo "🔨 启动数据库服务..."
docker compose up -d mysql redis

# 等待MySQL完全启动并可接受连接
echo "⏳ 等待MySQL完全启动..."
for i in {1..60}; do
    if docker compose exec mysql mysqladmin ping -h localhost --silent 2>/dev/null; then
        # 额外检查数据库是否可以执行查询
        if docker compose exec mysql mysql -u root -p8737 -e "SELECT 1;" >/dev/null 2>&1; then
            echo "✅ MySQL已完全启动并可接受连接"
            break
        fi
    fi
    echo "等待MySQL启动... ($i/60)"
    sleep 2
done

# 检查MySQL是否成功启动
if ! docker compose exec mysql mysqladmin ping -h localhost --silent 2>/dev/null; then
    echo "❌ MySQL启动失败"
    docker compose logs mysql
    exit 1
fi

# 等待Redis完全启动
echo "⏳ 等待Redis完全启动..."
for i in {1..30}; do
    if docker compose exec redis redis-cli ping > /dev/null 2>&1; then
        # 额外检查Redis是否可以执行基本操作
        if docker compose exec redis redis-cli set test_key test_value > /dev/null 2>&1; then
            docker compose exec redis redis-cli del test_key > /dev/null 2>&1
            echo "✅ Redis已完全启动并可接受连接"
            break
        fi
    fi
    echo "等待Redis启动... ($i/30)"
    sleep 1
done

# 检查Redis是否成功启动
if ! docker compose exec redis redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis启动失败"
    docker compose logs redis
    exit 1
fi

# 数据库服务完全就绪后，构建并启动后端服务
echo "🔨 数据库服务就绪，开始构建并启动后端服务..."
docker compose build backend celery

# 启动后端和Celery服务
echo "🚀 启动后端服务..."
docker compose up -d backend celery

# 等待后端服务启动
echo "⏳ 等待后端服务启动..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health/ > /dev/null 2>&1 || \
       docker compose exec backend python -c "import requests; requests.get('http://localhost:8000')" > /dev/null 2>&1; then
        echo "✅ 后端服务已启动"
        break
    fi
    echo "等待后端服务启动... ($i/30)"
    sleep 3
done

# 最后启动前端服务
echo "🌐 启动前端服务..."
docker compose up -d frontend

# 等待前端服务启动
echo "⏳ 等待前端服务启动..."
for i in {1..20}; do
    if curl -f http://localhost/ > /dev/null 2>&1; then
        echo "✅ 前端服务已启动"
        break
    fi
    echo "等待前端服务启动... ($i/20)"
    sleep 2
done

# 检查所有服务状态
echo "🔍 检查服务状态..."
docker compose ps

# 显示服务健康状态
echo "🏥 检查服务健康状态..."
echo "MySQL状态:"
docker compose exec mysql mysqladmin ping -h localhost 2>/dev/null && echo "✅ MySQL正常" || echo "❌ MySQL异常"

echo "Redis状态:"
docker compose exec redis redis-cli ping 2>/dev/null && echo "✅ Redis正常" || echo "❌ Redis异常"

echo "后端状态:"
curl -f http://localhost:8000/ > /dev/null 2>&1 && echo "✅ 后端正常" || echo "❌ 后端异常"

echo "前端状态:"
curl -f http://localhost/ > /dev/null 2>&1 && echo "✅ 前端正常" || echo "❌ 前端异常"

echo "✅ 部署完成！"
echo "🌐 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:8000"
echo "📊 查看日志: docker compose logs -f [service_name]"
echo "📋 查看所有服务日志: docker compose logs -f"