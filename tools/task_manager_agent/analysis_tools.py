"""Analysis tools for Task Manager Agent - analyzing task priorities and patterns."""

from typing import List, Dict, Any
from datetime import datetime, date


def analyze_priorities(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze task priorities based on due dates, projects, and status.
    
    Args:
        tasks: List of tasks with extracted properties
    
    Returns:
        Dictionary with priority analysis and recommendations
    """
    today = date.today()
    
    # Sort by due date (soonest first)
    tasks_with_due = [t for t in tasks if t.get("due_date")]
    tasks_without_due = [t for t in tasks if not t.get("due_date")]
    
    # Sort tasks with due dates
    tasks_with_due.sort(key=lambda x: x.get("due_date", ""))
    
    # Categorize by urgency
    urgent = []  # Due today or tomorrow
    soon = []    # Due in next 3 days
    later = []   # Due later
    
    for task in tasks_with_due:
        due_str = task.get("due_date")
        if due_str:
            try:
                due_date = datetime.fromisoformat(due_str.split("T")[0]).date()
                days_until = (due_date - today).days
                
                if days_until <= 1:
                    urgent.append(task)
                elif days_until <= 3:
                    soon.append(task)
                else:
                    later.append(task)
            except:
                later.append(task)
    
    return {
        "urgent": urgent,
        "soon": soon,
        "later": later,
        "no_due_date": tasks_without_due,
        "total": len(tasks)
    }


def find_overdue(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find overdue tasks from a list.
    
    Args:
        tasks: List of tasks with extracted properties
    
    Returns:
        List of overdue tasks with days_overdue added
    """
    today = date.today()
    overdue = []
    
    for task in tasks:
        due_str = task.get("due_date")
        if due_str:
            try:
                due_date = datetime.fromisoformat(due_str.split("T")[0]).date()
                if due_date < today:
                    days_overdue = (today - due_date).days
                    task_copy = task.copy()
                    task_copy["days_overdue"] = days_overdue
                    overdue.append(task_copy)
            except:
                pass
    
    # Sort by days overdue (most overdue first)
    overdue.sort(key=lambda x: x.get("days_overdue", 0), reverse=True)
    
    return overdue


def calculate_waiting_duration(task: Dict[str, Any]) -> int:
    """Calculate how many days a task has been waiting.
    
    Args:
        task: Task with extracted properties (needs created_time)
    
    Returns:
        Number of days waiting
    """
    created_str = task.get("created_time")
    if not created_str:
        return 0
    
    try:
        created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        today = datetime.now(created.tzinfo)
        days = (today - created).days
        return max(0, days)
    except:
        return 0
