"""Analyze all active projects and calculate project health scores."""

from typing import List, Dict, Any
from datetime import datetime, date
from tools.common import query_database_complete, PROJECTS_DATA_SOURCE_ID
from .extract_project_properties import extract_project_properties
from .analyze_task_project_alignment import get_tasks_for_project
from .extract_task_properties import extract_task_properties


def get_all_active_projects() -> "List[Dict[str, Any]]":
    """Get all active projects (P1, P2, P3), excluding Done and Monitoring.
    
    Returns:
        List of project page objects with extracted properties
    """
    all_projects = query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        use_data_source=True
    )
    
    # Filter out Done and Monitoring projects
    active_projects = []
    for project_page in all_projects:
        project = extract_project_properties(project_page)
        priority = project.get("priority", "")
        
        # Exclude Done and Monitoring priorities
        if priority and "Done" not in priority and "Monitoring" not in priority:
            # Include P1, P2, P3 projects
            if "P1" in priority or "P2" in priority or "P3" in priority:
                active_projects.append(project)
    
    return active_projects


def analyze_project_health(project: "Dict[str, Any]", tasks: "List[Dict[str, Any]]") -> "Dict[str, Any]":
    """Calculate project health score based on multiple factors.
    
    Health factors:
    - Has active tasks? (This Week, Top Priority, On Deck)
    - Task due dates align with project due date?
    - Overdue tasks count
    - Waiting tasks count
    - Project due date proximity
    - Priority level vs activity level
    
    Args:
        project: Project dict with extracted properties
        tasks: List of task dicts with extracted properties
    
    Returns:
        Dict with health assessment including score, status, and factors
    """
    today = date.today()
    project_due_date = None
    if project.get("due_date"):
        try:
            project_due_date = datetime.fromisoformat(project["due_date"].split("T")[0]).date()
        except:
            pass
    
    # Categorize tasks
    active_statuses = ["This Week", "Top Priority", "On Deck"]
    active_tasks = [t for t in tasks if t.get("status") in active_statuses]
    done_tasks = [t for t in tasks if t.get("status") == "Done"]
    overdue_tasks = []
    waiting_tasks = [t for t in tasks if t.get("status") == "Waiting"]
    tasks_due_after_project = []
    
    for task in tasks:
        if task.get("status") == "Done":
            continue
            
        task_due = task.get("due_date")
        if task_due:
            try:
                task_due_date = datetime.fromisoformat(task_due.split("T")[0]).date()
                
                # Check if overdue
                if task_due_date < today:
                    overdue_tasks.append(task)
                
                # Check if task due after project due date
                if project_due_date and task_due_date > project_due_date:
                    tasks_due_after_project.append(task)
            except:
                pass
    
    # Calculate health score (0-100, higher is better)
    score = 100
    factors = []
    
    priority = project.get("priority", "")
    is_high_priority = "P1" in priority or "P2" in priority
    
    # Factor 1: Active tasks (critical for high-priority projects)
    if is_high_priority and len(active_tasks) == 0:
        score -= 30
        factors.append({
            "factor": "no_active_tasks",
            "severity": "high",
            "message": f"{priority} project has no active tasks"
        })
    elif len(active_tasks) == 0 and len(tasks) > 0:
        score -= 15
        factors.append({
            "factor": "no_active_tasks",
            "severity": "medium",
            "message": "Project has no active tasks"
        })
    
    # Factor 2: Overdue tasks
    if len(overdue_tasks) > 0:
        score -= min(20, len(overdue_tasks) * 5)
        factors.append({
            "factor": "overdue_tasks",
            "severity": "high" if len(overdue_tasks) > 2 else "medium",
            "message": f"{len(overdue_tasks)} overdue task(s)",
            "count": len(overdue_tasks)
        })
    
    # Factor 3: Tasks due after project deadline
    if len(tasks_due_after_project) > 0:
        score -= min(15, len(tasks_due_after_project) * 3)
        factors.append({
            "factor": "tasks_after_deadline",
            "severity": "medium",
            "message": f"{len(tasks_due_after_project)} task(s) due after project deadline",
            "count": len(tasks_due_after_project)
        })
    
    # Factor 4: Project due date proximity (if due soon and no active tasks)
    if project_due_date:
        days_until_due = (project_due_date - today).days
        if 0 <= days_until_due <= 14 and len(active_tasks) == 0:
            score -= 25
            factors.append({
                "factor": "due_soon_no_active",
                "severity": "high",
                "message": f"Project due in {days_until_due} days but has no active tasks",
                "days_until_due": days_until_due
            })
        elif days_until_due < 0:
            score -= 30
            factors.append({
                "factor": "project_overdue",
                "severity": "critical",
                "message": f"Project is {abs(days_until_due)} days overdue",
                "days_overdue": abs(days_until_due)
            })
    
    # Factor 5: Waiting tasks (moderate impact)
    if len(waiting_tasks) > len(active_tasks) and len(active_tasks) > 0:
        score -= 10
        factors.append({
            "factor": "too_many_waiting",
            "severity": "medium",
            "message": f"More waiting tasks ({len(waiting_tasks)}) than active ({len(active_tasks)})",
            "waiting_count": len(waiting_tasks),
            "active_count": len(active_tasks)
        })
    
    # Determine health status
    if score >= 80:
        status = "healthy"
    elif score >= 60:
        status = "needs_attention"
    else:
        status = "critical"
    
    return {
        "project_id": project["id"],
        "project_title": project["title"],
        "priority": priority,
        "health_score": max(0, score),  # Ensure non-negative
        "health_status": status,
        "factors": factors,
        "total_tasks": len(tasks),
        "active_tasks_count": len(active_tasks),
        "done_tasks_count": len(done_tasks),
        "overdue_tasks_count": len(overdue_tasks),
        "waiting_tasks_count": len(waiting_tasks),
        "tasks_due_after_project": len(tasks_due_after_project),
        "project_due_date": project.get("due_date"),
        "this_week": project.get("this_week", False)
    }
