import langfun as lf
from langfun.core.agentic import action
import os
import requests
from typing import Dict, Any, Optional
import json

class ImageGeneratorAction(lf.agentic.Action):
    """生成食谱图片的工具"""
    
    operation: str  # "generate_image", "enhance_prompt"
    dish_name: str
    dish_description: Optional[str] = None
    cuisine_type: Optional[str] = None
    key_ingredients: Optional[list] = None
    image_style: Optional[str] = None  # "realistic", "artistic", "cartoon", etc.
    
    def call(self, session: lf.agentic.Session, *, lm=None, api_key=None, **kwargs):
        """根据操作类型执行不同的图片生成功能"""
        
        if self.operation == "generate_image":
            return self._generate_image(session, lm=lm, api_key=api_key)
        elif self.operation == "enhance_prompt":
            return self._enhance_prompt(session, lm=lm)
        else:
            return {"error": f"不支持的操作: {self.operation}"}
    
    def _generate_image(self, session: lf.agentic.Session, *, lm=None, api_key=None):
        """生成食谱图片"""
        
        # 构建图片描述
        if self.dish_description:
            description = self.dish_description
        else:
            # 如果没有提供描述，根据菜名和菜系构建基本描述
            cuisine_info = f"{self.cuisine_type}风格的" if self.cuisine_type else ""
            ingredients_info = ""
            if self.key_ingredients and len(self.key_ingredients) > 0:
                ingredients_info = f"，主要材料包括{', '.join(self.key_ingredients)}"
            
            description = f"一道美味的{cuisine_info}{self.dish_name}{ingredients_info}，摆盘精美，色香味俱全。"
        
        # 添加图片风格
        style_info = ""
        if self.image_style:
            if self.image_style == "realistic":
                style_info = "，高清照片风格，逼真的食物摄影"
            elif self.image_style == "artistic":
                style_info = "，艺术风格，富有创意的美食摄影，柔和的光线"
            elif self.image_style == "cartoon":
                style_info = "，卡通风格，可爱的食物插画"
        
        # 完整的图片生成提示词
        image_prompt = f"{description}{style_info}"
        
        # 在实际应用中，这里会调用图片生成API
        # 以下是模拟API调用
        
        # 如果没有API密钥或是测试模式，则返回Unsplash随机图片
        dish_name_escaped = self.dish_name.replace(" ", "+")
        if not api_key:
            image_url = f"https://source.unsplash.com/random/1024x1024/?food,{dish_name_escaped}"
            return {
                "status": "success",
                "image_url": image_url,
                "prompt_used": image_prompt,
                "note": "使用了Unsplash随机图片，因为没有提供API密钥"
            }
        
        # 模拟API调用结果
        image_url = f"https://source.unsplash.com/random/1024x1024/?food,{dish_name_escaped}"
        
        return {
            "status": "success",
            "image_url": image_url,
            "prompt_used": image_prompt
        }
    
    def _enhance_prompt(self, session: lf.agentic.Session, *, lm=None):
        """增强图片生成提示词"""
        
        # 基本信息
        dish_info = f"菜名: {self.dish_name}"
        cuisine_info = f"菜系: {self.cuisine_type}" if self.cuisine_type else "菜系: 未指定"
        ingredients_info = f"主要食材: {', '.join(self.key_ingredients)}" if self.key_ingredients else "主要食材: 未指定"
        description_info = f"描述: {self.dish_description}" if self.dish_description else "描述: 无"
        
        prompt = f"""请基于以下信息，创建一个详细且生动的图片生成提示词，用于生成一道美食的照片:

        {dish_info}
        {cuisine_info}
        {ingredients_info}
        {description_info}
        
        提示词应该:
        1. 详细描述食物的外观、颜色、质地和摆盘
        2. 提及关键食材的视觉特点
        3. 描述适合该菜品的场景和氛围
        4. 包含摄影风格建议(如光线、角度、焦点等)
        
        请直接提供完整的提示词，不要包含解释或其他内容。
        """
        
        try:
            # 调用LLM增强提示词
            enhanced_prompt = session.query(prompt, lm=lm)
            
            return {
                "status": "success",
                "original_dish": self.dish_name,
                "enhanced_prompt": enhanced_prompt
            }
        except Exception as e:
            return {"error": f"增强提示词时出错: {str(e)}"} 