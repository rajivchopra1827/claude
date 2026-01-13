"""Get tasks with due dates in the past that aren't Done."""

from typing import List, Dict, Any
from datetime import date
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID


def get_overdue_tasks() -> "List[Dict[str, Any]]":
    """Get tasks with due dates in the past that aren't Done."""
    today = date.today().isoformat()
    
    tasks = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict={
            "and": [
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Done"}
                },
                {
                    "property": "Due",
                    "date": {"before": today}
                }
            ]
        },
        use_data_source=True
    )
    
    return tasks
