# Rajiv's Work Hub

An AI-powered personal work system that helps capture, organize, and act on tasks, knowledge, and insights through natural conversation.

## Overview

This system uses specialized agents to help manage work across Notion databases. Each agent has a specific role and expertise, working together to create a seamless workflow.

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

**Location:** `agents/inbox-agent.md`

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

**Location:** `agents/task-management-agent.md`

---

### 3. Context Retrieval Agent *(Coming Soon)*
**Purpose:** Find and synthesize information across your entire system

**Use for:**
- Finding related information across databases
- Answering questions about past work
- Pulling context for decisions
- Discovering patterns

---

### 4. Interview Assessor Agent *(Coming Soon)*
**Purpose:** Evaluate candidates against PM competency model

**Use for:**
- Analyzing interview transcripts
- Comparing candidates
- Generating structured assessments

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

## System Reference Files

- **System Map** (`context/system-map.md`) - Complete database schemas, workflows, rules
- **Agent Instructions** (`agents/*.md`) - Detailed behavior for each agent
- **This File** (`CLAUDE.md`) - Quick reference and onboarding

---

## Current Status

✅ **Live:**
- Inbox Agent (capture tasks, resources, insights)
- Task Management Agent (review, prioritize, process)
- Resources database in Notion
- System Audit Log for transparency

🚧 **In Progress:**
- Insights database (schema ready, not created)
- System Audit Log database (schema ready, not created)

📋 **Planned:**
- Context Retrieval Agent
- Interview Assessor Agent
- Weekly Planner Agent
- Artifact Generator Agent

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
3. Look at `context/system-map.md` for database schemas

**If you're not sure what I can do:**
- Ask: "What can you help me with?"
- Tell me what you're trying to accomplish
- I'll either do it or tell you which agent to build next

**If you want to extend the system:**
- New agent ideas go in `agents/` as `.md` files
- Follow the pattern of existing agents
- Reference `context/system-map.md` for database access

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