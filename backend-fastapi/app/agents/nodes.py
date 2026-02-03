# app/agents/nodes.py
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

from app.agents.state import ResumeState
from app.services.ats_checker import get_ats_score_components
from app.services.skill_gap_analyzer import analyze_skill_gap

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.7
)


# =====================================
# COORDINATOR AGENT - Brain of the system
# =====================================
# app/agents/nodes.py - UPDATE COORDINATOR

def coordinator_agent(state: ResumeState) -> ResumeState:
    """
    Enhanced coordinator with skill validation and learning path flow
    """
    messages = state.get("messages", [])
    ats_score = state.get("ats_score", 0)
    iteration = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 7)  # Increased for new steps
    completed = state.get("completed_steps", [])

    # HARD STOP
    if iteration >= max_iterations:
        messages.append("🧭 Coordinator: Max iterations reached. Stopping.")
        return {
            **state,
            "next_action": "complete",
            "decision_reason": "Max iterations reached",
            "messages": messages
        }

    iteration += 1

    # 1️⃣ First step: ATS analysis
    if ats_score == 0 and "analyze_ats" not in completed:
        messages.append("🧭 Coordinator: Starting with ATS analysis")
        next_action = "analyze_ats"
        reason = "Initial ATS evaluation"

    # 2️⃣ Poor ATS → fix structure first
    elif ats_score < 60 and "fix_structure" not in completed:
        messages.append(f"🧭 Coordinator: ATS score {ats_score}/100. Fixing structure first.")
        next_action = "fix_structure"
        state["needs_ats_improvement"] = True
        reason = "Critical structure issues"

    # 3️⃣ Reanalyze after structure fix
    elif state.get("needs_ats_improvement") and "reanalyze_ats" not in completed:
        messages.append("🧭 Coordinator: Re-analyzing ATS after fixes")
        next_action = "reanalyze_ats"
        reason = "Measure improvement"

    # 4️⃣ Validate actual skills (proceed regardless of ATS score after structure fixes done)
    elif "validate_skills" not in completed and ("analyze_ats" in completed or "reanalyze_ats" in completed):
        if ats_score >= 60:
            messages.append("🧭 Coordinator: ATS acceptable. Validating actual skills with evidence.")
        else:
            messages.append(f"🧭 Coordinator: ATS still {ats_score}/100, but proceeding to skill validation.")
        next_action = "validate_skills"
        reason = "Evidence-based skill validation"

    # 5️⃣ After validation → analyze gaps honestly
    elif "validate_skills" in completed and "analyze_gaps" not in completed:
        messages.append("🧭 Coordinator: Skills validated. Analyzing real gaps vs JD requirements.")
        next_action = "analyze_gaps"
        reason = "Honest gap identification"

    # 6️⃣ NEW - Assess proficiency levels
    elif "analyze_gaps" in completed and "assess_levels" not in completed:
        messages.append("🧭 Coordinator: Gaps identified. Assessing required proficiency levels.")
        next_action = "assess_levels"
        reason = "Level assessment for learning path"

    # 7️⃣ Finally → honest content optimization
    elif "assess_levels" in completed and "optimize_content" not in completed:
        messages.append("🧭 Coordinator: Creating honest resume optimization suggestions.")
        next_action = "optimize_content"
        reason = "Evidence-based improvements only"

    # 8️⃣ Done
    else:
        messages.append("✅ Coordinator: Complete analysis pipeline finished.")
        next_action = "complete"
        reason = "All steps completed"

    messages.append(f"  ➡️ Next: {next_action} | Reason: {reason}")

    return {
        **state,
        "iteration_count": iteration,
        "next_action": next_action,
        "decision_reason": reason,
        "messages": messages
    }
# =====================================
# ATS ANALYZER AGENT
# =====================================
def ats_analyzer_agent(state: ResumeState) -> ResumeState:
    messages = state.get("messages", [])
    messages.append("ATS Analyzer: Scanning resume for ATS compatibility...")

    # 🔑 store previous score
    prev_score = state.get("ats_score")

    resume_bytes = state["resume_text"].encode("utf-8")
    ats_result = get_ats_score_components(
        resume_bytes,
        state["job_description"],
        filename="resume.txt"
    )

    messages.append(
        f"ATS Analyzer: Score = {ats_result['overall_score']}/100"
    )

    completed = state.get("completed_steps", [])
    step_name = "reanalyze_ats" if "analyze_ats" in completed else "analyze_ats"

    completed.append(step_name)

    return {
        **state,
        "previous_ats_score": prev_score,
        "ats_score": ats_result["overall_score"],
        "ats_components": ats_result["component_scores"],
        "ats_justification": ats_result["justification"],
        "ats_ai_feedback": ats_result["ai_analysis"],
        "completed_steps": completed,
        "messages": messages
    }


# =====================================
# STRUCTURE FIXER AGENT
# =====================================
def structure_fixer_agent(state: ResumeState) -> ResumeState:
    """
    Suggests structural improvements for resumes with poor ATS scores.
    Uses LLM to generate contextual suggestions.
    """
    
    messages = state.get("messages", [])
    messages.append("Structure Fixer: Analyzing structural issues...")
    
    components = state.get("ats_components", {})
    
    prompt = f"""You are a resume structure optimization expert.

ATS Component Scores:
- Structure: {components.get('structure_score', 0)}/100
- Keywords: {components.get('keyword_score', 0)}/100
- Content Quality: {components.get('content_score', 0)}/100
- Formatting: {components.get('formatting_score', 0)}/100

Current Resume Sections Found:
{chr(10).join([f"- {k}: {len(v)} chars" for k, v in state['resume_sections'].items() if v.strip()])}

Job Description (first 300 chars):
{state['job_description'][:300]}...

Based on the low ATS scores, provide EXACTLY 3 specific structural fixes.
Focus on the LOWEST scoring components.

Format your response as:
1. [Specific issue] - [Concrete solution]
2. [Specific issue] - [Concrete solution]
3. [Specific issue] - [Concrete solution]

Be direct and actionable. No preamble."""

    try:
        response = llm.invoke([
            SystemMessage(content="You are an expert ATS resume optimizer specializing in structure and formatting."),
            HumanMessage(content=prompt)
        ])
        
        # Parse numbered suggestions
        suggestions = []
        for line in response.content.split('\n'):
            line = line.strip()
            if line and len(line) > 3 and line[0].isdigit() and line[1] in '.):':
                # Remove the number prefix
                clean_suggestion = line[2:].strip()
                if clean_suggestion:
                    suggestions.append(clean_suggestion)
        
        if not suggestions:
            # Fallback if parsing fails
            suggestions = [response.content]
        
        messages.append(f"Structure Fixer: Generated {len(suggestions)} structural improvements")
        
    except Exception as e:
        messages.append(f"Structure Fixer: Error - {str(e)}")
        suggestions = ["Unable to generate suggestions. Please try again."]
    
    completed = state.get("completed_steps", [])
    completed.append("fix_structure")

    return {
        **state,
        "structure_suggestions": suggestions,
        "completed_steps": completed,
        "messages": messages
    }

# =====================================
# SKILL GAP ANALYZER AGENT
# =====================================
def skill_gap_analyzer_agent(state: ResumeState) -> ResumeState:
    """
    Analyzes skill gaps using existing skill_gap_analyzer.
    Identifies what skills are missing for target roles.
    """
    
    messages = state.get("messages", [])
    messages.append("Skill Gap Analyzer: Comparing skills with job requirements...")
    
    # Use existing skill gap analyzer logic
    resume_bytes = state["resume_text"].encode("utf-8")
    gap_result = analyze_skill_gap(resume_bytes, filename="resume.txt")
    
    if "error" in gap_result:
        messages.append(f"Skill Gap Analyzer: {gap_result['error']}")
        return {
            **state,
            "user_skills": [],
            "skill_gaps": [],
            "career_matches": [],
            "messages": messages
        }
    
    # Extract top career match
    top_career = gap_result["top_3_careers"][0] if gap_result.get("top_3_careers") else {}
    
    messages.append(
        f"Skill Gap Analyzer: Found {len(gap_result.get('user_skills', []))} skills. "
        f"Best match: {top_career.get('career', 'Unknown')} "
        f"({top_career.get('probability', 0):.1f}% match)"
    )
    
    completed = state.get("completed_steps", [])
    completed.append("analyze_gaps")

    return {
        **state,
        "user_skills": gap_result.get("user_skills", []),
        "skill_gaps": top_career.get("missing_skills", [])[:10],
        "career_matches": gap_result.get("top_3_careers", []),
        "completed_steps": completed,
        "messages": messages
    }

# =====================================
# CONTENT OPTIMIZER AGENT
# =====================================
def content_optimizer_agent(state: ResumeState) -> ResumeState:
    """
    Generates HONEST content optimization suggestions.
    Only suggests highlighting/reframing skills they ACTUALLY have.
    Does NOT suggest adding fake skills.
    """
    
    messages = state.get("messages", [])
    messages.append("✍️ Content Optimizer: Creating honest, evidence-based suggestions...")
    
    validated_skills = state.get("validated_skills", [])
    level_assessment = state.get("level_assessment", {})
    jd_text = state["job_description"]
    
    # Separate skills by status
    confirmed = [s for s in validated_skills if s['status'] == 'confirmed']
    transferable = [s for s in validated_skills if s['status'] == 'transferable']
    missing = [s for s in validated_skills if s['status'] == 'missing']
    
    readiness = level_assessment.get("readiness_breakdown", {})
    ready_now = readiness.get("ready_now", [])
    
    prompt = f"""You are an ethical resume coach. Your job is to help candidates present their ACTUAL skills honestly, not to fabricate experience.

CONFIRMED SKILLS (they really have these):
{chr(10).join([f"- {s['skill']}: {', '.join(s['evidence'][:2])}" for s in confirmed])}

TRANSFERABLE SKILLS (they have similar/related skills):
{chr(10).join([f"- {s['skill']}: {', '.join(s['evidence'][:2])}" for s in transferable])}

MISSING SKILLS (they DON'T have these - DO NOT suggest adding them):
{', '.join([s['skill'] for s in missing])}

JOB DESCRIPTION:
{jd_text[:600]}

Provide EXACTLY 5 honest resume improvements:
1-3: How to HIGHLIGHT or REFRAME confirmed skills they already have
4-5: How to mention transferable skills with honest context

RULES:
✅ DO suggest: "Move Python to top of Skills section", "Quantify your PostgreSQL database size"
✅ DO suggest: "Reframe 'deployed app' as 'cloud deployment experience' (honest stretch)"
❌ DON'T suggest: "Add AWS to skills" (if they don't have it)
❌ DON'T suggest: "Mention Kubernetes experience" (if not present)

Format:
1. [Specific honest change for confirmed skill]
2. [Specific honest change for confirmed skill]
3. [Specific honest change for confirmed skill]
4. [Honest reframing of transferable skill]
5. [Honest reframing of transferable skill]

Be direct, actionable, and ETHICAL. Never suggest fabricating experience.
"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are an ethical career coach. You help candidates present their REAL skills honestly, never fabricate experience."),
            HumanMessage(content=prompt)
        ])
        
        # Parse numbered suggestions
        honest_improvements = []
        for line in response.content.split('\n'):
            line = line.strip()
            if line and len(line) > 3 and line[0].isdigit() and line[1] in '.):':
                clean_suggestion = line[2:].strip()
                if clean_suggestion:
                    honest_improvements.append(clean_suggestion)
        
        if not honest_improvements:
            honest_improvements = [response.content]
        
        messages.append(f"✍️ Content Optimizer: Generated {len(honest_improvements)} honest improvements")
        
    except Exception as e:
        messages.append(f"⚠️ Content Optimizer: Error - {str(e)}")
        honest_improvements = ["Unable to generate suggestions."]
    
    completed = state.get("completed_steps", [])
    completed.append("optimize_content")

    return {
        **state,
        "honest_improvements": honest_improvements,
        "alignment_suggestions": honest_improvements,  # Keep for compatibility
        "completed_steps": completed,
        "messages": messages
    }

def skill_validator_agent(state: ResumeState) -> ResumeState:
    """
    Validates which skills from JD are ACTUALLY present in resume with evidence.
    Uses LLM to detect skills even if not explicitly listed.
    """
    messages = state.get("messages", [])
    messages.append("🔍 Skill Validator: Analyzing resume for actual skill evidence...")

    resume_text = state["resume_text"]
    jd_text = state["job_description"]

    prompt = f"""You are an expert technical recruiter validating resume skills.

RESUME:
{resume_text[:2000]}

JOB REQUIREMENTS:
{jd_text[:800]}

Your task: For each skill/technology mentioned in the job requirements, determine if the candidate ACTUALLY has it based on EVIDENCE in their resume.

Classification rules:
- "confirmed": Explicitly mentioned AND used in projects/work with context
- "transferable": Not mentioned but similar/related skill is present
- "aspirational": Mentioned but no depth/context/evidence of real use
- "missing": No evidence whatsoever

Return a JSON array with this exact structure:
[
  {{
    "skill": "Python",
    "status": "confirmed",
    "evidence": ["Listed in Skills section", "Used in 3 projects", "5 years experience mentioned"],
    "confidence": 0.95
  }},
  {{
    "skill": "AWS",
    "status": "transferable",
    "evidence": ["Mentions cloud deployment", "Used Heroku (similar concept)"],
    "confidence": 0.4
  }},
  {{
    "skill": "Kubernetes",
    "status": "missing",
    "evidence": [],
    "confidence": 0.0
  }}
]

Be strict: Only mark as "confirmed" if there's REAL evidence of use.
"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are a technical recruiter expert at validating candidate skills based on resume evidence. Return only valid JSON."),
            HumanMessage(content=prompt)
        ])

        # Parse JSON response
        import json
        import re
        
        # Extract JSON from response (handle markdown code blocks)
        content = response.content.strip()
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        
        if json_match:
            validated_skills = json.loads(json_match.group(0))
        else:
            # Fallback: assume response is pure JSON
            validated_skills = json.loads(content)

        # Count by status
        confirmed = len([s for s in validated_skills if s['status'] == 'confirmed'])
        transferable = len([s for s in validated_skills if s['status'] == 'transferable'])
        missing = len([s for s in validated_skills if s['status'] == 'missing'])

        messages.append(
            f"🔍 Skill Validator: Confirmed: {confirmed}, Transferable: {transferable}, Missing: {missing}"
        )

    except Exception as e:
        messages.append(f"⚠️ Skill Validator: Error parsing - {str(e)}")
        validated_skills = []

    completed = state.get("completed_steps", [])
    completed.append("validate_skills")

    return {
        **state,
        "validated_skills": validated_skills,
        "completed_steps": completed,
        "messages": messages
    }

# app/agents/nodes.py - ADD THIS NEW AGENT

def gap_analyzer_agent(state: ResumeState) -> ResumeState:
    """
    Analyzes skill gaps using VALIDATED skills (not wishful thinking).
    Computes gap severity and estimates learning time.
    """
    messages = state.get("messages", [])
    messages.append("📊 Gap Analyzer: Computing honest skill gaps with severity...")

    validated_skills = state.get("validated_skills", [])
    jd_text = state["job_description"]

    # Build prompt with validated evidence
    skills_summary = "\n".join([
        f"- {s['skill']}: {s['status']} (confidence: {s['confidence']})"
        for s in validated_skills
    ])

    prompt = f"""You are a career coach analyzing skill gaps for job readiness.

VALIDATED SKILLS (with evidence):
{skills_summary}

JOB DESCRIPTION:
{jd_text[:800]}

For each skill marked as "transferable", "aspirational", or "missing", create a gap analysis.

Return JSON array:
[
  {{
    "skill": "AWS",
    "required_level": 2,
    "current_level": 0,
    "gap_severity": "critical",
    "evidence": ["JD mentions 'AWS required'", "Resume has no cloud experience"],
    "learning_time_estimate": "2-3 months"
  }},
  {{
    "skill": "Docker",
    "required_level": 1,
    "current_level": 0,
    "gap_severity": "important",
    "evidence": ["JD mentions containerization", "No Docker experience found"],
    "learning_time_estimate": "3-4 weeks"
  }}
]

Levels: 0=none, 1=basic, 2=intermediate, 3=advanced
Severity: "critical" (job requirement), "important" (preferred), "nice-to-have"
"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are a career development expert. Return only valid JSON."),
            HumanMessage(content=prompt)
        ])

        import json
        import re
        
        content = response.content.strip()
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        
        if json_match:
            skill_gaps = json.loads(json_match.group(0))
        else:
            skill_gaps = json.loads(content)

        # Calculate gap score (0-100)
        confirmed_skills = [s for s in validated_skills if s['status'] == 'confirmed']
        total_required = len(validated_skills)
        
        if total_required > 0:
            gap_score = (len(confirmed_skills) / total_required) * 100
        else:
            gap_score = 50.0

        critical_gaps = len([g for g in skill_gaps if g['gap_severity'] == 'critical'])
        
        messages.append(
            f"📊 Gap Analyzer: Gap Score: {gap_score:.1f}/100 | Critical gaps: {critical_gaps}"
        )

    except Exception as e:
        messages.append(f"⚠️ Gap Analyzer: Error - {str(e)}")
        skill_gaps = []
        gap_score = 0.0

    completed = state.get("completed_steps", [])
    completed.append("analyze_gaps")

    return {
        **state,
        "skill_gaps": skill_gaps,
        "gap_score": gap_score,
        "completed_steps": completed,
        "messages": messages
    }

# app/agents/nodes.py - ADD THIS NEW AGENT

def level_assessor_agent(state: ResumeState) -> ResumeState:
    """
    Assesses required proficiency levels (0-3) for each skill based on JD.
    Also determines user's current level based on validated evidence.
    
    Levels:
    0 = No knowledge/experience
    1 = Basic/Beginner (can use with guidance, 0-1 year)
    2 = Intermediate/Proficient (independent work, 1-3 years)
    3 = Advanced/Expert (can teach others, lead projects, 3+ years)
    """
    messages = state.get("messages", [])
    messages.append("📏 Level Assessor: Determining proficiency levels for each skill...")

    validated_skills = state.get("validated_skills", [])
    skill_gaps = state.get("skill_gaps", [])
    jd_text = state["job_description"]
    resume_text = state["resume_text"]

    # Build context for LLM
    validated_summary = "\n".join([
        f"- {s['skill']}: {s['status']} | Evidence: {', '.join(s['evidence'][:2])}"
        for s in validated_skills
    ])

    gaps_summary = "\n".join([
        f"- {g['skill']}: Severity={g['gap_severity']}, Current={g['current_level']}, Required={g['required_level']}"
        for g in skill_gaps
    ])

    prompt = f"""You are a technical hiring manager assessing skill proficiency levels.

JOB DESCRIPTION:
{jd_text[:1000]}

VALIDATED SKILLS (from resume):
{validated_summary}

IDENTIFIED GAPS:
{gaps_summary}

RESUME CONTEXT (for experience assessment):
{resume_text[:1500]}

Your task: For EACH skill mentioned in the JD, determine:
1. What proficiency level (0-3) is REQUIRED for this job
2. What proficiency level (0-3) the candidate CURRENTLY has based on evidence

Level definitions:
- 0: No knowledge/never used
- 1: Basic/Beginner - Can use with guidance, tutorials, or documentation. 0-1 year equivalent.
- 2: Intermediate/Proficient - Can work independently, solve common problems. 1-3 years equivalent.
- 3: Advanced/Expert - Can design systems, mentor others, handle edge cases. 3+ years equivalent.

Level assessment rules:
- If skill only mentioned in JD without emphasis → required_level = 1
- If JD says "experience with X" → required_level = 2
- If JD says "expert in X" or "lead X projects" → required_level = 3
- If resume mentions skill but no projects → current_level = 0 or 1
- If resume shows 1-2 projects with skill → current_level = 1
- If resume shows multiple projects, metrics, years of experience → current_level = 2
- If resume shows leadership, teaching, architecture with skill → current_level = 3

Return JSON:
{{
  "skill_levels": [
    {{
      "skill": "Python",
      "required_level": 2,
      "current_level": 2,
      "gap": 0,
      "assessment_reason": "JD requires intermediate Python. Resume shows 3 years experience with multiple projects.",
      "time_to_bridge": "0 months"
    }},
    {{
      "skill": "AWS",
      "required_level": 2,
      "current_level": 0,
      "gap": 2,
      "assessment_reason": "JD requires AWS experience. No evidence in resume.",
      "time_to_bridge": "2-3 months"
    }},
    {{
      "skill": "Docker",
      "required_level": 1,
      "current_level": 0,
      "gap": 1,
      "assessment_reason": "JD mentions Docker. No evidence in resume.",
      "time_to_bridge": "3-4 weeks"
    }}
  ],
  "overall_readiness": "45%",
  "readiness_breakdown": {{
    "ready_now": ["Python", "Django", "PostgreSQL"],
    "need_basic_learning": ["Docker", "CI/CD"],
    "need_intermediate_learning": ["AWS", "Kubernetes"],
    "need_advanced_learning": []
  }}
}}

Be realistic and evidence-based. Don't inflate current levels without proof.
"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are a technical assessor expert at evaluating skill proficiency levels. Return only valid JSON."),
            HumanMessage(content=prompt)
        ])

        import json
        import re
        
        content = response.content.strip()
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            level_data = json.loads(json_match.group(1))
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                level_data = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found in response")

        skill_levels = level_data.get("skill_levels", [])
        overall_readiness = level_data.get("overall_readiness", "Unknown")
        readiness_breakdown = level_data.get("readiness_breakdown", {})

        # Build required_levels dict for state
        required_levels = {
            item["skill"]: item["required_level"] 
            for item in skill_levels
        }

        # Count gaps by severity
        level_0_to_1 = len([s for s in skill_levels if s["gap"] == 1])
        level_0_to_2 = len([s for s in skill_levels if s["gap"] == 2])
        level_0_to_3 = len([s for s in skill_levels if s["gap"] == 3])
        no_gap = len([s for s in skill_levels if s["gap"] == 0])

        messages.append(
            f"📏 Level Assessor: Overall Readiness: {overall_readiness}"
        )
        messages.append(
            f"📏 Level Assessor: Ready: {no_gap} | Need L1: {level_0_to_1} | Need L2: {level_0_to_2} | Need L3: {level_0_to_3}"
        )

        # Store detailed level assessment
        level_assessment = {
            "skill_levels": skill_levels,
            "overall_readiness": overall_readiness,
            "readiness_breakdown": readiness_breakdown
        }

    except Exception as e:
        messages.append(f"⚠️ Level Assessor: Error - {str(e)}")
        required_levels = {}
        level_assessment = {}

    completed = state.get("completed_steps", [])
    completed.append("assess_levels")

    return {
        **state,
        "required_levels": required_levels,
        "level_assessment": level_assessment,  # Store full assessment
        "completed_steps": completed,
        "messages": messages
    }