"""Extract rich content from Slack messages (files, reactions, mentions, etc.)."""

import re
from typing import List, Dict, Any, Optional


def extract_files(message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract file information from a message.
    
    Args:
        message: Message object from Slack API
        
    Returns:
        List of file objects, each containing:
        - id: File ID
        - name: File name
        - url_private: Private URL to download file
        - mimetype: MIME type
        - size: File size in bytes
        - title: File title
    """
    files = message.get("files", [])
    
    extracted = []
    for file in files:
        extracted.append({
            "id": file.get("id"),
            "name": file.get("name"),
            "url_private": file.get("url_private"),
            "mimetype": file.get("mimetype"),
            "size": file.get("size"),
            "title": file.get("title"),
            "filetype": file.get("filetype"),
        })
    
    return extracted


def extract_reactions(message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract reaction information from a message.
    
    Args:
        message: Message object from Slack API
        
    Returns:
        List of reaction objects, each containing:
        - name: Reaction emoji name
        - count: Number of users who reacted
        - users: List of user IDs who reacted
    """
    reactions = message.get("reactions", [])
    
    extracted = []
    for reaction in reactions:
        extracted.append({
            "name": reaction.get("name"),
            "count": reaction.get("count", 0),
            "users": reaction.get("users", []),
        })
    
    return extracted


def extract_mentions(message_text: str) -> List[str]:
    """Extract user mentions from message text.
    
    Args:
        message_text: Message text content
        
    Returns:
        List of user IDs mentioned (e.g., ["U123456", "U789012"])
    """
    # Slack mentions are in format <@U123456> or <@U123456|username>
    pattern = r'<@(U[A-Z0-9]+)(?:\|[^>]+)?>'
    matches = re.findall(pattern, message_text)
    
    # Return unique user IDs
    return list(set(matches))


def extract_channel_references(message_text: str) -> List[str]:
    """Extract channel references from message text.
    
    Args:
        message_text: Message text content
        
    Returns:
        List of channel IDs referenced (e.g., ["C123456", "C789012"])
    """
    # Slack channel references are in format <#C123456|channel-name>
    pattern = r'<#(C[A-Z0-9]+)(?:\|[^>]+)?>'
    matches = re.findall(pattern, message_text)
    
    # Return unique channel IDs
    return list(set(matches))


def extract_links(message_text: str) -> List[str]:
    """Extract URLs from message text.
    
    Args:
        message_text: Message text content
        
    Returns:
        List of URLs found in the message
    """
    # Match URLs (http, https, or slack://)
    pattern = r'(https?://[^\s<>"{}|\\^`\[\]]+|slack://[^\s<>"{}|\\^`\[\]]+)'
    matches = re.findall(pattern, message_text)
    
    return matches


def extract_rich_content(message: Dict[str, Any]) -> Dict[str, Any]:
    """Extract all rich content from a Slack message.
    
    Args:
        message: Message object from Slack API
        
    Returns:
        Dictionary containing:
        - files: List of file objects
        - reactions: List of reaction objects
        - mentions: List of user IDs mentioned
        - channel_references: List of channel IDs referenced
        - links: List of URLs found in message text
    """
    message_text = message.get("text", "")
    
    return {
        "files": extract_files(message),
        "reactions": extract_reactions(message),
        "mentions": extract_mentions(message_text),
        "channel_references": extract_channel_references(message_text),
        "links": extract_links(message_text),
    }


def format_rich_content_summary(rich_content: Dict[str, Any]) -> str:
    """Format rich content as a human-readable summary string.
    
    Args:
        rich_content: Rich content dictionary from extract_rich_content()
        
    Returns:
        Formatted string summarizing the rich content
    """
    parts = []
    
    files = rich_content.get("files", [])
    if files:
        file_names = [f.get("name", "Unknown") for f in files]
        parts.append(f"📎 Files: {', '.join(file_names)}")
    
    reactions = rich_content.get("reactions", [])
    if reactions:
        reaction_names = [f":{r.get('name')}: ({r.get('count')})" for r in reactions]
        parts.append(f"👍 Reactions: {', '.join(reaction_names)}")
    
    mentions = rich_content.get("mentions", [])
    if mentions:
        parts.append(f"@ Mentions: {len(mentions)} user(s)")
    
    channel_refs = rich_content.get("channel_references", [])
    if channel_refs:
        parts.append(f"# Channels: {len(channel_refs)} channel(s)")
    
    links = rich_content.get("links", [])
    if links:
        parts.append(f"🔗 Links: {len(links)} URL(s)")
    
    if parts:
        return "\n".join(parts)
    
    return ""
