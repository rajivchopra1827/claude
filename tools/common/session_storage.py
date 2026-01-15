"""Session storage configuration for agent memory management."""

import os
from agno.db.sqlite import SqliteDb


def get_session_storage(table_name: str = "agent_sessions") -> SqliteDb:
    """Create and return a SQLite storage instance for session management.
    
    Args:
        table_name: Name of the table to store sessions in the database
        
    Returns:
        SqliteDb instance configured for session storage
    """
    # Determine database file path
    # Use data/ directory if it exists, otherwise project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    db_file = os.path.join(data_dir, "sessions.db")
    
    return SqliteDb(db_file=db_file)
