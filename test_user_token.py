"""Test if we can use a user token to see user's conversations."""

import os
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "env.txt"))

# Try user token if available
user_token = os.getenv("SLACK_USER_TOKEN")
bot_token = os.getenv("SLACK_BOT_TOKEN")

print("=" * 60)
print("Testing User Token Access")
print("=" * 60)
print()

if user_token:
    print("✓ Found SLACK_USER_TOKEN in env.txt")
    print(f"  Token starts with: {user_token[:10]}...")
    print()
    
    client = WebClient(token=user_token)
    
    print("1. Testing authentication...")
    try:
        auth = client.auth_test()
        if auth["ok"]:
            print(f"   ✓ Authenticated as user: {auth.get('user')}")
            print(f"   ✓ Team: {auth.get('team')}")
        else:
            print(f"   ✗ Auth failed: {auth.get('error')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    print()
    
    print("2. Listing conversations (user's view)...")
    try:
        response = client.conversations_list(
            types="public_channel,private_channel,im,mpim",
            exclude_archived=True,
            limit=100
        )
        
        if response["ok"]:
            conversations = response.get("channels", [])
            print(f"   ✓ Found {len(conversations)} conversations")
            
            # Check for unread counts (user tokens provide these!)
            channels_with_unread = []
            dms_with_unread = []
            
            for conv in conversations:
                unread_count = conv.get("unread_count", 0) or 0
                unread_display = conv.get("unread_count_display", 0) or 0
                
                if unread_count > 0 or unread_display > 0:
                    if conv.get("is_im") or conv.get("is_mpim"):
                        dms_with_unread.append((conv.get("name") or conv.get("user", "Unknown"), unread_display or unread_count))
                    else:
                        channels_with_unread.append((conv.get("name", "Unknown"), unread_display or unread_count))
            
            print(f"   ✓ Channels with unread: {len(channels_with_unread)}")
            print(f"   ✓ DMs with unread: {len(dms_with_unread)}")
            print()
            
            if channels_with_unread:
                print("   Channels with unread messages:")
                for name, count in channels_with_unread[:10]:
                    print(f"     - #{name}: {count} unread")
                if len(channels_with_unread) > 10:
                    print(f"     ... and {len(channels_with_unread) - 10} more")
                print()
            
            if dms_with_unread:
                print("   DMs with unread messages:")
                for name, count in dms_with_unread[:10]:
                    print(f"     - {name}: {count} unread")
                if len(dms_with_unread) > 10:
                    print(f"     ... and {len(dms_with_unread) - 10} more")
                print()
        else:
            print(f"   ✗ Failed: {response.get('error')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
else:
    print("⚠ No SLACK_USER_TOKEN found in env.txt")
    print()
    print("To get a user token:")
    print("1. Go to https://api.slack.com/apps")
    print("2. Select your app")
    print("3. Go to 'OAuth & Permissions'")
    print("4. Add user token scopes:")
    print("   - channels:read, channels:history")
    print("   - groups:read, groups:history")
    print("   - im:read, im:history")
    print("   - mpim:read, mpim:history")
    print("5. Click 'Install to Workspace'")
    print("6. Copy the 'User OAuth Token' (starts with xoxp-)")
    print("7. Add to env.txt as: SLACK_USER_TOKEN=xoxp-...")

print()
print("=" * 60)
