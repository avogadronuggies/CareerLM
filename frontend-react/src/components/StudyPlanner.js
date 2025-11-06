// src/components/StudyPlanner.js
import React, { useState, useEffect } from "react";
import "./StudyPlanner.css";
import { formatText } from "../utils/textFormatter";

function StudyPlanner({ resumeData }) {
  const [studyMaterials, setStudyMaterials] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");

  // Auto-load study materials from resumeData if available
  useEffect(() => {
    if (resumeData?.studyMaterials) {
      setStudyMaterials(resumeData.studyMaterials);
    }
  }, [resumeData]);

  if (!resumeData) {
    return (
      <div className="study-planner-container">
        <div className="empty-state-card">
          <h2>No Study Plan Available</h2>
          <p>
            Please upload your resume and job description in Resume Optimizer
            first
          </p>
          <p className="hint">
            The system will automatically generate personalized learning
            materials for you
          </p>
        </div>
      </div>
    );
  }

  if (!studyMaterials) {
    return (
      <div className="study-planner-container">
        <div className="empty-state-card">
          <h2>Generating Study Materials...</h2>
          <p>Please wait while we create your personalized learning plan</p>
        </div>
      </div>
    );
  }

  const {
    target_career,
    learning_resources,
    recommended_courses,
    practice_projects,
    certifications,
    timeline,
    study_plan,
  } = studyMaterials;

  return (
    <div className="study-planner-container">
      <div className="study-header">
        <h2>Personalized Study Plan</h2>
        <p>
          Your customized learning path for{" "}
          {target_career || "career development"}
        </p>
      </div>

      {/* Summary Card */}
      <div className="summary-grid">
        <div className="summary-item">
          <div className="summary-content">
            <h3>{learning_resources?.length || 0}</h3>
            <p>Learning Resources</p>
          </div>
        </div>
        <div className="summary-item">
          <div className="summary-content">
            <h3>{recommended_courses?.length || 0}</h3>
            <p>Recommended Courses</p>
          </div>
        </div>
        <div className="summary-item">
          <div className="summary-content">
            <h3>{practice_projects?.length || 0}</h3>
            <p>Practice Projects</p>
          </div>
        </div>
        <div className="summary-item">
          <div className="summary-content">
            <h3>{certifications?.length || 0}</h3>
            <p>Certifications</p>
          </div>
        </div>
      </div>

      {/* Tabbed Content */}
      <div className="study-tabs-container">
        <div className="study-tabs-header">
          <button
            className={`study-tab ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            Overview
          </button>
          <button
            className={`study-tab ${activeTab === "resources" ? "active" : ""}`}
            onClick={() => setActiveTab("resources")}
          >
            Resources
          </button>
          <button
            className={`study-tab ${activeTab === "courses" ? "active" : ""}`}
            onClick={() => setActiveTab("courses")}
          >
            Courses
          </button>
          <button
            className={`study-tab ${activeTab === "projects" ? "active" : ""}`}
            onClick={() => setActiveTab("projects")}
          >
            Projects
          </button>
          <button
            className={`study-tab ${activeTab === "certs" ? "active" : ""}`}
            onClick={() => setActiveTab("certs")}
          >
            Certifications
          </button>
          <button
            className={`study-tab ${activeTab === "timeline" ? "active" : ""}`}
            onClick={() => setActiveTab("timeline")}
          >
            Timeline
          </button>
        </div>

        <div className="study-tab-content">
          {/* Overview Tab */}
          {activeTab === "overview" && (
            <div className="overview-content">
              <h3>Complete Study Plan</h3>
              <div className="study-plan-text">
                <div
                  dangerouslySetInnerHTML={{ __html: formatText(study_plan) }}
                />
              </div>
            </div>
          )}

          {/* Learning Resources Tab */}
          {activeTab === "resources" && (
            <div className="resources-content">
              <h3>Learning Resources</h3>
              <p className="tab-subtitle">
                Curated resources to build your skills
              </p>
              {learning_resources && learning_resources.length > 0 ? (
                <div className="resources-list">
                  {learning_resources.map((resource, idx) => {
                    return (
                      <div key={idx} className="resource-card">
                        <div className="resource-number">{idx + 1}</div>
                        <div className="resource-content">
                          <div
                            dangerouslySetInnerHTML={{
                              __html: formatText(resource),
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="empty-message">No learning resources available</p>
              )}
            </div>
          )}

          {/* Recommended Courses Tab */}
          {activeTab === "courses" && (
            <div className="courses-content">
              <h3>Recommended Courses</h3>
              <p className="tab-subtitle">
                Top courses to accelerate your learning
              </p>
              {recommended_courses && recommended_courses.length > 0 ? (
                <div className="courses-list">
                  {recommended_courses.map((course, idx) => {
                    return (
                      <div key={idx} className="course-card">
                        <div className="course-badge">{idx + 1}</div>
                        <div className="course-details">
                          <div
                            dangerouslySetInnerHTML={{
                              __html: formatText(course),
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="empty-message">
                  No course recommendations available
                </p>
              )}
            </div>
          )}

          {/* Practice Projects Tab */}
          {activeTab === "projects" && (
            <div className="projects-content">
              <h3>Practice Projects</h3>
              <p className="tab-subtitle">
                Build your portfolio with these projects
              </p>
              {practice_projects && practice_projects.length > 0 ? (
                <div className="projects-list">
                  {practice_projects.map((project, idx) => {
                    return (
                      <div key={idx} className="project-card">
                        <div className="project-details">
                          <h4>Project {idx + 1}</h4>
                          <div
                            dangerouslySetInnerHTML={{
                              __html: formatText(project),
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="empty-message">No project ideas available</p>
              )}
            </div>
          )}

          {/* Certifications Tab */}
          {activeTab === "certs" && (
            <div className="certs-content">
              <h3>Recommended Certifications</h3>
              <p className="tab-subtitle">
                Industry-recognized credentials to boost your profile
              </p>
              {certifications && certifications.length > 0 ? (
                <div className="certs-list">
                  {certifications.map((cert, idx) => {
                    return (
                      <div key={idx} className="cert-card">
                        <div className="cert-badge">
                          <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" />
                          </svg>
                        </div>
                        <div className="cert-details">
                          <div
                            dangerouslySetInnerHTML={{
                              __html: formatText(cert),
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="empty-message">
                  No certification recommendations available
                </p>
              )}
            </div>
          )}

          {/* Timeline Tab */}
          {activeTab === "timeline" && (
            <div className="timeline-content">
              <h3>Learning Timeline</h3>
              <p className="tab-subtitle">Your roadmap to success</p>
              {timeline ? (
                <div className="timeline-display">
                  <div
                    dangerouslySetInnerHTML={{ __html: formatText(timeline) }}
                  />
                </div>
              ) : (
                <p className="empty-message">No timeline available</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StudyPlanner;
