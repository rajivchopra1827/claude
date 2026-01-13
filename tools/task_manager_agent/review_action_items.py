"""Helper functions for reviewing and creating tasks from action items."""

from typing import Dict, Any, List, Optional
from .create_task_from_action_item import create_task_from_action_item


def create_tasks_from_review_items(
    review_items: List[Dict[str, Any]], 
    approved_indices: List[int],
    project_id: Optional[str] = None,
    status: str = "Inbox"
) -> List[Dict[str, Any]]:
    """Create tasks from approved review items.
    
    Args:
        review_items: List of action item dictionaries to review
        approved_indices: List of indices (0-based) of items to create tasks for
        project_id: Optional Notion page ID of related project
        status: Task status (default: "Inbox")
        
    Returns:
        List of created task objects with action item context:
        [{"task": {...}, "action_item": {...}}, ...]
    """
    created_tasks = []
    
    for idx in approved_indices:
        if idx < 0 or idx >= len(review_items):
            continue
        
        item = review_items[idx]
        meeting_date = item.get("meeting_date")
        
        try:
            task = create_task_from_action_item(
                action_item=item,
                meeting_date=meeting_date,
                project_id=project_id,
                status=status
            )
            created_tasks.append({
                "task": task,
                "action_item": item
            })
        except Exception as e:
            # Store error for reporting
            created_tasks.append({
                "error": str(e),
                "action_item": item
            })
    
    return created_tasks


def format_review_item_for_display(item: Dict[str, Any], index: int) -> str:
    """Format a review item for display to the user.
    
    Args:
        item: Action item dictionary
        index: 1-based index for display
        
    Returns:
        Formatted string representation
    """
    action_text = item.get("action", "")
    person = item.get("person", "")
    meeting = item.get("meeting", "Unknown Meeting")
    meeting_date = item.get("meeting_date", "")
    due_date_text = item.get("due_date_text", "")
    
    # Build display text
    lines = [f"{index}. {action_text}"]
    
    # Add person if assigned
    if person:
        lines.append(f"   → Assigned to: {person}")
    
    # Add meeting context
    if meeting_date:
        lines.append(f"   → From: \"{meeting}\" ({meeting_date})")
    else:
        lines.append(f"   → From: \"{meeting}\"")
    
    # Add due date if mentioned
    if due_date_text:
        lines.append(f"   → Due: {due_date_text}")
    
    # Add suggested task name
    suggested_name = item.get("suggested_task_name") or item.get("suggested_waiting_task", "")
    if suggested_name:
        lines.append(f"   → Would create: \"{suggested_name}\"")
    
    # Add duplicates if any
    obvious_dups = item.get("obvious_duplicates", [])
    potential_dups = item.get("potential_duplicates", [])
    
    if obvious_dups:
        lines.append(f"   → ⚠️ Matches existing task(s):")
        for dup in obvious_dups:
            dup_title = dup.get("title", "Unknown")
            lines.append(f"      - \"{dup_title}\"")
    
    if potential_dups and not obvious_dups:
        lines.append(f"   → ⚠️ Possible match(es):")
        for dup in potential_dups[:2]:  # Show max 2 potential matches
            dup_title = dup.get("title", "Unknown")
            lines.append(f"      - \"{dup_title}\"")
    
    return "\n".join(lines)
