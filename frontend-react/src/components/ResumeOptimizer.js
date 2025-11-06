// src/components/ResumeOptimizer.js
import React from "react";
import ATSScore from "./ATSScore";
import "./ResumeBox.css";

function ResumeOptimizer({ resumeData }) {
  if (!resumeData) {
    return (
      <div className="resume-optimizer-container">
        <div className="result-section-compact empty-section">
          <div className="empty-state">
            <div className="empty-icon-wrapper">
              <svg
                className="empty-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3>No Resume Analyzed Yet</h3>
            <p>
              Upload a resume to see optimization results and ATS score
              analysis.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="resume-optimizer-container">
      {resumeData.error ? (
        <div className="result-section-compact error-section">
          <div className="error-result">
            <div className="error-header">
              <div className="error-icon-wrapper">
                <svg
                  className="error-icon"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <h3>Analysis Error</h3>
            </div>
            <p className="error-text">{resumeData.error}</p>
          </div>
        </div>
      ) : (
        <>
          <div className="result-section-compact header-section">
            <div className="result-header">
              <div className="success-icon-wrapper">
                <svg
                  className="result-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="header-content">
                <h3>Resume Optimization Results</h3>
                <p className="header-subtitle">
                  Analysis for: {resumeData.filename}
                </p>
              </div>
            </div>
          </div>

          {/* ATS Score and Results Grid */}
          <div className="optimizer-grid">
            {/* ATS Score Component */}
            {resumeData.ats_score && (
              <div className="result-section-compact ats-section">
                <ATSScore
                  score={resumeData.ats_score}
                  componentScores={resumeData.ats_analysis?.component_scores}
                  justification={resumeData.ats_analysis?.justification}
                  aiAnalysis={resumeData.ats_analysis?.ai_analysis}
                />
              </div>
            )}

            <div className="results-compact">
              {/* Identified Gaps - Left Align */}
              <div className="result-section-compact gaps-section">
                <div className="section-header-compact">
                  <div className="section-icon-wrapper warning">
                    <svg
                      className="section-icon"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                      />
                    </svg>
                  </div>
                  <h4>Identified Gaps</h4>
                  <span className="count-badge gaps-badge">
                    {resumeData.gaps?.length || 0}
                  </span>
                </div>
                <div className="section-content-compact">
                  {resumeData.gaps && resumeData.gaps.length > 0 ? (
                    <div className="items-row">
                      {resumeData.gaps.map((gap, idx) => {
                        return (
                          <span key={idx} className="item-chip gap-chip">
                            {gap}
                          </span>
                        );
                      })}
                    </div>
                  ) : (
                    <div className="no-items-compact success-message">
                      <svg
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        style={{ display: "inline", marginRight: "6px" }}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      <span>No gaps identified - Great job!</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Alignment Suggestions - Row Layout */}
              <div className="result-section-compact suggestions-section">
                <div className="section-header-compact">
                  <div className="section-icon-wrapper info">
                    <svg
                      className="section-icon"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                  </div>
                  <h4>Alignment Suggestions</h4>
                  <span className="count-badge suggestions-badge">
                    {resumeData.alignment_suggestions?.length || 0}
                  </span>
                </div>
                <div className="section-content-compact">
                  {resumeData.alignment_suggestions &&
                  resumeData.alignment_suggestions.length > 0 ? (
                    <div className="items-row">
                      {resumeData.alignment_suggestions.map(
                        (suggestion, idx) => {
                          return (
                            <span
                              key={idx}
                              className="item-chip suggestion-chip"
                            >
                              {suggestion}
                            </span>
                          );
                        }
                      )}
                    </div>
                  ) : (
                    <div className="no-items-compact success-message">
                      <svg
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        style={{ display: "inline", marginRight: "6px" }}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      <span>Perfect alignment - No changes needed!</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
export default ResumeOptimizer;
