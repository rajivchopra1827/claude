"""Create a new task in Notion."""

from typing import List, Dict, Any, Optional
from tools.common import get_notion_client, TASKS_DB_ID


def create_task(
    name: str,
    status: str = "Inbox",
    due_date: Optional[str] = None,
    project_id: Optional[str] = None,
    waiting: Optional[List[str]] = None,
    details: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new task in Notion.
    
    Args:
        name: Task name/title
        status: Task status (default: "Inbox")
        due_date: Due date in ISO-8601 format (YYYY-MM-DD)
        project_id: Notion page ID of related project
        waiting: List of people/things blocking this task
        details: Optional details/content to add to the task page
    
    Returns:
        Created task page object with id and url
    """
    client = get_notion_client()
    
    properties = {
        "Task": {
            "title": [{"text": {"content": name}}]
        },
        "Status": {
            "status": {"name": status}
        }
    }
    
    if due_date:
        properties["Due"] = {
            "date": {"start": due_date}
        }
    
    if project_id:
        properties["Project"] = {
            "relation": [{"id": project_id}]
        }
    
    if waiting:
        properties["Waiting"] = {
            "multi_select": [{"name": w} for w in waiting]
        }
    
    page = client.pages.create(
        parent={"database_id": TASKS_DB_ID},
        properties=properties
    )
    
    # Add details/content if provided (requires separate update)
    if details:
        client.blocks.children.append(
            block_id=page["id"],
            children=[{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": details}}]
                }
            }]
        )
    
    return page