// 技能数据加载器
// 从 public/data/skills.json 加载真实数据

let skillsCache = null

export async function loadSkills() {
    if (skillsCache) return skillsCache

    try {
        const response = await fetch(`${import.meta.env.BASE_URL}data/skills.json`)
        if (!response.ok) {
            throw new Error('Failed to load skills')
        }
        const data = await response.json()

        // 去重：按 id 去重，保留第一个出现的
        const seen = new Set()
        skillsCache = data.filter(skill => {
            if (seen.has(skill.id)) {
                return false
            }
            seen.add(skill.id)
            return true
        })

        return skillsCache
    } catch (error) {
        console.error('Error loading skills:', error)
        return []
    }
}

export function getSkillById(skills, id) {
    return skills.find(s => s.id === id)
}

// 示例数据作为后备
export const fallbackSkills = [
    {
        id: 'ui-ux-pro-max',
        name: 'UI/UX Pro Max',
        name_zh: 'UI/UX 设计专家',
        description: 'Comprehensive design guide for web and mobile applications.',
        description_zh: '全面的网页和移动应用设计指南。',
        category: 'development',
        category_zh: '开发工具',
    }
]
