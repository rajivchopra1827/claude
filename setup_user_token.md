# Setting Up User Token for Slack Inbox Agent

To let the bot see everything you see (your channels, DMs, unread messages), you need to set up OAuth to get a **user token**.

## Step 1: Configure OAuth in Slack App Settings

1. Go to https://api.slack.com/apps
2. Select your app "AIPOS Slack Inbox"
3. Click **"OAuth & Permissions"** in the left sidebar
4. Scroll down to **"User Token Scopes"**
5. Add these scopes:
   - `channels:read` - View basic information about public channels
   - `channels:history` - View messages in public channels
   - `groups:read` - View basic information about private channels
   - `groups:history` - View messages in private channels
   - `im:read` - View basic information about direct messages
   - `im:history` - View messages in direct messages
   - `mpim:read` - View basic information about group DMs
   - `mpim:history` - View messages in group DMs
   - `users:read` - View people in a workspace

6. Scroll up to **"Redirect URLs"** section
7. Add a redirect URL. For local testing, you can use:
   - `http://localhost:3000/oauth/callback` (or any port you prefer)

8. Scroll up to **"OAuth Tokens for Your Workspace"**
9. Click **"Add New Redirect URL"** if needed, then click **"Install to Workspace"**
10. Authorize the app - this will generate a **User OAuth Token** (starts with `xoxp-`)

## Step 2: Get Your User Token

After authorizing, you'll see:
- **User OAuth Token**: `xoxp-...` (this is what you need!)

Copy this token.

## Step 3: Add User Token to env.txt

Add this line to your `env.txt`:
```
SLACK_USER_TOKEN=xoxp-your-user-token-here
```

## Step 4: Update the Code

The code will be updated to use the user token instead of (or in addition to) the bot token.

## Alternative: Quick Test with Existing Token

If you already have a user token from the "Your App Configuration Tokens" section you showed earlier, you can use that! Just add it to `env.txt` as `SLACK_USER_TOKEN`.
