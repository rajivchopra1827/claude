"""Query tasks by title (for searching/finding tasks)."""

from typing import List, Dict, Any
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
from .extract_task_properties import extract_task_properties


def query_tasks_by_title(title_query: str) -> "List[Dict[str, Any]]":
    """Query tasks by title (for searching/finding tasks).
    
    Args:
        title_query: Search query for task title
    
    Returns:
        List of matching tasks with extracted properties
    """
    tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Task",
            "title": {"contains": title_query}
        },
        use_data_source=True
    )
    
    return [extract_task_properties(task) for task in tasks]
