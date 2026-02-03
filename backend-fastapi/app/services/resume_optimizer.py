# app/services/resume_optimizer.py
import re
import pdfplumber
import io
from app.agents import resume_workflow, ResumeState


def parse_resume_sections(resume_text):
    """Parse resume into common sections"""
    sections = {
        "Contact": "",
        "Summary": "", 
        "Experience": "", 
        "Education": "",
        "Skills": "", 
        "Projects": "",
        "Certifications": "",
        "Other": ""
    }
    
    current = "Other"
    for line in resume_text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        # Try to identify section headers
        if re.match(r"contact|email|phone|address", line, re.I):
            current = "Contact"
        elif re.match(r"summary|objective|profile", line, re.I):
            current = "Summary"
        elif re.match(r"experience|work|employment|job", line, re.I):
            current = "Experience"
        elif re.match(r"education|degree|university|college|school", line, re.I):
            current = "Education"
        elif re.match(r"skills?|technologies|tools|languages", line, re.I):
            current = "Skills"
        elif re.match(r"projects?|portfolio", line, re.I):
            current = "Projects"
        elif re.match(r"certifications?|licenses", line, re.I):
            current = "Certifications"
            
        # Add content to the current section
        sections[current] += line + "\n"
    
    return sections


def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file bytes"""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def optimize_resume_logic(resume_content, job_description, filename=None):
    """
    AGENTIC VERSION - Uses LangGraph workflow
    """
    
    # ===== EXTRACT TEXT =====
    if filename and filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_content)
    else:
        try:
            resume_text = resume_content.decode("utf-8")
        except Exception:
            resume_text = str(resume_content)
    
    # ===== PARSE SECTIONS =====
    sections = parse_resume_sections(resume_text)
    
    # ===== INITIALIZE STATE =====
    initial_state: ResumeState = {
    # ===== INPUT =====
    "resume_text": resume_text,
    "job_description": job_description,
    "resume_sections": sections,

    # ===== ATS =====
    "ats_score": 0,
    "previous_ats_score": None,
    "ats_components": {},
    "ats_justification": [],
    "ats_ai_feedback": "",
    "previous_ats_score": None,

    # ===== SKILL GAP =====
    "user_skills": [],
    "skill_gaps": [],
    "career_matches": [],

    # ===== OPTIMIZATION =====
    "structure_suggestions": [],
    "alignment_suggestions": [],

    # ===== AGENT CONTROL =====
    "next_action": "",                
    "needs_ats_improvement": False,
    "iteration_count": 0,
    "max_iterations": 10,              
    "completed_steps": [],   
    "decision_reason": "",        
    "messages": []
}

    
    # ===== RUN THE AGENTIC WORKFLOW =====
    print("\nStarting agentic workflow...\n")
    final_state = resume_workflow.invoke(initial_state)
    
    return {
        # ATS Analysis
        "ats_score": final_state["ats_score"],
        "ats_analysis": {
            "component_scores": final_state["ats_components"],
            "justification": final_state["ats_justification"],
            "ai_analysis": final_state["ats_ai_feedback"]
        },
        
        # Skill Validation (NEW)
        "validated_skills": final_state.get("validated_skills", []),
        "gap_score": final_state.get("gap_score", 0.0),
        
        # Level Assessment (NEW)
        "level_assessment": final_state.get("level_assessment", {}),
        
        # Suggestions
        "gaps": [g["skill"] for g in final_state.get("skill_gaps", [])],  # Simple list for compatibility
        "detailed_gaps": final_state.get("skill_gaps", []),  # NEW - Full gap details
        "honest_improvements": final_state.get("honest_improvements", []),  # NEW
        "alignment_suggestions": final_state.get("alignment_suggestions", []),  # Legacy
        "structure_suggestions": final_state.get("structure_suggestions", []),
        
        # Career matches
        "career_matches": final_state.get("career_matches", [])[:3],
        "user_skills": final_state.get("user_skills", []),
        
        # Debug
        "agent_execution_log": final_state["messages"],
        "total_iterations": final_state["iteration_count"],
        "completed_steps": final_state.get("completed_steps", []),
        
        "_agentic": True,
        "_version": "3.0"  # Updated version
    }