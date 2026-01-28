"""Get all tasks in Waiting status."""

from typing import List, Dict, Any
from .get_tasks_by_status import get_tasks_by_status


def get_waiting_tasks() -> "List[Dict[str, Any]]":
    """Get all tasks in Waiting status."""
    return get_tasks_by_status("Waiting")
