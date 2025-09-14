import React, { useState } from "react";
import "./App.css";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleResumeChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleJDChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");
    if (!resumeFile || !jobDescription) {
      setError("Please upload a resume and enter a job description.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);
    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/resume/optimize",
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch response from backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h2>Resume Optimizer</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Upload Resume (PDF or DOCX): </label>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleResumeChange}
          />
        </div>
        <div>
          <label>Job Description:</label>
          <textarea
            value={jobDescription}
            onChange={handleJDChange}
            rows={6}
            cols={50}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Optimizing..." : "Optimize Resume"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
      {result && (
        <div
          className="result-box"
          style={{
            marginTop: 24,
            textAlign: "left",
            background: "#f4f4f4",
            padding: 16,
            borderRadius: 8,
          }}
        >
          {result.error ? (
            <div style={{ color: "red" }}>Error: {result.error}</div>
          ) : (
            <>
              <h3>Gaps:</h3>
              <ul>
                {result.gaps && result.gaps.length > 0 ? (
                  result.gaps.map((gap, idx) => <li key={idx}>{gap}</li>)
                ) : (
                  <li>None</li>
                )}
              </ul>
              <h3>Alignment Suggestions:</h3>
              <ul>
                {result.alignment_suggestions &&
                result.alignment_suggestions.length > 0 ? (
                  result.alignment_suggestions.map((s, idx) => (
                    <li key={idx}>{s}</li>
                  ))
                ) : (
                  <li>None</li>
                )}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
