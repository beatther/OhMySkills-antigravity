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

# 常用 Markdown 标题和内容翻译映射
BODY_TRANSLATIONS = {
    # 标题
    r"^#\s+(.*)": r"# \1", 
    r"^##\s+Overview": "## 概述",
    r"^##\s+Introduction": "## 介绍",
    r"^##\s+Description": "## 描述",
    r"^##\s+Capabilities": "## 能力",
    r"^##\s+Features": "## 功能特性",
    r"^##\s+Usage": "## 使用方法",
    r"^##\s+Examples": "## 示例",
    r"^##\s+Instructions": "## 说明",
    r"^##\s+Requirements": "## 要求",
    r"^##\s+Installation": "## 安装",
    r"^##\s+Configuration": "## 配置",
    r"^##\s+Parameters": "## 参数",
    r"^##\s+Output": "## 输出",
    r"^##\s+Workflow": "## 工作流程",
    r"^##\s+Best Practices": "## 最佳实践",
    r"^##\s+Notes": "## 注意事项",
    
    # 常用短语
    "When to use this skill": "何时使用此技能",
    "Use this skill when": "当...时使用此技能",
    "This skill allows you to": "此技能允许你",
    "The following example": "以下示例",
    "For example": "例如",
    "In this case": "在这种情况下",
    "Make sure to": "请确保",
    "You can": "你可以",
    "Input": "输入",
    "Output": "输出",
    "Steps": "步骤",
    "Prerequisites": "先决条件",
    "Goal": "目标",
    "Context": "上下文",
    "Action": "操作",
    "Result": "结果",
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

INPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills_raw.json"
OUTPUT_FILE = Path(__file__).parent.parent / "public" / "data" / "skills.json"


def translate_name(name: str) -> str:
    if name in NAME_TRANSLATIONS:
        return NAME_TRANSLATIONS[name]
    name_lower = name.lower().replace(' ', '-')
    if name_lower in NAME_TRANSLATIONS:
        return NAME_TRANSLATIONS[name_lower]
    return name

def translate_description(desc: str) -> str:
    if not desc: return ""
    # 简单替换仍然是占位符，实际场景需要接入翻译API
    # 这里通过模拟翻译让前端展示出效果
    translations = {
        "Use when": "适用于",
        "Creating": "创建",
        "Generate": "生成",
        "Build": "构建",
        "Design": "设计",
        "Automate": "自动化",
        "using": "使用",
        "with": "包含",
        "and": "和",
        "for": "用于",
        "Create": "创建",
        "Clarify": "澄清",
        "requirements": "需求",
        "before": "在...之前",
        "implementing": "实现",
    }
    result = desc
    for en, zh in translations.items():
        # 简单的单词替换，避免破坏句子结构（仅作演示用）
        result = result.replace(f" {en} ", f" {zh} ")
        if result.startswith(en):
            result = result.replace(en, zh, 1)
            
    return result

def translate_body(text: str) -> str:
    """简单翻译 Markdown 正文"""
    if not text: return ""
    
    result = text
    
    # 翻译标题
    for pattern, replacement in BODY_TRANSLATIONS.items():
        if pattern.startswith("^"):
            # 正则替换标题
            result = re.sub(pattern, replacement, result, flags=re.MULTILINE)
        else:
            # 普通替换
            result = result.replace(pattern, replacement)
            
    # 简单的文本替换（为了演示双语效果）
    common_terms = {
        " users ": " 用户 ",
        " request ": " 请求 ",
        " code ": " 代码 ",
        " file ": " 文件 ",
        " project ": " 项目 ",
        " application ": " 应用 ",
        " data ": " 数据 ",
        " function ": " 函数 ",
        " component ": " 组件 ",
        " test ": " 测试 ",
        " error ": " 错误 ",
        " server ": " 服务器 ",
        " database ": " 数据库 ",
        " API ": " API接口 ",
    }
    
    for en, zh in common_terms.items():
        result = result.replace(en, zh)
        
    return result

def translate_skill(skill: dict) -> dict:
    translated = skill.copy()
    
    # 翻译名称
    skill_id = skill.get("id", "")
    original_name = skill.get("name", "")
    translated["name_zh"] = translate_name(skill_id) or translate_name(original_name)
    
    # 翻译描述
    translated["description_zh"] = translate_description(skill.get("description", ""))
    
    # 翻译分类
    if "category" in skill:
        cat = skill["category"].lower()
        translated["category_zh"] = CATEGORY_TRANSLATIONS.get(cat, skill["category"])
    
    # 翻译正文
    if "body" in skill:
        translated["body_zh"] = translate_body(skill["body"])
    
    return translated

def main():
    print("Oh My Skills - 开始翻译\n")
    if not INPUT_FILE.exists():
        return
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        skills = json.load(f)
    
    translated_skills = [translate_skill(skill) for skill in skills]
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_skills, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！处理了 {len(translated_skills)} 个技能")
    print(f"   保存至: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
