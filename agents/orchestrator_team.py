"""Orchestrator Team - intelligently routes user requests to specialized agents."""

import os
from agno.team import Team
from agno.models.openai import OpenAIChat
from .inbox_agent import inbox_agent
from .task_manager_agent import task_manager_agent
from .context_gathering_agent import context_gathering_agent
from .interview_assistant_agent import interview_assistant_agent


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "orchestrator_team.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter (between --- markers)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


orchestrator_team = Team(
    name="Work Hub Orchestrator",
    model=OpenAIChat(id="gpt-4o"),
    members=[
        inbox_agent,
        task_manager_agent,
        context_gathering_agent,
        interview_assistant_agent,
    ],
    respond_directly=True,  # Members respond directly to user
    determine_input_for_members=False,  # Pass input unchanged to members
    instructions=load_instructions(),
    markdown=True,
)
