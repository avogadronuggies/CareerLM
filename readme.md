# CareerLM

CareerLM is an AI-powered resume optimizer platform. It allows users to upload their resume (PDF or DOCX) and a job description, then analyzes gaps and provides alignment suggestions using an LLM (Ollama) backend.

## Project Structure

```
frontend-react/      # React app for resume upload and job description input
backend-fastapi/     # FastAPI backend for resume parsing and LLM integration
```

### Frontend (React)

- Upload resume (PDF/DOCX)
- Enter job description
- See gaps and suggestions below the Optimize button
- Run with:
  ```
  cd frontend-react
  npm install
  npm start
  ```

### Backend (FastAPI)

- Accepts resume and job description
- Parses PDF resumes using `pdfplumber`
- Extracts Experience, Skills, Projects sections
- Formats prompt and sends to Ollama LLM (default: llama3)
- Returns gaps and alignment suggestions
- Automatically starts Ollama server if not running
- Run with:
  ```
  cd backend-fastapi
  pip install -r requirements.txt
  python -m uvicorn app.main:app --reload
  ```

### Ollama LLM

- Make sure Ollama is installed locally
- The backend will start Ollama automatically if needed
- Default model: llama3 (can be changed in code)

## API Example

POST `/api/v1/resume/optimize`

- `resume`: file (PDF/DOCX)
- `job_description`: string

Returns JSON with gaps and alignment suggestions.

## Development Notes

- `.gitignore` is set up for Node, Python, VSCode, Docker, and temp files
- Backend and frontend are decoupled for easy development
- For best results, use plain text or well-structured PDF resumes

---

Feel free to contribute or customize the models and parsing logic!
