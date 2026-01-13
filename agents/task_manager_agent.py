"""Task Manager Agent - reviews, prioritizes, and manages tasks."""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.task_manager_agent import (
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
from tools.inbox_agent import search_projects


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "task_manager_agent.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


task_manager_agent = Agent(
    name="Task Manager Agent",
    model=OpenAIChat(id="gpt-4o"),
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
    ],
    markdown=True,
)
