# Rajiv's Notion Structure Map

This document maps your core Notion databases and how they interconnect. Use this as the canonical reference for agents navigating your workspace.

## Core Databases

### Tasks
**URL:** https://www.notion.so/2d3e6112fa50800495a7fb6b41a2bdd8
**Purpose:** Individual task management
**Data Source ID:** `collection://2d3e6112-fa50-80e9-8a3a-000bc4723604`

**Key Properties:**
- **Name** (Title): Task description
- **Status** (Status): Inbox → Backlog → Waiting → This Week → On Deck → Top Priority → Done
- **Due** (Date): When task is due
- **Completed** (Date): When task was marked done
- **Project** (Relation): Links to Projects database
- **Resources** (Relation): Links to Resources database
- **Waiting** (Multi-select): Blocking factors/owners (📅 Meeting, Megan, Paolo, Reid, Cassidy, JD, Jason, Ricardo, Devik, Randa, Lauren, Melissa, Aaron, External)
- **Root Project** (Formula): Auto-calculated parent project

**Views:**
- **Today**: Quick view of current work
- **Inbox**: Incoming tasks to triage
- **Waiting**: Tasks blocked on something/someone
- **Weekly Review**: All tasks with priority/project context
- **Completed**: Archived completed tasks (list view)
- **Tasks Database**: Main table view with all properties

**Rules:**
- Tasks MUST be actionable ("Send email to X" not "Align on X")
- Default status: Inbox
- Active Status Priorities: Top Priority > On Deck > This Week > Waiting
- Default project: None (assign during triage)
- Use Waiting field if blocked on someone


---

### Projects
**URL:** https://www.notion.so/2d3e6112fa50802bae32f7868a52d84c
**Purpose:** Container for related tasks; larger work items with priority and resource allocation
**Data Source ID:** `collection://2d3e6112-fa50-8015-8921-000b39445099`

**Key Properties:**
- **Name** (Title): Project name
- **Priority** (Select): P1 (Max=1) → P2 (Max=3) → P3 (Max=5) → Monitoring → Done
- **Due** (Date): Project deadline
- **Completed** (Date): When project finished
- **Tasks** (Relation): Links to Tasks database
- **Sub-item** (Relation): Self-relations for nested projects/epics
- **Parent item** (Relation): Self-relations for hierarchy
- **Resources** (Relation): Links to Resources database
- **This Week** (Checkbox): Marks projects active this week
- **Actionable Tasks** (Formula): Count of non-Done tasks
- **Waiting Tasks** (Formula): Count of tasks in Waiting status

**Views:**
- **This Week**: Priority-grouped view of weekly projects
- **Task Planning**: All projects with task counts
- **Weekly Prioritization**: Priority tier breakdown
- **Completed**: Timeline view of finished projects

**Rules:**
- P1 = max 1 project, P2 = max 3, P3 = max 5
- Projects can be hierarchical (parent/sub-items) - but unless otherwise stated tasks should be added to the main project

---

### Resources
**URL:** https://www.notion.so/67b98aee3f514662bbb92fd6dcdaf2ee
**Purpose:** Knowledge base - articles, videos, podcasts, papers, tools, books
**Data Source ID:** `collection://276649c7-5cd6-46bd-8409-ddfa36addd5d`

**Key Properties:**
- **Name** (Title): Resource title
- **Type** (Select): Article | Video | Podcast | Paper/Report | Tool/Product | Book | Other
- **Area** (Select): AI | EPD | Organization | Research & Insight | Leadership
- **Status** (Status): Inbox → Active → Archived
- **URL** (URL): Link to resource
- **Summary** (Text): Key takeaways or AI-generated summary
- **Source** (Text): Where found (HN, Twitter, email, etc.)
- **Related Projects** (Relation): Links to Projects
- **Related Tasks** (Relation): Links to Tasks
- **Confidence Score** (Number): 0-100 for auto-tagged items
- **Tags** (Multi-select): Custom tags (currently empty)

**Views:**
- **Default view**: Table with all properties, filterable by Area/Status/Type

---

### Ideas
**URL:** https://www.notion.so/e1c6bd6b4c8d4ef2b0dbc679e408254a
**Purpose:** Capture observations, ideas, strategic thoughts, patterns, and questions that are not yet actionable but worth remembering
**Data Source ID:** `collection://b9105b1d-6bdb-44f2-993b-40e324d1ba28`

**Key Properties:**
- **Title** (Title): Idea title
- **Type** (Select): Customer Observation | Feature Idea | Strategic Thought | Data/Screenshot | Pattern | Question
- **Work Area** (Multi-select): AI Strategy | Product | Market & Competitive | Team & Hiring | Technical | Leadership
- **Status** (Status): Inbox → Processed → Archived
- **Content** (Text): Rich idea details, supports embedding images
- **Source** (Text): Where/how the idea was captured
- **Related Projects** (Relation): Links to Projects database
- **Related Tasks** (Relation): Links to Tasks database
- **Confidence Score** (Number): 0-100 for uncertain tagging

**Views:**
- **Default view**: Table with Type, Work Area, Status, and relationships visible

**Rules:**
- Default status: Inbox
- Use when capturing non-actionable observations, customer quotes, ideas, or strategic thoughts
- Link to related Projects/Tasks when context is clear

---

### Meeting Transcripts
**URL:** https://www.notion.so/29fe6112fa5080609d34cf9063bc3706
**Purpose:** Store meeting notes and auto-extract topics/attendees
**Data Source ID:** `collection://29fe6112-fa50-800c-86a8-000b97eb3fd6`

**Key Properties:**
- **Name** (Title): Meeting name/topic
- **Date** (Date): Meeting date (MM/DD/YYYY format)
- **Attendees** (Text): Comma-separated list
- **Attendees (Split)** (Formula): Auto-parsed attendee list
- **Notes** (Text): Meeting notes/transcript
- **Topics** (Formula): Auto-extracted topics
- **URL** (URL): Link to transcript or recording

**Views:**
- **Default view**: Table sorted by date descending

---

## Root Pages (Private Space)

### Documents
**URL:** https://www.notion.so/156e6112fa5080bd9f05f5a7e6068354
**Purpose:** Hub for organized documentation by domain
**Type:** Root page with sub-pages

**Contains:**
- **ELT** - Engineering, Leadership, Technical docs
- **AI** - AI-related documents and research
- **EPD** - Engineering & Product documentation
- **Ideas / Research** - Research findings and ideas
- **Personal** - Personal workspace items
- **AI Resources** - AI-specific resource library

---

### 1:1s / Meeting Agendas
**URL:** https://www.notion.so/156e6112fa508018aec1df2faa6a17ab
**Purpose:** Hub for 1:1 agendas and team meeting notes, organized by team
**Type:** Root page with sub-pages organized by team

**ELT Team:**
- Devik / Rajiv
- All-Hands

**EPD Team:**
- Aaron <> Rajiv 1:1
- Cassidy / Rajiv
- EPD Staff Meeting
- Matt Woods (PM)
- Megan Haase (Ops)
- Megan / Rajiv - Career Monthly
- Melissa / Rajiv - 1:1
- Melissa / Rajiv - Career Monthly
- Paolo / Rajiv - 1:1
- Reporting Pod

**Agency:**
- EPD Agency Liaisons Bi-Weekly
- Agency <> EPD Leads Sync
- Chip / Rajiv
- Kelly / Rajiv
- Shannon / Rajiv
- Rayann / Rajiv
- Jenny / Rajiv
- Marketing x EPD

---

## Relationships Map

```
Projects
  ├─ Tasks (1:many) - Project relation on Tasks points here
  ├─ Sub-items (self-relation, hierarchical) - Can nest projects
  ├─ Parent item (self-relation) - Links to parent project
  ├─ Resources (many:many)
  └─ Ideas (many:many) - Related Projects relation

Tasks
  ├─ Project (many:1) - Points to Projects database
  ├─ Resources (many:many) - Links to Resources database
  └─ Ideas (many:many) - Related Tasks relation on Ideas

Resources
  ├─ Related Projects (many:many) - Links to Projects database
  └─ Related Tasks (many:many) - Links to Tasks database

Ideas
  ├─ Related Projects (many:many) - Links to Projects database
  ├─ Related Tasks (many:many) - Links to Tasks database
  └─ Standalone capture of observations/ideas/questions

Meeting Transcripts
  └─ Standalone (can be manually linked to Documents or 1:1s pages)

Documents
  └─ Root hub for topic-specific sub-pages and databases (not a database itself)

1:1s / Meeting Agendas
  └─ Root hub for recurring meeting agendas organized by team (not a database itself)
```

---

## Key Patterns

1. **Status-driven task workflow:** Tasks move through a linear status pipeline. Status determines visibility and priority.
2. **Priority-driven project workflow:** Projects are constrained by priority tiers (P1 max 1, P2 max 3, P3 max 5).
3. **Relational linking:** Resources, Tasks, and Projects are cross-linked to preserve context across the system.
4. **Hierarchical nesting:** Projects can contain sub-projects; Documents and 1:1s pages organize content hierarchically by topic/team.
5. **Formula automation:** Auto-calculations reduce manual work (Actionable Tasks count, Waiting Tasks count, auto-parsed attendees, extracted topics).
6. **Multiple views:** Same databases have different views optimized for different contexts (e.g., Tasks: Today view vs Weekly Review view).

---

## When to Use What

- **Add a Task** when you have a single actionable item with a due date
- **Add a Project** when you have multiple related tasks or work spanning multiple weeks
- **Add a Resource** when you find something worth remembering/using (articles, tools, research, etc.)
- **Add an Idea** when you have an observation, idea, customer quote, pattern, or strategic thought that's not yet actionable
- **Add Meeting Transcript** after meetings to preserve context; topics/attendees auto-extract
- **Documents** for static reference materials organized by domain (best for long-form, FYI content)
- **1:1s / Meeting Agendas** to prep for and track recurring conversations organized by team

---

## Agent Reference Guide

### To find information about a specific area:
- **AI topics** → Resources database (filter Area=AI), Ideas (filter Work Area=AI Strategy), or Documents > AI
- **EPD work** → Projects/Tasks (filter), Ideas (filter Work Area=Product), Documents > EPD, or 1:1s > EPD Team section
- **Meetings & decisions** → Meeting Transcripts, Ideas (ideas/strategic thoughts), or 1:1s / Meeting Agendas pages
- **Tools & references** → Resources database (filter Type=Tool/Product)
- **Ideas & observations** → Ideas database (filter by Type: Feature Idea, Customer Observation, Strategic Thought)
- **Long-form docs** → Documents hub by domain
- **Rajiv's role/context** → Use `get_work_context()` tool for role, team structure, strategic priorities, decision framework
- **Strategic documents** → See Key Reference Documents section above (EPD Strategy, AI V2MOM, Strategic Presentation)

### To create connections:
- When creating a Task: link to its Project and any related Resources
- When creating a Project: link to Resources and any Sub-items
- When creating a Resource: link to Related Projects/Tasks for context

### Data source IDs for API queries:
- Tasks: `collection://2d3e6112-fa50-80e9-8a3a-000bc4723604`
- Projects: `collection://2d3e6112-fa50-8015-8921-000b39445099`
- Resources: `collection://276649c7-5cd6-46bd-8409-ddfa36addd5d`
- Ideas: `collection://b9105b1d-6bdb-44f2-993b-40e324d1ba28`
- Meeting Transcripts: `collection://29fe6112-fa50-800c-86a8-000b97eb3fd6`

---

## Key Reference Documents

### PM Competency Model
**URL:** https://www.notion.so/digible/232e6112fa50802692b6ef43788abce5  
**Use Case:** Evaluating PM candidates in interviews

### EPD Strategy 2026
**URL:** https://www.notion.so/digible/EPD-Strategy-2026-Refresh-2ade6112fa50804799c8fbb9f3687e74  
**Use Case:** Reference for strategic decisions

### AI V2MOM
**URL:** https://www.notion.so/digible/AI-V2MOM-2e8e6112fa50803091cecae487eb7231  
**Use Case:** AI strategy and vision alignment

### Strategic Presentation
**URL:** https://docs.google.com/presentation/d/1vXVw7gigwEWCoVv1Q-cd9J7uk5iaHg0R0wczV40Pvys/edit?slide=id.g3467a16400a_0_6#slide=id.g3467a16400a_0_6  
**Use Case:** High-level strategic overview and company priorities

### Rajiv's Work Context
**Location:** `context/rajiv_context.md` (local file)  
**Use Case:** Rajiv's role, team structure, strategic priorities, decision-making framework, and success metrics. Accessible via `get_work_context()` tool in Context Gathering Agent.

---


## Common Workflows

### 1. Capture External Resource
**Trigger:** User shares URL with "save this" or "remind me to read"

**Steps:**
1. Fetch URL metadata (title, description)
2. Infer Type based on URL pattern (youtube.com → Video, etc.)
3. Infer Work Area from content
4. Create Resource entry with Status: To Review, Confidence Score
5. If user said "remind me", create Task linked to Resource
6. Confirm what was done

**Example:**
```
User: "Save this and remind me to watch: https://youtube.com/watch?v=xyz"
→ Create Resource: Type=Video, Work Area=AI Strategy (inferred), Status=To Review
→ Create Task: "Watch: [video title]", Status=Inbox, Related Resource=[link]
→ Respond: "Saved to Resources (AI Strategy). Task created in Inbox."
```

### 2. Create Task with Project Context
**Trigger:** User describes a task mentioning a project

**Steps:**
1. Search Projects database for mentioned project name
2. Extract due date if mentioned (parse "next Friday", "Monday", etc.)
3. Determine status (default: Inbox unless specified)
4. Create task with project relation
5. Confirm with project name and due date

**Example:**
```
User: "Add task to review Q4 plan with Reid for Reporting Pod due next Friday"
→ Search Projects: "Reporting Pod" → Found: [URL]
→ Parse date: "next Friday" → 2026-01-17
→ Create Task: Name="Review Q4 plan with Reid", Project=[Reporting Pod], Due=2026-01-17, Status=Inbox
→ Respond: "Created task in Reporting Pod project, due Jan 17"
```

### 3. Capture Idea/Observation
**Trigger:** User shares something that's not actionable yet but worth remembering

**Steps:**
1. Determine Type (customer observation, feature idea, strategic thought, etc.)
2. Infer Work Area
3. Create Idea with Status: Inbox
4. Confirm capture

**Example:**
```
User: "Customer just said they'd pay 2x for automated competitive monitoring"
→ Create Idea: Type=Customer Observation, Work Area=Market & Competitive + AI Strategy, 
   Content=[quote], Status=Inbox
→ Respond: "Captured as customer observation (Market + AI Strategy)"
```

### 4. Interview Assessment
**Trigger:** User asks to assess a candidate interview

**Steps:**
1. Fetch PM Competency Model page
2. Search Meeting Transcripts for candidate name
3. Analyze transcript against competency criteria
4. Provide structured assessment
5. Optionally: Create task for follow-up or decision

**Example:**
```
User: "Analyze my interview with Doug against PM competency model"
→ Fetch competency model
→ Search transcripts: "Doug" → Found recent interview
→ Analyze against: Product Sense, Execution, Leadership, etc.
→ Provide assessment with evidence from transcript
```

### 5. Task Management - Converting Intention to Action
**Trigger:** User states an intention that needs to become concrete task

**Steps:**
1. Identify if stated intention is already actionable
2. If not, help convert to specific next action
3. Create task with actionable phrasing

**Example:**
```
User: "I need to align the X decision"
→ Claude: "To make this actionable: who needs to be aligned and how?"
User: "Send Slack to A, B, C"
→ Create Task: "Send Slack message to A, B, C to align X decision"
```

---

## Confidence Scoring & Review Queue

**When to use confidence scores:**
- Auto-tagging Work Areas: High confidence = >80%, Medium = 60-80%, Low = <60%
- Auto-determining Type: Similar thresholds
- Auto-linking to Projects: High confidence only >80%

**Review Queue Logic:**
- Confidence <70% → Mark for review
- User can query "show me review queue" to see uncertain items
- Items in review stay functional but flagged for human verification

---

## Important Constraints

### What Can't Be Databases
- Strategy artifacts (EPD Strategy, AI V2MOM, etc.) - need individual permissions, stored as Notion pages or external documents
- 1:1 meeting agendas - need individual permissions
- Process documentation - need individual permissions
- Work context - stored locally in `context/rajiv_context.md` for easy updates and agent access

### Task Actionability Rule
Tasks MUST be concrete next actions. If user states an intention:
- ❌ "Align X decision" 
- ✅ "Send Slack to A, B, C about X decision"

Help convert intentions to actions before creating tasks.

### Project Priority Limits
- P1: Maximum 1 project
- P2: Maximum 3 projects
- P3: Maximum 5 projects
Flag if user tries to exceed these limits.

---

## Search Strategy

**Primary method:** Context-based search (user wants this most)

When user asks to find something:
1. Search across relevant databases (Tasks, Projects, Resources, Ideas, Meeting Transcripts)
2. Filter by Work Area if context suggests (Ideas: AI Strategy, Product, Market & Competitive, Team & Hiring, Technical, Leadership)
3. Look for relations (e.g., "show me everything about Reporting Pod" → project + tasks + resources + related ideas)
4. Present results with context about where they came from

**Example:**
```
User: "What have we learned about AI competitive landscape?"
→ Search Resources: Work Area contains "AI Strategy" + "Market & Competitive"
→ Search Ideas: Same filters
→ Search Competitor Tracker: AI-related companies
→ Present synthesized view with links

---

## Recent Changes

**January 2026:**
- Added **work context system** - Context Gathering Agent now has access to Rajiv's work context via `get_work_context()` tool
- Added **AI V2MOM** and **Strategic Presentation** to Key Reference Documents
- Updated agent reference guide to include work context and strategic document access

**January 12, 2026:**
- Added **Ideas database** as a core database for capturing observations, ideas, strategic thoughts, patterns, and questions
- Updated relationships map to show Ideas connections to Projects and Tasks
- Updated search strategy and agent reference guide to include Ideas
- Added data source ID for Ideas: `collection://b9105b1d-6bdb-44f2-993b-40e324d1ba28`

Last updated: January 2026
