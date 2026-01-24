"""Create a new idea in Notion."""

from typing import List, Dict, Any, Optional
import json
from tools.common import get_notion_client, IDEAS_DB_ID

# #region agent log
DEBUG_LOG_PATH = "/Users/rajivchopra/Claude/.cursor/debug.log"
def _debug_log(location, message, data, hypothesis_id):
    import time
    entry = {"location": location, "message": message, "data": data, "timestamp": int(time.time()*1000), "sessionId": "debug-session", "hypothesisId": hypothesis_id}
    with open(DEBUG_LOG_PATH, "a") as f: f.write(json.dumps(entry) + "\n")
# #endregion

def create_idea(
    title: str,
    idea_type: str,
    content: Optional[str] = None,
    work_areas: Optional[List[str]] = None,
    source: Optional[str] = None,
    status: str = "Inbox",
    project_ids: Optional[List[str]] = None,
    task_ids: Optional[List[str]] = None,
    confidence_score: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new idea in Notion.
    
    Args:
        title: Idea title
        idea_type: Type (Customer Observation, Feature Idea, Strategic Thought, Data/Screenshot, Pattern, Question)
        content: Rich text content
        work_areas: List of work areas (AI Strategy, Product, Market & Competitive, Team & Hiring, Technical, Leadership)
        source: Source context
        status: Status (default: "Inbox")
        project_ids: List of related project IDs
        task_ids: List of related task IDs
        confidence_score: Confidence score 0-100
    
    Returns:
        Created idea page object with id and url
    """
    # #region agent log
    import os
    api_key = os.getenv("NOTION_API_KEY", "")
    _debug_log("create_idea.py:entry", "Function called", {"title": title, "idea_type": idea_type, "IDEAS_DB_ID": IDEAS_DB_ID, "api_key_prefix": api_key[:10] if api_key else "MISSING", "api_key_suffix": api_key[-4:] if api_key else "MISSING"}, "A,D")
    # #endregion
    
    client = get_notion_client()
    
    # #region agent log
    # Test if we can retrieve the database before trying to create
    try:
        db_info = client.databases.retrieve(database_id=IDEAS_DB_ID)
        _debug_log("create_idea.py:db_check", "Database retrieved successfully", {"db_title": db_info.get("title", [{}])[0].get("plain_text", "unknown"), "db_id": IDEAS_DB_ID}, "A,B,C")
    except Exception as db_err:
        _debug_log("create_idea.py:db_check_failed", "Failed to retrieve database", {"error": str(db_err), "db_id": IDEAS_DB_ID}, "A,B,C")
    # #endregion
    
    properties = {
        "Title": {
            "title": [{"text": {"content": title}}]
        },
        "Type": {
            "select": {"name": idea_type}
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
    
    # #region agent log
    _debug_log("create_idea.py:before_create", "About to create page", {"database_id": IDEAS_DB_ID, "properties_keys": list(properties.keys())}, "A,B")
    # #endregion
    
    try:
        page = client.pages.create(
            parent={"database_id": IDEAS_DB_ID},
            properties=properties
        )
        # #region agent log
        _debug_log("create_idea.py:after_create", "Page created successfully", {"page_id": page.get("id"), "page_url": page.get("url")}, "A,B,C")
        # #endregion
    except Exception as create_err:
        # #region agent log
        _debug_log("create_idea.py:create_failed", "Page creation failed", {"error": str(create_err), "error_type": type(create_err).__name__}, "A,B,C,D")
        # #endregion
        raise
    
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
