# Rajiv's Work Hub

> **User Guide for End Users**  
> This guide explains how to use the system from a user perspective. For technical documentation, see [`README.md`](README.md).

An AI-powered personal work system that helps capture, organize, and act on tasks, knowledge, and insights through natural conversation.

## Overview

This system uses specialized AI agents built with the Agno framework to help manage work across Notion databases. Each agent has a specific role and expertise, working together to create a seamless workflow. Agents use deterministic tools (Python functions) to interact with Notion and other systems, while LLM reasoning guides decision-making.

---

## Quick Start

**Tell me what you want to do:**

- "I need to capture something" or just share a URL, thought, or observation → Inbox Agent
- "What should I work on today?" or "Help me plan my week" → Task Management Agent
- "Find everything about [topic]" → Context Retrieval Agent (coming soon)
- "Assess my interview with [candidate]" → Interview Assessor Agent (coming soon)

I'll automatically load the right agent and context.

---

## Available Agents

### 1. Inbox Agent
**Purpose:** Capture anything quickly - tasks, resources, insights

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
- Instructions: `.claude/agents/inbox-ingester.md`
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

**Location:** `.claude/agents/task-manager.md`

---

### 3. Context Retrieval Agent *(Coming Soon)*
**Purpose:** Find and synthesize information across your entire system

**Use for:**
- Finding related information across databases
- Answering questions about past work
- Pulling context for decisions
- Discovering patterns

---

### 4. Interview Assistant Agent
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
- Instructions: `.claude/agents/interview-assistant.md`
- Tools: `tools/interview_assistant_agent/`

---

## System Architecture

### Notion Databases

**Core Work Databases:**
- **Tasks** - Actionable next steps (must be concrete actions)
- **Projects** - High-level ongoing initiatives  
- **Resources** - External content (articles, videos, tools)
- **Insights** - Raw captures (observations, ideas, screenshots)
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

## How to Use This System

### For Quick Captures
Just start talking - I'll figure out what to do with it:
```
You: "Customer mentioned they need faster reporting"
Me: [Loads Inbox Agent, captures as insight]

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

### For Finding Things
*(Context Retrieval Agent - coming soon)*
```
You: "Show me everything about Reporting Pod"
Me: [Searches across all databases, presents with context]
```

---

## Agent Selection Logic

I automatically choose the right agent based on your intent:

**Capture/Save signals** → Inbox Agent
- URLs, "save this", "remind me", "customer said", [screenshot]

**Task management signals** → Task Management Agent  
- "what should I work on", "process inbox", "mark done", "show me tasks"

**Search/retrieval signals** → Context Retrieval Agent
- "find", "show me", "what did we learn", "everything about"

**Assessment signals** → Interview Assessor Agent
- "assess interview", "evaluate candidate", "compare candidates"

If unclear, I'll ask which agent you want to use.

---

## Technical Architecture

### Agno Framework
This system is built on [Agno](https://docs.agno.com/), a multi-agent framework that combines:
- **Agents**: LLM-powered decision makers with instructions and tools
- **Tools**: Deterministic Python functions for reliable operations (Notion API, URL fetching, etc.)
- **Router**: Intelligent routing to select the right agent based on user intent

### Project Structure
```
/
├── agents/                    # Agno agent definitions (Python)
│   ├── inbox_agent.py
│   ├── task_manager_agent.py
│   ├── interview_assistant_agent.py
│   └── router.py             # Routes user input to agents
│
├── tools/                     # Deterministic tools organized by agent
│   ├── inbox_agent/          # create_task, create_resource, create_insight, etc.
│   ├── task_manager_agent/  # get_daily_review, update_task, analyze_priorities, etc.
│   └── interview_assistant_agent/  # fetch_page, extract_competencies, etc.
│
├── .claude/agents/           # Agent instructions (markdown)
│   ├── inbox-ingester.md
│   ├── task-manager.md
│   └── interview-assistant.md
│
├── src/                      # Legacy code (reference)
│   └── notion_api.py
│
└── main.py                   # Entry point for Cursor chat
```

### How It Works
1. **User Input**: You type natural language in Cursor chat
2. **Routing**: `router.py` analyzes your input and selects the appropriate agent
3. **Agent Execution**: The agent uses its tools and LLM reasoning to complete the task
4. **Response**: Agent returns a formatted response with what it did

### Invocation
Agents are invoked through Cursor chat. Simply type your request naturally:
- "Save this article: [URL]" → Routes to Inbox Agent
- "What should I work on today?" → Routes to Task Manager Agent
- "Analyze this interview transcript" → Routes to Interview Assistant Agent

You can also use `main.py` directly:
```bash
python main.py "What should I work on today?"
```

## System Reference Files

- **System Map** (`.claude/context/notion-taxonomy.md`) - Complete database schemas, workflows, rules
- **Agent Instructions** (`.claude/agents/*.md`) - Detailed behavior for each agent (loaded into agents at runtime)
- **Agent Code** (`agents/*.py`) - Agno agent definitions with tool registration
- **Tools** (`tools/*/`) - Deterministic Python functions for each agent
- **This File** (`CLAUDE.md`) - Quick reference and onboarding

---

## Current Status

✅ **Live:**
- Inbox Agent (capture tasks, resources, insights) - Built with Agno
- Task Management Agent (review, prioritize, process) - Built with Agno
- Interview Assistant Agent (analyze transcripts) - Built with Agno
- Resources database in Notion
- Agno-based architecture with tools and routing

🚧 **In Progress:**
- Insights database (schema ready, not created)
- System Audit Log database (schema ready, not created)

📋 **Planned:**
- Context Retrieval Agent
- Weekly Planner Agent
- Artifact Generator Agent
- AgentOS integration for production runtime (FastAPI + UI)

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

## Getting Help

**If something doesn't work:**
1. Check the System Audit Log for what happened
2. Tell me what went wrong - I'll learn from it
3. Look at `.claude/context/notion-taxonomy.md` for database schemas

**If you're not sure what I can do:**
- Ask: "What can you help me with?"
- Tell me what you're trying to accomplish
- I'll either do it or tell you which agent to build next

**If you want to extend the system:**
- Create new agent: Add Python file in `agents/` (e.g., `agents/new_agent.py`)
- Add instructions: Create markdown file in `.claude/agents/` (e.g., `new-agent.md`)
- Create tools: Add tool modules in `tools/new_agent/` (e.g., `notion_tools.py`)
- Register agent: Add to `agents/router.py` for routing
- Reference `.claude/context/notion-taxonomy.md` for database access
- See `DEVELOPER_GUIDE.md` for detailed instructions (coming soon)

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

Ready to work? Just tell me what you need.