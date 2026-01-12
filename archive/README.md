# Archive

This directory contains legacy code that is no longer actively used but preserved for reference.

## Contents

- **`src/notion_api.py`** - Original monolithic Notion API client (567 lines)
  - Replaced by modular tools in `tools/` organized by agent
  - Functionality extracted into `tools/common/` (shared utilities) and agent-specific tool modules
  - Archived: January 2026

- **`test_notion_api.py`** - Tests for the original `src/notion_api.py`
  - Located in `archive/test_notion_api.py` (moved from root directory)
  - No longer relevant as the API has been refactored into tools
  - Archived: January 2026

## Why Archived

The codebase was refactored to use the Agno framework with:
- **Modular tools** organized by agent (`tools/inbox_agent/`, `tools/task_manager_agent/`, etc.)
- **Shared utilities** in `tools/common/` to eliminate duplication
- **Agent-based architecture** where each agent has its own tools and instructions

The old monolithic API served as a reference during migration but is no longer needed in the active codebase.
