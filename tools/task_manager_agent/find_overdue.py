"""Find overdue tasks from a list."""

from typing import List, Dict, Any
from datetime import datetime, date


def find_overdue(tasks) -> "List[Dict[str, Any]]":
    """Find overdue tasks from a list.
    
    Args:
        tasks: List[Dict[str, Any]] - List of tasks with extracted properties
    
    Returns:
        List[Dict[str, Any]]: List of overdue tasks with days_overdue added
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
