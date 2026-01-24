"""Get list of conversations with unread messages."""

import json
import time
from typing import List, Dict, Any, Optional
from slack_sdk.errors import SlackApiError
from .slack_client import get_slack_client


def get_unread_messages(
    include_channels: bool = True,
    include_dms: bool = True,
    include_groups: bool = True
) -> List[Dict[str, Any]]:
    """Get list of conversations with unread messages.
    
    Args:
        include_channels: Include public channels
        include_dms: Include direct messages
        include_groups: Include private channels/groups
        
    Returns:
        List of conversation objects with unread messages, each containing:
        - id: Conversation ID
        - name: Channel/DM name
        - is_im: True if direct message
        - is_channel: True if public channel
        - is_group: True if private channel
        - unread_count: Number of unread messages (DMs only)
        - unread_count_display: Display count (DMs only)
        - last_read: Timestamp of last read message (from conversations.info)
        - has_recent_activity: True if activity in last 24 hours
    """
    client = get_slack_client()
    
    # #region debug log - Check token type
    import os
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "env.txt"))
    user_token = os.getenv("SLACK_USER_TOKEN")
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    token_prefix = client.token[:4] if hasattr(client, 'token') and client.token else "unknown"
    is_user_token = token_prefix == "xoxp"
    with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"B","location":"get_unread_messages.py:34","message":"Token type check","data":{"token_prefix":token_prefix,"is_user_token":is_user_token,"has_user_token_env":bool(user_token),"has_bot_token_env":bool(bot_token)},"timestamp":int(time.time()*1000)})+'\n')
    # #endregion
    
    # Build types list based on what to include
    types_list = []
    if include_channels:
        types_list.append("public_channel")
    if include_dms:
        types_list.append("im")
    if include_groups:
        types_list.append("private_channel")
    
    types_str = ",".join(types_list) if types_list else "public_channel,im,private_channel"
    
    # #region debug log
    with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"C","location":"get_unread_messages.py:42","message":"Attempting conversations_list","data":{"types_str":types_str,"include_groups":include_groups},"timestamp":int(__import__('time').time()*1000)})+'\n')
    # #endregion
    
    try:
        # Get all conversations
        response = client.conversations_list(
            types=types_str,
            exclude_archived=True,
            limit=1000
        )
        
        # #region debug log
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"C","location":"get_unread_messages.py:52","message":"API response received","data":{"ok":response.get("ok"),"error":response.get("error")},"timestamp":int(__import__('time').time()*1000)})+'\n')
        # #endregion
        
        if not response["ok"]:
            error = response.get('error', 'unknown')
            
            # #region debug log
            with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"B","location":"get_unread_messages.py:58","message":"API error detected","data":{"error":error,"needed_scope":response.get("needed")},"timestamp":int(__import__('time').time()*1000)})+'\n')
            # #endregion
            
            # If missing groups:read scope and we're trying to include groups, retry without them
            if error == 'missing_scope' and include_groups and 'groups:read' in str(response.get('needed', '')):
                # #region debug log
                with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"B","location":"get_unread_messages.py:64","message":"Retrying without private channels","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
                # #endregion
                
                # Retry without private channels
                types_list_retry = [t for t in types_list if t != "private_channel"]
                types_str_retry = ",".join(types_list_retry) if types_list_retry else "public_channel,im"
                
                response = client.conversations_list(
                    types=types_str_retry,
                    exclude_archived=True,
                    limit=1000
                )
                
                # #region debug log
                with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"B","location":"get_unread_messages.py:75","message":"Retry response","data":{"ok":response.get("ok"),"error":response.get("error")},"timestamp":int(__import__('time').time()*1000)})+'\n')
                # #endregion
            
            if not response["ok"]:
                raise Exception(f"Slack API error: {response.get('error', 'unknown')}")
    
    except SlackApiError as e:
        # #region debug log
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"C","location":"get_unread_messages.py:95","message":"SlackApiError caught","data":{"error":e.response.get("error") if hasattr(e, 'response') else str(e),"needed":e.response.get("needed") if hasattr(e, 'response') and e.response else None},"timestamp":int(__import__('time').time()*1000)})+'\n')
        # #endregion
        
        # If missing groups:read scope and we're trying to include groups, retry without them
        if (hasattr(e, 'response') and e.response and 
            e.response.get('error') == 'missing_scope' and 
            include_groups and 
            'groups:read' in str(e.response.get('needed', ''))):
            
            # #region debug log
            with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"C","location":"get_unread_messages.py:103","message":"Retrying without private channels (exception handler)","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
            # #endregion
            
            # Retry without private channels
            types_list_retry = [t for t in types_list if t != "private_channel"]
            types_str_retry = ",".join(types_list_retry) if types_list_retry else "public_channel,im"
            
            try:
                response = client.conversations_list(
                    types=types_str_retry,
                    exclude_archived=True,
                    limit=1000
                )
                
                # #region debug log
                with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"C","location":"get_unread_messages.py:115","message":"Retry response (exception handler)","data":{"ok":response.get("ok"),"error":response.get("error")},"timestamp":int(__import__('time').time()*1000)})+'\n')
                # #endregion
                
                if not response["ok"]:
                    raise Exception(f"Slack API error: {response.get('error', 'unknown')}")
            except SlackApiError as retry_error:
                raise Exception(f"Failed to get unread messages: {str(retry_error)}")
        else:
            raise Exception(f"Failed to get unread messages: {str(e)}")
    
    # Process conversations (works for both successful first try and successful retry)
    conversations = response.get("channels", [])
    
    # #region debug log
    with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"get_unread_messages.py:139","message":"Conversations received","data":{"total_conversations":len(conversations)},"timestamp":int(time.time()*1000)})+'\n')
    # #endregion
    
    # #region debug log - Sample conversation structure from conversations_list
    if conversations:
        sample_conv = conversations[0]
        sample_keys = list(sample_conv.keys())
        sample_data = {k: sample_conv.get(k) for k in ['id', 'name', 'is_im', 'is_channel', 'is_group', 'is_member', 'unread_count', 'unread_count_display', 'updated']}
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"get_unread_messages.py:145","message":"Sample conversation from conversations_list","data":{"all_keys":sample_keys,"sample_fields":sample_data},"timestamp":int(time.time()*1000)})+'\n')
    # #endregion
    
    # User tokens provide unread_count/unread_count_display and can see all user's conversations
    # Bot tokens don't provide unread counts and can only read channels bot is a member of
    # Filter to conversations with unread messages (user tokens) or bot member channels (bot tokens)
    
    # Calculate 24 hours ago timestamp
    twenty_four_hours_ago = time.time() - (24 * 60 * 60)
    
    unread_conversations = []
    for conv in conversations:
        # #region debug log
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"G","location":"get_unread_messages.py:144","message":"Checking conversation","data":{"id":conv.get("id"),"name":conv.get("name","DM"),"is_im":conv.get("is_im"),"unread_count":conv.get("unread_count"),"unread_count_display":conv.get("unread_count_display"),"is_member":conv.get("is_member")},"timestamp":int(__import__('time').time()*1000)})+'\n')
        # #endregion
        
        # Check for unread indicators
        unread_count = conv.get("unread_count") or 0
        unread_count_display = conv.get("unread_count_display") or 0
        
        is_im = conv.get("is_im", False)
        is_mpim = conv.get("is_mpim", False)
        is_member = conv.get("is_member", False)
        
        # Skip channels where user is not a member (can't read)
        if not (is_im or is_mpim) and not is_member:
            # #region debug log
            with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"G","location":"get_unread_messages.py:163","message":"Skipping - not member","data":{"name":conv.get("name")},"timestamp":int(__import__('time').time()*1000)})+'\n')
            # #endregion
            continue
        
        # Get detailed conversation info including last_read timestamp
        last_read = None
        conv_info_unread_count = None
        conv_info_unread_count_display = None
        try:
            conv_info = client.conversations_info(channel=conv["id"])
            if conv_info.get("ok") and conv_info.get("channel"):
                channel_info = conv_info["channel"]
                # #region debug log - Check conversations.info for unread fields
                info_keys = list(channel_info.keys())
                info_unread_fields = {k: channel_info.get(k) for k in ['unread_count', 'unread_count_display', 'last_read'] if k in channel_info}
                with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"C","location":"get_unread_messages.py:179","message":"conversations.info response","data":{"conv_id":conv.get("id"),"conv_name":conv.get("name","DM"),"has_unread_fields":bool(info_unread_fields),"unread_fields":info_unread_fields,"sample_keys":info_keys[:10]},"timestamp":int(time.time()*1000)})+'\n')
                # #endregion
                
                # Check if conversations.info has unread_count that conversations_list doesn't
                conv_info_unread_count = channel_info.get("unread_count")
                conv_info_unread_count_display = channel_info.get("unread_count_display")
                
                # last_read is available for DMs and sometimes for channels with user tokens
                last_read_ts = channel_info.get("last_read")
                if last_read_ts:
                    # Convert Slack timestamp to float
                    try:
                        last_read = float(last_read_ts)
                    except (ValueError, TypeError):
                        pass
        except Exception as e:
            # #region debug log
            with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"C","location":"get_unread_messages.py:195","message":"conversations.info failed","data":{"conv_id":conv.get("id"),"error":str(e)},"timestamp":int(time.time()*1000)})+'\n')
            # #endregion
            # If conversations.info fails, continue without last_read
            # This can happen with bot tokens or missing scopes
            pass
        
        # Use unread_count from conversations.info if available and conversations_list doesn't have it
        if conv_info_unread_count is not None and unread_count == 0:
            unread_count = conv_info_unread_count
        if conv_info_unread_count_display is not None and unread_count_display == 0:
            unread_count_display = conv_info_unread_count_display
        
        # Check if conversation has recent activity (last 24 hours)
        updated_ts = conv.get("updated", 0)
        # updated is in milliseconds, convert to seconds
        if isinstance(updated_ts, (int, float)) and updated_ts > 1000000000000:
            updated_ts = updated_ts / 1000
        
        has_recent_activity = False
        if updated_ts and updated_ts > twenty_four_hours_ago:
            has_recent_activity = True
        
        # Include conversation if:
        # 1. Has explicit unread count (DMs)
        # 2. Has recent activity (last 24 hours)
        # 3. Is a DM (always include for processing)
        # 4. Has last_read timestamp (means we can track unread state)
        should_include = (
            unread_count > 0 or 
            unread_count_display > 0 or 
            has_recent_activity or 
            is_im or 
            is_mpim or
            last_read is not None
        )
        
        # #region debug log - Filtering decision
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"D","location":"get_unread_messages.py:225","message":"Filtering decision","data":{"conv_name":conv.get("name","DM"),"unread_count":unread_count,"unread_count_display":unread_count_display,"has_recent_activity":has_recent_activity,"is_im":is_im,"is_mpim":is_mpim,"has_last_read":last_read is not None,"should_include":should_include},"timestamp":int(time.time()*1000)})+'\n')
        # #endregion
        
        if not should_include:
            continue
        
        unread_conversations.append({
            "id": conv["id"],
            "name": conv.get("name") or conv.get("user", "Unknown"),
            "is_im": is_im,
            "is_channel": conv.get("is_channel", False),
            "is_group": conv.get("is_group", False),
            "is_mpim": is_mpim,
            "is_private": conv.get("is_private", False),
            "is_member": is_member,
            "unread_count": unread_count,
            "unread_count_display": unread_count_display,
            "last_read": last_read,  # Timestamp of last read message
            "has_recent_activity": has_recent_activity,
            "user": conv.get("user"),  # For DMs
            "updated": updated_ts,  # Last update timestamp
        })
        # #region debug log
        with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"G","location":"get_unread_messages.py:185","message":"Added conversation with unread","data":{"name":conv.get("name") or conv.get("user","Unknown"),"unread_count":unread_count,"unread_display":unread_count_display},"timestamp":int(__import__('time').time()*1000)})+'\n')
        # #endregion
    
    # #region debug log
    with open('/Users/rajivchopra/Claude/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"D","location":"get_unread_messages.py:172","message":"Final unread count","data":{"unread_conversations_count":len(unread_conversations)},"timestamp":int(__import__('time').time()*1000)})+'\n')
    # #endregion
    
    return unread_conversations
