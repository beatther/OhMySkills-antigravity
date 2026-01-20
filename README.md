# ⚡ Oh My Skills

> AI 代理技能双语展示平台 | Bilingual AI Agent Skills Showcase

📍 **在线体验**: [https://beatther.github.io/OhMySkills-antigravity/](https://beatther.github.io/OhMySkills-antigravity/)

---

## ✨ 项目简介

Oh My Skills 是一个专注于展示 AI 代理技能（Agent Skills）的双语网站。它从多个 GitHub 开源仓库聚合技能数据，并使用 LLM 自动翻译成中文，让中国开发者更方便地浏览、学习和使用这些技能。

### 🌟 核心特性

- **📦 一键下载**：每个技能都支持一键打包下载，自动生成兼容 6 种主流 AI 编程工具的目录结构
- **🌐 双语展示**：所有技能均提供中英文对照，支持查看英文原文
- **🔍 智能搜索**：支持按技能名称、描述进行快速搜索
- **📱 响应式设计**：完美适配桌面端和移动端
- **🚀 静态部署**：基于 GitHub Pages 部署，访问快速稳定

---

## 📥 下载格式支持

下载的技能包支持以下 AI 编程工具：

| 工具 | 目录结构 |
|------|---------|
| **Claude Code** | `.claude/skills/[skill-id]/SKILL.md` |
| **Cursor** | `.cursor/skills/[skill-id]/SKILL.md` |
| **Codex** | `.codex/skills/[skill-id]/SKILL.md` |
| **Gemini** | `.gemini/skills/[skill-id]/SKILL.md` |
| **Windsurf** | `.windsurf/skills/[skill-id]/SKILL.md` |
| **Roo** | `.roo/skills/[skill-id]/SKILL.md` |

只需将下载的 ZIP 解压后，复制对应的目录到你的项目根目录即可使用。

---

## 🛠️ 本地开发

### 前置要求

- Node.js 18+
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173/OhMySkills-antigravity/ 查看效果。

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist/` 目录。

---

## 📊 数据来源

技能数据聚合自以下开源仓库：

- [skillcreatorai/Ai-Agent-Skills](https://github.com/skillcreatorai/Ai-Agent-Skills)
- [anthropics/skills](https://github.com/anthropics/skills)

### 数据更新

1. 运行数据采集脚本：
   ```bash
   python3 scripts/fetch_skills.py
   ```

2. 运行翻译脚本（需配置 DeepSeek API Key）：
   ```bash
   export DEEPSEEK_API_KEY='your-api-key'
   python3 scripts/translate_skills_deepseek.py
   ```

---

## 📁 项目结构

```
OhMySkills-antigravity/
├── public/
│   └── data/
│       ├── skills.json          # 翻译后的技能数据
│       └── skills_raw.json      # 原始技能数据
├── scripts/
│   ├── fetch_skills.py          # GitHub 数据采集
│   └── translate_skills_deepseek.py  # LLM 翻译脚本
├── src/
│   ├── components/              # React 组件
│   ├── pages/                   # 页面组件
│   └── App.jsx                  # 应用入口
├── index.html
├── vite.config.js
└── package.json
```

---

## 🚀 部署

项目使用 GitHub Actions 自动部署到 GitHub Pages。

每次推送到 `main` 分支时会自动触发部署流程：
1. 安装依赖
2. 构建项目
3. 部署到 GitHub Pages

部署配置文件：`.github/workflows/deploy.yml`

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你发现了新的优质技能仓库，或有任何改进建议，请随时联系。

---

## 📄 License

MIT License

---

<p align="center">
  <b>Made with ❤️ for the AI Developer Community</b>
</p>
