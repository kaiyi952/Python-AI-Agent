from flask import Flask, request, jsonify, send_from_directory
import os
import sys
from simple_chef import generate_recipe, generate_image, save_recipe

app = Flask(__name__)

@app.route('/')
def index():
    # 提供HTML页面
    return send_from_directory('.', 'web_interface.html')

@app.route('/api/generate-recipe', methods=['POST'])
def api_generate_recipe():
    try:
        # 获取请求数据
        data = request.json
        ingredients = data.get('ingredients', '')
        cuisine_type = data.get('cuisine_type', '')
        special_requirements = data.get('special_requirements', '')
        
        if not ingredients or not cuisine_type:
            return jsonify({'error': '请提供食材和菜系'}), 400
        
        # 调用simple_chef.py生成食谱
        recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
        
        # 提取菜名
        recipe_name = None
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                recipe_name = line.replace('#', '').strip()
                break
        
        if not recipe_name:
            recipe_name = "美味食谱"
        
        # 生成图片URL
        image_url = generate_image(recipe_name)
        
        # 保存食谱
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # 解析食谱内容提取结构化数据
        ingredients_list = []
        steps_list = []
        tips_list = []
        prep_time = "15"
        cook_time = "30"
        
        section = None
        for line in lines:
            line = line.strip()
            if line.startswith('## 食材') or line.startswith('### 食材'):
                section = 'ingredients'
                continue
            elif line.startswith('## 步骤') or line.startswith('### 步骤') or line.startswith('## 准备') or line.startswith('### 准备'):
                section = 'steps'
                continue
            elif line.startswith('## 烹饪技巧') or line.startswith('### 烹饪技巧'):
                section = 'tips'
                continue
            elif line.startswith('## 预计') or line.startswith('### 预计'):
                section = 'time'
                continue
            elif line.startswith('##') or line.startswith('###'):
                section = None
                continue
                
            if section == 'ingredients' and line.startswith('-'):
                ingredients_list.append(line[1:].strip())
            elif section == 'steps' and (line.startswith('-') or line.startswith('1.') or line.startswith('1、')):
                # 移除数字编号
                step = line
                if line[0].isdigit():
                    parts = line.split('.', 1) if '.' in line else line.split('、', 1)
                    if len(parts) > 1:
                        step = parts[1].strip()
                elif line.startswith('-'):
                    step = line[1:].strip()
                steps_list.append(step)
            elif section == 'tips' and line.startswith('-'):
                tips_list.append(line[1:].strip())
            elif section == 'time' and ('准备时间' in line or '预计时间' in line):
                if '准备时间' in line:
                    prep_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(prep_parts) > 1:
                        prep_time = prep_parts[1].strip().split(' ')[0]
                if '烹饪时间' in line:
                    cook_parts = line.split(':', 1) if ':' in line else line.split('：', 1)
                    if len(cook_parts) > 1:
                        cook_time = cook_parts[1].strip().split(' ')[0]
        
        # 返回结构化数据
        return jsonify({
            'name': recipe_name,
            'ingredients': ingredients_list,
            'steps': steps_list,
            'tips': tips_list,
            'prepTime': prep_time,
            'cookTime': cook_time,
            'imageUrl': image_url,
            'markdown': recipe_markdown,
            'savedFile': saved_file
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 