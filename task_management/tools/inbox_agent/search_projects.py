"""Search for projects by name."""

from typing import List, Dict, Any, Optional
from tools.common import query_database_complete, PROJECTS_DATA_SOURCE_ID


def search_projects(query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for projects by name.
    
    Args:
        query: Search query (optional)
    
    Returns:
        List of matching project pages
    """
    if query:
        return query_database_complete(
            PROJECTS_DATA_SOURCE_ID,
            filter_dict={
                "property": "Name",
                "title": {"contains": query}
            },
            use_data_source=True
        )
    else:
        return query_database_complete(PROJECTS_DATA_SOURCE_ID, use_data_source=True)
