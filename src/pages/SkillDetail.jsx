import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import DownloadButton from '../components/DownloadButton'
import { loadSkills, getSkillById, fallbackSkills } from '../data/skills'
import './SkillDetail.css'

function SkillDetail() {
    const { id } = useParams()
    const [skill, setSkill] = useState(null)
    const [loading, setLoading] = useState(true)
    const [showOriginalBody, setShowOriginalBody] = useState(false)

    useEffect(() => {
        loadSkills()
            .then(data => {
                const skills = data.length > 0 ? data : fallbackSkills
                const found = getSkillById(skills, id)
                setSkill(found)
                setLoading(false)
            })
            .catch(() => {
                const found = getSkillById(fallbackSkills, id)
                setSkill(found)
                setLoading(false)
            })
    }, [id])

    if (loading) {
        return (
            <div className="skill-detail-page loading">
                <div className="loading-spinner">加载中...</div>
            </div>
        )
    }

    if (!skill) {
        return (
            <div className="skill-detail-page">
                <div className="not-found">
                    <h2>技能未找到</h2>
                    <Link to="/skills" className="back-link">← 返回列表</Link>
                </div>
            </div>
        )
    }

    // 标题格式: English (中文翻译)
    const title = skill.name_zh && skill.name_zh !== skill.name
        ? `${skill.name} (${skill.name_zh})`
        : skill.name

    return (
        <div className="skill-detail-page">
            <Link to="/skills" className="back-link">← 返回列表</Link>

            <div className="skill-header">
                <div className="skill-meta">
                    {skill.category && (
                        <span className="skill-category">{skill.category_zh || skill.category}</span>
                    )}
                    {skill.source && (
                        <span className="skill-source">来源: {skill.source}</span>
                    )}
                </div>

                <h1 className="skill-title">{title}</h1>

                <p className="skill-description">
                    {skill.description_zh || skill.description}
                </p>

                <div className="action-buttons">
                    <DownloadButton skill={skill} />

                    {skill.html_url && (
                        <a
                            href={skill.html_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="github-link-btn"
                        >
                            在 GitHub 上查看 →
                        </a>
                    )}
                </div>
            </div>

            {skill.body && (
                <div className="skill-content">
                    <h2 className="content-title">详细说明</h2>

                    {/* 中文翻译版 Markdown */}
                    <div className="markdown-content">
                        <ReactMarkdown>{skill.body_zh || skill.body}</ReactMarkdown>
                    </div>

                    {/* 显示/隐藏英文原文按钮 */}
                    <button
                        className="toggle-original-body"
                        onClick={() => setShowOriginalBody(!showOriginalBody)}
                    >
                        <span className="toggle-icon">{showOriginalBody ? '▽' : '▷'}</span>
                        <span>{showOriginalBody ? '隐藏英文原文' : '查看英文原文'}</span>
                    </button>

                    {/* 英文原文 Markdown */}
                    {showOriginalBody && (
                        <div className="original-body">
                            <h3 className="original-title">English Original</h3>
                            <div className="markdown-content original">
                                <ReactMarkdown>{skill.body}</ReactMarkdown>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default SkillDetail
