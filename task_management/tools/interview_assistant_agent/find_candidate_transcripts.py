"""Find interview transcripts for a specific candidate."""

from typing import List, Dict, Any
from tools.notion import search_transcripts


def find_candidate_transcripts(candidate_name: str) -> List[Dict[str, Any]]:
    """Find all interview transcripts for a specific candidate.
    
    Searches the transcripts database for meetings that mention the candidate name
    in the meeting name, attendees, or notes fields.
    
    Args:
        candidate_name: Name of the candidate to search for (e.g., "Aida", "Geoffrey")
    
    Returns:
        List of transcript summaries, each containing:
        - page_id: Notion page ID
        - name: Meeting name
        - date: Meeting date
        - attendees: Attendees list
        - notes: AI-generated summary/notes
        - url: URL property
        - action_items: List of extracted action items
    """
    # Search for candidate name in meeting name and attendees
    # Use keywords search which searches in Name and Notes fields
    results = search_transcripts(
        keywords=candidate_name,
        limit=50  # Allow for multiple interviews per candidate
    )
    
    # Also search by attendee name to catch cases where candidate is listed as attendee
    attendee_results = search_transcripts(
        attendee=candidate_name,
        limit=50
    )
    
    # Combine results and deduplicate by page_id
    all_results = {}
    for result in results + attendee_results:
        page_id = result.get("page_id")
        if page_id:
            all_results[page_id] = result
    
    # Return as list, sorted by date (most recent first)
    sorted_results = sorted(
        all_results.values(),
        key=lambda x: x.get("date", ""),
        reverse=True
    )
    
    return sorted_results
