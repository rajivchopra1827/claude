"""Task Manager Agent - reviews, prioritizes, and manages tasks."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from task_management.tools.task_manager_agent import (
    get_daily_review,
    get_inbox_tasks,
    get_waiting_tasks,
    get_overdue_tasks,
    extract_task_properties,
    query_tasks_by_title,
    update_task,
    batch_update_tasks,
    analyze_priorities,
    find_overdue,
    calculate_waiting_duration,
    get_weekly_review,
    process_action_items,
    create_tasks_from_review_items,
    format_review_item_for_display,
)
from task_management.tools.inbox_agent import search_projects


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('task_manager_agent')


task_manager_agent = Agent(
    name="Task Manager Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="task_manager_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        get_daily_review,
        get_inbox_tasks,
        get_waiting_tasks,
        get_overdue_tasks,
        extract_task_properties,
        query_tasks_by_title,
        update_task,
        batch_update_tasks,
        analyze_priorities,
        find_overdue,
        calculate_waiting_duration,
        get_weekly_review,
        process_action_items,
        create_tasks_from_review_items,
        format_review_item_for_display,
        search_projects,  # For project context
        get_rajiv_context,
    ],
    markdown=True,
)
