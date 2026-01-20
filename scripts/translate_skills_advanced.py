#!/usr/bin/env python3
"""
Oh My Skills - 智能翻译脚本
接入 Google Translate (deep-translator) 实现高质量内容的本地翻译
"""

import json
import time
import re
from pathlib import Path
from deep_translator import GoogleTranslator

# 配置
# ==========
BATCH_SIZE = 5      # 每批处理的数量，避免过快
DELAY = 1.0         # 每次 API 调用间隔（秒）
MAX_RETRIES = 3     # 重试次数

INPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills_raw.json"
OUTPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills.json"

# 缓存文件，避免重复翻译
CACHE_FILE = Path(__file__).parent / "translation_cache.json"

# 初始化翻译器
translator = GoogleTranslator(source='auto', target='zh-CN')

# 固定的专业术语映射（有些词 Google 翻译可能不准，强制覆盖）
TERM_MAPPING = {
    "Artifacts": "Artifacts",
    "Claude": "Claude",
    "React": "React",
    "Expo": "Expo",
    "Vercel": "Vercel",
    "Markdown": "Markdown",
    "p5.js": "p5.js",
    "TypeScript": "TypeScript",
    "JavaScript": "JavaScript",
    "Python": "Python",
    "MCP": "MCP",
    "LLM": "LLM",
    "AI": "AI",
    "Agent": "智能体",
}

CATEGORY_TRANSLATIONS = {
    "development": "开发工具",
    "workflow": "工作流",
    "testing": "测试",
    "documentation": "文档",
    "backend": "后端",
    "frontend": "前端",
    "data": "数据",
    "security": "安全",
    "devops": "DevOps",
    "tools": "工具",
    "design": "设计",
    "productivity": "生产力",
}

# 加载缓存
cache = {}
if CACHE_FILE.exists():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except:
        pass

def save_cache():
    """保存翻译缓存"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def smart_translate(text: str) -> str:
    """调用 Google 翻译，带缓存和重试"""
    if not text or not text.strip():
        return text
    
    # 检查缓存
    if text in cache:
        return cache[text]
    
    # 尝试翻译
    for i in range(MAX_RETRIES):
        try:
            # 限制文本长度，避免超出 URL 限制 (Google 免费接口限制约 5000 字符)
            if len(text) > 4000:
                print(f"⚠️ 文本过长 ({len(text)} 字符)，将被截断翻译...")
                translated = translator.translate(text[:4000]) + "..."
            else:
                translated = translator.translate(text)
            
            # 应用术语修正
            for term, replacement in TERM_MAPPING.items():
                translated = translated.replace(term, replacement)
                # 修复可能被翻译的术语（例如 React -> 反应）
                # 这里简单处理，保持某些专有名词大写
            
            # 写入缓存
            cache[text] = translated
            save_cache() # 实时保存防止中断
            
            time.sleep(DELAY) # 礼貌延时
            return translated
        except Exception as e:
            print(f"   ⚠️ 翻译失败 (重试 {i+1}/{MAX_RETRIES}): {e}")
            time.sleep(2)
    
    print(f"   ❌ 最终翻译失败，使用原文")
    return text

def translate_markdown_body(body: str) -> str:
    """
    智能翻译 Markdown 正文
    策略：按段落拆分，分别翻译，保留代码块
    """
    if not body:
        return ""
        
    # 1. 保护代码块 (```...```) 不被翻译
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    # 将代码块替换为占位符
    text_safe = re.sub(r'```[\s\S]*?```', save_code_block, body)
    
    # 2. 保护行内代码 (`...`) 
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(0))
        return f"__INLINE_CODE_{len(inline_codes)-1}__"
    
    text_safe = re.sub(r'`[^`\n]+`', save_inline_code, text_safe)
    
    # 3. 按行拆分翻译（保留 Markdown 结构）
    lines = text_safe.split('\n')
    translated_lines = []
    
    buffer_text = ""
    buffer_indices = []
    
    for idx, line in enumerate(lines):
        line = line.strip()
        
        # 跳过空行、只有符号的行
        if not line or re.match(r'^[-=*_#\s]+$', line):
            translated_lines.append(line) # 保持原样
            continue
            
        # 识别标题
        header_match = re.match(r'^(#+)\s+(.*)', line)
        if header_match:
            level = header_match.group(1)
            content = header_match.group(2)
            trans = smart_translate(content)
            translated_lines.append(f"{level} {trans}")
            continue
            
        # 识别列表项
        list_match = re.match(r'^([-*]|\d+\.)\s+(.*)', line)
        if list_match:
            marker = list_match.group(1)
            content = list_match.group(2)
            trans = smart_translate(content)
            translated_lines.append(f"{marker} {trans}")
            continue
            
        # 普通文本段落
        trans = smart_translate(line)
        translated_lines.append(trans)
    
    # 重新组合
    result = '\n'.join(translated_lines)
    
    # 4. 还原行内代码
    for i, code in enumerate(inline_codes):
        result = result.replace(f"__INLINE_CODE_{i}__", code)
        
    # 5. 还原代码块
    for i, block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", block)
        
    return result

def translate_skill_full(skill: dict, index: int, total: int) -> dict:
    """完整翻译单个技能"""
    print(f"[{index+1}/{total}] 处理技能: {skill.get('name')}...")
    
    translated = skill.copy()
    
    # 1. 翻译名称
    # 名称通常较短，可以直接翻译，或者保持英文 (很多技术名词保留英文更好)
    # 这里我们策略是：如果翻译后差别很大且不全是 ASCII，则保留；
    # 或者对于特定词汇使用映射
    name = skill.get("name", "")
    # 尝试翻译名称，但如果是专有名词可能不需要
    # translated["name_zh"] = smart_translate(name) 
    # 保持混合模式：使用之前的固定映射优先，没有的再 API 翻译
    # 为了演示效果，我们对名称也尝试 API 翻译，如果不满意可以手动改
    name_zh = smart_translate(name)
    # 如果翻译包含英文，尽量保留英文原文作为主，这里只存中文部分
    translated["name_zh"] = name_zh
    
    # 2. 翻译描述 (Description)
    desc = skill.get("description", "")
    if desc:
        print(f"   - 翻译描述...")
        translated["description_zh"] = smart_translate(desc)
    
    # 3. 翻译分类
    cat = skill.get("category", "").lower()
    translated["category_zh"] = CATEGORY_TRANSLATIONS.get(cat, skill.get("category"))
    
    # 4. 翻译正文 (Markdown Body)
    # 这是最耗时的部分
    body = skill.get("body", "")
    if body:
        print(f"   - 翻译详细说明 ({len(body)} 字符)...")
        translated["body_zh"] = translate_markdown_body(body)
    
    return translated

def main():
    print("🌍 Oh My Skills - 启动 Google 智能翻译")
    print("========================================")
    
    if not INPUT_FILE.exists():
        print(f"❌ 找不到输入文件: {INPUT_FILE}")
        return
        
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            skills = json.load(f)
    except Exception as e:
        print(f"❌ 读取 JSON 失败: {e}")
        return

    total_skills = len(skills)
    translated_skills = []
    
    # 只处理前 N 个或者全部，这里是全部
    # 建议先测试前 3 个: skills[:3]
    # 但用户要求生成高质量 json，所以我们跑全量 (可能会花几分钟)
    
    try:
        for i, skill in enumerate(skills):
            translated_skill = translate_skill_full(skill, i, total_skills)
            translated_skills.append(translated_skill)
            
            # 定期保存结果到文件，防止中途 crash
            if (i + 1) % 5 == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(translated_skills + skills[i+1:], f, ensure_ascii=False, indent=2)
                print(f"   💾 进度已保存 ({i+1}/{total_skills})")
                
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断，保存已翻译内容...")
    
    # 最终保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_skills, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 全部完成！")
    print(f"   已生成高质量翻译文件: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
