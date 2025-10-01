import React from 'react';
import './ATSScore.css';

const ATSScore = ({ score, componentScores, justification, aiAnalysis }) => {
  // Calculate the circle's circumference
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  
  // Calculate the offset (what's left unfilled)
  const offset = circumference - (score / 100) * circumference;
  
  // Determine the score color based on score value
  const getScoreColor = (scoreValue) => {
    if (scoreValue >= 80) return '#4CAF50'; // Green for high scores
    if (scoreValue >= 60) return '#FF9800'; // Orange for medium scores
    return '#F44336'; // Red for low scores
  };
  
  // Get text color for contrast on colored backgrounds
  const getTextColor = (scoreValue) => {
    return '#FFFFFF'; // White text for better visibility on colored backgrounds
  };
  
  // Format AI analysis to display full content with detailed suggestions
  const formatAIAnalysis = (analysis) => {
    if (!analysis) return null;
    
    // Make sure analysis is a string
    const analysisText = typeof analysis === 'string' ? analysis : JSON.stringify(analysis);
    
    // Extract numbered points and their descriptions
    const fullSuggestionRegex = /(\d+\.\s+\*\*([^*]+)\*\*)([\s\S]*?)(?=\d+\.|$)/g;
    let fullMatches = [...analysisText.matchAll(fullSuggestionRegex)];
    
    if (fullMatches.length > 0) {
      return (
        <ul className="ai-suggestions-list">
          {fullMatches.map((match, index) => {
            const fullPoint = match[0].trim();
            const title = match[2].trim();
            // Get the description text that follows the title
            const description = fullPoint.substring(fullPoint.indexOf(title) + title.length).trim();
            
            return (
              <li key={index} className="ai-suggestion-item">
                <span className="ai-suggestion-bullet">•</span>
                <div className="ai-suggestion-content">
                  <strong>{title}:</strong>
                  <span dangerouslySetInnerHTML={{ __html: description.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') }} />
                </div>
              </li>
            );
          })}
        </ul>
      );
    } else {
      // Fallback to the old numbered list extraction if the full suggestion regex doesn't match
      const numberedListRegex = /^\d+\.\s+(.+)$/gm;
      let matches = [...analysisText.matchAll(numberedListRegex)];
      
      if (matches.length > 0) {
        return (
          <ul className="ai-suggestions-list">
            {matches.map((match, index) => {
              // Get the text after the number
              const point = match[1];
              
              // Extract any text between asterisks for emphasis
              const formattedPoint = point.replace(/\*\*(.+?)\*\*/g, (_, p1) => {
                return `<strong>${p1}</strong>`;
              });
              
              return (
                <li key={index} className="ai-suggestion-item">
                  <span className="ai-suggestion-bullet">•</span>
                  <span dangerouslySetInnerHTML={{ __html: formattedPoint }} />
                </li>
              );
            })}
          </ul>
        );
      } else {
        // If it's not in numbered list format, format the entire text with paragraph breaks
        const paragraphs = analysisText.split('\n\n').filter(p => p.trim().length > 0);
        
        if (paragraphs.length > 0) {
          return (
            <div className="ai-analysis-paragraphs">
              {paragraphs.map((paragraph, index) => {
                // Format **bold text** as HTML
                const formattedParagraph = paragraph.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
                
                return (
                  <p key={index} dangerouslySetInnerHTML={{ __html: formattedParagraph }} />
                );
              })}
            </div>
          );
        } else {
          // If no paragraphs, just format and display the whole text
          const formattedText = analysisText.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
          return <p dangerouslySetInnerHTML={{ __html: formattedText }} />;
        }
      }
    }
  };
  
  // Format component score percentages
  const formatComponentScore = (name, value) => {
    return (
      <div className="ats-component-score" key={name}>
        <div className="component-name">{name}</div>
        <div className="score-bar-container">
          <div 
            className="score-bar" 
            style={{ 
              width: `${value}%`, 
              backgroundColor: getScoreColor(value),
              position: 'relative'
            }} 
          >
            <span 
              className="bar-percentage" 
              style={{ 
                color: getTextColor(value),
                position: 'absolute',
                right: '8px',
                top: '50%',
                transform: 'translateY(-50%)',
                fontSize: '11px',
                fontWeight: 'bold',
                display: value > 15 ? 'block' : 'none'
              }}
            >
              {value}%
            </span>
          </div>
        </div>
        <div className="component-value">{value < 16 ? `${value}%` : ''}</div>
      </div>
    );
  };

  return (
    <div className="ats-score-container">
      {/* Circular progress indicator */}
      <div className="ats-score-circle">
        <svg width="120" height="120" viewBox="0 0 120 120">
          {/* Background circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="transparent"
            stroke="#e0e0e0"
            strokeWidth="10"
          />
          {/* Progress circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="transparent"
            stroke={getScoreColor(score)}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            transform="rotate(-90 60 60)"
          />
          {/* Score text */}
          <text
            x="50%"
            y="50%"
            dy=".3em"
            textAnchor="middle"
            fontSize="24"
            fontWeight="bold"
            fill={getScoreColor(score)}
          >
            {score}
          </text>
        </svg>
        <div className="ats-score-label">ATS Score</div>
      </div>

      {/* Component scores */}
      <div className="ats-component-scores">
        <h4>Score Breakdown</h4>
        {componentScores && (
          <>
            {formatComponentScore('Structure', componentScores.structure_score)}
            {formatComponentScore('Keywords', componentScores.keyword_score)}
            {formatComponentScore('Content', componentScores.content_score)}
            {formatComponentScore('Formatting', componentScores.formatting_score)}
          </>
        )}
      </div>

      {/* Justification */}
      <div className="ats-justification">
        <h4>ATS Analysis</h4>
        <ul>
          {justification && justification.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>

      {/* AI Analysis */}
      <div className="ats-ai-analysis">
        <h4>Improvement Suggestions</h4>
        <div className="ai-analysis-content">
          {aiAnalysis ? (
            <div>
              {formatAIAnalysis(aiAnalysis)}
            </div>
          ) : (
            <p>No AI analysis available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ATSScore;