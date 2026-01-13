"""Classify user input as TASK, RESOURCE, INSIGHT, or MULTIPLE."""

import re
from typing import Dict, Any


def classify_input(user_input: str) -> Dict[str, Any]:
    """Classify user input as TASK, RESOURCE, INSIGHT, or MULTIPLE.
    
    Args:
        user_input: User's input text
    
    Returns:
        Dictionary with classification, confidence, and extracted information
    """
    input_lower = user_input.lower()
    
    # Check for URL
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, user_input)
    has_url = len(urls) > 0
    
    # Task signals
    task_keywords = ["add task", "remind me", "schedule", "todo", "to do", "task to", "need to"]
    has_task_signal = any(keyword in input_lower for keyword in task_keywords)
    has_action_verbs = any(verb in input_lower for verb in ["email", "send", "review", "schedule", "meet", "call"])
    
    # Resource signals
    resource_keywords = ["save this", "check out", "read this", "watch this", "found this"]
    has_resource_signal = any(keyword in input_lower for keyword in resource_keywords)
    
    # Insight signals
    insight_keywords = ["customer said", "just realized", "idea:", "observation", "pattern", "screenshot"]
    has_insight_signal = any(keyword in input_lower for keyword in insight_keywords)
    
    # Multiple signals
    has_multiple = (has_url and has_task_signal) or ("remind me to" in input_lower and has_url)
    
    if has_multiple:
        return {
            "classification": "MULTIPLE",
            "confidence": 0.85,
            "urls": urls,
            "has_task": True,
            "has_resource": True
        }
    elif has_url or has_resource_signal:
        return {
            "classification": "RESOURCE",
            "confidence": 0.90 if has_url else 0.70,
            "urls": urls
        }
    elif has_task_signal or has_action_verbs:
        return {
            "classification": "TASK",
            "confidence": 0.85 if has_task_signal else 0.70,
            "urls": []
        }
    elif has_insight_signal:
        return {
            "classification": "INSIGHT",
            "confidence": 0.80,
            "urls": []
        }
    else:
        # Default to insight for observations
        return {
            "classification": "INSIGHT",
            "confidence": 0.60,
            "urls": []
        }
