# 智能食谱助手

根据用户提供的食材和偏好，智能生成个性化食谱的应用程序。

## 项目结构

- `/smartChef`: 核心 Python 代码
  - `simple_chef.py`: 食谱生成脚本
  - `recipes/`: 保存生成的食谱
- `/frontend-react`: React 前端应用
- `/backend-flask`: Flask 后端 API 服务
- `/frontend`: 原始 HTML/JS 前端(已被 React 前端替代)

## 功能特点

- 基于用户现有食材生成创意食谱
- 支持多种菜系选择
- 可以添加特殊要求（如低卡、素食等）
- 生成美观的图片展示
- 保存历史食谱记录

## 快速开始

### 后端设置

1. 安装依赖:

```bash
cd backend-flask
pip install -r requirements.txt
```

2. 启动 Flask 服务器:

```bash
python app.py
```

服务器将在 http://localhost:5000 运行。

### 前端设置

1. 安装依赖:

```bash
cd frontend-react
npm install
```

2. 启动开发服务器:

```bash
npm start
```

应用将在 http://localhost:3000 运行。

## 技术栈

- 前端: React, Bootstrap, React-Markdown
- 后端: Flask, Python
- AI: OpenAI API

## 注意事项

- 确保在`.env`文件中设置了正确的 API 密钥
- 确保 backend-flask 目录中的 app.py 能够正确找到 smartChef/simple_chef.py
