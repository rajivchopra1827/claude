"""Create a new insight in Notion."""

from typing import List, Dict, Any, Optional
from tools.common import get_notion_client, INSIGHTS_DB_ID


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
