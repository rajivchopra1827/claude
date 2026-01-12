"""Query tools for Task Manager Agent - fetching tasks from Notion."""

from typing import List, Dict, Any, Optional
from datetime import date
from tools.common import (
    query_database_complete,
    TASKS_DATA_SOURCE_ID,
    PROJECTS_DATA_SOURCE_ID,
)


def get_tasks_by_status(status: str) -> List[Dict[str, Any]]:
    """Get all tasks with a specific status."""
    return query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"equals": status}
        },
        use_data_source=True
    )


def get_tasks_by_statuses(statuses: List[str]) -> List[Dict[str, Any]]:
    """Get all tasks matching any of the given statuses."""
    if not statuses:
        return []
    
    filters = [
        {
            "property": "Status",
            "status": {"equals": status}
        }
        for status in statuses
    ]
    
    return query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={"or": filters},
        use_data_source=True
    )


def get_waiting_tasks() -> List[Dict[str, Any]]:
    """Get all tasks in Waiting status."""
    return get_tasks_by_status("Waiting")


def get_inbox_tasks() -> List[Dict[str, Any]]:
    """Get all tasks in Inbox status."""
    return get_tasks_by_status("Inbox")


def get_overdue_tasks() -> List[Dict[str, Any]]:
    """Get tasks with due dates in the past that aren't Done."""
    today = date.today().isoformat()
    
    tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "and": [
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Done"}
                },
                {
                    "property": "Due",
                    "date": {"before": today}
                }
            ]
        },
        use_data_source=True
    )
    
    return tasks


def extract_task_properties(task: Dict[str, Any]) -> Dict[str, Any]:
    """Extract readable properties from a Notion task page object."""
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


def get_daily_review() -> Dict[str, Any]:
    """Get complete daily review data - all tasks organized by priority."""
    active_tasks = get_tasks_by_statuses(["Top Priority", "This Week", "On Deck"])
    waiting_tasks = get_waiting_tasks()
    overdue_tasks = get_overdue_tasks()
    
    organized = {
        "top_priority": [],
        "this_week": [],
        "on_deck": [],
        "waiting": [],
        "overdue": []
    }
    
    for task in active_tasks:
        props = extract_task_properties(task)
        status = props["status"]
        if status == "Top Priority":
            organized["top_priority"].append(props)
        elif status == "This Week":
            organized["this_week"].append(props)
        elif status == "On Deck":
            organized["on_deck"].append(props)
    
    for task in waiting_tasks:
        organized["waiting"].append(extract_task_properties(task))
    
    for task in overdue_tasks:
        organized["overdue"].append(extract_task_properties(task))
    
    return organized


def query_tasks_by_title(title_query: str) -> List[Dict[str, Any]]:
    """Query tasks by title (for searching/finding tasks).
    
    Args:
        title_query: Search query for task title
    
    Returns:
        List of matching tasks with extracted properties
    """
    tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Task",
            "title": {"contains": title_query}
        },
        use_data_source=True
    )
    
    return [extract_task_properties(task) for task in tasks]
