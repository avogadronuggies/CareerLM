"""
Resume Routes Module

This module defines the API endpoints for resume-related operations including
optimization, skill gap analysis, and study materials generation.
"""

import json
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

# Import centralized parser
from app.services.resume_parser import ResumeParser, get_parser

# Import service modules
from app.services.resume_optimizer import optimize_resume_logic
from app.services.skill_gap_analyzer import analyze_skill_gap

# Import Supabase client
from supabase_client import supabase

router = APIRouter()


@router.post("/optimize")
async def optimize_resume(
    user_id: str = Form(...),
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Optimize a resume against a job description.
    
    This endpoint performs:
    1. Text extraction from the resume PDF
    2. Section parsing and analysis
    3. Resume optimization suggestions via LLM
    4. ATS scoring
    5. Skill gap analysis
    6. Persistence to Supabase
    
    Args:
        user_id: The user's unique identifier.
        resume: The uploaded resume file (PDF).
        job_description: The target job description.
        
    Returns:
        JSON response with optimization results, ATS score, and career analysis.
    """
    # 1️⃣ Read resume bytes once
    resume_bytes = await resume.read()
    
    # 2️⃣ Use centralized parser to extract text and sections
    parser = get_parser()
    resume_text, sections = parser.parse_resume(resume_bytes, filename=resume.filename)
    
    # 3️⃣ Run optimizer logic with pre-parsed text and sections
    analysis_result = optimize_resume_logic(resume_text, sections, job_description)
    
    # 4️⃣ Run skill gap analysis with pre-parsed text
    skill_gap_result = analyze_skill_gap(resume_text, filename=resume.filename)

    # 5️⃣ Build response object
    result = {
        "sections": sections,
        "analysis": {
            "gaps": analysis_result.get("gaps", []),
            "alignment_suggestions": analysis_result.get("alignment_suggestions", []),
            "prompt": analysis_result.get("prompt", "")
        },
        "ats_score": analysis_result.get("ats_score"),
        "ats_analysis": analysis_result.get("ats_analysis", {}),
        "careerAnalysis": {
            "user_skills": skill_gap_result.get("user_skills", []),
            "total_skills_found": skill_gap_result.get("total_skills_found", 0),
            "career_matches": skill_gap_result.get("career_matches", []),
            "top_3_careers": skill_gap_result.get("top_3_careers", []),
            "ai_recommendations": skill_gap_result.get("ai_recommendations", ""),
            "analysis_summary": skill_gap_result.get("analysis_summary", {})
        } if "error" not in skill_gap_result else None,
        "summary": "",
        "filename": resume.filename,
    }

    # 6️⃣ Insert/Update Supabase
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
        "content": json.dumps(result),
        "ats_score": result.get("ats_score"),
        "raw_file_path": result.get("filename"),
        "notes": ""
    }).execute()

    return JSONResponse({
        "optimization": result,
        "resume_id": resume_id,
        "version_stored": stored_version.data
    })


@router.post("/skill-gap-analysis")
async def skill_gap_analysis(resume: UploadFile = File(...)):
    """
    Analyze career matches based on skills clustering.
    
    Returns probability-based career recommendations and skill gaps for each career.
    
    Args:
        resume: The uploaded resume file (PDF).
        
    Returns:
        JSON response with skill analysis and career recommendations.
    """
    try:
        # Read resume file
        resume_bytes = await resume.read()
        
        # Use centralized parser to extract text
        parser = get_parser()
        resume_text = parser.extract_text(resume_bytes, filename=resume.filename)
        
        # Perform career clustering analysis with pre-parsed text
        analysis_result = analyze_skill_gap(resume_text, filename=resume.filename)
        
        # Check for errors
        if "error" in analysis_result:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": analysis_result["error"]
                }
            )
        
        return JSONResponse({
            "success": True,
            "filename": resume.filename,
            "user_skills": analysis_result["user_skills"],
            "total_skills_found": analysis_result["total_skills_found"],
            "career_matches": analysis_result["career_matches"],
            "top_3_careers": analysis_result["top_3_careers"],
            "ai_recommendations": analysis_result["ai_recommendations"],
            "analysis_summary": analysis_result["analysis_summary"]
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to analyze career matches"
            }
        )


@router.post("/generate-study-materials")
async def generate_study_materials(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    target_career: str = Form(None),
    missing_skills: str = Form(None)
):
    """
    Generate personalized study materials and learning resources based on skill gaps.
    
    Args:
        resume: The uploaded resume file (PDF).
        job_description: The target job description.
        target_career: Optional target career path.
        missing_skills: Optional JSON string of missing skills.
        
    Returns:
        JSON response with study materials and learning resources.
    """
    try:
        # Read resume file
        resume_bytes = await resume.read()
        
        # Import the function
        from app.services.study_materials_generator import generate_learning_resources
        
        # Parse missing skills if provided
        skills_list = json.loads(missing_skills) if missing_skills else []
        
        # Generate study materials
        study_result = generate_learning_resources(
            resume_bytes,
            job_description,
            filename=resume.filename,
            target_career=target_career,
            missing_skills=skills_list
        )
        
        return JSONResponse({
            "success": True,
            "filename": resume.filename,
            "target_career": target_career,
            "learning_resources": study_result.get("learning_resources", []),
            "study_plan": study_result.get("study_plan", ""),
            "recommended_courses": study_result.get("recommended_courses", []),
            "practice_projects": study_result.get("practice_projects", []),
            "certifications": study_result.get("certifications", []),
            "timeline": study_result.get("timeline", "")
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to generate study materials"
            }
        )
