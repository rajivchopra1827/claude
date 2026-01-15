"""Analyze productivity patterns over time."""

from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from collections import defaultdict
import json
import os

# #region agent log
log_path = "/Users/rajivchopra/Claude/.cursor/debug.log"
def _log(msg, data=None, hypothesis_id=None):
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({"location": "analyze_time_patterns.py:entry", "message": msg, "data": data or {}, "hypothesisId": hypothesis_id, "timestamp": __import__("time").time()}) + "\n")
    except: pass
# #endregion


def analyze_time_patterns(tasks: "List[Dict[str, Any]]") -> "Dict[str, Any]":
    """Identify patterns in completion dates and productivity trends.
    
    Args:
        tasks: List of task dictionaries with properties
    
    Returns:
        Dictionary containing:
        - day_of_week_patterns: Completion patterns by day of week
        - weekly_trends: Week-over-week trends
        - monthly_trends: Month-over-month trends
        - completion_patterns: General completion patterns
    """
    # #region agent log
    _log("analyze_time_patterns called", {"tasks_type": str(type(tasks)), "tasks_len": len(tasks) if isinstance(tasks, list) else "not_list", "tasks_is_none": tasks is None}, "A")
    # #endregion
    completed_tasks = [t for t in tasks if t.get("status") == "Done" and t.get("completed_date")]
    
    if not completed_tasks:
        return {
            "day_of_week_patterns": {},
            "weekly_trends": {},
            "monthly_trends": {},
            "completion_patterns": {}
        }
    
    # Analyze day of week patterns
    day_of_week_counts = defaultdict(int)
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for task in completed_tasks:
        completed_date = task.get("completed_date")
        if completed_date:
            try:
                task_date = datetime.fromisoformat(completed_date).date()
                day_name = day_names[task_date.weekday()]
                day_of_week_counts[day_name] += 1
            except (ValueError, AttributeError):
                pass
    
    # Analyze weekly trends
    weekly_counts = defaultdict(int)
    for task in completed_tasks:
        completed_date = task.get("completed_date")
        if completed_date:
            try:
                task_date = datetime.fromisoformat(completed_date).date()
                # Monday of the week
                days_since_monday = task_date.weekday()
                monday = task_date - timedelta(days=days_since_monday)
                week_key = monday.isoformat()
                weekly_counts[week_key] += 1
            except (ValueError, AttributeError):
                pass
    
    # Analyze monthly trends
    monthly_counts = defaultdict(int)
    for task in completed_tasks:
        completed_date = task.get("completed_date")
        if completed_date:
            try:
                task_date = datetime.fromisoformat(completed_date).date()
                month_key = task_date.strftime("%Y-%m")
                monthly_counts[month_key] += 1
            except (ValueError, AttributeError):
                pass
    
    # Find most productive day/week/month
    most_productive_day = max(day_of_week_counts.items(), key=lambda x: x[1]) if day_of_week_counts else None
    most_productive_week = max(weekly_counts.items(), key=lambda x: x[1]) if weekly_counts else None
    most_productive_month = max(monthly_counts.items(), key=lambda x: x[1]) if monthly_counts else None
    
    # Calculate trends
    weekly_trend = None
    if len(weekly_counts) >= 2:
        sorted_weeks = sorted(weekly_counts.keys())
        recent_weeks = sorted_weeks[-2:]
        recent_count = weekly_counts[recent_weeks[-1]]
        prev_count = weekly_counts[recent_weeks[-2]]
        
        if recent_count > prev_count:
            weekly_trend = "improving"
        elif recent_count < prev_count:
            weekly_trend = "declining"
        else:
            weekly_trend = "stable"
    
    monthly_trend = None
    if len(monthly_counts) >= 2:
        sorted_months = sorted(monthly_counts.keys())
        recent_months = sorted_months[-2:]
        recent_count = monthly_counts[recent_months[-1]]
        prev_count = monthly_counts[recent_months[-2]]
        
        if recent_count > prev_count:
            monthly_trend = "improving"
        elif recent_count < prev_count:
            monthly_trend = "declining"
        else:
            monthly_trend = "stable"
    
    return {
        "day_of_week_patterns": dict(day_of_week_counts),
        "most_productive_day": most_productive_day[0] if most_productive_day else None,
        "weekly_trends": {
            "weekly_counts": dict(weekly_counts),
            "most_productive_week": most_productive_week[0] if most_productive_week else None,
            "trend": weekly_trend
        },
        "monthly_trends": {
            "monthly_counts": dict(monthly_counts),
            "most_productive_month": most_productive_month[0] if most_productive_month else None,
            "trend": monthly_trend
        },
        "completion_patterns": {
            "total_completed": len(completed_tasks),
            "avg_per_day": len(completed_tasks) / max(len(day_of_week_counts), 1) if day_of_week_counts else 0,
            "avg_per_week": len(completed_tasks) / max(len(weekly_counts), 1) if weekly_counts else 0,
            "avg_per_month": len(completed_tasks) / max(len(monthly_counts), 1) if monthly_counts else 0,
        }
    }
