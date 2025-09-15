import re
import pdfplumber
import io
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def parse_resume_sections(resume_text):
    sections = {"Experience": "", "Skills": "", "Projects": ""}
    current = None
    for line in resume_text.splitlines():
        line = line.strip()
        if re.match(r"experience", line, re.I):
            current = "Experience"
        elif re.match(r"skills?", line, re.I):
            current = "Skills"
        elif re.match(r"projects?", line, re.I):
            current = "Projects"
        elif current and line:
            sections[current] += line + "\n"
    return sections


def create_prompt(sections, job_description):
    return (
        f"Experience:\n{sections['Experience'].strip()}\n\n"
        f"Skills:\n{sections['Skills'].strip()}\n\n"
        f"Projects:\n{sections['Projects'].strip()}\n\n"
        f"Job description:\n{job_description.strip()}\n\n"
        "Return the following:\n"
        "1. What gaps are there in the resume compared to the job description?\n"
        "2. How can the candidate align their resume better to the job description?\n"
    )


def groq_response(prompt: str):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # You can switch to "llama3-70b-8192" if needed
            messages=[
                {"role": "system", "content": "You are a helpful career assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        text = completion.choices[0].message.content

        # Extract structured info (like you were doing for Ollama)
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


def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def optimize_resume_logic(resume_content, job_description, filename=None):
    # PDF parsing
    if filename and filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_content)
    else:
        try:
            resume_text = resume_content.decode("utf-8")
        except Exception:
            resume_text = str(resume_content)

    sections = parse_resume_sections(resume_text)
    prompt = create_prompt(sections, job_description)
    result = groq_response(prompt)
    return result
