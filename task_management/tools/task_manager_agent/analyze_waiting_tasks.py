"""Analyze waiting tasks by duration and project."""

from typing import Dict, Any, List
from datetime import datetime, date
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties
from .analyze_task_project_alignment import get_tasks_for_project


def analyze_waiting_tasks() -> "Dict[str, Any]":
    """Analyze waiting tasks by duration and project.
    
    Groups waiting tasks by duration buckets:
    - Recent (<3 days)
    - Moderate (3-7 days)
    - Needs follow-up (>7 days)
    
    Also groups by project.
    
    Returns:
        Dict with waiting tasks analysis
    """
    # Get all waiting tasks
    waiting_task_pages = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"equals": "Waiting"}
        },
        use_data_source=True
    )
    
    waiting_tasks = [extract_task_properties(t) for t in waiting_task_pages]
    
    today = date.today()
    
    # Calculate waiting duration for each task
    recent = []
    moderate = []
    need_followup = []
    
    for task in waiting_tasks:
        created_time = task.get("created_time")
        if created_time:
            try:
                # Parse ISO format datetime
                created_dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                created_date = created_dt.date()
                days_waiting = (today - created_date).days
                
                task_with_duration = task.copy()
                task_with_duration["days_waiting"] = days_waiting
                
                if days_waiting < 3:
                    recent.append(task_with_duration)
                elif days_waiting <= 7:
                    moderate.append(task_with_duration)
                else:
                    need_followup.append(task_with_duration)
            except:
                # If we can't parse, assume it needs follow-up
                task_with_duration = task.copy()
                task_with_duration["days_waiting"] = None
                need_followup.append(task_with_duration)
        else:
            # No created time, assume needs follow-up
            task_with_duration = task.copy()
            task_with_duration["days_waiting"] = None
            need_followup.append(task_with_duration)
    
    # Group by project
    waiting_by_project = {}
    
    for task in waiting_tasks:
        project_ids = task.get("project_ids", [])
        if not project_ids:
            # Orphaned waiting task
            if "orphaned" not in waiting_by_project:
                waiting_by_project["orphaned"] = []
            waiting_by_project["orphaned"].append(task)
        else:
            for project_id in project_ids:
                if project_id not in waiting_by_project:
                    waiting_by_project[project_id] = []
                waiting_by_project[project_id].append(task)
    
    # Get project titles for better reporting
    from tools.common import PROJECTS_DATA_SOURCE_ID
    from .extract_project_properties import extract_project_properties
    
    project_titles = {}
    if waiting_by_project:
        all_projects = query_database_complete(
            PROJECTS_DATA_SOURCE_ID,
            use_data_source=True
        )
        
        for project_page in all_projects:
            project = extract_project_properties(project_page)
            project_id = project.get("id")
            if project_id in waiting_by_project:
                project_titles[project_id] = project.get("title", f"Project {project_id[:8]}")
    
    # Format waiting by project with titles
    waiting_by_project_formatted = {}
    for project_id, tasks in waiting_by_project.items():
        if project_id == "orphaned":
            waiting_by_project_formatted["orphaned"] = {
                "project_title": "No Project",
                "tasks": tasks,
                "count": len(tasks)
            }
        else:
            waiting_by_project_formatted[project_id] = {
                "project_title": project_titles.get(project_id, f"Project {project_id[:8]}"),
                "tasks": tasks,
                "count": len(tasks)
            }
    
    return {
        "total_waiting": len(waiting_tasks),
        "recent": recent,
        "moderate": moderate,
        "need_followup": need_followup,
        "need_followup_count": len(need_followup),
        "waiting_by_project": waiting_by_project_formatted
    }
