#!/usr/bin/env python3
"""
Oh My Skills - GitHub 数据采集脚本
从配置的 GitHub 仓库获取 skills 数据
"""

import os
import re
import json
import yaml
import requests
from pathlib import Path
from typing import Optional

# 配置：GitHub 仓库列表
REPOSITORIES = [
    {
        "name": "Ai-Agent-Skills",
        "owner": "skillcreatorai",
        "repo": "Ai-Agent-Skills",
        "skills_path": "skills"
    },
    {
        "name": "anthropics-skills",
        "owner": "anthropics",
        "repo": "skills",
        "skills_path": "skills"
    }
]

# GitHub API Token（可选，用于提高 API 限制）
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "data"


def get_headers():
    """获取 GitHub API 请求头"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OhMySkills"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers


def parse_skill_md(content: str) -> dict:
    """解析 SKILL.md 文件内容"""
    result = {
        "name": "",
        "description": "",
        "body": ""
    }
    
    # 提取 YAML frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if frontmatter_match:
        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
            result["name"] = metadata.get("name", "")
            result["description"] = metadata.get("description", "")
            result["body"] = frontmatter_match.group(2).strip()
        except yaml.YAMLError:
            pass
    
    return result


def fetch_repo_skills(repo_config: dict) -> list:
    """从单个仓库获取 skills 列表"""
    skills = []
    owner = repo_config["owner"]
    repo = repo_config["repo"]
    skills_path = repo_config["skills_path"]
    
    # 获取 skills 目录内容
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{skills_path}"
    
    try:
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        contents = response.json()
        
        for item in contents:
            if item["type"] == "dir":
                skill_id = item["name"]
                skill_md_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{skills_path}/{skill_id}/SKILL.md"
                
                try:
                    md_response = requests.get(skill_md_url, headers=get_headers())
                    md_response.raise_for_status()
                    md_data = md_response.json()
                    
                    # 解码 base64 内容
                    import base64
                    content = base64.b64decode(md_data["content"]).decode("utf-8")
                    
                    # 解析 SKILL.md
                    skill_data = parse_skill_md(content)
                    skill_data["id"] = skill_id
                    skill_data["source"] = repo_config["name"]
                    skill_data["html_url"] = f"https://github.com/{owner}/{repo}/tree/main/{skills_path}/{skill_id}"
                    
                    skills.append(skill_data)
                    print(f"  ✓ {skill_id}")
                    
                except Exception as e:
                    print(f"  ✗ {skill_id}: {e}")
                    
    except Exception as e:
        print(f"Error fetching {owner}/{repo}: {e}")
    
    return skills


def main():
    """主函数"""
    print("Oh My Skills - 开始采集数据\n")
    
    all_skills = []
    
    for repo_config in REPOSITORIES:
        print(f"📦 {repo_config['name']} ({repo_config['owner']}/{repo_config['repo']})")
        skills = fetch_repo_skills(repo_config)
        all_skills.extend(skills)
        print(f"   共获取 {len(skills)} 个技能\n")
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 保存为 JSON
    output_file = OUTPUT_DIR / "skills_raw.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_skills, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！共采集 {len(all_skills)} 个技能")
    print(f"   保存至: {output_file}")


if __name__ == "__main__":
    main()
