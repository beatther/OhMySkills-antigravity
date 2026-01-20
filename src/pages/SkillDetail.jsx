import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import BilingualBlock from '../components/BilingualBlock'
import DownloadButton from '../components/DownloadButton'
import { loadSkills, getSkillById, fallbackSkills } from '../data/skills'
import './SkillDetail.css'

function SkillDetail() {
    const { id } = useParams()
    const [skill, setSkill] = useState(null)
    const [loading, setLoading] = useState(true)

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

                <h1 className="skill-title">
                    <BilingualBlock
                        chinese={skill.name_zh}
                        english={skill.name}
                    />
                </h1>

                <div className="skill-description">
                    <BilingualBlock
                        chinese={skill.description_zh}
                        english={skill.description}
                    />
                </div>

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
                    <BilingualBlock
                        chinese={skill.body_zh}
                        english={skill.body}
                        isMarkdown={true}
                    />
                </div>
            )}
        </div>
    )
}

export default SkillDetail
