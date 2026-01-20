import { Link } from 'react-router-dom'
import './SkillCard.css'

function SkillCard({ skill }) {
    // 标题格式: English (中文翻译)
    const title = skill.name_zh && skill.name_zh !== skill.name
        ? `${skill.name} (${skill.name_zh})`
        : skill.name

    // 描述使用中文翻译
    const description = skill.description_zh || skill.description

    return (
        <Link to={`/skill/${skill.id}`} className="skill-card">
            <div className="skill-card-header">
                <h3 className="skill-name">{title}</h3>
                {skill.category && (
                    <span className="skill-category">{skill.category_zh || skill.category}</span>
                )}
            </div>

            <p className="skill-description">
                {description}
            </p>

            <div className="skill-card-footer">
                <span className="skill-author">{skill.source || '社区'}</span>
                <span className="skill-arrow">→</span>
            </div>
        </Link>
    )
}

export default SkillCard
