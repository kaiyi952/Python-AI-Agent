# 智能食谱助手 - 后端

这是智能食谱助手项目的 Flask 后端部分。它调用`simple_chef.py`脚本来生成食谱，并为前端提供 API 服务。

## 项目设置

安装依赖:

```bash
pip install -r requirements.txt
```

启动服务器:

```bash
python app.py
```

## API 端点

### 生成食谱

```
POST /api/generate-recipe
```

请求体:

```json
{
  "ingredients": "土豆，鸡蛋，洋葱",
  "cuisine_type": "中餐",
  "special_requirements": "低卡"
}
```

响应:

```json
{
  "recipe_content": "# 菜品名称\n\n## 食材\n...",
  "image_url": "https://example.com/image.jpg",
  "recipe_name": "菜品名称",
  "saved_file": "recipes/菜品名称_20240101_123456.md"
}
```

### 获取食谱历史

```
GET /api/recipe-history
```

响应:

```json
[
  {
    "filename": "菜品名称_20240101_123456.md",
    "name": "菜品名称",
    "created_at": "20240101_123456",
    "tags": ["AI生成"],
    "excerpt": "# 菜品名称\n\n## 食材\n..."
  }
]
```

## 依赖

- Flask: Web 框架
- flask-cors: 处理跨域请求
- python-dotenv: 环境变量管理

## 注意事项

确保`smartChef/simple_chef.py`文件存在且可访问，因为后端依赖它来生成食谱。
