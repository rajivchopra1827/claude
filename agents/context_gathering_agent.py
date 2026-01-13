"""Context Gathering Agent - finds and summarizes information from Notion."""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.context_gathering_agent import (
    search_transcripts,
    get_transcript,
    get_transcript_content,
    extract_action_items_from_transcript,
    extract_action_items_from_notes,
)


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "context_gathering_agent.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter (between --- markers)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


context_gathering_agent = Agent(
    name="Context Gathering Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=load_instructions(),
    tools=[
        search_transcripts,
        get_transcript,
        get_transcript_content,
        extract_action_items_from_transcript,
        extract_action_items_from_notes,
    ],
    markdown=True,
)
