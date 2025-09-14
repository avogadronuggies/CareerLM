from fastapi import FastAPI
from app.api.v1 import routes_resume
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CareerLM Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Resume Optimizer routes
app.include_router(routes_resume.router, prefix="/api/v1/resume", tags=["Resume"])
