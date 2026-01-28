"""Extract readable properties from a Notion task page object."""

from typing import Dict, Any


def extract_task_properties(task) -> "Dict[str, Any]":
    """Extract readable properties from a Notion task page object.
    
    Args:
        task: Dict[str, Any] - Notion task page object
    
    Returns:
        Dict[str, Any] - Extracted task properties
    """
    props = task.get("properties", {})
    
    # Extract Status
    status_obj = props.get("Status", {}).get("status", {})
    status = status_obj.get("name") if status_obj else None
    
    # Extract Task name (title)
    title_obj = props.get("Task", {}) or props.get("Name", {})
    title = ""
    if title_obj.get("title"):
        title = "".join([text.get("plain_text", "") for text in title_obj["title"]])
    
    # Extract Due date
    due_obj = props.get("Due", {}).get("date", {})
    due_date = due_obj.get("start") if due_obj else None
    
    # Extract Completed date
    completed_obj = props.get("Completed", {}).get("date", {})
    completed_date = completed_obj.get("start") if completed_obj else None
    
    # Extract Project (relation)
    project_relation = props.get("Project", {}).get("relation", [])
    project_ids = [rel.get("id") for rel in project_relation] if project_relation else []
    
    # Extract Waiting (multi-select)
    waiting_obj = props.get("Waiting", {}).get("multi_select", [])
    waiting = [w.get("name") for w in waiting_obj] if waiting_obj else []
    
    return {
        "id": task.get("id"),
        "url": task.get("url"),
        "title": title,
        "status": status,
        "due_date": due_date,
        "completed_date": completed_date,
        "project_ids": project_ids,
        "waiting": waiting,
        "created_time": task.get("created_time"),
        "last_edited_time": task.get("last_edited_time")
    }
