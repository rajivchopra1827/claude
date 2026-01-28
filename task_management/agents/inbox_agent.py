"""Inbox Agent - captures tasks, resources, and ideas."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from task_management.tools.inbox_agent import (
    create_task,
    create_resource,
    create_idea,
    search_projects,
    fetch_url_metadata,
    infer_resource_type,
    classify_input,
    extract_metadata,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('inbox_agent')


inbox_agent = Agent(
    name="Inbox Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="inbox_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        create_task,
        create_resource,
        create_idea,
        search_projects,
        fetch_url_metadata,
        infer_resource_type,
        classify_input,
        extract_metadata,
        get_rajiv_context,
    ],
    markdown=True,
)
