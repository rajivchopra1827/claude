"""Enhanced duplicate detection for action items with confidence categorization."""

from typing import Dict, Any, List
from difflib import SequenceMatcher
from .get_action_items_for_review import extract_keywords


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using SequenceMatcher.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def categorize_duplicates(
    action_item: Dict[str, Any], 
    all_tasks_cache: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize duplicates into obvious vs potential matches.
    
    Args:
        action_item: Action item dictionary with 'action' field
        all_tasks_cache: Pre-fetched list of all tasks to search through
        
    Returns:
        Dictionary with 'obvious_duplicates' and 'potential_duplicates' lists
    """
    action_text = action_item.get("action", "")
    if not action_text:
        return {"obvious_duplicates": [], "potential_duplicates": []}
    
    # Extract keywords
    keywords = extract_keywords(action_text)
    if not keywords:
        return {"obvious_duplicates": [], "potential_duplicates": []}
    
    obvious_duplicates = []
    potential_duplicates = []
    seen_task_ids = set()
    action_lower = action_text.lower()
    
    for task in all_tasks_cache:
        task_id = task.get("id")
        if not task_id or task_id in seen_task_ids:
            continue
        
        task_title = task.get("title", "").lower()
        if not task_title:
            continue
        
        # Count matching keywords
        matching_keywords = sum(1 for kw in keywords[:3] if kw.lower() in task_title)
        
        # Calculate text similarity
        similarity = calculate_similarity(action_lower, task_title)
        
        # Categorize: Obvious duplicates need 2+ keywords AND high similarity
        if matching_keywords >= 2 and similarity > 0.8:
            obvious_duplicates.append(task)
            seen_task_ids.add(task_id)
        elif matching_keywords >= 1:
            # Potential duplicate: at least one keyword match
            potential_duplicates.append(task)
            seen_task_ids.add(task_id)
    
    return {
        "obvious_duplicates": obvious_duplicates,
        "potential_duplicates": potential_duplicates
    }
