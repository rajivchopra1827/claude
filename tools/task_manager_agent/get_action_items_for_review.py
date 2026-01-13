"""Get action items from meeting transcripts for review."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from tools.context_gathering_agent import search_transcripts
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties


def is_for_rajiv(action_item: Dict[str, Any]) -> bool:
    """Determine if action item is assigned to Rajiv.
    
    Args:
        action_item: Action item dictionary with 'person' field
        
    Returns:
        True if action item is for Rajiv, False otherwise
    """
    person = action_item.get("person")
    if not person:
        return False
    
    # Handle None case and convert to string
    person_str = str(person).lower().strip()
    if not person_str:
        return False
    
    # Check for Rajiv variations
    rajiv_names = ["rajiv", "rajiv chopra"]
    return any(name in person_str for name in rajiv_names)


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from action item text.
    
    Args:
        text: Action item text
        
    Returns:
        List of keywords (excluding common words)
    """
    # Common words to exclude
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "have", "has", "had", "do", "does", "did", "will", "would",
        "should", "could", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them", "my", "your", "his", "her",
        "its", "our", "their", "to", "of", "with", "on", "at", "by",
        "for", "from", "about", "into", "through", "during", "before",
        "after", "above", "below", "up", "down", "out", "off", "over",
        "under", "again", "further", "then", "once"
    }
    
    # Simple keyword extraction - split by spaces and filter
    words = text.lower().split()
    keywords = [w.strip(".,!?;:()[]{}") for w in words if len(w) > 3 and w not in stop_words]
    
    # Return unique keywords, prioritizing longer words
    unique_keywords = []
    seen = set()
    for kw in sorted(keywords, key=len, reverse=True):
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords[:5]  # Return top 5 keywords


def check_duplicates(action_item: Dict[str, Any], all_tasks_cache: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Check for potential duplicate tasks using in-memory search.
    
    Args:
        action_item: Action item dictionary with 'action' field
        all_tasks_cache: Pre-fetched list of all tasks to search through
        
    Returns:
        List of potentially matching tasks
    """
    action_text = action_item.get("action", "")
    if not action_text:
        return []
    
    # Extract keywords
    keywords = extract_keywords(action_text)
    if not keywords:
        return []
    
    # Search for tasks with similar keywords in memory
    potential_matches = []
    seen_task_ids = set()
    action_lower = action_text.lower()
    
    # Check top 3 keywords
    for keyword in keywords[:3]:
        keyword_lower = keyword.lower()
        for task in all_tasks_cache:
            task_id = task.get("id")
            if task_id and task_id not in seen_task_ids:
                # Check if keyword appears in task title
                task_title = task.get("title", "").lower()
                if keyword_lower in task_title:
                    # Additional check: if multiple keywords match, it's more likely a duplicate
                    matching_keywords = sum(1 for kw in keywords[:3] if kw.lower() in task_title)
                    if matching_keywords >= 1:  # At least one keyword match
                        seen_task_ids.add(task_id)
                        potential_matches.append(task)
    
    return potential_matches


def get_action_items_for_review(days_back: int = 7, check_duplicates_flag: bool = True) -> Dict[str, Any]:
    """Get action items from meeting transcripts for review.
    
    Args:
        days_back: Number of days to look back (default: 7)
        check_duplicates_flag: Whether to check for duplicate tasks (default: True)
        
    Returns:
        Dictionary with action items categorized by assignment:
        {
            "summary": {
                "total_action_items": int,
                "for_rajiv": int,
                "waiting_on_others": int,
                "unassigned": int,
                "potential_duplicates": int
            },
            "for_rajiv": [...],
            "waiting_on_others": [...],
            "unassigned": [...]
        }
    """
    # Calculate date threshold
    threshold_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    # OPTIMIZATION: Pre-fetch all tasks once if duplicate checking is enabled
    # This replaces dozens of individual API calls with a single call
    all_tasks_cache = []
    if check_duplicates_flag:
        # Fetch all non-Done tasks once and extract their properties for in-memory searching
        # We exclude "Done" tasks since we don't need to check for duplicates against completed tasks
        all_task_pages = query_database_complete(
            TASKS_DATA_SOURCE_ID,
            filter_dict={
                "property": "Status",
                "status": {"does_not_equal": "Done"}
            },
            use_data_source=True
        )
        # Extract properties for efficient searching
        all_tasks_cache = [extract_task_properties(task) for task in all_task_pages]
    
    # Search for transcripts
    transcripts = search_transcripts(date_on_or_after=threshold_date, limit=50)
    
    # Collect all action items
    all_action_items = []
    for transcript in transcripts:
        action_items = transcript.get("action_items", [])
        meeting_name = transcript.get("name", "Unknown Meeting")
        meeting_date = transcript.get("date", "")
        
        for item in action_items:
            # Add meeting context to action item
            enriched_item = {
                **item,
                "meeting": meeting_name,
                "meeting_date": meeting_date,
            }
            all_action_items.append(enriched_item)
    
    # Categorize action items
    for_rajiv = []
    waiting_on_others = []
    unassigned = []
    total_duplicates = 0
    
    for item in all_action_items:
        # Check for duplicates (only if enabled and using cached tasks)
        if check_duplicates_flag:
            duplicates = check_duplicates(item, all_tasks_cache)
            item["potential_duplicates"] = duplicates
            if duplicates:
                total_duplicates += 1
        else:
            item["potential_duplicates"] = []
        
        # Generate suggested task name
        action_text = item.get("action", "") or ""
        person = item.get("person") or ""
        
        if is_for_rajiv(item):
            # For Rajiv - suggest task name
            suggested_name = action_text
            item["suggested_task_name"] = suggested_name
            for_rajiv.append(item)
        elif person:
            # For others - suggest waiting task
            person_str = str(person) if person else "Unknown"
            suggested_waiting = f"Follow up with {person_str} on: {action_text}"
            item["suggested_waiting_task"] = suggested_waiting
            waiting_on_others.append(item)
        else:
            # Unassigned
            item["suggested_task_name"] = action_text
            unassigned.append(item)
    
    # Build summary
    summary = {
        "total_action_items": len(all_action_items),
        "for_rajiv": len(for_rajiv),
        "waiting_on_others": len(waiting_on_others),
        "unassigned": len(unassigned),
        "potential_duplicates": total_duplicates,
        "date_range": {
            "from": threshold_date,
            "to": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    return {
        "summary": summary,
        "for_rajiv": for_rajiv,
        "waiting_on_others": waiting_on_others,
        "unassigned": unassigned
    }
