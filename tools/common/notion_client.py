"""Shared Notion API client and query utilities."""

import os
from typing import List, Dict, Any, Optional
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from env.txt
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "env.txt"
))

# Initialize client singleton
_client = None


def get_notion_client() -> Client:
    """Get authenticated Notion client (singleton).
    
    Returns:
        Authenticated Notion Client instance
        
    Raises:
        ValueError: If NOTION_API_KEY is not set in environment
    """
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
    """Query a Notion database and return ALL results (handles pagination).
    
    Args:
        database_id: Notion database ID or data source ID
        filter_dict: Filter criteria (e.g., {"property": "Status", "status": {"equals": "Inbox"}})
        sorts: Sort criteria (e.g., [{"property": "Due", "direction": "ascending"}])
        use_data_source: If True, use data_sources.query() instead of pages.search()
    
    Returns:
        List of all page objects (complete results, pagination handled automatically)
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
        query_params = {}
        if filter_dict:
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
