"""Track processed Slack messages to avoid duplicates."""

import os
import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


def get_db_path() -> str:
    """Get the path to the SQLite database file."""
    # Use same location as session storage
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    return os.path.join(data_dir, "sessions.db")


def init_message_tracker_table():
    """Initialize the processed_slack_messages table if it doesn't exist."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_slack_messages (
            message_id TEXT PRIMARY KEY,
            channel_id TEXT NOT NULL,
            message_ts TEXT NOT NULL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_notion_id TEXT,
            created_notion_type TEXT
        )
    """)
    
    # Create index on channel_id and message_ts for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_channel_ts 
        ON processed_slack_messages(channel_id, message_ts)
    """)
    
    conn.commit()
    conn.close()


def is_message_processed(message_id: str) -> bool:
    """Check if a message has already been processed.
    
    Args:
        message_id: Unique message identifier (channel_id + message_ts)
        
    Returns:
        True if message has been processed, False otherwise
    """
    init_message_tracker_table()
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM processed_slack_messages WHERE message_id = ?",
        (message_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None


def mark_message_processed(
    message_id: str,
    channel_id: str,
    message_ts: str,
    created_notion_id: Optional[str] = None,
    created_notion_type: Optional[str] = None
):
    """Mark a message as processed.
    
    Args:
        message_id: Unique message identifier (channel_id + message_ts)
        channel_id: Slack channel/conversation ID
        message_ts: Message timestamp from Slack
        created_notion_id: Notion page ID if a Notion entry was created
        created_notion_type: Type of Notion entry (task, resource, idea)
    """
    init_message_tracker_table()
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO processed_slack_messages 
        (message_id, channel_id, message_ts, processed_at, created_notion_id, created_notion_type)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
    """, (message_id, channel_id, message_ts, created_notion_id, created_notion_type))
    
    conn.commit()
    conn.close()


def get_message_id(channel_id: str, message_ts: str) -> str:
    """Generate a unique message ID from channel_id and message_ts.
    
    Args:
        channel_id: Slack channel/conversation ID
        message_ts: Message timestamp from Slack
        
    Returns:
        Unique message identifier
    """
    return f"{channel_id}:{message_ts}"


def get_processed_messages_by_date_range(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """Get all processed messages within a date range.
    
    Args:
        start_date: Start of date range (default: None, no lower limit)
        end_date: End of date range (default: None, no upper limit)
        
    Returns:
        List of processed message records
    """
    init_message_tracker_table()
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT * FROM processed_slack_messages WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND processed_at >= ?"
        params.append(start_date.isoformat())
    
    if end_date:
        query += " AND processed_at <= ?"
        params.append(end_date.isoformat())
    
    query += " ORDER BY processed_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Get column names
    columns = [description[0] for description in cursor.description]
    
    # Convert to list of dictionaries
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    
    return results


def clear_processed_messages(older_than_days: Optional[int] = None):
    """Clear processed message records.
    
    Args:
        older_than_days: If provided, only clear messages older than N days.
                        If None, clear all records.
    """
    init_message_tracker_table()
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if older_than_days:
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        cursor.execute(
            "DELETE FROM processed_slack_messages WHERE processed_at < ?",
            (cutoff_date.isoformat(),)
        )
    else:
        cursor.execute("DELETE FROM processed_slack_messages")
    
    conn.commit()
    conn.close()
