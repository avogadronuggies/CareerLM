// src/components/ResumeOptimizer.js
import React from "react";

function ResumeOptimizer({ resumeData }) {
  return (
    <div>
      <h2>Resume Optimizer</h2>
      {resumeData ? <p>Analyzing: {resumeData.filename}</p> : <p>No resume uploaded yet.</p>}
    </div>
  );
}

export default ResumeOptimizer;
