"""
Direct Notion API client for reliable database queries and CRUD operations.
Handles pagination, filtering, and complete data retrieval.
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from env.txt
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "env.txt"))

# Database IDs (from your taxonomy)
TASKS_DB_ID = "2d3e6112-fa50-8004-95a7-fb6b41a2bdd8"
TASKS_DATA_SOURCE_ID = "2d3e6112-fa50-80e9-8a3a-000bc4723604"  # collection:// format
PROJECTS_DB_ID = "2d3e6112-fa50-8015-8921-000b39445099"
PROJECTS_DATA_SOURCE_ID = "2d3e6112-fa50-8015-8921-000b39445099"
RESOURCES_DB_ID = "276649c7-5cd6-46bd-8409-ddfa36addd5d"
INSIGHTS_DB_ID = "b9105b1d-6bdb-44f2-993b-40e324d1ba28"

# Initialize client
_client = None

def get_notion_client() -> Client:
    """Get authenticated Notion client (singleton)."""
    global _client
    if _client is None:
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            raise ValueError("NOTION_API_KEY environment variable not set. Add it to env.txt")
        _client = Client(auth=api_key)
    return _client


def query_database_complete(
    database_id: str,
    filter_dict: Optional[Dict] = None,
    sorts: Optional[List[Dict]] = None,
    use_data_source: bool = False
) -> List[Dict[str, Any]]:
    """
    Query a Notion database and return ALL results (handles pagination).
    
    Args:
        database_id: Notion database ID or data source ID
        filter_dict: Filter criteria (e.g., {"property": "Status", "select": {"equals": "Top Priority"}})
        sorts: Sort criteria (e.g., [{"property": "Due", "direction": "ascending"}])
        use_data_source: If True, use data_sources.query() instead of pages.search()
    
    Returns:
        List of all page objects
    """
    client = get_notion_client()
    all_results = []
    
    if use_data_source:
        # Use data_sources.query() for data source IDs
        # Remove collection:// prefix if present
        data_source_id = database_id.replace("collection://", "")
        query_params = {"data_source_id": data_source_id}
        if filter_dict:
            query_params["filter"] = filter_dict
        if sorts:
            query_params["sorts"] = sorts
        
        # First query
        response = client.data_sources.query(**query_params)
        all_results.extend(response.get("results", []))
        
        # Paginate through remaining results
        while response.get("has_more"):
            next_cursor = response.get("next_cursor")
            query_params["start_cursor"] = next_cursor
            response = client.data_sources.query(**query_params)
            all_results.extend(response.get("results", []))
    else:
        # Use pages.search() for database IDs - search for pages in this database
        # This is a workaround since databases.query() doesn't exist
        query_params = {}
        if filter_dict:
            query_params["filter"] = {"value": "page", "property": "object"}
            # Add database filter
            query_params["filter"] = {
                "and": [
                    {"value": "page", "property": "object"},
                    {"value": database_id, "property": "parent_id"}
                ]
            }
        
        # Use search API to find pages in database
        response = client.search(query=database_id, **query_params)
        all_results.extend(response.get("results", []))
        
        # Filter results to only include pages from this database
        filtered_results = []
        for result in all_results:
            parent = result.get("parent", {})
            if parent.get("database_id") == database_id or parent.get("type") == "database_id":
                filtered_results.append(result)
        all_results = filtered_results
    
    return all_results


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
    
    # Build OR filter
    filters = [
        {
            "property": "Status",
            "status": {"equals": status}
        }
        for status in statuses
    ]
    
    return query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "or": filters
        },
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
    """
    Extract readable properties from a Notion task page object.
    Converts Notion's nested property format to simple dict.
    """
    props = task.get("properties", {})
    
    # Extract Status (Status property type, not Select)
    status_obj = props.get("Status", {}).get("status", {})
    status = status_obj.get("name") if status_obj else None
    
    # Extract Task name (title) - try both "Task" and "Name"
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
    """
    Get complete daily review data - all tasks organized by priority.
    Returns formatted data ready for agent consumption.
    """
    # Get all active tasks
    active_tasks = get_tasks_by_statuses(["Top Priority", "This Week", "On Deck"])
    waiting_tasks = get_waiting_tasks()
    overdue_tasks = get_overdue_tasks()
    
    # Organize by status
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


# ============================================================================
# CREATE OPERATIONS
# ============================================================================

def create_task(
    name: str,
    status: str = "Inbox",
    due_date: Optional[str] = None,
    project_id: Optional[str] = None,
    waiting: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new task in Notion.
    
    Args:
        name: Task name/title
        status: Task status (default: "Inbox")
        due_date: Due date in ISO-8601 format (YYYY-MM-DD)
        project_id: Notion page ID of related project
        waiting: List of people/things blocking this task
    
    Returns:
        Created task page object
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
    """
    Create a new resource in Notion.
    
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
        Created resource page object
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
    """
    Create a new insight in Notion.
    
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
        Created insight page object
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


# ============================================================================
# UPDATE OPERATIONS
# ============================================================================

def update_task(
    task_id: str,
    status: Optional[str] = None,
    due_date: Optional[str] = None,
    completed_date: Optional[str] = None,
    project_id: Optional[str] = None,
    waiting: Optional[List[str]] = None,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a task in Notion.
    
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
        properties["Status"] = {"select": {"name": status}}
    
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


# ============================================================================
# READ OPERATIONS (Additional)
# ============================================================================

def fetch_page(page_id: str) -> Dict[str, Any]:
    """
    Fetch a single Notion page by ID.
    Useful for fetching specific pages like the PM competency model.
    
    Args:
        page_id: Notion page ID
    
    Returns:
        Page object
    """
    client = get_notion_client()
    return client.pages.retrieve(page_id=page_id)


def search_projects(query: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search for projects by name.
    
    Args:
        query: Search query (optional)
    
    Returns:
        List of matching project pages
    """
    if query:
        # Use database query with title filter
        return query_database_complete(
            PROJECTS_DATA_SOURCE_ID,
            filter_dict={
                "property": "Name",
                "title": {"contains": query}
            },
            use_data_source=True
        )
    else:
        # Return all projects
        return query_database_complete(PROJECTS_DATA_SOURCE_ID, use_data_source=True)
