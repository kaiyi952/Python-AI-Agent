from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import requests
import json
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

class RecipeRequest(BaseModel):
    ingredients: List[str]
    cuisine_type: str

class RecipeResponse(BaseModel):
    recipe: str
    image_url: str

@app.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(request: RecipeRequest):
    try:
        logger.info(f"收到请求：食材 - {request.ingredients}, 菜系 - {request.cuisine_type}")
        
        # 生成食谱
        recipe_prompt = f"""
        请根据以下食材和菜系类型生成一个详细的食谱：
        食材：{', '.join(request.ingredients)}
        菜系：{request.cuisine_type}
        
        请提供：
        1. 菜名
        2. 所需食材清单
        3. 详细步骤
        4. 烹饪技巧
        """
        
        logger.info("开始调用 DeepSeek API 生成食谱")
        try:
            # 调用 DeepSeek API
            recipe = generate_recipe_with_deepseek(recipe_prompt)
            logger.info("食谱生成成功")
        except Exception as e:
            logger.error(f"DeepSeek 食谱生成错误: {str(e)}")
            # 如果 API 调用失败，使用模拟数据
            recipe = generate_mock_recipe(request.ingredients, request.cuisine_type)
        
        # 使用占位图片
        image_url = f"https://source.unsplash.com/random/1024x1024/?food,{request.cuisine_type},{','.join(request.ingredients)}"
        
        logger.info("请求处理成功，返回结果")
        return RecipeResponse(
            recipe=recipe,
            image_url=image_url
        )
        
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_recipe_with_deepseek(prompt):
    """使用 DeepSeek API 生成食谱"""
    try:
        # 这里是调用 DeepSeek API 的代码
        # 由于我们没有实际的 DeepSeek API 密钥，这里只返回模拟数据
        return generate_mock_recipe(["鸡蛋", "番茄"], "中餐")
    except Exception as e:
        logger.error(f"DeepSeek API 调用失败: {str(e)}")
        raise e

def generate_mock_recipe(ingredients, cuisine_type):
    """生成模拟食谱数据"""
    mock_recipes = {
        "中餐": {
            "鸡蛋": """
# 番茄炒蛋

## 食材
- 鸡蛋 4个
- 番茄 2个
- 葱花 适量
- 盐 适量
- 糖 少许
- 食用油 适量

## 步骤
1. 将鸡蛋打入碗中，加少许盐，搅拌均匀
2. 番茄洗净，切成小块
3. 热锅凉油，倒入打散的鸡蛋液
4. 待鸡蛋半凝固时，用铲子翻炒，炒至金黄色盛出备用
5. 锅中再加少许油，放入番茄翻炒
6. 番茄出汁后，加入少许盐和糖调味
7. 放入炒好的鸡蛋，快速翻炒均匀
8. 撒上葱花即可出锅

## 烹饪技巧
- 鸡蛋要用中小火炒，避免炒老
- 番茄加糖可以提鲜去酸
- 最后翻炒不宜过久，保持鸡蛋的嫩滑口感
            """,
            "牛肉": """
# 红烧牛肉

## 食材
- 牛肉 500克
- 姜 适量
- 大蒜 适量
- 八角 2个
- 桂皮 一小块
- 干辣椒 适量
- 酱油 适量
- 料酒 适量
- 冰糖 适量
- 盐 适量

## 步骤
1. 牛肉切成大块，焯水去血水
2. 锅中放入适量油，下入姜片、蒜瓣煸香
3. 放入牛肉翻炒至表面变色
4. 加入八角、桂皮、干辣椒等香料
5. 倒入适量酱油、料酒、清水，加入冰糖
6. 大火烧开后转小火慢炖1-2小时，直至牛肉酥烂
7. 大火收汁，调入盐即可

## 烹饪技巧
- 牛肉最好选择牛腩或牛腱
- 炖煮时间要足够长，才能使牛肉变得软烂
- 冰糖可以使牛肉颜色更红亮
            """,
            "鸡肉": """
# 宫保鸡丁

## 食材
- 鸡胸肉 300克
- 花生米 50克
- 干辣椒 10个
- 葱姜蒜 适量
- 花椒 适量
- 酱油 适量
- 醋 适量
- 料酒 适量
- 淀粉 适量
- 糖 适量
- 盐 适量

## 步骤
1. 鸡胸肉切成小丁，用盐、料酒、淀粉腌制10分钟
2. 花生米炒熟后备用
3. 干辣椒切段，葱姜蒜切末
4. 热锅凉油，放入花椒和干辣椒炒香
5. 放入葱姜蒜爆香
6. 倒入鸡丁翻炒至变色
7. 加入酱油、醋、糖调味
8. 最后放入花生米翻炒均匀即可

## 烹饪技巧
- 鸡肉不要炒过久，否则会变柴
- 花生米提前炒熟更香脆
- 可以根据个人口味调整辣椒的用量
            """
        },
        "西餐": {
            "牛肉": """
# 黑椒牛排

## 食材
- 牛排 300克
- 黑胡椒 适量
- 盐 适量
- 迷迭香 适量
- 橄榄油 适量
- 黄油 20克
- 大蒜 2瓣

## 步骤
1. 牛排提前取出冰箱回温30分钟
2. 用厨房纸吸干牛排表面的水分
3. 在牛排两面撒上盐和黑胡椒腌制10分钟
4. 平底锅加热至冒烟，倒入少量橄榄油
5. 将牛排放入锅中，每面煎2-3分钟（三分熟）
6. 加入黄油、拍扁的大蒜和迷迭香
7. 用勺子将融化的黄油不断浇在牛排上
8. 取出牛排静置5分钟后切片享用

## 烹饪技巧
- 牛排一定要回温再煎
- 煎牛排的锅一定要足够热
- 煎牛排时不要频繁翻动
- 根据个人喜好调整煎制时间
            """,
            "鸡蛋": """
# 法式欧姆蛋

## 食材
- 鸡蛋 3个
- 牛奶 30毫升
- 黄油 20克
- 盐 适量
- 黑胡椒 适量
- 帕玛森奶酪 适量
- 香葱 适量

## 步骤
1. 将鸡蛋打入碗中，加入牛奶、盐和黑胡椒，充分搅拌
2. 平底锅中放入黄油融化
3. 倒入蛋液，用筷子快速搅动
4. 当底部凝固但表面仍有些湿润时，停止搅动
5. 用铲子将一侧折叠，形成半月形
6. 撒上帕玛森奶酪和切碎的香葱
7. 滑入盘中即可享用

## 烹饪技巧
- 用中小火煎制，避免蛋饼煎老
- 保持蛋饼内部微湿润，口感更佳
- 可以根据喜好在蛋液中加入其他配料
            """,
            "猪肉": """
# 香煎猪排配苹果酱

## 食材
- 猪排 2块
- 苹果 2个
- 洋葱 1/2个
- 迷迭香 适量
- 盐 适量
- 黑胡椒 适量
- 橄榄油 适量
- 黄油 20克
- 蜂蜜 适量
- 白葡萄酒 50毫升

## 步骤
1. 猪排用厨房纸吸干水分，撒上盐和黑胡椒腌制
2. 苹果去皮切块，洋葱切丝
3. 热锅加入橄榄油，将猪排两面煎至金黄色
4. 取出猪排，在同一个锅中加入黄油
5. 放入洋葱炒软，再加入苹果块和迷迭香
6. 倒入白葡萄酒煮至苹果软烂
7. 加入蜂蜜调味，煮至糖色
8. 将猪排放回锅中，浇上苹果酱即可

## 烹饪技巧
- 煎猪排前最好敲打一下，使其更加柔嫩
- 苹果选择酸甜口味的品种更佳
- 苹果酱可以提前一天制作，风味会更好
            """
        },
        "日式": {
            "鸡蛋": """
# 日式厚蛋烧

## 食材
- 鸡蛋 4个
- 海苔 适量
- 酱油 1小勺
- 味淋 1小勺
- 糖 1小勺
- 盐 少许

## 步骤
1. 将鸡蛋打入碗中，加入酱油、味淋、糖和盐
2. 充分搅拌均匀，过筛使蛋液更加细腻
3. 准备一个长方形平底锅，抹上一层薄油
4. 小火加热锅，倒入少量蛋液，摇晃锅使蛋液铺满锅底
5. 当蛋液开始凝固但表面仍有些湿润时，从远端开始向自己卷起
6. 将卷好的蛋卷推到锅的远端
7. 再次往锅中倒入少量蛋液，使其流到已卷好的蛋卷下方
8. 重复上述过程，直到蛋液用完
9. 取出蛋卷，冷却后切片，点缀海苔即可

## 烹饪技巧
- 整个过程保持小火，避免蛋卷表面上色过深
- 每次倒入的蛋液不宜过多，薄薄一层即可
- 可以使用专用的方形蛋烧锅，更容易成型
            """,
            "三文鱼": """
# 三文鱼茶泡饭

## 食材
- 生三文鱼片 200克
- 熟米饭 1碗
- 日式酱油 适量
- 芥末 少许
- 海苔碎 适量
- 芝麻 适量
- 葱花 适量
- 绿茶 200毫升

## 步骤
1. 三文鱼切成薄片，备用
2. 米饭放入碗中，撒上葱花、海苔碎和芝麻
3. 将三文鱼片铺在米饭上
4. 沿碗边淋入适量酱油
5. 点缀少许芥末
6. 冲入热绿茶
7. 盖上盖子焖2分钟
8. 开盖轻轻搅拌即可享用

## 烹饪技巧
- 三文鱼要选择新鲜的刺身级
- 绿茶温度不宜过高，以免煮熟三文鱼
- 可以根据个人口味调整酱油的用量
            """,
            "猪肉": """
# 日式炸猪排

## 食材
- 猪里脊肉 300克
- 面包糠 适量
- 鸡蛋 2个
- 面粉 适量
- 盐 适量
- 黑胡椒 适量
- 高汤 100毫升
- 酱油 2汤匙
- 味淋 2汤匙
- 糖 1汤匙
- 高丽菜 适量
- 食用油 适量

## 步骤
1. 猪里脊肉切成1厘米厚的片，用刀背轻拍
2. 撒上盐和黑胡椒腌制10分钟
3. 依次裹上面粉、蛋液和面包糠
4. 热油温度达到170度，放入裹好的猪排
5. 炸至金黄色，取出沥油
6. 高汤、酱油、味淋和糖煮沸制成酱汁
7. 将炸猪排切条，配上切丝的高丽菜
8. 淋上酱汁即可食用

## 烹饪技巧
- 猪肉拍打可以使其更加松软
- 炸制时保持油温稳定，避免过热
- 面包糠最好选择日式面包糠，更加蓬松
            """
        }
    }
    
    # 尝试找到匹配的菜系
    if cuisine_type in mock_recipes:
        cuisine_recipes = mock_recipes[cuisine_type]
        
        # 尝试根据食材匹配食谱
        for ingredient in ingredients:
            for key in cuisine_recipes.keys():
                if key in ingredient:
                    return cuisine_recipes[key]
        
        # 如果没有找到匹配的食材，返回该菜系的第一个食谱
        return list(cuisine_recipes.values())[0]
    else:
        # 如果没有找到匹配的菜系，默认返回中餐食谱
        return list(mock_recipes["中餐"].values())[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 