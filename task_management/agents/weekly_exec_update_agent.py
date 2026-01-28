"""Weekly Exec Update Agent - generates executive updates for leadership."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from task_management.tools.weekly_exec_update_agent import (
    get_weekly_exec_data,
    search_recent_decisions,
)
from task_management.tools.context_gathering_agent import (
    search_transcripts,
    get_transcript_content,
    extract_action_items,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('weekly_exec_update_agent')


weekly_exec_update_agent = Agent(
    name="Weekly Exec Update Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="weekly_exec_update_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        get_weekly_exec_data,
        search_recent_decisions,
        search_transcripts,
        get_transcript_content,
        extract_action_items,
        get_rajiv_context,
    ],
    markdown=True,
)
