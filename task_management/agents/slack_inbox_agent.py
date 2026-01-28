"""Slack Inbox Agent - processes Slack messages and organizes them into Notion."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from task_management.tools.slack_inbox_agent import (
    get_unread_messages,
    get_conversation_history,
    classify_slack_message,
    process_slack_messages,
)
from task_management.tools.inbox_agent import (
    create_task,
    create_resource,
    create_idea,
    search_projects,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('slack_inbox_agent')


slack_inbox_agent = Agent(
    name="Slack Inbox Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="slack_inbox_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        get_unread_messages,
        get_conversation_history,
        classify_slack_message,
        process_slack_messages,
        create_task,
        create_resource,
        create_idea,
        search_projects,
        get_rajiv_context,
    ],
    markdown=True,
)
