import { useState } from 'react'
import './BilingualBlock.css'

function BilingualBlock({ chinese, english, type = 'text' }) {
    const [showOriginal, setShowOriginal] = useState(false)

    if (!english) return <div className="bilingual-content">{chinese}</div>

    return (
        <div className="bilingual-block">
            <div className={`bilingual-content ${type === 'code' ? 'code-block' : ''}`}>
                {chinese}
            </div>

            <button
                className="toggle-original"
                onClick={() => setShowOriginal(!showOriginal)}
            >
                <span className="toggle-icon">{showOriginal ? '▽' : '▷'}</span>
                <span>{showOriginal ? '隐藏原文' : '显示原文'}</span>
            </button>

            {showOriginal && (
                <div className={`original-content ${type === 'code' ? 'code-block' : ''}`}>
                    {english}
                </div>
            )}
        </div>
    )
}

export default BilingualBlock
