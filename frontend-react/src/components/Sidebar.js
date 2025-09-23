"use client"
import "./Sidebar.css"

function Sidebar({ setCurrentPage }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">CareerLM</h2>
        <div className="sidebar-subtitle">Your Career Assistant</div>
      </div>

      <nav className="sidebar-nav">
        <ul className="sidebar-menu">
          <li className="menu-item upload-item" onClick={() => setCurrentPage("upload")}>
            <span className="menu-icon">⬆</span>
            <span className="menu-text">Upload Resume</span>
          </li>

          <li className="menu-item" onClick={() => setCurrentPage("dashboard")}>
            <span className="menu-icon">📊</span>
            <span className="menu-text">Dashboard</span>
          </li>
          <li className="menu-item" onClick={() => setCurrentPage("resume_optimizer")}>
            <span className="menu-icon">📄</span>
            <span className="menu-text">Resume Optimizer</span>
          </li>
          <li className="menu-item" onClick={() => setCurrentPage("skill_gap")}>
            <span className="menu-icon">🎯</span>
            <span className="menu-text">Skill Gap Analyzer</span>
          </li>
          <li className="menu-item" onClick={() => setCurrentPage("mock_interview")}>
            <span className="menu-icon">🎤</span>
            <span className="menu-text">Mock Interview</span>
          </li>
          <li className="menu-item" onClick={() => setCurrentPage("cold_email")}>
            <span className="menu-icon">✉</span>
            <span className="menu-text">Cold Email Generator</span>
          </li>
          <li className="menu-item" onClick={() => setCurrentPage("study_planner")}>
            <span className="menu-icon">📚</span>
            <span className="menu-text">Study Planner</span>
          </li>
        </ul>
      </nav>
    </div>
  )
}

export default Sidebar
