"""Get all tasks with a specific status."""

from typing import List, Dict, Any
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID


def get_tasks_by_status(status: str) -> "List[Dict[str, Any]]":
    """Get all tasks with a specific status."""
    return query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "property": "Status",
            "status": {"equals": status}
        },
        use_data_source=True
    )
