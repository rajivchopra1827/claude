"""Get comprehensive data for weekly executive update, organized by strategic priority."""

from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from task_management.tools.task_manager_agent.analyze_all_projects import get_all_active_projects, analyze_project_health
from task_management.tools.task_manager_agent.analyze_task_project_alignment import get_tasks_for_project
from task_management.tools.task_manager_agent.extract_task_properties import extract_task_properties
from task_management.tools.task_manager_agent.get_action_items_for_review import get_action_items_for_review
from task_management.tools.task_manager_agent.analyze_waiting_tasks import analyze_waiting_tasks
from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID, get_strategic_priorities, get_priority_by_person


def classify_by_strategic_priority(title: str, project_name: str = "") -> str:
    """Classify a task or project by strategic priority based on keywords.
    
    Args:
        title: Task or project title
        project_name: Optional project name for additional context
        
    Returns:
        Strategic priority key or "other"
    """
    combined_text = f"{title} {project_name}".lower()
    
    # Get strategic priorities from context
    strategic_priorities = get_strategic_priorities()
    
    # Edge case: "Fiona Posts demo" should be Posts, not Fiona 2.0
    if "fiona posts" in combined_text or "fiona posts demo" in combined_text:
        return "posts"
    
    # Check for person names first (more specific)
    words = combined_text.split()
    for word in words:
        # Capitalize first letter to check person name
        person_name = word.capitalize() if word else ""
        priority = get_priority_by_person(person_name)
        if priority:
            return priority
    
    # Check keywords for each priority
    # Use a scoring system: more specific matches win
    best_match = None
    best_score = 0
    
    # Priority-specific indicators (very specific, should match first)
    priority_indicators = {
        "fiona_2": ["fiona", "reporting", "csat", "kelsey", "cassidy"],
        "posts": ["posts", "zumper", "greystar", "organic", "michelle", "shannon"],
        "ai_fulfillment": ["aep", "fulfillment", "megan", "jenny", "pmt"],
        "digible_ai": ["digible.ai", "digible ai", "tiger team", "skunkworks"],
        "ai_enablement": ["ai enablement", "ai training", "ai governance"],
    }
    
    # First check for very specific indicators
    for priority_key, indicators in priority_indicators.items():
        for indicator in indicators:
            if indicator.lower() in combined_text:
                exclusions = strategic_priorities.get(priority_key, {}).get("exclusions", [])
                if not any(excl in combined_text for excl in exclusions):
                    return priority_key
    
    # Then check all keywords, scoring by specificity (shorter = more specific)
    for priority_key, priority_info in strategic_priorities.items():
        keywords = priority_info.get("keywords", [])
        people = priority_info.get("people", [])
        
        # Check people names (very specific)
        for person in people:
            if person.lower() in combined_text:
                return priority_key
        
        # Check keywords, score by specificity
        for keyword in keywords:
            if keyword.lower() in combined_text:
                exclusions = priority_info.get("exclusions", [])
                if not any(excl in combined_text for excl in exclusions):
                    # Score: shorter keywords are more specific
                    score = 1000 / (len(keyword) + 1)
                    if score > best_score:
                        best_score = score
                        best_match = priority_key
    
    if best_match:
        return best_match
    
    return "other"


def get_tasks_completed_this_week() -> List[Dict[str, Any]]:
    """Get all tasks completed in the last 7 days.
    
    Returns:
        List of completed task dictionaries
    """
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Query tasks with Completed date in last 7 days
    filter_dict = {
        "and": [
            {
                "property": "Status",
                "status": {"equals": "Done"}
            },
            {
                "property": "Completed",
                "date": {"on_or_after": week_ago.isoformat()}
            }
        ]
    }
    
    completed_pages = query_database_complete(
        TASKS_DATA_SOURCE_ID,
        filter_dict=filter_dict,
        sorts=[{"property": "Completed", "direction": "descending"}],
        use_data_source=True
    )
    
    return [extract_task_properties(page) for page in completed_pages]


def get_weekly_exec_data() -> Dict[str, Any]:
    """Get comprehensive data for weekly executive update, organized by strategic priority.
    
    Returns:
        Dict with:
        - strategic_priorities: Data for each of the 5 strategic priorities
        - accomplishments: Tasks completed this week
        - blockers: Waiting/blocked items
        - action_items: Pending action items from meetings
        - summary: High-level summary statistics
    """
    today = date.today()
    
    # 1. Get all active projects and their health
    active_projects = get_all_active_projects()
    
    # 2. Organize projects by strategic priority
    priorities_data = {
        "fiona_2": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"},
        "posts": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"},
        "ai_fulfillment": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"},
        "digible_ai": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"},
        "ai_enablement": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"},
        "other": {"projects": [], "tasks_completed": [], "blockers": [], "status": "on_track"}
    }
    
    # Analyze each project
    for project in active_projects:
        task_pages = get_tasks_for_project(project["id"])
        tasks = [extract_task_properties(t) for t in task_pages]
        health = analyze_project_health(project, tasks)
        
        # Classify project by strategic priority
        priority_key = classify_by_strategic_priority(project["title"])
        
        # Add project with health data
        project_data = {
            "project": project,
            "health": health,
            "tasks": tasks
        }
        priorities_data[priority_key]["projects"].append(project_data)
        
        # Determine status based on health
        if health["health_status"] == "critical":
            if priorities_data[priority_key]["status"] != "blocked":
                priorities_data[priority_key]["status"] = "at_risk"
        elif health["health_status"] == "needs_attention":
            if priorities_data[priority_key]["status"] == "on_track":
                priorities_data[priority_key]["status"] = "at_risk"
    
    # 3. Get tasks completed this week and organize by priority
    completed_tasks = get_tasks_completed_this_week()
    for task in completed_tasks:
        # Try to classify by project name if available
        project_name = ""
        if task.get("project_ids"):
            # Find matching project
            for project in active_projects:
                if project["id"] in task.get("project_ids", []):
                    project_name = project["title"]
                    break
        
        priority_key = classify_by_strategic_priority(task["title"], project_name)
        priorities_data[priority_key]["tasks_completed"].append(task)
    
    # 4. Get waiting tasks and organize by priority
    waiting_analysis = analyze_waiting_tasks()
    all_waiting = (
        waiting_analysis.get("recent", []) +
        waiting_analysis.get("moderate", []) +
        waiting_analysis.get("need_followup", [])
    )
    
    for waiting_task in all_waiting:
        project_name = ""
        if waiting_task.get("project_ids"):
            for project in active_projects:
                if project["id"] in waiting_task.get("project_ids", []):
                    project_name = project["title"]
                    break
        
        priority_key = classify_by_strategic_priority(waiting_task["title"], project_name)
        priorities_data[priority_key]["blockers"].append(waiting_task)
        
        # Mark as blocked if has blockers
        if waiting_task.get("days_waiting", 0) > 7:
            priorities_data[priority_key]["status"] = "blocked"
    
    # 5. Get action items from last week
    action_items = get_action_items_for_review(days_back=7)
    
    # 6. Build the final response with strategic priority info
    strategic_priorities_config = get_strategic_priorities()
    strategic_priorities = {}
    for key, priority_info in strategic_priorities_config.items():
        data = priorities_data[key]
        strategic_priorities[key] = {
            "name": priority_info.get("name", key.replace("_", " ").title()),
            "display_name": priority_info.get("display_name", priority_info.get("name", key.replace("_", " ").title())),
            "success_metric": priority_info.get("success_metric", ""),
            "deadline": priority_info.get("deadline", ""),
            "status": data["status"],
            "projects": [{
                "title": p["project"]["title"],
                "priority": p["project"].get("priority", ""),
                "health_score": p["health"]["health_score"],
                "health_status": p["health"]["health_status"],
                "active_tasks": p["health"]["active_tasks_count"],
                "overdue_tasks": p["health"]["overdue_tasks_count"],
                "factors": p["health"]["factors"]
            } for p in data["projects"]],
            "tasks_completed_this_week": [{
                "title": t["title"],
                "completed_date": t.get("completed_date")
            } for t in data["tasks_completed"]],
            "blockers": [{
                "title": t["title"],
                "waiting_on": t.get("waiting", []),
                "days_waiting": t.get("days_waiting", 0)
            } for t in data["blockers"]]
        }
    
    # 7. Build summary
    total_completed = len(completed_tasks)
    total_blockers = len(all_waiting)
    priorities_at_risk = sum(1 for p in strategic_priorities.values() if p["status"] == "at_risk")
    priorities_blocked = sum(1 for p in strategic_priorities.values() if p["status"] == "blocked")
    
    summary = {
        "week_ending": today.isoformat(),
        "total_tasks_completed": total_completed,
        "total_blockers": total_blockers,
        "priorities_on_track": 5 - priorities_at_risk - priorities_blocked,
        "priorities_at_risk": priorities_at_risk,
        "priorities_blocked": priorities_blocked,
        "action_items_pending": action_items["summary"]["total_action_items"],
        "action_items_for_rajiv": action_items["summary"]["for_rajiv"]
    }
    
    return {
        "summary": summary,
        "strategic_priorities": strategic_priorities,
        "action_items": {
            "for_rajiv": action_items.get("for_rajiv", [])[:5],  # Top 5
            "waiting_on_others": action_items.get("waiting_on_others", [])[:5],  # Top 5
            "summary": action_items["summary"]
        },
        "other_projects": priorities_data["other"]  # Non-strategic projects
    }
