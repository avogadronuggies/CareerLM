"""
Resume Optimizer Module

This module provides functionality to analyze resumes against job descriptions,
identifying gaps and providing alignment suggestions using LLM.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from app.services.ats_checker import get_ats_score

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def create_prompt(sections: dict, job_description: str) -> str:
    """
    Create a prompt for the LLM to analyze resume gaps.
    
    Args:
        sections: Dictionary of parsed resume sections.
        job_description: The target job description.
        
    Returns:
        Formatted prompt string.
    """
    experience = sections.get("experience", "").strip()
    skills = sections.get("skills", "").strip()
    projects = sections.get("projects", "").strip()
    
    return (
        f"Experience:\n{experience}\n\n"
        f"Skills:\n{skills}\n\n"
        f"Projects:\n{projects}\n\n"
        f"Job description:\n{job_description.strip()}\n\n"
        "Return the following:\n"
        "1. What gaps are there in the resume compared to the job description? \n"
        "Don't overthink and just return the gaps you find.\n"
        "2. How can the candidate align their resume better to the job description?\n"
    )


def groq_response(prompt: str) -> dict:
    """
    Get optimization suggestions from Groq LLM.
    
    Args:
        prompt: The formatted prompt to send to the LLM.
        
    Returns:
        Dictionary containing gaps, suggestions, and the original prompt.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        text = completion.choices[0].message.content

        # Extract structured info
        gaps, suggestions = [], []
        for line in text.splitlines():
            if line.strip().startswith("1."):
                gaps.append(line.strip()[2:].strip())
            elif line.strip().startswith("2."):
                suggestions.append(line.strip()[2:].strip())

        return {
            "gaps": gaps or [text],
            "alignment_suggestions": suggestions or [],
            "prompt": prompt
        }

    except Exception as e:
        return {"error": str(e), "prompt": prompt}


def optimize_resume_logic(resume_text: str, resume_sections: dict, job_description: str) -> dict:
    """
    Main function to optimize a resume against a job description.
    
    This function analyzes the resume content, identifies gaps compared to
    the job description, and provides ATS scoring.
    
    Args:
        resume_text: The extracted resume text.
        resume_sections: The parsed resume sections dictionary.
        job_description: The target job description.
        
    Returns:
        Dictionary containing gaps, suggestions, ATS score, and analysis.
    """
    # Create prompt for LLM
    prompt = create_prompt(resume_sections, job_description)
    
    # Get optimization suggestions from LLM
    result = groq_response(prompt)
    
    # Get ATS score and analysis
    ats_analysis = get_ats_score(resume_text, resume_sections, job_description)
    
    # Add ATS score to result
    result["ats_score"] = ats_analysis["overall_score"]
    result["ats_analysis"] = {
        "component_scores": ats_analysis["component_scores"],
        "justification": ats_analysis["justification"],
        "ai_analysis": ats_analysis["ai_analysis"]
    }
    
    return result
