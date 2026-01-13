"""Search meeting transcripts in Notion."""

from typing import List, Dict, Any, Optional
from tools.common import query_database_complete, MEETING_TRANSCRIPTS_DATA_SOURCE_ID
from .extract_action_items import extract_action_items


def search_transcripts(
    keywords: Optional[str] = None,
    attendee: Optional[str] = None,
    date_from: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    meeting_name: Optional[str] = None,
    limit: Optional[int] = 20
) -> List[Dict[str, Any]]:
    """Search meeting transcripts with various filters.
    
    Args:
        keywords: Search for keywords in meeting name, notes, or transcript content
        attendee: Filter by attendee name (searches in Attendees field)
        date_from: Filter transcripts from this date (YYYY-MM-DD format)
        date_on_or_after: Filter transcripts on or after this date (YYYY-MM-DD format)
        date_before: Filter transcripts before this date (YYYY-MM-DD format)
        meeting_name: Filter by meeting name (partial match)
        limit: Maximum number of results to return (default: 20, max: 100)
    
    Returns:
        List of transcript summaries with essential fields only:
        - page_id: Notion page ID (for fetching full transcript if needed)
        - name: Meeting name
        - date: Meeting date
        - attendees: Attendees list
        - notes: AI-generated summary/notes (truncated if too long)
        - url: URL property
    """
    filters = []
    
    # Build filter conditions
    if keywords:
        # Search in Name (title), Notes, and potentially content
        # Note: Notion API doesn't support full-text search across all fields easily
        # We'll search in Name and Notes fields
        filters.append({
            "or": [
                {
                    "property": "Name",
                    "title": {"contains": keywords}
                },
                {
                    "property": "Notes",
                    "rich_text": {"contains": keywords}
                }
            ]
        })
    
    if attendee:
        filters.append({
            "property": "Attendees",
            "rich_text": {"contains": attendee}
        })
    
    if date_from or date_on_or_after:
        date_value = date_on_or_after or date_from
        filters.append({
            "property": "Date",
            "date": {"on_or_after": date_value}
        })
    
    if date_before:
        filters.append({
            "property": "Date",
            "date": {"before": date_before}
        })
    
    if meeting_name:
        filters.append({
            "property": "Name",
            "title": {"contains": meeting_name}
        })
    
    # Build filter dict
    filter_dict = None
    if filters:
        if len(filters) == 1:
            filter_dict = filters[0]
        else:
            filter_dict = {"and": filters}
    
    # Query database (limit results to prevent token overflow)
    max_limit = min(limit or 20, 100)  # Cap at 100 for safety
    all_results = query_database_complete(
        MEETING_TRANSCRIPTS_DATA_SOURCE_ID,
        filter_dict=filter_dict,
        sorts=[{"property": "Date", "direction": "descending"}],
        use_data_source=True
    )
    
    # Limit results
    limited_results = all_results[:max_limit]
    
    # Extract only essential fields to reduce token usage
    summaries = []
    for page in limited_results:
        properties = page.get("properties", {})
        
        # Extract name
        name = ""
        name_prop = properties.get("Name", {})
        if name_prop.get("title"):
            name = "".join([item.get("plain_text", "") for item in name_prop["title"]])
        
        # Extract date
        date = None
        date_prop = properties.get("Date", {})
        if date_prop.get("date"):
            date = date_prop["date"].get("start")
        
        # Extract attendees
        attendees = ""
        attendees_prop = properties.get("Attendees", {})
        if attendees_prop.get("rich_text"):
            attendees = "".join([item.get("plain_text", "") for item in attendees_prop["rich_text"]])
        
        # Extract notes (keep full version for action item extraction, truncate for display)
        notes_full = ""
        notes_prop = properties.get("Notes", {})
        if notes_prop.get("rich_text"):
            notes_full = "".join([item.get("plain_text", "") for item in notes_prop["rich_text"]])
        
        # Truncate notes for display (to prevent token overflow)
        notes = notes_full
        if len(notes) > 500:
            notes = notes[:500] + "..."
        
        # Extract URL
        url = None
        url_prop = properties.get("URL", {})
        if url_prop.get("url"):
            url = url_prop["url"]
        
        page_id = page.get("id")
        
        # Extract action items from full notes (before truncation)
        action_items = []
        if notes_full:
            try:
                action_items = extract_action_items(notes_full)
            except Exception:
                # If extraction fails, continue without action items
                pass
        
        summaries.append({
            "page_id": page_id,
            "name": name,
            "date": date,
            "attendees": attendees,
            "notes": notes,  # Truncated for display
            "url": url,
            "action_items": action_items,  # Extracted from full notes
        })
    
    return summaries
