"""Extract action items from meeting transcript notes."""

import re
from typing import List, Dict, Any, Optional
from tools.common import get_notion_client


def find_action_items_section(notes: str) -> Optional[str]:
    """Find and return the action items section from notes.
    
    Looks for "### Next Steps" or "### Action Items" heading and returns
    everything after it until the next heading or end of text.
    
    Args:
        notes: Full notes text from transcript
        
    Returns:
        Action items section text, or None if not found
    """
    # Pattern to match "### Next Steps" or "### Action Items" followed by content
    # until next heading (###) or end of string
    pattern = r"(?:###\s*(?:Next Steps|Action Items)\s*\n)(.*?)(?=\n###|\Z)"
    match = re.search(pattern, notes, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_bullets(text: str) -> List[str]:
    """Extract all bullet points from text.
    
    Args:
        text: Text containing bullet points
        
    Returns:
        List of bullet point text (with bullet marker removed)
    """
    bullets = []
    for line in text.split('\n'):
        line = line.strip()
        # Match bullet points starting with - or *
        if line.startswith('- ') or line.startswith('* '):
            bullets.append(line[2:].strip())
        # Also handle indented bullets (sub-items)
        elif line.startswith('  - ') or line.startswith('  * '):
            bullets.append(line[4:].strip())
    return bullets


def parse_action_item(bullet: str) -> Dict[str, Any]:
    """Parse a bullet point into structured action item.
    
    Args:
        bullet: Bullet point text (e.g., "Rajiv: Goal recalibration homework")
        
    Returns:
        Dictionary with:
        - person: Person responsible (if mentioned)
        - action: Action description
        - raw_text: Original bullet point text
        - has_due_date: Boolean indicating if due date mentioned
        - due_date_text: Extracted due date text (if any)
    """
    # Pattern: "Person: Action description" or "Person - Action description"
    # Handle both single names and full names (e.g., "Rajiv" or "Rajiv Chopra")
    # Also handle multiple people: "Rajiv and Melissa: ..."
    person_patterns = [
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+and\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)*):\s*(.+)$",  # "Person: action" or "Person and Person: action"
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+and\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)*)\s+-\s+(.+)$",  # "Person - action" or "Person and Person - action"
    ]
    
    person = None
    action = bullet
    
    for pattern in person_patterns:
        match = re.match(pattern, bullet, re.IGNORECASE)
        if match:
            person = match.group(1)
            action = match.group(2)
            break
    
    # Check for due date mentions
    # Order matters - more specific patterns first
    due_date_patterns = [
        r"by\s+(\w+day\s+\d+/\d+)",      # "by Friday 1/15"
        r"by\s+(\w+day)",                 # "by Friday"
        r"next\s+(\w+day)",               # "next Monday"
        r"(\w+day)\s+\d+/\d+",           # "Monday 1/15"
        r"(\d+/\d+/\d+)",                 # "1/15/2024"
        r"(\d+/\d+)",                     # "1/15", "12/25"
        r"(\w+day)",                      # "Monday", "Friday" (standalone, but check it's not part of another word)
    ]
    
    due_date_text = None
    for pattern in due_date_patterns:
        match = re.search(pattern, action, re.IGNORECASE)
        if match:
            due_date_text = match.group(1)
            # Avoid false positives - don't match "today" or "yesterday" as days
            if due_date_text.lower() in ['today', 'yesterday']:
                continue
            break
    
    return {
        "person": person,
        "action": action,
        "raw_text": bullet,
        "has_due_date": due_date_text is not None,
        "due_date_text": due_date_text
    }


def extract_action_items(notes: str) -> List[Dict[str, Any]]:
    """Extract action items from meeting transcript notes.
    
    Args:
        notes: Full notes text from transcript
        
    Returns:
        List of parsed action items, each containing:
        - person: Person responsible (if mentioned)
        - action: Action description
        - raw_text: Original bullet point text
        - has_due_date: Boolean indicating if due date mentioned
        - due_date_text: Extracted due date text (if any)
    """
    if not notes:
        return []
    
    # Find the action items section
    section = find_action_items_section(notes)
    if not section:
        return []
    
    # Extract bullet points from the section
    bullets = extract_bullets(section)
    if not bullets:
        return []
    
    # Parse each bullet into structured action item
    action_items = []
    for bullet in bullets:
        # Skip empty bullets
        if not bullet.strip():
            continue
        action_items.append(parse_action_item(bullet))
    
    return action_items


def extract_action_items_from_notes(notes: str) -> List[Dict[str, Any]]:
    """Extract action items directly from notes text.
    
    This is a convenience wrapper around extract_action_items() for clarity.
    
    Args:
        notes: Full notes text from transcript
        
    Returns:
        List of parsed action items
    """
    return extract_action_items(notes)


def extract_action_items_from_transcript(page_id: str) -> List[Dict[str, Any]]:
    """Extract action items from a specific meeting transcript.
    
    NOTE: This function may fail if the page_id comes from data_sources.query() results,
    as those pages may not be directly accessible via pages.retrieve(). 
    Instead, use extract_action_items_from_notes() with the Notes field from search results.
    
    Args:
        page_id: Notion page ID of the transcript (must be a valid UUID format)
                 Use the 'page_id' field from search_transcripts() results
        
    Returns:
        List of parsed action items with same structure as extract_action_items()
        
    Raises:
        ValueError: If page_id is not a valid UUID format
    """
    import re
    
    # Validate page_id is a UUID (Notion page IDs are UUIDs)
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, page_id, re.IGNORECASE):
        raise ValueError(
            f"Invalid page_id format: '{page_id}'. "
            f"Expected a UUID format (e.g., '29fe6112-fa50-8060-9d34-cf9063bc3706'). "
            f"Use the 'page_id' field from search_transcripts() results."
        )
    
    client = get_notion_client()
    
    # Fetch page - this may fail for pages from data_sources.query()
    page = client.pages.retrieve(page_id=page_id)
    
    # Extract Notes property
    properties = page.get("properties", {})
    notes_prop = properties.get("Notes", {})
    
    notes = ""
    if notes_prop.get("rich_text"):
        notes = "".join([item.get("plain_text", "") for item in notes_prop["rich_text"]])
    
    # Extract action items from notes
    return extract_action_items(notes)
