"""Interview Assistant Agent - analyzes interview transcripts against competency models."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, load_agent_instructions, get_rajiv_context
from task_management.tools.interview_assistant_agent import (
    fetch_page,
    extract_competencies,
    map_evidence_to_competencies,
    fetch_competency_model,
    fetch_scorecard,
    find_candidate_transcripts,
    analyze_transcript,
    analyze_transcript_from_page_id,
    generate_summary,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    return load_agent_instructions('interview_assistant_agent')


interview_assistant_agent = Agent(
    name="Interview Assistant Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="interview_assistant_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        fetch_page,
        fetch_competency_model,
        extract_competencies,
        map_evidence_to_competencies,
        fetch_scorecard,
        find_candidate_transcripts,
        analyze_transcript,
        analyze_transcript_from_page_id,
        generate_summary,
        get_rajiv_context,
    ],
    markdown=True,
)
