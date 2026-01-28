"""Get a specific meeting transcript by page ID (properties only, no content)."""

from typing import Dict, Any, Optional
from tools.common import get_notion_client
from .extract_action_items import extract_action_items


def get_transcript(page_id: str, include_action_items: bool = False) -> Dict[str, Any]:
    """Get a specific meeting transcript by page ID, returning only database properties.
    
    This function returns only the column/property values, not the full transcript content.
    Use get_transcript_content() if you need the actual transcript text from the page body.
    
    Args:
        page_id: Notion page ID of the transcript
        include_action_items: If True, extract and include action items from Notes field
    
    Returns:
        Dictionary containing:
        - page_id: Notion page ID
        - name: Meeting name
        - date: Meeting date
        - attendees: Attendees list
        - notes: AI-generated summary/notes
        - url: URL property
        - action_items: List of extracted action items (if include_action_items=True)
    """
    client = get_notion_client()
    
    # Fetch page
    page = client.pages.retrieve(page_id=page_id)
    
    # Extract properties only (no page content)
    properties = page.get("properties", {})
    
    name = ""
    name_prop = properties.get("Name", {})
    if name_prop.get("title"):
        name = "".join([item.get("plain_text", "") for item in name_prop["title"]])
    
    date = None
    date_prop = properties.get("Date", {})
    if date_prop.get("date"):
        date = date_prop["date"].get("start")
    
    attendees = ""
    attendees_prop = properties.get("Attendees", {})
    if attendees_prop.get("rich_text"):
        attendees = "".join([item.get("plain_text", "") for item in attendees_prop["rich_text"]])
    
    notes = ""
    notes_prop = properties.get("Notes", {})
    if notes_prop.get("rich_text"):
        notes = "".join([item.get("plain_text", "") for item in notes_prop["rich_text"]])
    
    url = None
    url_prop = properties.get("URL", {})
    if url_prop.get("url"):
        url = url_prop["url"]
    
    result = {
        "page_id": page_id,
        "name": name,
        "date": date,
        "attendees": attendees,
        "notes": notes,
        "url": url,
    }
    
    # Extract action items if requested
    if include_action_items:
        result["action_items"] = extract_action_items(notes)
    
    return result