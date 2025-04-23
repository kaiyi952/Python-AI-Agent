# 智能食谱助手

根据用户提供的食材和偏好，智能生成个性化食谱的应用程序。

## 项目结构

- `/smartChef`: 核心 Python 代码
  - `simple_chef.py`: 食谱生成脚本
  - `web_server.py`: Flask Web 服务器
  - `web_interface.html`: 网页界面
  - `recipes/`: 保存生成的食谱
  - `images/`: 保存生成的食谱图片
- `/frontend-react`: React 前端应用
- `/backend-flask`: Flask 后端 API 服务
- `/frontend`: 原始 HTML/JS 前端(已被 React 前端替代)

## 环境设置

1. 复制环境变量示例文件:

```bash
cp .env.example .env
```

2. 编辑`.env`文件，添加您的 OpenAI API 密钥:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**重要:** 切勿将包含真实 API 密钥的`.env`文件提交到 Git 仓库。该文件已在`.gitignore`中被忽略。

## 功能特点

- 基于用户现有食材生成创意食谱
- 支持多种菜系选择
- 可以添加特殊要求（如低卡、素食等）
- 生成美观的图片展示
- 保存历史食谱记录

## 快速开始

### 简单版本（直接运行）

1. 安装依赖:

```bash
pip install -r requirements.txt
```

2. 启动 Web 服务器:

```bash
python smartChef/web_server.py
```

服务器将在 http://localhost:5000 运行。

### 后端设置（高级版本）

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

### 前端设置（高级版本）

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

- 前端: HTML/JS/CSS, React (高级版本)
- 后端: Flask, Python
- AI: OpenAI API (GPT, DALL-E)

## 注意事项

- 确保在`.env`文件中设置了正确的 API 密钥
- 首次运行时会自动创建`recipes`和`images`目录
- 生成的食谱会保存在`recipes`目录中
- 生成的图片会保存在`images`目录中
