# LLM logic for resume optimization


import re
import requests
import pdfplumber
import io

def parse_resume_sections(resume_text):
    # Very basic section extraction (expand as needed)
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

def create_ollama_prompt(sections, job_description):
    prompt = (
        f"Experience:\n{sections['Experience'].strip()}\n\n"
        f"Skills:\n{sections['Skills'].strip()}\n\n"
        f"Projects:\n{sections['Projects'].strip()}\n\n"
        f"Job description:\n{job_description.strip()}\n\n"
        "Return the following:\n1. What gaps are there in the resume compared to the job description?\n"
        "2. How can the candidate align their resume better to the job description?\n"
    )
    return prompt


OLLAMA_HOST = "http://localhost:11434"  # Change if your Ollama server is remote
OLLAMA_MODEL = "llama3"  # Change to your preferred model

def ollama_response(prompt):
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        print(f"Sending prompt to Ollama: {prompt[:200]}...")
        resp = requests.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "")
        gaps, suggestions = [], []
        for line in text.splitlines():
            if line.strip().startswith("1."):
                gaps.append(line.strip()[2:].strip())
            elif line.strip().startswith("2."):
                suggestions.append(line.strip()[2:].strip())
        return {
            "gaps": gaps or [text],
            "alignment_suggestions": suggestions,
            "prompt": prompt
        }
    except Exception as e:
        print(f"Ollama API error: {e}")
        return {"error": str(e), "prompt": prompt}

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def optimize_resume_logic(resume_content, job_description, filename=None):
    # If filename ends with .pdf, parse as PDF
    if filename and filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_content)
    else:
        try:
            resume_text = resume_content.decode("utf-8")
        except Exception:
            resume_text = str(resume_content)
    sections = parse_resume_sections(resume_text)
    prompt = create_ollama_prompt(sections, job_description)
    ollama_result = ollama_response(prompt)
    return ollama_result
