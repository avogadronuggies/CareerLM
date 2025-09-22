import { useState } from "react";
import Sidebar from "../components/Sidebar";
import ResumeUpload from "../components/ResumeUpload";
import SkillGapAnalyzer from "../components/SkillGapAnalyzer";
import MockInterview from "../components/MockInterview";
import ColdEmailGenerator from "../components/ColdEmailGenerator";
import StudyPlanner from "../components/StudyPlanner";
import "./Dashboard.css";


function Dashboard() {
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [resumeData, setResumeData] = useState(null);

  const renderPage = () => {
    switch (currentPage) {
      case "upload":
        return <ResumeUpload onResult={setResumeData} />;
      case "skill_gap":
        return <SkillGapAnalyzer resumeData={resumeData} />;
      case "mock_interview":
        return <MockInterview resumeData={resumeData} />;
      case "cold_email":
        return <ColdEmailGenerator resumeData={resumeData} />;
      case "study_planner":
        return <StudyPlanner resumeData={resumeData} />;
      default:
        return (
          <div className="dashboard-welcome">
            <div className="welcome-card">
              <div className="welcome-header">
                <h2 className="welcome-title">Welcome to your Dashboard</h2>
                <div className="welcome-icon">
                  <svg
                    width="48"
                    height="48"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M12 2L2 7L12 12L22 7L12 2Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M2 17L12 22L22 17"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M2 12L12 17L22 12"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              </div>
              <div className="welcome-content">
                {resumeData ? (
                  <div className="resume-status success">
                    <div className="status-icon">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M9 12L11 14L15 10"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <circle
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="2"
                        />
                      </svg>
                    </div>
                    <div className="status-text">
                      <p className="status-title">Resume Analyzed</p>
                      <p className="status-subtitle">
                        Latest file: {resumeData.filename}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="resume-status pending">
                    <div className="status-icon">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <circle
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="2"
                        />
                        <path
                          d="M12 6V12L16 14"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <div className="status-text">
                      <p className="status-title">No Resume Uploaded</p>
                      <p className="status-subtitle">
                        Click "Upload Resume" to get started
                      </p>
                    </div>
                  </div>
                )}
              </div>
              <div className="quick-actions">
                <h3 className="actions-title">Quick Actions</h3>
                <div className="actions-grid">
                  <button
                    className="action-card"
                    onClick={() => setCurrentPage("upload")}
                  >
                    <div className="action-icon">
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M21 15V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V15"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <polyline
                          points="7,10 12,15 17,10"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <line
                          x1="12"
                          y1="15"
                          x2="12"
                          y2="3"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                        />
                      </svg>
                    </div>
                    <span>Upload Resume</span>
                  </button>
                  <button
                    className="action-card"
                    onClick={() => setCurrentPage("resume_optimizer")}
                  >
                    <div className="action-icon">
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M14.7 6.3A1 1 0 0 0 13 5H6A2 2 0 0 0 4 7V18A2 2 0 0 0 6 20H18A2 2 0 0 0 20 18V10A1 1 0 0 0 18.7 8.3L14.7 6.3Z"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <span>Optimize Resume</span>
                  </button>
                  <button
                    className="action-card"
                    onClick={() => setCurrentPage("skill_gap")}
                  >
                    <div className="action-icon">
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M9 11H15M9 15H15M17 21L20 18L17 15M7 21L4 18L7 15M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H15.8C16.9201 21 17.4802 21 17.908 20.782C18.2843 20.5903 18.5903 20.2843 18.782 19.908C19 19.4802 19 18.9201 19 17.8V9L13 3Z"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <span>Analyze Skills</span>
                  </button>
                  <button
                    className="action-card"
                    onClick={() => setCurrentPage("mock_interview")}
                  >
                    <div className="action-icon">
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M8 12H16M8 16H16M6 20H18A2 2 0 0 0 20 18V6A2 2 0 0 0 18 4H6A2 2 0 0 0 4 6V18A2 2 0 0 0 6 20Z"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <span>Mock Interview</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar setCurrentPage={setCurrentPage} />
      <div className="main-content">
        <div className="content-wrapper">{renderPage()}</div>
      </div>
    </div>
  );
}

export default Dashboard;
