"""Extract metadata from user input (dates, projects, people, etc.)."""

import re
from typing import Dict, Any
from datetime import datetime, timedelta
from calendar import monthrange


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
