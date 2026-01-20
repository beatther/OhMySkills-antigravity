import { useState, useEffect } from 'react'
import SkillCard from '../components/SkillCard'
import { loadSkills, fallbackSkills } from '../data/skills'
import './SkillList.css'

function SkillList() {
    const [skills, setSkills] = useState([])
    const [loading, setLoading] = useState(true)
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('')

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

    const categories = [...new Set(skills.map(s => s.category_zh || s.category).filter(Boolean))]

    const filteredSkills = skills.filter(skill => {
        const matchesSearch =
            (skill.name_zh || skill.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
            (skill.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
            (skill.description_zh || skill.description || '').toLowerCase().includes(searchTerm.toLowerCase())

        const matchesCategory = !selectedCategory ||
            (skill.category_zh || skill.category) === selectedCategory

        return matchesSearch && matchesCategory
    })

    if (loading) {
        return (
            <div className="skill-list-page loading">
                <div className="loading-spinner">加载中...</div>
            </div>
        )
    }

    return (
        <div className="skill-list-page">
            <div className="list-header">
                <h1 className="page-title">技能列表</h1>
                <p className="page-subtitle">
                    共 {skills.length} 个技能，支持中英双语展示
                </p>
            </div>

            <div className="filters">
                <div className="search-box">
                    <input
                        type="text"
                        placeholder="搜索技能..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>

                <div className="category-filter">
                    <button
                        className={`category-btn ${selectedCategory === '' ? 'active' : ''}`}
                        onClick={() => setSelectedCategory('')}
                    >
                        全部
                    </button>
                    {categories.map(category => (
                        <button
                            key={category}
                            className={`category-btn ${selectedCategory === category ? 'active' : ''}`}
                            onClick={() => setSelectedCategory(category)}
                        >
                            {category}
                        </button>
                    ))}
                </div>
            </div>

            <div className="skills-grid">
                {filteredSkills.map((skill, index) => (
                    <SkillCard key={`${skill.id}-${index}`} skill={skill} />
                ))}
            </div>

            {filteredSkills.length === 0 && (
                <div className="no-results">
                    <p>没有找到匹配的技能</p>
                </div>
            )}
        </div>
    )
}

export default SkillList
