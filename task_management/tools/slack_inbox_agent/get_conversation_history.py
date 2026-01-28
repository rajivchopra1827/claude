"""Get message history for a conversation."""

import time
from typing import List, Dict, Any, Optional
from .slack_client import get_slack_client


def get_conversation_history(
    channel_id: str,
    limit: int = 100,
    oldest: Optional[str] = None,
    latest: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get message history for a conversation.
    
    Args:
        channel_id: Conversation ID (channel or DM ID)
        limit: Maximum number of messages to retrieve (default: 100)
        oldest: Only messages after this timestamp (Unix timestamp)
        latest: Only messages before this timestamp (Unix timestamp)
        
    Returns:
        List of message objects, each containing:
        - text: Message text
        - user: User ID who sent the message
        - ts: Message timestamp
        - thread_ts: Thread timestamp if in thread
        - channel: Channel ID
        - type: Message type
    """
    client = get_slack_client()
    
    try:
        all_messages = []
        cursor = None
        
        # Handle pagination for large conversation histories
        while True:
            params = {
                "channel": channel_id,
                "limit": min(limit, 200),  # Slack API max is 200 per request
            }
            
            if oldest:
                params["oldest"] = oldest
            if latest:
                params["latest"] = latest
            if cursor:
                params["cursor"] = cursor
            
            response = client.conversations_history(**params)
            
            if not response["ok"]:
                raise Exception(f"Slack API error: {response.get('error', 'unknown')}")
            
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
        
        return user_messages
        
    except Exception as e:
        raise Exception(f"Failed to get conversation history: {str(e)}")


def get_unread_messages_from_conversation(
    channel_id: str,
    last_read_ts: Optional[float] = None
) -> List[Dict[str, Any]]:
    """Get unread messages from a specific conversation.
    
    Args:
        channel_id: Conversation ID
        last_read_ts: Last read timestamp as float (Unix timestamp)
        
    Returns:
        List of unread message objects
    """
    if last_read_ts:
        # Convert float timestamp to string format Slack expects
        oldest_ts = str(last_read_ts)
        # Get messages after last read timestamp
        messages = get_conversation_history(
            channel_id=channel_id,
            limit=200,
            oldest=oldest_ts
        )
    else:
        # Get recent messages (assume last 50 are potentially unread)
        messages = get_conversation_history(
            channel_id=channel_id,
            limit=50
        )
    
    return messages


def get_recent_messages_from_conversation(
    channel_id: str,
    hours: int = 24,
    limit: int = 200
) -> List[Dict[str, Any]]:
    """Get messages from a conversation from the last N hours.
    
    Args:
        channel_id: Conversation ID
        hours: Number of hours to look back (default: 24)
        limit: Maximum number of messages to retrieve (default: 200)
        
    Returns:
        List of message objects from the last N hours
    """
    # Calculate timestamp for N hours ago
    hours_ago_ts = time.time() - (hours * 60 * 60)
    oldest_ts = str(hours_ago_ts)
    
    return get_conversation_history(
        channel_id=channel_id,
        limit=limit,
        oldest=oldest_ts
    )


def get_unread_and_recent_messages(
    channel_id: str,
    last_read_ts: Optional[float] = None,
    include_recent_hours: int = 24,
    limit: int = 200
) -> Dict[str, Any]:
    """Get both unread messages and recent messages (last N hours) from a conversation.
    
    This function ensures you get all messages you'd see if you opened Slack:
    - Unread messages (if last_read_ts is provided)
    - Recent messages from the last N hours (even if read)
    
    Args:
        channel_id: Conversation ID
        last_read_ts: Last read timestamp as float (Unix timestamp)
        include_recent_hours: Number of hours to include for recent activity (default: 24)
        limit: Maximum number of messages to retrieve per category (default: 200)
        
    Returns:
        Dictionary with:
        - unread: List of unread messages (if last_read_ts provided)
        - recent: List of recent messages from last N hours
        - all: Combined list of all unique messages (deduplicated by ts)
    """
    unread_messages = []
    recent_messages = []
    
    # Get unread messages if last_read_ts is provided
    if last_read_ts:
        unread_messages = get_unread_messages_from_conversation(
            channel_id=channel_id,
            last_read_ts=last_read_ts
        )
    
    # Get recent messages from last N hours
    recent_messages = get_recent_messages_from_conversation(
        channel_id=channel_id,
        hours=include_recent_hours,
        limit=limit
    )
    
    # Combine and deduplicate messages by ts (timestamp)
    all_messages_dict = {}
    
    # Add unread messages
    for msg in unread_messages:
        ts = msg.get("ts")
        if ts:
            all_messages_dict[ts] = msg
    
    # Add recent messages (will overwrite duplicates, keeping the same message)
    for msg in recent_messages:
        ts = msg.get("ts")
        if ts:
            all_messages_dict[ts] = msg
    
    # Convert back to list, sorted by timestamp (newest first)
    all_messages = sorted(
        all_messages_dict.values(),
        key=lambda m: float(m.get("ts", 0)),
        reverse=True
    )
    
    return {
        "unread": unread_messages,
        "recent": recent_messages,
        "all": all_messages
    }
