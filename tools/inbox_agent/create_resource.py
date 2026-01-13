"""Create a new resource in Notion."""

from typing import List, Dict, Any, Optional
from tools.common import get_notion_client, RESOURCES_DB_ID


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
