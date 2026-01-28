"""Check for priority limit violations."""

from typing import Dict, Any, List
from tools.common import query_database_complete, PROJECTS_DATA_SOURCE_ID
from .extract_project_properties import extract_project_properties


def check_priority_limits() -> "Dict[str, Any]":
    """Check for priority limit violations.
    
    Limits:
    - P1: max 1 project
    - P2: max 3 projects
    - P3: max 5 projects
    
    Returns:
        Dict with priority counts, violations, and suggestions
    """
    all_projects = query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        use_data_source=True
    )
    
    # Count projects by priority
    p1_projects = []
    p2_projects = []
    p3_projects = []
    
    for project_page in all_projects:
        project = extract_project_properties(project_page)
        priority = project.get("priority") or ""
        
        # Skip completed projects
        if project.get("completed_date") or (priority and "Done" in priority):
            continue
        
        if priority and "P1" in priority:
            p1_projects.append(project)
        elif priority and "P2" in priority:
            p2_projects.append(project)
        elif priority and "P3" in priority:
            p3_projects.append(project)
    
    # Check for violations
    violations = []
    
    p1_count = len(p1_projects)
    p2_count = len(p2_projects)
    p3_count = len(p3_projects)
    
    p1_limit = 1
    p2_limit = 3
    p3_limit = 5
    
    if p1_count > p1_limit:
        violations.append({
            "priority": "P1",
            "current_count": p1_count,
            "limit": p1_limit,
            "excess": p1_count - p1_limit,
            "severity": "high",
            "message": f"P1 limit exceeded: {p1_count} projects (max {p1_limit})",
            "projects": p1_projects
        })
    
    if p2_count > p2_limit:
        violations.append({
            "priority": "P2",
            "current_count": p2_count,
            "limit": p2_limit,
            "excess": p2_count - p2_limit,
            "severity": "high",
            "message": f"P2 limit exceeded: {p2_count} projects (max {p2_limit})",
            "projects": p2_projects
        })
    
    if p3_count > p3_limit:
        violations.append({
            "priority": "P3",
            "current_count": p3_count,
            "limit": p3_limit,
            "excess": p3_count - p3_limit,
            "severity": "medium",
            "message": f"P3 limit exceeded: {p3_count} projects (max {p3_limit})",
            "projects": p3_projects
        })
    
    # Generate suggestions for violations
    suggestions = []
    for violation in violations:
        priority = violation["priority"]
        excess = violation["excess"]
        projects = violation["projects"]
        
        # Suggest moving excess projects to lower priority
        if priority == "P1" and excess > 0:
            # Suggest moving excess P1 projects to P2
            suggestions.append({
                "priority": "P1",
                "action": "move_to_p2",
                "message": f"Consider moving {excess} P1 project(s) to P2",
                "candidates": projects[1:]  # All except the first one
            })
        elif priority == "P2" and excess > 0:
            # Suggest moving excess P2 projects to P3
            suggestions.append({
                "priority": "P2",
                "action": "move_to_p3",
                "message": f"Consider moving {excess} P2 project(s) to P3",
                "candidates": projects[p2_limit:]  # Projects beyond the limit
            })
        elif priority == "P3" and excess > 0:
            # Suggest moving excess P3 projects to Monitoring
            suggestions.append({
                "priority": "P3",
                "action": "move_to_monitoring",
                "message": f"Consider moving {excess} P3 project(s) to Monitoring",
                "candidates": projects[p3_limit:]  # Projects beyond the limit
            })
    
    return {
        "p1_count": p1_count,
        "p1_limit": p1_limit,
        "p2_count": p2_count,
        "p2_limit": p2_limit,
        "p3_count": p3_count,
        "p3_limit": p3_limit,
        "violations": violations,
        "suggestions": suggestions,
        "p1_projects": p1_projects,
        "p2_projects": p2_projects,
        "p3_projects": p3_projects
    }
