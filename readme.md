# CareerLM 🚀

AI-powered career assistant that helps job seekers optimize resumes, identify skill gaps, and prepare for interviews.

## Features

- **Resume Optimizer** – ATS scoring, gap analysis, and AI suggestions
- **Skill Gap Analyzer** – Career path matching with skill recommendations  
- **Mock Interview** – AI interview practice with feedback
- **Cold Email Generator** – Personalized outreach templates
- **Study Planner** – Learning paths for missing skills

## Tech Stack

```
Frontend:  React
Backend:   FastAPI + LangGraph Agents
AI:        Groq (llama-3.1-8b-instant)
Database:  PostgreSQL (Supabase)
```

## Quick Start

```bash
# Backend
cd backend-fastapi
pip install -r requirements.txt
# Add .env with SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY
uvicorn app.main:app --reload

# Frontend
cd frontend-react
npm install
npm start
```

## Project Structure

```
CareerLM/
├── frontend-react/     # React app
│   └── src/
│       ├── components/ # UI components
│       ├── pages/      # Home, Dashboard, Auth
│       └── context/    # User session
│
└── backend-fastapi/    # FastAPI server
    └── app/
        ├── agents/     # LangGraph workflow
        ├── services/   # Business logic
        └── api/        # REST endpoints
```

**Built with ❤️ by [avogadronuggies](https://github.com/avogadronuggies)**
