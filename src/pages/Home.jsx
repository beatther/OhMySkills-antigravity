import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SkillCard from '../components/SkillCard'
import { loadSkills, fallbackSkills } from '../data/skills'
import './Home.css'

function Home() {
    const [skills, setSkills] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadSkills()
            .then(data => {
                setSkills(data.length > 0 ? data : fallbackSkills)
                setLoading(false)
            })
            .catch(() => {
                setSkills(fallbackSkills)
                setLoading(false)
            })
    }, [])

    const featuredSkills = skills.slice(0, 6)

    if (loading) {
        return (
            <div className="home loading">
                <div className="loading-spinner">加载中...</div>
            </div>
        )
    }

    return (
        <div className="home">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <h1 className="hero-title">
                        <span className="hero-icon">⚡</span>
                        Oh My Skills
                    </h1>
                    <p className="hero-subtitle">
                        AI 代理技能双语展示平台
                    </p>
                    <p className="hero-description">
                        探索、学习和下载 AI 代理技能，支持 Claude、Cursor、Codex、Gemini 等多种格式
                    </p>
                    <div className="hero-actions">
                        <Link to="/skills" className="btn btn-primary">
                            浏览全部技能
                        </Link>
                        <a
                            href="https://github.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-secondary"
                        >
                            查看源码
                        </a>
                    </div>
                </div>

                <div className="hero-stats">
                    <div className="stat">
                        <span className="stat-value">{skills.length}</span>
                        <span className="stat-label">技能数量</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">6+</span>
                        <span className="stat-label">支持格式</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">中英</span>
                        <span className="stat-label">双语展示</span>
                    </div>
                </div>
            </section>

            {/* Featured Skills */}
            <section className="featured">
                <div className="section-header">
                    <h2 className="section-title">精选技能</h2>
                    <Link to="/skills" className="view-all">
                        查看全部 →
                    </Link>
                </div>

                <div className="skills-grid">
                    {featuredSkills.map(skill => (
                        <SkillCard key={skill.id} skill={skill} />
                    ))}
                </div>
            </section>

            {/* Formats Section */}
            <section className="formats">
                <h2 className="section-title">支持的 AI 工具</h2>
                <div className="formats-grid">
                    {['Claude', 'Cursor', 'Codex', 'Gemini', 'Windsurf', 'Roo'].map(name => (
                        <div key={name} className="format-card">
                            <span className="format-name">{name}</span>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    )
}

export default Home
