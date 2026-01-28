"""Get task history with date filtering and completion data."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from task_management.tools.task_manager_agent.extract_task_properties import extract_task_properties
import json
import os

# #region agent log
log_path = "/Users/rajivchopra/Claude/.cursor/debug.log"
def _log(msg, data=None, hypothesis_id=None):
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({"location": "get_task_history.py", "message": msg, "data": data or {}, "hypothesisId": hypothesis_id, "timestamp": __import__("time").time()}) + "\n")
    except: pass
# #endregion


def parse_date_range(date_str: Optional[str] = None) -> "tuple[Optional[str], Optional[str]]":
    """Parse natural date expressions into start and end dates.
    
    Args:
        date_str: Natural date expression like "last week", "this month", "last 30 days", "2024-01-01"
    
    Returns:
        Tuple of (start_date, end_date) in ISO format, or (None, None) for all time
    """
    if not date_str:
        return None, None
    
    today = date.today()
    date_str_lower = date_str.lower().strip()
    
    # Handle "last N days"
    if date_str_lower.startswith("last ") and " day" in date_str_lower:
        try:
            days = int(date_str_lower.split("last ")[1].split(" day")[0])
            start_date = (today - timedelta(days=days)).isoformat()
            end_date = today.isoformat()
            return start_date, end_date
        except (ValueError, IndexError):
            pass
    
    # Handle "this week"
    if date_str_lower == "this week":
        # Monday of this week
        days_since_monday = today.weekday()
        start_date = (today - timedelta(days=days_since_monday)).isoformat()
        end_date = today.isoformat()
        return start_date, end_date
    
    # Handle "last week"
    if date_str_lower == "last week":
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday + 7)
        start_date = last_monday.isoformat()
        end_date = (last_monday + timedelta(days=6)).isoformat()
        return start_date, end_date
    
    # Handle "this month"
    if date_str_lower == "this month":
        start_date = today.replace(day=1).isoformat()
        end_date = today.isoformat()
        return start_date, end_date
    
    # Handle "last month"
    if date_str_lower == "last month":
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1).isoformat()
        end_date = last_day_last_month.isoformat()
        return start_date, end_date
    
    # Handle ISO date format (YYYY-MM-DD)
    try:
        parsed_date = datetime.fromisoformat(date_str).date()
        return parsed_date.isoformat(), parsed_date.isoformat()
    except ValueError:
        pass
    
    # If we can't parse it, return None (all time)
    return None, None


def get_task_history(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date_range: Optional[str] = None,
    include_completed: bool = True,
    include_active: bool = True
) -> "Dict[str, Any]":
    """Get task history with filtering by date range.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        date_range: Natural date expression (e.g., "last week", "this month", "last 30 days")
                   If provided, overrides start_date and end_date
        include_completed: Include completed tasks
        include_active: Include active (non-completed) tasks
    
    Returns:
        Dictionary containing:
        - tasks: List of task dictionaries with properties
        - summary: Summary statistics
        - date_range: Actual date range used
    """
    # Parse date range if provided
    if date_range:
        parsed_start, parsed_end = parse_date_range(date_range)
        if parsed_start:
            start_date = parsed_start
        if parsed_end:
            end_date = parsed_end
    
    # Build filter
    filter_conditions = []
    
    # Status filter
    if include_completed and include_active:
        # Include all tasks
        pass
    elif include_completed:
        filter_conditions.append({
            "property": "Status",
            "status": {"equals": "Done"}
        })
    elif include_active:
        filter_conditions.append({
            "property": "Status",
            "status": {"does_not_equal": "Done"}
        })
    
    # Date filters - filter by created_time or completed_date
    if start_date or end_date:
        date_filters = []
        
        if start_date:
            # Tasks created on or after start_date, or completed on or after start_date
            date_filters.append({
                "or": [
                    {
                        "property": "Completed",
                        "date": {"on_or_after": start_date}
                    },
                    {
                        "property": "Completed",
                        "date": {"is_empty": True}
                    }
                ]
            })
        
        if end_date:
            # Tasks created on or before end_date, or completed on or before end_date
            date_filters.append({
                "or": [
                    {
                        "property": "Completed",
                        "date": {"on_or_before": end_date}
                    },
                    {
                        "property": "Completed",
                        "date": {"is_empty": True}
                    }
                ]
            })
        
        if date_filters:
            filter_conditions.extend(date_filters)
    
    # Build final filter
    filter_dict = None
    if filter_conditions:
        if len(filter_conditions) == 1:
            filter_dict = filter_conditions[0]
        else:
            filter_dict = {"and": filter_conditions}
    
    # #region agent log
    _log("get_task_history called", {"start_date": start_date, "end_date": end_date, "date_range": date_range, "include_completed": include_completed, "include_active": include_active}, "C")
    # #endregion
    
    # Query tasks
    tasks_raw = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict=filter_dict,
        use_data_source=True
    )
    
    # #region agent log
    _log("tasks_raw fetched", {"count": len(tasks_raw)}, "C")
    # #endregion
    
    # Extract properties
    tasks = []
    for task in tasks_raw:
        task_props = extract_task_properties(task)
        
        # Filter by date range on created_time if needed
        if start_date or end_date:
            created_time = task_props.get("created_time")
            if created_time:
                created_date = datetime.fromisoformat(created_time.replace("Z", "+00:00")).date()
                
                if start_date and created_date < datetime.fromisoformat(start_date).date():
                    continue
                if end_date and created_date > datetime.fromisoformat(end_date).date():
                    continue
        
        tasks.append(task_props)
    
    # Calculate summary statistics
    completed_tasks = [t for t in tasks if t.get("status") == "Done"]
    active_tasks = [t for t in tasks if t.get("status") != "Done"]
    
    # Calculate time to complete for completed tasks
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
    
    summary = {
        "total_tasks": len(tasks),
        "completed_tasks": len(completed_tasks),
        "active_tasks": len(active_tasks),
        "completion_rate": len(completed_tasks) / len(tasks) if tasks else 0,
        "avg_time_to_complete_days": sum(time_to_complete_days) / len(time_to_complete_days) if time_to_complete_days else None,
        "min_time_to_complete_days": min(time_to_complete_days) if time_to_complete_days else None,
        "max_time_to_complete_days": max(time_to_complete_days) if time_to_complete_days else None,
    }
    
    return {
        "tasks": tasks,
        "summary": summary,
        "date_range": {
            "start": start_date,
            "end": end_date,
            "date_range_str": date_range
        }
    }
