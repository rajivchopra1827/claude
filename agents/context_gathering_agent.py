"""Context Gathering Agent - finds and summarizes information from Notion."""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.common import get_session_storage, get_rajiv_context
from tools.context_gathering_agent import (
    search_transcripts,
    get_transcript,
    get_transcript_content,
    extract_action_items_from_transcript,
    extract_action_items_from_notes,
)


def load_instructions() -> str:
    """Load instructions from markdown file with Rajiv context injected."""
    from tools.common import load_agent_instructions
    return load_agent_instructions('context_gathering_agent')


context_gathering_agent = Agent(
    name="Context Gathering Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=get_session_storage(table_name="context_gathering_agent_sessions"),
    add_history_to_context=True,
    num_history_runs=3,
    instructions=load_instructions(),
    tools=[
        search_transcripts,
        get_transcript,
        get_transcript_content,
        extract_action_items_from_transcript,
        extract_action_items_from_notes,
        get_rajiv_context,
    ],
    markdown=True,
)
