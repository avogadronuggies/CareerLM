import io
import json
import pdfplumber
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.resume_optimizer import optimize_resume_logic
from supabase_client import supabase
import re

router = APIRouter()

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def parse_resume_sections(text: str):
    """Parse resume into sections: experience, projects, skills, education"""
    section_titles = ["Experience", "Projects", "Skills", "Education"]
    pattern = r"(?i)\b(" + "|".join(section_titles) + r")\b"
    splits = re.split(pattern, text)

    sections, current_section = {}, None
    for part in splits:
        part = part.strip()
        if not part:
            continue

        if part.lower() in [s.lower() for s in section_titles]:
            current_section = part.lower()
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += ("\n" if sections[current_section] else "") + part

    if "skills" in sections:
        skills_list = re.split(r"[,\n;]+", sections["skills"])
        sections["skills"] = [s.strip() for s in skills_list if s.strip()]

    return sections


@router.post("/optimize")
async def optimize_resume(
    user_id: str = Form(...),
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1️⃣ Extract raw text
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)

    # 2️⃣ Parse structured sections
    sections = parse_resume_sections(resume_text)

    # 3️⃣ Run optimizer logic
    analysis_result = optimize_resume_logic(resume_bytes, job_description, filename=resume.filename)

    analysis_result = optimize_resume_logic(resume_bytes, job_description, filename=resume.filename)

    result = {
        "sections": sections,
        "analysis": {
            "gaps": analysis_result.get("gaps", []),
            "alignment_suggestions": analysis_result.get("alignment_suggestions", []),
            "prompt": analysis_result.get("prompt", "")
        },
        "ats_score": None,
        "summary": "",
        "filename": resume.filename,
    }


    # 4️⃣ Insert/Update Supabase
    existing_resume = supabase.table("resumes").select("*").eq("user_id", user_id).execute()

    if existing_resume.data:
        resume_id = existing_resume.data[0]["resume_id"]
        new_version_number = existing_resume.data[0]["current_version"] + 1

        supabase.table("resumes").update({
            "current_version": new_version_number,
            "latest_update": datetime.utcnow().isoformat()
        }).eq("resume_id", resume_id).execute()

    else:
        resp = supabase.table("resumes").insert({
            "user_id": user_id,
            "template_type": "default",
            "current_version": 1,
            "latest_update": datetime.utcnow().isoformat()
        }).execute()

        resume_id = resp.data[0]["resume_id"]
        new_version_number = 1

    stored_version = supabase.table("resume_versions").insert({
        "resume_id": resume_id,
        "version_number": new_version_number,
        "content": json.dumps(result),   # ✅ ensure JSONB compatibility
        "ats_score": result.get("ats_score"),
        "raw_file_path": result.get("filename"),
        "notes": ""
    }).execute()

    return JSONResponse({
        "optimization": result,
        "resume_id": resume_id,
        "version_stored": stored_version.data
    })