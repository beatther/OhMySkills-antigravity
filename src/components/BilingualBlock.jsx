import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './BilingualBlock.css'

function BilingualBlock({ chinese, english, type = 'text', isMarkdown = false }) {
    const [showOriginal, setShowOriginal] = useState(false)

    // 如果中英文相同，说明没有翻译，显示提示
    const hasTranslation = chinese !== english && chinese
    const displayContent = hasTranslation ? chinese : english

    const renderContent = (content, className) => {
        if (!content) return null

        if (isMarkdown) {
            return (
                <div className={`${className} markdown-content`}>
                    <ReactMarkdown>{content}</ReactMarkdown>
                </div>
            )
        }

        return <div className={className}>{content}</div>
    }

    return (
        <div className="bilingual-block">
            {renderContent(displayContent, `bilingual-content ${type === 'code' ? 'code-block' : ''}`)}

            {english && (
                <>
                    <button
                        className="toggle-original"
                        onClick={() => setShowOriginal(!showOriginal)}
                    >
                        <span className="toggle-icon">{showOriginal ? '▽' : '▷'}</span>
                        <span>{showOriginal ? '隐藏原文' : '显示原文'}</span>
                    </button>

                    {showOriginal && renderContent(english, `original-content ${type === 'code' ? 'code-block' : ''}`)}
                </>
            )}
        </div>
    )
}

export default BilingualBlock
