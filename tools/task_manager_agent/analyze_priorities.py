"""Analyze task priorities based on due dates, projects, and status."""

from typing import List, Dict, Any
from datetime import datetime, date


def analyze_priorities(tasks) -> "Dict[str, Any]":
    """Analyze task priorities based on due dates, projects, and status.
    
    Args:
        tasks: List[Dict[str, Any]] - List of tasks with extracted properties
    
    Returns:
        Dict[str, Any]: Dictionary with priority analysis and recommendations
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
