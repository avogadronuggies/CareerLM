import re
import pdfplumber
import io
from groq import Groq
import os
from dotenv import load_dotenv
import numpy as np

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file bytes"""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

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
        "Publications": "",
        "Awards": "",
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
        elif re.match(r"publications?|papers|research", line, re.I):
            current = "Publications"
        elif re.match(r"awards?|honors|achievements", line, re.I):
            current = "Awards"
            
        # Add content to the current section
        sections[current] += line + "\n"
    
    return sections

def calculate_structure_score(sections):
    """Calculate a score based on resume structure and completeness"""
    # Essential sections that should exist in a good resume
    essential_sections = ["Contact", "Experience", "Education", "Skills"]
    helpful_sections = ["Summary", "Projects", "Certifications", "Publications", "Awards"]
    
    # Check for presence and content in essential sections
    essential_score = 0
    for section in essential_sections:
        if sections[section].strip():
            # Has meaningful content (more than just a header)
            if len(sections[section].strip()) > 20:  # Arbitrary min length
                essential_score += 25  # Max 100 for essential sections
    
    # Bonus points for helpful sections
    helpful_score = 0
    for section in helpful_sections:
        if sections[section].strip():
            if len(sections[section].strip()) > 20:
                helpful_score += 10  # Max 50 for helpful sections
    
    # Normalize scores
    normalized_essential = min(100, essential_score)
    normalized_helpful = min(50, helpful_score)
    
    structure_score = (normalized_essential * 0.7) + (normalized_helpful * 0.3)
    return round(structure_score)

def calculate_keyword_score(resume_text, job_description):
    """Calculate keyword matching score between resume and job description"""
    if not job_description.strip():
        return 75  # Default score if no job description provided
    
    # Extract potential keywords from job description
    # Focus on nouns, technical terms, and skills
    job_words = set(re.findall(r'\b[A-Za-z][A-Za-z0-9+#\-\.]{2,}\b', job_description.lower()))
    resume_words = set(re.findall(r'\b[A-Za-z][A-Za-z0-9+#\-\.]{2,}\b', resume_text.lower()))
    
    # Common words to exclude
    stop_words = {
        'the', 'and', 'for', 'with', 'that', 'this', 'you', 'not', 'are', 'from', 'your',
        'have', 'has', 'had', 'was', 'were', 'will', 'would', 'should', 'could', 'can',
        'our', 'their', 'his', 'her', 'its', 'they', 'them', 'these', 'those', 'been',
        'being', 'did', 'does', 'doing', 'done', 'who', 'what', 'when', 'where', 'why',
        'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'some', 'such',
        'than', 'too', 'very', 'just', 'own'
    }
    
    # Filter out common stop words
    job_keywords = job_words - stop_words
    resume_keywords = resume_words - stop_words
    
    # Calculate match percentage
    if not job_keywords:
        return 75  # Default if no meaningful keywords found
    
    matched_keywords = job_keywords.intersection(resume_keywords)
    match_percentage = (len(matched_keywords) / len(job_keywords)) * 100
    
    # Scale the score - 0% match = 0, 50% match = 75, 100% match = 100
    # This rewards good matches while not being too strict
    if match_percentage <= 50:
        keyword_score = match_percentage * 1.5
    else:
        keyword_score = 75 + ((match_percentage - 50) * 0.5)
    
    return round(min(100, keyword_score))

def calculate_content_quality_score(resume_text):
    """Analyze content quality factors like action verbs, quantification, etc."""
    
    # Check for action verbs at start of bullets (common resume best practice)
    action_verbs = [
        'achieved', 'accelerated', 'accomplished', 'administered', 'advanced', 'analyzed',
        'architected', 'assembled', 'assessed', 'attained', 'authored', 'automated',
        'balanced', 'boosted', 'briefed', 'budgeted', 'built', 'calculated', 'captured',
        'centralized', 'chaired', 'championed', 'clarified', 'coached', 'collaborated',
        'communicated', 'compiled', 'completed', 'composed', 'computed', 'conceptualized',
        'conducted', 'consolidated', 'constructed', 'consulted', 'contacted', 'contributed',
        'controlled', 'converted', 'coordinated', 'created', 'customized', 'decreased',
        'defined', 'delegated', 'delivered', 'deployed', 'designed', 'detected', 'determined',
        'developed', 'devised', 'diagnosed', 'directed', 'discovered', 'dispatched',
        'distributed', 'documented', 'doubled', 'drafted', 'drove', 'earned', 'edited',
        'eliminated', 'enabled', 'enhanced', 'ensured', 'established', 'evaluated',
        'examined', 'executed', 'expanded', 'expedited', 'facilitated', 'fixed', 'formulated',
        'founded', 'gained', 'generated', 'guided', 'handled', 'headed', 'helped',
        'identified', 'implemented', 'improved', 'increased', 'influenced', 'informed',
        'initiated', 'inspected', 'installed', 'instituted', 'instructed', 'integrated',
        'interpreted', 'interviewed', 'introduced', 'invented', 'investigated', 'launched',
        'led', 'leveraged', 'maintained', 'managed', 'marketed', 'maximized', 'measured',
        'mediated', 'modernized', 'modified', 'monitored', 'motivated', 'navigated',
        'negotiated', 'operated', 'optimized', 'orchestrated', 'organized', 'originated',
        'overhauled', 'oversaw', 'performed', 'persuaded', 'pioneered', 'planned',
        'prepared', 'presented', 'processed', 'procured', 'produced', 'programmed',
        'promoted', 'provided', 'publicized', 'published', 'purchased', 'recommended',
        'reconciled', 'recorded', 'recruited', 'redesigned', 'reduced', 'reengineered',
        'referred', 'reformed', 'reinvented', 'released', 'remodeled', 'repaired',
        'replaced', 'reported', 'represented', 'researched', 'resolved', 'restored',
        'restructured', 'retrieved', 'revamped', 'reviewed', 'revised', 'revitalized',
        'saved', 'scheduled', 'screened', 'secured', 'selected', 'separated', 'served',
        'serviced', 'set', 'settled', 'shaped', 'shared', 'showed', 'simplified',
        'simulated', 'solved', 'sorted', 'spearheaded', 'specified', 'standardized',
        'stimulated', 'streamlined', 'strengthened', 'structured', 'studied', 'submitted',
        'summarized', 'supervised', 'supported', 'surpassed', 'surveyed', 'synthesized',
        'systematized', 'tabulated', 'targeted', 'taught', 'tested', 'tracked',
        'trained', 'transformed', 'translated', 'trimmed', 'tripled', 'troubleshot',
        'tutored', 'unified', 'updated', 'upgraded', 'utilized', 'validated',
        'valued', 'verified', 'visualized', 'wrote'
    ]
    
    # Count bullet points that start with action verbs
    lines = resume_text.splitlines()
    bullet_lines = [line.strip() for line in lines if line.strip().startswith(('-', '•', '*', '✓'))]
    
    action_verb_count = 0
    for line in bullet_lines:
        # Remove the bullet and check if first word is an action verb
        cleaned_line = re.sub(r'^[-•*✓]\s*', '', line).strip().lower()
        first_word = cleaned_line.split(' ')[0].rstrip(',.:;')
        if first_word in action_verbs:
            action_verb_count += 1
    
    # Calculate action verb percentage (if any bullet points)
    action_verb_score = 0
    if bullet_lines:
        action_verb_percentage = (action_verb_count / len(bullet_lines)) * 100
        action_verb_score = min(100, action_verb_percentage)
    
    # Check for metrics and quantifiable achievements
    metrics_pattern = r'\b\d+%|\$\d+|\d+\s*(percent|dollars|users|clients|people|customers|sales|revenue|growth|increase|decrease|reduction)\b'
    metrics_matches = re.findall(metrics_pattern, resume_text.lower())
    
    # Score based on number of metrics (diminishing returns)
    if metrics_matches:
        metrics_score = min(100, len(metrics_matches) * 20)
    else:
        metrics_score = 0
    
    # Overall content quality is weighted between action verbs and metrics
    content_score = (action_verb_score * 0.6) + (metrics_score * 0.4)
    return round(content_score)

def calculate_formatting_score(resume_text):
    """Check for good formatting practices in resumes"""
    
    lines = resume_text.splitlines()
    
    # Check consistent use of bullet points
    bullet_pattern = r'^[-•*✓]\s+'
    has_bullets = any(re.match(bullet_pattern, line.strip()) for line in lines)
    
    # Check for appropriate line spacing (not too compact, not too sparse)
    blank_line_count = sum(1 for line in lines if not line.strip())
    total_lines = len(lines)
    blank_ratio = blank_line_count / total_lines if total_lines > 0 else 0
    
    # Check for consistent date formatting
    date_patterns = [
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',  # Month Year
        r'\b\d{2}/\d{2}/\d{4}\b',  # MM/DD/YYYY
        r'\b\d{4}-\d{2}\b'         # YYYY-MM
    ]
    
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, resume_text))
    
    has_consistent_dates = len(dates) >= 2
    
    # Calculate formatting score
    formatting_score = 0
    
    # Bullet points
    if has_bullets:
        formatting_score += 30
    
    # Appropriate spacing
    if 0.05 <= blank_ratio <= 0.3:  # Good spacing range
        formatting_score += 40
    elif blank_ratio > 0 and blank_ratio < 0.5:  # Acceptable spacing
        formatting_score += 20
    
    # Date consistency
    if has_consistent_dates:
        formatting_score += 30
    
    return formatting_score

def get_ats_score_components(resume_bytes, job_description, filename=None):
    """Calculate ATS score components for a resume"""
    
    # Parse resume text
    if filename and filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_bytes)
    else:
        try:
            resume_text = resume_bytes.decode("utf-8")
        except Exception:
            resume_text = str(resume_bytes)
            
    # Parse resume into sections
    sections = parse_resume_sections(resume_text)
    
    # Calculate individual component scores
    structure_score = calculate_structure_score(sections)
    keyword_score = calculate_keyword_score(resume_text, job_description)
    content_score = calculate_content_quality_score(resume_text)
    formatting_score = calculate_formatting_score(resume_text)
    
    # Calculate overall ATS score with weights
    weights = {
        'structure': 0.25,
        'keywords': 0.35,
        'content': 0.25,
        'formatting': 0.15
    }
    
    overall_score = round(
        structure_score * weights['structure'] +
        keyword_score * weights['keywords'] +
        content_score * weights['content'] +
        formatting_score * weights['formatting']
    )
    
    # Generate justification for score
    justifications = []
    
    # Structure justification
    if structure_score >= 80:
        justifications.append("Strong resume structure with all essential sections.")
    elif structure_score >= 60:
        justifications.append("Good resume structure, but could improve some sections.")
    else:
        justifications.append("Resume is missing key sections that ATS systems expect.")
        
    # Keyword justification
    if keyword_score >= 80:
        justifications.append("Excellent keyword matching with job description.")
    elif keyword_score >= 60:
        justifications.append("Decent keyword matching, but some key terms are missing.")
    else:
        justifications.append("Poor keyword alignment with the job description.")
        
    # Content justification
    if content_score >= 80:
        justifications.append("Strong use of action verbs and quantifiable achievements.")
    elif content_score >= 60:
        justifications.append("Good content, but could use more action verbs or metrics.")
    else:
        justifications.append("Content lacks action verbs and measurable achievements.")
        
    # Formatting justification
    if formatting_score >= 80:
        justifications.append("Clean, consistent formatting that ATS systems can parse easily.")
    elif formatting_score >= 60:
        justifications.append("Acceptable formatting, but some inconsistencies may affect parsing.")
    else:
        justifications.append("Formatting issues may prevent proper ATS parsing.")
    
    # Add detailed AI analysis with LLM
    ai_analysis = generate_ats_feedback(resume_text, job_description, overall_score)
    
    return {
        "overall_score": overall_score,
        "component_scores": {
            "structure_score": structure_score,
            "keyword_score": keyword_score,
            "content_score": content_score,
            "formatting_score": formatting_score
        },
        "justification": justifications,
        "ai_analysis": ai_analysis
    }

def generate_ats_feedback(resume_text, job_description, overall_score):
    """Generate detailed AI feedback on the resume's ATS-friendliness"""
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyst.
    
    Below is a resume and a job description. The resume has received an ATS score of {overall_score}/100.
    
    Resume:
    {resume_text[:3000]}  # Limiting length to avoid token limits
    
    Job Description:
    {job_description[:1000]}
    
    Based on your expertise in ATS systems and resume optimization, provide THREE specific, actionable suggestions to improve this resume's ATS compatibility. Focus on:
    1. Format improvements for better parsing
    2. Content optimization for keyword matching
    3. Structure enhancements for ATS readability
    
    Provide your response as a list of 3 numbered suggestions, each with a brief explanation.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert resume analyst helping job seekers improve their ATS compatibility."},
                {"role": "user", "content": prompt},
            ],
        )
        
        ai_feedback = completion.choices[0].message.content
        
        # Clean up feedback if needed
        return ai_feedback
        
    except Exception as e:
        # Return a generic response if API call fails
        return f"Error generating AI feedback: {str(e)}"

def get_ats_score(resume_bytes, job_description, filename=None):
    """Main function to get ATS score and analysis"""
    return get_ats_score_components(resume_bytes, job_description, filename)