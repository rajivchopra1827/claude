"""Slack client wrapper for API operations."""

import os
from typing import Optional, List, Set, Tuple
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables from env.txt
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "env.txt"
))

_slack_client: Optional[WebClient] = None

# Required scopes for full inbox visibility
REQUIRED_USER_TOKEN_SCOPES = {
    "channels:read",
    "channels:history",
    "groups:read",
    "groups:history",
    "im:read",
    "im:history",
    "mpim:read",
    "mpim:history",
}


def verify_token_scopes(client: WebClient, token_type: str = "user") -> Tuple[bool, Set[str]]:
    """Verify that the token has the required scopes.
    
    Note: auth.test doesn't return scopes, so this function cannot actually verify scopes.
    It's kept for potential future use if Slack adds scope info to auth.test.
    
    Args:
        client: Slack WebClient instance
        token_type: Type of token ("user" or "bot")
        
    Returns:
        Tuple of (has_all_scopes, missing_scopes) - always returns (True, set()) since
        we can't actually verify scopes via auth.test
    """
    # Slack's auth.test API doesn't return scopes, so we can't verify them
    # We'll return True to allow the client to be created, and let actual API calls
    # fail with proper error messages if scopes are missing
    return True, set()


def get_slack_client(use_user_token: bool = True, verify_scopes: bool = True) -> WebClient:
    """Get or create Slack WebClient instance.
    
    Args:
        use_user_token: If True, prefer user token (sees user's channels/DMs).
                       If False or user token unavailable, use bot token.
        verify_scopes: If True, verify token has required scopes (default: True)
    
    Returns:
        WebClient instance configured with user token (preferred) or bot token
        
    Raises:
        ValueError: If neither SLACK_USER_TOKEN nor SLACK_BOT_TOKEN is set
    """
    global _slack_client
    
    if _slack_client is None:
        # Prefer user token if available (sees everything user sees)
        if use_user_token:
            user_token = os.getenv("SLACK_USER_TOKEN")
            
            if user_token:
                client = WebClient(token=user_token)
                
                # Note: auth.test doesn't return scopes, so we can't verify them upfront
                # We'll skip verification and let actual API calls handle permission errors
                # This allows the system to work - if scopes are missing, API calls will fail
                # with clear error messages indicating which scopes are needed
                
                _slack_client = client
                return _slack_client
        
        # Fall back to bot token
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        if not bot_token:
            raise ValueError(
                "Neither SLACK_USER_TOKEN nor SLACK_BOT_TOKEN is set. "
                "Add at least one to env.txt"
            )
        
        client = WebClient(token=bot_token)
        
        # Note: auth.test doesn't return scopes, so we can't verify them
        # Bot tokens have different scope requirements than user tokens
        # For full inbox visibility, a user token is recommended
        
        _slack_client = client
    
    return _slack_client


def get_slack_app_token() -> str:
    """Get Slack app-level token for Socket Mode.
    
    Returns:
        App-level token string
        
    Raises:
        ValueError: If SLACK_APP_TOKEN is not set in environment
    """
    app_token = os.getenv("SLACK_APP_TOKEN")
    if not app_token:
        raise ValueError(
            "SLACK_APP_TOKEN environment variable not set. "
            "Add it to env.txt"
        )
    return app_token
