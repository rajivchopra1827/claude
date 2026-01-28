"""Update multiple tasks in batch."""

from typing import List, Dict, Any
from .update_task import update_task


def batch_update_tasks(updates) -> "List[Dict[str, Any]]":
    """Update multiple tasks in batch.
    
    Args:
        updates: List[Dict[str, Any]] - List of update dictionaries, each with task_id and update fields
    
    Returns:
        List[Dict[str, Any]]: List of updated task page objects
    """
    results = []
    for update in updates:
        task_id = update.pop("task_id")
        results.append(update_task(task_id, **update))
    return results
