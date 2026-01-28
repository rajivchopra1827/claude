"""Get complete daily review data - all tasks organized by priority."""

from typing import Dict, Any
from datetime import date
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties
from .get_action_items_for_review import get_action_items_for_review


def get_daily_review() -> "Dict[str, Any]":
    """Get complete daily review data - all tasks organized by priority.
    
    Includes action items from meetings in the last 7 days.
    
    Returns:
        Dictionary containing:
        - top_priority: List of Top Priority tasks
        - this_week: List of This Week tasks
        - on_deck: List of On Deck tasks
        - waiting: List of Waiting tasks
        - overdue: List of overdue tasks
        - action_items: Dictionary with action items from last 7 days:
          - summary: Summary statistics
          - for_rajiv: Action items assigned to Rajiv
          - waiting_on_others: Action items assigned to others
          - unassigned: Action items with no assigned person
    """
    # OPTIMIZATION: Combine multiple queries into fewer API calls
    # Instead of 3 separate queries, we'll fetch tasks more efficiently
    
    # Query 1: Get all active tasks (Top Priority, This Week, On Deck) in one call
    active_tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "or": [
                {"property": "Status", "status": {"equals": "Top Priority"}},
                {"property": "Status", "status": {"equals": "This Week"}},
                {"property": "Status", "status": {"equals": "On Deck"}}
            ]
        },
        use_data_source=True
    )
    
    # Query 2: Get waiting tasks
    waiting_tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"equals": "Waiting"}
        },
        use_data_source=True
    )
    
    # Query 3: Get overdue tasks (tasks with due dates in the past that aren't Done)
    today = date.today().isoformat()
    overdue_tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "and": [
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Done"}
                },
                {
                    "property": "Due",
                    "date": {"before": today}
                }
            ]
        },
        use_data_source=True
    )
    
    organized = {
        "top_priority": [],
        "this_week": [],
        "on_deck": [],
        "waiting": [],
        "overdue": []
    }
    
    # Organize active tasks by status
    for task in active_tasks:
        props = extract_task_properties(task)
        status = props["status"]
        if status == "Top Priority":
            organized["top_priority"].append(props)
        elif status == "This Week":
            organized["this_week"].append(props)
        elif status == "On Deck":
            organized["on_deck"].append(props)
    
    # Process waiting tasks
    for task in waiting_tasks:
        organized["waiting"].append(extract_task_properties(task))
    
    # Process overdue tasks
    for task in overdue_tasks:
        organized["overdue"].append(extract_task_properties(task))
    
    # Get action items from last 7 days
    action_items = get_action_items_for_review(days_back=7)
    organized["action_items"] = action_items
    
    return organized
