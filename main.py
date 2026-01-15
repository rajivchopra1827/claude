"""Main entry point for Cursor chat integration."""

from agents.orchestrator_team import orchestrator_team
from agno.run.agent import RunEvent
from agno.run.team import TeamRunEvent
from tools.common.visual_formatter import (
    console,
    print_agent_header,
    print_tool_call,
    print_tool_success,
    print_thinking,
    print_error,
    print_separator,
    format_agent_name,
    print_aipos_greeting,
    print_contextual_comment,
)


def handle_chat(user_input: str) -> str:
    """Handle user input from Cursor chat.
    
    Args:
        user_input: User's natural language input
    
    Returns:
        Agent's response as string
    """
    response = orchestrator_team.run(user_input)
    return response.content


def get_greeting_context() -> dict:
    """Gather context for startup greeting - task counts and status."""
    try:
        from tools.task_manager_agent.get_tasks_by_status import get_tasks_by_status
        from tools.task_manager_agent import get_overdue_tasks
        from datetime import date
        
        # Get task counts
        inbox_tasks = get_tasks_by_status("Inbox")
        overdue_tasks = get_overdue_tasks()
        
        # Get tasks completed today
        from tools.common import query_database_complete, TASKS_DATA_SOURCE_ID
        today = date.today().isoformat()
        completed_today = query_database_complete(
            TASKS_DATA_SOURCE_ID,
            filter_dict={
                "and": [
                    {"property": "Status", "status": {"equals": "Done"}},
                    {"property": "Completed", "date": {"equals": today}}
                ]
            },
            use_data_source=True
        )
        
        return {
            "unread_tasks": len(inbox_tasks),
            "overdue_tasks": len(overdue_tasks),
            "completed_today": len(completed_today),
        }
    except Exception:
        # If we can't get context, return empty dict - greeting will use fallback
        return {}


def interactive_cli():
    """Run an interactive CLI session with the agents."""
    console.print("[bold cyan]=" * 60)
    console.print("[bold cyan]🤖 AIPOS - AI Personal Operating System[/bold cyan]")
    console.print("[bold cyan]=" * 60)
    console.print()
    
    # Gather context for greeting
    context = get_greeting_context()
    print_aipos_greeting(context=context)
    
    console.print("Type your questions or commands. Type 'quit', 'exit', or 'q' to end.\n")
    
    while True:
        try:
            # Get user input
            console.print("[bold bright_white]You:[/bold bright_white] ", end="")
            user_input = input().strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                console.print()
                console.print("[bold cyan]AIPOS offline.[/bold cyan]")
                console.print()
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Stream response from orchestrator team
            # With respond_directly=True, members respond directly when delegated.
            # However, the team leader can also respond directly (e.g., for meta questions).
            # Strategy: Track if we've seen member responses. If yes, only print member content.
            # If no member responses, print team leader content (direct response without delegation).
            # Use stream_events=True to capture tool call events
            try:
                stream = orchestrator_team.run(user_input, stream=True, stream_events=True)
            except TypeError:
                # Fallback if stream_events parameter doesn't exist
                stream = orchestrator_team.run(user_input, stream=True)
            has_member_response = False
            current_agent_name = None
            thinking_shown = False
            tool_calls_shown = set()
            
            for chunk in stream:
                # Handle team run started
                if chunk.event == TeamRunEvent.run_started:
                    thinking_shown = True
                    print_thinking()
                
                # Handle tool call started (both team and agent level)
                if chunk.event in [TeamRunEvent.tool_call_started, RunEvent.tool_call_started]:
                    tool_name = None
                    # Try multiple ways to get tool name
                    if hasattr(chunk, 'tool_name'):
                        tool_name = chunk.tool_name
                    elif hasattr(chunk, 'tool'):
                        tool_obj = chunk.tool
                        if isinstance(tool_obj, dict):
                            tool_name = tool_obj.get('tool_name') or tool_obj.get('name')
                        elif hasattr(tool_obj, 'tool_name'):
                            tool_name = tool_obj.tool_name
                        elif hasattr(tool_obj, 'name'):
                            tool_name = tool_obj.name
                        elif hasattr(tool_obj, '__name__'):
                            tool_name = tool_obj.__name__
                    
                    if tool_name and tool_name not in tool_calls_shown:
                        print_tool_call(tool_name)
                        tool_calls_shown.add(tool_name)
                
                # Handle tool call completed
                if chunk.event in [TeamRunEvent.tool_call_completed, RunEvent.tool_call_completed]:
                    tool_name = None
                    # Try multiple ways to get tool name
                    if hasattr(chunk, 'tool_name'):
                        tool_name = chunk.tool_name
                    elif hasattr(chunk, 'tool'):
                        tool_obj = chunk.tool
                        if isinstance(tool_obj, dict):
                            tool_name = tool_obj.get('tool_name') or tool_obj.get('name')
                        elif hasattr(tool_obj, 'tool_name'):
                            tool_name = tool_obj.tool_name
                        elif hasattr(tool_obj, 'name'):
                            tool_name = tool_obj.name
                        elif hasattr(tool_obj, '__name__'):
                            tool_name = tool_obj.__name__
                    
                    if tool_name:
                        print_tool_success(tool_name)
                    else:
                        print_tool_success()
                
                # Handle agent name and content when we detect an agent is responding
                if chunk.event == RunEvent.run_content:
                    # Try to get agent name/ID from various possible attributes
                    agent_name = None
                    agent_id = None
                    
                    # Try different ways to get agent information
                    if hasattr(chunk, 'agent_id'):
                        agent_id = chunk.agent_id
                    elif hasattr(chunk, 'agent'):
                        agent_id = chunk.agent
                    elif hasattr(chunk, 'run') and hasattr(chunk.run, 'agent'):
                        agent_obj = chunk.run.agent
                        if hasattr(agent_obj, 'name'):
                            agent_name = agent_obj.name
                        elif hasattr(agent_obj, 'id'):
                            agent_id = agent_obj.id
                    
                    # If we have agent_id but not name, try to find name from team members
                    if agent_id and not agent_name:
                        for member in orchestrator_team.members:
                            if hasattr(member, 'id') and str(member.id) == str(agent_id):
                                agent_name = getattr(member, 'name', None)
                                break
                            elif hasattr(member, 'name') and str(member.name) == str(agent_id):
                                agent_name = member.name
                                break
                            elif str(member) == str(agent_id):
                                agent_name = getattr(member, 'name', str(agent_id))
                                break
                    
                    # If we still don't have a name, use agent_id or default
                    if not agent_name:
                        agent_name = agent_id if agent_id else "Agent"
                    
                    # Show agent header if this is a new agent responding
                    if agent_name and agent_name != current_agent_name:
                        current_agent_name = agent_name
                        if not has_member_response:
                            print_separator()
                            print_agent_header(agent_name)
                    
                    # Mark that we have a member response and print content
                    has_member_response = True
                    if chunk.content:
                        console.print(chunk.content, end='', markup=False)
                
                # Only print team leader content if no member has responded
                # (team leader responding directly, e.g., for meta questions)
                elif chunk.event == TeamRunEvent.run_content and not has_member_response:
                    if chunk.content:
                        console.print(chunk.content, end='', markup=False)
                
                # Handle team run completed
                if chunk.event == TeamRunEvent.run_completed:
                    pass  # Completion handled by content display
            
            print_separator()
            
        except KeyboardInterrupt:
            console.print("\n")
            console.print("[bold cyan]AIPOS interrupted.[/bold cyan]")
            console.print()
            break
        except Exception as e:
            print_error(str(e))
            console.print()


if __name__ == "__main__":
    import sys
    
    # Check for interactive mode flag or no arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-i', '--interactive', 'interactive']:
            interactive_cli()
        else:
            # One-shot mode: process the message
            user_input = " ".join(sys.argv[1:])
            result = handle_chat(user_input)
            console.print(result)
    else:
        # Default to interactive mode when no arguments
        interactive_cli()
