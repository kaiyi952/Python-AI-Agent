from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import base64
import requests
from simple_chef import generate_recipe, generate_image, save_recipe
from openai import OpenAI
from dotenv import load_dotenv
import time
import json

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def index():
    # 提供HTML页面
    return send_from_directory('.', 'web_interface.html')

def generate_recipe_image(recipe_name, recipe_description):
    """使用OpenAI DALL-E 3生成食谱图片"""
    try:
        # 构建提示词，包含菜名和菜品描述
        prompt = f"一盘美味可口的{recipe_name}，高清专业美食摄影，顶视角，光线明亮，摆盘精美，背景简洁。{recipe_description}"
        
        print(f"正在为{recipe_name}生成真实图片...")
        
        # 调用DALL-E 3 API生成图片
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # 获取图片URL
        image_url = response.data[0].url
        print(f"✅ 图片生成成功!")
        
        # 保存图片到本地
        try:
            img_data = requests.get(image_url).content
            # 创建images目录
            os.makedirs("images", exist_ok=True)
            # 生成文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"images/{recipe_name.replace(' ', '_')}_{timestamp}.png"
            # 保存图片
            with open(filename, 'wb') as handler:
                handler.write(img_data)
            print(f"✅ 图片已保存至: {filename}")
            
            # 返回本地图片路径和原始URL
            return {
                "local_path": filename,
                "url": image_url
            }
        except Exception as e:
            print(f"❌ 保存图片失败: {str(e)}")
            # 如果保存失败，仍然返回在线URL
            return {
                "url": image_url
            }
        
    except Exception as e:
        print(f"❌ 图片生成失败: {str(e)}")
        # 使用备用方法生成图片URL
        fallback_url = generate_image(recipe_name)
        return {
            "url": fallback_url,
            "fallback": True
        }

@app.route('/api/generate-recipe', methods=['POST'])
def api_generate_recipe():
    try:
        # 获取请求数据
        data = request.json
        ingredients = data.get('ingredients', '')
        cuisine_type = data.get('cuisine_type', '')
        special_requirements = data.get('special_requirements', '')
        generate_ai_image = data.get('generate_ai_image', True)  # 是否生成AI图片的标志
        
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
        
        # 解析食谱内容提取结构化数据
        ingredients_list = []
        steps_list = []
        tips_list = []
        prep_time = "15"
        cook_time = "30"
        recipe_description = ""
        
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
        
        # 构建菜品描述，用于图像生成
        recipe_description = f"使用{', '.join(ingredients_list[:3])}等材料制作的{cuisine_type}菜品。"
        
        # 根据用户选择决定是否使用AI生成图片
        if generate_ai_image:
            # 使用DALL-E生成更真实的食谱图片
            image_result = generate_recipe_image(recipe_name, recipe_description)
            image_url = image_result.get('url')
            local_image_path = image_result.get('local_path', '')
        else:
            # 使用Unsplash随机图片
            image_url = generate_image(recipe_name)
            local_image_path = ""
        
        # 保存食谱
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # 返回结构化数据
        return jsonify({
            'name': recipe_name,
            'ingredients': ingredients_list,
            'steps': steps_list,
            'tips': tips_list,
            'prepTime': prep_time,
            'cookTime': cook_time,
            'imageUrl': image_url,
            'localImagePath': local_image_path,
            'markdown': recipe_markdown,
            'savedFile': saved_file,
            'aiImageGenerated': generate_ai_image
        })
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'error': f'生成食谱时出错: {str(e)}'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    # 确保recipes和images目录存在
    os.makedirs("recipes", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    app.run(debug=True, port=5000) 