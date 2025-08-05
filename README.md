# OA办公自动化系统

这是一个基于Django + Vue.js的办公自动化系统，包含用户认证、请假管理等功能。

## 项目结构

```
OA/
├── back/           # Django后端
│   ├── HiiaenOAback/   # Django项目配置
│   ├── apps/           # Django应用
│   │   ├── oaauth/     # 用户认证模块
│   │   └── absent/     # 请假管理模块
│   └── manage.py       # Django管理脚本
└── front/          # Vue.js前端
    └── oafront/        # Vue项目
        ├── src/        # 源代码
        ├── public/     # 静态资源
        └── package.json # 依赖配置
```

## 技术栈

### 后端
- Python 3.x
- Django
- Django REST Framework

### 前端
- Vue.js 3
- Vite
- Vue Router
- Pinia (状态管理)

## 快速开始

### 后端启动

1. 进入后端目录
```bash
cd back
```

2. 安装依赖
```bash
pip install django djangorestframework django-cors-headers
```

3. 运行迁移
```bash
python manage.py migrate
```

4. 启动开发服务器
```bash
python manage.py runserver
```

### 前端启动

1. 进入前端目录
```bash
cd front/oafront
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

## 功能模块

- 用户认证登录
- 请假申请管理
- 请假审批流程

## 开发说明

- 后端API接口遵循RESTful规范
- 前端使用组件化开发
- 支持跨域请求配置

## 许可证

MIT License