"""Create a task from an action item."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from task_management.tools.inbox_agent.create_task import create_task


def parse_due_date(due_date_text: str, meeting_date: Optional[str] = None) -> Optional[str]:
    """Parse due date from action item text.
    
    Args:
        due_date_text: Text like "Wednesday", "today", "1/15", "next Monday"
        meeting_date: Meeting date in YYYY-MM-DD format (for relative date calculation)
        
    Returns:
        ISO-8601 date string (YYYY-MM-DD) or None if can't parse
    """
    if not due_date_text:
        return None
    
    due_date_text = due_date_text.lower().strip()
    today = datetime.now()
    
    # Handle "today"
    if "today" in due_date_text:
        return today.strftime("%Y-%m-%d")
    
    # Handle day names (Monday, Tuesday, etc.)
    days_of_week = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }
    
    for day_name, day_num in days_of_week.items():
        if day_name in due_date_text:
            # Find next occurrence of this day
            current_day = today.weekday()
            days_ahead = day_num - current_day
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            if "next" in due_date_text:
                days_ahead += 7
            target_date = today + timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")
    
    # Handle date formats like "1/15" or "1/15/2025"
    if "/" in due_date_text:
        parts = due_date_text.split("/")
        if len(parts) >= 2:
            try:
                month = int(parts[0])
                day = int(parts[1])
                year = int(parts[2]) if len(parts) > 2 else today.year
                # If month/day is in the past, assume next year
                if month < today.month or (month == today.month and day < today.day):
                    if len(parts) == 2:  # Only if year wasn't specified
                        year = today.year + 1
                return datetime(year, month, day).strftime("%Y-%m-%d")
            except ValueError:
                pass
    
    return None


def create_task_from_action_item(
    action_item: Dict[str, Any],
    meeting_date: Optional[str] = None,
    project_id: Optional[str] = None,
    status: str = "Inbox"
) -> Dict[str, Any]:
    """Create a task from an action item.
    
    Args:
        action_item: Action item dictionary with 'action', 'person', 'due_date_text' fields
        meeting_date: Meeting date in YYYY-MM-DD format (for relative date calculation)
        project_id: Optional Notion page ID of related project
        status: Task status (default: "Inbox")
        
    Returns:
        Created task page object with id and url
    """
    action_text = action_item.get("action", "")
    person = action_item.get("person", "")
    due_date_text = action_item.get("due_date_text", "")
    
    # Build task name
    task_name = action_text
    if person and person.lower() not in ["rajiv", "rajiv chopra"]:
        # If assigned to someone else, create a follow-up task
        task_name = f"Follow up with {person} on: {action_text}"
    
    # Parse due date
    due_date = None
    if due_date_text:
        due_date = parse_due_date(due_date_text, meeting_date)
    
    # Determine waiting field
    waiting = None
    if person and person.lower() not in ["rajiv", "rajiv chopra", "team", "unassigned"]:
        # Set waiting field if action is for someone else
        waiting = [person]
    
    # Create the task
    return create_task(
        name=task_name,
        status=status,
        due_date=due_date,
        project_id=project_id,
        waiting=waiting
    )
