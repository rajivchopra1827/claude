"""Analyze productivity across different projects."""

from typing import Dict, Any, List, Optional
from collections import defaultdict


def analyze_project_productivity(
    projects: "List[Dict[str, Any]]",
    priority_filter: Optional[str] = None
) -> "Dict[str, Any]":
    """Compare productivity across projects.
    
    Args:
        projects: List of project dictionaries with task_metrics
        priority_filter: Optional filter by priority (P1, P2, P3)
    
    Returns:
        Dictionary containing:
        - projects_by_velocity: Projects ranked by completion velocity
        - projects_by_priority: Projects grouped by priority
        - priority_comparison: Productivity comparison across priorities
        - fastest_projects: Top performing projects
        - slowest_projects: Projects needing attention
    """
    # Filter by priority if specified
    if priority_filter:
        projects = [p for p in projects if p.get("priority") == priority_filter]
    
    if not projects:
        return {
            "projects_by_velocity": [],
            "projects_by_priority": {},
            "priority_comparison": {},
            "fastest_projects": [],
            "slowest_projects": []
        }
    
    # Group projects by priority
    projects_by_priority = defaultdict(list)
    for project in projects:
        priority = project.get("priority") or "None"
        projects_by_priority[priority].append(project)
    
    # Calculate velocity (completion rate weighted by project age)
    projects_with_velocity = []
    for project in projects:
        task_metrics = project.get("task_metrics", {})
        completion_rate = task_metrics.get("completion_rate", 0)
        project_age_days = task_metrics.get("project_age_days")
        total_tasks = task_metrics.get("total_tasks", 0)
        
        # Velocity = completion rate, but also consider project age
        # Older projects with high completion rates are good
        # Newer projects with high completion rates are excellent
        velocity_score = completion_rate
        
        # Adjust for project age (newer projects get slight boost)
        if project_age_days and project_age_days > 0:
            # Normalize: projects older than 90 days get full weight
            age_factor = min(project_age_days / 90.0, 1.0)
            velocity_score = completion_rate * (1.0 + (1.0 - age_factor) * 0.1)
        
        projects_with_velocity.append({
            "project": project,
            "velocity_score": velocity_score,
            "completion_rate": completion_rate,
            "total_tasks": total_tasks,
            "completed_tasks": task_metrics.get("completed_tasks", 0),
            "project_age_days": project_age_days
        })
    
    # Sort by velocity
    projects_with_velocity.sort(key=lambda x: x["velocity_score"], reverse=True)
    
    # Calculate priority comparison
    priority_comparison = {}
    for priority, priority_projects in projects_by_priority.items():
        if not priority_projects:
            continue
        
        total_completion_rate = sum(
            p.get("task_metrics", {}).get("completion_rate", 0)
            for p in priority_projects
        )
        avg_completion_rate = total_completion_rate / len(priority_projects)
        
        total_tasks = sum(
            p.get("task_metrics", {}).get("total_tasks", 0)
            for p in priority_projects
        )
        total_completed = sum(
            p.get("task_metrics", {}).get("completed_tasks", 0)
            for p in priority_projects
        )
        
        priority_comparison[priority] = {
            "project_count": len(priority_projects),
            "avg_completion_rate": avg_completion_rate,
            "total_tasks": total_tasks,
            "total_completed": total_completed,
            "overall_completion_rate": total_completed / total_tasks if total_tasks > 0 else 0
        }
    
    # Identify fastest and slowest projects (top/bottom 25%)
    num_projects = len(projects_with_velocity)
    top_n = max(1, num_projects // 4) if num_projects >= 4 else num_projects
    bottom_n = max(1, num_projects // 4) if num_projects >= 4 else num_projects
    
    fastest_projects = [
        {
            "title": p["project"].get("title"),
            "priority": p["project"].get("priority"),
            "completion_rate": p["completion_rate"],
            "total_tasks": p["total_tasks"],
            "completed_tasks": p["completed_tasks"],
            "velocity_score": p["velocity_score"]
        }
        for p in projects_with_velocity[:top_n]
    ]
    
    slowest_projects = [
        {
            "title": p["project"].get("title"),
            "priority": p["project"].get("priority"),
            "completion_rate": p["completion_rate"],
            "total_tasks": p["total_tasks"],
            "completed_tasks": p["completed_tasks"],
            "velocity_score": p["velocity_score"]
        }
        for p in projects_with_velocity[-bottom_n:]
    ]
    
    return {
        "projects_by_velocity": [
            {
                "title": p["project"].get("title"),
                "priority": p["project"].get("priority"),
                "completion_rate": p["completion_rate"],
                "total_tasks": p["total_tasks"],
                "completed_tasks": p["completed_tasks"],
                "velocity_score": p["velocity_score"]
            }
            for p in projects_with_velocity
        ],
        "projects_by_priority": {
            priority: [
                {
                    "title": p.get("title"),
                    "completion_rate": p.get("task_metrics", {}).get("completion_rate", 0),
                    "total_tasks": p.get("task_metrics", {}).get("total_tasks", 0),
                    "completed_tasks": p.get("task_metrics", {}).get("completed_tasks", 0)
                }
                for p in priority_projects
            ]
            for priority, priority_projects in projects_by_priority.items()
        },
        "priority_comparison": priority_comparison,
        "fastest_projects": fastest_projects,
        "slowest_projects": slowest_projects
    }
