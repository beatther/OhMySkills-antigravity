#!/usr/bin/env python3
"""
Oh My Skills - 翻译脚本
为采集的 skills 添加中文翻译
"""

import json
import re
from pathlib import Path

# 技能名称翻译映射
NAME_TRANSLATIONS = {
    "algorithmic-art": "算法艺术",
    "artifacts-builder": "Artifacts 构建器",
    "ask-questions-if-underspecified": "自动追问澄清",
    "backend-development": "后端开发",
    "brand-guidelines": "品牌指南",
    "canvas-design": "Canvas 设计",
    "changelog-generator": "更新日志生成器",
    "code-documentation": "代码文档",
    "code-refactoring": "代码重构",
    "code-review": "代码审查",
    "competitive-ads-extractor": "竞品广告提取器",
    "content-research-writer": "内容研究写作",
    "database-design": "数据库设计",
    "developer-growth-analysis": "开发者增长分析",
    "doc-coauthoring": "文档协作",
    "docx": "Word 文档处理",
    "domain-name-brainstormer": "域名头脑风暴",
    "expo-app-design": "Expo 应用设计",
    "expo-deployment": "Expo 部署",
    "file-organizer": "文件整理器",
    "frontend-design": "前端设计",
    "image-enhancer": "图像增强",
    "internal-comms": "内部沟通",
    "invoice-organizer": "发票整理器",
    "javascript-typescript": "JavaScript/TypeScript",
    "jira-issues": "Jira 问题管理",
    "job-application": "求职申请",
    "lead-research-assistant": "潜客研究助手",
    "llm-application-dev": "LLM 应用开发",
    "mcp-builder": "MCP 构建器",
    "meeting-insights-analyzer": "会议洞察分析",
    "pdf": "PDF 处理",
    "pptx": "PPT 处理",
    "python-development": "Python 开发",
    "qa-regression": "QA 回归测试",
    "raffle-winner-picker": "抽奖器",
    "react-best-practices": "React 最佳实践",
    "skill-creator": "技能创建器",
    "slack-gif-creator": "Slack GIF 制作",
    "theme-factory": "主题工厂",
    "upgrading-expo": "升级 Expo",
    "vercel-deploy": "Vercel 部署",
    "video-downloader": "视频下载器",
    "web-design-guidelines": "网页设计指南",
    "webapp-testing": "Web 应用测试",
    "web-artifacts-builder": "Web Artifacts 构建器",
    "xlsx": "Excel 处理",
}

# 分类翻译
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

INPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills_raw.json"
OUTPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills.json"


def translate_name(name: str) -> str:
    """翻译技能名称"""
    # 先查找精确匹配
    if name in NAME_TRANSLATIONS:
        return NAME_TRANSLATIONS[name]
    
    # 尝试用 id 匹配
    name_lower = name.lower().replace(' ', '-')
    if name_lower in NAME_TRANSLATIONS:
        return NAME_TRANSLATIONS[name_lower]
    
    # 返回原名
    return name


def translate_description(desc: str) -> str:
    """简单翻译描述"""
    if not desc:
        return ""
    
    # 常见短语翻译
    translations = {
        "Use when": "适用于",
        "Creating": "创建",
        "Generate": "生成",
        "Build": "构建",
        "Design": "设计",
        "Automate": "自动化",
        "with seeded randomness": "使用种子随机性",
        "interactive parameter exploration": "交互式参数探索",
        "users request": "用户请求",
        "using code": "使用代码",
        "generative art": "生成艺术",
        "algorithmic art": "算法艺术",
        "flow fields": "流场",
        "particle systems": "粒子系统",
    }
    
    result = desc
    for en, zh in translations.items():
        result = result.replace(en, zh)
    
    return result


def translate_skill(skill: dict) -> dict:
    """为技能添加中文翻译字段"""
    translated = skill.copy()
    
    # 翻译名称
    skill_id = skill.get("id", "")
    original_name = skill.get("name", "")
    translated["name_zh"] = translate_name(skill_id) or translate_name(original_name)
    
    # 翻译描述
    original_desc = skill.get("description", "")
    translated["description_zh"] = translate_description(original_desc)
    
    # 翻译分类
    if "category" in skill:
        cat = skill["category"].lower()
        translated["category_zh"] = CATEGORY_TRANSLATIONS.get(cat, skill["category"])
    
    # body 暂时保持原文（Markdown 内容较长）
    if "body" in skill:
        translated["body_zh"] = skill["body"]
    
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
    
    # 统计翻译情况
    translated_count = sum(1 for s in translated_skills if s.get("name_zh") != s.get("name"))
    print(f"✅ 完成！处理了 {len(translated_skills)} 个技能")
    print(f"   其中 {translated_count} 个有中文名称翻译")
    print(f"   保存至: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
