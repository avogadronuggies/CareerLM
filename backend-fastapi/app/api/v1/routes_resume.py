# Resume optimization endpoint

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.resume_optimizer import optimize_resume_logic

router = APIRouter()

# Resume optimization endpoint
@router.post("/optimize")
async def optimize_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Read resume file content
    resume_content = await resume.read()
    # Pass file bytes and filename to optimizer for PDF support
    result = optimize_resume_logic(resume_content, job_description, filename=resume.filename)
    return JSONResponse(content=result)
