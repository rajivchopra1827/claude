"""Orchestrator Team - intelligently routes user requests to specialized agents."""

from agno.team import Team
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions
from .inbox_agent import inbox_agent
from .slack_inbox_agent import slack_inbox_agent
from .task_manager_agent import task_manager_agent
from .context_gathering_agent import context_gathering_agent
from .interview_assistant_agent import interview_assistant_agent
from .productivity_analysis_agent import productivity_analysis_agent
from .weekly_exec_update_agent import weekly_exec_update_agent


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('orchestrator_team')


orchestrator_team = Team(
    name="AIPOS",
    model=OpenAIChat(id="gpt-4o"),
    members=[
        inbox_agent,
        slack_inbox_agent,
        task_manager_agent,
        context_gathering_agent,
        interview_assistant_agent,
        productivity_analysis_agent,
        weekly_exec_update_agent,
    ],
    db=get_session_storage(table_name="orchestrator_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    respond_directly=True,  # Members respond directly to user
    determine_input_for_members=False,  # Pass input unchanged to members
    instructions=load_instructions(),
    markdown=True,
)
