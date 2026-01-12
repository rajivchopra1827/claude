"""Interview Assistant Agent - analyzes interview transcripts against competency models."""

import os
from agno.agent import Agent
from agno.models.anthropic import Claude
from tools.interview_assistant_agent import (
    fetch_page,
    extract_competencies,
    map_evidence_to_competencies,
)
from tools.interview_assistant_agent.notion_tools import fetch_competency_model


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "interview_assistant_agent.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


interview_assistant_agent = Agent(
    name="Interview Assistant Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=load_instructions(),
    tools=[
        fetch_page,
        fetch_competency_model,
        extract_competencies,
        map_evidence_to_competencies,
    ],
    markdown=True,
)
