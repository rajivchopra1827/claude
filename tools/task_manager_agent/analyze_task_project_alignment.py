"""Analyze alignment between projects and their tasks."""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties


def get_tasks_for_project(project_id: str) -> "List[Dict[str, Any]]":
    """Get all tasks linked to a specific project.
    
    Args:
        project_id: Notion page ID of the project
    
    Returns:
        List of task page objects linked to the project
    """
    tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Project",
            "relation": {"contains": project_id}
        },
        use_data_source=True
    )
    
    return tasks


def analyze_project_task_alignment(
    project: "Dict[str, Any]",
    tasks: Optional["List[Dict[str, Any]]"] = None
) -> "Dict[str, Any]":
    """Analyze alignment between a project and its tasks.
    
    Checks:
    - Does project have active tasks? (This Week, Top Priority, On Deck)
    - Do task due dates align with project due date?
    - Are overdue tasks in appropriate status?
    - Do high-priority projects have active work?
    
    Args:
        project: Project dict with extracted properties (from extract_project_properties)
        tasks: Optional list of task page objects. If None, will fetch tasks for project.
    
    Returns:
        Dict with alignment issues and recommendations
    """
    if tasks is None:
        task_pages = get_tasks_for_project(project["id"])
    else:
        task_pages = tasks
    
    # Extract task properties
    extracted_tasks = [extract_task_properties(task) for task in task_pages]
    
    today = date.today()
    project_due_date = None
    if project.get("due_date"):
        try:
            project_due_date = datetime.fromisoformat(project["due_date"].split("T")[0]).date()
        except:
            pass
    
    # Categorize tasks
    active_statuses = ["This Week", "Top Priority", "On Deck"]
    active_tasks = [t for t in extracted_tasks if t.get("status") in active_statuses]
    overdue_tasks = []
    tasks_due_after_project = []
    
    for task in extracted_tasks:
        task_due = task.get("due_date")
        if task_due:
            try:
                task_due_date = datetime.fromisoformat(task_due.split("T")[0]).date()
                
                # Check if overdue
                if task_due_date < today and task.get("status") != "Done":
                    overdue_tasks.append(task)
                
                # Check if task due after project due date
                if project_due_date and task_due_date > project_due_date:
                    tasks_due_after_project.append(task)
            except:
                pass
    
    # Identify issues
    issues = []
    recommendations = []
    
    priority = project.get("priority")
    is_high_priority = priority in ["P1", "P2"]
    
    # Issue: High-priority project has no active tasks
    if is_high_priority and len(active_tasks) == 0:
        issues.append({
            "type": "no_active_tasks",
            "severity": "high",
            "message": f"{priority} project has no active tasks (This Week, Top Priority, or On Deck)"
        })
        # Find tasks that could be activated
        backlog_tasks = [t for t in extracted_tasks if t.get("status") == "Backlog"]
        if backlog_tasks:
            recommendations.append({
                "type": "activate_tasks",
                "message": f"Consider moving {len(backlog_tasks)} backlog task(s) to This Week",
                "task_titles": [t["title"] for t in backlog_tasks[:5]]  # Limit to 5
            })
    
    # Issue: Overdue tasks in wrong status
    overdue_in_backlog = [t for t in overdue_tasks if t.get("status") == "Backlog"]
    if overdue_in_backlog:
        issues.append({
            "type": "overdue_in_backlog",
            "severity": "high",
            "message": f"{len(overdue_in_backlog)} overdue task(s) in Backlog status",
            "tasks": overdue_in_backlog
        })
        recommendations.append({
            "type": "move_overdue",
            "message": "Move overdue tasks to This Week or Top Priority",
            "task_titles": [t["title"] for t in overdue_in_backlog]
        })
    
    # Issue: Tasks due after project deadline
    if tasks_due_after_project:
        issues.append({
            "type": "tasks_after_deadline",
            "severity": "medium",
            "message": f"{len(tasks_due_after_project)} task(s) due after project deadline",
            "tasks": tasks_due_after_project
        })
        recommendations.append({
            "type": "adjust_due_dates",
            "message": "Review and adjust task due dates to align with project deadline",
            "task_titles": [t["title"] for t in tasks_due_after_project]
        })
    
    # Issue: Project due soon but no active tasks
    if project_due_date:
        days_until_due = (project_due_date - today).days
        if 0 <= days_until_due <= 14 and len(active_tasks) == 0:
            issues.append({
                "type": "due_soon_no_active",
                "severity": "high",
                "message": f"Project due in {days_until_due} days but has no active tasks"
            })
            recommendations.append({
                "type": "activate_for_deadline",
                "message": "Activate tasks to meet project deadline",
                "task_titles": [t["title"] for t in extracted_tasks if t.get("status") != "Done"][:5]
            })
    
    return {
        "project_id": project["id"],
        "project_title": project["title"],
        "total_tasks": len(extracted_tasks),
        "active_tasks_count": len(active_tasks),
        "overdue_tasks_count": len(overdue_tasks),
        "tasks_due_after_project": len(tasks_due_after_project),
        "issues": issues,
        "recommendations": recommendations,
        "active_tasks": active_tasks,
        "overdue_tasks": overdue_tasks
    }
