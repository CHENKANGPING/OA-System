#!/bin/bash

echo "开始部署OA系统..."

# 停止现有容器
docker-compose down

# 清理旧镜像
docker system prune -f

# 构建并启动服务
docker-compose up --build -d

# 等待数据库启动
echo "等待数据库启动..."
sleep 30

# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户（可选）
# docker-compose exec backend python manage.py createsuperuser

# 收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput

echo "部署完成！"
echo "前端访问地址: http://localhost"
echo "后端API地址: http://localhost:8000"