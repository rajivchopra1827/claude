"""Productivity Analysis Agent - analyzes productivity metrics and patterns."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from tools.productivity_analysis_agent import (
    get_task_history,
    get_project_history,
    calculate_productivity_metrics,
    analyze_time_patterns,
    analyze_project_productivity,
    identify_bottlenecks,
    generate_productivity_report,
    compare_periods,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('productivity_analysis_agent')


productivity_analysis_agent = Agent(
    name="Productivity Analysis Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="productivity_analysis_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        get_task_history,
        get_project_history,
        calculate_productivity_metrics,
        analyze_time_patterns,
        analyze_project_productivity,
        identify_bottlenecks,
        generate_productivity_report,
        compare_periods,
        get_rajiv_context,
    ],
    markdown=True,
)
