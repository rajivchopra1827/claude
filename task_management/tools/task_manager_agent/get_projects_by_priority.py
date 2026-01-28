"""Query projects by priority and due date."""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from tools.common import query_database_complete, PROJECTS_DATA_SOURCE_ID


def get_projects_by_priority(priority: str) -> "List[Dict[str, Any]]":
    """Get all projects with a specific priority.
    
    Args:
        priority: Priority level (P1, P2, P3, Monitoring, Done)
    
    Returns:
        List of project page objects matching the priority
    """
    return query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Priority",
            "select": {"equals": priority}
        },
        use_data_source=True
    )


def get_projects_due_soon(days_ahead: int = 14) -> "List[Dict[str, Any]]":
    """Get projects with due dates within the specified number of days.
    
    Args:
        days_ahead: Number of days ahead to look (default: 14)
    
    Returns:
        List of project page objects with due dates within the timeframe
    """
    today = date.today()
    end_date = today + timedelta(days=days_ahead)
    
    return query_database_complete(
        PROJECTS_DATA_SOURCE_ID,
        filter_dict={
            "and": [
                {
                    "property": "Due",
                    "date": {"is_not_empty": True}
                },
                {
                    "property": "Due",
                    "date": {
                        "on_or_before": end_date.isoformat()
                    }
                }
            ]
        },
        use_data_source=True
    )


def get_projects_needing_attention(days_ahead: int = 14) -> "List[Dict[str, Any]]":
    """Get projects that need attention: P1/P2 priority OR due within N days.
    
    Args:
        days_ahead: Number of days ahead to consider "due soon" (default: 14)
    
    Returns:
        List of project page objects (deduplicated)
    """
    # Get P1 and P2 projects
    p1_projects = get_projects_by_priority("P1")
    p2_projects = get_projects_by_priority("P2")
    
    # Get projects due soon
    due_soon_projects = get_projects_due_soon(days_ahead)
    
    # Combine and deduplicate by ID
    seen_ids = set()
    result = []
    
    for project in p1_projects + p2_projects + due_soon_projects:
        project_id = project.get("id")
        if project_id and project_id not in seen_ids:
            seen_ids.add(project_id)
            result.append(project)
    
    return result
