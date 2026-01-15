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
    "aipos": "🤖",
    "celebration": "🎉",
    "easter_egg": "🥚",
    "witty": "💭",
}


def get_agent_color(agent_name: str) -> str:
    """Get color for an agent based on its name."""
    name_lower = agent_name.lower()
    if "aipos" in name_lower:
        return "cyan"  # AIPOS gets special cyan color
    elif "inbox" in name_lower:
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
    if "aipos" in name_lower:
        return ICONS["aipos"]  # AIPOS gets special icon
    elif "inbox" in name_lower:
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


def format_aipos_greeting(time_of_day: Optional[str] = None, context: Optional[dict] = None) -> Text:
    """Format AIPOS greeting with deadpan absurdist personality.
    
    Args:
        time_of_day: Optional time of day ('morning', 'afternoon', 'evening', 'late_night', 'early_morning')
        context: Optional dict with context info (e.g., {'unread_tasks': 23, 'hours_until_meeting': 7})
    
    Returns:
        Formatted greeting text with deadpan observation
    """
    from datetime import datetime
    
    now = datetime.now()
    hour = now.hour
    
    # Determine time of day if not provided
    if not time_of_day:
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "late_night"
    
    # Generate deadpan greeting based on context
    greeting = None
    
    if context:
        unread_tasks = context.get('unread_tasks', 0)
        hours_until_meeting = context.get('hours_until_meeting', None)
        days_since_last_use = context.get('days_since_last_use', None)
        scheduled_hours = context.get('scheduled_hours', None)
        meeting_hours = context.get('meeting_hours', None)
        completed_today = context.get('completed_today', 0)
        overdue_tasks = context.get('overdue_tasks', 0)
        
        time_str = now.strftime('%I:%M%p')
        
        # Prioritize most absurd observations with ironic endings
        if completed_today == 0 and overdue_tasks > 0:
            greeting = f"AIPOS operational. It is {time_str}. You have {completed_today} tasks marked as complete today and {overdue_tasks} marked as overdue. Well done."
        elif unread_tasks > 20:
            greeting = f"AIPOS active. It is {time_str}. You have {unread_tasks} unread tasks. You have processed {completed_today} tasks today. Excellent progress."
        elif time_of_day == "late_night" and hours_until_meeting:
            greeting = f"AIPOS initialized. It is {time_str}. You have {unread_tasks} unread tasks and {hours_until_meeting} hours until your first meeting. Rest well."
        elif days_since_last_use and days_since_last_use > 0:
            greeting = f"AIPOS ready. It is {time_str}. You last used this system {days_since_last_use} days ago. Your inbox has grown by {unread_tasks} items in your absence. Welcome back."
        elif scheduled_hours and meeting_hours:
            total_hours = scheduled_hours + meeting_hours
            greeting = f"AIPOS online. It is {time_str}. You have scheduled {scheduled_hours} hours of work today and {meeting_hours} hours of meetings. A productive day ahead."
        elif overdue_tasks > 0:
            greeting = f"AIPOS ready. It is {time_str}. You have {overdue_tasks} overdue tasks and {unread_tasks} unread tasks. Keep it up."
        elif unread_tasks > 0:
            greeting = f"AIPOS ready. It is {time_str}. You have {unread_tasks} unread tasks. Off to a good start."
    
    # Fallback to simple time-based greeting
    if not greeting:
        time_str = now.strftime('%I:%M%p')
        if time_of_day == "late_night":
            greeting = f"AIPOS initialized. It is {time_str}."
        elif time_of_day == "early_morning":
            greeting = f"AIPOS initialized. It is {time_str}."
        else:
            greeting = f"AIPOS ready. It is {time_str}."
    
    text = Text(f"{ICONS['aipos']} {greeting}")
    text.stylize("bold cyan")
    return text


def format_celebration(message: str, milestone: Optional[str] = None) -> Text:
    """Format celebration message for wins and milestones.
    
    Args:
        message: Celebration message
        milestone: Optional milestone description
    
    Returns:
        Formatted celebration text
    """
    if milestone:
        text = Text(f"{ICONS['celebration']} {message} ({milestone})")
    else:
        text = Text(f"{ICONS['celebration']} {message}")
    text.stylize("bold green")
    return text


def format_easter_egg(message: str, subtle: bool = True) -> Text:
    """Format easter egg message - hidden surprises.
    
    Args:
        message: Easter egg message
        subtle: If True, use subtle styling; if False, more prominent
    
    Returns:
        Formatted easter egg text
    """
    if subtle:
        text = Text(f"{ICONS['easter_egg']} {message}")
        text.stylize("dim italic cyan")
    else:
        text = Text(f"{ICONS['easter_egg']} {message}")
        text.stylize("bold cyan")
    return text


def format_contextual_comment(message: str, tone: str = "witty") -> Text:
    """Format contextual comment - witty observations.
    
    Args:
        message: Comment message
        tone: Tone of comment ('witty', 'observational', 'encouraging')
    
    Returns:
        Formatted comment text
    """
    icon = ICONS.get("witty", "💭")
    
    if tone == "encouraging":
        text = Text(f"💪 {message}")
        text.stylize("dim green")
    elif tone == "observational":
        text = Text(f"👀 {message}")
        text.stylize("dim yellow")
    else:  # witty
        text = Text(f"{icon} {message}")
        text.stylize("dim italic cyan")
    
    return text


def print_aipos_greeting(time_of_day: Optional[str] = None, context: Optional[dict] = None):
    """Print AIPOS greeting with deadpan absurdist observation."""
    greeting_text = format_aipos_greeting(time_of_day, context)
    console.print(greeting_text)
    console.print()


def print_celebration(message: str, milestone: Optional[str] = None):
    """Print celebration message."""
    celebration_text = format_celebration(message, milestone)
    console.print(celebration_text)
    console.print()


def print_easter_egg(message: str, subtle: bool = True):
    """Print easter egg message."""
    egg_text = format_easter_egg(message, subtle)
    console.print(egg_text)


def print_contextual_comment(message: str, tone: str = "witty"):
    """Print contextual comment."""
    comment_text = format_contextual_comment(message, tone)
    console.print(comment_text)
