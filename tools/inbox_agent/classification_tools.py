"""Classification tools for Inbox Agent - classifying input and extracting metadata."""

import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from calendar import monthrange


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


def extract_metadata(user_input: str) -> Dict[str, Any]:
    """Extract metadata from user input (dates, projects, people, etc.).
    
    Args:
        user_input: User's input text
    
    Returns:
        Dictionary with extracted metadata
    """
    metadata = {
        "due_date": None,
        "project_mentions": [],
        "people_mentions": [],
        "urls": []
    }
    
    # Extract URLs
    url_pattern = r'https?://[^\s]+'
    metadata["urls"] = re.findall(url_pattern, user_input)
    
    # Extract dates (simple patterns)
    # "next Friday", "Monday", "end of month", etc.
    today = datetime.now()
    
    if "next friday" in user_input.lower():
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        metadata["due_date"] = (today + timedelta(days=days_until_friday)).strftime("%Y-%m-%d")
    elif "monday" in user_input.lower():
        days_until_monday = (0 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        metadata["due_date"] = (today + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")
    elif "end of month" in user_input.lower():
        # Get last day of current month
        last_day_num = monthrange(today.year, today.month)[1]
        last_day = datetime(today.year, today.month, last_day_num).date()
        metadata["due_date"] = last_day.strftime("%Y-%m-%d")
    
    # Extract project mentions (common projects)
    common_projects = ["reporting pod", "agency enablement pod", "ai transformation", "pm hiring", "epd"]
    for project in common_projects:
        if project in user_input.lower():
            metadata["project_mentions"].append(project.title())
    
    # Extract people mentions (common names)
    common_people = ["reid", "paolo", "aaron", "megan", "melissa", "cassidy", "jd", "jason", "ricardo", "devik", "randa", "lauren"]
    for person in common_people:
        if person.lower() in user_input.lower():
            metadata["people_mentions"].append(person.title())
    
    return metadata
