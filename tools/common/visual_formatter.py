"""Visual formatting utilities for CLI output."""

from typing import Optional
from rich.console import Console
from rich.text import Text

# Initialize console
console = Console()

# Color scheme
COLORS = {
    "agent_inbox": "cyan",
    "agent_task_manager": "blue",
    "agent_interview": "magenta",
    "agent_context": "green",
    "agent_orchestrator": "yellow",
    "tool_call": "yellow",
    "tool_success": "green",
    "thinking": "dim white",
    "error": "red",
    "user": "bright_white",
}

# Icon mappings
ICONS = {
    "thinking": "🤔",
    "tool": "🔧",
    "success": "✅",
    "error": "❌",
    "agent": "🤖",
    "inbox": "📥",
    "task": "📋",
    "interview": "🎯",
    "context": "🔍",
    "orchestrator": "🎭",
}


def get_agent_color(agent_name: str) -> str:
    """Get color for an agent based on its name."""
    name_lower = agent_name.lower()
    if "inbox" in name_lower:
        return COLORS["agent_inbox"]
    elif "task" in name_lower or "manager" in name_lower:
        return COLORS["agent_task_manager"]
    elif "interview" in name_lower:
        return COLORS["agent_interview"]
    elif "context" in name_lower or "gathering" in name_lower:
        return COLORS["agent_context"]
    elif "orchestrator" in name_lower or "team" in name_lower:
        return COLORS["agent_orchestrator"]
    else:
        return COLORS["agent_orchestrator"]


def get_agent_icon(agent_name: str) -> str:
    """Get icon for an agent based on its name."""
    name_lower = agent_name.lower()
    if "inbox" in name_lower:
        return ICONS["inbox"]
    elif "task" in name_lower or "manager" in name_lower:
        return ICONS["task"]
    elif "interview" in name_lower:
        return ICONS["interview"]
    elif "context" in name_lower or "gathering" in name_lower:
        return ICONS["context"]
    elif "orchestrator" in name_lower or "team" in name_lower:
        return ICONS["orchestrator"]
    else:
        return ICONS["agent"]


def format_agent_name(agent_name: str) -> Text:
    """Format agent name with color and icon."""
    icon = get_agent_icon(agent_name)
    color = get_agent_color(agent_name)
    text = Text(f"{icon} {agent_name}")
    text.stylize(f"bold {color}")
    return text


def format_tool_call(tool_name: str) -> Text:
    """Format tool call message."""
    text = Text(f"{ICONS['tool']} Using {tool_name}...")
    text.stylize(COLORS["tool_call"])
    return text


def format_tool_success(tool_name: Optional[str] = None) -> Text:
    """Format tool success message."""
    if tool_name:
        text = Text(f"{ICONS['success']} {tool_name} completed")
    else:
        text = Text(f"{ICONS['success']} Completed")
    text.stylize(COLORS["tool_success"])
    return text


def format_thinking() -> Text:
    """Format thinking indicator."""
    text = Text(f"{ICONS['thinking']} Thinking...")
    text.stylize(COLORS["thinking"])
    return text


def format_error(message: str) -> Text:
    """Format error message."""
    text = Text(f"{ICONS['error']} {message}")
    text.stylize(COLORS["error"])
    return text


def print_agent_header(agent_name: str):
    """Print a styled header for agent responses."""
    agent_text = format_agent_name(agent_name)
    console.print(agent_text)
    console.print()  # Blank line


def print_tool_call(tool_name: str):
    """Print tool call indicator."""
    tool_text = format_tool_call(tool_name)
    console.print(tool_text)


def print_tool_success(tool_name: Optional[str] = None):
    """Print tool success indicator."""
    success_text = format_tool_success(tool_name)
    console.print(success_text)


def print_thinking():
    """Print thinking indicator."""
    thinking_text = format_thinking()
    console.print(thinking_text)


def print_error(message: str):
    """Print error message."""
    error_text = format_error(message)
    console.print(error_text)


def print_separator():
    """Print a visual separator."""
    console.print()  # Blank line
