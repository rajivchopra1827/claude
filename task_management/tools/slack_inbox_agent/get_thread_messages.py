"""Get thread messages from Slack conversations."""

from typing import List, Dict, Any, Optional
from .slack_client import get_slack_client


def get_thread_messages(
    channel_id: str,
    thread_ts: str,
    limit: int = 1000
) -> List[Dict[str, Any]]:
    """Get all messages in a thread.
    
    Args:
        channel_id: Conversation ID
        thread_ts: Thread timestamp (ts of the parent message)
        limit: Maximum number of messages to retrieve (default: 1000)
        
    Returns:
        List of message objects in the thread, including the parent message.
        Messages are sorted by timestamp (oldest first).
    """
    client = get_slack_client()
    
    try:
        all_messages = []
        cursor = None
        
        # Handle pagination for large threads
        while True:
            params = {
                "channel": channel_id,
                "ts": thread_ts,
                "limit": min(limit, 1000),  # Slack API max is 1000 per request
            }
            
            if cursor:
                params["cursor"] = cursor
            
            response = client.conversations_replies(**params)
            
            if not response["ok"]:
                error = response.get("error", "unknown")
                # thread_not_found is okay - means no thread exists
                if error == "thread_not_found":
                    return []
                raise Exception(f"Slack API error: {error}")
            
            messages = response.get("messages", [])
            all_messages.extend(messages)
            
            # Check if there are more pages
            response_metadata = response.get("response_metadata", {})
            cursor = response_metadata.get("next_cursor")
            
            # Stop if no more pages or we've reached the limit
            if not cursor or len(all_messages) >= limit:
                break
        
        # Filter out bot messages and system messages
        user_messages = [
            msg for msg in all_messages[:limit]
            if msg.get("type") == "message" and not msg.get("bot_id")
        ]
        
        # Sort by timestamp (oldest first)
        user_messages.sort(key=lambda m: float(m.get("ts", 0)))
        
        return user_messages
        
    except Exception as e:
        raise Exception(f"Failed to get thread messages: {str(e)}")


def get_thread_replies(
    channel_id: str,
    thread_ts: str,
    limit: int = 1000
) -> List[Dict[str, Any]]:
    """Get only the reply messages in a thread (excludes the parent message).
    
    Args:
        channel_id: Conversation ID
        thread_ts: Thread timestamp (ts of the parent message)
        limit: Maximum number of messages to retrieve (default: 1000)
        
    Returns:
        List of reply message objects (excluding parent), sorted by timestamp.
    """
    all_messages = get_thread_messages(channel_id, thread_ts, limit)
    
    # Filter out the parent message (ts == thread_ts)
    replies = [
        msg for msg in all_messages
        if msg.get("ts") != thread_ts
    ]
    
    return replies


def has_thread_replies(message: Dict[str, Any]) -> bool:
    """Check if a message has thread replies.
    
    Args:
        message: Message object from Slack API
        
    Returns:
        True if message has replies, False otherwise
    """
    # Check for reply_count field
    reply_count = message.get("reply_count", 0)
    if reply_count and reply_count > 0:
        return True
    
    # Check for thread_ts field (indicates this is a reply)
    thread_ts = message.get("thread_ts")
    if thread_ts and thread_ts != message.get("ts"):
        return True
    
    return False


def get_thread_ts(message: Dict[str, Any]) -> Optional[str]:
    """Get the thread timestamp from a message.
    
    For parent messages, this returns the message's own ts.
    For reply messages, this returns the thread_ts.
    
    Args:
        message: Message object from Slack API
        
    Returns:
        Thread timestamp string, or None if message is not in a thread
    """
    # If message has thread_ts, use it (this is a reply)
    thread_ts = message.get("thread_ts")
    if thread_ts:
        return thread_ts
    
    # If message has reply_count > 0, it's a parent message
    # Use the message's own ts as the thread_ts
    reply_count = message.get("reply_count", 0)
    if reply_count and reply_count > 0:
        return message.get("ts")
    
    return None
