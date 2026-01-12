"""Notion API tools for Interview Assistant Agent - fetching pages."""

from typing import Dict, Any
from tools.common import get_notion_client, PM_COMPETENCY_MODEL_ID


def fetch_page(page_id: str) -> Dict[str, Any]:
    """Fetch a single Notion page by ID.
    
    Args:
        page_id: Notion page ID
    
    Returns:
        Page object
    """
    client = get_notion_client()
    return client.pages.retrieve(page_id=page_id)


def fetch_competency_model() -> Dict[str, Any]:
    """Fetch the PM competency model page.
    
    Returns:
        PM competency model page object
    """
    return fetch_page(PM_COMPETENCY_MODEL_ID)
