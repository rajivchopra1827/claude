"""Update tools for Task Manager Agent - updating tasks in Notion."""

from typing import List, Dict, Any, Optional
from tools.common import get_notion_client


def update_task(
    task_id: str,
    status: Optional[str] = None,
    due_date: Optional[str] = None,
    completed_date: Optional[str] = None,
    project_id: Optional[str] = None,
    waiting: Optional[List[str]] = None,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """Update a task in Notion.
    
    Args:
        task_id: Notion page ID of the task
        status: New status
        due_date: New due date (ISO-8601 format)
        completed_date: Completed date (ISO-8601 format)
        project_id: Project ID to link
        waiting: List of waiting items
        name: New task name
    
    Returns:
        Updated task page object
    """
    client = get_notion_client()
    
    properties = {}
    
    if status:
        properties["Status"] = {"status": {"name": status}}
    
    if due_date:
        properties["Due"] = {"date": {"start": due_date}}
    
    if completed_date:
        properties["Completed"] = {"date": {"start": completed_date}}
    
    if project_id:
        properties["Project"] = {"relation": [{"id": project_id}]}
    
    if waiting is not None:
        properties["Waiting"] = {"multi_select": [{"name": w} for w in waiting]}
    
    if name:
        properties["Task"] = {"title": [{"text": {"content": name}}]}
    
    return client.pages.update(
        page_id=task_id,
        properties=properties
    )


def batch_update_tasks(updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Update multiple tasks in batch.
    
    Args:
        updates: List of update dictionaries, each with task_id and update fields
    
    Returns:
        List of updated task page objects
    """
    results = []
    for update in updates:
        task_id = update.pop("task_id")
        results.append(update_task(task_id, **update))
    return results
