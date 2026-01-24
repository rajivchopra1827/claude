"""Process unread Slack messages and create Notion entries."""

from typing import List, Dict, Any, Optional
from .get_unread_messages import get_unread_messages
from .get_conversation_history import get_unread_and_recent_messages
from .get_thread_messages import get_thread_replies, has_thread_replies, get_thread_ts
from .classify_slack_message import classify_slack_message
from .extract_rich_content import extract_rich_content, format_rich_content_summary
from .message_tracker import (
    is_message_processed,
    mark_message_processed,
    get_message_id
)
from .slack_client import get_slack_client
from tools.inbox_agent import (
    create_task,
    create_resource,
    create_idea,
    search_projects,
    fetch_url_metadata,
    infer_resource_type,
)


def _get_user_name(client, user_id: Optional[str]) -> Optional[str]:
    """Get user name from Slack client.
    
    Args:
        client: Slack client instance
        user_id: User ID to look up
        
    Returns:
        User name as string, or None if not found
    """
    if not user_id:
        return None
    
    try:
        user_info = client.users_info(user=user_id)
        if user_info.get("ok"):
            return user_info["user"].get("real_name") or user_info["user"].get("name")
    except:
        pass
    
    return None


def _build_enhanced_text(message_text: str, rich_content_summary: Optional[str]) -> str:
    """Build enhanced message text with rich content.
    
    Args:
        message_text: Original message text
        rich_content_summary: Optional rich content summary
        
    Returns:
        Enhanced text with rich content appended if available
    """
    if rich_content_summary:
        return f"{message_text}\n\n{rich_content_summary}"
    return message_text


def _log_error_to_debug_file(error_msg: str, location: str, data: Dict[str, Any]) -> None:
    """Log error to debug log file.
    
    Args:
        error_msg: Error message
        location: Location identifier (e.g., "process_slack_messages.py:230")
        data: Additional data to log
    """
    import json
    import time
    try:
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "B",
                "location": location,
                "message": "message processing error",
                "data": {"error": error_msg, **data},
                "timestamp": int(time.time() * 1000)
            }) + '\n')
    except:
        pass


def _process_thread_reply(
    reply: Dict[str, Any],
    client,
    channel_id: str,
    channel_name: Optional[str],
    is_dm: bool,
    reprocess: bool
) -> Optional[Dict[str, Any]]:
    """Process a single thread reply message.
    
    Args:
        reply: Reply message dict
        client: Slack client instance
        channel_id: Channel ID
        channel_name: Channel name
        is_dm: Whether this is a DM
        reprocess: Whether to reprocess already-processed messages
        
    Returns:
        Dict with created item info if successful, None if skipped/failed
    """
    reply_ts = reply.get("ts")
    if not reply_ts:
        return None
    
    reply_id = get_message_id(channel_id, reply_ts)
    if not reprocess and is_message_processed(reply_id):
        return {"skipped": True}
    
    reply_text = reply.get("text", "")
    if not reply_text or reply_text.strip() == "":
        mark_message_processed(reply_id, channel_id, reply_ts)
        return {"skipped": True}
    
    # Get reply user info
    reply_user_id = reply.get("user")
    reply_user_name = _get_user_name(client, reply_user_id)
    
    # Extract rich content from reply
    reply_rich_content = extract_rich_content(reply)
    reply_rich_summary = format_rich_content_summary(reply_rich_content)
    
    # Build reply text with context
    reply_with_context = f"Thread reply in {channel_name}:\n\n{reply_text}"
    if reply_rich_summary:
        reply_with_context += f"\n\n{reply_rich_summary}"
    
    # Create Notion entry for reply (simplified - just create as idea for now)
    try:
        reply_title = reply_text[:100]
        if len(reply_text) > 100:
            reply_title = reply_text[:97] + "..."
        
        reply_idea = create_idea(
            title=f"Slack Thread: {reply_title}",
            idea_type="Pattern",
            content=reply_with_context,
            status="Inbox",
            source=f"Slack Thread - {channel_name}"
        )
        
        mark_message_processed(
            reply_id,
            channel_id,
            reply_ts,
            created_notion_id=reply_idea["id"],
            created_notion_type="idea"
        )
        
        return {
            "skipped": False,
            "created_item": {
                "type": "idea",
                "id": reply_idea["id"],
                "url": reply_idea.get("url"),
                "title": reply_title
            },
            "counts": {"tasks": 0, "resources": 0, "ideas": 1}
        }
    except Exception as e:
        error_msg = str(e)
        _log_error_to_debug_file(
            error_msg,
            "process_slack_messages.py:thread_reply",
            {"channel_name": channel_name}
        )
        
        # If Ideas database is not accessible, skip thread replies instead of failing
        if "Could not find database" in error_msg or "database" in error_msg.lower():
            print(f"Warning: Ideas database not accessible. Skipping thread replies. Error: {error_msg}")
            mark_message_processed(reply_id, channel_id, reply_ts)
            return {"skipped": True}
        else:
            print(f"Error processing thread reply: {e}")
            return None


def _handle_resource_creation_retry(
    classification: Dict[str, Any],
    message_text: str,
    rich_content_summary: Optional[str],
    rich_content: Dict[str, Any],
    channel_name: Optional[str],
    message_id: str,
    channel_id: str,
    message_ts: str
) -> Optional[Dict[str, Any]]:
    """Retry resource creation with Inbox status if original failed.
    
    Args:
        classification: Classification result
        message_text: Message text
        rich_content_summary: Rich content summary
        rich_content: Rich content dict
        channel_name: Channel name
        message_id: Message ID
        channel_id: Channel ID
        message_ts: Message timestamp
        
    Returns:
        Dict with notion_id, notion_type if retry succeeds, None otherwise
    """
    if classification["classification"] != "RESOURCE":
        return None
    
    try:
        # Retry with Inbox status
        urls = classification.get("urls", []) or rich_content.get("links", [])
        if urls:
            url = urls[0]
            try:
                metadata = fetch_url_metadata(url)
                title = metadata.get("title", url)
                resource_type = infer_resource_type(url)
            except:
                title = url
                resource_type = None
        else:
            title = message_text[:100]
            url = None
            resource_type = None
        
        summary = _build_enhanced_text(message_text, rich_content_summary)
        
        resource = create_resource(
            name=f"Slack: {title}",
            url=url,
            resource_type=resource_type,
            status="Inbox",  # Retry with Inbox
            source=f"Slack - {channel_name}" if channel_name else "Slack DM",
            summary=summary
        )
        
        return {
            "notion_id": resource["id"],
            "notion_type": "resource"
        }
    except Exception:
        return None


def _mark_message_read_if_requested(client, channel_id: str, message_ts: str, mark_as_read: bool) -> None:
    """Mark message as read if requested.
    
    Args:
        client: Slack client instance
        channel_id: Channel ID
        message_ts: Message timestamp
        mark_as_read: Whether to mark as read
    """
    if mark_as_read:
        try:
            client.conversations_mark(
                channel=channel_id,
                ts=message_ts
            )
        except:
            pass  # Ignore errors marking as read


def _create_notion_entry_from_classification(
    classification: Dict[str, Any],
    message_text: str,
    rich_content_summary: Optional[str],
    rich_content: Dict[str, Any],
    channel_name: Optional[str],
    is_dm: bool,
    user_name: Optional[str],
    enhanced_text: str
) -> Dict[str, Any]:
    """Create Notion entry based on classification.
    
    Args:
        classification: Classification result with 'classification' key
        message_text: Original message text
        rich_content_summary: Optional rich content summary
        rich_content: Rich content dict with 'links' etc.
        channel_name: Channel name (None for DMs)
        is_dm: Whether this is a direct message
        user_name: Optional user name
        enhanced_text: Enhanced text with rich content
        
    Returns:
        Dictionary with:
        - notion_id: Created Notion entry ID (or None)
        - notion_type: Type of entry ('task', 'resource', 'idea', or None)
        - created_items: List of created item dicts with type, id, url, title
        - counts: Dict with 'tasks', 'resources', 'ideas' counts
    """
    notion_id = None
    notion_type = None
    created_items = []
    counts = {"tasks": 0, "resources": 0, "ideas": 0}
    
    class_type = classification["classification"]
    
    if class_type == "TASK":
        # Extract task details
        task_name = message_text[:100]  # Truncate if needed
        if len(message_text) > 100:
            task_name = message_text[:97] + "..."
        
        # Create task
        task = create_task(
            name=f"Slack: {task_name}",
            status="Inbox"
        )
        notion_id = task["id"]
        notion_type = "task"
        created_items.append({
            "type": "task",
            "id": task["id"],
            "url": task.get("url"),
            "title": task_name
        })
        counts["tasks"] = 1
        
    elif class_type == "RESOURCE":
        # Extract URLs from classification or rich content
        urls = classification.get("urls", []) or rich_content.get("links", [])
        if urls:
            url = urls[0]
            # Fetch metadata
            try:
                metadata = fetch_url_metadata(url)
                title = metadata.get("title", url)
                resource_type = infer_resource_type(url)
            except:
                title = url
                resource_type = None
        else:
            # No URL, treat as resource based on content
            title = message_text[:100]
            url = None
            resource_type = None
        
        # Build summary with rich content
        summary = _build_enhanced_text(message_text, rich_content_summary)
        
        # Create resource
        resource = create_resource(
            name=f"Slack: {title}",
            url=url,
            resource_type=resource_type,
            status="Inbox",
            source=f"Slack - {channel_name}" if channel_name else "Slack DM",
            summary=summary
        )
        notion_id = resource["id"]
        notion_type = "resource"
        created_items.append({
            "type": "resource",
            "id": resource["id"],
            "url": resource.get("url"),
            "title": title
        })
        counts["resources"] = 1
        
    elif class_type == "IDEA":
        # Create idea with enhanced content
        idea_title = message_text[:100]
        if len(message_text) > 100:
            idea_title = message_text[:97] + "..."
        
        idea_content = enhanced_text
        
        idea = create_idea(
            title=f"Slack: {idea_title}",
            idea_type="Pattern",  # Default, could be improved
            content=idea_content,
            status="Inbox",
            source=f"Slack - {channel_name}" if channel_name else f"Slack DM from {user_name}" if user_name else "Slack"
        )
        notion_id = idea["id"]
        notion_type = "idea"
        created_items.append({
            "type": "idea",
            "id": idea["id"],
            "url": idea.get("url"),
            "title": idea_title
        })
        counts["ideas"] = 1
        
    elif class_type == "MULTIPLE":
        # Handle multiple - create both resource and task
        urls = classification.get("urls", []) or rich_content.get("links", [])
        if urls:
            url = urls[0]
            try:
                metadata = fetch_url_metadata(url)
                title = metadata.get("title", url)
                resource_type = infer_resource_type(url)
            except:
                title = url
                resource_type = None
            
            # Build summary with rich content
            summary = _build_enhanced_text(message_text, rich_content_summary)
            
            # Create resource
            resource = create_resource(
                name=f"Slack: {title}",
                url=url,
                resource_type=resource_type,
                status="Inbox",
                source=f"Slack - {channel_name}" if channel_name else "Slack DM",
                summary=summary
            )
            created_items.append({
                "type": "resource",
                "id": resource["id"],
                "url": resource.get("url"),
                "title": title
            })
            counts["resources"] = 1
            
            # Create task to review it
            task = create_task(
                name=f"Review: {title}",
                status="Inbox"
            )
            created_items.append({
                "type": "task",
                "id": task["id"],
                "url": task.get("url"),
                "title": f"Review: {title}"
            })
            counts["tasks"] = 1
            # Use resource ID for tracking
            notion_id = resource["id"]
            notion_type = "resource"
    
    return {
        "notion_id": notion_id,
        "notion_type": notion_type,
        "created_items": created_items,
        "counts": counts
    }


def process_slack_messages(
    mark_as_read: bool = False,
    max_messages: int = 50,
    reprocess: bool = False,
    include_threads: bool = True
) -> Dict[str, Any]:
    """Process unread Slack messages and create Notion entries.
    
    Args:
        mark_as_read: Whether to mark messages as read after processing
        max_messages: Maximum number of messages to process
        reprocess: If True, reprocess messages even if already processed (default: False)
        include_threads: If True, process thread replies as separate items (default: True)
        
    Returns:
        Dictionary with processing results:
        - processed: Number of messages processed
        - skipped: Number of messages skipped (already processed)
        - created: Dict with counts of created items (tasks, resources, ideas)
        - items: List of created Notion entries
    """
    client = get_slack_client()
    
    # Get all conversations with unread messages or recent activity
    all_conversations = get_unread_messages()
    
    if not all_conversations:
        return {
            "processed": 0,
            "skipped": 0,
            "created": {"tasks": 0, "resources": 0, "ideas": 0},
            "items": []
        }
    
    created_items = []
    tasks_created = 0
    resources_created = 0
    ideas_created = 0
    messages_processed = 0
    messages_skipped = 0
    
    # Check if Ideas database is accessible (for thread replies)
    ideas_db_accessible = True
    if include_threads:
        try:
            from tools.common import get_notion_client, IDEAS_DB_ID
            test_client = get_notion_client()
            # Try to retrieve the database to check if it's accessible
            test_client.databases.retrieve(database_id=IDEAS_DB_ID)
        except Exception as e:
            ideas_db_accessible = False
            print(f"Warning: Ideas database not accessible. Thread replies will be skipped. Error: {str(e)}")
            include_threads = False  # Disable thread processing if DB not accessible
    
    # Sort by unread count (if available) or updated timestamp
    # Prioritize conversations with explicit unread counts or recent activity
    def sort_key(conv):
        unread = conv.get("unread_count_display") or conv.get("unread_count") or 0
        updated = conv.get("updated", 0) or 0
        has_recent = conv.get("has_recent_activity", False)
        # Prioritize: unread count > recent activity > recency
        return (unread > 0, has_recent, unread, updated)
    
    sorted_conversations = sorted(
        all_conversations,
        key=sort_key,
        reverse=True
    )[:50]  # Process top 50 conversations
    
    # Process each conversation
    for conv in sorted_conversations:
        if messages_processed >= max_messages:
            break
            
        channel_id = conv["id"]
        channel_name = conv["name"]
        is_dm = conv["is_im"]
        last_read_ts = conv.get("last_read")
        
        try:
            # Get unread and recent messages (last 24 hours)
            message_data = get_unread_and_recent_messages(
                channel_id=channel_id,
                last_read_ts=last_read_ts,
                include_recent_hours=24,
                limit=200
            )
            
            # Process all messages (unread + recent)
            all_messages = message_data.get("all", [])
            
            for message in all_messages:
                if messages_processed >= max_messages:
                    break
                
                message_ts = message.get("ts")
                if not message_ts:
                    continue
                
                # Check if message has already been processed
                message_id = get_message_id(channel_id, message_ts)
                if not reprocess and is_message_processed(message_id):
                    messages_skipped += 1
                    continue
                
                message_text = message.get("text", "")
                if not message_text or message_text.strip() == "":
                    # Still mark as processed even if empty (to avoid reprocessing)
                    mark_message_processed(message_id, channel_id, message_ts)
                    continue
                
                # Get user info if available
                user_id = message.get("user")
                user_name = _get_user_name(client, user_id)
                
                # Extract rich content
                rich_content = extract_rich_content(message)
                rich_content_summary = format_rich_content_summary(rich_content)
                
                # Build enhanced message text with rich content
                enhanced_text = _build_enhanced_text(message_text, rich_content_summary)
                
                # Classify the message
                classification = classify_slack_message(
                    message_text=message_text,
                    channel_name=channel_name if not is_dm else None,
                    is_dm=is_dm,
                    user_name=user_name
                )
                
                # Process thread replies if enabled
                thread_replies = []
                if include_threads and has_thread_replies(message):
                    thread_ts = get_thread_ts(message)
                    if thread_ts:
                        try:
                            thread_replies = get_thread_replies(channel_id, thread_ts)
                        except Exception as e:
                            # If thread fetch fails, continue without thread replies
                            pass
                
                # Create Notion entry based on classification
                try:
                    result = _create_notion_entry_from_classification(
                        classification=classification,
                        message_text=message_text,
                        rich_content_summary=rich_content_summary,
                        rich_content=rich_content,
                        channel_name=channel_name,
                        is_dm=is_dm,
                        user_name=user_name,
                        enhanced_text=enhanced_text
                    )
                    
                    notion_id = result["notion_id"]
                    notion_type = result["notion_type"]
                    created_items.extend(result["created_items"])
                    tasks_created += result["counts"]["tasks"]
                    resources_created += result["counts"]["resources"]
                    ideas_created += result["counts"]["ideas"]
                    
                    # Mark message as processed
                    mark_message_processed(
                        message_id,
                        channel_id,
                        message_ts,
                        created_notion_id=notion_id,
                        created_notion_type=notion_type
                    )
                    
                    # Process thread replies as separate items
                    for reply in thread_replies:
                        if messages_processed >= max_messages:
                            break
                        
                        reply_result = _process_thread_reply(
                            reply=reply,
                            client=client,
                            channel_id=channel_id,
                            channel_name=channel_name,
                            is_dm=is_dm,
                            reprocess=reprocess
                        )
                        
                        if reply_result is None:
                            continue  # Error occurred
                        
                        if reply_result.get("skipped"):
                            messages_skipped += 1
                            continue
                        
                        # Update counters and items
                        created_items.append(reply_result["created_item"])
                        ideas_created += reply_result["counts"]["ideas"]
                        messages_processed += 1
                
                except Exception as e:
                    error_msg = str(e)
                    _log_error_to_debug_file(
                        error_msg,
                        "process_slack_messages.py:main_message",
                        {
                            "classification": classification.get("classification"),
                            "channel_name": channel_name
                        }
                    )
                    
                    # Handle specific errors gracefully
                    if "Invalid status option" in error_msg:
                        # Try with "Inbox" status instead
                        retry_result = _handle_resource_creation_retry(
                            classification=classification,
                            message_text=message_text,
                            rich_content_summary=rich_content_summary,
                            rich_content=rich_content,
                            channel_name=channel_name,
                            message_id=message_id,
                            channel_id=channel_id,
                            message_ts=message_ts
                        )
                        
                        if retry_result:
                            notion_id = retry_result["notion_id"]
                            notion_type = retry_result["notion_type"]
                            mark_message_processed(message_id, channel_id, message_ts, notion_id, notion_type)
                            resources_created += 1
                            messages_processed += 1
                            continue
                        else:
                            print(f"Error processing message (retry failed): {e}")
                    
                    # Log error but continue processing
                    print(f"Error processing message: {e}")
                    # Mark as processed to avoid infinite retries
                    try:
                        mark_message_processed(message_id, channel_id, message_ts)
                    except:
                        pass
                    continue
                
                messages_processed += 1
                
                # Mark as read if requested
                _mark_message_read_if_requested(client, channel_id, message_ts, mark_as_read)
                        
        except Exception as e:
            print(f"Error processing conversation {channel_name}: {e}")
            continue
    
    return {
        "processed": messages_processed,
        "skipped": messages_skipped,
        "created": {
            "tasks": tasks_created,
            "resources": resources_created,
            "ideas": ideas_created
        },
        "items": created_items
    }
