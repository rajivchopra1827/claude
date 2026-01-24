"""Simple test script to debug Slack API access."""

import os
import json
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "env.txt"))

bot_token = os.getenv("SLACK_BOT_TOKEN")
if not bot_token:
    print("ERROR: SLACK_BOT_TOKEN not found in env.txt")
    exit(1)

client = WebClient(token=bot_token)

print("=" * 60)
print("Testing Slack API Access")
print("=" * 60)
print()

# Test 1: Get bot info
print("1. Testing bot authentication...")
try:
    auth_test = client.auth_test()
    if auth_test["ok"]:
        print(f"   ✓ Bot authenticated as: {auth_test.get('user')}")
        print(f"   ✓ Team: {auth_test.get('team')}")
    else:
        print(f"   ✗ Auth failed: {auth_test.get('error')}")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 2: List conversations
print("2. Listing conversations...")
try:
    response = client.conversations_list(
        types="public_channel,im",
        exclude_archived=True,
        limit=100
    )
    
    if response["ok"]:
        conversations = response.get("channels", [])
        print(f"   ✓ Found {len(conversations)} total conversations")
        
        # Filter to only channels bot is a member of
        member_channels = [c for c in conversations if c.get("is_member", False)]
        dms = [c for c in conversations if c.get("is_im", False)]
        
        print(f"   ✓ Bot is member of {len(member_channels)} channels")
        print(f"   ✓ Bot has {len(dms)} DMs")
        print()
        
        # Show first few member channels
        if member_channels:
            print("   Channels bot is a member of:")
            for conv in member_channels[:10]:
                name = conv.get("name", "Unknown")
                updated = conv.get("updated", 0)
                unread_count = conv.get("unread_count")
                unread_display = conv.get("unread_count_display")
                print(f"     - {name} (updated: {updated}, unread_count: {unread_count}, unread_display: {unread_display})")
            if len(member_channels) > 10:
                print(f"     ... and {len(member_channels) - 10} more")
        print()
        
        # Show first few DMs
        if dms:
            print("   Direct Messages:")
            for conv in dms[:5]:
                user_id = conv.get("user")
                unread_count = conv.get("unread_count")
                unread_display = conv.get("unread_count_display")
                print(f"     - DM with {user_id} (unread_count: {unread_count}, unread_display: {unread_display})")
            if len(dms) > 5:
                print(f"     ... and {len(dms) - 5} more")
        print()
        
    else:
        print(f"   ✗ Failed: {response.get('error')}")
except SlackApiError as e:
    print(f"   ✗ Slack API Error: {e.response.get('error')}")
    if e.response.get('needed'):
        print(f"     Missing scope: {e.response.get('needed')}")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 3: Try to get messages from a channel bot is member of
print("3. Testing message retrieval from channels bot is a member of...")
if member_channels:
    test_channel = member_channels[0]
    channel_id = test_channel["id"]
    channel_name = test_channel.get("name", "Unknown")
    
    print(f"   Testing channel: {channel_name} ({channel_id})")
    try:
        history = client.conversations_history(
            channel=channel_id,
            limit=5
        )
        
        if history["ok"]:
            messages = history.get("messages", [])
            print(f"   ✓ Successfully retrieved {len(messages)} messages")
            
            if messages:
                print("   Sample messages:")
                for msg in messages[:3]:
                    text = msg.get("text", "")[:50]
                    user = msg.get("user", "Unknown")
                    ts = msg.get("ts", "")
                    print(f"     - [{ts}] {user}: {text}...")
        else:
            print(f"   ✗ Failed: {history.get('error')}")
    except SlackApiError as e:
        print(f"   ✗ Slack API Error: {e.response.get('error')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
else:
    print("   ⚠ No channels found where bot is a member")
print()

# Test 4: Try to get messages from a DM
print("4. Testing message retrieval from DMs...")
if dms:
    test_dm = dms[0]
    dm_id = test_dm["id"]
    user_id = test_dm.get("user", "Unknown")
    
    print(f"   Testing DM with user: {user_id} ({dm_id})")
    try:
        history = client.conversations_history(
            channel=dm_id,
            limit=5
        )
        
        if history["ok"]:
            messages = history.get("messages", [])
            print(f"   ✓ Successfully retrieved {len(messages)} messages")
            
            if messages:
                print("   Sample messages:")
                for msg in messages[:3]:
                    text = msg.get("text", "")[:50]
                    user = msg.get("user", "Unknown")
                    ts = msg.get("ts", "")
                    print(f"     - [{ts}] {user}: {text}...")
        else:
            print(f"   ✗ Failed: {history.get('error')}")
    except SlackApiError as e:
        print(f"   ✗ Slack API Error: {e.response.get('error')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
else:
    print("   ⚠ No DMs found")
print()

print("=" * 60)
print("Test Complete")
print("=" * 60)
