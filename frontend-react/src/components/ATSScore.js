import React, { useState } from "react";
import "./ATSScore.css";
import { formatAIAnalysis } from "../utils/textFormatter";

const ATSScore = ({ score, componentScores, justification, aiAnalysis }) => {
  // State for expand/collapse
  const [isExpanded, setIsExpanded] = useState(false);

  // Calculate the circle's circumference
  const radius = 40;
  const circumference = 2 * Math.PI * radius;

  // Calculate the offset (what's left unfilled)
  const offset = circumference - (score / 100) * circumference;

  // Determine the score color based on score value
  const getScoreColor = (scoreValue) => {
    if (scoreValue >= 80) return "#4CAF50"; // Green for high scores
    if (scoreValue >= 60) return "#FF9800"; // Orange for medium scores
    return "#F44336"; // Red for low scores
  };

  // Get text color for contrast on colored backgrounds
  const getTextColor = (scoreValue) => {
    return "#FFFFFF"; // White text for better visibility on colored backgrounds
  };

  // Format formatted suggestions for display
  const renderFormattedSuggestions = (analysis) => {
    const formatted = formatAIAnalysis(analysis);

    if (!formatted) return null;

    return (
      <ul className="ai-suggestions-list">
        {formatted.map((item, index) => (
          <li key={index} className="ai-suggestion-item">
            <span className="ai-suggestion-bullet">•</span>
            <div className="ai-suggestion-content">
              {item.title && <strong>{item.title}:</strong>}
              <span dangerouslySetInnerHTML={{ __html: item.description }} />
            </div>
          </li>
        ))}
      </ul>
    );
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
              position: "relative",
            }}
          >
            <span
              className="bar-percentage"
              style={{
                color: getTextColor(value),
                position: "absolute",
                right: "8px",
                top: "50%",
                transform: "translateY(-50%)",
                fontSize: "11px",
                fontWeight: "bold",
                display: value > 15 ? "block" : "none",
              }}
            >
              {value}%
            </span>
          </div>
        </div>
        <div className="component-value">{value < 16 ? `${value}%` : ""}</div>
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
            {formatComponentScore("Structure", componentScores.structure_score)}
            {formatComponentScore("Keywords", componentScores.keyword_score)}
            {formatComponentScore("Content", componentScores.content_score)}
            {formatComponentScore(
              "Formatting",
              componentScores.formatting_score
            )}
          </>
        )}
      </div>

      {/* Justification */}
      <div className="ats-justification">
        <h4>ATS Analysis</h4>
        <ul>
          {justification &&
            justification.map((item, index) => <li key={index}>{item}</li>)}
        </ul>
      </div>

      {/* AI Analysis */}
      <div className="ats-ai-analysis">
        <div className="ai-analysis-header">
          <h4>Improvement Suggestions</h4>
          <button
            className="expand-toggle-btn"
            onClick={() => setIsExpanded(!isExpanded)}
            aria-label={
              isExpanded ? "Collapse suggestions" : "Expand suggestions"
            }
          >
            <svg
              className={`expand-icon ${isExpanded ? "expanded" : ""}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              width="20"
              height="20"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
            <span>{isExpanded ? "Show Less" : "Show More"}</span>
          </button>
        </div>
        {isExpanded && (
          <div className="ai-analysis-content">
            {aiAnalysis ? (
              renderFormattedSuggestions(aiAnalysis)
            ) : (
              <p>No AI analysis available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ATSScore;
