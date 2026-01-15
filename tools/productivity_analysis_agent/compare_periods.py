"""Compare productivity between two time periods."""

from typing import Dict, Any, Optional
from tools.productivity_analysis_agent.get_task_history import get_task_history
from tools.productivity_analysis_agent.calculate_productivity_metrics import calculate_productivity_metrics


def compare_periods(
    period1_date_range: str,
    period2_date_range: str
) -> "Dict[str, Any]":
    """Compare productivity between two time periods.
    
    Args:
        period1_date_range: Natural date expression for first period (e.g., "last month")
        period2_date_range: Natural date expression for second period (e.g., "this month")
    
    Returns:
        Dictionary containing:
        - period1_metrics: Metrics for first period
        - period2_metrics: Metrics for second period
        - comparison: Side-by-side comparison with changes
        - insights: Key insights about changes
    """
    # Get tasks for both periods
    period1_data = get_task_history(date_range=period1_date_range)
    period2_data = get_task_history(date_range=period2_date_range)
    
    period1_tasks = period1_data.get("tasks", [])
    period2_tasks = period2_data.get("tasks", [])
    
    # Calculate metrics for both periods
    period1_metrics = calculate_productivity_metrics(period1_tasks, period="month")
    period2_metrics = calculate_productivity_metrics(period2_tasks, period="month")
    
    period1_overall = period1_metrics.get("overall_metrics", {})
    period2_overall = period2_metrics.get("overall_metrics", {})
    
    # Calculate changes
    completion_rate_change = period2_overall.get("completion_rate", 0) - period1_overall.get("completion_rate", 0)
    completed_tasks_change = period2_overall.get("completed_tasks", 0) - period1_overall.get("completed_tasks", 0)
    total_tasks_change = period2_overall.get("total_tasks", 0) - period1_overall.get("total_tasks", 0)
    
    avg_time_change = None
    period1_avg_time = period1_overall.get("avg_time_to_complete_days")
    period2_avg_time = period2_overall.get("avg_time_to_complete_days")
    if period1_avg_time is not None and period2_avg_time is not None:
        avg_time_change = period2_avg_time - period1_avg_time
    
    # Determine if improving or declining
    is_improving = completion_rate_change > 0 and completed_tasks_change >= 0
    is_declining = completion_rate_change < 0 or completed_tasks_change < 0
    
    # Generate insights
    insights = []
    
    if completion_rate_change > 0.1:
        insights.append(f"Completion rate improved significantly (+{completion_rate_change:.1%})")
    elif completion_rate_change < -0.1:
        insights.append(f"Completion rate declined ({completion_rate_change:.1%})")
    
    if completed_tasks_change > 5:
        insights.append(f"Completed {completed_tasks_change} more tasks in period 2")
    elif completed_tasks_change < -5:
        insights.append(f"Completed {abs(completed_tasks_change)} fewer tasks in period 2")
    
    if avg_time_change is not None:
        if avg_time_change < -2:
            insights.append(f"Tasks completed {abs(avg_time_change):.1f} days faster on average")
        elif avg_time_change > 2:
            insights.append(f"Tasks took {avg_time_change:.1f} days longer on average")
    
    if not insights:
        insights.append("Productivity levels remained relatively stable between periods")
    
    comparison = {
        "period1": {
            "date_range": period1_date_range,
            "total_tasks": period1_overall.get("total_tasks", 0),
            "completed_tasks": period1_overall.get("completed_tasks", 0),
            "completion_rate": period1_overall.get("completion_rate", 0),
            "avg_time_to_complete_days": period1_avg_time
        },
        "period2": {
            "date_range": period2_date_range,
            "total_tasks": period2_overall.get("total_tasks", 0),
            "completed_tasks": period2_overall.get("completed_tasks", 0),
            "completion_rate": period2_overall.get("completion_rate", 0),
            "avg_time_to_complete_days": period2_avg_time
        },
        "changes": {
            "completion_rate_change": completion_rate_change,
            "completed_tasks_change": completed_tasks_change,
            "total_tasks_change": total_tasks_change,
            "avg_time_to_complete_change": avg_time_change
        },
        "trend": "improving" if is_improving else "declining" if is_declining else "stable"
    }
    
    return {
        "period1_metrics": period1_metrics,
        "period2_metrics": period2_metrics,
        "comparison": comparison,
        "insights": insights
    }
