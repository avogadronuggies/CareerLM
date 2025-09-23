// src/components/MockInterview.js
import React from "react";

function MockInterview({ resumeData }) {
  return (
    <div>
      <h2>Mock Interview</h2>
      {resumeData ? <p>Preparing questions based on: {resumeData.filename}</p> : <p>No resume uploaded yet.</p>}
    </div>
  );
}

export default MockInterview;
