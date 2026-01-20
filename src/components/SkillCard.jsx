import { Link } from 'react-router-dom'
import './SkillCard.css'

function SkillCard({ skill }) {
    return (
        <Link to={`/skill/${skill.id}`} className="skill-card">
            <div className="skill-card-header">
                <h3 className="skill-name">{skill.name_zh || skill.name}</h3>
                {skill.category && (
                    <span className="skill-category">{skill.category_zh || skill.category}</span>
                )}
            </div>

            <p className="skill-description">
                {skill.description_zh || skill.description}
            </p>

            {skill.tags && skill.tags.length > 0 && (
                <div className="skill-tags">
                    {(skill.tags_zh || skill.tags).slice(0, 3).map((tag, index) => (
                        <span key={index} className="skill-tag">{tag}</span>
                    ))}
                </div>
            )}

            <div className="skill-card-footer">
                <span className="skill-author">{skill.author || '社区'}</span>
                <span className="skill-arrow">→</span>
            </div>
        </Link>
    )
}

export default SkillCard
