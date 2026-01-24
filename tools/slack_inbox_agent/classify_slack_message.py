"""Classify Slack messages as TASK, RESOURCE, IDEA, or MULTIPLE."""

import re
from typing import Dict, Any, Optional
from tools.inbox_agent.classify_input import classify_input


def classify_slack_message(
    message_text: str,
    channel_name: Optional[str] = None,
    is_dm: bool = False,
    user_name: Optional[str] = None
) -> Dict[str, Any]:
    """Classify a Slack message using existing classification logic.
    
    Args:
        message_text: The message text content
        channel_name: Name of the channel (if not DM)
        is_dm: True if this is a direct message
        user_name: Name of the user who sent the message
        
    Returns:
        Dictionary with classification, confidence, and extracted information
    """
    # Use existing classification logic
    classification = classify_input(message_text)
    
    # Enhance with Slack-specific context
    result = {
        "classification": classification["classification"],
        "confidence": classification["confidence"],
        "urls": classification.get("urls", []),
        "slack_context": {
            "channel": channel_name,
            "is_dm": is_dm,
            "user": user_name
        }
    }
    
    # Adjust confidence based on context
    # DMs are often more actionable
    if is_dm and classification["classification"] == "TASK":
        result["confidence"] = min(0.95, classification["confidence"] + 0.1)
    
    # Channel messages mentioning you might be tasks
    if not is_dm and "@" in message_text and classification["classification"] != "TASK":
        # Check if it's likely a task request
        task_indicators = ["can you", "please", "need", "should", "could you"]
        if any(indicator in message_text.lower() for indicator in task_indicators):
            result["classification"] = "TASK"
            result["confidence"] = 0.75
    
    return result
