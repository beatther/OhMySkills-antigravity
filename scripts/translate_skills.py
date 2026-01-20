#!/usr/bin/env python3
"""
Oh My Skills - 增强版字典翻译脚本
无需 API，基于规则和大量术语库进行本地翻译
"""

import json
import re
from pathlib import Path

# ==========================================
# 1. 技能名称映射 (精确匹配)
# ==========================================
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

# ==========================================
# 2. Markdown 标题映射 (正则匹配)
# ==========================================
HEADER_TRANSLATIONS = {
    r"^#\s+(.*)": r"# \1", 
    r"^##\s+Overview": "## 概述",
    r"^##\s+Introduction": "## 介绍",
    r"^##\s+Description": "## 描述",
    r"^##\s+Capabilities": "## 核心能力",
    r"^##\s+Features": "## 功能特性",
    r"^##\s+Usage": "## 使用方法",
    r"^##\s+Examples": "## 示例代码",
    r"^##\s+Instructions": "## 详细说明",
    r"^##\s+Requirements": "## 环境要求",
    r"^##\s+Installation": "## 安装步骤",
    r"^##\s+Configuration": "## 配置选项",
    r"^##\s+Parameters": "## 参数列表",
    r"^##\s+Output": "## 输出格式",
    r"^##\s+Workflow": "## 工作流程",
    r"^##\s+Best Practices": "## 最佳实践",
    r"^##\s+Notes": "## 注意事项",
    r"^##\s+Tips": "## 实用技巧",
    r"^###\s+Step (\d+)": r"### 第 \1 步",
    r"^###\s+Prerequisites": "### 先决条件",
}

# ==========================================
# 3. 常用词汇和短语映射 (不区分大小写)
# ==========================================
PHRASE_TRANSLATIONS = {
    # 引导语
    "Use this skill when": "适用于以下场景",
    "This skill allows you to": "此技能允许你",
    "You can use this to": "你可以用它来",
    "Make sure to": "请确保",
    "For example": "例如",
    "In this case": "在这种情况下",
    "The following": "以下",
    "Please note": "请注意",
    
    # 动作
    "Create": "创建",
    "Generate": "生成",
    "Build": "构建",
    "Design": "设计",
    "Automate": "自动化",
    "Analyze": "分析",
    "Extract": "提取",
    "Convert": "转换",
    "Upload": "上传",
    "Download": "下载",
    "Install": "安装",
    "Run": "运行",
    "Test": "测试",
    "Debug": "调试",
    "Deploy": "部署",
    "Review": "审查",
    "Refactor": "重构",
    "Optimize": "优化",
    "Document": "编写文档",
    
    # 名词
    "Application": "应用",
    "Project": "项目",
    "Component": "组件",
    "Function": "函数",
    "Method": "方法",
    "Variable": "变量",
    "Database": "数据库",
    "Server": "服务器",
    "Client": "客户端",
    "Frontend": "前端",
    "Backend": "后端",
    "Interface": "接口",
    "User": "用户",
    "Request": "请求",
    "Response": "响应",
    "Error": "错误",
    "Success": "成功",
    "File": "文件",
    "Folder": "文件夹",
    "Directory": "目录",
    "Image": "图片",
    "Video": "视频",
    "Audio": "音频",
    "Text": "文本",
    "Code": "代码",
    "Data": "数据",
    "Configuration": "配置",
    "Settings": "设置",
    "Options": "选项",
    "Parameters": "参数",
    "Arguments": "参数",
    "Result": "结果",
    "Output": "输出",
    "Input": "输入",
    "example": "示例",
    "template": "模板",
    "library": "库",
    "framework": "框架",
    "tool": "工具",
    "script": "脚本",
    "command": "命令",
    
    # 介词/连词 (小心使用，避免过度替换破坏语序，仅替换明确的)
    " using ": " 使用 ",
    " with ": " 包含 ",
    " for ": " 用于 ",
    # " and ": " 和 ", # and 太常见，容易破坏代码或专有名词，暂不替换
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

def translate_text_smart(text: str) -> str:
    """智能替换文本中的词汇"""
    if not text: return ""
    
    result = text
    
    # 按照短语长度降序排列，优先替换长短语
    sorted_phrases = sorted(PHRASE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for en, zh in sorted_phrases:
        # 使用正则进行不区分大小写的替换，但要确保单词边界（避免替换单词的一部分）
        # 允许前后是空格、标点或字符串边界
        pattern = re.compile(r'(^|[\s\W])' + re.escape(en) + r'($|[\s\W])', re.IGNORECASE)
        
        # 替换时保留原来的分隔符
        # group(1) 是前分隔符，group(2) 是后分隔符
        # 简单替换：result = pattern.sub(lambda m: m.group(1) + zh + m.group(2), result)
        
        # 由于 Python re 的限制，这样替换比较安全：
        # 先简单替换常用词
        if len(en) > 3: # 只替换较长的词，避免误伤
             result = result.replace(en, zh)
             result = result.replace(en.lower(), zh)
             result = result.replace(en.capitalize(), zh)
            
    return result

def translate_body(text: str) -> str:
    """翻译 Markdown 正文"""
    if not text: return ""
    
    # 1. 保护代码块
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_{len(code_blocks)-1}__"
    
    text_safe = re.sub(r'```[\s\S]*?```', save_code, text)
    text_safe = re.sub(r'`[^`\n]+`', save_code, text_safe)
    
    lines = text_safe.split('\n')
    translated_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 翻译标题
        is_header = False
        for pattern, replacement in HEADER_TRANSLATIONS.items():
            if re.match(pattern, line_stripped):
                line = re.sub(pattern, replacement, line)
                is_header = True
                break
        
        # 如果不是标题，也不是空行，尝试翻译内容
        if not is_header and line_stripped and not re.match(r'^[-=*_#]+$', line_stripped):
            line = translate_text_smart(line)
            
        translated_lines.append(line)
    
    result = '\n'.join(translated_lines)
    
    # 还原代码
    for i, code in enumerate(code_blocks):
        result = result.replace(f"__CODE_{i}__", code)
        
    return result

def translate_skill(skill: dict) -> dict:
    translated = skill.copy()
    
    # 名称
    skill_id = skill.get("id", "")
    original_name = skill.get("name", "")
    translated["name_zh"] = translate_name(skill_id) or translate_name(original_name)
    
    # 描述
    translated["description_zh"] = translate_text_smart(skill.get("description", ""))
    
    # 分类
    if "category" in skill:
        cat = skill["category"].lower()
        translated["category_zh"] = CATEGORY_TRANSLATIONS.get(cat, skill["category"])
    
    # 正文
    if "body" in skill:
        translated["body_zh"] = translate_body(skill["body"])
    
    return translated

def main():
    print("Oh My Skills - 开始增强本地翻译 (无需联网)\n")
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
