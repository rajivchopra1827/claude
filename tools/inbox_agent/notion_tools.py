"""Notion API tools for Inbox Agent - creating tasks, resources, and insights."""

from typing import List, Dict, Any, Optional
from tools.common import (
    get_notion_client,
    query_database_complete,
    TASKS_DB_ID,
    PROJECTS_DATA_SOURCE_ID,
    RESOURCES_DB_ID,
    INSIGHTS_DB_ID,
)


def create_task(
    name: str,
    status: str = "Inbox",
    due_date: Optional[str] = None,
    project_id: Optional[str] = None,
    waiting: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create a new task in Notion.
    
    Args:
        name: Task name/title
        status: Task status (default: "Inbox")
        due_date: Due date in ISO-8601 format (YYYY-MM-DD)
        project_id: Notion page ID of related project
        waiting: List of people/things blocking this task
    
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
    
    return client.pages.create(
        parent={"database_id": TASKS_DB_ID},
        properties=properties
    )


def create_resource(
    name: str,
    url: Optional[str] = None,
    resource_type: Optional[str] = None,
    area: Optional[str] = None,
    status: str = "To Review",
    summary: Optional[str] = None,
    source: Optional[str] = None,
    project_ids: Optional[List[str]] = None,
    confidence_score: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new resource in Notion.
    
    Args:
        name: Resource title
        url: Resource URL
        resource_type: Type (Article, Video, Podcast, Paper/Report, Tool/Product, Book, Other)
        area: Area (AI, EPD, Organization, Research & Insight, Leadership)
        status: Status (default: "To Review")
        summary: Summary text
        source: Where found
        project_ids: List of related project IDs
        confidence_score: Confidence score 0-100
    
    Returns:
        Created resource page object with id and url
    """
    client = get_notion_client()
    
    properties = {
        "Name": {
            "title": [{"text": {"content": name}}]
        },
        "Status": {
            "status": {"name": status}
        }
    }
    
    if url:
        properties["URL"] = {"url": url}
    
    if resource_type:
        properties["Type"] = {"select": {"name": resource_type}}
    
    if area:
        properties["Area"] = {"select": {"name": area}}
    
    if summary:
        properties["Summary"] = {"rich_text": [{"text": {"content": summary}}]}
    
    if source:
        properties["Source"] = {"rich_text": [{"text": {"content": source}}]}
    
    if project_ids:
        properties["Related Projects"] = {
            "relation": [{"id": pid} for pid in project_ids]
        }
    
    if confidence_score is not None:
        properties["Confidence Score"] = {"number": confidence_score}
    
    return client.pages.create(
        parent={"database_id": RESOURCES_DB_ID},
        properties=properties
    )


def create_insight(
    title: str,
    insight_type: str,
    content: Optional[str] = None,
    work_areas: Optional[List[str]] = None,
    source: Optional[str] = None,
    status: str = "Inbox",
    project_ids: Optional[List[str]] = None,
    task_ids: Optional[List[str]] = None,
    confidence_score: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new insight in Notion.
    
    Args:
        title: Insight title
        insight_type: Type (Customer Observation, Feature Idea, Strategic Thought, Data/Screenshot, Pattern, Question)
        content: Rich text content
        work_areas: List of work areas (AI Strategy, Product, Market & Competitive, Team & Hiring, Technical, Leadership)
        source: Source context
        status: Status (default: "Inbox")
        project_ids: List of related project IDs
        task_ids: List of related task IDs
        confidence_score: Confidence score 0-100
    
    Returns:
        Created insight page object with id and url
    """
    client = get_notion_client()
    
    properties = {
        "Title": {
            "title": [{"text": {"content": title}}]
        },
        "Type": {
            "select": {"name": insight_type}
        },
        "Status": {
            "status": {"name": status}
        }
    }
    
    if work_areas:
        properties["Work Area"] = {
            "multi_select": [{"name": area} for area in work_areas]
        }
    
    if source:
        properties["Source"] = {"rich_text": [{"text": {"content": source}}]}
    
    if project_ids:
        properties["Related Projects"] = {
            "relation": [{"id": pid} for pid in project_ids]
        }
    
    if task_ids:
        properties["Related Tasks"] = {
            "relation": [{"id": tid} for tid in task_ids]
        }
    
    if confidence_score is not None:
        properties["Confidence Score"] = {"number": confidence_score}
    
    page = client.pages.create(
        parent={"database_id": INSIGHTS_DB_ID},
        properties=properties
    )
    
    # Add content if provided (requires separate update)
    if content:
        client.blocks.children.append(
            block_id=page["id"],
            children=[{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            }]
        )
    
    return page


def search_projects(query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for projects by name.
    
    Args:
        query: Search query (optional)
    
    Returns:
        List of matching project pages
    """
    if query:
        return query_database_complete(
            PROJECTS_DATA_SOURCE_ID,
            filter_dict={
                "property": "Name",
                "title": {"contains": query}
            },
            use_data_source=True
        )
    else:
        return query_database_complete(PROJECTS_DATA_SOURCE_ID, use_data_source=True)
