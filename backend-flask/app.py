from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
from datetime import datetime

# 添加smartChef目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入simple_chef.py中的函数
from smartChef.simple_chef import generate_recipe, generate_image, save_recipe

app = Flask(__name__)
CORS(app)  # 启用CORS以允许前端跨域请求

@app.route('/api/generate-recipe', methods=['POST'])
def api_generate_recipe():
    """API端点，用于生成食谱"""
    try:
        # 解析请求数据
        data = request.json
        ingredients = data.get('ingredients', '')
        cuisine_type = data.get('cuisine_type', '')
        special_requirements = data.get('special_requirements', None)
        
        if not ingredients or not cuisine_type:
            return jsonify({'error': '请提供食材和菜系'}), 400
        
        # 调用simple_chef.py中的函数生成食谱
        recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
        
        # 从markdown中提取菜名
        recipe_name = None
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# '):
                recipe_name = line[2:].strip()
                break
        
        if not recipe_name:
            recipe_name = "美味食谱"
        
        # 生成图片URL
        image_url = generate_image(recipe_name)
        
        # 保存食谱到文件
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # 返回食谱内容和图片URL
        return jsonify({
            'recipe_content': recipe_markdown,
            'image_url': image_url,
            'recipe_name': recipe_name,
            'saved_file': saved_file
        })
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'error': f'生成食谱时出错: {str(e)}'}), 500

@app.route('/api/recipe-history', methods=['GET'])
def get_recipe_history():
    """API端点，获取之前生成的食谱历史"""
    try:
        recipes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'smartChef', 'recipes')
        recipe_files = []
        
        if os.path.exists(recipes_dir):
            for file in os.listdir(recipes_dir):
                if file.endswith('.md'):
                    file_path = os.path.join(recipes_dir, file)
                    metadata = {}
                    recipe_content = ""
                    
                    # 读取食谱文件并提取元数据
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        lines = f.readlines()
                        in_metadata = False
                        
                        for i, line in enumerate(lines):
                            if line.strip() == '---' and i == 0:
                                in_metadata = True
                                continue
                            elif line.strip() == '---' and in_metadata:
                                in_metadata = False
                                continue
                            
                            if in_metadata:
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    metadata[key.strip()] = value.strip()
                            else:
                                recipe_content += line
                    
                    # 构建食谱数据
                    recipe_data = {
                        'filename': file,
                        'name': metadata.get('name', file.split('_')[0]),
                        'created_at': metadata.get('created_at', ''),
                        'tags': metadata.get('tags', '').replace('[', '').replace(']', '').split(','),
                        'excerpt': recipe_content[:200] + '...' if len(recipe_content) > 200 else recipe_content
                    }
                    
                    recipe_files.append(recipe_data)
        
        # 按创建时间排序
        recipe_files.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify(recipe_files)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'error': f'获取食谱历史时出错: {str(e)}'}), 500

if __name__ == '__main__':
    # 确保recipes目录存在
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'smartChef', 'recipes'), exist_ok=True)
    app.run(debug=True, port=5000) 