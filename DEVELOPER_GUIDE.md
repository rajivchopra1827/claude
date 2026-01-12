# Developer Guide

Guide for extending and maintaining Rajiv's Work Hub agent system.

## Architecture Overview

This system uses the [Agno framework](https://docs.agno.com/) to build AI agents that combine:
- **LLM reasoning** (Claude Sonnet) for decision-making
- **Deterministic tools** (Python functions) for reliable operations
- **Instructions** (markdown files) for agent behavior

## Project Structure

```
/
├── agents/                    # Agno agent definitions
│   ├── __init__.py
│   ├── inbox_agent.py        # Inbox Agent
│   ├── task_manager_agent.py # Task Manager Agent
│   ├── interview_assistant_agent.py
│   └── router.py            # Routes user input to agents
│
├── tools/                     # Deterministic tools
│   ├── common/               # Shared utilities (NEW)
│   │   ├── __init__.py
│   │   ├── notion_client.py  # get_notion_client, query_database_complete
│   │   └── constants.py      # Database IDs, shared constants
│   │
│   ├── inbox_agent/
│   │   ├── notion_tools.py  # create_task, create_resource, etc.
│   │   ├── url_tools.py      # fetch_url_metadata, infer_resource_type
│   │   └── classification_tools.py
│   ├── task_manager_agent/
│   │   ├── query_tools.py    # get_daily_review, get_inbox_tasks, etc.
│   │   ├── update_tools.py   # update_task, batch_update_tasks
│   │   └── analysis_tools.py # analyze_priorities, find_overdue
│   └── interview_assistant_agent/
│       ├── notion_tools.py   # fetch_page, fetch_competency_model
│       └── analysis_tools.py # extract_competencies
│
├── .claude/agents/           # Agent instructions (markdown)
│   ├── inbox-ingester.md
│   ├── task-manager.md
│   └── interview-assistant.md
│
└── main.py                   # Entry point
```

## Adding a New Agent

### Step 1: Create Agent Instructions

Create a markdown file in `.claude/agents/` with agent instructions:

```markdown
---
name: my-new-agent
description: "What this agent does"
model: sonnet
---

# My New Agent

You are an agent that does X, Y, Z.

## Your Mission
...

## Tools Available
- `create_thing()` - Creates a thing
- `update_thing()` - Updates a thing
...
```

### Step 2: Create Tools

Create a directory `tools/my_new_agent/` and add tool modules:

```python
# tools/my_new_agent/__init__.py
from .notion_tools import create_thing, update_thing

__all__ = ["create_thing", "update_thing"]

# tools/my_new_agent/notion_tools.py
def create_thing(name: str, status: str = "Active") -> Dict[str, Any]:
    """Create a new thing in Notion.
    
    Args:
        name: Thing name
        status: Thing status
    
    Returns:
        Created thing page object
    """
    # Implementation using Notion API
    ...
```

**Tool Guidelines:**
- Use clear docstrings with Args and Returns sections
- Include type hints
- Handle errors gracefully
- Return structured data (dicts with id, url, etc.)

### Step 3: Create Agent File

Create `agents/my_new_agent.py`:

```python
"""My New Agent - does X, Y, Z."""

import os
from agno.agent import Agent
from agno.models.anthropic import Claude
from tools.my_new_agent import create_thing, update_thing


def load_instructions() -> str:
    """Load instructions from markdown file."""
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".claude",
        "agents",
        "my-new-agent.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()


my_new_agent = Agent(
    name="My New Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=load_instructions(),
    tools=[
        create_thing,
        update_thing,
    ],
    markdown=True,
)
```

### Step 4: Add to Router

Update `agents/router.py` to route to your agent:

```python
from .my_new_agent import my_new_agent

def route_to_agent(user_input: str) -> "Agent":
    input_lower = user_input.lower()
    
    # My new agent signals
    if any(keyword in input_lower for keyword in ["my keyword", "another keyword"]):
        return my_new_agent
    
    # ... existing routing logic
```

### Step 5: Export Agent

Add to `agents/__init__.py`:

```python
from .my_new_agent import my_new_agent

__all__ = [..., "my_new_agent"]
```

## Adding Tools to Existing Agent

### Step 1: Create Tool Function

Add to appropriate tool module (e.g., `tools/inbox_agent/notion_tools.py`):

```python
def new_tool_function(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """Description of what this tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (optional)
    
    Returns:
        Dictionary with results
    """
    # Implementation
    ...
```

### Step 2: Export Tool

Add to `tools/inbox_agent/__init__.py`:

```python
from .notion_tools import new_tool_function

__all__ = [..., "new_tool_function"]
```

### Step 3: Register Tool

Add to agent's tools list in `agents/inbox_agent.py`:

```python
from tools.inbox_agent import new_tool_function

inbox_agent = Agent(
    ...
    tools=[
        ...,
        new_tool_function,
    ],
)
```

## Tool Development Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
def my_tool(param: str) -> Dict[str, Any]:
    try:
        # Do something
        result = do_operation(param)
        return {"success": True, "data": result}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
```

### 2. Type Hints

Always include type hints:

```python
from typing import List, Dict, Any, Optional

def my_tool(
    name: str,
    items: List[str],
    optional_param: Optional[int] = None
) -> Dict[str, Any]:
    ...
```

### 3. Docstrings

Use clear docstrings with Args and Returns:

```python
def my_tool(param: str) -> Dict[str, Any]:
    """Brief description.
    
    Longer description explaining what this tool does and when to use it.
    
    Args:
        param: Description of parameter
    
    Returns:
        Dictionary with:
        - success: bool indicating success
        - data: result data if successful
        - error: error message if failed
    """
    ...
```

### 4. Shared Utilities (`tools/common/`)

All agents share common utilities in `tools/common/` to avoid code duplication:

**`notion_client.py`**:
- `get_notion_client()` - Returns singleton Notion API client
- `query_database_complete()` - Queries Notion database with automatic pagination

**`constants.py`**:
- Database IDs (e.g., `TASKS_DB_ID`, `PROJECTS_DB_ID`)
- Data source IDs (e.g., `TASKS_DATA_SOURCE_ID`)
- Other shared constants (e.g., `PM_COMPETENCY_MODEL_ID`)

**Usage in tools:**
```python
from tools.common import get_notion_client, query_database_complete, TASKS_DB_ID

# Get client
client = get_notion_client()

# Query with pagination
results = query_database_complete(
    database_id=TASKS_DB_ID,
    filter_dict={"property": "Status", "status": {"equals": "Active"}},
    use_data_source=True
)
```

**Benefits:**
- Single source of truth for Notion client initialization
- Consistent pagination handling across all agents
- Centralized database IDs - easier to update if schemas change
- Reduces code duplication

### 5. Notion API Patterns

When working with Notion in your tools:

```python
# Import shared utilities
from tools.common import get_notion_client, query_database_complete, TASKS_DB_ID

# Get client
client = get_notion_client()

# Create page
page = client.pages.create(
    parent={"database_id": TASKS_DB_ID},
    properties={
        "Name": {"title": [{"text": {"content": name}}]},
        "Status": {"status": {"name": status}}
    }
)

# Query database (use query_database_complete for pagination)
results = query_database_complete(
    database_id=TASKS_DB_ID,
    filter_dict={"property": "Status", "status": {"equals": "Active"}},
    use_data_source=True
)
```

**Always use `query_database_complete()`** instead of raw Notion API queries - it handles pagination automatically and returns complete results.

## Testing Agents

### Manual Testing

Test agents directly:

```python
from agents.inbox_agent import inbox_agent

response = inbox_agent.run("Save this article: https://example.com/article")
print(response.content)
```

### Testing Tools

Test tools independently:

```python
from tools.inbox_agent.notion_tools import create_task

result = create_task(
    name="Test task",
    status="Inbox",
    due_date="2026-01-20"
)
print(result)
```

## Common Patterns

### Loading Instructions

All agents use the same pattern:

```python
def load_instructions() -> str:
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".claude",
        "agents",
        "agent-name.md"
    )
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    
    return content.strip()
```

### Notion Client Singleton

All tools use the shared Notion client from `tools.common`:

```python
# In your tool file
from tools.common import get_notion_client

# Use it
client = get_notion_client()
```

The client is initialized once in `tools/common/notion_client.py` and reused across all agents. Don't create your own client - always import from `tools.common`.

### Environment Variables

Load from `env.txt`:

```python
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "env.txt"
))
```

## Dependencies

Key dependencies:
- `agno>=2.0.0` - Agent framework
- `anthropic>=0.18.0` - Claude API client
- `notion-client>=2.2.1` - Notion API client
- `httpx>=0.25.0` - HTTP client for URL fetching
- `python-dotenv>=1.0.0` - Environment variable loading

Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Agent Not Responding
- Check that instructions file exists and is readable
- Verify tools are properly imported and registered
- Check for syntax errors in agent file

### Tool Not Working
- Verify Notion API key is set in `env.txt`
- Check tool function signature matches usage
- Test tool independently to isolate issue

### Routing Issues
- Check router keywords match your use case
- Add more specific keywords if needed
- Consider using LLM-based routing for complex cases

## Shared Utilities Reference

### `tools/common/notion_client.py`

**`get_notion_client() -> Client`**
- Returns singleton Notion API client
- Handles API key loading from environment
- Raises `ValueError` if `NOTION_API_KEY` not set

**`query_database_complete(database_id: str, filter_dict: Optional[Dict] = None, use_data_source: bool = False) -> List[Dict]`**
- Queries Notion database with automatic pagination
- Returns complete list of results (all pages)
- `use_data_source=True` uses data source ID instead of database ID (for multi-source databases)
- Handles pagination cursor automatically

### `tools/common/constants.py`

All database IDs and shared constants:
- `TASKS_DB_ID` - Tasks database ID
- `TASKS_DATA_SOURCE_ID` - Tasks data source ID
- `PROJECTS_DB_ID` - Projects database ID
- `PROJECTS_DATA_SOURCE_ID` - Projects data source ID
- `RESOURCES_DB_ID` - Resources database ID
- `INSIGHTS_DB_ID` - Insights database ID
- `PM_COMPETENCY_MODEL_ID` - PM Competency Model page ID

**When to update constants:**
- If a database ID changes in Notion
- If a new shared database is added
- If a new shared page ID is needed

## Future Enhancements

- Add AgentOS for production runtime (FastAPI + UI)
- Implement LLM-based routing for better agent selection
- Add memory/storage for agents to remember context
- Add knowledge base for agentic RAG
- Add monitoring and logging
- Implement confidence scoring as a tool
