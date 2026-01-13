"""Get all tasks matching any of the given statuses."""

from typing import List, Dict, Any
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID


def get_tasks_by_statuses(statuses: "List[str]") -> "List[Dict[str, Any]]":
    """Get all tasks matching any of the given statuses."""
    if not statuses:
        return []
    
    filters = [
        {
            "property": "Status",
            "status": {"equals": status}
        }
        for status in statuses
    ]
    
    return query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={"or": filters},
        use_data_source=True
    )
