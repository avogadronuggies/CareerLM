// src/components/SkillGapAnalyzer.js
import React from "react";

function SkillGapAnalyzer({ resumeData }) {
  return (
    <div>
      <h2>Skill Gap Analyzer</h2>
      {resumeData ? <p>Checking skills for: {resumeData.filename}</p> : <p>No resume uploaded yet.</p>}
    </div>
  );
}

export default SkillGapAnalyzer;
