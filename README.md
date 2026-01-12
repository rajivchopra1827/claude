# Rajiv's Work Hub

> **Technical Reference for Developers**  
> This README provides technical documentation for developers working on or extending this system. For end-user guidance, see [`CLAUDE.md`](CLAUDE.md).

An AI-powered personal work system built with the [Agno framework](https://docs.agno.com/) that helps capture, organize, and act on tasks, knowledge, and insights through natural conversation.

## Overview

This system uses specialized AI agents that combine:
- **LLM reasoning** (Claude Sonnet) for intelligent decision-making
- **Deterministic tools** (Python functions) for reliable Notion API operations
- **Natural language interface** for frictionless interaction

Each agent has a specific role and expertise, working together to create a seamless workflow.

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

## Available Agents

### 1. Inbox Agent
**Purpose:** Capture anything quickly - tasks, resources, insights

**Use for:**
- Saving articles, videos, tools
- Capturing customer observations, feature ideas, strategic thoughts
- Creating tasks with proper context
- Quick voice-dictated captures

**Location:** 
- Agent code: `agents/inbox_agent.py`
- Instructions: `.claude/agents/inbox-ingester.md`
- Tools: `tools/inbox_agent/`

### 2. Task Management Agent
**Purpose:** Review, prioritize, and manage tasks intelligently

**Use for:**
- Daily review: "What should I work on today?"
- Inbox triage: "Help me process my inbox"
- Checking blockers: "What am I waiting on?"
- Status updates: "Mark these tasks done..."
- Weekly planning: "Help me plan this week"

**Location:** 
- Agent code: `agents/task_manager_agent.py`
- Instructions: `.claude/agents/task-manager.md`
- Tools: `tools/task_manager_agent/`

### 3. Interview Assistant Agent
**Purpose:** Evaluate candidates against PM competency model

**Use for:**
- Analyzing interview transcripts
- Comparing candidates
- Generating structured assessments

**Location:**
- Agent code: `agents/interview_assistant_agent.py`
- Instructions: `.claude/agents/interview-assistant.md`
- Tools: `tools/interview_assistant_agent/`

## Architecture

### Project Structure

```
/
├── agents/                    # Agno agent definitions
│   ├── inbox_agent.py
│   ├── task_manager_agent.py
│   ├── interview_assistant_agent.py
│   └── router.py             # Routes user input to agents
│
├── tools/                     # Deterministic tools
│   ├── common/               # Shared utilities
│   │   ├── notion_client.py  # get_notion_client, query_database_complete
│   │   └── constants.py      # Database IDs, shared constants
│   │
│   ├── inbox_agent/          # create_task, create_resource, etc.
│   ├── task_manager_agent/   # get_daily_review, update_task, etc.
│   └── interview_assistant_agent/  # fetch_competency_model, etc.
│
├── .claude/agents/          # Agent instructions (markdown)
│   ├── inbox-ingester.md
│   ├── task-manager.md
│   └── interview-assistant.md
│
├── archive/                  # Legacy code (reference only)
│   └── src/notion_api.py    # Old monolithic API
│
└── main.py                  # Entry point
```

### How It Works

1. **User Input**: You type natural language in Cursor chat or command line
2. **Routing**: `router.py` analyzes your input and selects the appropriate agent
3. **Agent Execution**: The agent uses its tools and LLM reasoning to complete the task
4. **Response**: Agent returns a formatted response with what it did

### Notion Integration

All agents interact with Notion databases:
- **Tasks** - Actionable next steps
- **Projects** - High-level ongoing initiatives
- **Resources** - External content (articles, videos, tools)
- **Insights** - Raw captures (observations, ideas, screenshots)
- **Meeting Transcripts** - Interview transcripts (read-only)

Database IDs and shared utilities are centralized in `tools/common/` for easy maintenance.

## Key Features

- **Frictionless Capture**: Just tell the system what you're thinking
- **Intelligent Routing**: Automatically selects the right agent for your request
- **Confidence-Based Execution**: Acts when confident (>70%), flags uncertainty otherwise
- **Context-Aware**: Links related items, suggests projects, infers metadata
- **Batch Operations**: Process multiple items efficiently

## Documentation

- **CLAUDE.md** - Main user guide and system overview
- **DEVELOPER_GUIDE.md** - Guide for extending and maintaining the system
- **.claude/agents/** - Detailed agent instructions
- **.claude/context/notion-taxonomy.md** - Complete database schemas

## Dependencies

Key dependencies:
- `agno>=2.0.0` - Agent framework
- `anthropic>=0.18.0` - Claude API client
- `notion-client>=2.2.1` - Notion API client
- `httpx>=0.25.0` - HTTP client for URL fetching
- `python-dotenv>=1.0.0` - Environment variable loading

## Development

See `DEVELOPER_GUIDE.md` for:
- Adding new agents
- Creating new tools
- Extending existing agents
- Testing and debugging

## License

Private project - not for distribution.
