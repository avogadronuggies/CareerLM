# app/agents/graph.py

from langgraph.graph import StateGraph, END
from app.agents.state import ResumeState
from app.agents.nodes import (
    coordinator_agent,
    ats_analyzer_agent,
    structure_fixer_agent,
    skill_validator_agent,  # NEW
    gap_analyzer_agent,      # NEW (enhanced)
    level_assessor_agent,    # NEW
    content_optimizer_agent
)


def route_next_action(state: ResumeState) -> str:
    """Router function"""
    next_action = state["next_action"]
    print(f"  🔀 Router: next_action = '{next_action}'")
    return next_action


def create_resume_workflow():
    """Creates and compiles the LangGraph workflow."""
    
    print("🔧 Building enhanced workflow graph...")
    
    workflow = StateGraph(ResumeState)
    
    # ===== ADD NODES =====
    print("  → Adding coordinator node")
    workflow.add_node("coordinator", coordinator_agent)
    
    print("  → Adding analyze_ats node")
    workflow.add_node("analyze_ats", ats_analyzer_agent)
    
    print("  → Adding fix_structure node")
    workflow.add_node("fix_structure", structure_fixer_agent)
    
    print("  → Adding validate_skills node")  # NEW
    workflow.add_node("validate_skills", skill_validator_agent)
    
    print("  → Adding analyze_gaps node (enhanced)")  # NEW
    workflow.add_node("analyze_gaps", gap_analyzer_agent)
    
    print("  → Adding assess_levels node")  # NEW
    workflow.add_node("assess_levels", level_assessor_agent)
    
    print("  → Adding optimize_content node")
    workflow.add_node("optimize_content", content_optimizer_agent)
    
    print("  → Adding reanalyze_ats node")
    workflow.add_node("reanalyze_ats", ats_analyzer_agent)
    
    # ===== SET ENTRY POINT =====
    print("  → Setting entry point to coordinator")
    workflow.set_entry_point("coordinator")
    
    # ===== ADD CONDITIONAL EDGES FROM COORDINATOR =====
    print("  → Adding conditional edges from coordinator")
    workflow.add_conditional_edges(
        "coordinator",
        route_next_action,
        {
            "analyze_ats": "analyze_ats",
            "fix_structure": "fix_structure",
            "validate_skills": "validate_skills",  # NEW
            "analyze_gaps": "analyze_gaps",
            "assess_levels": "assess_levels",      # NEW
            "optimize_content": "optimize_content",
            "reanalyze_ats": "reanalyze_ats",
            "complete": END
        }
    )
    
    # ===== ADD EDGES BACK TO COORDINATOR =====
    print("  → Adding edges back to coordinator")
    workflow.add_edge("analyze_ats", "coordinator")
    workflow.add_edge("fix_structure", "coordinator")
    workflow.add_edge("validate_skills", "coordinator")   # NEW
    workflow.add_edge("analyze_gaps", "coordinator")
    workflow.add_edge("assess_levels", "coordinator")     # NEW
    workflow.add_edge("optimize_content", "coordinator")
    workflow.add_edge("reanalyze_ats", "coordinator")
    
    # ===== COMPILE THE GRAPH =====
    print("  → Compiling graph...")
    app = workflow.compile()
    print("✓ Graph compiled successfully!")
    
    return app


# Create singleton
print("📦 Creating resume_workflow singleton...")
resume_workflow = create_resume_workflow()
print("✓ resume_workflow ready!")