"""Identify bottlenecks and areas where work gets stuck."""

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
            f.write(json.dumps({"location": "identify_bottlenecks.py:entry", "message": msg, "data": data or {}, "hypothesisId": hypothesis_id, "timestamp": __import__("time").time()}) + "\n")
    except: pass
# #endregion


def identify_bottlenecks(tasks: "List[Dict[str, Any]]", projects: "List[Dict[str, Any]]") -> "Dict[str, Any]":
    """Find where tasks get stuck and identify bottlenecks.
    
    Args:
        tasks: List of task dictionaries with properties
        projects: List of project dictionaries with task_metrics
    
    Returns:
        Dictionary containing:
        - waiting_tasks: Tasks stuck in Waiting status
        - overdue_tasks: Tasks past their due date
        - stalled_projects: Projects with no recent progress
        - priority_drift: Projects not aligned with priorities
        - bottlenecks_summary: Summary of all bottlenecks
    """
    # #region agent log
    _log("identify_bottlenecks called", {"tasks_type": str(type(tasks)), "tasks_len": len(tasks) if isinstance(tasks, list) else "not_list", "tasks_is_none": tasks is None, "projects_type": str(type(projects)), "projects_len": len(projects) if isinstance(projects, list) else "not_list", "projects_is_none": projects is None}, "B")
    # #endregion
    today = date.today()
    
    # Find waiting tasks
    waiting_tasks = []
    for task in tasks:
        if task.get("status") == "Waiting":
            waiting_info = {
                "title": task.get("title"),
                "waiting_on": task.get("waiting", []),
                "due_date": task.get("due_date"),
                "created_time": task.get("created_time"),
                "project_ids": task.get("project_ids", [])
            }
            
            # Calculate how long it's been waiting
            created_time = task.get("created_time")
            if created_time:
                try:
                    created_dt = datetime.fromisoformat(created_time.replace("Z", "+00:00")).date()
                    waiting_days = (today - created_dt).days
                    waiting_info["waiting_days"] = waiting_days
                except (ValueError, AttributeError):
                    waiting_info["waiting_days"] = None
            
            waiting_tasks.append(waiting_info)
    
    # Sort by waiting days (longest first)
    waiting_tasks.sort(key=lambda x: x.get("waiting_days") or 0, reverse=True)
    
    # Find overdue tasks
    overdue_tasks = []
    for task in tasks:
        if task.get("status") != "Done":
            due_date = task.get("due_date")
            if due_date:
                try:
                    due = datetime.fromisoformat(due_date).date()
                    if due < today:
                        overdue_days = (today - due).days
                        overdue_tasks.append({
                            "title": task.get("title"),
                            "due_date": due_date,
                            "overdue_days": overdue_days,
                            "status": task.get("status"),
                            "project_ids": task.get("project_ids", [])
                        })
                except (ValueError, AttributeError):
                    pass
    
    # Sort by overdue days (most overdue first)
    overdue_tasks.sort(key=lambda x: x.get("overdue_days", 0), reverse=True)
    
    # Find stalled projects (no completed tasks in last 30 days)
    stalled_projects = []
    thirty_days_ago = today - timedelta(days=30)
    
    for project in projects:
        task_metrics = project.get("task_metrics", {})
        completed_tasks_count = task_metrics.get("completed_tasks", 0)
        total_tasks = task_metrics.get("total_tasks", 0)
        
        # A project is stalled if:
        # 1. It has tasks but none completed recently
        # 2. It has a low completion rate and hasn't been updated recently
        if total_tasks > 0:
            completion_rate = task_metrics.get("completion_rate", 0)
            last_edited = project.get("last_edited_time")
            
            is_stalled = False
            if completion_rate < 0.5:  # Less than 50% complete
                if last_edited:
                    try:
                        edited_dt = datetime.fromisoformat(last_edited.replace("Z", "+00:00")).date()
                        if edited_dt < thirty_days_ago:
                            is_stalled = True
                    except (ValueError, AttributeError):
                        pass
                else:
                    is_stalled = True
            
            if is_stalled:
                stalled_projects.append({
                    "title": project.get("title"),
                    "priority": project.get("priority"),
                    "completion_rate": completion_rate,
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks_count,
                    "last_edited": last_edited
                })
    
    # Detect priority drift (P1 projects with low activity)
    priority_drift = []
    for project in projects:
        priority = project.get("priority")
        if priority == "P1":
            task_metrics = project.get("task_metrics", {})
            completion_rate = task_metrics.get("completion_rate", 0)
            total_tasks = task_metrics.get("total_tasks", 0)
            
            # P1 project with low completion rate or few tasks is a concern
            if completion_rate < 0.3 or total_tasks < 3:
                priority_drift.append({
                    "title": project.get("title"),
                    "priority": priority,
                    "completion_rate": completion_rate,
                    "total_tasks": total_tasks,
                    "issue": "Low completion rate" if completion_rate < 0.3 else "Few tasks"
                })
    
    # Create summary
    bottlenecks_summary = {
        "waiting_tasks_count": len(waiting_tasks),
        "overdue_tasks_count": len(overdue_tasks),
        "stalled_projects_count": len(stalled_projects),
        "priority_drift_count": len(priority_drift),
        "avg_waiting_days": sum(t.get("waiting_days") or 0 for t in waiting_tasks) / len(waiting_tasks) if waiting_tasks else 0,
        "avg_overdue_days": sum(t.get("overdue_days", 0) for t in overdue_tasks) / len(overdue_tasks) if overdue_tasks else 0,
    }
    
    return {
        "waiting_tasks": waiting_tasks[:10],  # Top 10 longest waiting
        "overdue_tasks": overdue_tasks[:10],  # Top 10 most overdue
        "stalled_projects": stalled_projects,
        "priority_drift": priority_drift,
        "bottlenecks_summary": bottlenecks_summary
    }
