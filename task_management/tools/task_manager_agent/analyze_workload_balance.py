"""Analyze workload balance - task distribution and capacity."""

from typing import Dict, Any, List
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID, PROJECTS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties
from .extract_project_properties import extract_project_properties


def analyze_workload_balance() -> "Dict[str, Any]":
    """Analyze workload balance across projects.
    
    Calculates:
    - Total tasks in This Week status
    - Tasks per project distribution
    - Projects with too many tasks (>8-10?)
    - Projects with no tasks in This Week but marked "This Week"
    - Overall workload assessment (manageable, heavy, overloaded)
    
    Returns:
        Dict with workload analysis and issues
    """
    # Get all tasks in "This Week" status
    this_week_tasks_pages = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"equals": "This Week"}
        },
        use_data_source=True
    )
    
    this_week_tasks = [extract_task_properties(t) for t in this_week_tasks_pages]
    
    # Group tasks by project
    tasks_by_project = {}
    orphaned_this_week = []
    
    for task in this_week_tasks:
        project_ids = task.get("project_ids", [])
        if not project_ids:
            orphaned_this_week.append(task)
        else:
            # Tasks can have multiple projects, but typically one
            for project_id in project_ids:
                if project_id not in tasks_by_project:
                    tasks_by_project[project_id] = []
                tasks_by_project[project_id].append(task)
    
    # Get project details for projects with This Week tasks
    project_details = {}
    for project_id in tasks_by_project.keys():
        # Query for this specific project
        projects = query_database_complete(
            PROJECTS_DATA_SOURCE_ID,
            filter_dict={
                "property": "Name",
                "title": {"is_not_empty": True}
            },
            use_data_source=True
        )
        
        # Find the project
        for project_page in projects:
            if project_page.get("id") == project_id:
                project_details[project_id] = extract_project_properties(project_page)
                break
    
    # Analyze distribution
    distribution_by_project = {}
    projects_with_too_many = []
    projects_marked_this_week_no_tasks = []
    
    for project_id, tasks in tasks_by_project.items():
        project = project_details.get(project_id, {})
        project_title = project.get("title", f"Project {project_id[:8]}")
        task_count = len(tasks)
        
        distribution_by_project[project_id] = {
            "project_title": project_title,
            "task_count": task_count,
            "tasks": tasks
        }
        
        # Flag projects with too many tasks
        if task_count > 10:
            projects_with_too_many.append({
                "project_id": project_id,
                "project_title": project_title,
                "task_count": task_count
            })
        elif task_count > 8:
            projects_with_too_many.append({
                "project_id": project_id,
                "project_title": project_title,
                "task_count": task_count,
                "severity": "warning"
            })
    
    # Check for projects marked "This Week" but with no tasks in that status
    all_projects = query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        use_data_source=True
    )
    
    for project_page in all_projects:
        project = extract_project_properties(project_page)
        if project.get("this_week") and project.get("id") not in tasks_by_project:
            # This project is marked "This Week" but has no tasks in that status
            projects_marked_this_week_no_tasks.append({
                "project_id": project.get("id"),
                "project_title": project.get("title"),
                "priority": project.get("priority")
            })
    
    # Calculate overall workload assessment
    total_this_week = len(this_week_tasks)
    
    if total_this_week <= 8:
        workload_assessment = "manageable"
    elif total_this_week <= 15:
        workload_assessment = "heavy"
    else:
        workload_assessment = "overloaded"
    
    # Collect issues
    issues = []
    
    if projects_with_too_many:
        critical = [p for p in projects_with_too_many if p.get("task_count", 0) > 10]
        if critical:
            issues.append({
                "type": "too_many_tasks",
                "severity": "high",
                "message": f"{len(critical)} project(s) have >10 tasks in This Week",
                "projects": critical
            })
        warnings = [p for p in projects_with_too_many if p.get("severity") == "warning"]
        if warnings:
            issues.append({
                "type": "many_tasks",
                "severity": "medium",
                "message": f"{len(warnings)} project(s) have 8-10 tasks in This Week",
                "projects": warnings
            })
    
    if projects_marked_this_week_no_tasks:
        issues.append({
            "type": "marked_this_week_no_tasks",
            "severity": "medium",
            "message": f"{len(projects_marked_this_week_no_tasks)} project(s) marked 'This Week' but have no tasks in that status",
            "projects": projects_marked_this_week_no_tasks
        })
    
    if orphaned_this_week:
        issues.append({
            "type": "orphaned_this_week",
            "severity": "low",
            "message": f"{len(orphaned_this_week)} task(s) in This Week without projects",
            "tasks": orphaned_this_week
        })
    
    return {
        "total_this_week_tasks": total_this_week,
        "workload_assessment": workload_assessment,
        "distribution_by_project": distribution_by_project,
        "projects_with_too_many": projects_with_too_many,
        "projects_marked_this_week_no_tasks": projects_marked_this_week_no_tasks,
        "orphaned_this_week": orphaned_this_week,
        "issues": issues
    }
