import "./ResumeBox.css";

function ResultBox({ result }) {
  if (!result) return null;

  return (
    <div className="result-box">
      <div className="result-card">
        {result.error ? (
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
            <p className="error-text">{result.error}</p>
          </div>
        ) : (
          <>
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
                <h3>Optimization Results</h3>
                <p className="header-subtitle">
                  Analysis completed successfully
                </p>
              </div>
            </div>

            <div className="results-grid">
              <div className="result-section gaps-section">
                <div className="section-header">
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
                  <div className="section-title">
                    <h4>Identified Gaps</h4>
                    <span className="count-badge gaps-badge">
                      {result.gaps?.length || 0}
                    </span>
                  </div>
                </div>
                <div className="section-content">
                  <ul className="result-list">
                    {result.gaps && result.gaps.length > 0 ? (
                      result.gaps.map((gap, idx) => (
                        <li key={idx} className="result-item gap-item">
                          <div className="item-indicator gap-indicator"></div>
                          <span className="item-text">{gap}</span>
                        </li>
                      ))
                    ) : (
                      <li className="result-item no-items success-item">
                        <div className="check-icon-wrapper">
                          <svg
                            className="check-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                        </div>
                        <span className="item-text">
                          No gaps identified - Great job!
                        </span>
                      </li>
                    )}
                  </ul>
                </div>
              </div>

              <div className="result-section suggestions-section">
                <div className="section-header">
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
                  <div className="section-title">
                    <h4>Alignment Suggestions</h4>
                    <span className="count-badge suggestions-badge">
                      {result.alignment_suggestions?.length || 0}
                    </span>
                  </div>
                </div>
                <div className="section-content">
                  <ul className="result-list">
                    {result.alignment_suggestions &&
                    result.alignment_suggestions.length > 0 ? (
                      result.alignment_suggestions.map((suggestion, idx) => (
                        <li key={idx} className="result-item suggestion-item">
                          <div className="item-indicator suggestion-indicator"></div>
                          <span className="item-text">{suggestion}</span>
                        </li>
                      ))
                    ) : (
                      <li className="result-item no-items success-item">
                        <div className="check-icon-wrapper">
                          <svg
                            className="check-icon"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                        </div>
                        <span className="item-text">
                          Perfect alignment - No changes needed!
                        </span>
                      </li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ResultBox;
