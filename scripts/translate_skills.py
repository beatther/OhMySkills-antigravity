#!/usr/bin/env python3
"""
Oh My Skills - 翻译脚本
为采集的 skills 添加中文翻译
"""

import json
from pathlib import Path

# 翻译映射（可扩展）
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
}

TAG_TRANSLATIONS = {
    "ui": "界面设计",
    "ux": "用户体验",
    "design": "设计",
    "frontend": "前端",
    "code-review": "代码审查",
    "quality": "质量",
    "security": "安全",
    "git": "Git",
    "version-control": "版本控制",
    "workflow": "工作流",
    "testing": "测试",
    "automation": "自动化",
    "docs": "文档",
    "readme": "README",
    "api": "API",
    "database": "数据库",
    "sql": "SQL",
    "optimization": "优化",
}

INPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills_raw.json"
OUTPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills.json"


def translate_category(category: str) -> str:
    """翻译分类"""
    return CATEGORY_TRANSLATIONS.get(category.lower(), category)


def translate_tags(tags: list) -> list:
    """翻译标签"""
    return [TAG_TRANSLATIONS.get(tag.lower(), tag) for tag in tags]


def translate_skill(skill: dict) -> dict:
    """为技能添加中文翻译字段"""
    translated = skill.copy()
    
    # 翻译分类
    if "category" in skill:
        translated["category_zh"] = translate_category(skill["category"])
    
    # 翻译标签
    if "tags" in skill and skill["tags"]:
        translated["tags_zh"] = translate_tags(skill["tags"])
    
    # 名称和描述暂时保留原文，后续可接入翻译 API
    translated["name_zh"] = skill.get("name", "")
    translated["description_zh"] = skill.get("description", "")
    
    return translated


def main():
    """主函数"""
    print("Oh My Skills - 开始翻译\n")
    
    if not INPUT_FILE.exists():
        print(f"❌ 找不到输入文件: {INPUT_FILE}")
        print("   请先运行 fetch_skills.py 采集数据")
        return
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        skills = json.load(f)
    
    translated_skills = [translate_skill(skill) for skill in skills]
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_skills, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！翻译了 {len(translated_skills)} 个技能")
    print(f"   保存至: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
