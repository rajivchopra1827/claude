"""Search recent meeting transcripts for decisions, blockers, and key discussions."""

from typing import Dict, Any, List, Optional
from datetime import date, timedelta
from task_management.tools.context_gathering_agent.search_transcripts import search_transcripts
from task_management.tools.context_gathering_agent.get_transcript_content import get_transcript_content


# Keywords that often indicate decisions or important discussions
DECISION_KEYWORDS = [
    "decided", "agreed", "will do", "action item", "next step",
    "commitment", "approved", "confirmed", "going forward",
    "the plan is", "we're going to", "decision:"
]

BLOCKER_KEYWORDS = [
    "blocked", "waiting on", "risk", "concern", "issue",
    "problem", "challenge", "dependency", "delayed", "stuck"
]

STRATEGIC_KEYWORDS = [
    "fiona", "digible.ai", "ai strategy", "posts", "reporting",
    "fulfillment", "enablement", "roadmap", "milestone", "deadline"
]


def search_recent_decisions(
    days_back: int = 7,
    include_full_content: bool = False
) -> Dict[str, Any]:
    """Search recent meeting transcripts for decisions, blockers, and key discussions.
    
    Args:
        days_back: Number of days to look back (default: 7)
        include_full_content: Whether to fetch full transcript content (slower but more thorough)
        
    Returns:
        Dict with:
        - decisions: List of potential decisions/agreements found
        - blockers: List of blockers/risks mentioned
        - strategic_discussions: Discussions related to strategic priorities
        - meetings_analyzed: List of meetings that were searched
    """
    today = date.today()
    start_date = (today - timedelta(days=days_back)).isoformat()
    
    # Search for recent transcripts
    transcripts = search_transcripts(
        date_on_or_after=start_date,
        limit=20
    )
    
    results = {
        "decisions": [],
        "blockers": [],
        "strategic_discussions": [],
        "meetings_analyzed": []
    }
    
    for transcript in transcripts:
        meeting_info = {
            "name": transcript.get("name", "Unknown Meeting"),
            "date": transcript.get("date"),
            "attendees": transcript.get("attendees", ""),
            "page_id": transcript.get("page_id")
        }
        results["meetings_analyzed"].append(meeting_info)
        
        # Get the notes content
        notes = transcript.get("notes", "")
        
        # If we want more thorough analysis and notes are short, get full content
        if include_full_content and len(notes) < 200 and transcript.get("page_id"):
            try:
                full_content = get_transcript_content(transcript["page_id"])
                if full_content:
                    notes = full_content
            except Exception:
                pass  # Continue with truncated notes if full content fails
        
        # Search for decisions
        notes_lower = notes.lower()
        for keyword in DECISION_KEYWORDS:
            if keyword.lower() in notes_lower:
                # Extract context around the keyword
                excerpt = _extract_excerpt(notes, keyword)
                if excerpt:
                    results["decisions"].append({
                        "meeting": meeting_info["name"],
                        "date": meeting_info["date"],
                        "keyword_found": keyword,
                        "excerpt": excerpt
                    })
                break  # Only one decision entry per meeting per keyword type
        
        # Search for blockers
        for keyword in BLOCKER_KEYWORDS:
            if keyword.lower() in notes_lower:
                excerpt = _extract_excerpt(notes, keyword)
                if excerpt:
                    results["blockers"].append({
                        "meeting": meeting_info["name"],
                        "date": meeting_info["date"],
                        "keyword_found": keyword,
                        "excerpt": excerpt
                    })
                break
        
        # Search for strategic discussions
        for keyword in STRATEGIC_KEYWORDS:
            if keyword.lower() in notes_lower:
                excerpt = _extract_excerpt(notes, keyword)
                if excerpt:
                    results["strategic_discussions"].append({
                        "meeting": meeting_info["name"],
                        "date": meeting_info["date"],
                        "topic": keyword,
                        "excerpt": excerpt
                    })
                break
        
        # Also include action items from the transcript
        if transcript.get("action_items"):
            for action_item in transcript["action_items"]:
                # Action items are implicit decisions
                results["decisions"].append({
                    "meeting": meeting_info["name"],
                    "date": meeting_info["date"],
                    "keyword_found": "action item",
                    "excerpt": f"{action_item.get('person', 'Someone')} to: {action_item.get('action', '')}"
                })
    
    # Deduplicate and limit results
    results["decisions"] = _deduplicate_excerpts(results["decisions"])[:10]
    results["blockers"] = _deduplicate_excerpts(results["blockers"])[:5]
    results["strategic_discussions"] = _deduplicate_excerpts(results["strategic_discussions"])[:5]
    
    return results


def _extract_excerpt(text: str, keyword: str, context_chars: int = 150) -> Optional[str]:
    """Extract an excerpt of text around a keyword.
    
    Args:
        text: Full text to search
        keyword: Keyword to find
        context_chars: Number of characters of context on each side
        
    Returns:
        Excerpt string or None if keyword not found
    """
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    pos = text_lower.find(keyword_lower)
    if pos == -1:
        return None
    
    start = max(0, pos - context_chars)
    end = min(len(text), pos + len(keyword) + context_chars)
    
    excerpt = text[start:end].strip()
    
    # Clean up the excerpt
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(text):
        excerpt = excerpt + "..."
    
    # Replace newlines with spaces for cleaner display
    excerpt = " ".join(excerpt.split())
    
    return excerpt


def _deduplicate_excerpts(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate excerpts based on similar content.
    
    Args:
        items: List of excerpt dicts
        
    Returns:
        Deduplicated list
    """
    seen_excerpts = set()
    unique_items = []
    
    for item in items:
        excerpt = item.get("excerpt", "")
        # Use first 50 chars as dedup key
        key = excerpt[:50].lower() if excerpt else ""
        
        if key and key not in seen_excerpts:
            seen_excerpts.add(key)
            unique_items.append(item)
    
    return unique_items
