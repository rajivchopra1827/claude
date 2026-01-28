"""Classify tasks using the LNO Framework (Leverage, Neutral, Overhead)."""

from typing import Dict, Any, List, Optional
from tools.common import get_strategic_priorities


def classify_task_lno(
    task: Dict[str, Any],
    project_context: Optional[Dict[str, Any]] = None,
    strategic_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Classify a task using the LNO Framework.
    
    L (Leverage ~10X): "Do a great job. Let your inner perfectionist shine."
    N (Neutral ~1X): "Do a strictly good job. No better."
    O (Overhead <1X): "Just get it done. Actively try to do a bad job."
    
    Args:
        task: Dict[str, Any] - Task object with extracted properties (title, status, project_ids, etc.)
        project_context: Optional[Dict[str, Any]] - Project information if available (priority, name, etc.)
        strategic_context: Optional[Dict[str, Any]] - Strategic context from get_rajiv_context()
    
    Returns:
        Dict[str, Any]: Classification result with:
            - classification: "L" | "N" | "O"
            - confidence: float (0.0-1.0)
            - reasoning: str - Why this classification
            - signals: List[str] - What indicators led to this
    """
    title = task.get("title", "").lower()
    signals = []
    l_score = 0
    n_score = 0
    o_score = 0
    
    # L (Leverage) signals - Strategic, high-impact, unique expertise
    l_keywords = [
        "strategy", "strategic", "decision", "decide", "direction",
        "stakeholder", "executive", "leadership", "vision", "roadmap",
        "framework", "system", "process", "architecture", "design",
        "unlock", "enable", "foundation", "critical", "high-stakes",
        "presentation", "pitch", "proposal", "planning", "alignment"
    ]
    
    # O (Overhead) signals - Administrative, compliance, low value
    o_keywords = [
        "admin", "administrative", "compliance", "submit", "submit",
        "form", "form", "approve", "sign", "acknowledge", "confirm",
        "update", "status update", "check", "verify", "log", "track",
        "report", "reporting", "document", "documentation", "file",
        "organize", "clean", "archive", "backup", "sync"
    ]
    
    # Check task title for keywords
    title_words = set(title.split())
    for keyword in l_keywords:
        if keyword in title:
            l_score += 2
            signals.append(f"Contains '{keyword}' (strategic/leverage indicator)")
    
    for keyword in o_keywords:
        if keyword in title:
            o_score += 2
            signals.append(f"Contains '{keyword}' (administrative/overhead indicator)")
    
    # Strategic context analysis
    if strategic_context:
        strategic_content = strategic_context.get("content", "").lower()
        
        # Get strategic priorities and extract all keywords
        strategic_priorities = get_strategic_priorities()
        strategic_terms = []
        for priority_info in strategic_priorities.values():
            # Add keywords from "Also known as" and related work
            strategic_terms.extend(priority_info.get("keywords", []))
            # Add priority name itself
            if priority_info.get("name"):
                strategic_terms.append(priority_info["name"].lower())
            if priority_info.get("display_name"):
                strategic_terms.append(priority_info["display_name"].lower())
        
        # Also add common strategic terms
        strategic_terms.extend(["csat", "mrr", "expansion revenue"])
        
        # Check if task relates to strategic priorities
        for term in strategic_terms:
            if term and (term in title or term in strategic_content):
                # Strategic alignment suggests L, but not automatically
                # Only if it's a strategic decision/planning task
                if any(kw in title for kw in ["strategy", "decision", "plan", "design", "framework"]):
                    l_score += 3
                    signals.append(f"Strategic priority alignment with decision/planning work")
                break
    
    # Project context analysis
    if project_context:
        project_name = project_context.get("name", "").lower()
        project_priority = project_context.get("priority", "")
        
        # Strategic projects (Fiona 2.0, Digible.AI) - but only if task type suggests L
        if any(term in project_name for term in ["fiona", "digible", "marketing intelligence", "ai disruption"]):
            if any(kw in title for kw in ["strategy", "decision", "plan", "design", "framework", "stakeholder"]):
                l_score += 2
                signals.append(f"Strategic project with decision/planning work")
        
        # Don't auto-map P1 → L (as user specified)
        # But P1 projects with strategic work types are more likely L
        if project_priority == "P1":
            if any(kw in title for kw in ["strategy", "decision", "plan", "design", "framework"]):
                l_score += 1
                signals.append("P1 project with strategic work type")
    
    # Task type inference
    # Strategic planning/decision work
    if any(phrase in title for phrase in ["create strategy", "design system", "make decision", 
                                          "define framework", "set direction", "plan approach",
                                          "stakeholder meeting", "executive presentation"]):
        l_score += 3
        signals.append("Strategic planning/decision work type")
    
    # Routine execution work
    if any(phrase in title for phrase in ["review", "update", "prep", "prepare", "follow up",
                                          "schedule", "coordinate", "sync"]):
        # Could be N or O depending on context
        if any(kw in title for kw in ["admin", "status", "compliance", "form"]):
            o_score += 2
            signals.append("Routine administrative work")
        else:
            n_score += 2
            signals.append("Routine execution work")
    
    # Administrative/compliance work
    if any(phrase in title for phrase in ["fill out", "submit form", "approve request",
                                          "acknowledge", "confirm receipt", "log time"]):
        o_score += 3
        signals.append("Administrative/compliance work")
    
    # Meeting-related tasks
    if "meeting" in title:
        if any(kw in title for kw in ["prep", "prepare", "agenda"]):
            # Meeting prep could be N (routine) or L (strategic)
            if any(kw in title for kw in ["stakeholder", "executive", "strategy", "planning"]):
                l_score += 2
                signals.append("Strategic meeting preparation")
            else:
                n_score += 1
                signals.append("Routine meeting preparation")
        elif any(kw in title for kw in ["schedule", "book", "coordinate"]):
            o_score += 2
            signals.append("Meeting scheduling (administrative)")
    
    # Documentation tasks
    if "document" in title or "doc" in title:
        if any(kw in title for kw in ["strategy", "framework", "design", "architecture", "system"]):
            l_score += 2
            signals.append("Strategic documentation")
        else:
            n_score += 1
            signals.append("Routine documentation")
    
    # Default classification logic
    # If no strong signals, default to N (neutral)
    if l_score == 0 and n_score == 0 and o_score == 0:
        n_score += 1
        signals.append("No strong indicators - defaulting to Neutral")
    
    # Determine classification
    max_score = max(l_score, n_score, o_score)
    
    if max_score == l_score and l_score > 0:
        classification = "L"
        confidence = min(0.9, 0.5 + (l_score - max(n_score, o_score)) * 0.1)
        reasoning = "High leverage work requiring deep focus and quality. Strategic decisions, unique expertise, or work that unlocks other high-value initiatives."
    elif max_score == o_score and o_score > 0:
        classification = "O"
        confidence = min(0.9, 0.5 + (o_score - max(l_score, n_score)) * 0.1)
        reasoning = "Overhead work - administrative, compliance, or low-value tasks. Minimize time investment, just get it done."
    else:
        classification = "N"
        confidence = min(0.9, 0.5 + (n_score - max(l_score, o_score)) * 0.1)
        reasoning = "Neutral work - routine execution that needs to happen. Good enough quality is sufficient, no need to over-invest."
    
    # If scores are very close, lower confidence
    scores = [l_score, n_score, o_score]
    scores.sort(reverse=True)
    if scores[0] - scores[1] < 2:
        confidence = max(0.3, confidence - 0.2)
        signals.append("Close scores - classification uncertain")
    
    return {
        "classification": classification,
        "confidence": round(confidence, 2),
        "reasoning": reasoning,
        "signals": signals,
        "scores": {
            "L": l_score,
            "N": n_score,
            "O": o_score
        }
    }
