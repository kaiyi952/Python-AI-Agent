"""
SmartChef 简化版 - 直接调用OpenAI API
"""
import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 确保recipes目录存在
os.makedirs("recipes", exist_ok=True)

def generate_recipe(ingredients, cuisine_type, special_requirements=None):
    """使用OpenAI API生成食谱"""
    
    print(f"📋 生成{cuisine_type}食谱")
    print(f"食材: {ingredients}")
    if special_requirements:
        print(f"特殊要求: {special_requirements}")
    
    # 构建提示词
    prompt = f"""请根据以下食材创建一个详细的{cuisine_type}食谱:
    
    可用食材: {ingredients}
    
    {'特殊要求: ' + special_requirements if special_requirements else ''}
    
    请提供:
    1. 有创意的菜名
    2. 详细的食材清单(包括数量)
    3. 准备和烹饪的详细步骤
    4. 烹饪技巧和窍门
    5. 预计准备和烹饪时间
    
    请使用Markdown格式，并确保食谱符合{cuisine_type}的风格。
    """
    
    try:
        # 调用OpenAI API
        print("🤖 正在调用OpenAI API生成食谱...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位专业厨师，擅长根据现有食材创造美味的食谱。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # 提取生成的食谱
        recipe_markdown = response.choices[0].message.content.strip()
        
        # 计算并显示API调用时间
        elapsed_time = time.time() - start_time
        print(f"✅ 食谱生成完成! (用时: {elapsed_time:.2f}秒)")
        
        return recipe_markdown
        
    except Exception as e:
        print(f"❌ OpenAI API调用失败: {str(e)}")
        print("⚠️ 使用预设的模拟数据作为替代...")
        
        # 返回模拟数据
        return generate_mock_recipe(ingredients, cuisine_type, special_requirements)

def generate_mock_recipe(ingredients, cuisine_type, special_requirements=None):
    """当API调用失败时生成模拟食谱数据"""
    
    # 解析食材
    ingredient_list = [i.strip() for i in ingredients.split('，')]
    
    # 根据食材和菜系选择合适的模拟食谱
    if "鸡蛋" in ingredient_list:
        if cuisine_type == "中餐":
            if "牛奶" in ingredient_list:
                return """# 牛奶蒸蛋

## 食材
- 鸡蛋 3个
- 牛奶 200ml
- 盐 1/4茶匙
- 葱花 适量（装饰用）

## 步骤
1. 将鸡蛋打入碗中，搅拌均匀但不要起泡
2. 牛奶加热至温热（不要煮沸）
3. 将温热的牛奶慢慢倒入蛋液中，边倒边搅拌
4. 加入盐调味，继续搅拌均匀
5. 将蛋奶液过筛，去除杂质
6. 将蛋奶液倒入耐热容器中
7. 上锅蒸15分钟（水开后中小火）
8. 出锅前撒上葱花点缀

## 烹饪技巧
- 蒸的过程中不要揭盖，避免表面不平整
- 筛蛋液可以让蒸蛋更加细腻
- 牛奶温度不要太高，避免蛋液提前凝固
- 蒸好后可以滴几滴香油提香

## 时间
- 准备时间：10分钟
- 烹饪时间：15分钟
- 总时间：25分钟

## 营养信息
这道牛奶蒸蛋热量较低，蛋白质含量丰富，非常适合低卡饮食需求。"""
            else:
                return """# 葱花蒸蛋

## 食材
- 鸡蛋 3个
- 清水 240ml
- 盐 1/4茶匙
- 葱花 适量
- 香油 少许

## 步骤
1. 将鸡蛋打入碗中，用筷子搅拌均匀
2. 加入清水和盐，比例约为1:1.3（蛋液:水）
3. 继续搅拌均匀，然后过筛一次
4. 将蛋液倒入碗中，撒上葱花
5. 上锅蒸10-15分钟（水开后转中小火）
6. 出锅后滴几滴香油提香

## 烹饪技巧
- 蒸的过程中不要揭盖，避免表面不平整
- 筛蛋液可以让蒸蛋更加细腻
- 水温不要太烫，避免蛋液提前凝固
- 可以在碗底铺一层保鲜膜，方便取出

## 时间
- 准备时间：5分钟
- 烹饪时间：15分钟
- 总时间：20分钟

## 营养信息
这道葱花蒸蛋热量低，蛋白质含量丰富，是理想的低卡食品。"""
        elif cuisine_type == "西餐":
            return """# 低卡牛奶法式炒蛋

## 食材
- 鸡蛋 2个
- 牛奶 50ml
- 黑胡椒 少许
- 盐 少许
- 橄榄油 5ml
- 欧芹 少许（装饰用）

## 步骤
1. 将鸡蛋打入碗中，加入牛奶、盐和黑胡椒
2. 用叉子轻轻搅拌均匀
3. 平底锅小火加热，倒入橄榄油
4. 倒入蛋液，用橡皮铲不停地搅动
5. 当蛋液变得浓稠但仍然湿润时，关火
6. 余热会继续煮熟蛋液，保持其柔嫩的口感
7. 盛出装盘，撒上欧芹点缀

## 烹饪技巧
- 全程使用小火，避免炒蛋变老
- 不停地搅动可以让蛋液形成细小的蛋花
- 蛋液7分熟时就可以关火，余热会继续煮熟
- 可以加入少量切碎的蔬菜提升营养价值

## 时间
- 准备时间：5分钟
- 烹饪时间：3-5分钟
- 总时间：10分钟

## 营养信息
这道法式炒蛋热量较低，特别是使用少量的橄榄油代替黄油，更适合低卡饮食需求。"""
    
    elif "牛肉" in ingredient_list:
        if cuisine_type == "中餐":
            return """# 低脂清炖牛肉汤

## 食材
- 精瘦牛肉 300克
- 姜片 5片
- 葱段 3段
- 八角 1个
- 料酒 1汤匙
- 盐 适量
- 清水 1500ml

## 步骤
1. 牛肉洗净，切成4厘米见方的块
2. 锅中加入清水，放入牛肉，大火煮沸
3. 撇去浮沫，加入姜片、葱段、八角和料酒
4. 转小火慢炖1.5小时，直至牛肉软烂
5. 加入适量盐调味即可

## 烹饪技巧
- 选择精瘦牛肉部位，减少脂肪摄入
- 炖煮时间要足够长，才能使牛肉软烂
- 可以提前一天炖好，放冷后去除表面凝固的油脂，再加热食用
- 不要添加油脂，利用牛肉本身的鲜味

## 时间
- 准备时间：15分钟
- 烹饪时间：90分钟
- 总时间：105分钟

## 营养信息
清炖牛肉汤不添加额外油脂，选用精瘦牛肉部位，是一道低脂高蛋白的健康菜品。"""
    
    # 默认返回通用食谱
    return f"""# 简易{cuisine_type}健康餐

## 食材
{', '.join('- ' + ing for ing in ingredient_list)}
- 盐 适量
- 黑胡椒 适量

## 步骤
1. 准备所有食材，清洗干净
2. 根据食材特性，选择合适的烹饪方式
3. 控制用油量，尽量采用蒸、煮、炖等低脂烹饪方式
4. 适量调味，注重食材本身的鲜味

## 烹饪技巧
- 减少油盐用量，有助于降低热量摄入
- 保持食材的原汁原味，少加调味料
- 可以添加各种香草增香，减少盐的使用

## 时间
- 准备时间：10分钟
- 烹饪时间：20分钟
- 总时间：30分钟

## 营养信息
这是一道符合低卡要求的健康食谱，注重保留食材营养的同时，减少不必要的热量摄入。"""

def generate_image(dish_name):
    """使用Unsplash生成食物图片URL (因为OpenAI图像生成是付费的)"""
    
    # 简单起见，使用Unsplash随机图片API
    dish_name_escaped = dish_name.replace(" ", "+")
    image_url = f"https://source.unsplash.com/random/800x600/?food,{dish_name_escaped}"
    
    return image_url

def save_recipe(recipe_content, recipe_name=None):
    """保存食谱到文件"""
    
    # 如果没有提供菜名，尝试从内容中提取
    if not recipe_name:
        # 尝试从markdown的标题中提取菜名
        lines = recipe_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                recipe_name = line[2:].strip()
                break
        
        # 如果仍然没有菜名，使用默认名称
        if not recipe_name:
            recipe_name = "美味食谱"
    
    print(f"💾 正在保存食谱: {recipe_name}")
    
    # 创建文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = recipe_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = f"recipes/{safe_name}_{timestamp}.md"
    
    # 添加元数据
    metadata = f"""---
name: {recipe_name}
created_at: {timestamp}
tags: [AI生成]
---

"""
    
    # 获取菜名对应的图片URL
    image_url = generate_image(recipe_name)
    
    # 添加图片到食谱末尾
    recipe_with_image = recipe_content + f"\n\n![{recipe_name}]({image_url})\n"
    
    # 保存到文件
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(metadata + recipe_with_image)
    
    print(f"✅ 食谱已保存至: {filename}")
    return filename

def main():
    """主函数"""
    print("=" * 50)
    print("欢迎使用 SmartChef - 智能食谱助手 (简化版)")
    print("=" * 50)
    
    # 获取用户输入
    print("\n请输入您可用的食材 (用逗号分隔):")
    ingredients = input("> ")
    
    print("\n请选择菜系类型 (如中餐、西餐、日式等):")
    cuisine_type = input("> ")
    
    print("\n请输入特殊要求 (可选，如偏辣、低卡路里等):")
    special_requirements = input("> ")
    if not special_requirements.strip():
        special_requirements = None
    
    print("\n" + "=" * 50)
    print("正在生成您的专属食谱，请稍候...")
    print("=" * 50 + "\n")
    
    # 生成食谱
    recipe_markdown = generate_recipe(ingredients, cuisine_type, special_requirements)
    
    if recipe_markdown:
        # 提取菜名
        recipe_name = None
        lines = recipe_markdown.split('\n')
        for line in lines:
            if line.startswith('# '):
                recipe_name = line[2:].strip()
                break
        
        # 保存食谱
        saved_file = save_recipe(recipe_markdown, recipe_name)
        
        # 打印食谱预览
        print("\n📝 食谱预览:\n")
        preview_lines = recipe_markdown.split('\n')[:15]  # 只显示前15行
        print("\n".join(preview_lines))
        print("...\n[完整食谱请查看保存的文件]")
    else:
        print("❌ 无法生成食谱，请稍后再试。")
    
    print("\n" + "=" * 50)
    print("感谢使用 SmartChef!")
    print("=" * 50)

if __name__ == "__main__":
    main() 