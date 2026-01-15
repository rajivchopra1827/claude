"""Get project history with progress tracking."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date
from tools.common import query_database_complete, PROJECTS_DATA_SOURCE_ID
from tools.task_manager_agent.extract_project_properties import extract_project_properties
from tools.task_manager_agent.extract_task_properties import extract_task_properties
from tools.common import TASKS_DATA_SOURCE_ID


def get_project_history(
    include_completed: bool = True,
    include_active: bool = True,
    priority_filter: Optional[str] = None
) -> "Dict[str, Any]":
    """Get project history with progress tracking.
    
    Args:
        include_completed: Include completed projects
        include_active: Include active (non-completed) projects
        priority_filter: Filter by priority (P1, P2, P3, Monitoring, Done)
    
    Returns:
        Dictionary containing:
        - projects: List of project dictionaries with properties and task data
        - summary: Summary statistics
    """
    # Build filter
    filter_conditions = []
    
    # Status filter
    if include_completed and include_active:
        # Include all projects
        pass
    elif include_completed:
        filter_conditions.append({
            "property": "Priority",
            "select": {"equals": "Done"}
        })
    elif include_active:
        filter_conditions.append({
            "property": "Priority",
            "select": {"does_not_equal": "Done"}
        })
    
    # Priority filter
    if priority_filter:
        filter_conditions.append({
            "property": "Priority",
            "select": {"equals": priority_filter}
        })
    
    # Build final filter
    filter_dict = None
    if filter_conditions:
        if len(filter_conditions) == 1:
            filter_dict = filter_conditions[0]
        else:
            filter_dict = {"and": filter_conditions}
    
    # Query projects
    projects_raw = query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        filter_dict=filter_dict,
        use_data_source=True
    )
    
    # Extract properties and enrich with task data
    projects = []
    all_tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        use_data_source=True
    )
    
    # Create task lookup by project ID
    tasks_by_project = {}
    for task in all_tasks:
        task_props = extract_task_properties(task)
        project_ids = task_props.get("project_ids", [])
        for project_id in project_ids:
            if project_id not in tasks_by_project:
                tasks_by_project[project_id] = []
            tasks_by_project[project_id].append(task_props)
    
    for project in projects_raw:
        project_props = extract_project_properties(project)
        project_id = project_props.get("id")
        
        # Get tasks for this project
        project_tasks = tasks_by_project.get(project_id, [])
        completed_tasks = [t for t in project_tasks if t.get("status") == "Done"]
        active_tasks = [t for t in project_tasks if t.get("status") != "Done"]
        
        # Calculate project metrics
        total_tasks = len(project_tasks)
        completion_rate = len(completed_tasks) / total_tasks if total_tasks > 0 else 0
        
        # Calculate time to complete for completed tasks
        time_to_complete_days = []
        for task in completed_tasks:
            created = task.get("created_time")
            completed = task.get("completed_date")
            
            if created and completed:
                try:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    completed_dt = datetime.fromisoformat(completed)
                    days = (completed_dt.date() - created_dt.date()).days
                    if days >= 0:
                        time_to_complete_days.append(days)
                except (ValueError, AttributeError):
                    pass
        
        # Calculate project age
        project_age_days = None
        created = project_props.get("created_time")
        if created:
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                project_age_days = (date.today() - created_dt.date()).days
            except (ValueError, AttributeError):
                pass
        
        # Add task metrics to project
        project_props["task_metrics"] = {
            "total_tasks": total_tasks,
            "completed_tasks": len(completed_tasks),
            "active_tasks": len(active_tasks),
            "completion_rate": completion_rate,
            "avg_time_to_complete_days": sum(time_to_complete_days) / len(time_to_complete_days) if time_to_complete_days else None,
            "project_age_days": project_age_days,
        }
        
        projects.append(project_props)
    
    # Calculate summary statistics
    completed_projects = [p for p in projects if p.get("priority") == "Done"]
    active_projects = [p for p in projects if p.get("priority") != "Done"]
    
    # Group by priority
    projects_by_priority = {}
    for project in projects:
        priority = project.get("priority") or "None"
        if priority not in projects_by_priority:
            projects_by_priority[priority] = []
        projects_by_priority[priority].append(project)
    
    summary = {
        "total_projects": len(projects),
        "completed_projects": len(completed_projects),
        "active_projects": len(active_projects),
        "projects_by_priority": {k: len(v) for k, v in projects_by_priority.items()},
        "avg_completion_rate": sum(p["task_metrics"]["completion_rate"] for p in projects) / len(projects) if projects else 0,
    }
    
    return {
        "projects": projects,
        "summary": summary
    }
