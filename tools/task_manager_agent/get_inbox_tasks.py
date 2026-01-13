"""Get all tasks in Inbox status."""

from typing import List, Dict, Any
from .get_tasks_by_status import get_tasks_by_status


def get_inbox_tasks() -> "List[Dict[str, Any]]":
    """Get all tasks in Inbox status."""
    return get_tasks_by_status("Inbox")
