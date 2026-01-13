"""Calculate how many days a task has been waiting."""

from typing import Dict, Any
from datetime import datetime


def calculate_waiting_duration(task) -> int:
    """Calculate how many days a task has been waiting.
    
    Args:
        task: Dict[str, Any] - Task with extracted properties (needs created_time)
    
    Returns:
        int: Number of days waiting
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
