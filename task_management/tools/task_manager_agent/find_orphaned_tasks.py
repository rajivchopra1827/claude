"""Find tasks without projects (orphaned tasks)."""

from typing import Dict, Any, List
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties


def find_orphaned_tasks() -> "Dict[str, Any]":
    """Find tasks that are not Done and have no project assigned.
    
    Groups by status to help identify patterns.
    
    Returns:
        Dict with orphaned tasks grouped by status
    """
    # Get all tasks that are not Done
    all_task_pages = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"does_not_equal": "Done"}
        },
        use_data_source=True
    )
    
    all_tasks = [extract_task_properties(t) for t in all_task_pages]
    
    # Filter tasks with no project_ids
    orphaned_tasks = [t for t in all_tasks if not t.get("project_ids")]
    
    # Group by status
    by_status = {}
    
    for task in orphaned_tasks:
        status = task.get("status", "Unknown")
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(task)
    
    # Count by status
    status_counts = {status: len(tasks) for status, tasks in by_status.items()}
    
    # Generate recommendations
    recommendations = []
    
    if orphaned_tasks:
        # Check if any orphaned tasks might belong to projects based on keywords
        # This is a simple heuristic - could be enhanced
        inbox_orphaned = [t for t in orphaned_tasks if t.get("status") == "Inbox"]
        if inbox_orphaned:
            recommendations.append({
                "type": "link_inbox_tasks",
                "message": f"{len(inbox_orphaned)} orphaned task(s) in Inbox - consider linking to projects during triage",
                "count": len(inbox_orphaned)
            })
        
        backlog_orphaned = [t for t in orphaned_tasks if t.get("status") == "Backlog"]
        if backlog_orphaned:
            recommendations.append({
                "type": "review_backlog_tasks",
                "message": f"{len(backlog_orphaned)} orphaned task(s) in Backlog - review if they need projects",
                "count": len(backlog_orphaned)
            })
        
        this_week_orphaned = [t for t in orphaned_tasks if t.get("status") == "This Week"]
        if this_week_orphaned:
            recommendations.append({
                "type": "link_this_week_tasks",
                "message": f"{len(this_week_orphaned)} orphaned task(s) in This Week - should be linked to projects",
                "count": len(this_week_orphaned),
                "severity": "high"
            })
        
        top_priority_orphaned = [t for t in orphaned_tasks if t.get("status") == "Top Priority"]
        if top_priority_orphaned:
            recommendations.append({
                "type": "link_top_priority_tasks",
                "message": f"{len(top_priority_orphaned)} orphaned task(s) in Top Priority - should be linked to projects",
                "count": len(top_priority_orphaned),
                "severity": "high"
            })
    
    return {
        "total_orphaned": len(orphaned_tasks),
        "tasks": orphaned_tasks,
        "by_status": by_status,
        "status_counts": status_counts,
        "recommendations": recommendations
    }
