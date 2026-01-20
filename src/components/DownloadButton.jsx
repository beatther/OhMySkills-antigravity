import { useState } from 'react'
import JSZip from 'jszip'
import { saveAs } from 'file-saver'
import './DownloadButton.css'

const FORMATS = [
    { name: 'Claude', path: '.claude/skills' },
    { name: 'Cursor', path: '.cursor/skills' },
    { name: 'Codex', path: '.codex/skills' },
    { name: 'Gemini', path: '.gemini/skills' },
    { name: 'Windsurf', path: '.windsurf/skills' },
    { name: 'Roo', path: '.roo/skills' },
]

function generateSkillMd(skill) {
    const body = skill.body || ''

    // 检查 body 是否已经包含 YAML Frontmatter
    if (body.trim().startsWith('---')) {
        // 如果已经有 frontmatter，直接返回原始内容（确保最真实地还原 GitHub 文件）
        // 这里的假设是 GitHub 上的 SKILL.md 已经是完整的、可用的格式
        return body
    }

    // 如果没有 frontmatter，则手动构建标准格式
    const description = skill.description || ''
    // 转义引号
    const safeDescription = description.replace(/"/g, '\\"')

    return `---
name: ${skill.id || skill.name}
description: "${safeDescription}"
---

# ${skill.name}

${body || description || ''}
`
}

function generateReadme(skill) {
    return `# ${skill.name_zh || skill.name}

${skill.description_zh || skill.description || ''}

## 安装方式

将对应的目录复制到你的项目根目录：

- **Claude Code**: 复制 \`.claude/\` 目录
- **Cursor**: 复制 \`.cursor/\` 目录  
- **Codex**: 复制 \`.codex/\` 目录
- **Gemini**: 复制 \`.gemini/\` 目录
- **Windsurf**: 复制 \`.windsurf/\` 目录
- **Roo**: 复制 \`.roo/\` 目录

## 原始链接

${skill.html_url ? `GitHub: ${skill.html_url}` : '来源: Oh My Skills'}
`
}

async function handleDownload(skill, setDownloading) {
    setDownloading(true)

    try {
        const zip = new JSZip()

        // 更安全的文件名净化：仅保留字母、数字、下划线和连字符
        const rawId = skill.id || skill.name || 'skill'
        const safeId = rawId.toLowerCase()
            .replace(/[^a-z0-9\-_]/g, '-')  // 替换所有非安全字符为 -
            .replace(/-+/g, '-')            // 合并连续的 -
            .replace(/^-|-$/g, '')          // 去除首尾的 -

        const skillId = safeId || 'skill-package' // 防止空字符串

        const skillMd = generateSkillMd(skill)

        // Add SKILL.md for each format
        FORMATS.forEach(format => {
            zip.file(`${format.path}/${skillId}/SKILL.md`, skillMd)
        })

        // Add README
        zip.file('README.md', generateReadme(skill))

        // Generate and download
        const content = await zip.generateAsync({ type: 'blob' })
        saveAs(content, `${skillId}.zip`)
    } catch (error) {
        console.error('Download failed:', error)
        alert('下载失败，请重试')
    } finally {
        setDownloading(false)
    }
}

function DownloadButton({ skill }) {
    const [downloading, setDownloading] = useState(false)

    return (
        <div className="download-section">
            <button
                className={`download-btn ${downloading ? 'downloading' : ''}`}
                onClick={() => handleDownload(skill, setDownloading)}
                disabled={downloading}
            >
                {downloading ? (
                    <>
                        <span className="spinner"></span>
                        下载中...
                    </>
                ) : (
                    <>
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
                        </svg>
                        下载技能包
                    </>
                )}
            </button>
            <p className="download-hint">
                包含 {FORMATS.length} 种格式：{FORMATS.map(f => f.name).join('、')}
            </p>
        </div>
    )
}

export default DownloadButton
