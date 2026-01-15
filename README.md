# AIPOS - AI Personal Operating System

An AI-powered personal work system built with the [Agno framework](https://docs.agno.com/) that helps capture, organize, and act on tasks, knowledge, and ideas through natural conversation. AIPOS is your digital butler - efficient, witty, and always one step ahead.

## Overview

This system uses specialized AI agents that combine:
- **LLM reasoning** (Claude Sonnet) for intelligent decision-making
- **Deterministic tools** (Python functions) for reliable Notion API operations
- **Natural language interface** for frictionless interaction

Each agent has a specific role and expertise, working together to create a seamless workflow. Agents use deterministic tools (Python functions) to interact with Notion and other systems, while LLM reasoning guides decision-making.

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create env.txt with:
# NOTION_API_KEY=your_notion_api_key_here
```

### Usage

**Via Cursor Chat:**
Simply type your request naturally:
- "Save this article: [URL]" → Routes to Inbox Agent
- "What should I work on today?" → Routes to Task Manager Agent
- "Analyze this interview transcript" → Routes to Interview Assistant Agent

**Via Command Line:**
```bash
python main.py "What should I work on today?"
```

---

## Available Agents

### 1. Inbox Agent
**Purpose:** Capture anything quickly - tasks, resources, ideas

**Use for:**
- Saving articles, videos, tools
- Capturing customer observations, feature ideas, strategic thoughts
- Creating tasks with proper context
- Quick voice-dictated captures

**Examples:**
- "Save this article and remind me to read it: [URL]"
- "Customer said they'd pay 2x for automated monitoring"
- "Add task to review Q4 plan with Reid for Reporting Pod"

**Location:** 
- Agent code: `agents/inbox_agent.py`
- Instructions: `agents/instructions/inbox_agent.md`
- Tools: `tools/inbox_agent/`

---

### 2. Task Management Agent
**Purpose:** Review, prioritize, and manage your tasks intelligently

**Use for:**
- Daily review: "What should I work on today?"
- Inbox triage: "Help me process my inbox"
- Checking blockers: "What am I waiting on?"
- Status updates: "Mark these tasks done..."
- Weekly planning: "Help me plan this week"

**Examples:**
- "What should I work on today?"
- "Process my inbox"
- "Move hiring tasks to This Week"
- "Show me overdue tasks"

**Location:** 
- Agent code: `agents/task_manager_agent.py`
- Instructions: `agents/instructions/task_manager_agent.md`
- Tools: `tools/task_manager_agent/`

---

### 3. Interview Assistant Agent
**Purpose:** Evaluate candidates against PM competency model

**Use for:**
- Analyzing interview transcripts
- Comparing candidates
- Generating structured assessments

**Examples:**
- "Analyze this interview transcript against our PM competency model"
- "Assess candidate performance on product sense and execution"

**Location:**
- Agent code: `agents/interview_assistant_agent.py`
- Instructions: `agents/instructions/interview_assistant_agent.md`
- Tools: `tools/interview_assistant_agent/`

---

## How to Use This System

### For Quick Captures
Just start talking - I'll figure out what to do with it:
```
You: "Customer mentioned they need faster reporting"
Me: [Loads Inbox Agent, captures as idea]

You: "https://youtube.com/watch?v=xyz - save this"  
Me: [Loads Inbox Agent, creates resource + task]
```

### For Task Management
Be explicit about what you want to do:
```
You: "What should I work on today?"
Me: [Loads Task Management Agent, shows priorities]

You: "Help me process my inbox"
Me: [Loads Task Management Agent, triages with suggestions]
```

### Agent Selection Logic

I automatically choose the right agent based on your intent:

**Capture/Save signals** → Inbox Agent
- URLs, "save this", "remind me", "customer said", [screenshot]

**Task management signals** → Task Management Agent  
- "what should I work on", "process inbox", "mark done", "show me tasks"

**Assessment signals** → Interview Assistant Agent
- "assess interview", "evaluate candidate", "compare candidates"

If unclear, I'll ask which agent you want to use.

---

## Key Principles

### 1. Frictionless Capture
You shouldn't have to think about where things go or how to structure them. Just tell the system what you're thinking.

### 2. Actionable Tasks
Tasks must be concrete actions, not vague intentions:
- ❌ "Align on decision"
- ✅ "Send email to Reid and Paolo about decision"

### 3. Confidence-Based Execution
- >70% confidence: System acts, confirms after
- <70% confidence: System acts but flags for review

### 4. Context Over Hierarchy
Information is connected through relations and tags, not locked into folders. Search and filter dynamically.

### 5. Intelligence Over Automation
Agents provide smart suggestions and flag issues, not just mechanical execution.

---

## Common Workflows

### Morning Routine
```
You: "What should I work on today?"
[Reviews priorities, flags overdue items, suggests focus]
```

### Quick Capture
```
You: [Paste URL or thought]
[Automatically routes to right database with proper tags]
```

### Inbox Processing
```
You: "Process my inbox"  
[Suggests project links, statuses, due dates for batch approval]
```

### Weekly Planning
```
You: "Help me plan this week"
[Reviews projects, suggests tasks to activate, checks for stuck work]
```

### Follow-ups
```
You: "What am I waiting on?"
[Shows blocked tasks, suggests follow-ups for items >7 days]
```

---

## Tips for Working with Me

### Be Natural
Just talk normally - you don't need to specify databases, fields, or format things specially:
- ✅ "Add task to review Q4 plan with Reid next Friday"
- ❌ "Create entry in Tasks database with Name='Review Q4 plan' and Due='2026-01-17'"

### Batch Operations
Tell me multiple things at once, I'll handle them:
- "Mark done: email Paolo, review doc, schedule meeting"
- "Move all hiring tasks to This Week"

### Trust the System
If I'm >70% confident, I'll just do it. If something's wrong, you can always correct it later. The audit log tracks everything.

### Give Feedback
If I misclassify something or make a wrong suggestion, tell me. I learn from the patterns.

### Use Voice
This system is designed for voice dictation. Use MacWhisper to dictate, paste the text, and I'll handle it.

---

## System Architecture

### Notion Databases

**Core Work Databases:**
- **Tasks** - Actionable next steps (must be concrete actions)
- **Projects** - High-level ongoing initiatives  
- **Resources** - External content (articles, videos, tools)
- **Ideas** - Raw captures (observations, ideas, screenshots)
- **Meeting Transcripts** - Granola imports (read-only)

**Research & Intelligence:**
- **Competitor Tracker** - Market intelligence
- **Customer Conversations** - Research database

**Audit:**
- **System Audit Log** - Tracks all agent actions and confidence scores

### Work Areas (Tags)

Content is tagged across these dimensions:
- AI Strategy
- Product
- Market & Competitive
- Team & Hiring
- Technical
- Leadership

Multiple tags encouraged (e.g., "AI competitive tool" → AI Strategy + Market + Technical)

### Project Structure

```
/
├── agents/                    # Agno agent definitions (Python)
│   ├── inbox_agent.py
│   ├── task_manager_agent.py
│   ├── interview_assistant_agent.py
│   └── orchestrator_team.py  # Agno Team that routes user input to agents
│
├── agents/instructions/      # Agent instructions (markdown)
│   ├── inbox_agent.md
│   ├── task_manager_agent.md
│   └── interview_assistant_agent.md
│
├── tools/                     # Deterministic tools organized by agent
│   ├── common/               # Shared utilities
│   │   ├── notion_client.py  # get_notion_client, query_database_complete
│   │   └── constants.py      # Database IDs, shared constants
│   │
│   ├── inbox_agent/          # create_task, create_resource, create_idea, etc.
│   ├── task_manager_agent/   # get_daily_review, update_task, analyze_priorities, etc.
│   └── interview_assistant_agent/  # fetch_page, extract_competencies, etc.
│
├── context/                  # Reference documentation and work context
│   └── notion_taxonomy.md    # Database schemas and workflows
│
├── archive/                  # Legacy code (reference only)
│   └── src/notion_api.py    # Old monolithic API
│
└── main.py                   # Entry point for Cursor chat
```

### How It Works

1. **User Input**: You type natural language in Cursor chat
2. **Orchestration**: `orchestrator_team.py` (Agno Team) intelligently routes your input to the appropriate agent
3. **Agent Execution**: The agent uses its tools and LLM reasoning to complete the task
4. **Response**: Agent returns a formatted response with what it did

### Agno Framework

This system is built on [Agno](https://docs.agno.com/), a multi-agent framework that combines:
- **Agents**: LLM-powered decision makers with instructions and tools
- **Tools**: Deterministic Python functions for reliable operations (Notion API, URL fetching, etc.)
- **Orchestrator Team**: Agno Team that uses LLM reasoning to intelligently route requests to specialized agents

---

## Developer Guide

### Architecture Overview

This system uses the [Agno framework](https://docs.agno.com/) to build AI agents that combine:
- **LLM reasoning** (Claude Sonnet) for decision-making
- **Deterministic tools** (Python functions) for reliable operations
- **Instructions** (markdown files) for agent behavior

### Adding a New Agent

#### Step 1: Create Agent Instructions

Create a markdown file in `agents/instructions/` with agent instructions:

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

#### Step 2: Create Tools

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

#### Step 3: Create Agent File

Create `agents/my_new_agent.py`:

```python
"""My New Agent - does X, Y, Z."""

import os
from agno.agent import Agent
from agno.models.anthropic import Claude
from tools.my_new_agent import create_thing, update_thing


def load_instructions() -> str:
    """Load instructions from markdown file, skipping frontmatter."""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "my_new_agent.md"
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

#### Step 4: Add to Orchestrator Team

Update `agents/orchestrator_team.py` to add your agent as a team member:

```python
from .my_new_agent import my_new_agent

orchestrator_team = Team(
    # ... existing config ...
    members=[
        inbox_agent,
        task_manager_agent,
        context_gathering_agent,
        interview_assistant_agent,
        my_new_agent,  # Add your agent here
    ],
)
```

Then update `agents/instructions/orchestrator_team.md` to include routing instructions for your new agent.
    
    # ... existing routing logic
```

#### Step 5: Export Agent

Add to `agents/__init__.py`:

```python
from .my_new_agent import my_new_agent

__all__ = [..., "my_new_agent"]
```

### Adding Tools to Existing Agent

#### Step 1: Create Tool Function

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

#### Step 2: Export Tool

Add to `tools/inbox_agent/__init__.py`:

```python
from .notion_tools import new_tool_function

__all__ = [..., "new_tool_function"]
```

#### Step 3: Register Tool

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

### Tool Development Best Practices

#### 1. Error Handling

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

#### 2. Type Hints

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

#### 3. Docstrings

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

#### 4. Shared Utilities (`tools/common/`)

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

#### 5. Notion API Patterns

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

### Testing Agents

#### Manual Testing

Test agents directly:

```python
from agents.inbox_agent import inbox_agent

response = inbox_agent.run("Save this article: https://example.com/article")
print(response.content)
```

#### Testing Tools

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

### Common Patterns

#### Loading Instructions

All agents use the same pattern:

```python
def load_instructions() -> str:
    file_path = os.path.join(
        os.path.dirname(__file__),
        "instructions",
        "agent_name.md"
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

#### Notion Client Singleton

All tools use the shared Notion client from `tools.common`:

```python
# In your tool file
from tools.common import get_notion_client

# Use it
client = get_notion_client()
```

The client is initialized once in `tools/common/notion_client.py` and reused across all agents. Don't create your own client - always import from `tools.common`.

#### Environment Variables

Load from `env.txt`:

```python
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "env.txt"
))
```

### Troubleshooting

#### Agent Not Responding
- Check that instructions file exists and is readable
- Verify tools are properly imported and registered
- Check for syntax errors in agent file

#### Tool Not Working
- Verify Notion API key is set in `env.txt`
- Check tool function signature matches usage
- Test tool independently to isolate issue

#### Routing Issues
- Update orchestrator team instructions to include routing for your agent
- The orchestrator team uses LLM reasoning for routing - check team leader instructions in `agents/instructions/orchestrator_team.md`
- Improve routing by updating the team leader's understanding of when to route to each agent

### Shared Utilities Reference

#### `tools/common/notion_client.py`

**`get_notion_client() -> Client`**
- Returns singleton Notion API client
- Handles API key loading from environment
- Raises `ValueError` if `NOTION_API_KEY` not set

**`query_database_complete(database_id: str, filter_dict: Optional[Dict] = None, use_data_source: bool = False) -> List[Dict]`**
- Queries Notion database with automatic pagination
- Returns complete list of results (all pages)
- `use_data_source=True` uses data source ID instead of database ID (for multi-source databases)
- Handles pagination cursor automatically

#### `tools/common/constants.py`

All database IDs and shared constants:
- `TASKS_DB_ID` - Tasks database ID
- `TASKS_DATA_SOURCE_ID` - Tasks data source ID
- `PROJECTS_DB_ID` - Projects database ID
- `PROJECTS_DATA_SOURCE_ID` - Projects data source ID
- `RESOURCES_DB_ID` - Resources database ID
- `IDEAS_DB_ID` - Ideas database ID
- `PM_COMPETENCY_MODEL_ID` - PM Competency Model page ID

**When to update constants:**
- If a database ID changes in Notion
- If a new shared database is added
- If a new shared page ID is needed

---

## Reference Documentation

- **`context/notion_taxonomy.md`** - Complete database schemas, workflows, and rules
- **`context/rajiv_context.md`** - Rajiv's role, team, strategy, and decision-making context
- **`agents/instructions/`** - Detailed agent behavior instructions (loaded at runtime)

---

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

---

## Current Status

✅ **Live:**
- Inbox Agent (capture tasks, resources, ideas) - Built with Agno
- Task Management Agent (review, prioritize, process) - Built with Agno
- Interview Assistant Agent (analyze transcripts) - Built with Agno
- Resources database in Notion
- Agno-based architecture with tools and routing

🚧 **In Progress:**
- Ideas database (schema ready, not created)
- System Audit Log database (schema ready, not created)

📋 **Planned:**
- Context Retrieval Agent
- Weekly Planner Agent
- Artifact Generator Agent
- AgentOS integration for production runtime (FastAPI + UI)

---

## Getting Help

**If something doesn't work:**
1. Check the System Audit Log for what happened
2. Tell me what went wrong - I'll learn from it
3. Look at `context/notion_taxonomy.md` for database schemas

**If you're not sure what I can do:**
- Ask: "What can you help me with?"
- Tell me what you're trying to accomplish
- I'll either do it or tell you which agent to build next

---

## Philosophy

This isn't just a task manager or knowledge base - it's a thinking partner that:
- **Captures** without friction
- **Organizes** without your manual effort  
- **Surfaces** what matters when you need it
- **Learns** your patterns and priorities
- **Scales** as you add new capabilities

The goal: You focus on thinking and deciding. The system handles the rest.

---

## License

Private project - not for distribution.
