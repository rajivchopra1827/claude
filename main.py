"""Main entry point for Cursor chat integration."""

from agents.router import route_to_agent


def handle_chat(user_input: str) -> str:
    """Handle user input from Cursor chat.
    
    Args:
        user_input: User's natural language input
    
    Returns:
        Agent's response as string
    """
    agent = route_to_agent(user_input)
    response = agent.run(user_input)
    return response.content


if __name__ == "__main__":
    # For testing/CLI usage
    import sys
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = handle_chat(user_input)
        print(result)
    else:
        print("Usage: python main.py <your message>")
        print("Example: python main.py 'What should I work on today?'")
