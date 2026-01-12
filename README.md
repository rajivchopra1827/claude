# Claude Personal OS

A local-first, version-controlled system that mirrors your Notion workspace with SQLite for structured data and Markdown for documents.

## Architecture

### Structured Data (SQLite)
- **Tasks** - Individual actionable items
- **Projects** - Containers for related tasks
- **Resources** - Knowledge base (articles, videos, tools, etc.)
- **Insights** - Observations, ideas, strategic thoughts
- **Meeting Transcripts** - Meeting notes

### Document Storage (Markdown)
- `/data/documents/` - Long-form reference materials organized by domain
  - `ELT/` - Engineering, Leadership, Technical
  - `AI/` - AI-related documents
  - `EPD/` - Engineering & Product
  - `insights-research/` - Research findings
  - `personal/` - Personal workspace items
  - `ai-resources/` - AI-specific resources
- `/data/meetings/` - Meeting agendas organized by team
  - `ELT-team/`
  - `EPD-team/`
  - `Agency/`

## Workflow

1. **Agents write to local SQLite** - Instant operations, no network latency
2. **Background sync daemon** - Periodically pushes changes to Notion (every 15-30 min)
3. **Notion stays as archive** - Long-term storage and sharing source of truth

## Files

- `src/database.py` - SQLite schema and database helpers
- `src/api.py` - Clean API for agents (e.g., `create_task()`, `update_project()`)
- `src/sync.py` - Background daemon that syncs local changes to Notion

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize the database
python src/database.py

# Start the sync daemon
python src/sync.py
```

## Data Source IDs (for Notion sync)

- Tasks: `collection://2d3e6112-fa50-80e9-8a3a-000bc4723604`
- Projects: `collection://2d3e6112-fa50-8015-8921-000b39445099`
- Resources: `collection://276649c7-5cd6-46bd-8409-ddfa36addd5d`
- Insights: `collection://b9105b1d-6bdb-44f2-993b-40e324d1ba28`
- Meeting Transcripts: `collection://29fe6112-fa50-800c-86a8-000b97eb3fd6`
