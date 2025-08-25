# OA办公自动化系统

这是一个基于Django + Vue.js的办公自动化系统，包含用户认证、请假管理、通知公告、员工管理等功能。

## 项目结构

```
OA-System/
├── back/                   # Django后端
│   ├── HiiaenOAback/      # Django项目配置
│   │   ├── settings.py    # 项目设置
│   │   ├── urls.py        # 主路由配置
│   │   ├── celery.py      # Celery异步任务配置
│   │   └── wsgi.py        # WSGI配置
│   ├── apps/              # Django应用
│   │   ├── oaauth/        # 用户认证模块
│   │   ├── absent/        # 请假管理模块
│   │   ├── inform/        # 通知公告模块
│   │   ├── staff/         # 员工管理模块
│   │   ├── image/         # 图片上传模块
│   │   └── home/          # 首页数据模块
│   ├── utlis/             # 工具类
│   │   └── aeser.py       # AES加密工具
│   ├── templates/         # 模板文件
│   ├── requirements.txt   # Python依赖
│   └── manage.py          # Django管理脚本
└── front/                 # Vue.js前端
    └── oafront/           # Vue项目
        ├── src/           # 源代码
        ├── public/        # 静态资源
        └── package.json   # 依赖配置
```

## 技术栈

### 后端
- **Python 3.x** - 编程语言
- **Django 4.2.23** - Web框架
- **Django REST Framework** - API开发框架
- **MySQL** - 数据库
- **Celery** - 异步任务队列
- **Redis** - 缓存和消息代理
- **JWT** - 身份认证
- **Pandas** - 数据处理

### 前端
- **Vue.js 3** - 前端框架
- **Vite** - 构建工具
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Element Plus** - UI组件库

## 环境要求

- Docker 20.0+
- Docker Compose 2.0+

## 快速部署

### 使用一键部署脚本

本项目提供了自动化部署脚本，可以一键部署整个系统。

#### 1. 克隆项目

```bash
git clone <repository-url>
cd OA-System
```

#### 2. 运行部署脚本

**Linux/macOS:**
```bash
# 给脚本添加执行权限
sudo chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

**Windows (Git Bash):**
```bash
# 运行部署脚本
bash deploy.sh
```

**Windows (PowerShell):**
```powershell
# 使用WSL或Git Bash运行
wsl bash deploy.sh
```

#### 3. 访问系统

部署脚本会自动完成以下操作：
- 检查Docker服务状态
- 停止现有容器并清理系统
- 构建并启动所有服务
- 等待MySQL和Redis启动完成
- 执行数据库迁移
- 收集静态文件
- 显示服务状态

等待部署完成后（约2-3分钟），系统会自动完成数据初始化：

- **前端地址**: http://localhost
- **后端API**: http://localhost/api/

### 手动部署（可选）

如果您需要手动控制部署过程，也可以使用以下命令：

```bash
# 构建并启动所有服务
docker compose up --build -d

# 查看服务状态
docker compose ps
```

#### 3. 访问系统

等待所有服务启动完成后（约1-2分钟），系统会自动完成数据初始化：

- **前端地址**: http://localhost
- **后端API**: http://localhost/api/

### 服务架构

Docker Compose包含以下服务：

- **frontend**: Nginx + Vue.js前端 (端口: 80)
- **backend**: Django后端API (内部端口: 8000)
- **mysql**: MySQL数据库 (内部端口: 3306)
- **redis**: Redis缓存 (内部端口: 6379)

### 默认账户

初始化完成后，可使用以下账户登录：

| 邮箱 | 密码 | 角色 | 部门 |
|------|------|------|------|
| dongdong@qq.com | 111111 | 超级用户 | 董事会 |
| duoduo@qq.com | 111111 | 超级用户 | 董事会 |
| zhangsan@qq.com | 111111 | 普通用户 | 产品开发部 |
| lisi@qq.com | 111111 | 普通用户 | 运营部 |
| wangwu@qq.com | 111111 | 普通用户 | 人事部 |
| zhaoliu@qq.com | 111111 | 普通用户 | 财务部 |
| sunqi@qq.com | 111111 | 普通用户 | 销售部 |

## 使用教程

### 1. 系统登录

1. 打开浏览器访问 `http://localhost`
2. 使用默认账户登录（见上方默认账户表格）
3. 首次登录需要激活账户

### 2. 用户管理

#### 2.1 添加员工

1. 进入「员工管理」页面
2. 点击「添加员工」按钮
3. 填写员工信息：
   - 真实姓名
   - 邮箱地址
   - 电话号码
   - 所属部门
4. 系统将自动发送激活邮件给新员工

#### 2.2 批量导入员工

1. 下载员工信息模板
2. 按模板格式填写员工信息
3. 上传Excel文件进行批量导入

#### 2.3 员工状态管理

- **未激活**：新注册用户，需要通过邮件激活
- **已激活**：正常使用状态
- **已锁定**：禁止登录状态

### 3. 请假管理

#### 3.1 申请请假

1. 进入「请假申请」页面
2. 填写请假信息：
   - 请假标题
   - 请假类型（事假、病假、年假等）
   - 请假时间（开始日期-结束日期）
   - 请假原因
3. 提交申请，等待审批

#### 3.2 审批请假

1. 管理员进入「请假审批」页面
2. 查看待审批的请假申请
3. 选择「通过」或「拒绝」
4. 填写审批意见
5. 提交审批结果

#### 3.3 请假状态

- **审批中**：刚提交的申请，等待审批
- **已通过**：审批通过的申请
- **已拒绝**：审批拒绝的申请

### 4. 通知公告

#### 4.1 发布公告

1. 进入「通知公告」页面
2. 点击「发布公告」
3. 填写公告信息：
   - 公告标题
   - 公告内容
   - 发布范围（全公司或指定部门）
4. 发布公告

#### 4.2 查看公告

1. 员工可在首页查看最新公告
2. 点击公告标题查看详细内容
3. 系统会记录阅读状态

### 5. 数据统计

#### 5.1 首页仪表板

- 各部门员工数量统计
- 最新请假申请
- 最新通知公告
- 数据可视化图表

#### 5.2 报表导出

- 员工信息报表
- 请假统计报表
- 支持Excel格式导出

## API接口文档

### 认证接口

- `POST /oaauth/login/` - 用户登录
- `POST /oaauth/reset/password/` - 重置密码
- `GET /oaauth/userinfo/` - 获取用户信息

### 请假接口

- `GET /absent/absent/` - 获取请假列表
- `POST /absent/absent/` - 创建请假申请
- `PUT /absent/absent/{id}/` - 更新请假申请
- `GET /absent/absenttype/` - 获取请假类型

### 通知接口

- `GET /inform/inform/` - 获取通知列表
- `POST /inform/inform/` - 创建通知
- `POST /inform/read/` - 标记已读

### 员工管理接口

- `GET /staff/staff/` - 获取员工列表
- `POST /staff/add/` - 添加员工
- `POST /staff/upload/` - 批量导入员工
- `POST /staff/active/{uid}/` - 激活员工账户

## 常见问题

### Q1: 数据库连接失败

**A:** 检查以下配置：
- MySQL服务是否启动
- 数据库用户名密码是否正确
- 数据库是否存在
- 防火墙设置

### Q2: 邮件发送失败

**A:** 检查以下配置：
- SMTP服务器设置
- 邮箱授权码配置
- Celery服务是否启动

### Q3: 前端无法访问后端API

**A:** 检查以下配置：
- 后端服务是否启动
- CORS跨域配置
- API地址配置

### Q4: 文件上传失败

**A:** 检查以下配置：
- 文件大小限制
- 文件类型限制
- 存储路径权限

## 常用Docker命令

```bash
# 查看服务日志
docker compose logs -f [service_name]

# 重启服务
docker compose restart [service_name]

# 停止所有服务
docker compose down

# 停止并删除数据卷
docker compose down -v

# 进入容器
docker compose exec [service_name] bash

# 查看数据库
docker compose exec mysql mysql -u root -p123456 hiiaenoa
```

## 数据持久化

项目配置了数据卷持久化：

- **MySQL数据**: `mysql_data` 卷
- **Redis数据**: `redis_data` 卷
- **上传文件**: `media_data` 卷

## 环境配置

### 数据库配置

默认MySQL配置（可在docker-compose.yml中修改）：
- 数据库名: `hiiaenoa`
- 用户名: `root`
- 密码: `123456`
- 端口: `3306`

### Redis配置

默认Redis配置：
- 端口: `6379`
- 无密码认证

## 故障排除

### 服务启动失败

```bash
# 查看详细日志
docker compose logs backend
docker compose logs mysql

# 检查服务健康状态
docker compose ps
```

### 数据库连接失败

```bash
# 确保MySQL服务完全启动
docker compose logs mysql

# 手动重启backend服务
docker compose restart backend
```

### API访问404/502错误

```bash
# 检查nginx配置
docker compose exec frontend cat /etc/nginx/nginx.conf

# 重启前端服务
docker compose restart frontend
```

### 重新初始化数据

```bash
# 停止服务并清除数据
docker compose down -v

# 重新启动（系统会自动完成数据初始化）
docker compose up --build -d
```

## 生产环境优化

对于生产环境部署，建议进行以下优化：

1. **安全配置**:
   - 修改默认密码
   - 配置HTTPS
   - 设置防火墙规则

2. **性能优化**:
   - 增加资源限制
   - 配置日志轮转
   - 启用数据库优化

3. **监控配置**:
   - 添加健康检查
   - 配置监控告警
   - 设置备份策略

## 开发说明

- 后端API接口遵循RESTful规范
- 前端使用组件化开发
- 支持跨域请求配置
- 使用JWT进行身份认证
- 异步任务使用Celery处理
