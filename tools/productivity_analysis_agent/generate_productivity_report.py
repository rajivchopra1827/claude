"""Generate comprehensive productivity reports."""

from typing import Dict, Any, Optional
from datetime import date
from tools.productivity_analysis_agent.get_task_history import get_task_history
from tools.productivity_analysis_agent.get_project_history import get_project_history
from tools.productivity_analysis_agent.calculate_productivity_metrics import calculate_productivity_metrics
from tools.productivity_analysis_agent.analyze_time_patterns import analyze_time_patterns
from tools.productivity_analysis_agent.analyze_project_productivity import analyze_project_productivity
from tools.productivity_analysis_agent.identify_bottlenecks import identify_bottlenecks


def generate_productivity_report(
    date_range: Optional[str] = None,
    period: str = "month"
) -> "Dict[str, Any]":
    """Generate a comprehensive productivity report for a time period.
    
    Args:
        date_range: Natural date expression (e.g., "last month", "this week")
        period: Aggregation period for metrics ("day", "week", "month")
    
    Returns:
        Dictionary containing comprehensive productivity report with:
        - summary: High-level summary metrics
        - time_analysis: Time-based productivity analysis
        - project_analysis: Project-based productivity analysis
        - patterns: Productivity patterns identified
        - bottlenecks: Bottlenecks and issues found
        - recommendations: Actionable recommendations
    """
    # Get data
    task_data = get_task_history(date_range=date_range)
    project_data = get_project_history()
    
    tasks = task_data.get("tasks", [])
    projects = project_data.get("projects", [])
    
    # Calculate core metrics
    metrics = calculate_productivity_metrics(tasks, period=period)
    
    # Analyze time patterns
    patterns = analyze_time_patterns(tasks)
    
    # Analyze project productivity
    project_analysis = analyze_project_productivity(projects)
    
    # Identify bottlenecks
    bottlenecks = identify_bottlenecks(tasks, projects)
    
    # Generate summary
    overall_metrics = metrics.get("overall_metrics", {})
    summary = {
        "date_range": date_range or "all time",
        "total_tasks": overall_metrics.get("total_tasks", 0),
        "completed_tasks": overall_metrics.get("completed_tasks", 0),
        "completion_rate": overall_metrics.get("completion_rate", 0),
        "avg_time_to_complete_days": overall_metrics.get("avg_time_to_complete_days"),
        "total_projects": len(projects),
        "active_projects": len([p for p in projects if p.get("priority") != "Done"]),
    }
    
    # Generate recommendations
    recommendations = []
    
    # Based on bottlenecks
    bottlenecks_summary = bottlenecks.get("bottlenecks_summary", {})
    if bottlenecks_summary.get("waiting_tasks_count", 0) > 5:
        recommendations.append(f"Follow up on {bottlenecks_summary['waiting_tasks_count']} waiting tasks")
    
    if bottlenecks_summary.get("overdue_tasks_count", 0) > 3:
        recommendations.append(f"Address {bottlenecks_summary['overdue_tasks_count']} overdue tasks")
    
    if bottlenecks_summary.get("stalled_projects_count", 0) > 0:
        recommendations.append(f"Review {bottlenecks_summary['stalled_projects_count']} stalled projects")
    
    if bottlenecks.get("priority_drift"):
        recommendations.append("Focus more on P1 priority projects")
    
    # Based on patterns
    if patterns.get("weekly_trends", {}).get("trend") == "declining":
        recommendations.append("Productivity has declined recently - consider reviewing priorities")
    
    # Based on project analysis
    slowest_projects = project_analysis.get("slowest_projects", [])
    if slowest_projects:
        top_slow = slowest_projects[0]
        recommendations.append(f"Consider reviewing '{top_slow['title']}' - lowest completion rate")
    
    if not recommendations:
        recommendations.append("Keep up the good work! Productivity looks healthy")
    
    return {
        "summary": summary,
        "time_analysis": {
            "metrics_by_period": metrics.get("metrics_by_period", {}),
            "trends": metrics.get("trends", {}),
            "patterns": patterns
        },
        "project_analysis": project_analysis,
        "bottlenecks": bottlenecks,
        "recommendations": recommendations
    }
