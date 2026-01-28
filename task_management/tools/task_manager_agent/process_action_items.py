"""Process action items from meeting transcripts with auto-creation and review workflow."""

from typing import Dict, Any, List
from .get_action_items_for_review import (
    get_action_items_for_review,
    is_for_rajiv
)
from .check_action_item_duplicates import categorize_duplicates
from .create_task_from_action_item import create_task_from_action_item
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties


def process_action_items(days_back: int = 1) -> Dict[str, Any]:
    """Process action items from meeting transcripts.
    
    Auto-creates tasks for obvious action items (assigned to Rajiv, no duplicates)
    and returns the rest for review, categorized by duplicate status.
    
    Args:
        days_back: Number of days to look back (default: 1 for daily processing)
        
    Returns:
        Dictionary with:
        {
            "summary": {
                "total_action_items": int,
                "auto_created": int,
                "needs_review": int,
                "obvious_duplicates": int,
                "potential_duplicates": int,
                "others": int
            },
            "auto_created_tasks": [...],  # List of created task objects
            "review_items": {
                "obvious_duplicates": [...],  # With duplicate info
                "potential_duplicates": [...],  # With duplicate info
                "others": [...]  # Unassigned or assigned to others
            }
        }
    """
    # Fetch all action items for the date range
    action_items_data = get_action_items_for_review(days_back=days_back, check_duplicates_flag=True)
    
    # Pre-fetch all tasks for duplicate checking
    all_task_pages = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"does_not_equal": "Done"}
        },
        use_data_source=True
    )
    all_tasks_cache = [extract_task_properties(task) for task in all_task_pages]
    
    # Collect all action items (combine for_rajiv, waiting_on_others, unassigned)
    all_action_items = []
    all_action_items.extend(action_items_data.get("for_rajiv", []))
    all_action_items.extend(action_items_data.get("waiting_on_others", []))
    all_action_items.extend(action_items_data.get("unassigned", []))
    
    # Categorize and process
    auto_created_tasks = []
    review_obvious_duplicates = []
    review_potential_duplicates = []
    review_others = []
    
    for item in all_action_items:
        # Check if assigned to Rajiv
        assigned_to_rajiv = is_for_rajiv(item)
        
        # Categorize duplicates using enhanced detection
        duplicate_categories = categorize_duplicates(item, all_tasks_cache)
        obvious_dups = duplicate_categories.get("obvious_duplicates", [])
        potential_dups = duplicate_categories.get("potential_duplicates", [])
        
        # Add duplicate info to item
        item["obvious_duplicates"] = obvious_dups
        item["potential_duplicates"] = potential_dups
        
        # Determine category
        if assigned_to_rajiv and len(obvious_dups) == 0 and len(potential_dups) == 0:
            # Auto-create: assigned to Rajiv, no duplicates
            try:
                meeting_date = item.get("meeting_date")
                task = create_task_from_action_item(
                    action_item=item,
                    meeting_date=meeting_date,
                    status="Inbox"
                )
                auto_created_tasks.append({
                    "task": task,
                    "action_item": item
                })
            except Exception as e:
                # If creation fails, add to review instead
                review_others.append({
                    **item,
                    "creation_error": str(e)
                })
        elif assigned_to_rajiv and len(obvious_dups) > 0:
            # Review: assigned to Rajiv but has obvious duplicates
            review_obvious_duplicates.append(item)
        elif assigned_to_rajiv and len(potential_dups) > 0:
            # Review: assigned to Rajiv but has potential duplicates
            review_potential_duplicates.append(item)
        else:
            # Review: unassigned or assigned to others
            review_others.append(item)
    
    # Build summary
    summary = {
        "total_action_items": len(all_action_items),
        "auto_created": len(auto_created_tasks),
        "needs_review": len(review_obvious_duplicates) + len(review_potential_duplicates) + len(review_others),
        "obvious_duplicates": len(review_obvious_duplicates),
        "potential_duplicates": len(review_potential_duplicates),
        "others": len(review_others)
    }
    
    return {
        "summary": summary,
        "auto_created_tasks": auto_created_tasks,
        "review_items": {
            "obvious_duplicates": review_obvious_duplicates,
            "potential_duplicates": review_potential_duplicates,
            "others": review_others
        }
    }
