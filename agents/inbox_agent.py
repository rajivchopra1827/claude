"""Inbox Agent - captures tasks, resources, and insights."""

import os
import re
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.inbox_agent import (
    create_task,
    create_resource,
    create_insight,
    search_projects,
    fetch_url_metadata,
    infer_resource_type,
    classify_input,
    extract_metadata,
)


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "inbox_agent.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter (between --- markers)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


inbox_agent = Agent(
    name="Inbox Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=load_instructions(),
    tools=[
        create_task,
        create_resource,
        create_insight,
        search_projects,
        fetch_url_metadata,
        infer_resource_type,
        classify_input,
        extract_metadata,
    ],
    markdown=True,
)
