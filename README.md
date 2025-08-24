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

- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- Redis 6.0+

## 安装与配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd OA-System
```

### 2. 后端配置

#### 2.1 创建虚拟环境

```bash
cd back
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 数据库配置

1. 创建MySQL数据库：
```sql
CREATE DATABASE hiiaenoa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `HiiaenOAback/settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hiiaenoa',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

#### 2.4 运行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.5 初始化数据

```bash
# 初始化部门数据
python manage.py initdeparments

# 初始化请假类型
python manage.py initabsenttype

# 创建超级用户
python manage.py inituser
```

#### 2.6 启动Redis服务

```bash
# Windows (如果安装了Redis)
redis-server

# 或使用Docker
docker run -d -p 6379:6379 redis:alpine
```

#### 2.7 启动Celery Worker（可选）

```bash
# 新开终端窗口
celery -A HiiaenOAback worker -l info
```

#### 2.8 启动后端服务

```bash
python manage.py runserver
```

后端服务将在 `http://127.0.0.1:8000` 启动

### 3. 前端配置

#### 3.1 安装依赖

```bash
cd front/oafront
npm install
```

#### 3.2 配置环境变量

检查 `.env.development` 文件，确保API地址正确：
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

#### 3.3 启动前端服务

```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

## 使用教程

### 1. 系统登录

1. 打开浏览器访问 `http://localhost:5173`
2. 使用初始化的管理员账号登录
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

## 部署说明

### 生产环境部署

1. **后端部署**：
   - 使用Gunicorn作为WSGI服务器
   - 配置Nginx作为反向代理
   - 使用Supervisor管理进程

2. **前端部署**：
   - 执行 `npm run build` 构建生产版本
   - 将dist目录部署到Web服务器

3. **数据库**：
   - 使用生产级MySQL配置
   - 定期备份数据

4. **缓存**：
   - 配置Redis集群
   - 设置合适的缓存策略

## 开发说明

- 后端API接口遵循RESTful规范
- 前端使用组件化开发
- 支持跨域请求配置
- 使用JWT进行身份认证
- 异步任务使用Celery处理
