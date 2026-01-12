# Claude Personal OS

## Overview

This is Rajiv's Claude-integrated personal operating system—a local-first workspace that mirrors Notion with SQLite for structured data and Markdown for documents. Claude agents work here to capture inputs, organize knowledge, and manage tasks with zero friction.

## Architecture

**Structured Data (SQLite)**
- Tasks - Individual actionable items
- Projects - Containers for related work
- Resources - Knowledge base (articles, videos, tools, research)
- Insights - Observations, ideas, patterns, strategic thoughts
- Meeting Transcripts - Meeting notes and context

**Document Storage (Markdown)**
- `/data/documents/` - Long-form reference materials by domain
- `/data/meetings/` - Meeting agendas organized by team

## Key Concept: Inbox-First Capture

When Rajiv provides input (text, URL, screenshot, idea), agents classify it and route to the right place:
- **Task** → actionable items with deadlines
- **Resource** → external content to remember/learn
- **Insight** → observations/ideas/patterns not yet actionable
- **Project** → container for related work

## Notion Integration

All databases sync with Notion for long-term storage and sharing. Use these data source IDs for API queries:

- Tasks: `collection://2d3e6112-fa50-80e9-8a3a-000bc4723604`
- Projects: `collection://2d3e6112-fa50-8015-8921-000b39445099`
- Resources: `collection://276649c7-5cd6-46bd-8409-ddfa36addd5d`
- Insights: `collection://b9105b1d-6bdb-44f2-993b-40e324d1ba28`
- Meeting Transcripts: `collection://29fe6112-fa50-800c-86a8-000b97eb3fd6`

## Work Areas (for tagging/filtering)

- **AI Strategy** - AI/ML/LLM/automation/agentic systems
- **Product** - Product/features/roadmap/EPD
- **Market & Competitive** - Competitor/market/customer intelligence
- **Team & Hiring** - Hiring/recruiting/team/org
- **Technical** - Technical/architecture/engineering
- **Leadership** - Company/ELT/board/strategy

## Agent Behavior

### Inbox Agent
Routes all incoming items to the right database. See `.claude/agents/inbox-agent.md` for detailed rules.

**Golden Rule:** Bias toward action. If >70% confident, create the entry. Mention confidence if lower.

### Task Actionability
Tasks MUST be concrete next actions:
- ❌ "Align X decision"
- ✅ "Send Slack to A, B, C about X decision"

Help convert vague intentions to specific actions before creating tasks.

### Project Priority Limits
- P1: Maximum 1 active project
- P2: Maximum 3 active projects
- P3: Maximum 5 active projects

## File Structure

```
/Users/rajivchopra/Claude/
├── CLAUDE.md                    (this file)
├── README.md                    (architecture overview)
├── .claude/
│   ├── agents/
│   │   ├── inbox-agent.md       (detailed inbox agent instructions)
│   │   └── interview-data-extractor.md
│   └── context/
│       └── notion-taxonomy.md   (Notion structure reference)
├── src/
│   ├── database.py              (SQLite schema and helpers)
│   ├── api.py                   (Clean API for agents)
│   └── sync.py                  (Background sync to Notion)
└── requirements.txt
```

## Common Workflows

1. **Capture External Resource**
   - Fetch URL metadata
   - Infer Type and Work Area
   - Create Resource entry
   - If "remind me" → also create Task

2. **Create Task with Project Context**
   - Search Projects database for mentioned project
   - Parse due date
   - Create Task linked to Project
   - Confirm

3. **Capture Insight/Observation**
   - Determine Type (Customer Observation, Feature Idea, Strategic Thought, etc.)
   - Infer Work Area
   - Create Insight with Status: Inbox

4. **Task Management**
   - Convert vague intentions to concrete actions
   - Default status: Inbox (triage later)
   - Link to Projects and Resources when context is clear

## Key Rules

- Tasks are actionable next steps, not intentions
- Default status for new items: Inbox
- Use Waiting field on Tasks if blocked on someone
- Link related items (Task → Project/Resource, Resource → Project/Task)
- Confidence scores on auto-tagged items (especially Work Area inference)
- All databases sync to Notion as source of truth

## Reference

For full Notion structure details, see `.claude/context/notion-taxonomy.md`.

For detailed Inbox Agent behavior, see `.claude/agents/inbox-agent.md`.
