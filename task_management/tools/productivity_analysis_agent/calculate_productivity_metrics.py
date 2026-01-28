"""Calculate productivity metrics from task and project data."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from collections import defaultdict


def calculate_productivity_metrics(
    tasks: "List[Dict[str, Any]]",
    period: str = "day"  # "day", "week", "month"
) -> "Dict[str, Any]":
    """Calculate productivity metrics aggregated by time period.
    
    Args:
        tasks: List of task dictionaries with properties
        period: Aggregation period ("day", "week", "month")
    
    Returns:
        Dictionary containing:
        - metrics_by_period: Metrics grouped by time period
        - overall_metrics: Overall summary metrics
        - trends: Trend indicators (improving/declining)
    """
    if not tasks:
        return {
            "metrics_by_period": {},
            "overall_metrics": {},
            "trends": {}
        }
    
    # Group tasks by period
    tasks_by_period = defaultdict(list)
    
    for task in tasks:
        completed_date = task.get("completed_date")
        created_time = task.get("created_time")
        
        # Use completed date if available, otherwise created date
        if completed_date:
            try:
                task_date = datetime.fromisoformat(completed_date).date()
            except (ValueError, AttributeError):
                continue
        elif created_time:
            try:
                task_date = datetime.fromisoformat(created_time.replace("Z", "+00:00")).date()
            except (ValueError, AttributeError):
                continue
        else:
            continue
        
        # Determine period key
        if period == "day":
            period_key = task_date.isoformat()
        elif period == "week":
            # Monday of the week
            days_since_monday = task_date.weekday()
            monday = task_date - timedelta(days=days_since_monday)
            period_key = monday.isoformat()
        elif period == "month":
            period_key = task_date.strftime("%Y-%m")
        else:
            period_key = task_date.isoformat()
        
        tasks_by_period[period_key].append(task)
    
    # Calculate metrics for each period
    metrics_by_period = {}
    period_keys_sorted = sorted(tasks_by_period.keys())
    
    for period_key in period_keys_sorted:
        period_tasks = tasks_by_period[period_key]
        completed_tasks = [t for t in period_tasks if t.get("status") == "Done"]
        
        # Calculate time to complete
        time_to_complete_days = []
        for task in completed_tasks:
            created = task.get("created_time")
            completed = task.get("completed_date")
            
            if created and completed:
                try:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    completed_dt = datetime.fromisoformat(completed)
                    days = (completed_dt.date() - created_dt.date()).days
                    if days >= 0:
                        time_to_complete_days.append(days)
                except (ValueError, AttributeError):
                    pass
        
        metrics_by_period[period_key] = {
            "total_tasks": len(period_tasks),
            "completed_tasks": len(completed_tasks),
            "completion_rate": len(completed_tasks) / len(period_tasks) if period_tasks else 0,
            "avg_time_to_complete_days": sum(time_to_complete_days) / len(time_to_complete_days) if time_to_complete_days else None,
        }
    
    # Calculate overall metrics
    all_completed = [t for t in tasks if t.get("status") == "Done"]
    all_active = [t for t in tasks if t.get("status") != "Done"]
    
    overall_time_to_complete = []
    for task in all_completed:
        created = task.get("created_time")
        completed = task.get("completed_date")
        
        if created and completed:
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                completed_dt = datetime.fromisoformat(completed)
                days = (completed_dt.date() - created_dt.date()).days
                if days >= 0:
                    overall_time_to_complete.append(days)
            except (ValueError, AttributeError):
                pass
    
    overall_metrics = {
        "total_tasks": len(tasks),
        "completed_tasks": len(all_completed),
        "active_tasks": len(all_active),
        "completion_rate": len(all_completed) / len(tasks) if tasks else 0,
        "avg_time_to_complete_days": sum(overall_time_to_complete) / len(overall_time_to_complete) if overall_time_to_complete else None,
        "min_time_to_complete_days": min(overall_time_to_complete) if overall_time_to_complete else None,
        "max_time_to_complete_days": max(overall_time_to_complete) if overall_time_to_complete else None,
    }
    
    # Calculate trends (compare last two periods)
    trends = {}
    if len(period_keys_sorted) >= 2:
        last_period = metrics_by_period[period_keys_sorted[-1]]
        prev_period = metrics_by_period[period_keys_sorted[-2]]
        
        completion_rate_change = last_period["completion_rate"] - prev_period["completion_rate"]
        completed_tasks_change = last_period["completed_tasks"] - prev_period["completed_tasks"]
        
        trends = {
            "completion_rate_trend": "improving" if completion_rate_change > 0 else "declining" if completion_rate_change < 0 else "stable",
            "completion_rate_change": completion_rate_change,
            "completed_tasks_trend": "improving" if completed_tasks_change > 0 else "declining" if completed_tasks_change < 0 else "stable",
            "completed_tasks_change": completed_tasks_change,
        }
    
    return {
        "metrics_by_period": metrics_by_period,
        "overall_metrics": overall_metrics,
        "trends": trends,
        "period": period
    }
