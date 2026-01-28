"""Get complete weekly review - comprehensive analysis of all active projects and tasks."""

from typing import Dict, Any, List
from .analyze_all_projects import get_all_active_projects, analyze_project_health
from .analyze_workload_balance import analyze_workload_balance
from .check_priority_limits import check_priority_limits
from .analyze_waiting_tasks import analyze_waiting_tasks
from .find_orphaned_tasks import find_orphaned_tasks
from .analyze_task_project_alignment import get_tasks_for_project
from .get_action_items_for_review import get_action_items_for_review


def get_weekly_review() -> "Dict[str, Any]":
    """Get complete weekly review data - comprehensive analysis of all active projects and tasks.
    
    Returns:
        Dict with comprehensive weekly review including:
        - Summary statistics
        - Projects by health status
        - Workload balance analysis
        - Priority violations
        - Waiting tasks analysis
        - Orphaned tasks
        - Action items from meetings (last 7 days)
    """
    # 1. Get all active projects
    active_projects = get_all_active_projects()
    
    # 2. Analyze each project's health
    projects_by_health = {
        "healthy": [],
        "needs_attention": [],
        "critical": []
    }
    
    projects_by_priority = {
        "P1": [],
        "P2": [],
        "P3": []
    }
    
    for project in active_projects:
        # Get tasks for this project
        task_pages = get_tasks_for_project(project["id"])
        from .extract_task_properties import extract_task_properties
        tasks = [extract_task_properties(t) for t in task_pages]
        
        # Analyze health
        health = analyze_project_health(project, tasks)
        
        # Add project info to health result
        health["project"] = project
        
        # Categorize by health status
        status = health["health_status"]
        projects_by_health[status].append(health)
        
        # Also categorize by priority
        priority = project.get("priority", "")
        if "P1" in priority:
            projects_by_priority["P1"].append(health)
        elif "P2" in priority:
            projects_by_priority["P2"].append(health)
        elif "P3" in priority:
            projects_by_priority["P3"].append(health)
    
    # 3. Analyze workload balance
    workload_analysis = analyze_workload_balance()
    
    # 4. Check priority violations
    priority_check = check_priority_limits()
    
    # 5. Analyze waiting tasks
    waiting_analysis = analyze_waiting_tasks()
    
    # 6. Find orphaned tasks
    orphaned_analysis = find_orphaned_tasks()
    
    # 7. Get action items from last week (7 days)
    action_items = get_action_items_for_review(days_back=7)
    
    # 8. Generate comprehensive summary
    summary = {
        "total_active_projects": len(active_projects),
        "projects_by_priority": {
            "P1": len(projects_by_priority["P1"]),
            "P2": len(projects_by_priority["P2"]),
            "P3": len(projects_by_priority["P3"])
        },
        "projects_by_health": {
            "healthy": len(projects_by_health["healthy"]),
            "needs_attention": len(projects_by_health["needs_attention"]),
            "critical": len(projects_by_health["critical"])
        },
        "priority_violations": {
            "has_violations": len(priority_check["violations"]) > 0,
            "violation_count": len(priority_check["violations"])
        },
        "total_tasks_this_week": workload_analysis["total_this_week_tasks"],
        "workload_assessment": workload_analysis["workload_assessment"],
        "waiting_tasks_total": waiting_analysis["total_waiting"],
        "waiting_tasks_need_followup": waiting_analysis["need_followup_count"],
        "orphaned_tasks_count": orphaned_analysis["total_orphaned"],
        "action_items": {
            "total": action_items["summary"]["total_action_items"],
            "for_rajiv": action_items["summary"]["for_rajiv"],
            "waiting_on_others": action_items["summary"]["waiting_on_others"]
        }
    }
    
    return {
        "summary": summary,
        "projects_by_health": projects_by_health,
        "projects_by_priority": projects_by_priority,
        "workload_balance": workload_analysis,
        "priority_violations": priority_check,
        "waiting_tasks": waiting_analysis,
        "orphaned_tasks": orphaned_analysis,
        "action_items": action_items
    }
