// src/components/StudyPlanner.js
import React from "react";

function StudyPlanner({ resumeData }) {
  return (
    <div>
      <h2>Study Planner</h2>
      {resumeData ? <p>Creating plan for: {resumeData.filename}</p> : <p>No resume uploaded yet.</p>}
    </div>
  );
}

export default StudyPlanner;
