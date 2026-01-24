# How to Get a User Token for Slack Inbox Agent

You're currently seeing only the "Bot User OAuth Token" because user token scopes aren't enabled yet. Here's how to enable them:

## Step 1: Add User Token Scopes

1. In your Slack app settings (https://api.slack.com/apps), select your app
2. Click **"OAuth & Permissions"** in the left sidebar
3. Scroll down to find **"User Token Scopes"** section (below "Bot Token Scopes")
4. Click **"Add an OAuth Scope"** under User Token Scopes
5. Add these scopes one by one:
   - `channels:read` - View basic information about public channels
   - `channels:history` - View messages in public channels  
   - `groups:read` - View basic information about private channels
   - `groups:history` - View messages in private channels
   - `im:read` - View basic information about direct messages
   - `im:history` - View messages in direct messages
   - `mpim:read` - View basic information about group DMs
   - `mpim:history` - View messages in group DMs
   - `users:read` - View people in a workspace

## Step 2: Reinstall the App

After adding the scopes:
1. Scroll up to the **"OAuth Tokens for Your Workspace"** section
2. Click the green **"Reinstall to Digible"** button
3. Review the permissions and click **"Allow"**

## Step 3: Get Your User Token

After reinstalling, you should now see TWO tokens:
- **Bot User OAuth Token** (xoxb-...) - what you have now
- **User OAuth Token** (xoxp-...) - NEW! This is what you need

Copy the **User OAuth Token** (starts with `xoxp-`)

## Step 4: Add to env.txt

Add this line to your `env.txt`:
```
SLACK_USER_TOKEN=xoxp-your-user-token-here
```

## Step 5: Test

Run: `python3 test_user_token.py` to verify it works!
