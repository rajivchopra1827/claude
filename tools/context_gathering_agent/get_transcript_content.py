"""Get the full transcript content from a meeting transcript page."""

from typing import Dict, Any
from tools.common import get_page_content


def get_transcript_content(page_id: str) -> Dict[str, Any]:
    """Get the full transcript content from a meeting transcript page.
    
    This function fetches the actual transcript text stored in the page body content.
    Use get_transcript() if you only need the database properties (name, date, attendees, notes, url).
    
    Args:
        page_id: Notion page ID of the transcript
    
    Returns:
        Dictionary containing:
        - page_id: Notion page ID
        - transcript: Full raw transcript text from page content
    """
    # Extract full transcript content from page blocks
    transcript = get_page_content(page_id)
    
    return {
        "page_id": page_id,
        "transcript": transcript
    }
