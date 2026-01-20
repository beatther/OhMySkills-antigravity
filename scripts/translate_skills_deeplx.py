#!/usr/bin/env python3
"""
Oh My Skills - DeepL (DeepLX) 高质量翻译脚本
利用 DeepLX 接口进行更通顺的段落级翻译
"""

import json
import time
import re
import requests
import random
from pathlib import Path

# DeepLX 接口地址列表 (可以使用公共节点，或者您自己在本地部署的 localhost:1188)
# 这里列出几个常见的公共端点，脚本会尝试轮询
DEEPLX_ENDPOINTS = [
    "https://api.deeplx.org/translate",
    "https://deeplx.vercel.app/translate",
    # 如果您在本地运行了 DeepLX (docker run -p 1188:1188 missuo/deeplx)，请解开下面这行
    # "http://localhost:1188/translate",
]

INPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills_raw.json"
OUTPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills.json"
CACHE_FILE = Path(__file__).parent / "translation_cache_deeplx.json"

# 加载缓存
cache = {}
if CACHE_FILE.exists():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except:
        pass

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def translate_with_deepl(text: str) -> str:
    """使用 DeepLX 接口翻译"""
    if not text or not text.strip():
        return text
    
    # 检查缓存
    if text in cache:
        return cache[text]
    
    # 尝试轮询接口
    payload = {
        "text": text,
        "source_lang": "EN",
        "target_lang": "ZH"
    }
    
    for endpoint in DEEPLX_ENDPOINTS:
        try:
            time.sleep(1 + random.random()) # 随机延时防封
            resp = requests.post(endpoint, json=payload, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 200 and data.get("data"):
                    result = data["data"]
                    # 成功！
                    print(f"    ✅ DeepL 翻译成功: {result[:20]}...")
                    cache[text] = result
                    save_cache()
                    return result
        except Exception as e:
            print(f"    ⚠️ 端点 {endpoint} 失败: {e}")
            continue
            
    print(f"    ❌ 所有 DeepLX 端点均失败，保留原文")
    return text

def translate_markdown_body(body: str) -> str:
    """
    智能翻译 Markdown 正文
    策略：按段落拆分，保护代码块
    """
    if not body:
        return ""
        
    # 1. 保护代码块
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    text_safe = re.sub(r'```[\s\S]*?```', save_code_block, body)
    
    # 2. 保护行内代码
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(0))
        return f"__INLINE_CODE_{len(inline_codes)-1}__"
    
    text_safe = re.sub(r'`[^`\n]+`', save_inline_code, text_safe)
    
    # 3. 按行/段落翻译
    lines = text_safe.split('\n')
    translated_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 跳过空行和纯符号行
        if not line_stripped or re.match(r'^[-=*_#\s]+$', line_stripped):
            translated_lines.append(line)
            continue
        
        # 识别标题
        header_match = re.match(r'^(#+)\s+(.*)', line)
        if header_match:
            level = header_match.group(1)
            content = header_match.group(2)
            # 翻译标题内容
            trans = translate_with_deepl(content)
            translated_lines.append(f"{level} {trans}")
            continue
            
        # 识别列表
        list_match = re.match(r'^([-*]|\d+\.)\s+(.*)', line)
        if list_match:
            marker = list_match.group(1)
            content = list_match.group(2)
            trans = translate_with_deepl(content)
            translated_lines.append(f"{marker} {trans}")
            continue

        # 普通文本
        # 为了提高 DeepL 效果，最好是整段翻译，但这里为了保持 Markdown 结构，按行处理比较安全
        # 也可以尝试把连续的文本行合并翻译，但逻辑较复杂，先按行
        trans = translate_with_deepl(line)
        translated_lines.append(trans)
        
    result = '\n'.join(translated_lines)
    
    # 4. 还原占位符
    for i, code in enumerate(inline_codes):
        result = result.replace(f"__INLINE_CODE_{i}__", code)
        
    for i, block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", block)
        
    return result

def main():
    print("🚀 Oh My Skills - 启动 DeepL (DeepLX) 高质量翻译")
    print("================================================")
    
    if not INPUT_FILE.exists():
        return
        
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        skills = json.load(f)
        
    translated_skills = []
    total = len(skills)
    
    for i, skill in enumerate(skills):
        print(f"[{i+1}/{total}] 处理: {skill.get('name')}")
        translated = skill.copy()
        
        # 1. 描述
        if "description" in skill:
            translated["description_zh"] = translate_with_deepl(skill["description"])
            
        # 2. 正文
        if "body" in skill:
            translated["body_zh"] = translate_markdown_body(skill["body"])
            
        # 3. 简单的分类映射 (保留之前的)
        cat_map = {
            "development": "开发工具", "workflow": "工作流", "testing": "测试",
            "documentation": "文档", "backend": "后端", "frontend": "前端",
        }
        if "category" in skill:
            cat = skill["category"].lower()
            translated["category_zh"] = cat_map.get(cat, skill["category"])
            
        translated["name_zh"] = translate_with_deepl(skill.get("name"))
        
        translated_skills.append(translated)
        
        # 定期保存
        if (i+1) % 5 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(translated_skills + skills[i+1:], f, ensure_ascii=False, indent=2)
                
    # 最终保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_skills, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
