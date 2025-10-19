"""
ComfyUI-Doubao 节点定义
"""

import json
import requests
import base64
import io
from PIL import Image
import numpy as np
import torch

class VolcengineChatAPI:
    """火山引擎对话(Chat) API节点"""
    
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "doubao-pro"}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 4096}),
            },
            "optional": {
                "image": ("IMAGE", {"default": None}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate_chat"
    CATEGORY = "Doubao"
    
    def generate_chat(self, api_key, model, prompt, system_prompt="", temperature=0.7, max_tokens=1024, image=None):
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        messages = []
        
        # 添加系统消息
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 构建用户消息
        if image is not None:
            # 将ComfyUI图像格式转换为PIL图像
            if len(image.shape) == 4:  # 批量图像
                img_np = (image[0] * 255).cpu().numpy().astype(np.uint8)
                pil_image = Image.fromarray(img_np)
            else:
                img_np = (image * 255).cpu().numpy().astype(np.uint8)
                pil_image = Image.fromarray(img_np)
            
            # 将PIL图像转换为Base64
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # 多模态消息（包含图像）
            user_content = [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}",
                        "detail": "high"
                    }
                }
            ]
            messages.append({
                "role": "user",
                "content": user_content
            })
        else:
            # 纯文本消息
            messages.append({
                "role": "user",
                "content": prompt
            })
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return (result["choices"][0]["message"]["content"],)
            else:
                return ("Error: No response content",)
        except Exception as e:
            return (f"Error: {str(e)}",)


class VolcengineImageGenerationBase:
    """火山引擎图片生成API基类"""
    
    @classmethod
    def get_size_options_4_0(cls):
        """Seedream 4.0系列的尺寸选项（统一保留4.0口径）"""
        return [
            "1K",
            "2K",
            "4K",
            "2048×2048 (1:1)",
            "2304×1728 (4:3)",
            "1728×2304 (3:4)",
            "2560×1440 (16:9)",
            "1440×2560 (9:16)",
            "2496×1664 (3:2)",
            "1664×2496 (2:3)",
            "3024×1296 (21:9)",
            "4096×4096 (1:1)",
        ]

    # 3.0系列已移除，不再提供尺寸选项
    def process_image(self, image):
        """处理ComfyUI图像为Base64编码"""
        if image is None:
            return None
            
        # 将ComfyUI图像格式转换为PIL图像
        if len(image.shape) == 4:  # 批量图像
            img_np = (image[0] * 255).cpu().numpy().astype(np.uint8)
            pil_image = Image.fromarray(img_np)
        else:
            img_np = (image * 255).cpu().numpy().astype(np.uint8)
            pil_image = Image.fromarray(img_np)
        
        # 将PIL图像转换为Base64
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return f"data:image/png;base64,{img_base64}"
    
    def process_images(self, images):
        """处理多个ComfyUI图像为Base64编码列表"""
        if images is None:
            return None
            
        base64_images = []
        
        # 处理批量图像
        for i in range(images.shape[0]):
            img_np = (images[i] * 255).cpu().numpy().astype(np.uint8)
            pil_image = Image.fromarray(img_np)
            
            # 将PIL图像转换为Base64
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_images.append(f"data:image/png;base64,{img_base64}")
        
        return base64_images
    
    def normalize_size(self, size):
        s = str(size).strip()
        # 去掉括号中的比例说明
        if " (" in s:
            s = s.split(" (", 1)[0]
        # 将乘号×或大写X统一替换为小写x
        s = s.replace("×", "x").replace("X", "x")
        return s
    
    def handle_response(self, response):
        """处理API响应并返回ComfyUI期望的IMAGE张量。
        同时兼容两种返回格式：url 与 b64_json。
        """
        try:
            response.raise_for_status()
            result = response.json()

            images = []
            image_sources = []

            # Ark Images API通常在 result["data"] 中返回图片列表
            data_items = result.get("data", [])

            for item in data_items:
                # b64_json 直接解码
                if "b64_json" in item and item["b64_json"]:
                    try:
                        img_bytes = base64.b64decode(item["b64_json"])
                        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                        img_np = np.array(img, dtype=np.float32) / 255.0
                        images.append(img_np)
                        image_sources.append("b64_json")
                    except Exception as _:
                        pass

                # url 下载
                elif "url" in item and item["url"]:
                    try:
                        img_response = requests.get(item["url"])
                        img_response.raise_for_status()
                        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
                        img_np = np.array(img, dtype=np.float32) / 255.0
                        images.append(img_np)
                        image_sources.append(item["url"])
                    except Exception as _:
                        pass

            if len(images) == 0:
                # 尝试其它可能的字段，例如 result["images"]
                fallback_images = result.get("images") or result.get("output")
                if isinstance(fallback_images, list):
                    for b64 in fallback_images:
                        try:
                            if isinstance(b64, str):
                                # 兼容可能带有前缀的 base64
                                if b64.startswith("data:image"):
                                    b64 = b64.split(",", 1)[1]
                                img_bytes = base64.b64decode(b64)
                                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                                img_np = np.array(img, dtype=np.float32) / 255.0
                                images.append(img_np)
                                image_sources.append("inline_b64")
                        except Exception:
                            pass

            if len(images) > 0:
                batch_np = np.stack(images, axis=0)
                # 转换为torch张量，符合ComfyUI的IMAGE类型
                batch_tensor = torch.from_numpy(batch_np).float()
                info = json.dumps({
                    "count": len(images),
                    "sources": image_sources
                }, ensure_ascii=False)
                return (batch_tensor, info)

            # 没有成功解析出图片，返回一个占位图避免下游节点报错
            placeholder = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            err_msg = json.dumps({
                "error": "No images in response",
                "raw": result
            }, ensure_ascii=False)
            return (placeholder, err_msg)
        except Exception as e:
            # 异常时同样返回占位图，附带错误信息
            placeholder = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            return (placeholder, f"Error: {str(e)}")


class VolcengineSeedream4TextToImage(VolcengineImageGenerationBase):
    """火山引擎Seedream 4.0文生图节点"""
    
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "doubao-seedream-4-0-250828", "multiline": False}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "size": (cls.get_size_options_4_0(), {"default": "2048×2048 (1:1)"}),
                "sequential_image_generation": (["auto", "disabled"], {"default": "disabled"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "max_images": ("INT", {"default": 1, "min": 1, "max": 15}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "info",)
    FUNCTION = "generate_image"
    CATEGORY = "Doubao"
    
    def generate_image(self, api_key, model, prompt, size="2048×2048 (1:1)", sequential_image_generation="disabled", seed=-1, watermark=False, max_images=1):
        size_norm = self.normalize_size(size)
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {"model": model, "prompt": prompt, "size": size_norm, "sequential_image_generation": sequential_image_generation, "response_format": "b64_json", "seed": seed, "watermark": watermark}
        if sequential_image_generation == "auto":
            data["sequential_image_generation_options"] = {"max_images": max_images}
        response = requests.post(url, headers=headers, json=data)
        return self.handle_response(response)


class VolcengineSeedream4ImageToImage(VolcengineImageGenerationBase):
    """火山引擎Seedream 4.0图生图节点"""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "doubao-seedream-4-0-250828", "multiline": False}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE", {"default": None}),
                "size": (cls.get_size_options_4_0(), {"default": "2048×2048 (1:1)"}),
                "sequential_image_generation": (["auto", "disabled"], {"default": "disabled"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "max_images": ("INT", {"default": 1, "min": 1, "max": 15}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "info",)
    FUNCTION = "generate_image"
    CATEGORY = "Doubao"
    
    def generate_image(self, api_key, model, prompt, image, size="2048×2048 (1:1)", sequential_image_generation="disabled", seed=-1, watermark=False, max_images=1):
        size_norm = self.normalize_size(size)
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {
            "model": model,
            "prompt": prompt,
            "size": size_norm,
            "sequential_image_generation": sequential_image_generation,
            "image": self.process_image(image),
            "response_format": "b64_json",
            "seed": seed,
            "watermark": watermark,
        }
        if sequential_image_generation == "auto":
            data["sequential_image_generation_options"] = {"max_images": max_images}
        response = requests.post(url, headers=headers, json=data)
        return self.handle_response(response)


class VolcengineSeedream4MultiImageFusion(VolcengineImageGenerationBase):
    """火山引擎Seedream 4.0多图融合节点"""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "doubao-seedream-4-0-250828", "multiline": False}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "images": ("IMAGE", {"default": None}),
                "size": (cls.get_size_options_4_0(), {"default": "2048×2048 (1:1)"}),
                "sequential_image_generation": (["auto", "disabled"], {"default": "disabled"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "max_images": ("INT", {"default": 1, "min": 1, "max": 15}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "info",)
    FUNCTION = "generate_image"
    CATEGORY = "Doubao"
    
    def generate_image(self, api_key, model, prompt, images, size="2048×2048 (1:1)", sequential_image_generation="disabled", seed=-1, watermark=False, max_images=1):
        size_norm = self.normalize_size(size)
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        base64_images = self.process_images(images)
        data = {
            "model": model,
            "prompt": prompt,
            "size": size_norm,
            "sequential_image_generation": sequential_image_generation,
            "image": base64_images,
            "response_format": "b64_json",
            "seed": seed,
            "watermark": watermark,
        }
        if sequential_image_generation == "auto":
            data["sequential_image_generation_options"] = {"max_images": max_images}
        response = requests.post(url, headers=headers, json=data)
        return self.handle_response(response)


class VolcengineSeedream4StreamOutput(VolcengineImageGenerationBase):
    """火山引擎Seedream 4.0流式输出节点（简化为顺序多图）"""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "model": ("STRING", {"default": "doubao-seedream-4-0-250828", "multiline": False}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "size": (cls.get_size_options_4_0(), {"default": "2048×2048 (1:1)"}),
                "sequential_image_generation": (["auto", "disabled"], {"default": "auto"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "max_images": ("INT", {"default": 3, "min": 1, "max": 15}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "info",)
    FUNCTION = "generate_image"
    CATEGORY = "Doubao"
    
    def generate_image(self, api_key, model, prompt, size="2048×2048 (1:1)", sequential_image_generation="auto", seed=-1, watermark=False, max_images=3):
        size_norm = self.normalize_size(size)
        url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {
            "model": model,
            "prompt": prompt,
            "size": size_norm,
            "sequential_image_generation": sequential_image_generation,
            "response_format": "b64_json",
            "seed": seed,
            "watermark": watermark,
        }
        if sequential_image_generation == "auto":
            data["sequential_image_generation_options"] = {"max_images": max_images}
        response = requests.post(url, headers=headers, json=data)
        return self.handle_response(response)



# 节点映射
NODE_CLASS_MAPPINGS = {
    "VolcengineChatAPI": VolcengineChatAPI,
    "VolcengineSeedream4TextToImage": VolcengineSeedream4TextToImage,
    "VolcengineSeedream4ImageToImage": VolcengineSeedream4ImageToImage,
    "VolcengineSeedream4MultiImageFusion": VolcengineSeedream4MultiImageFusion,
    "VolcengineSeedream4StreamOutput": VolcengineSeedream4StreamOutput,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "VolcengineChatAPI": "Doubao Chat（火山引擎对话API）",
    "VolcengineSeedream4TextToImage": "Doubao Seedream4 文生图",
    "VolcengineSeedream4ImageToImage": "Doubao Seedream4 图生图",
    "VolcengineSeedream4MultiImageFusion": "Doubao Seedream4 多图融合",
    "VolcengineSeedream4StreamOutput": "Doubao Seedream4 流式输出",
}