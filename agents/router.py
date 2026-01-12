"""Router for directing user input to appropriate agent."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agno.agent import Agent

from .inbox_agent import inbox_agent
from .task_manager_agent import task_manager_agent
from .interview_assistant_agent import interview_assistant_agent


def route_to_agent(user_input: str) -> "Agent":
    """Route user input to appropriate agent based on keywords and intent.
    
    Args:
        user_input: User's input text
    
    Returns:
        Appropriate agent instance
    """
    input_lower = user_input.lower()
    
    # Interview signals
    interview_keywords = [
        "interview", "assess candidate", "competency", "evaluate candidate",
        "transcript", "pm candidate", "hiring"
    ]
    if any(keyword in input_lower for keyword in interview_keywords):
        return interview_assistant_agent
    
    # Task manager signals
    task_manager_keywords = [
        "what should i work", "process inbox", "show tasks", "mark done",
        "what am i waiting", "overdue", "daily review", "plan this week",
        "help me plan", "triage", "update task", "move to", "status"
    ]
    if any(keyword in input_lower for keyword in task_manager_keywords):
        return task_manager_agent
    
    # Inbox signals (capture/create)
    inbox_keywords = [
        "save", "remind me", "capture", "add task", "create task",
        "save this", "check out", "found this", "idea:", "customer said"
    ]
    if any(keyword in input_lower for keyword in inbox_keywords):
        return inbox_agent
    
    # Default to inbox for captures (most common case)
    return inbox_agent
