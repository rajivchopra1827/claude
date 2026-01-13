"""Fetch a single Notion page by ID."""

from typing import Dict, Any
from tools.common import get_notion_client


def fetch_page(page_id: str) -> Dict[str, Any]:
    """Fetch a single Notion page by ID.
    
    Args:
        page_id: Notion page ID
    
    Returns:
        Page object
    """
    client = get_notion_client()
    return client.pages.retrieve(page_id=page_id)
