// src/components/ColdEmailGenerator.js
import React from "react";

function ColdEmailGenerator({ resumeData }) {
  return (
    <div>
      <h2>Cold Email Generator</h2>
      {resumeData ? <p>Generating emails based on: {resumeData.filename}</p> : <p>No resume uploaded yet.</p>}
      <h1>Coming Soon...</h1>
    </div>
  );
}

export default ColdEmailGenerator;
