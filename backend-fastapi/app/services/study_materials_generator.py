import re
import pdfplumber
import io
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_pdf(file_bytes):
    """Extract text content from PDF file."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_current_experience_level(resume_text):
    """Determine experience level from resume."""
    resume_lower = resume_text.lower()
    
    # Count years of experience mentions
    years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
    years_matches = re.findall(years_pattern, resume_lower)
    
    if years_matches:
        max_years = max([int(y) for y in years_matches])
        if max_years >= 5:
            return "Senior"
        elif max_years >= 2:
            return "Mid-Level"
        else:
            return "Junior"
    
    # Check for keywords
    if any(word in resume_lower for word in ['senior', 'lead', 'principal', 'architect']):
        return "Senior"
    elif any(word in resume_lower for word in ['junior', 'entry', 'intern', 'graduate']):
        return "Junior"
    else:
        return "Mid-Level"


def generate_learning_resources(resume_content, job_description, filename=None, target_career=None, missing_skills=None):
    """Generate personalized study materials and learning paths."""
    try:
        # Extract text from resume
        if filename and filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_content)
        else:
            try:
                resume_text = resume_content.decode("utf-8")
            except Exception:
                resume_text = str(resume_content)
        
        # Determine experience level
        experience_level = extract_current_experience_level(resume_text)
        
        # Prepare skills list for prompt
        skills_text = ", ".join(missing_skills) if missing_skills else "key required skills"
        
        # Create comprehensive prompt for study materials
        prompt = f"""You are an expert career development advisor and learning path designer.

Current Situation:
- Experience Level: {experience_level}
- Target Career: {target_career or "Career Transition"}
- Key Skills to Learn: {skills_text}
- Job Requirements: {job_description[:500]}...

Generate a comprehensive, actionable learning plan with:

1. **Learning Resources** (5-7 items):
   - For each skill, provide specific resources (online courses, books, tutorials)
   - Include platform names (Coursera, Udemy, freeCodeCamp, YouTube channels, etc.)
   - Specify difficulty level (Beginner/Intermediate/Advanced)
   - Example format: "Python for Data Science (Coursera) - Beginner, 4 weeks"

2. **Recommended Courses** (3-5 courses):
   - Specific course names with platforms
   - Duration and cost estimate
   - Order them by priority

3. **Practice Projects** (3-5 projects):
   - Hands-on projects to build portfolio
   - Specific, achievable project ideas
   - Technologies/tools needed for each

4. **Certifications** (2-4 certifications):
   - Industry-recognized certifications relevant to the target role
   - Include provider (AWS, Google, Microsoft, etc.)
   - Approximate cost and preparation time

5. **Learning Timeline**:
   - Week-by-week breakdown for the first 3 months
   - Realistic time commitment (e.g., "10-15 hours/week")
   - Key milestones to track progress

Format each section clearly with headers. Be specific, practical, and prioritize based on job market demand."""

        # Use a different model for variety (mixtral for detailed planning)
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Different model for detailed planning
            messages=[
                {"role": "system", "content": "You are an expert career development advisor specializing in creating personalized learning paths."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000
        )

        response_text = completion.choices[0].message.content
        
        # Parse the response into structured format
        parsed_result = parse_study_materials(response_text)
        
        # Add full study plan text
        parsed_result["study_plan"] = response_text
        parsed_result["experience_level"] = experience_level
        parsed_result["target_career"] = target_career
        
        return parsed_result

    except Exception as e:
        return {
            "error": f"Failed to generate study materials: {str(e)}",
            "learning_resources": [],
            "recommended_courses": [],
            "practice_projects": [],
            "certifications": [],
            "timeline": "",
            "study_plan": ""
        }


def parse_study_materials(response_text):
    """Parse AI response into structured study materials."""
    result = {
        "learning_resources": [],
        "recommended_courses": [],
        "practice_projects": [],
        "certifications": [],
        "timeline": ""
    }
    
    current_section = None
    lines = response_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # Detect sections
        line_lower = line.lower()
        if 'learning resource' in line_lower:
            current_section = 'learning_resources'
            continue
        elif 'recommended course' in line_lower or 'courses' in line_lower:
            current_section = 'recommended_courses'
            continue
        elif 'practice project' in line_lower or 'projects' in line_lower:
            current_section = 'practice_projects'
            continue
        elif 'certification' in line_lower:
            current_section = 'certifications'
            continue
        elif 'timeline' in line_lower or 'learning timeline' in line_lower:
            current_section = 'timeline'
            continue
        
        # Extract content
        if current_section and line:
            # Remove bullets, numbers
            cleaned_line = re.sub(r'^[\d\.\-\*\•]+\s*', '', line).strip()
            
            if cleaned_line and not cleaned_line.startswith('#'):
                if current_section == 'timeline':
                    result[current_section] += cleaned_line + "\n"
                else:
                    # Skip section headers
                    if len(cleaned_line) > 10 and not cleaned_line.endswith(':'):
                        result[current_section].append(cleaned_line)
    
    return result


def generate_quick_recommendations(missing_skills, target_career):
    """Generate quick study recommendations without full resume analysis."""
    try:
        skills_text = ", ".join(missing_skills[:5]) if missing_skills else "required skills"
        
        prompt = f"""Provide quick learning recommendations for someone targeting a {target_career} role who needs to learn: {skills_text}

Format:
1. Top 3 online courses (with platform and duration)
2. Top 3 free resources (tutorials, documentation, YouTube channels)
3. Top 2 practice project ideas
4. Estimated timeline to become job-ready

Be concise and specific."""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a career advisor providing quick learning recommendations."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error generating recommendations: {str(e)}"
