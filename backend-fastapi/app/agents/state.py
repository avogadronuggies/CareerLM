# app/agents/state.py
from typing import TypedDict, List, Dict, Optional, Literal


class SkillEvidence(TypedDict):
    """Evidence for a skill's presence in resume"""
    skill: str
    status: Literal["confirmed", "transferable", "aspirational", "missing"]
    evidence: List[str]  # Where it appears in resume
    confidence: float  # 0.0 to 1.0


class SkillGap(TypedDict):
    """Detailed gap analysis for a skill"""
    skill: str
    required_level: int  # 0-3 (0=awareness, 1=basic, 2=intermediate, 3=advanced)
    current_level: int   # 0-3
    gap_severity: Literal["critical", "important", "nice-to-have"]
    evidence: List[str]
    learning_time_estimate: str  # e.g., "2-4 weeks"


class LearningResource(TypedDict):
    """A course or resource recommendation"""
    skill: str
    level: int  # Target level (0-3)
    resource_type: Literal["course", "certification", "project", "book", "practice"]
    title: str
    provider: str
    url: Optional[str]
    duration: str
    cost: Literal["free", "paid", "freemium"]
    priority: Literal["high", "medium", "low"]


class ResumeState(TypedDict):
    """State that flows through the agentic workflow"""
    
    # ===== INPUT =====
    resume_text: str
    job_description: str
    resume_sections: Dict[str, str]
    
    # ===== ATS ANALYSIS =====
    ats_score: int
    ats_components: Dict[str, int]
    ats_justification: List[str]
    ats_ai_feedback: str
    previous_ats_score: Optional[int]
    
    # ===== SKILL VALIDATION (NEW) =====
    validated_skills: List[SkillEvidence]  # Skills with evidence
    user_skills: List[str]  # Legacy - kept for compatibility
    
    # ===== SKILL GAP ANALYSIS (ENHANCED) =====
    skill_gaps: List[SkillGap]  # Detailed gap analysis
    gap_score: float  # 0-100 (how well they match the role)
    career_matches: List[Dict]
    
    # ===== LEARNING PATH (NEW) =====
    required_levels: Dict[str, int]  # {skill: target_level}
    learning_resources: List[LearningResource]
    learning_timeline: str  # "2-3 months to reach 75% match"
    
    # ===== OPTIMIZATION RESULTS =====
    structure_suggestions: List[str]
    alignment_suggestions: List[str]  # Now honest, evidence-based
    honest_improvements: List[str]  # NEW - what they can do NOW
    future_improvements: List[str]  # NEW - what they can do AFTER learning

    # ===== LEARNING PATH (NEW) =====
    required_levels: Dict[str, int]  # {skill: target_level}
    level_assessment: Dict  # NEW - Full level assessment data
    learning_resources: List[LearningResource]
    learning_timeline: str
    
    # ===== AGENT CONTROL FLOW =====
    next_action: Literal[
        "analyze_ats",
        "validate_skills",
        "analyze_gaps",
        "assess_levels",
        "generate_learning_path",
        "optimize_content",
        "fix_structure",
        "reanalyze_ats",
        "complete"
    ]
    needs_ats_improvement: bool
    iteration_count: int
    max_iterations: int
    completed_steps: List[str]
    decision_reason: str
    messages: List[str]