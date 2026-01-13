"""Extract readable properties from a Notion project page object."""

from typing import Dict, Any


def extract_project_properties(project) -> "Dict[str, Any]":
    """Extract readable properties from a Notion project page object.
    
    Args:
        project: Dict[str, Any] - Notion project page object
    
    Returns:
        Dict[str, Any] - Extracted project properties
    """
    props = project.get("properties", {})
    
    # Extract Project name (title)
    title_obj = props.get("Name", {})
    title = ""
    if title_obj.get("title"):
        title = "".join([text.get("plain_text", "") for text in title_obj["title"]])
    
    # Extract Priority
    priority_obj = props.get("Priority", {}).get("select", {})
    priority = priority_obj.get("name") if priority_obj else None
    
    # Extract Due date
    due_obj = props.get("Due", {}).get("date", {})
    due_date = due_obj.get("start") if due_obj else None
    
    # Extract Completed date
    completed_obj = props.get("Completed", {}).get("date", {})
    completed_date = completed_obj.get("start") if completed_obj else None
    
    # Extract This Week (checkbox)
    this_week_obj = props.get("This Week", {}).get("checkbox", {})
    this_week = this_week_obj if isinstance(this_week_obj, bool) else False
    
    # Extract Tasks (relation)
    tasks_relation = props.get("Tasks", {}).get("relation", [])
    task_ids = [rel.get("id") for rel in tasks_relation] if tasks_relation else []
    
    # Extract Actionable Tasks count (formula) - if available
    actionable_tasks_obj = props.get("Actionable Tasks", {})
    actionable_tasks_count = None
    if actionable_tasks_obj.get("formula", {}).get("number") is not None:
        actionable_tasks_count = actionable_tasks_obj["formula"]["number"]
    
    # Extract Waiting Tasks count (formula) - if available
    waiting_tasks_obj = props.get("Waiting Tasks", {})
    waiting_tasks_count = None
    if waiting_tasks_obj.get("formula", {}).get("number") is not None:
        waiting_tasks_count = waiting_tasks_obj["formula"]["number"]
    
    return {
        "id": project.get("id"),
        "url": project.get("url"),
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed_date": completed_date,
        "this_week": this_week,
        "task_ids": task_ids,
        "actionable_tasks_count": actionable_tasks_count,
        "waiting_tasks_count": waiting_tasks_count,
        "created_time": project.get("created_time"),
        "last_edited_time": project.get("last_edited_time")
    }
